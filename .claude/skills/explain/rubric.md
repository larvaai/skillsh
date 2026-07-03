# Rubric — 7 tiêu chí chấm một câu `explain`

Mỗi tiêu chí 0/1/2. Khung chung: `grade/meta-rubric.md`. Chuẩn gốc để chấm: `explain/SKILL.md` (bảng mức L0–L8 + 3 chế độ) và `explain/rule/principles.md` (cách nói). Rubric chỉ biến hợp đồng đó thành thước đo được — KHÔNG thêm tiêu chuẩn mới.

**Đầu vào để chấm (fixture):** project (codebase bản explain đang nói tới, để kiểm bịa) · level (L0–L8 bản explain phải bám) · mode (overview/flow/why) · output (nguyên văn câu trả lời).

Tiêu chí **1 (Mức), 4 (Lời văn), 5 (Bám code)** là **xương sống (gate)**.

## 1. MỨC — bám đúng mức user (xương sống)

Bản explain nói đúng độ sâu và đúng loại từ ngữ cho `level`.

- 0 — sai mức rõ: dùng tên code/thuật ngữ dưới ngưỡng cho phép (L0–L1 mà nhắc tên hàm/file), hoặc quá sơ sài / quá sâu so với mức. Dùng code name khi level < L4 → tiêu chí này 0.
- 1 — đúng mức phần lớn, lệch nhẹ 1–2 chỗ.
- 2 — khớp mức: đúng từ ngữ, đúng độ sâu, đúng hành vi mức (L4 trả thẳng như đồng nghiệp; L2 nhắc entrypoint + luồng chính, tên module chỉ như gợi ý; L5–L8 trả ngắn rồi hand off).

## 2. CHẾ ĐỘ — đúng việc của mode

- 0 — sai chế độ: hỏi *why* mà đi giải thích *how*; hỏi *flow* mà đổ một cục không theo bước.
- 1 — đúng chế độ nhưng lẫn: flow không dừng từng bước; overview thiếu "cho ai / vì sao tồn tại"; why lẫn sang cách hoạt động.
- 2 — trọn vẹn: overview nói app làm gì + cho ai + vì sao tồn tại; flow đi từng bước, dừng chờ xác nhận; why kết bằng "quan trọng hay bỏ qua được + lý do".

## 3. ĐỦ Ý — không cắt ý cốt lõi

- 0 — thiếu ý quan trọng: đọc xong vẫn không nắm được điều cốt lõi của phần được hỏi.
- 1 — đủ ý chính, thiếu 1 mảnh phụ.
- 2 — đủ ý cho đúng phạm vi câu hỏi, không thừa không thiếu. Ngắn gọn là hình thức — thiếu ý không được tính là "gọn".

## 4. LỜI VĂN — dễ đọc theo gu project (xương sống)

Theo `principles.md`: câu ngắn, phẳng, đơn giản hoá hình thức chứ không đơn giản hoá nội dung.

- 0 — dày đặc / học thuật, tường bullet kèm trích số dòng, nhiều tầng cấu trúc → khó đọc.
- 1 — đọc được nhưng còn rườm hoặc thừa định dạng.
- 2 — câu ngắn, phẳng, dễ đọc; chỉ dùng list/tiêu đề/đậm khi giúp; không trích số dòng vô ích.

## 5. BÁM CODE — không bịa (xương sống)

- 0 — có claim bịa: nhắc file/API/hành vi không có trong code. Bất kỳ claim bịa nào → tiêu chí này 0.
- 1 — đúng phần lớn nhưng 1 chỗ suy đoán/mơ hồ không gắn nhãn.
- 2 — mọi claim khớp code thật; chỗ chưa chắc được gắn nhãn "chưa chắc". Trích dẫn code chỉ khi level ≥ L4, và phải trích đúng.

## 6. RANH GIỚI — đúng vai explain

- 0 — làm việc skill khác: dựng `.ai-understanding/` (atlas), đào data-flow/side-effect sâu (trace), liệt gap/edge case (review), phán giữ-sửa-xoá (triage).
- 1 — chủ yếu đúng vai, lấn nhẹ.
- 2 — đúng vai: dạy người hiểu theo mức; ở L5–L8 thì trả ngắn rồi hand off đúng sibling.

## 7. KẾT — gợi ý bước tiếp đúng mức

- 0 — không có gợi ý, hoặc gợi ý sai mức / sai skill.
- 1 — có gợi ý nhưng lệch mức hoặc chung chung.
- 2 — kết bằng gợi ý đúng mức; L5–L8 hand off đúng sibling kèm câu hỏi định hướng.

## Gate (tiêu chí xương sống)

Tiêu chí 1, 4, 5 là xương sống. Bất kỳ cái nào = 0 → bản explain **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 12/14 nhưng bịa code (tiêu chí 5 = 0) vẫn rớt — vì người đọc sẽ tin nhầm. Gate quan trọng hơn tổng: khi so nhiều bản, loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Khung report (xếp nhiều bản cạnh nhau)

```
CHẤM: explain · <project> · <level> · <mode>
1 Mức        [n] — <lý do 1 câu>
2 Chế độ     [n] — <...>
3 Đủ ý       [n] — <...>
4 Lời văn    [n] — <...>
5 Bám code   [n] — <...>
6 Ranh giới  [n] — <...>
7 Kết        [n] — <...>
TỔNG: <n>/14   GATE: <đạt | rớt: tiêu chí ...>
SỬA TRƯỚC TIÊN: <một câu — đòn bẩy lớn nhất>
```

## Vì sao 7 tiêu chí này

Bốn cái đầu đo *câu trả lời có đúng cái explain hứa không* (mức, chế độ, đủ ý, cách nói). Ba cái sau đo *có trung thực và đúng vai không* (bám code, ranh giới, kết). Gộp lại = toàn bộ hợp đồng của explain, không hơn. Thêm tiêu chí thứ 8 chỉ khi có một kiểu lỗi thật lặp lại mà 7 cái này không bắt được.
