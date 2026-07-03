# Module Build Spec — Orchestration (LÕI sản phẩm)

> Bám FROZEN contract `docs/contracts/orchestration.md` + gọi `execute_tool` qua `docs/contracts/execution-core.md`.
> Anchor gốc: `supervisor/loop.py:_drive`, `supervisor/graph.py:judge_acceptance[357-382]`, `delegation/manager.py[63-192]`, `decompose_agent/solve.py+accept.py`.
> Python 3.11 · `@dataclass(frozen=True)` · ports = `Protocol(runtime_checkable)` · mỗi quyết định lớn kèm rationale.

## 1. Góc nhìn lãnh đạo

Đây là bộ não biến "một prompt" thành "task hoàn thành có bằng chứng": nó quyết định vòng lặp, chia việc, giao con, và **chỉ tuyên FINISHED khi mọi tiêu chí có chứng cứ THẬT** — không tự tin giả, không chạy vô hạn. Ba rủi ro chết người của agent (finish giả, loop vô hạn, con vượt quyền cha) đều bị đóng bằng ba cổng cứng ở đây (acceptance-by-evidence, guards, scope⊆parent), nên module này là chỗ product-quality được bảo chứng, không phải chỗ tô LLM.

---

## 2. Cấu trúc code

### 2.0 Ports (Protocol) — ranh giới với module khác

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class KernelPort(Protocol):
    # Execution-Core contract — ta GỌI, không build.
    def execute_tool(self, tool_name: str, args: dict | None = None,
                     *, context: "ToolCallContext | None" = None) -> dict: ...

@runtime_checkable
class SessionPort(Protocol):
    identity: "SessionIdentity"
    allowed_capabilities: frozenset[str]
    def execute_tool(self, name: str, args: dict) -> dict: ...

@runtime_checkable
class SessionFactoryPort(Protocol):
    def create_child(self, parent, *, allowed_capabilities: frozenset[str]) -> SessionPort: ...
    def restore(self, *, identity, state, allowed_capabilities) -> SessionPort: ...

@runtime_checkable
class OraclePort(Protocol):           # LLM Orchestrator — trả OrchestratorDecision (JSON-gated ở Discipline)
    def decide(self, state: "TaskLoopState", *, budget) -> "OrchestratorDecision": ...

@runtime_checkable
class CheckpointStore(Protocol):      # SQLite; atomic save/load. Nội bộ Observability/Control-plane.
    def save(self, session_id: str, snapshot: dict) -> None: ...
    def load(self, session_id: str) -> dict | None: ...

@runtime_checkable
class Blackboard(Protocol):           # nơi evidence sống; ta chỉ resolve id → Evidence
    def resolve(self, evidence_id: str) -> "Evidence | None": ...
```

**Rationale:** Orchestration KHÔNG import kernel internals; mọi hành động đi qua `SessionPort.execute_tool → KernelPort` (rule-5 một-cửa, DoD D1). Oracle là port để test bơm quyết định deterministic (không cần LLM thật trong unit/property test).

### 2.1 Data (frozen dataclass)

```python
@dataclass(frozen=True)
class AcceptanceCheck:
    id: str
    text: str
    status: str = "pending"            # pending|passed|failed
    evidence_ids: tuple[str, ...] = ()
    @property
    def is_satisfied(self) -> bool:    # oracle gốc state.py:35-37
        return self.status == "passed" and len(self.evidence_ids) > 0

@dataclass(frozen=True)
class Evidence:
    id: str
    kind: str            # artifact|tool_result|reviewer_report|diff|test_result | session_plan|context_packet|ac_report
    source_node_id: str  # [G1] provenance: node/AC đã SINH ra evidence này
    source_ac_id: str    # [G1] AC gốc — chống cross-AC reuse

_REAL_EVIDENCE = frozenset({"artifact", "tool_result", "reviewer_report", "diff", "test_result"})
def is_real_evidence(e: Evidence) -> bool:   # evidence.py:16-23 — scaffolding bị loại
    return e.kind in _REAL_EVIDENCE

@dataclass(frozen=True)
class OrchestratorDecision:
    decision: str        # continue|need_tool|finished|blocked|failed
    next_agent_calls: tuple["AgentAssignment", ...] = ()
    tool_requests: tuple[dict, ...] = ()
    acceptance_status: tuple[dict, ...] = ()   # [{id,status,evidence_ids}] do O đề xuất
    commands: tuple[dict, ...] = ()

