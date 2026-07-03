# 08 — Skeleton: Live Slice Report — HexAgent (clean rebuild)

> Skill `skeleton` · Giai đoạn 8 (PROOF / Walking Skeleton). Vào bằng **Tech Decision GĐ7** (`pipeline/07-stack.md`) + **Architecture Brief GĐ6** (`pipeline/06-shape.md`) + **Domain GĐ5** (`pipeline/05-idea-domain.md`). Ra bằng **một Live Slice Report** cho lát cắt mỏng nhất xuyên đủ tầng, chứng minh kiến trúc + stack + boundary + delivery CHẠY THẬT trước khi đổ người.
> Anchor gốc: `00-understanding/REBUILD-BRIEF.md` + `evidence-A/B/C` + `ATLAS.md`. Đây là **rebuild có tham chiếu code gốc** (brownfield-informed): nhiều tầng ĐÃ chạy thật trong bản GỐC (anchor `file:line`) → với mỗi ô validate phân biệt rõ **"bằng chứng chạy trong bản GỐC"** vs **"phần cần dựng lại trong rebuild"**. KHÔNG tick khống ô nào chưa chạy thật TRÊN BẢN REBUILD.
> Chế độ tự-quyết: cổng go/no-go do người viết đóng vai **CTO (mở cổng) · Tech-lead + dev (chủ sở hữu)** tự quyết, ghi rõ lý do + phương án đã loại. Không hỏi user. `skeleton` KHÔNG viết code slice — định slice + đường đi E2E + checklist rồi bàn giao `/frame`; nhận lại link staging + kết quả test để lấp Report.

---

## ── GÓC NHÌN LÃNH ĐẠO (đọc trước, 60 giây — không cần biết code) ──

**Ta đang chứng minh điều gì.** Trước khi đổ người vào dựng đủ hệ, ta cắt **một lát mỏng nhất nhưng xuyên hết tầng** để chứng minh cái LÕI của sản phẩm chạy thật: *giao 1 task 2 bước → agent tự lập kế hoạch → sắp thứ tự theo phụ thuộc → giao cho 1 sub-agent làm → chấm nghiệm-thu bằng bằng chứng THẬT → chỉ kết thúc khi đủ bằng chứng, và có phanh chặn chạy-vô-hạn*. Nếu lát này chạy được end-to-end trên staging thì ba lời hứa đắt nhất của hệ — *không báo-xong-khống, không chạy-vô-hạn, không leo-thang-quyền* — đã được chứng minh bằng máy, không bằng lời.

**Trạng thái hôm nay (nói thẳng).** Đây là **rebuild trên nền một hệ đã chạy**. Bản GỐC (`/Users/uspro/Desktop/namnson/hex_agent`) đã chứng minh **cả 9 tầng chạy thật** — có anchor `file:line` cho từng tầng (vòng lặp `supervisor/loop.py:_drive`, cửa giao-việc `delegation/manager.py:63`, resume `orchestrator/loop.py:resume`, nghiệm-thu-bằng-bằng-chứng `judge_acceptance`). NHƯNG code REBUILD **chưa được gõ và chưa deploy lên staging** → **0/9 ô tick THẬT trên bản rebuild**. Vì vậy trạng thái trung thực là: **kiến trúc & stack đã được chứng minh chạy ở bản gốc; slice rebuild đã được ĐÓNG KHUNG đầy đủ (scope + đường đi + tiêu chí) và bàn giao cho đội build (`/frame`) để dựng thật rồi báo link staging + kết quả test về đây.** Chưa được tuyên "pass".

**Ba điều lãnh đạo cần nhìn.** (1) **Link staging:** `⏳ CHƯA CÓ` — sẽ có sau khi `/frame` dựng slice trên nền Python 3.11 + LangGraph + SQLite đã chốt GĐ7. (2) **Checklist validate:** 0/9 tick-thật-rebuild; nhưng 9/9 có **bằng chứng-gốc anchored** cho thấy đường đi khả thi → rủi ro tổng THẤP (đang tái dựng cái đã chạy, không khám phá từ 0). (3) **Giả định phải đổi:** một ẩn số kỹ thuật **duy nhất** còn treo — LangGraph resume "một-lần-đúng, không chạy-lại-gây-tác-dụng-phụ" (SPIKE-1 từ GĐ7) — được **cố tình DÍNH vào chính slice này** để đo cho rẻ. Đây là điều kiện go/no-go thật của cổng.

