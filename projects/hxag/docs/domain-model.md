# Domain Model — HexAgent (GĐ5 WORLD MODEL)

> Đủ-là-đủ: entity có identity+lifecycle, business rule bất biến, domain event chính, ranh giới context. Nguồn: `rebuild-hex-agent/pipeline/05-idea-domain.md`.

## Bounded contexts (ranh giới)
1. **Orchestration** — task loop, plan/decompose, delegation, acceptance. *(lõi)*
2. **Execution-Core** — kernel chokepoint, session, registry, schemas.
3. **Discipline** — json-gate, finish-gate, budget, condense (logic thuần).
4. **Tools & Safety** — sandbox jail, policy deny, tool adapters.
5. **Observability / Control-Plane** — event, emitter, snapshot, command, redaction.
6. **Knowledge** — RAG (tuỳ chọn, mặc định tắt).

## Entity (identity + lifecycle)
| Entity | Identity | Lifecycle |
|---|---|---|
| **Task** | task_id | accepted → running → FINISHED/BLOCKED/FAILED |
| **Plan/Node** | node_id | pending → active → (done \| blocked \| decomposed) |
| **DoneWhen** | (node_id, check) | tiêu chí bất biến; verdict do gate ghi, không do author |
| **Run/Session** | run_id / session_id | open → (child…) → closed; state chỉ ở session |
| **Delegation** | delegation_id | requested → running → success/rejected/failed |
| **AcceptanceCriterion** | ac_id | pending → passed/failed (kèm evidence_ids) |
| **Evidence** | evidence_id | bất biến, có kiểu (artifact/tool_result/reviewer_report/diff/test_result) |
| **Budget** | per-run | đếm bước/parse/depth; hết → cắt |
| **Event** | event_id + seq | append-only, per-run monotonic seq |

## Business rule BẤT BIẾN (5 rule lõi)
1. **Finish-by-evidence:** chỉ FINISHED khi mọi AC `is_satisfied` (status=passed ∧ evidence_ids≠∅). Oracle gốc `state.py:35-37`.
2. **Gate ghi verdict, không phải worker:** worker đề xuất; chỉ gate quyết done/pass.
3. **Scope con ⊆ cha:** mọi delegation thu hẹp hoặc bằng scope cha; fail-closed.
4. **Plan có chứng-minh-dừng:** μ(node)=len(done_when) co ngặt mỗi lần chia (chống chia-giả/loop vô hạn).
5. **Một cửa execute_tool:** mọi hành động (LLM/tool) qua đúng một chokepoint → trace + scope-check.

## Domain event chính
`TaskAccepted` · `PlanDecomposed` · `NodeDelegated` · `AcceptanceJudged` · `TaskFinished` · `TaskBlocked`.

## Data ownership
State chỉ sống trong Session (kernel đông cứng, stateless); Event log & checkpoint SQLite là nguồn audit/tua-lại; UI ⊥ core (không import core).

## Cổng GĐ5: domain đủ rõ để định hình kiến trúc? → GO.
