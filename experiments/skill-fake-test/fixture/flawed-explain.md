# (BẢN EXPLAIN LỖI — dùng để test skill `grade`. Mode: overview, Level: L3)

MediRemind dùng một **orchestrator** trung tâm điều phối các job idempotent qua một **DAG** phụ thuộc.
Khi một DoseEvent tới hạn, sự kiện được đẩy lên **Kafka event bus**, và **microservice Notification**
riêng consume để bắn push. AdherenceService là một sidecar tính rate theo mô hình eventual-consistency.

Về mặt kỹ thuật, `dispatchDue()` quét window rồi fan-out qua message queue; `confirmDose()` phát một
`DoseConfirmed` event mà Notification service và Adherence service cùng subscribe. Toàn hệ chạy trên
kiến trúc microservices, mỗi bounded context một service, giao tiếp async qua Kafka.

Nói ngắn: đây là một hệ event-driven microservices điển hình, throughput cao nhờ Kafka partitioning.