**Kết luận cho lãnh đạo.** Sẵn sàng đổ người vào build full: **CHƯA** — đúng theo kỷ luật cổng (chưa có staging chạy thật trên bản rebuild thì chưa pass). Nhưng rủi ro để **bắt đầu dựng slice này** là THẤP và có địa chỉ: mọi tầng đã có tiền lệ chạy ở gốc, ẩn số còn lại đúng một cái và đã được đóng khung để đo ngay trong slice. Đề nghị: **GO cho việc dựng slice** (không phải GO cho build-full) → `/frame` dựng + chạy SPIKE-1 → quay lại cổng này với số thật.

---

## ── CHI TIẾT KỸ THUẬT (cho dev) ──

### 1. Slice — lát cắt mỏng nhất xuyên đủ tầng

**Tên slice:** `finish-by-evidence-tối-thiểu` — *"Giao 1 task 2 bước → plan → order theo deps → delegate 1 worker → judge acceptance trên evidence THẬT → FINISHED, có budget/guard chặn runaway; resume được từ SQLite giữa chừng."*

**Cụ thể hoá task 2 bước** (đủ nhỏ để mỏng, đủ để chạm mọi tầng rủi ro): task gốc `T0` có `done_when` gồm 2 tiêu chí độc lập-có-thứ-tự, ví dụ:
- `N1 (work)`: "tạo file `var/workspace/out.txt` chứa chuỗi X" — `done_when = [file tồn tại ∧ nội-dung==X]`, evidence = `tool_result` của `fs_write` + `fs_read`.
- `N2 (work, depends_on=[N1])`: "đọc `out.txt`, ghi độ dài vào `var/workspace/len.txt`" — `done_when = [len.txt tồn tại ∧ ==len(X)]`, evidence = `tool_result`.
- `N_reduce (synthetic)`: gom artifact 2 node → AC gốc của `T0`.

Task này **cố ý** đi qua: decompose (Cổng-2 `accept_decomposition` với μ↓), ordering có phụ thuộc (`N2` không được chạy trước `N1`), delegate ra 1 worker với **scope con ⊆ cha** (worker chỉ được cấp `fs_read/fs_write` trong jail, KHÔNG `terminal_run`), tool chạy thật qua `execute_tool` (phát `tool.requested/completed` vào `events.jsonl`), judge acceptance trên **evidence thật** (`tool_result`, KHÔNG phải scaffolding), và finish có biên (budget `max_steps` + no-progress guard).

**Lý do chọn slice này + slice đã cân nhắc & loại:**
- **Chọn** vì nó chạm **6/7 invariant lõi** của REBRIEF trong ít code nhất: I2/I3 (session state), I1 (một chokepoint execute_tool), event-log-first (I·evt), I13/I14 (delegation scope⊆parent), evidence-based finish + bounded (E10/discipline), I10/I11 (SQLite resume). Chỉ I16/I17 (redact/attribution ở control-plane) là **không** thuộc slice này — control-plane UI là "sau MVP" (ADR-006 GĐ6) → cố tình để ngoài (Đủ-là-đủ).
- **Loại "chỉ single-agent, không delegate"** — mỏng hơn nhưng KHÔNG chạm cửa giao-việc riêng (`DelegationManager`) và scope-shrink, tức bỏ đúng rủi ro multi-agent (LÕI của sản phẩm, P3/E10). Không đáng: chứng minh thiếu chốt nguy hiểm nhất.
- **Loại "task 1 bước, không deps"** — bỏ `next_node()` ordering + Cổng-2 μ↓; slice không chứng minh được "không leo sớm" và "chứng-minh-dừng". Loại.
- **Loại "full control-plane UI + SSE stream"** — phình sang seam BE↔UI (sau MVP), thêm 1 tầng transport không cần cho việc chứng minh LÕI loop. Loại (giữ cho slice sau).
- **Giữ resume-giữa-chừng TRONG slice** (không tách): để DÍNH LUÔN **SPIKE-1** (ẩn số rủi ro cao duy nhất của GĐ7) vào lát rẻ nhất — kill process sau `N1`, resume cùng `run_id`, kiểm không re-emit `tool.requested` của `N1`.

