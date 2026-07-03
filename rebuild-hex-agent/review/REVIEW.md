# REVIEW — Rà soát gap thiết kế: HexAgent (clean rebuild)

> Skill `review` (L6+) · Chế độ **tổng thể** (edge → error → permission). Rà soát THIẾT KẾ vừa rebuild — đọc `05-idea-domain`, `06-shape`, `08-skeleton`, `10-modules` — đóng vai người cố tình phá.
> Anchor: `00-understanding/REBUILD-BRIEF.md` (7 invariant) + `evidence-A/B/C` (anchor `file:line` bản GỐC). Chỉ khẳng định điều evidence chống lưng; gap "nghi ngờ" gắn nhãn rõ.
> Chế độ tự-quyết: KHÔNG hỏi user. Ở cổng đóng vai **Reviewer (không tự duyệt phần mình viết)** — tự quyết GO/NO-GO, ghi rõ lý do + phương án đã loại.
> Phạm vi: thiết kế trên giấy (chưa có code — skeleton 0/9 tick). Review đọc để tìm LỖ HỔNG, không đọc để hiểu. Không đề xuất fix chi tiết code; mỗi gap Critical trỏ skill CÓ THẬT để build (`/frame`).

---

## ── GÓC NHÌN LÃNH ĐẠO (đọc trước, 90 giây — không cần biết code) ──

**Cái tôi tìm được, nói thẳng.** Thiết kế rebuild giữ đúng 7 invariant lõi và hai chokepoint — *xương sống chắc*. Nhưng khi tôi đóng vai kẻ phá, tôi tìm được **12 lỗ hổng** mà thiết kế **chưa đóng bằng chữ**: chỗ agent có thể **báo-xong-khống** vòng qua gate, chỗ **loop kẹt vô hạn** dù đã có guard, chỗ **secret rò ra log**, và chỗ **resume nửa-ghi** làm chạy-lại-gây-tác-dụng-phụ. Ba trong số đó là **Critical** — nếu để nguyên, đúng hai bệnh chết người mà cả sản phẩm này sinh ra để chữa (báo-xong-khống + chạy-vô-hạn/leo-quyền) vẫn *lọt được* qua khe hở.

**Ba điều Critical lãnh đạo phải biết (mỗi cái một câu).**
1. **Gate nghiệm-thu chống được evidence GIẢ, nhưng chưa chống được evidence THẬT-của-node-KHÁC.** Một AC có thể "pass" bằng cách trỏ tới `tool_result` có thật nhưng của việc khác — evidence là thật về *kiểu*, giả về *nội dung*. Đây chính là biến-thể tinh vi của báo-xong-khống mà `judge_acceptance` hiện chưa buộc kiểm.
2. **Guard chống chạy-vô-hạn đo ở tầng loop cha, không đo được sub-agent con.** Một node `blocked` bị đưa lại vào delegate mỗi round: mỗi round *có* tiến triển giả (child tạo artifact rác) → no-progress guard không bắt, budget cha còn → **kẹt vòng gần-vô-hạn** đốt tiền tới trần depth×steps.
3. **Redaction là điều-kiện chặn write-tool, nhưng thiết kế KHÔNG có cơ chế ép thứ tự đó.** Known gap gốc (`tool.requested` log raw args) được ghi thành "phải redact TRƯỚC khi bật write-tool" — nhưng không module nào *sở hữu việc enforce thứ tự này*. Nếu một team bật `fs_write` trước khi Observability bật redact → secret (API key trong args) rò vào `events.jsonl` vĩnh viễn (log append-only, không xoá được).

**Điều tôi KHÔNG tìm thấy gap (khớp — để lãnh đạo yên tâm).** Cấu trúc cây acyclic + μ co ngặt (chứng-minh-dừng decompose) là chắc; scope con⊆cha enforce 2 tầng là chắc; freeze-kernel + state-chỉ-ở-session (isolation) là chắc. Xương sống không gãy — vấn đề nằm ở các *khe hở giữa các chốt*, không phải ở chính các chốt.

**Đề nghị cổng.** GO cho việc *chuyển 3 gap Critical sang `/frame` đóng khung + đóng trong slice đầu* (chúng RẺ vì đều nằm trong slice "finish-by-evidence-tối-thiểu" GĐ8 đã định). KHÔNG chặn pipeline — nhưng **3 Critical là điều-kiện chặn "mở write-tool + mở delegation thật"** (khớp đúng quyết định GĐ13: alpha R1 chưa mở write/delegation).

---

## ── CHI TIẾT KỸ THUẬT (cho dev) ──

**PHẠM VI:** thiết kế rebuild HexAgent — vòng lặp plan→order→delegate→judge→finish + budget/resume/redaction, qua 4 artifact (05/06/08/10).
**CHẾ ĐỘ:** tổng thể (edge → error → permission).
**Trạng thái:** thiết-kế-trên-giấy; chưa có code (skeleton 0/9 tick). Gap = "thiết kế chưa nói cách xử lý", không phải "code sai".

Ký hiệu evidence mỗi gap: `neo bản GỐC (file:line)` = chỗ bản gốc CÓ/KHÔNG cơ chế · `artifact rebuild §` = chỗ thiết kế rebuild bỏ ngỏ.

---

## GAP TÌM ĐƯỢC

