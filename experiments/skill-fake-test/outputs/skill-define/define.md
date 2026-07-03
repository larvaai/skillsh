# skill-define: tự phát hiện reminder bị gửi lặp/flaky rồi cảnh báo

Nhu cầu: "muốn tự phát hiện reminder bị gửi lặp/flaky rồi cảnh báo"

Trường hợp A: cùng một reminder gửi 2+ lần cho một user trong khoảng ngắn -> gom log theo (reminder_id, user_id) trong cửa sổ thời gian, đếm >1 thì báo trùng
Trường hợp B: job scheduler chạy lại sau retry/crash làm gửi lại reminder đã gửi -> đối chiếu cờ đã-gửi (idempotency key/sent_at) trước khi cảnh báo, phát hiện gửi-lại-dù-đã-đánh-dấu
Trường hợp C: reminder lúc gửi lúc không giữa các lần chạy giống nhau (flaky) -> so tỉ lệ gửi thành công theo từng lần chạy job, tụt dưới ngưỡng thì cảnh báo
Trường hợp D: cùng nội dung tới qua nhiều kênh (email + push + SMS) bị người dùng coi là lặp -> gom theo nội dung/hash + user, vượt số kênh cho phép thì báo
Trường hợp E: tăng đột biến số reminder gửi trong một cửa sổ (bug loop) -> đếm tổng theo phút/giờ, vượt baseline thì cảnh báo sớm

Không có skill này thì bình thường làm sao: viết một query/cron nhỏ trên bảng log gửi reminder (GROUP BY reminder_id+user, đếm trùng, so ngưỡng) hoặc bật alert sẵn có của hệ log/monitoring (Grafana/CloudWatch) — với một hệ, cách này đã đủ nhanh và đủ tốt.

Trùng skill có sẵn: không có skill nào trong `.claude/skills/` làm việc này; gần nhất là `operate` (dựng ops dashboard + incident + metric sau release) và `review` (soi edge case/error path) nhưng cả hai không phải là bộ dò-lặp/flaky cho reminder.

Kết luận: CHƯA đáng làm skill mới. Đây là một rule dò trùng + một ngưỡng cảnh báo — một truy vấn log hoặc alert monitoring là xong, không cần đóng gói quy trình. Chỉ nên cân nhắc làm skill nếu việc này lặp lại trên NHIỀU loại thông báo/nhiều hệ với cùng một khuôn dò-lặp-rồi-cảnh-báo; khi đó dùng skill-creator để viết SKILL.md thật.
