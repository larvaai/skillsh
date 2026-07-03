<!-- Chấm output của skill review: có tìm đúng loại gap (edge/error/permission), có bằng chứng-vị trí cụ thể, không bịa, xếp theo mức nghiêm trọng, và kết bằng bước tiếp đúng không. | gate: 1. ĐÚNG LOẠI GAP — gap báo phải thuộc edge/error/permission, không lấn sang explain/trace/triage/plan, 2. BẰNG CHỨNG — mỗi finding neo được vào vị trí cụ thể (file·symbol) + điều thiếu + hậu quả, không mơ hồ, 3. KHÔNG BỊA — mọi gap có thật trong code; chỗ chưa chắc phải tách xuống 'có thể là gap' -->

# Rubric — 6 tiêu chí chấm một output `review`

Mỗi tiêu chí 0/1/2. Chuẩn gốc: `review/SKILL.md` (ba chế độ, luật evidence, bảng mức độ, hand-off). Rubric chỉ biến hợp đồng đó thành thước đo — không thêm tiêu chuẩn mới.

## 1. ĐÚNG LOẠI GAP — bám chế độ, không lấn skill khác (xương sống)

Gap tìm được phải thuộc đúng phạm vi review: edge case còn thiếu, error path chưa xử, lỗ hổng permission. Không lấn sang việc skill khác (giải thích code = explain, đào data-flow = trace, phán giữ-xoá file = triage, đề xuất fix = plan).

- 0 — sai loại: báo "gap" mà thực ra là giải thích code chạy sao, hay liệt kê đề xuất fix/refactor, hay phán số phận file; hoặc chế độ đang chạy không khớp gap báo (đang error mà toàn nói style).
- 1 — phần lớn đúng loại gap, có 1–2 mục lạc sang giải thích/fix/việc skill khác.
- 2 — mọi mục đều là gap thật thuộc edge/error/permission; không mục nào lấn sang explain/trace/triage/plan.

## 2. BẰNG CHỨNG — mỗi finding có vị trí cụ thể, không mơ hồ (xương sống)

Theo luật `file · dòng/symbol · điều thiếu · hậu quả`. Mỗi gap phải neo được vào một chỗ chỉ ra được trong code.

- 0 — có finding không vị trí: nói chung chung ("thiếu validation ở nhiều chỗ", "error handling chưa tốt") mà không chỉ được file/symbol; hoặc thiếu "điều thiếu" hoặc "hậu quả".
- 1 — phần lớn finding có vị trí + hậu quả, 1 chỗ còn mơ hồ hoặc thiếu một nửa (có vị trí nhưng không nói hậu quả, hoặc ngược lại).
- 2 — mọi finding đủ `vị trí (file·symbol) + điều thiếu + hậu quả`, chỉ đúng chỗ, không mơ hồ.

## 3. KHÔNG BỊA — mọi gap có thật trong code (xương sống)

- 0 — có gap bịa: dẫn file/symbol/hành vi không tồn tại, hoặc khẳng định "chưa xử lý" một case mà code thật đã xử lý. Bất kỳ gap bịa nào → tiêu chí này 0.
- 1 — mọi gap khớp code, nhưng có 1 chỗ suy đoán không chắc mà KHÔNG gắn nhãn "có thể là gap".
- 2 — mọi gap khớp code thật; chỗ chưa chắc được tách xuống mục "CÓ THỂ LÀ GAP" kèm câu hỏi cần xác nhận.

## 4. XẾP ƯU TIÊN — theo mức nghiêm trọng

Theo bảng: Critical (lỗi production / mất data / security breach) → Medium (sai hành vi case cụ thể, không crash) → Low (thiếu nhỏ, UX, inconsistency).

- 0 — không gắn mức, hoặc gắn sai nặng-nhẹ (một lỗ hổng permission bypass bị để Low; một inconsistency nhỏ gắn Critical).
- 1 — có gắn mức và đại thể đúng, nhưng thứ tự/nhãn lệch ở 1 mục hoặc không sắp nặng lên trước.
- 2 — mỗi gap có nhãn mức đúng bản chất hậu quả, và báo cáo sắp nặng trước nhẹ sau.

## 5. KẾT — bước tiếp đúng vai

Review chỉ báo cáo, không tự fix; kết bằng gợi ý đúng theo kết quả (có Critical → hand off `plan`; có "có thể là gap" → hỏi đào sâu; không thấy gap → gợi ý review phần khác hoặc plan).

- 0 — không có bước tiếp, HOẶC tự nhảy vào viết fix/sửa code (vượt vai review).
- 1 — có gợi ý nhưng chung chung hoặc không khớp kết quả (có Critical mà không dẫn sang plan).
- 2 — kết bằng gợi ý khớp kết quả và đúng sibling (`plan` khi cần fix), không tự fix.

## Gate (tiêu chí xương sống)

Tiêu chí **1, 2, 3** là xương sống. Bất kỳ cái nào = 0 → output review **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Lý do: một report bịa một gap (t3=0), hoặc gap không chỉ được chỗ nào (t2=0), hoặc toàn đề xuất fix thay vì gap thật (t1=0) — đều khiến người đọc tin nhầm hoặc không hành động được, nên vô giá trị dù các mục khác đẹp. Khi so nhiều bản: loại hết bản rớt gate trước, rồi mới xếp theo tổng.