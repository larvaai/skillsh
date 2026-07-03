# 05 — Idea → Domain: HexAgent (clean rebuild)

> Skill `idea` · Giai đoạn 0–5 (Idea Intake → Business → Product/PRD → Domain Model). DỪNG ở Domain.
> Anchor: `00-understanding/REBUILD-BRIEF.md` + `evidence-A-core-loop.md` / `-B-domain-architecture.md` / `-C-roadmap.md`.
> Chế độ tự-quyết: mọi cổng do người viết đóng vai Product/CTO tự quyết GO, ghi rõ lý do + phương án đã loại. Không hỏi user.

---

## Góc nhìn lãnh đạo (đọc 60 giây)

**Ta đang xây lại cái gì.** Một agent mà bạn *giao đúng một mục tiêu*, nó tự lập kế hoạch, chia nhỏ thành các bước có thứ tự, giao cho các sub-agent làm, và **chỉ báo "xong" khi mọi tiêu chí nghiệm thu đều có bằng chứng thật** — không phải khi nó "tự thấy đủ". Đây là bản rebuild sạch của `hex_agent`, giữ nguyên vòng lặp lõi đó.

**Vì sao đáng làm.** Agent tự-điều-phối hiện có hai bệnh chết người mà thị trường đều dính: (1) **báo xong khống** — tự tuyên bố hoàn thành khi chưa thật sự làm; (2) **chạy vô hạn / leo thang quyền** — đốt tiền LLM, hoặc sub-agent tự cấp cho mình quyền vượt cha. Sản phẩm này biến "hoàn thành" thành thứ *chứng minh được bằng bằng chứng*, và biến "dừng" thành thứ *có biên cứng*. Đó là điểm bán lõi, không phải tính năng phụ.

**Cái quyết định thành/bại (1 dòng cho sếp).** Nếu MVP giao được một task thật mà agent plan → delegate → finish **có biên**, và ta chứng minh được nó *không bao giờ* FINISHED khi thiếu bằng chứng, thì phần còn lại (tools, UI control plane, RAG) chỉ là mở rộng an toàn quanh lõi đã chắc.

**Ta cố tình CHƯA làm gì bây giờ.** Chưa chọn kiến trúc/framework/DB cụ thể (đó là `shape`/`stack`), chưa realtime Control-Tower UI, chưa Departments/IntentRouter/Ledger (park-with-trigger). Stage này dừng đúng ở Domain Model — đủ rõ để định hình kiến trúc.

---

## GĐ0 — Idea Intake

| Trường | Nội dung |
|---|---|
| **Ý tưởng** | Rebuild sạch `hex_agent`, tâm điểm là vòng lặp tự-điều-phối task: giao 1 task → plan → order → delegate → finish-khi-thật-xong-có-biên. |
| **Slug** | `hex-agent-rebuild` |
| **Độ rõ (Router)** | **rõ ràng** — đã biết cho ai (đội cần agent làm task nhiều-bước tự trị), input (1 task/goal), output (task FINISHED có bằng chứng), ranh giới (6 bounded context đã đặt tên trong BRIEF). |
| **Độ khả thi (Router)** | **khả thi rõ** — bản gốc đã chạy (`evidence-C:E01–E10 ✓`, 327 tests, E19 ✓). Không có ẩn số kỹ thuật/business chặn đường; rebuild là tái dựng cái đã chứng minh. → **Nhánh C** (đi GĐ1→GĐ5). |
| **Nguồn sự thật** | Không bịa; mọi khẳng định cơ chế neo về `evidence-A/B/C:file:line` của hex_agent gốc. |

---

## GĐ1 — Business Discovery (WHY)

**Ai đau & đau gì.** Đội xây agent tự trị (internal platform team / builder). Hai nỗi đau đo được:
- **Báo-xong-khống**: agent tuyên bố hoàn thành khi chưa làm → công việc phải làm lại, mất niềm tin. Bản gốc chống bằng gate nghiệm thu-bằng-bằng-chứng (`evidence-A §4`, `judge_acceptance` `supervisor/graph.py:357-382`).
- **Chạy vô hạn / đốt tiền**: vòng lặp không biên → chi phí LLM tăng tuyến tính, không dừng. Bản gốc chống bằng chồng guard (`evidence-A §4-5`: max_rounds, no-progress, repeat-decision, parse-budget, MAX_DEPTH, per-root step budget).

