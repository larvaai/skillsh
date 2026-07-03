CHẤM: 09-backlog · /Users/uspro/Desktop/skillsh/rebuild-hex-agent/pipeline/09-backlog.md

[2] — Roadmap mở bằng Business Objective đo được (M1 zero false-finish) + bảng theme×release, mỗi Epic mở bằng business value nghiệp vụ + trạng thái, jargon lọt vào đều được dịch nghĩa → lãnh đạo dừng ở tầng epic vẫn hiểu.
[2] — Đủ ba artifact đúng cây tầng: Roadmap neo Objective→Goal, Backlog Epic→Feature→Story→AC (không nhảy tầng), Release Plan có Release AC + phụ thuộc + rủi ro + mục hoãn kèm lý do + park-with-trigger; R1 bao slice GĐ8 làm feature đầu.
[2] — Mọi story R1 có ≥1 AC Given/When/Then kiểm được bằng máy, AC nằm đúng dưới story + nối rule Domain, kèm Tasks thô để size + Test ref TC-… → dev cầm S1.1.1/S1.6.1 bắt tay ngay.
[2] — Đủ-là-đủ: R1 tới Story+AC, R2 Feature+Story-chính (AC refine sau), R3 ⭐ tới AC, R4 chỉ theme+epic; số AC tỉ lệ rủi ro; Domain treo → open-Q, không bịa story.
[0] — TRÍCH CODE SAI (gate): AC-1 S3.1.1 dẫn "roles/agent.py:53" cho logic allowlist = union − forbidden, nhưng agent.py:53 là dòng "may_route_to" trong envelope blocker; logic thật ở roles/spec.py:64 → đúng trigger "0" của tiêu chí xương sống này.
[2] — Mỗi quyết định release có lý do kiểm được + phương án đã loại nêu tên (loại multi-agent-trước, loại gộp-R2-vào-R3, loại Control-Tower-ở-R1, loại (a)(b)(c) tầng cổng); thứ tự theo gỡ-rủi-ro không theo độ khó.
[2] — Không chọn lại stack/kiến trúc (chỉ tham chiếu để size+thứ tự), DoD chỉ trỏ GĐ11, Test ref chỉ móc TC-, gợi ý ranh giới module chỉ trỏ /modules; câu ngoài vai (NFR-số) ghi open-Q → Operate.
[2] — Cổng dùng đúng câu doc GĐ9 + câu phụ, trình artifact+rủi ro+open-Q trước quyết định, bàn giao liệt kê đủ /modules·/frame·/idea·/partner để PO/Tech-lead quyết; GO tự-cấp hợp lệ trong chế độ tự-quyết đã khai + không ép đi tiếp.

TỔNG: 14/16

GATE: rớt: tiêu chí 5 (TRACEABILITY & KHÔNG BỊA — xương sống) = 0 vì trích code sai `roles/agent.py:53` cho logic `union − forbidden` (logic thật ở `roles/spec.py:64`). Theo luật gate của rubric, một bản 14/16 mang một AC dẫn `path:line` sai code gốc vẫn RỚT, vì đội delivery sẽ xây kế hoạch trên bằng chứng giả.

SỬA TRƯỚC TIÊN: Sửa AC-1 S3.1.1 trích `roles/agent.py:53` → `roles/spec.py:54-64` (`return frozenset(union - forbidden) # forbidden wins`), rồi chỉnh con số tự-khai R1 ở cả ba khối (backlog head + cổng + bàn giao) về đúng "5 epic / 6 feature / 7 story" và "14 SECRET_KEYS".

---

## 2. Bảng tiêu chí × 3 lens + phân xử

