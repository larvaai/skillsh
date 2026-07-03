# 06 — Shape: Solution Architecture — HexAgent (clean rebuild)

> Skill `shape` · Giai đoạn 6 (Solution Architecture). Vào bằng Domain Model GĐ5 (`pipeline/05-idea-domain.md`), ra bằng Architecture Brief + C4 (Context & Container) + Data Flow + Integration Model + Security Model + ADRs. Chốt HÌNH HÀI hệ thống — **chưa** chốt framework (đó là `stack` GĐ7).
> Anchor: `00-understanding/REBUILD-BRIEF.md` + `evidence-A/B/C` + `ATLAS.md`. Bám 6 bounded context + 5 rule bất biến + 6 domain event + data ownership của GĐ5. Không đẻ context mới, không bịa NFR.
> Chế độ tự-quyết: mọi cổng do người viết đóng vai **Kiến trúc sư / CTO (Security review song song)** tự quyết GO, ghi rõ lý do + phương án đã loại. Không hỏi user.

---

## Góc nhìn lãnh đạo (đọc 60 giây, không cần biết code)

**Hệ thống có hình gì.** Một **khối triển khai đơn (modular monolith) kiểu hexagonal** — một nhân (kernel) *đông cứng* trước khi chạy, bao quanh là 6 module ranh giới rõ, mỗi module đúng một bounded context của GĐ5. Toàn bộ **state chỉ sống trong session**, nhân không giữ state → hai lần chạy khác nhau không rò dữ liệu cho nhau. Mọi hành động của agent đi qua đúng **một cửa** (`execute_tool`); việc giao-việc-cho-sub-agent đi qua **một cửa riêng thứ hai** (delegation). Hai cửa đó là nơi ta gắn kiểm-quyền, audit và giới hạn ngân sách một lần cho tất cả.

**Vì sao hình này hợp rủi ro & quy mô.** Sản phẩm là một agent tự trị — rủi ro lớn nhất *không* phải scale hạ tầng, mà là **hai bệnh chết người**: (1) báo-xong-khống và (2) chạy-vô-hạn / leo-thang-quyền. Modular monolith một tiến trình là đủ cho quy mô hiện tại (một agent điều phối các sub-agent trong cùng process), và nó cho ta đóng cả hai bệnh bằng *kiến trúc* chứ không bằng lời hứa: finish chỉ xảy ra ở một cổng nghiệm-thu-bằng-bằng-chứng, và runaway bị chặn bởi một tầng guard + budget cứng. Tách microservices lúc này chỉ thêm chi phí vận hành mà không đổi được bản chất rủi ro (xem ADR-001).

**Ba điều CTO nhìn để biết on-track.** (1) Nhân đã *freeze* trước run đầu và state *chỉ* ở session → 0 rò state. (2) Có đúng *hai* chokepoint (tool + delegation), không có đường vòng nào bỏ qua audit/scope-check. (3) `FINISHED` *bất khả* khi thiếu evidence thật, và mọi task luôn về terminal trong biên (không treo). Nếu ba điều này giữ, phần còn lại (tools, control-plane UI, RAG) chỉ là mở rộng an toàn quanh lõi.

---

## 1. Architecture Brief — bảng quyết định

> Đây là bảng đọc-được cho lãnh đạo: mỗi dòng là một quyết định nghiệp vụ, không cần đọc code. Chi tiết cho dev nằm ở C4 + ADR bên dưới.

