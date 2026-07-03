# ATLAS — Bản đồ hiểu biết nền của `hex_agent` (gốc)

> built_at: 2026-07-02 (static, từ evidence A/B/C) · built_commit: n/a (không phải git repo; nguồn = read-only investigation `/Users/uspro/Desktop/namnson/hex_agent`) · scope: partial (dựng từ 3 evidence file đã chắt lọc, KHÔNG tự quét lại code gốc)
> project: hex-agent-rebuild (đọc-hiểu bản GỐC để rebuild) · stage: 00 Foundation (atlas) · understanding level (agent): 4 (xem §12)
> Đây là NỀN dùng chung: mọi stage sau (shape/stack/skeleton/modules/frame/explain/…) ĐỌC file này TRƯỚC, khỏi quét lại evidence.

---

## Góc nhìn lãnh đạo (đọc 60 giây, không cần biết code)

1. **Sản phẩm là gì.** `hex_agent` là một **agent tự-điều-phối**: bạn giao MỘT mục tiêu → nó tự lập kế hoạch, chia nhỏ thành các bước có thứ tự, giao cho các sub-agent làm, và **chỉ dừng khi mọi tiêu chí nghiệm thu được chứng minh bằng bằng chứng THẬT** (không phải "agent tự nói xong là xong").
2. **Vì sao đáng tin.** Toàn bộ hành động của agent đi qua đúng MỘT cửa (`execute_tool`) và MỌI thứ xảy ra đều được ghi thành nhật ký sự kiện (event log). Nhờ vậy hệ **xem lại được, chạy lại được, và không rò rỉ bí mật** — giống hộp kính (glass-box) thay vì hộp đen.
3. **Vì sao không sợ "chạy mãi không dừng".** Có hai chốt an toàn đối nhau: một chốt bắt "chỉ xong khi đủ bằng chứng", một chốt bắt "cắt cứng khi hết ngân sách / không tiến triển / lặp quyết định". "Chỉ kết thúc khi hoàn thành" và "không chạy vô hạn" cùng tồn tại một cách có kỷ luật.

**Một câu cho người dựng nền:** hex_agent = *hexagonal microkernel* (nhân đông cứng, session sống) + *event-log-first control plane* + một *vòng lặp task* dừng bằng bằng-chứng-thật và chặn runaway bằng budget/guards. Ba trụ này là bất biến; mọi thứ khác là để làm ba trụ đó an toàn.

---

## §1. Project intake — hệ giải quyết bài toán gì

| Mục | Nội dung |
|---|---|
| **Purpose** | Một agent nhận 1 task → tự plan → sắp thứ tự bước → delegate cho sub-agent → **FINISHED chỉ khi mọi AC có evidence thật** |
| **Actors** | Người giao task (human) · Agent-O (orchestrator/điều phối) · Worker/sub-agent (thực thi) · Gate (accept/judge, KHÔNG phải agent) · UI (pure consumer read-model) |
| **Runtime type** | Autonomous multi-agent **agent** (không phải CRUD web); có mặt phẳng điều khiển realtime (control plane) + console UI |
| **Kiến trúc gốc** | Hexagonal microkernel (frozen kernel + mutable session), glass-box event-log-first, 3 seam BE↔UI đóng kín |
| **Tech stack (quan sát)** | Python · LangGraph (graph topology + AgentState) · SQLite (`langgraph.sqlite` = chân lý resume) · Qdrant (RAG, optional) · LLM OpenAI-compatible JSON-mode adapter · SSE (`GET /api/stream`) |
| **How to run** | DoD S0 = `run_smoke.py` offline deterministic (kernel+JSON+events chạy được không cần mạng) |

**Evidence:**
- File: `orchestrator/loop.py:93-147` (`run()` façade), `core/kernel.py:76-89` (AgentKernel), `graph/runtime.py:31-66` (`build_agent_graph`)
- Suy luận: façade dựng `TaskEnvelope`+`KernelSession`, compile LangGraph, stream tới terminal → đây là 1 hệ agent chứ không phải service request/response
- Mức chắc chắn: chắc chắn (evidence A §1, B §0, C §1)

---

## §2. Kiến trúc & bounded contexts — hình dáng hệ thống

