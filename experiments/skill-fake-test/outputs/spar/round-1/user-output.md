Nguyên nhân gửi lặp: thường do hệ thống retry khi gửi notification bị lỗi mạng.
Gửi xong nhưng không nhận được xác nhận, nên nó gửi lại. Ngoài ra nếu có nhiều
server chạy job nhắc thì mỗi server có thể tự bắn một cái.

Cơ chế đảm bảo một lần: mỗi liều thuốc sinh ra một mã reminder riêng (theo
user + thuốc + khung giờ). Trước khi gửi thì kiểm tra trong DB xem mã đó đã gửi
chưa, gửi rồi thì bỏ qua. Như vậy dù retry mấy lần cũng chỉ đi một cái.

Đánh đổi: phải ghi và tra DB thêm một bước nên chậm hơn tí và tốn chỗ lưu.
Trường hợp vẫn cần nhắc lại: khi người dùng bấm "báo lại sau" (snooze) thì mình
cố ý nhắc lại, cái đó không tính là gửi lặp.
