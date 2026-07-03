# Rubric — chấm chung một bản trả lời

Dùng cho cả bản của bạn và bản của Claude, cùng một thước. Khung chung: `grade/meta-rubric.md`. Mỗi tiêu chí 0/1/2. Chấm theo phạm vi câu hỏi trong `prompt.md`, không theo một chuẩn tự nghĩ ra. Nếu `prompt.md` có dán tiêu chí riêng ở dòng `rubric:` thì theo tiêu chí đó thay cho rubric này.

**Đầu vào để chấm (fixture):** `prompt.md` (phạm vi câu hỏi + dòng `rubric:` nếu có) · `user-output.md` và/hoặc `claude-output.md` (bản cần chấm).

## 1. ĐÚNG — không sai, không bịa (xương sống)

Claim đúng sự thật, đúng câu hỏi. Chỗ chưa chắc phải gắn nhãn "chưa chắc".

- 0 — có claim sai hoặc bịa: nói một điều không đúng, hoặc dựng ra dữ kiện/nguồn không có. Một claim bịa là đủ 0.
- 1 — đúng phần lớn, một chỗ suy đoán không gắn nhãn.
- 2 — mọi claim đúng hoặc gắn nhãn rõ mức chắc chắn.

## 2. ĐỦ Ý — trả đủ phạm vi câu hỏi

- 0 — thiếu ý cốt lõi: đọc xong vẫn chưa trả lời được câu hỏi.
- 1 — đủ ý chính, thiếu một mảnh phụ.
- 2 — đủ cho đúng phạm vi, không thừa không thiếu. Thiếu ý không được tính là "gọn".

## 3. LẬP LUẬN — có cơ sở, không phán suông

- 0 — kết luận không kèm lý do, hoặc lý do không dẫn tới kết luận.
- 1 — có lý do nhưng mỏng hoặc nhảy bước.
- 2 — mỗi kết luận có cơ sở dẫn được, người đọc theo được đường đi.

## 4. RÕ — dễ đọc (xương sống)

Câu ngắn, phẳng, đơn giản hoá hình thức chứ không đơn giản hoá nội dung.

- 0 — dày đặc, vòng vo, hoặc tường bullet khó nắm.
- 1 — đọc được nhưng còn rườm hoặc thừa định dạng.
- 2 — câu ngắn, phẳng, dễ đọc; chỉ dùng list/đậm khi giúp.

## 5. TRỌNG TÂM — không lạc đề

- 0 — trả lời chuyện khác, hoặc chèn nhiều thứ ngoài câu hỏi.
- 1 — bám đề nhưng có đoạn lan man.
- 2 — bám đúng câu hỏi từ đầu tới cuối.

## Khung report

```
CHẤM: spar · <prompt-slug> · <bản: user | claude>
1 Đúng       [n] — <lý do 1 câu>
2 Đủ ý       [n] — <...>
3 Lập luận   [n] — <...>
4 Rõ         [n] — <...>
5 Trọng tâm  [n] — <...>
TỔNG: <n>/10   GATE(1,4): đạt / rớt ở <tiêu chí>
SỬA TRƯỚC TIÊN: <một câu — đòn bẩy lớn nhất>
```

## Gate

Tiêu chí **1 (Đúng)** và **4 (Rõ)** là xương sống. Bất kỳ cái nào = 0 → bản đó **rớt gate** dù tổng cao: một câu trả lời sai/bịa gây hại hơn câu vụng-nhưng-đúng (crit 1 phủ A1+A2), và một câu không đọc được thì không học được gì từ nó (crit 4 phủ A3 — đúng yêu cầu meta-rubric là trục đọc-được phải nằm trong gate). Khi so hai bản: loại bản rớt gate trước, rồi mới xếp theo tổng.

## Vì sao 5 tiêu chí này

Ba cái đầu đo *nội dung có đáng tin và đủ không* (đúng, đủ ý, lập luận). Hai cái sau đo *có đọc được và bám đề không* (rõ, trọng tâm). Gộp lại đủ để chấm một câu trả lời bất kỳ mà không phụ thuộc chủ đề. Thêm tiêu chí thứ 6 chỉ khi một kiểu lỗi thật lặp lại mà 5 cái này không bắt được.