@dataclass(frozen=True)
class AgentAssignment:
    agent_id: str; objective: str; scope_of_work: str
    allowed_capabilities: frozenset[str]        # O sở hữu biên; Broker KHÔNG nới
    target_kind: str = "agent"                  # agent|department

@dataclass(frozen=True)
class DelegationSpec:
    objective: str; briefing: str
    allowed_capabilities: frozenset[str]; max_steps: int

@dataclass(frozen=True)
class DelegationPolicy:
    max_depth: int = 8; max_steps: int = 100

@dataclass(frozen=True)
class DelegationResult:
    outcome: str                    # success|rejected|failed
    artifacts: tuple = (); summary: str = ""; error: str | None = None

@dataclass(frozen=True)
class TaskLoopOutcome:
    status: str                     # FINISHED|BLOCKED|FAILED
    session_id: str; round_no: int
    acceptance: tuple[AcceptanceCheck, ...]
    reason: str | None = None       # error code khi BLOCKED/FAILED
```

`TaskLoopState` giữ **primitive-only** (encode/decode được cho checkpoint): `session_id, round_no, acceptance (tuple), artifacts_seen (frozenset[str]), last_decision_sig, parse_errors, applied_command_ids (frozenset[str])`.

### 2.2 `run_task_loop` / `_drive` — vòng đời task

```python
def run_task_loop(task, acceptance_criteria, *, kernel, budget) -> TaskLoopOutcome:
    _reject_unsatisfiable(acceptance_criteria)          # 0 AC → ACCEPTANCE_UNSATISFIABLE
    state = TaskLoopState.initial(task, acceptance_criteria)
    return _drive(state, kernel=kernel, budget=budget)

def _drive(state, *, kernel, budget, oracle, ckpt) -> TaskLoopOutcome:   # supervisor/loop.py:_drive[157-241]
    while not state.is_terminal:
        # 1. O quyết định (JSON-gated ở Discipline; parse fail → parse-budget guard)
        try:
            decision = oracle.decide(state, budget=budget)
        except ParseError:
            state = state.bump_parse_error()
            if state.parse_errors > budget.max_parse_errors:            # parse-budget → FAILED
                return _terminate(state, "FAILED", reason="LOOP_PARSE_BUDGET")
            continue

        # 2. route
        if decision.decision == "finished":
            state = judge_acceptance(state, decision, blackboard=ckpt.blackboard)  # cổng cứng
            if state.all_accepted():
                return _terminate(state, "FINISHED")
            state = state.note_denied_finish()          # không all_accepted → tiếp, đếm vào no-progress
        elif decision.decision == "need_tool":
            state = run_tool(state, decision, kernel=kernel)            # qua execute_tool (D1)
        elif decision.decision == "continue":
            state = run_round(state, decision, kernel=kernel)          # delegate/round
        elif decision.decision in ("blocked", "failed"):
            return _terminate(state, decision.decision.upper())

        # 3. commands roster (idempotent theo applied_command_ids)
        state = apply_pending_commands(state, decision.commands)

        # 4. guards — TRƯỚC checkpoint để BLOCKED cũng được lưu
        verdict = _check_guards(state, budget)          # → None | (status, error_code)
        if verdict:
            state = state.advance_round()
            ckpt.save(state.session_id, state.encode())                # atomic: guards thấy state đã ghi
            return _terminate(state, verdict[0], reason=verdict[1])

        # 5. checkpoint ATOMIC: commands + round + save cùng một txn (rule resume)
        state = state.advance_round()
        ckpt.save(state.session_id, state.encode())
    return _terminate(state, "BLOCKED", reason="LOOP_NO_PROGRESS")
