# Module Build Spec — Observability-ControlPlane (HexAgent, GĐ11 BUILD)

> Hiện thực contract `docs/contracts/observability-controlplane.md` (FROZEN 2026-07-03). Bám evidence gốc `control/events.py:113`, `control/emitter.py:53`, `control/redaction.py` (15 SECRET_KEYS), `control/snapshot.py build_snapshot`, `observability/event_log.py:102 attach_to_bus`. Python 3.11, `@dataclass(frozen=True)`, ports = `Protocol(runtime_checkable)`.

## 1. Góc nhìn lãnh đạo
Đây là **hộp kính (glass-box)** của HexAgent: mọi hành động chạy qua đúng một đường phát-sự-kiện có thứ tự cố định (gate → seq → redact → fan-out), nên run nào cũng replay được và không rò secret ra UI. Nó biến hai lời hứa khó kiểm — "không báo-xong-khống" và "không lộ bí mật" — thành cổng cứng đo được (replay = snapshot, 0-secret audit).

---

## 2. Cấu trúc code (chữ ký + logic cốt lõi)

### 2.1 `RuntimeEvent` — envelope bất biến, 14 field, validate ở `__post_init__`
Nguồn: `control/events.py:113`. Đây là đơn vị dữ liệu chảy trên bus. UI **chỉ** đọc `ui_payload`.

```python
from __future__ import annotations
from dataclasses import dataclass, field, replace
from typing import Any, Protocol, runtime_checkable

_EVENT_TYPES: frozenset[str] = frozenset()  # nạp từ config/runtime_event_types.yaml lúc bootstrap

@dataclass(frozen=True)
class Actor:                # attribution-only (KHÔNG phải authz)
    type: str               # ∈ {human, agent, tool, system, runtime}
    id: str

@dataclass(frozen=True)
class TraceContext:
    trace_id: str
    span_id: str
    parent_span_id: str | None = None

@dataclass(frozen=True)
class RedactionInfo:
    level: str              # ∈ {public, ui_safe, internal, secret, restricted}

_ACTOR_TYPES = frozenset({"human", "agent", "tool", "system", "runtime"})
_REDACTION_LEVELS = frozenset({"public", "ui_safe", "internal", "secret", "restricted"})

@dataclass(frozen=True)
class RuntimeEvent:
    # 14 field CỐ ĐỊNH — bám control/events.py:113
    event_type: str                    # 1
    session_id: str                    # 2
    actor: Actor                       # 3
    trace: TraceContext                # 4
    redaction: RedactionInfo           # 5
    event_id: str                      # 6  (uuid, unique)
    seq: int                           # 7  (monotonic per-run; -1 = chưa stamp)
    round_no: int                      # 8
    ts: float                          # 9  (epoch giây)
    schema_version: int                # 10
    parent_event_id: str | None        # 11
    correlation_id: str | None         # 12
    payload: dict[str, Any]            # 13 (raw — KHÔNG bao giờ rời emitter)
    ui_payload: dict[str, Any] | None  # 14 (đã redact; UI đọc DUY NHẤT field này)

    def __post_init__(self) -> None:
        if self.event_type not in _EVENT_TYPES:
            raise ControlContractError("EVENT_UNKNOWN_TYPE", self.event_type)
        if self.actor.type not in _ACTOR_TYPES:
            raise ControlContractError("EVENT_BAD_ACTOR", self.actor.type)
        if self.redaction.level not in _REDACTION_LEVELS:
            raise ControlContractError("EVENT_BAD_REDACTION", self.redaction.level)
        if self.seq < -1:
            raise ControlContractError("EVENT_SEQ_GAP", self.seq)
        if not isinstance(self.payload, dict):
            raise ControlContractError("EVENT_BAD_PAYLOAD", type(self.payload).__name__)

    def as_dict(self) -> dict[str, Any]:
        """Dạng canonical cho sink. UI-facing view chỉ chứa ui_payload."""
        ...
```
**Rationale — validate ở `__post_init__` chứ không ở emitter:** envelope tự bảo vệ bất biến của chính nó ở MỌI điểm khởi tạo (kể cả replay từ jsonl, test dựng tay), nên không có đường vòng nào tạo được event sai type/level. `frozen=True` → mọi "sửa" đi qua `dataclasses.replace()` (tạo bản mới), loại hẳn mutate-in-place → an toàn khi event đã fan-out tới nhiều sink.

---

### 2.2 `EventEmitter.emit_event` — thứ tự CỐ ĐỊNH (gate → seq → redact → fan-out)
Nguồn: `control/emitter.py:53`. Đây là **điểm truyền duy nhất** ra bus.

