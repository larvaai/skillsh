CHẤM: explain · /Users/uspro/Desktop/skillsh/rebuild-hex-agent/explain/EXPLAIN.md

[2] — Mọi claim code spot-check khớp GỐC cả thứ tự lẫn vị trí (execute_tool: deepcopy args→publish tool.requested→scope-check→middleware, kernel.py:106-150; next_node leftmost-pending by (depth,order), tree.py:43-51; delegation scope child⊆parent fail-closed, policy.py:25-27; StateStore deepcopy, state.py:19-27; redact-before-fanout, emitter.py:53-61) và số liệu truy được (12 gap/3 Critical→REVIEW.md:12; 7 invariant→REBUILD-BRIEF:28), nhưng "0 rò state" (dòng 62) là con-số-thuộc-tính-thiết-kế trình bày như đã-đạt trên bản rebuild CHƯA có code (REVIEW.md:6 skeleton 0/9 tick) mà không gắn nhãn "invariant đích, chưa đo" — còn đúng 1 chỗ mơ hồ, không tới mức bịa (có nguồn I2/I3 chống lưng).
[3] — Bảng kiểm thuật ngữ sạch: mọi tên nội bộ neo vào một bước trước khi gọi (execute_tool b5, delegation b4, decompose gate b2, judge_acceptance b7, event log b6, AgentKernel/KernelSession giữ tới Zoom 3), và mọi tên công nghệ ngoài kèm cụm đời thường hoặc giấu ở tầng thấp ("một file SQLite làm chân lý để tua lại" d54, "kho tri thức vector (Qdrant)" d72, "LangGraph chỉ lo điều phối" d64).
[3] — Ba vai dùng được thật: business có câu chuyện giá trị (Góc nhìn lãnh đạo + Zoom 0-1), CTO có hình hài + ranh giới (Zoom 2 tám bước + Zoom 3 bounded context + "hai chốt đối nhau"), dev có đường vào code cụ thể (module→bước + "Neo về gói rebuild" trỏ REBUILD-BRIEF/ATLAS §7/REVIEW/slice-01); giá trị lặp mỗi tầng (d34, d56, d74).
[3] — Đúng L3: dừng ở Zoom 2 kỹ + chạm Zoom 3 với trách nhiệm+ranh giới từng module; không trích số dòng/chữ ký hàm nào trong thân, chỉ gọi tên module/entrypoint đã neo (hợp lệ từ L2) — ranh giới trích-dẫn/gọi-tên sạch toàn bài.
[3] — Che nhãn vẫn đọc ra overview từ cấu trúc: Zoom 0-1 không tên code + đúng một ý cốt lõi, Zoom 2 là tám bước đánh số kể chuyện, Zoom 3 mỗi module trỏ về một bước; thuần vai explain, việc vượt vai chỉ là con trỏ sang review/frame/atlas.
[2] — Mâu thuẫn "cửa duy nhất vs hai chokepoint" CÓ được hoà giải TRONG bài (bước 4 nói delegation là "cửa RIÊNG cố tình khác cửa gọi-tool", bước 5 liệt kê "một cửa" chỉ gồm tool/file/LLM), nhưng claim tuyệt đối "mọi hành động ra thế giới bên ngoài... đúng MỘT cửa" (d32) không scope NGAY tại chỗ — scope nói muộn ở bước 4-5, đúng anchor mức 2.
[2] — Câu ngắn phẳng phần lớn, đánh số đúng cho luồng Zoom 2 và bullet đúng cho điểm-danh module Zoom 3, không meta trong thân, nhưng câu-dài-nối-gạch-ngang lặp thành tật ở vài chỗ (d32 câu "ý tưởng cốt lõi" chồng em-dash + chấm-phẩy, d46, d48, d62).
[3] — Kết đúng L3 với ≥2 hướng đích danh (đi sâu Zoom 3→L4, hoặc chọn luồng cụ thể "nghiệm thu"/"giao-việc" bằng chế độ flow), mỗi hướng nói rõ đi bằng gì và nối vào điều vừa dạy; thêm "Neo về gói rebuild" mở 4 cửa cụ thể.

