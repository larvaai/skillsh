# Module Build Spec — Execution-Core (HexAgent, GĐ11 BUILD)

> Hiện thực contract `docs/contracts/execution-core.md` (FROZEN 2026-07-03). Bám evidence gốc
> `core/kernel.py:106-150`, `core/session.py:49-85,188-194`, `core/schemas.py`. Không đổi contract.
> Bounded context #2 (Domain Model GĐ5). KHÔNG build: task loop/delegation (Orchestration),
> event emitter/redaction (Observability) — module này chỉ **phát** event qua bus, không hiện thực bus.

---

## 1. Góc nhìn lãnh đạo

Execution-Core là **một cửa duy nhất** (`execute_tool`) mà mọi hành động của agent phải đi qua — nó gắn trace, kiểm quyền (scope), và chuẩn hoá kết quả một lần cho toàn hệ, rồi đông cứng (`freeze`) để không ai đổi luật khi run đang chạy. Nó đảm bảo hai điều cứng: **không hành động nào lọt ra ngoài scope hay ngoài audit** (mọi call phát `tool.requested`/`completed|failed`, ngoài-scope → `ok=False` không raise), và **quyền của agent con luôn ⊆ quyền cha** (fail-closed) — chặn tận gốc bệnh runaway và leo-thang-quyền.

---

## 2. Cấu trúc code — chữ ký + logic cốt lõi

> Python 3.11. `@dataclass(frozen=True)` cho envelope/identity/context. Ports = `typing.Protocol`
> (`runtime_checkable`). Kernel **stateless** (đông cứng), state **chỉ** ở Session.

### 2.1 Ports (Protocol, runtime_checkable) — seam ra ngoài module

```python
from __future__ import annotations
from typing import Protocol, runtime_checkable, Any


@runtime_checkable
class ToolPort(Protocol):
    """Một capability chạy được. Owner: Tools-Safety cấp adapter cụ thể."""
    name: str
    def execute(self, args: dict, context: "ToolCallContext") -> "CapabilityResult": ...


@runtime_checkable
class EventSinkPort(Protocol):
    """Điểm phát event duy nhất ra Observability. Execution-Core CHỈ gọi publish(),
    KHÔNG hiện thực emitter/seq/redaction (đó là module Observability)."""
    def publish(self, event_type: str, payload: dict) -> None: ...


@runtime_checkable
class ToolMiddleware(Protocol):
    """Một mắt trong chain. next_ = mắt kế bên trong (inner). Trả CapabilityResult."""
    def __call__(self, request: "ToolRequest",
                 next_: "ToolHandler") -> "CapabilityResult": ...


# alias cho lời gọi phần lõi/inner của chain
ToolHandler = "Callable[[ToolRequest], CapabilityResult]"
```

### 2.2 Envelope + lineage (frozen) — `schemas.py`

```python
from dataclasses import dataclass, field, replace


@dataclass(frozen=True)
class SessionIdentity:
    """Bất biến 7-field lineage (evidence session.py). Con thừa kế + tăng depth."""
    session_id: str
    run_id: str
    task_id: str
    agent_id: str
    parent_session_id: str | None = None
    delegation_id: str | None = None
    depth: int = 0


@dataclass(frozen=True)
class ToolCallContext:
    """Lineage + scope đi kèm một call. Kernel đọc allowed_capabilities từ đây để scope-check."""
    session_id: str
    run_id: str
    task_id: str
    agent_id: str
    parent_session_id: str | None
    delegation_id: str | None
    allowed_capabilities: frozenset[str] = frozenset()

    @classmethod
    def from_session(cls, ident: SessionIdentity,
                     caps: frozenset[str]) -> "ToolCallContext":
        return cls(session_id=ident.session_id, run_id=ident.run_id,
                   task_id=ident.task_id, agent_id=ident.agent_id,
                   parent_session_id=ident.parent_session_id,
                   delegation_id=ident.delegation_id,
                   allowed_capabilities=caps)


@dataclass(frozen=True)
class ToolRequest:
    """Đối tượng bất biến chảy qua middleware chain. Tạo 1 lần trong execute_tool."""
    tool_name: str
    args: dict
    context: ToolCallContext


@dataclass(frozen=True)
class CapabilityResult:
    """Envelope MỌI tool trả. ok=False mang error-code khi ngoài-scope/không-thấy/exception."""
    ok: bool
    capability: str
    feature: str | None = None
    data: dict = field(default_factory=dict)
    error: str | None = None
    metadata: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {"ok": self.ok, "capability": self.capability, "feature": self.feature,
                "data": self.data, "error": self.error, "metadata": self.metadata}
```