```

**Rationale route-order:** `finished` xử lý TRƯỚC guards để O có cơ hội tuyên hoàn thành hợp lệ; nhưng finish giả (không all_accepted) rơi xuống guard no-progress → không lách được thành loop vô hạn.

### 2.3 `judge_acceptance` — cổng cứng finish-by-evidence [G1 đóng review]

```python
def judge_acceptance(state, decision, *, blackboard) -> TaskLoopState:   # graph.py:357-382
    updated: list[AcceptanceCheck] = []
    by_id = {a.id: a for a in state.acceptance}
    seen_evidence: dict[str, str] = {}            # evidence_id → ac_id đã dùng (chống cross-AC)
    for claim in decision.acceptance_status:      # [{id,status,evidence_ids}] do WORKER/O đề xuất
        ac = by_id.get(claim["id"])
        if ac is None:
            continue
        if claim["status"] != "passed":           # chỉ "passed" được honor [370]
            updated.append(replace(ac, status="failed")); continue
        good: list[str] = []
        for eid in claim["evidence_ids"]:
            ev = blackboard.resolve(eid)
            if ev is None:                    continue          # không resolve → bỏ
            if not is_real_evidence(ev):      continue          # scaffolding bị loại [373]
            if ev.source_ac_id != ac.id:      continue          # [G1] cross-AC reuse → REJECT
            if seen_evidence.get(eid) not in (None, ac.id): continue  # 1 evidence không xài 2 AC
            seen_evidence[eid] = ac.id
            good.append(eid)
        # gate ghi verdict — KHÔNG lấy status từ worker (rule-2, D5)
        updated.append(replace(ac, status=("passed" if good else "failed"),
                               evidence_ids=tuple(good)))
    return state.with_acceptance(tuple(updated))

def all_accepted(acs) -> bool:                     # rule-1
    return len(acs) > 0 and all(a.is_satisfied for a in acs)
```

**Rationale:** verdict do gate tính lại từ evidence THẬT + đúng provenance, không copy `status` worker gửi (D5). `source_ac_id != ac.id` là chốt G1: evidence sinh cho AC-X không thể "mượn" chứng cho AC-Y.

### 2.4 `DelegationManager.delegate` — chokepoint scope-safe [G3/D2]

```python
class DelegationManager:                                   # delegation/manager.py:63-192
    def __init__(self, factory: SessionFactoryPort, handlers: dict): ...

    def delegate(self, parent_session, target, spec, policy=None) -> DelegationResult:
        policy = policy or DelegationPolicy()
        # (1) validate TRƯỚC khi tạo child — fail-closed (policy.py:13-32)
        depth = parent_session.identity.depth + 1
        if depth > policy.max_depth:
            return DelegationResult("rejected", error="DELEGATION_DEPTH_EXCEEDED")
        if not spec.allowed_capabilities <= parent_session.allowed_capabilities:   # scope ⊆ parent
            return DelegationResult("rejected", error="DELEGATION_SCOPE_EXCEEDS_PARENT")
        if spec.max_steps > policy.max_steps:
            return DelegationResult("rejected", error="DELEGATION_STEPS_EXCEEDED")
        # (2) create_child (factory tự fail-closed scope lần 2 — defense in depth)
        child = self.factory.create_child(parent_session,
                                          allowed_capabilities=spec.allowed_capabilities)
        try:
            handler = self.handlers[target]
            res = handler.run(child, spec)                         # Handler.run [160]
            if res.outcome != "success":
                return DelegationResult(res.outcome, error=res.error)  # KHÔNG nửa-merge
            return DelegationResult("success", artifacts=res.artifacts, summary=res.summary)
        except Exception as exc:                                   # child crash
            return DelegationResult("failed", error=str(exc))
        finally:
            self._close(child)                                     # luôn đóng session con
```

**Rationale:** validate-before-create khiến scope-vi-phạm không bao giờ có session tồn tại; `finally close` đảm bảo không rò session dù crash; `outcome != success → không merge` để không có artifact nửa vời lọt lên cha.

### 2.5 Decompose gate `accept_decomposition` — chứng-minh-dừng [rule-4]

```python
def accept_decomposition(parent: Node, children: tuple[Node, ...]) -> tuple[bool, str]:  # accept.py:52-128
    mu_parent = len(parent.done_when)
    # μ co ngặt: MỌI con phải nhỏ hơn cha
    if any(len(c.done_when) >= mu_parent for c in children):
        return False, "MU_NOT_DECREASING"                 # chống chia-giả/loop
    # RENAME: con trùng cha (Jaccard>0.80) → không phải chia thật
    if any(_jaccard(_tok(c), _tok(parent)) > 0.80 for c in children):
        return False, "RENAME"
    # STUCK: không con nào tiến (0 con hoặc coverage-by-implication thủng)
    if not children or not _covers(parent.done_when, children):
        return False, "STUCK"
    return True, "OK"                                       # chạy TRƯỚC khi mutate tree