TỔNG: 21/24
GATE: đạt — cả ba tiêu chí xương sống (1=2, 2=3, 3=3) đều > 0; không tiêu chí nào rớt.
SỬA TRƯỚC TIÊN: Scope claim "đúng MỘT cửa" NGAY tại Zoom 1 ("một cửa cho mọi lệnh gọi-tool/LLM; giao-việc cố tình đi cửa tách RIÊNG — để không leo thang quyền") và đổi "0 rò state" (d62) thành "trạng thái cô lập theo thiết kế (invariant, chưa đo trên rebuild)" — hai sửa nhỏ gỡ đúng khe tiêu chí 6 + con-số-nghi ở tiêu chí 1, kéo 21→23/24.

---

## 2. Bảng tiêu chí × 3 lens + phân xử bất đồng

| # | Tiêu chí | ky-thuat | business | thi-cong | HỢP NHẤT | Ghi chú phân xử |
|---|---|---|---|---|---|---|
| 1 | Bám bằng chứng (xương sống) | 2 | 2 | 3 | **2** | Lấy thấp nhất (2). Không nâng: thi-cong tự thừa nhận "0 rò state nghi nhẹ về tình trạng" nhưng vẫn cho 3 — mức 3 đòi "chỗ chưa chắc gắn nhãn rõ", mà d62 không gắn nhãn "invariant chưa-đo". Không hạ về 0: "0 rò state" CÓ nguồn kiểm được (ATLAS:100 + REBUILD-BRIEF:29, I2/I3, backed evidence A/B + state.py deepcopy) → không thoả điều-kiện-0 "không có nguồn kiểm được". |
| 2 | Neo (xương sống) | 3 | 3 | 3 | **3** | Đồng thuận. Bảng kiểm thuật ngữ sạch, tự kiểm khớp. |
| 3 | Ba khán giả (xương sống) | 3 | 3 | 3 | **3** | business cho 3, hai lens kia cũng 3. (Lưu ý business ghi 3 dù ở tiêu chí 5 nó trừ điểm về "một ý cốt lõi" — không lan sang đây.) |
| 4 | Mức | 3 | 3 | 3 | **3** | Đồng thuận. L3 đúng, ranh giới trích-dẫn/gọi-tên sạch. |
| 5 | Chế độ & vai | 3 | 2 | 3 | **3** | KHÔNG lấy thấp nhất — NÂNG 2→3, có bằng chứng ngược. business hạ vì "d32 gói HAI ý (một-cửa + tách hai-chốt) vào một câu, vi phạm Zoom 1 đúng MỘT ý". Đọc lại d32: ý cốt lõi LÀ "một cửa cho mọi hành động → audit/chặn/tua" ; mệnh đề "tách chuyện xong-có-bằng-chứng khỏi cắt-ngân-sách" là mô tả HAI CHỐT ĐỐI NHAU — đây chính là hệ quả trực tiếp của cùng một ý thiết kế "kỷ luật cứng", được bài trình bày như một ý cốt lõi thống nhất (nhắc lại nguyên khối ở hộp d56). Không phải hai ý rời rạc → không vi phạm "đúng MỘT ý cốt lõi". Vấn đề câu-d32-dài là lỗi LỜI VĂN (tiêu chí 7), không phải lỗi cấu-trúc-chế-độ → tránh phạt kép. Cấu trúc overview theo thang zoom, thuần vai explain: đủ điều kiện mức 3. |
| 6 | Nhất quán nội tại | 2 | 2 | 1 | **2** | KHÔNG lấy thấp nhất — GIỮ 2, không hạ về 1, có lý do. Mức 0 = "mâu thuẫn KHÔNG được hoà giải"; bài CÓ hoà giải rõ (bước 4 nêu delegation là cửa RIÊNG cố tình tách + lý do "không leo thang quyền"; bước 5 giới hạn "một cửa" = tool/file/LLM) → không 0. Ranh giới 1-vs-2: mức 1 = "người đọc phải TỰ hoà giải"; mức 2 = "scope nói muộn, ở đoạn khác". Ở đây scope KHÔNG bị bỏ cho người đọc tự nối — bài tự nối ở bước 4-5, chỉ là muộn (Zoom 2) so với chỗ phát biểu (Zoom 1 d32). Đó đúng là anchor mức 2 verbatim ("scope nói muộn, ở đoạn khác"). thi-cong đếm "một cửa" lặp 32/34/74 để ghép mức 1, nhưng đó là CÙNG một claim vọng lại, không phải nhiều mâu thuẫn khác nhau; và bản thân thi-cong cũng viết "bài CÓ hoà giải muộn nên không rơi 0". Hai lens độc lập đọc ra 2 với anchor chắc → hợp nhất = 2, ghi rõ bất đồng thi-cong. |
| 7 | Lời văn | 2 | 2 | 2 | **2** | Đồng thuận. Câu-dài-nối-gạch-ngang lặp (d32/46/48/62) là tật chung cả ba lens chỉ ra → mức 2 ("còn 1-2 chỗ rườm"). |
| 8 | Kết | 3 | 3 | 3 | **3** | Đồng thuận. ≥2 hướng đích danh + chế độ đi kèm + 4 con trỏ đọc-tiếp. |