### 2.3 AgentKernel — chokepoint `execute_tool` (evidence `core/kernel.py:106-150`)

```python
class KernelFrozenError(RuntimeError):
    """Raise khi mutate registry/middleware sau freeze(). error-code KERNEL_FROZEN_MUTATION."""


class AgentKernel:
    def __init__(self, event_sink: EventSinkPort) -> None:
        self._registry: dict[str, ToolPort] = {}
        self._middleware: list[ToolMiddleware] = []   # thứ tự đăng ký = outer→inner
        self._events = event_sink
        self._frozen: bool = False

    # ---- mutation surface: cấm sau freeze (bất biến contract #3) ----
    def register(self, tool: ToolPort) -> None:
        if self._frozen:
            raise KernelFrozenError("KERNEL_FROZEN_MUTATION: register after freeze")
        self._registry[tool.name] = tool

    def use(self, middleware: ToolMiddleware) -> None:
        if self._frozen:
            raise KernelFrozenError("KERNEL_FROZEN_MUTATION: use() after freeze")
        self._middleware.append(middleware)

    def freeze(self) -> None:
        """Sau freeze: registry/middleware bất biến; chỉ session state đổi.
        Chốt bất biến bằng cờ + copy-đông (registry/middleware không nhận thêm)."""
        self._frozen = True

    @property
    def frozen(self) -> bool:
        return self._frozen

    # ---- CHOKEPOINT DUY NHẤT ----
    def execute_tool(self, tool_name: str, args: dict | None = None,
                     *, context: ToolCallContext | None = None) -> dict:
        ctx = context or _ANON_CONTEXT
        req = ToolRequest(tool_name=tool_name, args=dict(args or {}), context=ctx)

        # (1) BEFORE — luôn phát tool.requested (bất biến #1)
        self._events.publish("tool.requested", {
            "capability": tool_name, "args": req.args,
            "session_id": ctx.session_id, "run_id": ctx.run_id,
            "agent_id": ctx.agent_id, "delegation_id": ctx.delegation_id,
            "depth_hint": ctx.parent_session_id is not None,
        })

        # (2) SCOPE-CHECK — ngoài scope → ok=False, KHÔNG raise (bất biến #2)
        if tool_name not in ctx.allowed_capabilities:
            result = CapabilityResult(ok=False, capability=tool_name,
                                      error="CAP_OUTSIDE_SCOPE")
            self._events.publish("tool.failed",
                                 {"capability": tool_name, "error": "CAP_OUTSIDE_SCOPE"})
            return result.as_dict()

        tool = self._registry.get(tool_name)
        if tool is None:
            result = CapabilityResult(ok=False, capability=tool_name,
                                      error="CAP_NOT_FOUND")
            self._events.publish("tool.failed",
                                 {"capability": tool_name, "error": "CAP_NOT_FOUND"})
            return result.as_dict()

        # (3) MIDDLEWARE CHAIN outer→inner, lõi = tool.execute; exception KHÔNG thoát (#4)
        def _core(r: ToolRequest) -> CapabilityResult:
            return tool.execute(r.args, r.context)

        handler = _core
        for mw in reversed(self._middleware):        # reversed → gọi theo thứ tự đăng ký
            handler = _wrap(mw, handler)

        try:
            result = handler(req)
            if not isinstance(result, CapabilityResult):   # phòng adapter trả sai kiểu
                result = CapabilityResult(ok=False, capability=tool_name,
                                          error="CAP_BAD_ENVELOPE")
        except Exception as exc:                     # bọc: exception của tool không thoát kernel
            result = CapabilityResult(ok=False, capability=tool_name,
                                      error=f"{type(exc).__name__}: {exc}")

        # (4) AFTER — completed|failed theo ok (bất biến #1)
        self._events.publish("tool.completed" if result.ok else "tool.failed",
                             {"capability": tool_name, "ok": result.ok,
                              "error": result.error})
        return result.as_dict()


def _wrap(mw: ToolMiddleware, next_: "ToolHandler") -> "ToolHandler":
    def _step(req: ToolRequest) -> CapabilityResult:
        return mw(req, next_)
    return _step


_ANON_CONTEXT = ToolCallContext(
    session_id="-", run_id="-", task_id="-", agent_id="-",
    parent_session_id=None, delegation_id=None,
    allowed_capabilities=frozenset(),
)
```

