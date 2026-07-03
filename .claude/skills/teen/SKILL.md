---
name: teen
description: "Giải thích một đoạn code khó bằng ngôn ngữ đời thường, không cần biết code. Dùng khi người dùng paste một đoạn code và muốn hiểu nó đang làm gì mà không cần học lập trình. Chạy theo kỹ thuật Feynman: vấn đề trước, giải pháp sau, logic bằng lời nói."
---

# Teen — Giải thích code bằng lời thường

Mọi đoạn code, dù rắm rối đến đâu, đều đang giải quyết một vấn đề cụ thể. Skill này tìm vấn đề đó và kể lại bằng ngôn ngữ bất kỳ ai cũng hiểu — không cần biết code là gì.

## Quy tắc cứng
- Không dùng tên kỹ thuật trong lời giải thích (function, loop, variable, class, method, array... đều cấm).
- Nếu buộc phải nhắc tên kỹ thuật: giải thích nó là gì trước, chỉ nhắc một lần.
- Không giải thích "code này làm gì từng dòng" — giải thích "vấn đề này là gì và đoạn code giải quyết nó thế nào".
- Nếu có thể chạy thử trong đầu: chạy bằng lời nói, đừng dùng ký hiệu code.
- KHÔNG dùng analogy, ví dụ thay thế, hay câu chuyện ngoài context của project. Giải thích bằng chính những gì project đang làm — chỉ đơn giản hóa từ ngữ, không thay bằng tình huống khác.

## Quy trình

### Bước 1 — Đọc code, tìm vấn đề

Đọc toàn bộ đoạn code. Không giải thích ngay. Hỏi mình: *"Đoạn này đang giải quyết vấn đề gì trong project này?"*

Nếu code quá dài hoặc nhiều phần: hỏi người dùng muốn hiểu phần nào trước.

### Bước 2 — Nêu vấn đề trước

Một câu, không có từ kỹ thuật:

> "Đoạn code này giải quyết vấn đề: **[mô tả vấn đề đời thực]**."

Ví dụ tốt: "Đoạn này lo việc: lọc thông tin nhạy cảm trước khi hiện lên màn hình."
Ví dụ tệ: "Giống như người gác cổng kiểm tra khách trước khi vào." ← đây là analogy, không dùng.

### Bước 3 — Giải thích thẳng bằng context thật của project

Không dựng ví dụ thay thế. Dùng chính những gì project đang làm — chỉ thay từ kỹ thuật bằng từ bình thường:

> Ví dụ: thay vì nói "EventBus publish đến subscriber" → nói "agent hô lên, ai đang nghe thì nghe"
> Thay vì "EventEmitter validate và redact" → nói "emitter kiểm tra tin hợp lệ không, che thông tin nhạy cảm, rồi mới cho hiện lên màn hình"

Giải thích flow thật của project theo ngôn ngữ thường, theo đúng thứ tự xảy ra. Người dùng đã biết context — họ chỉ cần từ ngữ đơn giản hơn, không cần câu chuyện mới để hình dung.

### Bước 4 — Chạy bằng lời nói

Đi qua flow thật của project theo đúng thứ tự xảy ra, bằng câu bình thường. Không dùng ký hiệu code, dấu ngoặc, hay tên biến:

> "Agent vừa gọi xong một tool. Nó báo lên: 'tôi vừa gọi tool X, kết quả là Y.'
> EventLogger đang nghe — chép ngay vào file, kể cả thông tin nhạy cảm nếu có.
> Emitter không nghe được vì chưa ai nối dây tới nó.
> Màn hình user vẫn trống — không phải lỗi, chỉ là đường nối chưa được xây."

### Bước 5 — Một câu kết

Một câu tóm tắt tại sao chuyện này quan trọng — dùng đúng context của project, không trừu tượng:

> "Không phải hệ thống bị hỏng — mà hai phần hoạt động tốt riêng lẻ, chỉ chưa có ai nối chúng lại với nhau trong trường hợp này."

### Bước 6 — Gợi ý

Hỏi theo những gì vừa giải thích:
- *"Bạn muốn tôi chạy thử với một ví dụ khác không?"*
- *"Có phần nào bạn vẫn chưa hình dung được không?"*
- *"Bạn muốn biết đoạn này được dùng ở chỗ nào trong project không?"* → gợi ý skill `explain` hoặc `trace`.