**Chi phí nếu KHÔNG làm (ước lượng thô — không có số đo thực, đánh dấu open-Q).**
- Nếu để agent tự-báo-xong không gate: một phần công việc "xong" là giả → tỉ lệ phải-làm-lại > 0 và không audit được. Không có số production gốc → **open-Q OQ-1**.
- Nếu để loop không biên: mỗi task hỏng có thể đốt tới trần (bản gốc đặt per-delegation `max_steps=100`, `max_depth=8`, `policy.py:8-32`) — chi phí thực = trần × giá token, chưa có baseline → **open-Q OQ-1**.

**Success metric (đo được, chọn 1 lõi).**
> **M1 — "Zero false-finish":** trong bộ test nghiệm thu, số lần agent đạt `FINISHED` mà có ≥1 AC thiếu evidence thật = **0**. (Kiểm bằng oracle: `all_accepted()` chỉ true khi mọi AC `status=="passed" ∧ evidence_ids≠∅`, `state.py:35-37`.)

Metric phụ (theo dõi, không phải gate GĐ1):
- **M2 — "Bounded":** mọi task kết thúc ở trạng thái terminal (FINISHED/BLOCKED/FAILED) trong ≤ max_rounds, không treo.
- **M3 — "No escalation":** 0 delegation có scope con ⊄ cha (validate `policy.py:25-26`).

**Quyết định cổng GĐ1 (tự-quyết, đóng vai Product/CTO).**
- **GATE: GO.** Đáng đầu tư đi tiếp. Lý do: cơ chế lõi đã được chứng minh trong bản gốc (rủi ro kỹ thuật thấp), và hai nỗi đau (false-finish, runaway) là *khác biệt sản phẩm*, không phải nice-to-have.
- **Phương án đã loại:** (a) "chỉ wrap một single-agent loop, bỏ delegation" — loại vì mất chính LÕI sản phẩm P3 (multi-agent, `evidence-C §1 E10`). (b) "đợi có số production rồi mới build" — loại vì rebuild dựa trên hệ đã chạy, số production là để *tinh chỉnh trần*, không phải điều kiện tồn tại.
- **Open-Q mang sang sau:** OQ-1 (baseline chi phí/false-finish thực) → GĐ Operate.

---

## GĐ2–4 — Product / Requirements / PRD (WHAT VALUE / WHAT EXACTLY)

### Product Discovery

**Ai dùng.** Builder giao task cho agent (qua envelope), và người vận hành quan sát/điều khiển (control plane — sau MVP).

**Journey AS-IS → TO-BE.**
- **AS-IS** (agent tự trị ngây thơ): giao task → agent chạy tự do → tự nói "done" (không kiểm) → hoặc chạy đến hết token. Không audit, không resume, không biên.
- **TO-BE**: giao 1 task → agent plan thành cây có chứng minh dừng → order bước theo dependency → delegate qua *một* chokepoint có scope-check → judge acceptance bằng bằng chứng thật → FINISHED chỉ khi mọi AC có evidence; guard chặn runaway. Mọi hành động phát event → audit + resume được.

### MVP (chốt rõ)

