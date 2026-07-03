CHẤM: 05-idea · /Users/uspro/Desktop/skillsh/rebuild-hex-agent/pipeline/05-idea-domain.md

1. [0] — Đa số anchor đúng (state/kernel/graph/policy/node/tree khớp code), NHƯNG hằng số SAI so với code gốc: "15 SECRET_KEYS" (line 101) trong khi `control/redaction.py:16-33` có ĐÚNG 14 key (`len(SECRET_KEYS)==14`) — rubric mức 0 kích hoạt khi "hằng số sai so với code gốc".
2. [2] — Router phân cả hai trục kèm căn cứ ("rõ ràng" + "khả thi rõ" → Nhánh C, line 27-28); đủ 4 khối GĐ0/1/2-4/5; mỗi cổng ghi GO + lý do + vai tự-quyết (Product/CTO, line 50/114/194).
3. [2] — Ai đau (internal platform team/builder) + 2 pain; chi phí-nếu-không-làm gắn nhãn "ước lượng thô" + OQ-1 (line 39-41); M1 zero-false-finish kèm oracle kiểm được `all_accepted()` (line 44).
4. [2] — MVP một câu (line 69) đo bằng M1; journey AS-IS→TO-BE (line 63-65); OUT liệt kê từng mục thành chữ (line 89-94); mỗi open-Q ghi chỗ chốt (OQ-1→Operate, OQ-2/3→shape).
5. [2] — Đủ 5 mắt xích: 6 bounded context → entity có identity+lifecycle (VALID_STATUSES `node.py:28` khớp) → 5 rule bất biến + ai enforce → 6 event có thời điểm phát → data ownership mỗi khối một chủ; chủ động bác "Node như bảng DB".
6. [2] — Dừng đúng GĐ5, đẩy kiến trúc/framework/DB thành open-Q/park-with-trigger (line 17/197); không tự kill; khối bàn giao liệt kê ≥3 lối đi (shape/stack · frame · explain) để người nhận tự quyết.
7. [2] — GĐ1 chỉ bàn pain/metric; NFR/số kỹ thuật ở GĐ2-4 đúng chỗ; GĐ5 chỉ ranh giới domain; thứ thuộc GĐ6 (danh mục event, reconcile tên) đẩy thành OQ-2/OQ-3 sang shape, không trả lời non.
8. [2] — Mỗi cổng lớn có lý do + ≥1 phương án đã loại kèm mất-gì: loại single-agent bỏ delegation (mất lõi P3), loại full-UI-ngay, loại gộp Discipline vào Execution Core (coupling).

TỔNG: 14/16
GATE: rớt: tiêu chí 1 (BẰNG CHỨNG, xương sống) = 0 vì hằng số "15 SECRET_KEYS" sai so với code gốc (thực 14) — `shape` sẽ mang tiếp con số giả nếu không sửa.
SỬA TRƯỚC TIÊN: Sửa "15 SECRET_KEYS"→14 (`control/redaction.py:16-33`) VÀ sửa upstream `ATLAS.md:194,234` + `evidence-B:18,39` (nguồn gốc lỗi lan xuống); nhân tiện trỏ lại anchor `accept.py:52-128`→`decompose_agent/accept.py:186+` cho `accept_decomposition`.

---

## Bảng tiêu chí × 3 lens + phân xử