```

**Rationale:** gate thuần cấu trúc chạy TRƯỚC mutation → cây không bao giờ nhận nhánh không-thu-nhỏ μ; đây là chứng-minh-dừng của plan (μ là số nguyên giảm ngặt → hữu hạn).

### 2.6 `next_node` + guards

```python
def next_node(tree) -> Node | None:                        # tree.py:43-51
    # leftmost pending có mọi dep done (topo theo depth, order)
    return next((n for n in sorted(tree.pending(), key=lambda n:(n.depth, n.order))
                 if all(tree.status(d) == "done" for d in n.depends_on)), None)

def _check_guards(state, budget):                          # loop.py:164-239
    if state.round_no >= budget.max_rounds:            return ("BLOCKED", "LOOP_MAX_ROUNDS")
    if _no_progress(state):                            return ("BLOCKED", "LOOP_NO_PROGRESS")
    if state.repeat_count >= budget.max_repeat:        return ("BLOCKED", "LOOP_REPEAT_DECISION")
    if state.depth > budget.MAX_DEPTH:                 return ("BLOCKED", "LOOP_MAX_DEPTH")
    return None

def _no_progress(state) -> bool:                           # cần CẢ BA đứng yên [229-235]
    return (not state.artifacts_grew          # artifacts↑ ?
            and not state.acceptance_changed  # acceptance đổi ?
            and not state.had_command)        # có command ?
```

**Rationale:** no-progress đòi cả ba điều-kiện-động cùng đứng yên để không giết nhầm vòng đang tiến chậm (chỉ vừa thêm 1 artifact vẫn được đi tiếp). `next_node` leftmost-deps-done cho thứ tự ổn định, resume lại đúng chỗ.

### 2.7 `resume_task_loop` (SPIKE-1)

```python
def resume_task_loop(session_id, *, kernel) -> TaskLoopOutcome:   # loop.py:117-154
    snap = ckpt.load(session_id)
    if snap is None:                       return TaskLoopOutcome("FAILED", ..., reason="NO_CHECKPOINT")
    state = TaskLoopState.decode(snap)     # primitive-only → tái dựng chính xác
    session = factory.restore(identity=state.identity, state=snap["state"],
                              allowed_capabilities=frozenset(snap["caps"]))
    if state.is_terminal:                  return _outcome_from(state)   # idempotent: đã xong thì trả luôn
    return _drive(state, kernel=kernel, budget=..., ckpt=ckpt)           # tiếp từ round đã lưu
