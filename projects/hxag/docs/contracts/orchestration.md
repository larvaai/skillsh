# Contract — Orchestration (FROZEN 2026-07-03)

> Bám evidence gốc `supervisor/loop.py`, `supervisor/graph.py`, `delegation/manager.py`, `supervisor/state.py`.

## Public API
```python
def run_task_loop(task: TaskEnvelope, acceptance_criteria: list[AcceptanceCheck],
                  *, kernel, budget) -> TaskLoopOutcome: ...   # → FINISHED|BLOCKED|FAILED
def resume_task_loop(session_id: str, *, kernel) -> TaskLoopOutcome: ...

class DelegationManager:                                        # chokepoint RIÊNG (không thuộc kernel)
    def delegate(self, parent_session, target: str, spec: DelegationSpec,
                 policy: DelegationPolicy | None = None) -> DelegationResult: ...
```

## Data
```python
OrchestratorDecision(decision: str,  # continue|need_tool|finished|blocked|failed
                     next_agent_calls, tool_requests, acceptance_status, commands)
AgentAssignment(agent_id, objective, scope_of_work, allowed_capabilities, target_kind)
AcceptanceCheck(id, text, status, evidence_ids)   # is_satisfied = passed ∧ evidence_ids≠∅
DelegationResult(outcome: str, artifacts, summary, error)  # success|rejected|failed
```

## Bất biến contract
- FINISHED chỉ khi `all_accepted()` (mọi AC is_satisfied với evidence THẬT — không scaffolding).
- Worker KHÔNG set verdict; chỉ `judge_acceptance` set.
- `delegate`: policy.validate (depth≤max, scope ⊆ parent, max_steps) TRƯỚC khi tạo child; child crash → `finally` đóng session; outcome=failed → không nửa-merge.
- Guards: max_rounds, no-progress (artifacts↑ ∧ acceptance-đổi ∧ command — cần cả ba), repeat-decision, parse-budget, MAX_DEPTH.
- **[review G1]** evidence phải mang provenance (node_id/AC nguồn); reject cross-AC reuse.

## Error code
`ACCEPTANCE_UNSATISFIABLE` · `DELEGATION_SCOPE_EXCEEDS_PARENT` · `DELEGATION_DEPTH_EXCEEDED` · `DELEGATION_CHILD_TIMEOUT` · `LOOP_NO_PROGRESS` · `PLAN_DEPENDENCY_CYCLE`.
