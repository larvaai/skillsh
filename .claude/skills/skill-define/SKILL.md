---
name: skill-define
description: "Cho một nhu cầu, liệt kê nhanh các trường hợp hay gặp và việc cần làm, để xem có đáng làm skill mới không. Dùng khi người dùng muốn tạo skill mới hoặc cân nhắc một nhu cầu có đáng đóng gói thành skill không. Tự đưa bản nháp ngay, không hỏi lại."
---

# Skill Define

Trước khi liệt case: nhu cầu có khả năng tạo nội dung độc hại, đánh lừa ý định người dùng, hay phục vụ truy cập trái phép/lấy cắp dữ liệu → dừng ở đây, nói rõ không nên làm skill, không liệt case bên dưới.

Nhận một nhu cầu → liệt ngay 3-5 trường hợp hay gặp nhất, chọn trường hợp thật sự hay gặp chứ không cố cho đủ số. Mỗi trường hợp một dòng, một câu ngắn — không đoạn văn, không giải thích thêm:

Trường hợp A -> làm gì
Trường hợp B -> làm gì
Trường hợp C -> làm gì

Sau danh sách, một dòng duy nhất: không có skill này thì bình thường làm sao. Đó là câu trả lời cho "có đáng làm skill không" — cách thường đã đủ nhanh/đủ tốt thì nói thẳng không cần skill.

Giống skill đã có trong `.claude/skills/` → nói luôn, có thể không cần skill mới.

Kết luận đáng làm skill mới → thêm một dòng cuối: dùng skill-creator để viết SKILL.md thật. Skill-creator đã tự lo mục lục cho reference dài, tránh overfit vào đúng ví dụ đã thấy, và khớp tên thư mục với tên skill — skill-define không viết SKILL.md thay.

Người dùng sửa/thêm case → cập nhật danh sách, giữ nguyên format trên. Không hỏi gì thêm ngoài việc xác nhận danh sách đúng chưa.