### 🔴 CRITICAL

---

**[Critical] G1 — Evidence THẬT-nhưng-của-node-KHÁC vượt gate (báo-xong-khống tinh vi).**
`judge_acceptance` · neo `evidence-A §4` (`graph.py:357-382`, `evidence.py:16-23`) · rebuild `05 §5.3 rule#1`, `06 §4 bước 5`, `10 Orchestration contract`.

- **Điều thiếu:** Gate kiểm evidence theo HAI thứ: (a) resolve được trên Blackboard, (b) **kiểu** là real (artifact/tool_result/…) không phải scaffolding. Gate KHÔNG kiểm **evidence đó có thực sự thuộc về AC đang chấm** hay không — tức không có ràng buộc "evidence_id phải được sinh bởi hành động phục vụ AC này / node này".
- **Kịch bản fail cụ thể:** Task có AC-1 "file `out.txt` chứa X" và AC-2 "file `len.txt` chứa len(X)". Worker chạy `fs_write out.txt` thành công → sinh `tool_result` E1 (thật). Worker của N2 fail/không chạy, nhưng O nộp `acceptance_status=[{id:AC-2, status:passed, evidence_ids:[E1]}]` — trỏ AC-2 vào E1 (evidence THẬT của AC-1). Gate thấy E1 resolve được ∧ kiểu `tool_result` (real) → **honor AC-2 passed** → `all_accepted()` true → **FINISHED sai** dù `len.txt` chưa từng được ghi.
- **Vì sao lọt:** thiết kế chống *scaffolding-as-evidence* nhưng không chống *cross-AC evidence reuse*. Rule#2 (worker không ghi verdict) không cứu được vì chính O (không phải worker) nộp mapping AC→evidence, và O đang tự-chấm (honor-system một phần — ADR-004 đã ghi rủi ro này nhưng CHƯA đóng ở tầng gate).
- **Mức:** Critical — phá thẳng M1 "zero false-finish", đúng bệnh sản phẩm sinh ra để chữa.
- **Gợi ý sửa (không code):** gate phải buộc mỗi `evidence_id` mang **provenance** (node_id/AC nó phục vụ, sinh từ tool call nào) và từ chối evidence có provenance ≠ AC đang chấm; hoặc tối thiểu 1 evidence phải sinh SAU khi node của AC đó active. Đóng khung bằng `/frame` (slice acceptance-provenance).

---

**[Critical] G2 — Node `blocked` re-delegate mỗi round với tiến-triển-GIẢ → kẹt vòng gần-vô-hạn, đốt tiền.**
loop guard + delegation · neo `evidence-A §4-5` (no-progress `loop.py:229-235`, `delegation/manager.py:63-192`) · rebuild `08 §1 (N2 depends N1)`, `06 §4 bước 4-6`, `05 §5.3`.

- **Điều thiếu:** no-progress guard trip khi *(artifacts không tăng ∧ acceptance không đổi ∧ không command)*. Guard đo ở **tầng loop CHA**. Nhưng mỗi delegate con CÓ THỂ tạo artifact mới (rác/không giúp AC) mỗi round → "artifacts tăng" → guard KHÔNG trip. Node vẫn `blocked` (worker fail K lần) nhưng loop cha thấy "có tiến triển" → tiếp tục delegate lại.
- **Kịch bản fail cụ thể:** N2 phụ thuộc N1; N1 done nhưng nội dung sai khiến N2 luôn fail. Mỗi round O lại delegate N2, worker con chạy `fs_write` tạo file tạm mới (artifact +1) rồi fail AC. artifacts tăng đều → no-progress guard không bao giờ trip; acceptance không đổi nhưng điều kiện AND cần CẢ BA → không đủ. repeat-decision guard chỉ trip nếu *chữ ký quyết định* lặp y hệt — nếu O đổi objective/wording mỗi lần thì chữ ký khác → không trip. → loop chạy tới `max_rounds` (trần), mỗi round tốn 1 delegation (tới `max_steps=100` × depth) → **đốt tiền tối đa** trước khi BLOCKED.
- **Vì sao lọt:** "tiến triển" định nghĩa bằng *artifacts tăng* — một proxy phá được. STUCK detection chỉ có ở **tầng decompose** (`accept.py`/`solve.py`), KHÔNG có ở **tầng task-loop**. Không có guard "cùng một node fail N round liên tiếp → BLOCKED node đó".
- **Mức:** Critical — phá M2 "bounded" ở nghĩa kinh tế (về terminal nhưng đốt gần-trần), đúng bệnh chạy-vô-hạn.
- **Gợi ý sửa:** thêm per-node stuck-counter ở task-loop (node xuất hiện trong ≥N round mà status vẫn blocked/không tiến AC → BLOCKED node, không re-delegate); hoặc gắn "tiến triển" vào *acceptance/coverage* thay vì *artifact count* thô. `/frame` slice loop-stuck-guard.

---

**[Critical] G3 — Không module nào SỞ HỮU việc ép "redact-raw-args bật TRƯỚC write-tool" → secret rò vào log append-only.**
Tools-Safety ↔ Control-Plane · neo `evidence-B §6` ("Known gap: `tool.requested` logs raw args to jsonl"), ADR-006 · rebuild `06 §6.4 (⚠️ known gap)`, `08 §5 (redact bật TRƯỚC ô 8)`, `10 Tools-Safety SLA/SLO` + `10 Control-Plane`.