### 2. Đường đi (E2E) — mô tả từng chặng thật + anchor bản GỐC

| # | Chặng | Thành phần rebuild (module GĐ6) | Bằng chứng ĐƯỜNG ĐI ở bản GỐC (anchor file:line) |
|---|---|---|---|
| 1 | **Intake** | Facade / Entry nhận `TaskEnvelope(task_id,user_request)` → `SessionFactory` tạo Run/Session (state chỉ ở session) | `orchestrator/loop.py:run()` [93-147]; `core/session.py` SessionFactory (`ATLAS`/evidence-B §2) |
| 2 | **Kernel.execute_tool (LLM plan)** | Worker gọi LLM-as-capability QUA `execute_tool` để đề xuất cây plan; JSON-mode → `parse_decision` | `core/kernel.py:106-150` chokepoint; `supervisor/contracts.py:117-182` `parse_decision` strict JSON |
| 3 | **Decompose gate (`accept_decomposition`)** | Cổng-2 thuần cấu trúc chạy TRƯỚC khi đổi cây: μ(node)=len(done_when) co ngặt + coverage-by-implication + RENAME/STUCK | `decompose_agent/solve.py:_decompose()` [132-185]; `accept.py:52-128` (μ proof, coverage [101-127]) |
| 4 | **Order (`next_node`)** | node pending trái nhất mà mọi dep đã done (topo depth,order) → `N1` trước `N2` | `decompose_agent/tree.py:next_node()` [43-51] |
| 5 | **Delegate (`DelegationManager.delegate`)** | cửa RIÊNG (không phải kernel method): validate policy (depth≤max, **scope⊆parent**, max_steps) → child session (SessionFactory scope-shrink) → `Handler.run()` → merge artifact → close → emit `delegation.finished` | `delegation/manager.py:delegate()` [63-192]; `policy.py:13-32` scope⊆parent [25-26]; `session.py:163` scope-shrink |
| 6 | **Worker execute_tool (tool thật)** | child action `fs_write`/`fs_read` đi lại QUA `execute_tool` (I1) → sandbox jail (`resolve_in_workspace`) → PolicyGate fail-closed | `core/kernel.py:106-150`; `safety/sandbox.py:38,97` jail; `middleware/policy.py` PolicyGate |
| 7 | **Emit events.jsonl** | mọi capability call phát `tool.requested/completed` → EventLogger append `events.jsonl` + summary + metrics | `observability/event_log.py:102` attach_to_bus; EventLogger subscribe tool.*/task.* (evidence-B §7) |
| 8 | **judge_acceptance (evidence THẬT)** | O nộp `acceptance_status[{id,status,evidence_ids}]`; mỗi "passed" phải có ≥1 evidence resolve trên Blackboard ∧ **là REAL** (artifact/tool_result/reviewer_report/diff/test_result), scaffolding bị từ chối; worker KHÔNG ghi verdict | `supervisor/graph.py:judge_acceptance()` [357-382]; `evidence.py:16-23` real-vs-scaffolding |
| 9 | **Finish HOẶC Blocked (bounded)** | `all_accepted()` = mọi AC passed ∧ evidence≠∅ → **FINISHED**; chạm guard bất kỳ (max_rounds/no-progress/repeat-decision/parse-budget/MAX_DEPTH/per-root step) → **BLOCKED** | `supervisor/loop.py:_drive()` [157-241] (finished [186], guards [164-239]); `discipline/budget.py:Budget` [10-67] |
| ✚ | **Resume từ SQLite** (DÍNH SPIKE-1) | kill sau `N1`; resume cùng `run_id` từ `langgraph.sqlite`; commands+round+save trong MỘT transaction; KHÔNG re-emit `tool.requested` của `N1` | `orchestrator/loop.py:resume()` [217-273] (SQLite via `open_checkpointer` [246], resume from `next` [260-269]); atomic txn `loop.py:208-218` |

> **Đọc bảng này thế nào:** cột phải là bằng chứng rằng **đường đi từng chặng ĐÃ tồn tại và chạy ở bản gốc** — nghĩa là slice rebuild không phải khám phá kiến trúc, mà là *tái hiện một đường đã thông*. Đó là lý do rủi ro dựng slice THẤP. Nhưng "đã chạy ở gốc" ≠ "đã chạy ở rebuild" → xem checklist §4.