> **MVP = "Giao 1 task, agent plan + delegate + finish CÓ BIÊN."**
Cụ thể một task chạy end-to-end:
1. **Accept** task (envelope) → `TaskAccepted`.
2. **Plan/Decompose** task thành cây (forest theo parent + DAG theo depends_on, cả hai acyclic), mỗi node `work|reduce` có `done_when`; cổng-2 `accept_decomposition` chạy TRƯỚC khi đổi cây, có **chứng minh dừng** μ(node)=len(done_when) co ngặt (`evidence-A §2`, `accept.py:52-128`) → `PlanDecomposed`.
3. **Order** — `next_node()` = node pending trái nhất mà mọi dependency đã done (topo depth,order) — "không leo sớm" miễn phí (`tree.py:43-51`).
4. **Delegate** — qua `DelegationManager.delegate` (chokepoint RIÊNG, không phải method kernel): validate policy (depth≤max, scope ⊆ parent, max_steps) → child session → run → merge artifact → đóng child (`evidence-A §3`, `delegation/manager.py:63-192`) → `NodeDelegated`.
5. **Judge & finish** — `judge_acceptance`: mỗi AC "passed" cần ≥1 bằng chứng THẬT (artifact/tool_result/reviewer_report/diff/test_result), từ chối scaffolding; `all_accepted()` → `FINISHED` (`evidence-A §4`) → `AcceptanceJudged` + `TaskFinished`.
6. **Bounded** — guard dừng cứng: max_rounds, no-progress, repeat-decision, parse-budget, MAX_DEPTH, per-root step budget (`evidence-A §5`) → nếu chạm guard: `TaskBlocked`.

Trên nền kỹ thuật đủ để lõi chạy an toàn: **một chokepoint `execute_tool`** (mọi hành động qua đúng một cửa, `core/kernel.py:106-150`), **event-log-first** (mọi capability call phát `tool.requested/completed`), **SQLite = chân lý resume** (`langgraph.sqlite` truth, `checkpoint.json` chỉ là projection).

### Scope IN / OUT

**IN (MVP):**
- Vòng lặp: accept → plan(+gate-2 chứng minh dừng) → order → delegate(scope-check) → judge(evidence) → finish/blocked.
- Một chokepoint `execute_tool` + scope-check + envelope chuẩn hoá.
- Event log first-class (audit + replay + resume qua SQLite).
- Guard chống runaway (đủ 6 loại ở trên).
- Delegation chokepoint RIÊNG + scope child ⊆ parent.

**OUT (cố tình KHÔNG làm ở MVP — ghi thành chữ):**
- Realtime Control-Tower UI + transport (SSE/POST /api) + approval-checkpoint B2–B14 (`evidence-C §1 E21 pending`). MVP chỉ cần event-log-first, chưa cần UI điều khiển trực tiếp.
- RAG/Qdrant (E08), Skills progressive-disclosure (E07) — mở rộng, không thuộc lõi finish-loop.
- Departments (E11), IntentRouter (E12), Software Factory (E13), Ledger/Memory (E14), Labs (E20) — **park-with-trigger, YAGNI** (`evidence-C §4`).
- Enforcement authz đầy đủ ở command bridge (hiện gốc còn "trust-O bypass", `evidence-B §6`) — MVP giữ `issued_by` = attribution, authz thật để pha sau.

### NFR (có số khi liên quan)

| NFR | Số / ràng buộc | Nguồn |
|---|---|---|
| Biên vòng lặp | per-delegation `max_steps=100`, `max_depth=8` | `policy.py:8-32` |
| Biên decompose | root max_steps; per-node K=3 / K_LEAF=5; parse max=8; MAX_DEPTH=6 | `evidence-A §5`, `solve.py:34` |
| Chống rò secret | 0 secret trong `ui_payload`; 15 SECRET_KEYS mask trước fan-out | `evidence-B §6` |
| Resume | resume đúng run_id từ SQLite; 0 side-effect re-run (state serializable-only) | I10/I11, `evidence-C §3` |
| Isolation | 0 rò state giữa các run (freeze kernel + session sống) | I2/I3 |
| Audit | seq monotonic gap-free per run; replay(events[0..n]) = Snapshot(n) deterministic | `evidence-B §7 (ii,v)` |

### PRD rút gọn (1 trang)

- **Goal:** một agent tự-điều-phối giao được task nhiều-bước, chỉ FINISHED khi mọi AC có bằng chứng thật, và không chạy vô hạn.
- **Success metric:** M1 zero false-finish (gate); M2 bounded; M3 no-escalation.
- **Scope:** như IN/OUT trên.
- **Rollout thô:** theo build-sequence gốc — P0 Foundation (kernel+discipline+llm+observability) → P1–P2 single-agent+tools → **P3 multi-agent TaskLoop+delegation+acceptance = lõi MVP** → P4 control plane (sau) (`evidence-C §2`).
- **Open questions treo:** OQ-1 baseline (→Operate); OQ-2 danh mục đầy đủ ~50 event / 16 command (`config/runtime_*_types.yaml`) — chốt ở GĐ shape/skeleton; OQ-3 mismatch tên event kernel phát `tool.requested/completed` vs registry khai `tool.call_requested/before_call/after_call` — reconcile ở shape (`evidence-B §3`).

