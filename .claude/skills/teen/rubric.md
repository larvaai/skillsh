# Rubric — 6 tiêu chí chấm một câu `teen` (giải thích code bằng lời thường)

Mỗi tiêu chí 0/1/2. Khung chung: `grade/meta-rubric.md`. Chuẩn gốc để chấm: `teen/SKILL.md` (mục "Quy tắc cứng" + quy trình 6 bước theo kỹ thuật Feynman). Rubric chỉ biến hợp đồng đó thành thước đo được — KHÔNG thêm tiêu chuẩn mới.

**Đầu vào để chấm (fixture):** đoạn code được dán (nguyên văn, để kiểm bịa hành vi) · context project mà đoạn code thuộc về (nếu có, để kiểm "giải thích bằng chính việc của project") · phần người dùng muốn hiểu (nếu code dài, đã chọn phần nào) · output (nguyên văn lời giải thích).

Tiêu chí **1 (Feynman — vấn đề trước, đúng+đủ), 2 (Bám đoạn code, không bịa), 3 (Lời đời thường, không jargon)** là **xương sống (gate)** — phủ A1 / A2 / A3. Rớt bất kỳ cái nào → rớt cả bản dù tổng cao.

## 1. FEYNMAN — vấn đề trước, giải pháp sau, nắm được đoạn làm gì (xương sống · A1)

Mở bằng vấn đề đời thực (một câu, không từ kỹ thuật), rồi mới tới cách đoạn code giải quyết; đọc xong nắm được đoạn này LÀM GÌ, không phải diễn dòng-từng-dòng.