### 3. Link staging

`⏳ CHƯA CÓ — slice rebuild chưa được `/frame` dựng & deploy.` Khi có: URL staging chạy thật + tài khoản demo (giao 1 task 2 bước → xem event log → thấy FINISHED có evidence). **Không bịa link.** Đây là ô chặn cổng "pass".

### 4. Đã validate — checklist 9 ô (REBUILD: gốc-đã-chạy vs cần-dựng-lại)

> **Luật:** ô `[x]` = có bằng chứng chạy THẬT **trên bản rebuild** (staging mở được / CI xanh / test pass / có log-metric-trace). Vì rebuild chưa dựng → **không ô nào `[x]`**. Với mỗi ô ghi: **G** = bằng chứng chạy trong bản GỐC (anchor) · **R** = phần cần dựng lại + đo trong rebuild.

```text
[ ] 1. Kiến trúc hợp lý (hexagonal frozen-kernel + mutable session, loop tuần tự)
      G: gốc chạy trọn loop — orchestrator/loop.py:run [93-147], supervisor/loop.py:_drive [157-241].
      R: dựng lại facade+_drive trên Python 3.11; DoD = task 2 bước về FINISHED. → /frame.

[ ] 2. Stack/framework phù hợp (Python 3.11 · LangGraph · SQLite — GĐ7)
      G: gốc chạy trên đúng cụm này (ATLAS.md:27; langgraph.sqlite = truth).
      R: dựng graph tối thiểu + SQLite checkpointer; xác nhận bản Python chính xác (open-Q GĐ7). → /frame.

[ ] 3. Module boundary ổn (Orchestration/Execution-Core/Delegation qua PORT, không cross-import)
      G: delegation là cửa RIÊNG khỏi kernel — delegation/manager.py:63; execute_tool chokepoint core/kernel.py:106-150.
      R: dựng ToolPort/DelegationPort; test: không call site nào gọi tool/LLM ngoài execute_tool (audit-test). → /frame.

[ ] 4. Auth = scope chạy (allowed_capabilities tại execute_tool; scope con ⊆ cha khi delegate)
      G: gốc enforce 2 tầng — policy.py:25-26 + session.py:163 (SessionFactory scope-shrink).
      R: property-test (Hypothesis): với MỌI child-cap ⊄ parent → delegate REJECTED fail-closed. → /frame.

[ ] 5. DB = SQLite checkpoint hợp lý (chân lý resume; commands+round+save 1 transaction, resume 0 side-effect)
      G: gốc resume từ SQLite — orchestrator/loop.py:resume [217-273]; atomic txn loop.py:208-218.
      R: ⚠️ ĐÂY LÀ SPIKE-1 (ẩn số cao GĐ7) — kill sau N1, resume, kiểm (a) không re-emit tool.requested của N1,
         (b) round_no liên tục, (c) crash giữa txn không để checkpoint nửa-ghi. CHƯA ĐO. → /frame chạy + báo số.

[ ] 6. CI xanh (pipeline chạy test tự động trên slice)
      G: gốc có 327 test + tests_audit (evidence-C:25) — nhưng CI cụ thể chưa neo được cho bản rebuild.
      R: dựng CI tối thiểu (lint + pytest + audit-test) chạy trên slice; ô này chỉ tick khi pipeline XANH thật. → /frame + delivery.

[ ] 7. Test strategy thực tế (pytest + Hypothesis property + audit — GĐ7)
      G: gốc dùng pytest + tests_audit (evidence-C:25,66).
      R: viết ≥1 property-test cho invariant lõi (μ↓ HOẶC scope⊆parent) + ≥1 integration cho E2E slice + audit
         cho delegate/redaction. Chạy pass thật mới tick. → /frame.

[ ] 8. Observability = event-log đủ (events.jsonl + summary + metrics; seq monotonic; replay=snapshot)
      G: gốc EventLogger → jsonl+summary+metrics (observability/event_log.py:102); replay deterministic (evidence-B §7).
      R: slice phải sinh events.jsonl chứa tool.requested/completed của N1,N2 + delegation.finished; kiểm seq gap-free.
         ⚠️ Known gap gốc: tool.requested log raw args → REDACT trước khi bật write-tools (ADR-006 GĐ6). → /frame.

[ ] 9. Team hiểu flow delivery (dev chạy lại được full flow trên staging + đọc được đường đi E2E)
      G: đường đi E2E đã có anchor gốc (bảng §2) → dev có bản đồ.
      R: sau khi staging chạy, 1 dev NGOÀI dựng-lại-được từ Report này (không hỏi tác giả) mới tick. → /frame.
```

