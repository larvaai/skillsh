# 10 — Modules: Module Map + Module Contract — HexAgent (clean rebuild)

> Skill `modules` · Giai đoạn 10 (Module & Team Ownership — SỞ HỮU). Nhận **Domain Model GĐ5** (`pipeline/05-idea-domain.md`: 6 bounded context, 5 rule bất biến, 6 domain event, data ownership) + **Architecture Brief GĐ6** (`pipeline/06-shape.md`: 6 module = 6 context, 6 ADR, 2 chokepoint) + roadmap epic gốc (`00-understanding/REBUILD-BRIEF.md` §Roadmap + `evidence-C`). Ra bằng **Module Map** (context → module → owner → phụ thuộc) + **Module Contract** cho từng module.
> Anchor gốc: `REBUILD-BRIEF.md` (7 invariant) + `evidence-A/B/C` + `ATLAS.md`. Ranh giới bám **bounded context GĐ5**, KHÔNG theo màn hình. Không đẻ context mới.
> Chế độ tự-quyết: cổng go/no-go do người viết đóng vai **Kiến trúc sư + Eng-manager (chủ sở hữu, trình bằng chứng) · CTO (mở cổng)** tự quyết, ghi rõ lý do + phương án đã loại. Không hỏi user. `modules` KHÔNG code — vẽ ranh giới + contract rồi bàn giao `/delivery` (GĐ11), mỗi slice đóng khung bằng `/frame`.

```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Roadmap + Backlog (Epic→Feature→Story→AC)" lấy từ REBUILD-BRIEF §Roadmap + evidence-C (epic E01–E21), CHƯA qua cổng GĐ9 (skill /backlog) trong project này — pipeline/09-*.md không tồn tại.
- Rủi ro: (1) chưa truy vết ngược được về một artifact GĐ9 đã-qua-cổng; (2) có thể lệch nếu backlog thật khác roadmap gốc; (3) map feature→module dựa trên EPIC (thô hơn story/AC).
- Vẫn tiếp tục: domain (GĐ5) + kiến trúc (GĐ6) ĐÃ qua cổng và đã ánh xạ 6 module = 6 context 1–1 → ranh giới module có nền vững, chỉ phần "phủ hết feature" là dùng epic thay story. Muốn chuẩn + traceability đầy đủ: chạy /backlog trước để có Backlog đã-qua-cổng rồi kiểm chéo story→module.
```

---

## ── GÓC NHÌN LÃNH ĐẠO (đọc trước, 60 giây — không cần biết code) ──

**Ai chịu trách nhiệm cái gì khi có sự cố.** Hệ chia thành **6 module**, mỗi module đúng **một team sở hữu** — không có phần "chung của mọi người", nên khi hỏng biết gõ cửa ai ngay:

| Module | Team owner | Sở hữu (giữ phần nghiệp vụ nào) | KHÔNG sở hữu |
|---|---|---|---|
| **Orchestration** | Team **Orchestration** | Vòng lặp task: lập kế hoạch, sắp thứ tự, giao-việc, chấm nghiệm-thu, phanh chống chạy-vô-hạn. *Đây là LÕI sản phẩm.* | Chạy tool thật (Execution-Core) · dựng UI/audit (Control-Plane) |
| **Execution-Core** | Team **Platform** | Một cửa duy nhất mọi hành động đi qua (`execute_tool`); trí nhớ của mỗi lần chạy (session). "Nhân đông cứng, session sống". | Quyết *khi nào* giao việc (Orchestration) · nội dung tool (Tools-Safety) |
| **Discipline** | Team **Platform** | Thư viện luật thuần: kiểm định dạng JSON, chặn báo-xong-ẩu, đếm ngân sách, nén ngữ cảnh. | Không giữ dữ liệu sống nào; chỉ là hàm thuần |
| **Tools-Safety** | Team **Safety** | Nhà tù cho tool (chỉ đụng được thư mục cho phép); danh sách chặn cứng; mỗi tool một chính sách. | Quyết ai được gọi tool (scope là của Execution-Core) |
| **Control-Plane/Observability** | Team **Observability** | Sổ sự kiện bất biến (audit + phát lại), che secret trước khi lộ ra ngoài, kênh lệnh điều khiển. | Business logic loop (chỉ *tiêu thụ* event, UI ⟂ core) |
| **Knowledge** *(tùy chọn, ngoài lõi MVP)* | Team **Platform** | Tra cứu tri thức (RAG), hỏng thì im lặng trả rỗng chứ không làm sập loop. | Không nằm trên đường tới FINISHED |

**Một điều CTO phải nhớ (ranh giới sống-còn).** Có đúng **hai cửa công khai** để các team gọi vào nhau, mọi thứ khác là nội bộ module:
1. **Execution-Core** mở đúng một cửa: `execute_tool` — *mọi* hành động (gọi LLM, chạy tool) phải chui qua đây. Tool tự gọi thẳng, không qua cửa này = **vi phạm ranh giới** (mất audit + mất kiểm-quyền).
2. **Orchestration** mở đúng hai cửa: `run_task_loop` (khởi động vòng lặp) và `DelegationManager.delegate` (giao-việc-cho-sub-agent, cửa RIÊNG có luật scope con ⊆ cha).
Cấm mọi đường vòng cross-module. Nếu hai cửa này giữ được kỷ luật, **6 team chạy song song mà không giẫm nhau**, và hai bệnh chết người (báo-xong-khống, chạy-vô-hạn/leo-quyền) bị chặn bằng *ranh giới sở hữu*, không bằng lời hứa.

