# Frame — Slice 01: `taskloop-happy-path` — HexAgent (clean rebuild)

> Skill `frame` · giai đoạn **SLICE** (đóng khung MỘT lát cắt buildable rồi mới code). Vào bằng **Live Slice Report GĐ8** (`pipeline/08-skeleton.md`: slice `finish-by-evidence-tối-thiểu` đã đóng khung E2E 9+1 chặng) + **Backlog GĐ9** (`pipeline/09-backlog.md`: Story ⭐ LÕI R3 + AC) + **Module Map/Contract GĐ10** (`pipeline/10-modules.md`: 6 module · 2 seam công khai) + **Delivery Standards/DoD GĐ11** (`pipeline/11-delivery.md`: layout `src/…`, D1–D5, test pyramid).
> Anchor gốc: `00-understanding/REBUILD-BRIEF.md` (7 invariant) + `evidence-A/B/C` + `ATLAS.md`. Chỉ khẳng định điều evidence chống lưng; anchor `file:line` GỐC khi có (đây là rebuild brownfield-informed — đường đi đã chạy ở bản gốc `/Users/uspro/Desktop/namnson/hex_agent`).
> **Chế độ tự-quyết** (product owner: "không hỏi approval, tự quyết"): KHÔNG gọi AskUserQuestion, KHÔNG dừng chờ ở cổng. Ở cổng go/no-go frame đóng vai **Dev nhận slice đã đóng khung** (người duyệt của `frame`), tự chốt scope hợp lý + GHI RÕ quyết định + lý do + phương án đã loại. Đây là kỷ luật hỏi-trước-khi-code nhưng ở chế độ tự-quyết: **frame chỉ đóng khung + ra Plan/Contract; KHÔNG viết code app** (code thật là lượt sau, ngoài stage này).

---

## ── GÓC NHÌN LÃNH ĐẠO (đọc trước, 60 giây — không cần biết code) ──

**Ta đang đóng khung việc-đầu-tiên-viết-code, không phải cả hệ.** Bản gốc đã chứng minh cả 9 tầng chạy được; GĐ8 đã vẽ đường đi; GĐ9–11 đã chia việc, gán chủ, đặt luật "Done". Giờ tới lúc **gõ code**. Kỷ luật sống-còn của sản phẩm này là *không code cả app một lúc* — nên ta cắt đúng **một lát mỏng chạy được, có giá trị nhìn thấy**: giao 1 task 2 bước → agent tự lập kế hoạch → sắp thứ tự theo phụ thuộc → giao cho 1 sub-agent làm → chấm nghiệm-thu **bằng bằng chứng thật** → chỉ **FINISHED** khi đủ bằng chứng, và **budget chặn** nếu chạy quá tay.

**Vì sao lát này, không phải lát khác.** Đây chính là live-slice GĐ8 (`finish-by-evidence-tối-thiểu`) ở quy mô *build thật đầu tiên* — nó chạm **6/7 lời hứa đắt nhất** của sản phẩm trong ít code nhất: một-cửa-cho-mọi-hành-động, event-log-để-audit, giao-việc-không-leo-quyền, và **chỉ-báo-xong-khi-có-bằng-chứng-thật + có-phanh**. Ta **cố ý bỏ ra ngoài**: resume-từ-SQLite (đó là SPIKE-1, rủi ro cao — tách thành slice-02 để lát-đầu chạy được đã rồi mới gánh ẩn số), và toàn bộ bảng-điều-khiển-realtime/RAG/roles-catalog (sau-MVP theo backlog GĐ9).

**Ba điều lãnh đạo cần nhìn.** (1) **Định nghĩa "xong" của lát này**: chạy một task, thấy `FINISHED` với đúng 2 bằng chứng thật, và một cuốn sổ sự kiện (`events.jsonl`) ghi lại từng hành động — chạy được, đo được, không phải lời hứa. (2) **Rủi ro thấp, có địa chỉ**: mọi chặng đã có tiền lệ chạy ở bản gốc (có anchor `file:line`); ẩn số cao duy nhất (resume) đã được **tách ra khỏi** lát này để không kéo lùi. (3) **Kỷ luật fake-trước-real**: LLM-lập-kế-hoạch chạy bằng **bản mô phỏng tất định** (không gọi LLM thật, không tốn tiền, không may rủi) — ta test *luồng sản phẩm*, không test trí thông minh của model; gọi LLM thật để sau.