- **Điều thiếu:** ADR-006 + `08 §5` + `10` đều GHI ràng buộc "redact raw args TRƯỚC khi bật write-tool", nhưng đây là ràng buộc **thứ-tự-thời-gian giữa hai team khác nhau** (Safety bật write-tool · Observability bật redact) mà KHÔNG có cơ chế enforce: không error code "WRITE_TOOL_ENABLED_WITHOUT_REDACTION", không invariant kiểm lúc freeze/bootstrap, không test chặn. Nó là *lời hứa điều-phối*, không phải *ranh giới cứng*.
- **Kịch bản fail cụ thể:** Team Safety (module Tools-Safety) bật `fs_write` cho một slice. Team Observability chưa merge Redactor cho path `tool.requested` (hoặc SECRET_KEYS chưa cover key mới). Worker gọi `fs_write(path, content)` với `content` chứa `Authorization: Bearer sk-...` (hoặc args LLM chứa API key). `execute_tool` publish `tool.requested` với raw args → EventLogger append vào `events.jsonl`. Vì log **append-only bất biến** (chính là invariant #3/§6.3) → secret nằm đó **vĩnh viễn**, không xoá được, và mọi ai đọc audit log thấy nó.
- **Vì sao lọt:** thiết kế coi đây là "known gap đã ghi" nên xem như đã xử lý — nhưng *ghi ra risk ≠ đóng risk*. Hai team, không owner chung cho thứ tự → race tổ chức. Slice GĐ8 dùng `fs_write` (write-tool) chính là chỗ đầu tiên chạm gap này.
- **Mức:** Critical — rò secret vào audit log bất biến = security breach không-thu-hồi-được; là chính invariant #7 (redact tại biên) bị vượt.
- **Gợi ý sửa:** biến thành ranh giới cứng — registry/bootstrap từ chối freeze nếu có write-capability nào enabled mà Redactor chưa active cho `tool.requested` (fail-closed at freeze); error `WRITE_TOOL_ENABLED_WITHOUT_REDACTION`; audit-test bắt buộc. Gán owner rõ (đề xuất: Execution-Core, vì nó là nơi freeze + là nơi phát `tool.requested`). `/frame` slice redact-before-write-gate.

---

### 🟠 HIGH

---

**[High] G4 — AC không bao giờ satisfiable → task treo tới max_rounds thay vì fail nhanh; không phân biệt "chưa xong" vs "không thể xong".**
acceptance + loop · neo `evidence-A §4` (`all_accepted`, guards) · rebuild `05 §5.3 rule#1`, `06 §4 bước 6`.

- **Điều thiếu:** Nếu một AC được viết sai/không-thể-thoả (vd `done_when` trỏ artifact không hành động nào sinh ra được, hoặc criterion mâu thuẫn), `all_accepted()` không bao giờ true. Thiết kế chỉ dừng bằng guard *đếm* (max_rounds/no-progress) — không có phát hiện "AC vô nghiệm" sớm. Task tiêu tốn tới trần rồi BLOCKED, và lý do BLOCKED là "hết round" chứ không phải "AC không satisfiable" → chẩn đoán sai.
- **Kịch bản fail:** AC "file `report.pdf` tồn tại" nhưng scope worker chỉ có `fs_write .txt` (deny .pdf), hoặc AC yêu cầu `terminal_run` mà node không được cấp cap đó. Worker không bao giờ sinh evidence hợp lệ → loop chạy hết max_rounds → BLOCKED "max_rounds" (che giấu nguyên nhân thật = mismatch AC↔capability).
- **Mức:** High — không mất data, không breach, nhưng đốt trần budget + báo lỗi sai loại làm khó vận hành (OQ-1 baseline sẽ nhiễu).
- **Gợi ý sửa:** static pre-check khi accept plan: mỗi AC/`done_when` phải có ≥1 capability trong scope có thể sinh evidence kiểu tương ứng; nếu không → BLOCKED sớm với `ACCEPTANCE_UNSATISFIABLE`. Bàn `/frame`.

---

**[High] G5 — Child crash / timeout: thiết kế nói merge artifact khi success, KHÔNG nói parent xử lý gì khi child raise/treo.**
delegation · neo `evidence-A §3` (`delegate() [63-192]`: validate→run→merge→close), `DelegationResult.outcome∈{success,rejected,failed}` (`evidence-A §7`) · rebuild `06 §4 bước 4`, `10 Orchestration/Execution-Core contract`.

- **Điều thiếu:** `08 §2`/`06 §4` mô tả đường HAPPY: child chạy → merge artifact → đóng child. `DelegationResult.outcome` CÓ giá trị `failed`, nhưng thiết kế rebuild KHÔNG mô tả: (a) child **timeout** (không trả trong biên) thì ai cắt, đóng session con thế nào; (b) child **raise exception** giữa chừng — có chắc child session được close (không leak session/state)? (c) partial artifact khi child fail giữa merge — có nửa-merge vào parent Blackboard không? Contract Orchestration liệt kê error code delegation (`DELEGATION_SCOPE_EXCEEDS_PARENT`, `DELEGATION_DEPTH_EXCEEDED`) nhưng KHÔNG có `DELEGATION_CHILD_TIMEOUT` / `DELEGATION_CHILD_CRASHED`.
- **Kịch bản fail:** Worker con gọi LLM, provider treo > timeout. Không có per-delegation wall-clock timeout mô tả (chỉ có `max_steps` — đếm bước, không đếm thời gian). Child treo → parent `delegate()` block vô hạn → cả task-loop cha đứng (không tới được checkpoint/guard nào vì đang kẹt trong lời gọi đồng bộ). → task treo THẬT (không phải bounded).
- **Vì sao lọt:** budget là *step-count*, không *wall-clock*; guard loop cha chỉ chạy GIỮA các round, không cứu được kẹt TRONG một round (trong `delegate()`).
- **Mức:** High — treo thật (phá M2) nếu LLM/tool con treo; cũng có nguy cơ leak child session.
- **Gợi ý sửa:** delegation policy cần wall-clock timeout + `try/finally` đóng child session bất kể outcome; `failed` outcome phải rollback partial merge (transaction hoặc all-or-nothing merge); thêm error code timeout/crashed. `/frame` slice delegation-failure-path.

---

**[High] G6 — Checkpoint nửa-ghi khi crash GIỮA round (giữa apply-commands và save) — atomic-txn chỉ đóng phần cuối, không đóng công-việc-đã-làm-nhưng-chưa-save.**
resume · neo `evidence-A §6` (atomic txn `loop.py:208-218`: commands+round+save một transaction), `evidence-B §7` (SQLite=truth) · rebuild `05 §5.3 nền`, `06 ADR-005`, `08 ô#5 SPIKE-1`.

- **Điều thiếu:** Thiết kế đảm bảo *commands+round_no+save() trong MỘT transaction* → checkpoint không nửa-ghi. Nhưng câu hỏi review: **những side-effect đã xảy ra TRONG round trước khi tới transaction cuối** (tool đã chạy thật, file đã ghi ra `var/workspace/`, event đã emit vào jsonl) — nếu crash SAU khi tool chạy nhưng TRƯỚC khi save → resume từ checkpoint CŨ sẽ **chạy LẠI tool đó** (re-emit `tool.requested`, ghi lại file). SPIKE-1 (ô#5) đúng là để đo cái này, nhưng thiết kế CHƯA có cơ chế idempotency cho tool-side-effect, chỉ có idempotency cho *command* (`idempotency_key`, `evidence-A §6`).
- **Kịch bản fail:** N1 chạy `fs_write out.txt` (side-effect ra disk + emit tool.requested). Crash trước `ctx.save`. Resume từ checkpoint trước N1 → N1 chạy lại → out.txt ghi đè (ở đây idempotent tình cờ), nhưng event log có **hai** `tool.requested` cho cùng logical step → vi phạm SPIKE-1 tiêu chí (a) "không re-emit tool.requested của N1" + seq vẫn gap-free nhưng có bản-ghi-đúp → replay=snapshot có thể lệch. Nếu tool KHÔNG idempotent (vd `fs_append`, gọi API tính phí) → tác-dụng-phụ nhân đôi.
- **Vì sao lọt:** atomic-txn bảo vệ *state checkpoint*, không bảo vệ *tool side-effect* đã phát ra ngoài trước checkpoint. Idempotency chỉ áp cho command, không áp cho tool execution.
- **Mức:** High — SPIKE-1 gọi tên đúng ẩn số này; nếu không đóng, resume gây re-run side-effect (đúng thứ ADR-005 hứa chống).
- **Gợi ý sửa:** hoặc (a) checkpoint per-step (save NGAY sau mỗi execute_tool thành công, trước side-effect kế), hoặc (b) tool-call idempotency key (step_id) để resume skip step đã completed trong event log. Đây LÀ SPIKE-1 — `/frame` chạy đo + đóng theo tiêu chí a/b/c của `08 ô#5`.

---

**[High] G7 — `reduce` node gom sai sibling: thiết kế nêu op merge nhưng không nói ràng buộc "chỉ gom đúng con của cùng parent".**
decompose/reduce · neo `evidence-A §2` (`solve_reduce() [204-224]`, `run_reduce()` ops merge_json/pick/concat/manifest; synthetic reduce node `[187-201]`) · rebuild `08 §1 (N_reduce synthetic)`, `05 §5.4 PlanDecomposed`.

- **Điều thiếu:** reduce node "gom artifact các node con → AC gốc". Thiết kế không nêu ràng buộc reduce **chỉ** được gom artifact của **đúng tập con trực tiếp của parent nó** — nếu op `merge_json`/`concat` nhận danh sách source_ids do worker/O đề xuất, một reduce có thể vô tình (hoặc do prompt injection qua LLM) gom artifact của **sibling khác nhánh** hoặc node chưa done → tổng hợp sai/rò dữ liệu chéo nhánh.
- **Kịch bản fail:** Cây có parent P với con {A, B} và nhánh khác Q với con {C}. reduce của P nhận source_ids = [artifact_A, artifact_C] (C thuộc nhánh Q). Nếu không kiểm "source ⊆ children(P)" → reduce gom nhầm C vào kết quả P → AC gốc của P "pass" bằng dữ liệu không thuộc P.
- **Mức:** High — sai kết quả tổng hợp (không crash), có thể là đường phụ của G1 (evidence lẫn lộn giữa node).
- **Gợi ý sửa:** `run_reduce` phải validate mọi source_id ∈ artifacts của `children(parent)` đã done; reject nếu có source ngoài tập. `/frame` khi build reduce.

---

**[High] G8 — RENAME (Jaccard>0.80) / STUCK detection: ngưỡng cứng 0.80 có khe né; đồng nghĩa-khác-từ vượt được.**
decompose gate-2 · neo `evidence-A §2` (`accept.py:52-128`, RENAME Jaccard>0.80 `[165]`, STUCK) · rebuild `08 chặng#3`, `05 §5.3 rule#4`, `10 error PLAN_RENAME_DETECTED`.

- **Điều thiếu:** RENAME detect bằng Jaccard token-overlap > 0.80 giữa done_when cha và con. Đây là chống "chia giả" (con = cha đổi tên). Nhưng Jaccard là **lexical**, phá được: worker paraphrase criterion bằng từ đồng nghĩa (đổi "tạo file" → "sinh tài liệu", "kiểm tra" → "xác minh") → token overlap < 0.80 dù nghĩa y hệt → **RENAME không bị bắt** → μ *hình thức* co ngặt (len(done_when) giảm) nhưng *ngữ nghĩa* không → cây phình mà không thật sự tiến gần done. STUCK detection dựa trên gì thì rebuild không nêu rõ (chỉ nói "detects STUCK") → không đánh giá được đủ hay chưa.
- **Kịch bản fail:** cha done_when=["file X tồn tại và đúng nội dung"]. worker decompose thành con=["tài liệu X được sinh ra ở đường dẫn đúng", "nội dung tài liệu X khớp yêu cầu"] — nghĩa trùng cha, chia giả, nhưng Jaccard thấp (từ khác) → gate PASS → cây sâu thêm vô ích, tiêu MAX_DEPTH=6 nhanh hơn, mỗi tầng tốn budget.
- **Mức:** High — làm yếu chứng-minh-dừng ở tầng ngữ nghĩa; kết hợp G2 làm tăng đốt tiền. (⚠️ một phần là "có thể là gap": hiệu quả tuỳ prompt worker — xem phần "CÓ THỂ LÀ GAP" nếu muốn đào.)
- **Gợi ý sửa:** bổ sung tín hiệu ngữ nghĩa (embedding-similarity) song song Jaccard, hoặc buộc coverage-by-implication chặt hơn (mỗi con phải map tới ⊆ criteria cha đo được, không chỉ giảm count). Ghi rõ STUCK detection dùng tiêu chí gì. `/frame` khi build gate-2.

---

### 🟡 MEDIUM

---

**[Med] G9 — Scope escalation qua re-delegation depth: mỗi tầng con ⊆ cha, nhưng KHÔNG cấm con GIỮ NGUYÊN toàn bộ scope cha qua nhiều tầng → deep chain vẫn full-scope.**
delegation policy · neo `evidence-A §3` (scope⊆parent `policy.py:25-26`), `05 §5.3 rule#3` · rebuild `06 §6.2`, `10 Orchestration permission`.

- **Điều thiếu:** Bất biến là con ⊆ cha (⊆ cho phép BẰNG). Không có yêu cầu scope **thu hẹp thật** theo độ sâu. Một chuỗi delegate depth 8, mỗi tầng con = cha (⊆ thoả vì bằng) → tầng lá vẫn giữ **toàn bộ** capability gốc. Không phải leo-thang (không vượt cha) nhưng là **không-thu-hẹp** — trái tinh thần least-privilege mà "scope-shrink" (`session.py:163`) gợi ý. Broker "không mở scope" nhưng cũng không buộc thu hẹp.
- **Kịch bản fail:** O giao task với scope {fs_read, fs_write, terminal_run}. Delegate 8 tầng, mỗi tầng truyền nguyên scope. Một worker lá (đáng ra chỉ cần fs_read) vẫn có terminal_run → bề mặt tấn công rộng ở tầng sâu nhất, nơi khó audit nhất.
- **Mức:** Med — không phá invariant (vẫn ⊆), nhưng là lỗ least-privilege; kết hợp bug tool có thể thành đường thật.
- **Gợi ý sửa:** khuyến nghị (không cứng): O nên đặt allowed_capabilities per-assignment tối thiểu theo objective; hoặc cảnh báo audit khi scope con == cha ở depth>threshold. Ghi thành policy, không nhất thiết block.

---

**[Med] G10 — parse-error budget "CONSECUTIVE, reset on good parse": kẻ phá xen 1 good parse mỗi N lỗi để không bao giờ cạn budget.**
budget · neo `evidence-A §5` (`Budget`: max_parse_errors CONSECUTIVE, resets on good parse, `budget.py:10-67`) · rebuild `10 Discipline (max_parse_errors CONSECUTIVE)`, `06 Reliability`.

- **Điều thiếu:** parse-error budget đếm **liên tiếp**, reset khi có 1 good parse. Thiết kế coi đây là tính năng (bỏ qua lỗi thoáng qua). Nhưng nó phá được: LLM trả 4 lỗi rồi 1 JSON hợp lệ-nhưng-vô-nghĩa (parse OK, quyết định rỗng/lặp) → reset counter → lặp mãi. Budget CONSECUTIVE không bao giờ cạn dù tỉ lệ lỗi ~80%.
- **Kịch bản fail:** với `max_parse_errors=8` consecutive, một luồng LLM hỏng đều "7 fail + 1 trivial-pass" lặp lại → không bao giờ đạt 8 liên tiếp → parse-budget guard không FAILED. Phải dựa vào max_rounds/no-progress cứu — nhưng nếu decision hợp lệ đổi chữ ký mỗi lần (xem G2) thì cũng né repeat-guard.
- **Mức:** Med — có backstop (max_rounds), nhưng làm parse-budget vô dụng như một guard độc lập; tương tác với G2 kéo dài loop.
- **Gợi ý sửa:** thêm total-parse-error budget (không reset) song song với consecutive; hoặc reset chỉ khi good-parse KÈM tiến-triển-thật (không phải mọi parse hợp lệ). `/frame` khi build Budget.

---

**[Med] G11 — seq monotonic "per-run": resume cross-process có reset/đụng seq không? Thiết kế khẳng định gap-free nhưng nguồn seq khi restore chưa nêu.**
observability/resume · neo `evidence-B §2` (`SessionSeq` per-session monotonic, RLock, start 1), `evidence-B §7 (ii)` (seq monotonic gap-free per run) · rebuild `10 Control-Plane SLA (seq gap-free per-run)`, `08 ô#8`.

- **Điều thiếu:** `SessionSeq` start ở 1, giữ trong RLock **trong tiến trình**. Khi **resume ở tiến trình MỚI** (crash rồi khởi động lại), seq counter phải tiếp tục từ giá trị đã lưu, KHÔNG reset về 1. Thiết kế không nêu seq được persist/khôi phục ở đâu khi restore (state serializable-only — seq counter có nằm trong serialized state không?). Nếu reset về 1 → event sau-resume có seq đụng event trước-resume → **EVENT_SEQ_GAP / duplicate seq** → replay=snapshot vỡ (invariant (ii)/(v)).
- **Kịch bản fail:** run tới seq=42, crash. Resume tiến trình mới, SessionSeq khởi tạo start=1 → event tiếp theo seq=1 (đụng). Error code `EVENT_SEQ_GAP` (contract Control-Plane) trip HOẶC tệ hơn im lặng ghi đè → audit log hỏng.
- **Mức:** Med — audit/replay integrity, không mất data nghiệp vụ; SPIKE-1 chạm gần (resume) nên đo được cùng lúc.
- **Gợi ý sửa:** seq high-watermark phải persist trong checkpoint và restore trước khi emit event đầu tiên sau resume; test: resume rồi kiểm seq tiếp tục tăng không đụng. Gộp vào SPIKE-1 `/frame`.

---

**[Med] G12 — Cycle qua depends_on được đề xuất SAU khi cây đã có: gate-2 kiểm μ↓ mỗi lần chia, nhưng thêm DependencyEdge có kiểm acyclic mỗi lần thêm không?**
plan/decompose · neo `evidence-A §2` (forest+DAG "both acyclic" `[63-121]`, `next_node` topo) · rebuild `05 §5.2 DependencyEdge (acyclic, cố định sau khi đặt)`, `08 chặng#4`.

- **Điều thiếu:** Thiết kế khẳng định DAG acyclic và edge "cố định sau khi đặt". Nhưng gate-2 `accept_decomposition` là gate **cấu trúc cho decompose (thêm CON)** — μ(node)=len(done_when). Việc **thêm `depends_on` edge** giữa các node đã tồn tại (không thêm con) có đi qua kiểm acyclic không, hay chỉ dựa vào giả định "chỉ đặt lúc tạo"? Nếu O/worker được phép khai depends_on tự do mỗi round mà không có acyclic-check độc lập → có thể tạo cycle A→B→A → `next_node()` (topo) không tìm được node nào deps-all-done → **không node nào chạy được** → loop no-progress → BLOCKED (may mắn bounded), nhưng lý do che giấu (thực chất là cycle, báo là no-progress).
- **Kịch bản fail:** round 3 O đề xuất thêm edge N1.depends_on=[N2] trong khi N2.depends_on=[N1] đã có → cycle. `next_node()` trả None (không node nào sẵn sàng) → no-progress → BLOCKED "no-progress" thay vì "cycle detected".
- **Mức:** Med — bounded (không treo vô hạn nhờ no-progress backstop) nhưng chẩn đoán sai + phí round; nếu topo-sort giả định acyclic mà không kiểm có thể crash/loop tuỳ hiện thực.
- **Gợi ý sửa:** mỗi lần thêm/đổi depends_on phải chạy acyclic-check độc lập (không chỉ lúc tạo cây); error `PLAN_DEPENDENCY_CYCLE` rõ ràng thay vì để rơi vào no-progress. `/frame` khi build Tree mutation.

---

## CÓ THỂ LÀ GAP (chưa chắc — cần xác nhận khi có code)

- **G8-phụ (STUCK detection tiêu chí):** rebuild chỉ ghi "detects STUCK" mà không nêu định nghĩa STUCK ở tầng decompose. Cần đọc code `accept.py` thật (chưa có ở rebuild) để biết đủ hay không. *Câu hỏi:* STUCK = μ không giảm sau N attempt, hay = cùng decomposition đề xuất lặp? Nếu chỉ cái sau thì né được bằng đổi wording (như G8).
- **Condense mất evidence-id:** `condense.run` nén context khi vượt ngưỡng (`10 Discipline`). *Nghi ngờ:* nén có thể bỏ mất reference tới evidence_id cần cho judge sau đó → AC đúng-ra-pass thành thiếu-evidence (false BLOCKED). Cần xác nhận condense có bảo toàn evidence-id/artifact-ref không. *Chưa đủ chứng cứ trong artifact để khẳng định.*
- **`immediate_if_waiting` command khi KHÔNG có trạng thái waiting rõ:** command apply_at có `immediate_if_waiting` (`evidence-B §3`). *Nghi ngờ:* nếu loop không có khái niệm "waiting" tường minh ở rebuild (chưa mô tả state machine waiting), command loại này áp lúc nào? Có thể bị nuốt (không bao giờ waiting) hoặc áp sai thời điểm. Cần state-machine chi tiết (chưa có).

## KHÔNG TÌM THẤY GAP (đã soi, thấy ổn)

- **Cấu trúc cây acyclic lúc TẠO + μ co ngặt khi chia:** chứng-minh-dừng decompose (μ(node)=len(done_when) co ngặt mỗi lần accept) là chặt cho trường hợp thêm-con. (Gap chỉ ở thêm-edge-sau — G12, và ngữ nghĩa RENAME — G8.)
- **Scope con ⊆ cha (không leo-thang QUYỀN):** enforce 2 tầng (delegation policy + SessionFactory scope-shrink), fail-closed — không tìm được đường con VƯỢT cha. (Gap chỉ ở không-thu-hẹp — G9, mức Med.)
- **Isolation state giữa run:** freeze-kernel + state-chỉ-ở-session + deep-copy → không tìm được đường rò state cross-run. Chắc.
- **Scaffolding-as-evidence:** phân loại real vs scaffolding (`evidence.py:16-23`) chặn đúng session_plan/context_packet/ac_report. Chắc — gap G1 là *cross-AC reuse của evidence THẬT*, một trục khác.
- **Chokepoint đơn `execute_tool`:** mọi hành động một cửa; audit-test "0 call site bỏ qua" đóng đường vòng. Chắc (với điều kiện audit-test được viết — thuộc delivery).

---

## Bảng tổng hợp (scan nhanh)

| # | Mức | Trục | Điều thiếu (1 dòng) | Đóng ở đâu |
|---|---|---|---|---|
| G1 | 🔴 Critical | acceptance | evidence THẬT của node KHÁC vượt gate (cross-AC reuse) | `/frame` slice acceptance-provenance |
| G2 | 🔴 Critical | loop/budget | node blocked re-delegate + artifact-rác né no-progress → kẹt gần-vô-hạn | `/frame` slice loop-stuck-guard |
| G3 | 🔴 Critical | permission/redaction | không owner ép redact-TRƯỚC-write-tool → secret rò log bất biến | `/frame` slice redact-before-write-gate |
| G4 | 🟠 High | acceptance | AC vô nghiệm → treo tới max_rounds, báo sai loại | `/frame` (pre-check satisfiable) |
| G5 | 🟠 High | delegation/error | child crash/timeout: parent xử lý chưa mô tả; không wall-clock timeout | `/frame` slice delegation-failure-path |
| G6 | 🟠 High | resume | crash sau tool-side-effect trước save → re-run side-effect (SPIKE-1) | `/frame` (đo SPIKE-1) |
| G7 | 🟠 High | reduce | reduce gom sai sibling ngoài children(parent) | `/frame` khi build reduce |
| G8 | 🟠 High | decompose | RENAME Jaccard lexical → đồng-nghĩa-khác-từ né được | `/frame` khi build gate-2 |
| G9 | 🟡 Med | permission | scope không-thu-hẹp qua depth (⊆ nhưng ==) → lá full-scope | policy/audit-warn |
| G10 | 🟡 Med | budget | parse-budget CONSECUTIVE reset → xen good-parse né cạn | `/frame` khi build Budget |
| G11 | 🟡 Med | observability/resume | seq per-run reset khi resume cross-process → đụng seq | gộp SPIKE-1 |
| G12 | 🟡 Med | plan | thêm depends_on-edge sau có kiểm acyclic độc lập không → cycle | `/frame` khi build Tree mutation |

---

## Cổng REVIEW (tự-quyết — đóng vai Reviewer, KHÔNG tự duyệt phần mình viết)

**Câu hỏi cổng:** *"Thiết kế còn lỗ hổng nào chặn việc mở write-tool + delegation thật không?"*

**Trình bằng chứng (Reviewer):** soi 3 trục (edge/error/permission) trên 4 artifact thiết kế · tìm 12 gap có evidence (3 Critical / 5 High / 4 Med) + 3 "có-thể-là-gap" · phân biệt rõ gap-thật vs nghi-ngờ · mỗi Critical trỏ `/frame` (skill có thật) để đóng.

```
═══ CỔNG REVIEW — HexAgent (clean rebuild) ═══
Đã soi: plan/decompose · acceptance · delegation · budget · resume · redaction (đúng 6 mục nhiệm vụ).
Kết quả: 12 gap (3 Critical: G1 cross-AC-evidence · G2 loop-stuck-đốt-tiền · G3 redact-before-write) + 3 nghi-ngờ.
Xương sống (acyclic+μ↓ · scope⊆parent · isolation · scaffolding-reject · 1-chokepoint): KHÔNG gãy.
3 Critical đều RẺ để đóng — nằm gọn trong slice "finish-by-evidence-tối-thiểu" (GĐ8) qua /frame.
Ràng buộc: 3 Critical = điều-kiện chặn "mở write-tool + delegation thật" (khớp GĐ13: alpha R1 chưa mở write/delegation).
Câu hỏi cổng: Thiết kế đủ an toàn để mở write/delegation chưa?
════════════════
```

**GATE: NO-GO cho "mở write-tool + delegation thật ngay" · GO cho "đóng 3 Critical trong slice đầu qua /frame rồi mở dần".**

- **Lý do NO-GO (mở write/delegation ngay):** G3 (secret rò log bất biến) + G1 (false-finish tinh vi) + G2 (đốt tiền) đều lọt đúng khi write-tool/delegation *thật* được bật. Bật trước khi đóng = mở đúng ba khe hở dẫn tới hai bệnh chết người. Đây KHÔNG phải "thiết kế hỏng" — xương sống chắc — mà là *ba khe hở giữa các chốt chưa được bịt bằng cơ chế cứng*.
- **Lý do GO (đóng-rồi-mở-dần):** cả 3 Critical nằm trong slice GĐ8 đã định (dùng `fs_write` = write-tool, dùng delegate 1 worker, dùng judge-by-evidence) → đóng chúng KHÔNG thêm slice mới, chỉ thêm ràng buộc vào slice đang dựng. Khớp đúng rollout GĐ13 (alpha → pilot write-flag → beta delegation-flag): 3 Critical là **điều-kiện xanh của cổng pilot/beta đó**.
- **Phương án đã loại:**
  - (a) *Chặn cả pipeline tới khi đóng hết 12 gap* — loại: 5 High + 4 Med không chặn nền R1 alpha (read-only, chưa write/delegation); chặn hết = trái Đủ-là-đủ + trái quyết định GĐ13 đã GO alpha. Mang High/Med vào backlog vòng kế (I-1/I-3 của operate.json).
  - (b) *Tuyên GO đầy đủ vì "xương sống chắc"* — loại: xương sống chắc KHÔNG có nghĩa khe hở an toàn; G3 rò secret là không-thu-hồi-được, không được nuốt.
  - (c) *Tự-đóng gap trong review (viết fix)* — loại: skill review "không đề xuất fix chi tiết — fix là việc của /frame" (SKILL.md Quy tắc); review báo cáo trung thực + trỏ skill có thật, không lấn vai build.

**Bàn giao gap Critical → `/frame` (skill CÓ THẬT):**
- G1 → `/frame` slice **acceptance-provenance** (evidence phải mang node_id/AC-nguồn; gate reject cross-AC).
- G2 → `/frame` slice **loop-stuck-guard** (per-node stuck-counter ở task-loop; "tiến triển" gắn acceptance/coverage không phải artifact-count).
- G3 → `/frame` slice **redact-before-write-gate** (freeze fail-closed nếu write-cap enabled mà Redactor chưa active cho tool.requested; owner = Execution-Core; audit-test bắt buộc).

---

## Bàn giao

```
═══ BÀN GIAO — REVIEW: HexAgent (clean rebuild) ═══
Đã soi   : 4 artifact thiết kế (05/06/08/10) qua 3 trục (edge/error/permission), đúng 6 mục nhiệm vụ
           (plan/decompose · acceptance · delegation · budget · resume · redaction).
Kết quả  : 12 gap (3 Critical · 5 High · 4 Med) + 3 nghi-ngờ + 5 vùng-ổn. Xương sống 7-invariant KHÔNG gãy.
Critical : G1 cross-AC-evidence (false-finish tinh vi) · G2 loop-stuck (đốt tiền) · G3 redact-before-write (rò secret log).
Cổng     : NO-GO mở write/delegation NGAY · GO đóng 3 Critical trong slice đầu qua /frame rồi mở dần (khớp rollout GĐ13).
Artifact : rebuild-hex-agent/review/REVIEW.md (+ state rebuild-hex-agent/pipeline/_review.json)
→ Đóng 3 gap Critical (mỗi cái một slice): chạy /frame (acceptance-provenance · loop-stuck-guard · redact-before-write-gate)
→ 5 High + 4 Med: mang vào backlog vòng kế (khớp operate.json I-1/I-3): chạy /backlog
→ Đo SPIKE-1 (G6 resume side-effect + G11 seq) chung một lần: chạy /frame slice resume
→ Cần điều phối toàn pipeline / kiểm mắt xích: chạy /partner hoặc /traceability
════════════════
```

*Traceability:* REVIEW (L6+) nhận thiết kế đã-qua-cổng GĐ5/6/8/10 → soi tìm gap (KHÔNG làm lại việc stage khác) → 3 Critical bàn giao `/frame` (build), High/Med bàn giao `/backlog` (vòng kế). Khớp quyết định thượng nguồn: alpha R1 chưa mở write/delegation (GĐ13 ship.json) → 3 Critical đúng là điều-kiện-xanh của cổng pilot/beta. Không mắt xích đứt: mọi gap có địa chỉ đóng.