**Vì sao chia đúng thế này.** Ranh giới bám **bounded context của Domain (GĐ5)** — theo *ai-đổi-cái-gì* và *ai-sở-hữu-dữ-liệu-nào*, KHÔNG theo màn hình. Cây kế hoạch + nghiệm-thu chỉ Orchestration đụng; session state chỉ Execution-Core đụng; sổ event chỉ Control-Plane đụng. Không có mẩu dữ liệu nào hai team cùng ghi → không có xung đột "ai đúng".

---

## ── CHI TIẾT KỸ THUẬT (cho dev) ──

## 1. Module Map (bounded context → module → owner → phụ thuộc)

Đi từ Domain GĐ5 §5.1 (6 bounded context) — ánh xạ **1–1** sang module (đã chốt ở GĐ6 §1). Phụ thuộc = ai gọi cửa của ai.

```text
MODULE MAP — HexAgent (clean rebuild)   [→ = phụ thuộc, gọi vào cửa nào]

  ORCHESTRATION       ← context Orchestration (GĐ5 §5.1)   · Owner: Team Orchestration · LÕI
      seam vào (public): run_task_loop(envelope) · DelegationManager.delegate(request)
      → EXECUTION-CORE     qua execute_tool  (mọi hành động LLM/tool)          [cửa DUY NHẤT]
      → CONTROL-PLANE      phát domain event (in-process bus, một chiều) + đọc snapshot read-model
      → DISCIPLINE         gọi hàm thuần (json_gate/finish_gate/budget/condense) — không mạng
      → SQLite (embedded)  ghi checkpoint atomic (commands+round+save một txn) = chân lý resume

  EXECUTION-CORE      ← context Execution Core (GĐ5 §5.1)  · Owner: Team Platform · LÕI hạ tầng
      seam vào (public): execute_tool(request)   [CHOKEPOINT DUY NHẤT — mọi module hành động đi qua]
      → TOOLS-SAFETY       qua SafeToolPort (tool chạy trong sandbox jail + PolicyGate)
      → DISCIPLINE         middleware Budget/Condense đọc luật thuần
      → CONTROL-PLANE      phát tool.requested/completed|failed (event-log-first)
      → LLM provider       LLM-as-capability (đi QUA execute_tool, không call trực tiếp)

  DISCIPLINE          ← context Discipline (GĐ5 §5.1)      · Owner: Team Platform · thư viện thuần
      seam vào (public): json_gate.parse · finish_gate.check · budget.step · condense.run
      → (không phụ thuộc module nào — pure logic, stateless; được Orchestration + Execution-Core DÙNG)

  TOOLS-SAFETY        ← context Tools & Safety (GĐ5 §5.1)  · Owner: Team Safety · biên an toàn
      seam vào (public): SafeToolPort.execute(tool_request)  (chỉ Execution-Core gọi vào, qua port)
      → (không gọi ra module khác; là "lá" — Execution-Core gọi VÀO nó)

  CONTROL-PLANE / OBSERVABILITY  ← context Observability/Control Plane (GĐ5 §5.1) · Owner: Team Observability
      seam vào (public): EventEmitter.emit(event) · build_snapshot(events) · CommandQueue.submit(command)
      → Event log store    append-only jsonl + summary + metrics
      → (chỉ TIÊU THỤ event của các module khác; KHÔNG gọi ngược vào business logic — UI ⟂ core)

  KNOWLEDGE (optional, NGOÀI lõi MVP)  ← context Knowledge (GĐ5 §5.1) · Owner: Team Platform
      seam vào (public): RagPort.query(q)  (health-gated, never raises)
      → Vector KB (RAG store)  bất đồng bộ/tùy chọn; KB down → trả rỗng, loop vẫn chạy
      → (được Orchestration/worker DÙNG tùy chọn; không nằm trên critical path tới FINISHED)
```

**Sơ đồ phụ thuộc (ai gọi ai) + ranh giới security/integration:**

```text
     [Người giao task] ──TaskEnvelope──▶ ( run_task_loop )
                                              │
                            ┌─────────────────▼─────────────────┐
                            │          ORCHESTRATION            │  ← LÕI (owns plan tree, acceptance, evidence)
                            │  plan · order · delegate · judge  │
                            └──┬──────────┬──────────┬──────────┘
              execute_tool ────┘          │          └──── domain events / snapshot
              (cửa DUY NHẤT)              │                        │
                    ▼            DelegationManager.delegate        ▼
        ┌───────────────────┐   (cửa RIÊNG, scope⊆parent)  ┌──────────────────────┐
        │  EXECUTION-CORE   │◀───────────┘                 │  CONTROL-PLANE /      │
        │  execute_tool     │─── tool.requested/completed ▶│  OBSERVABILITY        │  ← audit boundary
        │  Session/Identity │                              │  emit·snapshot·command│    (redact TẠI biên)
        └──┬──────────┬─────┘                              └──────────────────────┘
   SafeToolPort    (dùng)                                          │ append
           ▼           ▼                                           ▼
   ┌──────────────┐ ┌────────────┐                        ┌──────────────────┐
   │ TOOLS-SAFETY │ │ DISCIPLINE │  (pure lib, dùng bởi   │ Event log store   │
   │ sandbox jail │ │ json/finish│   Orch + Exec-Core)    │ jsonl+summary     │
   │ PolicyGate   │ │ budget/cond│                        └──────────────────┘
   └──────────────┘ └────────────┘         [KNOWLEDGE(opt): RagPort.query — ngoài critical path]
   ═══ security boundary: workspace jail + scope-check ═══   ═══ integration boundary: BE↔UI 3-seam (sau MVP) ═══
```