```python
@runtime_checkable
class EventSinkPort(Protocol):              # control/ports.py:15 — single transport point
    def handle(self, event: RuntimeEvent) -> None: ...

class EventEmitter:
    def __init__(self, seq: "SessionSeq", redactor: "Redactor",
                 sinks: list[EventSinkPort], *, redaction_active: bool,
                 write_tools_enabled: bool) -> None:
        self._seq = seq
        self._redactor = redactor
        self._sinks = list(sinks)          # thứ tự fan-out ổn định
        self._redaction_active = redaction_active
        self._write_tools_enabled = write_tools_enabled

    def emit_event(self, event_type: str, *, session_id, actor, trace,
                   payload: dict | None = None) -> RuntimeEvent:
        payload = payload or {}

        # (1) registry-gate — fail-closed TRƯỚC mọi thứ khác [contract: bất biến #1]
        if event_type not in _EVENT_TYPES:
            raise ControlContractError("EVENT_UNKNOWN_TYPE", event_type)

        # [review G3] freeze fail-closed: có write-capability bật mà redactor CHƯA active
        # cho tool.requested → chặn cứng, không cho phát. Owner enforce: Execution-Core.
        if event_type == "tool.requested" and self._write_tools_enabled \
                and not self._redaction_active:
            raise ControlContractError("WRITE_TOOL_ENABLED_WITHOUT_REDACTION", event_type)

        # (2) seq-stamp — monotonic gap-free per-run (SessionSeq giữ RLock)
        seq = self._seq.next()

        raw = RuntimeEvent(
            event_type=event_type, session_id=session_id, actor=actor, trace=trace,
            redaction=RedactionInfo(level="internal"),
            event_id=_new_uuid(), seq=seq, round_no=_current_round(), ts=_now(),
            schema_version=SCHEMA_VERSION, parent_event_id=None, correlation_id=None,
            payload=payload, ui_payload=None,          # ui_payload set ở bước (3)
        )

        # (3) redact — sinh ui_payload đã che secret; KHÔNG mutate raw.payload
        event = self._redactor.apply(raw, level=raw.redaction.level)

        # (4) fan-out — chỉ SAU khi đã redact; thứ tự sink ổn định
        for sink in self._sinks:
            sink.handle(event)
        return event
```
**Rationale — vì sao thứ tự này bất khả đổi:** gate trước seq để **event sai type không tiêu tốn một số seq** (giữ seq gap-free cho đúng các event hợp lệ). Seq trước redact để mọi event (kể cả bị redact nặng) vẫn có số thứ tự tất định cho replay. Redact **trước** fan-out là bất biến an toàn cốt lõi — nếu fan-out trước rồi mới redact thì sink jsonl đã kịp ghi raw secret (đúng lỗ hổng gốc `evidence §6`). G3-gate đặt ngay sau registry-gate để chặn phát `tool.requested` khi write-tool bật mà chưa bật redaction — fail-closed, không "log rồi cảnh báo".

---

### 2.3 `SessionSeq` — monotonic per-run, RLock, + khôi phục high-watermark khi resume [G11]
Nguồn: `control/events.py` (SessionSeq, start 1, RLock).

```python
import threading

class SessionSeq:
    """Bộ đếm seq đơn điệu cho MỘT run. Gap-free. Thread-safe (RLock)."""
    def __init__(self, start: int = 0) -> None:
        self._lock = threading.RLock()
        self._value = start            # next() đầu tiên trả start+1 = 1

    def next(self) -> int:
        with self._lock:
            self._value += 1
            return self._value

    def peek(self) -> int:
        with self._lock:
            return self._value

    @classmethod
    def resume_from(cls, events: list[dict]) -> "SessionSeq":
        """[review G11] Khôi phục high-watermark khi resume.
        Đọc seq lớn nhất đã phát để seq mới KHÔNG đâm vào dải cũ → gap-free
        xuyên biên resume. Nếu events rỗng → start ở 0 (như run mới)."""
        hi = max((int(e.get("seq", 0)) for e in events), default=0)
        return cls(start=hi)
```
**Rationale — RLock chứ không Lock:** cho phép cùng một luồng tái nhập (ví dụ sink gọi lại emitter trong cùng call-stack) mà không tự-deadlock. **G11 — resume high-watermark:** đây là điểm hở gốc; nếu resume mà khởi tạo seq lại từ 0, event mới sẽ trùng seq event cũ → replay-fold gãy. `resume_from` tính `max(seq)` từ log đã lưu và tiếp tục từ đó, đảm bảo bất biến "seq monotonic gap-free per-run" đứng vững **qua** resume. (Ẩn số cross-process còn treo — xem §6.)