**Quyết định cổng GĐ2–4 (tự-quyết).**
- **GATE 1 "Hướng sản phẩm & MVP đủ rõ?": GO.** MVP cắt đúng lõi (plan→delegate→finish có biên); scope OUT rõ ràng theo YAGNI. Phương án đã loại: (a) MVP = "single-agent + tools, hoãn delegation" — loại vì delegation + acceptance-by-evidence LÀ điểm bán, hoãn = mất lõi. (b) MVP = "full control-plane UI ngay" — loại vì UI là consumer của read-model, không phải cơ chế lõi; event-log-first đủ cho MVP.
- **GATE 2 "PRD đủ tin cậy?": GO.** Số NFR đã neo về file:line gốc; open-Q có chỗ chốt (shape/skeleton/operate), không bịa số. Đủ để sang Domain.

---

## GĐ5 — Domain Model (WORLD MODEL) — DỪNG Ở ĐÂY

> Entity KHÔNG phải bảng DB. Đi: Bounded Context → Entity (identity + lifecycle) → Business Rule bất biến → Domain Event → Data Ownership.

### 5.1 Bounded Contexts (6)

| Context | Trách nhiệm lõi | Nguồn |
|---|---|---|
| **Orchestration** | Vòng lặp task: plan/decompose, order, delegate, acceptance/finish. Chứa Agent-O, cây kế hoạch, gate nghiệm thu. | `evidence-A §1-4`, `evidence-B §5 supervisor/delegation` |
| **Execution Core** | Kernel chokepoint (`execute_tool`), Session sống, registry, envelope. "Nhân đông cứng, session sống". | `evidence-B §2,§4` |
| **Discipline** | Logic thuần chia sẻ: json_gate, finish_gate, budget, condense. | `evidence-B §5`, `discipline/*` |
| **Tools & Safety** | Sandbox (workspace jail), PolicyGate fail-closed, SafeToolPort per-tool policy. | `evidence-B §5-6` |
| **Observability / Control Plane** | EventEmitter (gate→seq→redact→fan-out), RuntimeEvent envelope, TaskLoopSnapshot read-model, RuntimeCommand, Redactor. | `evidence-B §2-4` |
| **Knowledge** (optional) | RAG/Qdrant health-gated, offline-first. Ngoài lõi MVP. | `evidence-B §5`, `evidence-C E08` |

### 5.2 Entities (identity + lifecycle)

| Entity | Identity | Lifecycle | Neo |
|---|---|---|---|
| **Task/Goal** | `task_id` (trong `TaskEnvelope`) | accepted → running → FINISHED \| BLOCKED \| FAILED | `evidence-A §7`, `schemas.py:11-26` |
| **Plan** | cây gắn với task (forest+DAG) | empty → decomposed (mỗi lần chia qua gate-2) → closed | `evidence-A §2` |
| **Node(work\|reduce)** | `id` (trong Tree) | pending → active → (done \| blocked \| decomposed) | `node.py:28,102-177` |
| **DoneWhen** (criterion) | (check, params, artifact) thuộc node | bất biến trong node; verdict keys CẤM | `node.py:50-100`, `:20` |
| **DependencyEdge** | (from,to) trong `depends_on` | acyclic, cố định sau khi đặt | `evidence-A §2` (DAG acyclic) |
| **Run** | `run_id` (trong `SessionIdentity`) | mở khi task chạy → resume cùng run_id từ SQLite → terminal | `evidence-B §2`, `evidence-C §3` |
| **Session / SessionIdentity** | `session_id` + lineage 7-field (session/run/task/agent/parent_session/delegation/depth) | tạo bởi SessionFactory (child scope⊆parent) → mutate state → restore/close | `core/session.py:49-85,188-194` |
| **Delegation** | `delegation_id` | request → validate policy → child session → run → merge → finished | `delegation/manager.py:63-192` |
| **AcceptanceCriterion** | `id` (trong `AcceptanceCheck`) | pending → passed \| failed; `is_satisfied` = passed ∧ evidence≠∅ | `state.py:28-49` |
| **Evidence** | `evidence_id` trên Blackboard | tạo bởi hành động thật; phân loại real vs scaffolding | `evidence.py:16-40` |
| **Budget** | thuộc loop/delegation/decompose | knob cố định trước run; guard đọc để dừng | `discipline/budget.py:10-67`, `policy.py:8-32` |
| **Event (RuntimeEvent)** | `event_id` + `seq` (per-run monotonic) | phát → validate→seq→redact→fan-out; bất biến sau phát | `control/events.py:113+`, `emitter.py:53+` |
| **Command (RuntimeCommand)** | `idempotency_key` | issued → apply_at (immediate/if_waiting/next_checkpoint) → ack | `control/*`, `evidence-B §3` |
| **Checkpoint** | (theo run) — ⚠️ 3 loại khác nhau | core StateStore snapshot / control approval-gate / orchestrator UI-projection | `evidence-B §2` |
| **Permission** | per-agent caps | effective_from ∈ {immediately, next_turn, next_checkpoint} | `evidence-B §2` |