**Kiểm chéo feature (epic gốc → module) — không epic mồ côi, không epic hai chủ:**

| Epic (REBUILD-BRIEF §Roadmap / evidence-C) | Rơi vào module | Ghi chú |
|---|---|---|
| E01 Microkernel Core | Execution-Core | chokepoint + session + registry |
| E02 Output Discipline | Discipline | json/finish/budget/condense |
| E03 LLM Adapter | Execution-Core | LLM-as-capability đi QUA execute_tool (adapter port thuộc Exec-Core) |
| E04 Observability | Control-Plane/Observability | event log + summary + metrics |
| E05 Graph/Resume | Orchestration | graph topology + SQLite checkpoint (resume truth thuộc Orch/graph) |
| E06 Tools & Safety | Tools-Safety | sandbox + PolicyGate + SafeToolPort |
| E07 Skills | Discipline | progressive-disclosure = logic thuần render-contract (rìa; xem lý do gộp §3) |
| E08 RAG | Knowledge (optional) | health-gated, ngoài lõi MVP |
| E09 Roles & Lenses | Orchestration | role allowlist = union−forbidden feed vào allowed_capabilities (thuộc điều-phối scope) |
| E10 TaskLoop+Delegation+Acceptance | Orchestration | LÕI: run_task_loop + DelegationManager + judge_acceptance |
| E21 Realtime Control Plane | Control-Plane/Observability | contracts→emitter→transport→UI→reliability (sau MVP) |

Feature phủ hết vào đúng một module. (Epic future E11–E14/E20 = park-with-trigger, chưa cấp module — YAGNI; khi thaw sẽ cấp owner ở vòng modules sau.)

**Lý do gộp/tách + phương án đã loại (cho CTO audit ranh giới sau):**

- **Giữ 1 context = 1 module (không tách nhỏ hơn).** GĐ5 đã chốt 6 context có data-ownership sạch; GĐ6 ánh xạ 1–1. Đã cân **tách Delegation thành module riêng** (nó là chokepoint riêng, ADR-003) → **loại**: delegation *đọc/ghi cùng dữ liệu* của Orchestration (plan tree, allowed_capabilities do O đặt, scope⊆parent) — tách ra sẽ chia đôi quyền sở hữu "ai điều phối scope" cho hai team, đúng thứ rule #3 cấm nhập nhằng. Giữ delegation *trong* Orchestration nhưng expose như **cửa public riêng** đủ để audit tách bạch mà không chia data-ownership.
- **Gộp E07 Skills vào Discipline** (thay vì module riêng). Skills = render-contract/render-full = **logic thuần stateless** giống json_gate/condense, không sở hữu dữ liệu sống, một team ít đổi. **Đã cân tách Skills riêng** → loại: sẽ đẻ một module rìa chỉ có hàm thuần, thêm biên contract mà không thêm ranh giới sở hữu thật. Gộp vào Discipline (cùng bản chất "thư viện luật thuần") gọn hơn. (Rìa — nếu Skills phình thành catalog động có state → tách lại; ghi open-Q OQ-M1.)
- **Discipline + Execution-Core cùng owner Team Platform.** Đã cân **gộp Discipline vào Execution-Core một module** → loại (theo GĐ5: Discipline là logic *chia sẻ* cả Orchestration lẫn Execution-Core dùng; gộp vào Exec-Core tạo coupling ngược từ Orchestration vào nhân). Giữ *hai module* (ranh giới rõ để test độc lập) nhưng *một owner* (cùng đội hạ tầng, giảm chi phí phối hợp) — module ≠ team, một team ôm được nhiều module gần nhau.
- **Knowledge tách riêng dù optional.** Change frequency + tính "được-phép-hỏng" khác hẳn lõi (KB down không được làm sập loop). Đã cân **gộp vào Orchestration** → loại: sẽ kéo một phụ thuộc mạng tùy-chọn vào critical path lõi. Tách + health-gate giữ lõi sạch.

---

## 2. Module Contract (mỗi module một contract)

Độ sâu theo **Đủ-là-đủ**: module LÕI/nhiều-team-gọi/security-nặng (Orchestration, Execution-Core, Control-Plane, Tools-Safety) → contract đầy đủ; module thuần/rìa (Discipline, Knowledge) → gọn kèm lý do. `Owner + Responsibilities + Owns + Does NOT own + Public API` BẮT BUỘC mọi module; "Does NOT own" không bao giờ bỏ.

---