**Tổng tick THẬT (rebuild):** **0/9** — trung thực với luật "chạy thật, không mockup". **Bằng chứng-đường-đi gốc:** 9/9 có anchor → nền để dựng, không phải để tick.

### 5. Giả định đã đổi (feed ngược PRD/Architecture/backlog)

- **SPIKE-1 chưa từ "treo" → phải ĐO trong slice này.** GĐ7 để LangGraph resume ở trạng thái `TREO` (điều-kiện-đảo-chiều: fail → orchestrator tự viết). GĐ8 chốt: **đây là điều kiện go/no-go THẬT của walking skeleton** — không đo xong không được đổ người. (Cập nhật ngược: `stack.json.spike[0].do_o` → hiện thực ở đây.)
- **Reconcile tên event (OQ-3 GĐ6) phải làm NGAY trong slice.** Bản gốc có known-mismatch: kernel phát `tool.requested/completed` nhưng registry khai `tool.call_requested/before_call/after_call` (evidence-B §3). Slice này **buộc** dùng bộ tên đã reconcile (`tool.requested/completed/failed` = allowlist chân lý) vì ô 8 kiểm chính event đó → nếu không reconcile, event-log ô 8 sẽ lệch. (Cập nhật ngược GĐ6 §5 OQ-3: từ "quyết" → "thực thi ở skeleton".)
- **Redact-raw-args phải bật TRƯỚC ô 8 chạy write-tool.** ADR-006 GĐ6 ghi ràng buộc; slice dùng `fs_write` (write-tool) → redact SECRET_KEYS phải hoạt động trước khi ô 8 tick. Nâng từ "ghi chú" → "chặn ô 8". (Feed ngược Security Model GĐ6 §6.4.)
- **`max_steps` từ "knob không enforce ở core" → phải enforce trong slice.** evidence-B §2 lưu: core coi `max_steps` là knob KHÔNG enforce; nhưng ô 9 (bounded finish) cần budget cắt thật → slice phải enforce `Budget.max_steps` ở tầng loop/discipline (đúng như `discipline/budget.py` gốc), không để hở. (Feed ngược: xác nhận vị trí enforce = discipline, không phải core.)

### 6. Rủi ro còn lại (chưa gỡ trong slice → kiểm ở đâu)

- **R1 · LangGraph resume "một-lần-đúng" (SPIKE-1)** — rủi ro cao nhất; đo NGAY trong slice (ô 5). Nếu fail 3 tiêu chí (a/b/c) → mở lại orchestrator tự viết (§2 GĐ7), KHÔNG đụng shape. **Kiểm:** ngay trong live slice này (rẻ nhất).
- **R2 · NFR-số (P95 loop, ngưỡng alert error-rate) — OQ-1** — chưa có số, platform nội bộ tải thấp, **không bịa**. **Kiểm:** perf test GĐ12 (uat) + baseline ở Operate.
- **R3 · Judge = honor-system một phần** — hôm nay Agent-O tự chấm acceptance (judge≠doer chỉ trả giá khi có verifier tách riêng, evidence-C §4; ADR-004 GĐ6). Slice chứng minh *cơ chế evidence-gate* chạy, KHÔNG gỡ được rủi ro self-score. **Kiểm:** siết dần evidence types ở E21/Operate (merged E15→E21).
- **R4 · Control-plane UI + SSE + redaction đầy đủ** — cố ý NGOÀI slice (sau MVP). Rủi ro rò secret qua ui_payload chưa chứng minh ở đây. **Kiểm:** slice control-plane riêng (E21) + Security sign-off GĐ12.
- **R5 · CI/CD thực (ô 6)** — chưa có pipeline; chỉ có test gốc. **Kiểm:** dựng cùng Delivery Standards GĐ11 (`/delivery`).

---

## 7. Tự soi trước khi chốt (bắt buộc — theo rubric)