**Kết luận cho lãnh đạo.** Lát này **GO để dựng**: scope đóng khung xong, tiêu chí đo được, rủi ro thấp và đã cô lập ẩn số. Nó biến live-slice GĐ8 từ "đã-đóng-khung" thành "đã-chạy-thật trên một task" — bước cụ thể đầu tiên để R1/R3 của backlog thành sự thật. Cái *chưa* chứng minh ở lát này (resume, control-plane, multi-round phức tạp) **được ghi rõ là để-ngoài-có-chủ-đích**, không phải bỏ sót.

---

## ── CHI TIẾT KỸ THUẬT (cho dev) ──

### 0. Constitution của slice (Claude phải biết KHÔNG được làm gì)

- **Goal của slice:** dựng lát cắt sống end-to-end *tất định* chứng minh vòng lặp lõi `task → plan → order(deps) → delegate 1 worker (scope⊆parent) → judge-by-evidence → FINISHED, budget chặn`, chạy được bằng `pytest` integration (không cần LLM thật, không cần staging bên ngoài).
- **Non-goals (đóng khung cứng — vi phạm là sai):**
  1. KHÔNG resume-từ-SQLite / crash-recovery / atomic-txn (= SPIKE-1 → **slice-02**, `parking_lot`).
  2. KHÔNG control-plane UI / SSE / snapshot read-model / RuntimeCommand queue (sau-MVP, E21/R4).
  3. KHÔNG RAG / Knowledge module (optional, ngoài critical path — E08/R2).
  4. KHÔNG roles catalog / RoleView allowlist đầy đủ (E09 — slice chỉ cần `allowed_capabilities` thô đặt tay).
  5. KHÔNG gọi LLM thật (fake-trước-real: LLM-plan = simulator tất định trả cây plan cố định).
  6. KHÔNG multi-round phức tạp / retry-loop nhiều vòng / decompose sâu >1 tầng (task 2-bước phẳng, decompose đúng 1 lần).
  7. KHÔNG DB thật ngoài in-memory / KHÔNG auth / KHÔNG deploy production.
- **Coding rules (override Lock phrases theo project — GĐ11 §3):** frozen dataclass + `__post_init__` validate cho mọi entity; cross-module CHỈ qua `Protocol` trong `src/ports/` (cấm import implementation module khác); code tường minh > trừu tượng; diff nhỏ; không đẻ framework chung; không plugin system.

### 1. SCOPE (IN — đúng luồng happy-path + 1 guard)

Lát cắt = **happy-path của skeleton GĐ8, TRỪ resume**, cộng **đúng 1 guard** để chứng minh "có phanh":

| # | Trong scope | Bám nguồn |
|---|---|---|
| 1 | **Intake**: nhận `TaskEnvelope{task_id,user_request}` → `SessionFactory.create` tạo Run/Session (state chỉ ở session) | GĐ8 §2 chặng 1; evidence-B §2; `orchestrator/loop.py:run [93-147]` |
| 2 | **Kernel `execute_tool`** cho **LLM-plan (FAKE tất định)**: worker gọi LLM-as-capability QUA chokepoint → simulator trả cây plan cố định; JSON-mode → `parse_decision` strict | GĐ8 chặng 2; `core/kernel.py:106-150`; `supervisor/contracts.py:117-182` |
| 3 | **Decompose gate `accept_decomposition`** (Cổng-2 thuần cấu trúc, chạy TRƯỚC khi đổi cây): μ(node)=len(done_when) co **ngặt** + coverage-by-implication (đúng **1 lần** decompose T0→{N1,N2,N_reduce}) | GĐ8 chặng 3; `decompose_agent/solve.py:_decompose [132-185]`; `accept.py:52-128` |
| 4 | **Order `next_node()`**: node pending trái nhất mà mọi dep done → N1 trước N2 (N2 `depends_on=[N1]`) | GĐ8 chặng 4; `tree.py:next_node [43-51]` |
| 5 | **Delegate `DelegationManager.delegate`** (cửa RIÊNG, không phải method kernel): validate policy (depth≤max, **scope⊆parent**, max_steps) → child session (SessionFactory scope-shrink) → `Handler.run` → merge artifact → close → emit `delegation.finished` | GĐ8 chặng 5; `delegation/manager.py:63-192`; `policy.py:25-26`; `session.py:163` |
| 6 | **Worker `execute_tool` (tool THẬT)**: child `fs_write`/`fs_read` đi lại QUA chokepoint → sandbox jail `resolve_in_workspace` → PolicyGate fail-closed (worker chỉ cấp `fs_read/fs_write`, KHÔNG `terminal_run`) | GĐ8 chặng 6; `core/kernel.py:106-150`; `safety/sandbox.py:38,97` |
| 7 | **Emit `events.jsonl`**: mọi capability call phát `tool.requested/completed` → EventLogger append jsonl (+ summary/metrics tối thiểu); seq per-run monotonic gap-free | GĐ8 chặng 7; `observability/event_log.py:102` |
| 8 | **`judge_acceptance` trên evidence THẬT**: mỗi AC "passed" cần ≥1 evidence resolve ∧ là REAL (`tool_result`/`artifact`); scaffolding (session_plan/context_packet/ac_report) bị từ chối; **worker KHÔNG ghi verdict — chỉ gate ghi** | GĐ8 chặng 8; `supervisor/graph.py:357-382`; `evidence.py:16-23` |
| 9 | **Finish**: `all_accepted()` = mọi AC passed ∧ evidence≠∅ → **FINISHED**, phát `TaskFinished` | GĐ8 chặng 9; `supervisor/loop.py:_drive [186]`; `state.py:35-37` |
| **G** | **1 GUARD (budget)**: `Budget.max_steps` enforce ở tầng **discipline/loop** (không phải core — core coi là knob) → chạm max → **BLOCKED**, phát `TaskBlocked`. Đây là "phanh" chứng minh bounded. | GĐ8 chặng 9 + §5; `discipline/budget.py:Budget [10-67]`; feed-ngược GĐ8 §5 |