### CONTRACT — ORCHESTRATION            Owner: Team Orchestration   [LÕI sản phẩm]

```text
[Lãnh đạo]        : Giữ TOÀN BỘ vòng lặp "chỉ kết thúc khi thật xong" — lập kế hoạch, sắp thứ tự,
                    giao việc cho sub-agent, chấm nghiệm-thu bằng bằng chứng, phanh chống chạy-vô-hạn.
                    Task treo/báo-xong-sai/loop đốt tiền → hỏi Team Orchestration.
Responsibilities  : plan/decompose (+ Cổng-2 chứng-minh-dừng) · order (next_node) ·
                    delegate (cửa riêng, scope⊆parent) · judge_acceptance (gate ghi verdict) · guards+budget.
Owns (data/event) : Cây kế hoạch (Tree, Node, DoneWhen, DependencyEdge) · AcceptanceCheck + verdict
                    (worker chỉ đề xuất, GATE ghi — rule #2) · Evidence (Blackboard) · SQLite langgraph.sqlite
                    (chân lý resume; checkpoint.json = projection UI). allowed_capabilities per-assignment (O đặt).
                    Phát: TaskAccepted · PlanDecomposed · NodeDelegated · AcceptanceJudged · TaskFinished · TaskBlocked.
Does NOT own      : ✗ chạy tool/LLM thật (Execution-Core, qua execute_tool) · ✗ session state/StateStore (Execution-Core)
                    · ✗ sổ event + redaction (Control-Plane) · ✗ sandbox/policy (Tools-Safety). O KHÔNG gọi tool trực tiếp.
Public API (seam) : OpenAPI-style — hai cửa DUY NHẤT vào module:
                    · run_task_loop(TaskEnvelope{task_id,user_request,context?}) → Outcome{status∈FINISHED|BLOCKED|FAILED, run_id, evidence_ids}
                    · DelegationManager.delegate(DelegationRequest{parent_session_id, agent_id, objective,
                        scope_of_work, allowed_capabilities, max_steps, depth}) → DelegationResult{outcome∈success|rejected|failed, artifacts, summary, error?}
                    (resume: run_task_loop nhận cùng run_id → resume từ SQLite, 0 side-effect re-run)
Domain events     : phát 6 event GĐ5 §5.4 (trên); nghe — command từ Control-Plane (apply_pending_commands: roster/permission).
Permission model  : giao task = builder (Creator) · delegate = chỉ Orchestration nội bộ (O đặt scope, Broker KHÔNG mở);
                    scope con ⊆ cha enforce 2 tầng (delegation policy + SessionFactory ở Exec-Core). verdict: CHỈ gate ghi.
Error codes       : PLAN_DECOMPOSE_NOT_SHRINKING (μ không co ngặt) · PLAN_RENAME_DETECTED (Jaccard>0.80) ·
                    DELEGATION_SCOPE_EXCEEDS_PARENT · DELEGATION_DEPTH_EXCEEDED · ACCEPTANCE_EVIDENCE_MISSING ·
                    ACCEPTANCE_SCAFFOLDING_REJECTED · LOOP_MAX_ROUNDS · LOOP_NO_PROGRESS · LOOP_REPEAT_DECISION · PARSE_BUDGET_EXHAUSTED.
SLA/SLO           : Biên (không NFR-số production, bám NFR GĐ5): per-delegation max_steps=100, max_depth=8; decompose MAX_DEPTH=6, K=3/K_LEAF=5;
                    MỌI task về terminal ≤ max_rounds (M2 bounded). FINISHED bất khả khi thiếu evidence thật (M1 zero false-finish).
                    (P95 latency loop chưa có số → OQ-1 → Operate, KHÔNG bịa.)
Test contract     : · Control-Plane dựa trên 6 event GĐ5 (contract test Orch↔Observability: mỗi bước loop phát đúng event).
                    · Execution-Core: mọi delegate → child action VẪN qua execute_tool (audit test: 0 call site bỏ qua chokepoint).
                    · property-test bất biến: ∀ decomposition accepted → μ co ngặt; ∀ child-cap ⊄ parent → REJECTED (Hypothesis).
```

---

### CONTRACT — EXECUTION-CORE           Owner: Team Platform   [LÕI hạ tầng · CHOKEPOINT DUY NHẤT]

