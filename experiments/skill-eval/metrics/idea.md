<!-- Đo một lượt chạy skill `idea` có bám đúng hợp đồng không: phân loại đúng, đi đúng nhánh, hỏi đúng tầng, không vượt vai (không tự kill/build), và dừng-bàn giao đúng ở Domain. | gate: 1. ROUTER — phân loại đúng độ rõ + độ khả thi, 2. ĐÚNG NHÁNH — độ khả thi dẫn đúng đường A/B/C, 3. HỎI ĐÚNG TẦNG — mỗi giai đoạn chỉ hỏi câu thuộc tầng đó, 4. KHÔNG VƯỢT VAI — không tự kill / không tự build / dừng đúng Domain -->

# Rubric — 7 tiêu chí chấm một lượt chạy `idea`

Mỗi tiêu chí 0/1/2 có anchor rõ. Chuẩn gốc: `idea/SKILL.md` (Router + 3 nhánh + Quy tắc bắt buộc + Bàn giao). Rubric chỉ biến hợp đồng đó thành thước đo được — không thêm tiêu chuẩn mới. Chấm cái `idea` HỨA, không chấm cái ta ước nó làm.

## 1. ROUTER — phân loại đúng độ rõ + độ khả thi (xương sống)

Trước khi làm gì, `idea` phải phân loại: độ rõ (rõ/mơ hồ) × độ khả thi (không khả thi / chưa rõ / khả thi rõ), và nói ra phân loại đó.

- 0 — không phân loại, hoặc phân loại sai bản chất: gọi "khả thi rõ" khi còn ẩn số kỹ thuật/business chưa kiểm chứng, hoặc gắn "không khả thi" khi thật ra chỉ chưa rõ. Đoán độ khả thi mà chưa hỏi khi thiếu thông tin (đáng lẽ hỏi ≤3 câu trước).
- 1 — có phân loại đúng trục khả thi, nhưng lệch độ rõ, hoặc không nói rõ căn cứ (vì sao rõ/mơ hồ, vì sao khả thi/chưa).
- 2 — phân loại cả hai trục, khớp bản chất ý tưởng, có căn cứ ngắn; khi thiếu thông tin thì hỏi một cụm ≤3 câu rồi mới phân loại thay vì đoán mò.

## 2. ĐÚNG NHÁNH — độ khả thi dẫn đúng đường A/B/C (xương sống)

Độ khả thi quyết đường đi: không khả thi → Nhánh A (làm rõ nhu cầu); chưa rõ → Nhánh B (spike); khả thi rõ → Nhánh C (GĐ1→GĐ5). Độ rõ chỉ đổi TỐC ĐỘ trong C, không đổi đường.

- 0 — đi sai nhánh so với phân loại: phân loại "chưa rõ" mà nhảy thẳng vào GĐ1→GĐ5; hoặc "khả thi rõ" mà đi spike vô cớ. Ở Nhánh B mà ý còn mơ hồ nhưng đặt ẩn số spike ngay, chưa làm rõ nhu cầu trước.
- 1 — đúng nhánh nhưng trộn việc của nhánh khác, hoặc dùng độ rõ để đổi đường thay vì đổi tốc độ.
- 2 — đi đúng đúng một nhánh khớp độ khả thi; trong C, độ rõ chỉ điều tốc độ (mơ hồ hỏi kỹ hơn, rõ thì lướt); ở B, ý mơ hồ được làm rõ nhu cầu trước khi đặt ẩn số.

## 3. HỎI ĐÚNG TẦNG — mỗi giai đoạn chỉ hỏi câu thuộc tầng đó (xương sống)

GĐ1 hỏi pain/giá trị/metric, KHÔNG hỏi kiến trúc/DB/deadline/stack. GĐ2–4 hỏi user cần gì/MVP/scope, KHÔNG hỏi lại ROI hay stack. GĐ5 hỏi ranh giới domain, KHÔNG hỏi sprint/kiến trúc cụ thể. Lỡ chạm câu sai tầng → ghi thành open question mang sang đúng tầng, không trả lời non.

- 0 — hỏi lệch tầng rõ: GĐ1 hỏi DB/framework/kiến trúc, hoặc GĐ5 đi vào schema/sprint/stack. Bất kỳ câu hỏi lệch tầng nào bị trả lời non ngay tại chỗ → tiêu chí này 0.
- 1 — phần lớn đúng tầng, lỡ chạm 1 câu sai tầng nhưng có ghi nhận là open question mang sang sau (không trả non).
- 2 — mọi câu hỏi bám đúng tầng của giai đoạn đang đứng; câu vô tình thuộc tầng sau được park lại đúng chỗ, không trả lời sớm.

## 4. KHÔNG VƯỢT VAI — không tự kill / không tự build / dừng đúng Domain (xương sống)

Ba lằn ranh của `idea`: (a) không tự kill — không khả thi thì phản biện + giữ điểm hay, chỉ user mới quyết kill; (b) không tự build — không viết code, không chọn kiến trúc/framework/stack; (c) dừng đúng GĐ5 Domain, không tự trôi sang Architecture/Roadmap.