| # | Tiêu chí | ky-thuat | business | thi-cong | Trọng tài | Phân xử |
|---|---|---|---|---|---|---|
| 1 | ĐỌC-ĐƯỢC 3 TẦNG (xương sống) | 2 | 2 | 2 | **2** | Đồng thuận, giữ nguyên. |
| 2 | ĐỦ BA ARTIFACT + ĐÚNG CÂY TẦNG | 2 | 2 | 2 | **2** | Đồng thuận. |
| 3 | AC DÙNG ĐƯỢC (xương sống) | 2 | 2 | 2 | **2** | Đồng thuận. |
| 4 | ĐỦ-LÀ-ĐỦ | 2 | 2 | 2 | **2** | Đồng thuận. |
| 5 | TRACEABILITY & KHÔNG BỊA (xương sống) | 0 | 0 | 0 | **0** | Đồng thuận + tự kiểm code: agent.py:53 SAI đã xác nhận. Gate rớt. |
| 6 | LÝ DO + PHƯƠNG ÁN ĐÃ LOẠI | 2 | 2 | 2 | **2** | Đồng thuận. |
| 7 | RANH GIỚI VAI | 2 | 2 | 2 | **2** | Đồng thuận. |
| 8 | CỔNG + BÀN GIAO | 2 | 2 | **1** | **2** | **Bất đồng — trọng tài NÂNG lên 2** (xem dưới). |
| | **TỔNG** | 14 | 14 | 13 | **14** | |

**Bất đồng đáng chú ý & cách phân xử:**

1. **Tiêu chí 8 — thi-cong chấm 1, hai lens kia chấm 2.** Luật hợp nhất mặc định lấy điểm THẤP NHẤT (1), NHƯNG trọng tài NÂNG lên 2 vì thi-cong dock điểm trên căn cứ nằm NGOÀI rubric tiêu chí 8. Lý do thi-cong nêu: "khối trình cổng tái sinh con số sai 5 epic/7 feature/~10 story". Đó là lỗi TRACEABILITY (đã bị phạt trọn ở tiêu chí 5 = 0), không phải lỗi cấu trúc cổng/bàn giao. Anchor tiêu chí 8 (rubric dòng 63) chỉ đòi: cổng dùng đúng câu doc GĐ9 + câu phụ · trình đánh giá+rủi ro+open-Q trước quyết định · bàn giao liệt kê đủ lựa chọn để người duyệt quyết. Kiểm artifact: câu cổng đúng nguyên văn doc GĐ9 (dòng 309), câu phụ (dòng 310), trình open-Q + rủi ro trước GO (dòng 316, 324, 331), bàn giao 3 đường /modules·/frame·/idea·/partner (dòng 350-354). "GATE: GO" tự cấp là HỢP LỆ vì chế độ tự-quyết PO+Tech-lead đã khai ở dòng 5 và handoff KHÔNG ép một đường. Mọi mảnh của anchor-2 có đủ → 2. Không double-count một lỗi ở hai tiêu chí.

2. **Tiêu chí 5 — cả ba đồng thuận 0 nhưng lý do khác nhau về "cái gì kéo về 0".** ky-thuat + thi-cong nhấn agent.py:53; business nhấn con số 7-feature. Trọng tài tự mở code: CẢ HAI đều là lỗi thật (agent.py:53 sai citation = trigger "trích code sai"; 6 feature thực vs 7 tự-khai = trigger "tự khen kiểu đã-phủ-đủ đếm lại không khớp nội dung chính"). Một trong hai đã đủ kéo tiêu chí xương sống về 0; ở đây có cả hai → 0 vững chắc.

3. **ky-thuat khai thêm "class RoleView không tồn tại (class thật = Agent)" trong fix_first + nghi_bia.** Trọng tài BÁC claim phụ này: `grep RoleView` cho thấy `class RoleView` CÓ THẬT ở `roles/spec.py:32` (dùng ở registry.py:85-95, __init__.py). Story S3.1.1 dùng "RoleView" là ĐÚNG tên. Việc bác claim phụ này KHÔNG cứu được tiêu chí 5 (agent.py:53 vẫn sai), nhưng ghi lại để không nối lỗi giả vào bản cuối.

---

## 3. Nghi bịa / không nguồn — đã xác nhận

**[VỮNG — gate] `roles/agent.py:53` cho AC-1 S3.1.1 (allowlist = union − forbidden).**
Mở code: `roles/agent.py:53` = `"may_route_to": list(self.spec.may_route_to),` — nằm trong envelope blocker của `guard_tool_call`, KHÔNG liên quan logic allowlist. Logic `union − forbidden` thật ở `roles/spec.py:54-64`: method `allowed_tools(...)` kết `union = explicit_tools | core_tools`, gom `forbidden` từ skills, `return frozenset(union - forbidden)  # forbidden wins` (dòng 64). → Trích code SAI địa chỉ. Đây là lỗi xương sống kéo tiêu chí 5 = 0, gate rớt.