```text
ARCHITECTURE BRIEF — HexAgent (clean rebuild)

Architecture style : Hexagonal modular monolith, một tiến trình, nhân microkernel ĐÔNG CỨNG + session sống.
                     Lý do: 1 agent điều phối sub-agent trong-process; rủi ro là an-toàn-loop, không phải scale hạ tầng.
                     (ADR-001; loại: shared mutable core, microservices)

Module boundary    : 6 module = 6 bounded context GĐ5, ánh xạ 1–1:
                     • Orchestration    — vòng lặp task (plan/decompose, order, delegate-điều-phối, acceptance/finish, guards)
                     • Execution-Core   — kernel chokepoint execute_tool, Session/SessionIdentity, registry, envelope
                     • Discipline        — logic thuần chia sẻ: json_gate, finish_gate, budget, condense
                     • Tools-Safety     — sandbox (workspace jail), PolicyGate fail-closed, SafeToolPort per-tool
                     • Control-Plane/Observability — EventEmitter (gate→seq→redact→fan-out), RuntimeEvent, Snapshot read-model, RuntimeCommand, Redactor
                     • Knowledge (opt)  — RAG health-gated, offline-first (NGOÀI lõi MVP)
                     Ranh giới qua PORT (protocol), không cross-module import trực tiếp. (ADR-001)

Data ownership     : State CHỈ ở Session (Execution-Core sở hữu StateStore, deep-copy isolation) — nhân KHÔNG giữ state.
                     Cây kế hoạch + AcceptanceCheck-verdict + Evidence(Blackboard) → Orchestration.
                     Event stream + seq + Command queue + Redaction → Control-Plane.
                     SQLite (langgraph.sqlite) = chân lý resume → Orchestration/graph; checkpoint.json = projection UI (KHÔNG đọc để resume).
                     Cấm cross-module đọc/ghi trực tiếp state của module khác — đi qua port. (ADR-005; GĐ5 §5.5)

Integration        : • Người↔hệ thống: đồng bộ, request/response qua một facade (nhận TaskEnvelope, trả outcome).
                     • Nội bộ giữa module: domain event + port call trong-process (KHÔNG mạng).
                     • Ra LLM provider: đồng bộ, LLM-as-capability đi QUA execute_tool (không phải call trực tiếp).
                     • Ra Tool sandbox: đồng bộ, qua execute_tool + SafeToolPort.
                     • Ra Vector KB (RAG): bất đồng bộ-tùy-chọn, health-gated, offline-first (never raises).
                     • BE↔UI (control plane, sau MVP): 3 seam đóng — event stream (push) · snapshot (pull) · command (push).
                     (Integration Model §5)

Auth               : Authz theo scope/allowed_capabilities per-session (frozenset), enforce TẠI execute_tool.
                     Delegation: scope con ⊆ cha (SessionFactory + delegation policy). O đặt allowed_capabilities; Broker nắn context, KHÔNG mở scope.
                     Control command: requires_permission + checkpoint gate là authz THẬT; issued_by chỉ để quy trách (attribution ≠ authz).
                     (ADR-002, ADR-003, ADR-006)

Security           : Phân loại dữ liệu (Public/Internal/Confidential/Secret); redact-tại-biên trước fan-out (Redactor, SECRET_KEYS mask);
                     audit = event log append-only (nguồn replay). Threat model STRIDE cho luồng DELEGATE + luồng redaction (§4).
                     (ADR-003, ADR-006)

Reliability        : Budget cứng (loop/delegation/decompose) + tầng guard (max_rounds, no-progress, repeat-decision, parse-budget, MAX_DEPTH, per-root step)
                     + finish-gate (chặn finish nếu code_changed ∧ !validation_passed). LLM/tool retry: transient-vs-permanent phân loại.
                     "Chỉ xong khi đủ evidence" ⟂ "cắt cứng khi hết biên" — hai chốt đối nhau. (ADR-004)

Performance        : Loop tuần tự theo round (không cần realtime throughput). Đòn bẩy: (a) session state deep-copy chỉ khi delegate;
                     (b) condense context khi vượt ngưỡng (Discipline); (c) event emit không chặn loop (fan-out sau seq). Chưa có NFR P95 số → open-Q (không bịa).

Observability      : Event-log-first (glass-box). Mọi capability call phát tool.requested/completed|failed → jsonl + summary + metrics
                     (tool_calls/llm_calls/failures/blocks/parse_errors). seq monotonic gap-free per-run; replay(events[0..n])=Snapshot(n) deterministic.
                     Alert: chưa có ngưỡng số production → open-Q OQ-1 (→ Operate), KHÔNG bịa ngưỡng.

Deployment         : Single deployable (một tiến trình), một môi trường chạy; artifact resume = SQLite file per-run.
                     Cloud/on-prem đều chạy (không phụ thuộc dịch vụ managed nào cho lõi). Chốt hạ tầng cụ thể = việc GĐ7 `stack`.

Compliance         : KHÔNG áp dụng PDPA/GDPR ở MVP — đây là platform nội bộ cho đội builder, dữ liệu task là của chính đội dùng, không phải PII người tiêu dùng.
                     (1 dòng lý do; nếu sau này chạy trên dữ liệu KH → mở lại ở Security Model. Không bịa ràng buộc chưa ai đòi.)
```

**Ánh xạ boundary → bounded context GĐ5 (bám nguồn, không tự vẽ):** mỗi module ở trên nối 1–1 về một context trong `05-idea-domain.md §5.1`. Không có module nào không trace về được; không đẻ context mới.

---

## 2. C4 Context — HexAgent ngồi ở đâu trong thế giới

> Góc nhìn lãnh đạo: hệ thống là một hộp; xung quanh là ai giao việc và những hệ ngoài nào nó dựa vào. Đây là bức tranh quản-rủi-ro-tích-hợp, không cần hiểu kỹ thuật.

```text
        ┌─────────────────┐
        │  Người giao task │  (human builder — giao 1 Task/Goal qua envelope)
        └────────┬────────┘
                 │ giao TaskEnvelope (đồng bộ)  ▲ nhận outcome + xem event log
                 ▼                              │
        ╔═══════════════════════════════════════════════╗
        ║             HexAgent (hộp hệ thống)           ║
        ║  agent tự-điều-phối: plan → order → delegate  ║
        ║  → judge-by-evidence → finish CÓ BIÊN         ║
        ╚═══╤═════════════╤══════════════╤══════════════╝
            │             │              │
   gọi LLM  │   chạy tool │   truy vấn   │  (RAG, tùy chọn)
   (đồng bộ,│   (đồng bộ, │   tri thức   │  health-gated,
   qua      │   sandbox)  │              │  offline-first
   execute_ │             │              │
   tool)    ▼             ▼              ▼
      ┌──────────┐  ┌──────────────┐  ┌──────────────┐
      │   LLM     │  │ Tool sandbox │  │  Vector KB    │
      │ provider  │  │ (fs/terminal │  │  (RAG store)  │
      │ (JSON-mode│  │  jail'd)     │  │               │
      │  capability)│ └──────────────┘  └──────────────┘
      └──────────┘
```