1. **Lãnh đạo đọc RIÊNG khối đầu có biết on-track không?** — CÓ: khối "Góc nhìn lãnh đạo" nói thẳng *link staging chưa có → chưa pass*, *0/9 tick-rebuild nhưng 9/9 có tiền lệ gốc → rủi ro dựng thấp*, *ẩn số còn 1 cái (resume) đã đóng khung để đo*. Ngôn ngữ nghiệp vụ, không mở bằng tên framework.
2. **Dev đủ chạy lại full flow?** — CÓ: đường đi E2E 9+1 chặng có anchor gốc + module rebuild; checklist ghi rõ ô nào gốc-đã-chạy / ô nào cần dựng + đo gì để tick.
3. **Đủ + đúng các phần template GĐ8?** — CÓ: slice · đường đi E2E xuyên đủ tầng (không bỏ tầng nào; control-plane cố ý để ngoài + ghi lý do) · link staging (trung thực ⏳) · checklist 9 ô · giả định đã đổi · rủi ro còn lại.
4. **Mọi ô tick có bằng chứng chạy THẬT?** — CÓ (bằng cách KHÔNG tick ô nào): 0/9 tick-rebuild vì chưa có staging chạy thật → **không tick khống**. Phân biệt rõ bằng-chứng-gốc (đường đi) vs cần-dựng-lại (proof rebuild).
5. **Bám GĐ7, không bịa, không chọn lại stack, không trôi build full?** — CÓ: dùng đúng Python 3.11 · LangGraph · SQLite · pytest+Hypothesis đã chốt GĐ7; SPIKE-1 đặt đúng chỗ; không đẻ feature ngoài slice; code thật bàn giao `/frame`.

---

## 8. Cổng GĐ8 — LIVE SLICE (tự-quyết; đóng vai CTO mở cổng · Tech-lead + dev chủ sở hữu)

**Câu hỏi cổng (doc GĐ8):** *"Live slice pass chưa?"* — slice chạy thật trên staging, có test + observability, checklist validate tick đủ ô rủi ro cao. **Pass mới được scale ra nhiều module/feature.**

**Trình cổng (chủ sở hữu = Tech-lead + dev):**
- Slice đã đóng khung đầy đủ (scope + đường đi E2E 9+1 chặng + 9 ô checklist + tiêu chí tick + SPIKE-1 tiêu chí a/b/c).
- Tick THẬT trên rebuild: **0/9** (chưa có staging). Bằng chứng-đường-đi gốc: 9/9 anchored.
- Ô rủi ro cao còn trống: ô 5 (resume/SPIKE-1) — chưa đo → **mặc định chưa pass**.

```
═══ CỔNG GĐ8 — LIVE SLICE: "finish-by-evidence-tối-thiểu" (HexAgent rebuild) ═══
Slice        : task 2 bước → plan → order(deps) → delegate 1 worker (scope⊆parent) → judge-by-evidence → FINISHED/BLOCKED,
               +resume từ SQLite (DÍNH SPIKE-1). Xuyên Intake→execute_tool→decompose-gate→next_node→DelegationManager→worker
               →events.jsonl→judge_acceptance→finish.
Tick thật    : 0/9 trên bản REBUILD (chưa có staging chạy thật). 9/9 có bằng-chứng-đường-đi ở bản GỐC (anchored).
Ô rủi ro cao trống: #5 resume/SPIKE-1 (ẩn số go/no-go thật) · #6 CI · #8 observability đo thật — chưa chạy trên rebuild.
Link staging : ⏳ CHƯA CÓ.
Câu hỏi cổng : Live slice pass chưa?
════════════════
```

**Quyết định cổng (tự-quyết — product owner: "không hỏi approval").**