**Guard chọn = `max_steps` (đủ-là-đủ, 1 guard).** Loại no-progress/repeat-decision/parse-budget ra khỏi slice này (đưa `parking_lot` → slice sau): một guard là đủ để chứng minh *cơ chế phanh chạy được*; nhồi cả 4 guard = phình sang backlog S3.5.2 đầy đủ, vi phạm "đúng một slice".

### 2. BOUNDARY (OUT — ghi rõ để không trôi build cả app)

| Ngoài scope | Lý do (bám nguồn) | Về đâu |
|---|---|---|
| **Resume từ SQLite / SPIKE-1 / atomic-txn / crash-recovery** | Ẩn số rủi ro **cao nhất** (GĐ8 ô#5, D3 GĐ11); tách để lát-đầu chạy được trước rồi mới gánh. Fake-trước-real: slice-01 dùng in-memory state. | **slice-02** (`parking_lot`); backlog F1.6/S1.6.1 |
| **Multi-round phức tạp / retry K vòng / decompose sâu >1 tầng** | Task 2-bước phẳng đủ chạm mọi tầng rủi ro; multi-round = phình vòng lặp, khó cô lập lỗi | slice sau (E10 đầy đủ) |
| **Control-plane UI / SSE / snapshot / RuntimeCommand** | UI ⊥ core, sau-MVP (ADR-006 GĐ6, R4 GĐ9); event-log-first đã đủ audit cho slice | E21/R4 |
| **RAG / Knowledge** | Optional, ngoài critical path tới FINISHED (Contract Knowledge GĐ10) | E08/R2 |
| **Roles catalog / RoleView allowlist union−forbidden** | Slice chỉ cần `allowed_capabilities` thô đặt tay để chứng minh scope⊆parent | E09/R3 |
| **LLM thật / redact-raw-args cho write-tool production** | Fake-trước-real (test luồng, không test model). ⚠️ Slice dùng `fs_write` (write-tool) nhưng **fake args không chứa secret** → redact-raw-args (ADR-006) là điều kiện khi bật LLM/write-tool THẬT, ghi open-Q, KHÔNG bật trong slice fake. | LLM thật: slice sau; redact: gắn trước khi bật write-tool thật (D4 GĐ11) |
| **3 guard còn lại** (no-progress, repeat-decision, parse-budget), MAX_DEPTH, per-root step | 1 guard đủ chứng minh bounded; còn lại → S3.5.2 đầy đủ | slice sau |

### 3. ACCEPTANCE (Given/When/Then đo được — oracle, không tường thuật)

> Mọi AC chạy bằng `pytest` integration/property trên bản **tất định** (LLM-plan fake). Đo được = có oracle PASS/FAIL rõ, không phụ thuộc phán đoán.

- **AC-1 (happy-path FINISHED có evidence thật)** — *Given* task `T0` với `user_request` + 2 AC gốc (AC-a: tồn tại `out.txt`==X; AC-b: `len.txt`==len(X)), LLM-plan fake trả cây `{N1, N2(depends_on N1), N_reduce}`, worker cấp `{fs_read,fs_write}` / *When* `run_task_loop(envelope)` chạy tới terminal / *Then* outcome `status==FINISHED`, `all_accepted()==true`, và **đúng 2 evidence thật** (`tool_result` của `fs_write`/`fs_read`) được cite; **0 scaffolding** được tính. *(rule #1 Domain; state.py:35-37; evidence.py:16-23)*
- **AC-2 (events.jsonl đủ dấu vết)** — *Given* slice chạy xong AC-1 / *When* đọc `events.jsonl` / *Then* chứa `tool.requested`+`tool.completed` cho **cả N1 và N2** (fs_write/fs_read) + `delegation.finished`; `seq` per-run **monotonic gap-free**. *(evidence-B §7 (ii); GĐ8 ô#8; AC backlog F1.5)*
- **AC-3 (order — không leo sớm)** — *Given* N2 `depends_on=[N1]`, N1 chưa done / *When* `next_node()` / *Then* trả N1 (KHÔNG bao giờ N2 trước N1). *(tree.py:43-51; AC backlog S3.4.1)*
- **AC-4 (scope⊆parent, property)** — *Given* delegate request với child-cap ⊄ parent-scope / *When* `DelegationManager.delegate` validate policy / *Then* **REJECTED** fail-closed (property-test Hypothesis: ∀ child-cap ⊄ parent → rejected). *(rule #3; policy.py:25-26; D2 GĐ11)*
- **AC-5 (μ co ngặt — decompose gate)** — *Given* fake decompose đề xuất {N1,N2} phủ done_when của T0 / *When* `accept_decomposition` chạy TRƯỚC khi đổi cây / *Then* chấp nhận CHỈ khi mỗi child làm μ(node)=len(done_when) co **ngặt** + coverage-by-implication phủ done_when cha; children trùng tên cha (Jaccard>0.80) hoặc không giảm μ → RENAME/STUCK → từ chối. *(rule #4; accept.py:52-128; AC backlog S3.3.1)*
- **AC-6 (budget chặn — bounded, 1 guard)** — *Given* `Budget.max_steps=K` nhỏ và một fake-plan cố tình vượt K step / *When* loop chạy / *Then* về **BLOCKED**, phát `TaskBlocked`, **KHÔNG** vượt quá K step (budget cắt thật ở tầng discipline/loop). *(evidence-A §5; feed-ngược GĐ8 §5; AC backlog S3.5.2)*
- **AC-7 (worker không set verdict — audit)** — *Given* worker path / *When* audit tĩnh+động / *Then* KHÔNG nhánh nào để worker ghi `acceptance_status.verdict`; verdict CHỈ do gate ghi; `DoneWhen`/Node cấm verdict keys. *(rule #2; node.py:20; D5 GĐ11)*
- **AC-8 (chokepoint — không bypass, audit)** — *Given* toàn bộ call-site trong slice / *When* audit-adversarial (grep AST + runtime assert bus) / *Then* **0 call-site** gọi tool/LLM ngoài `execute_tool`. *(I1; D1 GĐ11)*

> **Đủ-là-đủ:** 8 AC = 1 happy-path (AC-1/2) + 3 invariant-điểm-bán chạm trong slice (AC-4 scope, AC-7 verdict, AC-8 chokepoint = D2/D5/D1) + 2 cơ chế lõi (AC-3 order, AC-5 μ↓) + 1 guard (AC-6 bounded). D3 (resume) + D4 (redact secret thật) **không** trong slice (boundary) → không đặt AC ở đây, ghi open-Q.

### 4. PLAN (các bước code cụ thể — theo Module Map GĐ10, KHÔNG code trong stage này)

> Thứ tự dựng = *gắn-vào-cửa-trước, rồi mới đổ hành vi*. Mỗi bước ghi module đích (GĐ10) + file. Đây là plan cho lượt code SAU; frame stage này chỉ đóng khung.

1. **Ports chung** (`src/ports/`): khai `ToolPort`, `DelegationPort`, `DelegationServicePort`, `EventSinkPort`, `SafeToolPort` bằng `typing.Protocol`. *(GĐ11 §3 cross-module chỉ qua Protocol)*
2. **Execution-Core — Kernel + freeze + Session** (`src/execution_core/`): `AgentKernel` (registry + event bus + middleware chain outer→inner Timing→PolicyGate→BudgetGuard→Retry→Condense→core), `bootstrap.freeze()` trước run đầu; `SessionIdentity` (7-field frozen), `SessionFactory.create/.restore(**kw-only)` (constructor DUY NHẤT, ép child scope⊆parent), `StateStore` in-memory deep-copy isolation. *(evidence-B §2; core/kernel.py:76-89; session.py:163)*
3. **Execution-Core — `execute_tool` chokepoint**: build `ToolRequest` → publish `tool.requested`(+lineage) → **scope-check** (capability ∈ allowed_capabilities else fail-closed) → middleware chain → publish `tool.completed|failed` → trả `CapabilityResult` (exception không escape). *(core/kernel.py:106-150; D1/D2)*
4. **Discipline** (`src/discipline/`): `json_gate.parse` (strict + repair), `budget.step` (`max_steps` KHÔNG tính parse-error — enforce Ở ĐÂY, không core), `finish_gate.check` (chặn finish nếu code_changed ∧ !validation_passed), `condense` (no-op/tối thiểu cho slice). *(discipline/budget.py:10-67; feed-ngược GĐ8 §5)*
5. **Tools-Safety** (`src/tools_safety/`): `fs_write`/`fs_read` jail (`resolve_in_workspace` → mọi path relative_to `var/workspace/`), `PolicyGate` fail-closed, `SafeToolPort.execute` trả `CapabilityResult` (deny→error, KHÔNG throw). KHÔNG `terminal_run` trong slice. *(safety/sandbox.py:38,97)*
6. **Orchestration — LLM-plan qua execute_tool + parse_decision** (`src/orchestration/`): worker gọi LLM-as-capability QUA `execute_tool` → **simulator tất định** trả JSON cây plan cố định; `parse_decision` strict JSON gate → `OrchestratorDecision`. *(supervisor/contracts.py:117-182; fake-trước-real)*
7. **Orchestration — decompose gate `accept_decomposition`**: `Tree` (forest `parent` + DAG `depends_on`, cả hai acyclic), `Node(work|reduce)` frozen, `DoneWhen` (check/params/artifact, cấm verdict keys); `accept_decomposition` = μ-proof co ngặt + coverage-by-implication + RENAME(Jaccard>0.80)/STUCK, chạy **TRƯỚC** khi đổi cây; thêm synthetic `N_reduce`. *(decompose_agent/solve.py:_decompose [132-185]; accept.py:52-128; node.py:20)*
8. **Orchestration — `next_node()` order**: node pending trái nhất mà mọi dep done (topo depth,order). *(tree.py:next_node [43-51])*
9. **Orchestration — `DelegationManager.delegate` (cửa RIÊNG)**: validate `DelegationPolicy` (depth≤max_depth=8, **scope⊆parent**, max_steps=100) → `SessionFactory` child (scope-shrink) → `Handler.run` → merge artifact + result → close child → emit `delegation.finished`. Broker viết `ContextPacket` KHÔNG có field scope (chỉ nắn context). *(delegation/manager.py:63-192; policy.py:25-26; broker.py)*
10. **Worker execute_tool (tool thật)**: child session gọi `fs_write` (ghi `out.txt`) rồi `fs_read` — lại đi QUA `execute_tool` (I1), sinh `tool_result` = evidence thật. *(core/kernel.py:106-150)*
11. **Control-Plane/Observability — EventLogger** (`src/control_plane/`): `EventEmitter.emit` (gate→seq→redact→fan-out; seq per-run RLock monotonic), `EventLogger` subscribe `tool.*`/`delegation.*` → append `events.jsonl` + summary + metrics tối thiểu. Redactor stub (SECRET_KEYS mask) — slice fake không chứa secret, redact-thật gắn trước write-tool THẬT (open-Q). *(control/emitter.py:53; observability/event_log.py:102)*
12. **Orchestration — `judge_acceptance`**: O nộp `acceptance_status[{id,status,evidence_ids}]`; mỗi "passed" resolve evidence trên Blackboard ∧ `evidence_type_of` ∈ REAL; scaffolding từ chối; `all_accepted()` = mọi AC passed ∧ evidence≠∅ → FINISHED. Worker KHÔNG ghi verdict. *(supervisor/graph.py:357-382; evidence.py:16-23; state.py:35-37)*
13. **Orchestration — `run_task_loop` driver + budget guard**: `while not terminal`: o_decide → route finished/continue/need_tool/blocked; `Budget.max_steps` chạm → BLOCKED. Terminal FINISHED/BLOCKED. *(supervisor/loop.py:_drive [157-241])*
14. **Test** (`tests/`, `tests_audit/`): integration E2E (AC-1/2/3/6), property Hypothesis (AC-4 scope⊆parent, AC-5 μ↓), audit-adversarial (AC-7 verdict, AC-8 no-bypass). Bám test pyramid GĐ11 §5.

### 5. FILES / MODULES chạm (bám layout Delivery GĐ11 §1 + Module Map GĐ10)

| Module (owner GĐ10) | File tạo/sửa (rebuild) | Vai trong slice | Anchor gốc |
|---|---|---|---|
| `src/ports/` (Platform) | `ports.py` (Protocol: Tool/Delegation/EventSink/SafeTool) | ranh giới cross-module | `control/ports.py:15` |
| **Execution-Core** (Platform) | `src/execution_core/kernel.py`, `session.py`, `bootstrap.py`, `schemas.py` | freeze + `execute_tool` chokepoint + SessionFactory scope-shrink | `core/kernel.py:76-89,106-150`; `session.py:163` |
| **Discipline** (Platform) | `src/discipline/json_gate.py`, `budget.py`, `finish_gate.py`, `condense.py` | parse + `max_steps` enforce + finish-gate | `discipline/budget.py:10-67` |
| **Tools-Safety** (Safety) | `src/tools_safety/fs_tools.py`, `sandbox.py`, `policy.py`, `safe_tool_port.py` | jail + PolicyGate fail-closed + fs_read/write | `safety/sandbox.py:38,97` |
| **Orchestration** (Orchestration) | `src/orchestration/loop.py`, `tree.py`, `node.py`, `accept.py`, `delegation_manager.py`, `policy.py`, `broker.py`, `contracts.py`, `judge.py`, `state.py`, `evidence.py`, `llm_sim.py` | plan/order/delegate/judge/loop + LLM-plan FAKE | `supervisor/loop.py:157-241`, `graph.py:357-382`; `delegation/manager.py:63-192`; `decompose_agent/{solve,accept,tree,node}.py` |
| **Control-Plane/Obs** (Observability) | `src/control_plane/emitter.py`, `event_log.py`, `redactor.py` (stub) | emit + seq gap-free + jsonl | `control/emitter.py:53`; `observability/event_log.py:102` |
| config/jail | `config/runtime_event_types.yaml` (allowlist `tool.requested/completed/failed` — OQ-3 reconcile), `var/workspace/` (jail) | catalog + jail | evidence-B §3 |
| tests | `tests/test_slice01_e2e.py`, `tests/test_order_nextnode.py`, `tests/prop_scope_shrink.py`, `tests/prop_mu_shrink.py`, `tests_audit/test_no_bypass.py`, `tests_audit/test_worker_no_verdict.py`, `tests/test_budget_blocks.py` | AC-1..AC-8 | GĐ11 §5 |

**Knowledge module: KHÔNG chạm** (optional, boundary). `do_not_touch`: chưa có code cũ trong repo rebuild (greenfield build trên nền tham chiếu) → `do_not_touch=[]`; nhưng **cấm sửa artifact pipeline GĐ5–14** (đó là hợp đồng stage trước).

### 6. RISKS (rủi ro slice + nơi kiểm)

- **RS-1 · Fake LLM-plan lệch cấu trúc thật** — simulator tất định phải trả JSON parse được bởi `parse_decision` + cây phủ đúng done_when của T0, nếu không AC-5 (μ↓) sai. *Kiểm:* AC-5 property + AC-1 e2e. *Giảm:* fix cây fake khớp contract `OrchestratorDecision` GĐ8 §7.
- **RS-2 · Budget enforce nhầm tầng** — nếu đặt `max_steps` ở core (core coi là knob) thay vì discipline/loop thì AC-6 không cắt thật (feed-ngược GĐ8 §5 cảnh báo đúng chỗ này). *Kiểm:* AC-6. *Giảm:* enforce ở `run_task_loop`/discipline, có test đếm step.
- **RS-3 · Scope-check không fail-closed** — nếu delegate không reject child-cap ⊄ parent thì phá D2/M3 (rủi ro RẤT CAO nếu lọt — privilege escalation, ATLAS §"nới scope"). *Kiểm:* AC-4 property Hypothesis. *Giảm:* enforce 2 tầng (delegation policy + SessionFactory).
- **RS-4 · Bypass chokepoint ẩn** — worker gọi fs trực tiếp không qua `execute_tool` → mất audit + mất scope-check (D1). *Kiểm:* AC-8 audit-adversarial (grep AST + runtime assert). *Giảm:* mọi tool chỉ expose qua `SafeToolPort` sau `execute_tool`.
- **RS-5 · seq không gap-free khi delegate tạo child session** — sub-session có thể làm seq nhảy nếu không dùng per-run RLock đúng. *Kiểm:* AC-2. *Giảm:* seq theo `run_id` (đồng nhất cha-con trong 1 run).
- **RS-6 (mang từ boundary — KHÔNG gỡ trong slice) · resume/SPIKE-1** — slice dùng in-memory, chưa chứng minh resume 0 side-effect. *Kiểm:* **slice-02** (D3 GĐ11) — open-Q.
- **RS-7 (open-Q) · redact-raw-args khi bật write-tool THẬT** — slice fake không chứa secret nên chưa chạm; khi bật LLM/write-tool thật phải bật redact TRƯỚC (ADR-006/D4). *Kiểm:* slice bật write-tool thật + Security sign-off GĐ12. Ghi open-Q, KHÔNG bịa đã-làm.

---

## 7. Tự soi trước khi chốt (theo kỷ luật frame)

1. **Đúng MỘT slice, không build cả app?** — CÓ: 1 lát happy-path + 1 guard; mọi thứ khác (resume, control-plane, RAG, roles, multi-round, 3 guard còn lại, LLM thật) → BOUNDARY/`parking_lot` có lý do.
2. **Scope/Boundary/Acceptance rõ, đo được?** — CÓ: 8 AC Given/When/Then có oracle PASS/FAIL (integration/property/audit), không tường thuật.
3. **Constitution (non_goals) chốt TRƯỚC plan code?** — CÓ: §0 liệt kê 7 non-goals + coding rules; plan §4 không đụng thứ nào ngoài đó.
4. **Fake-trước-real, contract-trước-code?** — CÓ: LLM-plan = simulator tất định (không LLM thật/DB thật/auth); code chỉ dùng field trong contract GĐ10 (2 seam: execute_tool · run_task_loop/delegate).
5. **Bám nguồn, không bịa?** — CÓ: mọi chặng anchor `file:line` gốc + nối AC backlog GĐ9 + module GĐ10 + DoD GĐ11; ẩn số (resume, redact-thật) ghi open-Q, KHÔNG tick khống.
6. **Chế độ tự-quyết đúng luật?** — CÓ: không hỏi user; đóng vai Dev-nhận-slice tự chốt scope + ghi phương án đã loại (§8). frame KHÔNG viết code app ở stage này (chỉ Plan/Contract) — đúng "hỏi-trước-khi-code".

---

## 8. Cổng SLICE (tự-quyết; đóng vai Dev nhận slice đã đóng khung — product owner: "không hỏi approval")

**Câu hỏi cổng:** *"Slice đã đóng khung đủ để dev bắt tay dựng đúng một lát, không trôi build cả app chưa?"* (Scope/Boundary/Acceptance rõ · non_goals chốt · plan bám module/contract · không ẩn số chặn việc bắt đầu.)

**Trình cổng (chủ sở hữu = Dev nhận slice):**
- Scope IN = 9 chặng happy-path + 1 guard; Boundary OUT = 7 nhóm có lý do + đích; 8 AC đo được.
- non_goals (7) chốt; plan 14 bước bám Module Map GĐ10 + layout GĐ11; files/modules liệt kê rõ.
- Ẩn số cao nhất (resume/SPIKE-1) đã **tách khỏi slice** → không chặn việc bắt đầu lát-đầu.

```
═══ CỔNG SLICE — slice-01 "taskloop-happy-path" (HexAgent rebuild) ═══
Scope IN   : Intake → execute_tool(LLM-plan FAKE) → decompose-gate(μ↓) → next_node(deps) →
             DelegationManager.delegate(scope⊆parent) → worker execute_tool(fs thật) →
             events.jsonl(seq gap-free) → judge_acceptance(evidence THẬT) → FINISHED · +1 guard budget→BLOCKED.
Boundary OUT: resume/SPIKE-1 (→slice-02) · control-plane UI/SSE · RAG · roles catalog · multi-round · LLM thật · 3 guard còn lại.
Acceptance : AC-1 FINISHED+2 evidence thật · AC-2 events.jsonl(tool.requested/completed+delegation.finished, seq gap-free) ·
             AC-3 order · AC-4 scope⊆parent(property) · AC-5 μ↓ · AC-6 budget→BLOCKED · AC-7 worker-no-verdict · AC-8 no-bypass.
Non-goals  : resume · control-plane · RAG · roles · LLM thật · multi-round phức tạp · DB/auth/prod (7).
Bám nguồn  : GĐ8 slice + GĐ9 AC(S3.2/3.3/3.4/3.5, F1.5) + GĐ10 module/contract + GĐ11 DoD(D1/D2/D5 chạm; D3/D4 open-Q).
Câu hỏi cổng: Slice đủ đóng khung để dựng đúng một lát chưa?
════════════════
```

**Quyết định cổng (tự-quyết — đóng vai Dev nhận slice).**

**GATE: GO cho dựng slice-01.** Lý do: (1) Scope/Boundary/Acceptance rõ + đo được (8 AC có oracle); (2) non_goals chốt → biết KHÔNG làm gì, không trôi build cả app; (3) plan bám đúng 2 seam công khai + layout module GĐ10/GĐ11, không đẻ API ngoài contract; (4) ẩn số rủi ro cao nhất (resume) đã tách khỏi lát-đầu → bắt đầu được ngay với rủi ro thấp (mọi chặng có tiền lệ chạy ở gốc). fake-trước-real giữ slice tất định, test được bằng `pytest` không cần LLM/staging.

**Phương án đã loại ở tầng cổng:**
- (a) *Gộp resume/SPIKE-1 vào slice-01 cho "một lát đầy đủ"* — **loại:** kéo ẩn số rủi ro cao nhất vào lát-đầu, nếu resume vướng thì cả lát tắc, không chứng minh được vòng lặp lõi chạy; tách slice-02 cho phép slice-01 xanh trước rồi mới gánh resume (đúng thứ-tự-gỡ-rủi-ro; khớp GĐ8 quyết định "GO dựng slice" nhưng chia nhỏ hơn để lát-đầu không dính SPIKE).
- (b) *Nhồi cả 4 guard + multi-round cho "bounded đầy đủ"* — **loại:** 1 guard (`max_steps`) đủ chứng minh cơ chế phanh chạy; 4 guard + multi-round = feature backlog S3.5.2 đầy đủ, vi phạm "đúng một slice", khó cô lập lỗi.
- (c) *Gọi LLM thật cho "chân thực"* — **loại:** phá luật fake-trước-real; test luồng sản phẩm không cần model thật, LLM thật thêm phi-tất-định + tốn tiền + kéo theo redact-raw-args (D4) chưa tới lượt. Simulator tất định trả cây plan cố định là đủ.
- (d) *Bật redact-raw-args thật trong slice* — **loại:** slice fake không sinh secret nên redact-thật chưa có gì để che; bật bây giờ = làm-sớm không cần thiết. Ghi open-Q RS-7 để gắn đúng lúc (trước write-tool THẬT, D4/GĐ12).

---

## 9. Bàn giao

```
═══ BÀN GIAO — Slice-01 "taskloop-happy-path" (HexAgent rebuild) ═══
Đã đóng khung : Scope(9 chặng happy-path + 1 guard) · Boundary(7 nhóm OUT có đích) · 8 AC đo được ·
                Plan 14 bước bám Module Map GĐ10 + layout GĐ11 · Files/modules 6 module (Knowledge không chạm) · 7 rủi ro.
Constitution  : 7 non-goals chốt (resume · control-plane · RAG · roles · LLM thật · multi-round · DB/auth/prod).
Fake-trước-real: LLM-plan = simulator tất định; tool fs_write/fs_read THẬT trong jail; test bằng pytest, không cần staging.
Invariant chạm: D1 no-bypass(AC-8) · D2 scope⊆parent(AC-4) · D5 worker-no-verdict(AC-7) + event-log-first(AC-2) + μ↓(AC-5) + bounded(AC-6).
Open-Q mang đi: RS-6 resume/SPIKE-1/D3 → slice-02 · RS-7 redact-raw-args/D4 → trước khi bật write-tool THẬT (GĐ12 Security).
Artifact      : rebuild-hex-agent/frame/slice-01-taskloop-happy-path.md (+ state pipeline/_frame.json)
→ Code thật slice-01 theo Plan §4 (lượt sau, đúng DoD GĐ11): tiếp tục /frame BUILD
→ Đóng khung slice-02 (resume/SPIKE-1) khi slice-01 xanh: /frame slice mới
→ Chứng minh chạy đúng (map AC→test→result) sau khi build: /uat (GĐ12)
════════════════
```

*Traceability:* frame **nhận** live-slice GĐ8 (`finish-by-evidence-tối-thiểu` — đường đi E2E 9+1 chặng, quyết định "GO dựng slice") → đóng khung **slice-01** = happy-path GĐ8 TRỪ resume + 1 guard; **nối AC** backlog GĐ9 (S3.2.1 scope→AC-4, S3.3.1 μ↓→AC-5, S3.4.1 order→AC-3, S3.5.1 evidence→AC-1, S3.5.2 bounded→AC-6, F1.5→AC-2) → **bám ranh giới** Module Map GĐ10 (2 seam công khai: execute_tool · run_task_loop/delegate; 6 module, Knowledge không chạm) + layout/DoD GĐ11 (D1/D2/D5 chạm→AC-8/4/7; D3/D4 tách→open-Q) → **bàn giao** code thật (lượt BUILD) + slice-02 resume + `/uat`. Mắt xích không đứt: ẩn số cao (resume/SPIKE-1, redact-thật) **tách có chủ đích** thành open-Q có địa chỉ, KHÔNG bịa đã-làm, KHÔNG kéo lùi lát-đầu.