```text
[Lãnh đạo]        : Là MỘT CỬA mà mọi hành động (gọi LLM, chạy tool) của cả hệ phải chui qua — nơi kiểm-quyền,
                    ghi audit, đếm ngân sách xảy ra "một lần cho tất cả". Cũng giữ trí nhớ mỗi lần chạy (session).
                    Hành động lọt-cửa / rò-state giữa hai lần chạy → hỏi Team Platform.
Responsibilities  : execute_tool chokepoint (build ToolRequest → tool.requested → scope-check →
                    middleware Timing→Policy→Budget→Retry→Condense→core → tool.completed|failed → CapabilityResult) ·
                    Session/SessionIdentity/SessionFactory (constructor DUY NHẤT, child scope⊆parent) · registry · envelope · LLM adapter.
Owns (data/event) : Session state / StateStore (per-run, deep-copy isolation — state CHỈ ở đây, nhân KHÔNG giữ state) ·
                    SessionIdentity lineage 7-field · registry (frozen sau bootstrap) · envelope schema (ToolRequest/CapabilityResult).
                    Phát: tool.requested · tool.completed · tool.failed (bộ 3 chuẩn — reconcile OQ-3 đã đóng ở GĐ6).
Does NOT own      : ✗ quyết KHI NÀO gọi tool/delegate (Orchestration) · ✗ nội dung/chính sách tool (Tools-Safety) ·
                    ✗ sổ event bền vững + redaction (Control-Plane; Exec-Core chỉ PHÁT, không lưu) · ✗ verdict nghiệm-thu (Orchestration).
Public API (seam) : execute_tool(ToolRequest{capability, args, ctx:ToolCallContext{session_id,run_id,task_id,agent_id,
                        delegation_id?,depth, allowed_capabilities}}) → CapabilityResult{ok, capability, feature, data?, error?, metadata}
                    · SessionFactory.create(identity, allowed_capabilities) / .restore(**kw-only) → KernelSession
                    (CHOKEPOINT: capability ∉ allowed_capabilities → fail-closed, KHÔNG chạy. Exception không bao giờ escape.)
Domain events     : phát tool.* (trên); nghe — không (nhân stateless-cross-run).
Permission model  : authz LÕI enforce TẠI execute_tool: tool ∈ allowed_capabilities(session) mới chạy (frozenset per-session).
                    Delegation scope-shrink: SessionFactory ép child cap ⊆ parent (không tạo child rộng hơn cha được).
Error codes       : CAPABILITY_NOT_IN_SCOPE (fail-closed) · CAPABILITY_UNKNOWN (không trong registry) ·
                    KERNEL_FROZEN_MUTATION (đổi registry/middleware sau freeze) · SESSION_SCOPE_WIDENING_FORBIDDEN.
SLA/SLO           : freeze kernel TRƯỚC run đầu (I2/I3) → 0 rò state giữa run. Mọi action traced + scope-checked + envelope chuẩn.
                    LLM retry: transient-vs-permanent phân loại ở middleware Retry; permanent → parse-budget/guard (Orchestration) cắt.
Test contract     : · audit test cho MỌI module: KHÔNG call site nào gọi tool/LLM ngoài execute_tool (chokepoint DUY NHẤT).
                    · property-test: ∀ child session → allowed_capabilities ⊆ parent (scope-shrink fail-closed).
                    · isolation test: hai run song song → 0 chia sẻ StateStore.
```

---

### CONTRACT — TOOLS-SAFETY             Owner: Team Safety   [biên an toàn]

```text
[Lãnh đạo]        : Nhà tù cho công cụ — mọi thao tác file/terminal chỉ đụng được thư mục cho phép, có danh sách
                    chặn cứng "fail-closed" (nghi ngờ thì CẤM). Tool thoát jail / chạy lệnh cấm → hỏi Team Safety.
Responsibilities  : sandbox workspace jail (mọi path relative_to var/workspace/) · PolicyGate fail-closed (deny-list) ·
                    SafeToolPort per-tool policy · tool set (fs_read/fs_write/fs_list sandbox; terminal_run argv-only).
Owns (data/event) : chính sách sandbox + deny-list · workspace jail config · từng tool implementation + policy của nó.
Does NOT own      : ✗ AI ĐƯỢC gọi tool (scope/allowed_capabilities là của Execution-Core) — Tools-Safety chặn HÀNH VI
                    (thoát jail/lệnh cấm), Execution-Core chặn QUYỀN (scope). Hai biên khác nhau. · ✗ phát/lưu event (Control-Plane).
Public API (seam) : SafeToolPort.execute(ToolRequest) → CapabilityResult   (CHỈ Execution-Core gọi vào, qua port — không ai gọi thẳng)
                    (deny → CapabilityResult.error, KHÔNG throw; escape jail → chặn TRƯỚC khi chạy)
Domain events     : không phát (Execution-Core phát tool.* thay); nghe — không.
Permission model  : fail-closed: path ∉ workspace jail → chặn; tool ∈ deny-list → chặn; terminal chỉ argv (không shell string).
Error codes       : SANDBOX_PATH_ESCAPE (path ngoài jail) · POLICY_DENIED (deny-list) · TERMINAL_SHELL_STRING_FORBIDDEN (chỉ argv).
SLA/SLO           : PolicyGate fail-closed (mặc định CẤM khi không chắc). ⚠️ ràng buộc từ ADR-006: redact raw args
                    TRƯỚC khi bật write-tool (known gap: tool.requested từng log raw args) — điều phối với Control-Plane.
Test contract     : · sandbox-escape test (path traversal → SANDBOX_PATH_ESCAPE) · policy-matrix test (deny-list fail-closed).
                    · contract với Execution-Core: SafeToolPort trả CapabilityResult chuẩn (không throw), luôn qua execute_tool.
```

---

### CONTRACT — CONTROL-PLANE / OBSERVABILITY   Owner: Team Observability   [audit + integration boundary]