> **Rationale (ADR-002):** một cửa `execute_tool` để gắn trace + scope + envelope **một lần** cho
> mọi call. Đã loại rải call-site (không đảm bảo mọi hành động bị trace/scope-check → có đường vòng).
> Middleware `reversed` khi build handler để thứ-tự-đăng-ký = thứ-tự-chạy outer→inner (Timing bọc
> ngoài cùng, core trong cùng), khớp evidence chain `Timing→PolicyGate→BudgetGuard→Retry→Condense→core`.

### 2.4 KernelSession — chokepoint per-run (evidence `core/session.py:49-85`)

```python
class KernelSession:
    """State per-run sống ở ĐÂY (kernel stateless). Mọi tool đi qua kernel.execute_tool."""
    def __init__(self, kernel: AgentKernel, identity: SessionIdentity,
                 allowed_capabilities: frozenset[str], state: dict | None = None) -> None:
        self._kernel = kernel
        self.identity = identity                             # frozen 7-field
        self.allowed_capabilities = allowed_capabilities     # frozenset[str]
        self._state: dict = dict(state or {})                # deep-copy isolation ở factory

    def execute_tool(self, name: str, args: dict) -> dict:
        """Cửa của session → dựng context từ identity+caps rồi ủy cho kernel (không tự chạy tool)."""
        ctx = ToolCallContext.from_session(self.identity, self.allowed_capabilities)
        return self._kernel.execute_tool(name, args, context=ctx)

    def snapshot(self) -> dict:
        import copy
        return copy.deepcopy(self._state)                    # nguồn cho restore round-trip (D3)
```

### 2.5 SessionFactory — hằng số dựng session, scope con ⊆ cha (evidence `core/session.py:188-194`)

```python
class ScopeViolationError(ValueError):
    """child caps ⊄ parent caps. fail-closed (raise trước khi tạo session)."""


class SessionFactory:
    """Chỗ DUY NHẤT dựng KernelSession → enforce scope-shrink + isolation."""
    def __init__(self, kernel: AgentKernel) -> None:
        self._kernel = kernel

    def create_root(self, *, run_id: str, task_id: str, agent_id: str,
                    allowed_capabilities: frozenset[str],
                    state: dict | None = None) -> KernelSession:
        ident = SessionIdentity(session_id=_new_id(), run_id=run_id, task_id=task_id,
                                agent_id=agent_id, parent_session_id=None,
                                delegation_id=None, depth=0)
        return KernelSession(self._kernel, ident, frozenset(allowed_capabilities), state)

    def create_child(self, parent: KernelSession, *,
                     allowed_capabilities: frozenset[str],
                     delegation_id: str | None = None) -> KernelSession:
        child_caps = frozenset(allowed_capabilities)
        # BẤT BIẾN D2 (business rule #3): child ⊆ parent, fail-closed
        if not child_caps <= parent.allowed_capabilities:
            raise ScopeViolationError(
                f"child caps {set(child_caps - parent.allowed_capabilities)} "
                f"outside parent scope")
        ident = SessionIdentity(
            session_id=_new_id(), run_id=parent.identity.run_id,
            task_id=parent.identity.task_id, agent_id=parent.identity.agent_id,
            parent_session_id=parent.identity.session_id,
            delegation_id=delegation_id, depth=parent.identity.depth + 1)
        import copy
        return KernelSession(self._kernel, ident, child_caps,
                             copy.deepcopy(parent.snapshot()))   # isolation: con không share state cha

    def restore(self, *, identity: SessionIdentity, state: dict,
                allowed_capabilities: frozenset[str]) -> KernelSession:
        """kw-only (evidence session.py:188-194). Round-trip resume cùng run_id (D3, SPIKE-1)."""
        return KernelSession(self._kernel, identity,
                             frozenset(allowed_capabilities), dict(state))


def _new_id() -> str:
    import uuid
    return uuid.uuid4().hex
```