- 0 — vượt vai bất kỳ: tự đề xuất "nên bỏ ý này" / tự ghi killed khi user chưa nói dừng; hoặc viết code / chọn stack-framework-kiến trúc; hoặc đi tiếp qua Domain sang Architecture. Bất kỳ vi phạm nào → tiêu chí này 0.
- 1 — giữ được vai nhưng lấn nhẹ: ví dụ gợi ý một hướng kiến trúc mờ, hoặc dùng câu phủ định cứng ("không làm được") khi phản biện dù chưa tự kill.
- 2 — không tự kill (luôn kèm lối đi tiếp, không câu phủ định cứng), không chạm code/stack/kiến trúc, dừng đúng ở Domain và chuyển sang khối Bàn giao.

## 5. NHỊP HỎI + TRUY VẾT — một cụm mỗi lượt, quyết định lớn ghi lý do + phương án loại

Một cụm câu hỏi mỗi lượt (≤3 câu cùng chủ đề, ưu tiên AskUserQuestion), không dồn hỏi hết. Mỗi quyết định lớn ghi lý do + phương án đã loại để audit sau; ý mới/rủi ro cao brainstorm ≥2 hướng rồi mới chốt.

- 0 — dồn nhiều cụm/nhiều tầng câu hỏi trong một lượt; hoặc chốt hướng lớn mà không có lý do lẫn phương án loại.
- 1 — nhịp hỏi đúng phần lớn nhưng 1 lượt hơi quá tải, hoặc quyết định lớn có lý do nhưng thiếu phương án đã loại; việc rủi ro cao chỉ nêu 1 hướng.
- 2 — mỗi lượt một cụm ≤3 câu cùng chủ đề; mỗi quyết định lớn kèm lý do + phương án loại; việc rủi ro cao brainstorm ≥2 hướng trước khi chốt.

## 6. ĐỦ-LÀ-ĐỦ — độ sâu artifact tỉ lệ rủi ro, không nhảy cóc giai đoạn

Độ sâu mỗi giai đoạn tỉ lệ rủi ro/ẩn số, không phải vị trí trong luồng. Việc nhỏ đã rõ → vài dòng mỗi giai đoạn (được rút gọn, ghi lý do). Ý mới/rủi ro cao → đầy đủ. KHÔNG bao giờ nhảy cóc giai đoạn để tiết kiệm — chỉ được rút gọn độ sâu.

- 0 — nhảy cóc giai đoạn (bỏ hẳn GĐ1 hoặc GĐ5 mà không lý do), hoặc lệch nặng: việc nhỏ mà bơm PRD 14 mục / Business Case 10 mục, hoặc việc rủi ro cao mà artifact hời hợt bỏ sót pain/metric/rule.
- 1 — đủ giai đoạn nhưng độ sâu chưa khớp rủi ro ở 1–2 chỗ (hơi thừa hoặc hơi mỏng).
- 2 — đủ giai đoạn, độ sâu bám rủi ro: nhỏ thì gọn có lý do, rủi ro cao thì đủ pain/metric/MVP/scope-out/entity+rule; không nhảy cóc, chỉ rút gọn.

## 7. BÀN GIAO — dừng đúng và trỏ đúng sibling

Sau GĐ5, ra khối Bàn giao: domain đã chốt + artifact path + liệt kê sibling đúng (partner cho GĐ6+/traceability, frame cho một slice, atlas/explain cho code cũ). Không tự chọn hộ skill nào tiếp.

- 0 — không bàn giao khi domain đã đủ rõ, hoặc trỏ sai sibling (vd bảo build code luôn), hoặc tự quyết hộ user chạy skill nào.
- 1 — có bàn giao nhưng thiếu một phần (thiếu artifact path, hoặc liệt kê sibling chung chung/thiếu lựa chọn).
- 2 — khối Bàn giao đủ: domain đã chốt + artifact path + các sibling đúng vai để user tự chọn, không chọn hộ.

## Gate (tiêu chí xương sống)

Tiêu chí **1 (Router), 2 (Đúng nhánh), 3 (Hỏi đúng tầng), 4 (Không vượt vai)** là xương sống. Bất kỳ cái nào = 0 → lượt chạy **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Lý do: bốn cái này là bản chất hợp đồng của `idea` — phân loại sai thì cả luồng sai; đi sai nhánh thì làm nhầm việc; hỏi sai tầng thì bắt user quyết non; vượt vai (tự kill/tự build/không dừng) là đúng thứ `idea` cam kết KHÔNG làm. Một lượt điểm cao mà tự viết code hay tự kill vẫn rớt. Khi so nhiều bản: loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Vì sao 7 tiêu chí này

Bốn cái đầu đo *đi có đúng đường không* (phân loại → chọn nhánh → hỏi đúng tầng → giữ đúng vai). Ba cái sau đo *chạy có kỷ luật và kết đúng chỗ không* (nhịp hỏi + truy vết, đủ-là-đủ, bàn giao). Gộp lại = toàn bộ hợp đồng của `idea`, không hơn. Thêm tiêu chí thứ 8 chỉ khi có kiểu lỗi thật lặp lại mà 7 cái này không bắt được.