**TỔNG hợp nhất: 2+3+3+3+3+2+2+3 = 21/24.**

### Bất đồng đáng chú ý & cách phân xử
- **Tiêu chí 1 (2 vs 2 vs 3):** phân xử = 2. thi-cong quá rộng tay ở "0 rò state" — nó tự thấy "nghi nhẹ" nhưng không hạ điểm. Đúng luật lấy-thấp-nhất, và tôi tự kiểm xác nhận 2 là công bằng (có nguồn → không phải bịa/0; không gắn nhãn chưa-đo → không phải sạch/3).
- **Tiêu chí 5 (3 vs 2 vs 3):** phân xử = 3, NÂNG business. Tôi mở artifact d32/d56: mệnh đề "hai chốt" là hệ quả cùng một ý thiết kế, không phải ý thứ hai độc lập; lỗi câu-dài thuộc tiêu chí 7. Nâng có bằng chứng, tránh phạt kép.
- **Tiêu chí 6 (2 vs 2 vs 1):** phân xử = 2, KHÔNG hạ theo thi-cong. Ranh giới 1↔2 nằm ở "người đọc tự hoà giải" (1) vs "scope nói muộn ở đoạn khác" (2); bài tự hoà giải rõ tại bước 4-5 → khớp mức 2. Đây là điểm yếu THẬT lớn nhất và là fix-first, nhưng chưa tới mức 1.

---

## 3. Nghi bịa / không nguồn — đã xác nhận

Gom từ cả 3 lens, tự kiểm lại từng cái trên file/code viện dẫn:

1. **"0 rò state" (EXPLAIN.md:62) — ĐỨNG một phần (giữ là điểm-trừ tiêu chí 1, KHÔNG phải bịa).**
   Kiểm: ATLAS.md:100 và REBUILD-BRIEF.md:29 đều ghi "state chỉ ở session → 0 rò state giữa các run (I2/I3)", anchor evidence A §2/§4/§7 + B §2. Cơ chế StateStore `copy.deepcopy` có thật trên GỐC (`core/state.py:19,23,27`: as_dict/snapshot/restore đều deepcopy). NHƯNG rebuild CHƯA có code (REVIEW.md:6 "skeleton 0/9 tick; thiết kế trên giấy") → "0 rò state" là INVARIANT-ĐÍCH chứ không phải phép đo trên rebuild, và bài trình bày ("nhiều lần chạy không giẫm lên nhau (0 rò state)") như thuộc-tính-đã-đạt mà không gắn nhãn "chưa đo". Kết: không bịa (có nguồn chống lưng), nhưng là con-số-gánh-kết-luận thiếu nhãn tình-trạng → đúng 1 chỗ mơ hồ, hạ tiêu chí 1 xuống 2. (Rubric mức-0 đòi "không có nguồn kiểm được" — không thoả.)

2. **"12 gap, 3 Critical" (EXPLAIN.md:82) — ĐỨNG (có nguồn, không bịa).**
   Kiểm: khớp REVIEW.md:12 ("12 lỗ hổng... Ba trong số đó là Critical") và bảng REVIEW.md:194-196 (G1/G2/G3 = 🔴 Critical). Cảnh báo business-lens rằng "cấp Critical do AI tự phong" là đúng về xuất xứ, nhưng với vai explain (thuật lại số từ nguồn thượng nguồn đã khai ở d4/d82) thì con số truy được → không phải bịa. Không giữ làm điểm trừ tiêu chí 1.