**GATE: NO-GO cho "pass live slice / đổ người vào build full."** Đúng kỷ luật: chưa có staging chạy thật trên bản rebuild + ô rủi ro cao (#5 resume) chưa đo → **chưa được tuyên pass**. KHÔNG dùng câu phủ định cứng: đây không phải "không chạy được" — mà là *chưa dựng nên chưa chứng minh*, có lối đi tiếp rõ ràng.

**Quyết định kèm theo — GO cho "dựng slice này ngay":** vì rủi ro dựng THẤP (9/9 tầng có tiền lệ chạy ở gốc, ẩn số còn đúng 1 cái đã đóng khung) → cho phép `/frame` bắt tay dựng + chạy SPIKE-1 + báo số về cổng này. Đây là **lối đi tiếp** thay cho phủ định.

**Phương án đã loại ở tầng cổng:**
- (a) *Tuyên "pass" dựa trên bằng-chứng-gốc (9/9 anchored)* — **loại**: "đã chạy ở gốc" ≠ "đã chạy ở rebuild"; tick theo gốc = tick khống trên bản rebuild → vi phạm luật "chạy thật, không mockup", lãnh đạo sẽ tin nhầm "kiến trúc rebuild đã chứng minh" và đổ ngân sách vào nền chưa chạy.
- (b) *Tách resume/SPIKE-1 ra khỏi slice cho "pass nhanh"* — **loại**: resume-atomic là ẩn số rủi ro cao DUY NHẤT của stack (ADR-002 điều-kiện); tách ra = pass một walking skeleton bỏ đúng chỗ dễ sụp → false-proof.
- (c) *Mở rộng slice sang control-plane UI + SSE để "chứng minh nốt"* — **loại**: control-plane là sau-MVP (ADR-006), thêm tầng transport không đổi bản chất rủi ro LÕI loop → vi phạm Đủ-là-đủ; giữ cho slice E21 riêng.

---

## 9. Bàn giao — Live Slice: "finish-by-evidence-tối-thiểu"

```
═══ BÀN GIAO — Live Slice: "finish-by-evidence-tối-thiểu" (HexAgent rebuild) ═══
Đã chứng minh   : (bản GỐC) 9/9 tầng có bằng-chứng-đường-đi anchored — loop/_drive, delegate:63, resume, judge_acceptance.
                  (bản REBUILD) slice đã đóng khung đầy đủ (scope + E2E 9+1 chặng + 9 ô + tiêu chí + SPIKE-1 a/b/c); tick thật 0/9.
Giả định đã đổi : SPIKE-1 từ "treo" → điều-kiện-go/no-go phải đo trong slice · OQ-3 reconcile tên event làm NGAY ·
                  redact-raw-args bật TRƯỚC ô 8 write-tool · max_steps enforce ở discipline (không phải core).
Code thật slice : CHƯA CÓ — dựng tại repo rebuild (nền Python 3.11+LangGraph+SQLite GĐ7) → /frame viết + deploy staging + chạy test/SPIKE-1.
Artifact        : rebuild-hex-agent/pipeline/08-skeleton.md (+ state pipeline/skeleton.json)
Rủi ro còn lại  : R1 resume/SPIKE-1 (đo trong slice) · R2 NFR-số (perf GĐ12/Operate) · R3 judge honor-system (siết E21/Operate)
                  · R4 control-plane redaction (slice E21 + Security GĐ12) · R5 CI/CD thật (Delivery GĐ11).
→ Viết CODE THẬT lát cắt này + deploy staging + chạy SPIKE-1 rồi báo link+kết quả về Report: chạy /frame
→ Phân rã roadmap + backlog (Epic→Feature→Story→AC) cho release gần nhất (GĐ9): chạy /backlog
→ Chốt chuẩn giao hàng (CI/CD, DoD, test pyramid) cho ô #6/#7: chạy /delivery
→ Cần điều phối cả pipeline / traceability đủ: chạy /partner
════════════════
```

*Traceability:* GĐ8 **nhận** Tech Decision GĐ7 (`07-stack.md`: Python 3.11·LangGraph·SQLite·OpenAI-compatible·pytest+Hypothesis·SSE + SPIKE-1 treo) làm thứ-cần-chứng-minh → định slice mỏng nhất xuyên đủ tầng chạm 6/7 invariant REBRIEF → checklist 9 ô phân biệt bằng-chứng-gốc (anchored) vs cần-dựng-lại → **feed ngược**: SPIKE-1 thành điều-kiện-go/no-go, OQ-3 reconcile thực thi, redact/ max_steps xác nhận vị trí → **bàn giao** code thật `/frame`, backlog `/backlog` (GĐ9); rủi ro NFR chỉ nơi kiểm (GĐ12/Operate). Không mắt xích nào đứt: mọi ẩn số treo có địa chỉ.
