## 1. Nguyên nhân gốc

Gửi lặp gần như luôn là hệ quả của việc gửi thông báo KHÔNG phải thao tác
idempotent (bắn lại thì ra thêm một cái). Ba nguồn thường gặp:

- Retry mù: job gửi xong nhưng mất kết nối trước khi nhận "đã gửi", nên retry
  bắn lại. Bản thân gửi thành công rồi.
- Nhiều worker cùng nhặt một liều: scheduler chạy nhiều instance, cùng quét ra
  cùng một liều đến hạn, mỗi instance gửi một cái (thiếu khoá giành việc).
- Job chạy trùng lịch: cron/scheduler bị trigger hai lần (deploy chồng, đồng hồ
  lệch, at-least-once của hàng đợi) nên cùng một liều vào hàng hai lần.

Điểm chung: hệ ở mức "at-least-once", còn người dùng cần "exactly-once nhìn
thấy". Chênh đó là chỗ sinh lặp.

## 2. Cơ chế mỗi liều nhắc đúng một lần

Dùng khoá idempotency ở tầng lưu, không dựa vào "gửi cẩn thận":

1. Định danh mỗi lần nhắc bằng một khoá tất định: `user_id + med_id +
   scheduled_at` (khung giờ ĐÃ chuẩn hoá về UTC, không phải thời điểm gửi thực).
   Cùng một liều thì mọi worker sinh ra đúng cùng một khoá.
2. Trước khi gửi, ghi khoá đó vào một bảng `sent_reminders` bằng INSERT có ràng
   buộc UNIQUE (hoặc `INSERT ... ON CONFLICT DO NOTHING`). Ai INSERT được (0→1)
   thì mới gửi; ai đụng UNIQUE thì bỏ, vì đã có người gửi/đang gửi.
3. Thứ tự an toàn: claim trước (ghi khoá, trạng thái `sending`) → gửi → cập nhật
   `sent`. Nếu gửi lỗi và cần retry, retry đọc lại chính khoá đó, không tạo khoá
   mới, nên retry mấy lần cũng chỉ đọc ra một bản ghi.

Mấu chốt là tính duy nhất được DB cưỡng chế (UNIQUE), không phải do code nhớ.
Retry, đa worker, job trùng — cả ba đều va vào cùng ràng buộc và bị chặn.

## 3. Đánh đổi và ngoại lệ có chủ đích

Đánh đổi:
- Thêm một vòng ghi/tra DB mỗi lần gửi (chi phí nhỏ, nhưng có).
- Bảng khoá phình theo thời gian → cần TTL/dọn bản ghi cũ.
- Nếu claim `sending` rồi worker chết trước khi gửi, liều đó có thể bị "kẹt" và
  KHÔNG bao giờ gửi. Nên cần timeout: bản ghi `sending` quá hạn được phép gửi
  lại — tức chấp nhận nghiêng nhẹ về "thà lặp hiếm còn hơn bỏ liều thuốc", vì với
  app y tế bỏ nhắc nguy hiểm hơn nhắc dư.

Trường hợp vẫn cần nhắc lại có chủ đích:
- Snooze / "báo lại sau": người dùng chủ động xin nhắc lần nữa → đó là một lần
  nhắc MỚI, mang khoá mới (thêm hậu tố lần snooze), không phải gửi lặp.
- Escalation khi chưa xác nhận uống: nếu sau X phút chưa ai bấm "đã uống", nhắc
  lại (hoặc báo người thân) là hành vi cố ý, cũng mang khoá riêng.
Ranh giới: lặp = cùng khoá bắn hai lần (lỗi); nhắc lại hợp lệ = khoá khác (tính
năng). Cơ chế trên chỉ chặn cái đầu, không đụng cái sau.