**Diễn giải (phẳng):** Người giao task đưa **một** mục tiêu vào hộp và sau đó chỉ *quan sát* (event log) — không điều khiển từng bước ở MVP. Hộp dựa vào **ba** hệ ngoài: một **LLM provider** để suy luận (nhưng LLM được gọi *như một capability đi qua execute_tool*, không phải đường tắt), một **Tool sandbox** để thao tác file/terminal trong jail, và một **Vector KB** tùy chọn cho tri thức. Rủi ro tích hợp lớn nhất là LLM provider (chi phí + độ trễ + lỗi transient) — đó là lý do budget/guard và retry-classify nằm ngay trên đường này.

---

## 3. C4 Container — bên trong hộp có những khối gì

> Công nghệ nêu ở mức **LOẠI** (in-process module, embedded DB, vector store…), KHÔNG tên framework — chốt framework là việc GĐ7 `stack`.

```text
╔══════════════════════════ HexAgent (một tiến trình) ══════════════════════════╗
║                                                                                ║
║  [Facade / Entry]  nhận TaskEnvelope, trả outcome, đọc event log               ║
║        │ (in-process call)                                                      ║
║        ▼                                                                        ║
║  ┌──────────────────────┐        domain events        ┌──────────────────────┐ ║
║  │  ORCHESTRATION        │───────(in-process bus)─────▶│ CONTROL-PLANE /       │ ║
║  │  vòng lặp task:        │                             │ OBSERVABILITY         │ ║
║  │  plan/decompose(+gate2)│◀─── snapshot read-model ────│ EventEmitter          │ ║
║  │  order(next_node)      │                             │ (gate→seq→redact→fan) │ ║
║  │  DELEGATION chokepoint │                             │ RuntimeEvent envelope │ ║
║  │  judge_acceptance      │                             │ Snapshot / Command    │ ║
║  │  guards + budget       │                             │ Redactor              │ ║
║  └───────┬───────┬───────┘                             └──────────┬───────────┘ ║
║          │       │ mọi hành động                                   │ ghi        ║
║          │       ▼ qua execute_tool                                ▼            ║
║          │  ┌──────────────────────┐                    ┌──────────────────┐   ║
║          │  │ EXECUTION-CORE        │                    │ Event log store   │   ║
║          │  │ AgentKernel (frozen)  │─── middleware ────▶│ (append jsonl +   │   ║
║          │  │ execute_tool CHOKEPT  │  Timing→Policy→    │  summary/metrics) │   ║
║          │  │ KernelSession (state) │  Budget→Retry→     └──────────────────┘   ║
║          │  │ SessionFactory        │  Condense→core                            ║
║          │  │ registry/envelope     │                                           ║
║          │  └───┬─────────┬─────────┘                                           ║
║   uses   │      │ uses    │ uses                                                ║
║  ┌───────▼──┐ ┌─▼───────┐ ┌▼──────────────┐   ┌──────────────┐                  ║
║  │DISCIPLINE│ │TOOLS-   │ │ (LLM adapter  │   │ KNOWLEDGE     │  (tùy chọn,     ║
║  │json_gate │ │SAFETY   │ │  = capability)│   │ RAG health-   │   ngoài lõi)    ║
║  │finish_gt │ │sandbox  │ └───────────────┘   │ gated         │                 ║
║  │budget    │ │jail +   │                     └──────────────┘                 ║
║  │condense  │ │PolicyGate│                                                      ║
║  └──────────┘ │fail-clsd│         ┌────────────────────────────┐                ║
║               └─────────┘         │ SQLite (embedded)          │                ║
║                                   │ = chân lý resume per-run    │                ║
║   Orchestration/graph ───────────▶│ (langgraph.sqlite)          │                ║
║                                   │ checkpoint.json = projection │                ║
║                                   └────────────────────────────┘                ║
╚════════════════════════════════════════════════════════════════════════════════╝

Giao thức giữa khối (mức loại, không framework):
- Orchestration ↔ Execution-Core : in-process call qua PORT (ToolPort/DelegationPort). KHÔNG mạng.
- Bất kỳ khối → Control-Plane      : phát domain event qua in-process event bus (một chiều, không chặn loop).
- Control-Plane → Orchestration    : snapshot read-model (pull) — fold event thành trạng thái đọc.
- Execution-Core → Event log store : append-only jsonl + summary/metrics.
- Orchestration/graph → SQLite     : ghi checkpoint atomic (commands+round+save một transaction).
- Execution-Core → LLM/Tool/RAG    : qua execute_tool + adapter/port (đồng bộ; RAG health-gated).
```

**Diễn giải (phẳng):** **Orchestration** cầm vòng lặp và hai chokepoint (execute_tool nằm ở Execution-Core; delegation nằm *trong* Orchestration nhưng là cửa RIÊNG). **Execution-Core** là nhân đông cứng: mọi tool/LLM call chui qua `execute_tool` và một chuỗi middleware cố định (Timing→Policy→Budget→Retry→Condense→core) — đó là chỗ scope-check, đếm budget, retry, và phát event xảy ra *một lần cho tất cả*. **Discipline** và **Tools-Safety** là thư viện logic thuần được Execution-Core dùng. **Control-Plane** chỉ *tiêu thụ* event để dựng read-model và nhận command — nó không chứa business logic (UI ⟂ core). **SQLite** là chân lý resume; `checkpoint.json` chỉ là ảnh chiếu cho UI.