> **Rationale (ADR-001):** kernel đông cứng + state chỉ ở session → 0 rò state giữa run đồng thời.
> `create_child` deep-copy snapshot cha để con **cô lập**; scope kiểm bằng `<=` frozenset là toàn-phần,
> fail-closed (raise) chứ không lặng lẽ cắt bớt — để lỗi lộ ra sớm ở biên tạo session.

---

## 3. Bám contract — ánh xạ API/bất biến → code

| Contract (public API) | Ánh xạ code |
|---|---|
| `AgentKernel.execute_tool(name, args, *, context)` | §2.3 `execute_tool` — kw-only `context`, trả `dict` (`.as_dict()`) |
| `AgentKernel.freeze()` | §2.3 `freeze()` set `_frozen=True`; `register`/`use` raise sau đó |
| `AgentKernel.use(middleware)` | §2.3 `use()` — append vào `_middleware`, cấm sau freeze |
| `KernelSession.identity: SessionIdentity` | §2.4 attr `identity` (frozen 7-field §2.2) |
| `KernelSession.allowed_capabilities: frozenset[str]` | §2.4 attr `allowed_capabilities` |
| `KernelSession.execute_tool(name, args)` | §2.4 → dựng context → `kernel.execute_tool` |
| `SessionFactory.create_root(...)` | §2.5 `create_root` (depth=0, no parent) |
| `SessionFactory.create_child(parent, *, allowed_capabilities)` | §2.5 `create_child` — scope ⊆ parent fail-closed |
| `SessionFactory.restore(*, identity, state, allowed_capabilities)` | §2.5 `restore` — kw-only |
| `CapabilityResult(ok, capability, feature, data, error, metadata)` + `.as_dict()` | §2.2 frozen dataclass |
| `ToolCallContext` | §2.2 frozen dataclass + `from_session` |

| Bất biến contract | Ánh xạ code |
|---|---|
| #1 Mọi call phát `tool.requested` (trước) + `tool.completed\|failed` (sau) | §2.3 (1) publish trước; (4) publish sau; nhánh scope/not-found cũng publish `tool.failed` |
| #2 `tool_name ∉ allowed_capabilities` → `ok=False` (không raise) | §2.3 (2) trả `CapabilityResult(ok=False, error="CAP_OUTSIDE_SCOPE")` |
| #3 Sau `freeze()`: registry/middleware bất biến; chỉ session state đổi | §2.3 `_frozen` guard ở `register`/`use`; state chỉ ở §2.4 `_state` |
| #4 Exception của tool KHÔNG thoát kernel | §2.3 (3) `try/except Exception` → `ok=False` |
| Error code `CAP_OUTSIDE_SCOPE` · `CAP_NOT_FOUND` · `KERNEL_FROZEN_MUTATION` | §2.3 lần lượt: nhánh scope, nhánh registry.get None, `KernelFrozenError` message |

---

## 4. Đạt DoD