```

---

## 3. Bám contract — public API + bất biến → code

| Contract | Hiện thực (§) | Bất biến giữ ra sao |
|---|---|---|
| `run_task_loop → FINISHED\|BLOCKED\|FAILED` | §2.2 `_drive` | terminal do `_terminate`, không đường khác |
| `resume_task_loop(session_id)` | §2.7 | decode primitive-state + `factory.restore` |
| `DelegationManager.delegate` | §2.4 | validate-before-create; `finally` close; outcome≠success→no-merge |
| `OrchestratorDecision(...)` | §2.1 | frozen, decision∈5 giá trị (JSON-gate ở Discipline) |
| `AcceptanceCheck.is_satisfied` | §2.1 | `passed ∧ evidence_ids≠∅` |
| **FINISHED ⟺ all_accepted()** | §2.2 route `finished` + §2.3 | finish giả rơi xuống guard, không lách |
| **Worker KHÔNG set verdict** | §2.3 | gate tính lại status từ evidence, bỏ status worker |
| **delegate scope⊆parent, depth≤max, max_steps** | §2.4 (1) | 3 check fail-closed trước create_child |
| **child crash → finally close; failed → no half-merge** | §2.4 | `except→failed`, `finally→_close`, `outcome≠success→return` |
| **Guards** max_rounds/no-progress/repeat/parse/MAX_DEPTH | §2.2 + §2.6 | parse ở loop, còn lại ở `_check_guards` |
| **[G1] evidence provenance + reject cross-AC** | §2.3 | `source_ac_id != ac.id → continue` |
| Error codes (6) | §2.4/§2.6/§2.2 | map thẳng vào `reason`/`error` |

---

## 4. Đạt DoD + ánh xạ AC

| DoD | Cách đạt | Test |
|---|---|---|
| **D1** không bypass execute_tool | `run_tool`/`run_round` chỉ qua `SessionPort.execute_tool` | audit-grep: 0 call kernel trực tiếp trong module |
| **D2** scope child ⊆ parent | §2.4 check `spec.caps <= parent.caps` fail-closed | property (Hypothesis) — §5 |
| **D3** resume round-trip (SPIKE-1) | primitive-only state + atomic ckpt cùng run_id; §2.7 | integration resume test — §5 |
| **D5** worker không verdict; evidence provenance | §2.3 gate tự tính; `source_ac_id` bắt buộc | property acceptance — §5 |

**Ánh xạ AC → test:**
- **M1** `all_accepted()` true chỉ khi passed ∧ evidence≠∅ ∧ kiểu-real → `test_finish_requires_real_evidence`, `test_scaffolding_rejected`.
- **M2** max_rounds/no-progress/repeat/parse/depth đều BLOCKED → `test_runaway_blocked[*]` (5 case).
- **M3** con xin quyền ngoài cha → `rejected{scope}` → `test_delegate_scope_exceeds_rejected` + property scope.
- **F-10.1** (plan μ) → `test_accept_decomposition_mu` + property μ giảm.

---

## 5. Test tối thiểu

**Unit**
- `test_finish_only_when_all_accepted`: 1 AC passed+real-evidence + 1 AC pending → `finished` bị từ chối, loop tiếp; đủ 2 → FINISHED.
- `test_worker_verdict_ignored`: worker gửi `status=passed` nhưng evidence rỗng → gate ghi `failed`.
- `test_runaway_blocked_no_progress`: oracle luôn trả `continue`, artifacts/acceptance/command đứng yên → BLOCKED `LOOP_NO_PROGRESS` trong ≤ max_rounds.
- `test_parse_budget_failed`: oracle raise ParseError > max → FAILED `LOOP_PARSE_BUDGET`.
- `test_delegate_child_crash_closed`: handler raise → outcome=failed ∧ `_close` được gọi (spy).

**Property (Hypothesis)**
- `prop_scope_subset`: ∀ caps con sinh ngẫu nhiên, `delegate` success ⟹ `child.caps ⊆ parent.caps`; nếu ⊄ ⟹ rejected. (D2/M3)
- `prop_mu_strictly_decreases`: ∀ cây con hợp lệ, `accept_decomposition`=OK ⟹ mọi `len(child.done_when) < len(parent.done_when)`. (rule-4)

**Adversarial (audit)**
- **G1** `test_cross_ac_evidence_rejected`: evidence có `source_ac_id="AC-1"` được O khai cho `AC-2` → gate loại, AC-2 vẫn `failed`, không FINISHED.
- **G2** `test_loop_stuck_blocked`: oracle lặp cùng chữ ký quyết định N lần → `LOOP_REPEAT_DECISION` BLOCKED (không vô hạn).
- **G-depth** `test_delegate_depth_exceeded`: depth cha = max → con `rejected{DELEGATION_DEPTH_EXCEEDED}`.

---

## 6. Còn treo / ẩn số

- **SPIKE-1 (D3 resume atomic):** cách nêu ở §2.2/§2.7 — commands+round+save trong MỘT txn checkpoint, state primitive-only. *Rủi ro:* SQLite write + event-append phải cùng txn (Observability sở hữu event log) → cần contract atomic-boundary với Control-plane; nếu event ghi ngoài txn, crash giữa chừng có thể resume-lệch seq. **Đề xuất:** ckpt.save trả version/seq để resume xác thực đối chiếu; đóng ở integration test D3.
- **G-review honor-system:** gate tin `blackboard.resolve` trả `source_ac_id/source_node_id` trung thực. Nếu module sinh-evidence gắn sai provenance thì G1 thủng ở tầng dưới. *Đề xuất:* audit-test kiểm mọi evidence real có provenance ≠ rỗng khi ghi (thuộc module sinh evidence, ngoài phạm vi này) — nêu như dependency-risk.
- **Broker never widens scope:** ta giả định `AgentAssignment.allowed_capabilities` do O đặt là biên duy nhất; Broker (context-shaping) không có trong module này — cần Roles/Broker giữ đúng cam kết "không set scope".