```text
[Lãnh đạo]        : Cuốn sổ bất biến ghi lại MỌI việc hệ làm (để audit + phát lại sau sự cố), che secret trước khi
                    lộ ra ngoài, và kênh nhận lệnh điều khiển. Secret rò ra UI/log / audit lệch → hỏi Team Observability.
Responsibilities  : EventEmitter (gate→seq→redact→fan-out) · RuntimeEvent envelope · seq monotonic gap-free per-run ·
                    TaskLoopSnapshot read-model (fold event) · RuntimeCommand + queue + ack · Redactor (SECRET_KEYS mask) ·
                    EventLogger (jsonl+summary+metrics) · EventReplayBuffer. (E21: transport/UI = sau MVP.)
Owns (data/event) : RuntimeEvent stream + seq (per-run monotonic) · RuntimeCommand queue + idempotency_key + ack ·
                    ui_payload đã redact · event log store (append-only jsonl + summary + metrics) · RuntimeCheckpoint (approval gate).
Does NOT own      : ✗ business logic loop (chỉ TIÊU THỤ event, UI ⟂ core — KHÔNG gọi ngược vào Orchestration) ·
                    ✗ phát ra hành động thật · ✗ authz THẬT (issued_by chỉ ATTRIBUTION; authz = requires_permission+checkpoint).
Public API (seam) : · EventEmitter.emit(RuntimeEvent) → void (validate→seq→redact→fan-out; raw không bao giờ rời emitter)
                    · build_snapshot(events[]) → TaskLoopSnapshot  (linear fold, deterministic theo seq; terminal-status guarded)
                    · CommandQueue.submit(RuntimeCommand{type, idempotency_key, apply_at∈immediate|immediate_if_waiting|next_checkpoint}) → CommandAck
                    · GET /api/stream (SSE, ?since=seq resync) · GET /api/snapshot · POST /api/commands   [sau MVP]
Domain events     : nghe TẤT CẢ (tool.*/loop.*/delegation.*/session.* — catalog config-driven closed allowlist, OQ-2 đóng GĐ6);
                    phát — command.*/ack. loop.* được fold vào snapshot; agent.* advisory (KHÔNG fold).
Permission model  : authz THẬT = requires_permission + checkpoint gate (KHÔNG suy từ issued_by — attribution ≠ authz, DEC-8).
                    UpdateAgentPermission LUÔN human-gated. Redaction level ∈ {public,ui_safe,internal,secret,restricted}.
Error codes       : EVENT_SEQ_GAP (seq không liên tục) · REDACTION_LEAK_DETECTED · COMMAND_IDEMPOTENCY_REPLAY (key trùng) ·
                    SNAPSHOT_TERMINAL_OVERWRITE (ghi đè terminal status — cấm).
SLA/SLO           : 0 secret trong ui_payload (redact TẠI biên trước fan-out) · seq monotonic gap-free per-run ·
                    replay(events[0..n]) = Snapshot(n) deterministic · emit KHÔNG chặn loop (fan-out sau seq).
                    (Ngưỡng alert/error-rate production chưa có số → OQ-1 → Operate, KHÔNG bịa.)
Test contract     : · replay-determinism test: build_snapshot(events) tái lập cùng snapshot theo seq · 0-secret test (SECRET_KEYS mask) ·
                    · command idempotency test (key trùng → 1 lần apply) · contract với Orchestration: 6 event GĐ5 có schema đúng.
```

---

### CONTRACT — DISCIPLINE               Owner: Team Platform   [thư viện thuần — contract GỌN có lý do]

```text
[Lãnh đạo]        : Bộ luật thuần dùng chung: kiểm định-dạng JSON đầu ra, chặn "báo xong khi code đổi mà chưa validate",
                    đếm ngân sách, nén ngữ cảnh khi quá dài. Không giữ dữ liệu sống — chỉ là hàm. Luật sai → hỏi Team Platform.
Responsibilities  : json_gate (parse strict + repair) · finish_gate (chặn finish nếu code_changed ∧ !validation_passed) ·
                    budget (max_steps/max_parse_errors CONSECUTIVE/max_same_tool_calls) · condense (nén context khi vượt ngưỡng).
Owns (data/event) : KHÔNG sở hữu dữ liệu sống nào (stateless pure functions) · sở hữu ĐỊNH NGHĨA luật + hằng số budget (knob).
Does NOT own      : ✗ dữ liệu loop/session (Orchestration/Execution-Core truyền vào, Discipline chỉ tính rồi trả) ·
                    ✗ phát event · ✗ quyết định terminal (trả tín hiệu, Orchestration quyết).
Public API (seam) : · json_gate.parse(raw) → ParseResult{ok, value?, repaired?, error?}
                    · finish_gate.check(code_changed, validation_passed, finish_reason?) → FinishVerdict{allow, reason?}
                    · budget.step(state) → BudgetVerdict{within, remaining, tripped?} · condense.run(context, threshold) → context'
Domain events     : không phát / không nghe (pure lib).
Permission model  : không có (không giữ tài nguyên; caller giữ quyền).
Error codes       : JSON_PARSE_UNREPAIRABLE · FINISH_BLOCKED_VALIDATION_MISSING · BUDGET_EXHAUSTED (trả tín hiệu, không throw).
SLA/SLO           : GỌN vì: stateless, một team ít đổi, không đối ngoại, không critical-path riêng (được module khác GỌI, không tự chạy).
                    Không SLA vận hành riêng — kế thừa SLA của module gọi nó. (Đủ-là-đủ: rút gọn độ sâu, KHÔNG bỏ ô.)
Test contract     : · property-test: parse(repair(x)) ổn định; budget.step đơn điệu giảm remaining; finish_gate chặn đúng ma trận
                    (code_changed×validation_passed). Dùng bởi Orchestration + Execution-Core → contract test 2 chiều.
```