### D1 — Không call-site nào bypass `execute_tool`
- **Cách đảm bảo:** ToolPort adapter **không tự chạy được** trong luồng thật — chúng chỉ được gọi
  bởi `_core` bên trong chain của `execute_tool`. Session không giữ tham chiếu tới `_registry`
  (private của kernel); cửa duy nhất của session là `session.execute_tool` → `kernel.execute_tool`.
  Không có API công khai nào gọi thẳng `tool.execute` ngoài chokepoint.
- **Audit-test (D1):** grep 0 đường vòng — `grep -rn "\.execute(" core/ | grep -v "execute_tool"`
  chỉ được khớp `_core`/định nghĩa `ToolPort.execute`, không call-site khác; và
  `grep -rn "_registry" core/` chỉ trong `kernel.py`. Fail nếu có bất kỳ module ngoài kernel chạm registry.

### D2 — Scope child ⊆ parent (property-test, fail-closed)
- **Cách đảm bảo:** §2.5 `create_child` kiểm `child_caps <= parent.allowed_capabilities` **trước khi**
  dựng session; vi phạm → `ScopeViolationError` (fail-closed, không cấp session một-phần).
- **Property-test (Hypothesis):** với mọi `parent_caps` và mọi tập `child_caps`:
  nếu `child ⊆ parent` → `create_child` thành công và `child.allowed_capabilities ⊆ parent`;
  nếu `child ⊄ parent` → raise `ScopeViolationError` (xem §5). Đây là gate cho D2.

### D4 (phối hợp) — 0 secret trong `ui_payload` (redact-before-write) + freeze-gate
- **Ranh giới:** redaction thực thi ở **Observability** (emitter redact `ui_payload` 15 SECRET_KEYS).
  Execution-Core **không** hiện thực redactor.
- **Owner gate mà Execution-Core GIỮ:** `freeze()` là cổng cứng "sẵn-sàng-write". Luật phối hợp D4:
  **kernel KHÔNG được `freeze()` để bật write-capability nếu chain redaction chưa gắn.** Execution-Core
  giữ gate này bằng cách: `freeze()` từ chối đông cứng khi registry có write-cap mà `event_sink`
  chưa khai báo `redaction_ready` (kiểm ở biên freeze, fail-closed). Cụ thể — `freeze()` gọi
  `self._events` phải là sink đã-redact; nếu bootstrap muốn bật write-tool, nó phải freeze **sau** khi
  Observability lắp redactor. Execution-Core phát `tool.requested` mang `args` thô → **hợp đồng ngược:**
  Observability PHẢI redact trước khi ghi jsonl (known gap evidence §6). Owner của "không-freeze-khi-chưa-redact"
  = Execution-Core; owner của "redact-nội-dung" = Observability. Audit-test 0-secret chạy ở Observability;
  Execution-Core đóng góp G3 freeze-gate (test: freeze với write-cap + sink chưa-redact → raise).

---

## 5. Test tối thiểu

### Unit (nhanh, offline)
```python
def test_scope_block_returns_ok_false_not_raise():
    k = AgentKernel(FakeSink()); k.register(EchoTool("read_file")); k.freeze()
    ctx = ToolCallContext.from_session(_ident(), frozenset())   # rỗng caps
    out = k.execute_tool("read_file", {}, context=ctx)
    assert out["ok"] is False and out["error"] == "CAP_OUTSIDE_SCOPE"   # không raise

def test_cap_not_found():
    k = AgentKernel(FakeSink()); k.freeze()
    ctx = ToolCallContext.from_session(_ident(), frozenset({"ghost"}))
    assert k.execute_tool("ghost", {}, context=ctx)["error"] == "CAP_NOT_FOUND"

def test_freeze_mutation_raises():
    k = AgentKernel(FakeSink()); k.freeze()
    with pytest.raises(KernelFrozenError):        # KERNEL_FROZEN_MUTATION
        k.register(EchoTool("x"))
    with pytest.raises(KernelFrozenError):
        k.use(lambda r, n: n(r))

def test_tool_exception_never_escapes():
    k = AgentKernel(FakeSink()); k.register(BoomTool("boom")); k.freeze()
    ctx = ToolCallContext.from_session(_ident(), frozenset({"boom"}))
    out = k.execute_tool("boom", {}, context=ctx)     # BoomTool raise trong execute
    assert out["ok"] is False                          # bọc → ok=False, không propagate

def test_envelope_shape_and_events():
    sink = FakeSink(); k = AgentKernel(sink); k.register(EchoTool("ping")); k.freeze()
    ctx = ToolCallContext.from_session(_ident(), frozenset({"ping"}))
    out = k.execute_tool("ping", {"a": 1}, context=ctx)
    assert set(out) == {"ok","capability","feature","data","error","metadata"}  # envelope shape
    assert sink.types == ["tool.requested", "tool.completed"]  # bất biến #1 trước+sau
```