**Style quan sát:** Hexagonal / microkernel + event-driven (event-log-first) + pipeline (middleware chain). Bất biến kiến trúc: **UI ⊥ core/** (UI không import core; ARC-1).

| Bounded context | Thư mục | Trách nhiệm | Được phụ thuộc vào |
|---|---|---|---|
| **Execution Core** | `core/` | `AgentKernel.execute_tool` = chokepoint DUY NHẤT; registry; in-process event bus; KernelSession (state sống) | (nền — không phụ thuộc lên) |
| **Control Plane** | `control/` | EventEmitter (validate→seq→redact→fan-out); RuntimeEvent envelope; TaskLoopSnapshot read-model; RuntimeCommand + registries | core (đọc event) |
| **Discipline** | `discipline/` | json_gate · finish_gate · budget · condense — logic thuần, không side effect | dùng bởi core/graph |
| **Tools & Safety** | `toolbox/`,`safety/`,`middleware/` | fs/terminal/code-intel sandboxed; workspace jail; PolicyGate fail-closed; SafeToolPort | qua chokepoint |
| **Orchestration** | `orchestrator/`,`graph/`,`supervisor/`,`delegation/`,`roles/` | run/resume façade + LangGraph + SQLite; multi-agent TaskLoop (Agent-O); DelegationManager (chokepoint RIÊNG); role allowlist | core, discipline |
| **Observability** | `observability/` | EventLogger → events.jsonl + summary.json + metrics | subscribe event bus |
| **Knowledge (optional)** | `rag/` | Qdrant vector KB, health-gated, offline-first | plugin |
| **UI** | `ui/` | pure consumer read-model; **NO imports from core/** | chỉ đọc 3 seam |

**3 seam đóng kín BE↔UI (contract cứng):**
1. **Event stream** — `RuntimeEvent.as_dict()` canonical; UI chỉ đọc `ui_payload`; `GET /api/stream` SSE (+ `?since=seq` resync đề xuất).
2. **Snapshot read-model** — `TaskLoopSnapshot` fold từ loop/approval/permission/checkpoint events; terminal status không bao giờ bị ghi đè; `GET /api/snapshot`.
3. **Command channel** — `RuntimeCommand`→`CommandAck`; `POST /api/commands`.

**Evidence:** `domain-rebuild-v0.md:26-65` (bounded contexts), `core/kernel.py:106-150` (chokepoint), `control/emitter.py:53+`, `control/ports.py:15` (EventSinkPort = điểm transport duy nhất) · Mức chắc chắn: chắc chắn (evidence B §1/§4).

---

## §3. Module inventory — mỗi module chịu gì (rút gọn)

| Module | Trách nhiệm cốt lõi | Public seam | Rủi ro / ghi chú |
|---|---|---|---|
| `core` | chokepoint `execute_tool`, registry, KernelSession, SessionFactory (child scope ⊆ parent) | `execute_tool`, `SessionFactory.restore` | **hệ trọng** — mọi hành động đi qua đây |
| `control` | event validate/redact/read-model/commands | 3 seam | redact-before-fanout là bất biến |
| `discipline` | json_gate/finish_gate/budget/condense | pure functions | worker KHÔNG được ghi verdict; gate mới ghi |
| `supervisor` | multi-agent TaskLoop, Agent-O, broker, evidence, judge_acceptance | `run_task_loop` (`supervisor/loop.py:70`) | O self-scores = honor-system (rủi ro, xem §11) |
| `delegation` | policy/scope/manager — **chokepoint RIÊNG** | `DelegationManager.delegate` (`delegation/manager.py:63`) | KHÔNG phải method của kernel; scope không được leo |
| `roles` | allowlist = union − forbidden | `RoleView` (`roles/agent.py:53`) | dept/route fields (`spec.py:45,49`) hiện chưa dùng |
| `graph`+`orchestrator` | LangGraph topology + AgentState v2 + SQLite checkpoint | `run`/`resume` | SQLite = truth; checkpoint.json chỉ projection |
| `toolbox`+`safety`+`middleware` | tool sandboxed + workspace jail + policy chain | `SafeToolPort`,`PolicyGate` | jail escape là rủi ro cao |
| `observability` | EventLogger → jsonl/summary/metrics | `attach_to_bus` (`observability/event_log.py:102`) | jsonl log raw args (rủi ro rò secret) |
| `rag` | Qdrant KB optional, health-gated | ingest/search | never raises; test skip nếu Qdrant down |
| `llm` | OpenAI-compatible JSON-mode adapter | `llm/adapter.py` | retry-classify transient vs permanent |

**Evidence:** evidence B §5, C §Key anchor index. Mức chắc chắn: chắc chắn (module) / một phần (chi tiết nội bộ từng module — chưa mở file gốc, chỉ qua evidence).

---

## §4. Domain model — khái niệm nghiệp vụ & bất biến

**Domain entities (tên chuẩn, dùng xuyên suốt mọi stage):**
`Task/Goal` · `Plan` · `Node(work|reduce)` · `DoneWhen` (criterion) · `DependencyEdge` · `Run` · `Session`/`SessionIdentity` · `Agent`/`Role` · `Delegation` · `AcceptanceCriterion` · `Evidence` · `Budget` · `Event(RuntimeEvent)` · `Command(RuntimeCommand)` · `Checkpoint` · `Permission`.

| Concept | Nghĩa | Đại diện code | Field / luật quan trọng |
|---|---|---|---|
| **Node** | 1 bước trong cây kế hoạch | `node.py:102-177` (frozen dataclass) | id,parent,kind(work\|reduce),status,depends_on,done_when(tuple),max_attempts,depth,order |
| **DoneWhen** | 1 tiêu chí "xong khi" của node | `node.py:50-100` | check,params,artifact; **verdict keys bị cấm** [node.py:20] — chỉ gate ghi verdict |
| **Plan/Tree** | forest theo `parent` + DAG theo `depends_on`, **cả hai acyclic** | `tree.py:Tree:21-51` | `next_node()` = node pending trái nhất mà mọi dep đã done |
| **SessionIdentity** | huyết thống bất biến 7 field | `core/session.py` | session_id/run_id/task_id/agent_id/parent_session_id/delegation_id/depth |
| **Run** | = `SessionIdentity.run_id` (không có class riêng) | — | **Step** = 1 lần `execute_tool` (không phải entity hạng nhất) |
| **AcceptanceCriterion** | tiêu chí nghiệm thu | `supervisor/state.py:28-49` | id,text,status(pending\|passed\|failed),evidence_ids; `is_satisfied` = passed AND evidence_ids non-empty |
| **Evidence** | bằng chứng thật vs scaffolding | `supervisor/evidence.py:16-40` | **THẬT** = artifact/tool_result/reviewer_report/diff/test_result; **KHÔNG** = session_plan/context_packet/ac_report |
| **RuntimeEvent** | envelope sự kiện | `control/events.py:113+` | frozen, 14 field, mọi validation ở `__post_init__` |
| **RuntimeCommand** | lệnh điều khiển | `control/*` | frozen, 7 field, idempotency_key |
| **Permission** | quyền per-agent | `control/*` | effective_from ∈ {immediately,next_turn,next_checkpoint}; authz thật ≠ attribution |

**7 bất biến chịu lực (KHÔNG được phá khi rebuild — từ REBUILD-BRIEF, chống lưng bởi evidence):**
1. **Nhân đông cứng, session sống** — freeze kernel trước run đầu (`core/bootstrap.py:28-53`); state chỉ ở session → 0 rò state giữa run (I2/I3).
2. **Một chokepoint `execute_tool`** — mọi hành động qua đúng 1 cửa (`core/kernel.py:106-150`) (I1).
3. **Event-log-first glass-box** — mọi capability call phát `tool.requested/completed`; event log = nguồn audit + replay.
4. **Delegation chokepoint RIÊNG + child scope ⊆ parent** — `delegation/manager.py:63`; validate ở `policy.py:25-26` (I13/I14).
5. **Nghiệm thu bằng bằng chứng + finish có biên** — chỉ FINISHED khi mọi AC có evidence thật; budget/guards chặn runaway.
6. **SQLite = chân lý resume; checkpoint nguyên tử** — `langgraph.sqlite` = truth, `checkpoint.json` = projection UI; commands+round+save trong 1 transaction (I10/I11).
7. **Redact tại biên; attribution ≠ authz** — `ui_payload` che secret trước khi rời emitter; `issued_by` chỉ quy trách, authz thật = `requires_permission` + checkpoint (I16/I17, DEC-8).

**Evidence:** evidence A §2/§4/§7, B §2, REBUILD-BRIEF §"7 invariant". Mức chắc chắn: chắc chắn.

---

## §5. State & lifecycle — object đổi trạng thái thế nào

**Node status machine:** `pending → active → (done | blocked | decomposed)` (`node.py:28`). Chuyển qua `tree.set_status()` + `rebuild_children()`. **Illegal:** worker tự set `done` mà không qua Gate-1; đặt verdict trong done_when.

**Task loop terminal:** `FINISHED` (mọi AC satisfied) · `BLOCKED` (guards: no-progress / repeat-decision) · `FAILED` (parse budget cạn).

**Resume lifecycle:** `orchestrator/loop.py:resume()` [217-273] — SQLite checkpoint qua `open_checkpointer(run_id)`, legacy JSON fallback, resume graph từ `next`. `supervisor/loop.py:resume_task_loop()` [117-154] load Blackboard, validate identity, gọi `_drive()` nếu chưa terminal.

**Bất biến an toàn:** commands + round + save trong MỘT atomic txn (`loop.py:208-218`); idempotency keys track command đã áp dụng (`state.py:98`).

**Evidence:** A §3/§6, node.py:28. Mức chắc chắn: chắc chắn.

---

## §6. API / contracts — các phần nói chuyện bằng gì

| Loại | Contract | Anchor | Ghi chú |
|---|---|---|---|
| Facade | `TaskEnvelope` (user_request, task_id, context, metadata) | `core/schemas.py:11-26` | đầu vào 1 task |
| Decision | `OrchestratorDecision` decision∈{continue,need_tool,finished,blocked,failed} | `supervisor/contracts.py:54-65` | `parse_decision()` strict JSON gate [117-182] |
| Assign | `AgentAssignment` (agent_id, objective, scope_of_work, **allowed_capabilities**, target_kind) | `contracts.py:45-51` | O đặt scope ở đây |
| Context | `ContextPacket` (target_agent_id, objective, briefing, source_ids — **NO scope field**) | `contracts.py:69-83` | Broker chỉ nắn context, KHÔNG mở scope |
| Delegation | `DelegationRequest/Result` (outcome∈{success,rejected,failed}, artifacts, summary, error) | `core.schemas` | progress qua `DelegationProgress` |
| Tool | `ToolRequest`/`ToolCallContext` (6 lineage + allowed_capabilities) → `CapabilityResult` (ok/capability/feature/data/error/metadata) | `core/*` | mọi tool trả `CapabilityResult` |
| Seam HTTP | `GET /api/stream` (SSE) · `GET /api/snapshot` · `POST /api/commands` | `control/*` | 3 seam đóng kín |
| Event catalog | ~50 type từ `config/runtime_event_types.yaml`: session.* agent.* tool.* permission/checkpoint.* command.* artifact.* loop.* delegation.* | config-driven | ⚠️ mismatch: kernel phát `tool.requested/completed` nhưng registry khai `tool.call_requested/before_call/after_call` |
| Command catalog | 16 type từ `config/runtime_command_types.yaml`; apply_at∈{immediate,immediate_if_waiting,next_checkpoint} | config-driven | null-permission group: Pause/Resume/StopAgentTurn/SubmitPrompt |

**Evidence:** A §7, B §2/§3/§4. Mức chắc chắn: chắc chắn (contract) / một phần (danh mục event đầy đủ — chỉ đọc mô tả, chưa mở YAML).

---

## §7. TRACE — vòng đời MỘT task (lăng kính trace, nền dùng chung)

> Đây là mục quan trọng nhất: mọi stage sau tái dùng để khỏi trace lại. Mỗi bước gắn nhãn **[STATE CHANGE]** (đổi state), **[SIDE EFFECT]** (tác động ra ngoài: event/log/DB/child session), **[BOUNDARY]** (qua ranh giới đáng chú ý: chokepoint / scope-check / gate). Anchor `file:line` gốc.

**Câu chuyện 1 dòng:** task đi vào → O quyết định → nếu cần chia thì Gate-2 chứng minh dừng → sắp thứ tự theo dependency → delegate xuống sub-agent (scope co lại) → worker chạy tool qua chokepoint → phát event → gate nghiệm thu bằng bằng chứng thật → FINISHED. Song song luôn có guards chặn runaway.

### Bước 0 — Intake
`orchestrator/loop.py:run()` [93-147] dựng `TaskEnvelope`(user_request,task_id) + `KernelSession`, compile LangGraph (`graph/runtime.py:31-66`), stream tới terminal.
- **[STATE CHANGE]** tạo `KernelSession` (state sống, per-run) trên nền kernel đã freeze.
- **[BOUNDARY]** kernel đã `freeze()` (`core/bootstrap.py:28-53`) — sau điểm này registry/middleware bất biến, chỉ session mutate (bất biến #1).

### Bước 1 — Supervisor drive (vòng lặp chính)
`supervisor/loop.py:_drive()` [157-241] — `while not state.is_terminal`:
- `o_decide(state, ctx, budget)` [171] → `OrchestratorDecision`.
- **[BOUNDARY]** `parse_decision()` strict JSON gate (`contracts.py:117-182`) — LLM plan phải parse đúng JSON, sai thì tiêu tốn parse-error budget.
- Route [184-201]: `finished`→judge+terminate · `continue`→run_round · `need_tool`→run_tool · `blocked/failed`→terminate.

### Bước 2 — Plan / Decompose (khi cần chia nhỏ)
Recursive: `decompose_agent/solve.py:solve()` [258-301] đi trên `Tree`.
- `worker.decompose()` đề xuất các child node.
- **[BOUNDARY]** **Gate-2 `accept_decomposition()`** (`decompose_agent/accept.py`) [gọi ở `solve.py:167`] — **gate CẤU TRÚC thuần, chạy TRƯỚC khi đổi cây**.
  - **Chứng minh dừng:** μ(node)=len(done_when); mỗi child được nhận **co ngặt** μ (`accept.py:52-128`); coverage-by-implication [101-127]; phát hiện RENAME (Jaccard>0.80) / STUCK [solve.py:165]. → cây không thể chia vô hạn.
- **[STATE CHANGE]** nếu accept: parent's `done_when` thành structural `all_children_done` [solve.py:175]; thêm synthetic reduce node [187-201]; children ghi vào tree.
- **[SIDE EFFECT]** ghi `Journal` audit + YAML checkpoint của Tree.
- Leaf: `solve_leaf()` [80-121] worker đề xuất → **Gate-1** kiểm → PASS=done / FAIL=retry (K=3, K_LEAF=5); budget guard [91].
- **Bất biến:** worker KHÔNG tự ghi verdict — chỉ gate ghi (`node.py:20` cấm verdict keys).

### Bước 3 — Order steps (không leo sớm)
`Tree.next_node()` [tree.py:43-51] = node **pending trái nhất mà MỌI dependency đã done** (topo theo depth,order).
- **[BOUNDARY]** đây là chỗ "không leo sớm" miễn phí: node có dep chưa done sẽ không bao giờ được chọn.

### Bước 4 — Delegate (chokepoint RIÊNG, scope co lại)
`delegation/manager.py:DelegationManager.delegate()` [63-192] — KHÔNG phải method của kernel.
- **[BOUNDARY]** validate policy (`policy.py:13-32`): depth ≤ max_depth(8), **capability scope ⊆ parent** [policy.py:25-26], max_steps(100).
- Supervisor side (`supervisor/graph.py:run_round()` [218-337]): authority gate (assignments ⊆ selected agents) [265-268]; skip completed turns (resume guard) [273-276]; Broker viết `ContextPacket` [278] (**KHÔNG có scope field** — chỉ nắn context); build `DelegationPolicy` từ O's `allowed_capabilities` [298]; gọi `delegation_service.delegate()` [299].
- **[STATE CHANGE]** tạo **child session** (SessionFactory, scope ⊆ parent) → `Handler.run()` [160].
- **[STATE CHANGE]** merge artifacts+result về parent; close child.
- **[SIDE EFFECT]** emit `delegation.finished`; append `AgentTurn` + **checkpoint SAU MỖI turn** [332].
- **Bất biến:** Broker never widens scope (`broker.py:1-8`); O alone controls capability boundaries.

### Bước 5 — Worker execute_tool (chokepoint DUY NHẤT)
`core/kernel.py:execute_tool` [106-150] — mọi hành động (LLM/tool/scope-check/obs/envelope) qua đúng cửa này.
- **[SIDE EFFECT]** publish `tool.requested` (kèm lineage + args).
- **[BOUNDARY]** scope-check: tool ∈ `allowed_capabilities`? nếu không → fail (không escape).
- **[BOUNDARY]** middleware chain (outer→inner): Timing → PolicyGate(fail-closed) → BudgetGuard → Retry → Condense → core.
- **[SIDE EFFECT]** publish `tool.completed | tool.failed`; trả `CapabilityResult` (exception never escapes).
- ⚠️ Rủi ro biết trước: `tool.requested` log raw args vào jsonl (`core/kernel.py:125`) — phải redact trước khi bật write tools.

### Bước 6 — Emit events → observe
- **[SIDE EFFECT]** EventLogger subscribe `tool.*`/`task.*` → `events.jsonl` + `summary.json` + metrics (tool_calls/llm_calls/failures/blocks/parse_errors) (`observability/event_log.py:102`).
- **[BOUNDARY]** nếu qua EventEmitter (control plane): gate → seq(monotonic per-session) → **redact (15 SECRET_KEYS)** → fan-out; `ui_payload` che secret TRƯỚC khi rời emitter (bất biến #7).

### Bước 7 — Judge acceptance (bằng chứng THẬT)
`supervisor/graph.py:judge_acceptance()` [357-382] — O cung cấp `acceptance_status` [{id,status,evidence_ids}].
- **[BOUNDARY]** mỗi evidence được cite phải **resolve trên Blackboard** AND là **evidence THẬT** [373] — không chấp nhận scaffolding (session_plan/context_packet/ac_report; `evidence.py:16-23`). Chỉ "passed" + ≥1 evidence hợp lệ mới được honor [370].
- **[STATE CHANGE]** cập nhật `AcceptanceCheck.status`.
- **Bất biến:** worker KHÔNG tự ghi verdict; O phải emit "finished" [184] rồi mới xét — nếu chưa `all_accepted()` thì bị từ chối [186-191].

### Bước 8 — Finish / terminate
- `state.all_accepted()` [`state.py:107-108`] = mọi `acceptance_checks.is_satisfied` (status=="passed" AND evidence_ids non-empty) → **[STATE CHANGE]** terminal = `FINISHED` [_drive:186-190].
- Agent-level finish gate: `discipline/finish_gate.py:check_finish()` [15-22] chặn final nếu `code_changed` nhưng `!validation_passed` (trừ finish_reason="blocker").

### Song song — Guards chặn runaway (luôn chạy cùng vòng lặp)
- **[BOUNDARY]** max_rounds [_drive:164]; no-progress guard (artifacts không tăng ∧ acceptance không đổi ∧ không có command) [229-235] → BLOCKED; repeat-decision guard (chữ ký quyết định lặp N× → BLOCKED) [237-238]; parse-error budget (CONSECUTIVE, reset khi parse tốt) [172-173] → FAILED.
- Budget: `discipline/budget.py:Budget` (max_steps — parse errors không tiêu; max_parse_errors; max_same_tool_calls). Decompose: MAX_DEPTH=6 (`solve.py:34`), K=3/K_LEAF=5, per-root step budget.
- **[STATE CHANGE] atomic:** commands + round_no++ + `ctx.save(state)` trong MỘT transaction [_drive:208-218].

**Kết:** "chỉ kết thúc khi xong" (Bước 7-8) + "không chạy vô hạn" (Guards) là HAI chốt đối nhau — đây là điểm thiết kế cốt lõi phải giữ khi rebuild.

---

## §8. Side effects map — code nào gây tác động thật

| Nơi | DB write | External API | Event/Log | Child session | Nguy hiểm |
|---|---|---|---|---|---|
| `core/kernel.execute_tool` | — | qua tool (LLM tốn phí) | `tool.requested/completed/failed` | — | scope-check chặn tool ngoài allowlist |
| `delegation/manager.delegate` | — | — | `delegation.finished` | **tạo & đóng child session** | scope escalation nếu policy sai |
| `orchestrator/loop` checkpoint | **SQLite save** (atomic) | — | — | — | mất atomicity = resume sai |
| `observability/event_log` | — | — | **jsonl + summary + metrics** | — | log raw args → rò secret (`kernel.py:125`) |
| `toolbox` fs/terminal | **file write** (jail) | terminal_run (argv-only) | — | — | sandbox escape ngoài `var/workspace/` |
| `control/emitter` | — | — | fan-out event | — | thiếu redact = rò secret ra UI |

**Evidence:** A §5/§6, B §6/§7. Mức chắc chắn: chắc chắn.

---

## §9. Security / permission map

- **Scope:** per-session `frozenset` `allowed_capabilities`; enforced trong `execute_tool`; **child ⊆ parent** khi delegate (SessionFactory, `session.py:163`).
- **Workspace jail:** `safety/sandbox.py:resolve_in_workspace` [38,97] — mọi path phải `relative_to var/workspace/`.
- **Redaction:** `ui_payload` redact trước khi rời emitter; 15 SECRET_KEYS hardcoded; raw payload không rời hệ. **Gap:** `tool.requested` log raw args vào jsonl.
- **Authz vs attribution (DEC-8):** `issued_by` = attribution only; authz thật = `requires_permission` + checkpoint. **Gap hiện tại:** `supervisor/command_bridge.py` trust-O bypass (enforcement đề xuất). `UpdateAgentPermission` luôn human-gated.
- **Policy deny-list:** `middleware/policy.py:PolicyGate` fail-closed.

**Evidence:** B §6, C §7. Mức chắc chắn: chắc chắn.

---

## §10. Test & observability map

- **Tests:** E19 Test Harness ✓ — `tests/`,`tests_audit/` (~327 tests). DoD gates mỗi phase: `run_smoke.py` (S0), resume round-trip (E05), sandbox-escape+policy-matrix (E06), TaskLoop reaches FINISHED + no privilege escalation (E10), 0 secret in ui_payload (E21).
- **Critical untested / rủi ro cần cover khi rebuild:** LLM JSON parse-repair, acceptance evidence-type check, delegation scope-shrink, redact-before-fanout, atomic checkpoint resume.
- **Observability:** EventLogger → events.jsonl + summary.json + metrics; tracing qua `TraceContext` (trace/span/parent_span) + `SessionSeq` (monotonic per-session). Debug production: xem events.jsonl (seq order) → build_snapshot fold → tìm terminal-status.

**Evidence:** C §1 (E19), B §7. Mức chắc chắn: chắc chắn (có tests) / một phần (nội dung từng test — chưa mở).

---

## §11. Change impact — sửa một chỗ ảnh hưởng đâu (nền cho stage sau)

| Thay đổi điển hình | Ảnh hưởng | Risk |
|---|---|---|
| Đổi LLM provider | `llm/adapter.py` (JSON-mode, retry-classify) — nhưng LLM là capability qua chokepoint nên không lan lên loop | thấp (đúng port) |
| Thêm tool mới | registry + `allowed_capabilities` + PolicyGate + SafeToolPort + redact keys | trung bình (quên scope/redact = rò) |
| Thêm evidence type | `supervisor/evidence.py:16-40` real-vs-scaffolding + judge_acceptance | cao (nới lỏng = finish giả) |
| Đổi node status / done_when | `node.py`, `tree.py`, Gate-1/Gate-2, chứng minh dừng | **rất cao** (phá termination proof) |
| Nới scope delegation | `policy.py:25-26`, SessionFactory | **rất cao** (privilege escalation) |
| Wire supervisor emitter | `supervisor/graph.py:48` (default None — chưa nối runtime) | trung bình (E21 pending) |

**Evidence:** C §3, A §2/§4. Mức chắc chắn: một phần (suy từ cấu trúc, chưa mở toàn bộ call sites).

---

## §12. Risks & unknowns — trung thực về phần chưa chắc

**Risks (chống lưng bởi evidence):**
| Risk | Vùng | Severity | Evidence |
|---|---|---|---|
| Log raw args rò secret trước khi bật write tools | observability/kernel | cao | `core/kernel.py:125`; B §6 |
| Event name mismatch (`tool.requested` vs registry `tool.call_requested`) | control/core | trung bình | B §3 |
| O self-scores acceptance = honor-system (judge≠doer chưa tách) | supervisor | cao | C §4; A §4 |
| `command_bridge.py` trust-O bypass (authz chưa enforce) | control/supervisor | cao | B §6 |
| Supervisor emitter `default None` — control plane chưa nối runtime (E21 pending B2–B14) | control | trung bình | C §1 |

**Unknowns / open-Q mang sang stage sau (KHÔNG bịa):**
| Unknown | Vì sao quan trọng | Cách verify | Priority |
|---|---|---|---|
| Danh sách đầy đủ ~50 event / 16 command | shape/modules cần contract chính xác | mở `config/runtime_event_types.yaml` + `runtime_command_types.yaml` | cao |
| Nội dung chi tiết từng module gốc (chỉ có evidence, chưa mở file) | tránh rebuild sai chi tiết nội bộ | mở code gốc `/Users/uspro/Desktop/namnson/hex_agent` khi cần | trung bình |
| E21 B2–B14 (control-store, command-queue, approval-checkpoint, transport, UI) chưa build | scope realtime control chưa rõ | đọc `docs/roadmap/` E21 detail | trung bình |
| Ranh giới v0 (giữ core/control/toolbox/safety/discipline; supervisor/delegation/roles/rag deferred) vs full | quyết định scope skeleton/backlog | xác nhận với stage `shape`/`skeleton` | cao |

**Assumptions đang giả định (chưa observed trực tiếp trong lượt này):** số dòng `file:line` lấy từ evidence A/B/C, KHÔNG tự mở lại code gốc → độ chắc là "chắc chắn theo evidence" chứ không "chắc chắn theo re-read".

---

## §13. Glossary — thống nhất ngôn ngữ (dễ hiểu sai)

| Term | Nghĩa trong hệ này | Ghi chú |
|---|---|---|
| **Run** vs **Task** | Run = `SessionIdentity.run_id`; Task = mục tiêu người giao (1 task có thể nhiều run khi resume) | Run không có class riêng |
| **Step** | 1 lần gọi `execute_tool` | không phải entity hạng nhất; max_steps là knob |
| **Done** vs **Decomposed** | Done = leaf pass Gate-1; Decomposed = node được chia (done_when → all_children_done) | trạng thái khác nhau của Node |
| **Checkpoint** (3 nghĩa!) | (a) `StateStore.snapshot` core; (b) `control.RuntimeCheckpoint` = approval gate; (c) `orchestrator.Checkpoint` = UI projection | ĐỪNG nhầm 3 cái |
| **Evidence** | chỉ artifact/tool_result/reviewer_report/diff/test_result | session_plan/context_packet/ac_report KHÔNG tính |
| **Chokepoint** (2 cái) | `execute_tool` (core, mọi hành động) và `DelegationManager.delegate` (delegation, RIÊNG) | delegate KHÔNG phải method kernel |
| **issued_by** | attribution (quy trách) — KHÔNG phải authz | authz thật = requires_permission + checkpoint |

---

## §14. Scorecard — tự chấm độ hiểu (trung thực)

**Level đạt: 4 (Sửa an toàn) — theo evidence, không phải theo số file.**

- **Đủ cho L1–L3:** biết stack/module/run · architecture style + dependency + data/domain model · trace được ≥4 flow (happy = execute_tool; failure = parse budget→FAILED / no-progress→BLOCKED; side-effect = event/jsonl/checkpoint; permission = scope ⊆ parent + redact). Xem §7 TRACE.
- **Đủ cho L4:** biết sửa chỗ nào ảnh hưởng đâu (§11), test/DoD nào bảo vệ (§10), risk & unknown ở đâu (§12).
- **Chưa đạt L5 (maintainer):** vì lượt này dựng từ evidence chắt lọc chứ chưa re-read toàn bộ code gốc; trade-off kiến trúc chi tiết (vì sao chọn LangGraph, chi tiết middleware order) còn ở mức "một phần". Muốn L5 cần mở `/Users/uspro/Desktop/namnson/hex_agent` trực tiếp.
- **Lý do 1 câu + evidence:** trace được vòng đời task end-to-end với chokepoint/gate/guard anchored `file:line` (evidence A §1-7) và biết impact radius của các thay đổi rủi ro cao (evidence C §3) → đủ nền cho mọi stage sau tái dùng, đủ để chỉ đạo `shape/stack/skeleton/frame` mà không phải quét lại.

---

## §15. Traceability — nối chuỗi pipeline

- **Nhận từ:** REBUILD-BRIEF.md (anchor chung) + evidence-A/B/C (bằng chứng gốc). Đây là stage 00 Foundation, KHÔNG có stage trước.
- **Bàn giao cho:** `shape` (GĐ6 — dùng §2 kiến trúc + §4 bất biến + 3 seam) · `stack` (GĐ7 — §1 tech stack + §12 unknowns) · `skeleton` (GĐ8 — §7 TRACE làm live slice) · `modules` (GĐ10 — §2/§3 bounded context làm module map) · `backlog` (GĐ9 — roadmap E01–E21 evidence C) · `explain`/`frame`/`triage` đọc file này thay vì quét evidence.
- **Open-Q chuyển tiếp:** 4 unknown ở §12 (danh mục event/command đầy đủ, chi tiết module gốc, scope E21, ranh giới v0-vs-full).

---

## Quyết định cổng (self-decide, không hỏi approval)

**GATE: GO.**
- **Người duyệt (đóng vai):** Kiến trúc sư / người dựng nền hiểu biết.
- **Quyết định:** GO — bản đồ hiểu biết đủ nền (L4) cho các stage sau tái dùng.
- **Lý do:** 3 evidence file đã hợp nhất mạch lạc; vòng đời task trace được end-to-end với chokepoint/gate/guard anchored; 7 bất biến + domain entities khớp REBUILD-BRIEF; risk/unknown ghi trung thực thay vì bịa.
- **Phương án đã loại:**
  1. *Re-read toàn bộ code gốc trước khi viết atlas* — loại vì Đủ-là-đủ: evidence A/B/C đã chắt lọc `file:line`; re-read tốn token mà stage sau vẫn mở code khi cần (đã ghi thành open-Q §12). Đổi lại chấp nhận trần L4 thay vì L5.
  2. *Dựng đủ 20 artifact riêng lẻ trong `.ai-understanding/`* — loại vì nhiệm vụ stage này yêu cầu MỘT bản đồ hợp nhất (`ATLAS.md`) làm nền pipeline, không phải bộ 20 file cho 1 repo sống; đã nhúng nội dung 20 artifact vào §1–§14 theo template.