---

## 4. Data Flow — một task xuyên các container (gắn domain event GĐ5)

> Kể bằng câu. Mỗi bước gắn đúng một domain event của GĐ5 §5.4 và bám data ownership GĐ5 §5.5.

1. **Accept.** Facade nhận `TaskEnvelope` (`task_id`, `user_request`) → tạo `Run`/`Session` qua SessionFactory (state khởi tạo *chỉ* trong session). → **event `TaskAccepted`**. *Chủ dữ liệu:* Execution-Core giữ session state; Orchestration mở vòng lặp.
2. **Plan / Decompose.** Orchestration cho worker đề xuất chia task thành cây (forest theo `parent` + DAG theo `depends_on`, cả hai acyclic). **Cổng-2 `accept_decomposition`** — thuần cấu trúc, chạy *TRƯỚC* khi đổi cây — kiểm chứng-minh-dừng μ(node)=len(done_when) co ngặt + coverage-by-implication + phát hiện RENAME/STUCK. Chỉ khi cổng-2 PASS mới mutate cây (thêm child + reduce node synthetic). → **event `PlanDecomposed`**. *Chủ dữ liệu:* Orchestration sở hữu Tree/Node/DoneWhen/edges.
3. **Order.** `next_node()` = node pending trái nhất mà mọi dependency đã done (topo theo depth,order) → "không leo sớm" miễn phí. (không phát event mới — là bước chọn nội bộ trong round.)
4. **Delegate.** Với node/assignment được chọn, Orchestration gọi **DELEGATION chokepoint** (cửa RIÊNG, không phải method của kernel): validate policy (depth≤max, **scope con ⊆ cha**, max_steps) → tạo child session (SessionFactory enforce scope-shrink) → child chạy vòng lặp con → child action lại đi qua `execute_tool` của kernel (phát `tool.requested/completed`) → merge artifact về parent → đóng child. → **event `NodeDelegated`** (`delegation.finished`). *Chủ dữ liệu:* O đặt `allowed_capabilities`; Broker nắn context, KHÔNG mở scope.
5. **Judge acceptance.** Sau mỗi round, O nộp `acceptance_status` [{id,status,evidence_ids}]. Cổng `judge_acceptance`: mỗi AC "passed" phải có ≥1 **evidence THẬT** (artifact/tool_result/reviewer_report/diff/test_result) resolve được trên Blackboard; scaffolding (session_plan/context_packet/ac_report) bị từ chối. Worker KHÔNG tự ghi verdict — gate là nơi DUY NHẤT gán outcome. → **event `AcceptanceJudged`**. *Chủ dữ liệu:* Orchestration (gate viết verdict).
6. **Finish HOẶC Blocked.**
   - `all_accepted()` = mọi AC `status=="passed" ∧ evidence_ids≠∅` → terminal **FINISHED**. → **event `TaskFinished`**. (finish-gate còn chặn nếu `code_changed ∧ !validation_passed`.)
   - Nếu chạm guard bất kỳ (max_rounds / no-progress: artifacts không tăng ∧ acceptance không đổi ∧ không command / repeat-decision: chữ ký lặp N× / parse-budget / MAX_DEPTH / per-root step) → terminal **BLOCKED**. → **event `TaskBlocked`**. Parse-budget cạn → FAILED.
7. **Checkpoint xuyên suốt.** Mỗi round: commands + round_no + save() land trong **một transaction atomic** vào SQLite → resume cùng `run_id` không side-effect re-run. Song song, mọi event ở các bước trên đi qua EventEmitter (gate→seq→redact→fan-out) → event log append-only + snapshot read-model.

