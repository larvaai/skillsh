# REBUILD BRIEF — the shared anchor for every pipeline stage

> Every skill stage (idea…operate + atlas/frame/review/explain/traceability/grade) MUST read this file first, then its own evidence files, then produce its artifact. This guarantees all stages name the same product, the same domain entities, the same invariants. Do NOT re-derive these — build on them.

## What we are rebuilding
The **essence** of `hex_agent`, stated by the product owner:
> "Giao MỘT task cho agent → nó tự lên plan → sắp xếp các bước phải làm → gọi các sub-agent vào làm việc → và chỉ KẾT THÚC khi task thật sự hoàn thành."

This is a **from-scratch rebuild** whose scope = the whole hex_agent, but centered on that autonomous task-orchestration loop. Everything else (kernel, tools, control plane, observability) exists to make that loop **safe, bounded, and provable**.

## Product identity
- **Name:** HexAgent (clean rebuild) — codename/slug `hex-agent-rebuild`.
- **One-line:** Một agent tự-điều-phối: bạn giao một mục tiêu, nó tự lập kế hoạch, chia nhỏ thành các bước có thứ tự, giao cho các sub-agent thực thi, và chỉ dừng khi MỌI tiêu chí nghiệm thu được chứng minh bằng bằng chứng thật.
- **Kiến trúc gốc:** hexagonal microkernel (nhân đông cứng + session sống), glass-box event-log-first.

## The core mechanism to preserve (the "only ends when complete" loop)
1. **Plan/Decompose** — task → cây kế hoạch (forest theo `parent` + DAG theo `depends_on`, cả hai acyclic). Node `work|reduce` với `done_when` (danh sách `DoneWhen` = tiêu chí + gate check + artifact). Cổng-2 `accept_decomposition` là gate CẤU TRÚC thuần chạy TRƯỚC khi đổi cây, có **chứng minh dừng** μ(node)=len(done_when) co ngặt mỗi lần chia + coverage-by-implication + phát hiện RENAME/STUCK.
2. **Order steps** — `next_node()` = node pending trái nhất mà mọi dependency đã done (topo theo depth,order) → "không leo sớm" miễn phí.
3. **Delegate** — chokepoint RIÊNG (`DelegationManager.delegate`, KHÔNG phải method của kernel): validate policy (depth≤max, scope ⊆ parent, max_steps) → child session → handler.run → merge artifact → đóng child. Broker chỉ nắn context, KHÔNG mở rộng scope; O đặt `allowed_capabilities`.
4. **Judge & finish** — `judge_acceptance`: mỗi AC "passed" phải có ≥1 **bằng chứng THẬT** (artifact/tool_result/reviewer_report/diff/test_result), KHÔNG chấp nhận scaffolding (session_plan/context_packet/ac_report). `all_accepted()` = mọi AC passed + có evidence → FINISHED. Worker KHÔNG tự ghi verdict — chỉ gate ghi.
5. **Bounded / anti-runaway** — vòng lặp dừng cứng bởi: max_rounds, no-progress guard (artifacts không tăng ∧ acceptance không đổi ∧ không có command), repeat-decision guard (chữ ký quyết định lặp N lần), parse-error budget (lỗi liên tiếp), MAX_DEPTH, per-root step budget. → "chỉ kết thúc khi xong" KHÔNG mâu thuẫn với "không chạy vô hạn".

## Domain entities (dùng đúng tên này xuyên suốt)
`Task/Goal` · `Plan` · `Node(work|reduce)` · `DoneWhen` (criterion) · `DependencyEdge` · `Run` · `Session`/`SessionIdentity` · `Agent`/`Role` · `Delegation` · `AcceptanceCriterion` · `Evidence` · `Budget` · `Event(RuntimeEvent)` · `Command(RuntimeCommand)` · `Checkpoint` · `Permission`.

Bounded contexts: **Orchestration** (task loop, plan, delegation, acceptance) · **Execution Core** (kernel chokepoint, session, registry) · **Discipline** (json/finish/budget/condense) · **Tools & Safety** (sandbox, policy) · **Observability/Control Plane** (events, snapshot, commands, redaction) · **Knowledge** (RAG, optional).

## The 7 load-bearing invariants (KHÔNG được phá khi rebuild)
1. **Nhân đông cứng, session sống** — freeze kernel trước run đầu; state chỉ ở session → 0 rò state giữa các run (I2/I3).
2. **Một chokepoint `execute_tool`** — mọi hành động (LLM/tool/scope-check/observability/envelope) đi qua đúng một cửa (I1).
3. **Event-log-first glass-box** — mọi capability call phát `tool.requested/completed`; event log là nguồn audit + replay.
4. **Delegation chokepoint RIÊNG + scope child ⊆ parent** — multi-agent auditable, không leo thang quyền (I13/I14).
5. **Nghiệm thu bằng bằng chứng + finish có biên** — chỉ FINISHED khi mọi AC có evidence thật; budget/guards chặn runaway (E10 + discipline).
6. **SQLite = chân lý resume; checkpoint nguyên tử** — `langgraph.sqlite` là truth, `checkpoint.json` chỉ là projection UI; commands+round+save trong một transaction (I10/I11).
7. **Redact tại biên; attribution ≠ authz** — `ui_payload` che secret trước khi rời emitter; `issued_by` chỉ để quy trách, authz thật = `requires_permission` + checkpoint (I16/I17, DEC-8).

## Roadmap skeleton (khi backlog cần) — bám epic gốc
P0 Foundation: E01 Kernel · E02 Discipline · E03 LLM · E04 Observability.
P1–P2 Single-agent+Tools: E05 Graph/Resume · E06 Tools&Safety · E07 Skills · E08 RAG.
P3 Multi-agent (LÕI của sản phẩm): E09 Roles · E10 TaskLoop+Delegation+Acceptance.
P4 Realtime Control: E21 Control Plane (contracts→emitter→transport→UI→reliability).
Future (park-with-trigger, YAGNI): E11 Departments · E12 IntentRouter · E13 SoftwareFactory · E14 Ledger/Memory · E20 Labs. E15 self-eval merged→E21.

## Cách làm việc (quan trọng — chế độ tự-quyết)
- Product owner đã nói: **"Không hỏi approval, tự quyết."** → KHÔNG gọi AskUserQuestion, KHÔNG dừng chờ ở cổng. Ở mỗi cổng, ĐÓNG vai người duyệt của skill (CTO/PO/Tech-lead tuỳ stage), tự đưa quyết định GO hợp lý, và GHI RÕ quyết định + lý do + phương án đã loại (ADR). Nếu một ẩn số thực sự chưa có dữ liệu → ghi thành open-Q mang sang stage sau, KHÔNG bịa số.
- Bám **hợp đồng đọc-được-3-tầng**: mở mỗi artifact bằng "Góc nhìn lãnh đạo" (1–3 điều nghiệp vụ, không jargon) → rồi chi tiết cho dev. 1 trang, scan 2–3 phút.
- **Đủ-là-đủ**: độ sâu tỉ lệ rủi ro/ẩn số; KHÔNG bỏ artifact nào skill yêu cầu, chỉ rút gọn độ sâu.
- **Không bịa**: chỉ khẳng định điều evidence (file 00-understanding/*) chống lưng; anchor về `file:line` gốc khi có.
- Ngôn ngữ artifact: **tiếng Việt** (khớp skill + product owner), thuật ngữ kỹ thuật/định danh code để nguyên tiếng Anh.