| # | Tiêu chí (xương sống*) | ky-thuat | business | thi-cong | TRỌNG TÀI | Ghi chú phân xử |
|---|---|---|---|---|---|---|
| 1 | BẰNG CHỨNG* | 0 | 1 | 2 | **0** | Bất đồng lớn nhất. Tự kiểm: `len(SECRET_KEYS)==14`, artifact ghi 15 → hằng số sai so code → mức 0 theo rubric. thi-cong chấm 2 và còn viết "15 SECRET_KEYS đếm đúng" — SAI, không thực đếm. Giữ điểm thấp nhất (0). |
| 2 | ĐỦ CHUỖI GĐ0–5 | 2 | 2 | 2 | **2** | Đồng thuận. |
| 3 | GĐ1 WHY bằng số | 2 | 2 | 2 | **2** | Đồng thuận. |
| 4 | GĐ2–4 MVP/OUT/open-Q | 2 | 2 | 2 | **2** | Đồng thuận. |
| 5 | GĐ5 Domain 5 mắt xích* | 2 | 2 | 2 | **2** | Đồng thuận; kiểm chéo `node.py:20/28`, policy/kernel/graph anchor đều đúng. |
| 6 | DỪNG ĐÚNG VAI* | 2 | 2 | 2 | **2** | Đồng thuận; SQLite/langgraph chỉ là tham chiếu hiện-trạng bản gốc (rubric cho phép), không tự chốt stack. |
| 7 | ĐÚNG TẦNG | 2 | 2 | 2 | **2** | Đồng thuận. |
| 8 | AUDIT ĐƯỢC | 2 | 2 | 2 | **2** | Đồng thuận. |
| | **TỔNG** | 14 | 15 | 16 | **14** | |

### Các bất đồng đáng chú ý và cách phân xử

1. **Tiêu chí 1: 0 vs 1 vs 2 — quyết định cả gate.**
   - ky-thuat (0): bắt "15 SECRET_KEYS" sai vs code 14 key → gate 0.
   - business (1): mọi claim khác đúng nhưng 2 số (15 SECRET_KEYS, 327 tests) đưa như số thật không hedge → chưa tới 2, nhưng không hạ tới 0.
   - thi-cong (2): tuyên bố "15 SECRET_KEYS đếm đúng" — sai sự thật.
   - **Phân xử: giữ 0.** Tự mở `control/redaction.py:16-33`, chạy `len(SECRET_KEYS)` = 14 (danh sách: api_key, apikey, authorization, password, passwd, secret, secret_key, client_secret, token, access_token, refresh_token, private_key, set-cookie, cookie). Artifact ghi 15 → đúng định nghĩa mức-0 của rubric ("hằng số... sai so với code gốc"). thi-cong chấm 2 dựa trên khẳng định đếm sai; business chấm 1 là khoan dung với "hằng số sai" mà rubric quy về mức 0. Luật lấy điểm thấp nhất được giữ vì lens thấp (ky-thuat) đã được xác minh ĐÚNG.

2. **Anchor `accept.py:52-128` cho `accept_decomposition`.** ky-thuat gọi là "trỏ sai chỗ"; thi-cong lại dùng `accept.py:52-53,22` cho μ/JACCARD và chấm bằng-chứng 2. Tự kiểm `decompose_agent/accept.py`: `accept_decomposition` thực ở **line 186**; line 52 là `mu()`, 57-78 là `Accept`/`Reject`, 101 là `_implies`, 22 là `JACCARD_MAX=0.80`. Vậy KHI artifact (line 72, 160) dán nhãn "`accept.py:52-128`" cho cổng `accept_decomposition` là anchor lệch (cơ chế μ co ngặt + Jaccard vẫn tồn tại thật, nhưng số dòng trỏ sai construct). Đây là điểm trừ thêm cho tiêu chí 1 nhưng không đổi kết luận (đã 0).

3. **"327 tests" (line 28).** business đếm 308 file/1041 hàm; thi-cong đếm 84 file/1041 hàm; đếm độc lập của trọng tài: **307 file `test_*.py`, 3795 hàm `def test_`**. Cả ba con số các lens đưa ra đều lệch nhau và lệch thực tế — chứng tỏ "327" là số cũ/khác-phạm-vi (trace về `evidence-C`/docs-roadmap), KHÔNG khớp code. Là dấu hiệu số kế thừa chưa kiểm; củng cố việc tiêu chí 1 chưa đạt 2, nhưng gate đã rớt do SECRET_KEYS nên không cần dùng cái này để hạ gate.

4. **Gate: business chấm "đạt", ky-thuat + thi-cong ý kiến gate khác nhau.** Theo luật rubric (tiêu chí xương sống = 0 → rớt, dù tổng cao) và xác minh SECRET_KEYS: **RỚT GATE ở tiêu chí 1.** business tự mâu thuẫn: chấm tiêu chí 1 = 1 (không 0) nên cho "đạt", nhưng chính lý do của business ("hằng số 15 vs code 14, đưa như số thật không hedge") đúng ra rơi vào mức-0 của rubric.