**[VỮNG] "R1: 5 epic / 7 feature / ~10 story có AC" (lặp 3 chỗ: cổng dòng 313, 320; bàn giao dòng 346).**
Đếm lại thân artifact: R1 có 5 epic (E01–E05) ✓, nhưng chỉ 6 feature (F1.1–F1.6, đúng như chính Release Plan dòng 249 tự liệt kê) và 7 story (S1.1.1, S1.1.2, S1.2.1, S1.3.1, S1.4.1, S1.5.1, S1.6.1). "7 feature" lệch +1 và mâu thuẫn chính nội dung + chính Release Plan của artifact; "~10 story" thổi phồng +3 (dù có "~"). Đúng trigger "tự khen đã-phủ-đủ đếm lại không khớp nội dung chính".

**[VỮNG] "redactor 15 SECRET_KEYS" (Tasks S1.5.1, dòng 123).**
Mở `control/redaction.py:16-31`: `SECRET_KEYS = frozenset({...})` chứa đúng 14 khoá (api_key, apikey, authorization, password, passwd, secret, secret_key, client_secret, token, access_token, refresh_token, private_key, set-cookie, cookie). Con số "15" (kế thừa từ 05-idea-domain.md) lệch code thật. Tác động thấp (nằm ở dòng Tasks-để-size, không ở AC) nhưng vẫn là con số không khớp code gốc.

**[VỮNG — nhẹ] "R3: 5 story ⭐ LÕI" (khối cổng dòng 320).**
Đếm dấu ⭐ trong R3: S3.1.1⭐, S3.2.1⭐, S3.3.1⭐, S3.4.1⭐, S3.5.1⭐⭐, S3.5.2⭐ = 6 story mang ⭐. Ghi "5" lệch −1. Có thể biện là "5 story lõi trong E10" (S3.2.1–S3.5.2) nhưng khối cổng ghi phạm vi "R3" → vẫn là con số không khớp. Nhẹ, đã bị bao trong tiêu chí 5 = 0.

**[IMPRECISE, KHÔNG PHẢI BỊA] `loop.py:208-218` cho AC-3 S1.6.1 (atomic txn commands+round+save).**
Hai file `loop.py` tồn tại. `orchestrator/loop.py:208-218` là bên trong `restore` (SessionFactory), KHÔNG phải atomic txn. NHƯNG `supervisor/loop.py:203-218` LÀ đúng khối "apply queued commands → advance round → save ONCE ... a crash here cannot leave a half-applied state" — hành vi atomic mô tả trong AC CÓ THẬT và dải dòng 208-218 nằm trong khối này. Lỗi duy nhất: thiếu tên thư mục (mơ hồ giữa hai file). Imprecise, không phải bịa hành vi — không tự nó phá gate (gate đã rớt vì agent.py:53).

**[BÁC BỎ] "class RoleView không tồn tại" (ky-thuat fix_first + nghi_bia).**
`grep RoleView` xác nhận `class RoleView` CÓ THẬT ở `roles/spec.py:32`, dùng ở `roles/registry.py:85-95`, export ở `roles/__init__.py:15-19`. Story S3.1.1 dùng tên "RoleView" là ĐÚNG. Claim phụ này của ky-thuat SAI, đã loại khỏi bản cuối.

**[VỮNG NGƯỢC — citation ĐÚNG, ghi để cân đối] Phần lớn citation khác khớp code.**
Tự kiểm mẫu: `supervisor/evidence.py:16-23` (EVIDENCE_TYPES + NON_EVIDENCE_KINDS scaffolding) khớp AC-2 S3.5.1 ✓; `delegation/policy.py:25-26` (`scope <= parent.allowed_capabilities`) + `:8-32` (max_depth=8) khớp AC-1/AC-4 S3.2.1 ✓; `decompose_agent/tree.py:43-51` (`next_node` = leftmost pending, deps done, `min(key=(depth,order))`) khớp AC-1 S3.4.1 ✓. → Traceability nền vững, chỉ một citation sai (agent.py:53) + hai con số lệch; nhưng theo luật gate, một citation sai là đủ 0.