### 5.3 Business Rules — BẤT BIẾN (không được phá khi rebuild)

1. **Chỉ FINISHED khi mọi AC có evidence THẬT.** `all_accepted()` = mọi AC `status=="passed" ∧ evidence_ids≠∅`; scaffolding (session_plan/context_packet/ac_report) KHÔNG tính là evidence — chỉ artifact/tool_result/reviewer_report/diff/test_result. (`state.py:35-37`, `evidence.py:16-23`, `graph.py:357-382`)
2. **Worker KHÔNG tự ghi verdict — chỉ gate ghi.** Node/`DoneWhen` cấm verdict keys; gate (accept/judge) là nơi DUY NHẤT gán outcome. (`node.py:20`, `evidence-A "Core immutables"`)
3. **Scope child ⊆ parent.** Mọi delegation con chỉ được tập capability ⊆ cha; SessionFactory + `policy.py:25-26` enforce; Broker nắn context nhưng KHÔNG mở rộng scope; O đặt `allowed_capabilities`. (`evidence-A §3`, `evidence-B §6`)
4. **Plan phải có chứng minh dừng μ co ngặt.** Cổng-2 `accept_decomposition` (structural, chạy TRƯỚC khi đổi cây): μ(node)=len(done_when), mỗi child được chấp nhận phải làm μ co NGẶT; + coverage-by-implication; + phát hiện RENAME (Jaccard>0.80)/STUCK. (`accept.py:52-128`, `evidence-A §2`)
5. **Mọi hành động qua `execute_tool`.** Một chokepoint duy nhất: build ToolRequest → publish `tool.requested` → scope-check → middleware chain → publish `tool.completed|failed` → trả `CapabilityResult`. Không có đường vòng; observability/safety/envelope gắn đúng một lần. (`core/kernel.py:106-150`, I1)

Bất biến nền (kế thừa, không phá): freeze kernel trước run đầu → 0 rò state (I2/I3); redact tại biên trước fan-out (I16); SQLite = chân lý resume, checkpoint atomic (commands+round+save một transaction, I10/I11); attribution (`issued_by`) ≠ authz (I17).

### 5.4 Domain Events (chính)

| Event | Khi nào phát | Neo |
|---|---|---|
| **TaskAccepted** | envelope nhận, task vào running | `evidence-A §1`, `loop.py:run()` |
| **PlanDecomposed** | gate-2 accept xong, cây đổi (child thêm, reduce node synthetic) | `evidence-A §2`, `_decompose()` |
| **NodeDelegated** | `DelegationManager.delegate` chạy cho một node/assignment | `evidence-A §3`, `delegation.finished` |
| **AcceptanceJudged** | `judge_acceptance` chấm AC theo evidence | `evidence-A §4`, `graph.py:357-382` |
| **TaskFinished** | `all_accepted()` true → terminal FINISHED | `evidence-A §4`, `state.py:107-108` |
| **TaskBlocked** | chạm guard (max_rounds/no-progress/repeat-decision/parse-budget/depth) → terminal BLOCKED | `evidence-A §4-5` |