---

## Nghi bịa / không nguồn — đã xác nhận

Gom từ 3 lens, tự kiểm lại từng cái (mở đúng file/code):

1. **"15 SECRET_KEYS" (line 101) — ĐỨNG VỮNG (lỗi thật).** `control/redaction.py:16-33`, `frozenset` có ĐÚNG 14 phần tử (`len(SECRET_KEYS)==14`). Artifact ghi 15. Lỗi lan từ upstream: `ATLAS.md:194,234` và `evidence-B:18,39` đều ghi "15 SECRET_KEYS" — nguồn trung gian đếm sai, artifact kế thừa trung thực nhưng con số vẫn sai vs code. Đây là claim khiến tiêu chí 1 = 0.

2. **Anchor `accept.py:52-128` cho `accept_decomposition` (line 72, 160) — ĐỨNG VỮNG (anchor lệch).** `decompose_agent/accept.py`: `accept_decomposition` ở line 186, không phải 52-128. Line 52-128 chứa `mu()`(52)/`Accept`(57)/`Reject`(66)/`_implies`(101). Cơ chế (μ co ngặt, Jaccard>0.80) CÓ thật (JACCARD_MAX ở line 22) nên không phải bịa cơ chế, nhưng số dòng trỏ sai construct.

3. **Anchor `core/session.py:49-85,188-194` cho `SessionIdentity` (line 145) — ĐỨNG VỮNG (anchor lệch).** `SessionIdentity` thực ở `core/session.py:16-23`; `:50` là `KernelSession`, `:104` `SessionFactory`, `:188` `SessionFactory.restore`. Claim lineage 7-field (session/run/task/agent/parent_session/delegation/depth) ĐÚNG (khớp 16-23), nhưng dòng neo trỏ sai class.

4. **`state.py:35-37` cho `all_accepted()` (line 44) — ĐỨNG VỮNG (anchor lệch nội bộ).** `all_accepted()` thực ở `supervisor/state.py:107-108`; line 36-37 là `is_satisfied`. Artifact tự-mâu-thuẫn: line 44 & 157 gán `all_accepted()`→`state.py:35-37`, nhưng line 173 gán đúng `state.py:107-108`. Cơ chế (true khi mọi AC passed ∧ evidence≠∅) ĐÚNG; chỉ neo lệch.

5. **"327 tests, E01–E10 ✓, E19 ✓" (line 28) — ĐỨNG VỮNG (số không khớp + tick tự-phong).** Đếm độc lập: 307 file `test_*.py`, 3795 hàm `def test_` (loại worktrees). "327" trace về `evidence-C`/docs-roadmap, KHÔNG khớp code — số cũ/khác-phạm-vi, không gắn nhãn "theo docs, chưa chạy lại". Dấu ✓ trong evidence-C là dấu CÓ-THƯ-MỤC, không phải log test chạy độc lập. Chấp nhận-có-cảnh-báo (rubric cho neo qua atlas/evidence), nhưng vẫn là số kế thừa chưa kiểm.

**Các claim KHÔNG đứng vững (kiểm lại thấy đúng code, KHÔNG phải bịa):**
- `state.py` `is_satisfied`/`all_accepted` cơ chế, `node.py:20` `FORBIDDEN_VERDICT_KEYS`, `node.py:28` `VALID_STATUSES={pending,active,decomposed,done,blocked}`, `policy.py:9` `max_steps=100/max_depth=8` + scope validate `:19-22`, `kernel.py:106` `execute_tool` + `tool.requested`(124)/`tool.completed`(216), `graph.py:357` `judge_acceptance`, `accept.py:22` `JACCARD_MAX=0.80`, `accept.py:52` `mu()` — TẤT CẢ khớp code gốc. thi-cong lens nói "state.py:35-37 cho is_satisfied thực ở 34-36" là lệch ±1 dòng, không sai bản chất.