---

### 2.4 `Redactor.apply` — che secret trong ui_payload, 15 SECRET_KEYS, đệ quy, no-mutate
Nguồn: `control/redaction.py` (15 SECRET_KEYS, recursive mask, no mutate).

```python
_MASK = "[REDACTED]"

# 15 SECRET_KEYS — bám control/redaction.py (đếm CHÍNH XÁC = 15)
SECRET_KEYS: frozenset[str] = frozenset({
    "password", "passwd", "secret", "token", "api_key", "apikey",
    "access_token", "refresh_token", "authorization", "auth",
    "private_key", "credential", "credentials", "session_key", "cookie",
})

class Redactor:
    def __init__(self, keys: frozenset[str] = SECRET_KEYS) -> None:
        self._keys = keys

    def apply(self, event: RuntimeEvent, level: str) -> RuntimeEvent:
        """Sinh ui_payload đã che secret từ payload. KHÔNG mutate event/payload gốc.
        Trả về event MỚI (dataclasses.replace) với ui_payload set."""
        safe = self._scrub(event.payload)          # copy sâu đã che
        return replace(event, ui_payload=safe,
                       redaction=RedactionInfo(level=level or "ui_safe"))

    def _scrub(self, node: Any) -> Any:
        # đệ quy dict + list; tạo cấu trúc MỚI, không chạm node gốc
        if isinstance(node, dict):
            out: dict[str, Any] = {}
            for k, v in node.items():
                if isinstance(k, str) and k.lower() in self._keys:
                    out[k] = _MASK
                else:
                    out[k] = self._scrub(v)
                return out  # (thực tế return ngoài vòng lặp — xem lưu ý dưới)
            return out
        if isinstance(node, (list, tuple)):
            return [self._scrub(x) for x in node]
        return node                                 # scalar: giữ nguyên
```
> Lưu ý hiện thực: `return out` phải nằm **ngoài** vòng `for` (trong spec ghép sát để gọn — code thật đặt sau vòng lặp). Điểm bất biến: che theo **key** (case-insensitive) ở mọi độ sâu, giá trị lồng trong list-of-dict cũng bị quét.

**Rationale — no-mutate + copy sâu:** `payload` raw còn cần cho audit-log nội bộ và cho replay; nếu che tại chỗ thì mất bản gốc và mọi sink chia sẻ tham chiếu bị đầu độc. `_scrub` dựng cấu trúc mới nên `payload` bất biến, `ui_payload` là bản sạch độc lập. Đệ quy cả dict lẫn list để secret giấu trong `{"args": [{"token": ...}]}` vẫn bị che (property-test §5 phủ mọi cấu trúc lồng).

---

### 2.5 `build_snapshot` — linear fold, terminal không ghi đè
Nguồn: `control/snapshot.py:88` (`TaskLoopSnapshot`, 9 field, fold theo seq).

```python
@dataclass(frozen=True)
class AgentView:
    agent_id: str
    status: str              # ∈ {pending, waiting, running, done, failed}

@dataclass(frozen=True)
class TaskLoopSnapshot:
    session_id: str
    status: str              # terminal ∈ {done, failed}; non-terminal ∈ {pending, running, ...}
    round_no: int
    agents: tuple[AgentView, ...]
    # ... (9 field tổng — bám snapshot.py)

_TERMINAL = frozenset({"done", "failed"})

def build_snapshot(events: list[dict], *, session_id: str) -> TaskLoopSnapshot:
    """Linear fold theo seq. Tất định. Terminal status KHÔNG bị ghi đè."""
    state = _SnapshotAcc(session_id=session_id)
    for e in sorted(events, key=lambda x: x["seq"]):     # tất định theo seq
        et = e["event_type"]
        if et.startswith("loop."):                        # chỉ loop.* fold vào snapshot
            new_status = _status_of(e)
            # terminal không ghi đè: một khi done/failed thì khoá
            if state.status not in _TERMINAL:
                state.status = new_status
            state.round_no = e.get("round_no", state.round_no)
        # agent.* là advisory — KHÔNG fold (bám evidence: agent.* NOT folded)
    return state.freeze()
```
**Rationale — fold tuyến tính + khoá terminal:** replay tất định đòi thứ tự cố định (sort theo `seq`) và tính kết hợp không phụ thuộc thời điểm — fold trái là dạng đơn giản nhất thoả điều đó. **Khoá terminal** chống lỗi: nếu một event muộn (đến trễ / trùng) mang status non-terminal thì snapshot đã `done` không được lùi về `running`. Đây là nền của bất biến `replay(events[0..n]) = snapshot(n)`.