- 0 — không nêu vấn đề trước khi giải thích, HOẶC đi diễn "dòng này làm X, dòng kia làm Y" thay vì "vấn đề là gì và đoạn này giải quyết thế nào" (vi phạm Luật cứng #3), HOẶC đọc xong vẫn không biết đoạn code làm gì.
- 1 — có nêu vấn đề nhưng mờ/lẫn với giải pháp, hoặc nắm được ý chính mà thiếu một mảnh cốt lõi của việc đoạn code làm.
- 2 — mở đúng một câu vấn đề đời thực → giải thích cách giải quyết theo đúng thứ tự xảy ra → nắm trọn đoạn này làm gì; không diễn từng dòng.

## 2. BÁM ĐOẠN CODE — không bịa hành vi (xương sống · A2)

Mọi điều nói ra truy được về chính đoạn code được dán (và context project nếu có); không gán hành vi đoạn code không có, không suy diễn cái không nằm trong đoạn.

- 0 — có claim bịa: mô tả một hành vi/đường nối/kết quả mà đoạn code không hề làm; hoặc kể việc của phần khác project như thể đoạn này làm. Bất kỳ claim bịa nào → tiêu chí này 0.
- 1 — chủ yếu bám code, một chỗ suy đoán/mơ hồ không gắn nhãn (đoán một nhánh mà không nói rõ là suy đoán).
- 2 — mọi điều nói ra khớp đúng đoạn code; nếu "chạy thử trong đầu" thì kết quả đúng theo code; chỗ chưa chắc được nói rõ là chưa chắc, không ngụy tạo.

## 3. LỜI ĐỜI THƯỜNG — không jargon, không tên hàm/file như thuật ngữ (xương sống · A3)

Ngôn ngữ đời thường, người không biết lập trình đọc là hiểu; không dùng tên kỹ thuật (function, loop, variable, class, method, array...) trong lời giải; nếu buộc phải nhắc một tên kỹ thuật thì giải thích nó là gì trước và chỉ nhắc một lần.

- 0 — dùng tên kỹ thuật trần trong lời giải (nhắc "function/loop/array/class..." hoặc bê tên hàm/tên file/tên biến vào như thuật ngữ mà không đổi sang lời thường) — vi phạm Luật cứng #1; hoặc buộc phải nhắc một tên kỹ thuật mà không giải thích trước / nhắc lại nhiều lần (vi phạm Luật cứng #2); hoặc dùng ký hiệu code, dấu ngoặc, tên biến khi "chạy trong đầu" (vi phạm Luật cứng #4).
- 1 — chủ yếu là lời thường nhưng còn lọt 1–2 chỗ hơi kỹ thuật hoặc câu rối, vẫn đọc được.
- 2 — toàn bộ là lời đời thường, câu ngắn phẳng; không một tên kỹ thuật trần; nếu có nhắc một khái niệm kỹ thuật thì đã giải nghĩa trước, đúng một lần; chạy-trong-đầu bằng lời nói, không ký hiệu.

## 4. GIẢI THẲNG BẰNG VIỆC CỦA PROJECT — không analogy, không ví dụ thay thế (A4/Luật cứng #5)

Giải thích bằng chính những gì đoạn code / project đang làm, chỉ đơn giản hóa từ ngữ; KHÔNG dựng câu chuyện, người gác cổng, ví dụ thay thế hay tình huống ngoài context.

- 0 — dùng analogy / câu chuyện / ví dụ thay thế ngoài context project để giải thích ("giống như người gác cổng...", "hãy tưởng tượng một nhà hàng...") — vi phạm Luật cứng #5.
- 1 — chủ yếu bám việc thật của project nhưng lỡ chèn một hình ảnh ví von nhỏ không cần thiết.
- 2 — giải thích thuần bằng việc thật của đoạn code/project, chỉ thay từ kỹ thuật bằng từ thường; không một tình huống bịa nào.

## 5. ĐỦ-LÀ-ĐỦ + KHÔNG LẤN VAI — chỉ giải một đoạn, không cần người đọc biết code (A4)

Độ sâu vừa đúng đoạn được hỏi; không đòi người đọc biết lập trình; không lấn sang giải thích cả project (đó là `explain`) hay theo dấu data/side-effect (đó là `trace`); code dài thì hỏi muốn hiểu phần nào trước.

- 0 — bắt người đọc phải biết code mới hiểu được (giả định kiến thức lập trình); HOẶC phình sang giải thích cả kiến trúc/nhiều phần project thay vì đúng đoạn được dán (lấn `explain`); HOẶC code dài nhiều phần mà không hỏi muốn hiểu phần nào, đổ hết một cục.
- 1 — đúng phạm vi phần lớn, hơi thừa/thiếu độ sâu ở một chỗ hoặc lỡ giả định một chút kiến thức nền.
- 2 — đúng đúng đoạn được hỏi, đủ để hiểu mà không cần biết lập trình; code dài thì hỏi chọn phần trước; không lấn `explain`/`trace`.

## 6. KẾT — một câu chốt + gợi ý bước tiếp hợp lý (A5)

Chốt bằng một câu vì-sao-chuyện-này-quan-trọng (dùng context thật, không trừu tượng), rồi gợi ý bước tiếp; nếu người dùng muốn biết đoạn này dùng ở đâu trong project thì trỏ `/explain` hoặc `/trace`.

- 0 — không có câu kết cũng không có gợi ý nào; HOẶC gợi ý sai skill (tự nhận đi map cả project / đào side-effect thay vì trỏ `explain`/`trace`).
- 1 — có kết hoặc gợi ý nhưng cụt/chung chung, hoặc câu chốt còn trừu tượng thay vì bám context thật.
- 2 — một câu chốt bám context thật của project + gợi ý mở đúng ("muốn thử ví dụ khác không", "còn chỗ nào chưa hình dung"), và trỏ `explain`/`trace` khi hỏi "đoạn này dùng ở đâu".

## Gate (tiêu chí xương sống)

Tiêu chí **1 (Feynman — đúng+đủ), 2 (Bám code — không bịa), 3 (Lời đời thường)** là xương sống, phủ ba trục A1 / A2 / A3. Bất kỳ cái nào = 0 → bản **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 10/12 nhưng bịa một hành vi đoạn code không có (tiêu chí 2 = 0) vẫn rớt — vì người đọc không biết code sẽ tin nhầm; một bản mượt nhưng bê "function/array" vào lời giải (tiêu chí 3 = 0) cũng rớt — vì đã phản bội đúng lời hứa "không cần biết code". Khi so nhiều bản: loại hết bản rớt gate TRƯỚC, rồi mới xếp phần còn lại theo tổng.

## Khung report (xếp nhiều bản cạnh nhau)

```
CHẤM: teen · <đoạn code / fixture>
1 Feynman (vấn đề trước, đủ)   [n/2] — <lý do 1 câu>
2 Bám code (không bịa)         [n/2] — <...>
3 Lời đời thường (không jargon)[n/2] — <...>
4 Việc thật, không analogy     [n/2] — <...>
5 Đủ-là-đủ, không lấn vai      [n/2] — <...>
6 Kết + gợi ý                  [n/2] — <...>
TỔNG: <n>/12   ·   GATE: đạt / RỚT ở <tiêu chí ...>
SỬA TRƯỚC TIÊN: <một câu — đòn bẩy lớn nhất để bản này tốt hơn>
```

## Vì sao 6 tiêu chí này

Ba xương sống đo *có làm đúng lời hứa cốt lõi không*: giải thích theo Feynman (vấn đề trước, nắm được đoạn làm gì — A1), trung thực với đoạn code (không bịa — A2), và người không biết code đọc được (không jargon — A3). Ba cái sau đo *có giữ đúng ba Luật cứng còn lại và đúng vai không*: giải bằng việc thật của project chứ không analogy (Luật cứng #5), đủ-là-đủ không lấn `explain`/`trace`, và kết đúng. Sáu cái này gấp trọn 5 Luật cứng + 6 bước quy trình của `teen`, không hơn. Không cần tiêu chí thứ 7 tách "cổng/bàn giao" vì `teen` không có cổng ký và không sinh artifact pipeline — trục A5 thu về câu kết + gợi ý (tiêu chí 6). Thêm tiêu chí mới chỉ khi có một kiểu lỗi thật lặp lại mà sáu cái này không bắt được.