(Ánh xạ tới catalog runtime gốc — session.*/tool.*/loop.*/delegation.* — chốt danh mục đầy đủ ở shape; **OQ-2**.)

### 5.5 Data Ownership

| Dữ liệu | Chủ sở hữu (context) | Ghi chú |
|---|---|---|
| Cây kế hoạch (Tree, Node, DoneWhen, edges) | Orchestration | YAML checkpoint + Journal audit gốc |
| AcceptanceCheck + verdict | Orchestration (gate viết) — worker chỉ đề xuất | Rule #2 |
| Evidence (Blackboard) | Orchestration | resolve khi judge |
| Session state / StateStore | Execution Core | per-run, deep-copy isolation; state CHỈ ở session |
| SessionIdentity (lineage) | Execution Core (SessionFactory là constructor duy nhất) | child scope⊆parent |
| RuntimeEvent stream + seq | Observability/Control Plane | seq monotonic per-run; nguồn audit/replay |
| RuntimeCommand queue + ack | Observability/Control Plane | idempotency_key |
| Redaction (ui_payload) | Observability/Control Plane | mask trước fan-out |
| SQLite `langgraph.sqlite` (resume truth) | Orchestration/graph | `checkpoint.json` = projection UI, KHÔNG đọc để resume |
| Budget knobs | Discipline (loop) / Delegation (per-delegation) / Decompose | cố định trước run |
| Sandbox/workspace + policy | Tools & Safety | jail `var/workspace/`, PolicyGate fail-closed |

**Quyết định cổng GĐ5 (tự-quyết, đóng vai CTO).**
- **GATE: GO — Domain đủ rõ để định hình kiến trúc & ranh giới module → DỪNG.** 6 bounded context có ranh giới; entity có identity+lifecycle; 5 rule bất biến + nền kế thừa liệt kê đủ; 6 domain event đặt tên; data ownership rõ ai giữ gì. Không đoán tiếp sang kiến trúc.
- **Phương án đã loại:** (a) gộp Discipline vào Execution Core — loại vì Discipline là logic thuần chia sẻ (json/finish/budget/condense) tái dùng nhiều context, tách ra tránh coupling. (b) coi Node như bảng DB (schema-first) — loại, đúng cảnh báo skill "nhảy PRD→DB schema là sai domain": Node là entity domain có lifecycle, không phải row.
- **Open-Q mang sang shape (GĐ6):** OQ-2 (danh mục đầy đủ event/command), OQ-3 (reconcile mismatch tên event), + ranh giới v0 vs full (từ ATLAS open-Q).

---

## Bàn giao sau GĐ5

```
═══ BÀN GIAO — HexAgent (clean rebuild) ═══
Domain đã chốt: 6 bounded context (Orchestration/Execution-Core/Discipline/Tools&Safety/
  Observability-ControlPlane/Knowledge); 5 rule bất biến (finish-có-evidence · gate-ghi-verdict ·
  scope child⊆parent · plan chứng-minh-dừng μ co ngặt · mọi hành động qua execute_tool);
  6 domain event (TaskAccepted→PlanDecomposed→NodeDelegated→AcceptanceJudged→TaskFinished/TaskBlocked).
Artifact: rebuild-hex-agent/pipeline/05-idea-domain.md
Open-Q sang GĐ6: OQ-2 danh mục event/command · OQ-3 reconcile tên event · ranh giới v0 vs full.
→ Kiến trúc/stack/module (GĐ6+): chạy /shape rồi /stack (đã có Domain đầu vào).
→ Build ngay một lát cắt: /frame (vd slice "accept→plan→next_node").
→ Hiểu code gốc trước khi đụng: /explain trên .ai-understanding/ (ATLAS đã dựng).
════════════════
```

*Traceability:* stage này (idea, GĐ0–5) nhận đầu vào từ `00-understanding/*` (atlas/evidence), là artifact pipeline ĐẦU TIÊN; bàn giao Domain Model xuống `shape` (GĐ6).