---

### CONTRACT — KNOWLEDGE (optional)     Owner: Team Platform   [ngoài lõi MVP — contract GỌN có lý do]

```text
[Lãnh đạo]        : Tra cứu tri thức (RAG) tùy chọn để làm giàu ngữ cảnh. Nguyên tắc sống-còn: hỏng thì IM LẶNG trả rỗng,
                    TUYỆT ĐỐI không làm sập vòng lặp lõi. RAG treo/làm chậm loop → hỏi Team Platform.
Responsibilities  : RAG query health-gated · ingest/index tài liệu (lazy) · offline-first fallback (never raises).
Owns (data/event) : vector KB store + index (uuid5 ids) · health-gate state.
Does NOT own      : ✗ nằm trên critical path tới FINISHED (loop chạy được KHÔNG cần RAG) · ✗ phát/lưu event lõi.
Public API (seam) : RagPort.query(q, k?) → SearchResult[]  (KB down/health-gate off → trả [] rỗng, KHÔNG throw)
                    · RagPort.ingest(docs) → IngestAck   [tùy chọn]
Domain events     : không phát event lõi (ngoài loop); nghe — không.
Permission model  : không đặc biệt (được worker gọi tùy chọn trong scope của session).
Error codes       : (không lộ lỗi ra loop — mọi lỗi → trả rỗng + health-gate off; log nội bộ).
SLA/SLO           : GỌN vì: optional, ngoài lõi MVP, được-phép-hỏng. SLO DUY NHẤT: never raises (KB down ⇒ loop vẫn chạy, trả rỗng).
Test contract     : · test "Qdrant down → query trả [] không throw, loop không đổi hành vi" (skip nếu KB không sẵn — offline-first).
```

---

## 3. Tự soi trước khi chốt

- **Lãnh đạo đọc được đoạn đầu?** — CÓ. Bảng *module × owner × sở hữu/không-sở-hữu* + "hai cửa công khai" mở đầu, ngôn ngữ nghiệp vụ, không đâm thẳng vào OpenAPI. Mỗi contract mở bằng dòng [Lãnh đạo] "giữ phần nghiệp vụ nào / hỏng thì hỏi ai".
- **Dev đủ hành động?** — CÓ. Mỗi contract có Public API (seam) + event + data ownership + "Does NOT own" + permission/error (module lõi) → team code trong ranh giới không phải hỏi lại.
- **Đúng + đủ?** — CÓ. Module Map + 6 Contract; mọi contract đủ Owner+Responsibilities+Owns+DoesNOTown+PublicAPI; module lõi thêm event/permission/error/SLA/test; module rìa (Discipline/Knowledge) rút gọn KÈM lý do. Epic E01–E21 map hết vào đúng một module.
- **Chia theo domain, không màn hình?** — CÓ. 6 module = 6 bounded context GĐ5, ánh xạ 1–1 (đã chốt GĐ6). Không module nào theo cụm màn hình; không module hai owner (module ≠ team: Platform ôm 3 module gần nhau, nhưng mỗi module vẫn đúng 1 owner).
- **Bám nguồn?** — CÓ. Ranh giới bám Domain GĐ5 §5.1/§5.5 + kiến trúc GĐ6 §1; data ownership khớp GĐ5 §5.5 (không data/event hai module cùng sở hữu); event = 6 event GĐ5 §5.4 + tool.* Exec-Core. Feature dùng epic (⚠️ đã cảnh báo — chưa có backlog GĐ9 qua cổng).

**Open-Q mang sang sau (không bịa):**
- **OQ-M1** — nếu Skills (E07) phình thành catalog động có state → tách khỏi Discipline thành module riêng (hiện gộp vì thuần/rìa). → xét lại ở vòng modules/backlog sau.
- **OQ-1** (kế thừa) — baseline P95 loop + error-rate + false-finish thực chưa có số → SLA/SLO chỉ có biên cứng, chưa có ngưỡng alert → Operate (GĐ14).

---

## 4. Cổng GĐ10 — MODULES (tự-quyết, đóng vai Kiến trúc sư + Eng-manager trình bằng chứng · CTO mở cổng)

**Câu hỏi cổng (doc GĐ10):** *"Ownership & contract đã rõ để các team chạy delivery SONG SONG chưa?"*