3. **"7 bất biến / 7 invariant" (EXPLAIN.md:80) — ĐỨNG (có nguồn).**
   Kiểm: khớp REBUILD-BRIEF.md:28 "The 7 load-bearing invariants". Nguồn khai ở d4.

4. **Thứ tự trong chokepoint execute_tool (EXPLAIN.md:48,50) — ĐỨNG (khớp GỐC cả thứ tự lẫn vị trí).**
   Kiểm `core/kernel.py:106-150`: deepcopy args → publish `tool.requested` (kèm lineage+args) → scope-check (`request.name not in allowed_capabilities` → fail) → (middleware chain) → tool.completed|failed. Bài nói "ghi lại hành động, kiểm quyền, rồi mới cho chạy" — đúng thứ tự. LLM-là-tool và redact-tại-biên (d50) khớp emitter.py:53-61 (validate→seq→redact→fan-out).

5. **next_node leftmost-pending (EXPLAIN.md:44,64) + delegation scope child⊆parent (EXPLAIN.md:46,62) — ĐỨNG.**
   Kiểm `decompose_agent/tree.py:43-51` (`min(ready, key=(depth,order))`, ready = pending & mọi dep done) và `delegation/policy.py:25-27` (`if not scope <= parent.allowed_capabilities: raise PermissionError`). Khớp.

6. **"dám tin để cho nó chạy" lặp 3 lần (d34/56/74) — KHÔNG phải bịa, KHÔNG giữ làm điểm trừ tiêu chí 1.**
   Kiểm: business-lens gọi đây là "kết luận giá trị không có bằng chứng NGOÀI (người dùng/chi phí/thị trường)". Đúng là không có bằng chứng thị-trường, nhưng đây là mệnh-đề-giá-trị (value framing) của vai explain, không phải claim-đo-được cần kiểm trên code/nguồn — rubric tiêu chí 1 kiểm "claim về code/thiết kế", không kiểm mệnh đề giá trị. Việc LẶP 3 lần là lỗi lời-văn/lặp-giá-trị (đã phản ánh ở tiêu chí 7 mức 2), không phải bịa.

7. **GATE "GO 14/14 đạt" trong EXPLAIN.grade.md (d13/38/94) — KHÔNG tính là bằng chứng, KHÔNG ảnh hưởng bản chấm này.**
   Kiểm: đây là điểm AI tự cấp ở chế độ tự-quyết, dùng rubric v1 (thang 14, đã BÃO HOÀ — RESULT.md 20260701 xác nhận baseline/B/D/E cùng 14/14). Theo luật gate của rubric v2, cổng tự-quyết KHÔNG là bằng chứng; và bản chấm này chấm EXPLAIN.md, không chấm EXPLAIN.grade.md. v2 tách đúng 3 khe mà v1 để sót (tiêu chí 6 mâu thuẫn-cửa, tiêu chí 7 câu-dài, con số "0 rò state") → giải thích vì sao v2 cho 21/24 chứ không 24/24.

8. **Module dirs ở Zoom 3 (core/, orchestrator/...) trình như bản đồ rebuild — KHÔNG phải bịa, có khai gián tiếp.**
   Kiểm: cấu trúc là của bản GỐC hex_agent (khớp evidence-B §5); rebuild chưa có code (REVIEW.md:6). Bài KHÔNG tự thú trong thân, nhưng header d4 khai "anchor file:line bản GỐC" → khai gián tiếp. Với tech-lead đi build đây là điểm cần biết nhưng không đủ thành lỗi-bịa; đã được phản ánh gián tiếp qua cùng cơ chế với "0 rò state" (thuộc-tính-thiết-kế-chưa-có-code).

**Kết luận phần 3:** sau kiểm, KHÔNG còn claim nào là BỊA (file/symbol/hành vi/thứ tự đều tồn tại và khớp GỐC; mọi con số truy được về nguồn đã khai). Điểm-trừ duy nhất còn đứng ở tiêu chí 1 là con-số-thuộc-tính-thiết-kế "0 rò state" trình bày thiếu nhãn "chưa đo trên rebuild" — hạ tiêu chí 1 từ 3 xuống 2, không đủ để rớt (có nguồn kiểm được).