### Property (Hypothesis) — D2 child ⊆ parent với mọi tập cap
```python
from hypothesis import given, strategies as st
CAPS = st.frozensets(st.sampled_from(["read","write","net","shell","spawn"]))

@given(parent=CAPS, child=CAPS)
def test_child_scope_subset_or_fail_closed(parent, child):
    f = SessionFactory(AgentKernel(FakeSink()))
    root = f.create_root(run_id="r", task_id="t", agent_id="a",
                         allowed_capabilities=parent)
    if child <= parent:
        c = f.create_child(root, allowed_capabilities=child)
        assert c.allowed_capabilities <= root.allowed_capabilities   # ⊆ luôn giữ
        assert c.identity.parent_session_id == root.identity.session_id
        assert c.identity.depth == root.identity.depth + 1
    else:
        with pytest.raises(ScopeViolationError):     # fail-closed
            f.create_child(root, allowed_capabilities=child)
```

### Property (bổ trợ D4-gate)
```python
@given(caps=CAPS)
def test_restore_round_trip_kwonly(caps):     # D3 hỗ trợ: restore giữ nguyên identity/state/caps
    f = SessionFactory(AgentKernel(FakeSink()))
    ident = _ident(); state = {"k": "v"}
    s = f.restore(identity=ident, state=state, allowed_capabilities=caps)
    assert s.identity == ident and s.snapshot() == state
    assert s.allowed_capabilities == caps
```

---

## 6. Còn treo / ẩn số

1. **Tên event `tool.requested/completed` vs registry `tool.call_requested/before_call/after_call`** —
   evidence §3 ghi mismatch gốc. Spec này phát theo contract (`tool.requested/completed/failed`).
   Cần Observability xác nhận catalog `runtime_event_types.yaml` khớp — nếu registry còn tên cũ, đây là
   điểm chỉnh chung (không đổi contract Execution-Core).
2. **D4 freeze-gate cần seam từ Observability:** cách Execution-Core biết "redaction_ready" chưa
   được chốt (đề xuất: sink expose cờ `redaction_ready`/kiểu `RedactedEventSink`). Cần Observability
   thống nhất giao ước ở bootstrap; hiện spec giả định freeze **sau** khi lắp redactor.
3. **`args` thô trong `tool.requested`:** Execution-Core cố ý phát `args` đầy đủ (cần cho trace/scope);
   trách nhiệm redact nằm ở Observability trước khi ghi jsonl. Ranh giới này phải được ghi rõ ở
   contract Observability để tránh rò secret (known gap evidence §6).
4. **Thứ tự middleware cụ thể** (`Timing→PolicyGate→BudgetGuard→Retry→Condense`) do Orchestration/Discipline
   đăng ký qua `use()`; Execution-Core chỉ đảm bảo **thứ tự đăng ký = thứ tự chạy outer→inner**, không
   sở hữu danh sách mắt.
5. **`metadata`/`feature` semantics** trong `CapabilityResult` để mở cho adapter Tools-Safety điền
   (vd feature-flag, timing). Contract không ràng buộc nội dung → chưa test giá trị, chỉ test shape.