**Bất biến data-flow (bám GĐ5 §5.3):** finish chỉ ở cổng-có-evidence (rule #1) · worker không ghi verdict (rule #2) · scope con ⊆ cha (rule #3) · plan có μ co ngặt (rule #4) · mọi hành động qua execute_tool (rule #5).

---

## 5. Integration Model — mỗi tích hợp một dòng

| Tích hợp | Pattern | Đồng bộ? | Ai chịu lỗi khi bên kia sập | Retry/Timeout/Fallback | Ai sở hữu contract |
|---|---|---|---|---|---|
| Người → HexAgent (giao task) | request/response qua Facade | Đồng bộ | Facade trả lỗi có cấu trúc | — (một lần giao) | Facade / TaskEnvelope schema |
| HexAgent → **LLM provider** | LLM-as-capability **qua execute_tool** | Đồng bộ | Execution-Core: middleware Retry phân loại transient-vs-permanent; budget đếm | Retry transient; timeout per-call; permanent → parse-budget/guard cắt | Execution-Core (adapter port) |
| HexAgent → **Tool sandbox** (fs/terminal) | qua execute_tool + SafeToolPort | Đồng bộ | Tools-Safety: PolicyGate fail-closed chặn trước; jail chặn escape | Timeout per-tool; deny → CapabilityResult.error (không throw) | Tools-Safety (SafeToolPort policy) |
| HexAgent → **Vector KB (RAG)** | health-gated query | Bất đồng bộ/tùy chọn | Knowledge: health-gate → nếu KB down thì **never raises**, trả rỗng | Offline-first fallback (bỏ qua RAG, loop vẫn chạy) | Knowledge (RAG port) |
| Nội bộ module ↔ module | domain event (in-process bus) + port call | Một chiều (event) / đồng bộ (port) | Emitter validate; port trả envelope chuẩn | — (in-process) | Bên phát event / port owner |
| BE ↔ UI (control plane — **sau MVP**) | 3 seam: event stream (push) · snapshot (pull) · command (push) | Push + pull | Replay buffer resync (needs_resync); command idempotency_key | Resync `?since=seq`; command idempotent theo key | Control-Plane (frozen contract) |

**Chốt open-Q integration còn treo từ GĐ5:**
- **OQ-2 (danh mục ~50 event / 16 command)** → **quyết ở đây:** catalog là **config-driven, closed set** — event types nạp từ một file cấu hình runtime (mức loại: config file enumerable), commands là tập đóng 16 loại với `apply_at ∈ {immediate, immediate_if_waiting, next_checkpoint}`. Không cần liệt kê từng dòng ở tầng shape; ràng buộc kiến trúc = "catalog phải là allowlist đóng, load từ config, không hard-code rải rác". Danh mục chi tiết là dữ liệu cấu hình, chốt vật lý ở `skeleton`/khi dựng registry.
- **OQ-3 (mismatch tên event: kernel phát `tool.requested/completed` vs registry khai `tool.call_requested/before_call/after_call`)** → **quyết ở đây:** chuẩn hoá về **một bộ tên do registry allowlist làm chân lý**; kernel emit phải khớp allowlist đó (reconcile về `tool.requested/completed/failed` — bộ 3 mà event-log/replay đang dùng). Đây là ràng buộc contract cho GĐ7/skeleton, không phải chọn framework.

---

## 6. Security Model

> Góc nhìn lãnh đạo (câu CTO/pháp lý hỏi đầu tiên): **Dữ liệu nhạy nhất** là *secret trong tham số tool/LLM* (key, token) và *nội dung task*. **Ai được xem gì** bị chặn bởi scope/allowed_capabilities tại đúng hai cửa (tool + delegation), scope con không bao giờ rộng hơn cha. **Có dấu vết audit không** — có: event log append-only, redact secret *trước* khi rời biên; và attribution (ai gây ra) tách khỏi authz (ai được phép).

### 6.1 Phân loại dữ liệu

| Lớp | Ví dụ | Xử lý |
|---|---|---|
| **Public** | tên tool, tên event type | tự do fan-out |
| **Internal** | plan tree, node status, acceptance verdict | trong hệ; vào snapshot read-model |
| **Confidential** | nội dung task/user_request, artifact | không rời hệ ngoài event log nội bộ; UI chỉ đọc `ui_payload` đã redact |
| **Secret** | key/token trong args tool/LLM | **mask trước fan-out** (Redactor, SECRET_KEYS → '[REDACTED]'); raw không bao giờ rời emitter |

### 6.2 Auth model (bám ADR-002/003/006)
- **Authz thi hành tại execute_tool:** tool ∉ `allowed_capabilities` của session → fail-closed (không chạy). Đây là cửa quyền lõi.
- **Delegation:** scope con **⊆** cha, enforce ở delegation chokepoint + SessionFactory. O đặt `allowed_capabilities`; Broker chỉ nắn context.
- **Control command (control-plane, sau MVP):** authz thật = `requires_permission` + checkpoint gate; `issued_by` chỉ để **quy trách** (attribution ≠ authz). `UpdateAgentPermission` luôn human-gated.

### 6.3 Audit
- Event log **append-only**, seq monotonic gap-free per-run → nguồn replay + audit bất biến.
- `replay(events[0..n]) = Snapshot(n)` deterministic → dựng lại trạng thái để soi sau sự cố.

### 6.4 Threat model STRIDE — luồng DELEGATE + luồng REDACTION (hai đường rủi ro nhất)

| Threat | Luồng delegate | Luồng redaction | Đối phó (đã có trong kiến trúc) |
|---|---|---|---|
| **S**poofing | Sub-agent giả danh cha để cấp scope? | — | SessionIdentity 7-field bất biến, chỉ SessionFactory tạo được child |
| **T**ampering | Worker sửa verdict để "tự nói xong"? | Sửa payload sau khi seq gán? | Rule #2 (worker cấm verdict keys; gate ghi) · event bất biến sau phát, seq gán ở emitter |
| **R**epudiation | Không biết ai gây delegation? | — | attribution `issued_by` + event log append-only truy được |
| **I**nfo disclosure | Child đọc dữ liệu ngoài scope cha? | **Secret rò vào ui_payload / jsonl?** | scope con ⊆ cha (fail-closed) · **redact-tại-biên trước fan-out**; ⚠️ known gap: `tool.requested` từng log raw args vào jsonl → phải redact TRƯỚC khi bật write-tools (ADR-006) |
| **D**oS | Delegation đệ quy vô hạn / đốt token? | Event storm? | depth≤max, per-delegation max_steps, MAX_DEPTH, per-root budget · seq/emit không chặn loop |
| **E**oP (leo quyền) | Child tự cấp cap vượt cha? | — | **scope con ⊆ cha** validate 2 tầng (policy + SessionFactory); Broker KHÔNG mở scope |

**Compliance:** không áp dụng PDPA/GDPR ở MVP (platform nội bộ, dữ liệu của chính đội dùng) — nếu chạy trên dữ liệu KH thì mở lại lớp Confidential + retention. Không bịa ràng buộc chưa ai đòi.

---

## 7. ADRs — mỗi quyết định lớn một bản ghi (đều có phương án đã loại)

```text
ADR-001 — Hexagonal frozen-kernel + mutable-session (modular monolith)
Bối cảnh   : 1 agent điều phối sub-agent trong cùng tiến trình; rủi ro là an-toàn-loop + rò-state, KHÔNG phải scale hạ tầng.
             Bất biến GĐ5: "nhân đông cứng, session sống" (I2/I3); ranh giới 6 bounded context.
Quyết định : Hexagonal modular monolith một tiến trình. Freeze kernel TRƯỚC run đầu (sau freeze không đổi registry/middleware,
             chỉ session state mutate). State CHỈ ở session. Module giao tiếp qua PORT (protocol), không cross-import.
Phương án đã loại :
  • Shared mutable core (nhân giữ state chung) — loại: state chia sẻ giữa run → rò dữ liệu giữa các task, không audit/isolate được (phá I2/I3).
  • Microservices ngay từ đầu — loại: thêm chi phí vận hành (network, deploy, phân tán tx) mà KHÔNG đổi bản chất rủi ro của agent tự trị;
    một agent + sub-agent in-process không cần biên mạng. (YAGNI; tách sau nếu có nhu cầu scale thật.)
Hệ quả     : + isolation mạnh, freeze bắt lỗi cấu hình sớm, dễ audit. − monolith phải kỷ luật ranh giới port để không thoái hoá thành big-ball-of-mud;
             − scale ngang bị giới hạn (chấp nhận: chưa phải bài toán hiện tại).

ADR-002 — Một chokepoint execute_tool (mọi hành động qua một cửa)
Bối cảnh   : Cần gắn observability + scope-check + envelope chuẩn + budget cho MỌI hành động (LLM/tool) mà không lặp code, không sót đường.
             Bất biến GĐ5 rule #5 + I1.
Quyết định : Đúng MỘT chokepoint `execute_tool` ở Execution-Core: build ToolRequest → publish tool.requested → scope-check →
             middleware chain (Timing→Policy→Budget→Retry→Condense→core) → publish tool.completed|failed → trả CapabilityResult.
             LLM cũng là capability đi qua cửa này.
Phương án đã loại :
  • Rải rác call sites (mỗi module tự gọi tool/LLM trực tiếp) — loại: mỗi call site phải tự nhớ scope-check + emit event + budget →
    chắc chắn sót một chỗ → lỗ audit + lỗ quyền. Một cửa = gắn cross-cutting concern ĐÚNG MỘT LẦN.
Hệ quả     : + mọi action traced/scope-checked/normalized; exception không escape. − một cửa thành điểm nóng: middleware chain phải giữ thứ tự đúng
             (outer→inner), thêm concern = thêm middleware, không thêm đường vòng.

ADR-003 — Delegation chokepoint RIÊNG (tách khỏi kernel)
Bối cảnh   : Giao-việc-cho-sub-agent có luật riêng (scope con ⊆ cha, depth, max_steps, merge artifact) khác với chạy một tool.
             Bất biến GĐ5 rule #3 (I13/I14).
Quyết định : Delegation là chokepoint RIÊNG (`DelegationManager.delegate`), KHÔNG phải method của kernel: validate policy →
             tạo child session (scope-shrink) → child chạy → merge → đóng child → emit delegation.finished. Broker nắn context, O đặt scope.
Phương án đã loại :
  • Để delegation là một method của kernel / một tool trong execute_tool — loại: trộn hai luật khác nhau (tool-scope vs delegation-policy)
    vào một cửa làm cửa đó phình + khó audit "ai cấp quyền cho ai"; tách cửa riêng giữ mỗi cửa một trách nhiệm, audit multi-agent rõ ràng.
Hệ quả     : + hai cửa độc lập, dễ soi leo-thang-quyền riêng; child action VẪN qua execute_tool (không bỏ qua ADR-002).
             − có hai chokepoint phải cùng giữ kỷ luật; ranh giới "cái gì là tool vs cái gì là delegation" phải rõ.

ADR-004 — Evidence-based acceptance + bounded finish
Bối cảnh   : Hai bệnh chết người: báo-xong-khống + chạy-vô-hạn. Success metric M1 = zero false-finish (GĐ1). Bất biến GĐ5 rule #1.
Quyết định : FINISHED chỉ khi `all_accepted()` = mọi AC passed ∧ có ≥1 evidence THẬT (artifact/tool_result/reviewer_report/diff/test_result);
             scaffolding bị từ chối. Song song, tầng guard + budget cứng (max_rounds/no-progress/repeat-decision/parse-budget/MAX_DEPTH/per-root)
             đảm bảo mọi task về terminal có biên. finish-gate chặn finish nếu code_changed ∧ !validation_passed.
Phương án đã loại :
  • LLM/worker tự tuyên bố "xong" (honor-system) — loại: đó CHÍNH là bệnh báo-xong-khống; không audit được, false-finish > 0.
    Acceptance phải do GATE chấm theo evidence thật, không phải self-report.
Hệ quả     : + M1 khả thi bằng kiến trúc (finish bất khả khi thiếu evidence); + không runaway. − phụ thuộc phân loại evidence real-vs-scaffolding
             đúng (là điểm cần siết dần); − guard chặt có thể BLOCKED task hợp lệ nhưng chậm tiến triển → cần chỉnh ngưỡng (open-Q OQ-1 → Operate).
             Lưu ý: hôm nay O tự chấm acceptance = honor-system một phần (judge≠doer chỉ trả giá khi có verifier tách riêng) → ghi rủi ro sang Operate.

ADR-005 — SQLite = chân lý resume (checkpoint atomic)
Bối cảnh   : Resume phải KHÔNG side-effect re-run; checkpoint phải nguyên tử (commands+round+save cùng lúc). Bất biến GĐ5 (I10/I11).
Quyết định : Một embedded relational store (langgraph.sqlite) = chân lý resume duy nhất; AgentState serializable-only;
             commands + round_no + save() trong MỘT transaction. `checkpoint.json` chỉ là PROJECTION cho UI, KHÔNG đọc để resume.
Phương án đã loại :
  • JSON checkpoint làm chân lý resume — loại: ghi nhiều file không atomic → resume từ trạng thái nửa-ghi → side-effect re-run / lệch state;
    JSON giữ vai trò projection đọc-thôi thì hợp, làm truth thì không đảm bảo nguyên tử.
Hệ quả     : + resume an toàn từ bất kỳ checkpoint, deterministic. − state buộc serializable-only (không nhét object sống vào state);
             − có hai biểu diễn (SQLite truth + json projection) phải giữ đồng bộ một chiều (SQLite → json, không ngược).
             (Loại DB cụ thể/managed = việc GĐ7; ở đây chỉ chốt "embedded relational, một chân lý, atomic".)

ADR-006 — Redact-tại-biên + attribution ≠ authz
Bối cảnh   : Glass-box phát mọi event ra ngoài (UI/log) nhưng args tool/LLM chứa secret; và cần biết "ai gây ra" tách khỏi "ai được phép".
             Bất biến GĐ5 (I16/I17, DEC-8). Known gap: tool.requested từng log raw args vào jsonl.
Quyết định : Redactor mask SECRET_KEYS → '[REDACTED]' NGAY TẠI emitter, TRƯỚC fan-out; raw payload không bao giờ rời emitter.
             `issued_by` (attribution) chỉ để quy trách; authz THẬT = requires_permission + checkpoint gate. Redact raw-args-log
             phải bật TRƯỚC khi mở write-tools.
Phương án đã loại :
  • Tin self-report / dùng issued_by làm quyền (trust-O bypass) — loại: attribution có thể bị giả/nhầm; dùng nó làm authz = lỗ leo quyền.
    Authz phải là gate riêng (permission + checkpoint), không suy ra từ "ai nói mình là ai".
Hệ quả     : + 0 secret trong ui_payload; + realtime control không rò bí mật; audit tách bạch trách-nhiệm vs quyền.
             − phải duy trì danh sách SECRET_KEYS (allowlist mask) cập nhật; − redaction thêm một bước ở đường nóng emit (chấp nhận: rẻ, một lần).
```

---

## Tự soi trước khi chốt (bắt buộc)

1. **Lãnh đạo đọc được đoạn đầu?** — CÓ. "Góc nhìn lãnh đạo" 60s + Architecture Brief mở đầu bằng 3 điều CTO nhìn (freeze/2-chokepoint/finish-bất-khả-thiếu-evidence), ngôn ngữ nghiệp vụ, không jargon.
2. **Dev đủ hành động?** — CÓ. Có style + 6 boundary ánh xạ 1–1 context GĐ5 + integration table + auth + C4 Context & Container + Data Flow gắn event → đủ để bước sang chọn stack GĐ7.
3. **Đúng + đủ các phần?** — CÓ. Brief + C4 Context + C4 Container + Data Flow + Integration + Security(+STRIDE) + 6 ADR (mỗi ADR có phương án đã loại). Mỗi boundary trace về một bounded context GĐ5. NFR bám GĐ5 (không bịa; thiếu số → open-Q). OQ-2/OQ-3 đã đóng ở §5; OQ-1 chuyển tiếp Operate có nhãn.
4. **Có lỡ chọn framework?** — KHÔNG. Công nghệ chỉ nêu ở mức loại (in-process module, embedded relational store, vector store, config file). Không tên framework/DB/lib nào bị chốt — dành cho GĐ7.

---

## Cổng GĐ6 — SHAPE (tự-quyết, đóng vai Kiến trúc sư/CTO + Security song song)

**AI duyệt (vai CTO/Kiến trúc sư, Security review song song) kiểm 4 điều:**
1. Đủ bộ artifact (Brief + C4 Context + Container + Data Flow + Integration + Security + ADRs) — ✔ không bỏ cái nào.
2. Module boundary bám đúng 6 bounded context GĐ5, ánh xạ 1–1; data ownership rõ (state chỉ ở session, không "ai cũng đọc") — ✔.
3. Mỗi quyết định lớn có ADR + phương án đã loại; OQ-2/OQ-3 đóng tại §5, OQ-1 chuyển tiếp Operate có nhãn — ✔.
4. Không tên framework nào bị chốt lén — ✔ (chỉ mức loại).
**Security song song:** đường rủi ro nhất (delegate + redaction) có STRIDE; known gap raw-args-log được ghi + ràng buộc "redact trước khi mở write-tools" (ADR-006) — ✔.

```
═══ CỔNG GĐ6 — SHAPE: HexAgent (clean rebuild) ═══
Style / Boundary / Data / Integration / Auth / Security: đã chốt.
  Style = hexagonal modular monolith (frozen kernel + mutable session), 6 module = 6 bounded context GĐ5.
  Data  = state chỉ ở session; SQLite = chân lý resume; checkpoint atomic.
  Auth  = scope/allowed_capabilities tại execute_tool; scope con ⊆ cha; attribution ≠ authz.
C4 Context: đã có · C4 Container: đã có · Data Flow: đã có (6 domain event) · ADR: 6 bản (mỗi cái có phương án đã loại).
Open-Q đóng tại GĐ6: OQ-2 (catalog = config-driven closed allowlist) · OQ-3 (registry allowlist = chân lý tên event, reconcile về tool.requested/completed/failed).
Open-Q còn treo → sau: OQ-1 baseline chi phí/false-finish (→ Operate); ngưỡng alert/P95 chưa có số (→ stack/skeleton/operate, không bịa).
Câu hỏi cổng: Architecture đủ vững để chọn stack & dựng live slice chưa?
════════════════
```

**Quyết định cổng (tự-quyết — product owner: "không hỏi approval").**
**GATE: GO.** Lý do: đủ bộ artifact, mọi boundary trace về bounded context GĐ5, 6 ADR quản đủ rủi ro lõi (isolation, hai chokepoint, finish-by-evidence, resume-truth, redaction), không chốt lén framework. Hai bệnh chết người được đóng bằng *kiến trúc* (ADR-004 + tầng guard), không phải lời hứa. Đủ vững để GĐ7 chọn stack và GĐ8 dựng live slice.
**Phương án đã loại ở tầng cổng:** (a) chờ có số NFR (P95/alert threshold) rồi mới GO — loại: NFR số là để *tinh chỉnh*, không phải điều kiện định-hình; thiếu số đã ghi open-Q có địa chỉ, không chặn shape. (b) mở rộng shape sang control-plane UI transport đầy đủ — loại: UI là consumer của read-model (sau MVP), không đổi hình lõi; giữ Đủ-là-đủ.

---

## Bàn giao sang `stack` (GĐ7)

```
═══ BÀN GIAO — SHAPE → STACK: HexAgent (clean rebuild) ═══
Hình đã chốt      : Hexagonal modular monolith một tiến trình · 6 module (Orchestration/Execution-Core/Discipline/
                    Tools-Safety/Control-Plane/Knowledge-opt) · integration chính = LLM/tool qua execute_tool (đồng bộ) +
                    event in-process + RAG health-gated + (sau MVP) 3-seam BE↔UI · deployment = single deployable, resume qua embedded SQLite.
Ràng buộc cho stack:
  • Ngôn ngữ/runtime phải hỗ trợ freeze-kernel + serializable-only state (resume không side-effect).
  • Cần embedded relational store làm chân lý resume + transaction atomic (commands+round+save).
  • Cần LLM adapter JSON-mode + phân loại retry transient-vs-permanent.
  • Cần vector store health-gated, offline-first (RAG tùy chọn, never raises).
  • Redactor mask SECRET_KEYS tại biên; event catalog + command catalog = config-driven closed allowlist.
  • Middleware chain có thứ tự cố định (Timing→Policy→Budget→Retry→Condense→core).
Open-Q chuyển tiếp:
  • OQ-1 baseline chi phí/false-finish thực → Operate (không phải việc stack).
  • Ngưỡng NFR số (P95 loop, alert error-rate) chưa có → cần ở stack/skeleton nếu đo được, KHÔNG bịa.
  • Loại DB/vector-store/LLM-provider cụ thể + framework graph-runtime = quyết ở GĐ7.
Artifact          : rebuild-hex-agent/pipeline/06-shape.md
→ Chọn framework/DB/lib hiện thực hình này (GĐ7): chạy /stack
→ Muốn dựng ngay một lát cắt sống để validate shape (vd "accept→plan→next_node→judge"): chạy /skeleton hoặc /frame
→ Cần hiểu code gốc shape sẽ đụng: chạy /atlas (đã có .ai-understanding) hoặc /explain
→ Cần điều phối cả pipeline: chạy /partner
════════════════
```
*Traceability:* GĐ6 nhận Domain Model GĐ5 (`pipeline/05-idea-domain.md`: 6 bounded context, 5 rule bất biến, 6 domain event, data ownership, OQ-2/OQ-3) → sinh Architecture Brief + C4 + Data Flow + Integration + Security + 6 ADR → bàn giao `stack` (GĐ7). OQ-2/OQ-3 đóng tại đây; OQ-1 + NFR-số chuyển tiếp có địa chỉ.