**Chủ sở hữu (Kiến trúc sư + Eng-manager) TRÌNH BẰNG CHỨNG:**
1. **Mỗi module đúng một owner** — 6 module, mỗi cái 1 team (Orchestration/Platform×3/Safety/Observability); module ≠ team, không module hai owner. ✔
2. **Không data/event bị hai module cùng sở hữu** — plan tree+acceptance+evidence+SQLite → CHỈ Orchestration; session state → CHỈ Execution-Core; event stream+redaction+command → CHỈ Control-Plane; sandbox/policy → CHỈ Tools-Safety (khớp GĐ5 §5.5). ✔
3. **Không feature mồ côi / hai chủ** — epic E01–E21 map hết vào đúng một module (bảng §1). ✔ (⚠️ dùng epic thay story — chưa có backlog GĐ9 qua cổng.)
4. **Mọi phụ thuộc đi qua contract/seam** — hai cửa công khai DUY NHẤT (Execution-Core: execute_tool; Orchestration: run_task_loop + DelegationManager.delegate); cấm cross-module bypass; tool tự gọi thẳng = vi phạm. ✔

```
═══ CỔNG GĐ10 — MODULES: HexAgent (clean rebuild) ═══
6 module = 6 bounded context GĐ5 (1–1) · mỗi module 1 owner · does-NOT-own rõ · data ownership sạch (không chồng).
Chokepoint seam: Execution-Core expose execute_tool (cửa DUY NHẤT mọi hành động) ·
                 Orchestration expose run_task_loop + DelegationManager.delegate (delegate = cửa RIÊNG, scope⊆parent).
                 Cấm cross-module bypass (tool gọi thẳng không qua execute_tool = vi phạm).
Contract: 6 bản · module lõi (Orch/Exec-Core/Control-Plane/Tools-Safety) đầy đủ event/permission/error/SLA/test ·
          module rìa (Discipline/Knowledge) gọn kèm lý do.
Feature: epic E01–E21 map hết vào đúng một module (⚠️ dùng epic — backlog GĐ9 chưa qua cổng project này).
Open-Q: OQ-M1 (Skills phình → tách khỏi Discipline) · OQ-1 (ngưỡng SLA-số → Operate).
Câu hỏi cổng: Ownership & contract đủ rõ để các team chạy delivery SONG SONG chưa?
════════════════
```

**Quyết định cổng (tự-quyết — product owner: "không hỏi approval", đóng vai CTO/Người duyệt).**
**GATE: GO.** Lý do: mỗi module đúng một owner + ranh giới does-NOT-own rõ + data ownership không chồng (khớp GĐ5 §5.5) + mọi phụ thuộc đi qua đúng hai cửa công khai (execute_tool · run_task_loop/delegate) → 6 team code song song không giẫm nhau. Bám nguồn: 6 module = 6 context GĐ5 đã-qua-cổng + kiến trúc GĐ6 đã-qua-cổng.
**Phương án đã loại ở tầng cổng:** (a) *chặn GO tới khi có backlog GĐ9 qua cổng* — loại: ranh giới module bám *domain* (GĐ5, đã qua cổng), không bám story; thiếu backlog chỉ ảnh hưởng phần "map feature" (đã cảnh báo ⚠️ + dùng epic), không lung lay ranh giới sở hữu. Ghi cảnh báo minh bạch thay vì chặn. (b) *tách Delegation + Skills thành module riêng cho "sạch"* — loại: cả hai chia đôi data-ownership/đẻ module rìa không thêm ranh giới thật (xem lý do §1).

---

## 5. Bàn giao sang `delivery` (GĐ11)

```
═══ BÀN GIAO — hex-agent-rebuild · GĐ10 xong ═══
Đã chốt   : 6 module · mỗi module 1 owner + contract · does-NOT-own rõ · data ownership sạch (không chồng) ·
            2 seam công khai DUY NHẤT (execute_tool · run_task_loop+delegate), cấm cross-module bypass.
Artifact  : rebuild-hex-agent/pipeline/10-modules.md
Theo dõi  : · chokepoint discipline (audit-test: 0 call site bỏ qua execute_tool) — rủi ro cao nhất khi nhiều team code song song
            · ADR-006: redact raw args TRƯỚC khi Tools-Safety bật write-tool (điều phối Safety↔Observability)
            · SPIKE-1 (resume 0 side-effect) còn treo từ GĐ8 — dính vào slice đầu của Orchestration
            · OQ-M1 (Skills tách khỏi Discipline nếu phình) · OQ-1 (SLA-số → Operate)
→ Nhiều team bắt đầu code song song, cần chuẩn giao hàng + DoD: chạy /delivery (GĐ11) — mỗi slice đóng khung bằng /frame
→ Chỉ build ngay MỘT slice trong một module: chạy /frame
→ Muốn kiểm chéo story→module (backlog chưa qua cổng): chạy /backlog (GĐ9) trước rồi quay lại
→ Ranh giới đụng code cũ, cần hiểu trước khi module đụng vào: chạy /atlas hoặc /explain
════════════════
```

*Traceability:* GĐ10 nhận Domain GĐ5 (6 bounded context + data ownership §5.5 + 6 domain event §5.4 + 5 rule bất biến) + kiến trúc GĐ6 (6 module 1–1 + 2 chokepoint + 6 ADR) + roadmap epic (REBUILD-BRIEF §Roadmap / evidence-C E01–E21, ⚠️ chưa có backlog GĐ9 qua cổng) → sinh Module Map + 6 Module Contract → bàn giao `delivery` (GĐ11). Ownership sạch (mỗi data/event một chủ, khớp §5.5); mọi phụ thuộc đi qua contract/seam. OQ-M1 mới; OQ-1 chuyển tiếp Operate.
