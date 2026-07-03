# Product Brief — HexAgent (GĐ2 WHAT VALUE)

## User + journey
- **User:** dev/đội tích hợp một agent tự-điều-phối vào hệ của họ.
- **AS-IS:** viết orchestrator thủ công, tự chế vòng lặp + tự chế điều kiện dừng → dễ sai, khó audit, dễ runaway.
- **TO-BE:** giao một `Task` + tiêu chí nghiệm thu → hệ tự plan/delegate/finish, trả trạng thái terminal + evidence + nhật ký tua-lại-được.

## MVP (cắt lát mỏng nhất có giá trị)
Giao một task 2 bước → agent tự lập plan → delegate 1 sub-agent → **nghiệm thu bằng evidence thật** → FINISHED, với budget/guard chặn runaway. (Chính là live-slice GĐ8.)

## Cố tình KHÔNG làm (out-of-scope MVP)
- UI điều khiển realtime (Control Tower) — pha sau (E21).
- RAG / knowledge base — mặc định tắt.
- Catalog role/department phức tạp — bắt đầu bằng vài role tối thiểu.
- Nới-ngân-sách-động do LLM tự quyết — giữ META-cap cứng, để pha sau.