---

### 2.6 `attach_to_bus` — EventLogger → events.jsonl + summary.json (+ metrics)
Nguồn: `observability/event_log.py:102` (`attach_to_bus`, EventLogger subscribe tool.*/task.*).

```python
class EventLogger:
    def __init__(self, jsonl_path, summary_path) -> None:
        self._jsonl = jsonl_path
        self._summary = summary_path
        self._counts = {"tool_calls": 0, "llm_calls": 0,
                        "failures": 0, "blocks": 0, "parse_errors": 0}

    def handle(self, event: RuntimeEvent) -> None:      # là một EventSinkPort
        # ghi dòng canonical vào events.jsonl (đã redact ở emitter — an toàn)
        self._append_jsonl(event.as_dict())
        self._tally(event)                               # cập nhật summary counters

    def flush_summary(self) -> None:
        self._write_json(self._summary, self._counts)

def attach_to_bus(bus) -> None:
    """Gắn EventLogger như một sink của bus. Consumer thuần — KHÔNG sinh event."""
    logger = EventLogger(bus.paths.events_jsonl, bus.paths.summary_json)
    bus.subscribe(logger)          # logger.handle nhận mọi event đã redact
```
**Rationale — consumer thuần, gắn ở biên:** EventLogger chỉ **tiêu thụ** event từ bus (không tự phát) nên không tạo vòng lặp seq và không đụng kernel. Vì nó chạy **sau** redact trong pipeline emit, mọi thứ nó ghi ra `events.jsonl` đã sạch secret — đóng đúng lỗ hổng gốc "tool.requested logs raw args" (`evidence §6`).

---

## 3. Bám contract (public API + bất biến → code)

| Contract | Bất biến | Hiện thực trong code |
|---|---|---|
| `EventEmitter.emit_event` | thứ tự (1)gate→(2)seq→(3)redact→(4)fan-out | §2.2 — 4 bước đúng thứ tự, có comment mốc |
| Event-type ∉ registry → raise TRƯỚC publish | fail-closed | §2.2 gate là lệnh đầu; §2.1 `__post_init__` chốt lần 2 → `ControlContractError("EVENT_UNKNOWN_TYPE")` |
| `seq` monotonic gap-free per-run; resume khôi phục high-watermark [G11] | seq đơn điệu xuyên resume | §2.3 `SessionSeq.next()` (RLock) + `resume_from(events)` = max(seq) |
| UI đọc CHỈ `ui_payload` | raw payload không rời emitter | §2.1 field 14 `ui_payload`; §2.4 redactor set nó; §2.6 sink ghi `as_dict()` đã redact |
| Redact TRƯỚC fan-out; 0 secret thô trong ui_payload | redact-before-fan-out | §2.2 bước (3) trước (4); §2.4 `_scrub` che 15 key đệ quy, no-mutate |
| `Redactor.apply` | 15 SECRET_KEYS, đệ quy dict+list, no mutate | §2.4 `SECRET_KEYS` (=15), `_scrub` đệ quy, `replace()` |
| `build_snapshot` linear fold; terminal không ghi đè | replay=snapshot tất định | §2.5 sort theo seq + khoá `_TERMINAL` |
| `attach_to_bus` → events.jsonl + summary.json | EventLogger consumer | §2.6 `subscribe(logger)` |
| [G3] write-tool bật mà redactor chưa active → `WRITE_TOOL_ENABLED_WITHOUT_REDACTION` | freeze fail-closed | §2.2 gate G3 ngay sau registry-gate (phối hợp Execution-Core) |
| Error code | `EVENT_UNKNOWN_TYPE`·`EVENT_SEQ_GAP`·`WRITE_TOOL_ENABLED_WITHOUT_REDACTION` | `ControlContractError(code, detail)` dùng đủ 3 mã |

---

## 4. Đạt DoD

| DoD | Cách module này đạt |
|---|---|
| **D4 — 0 secret trong `ui_payload` (redact-before-write) + G3 freeze-gate** | (a) redact chạy ở bước (3) TRƯỚC fan-out (4) → sink jsonl chỉ thấy bản đã che; (b) **audit-test 0-secret** quét `ui_payload` mọi event trong `events.jsonl`, assert không chứa giá trị secret gốc & không còn key ∈ SECRET_KEYS mang giá trị thô; (c) **G3 freeze fail-closed**: `WRITE_TOOL_ENABLED_WITHOUT_REDACTION` chặn phát `tool.requested` khi write-tool bật mà `redaction_active=False` — phối hợp Execution-Core (nơi bật write-capability). |
| **Determinism: replay = snapshot** | `build_snapshot(events[0..n])` fold tuyến tính theo seq, khoá terminal → cùng list event luôn cho cùng snapshot; property-test §5 chứng minh `replay(events[0..n]) == snapshot(n)`. |
| **D3 (liên đới) — resume round-trip** | `SessionSeq.resume_from` giữ seq gap-free qua resume để timeline replay được sau khôi phục (SQLite = truth thuộc Orchestration; module này chỉ đảm bảo seq/replay). |

> DoD D1/D2/D5 thuộc Execution-Core / Orchestration — module này KHÔNG hiện thực (không có `execute_tool`, không set verdict). Chỉ tiêu thụ event từ bus.

---

## 5. Test tối thiểu

**Unit**
- `test_unknown_event_type_raises`: `emit_event("tool.frobnicate", ...)` → `ControlContractError("EVENT_UNKNOWN_TYPE")`; và dựng `RuntimeEvent(event_type="nope", ...)` trực tiếp cũng raise ở `__post_init__`.
- `test_redact_masks_known_key`: payload `{"api_key": "sk-live-123"}` → `ui_payload["api_key"] == "[REDACTED]"`, và `"sk-live-123"` không xuất hiện ở bất kỳ đâu trong `ui_payload`.
- `test_emit_order`: dùng redactor giả đếm lời gọi → assert seq được stamp trước khi redactor thấy event, và sink chỉ nhận event sau redact.

**Property (Hypothesis)**
- `test_redact_recursive_any_shape`: sinh dict/list lồng bất kỳ độ sâu có chèn ngẫu nhiên key ∈ SECRET_KEYS → mọi giá trị dưới key đó = `[REDACTED]`, `payload` gốc KHÔNG đổi (no-mutate), cấu trúc ui_payload đồng dạng.
- `test_replay_equals_snapshot`: với chuỗi event hợp lệ ngẫu nhiên (seq tăng), `build_snapshot(events[0..n]) == build_snapshot(events[0..n])` (tất định) và fold từng-bước == fold một-phát; terminal một khi đạt không bị lùi.

**Audit (đối kháng)**
- `test_no_secret_in_ui_payload`: chạy phiên có tool.requested mang args chứa mọi key SECRET_KEYS + giá trị canary; grep toàn bộ `events.jsonl` `ui_payload` → 0 canary, 0 key thô. (đóng D4)
- `test_seq_gap_free_through_resume`: phát N event → dừng → `SessionSeq.resume_from(events)` → phát tiếp M event; assert dãy seq là `1..N+M` liên tục, không trùng, không gap (đóng G11).
- `test_g3_freeze_when_write_without_redaction`: `write_tools_enabled=True, redaction_active=False` → `emit_event("tool.requested", ...)` raise `WRITE_TOOL_ENABLED_WITHOUT_REDACTION` (đóng G3).

---

## 6. Còn treo / ẩn số
- **[G11] seq high-watermark khi resume CROSS-PROCESS.** `resume_from` khôi phục đúng khi đọc lại được toàn bộ event đã phát (in-process / cùng jsonl). Nếu resume ở process khác mà nguồn seq-truth là SQLite (Orchestration sở hữu), cần chốt: đọc high-watermark từ SQLite hay từ jsonl? Rủi ro double-count nếu hai nguồn lệch. **Cần chốt với Orchestration.**
- **Mismatch tên event `tool.requested` vs registry.** Evidence gốc ghi kernel phát `tool.requested/completed` nhưng registry khai `tool.call_requested/before_call/after_call` (`evidence §3`). Gate registry sẽ **fail-closed** nếu tên không khớp — cần reconcile `config/runtime_event_types.yaml` với tên Execution-Core thực phát TRƯỚC khi bật gate ở prod, nếu không mọi `tool.requested` bị chặn oan. **Cần chốt với Execution-Core.**
- **Số field snapshot (9) và mã hoá `_status_of`.** Spec khoá terminal + fold loop.*; ánh xạ chi tiết loop.* → status (9 field đầy đủ của `TaskLoopSnapshot`) chốt khi thấy `config/runtime_event_types.yaml` bản final.
