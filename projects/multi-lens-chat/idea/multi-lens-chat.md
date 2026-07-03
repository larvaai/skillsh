# Idea — multi-lens-chat

## Bức tranh mơ hồ (lời văn)
"Mình muốn một chat mà khi mình hỏi hay dán một đoạn code vào, không chỉ một AI trả lời, mà có mấy trợ lý nền cùng soi — một đứa soi kỹ thuật, một đứa soi rủi ro, một đứa soi business, một đứa soi UX — rồi gộp lại cho mình thấy các góc mình hay bỏ sót." Biết ngay chưa build được luôn: chưa rõ lens cố định hay tự định, chưa rõ streaming hay chờ, chưa rõ ai tổng hợp.

## Làm rõ thành plan
- **Input:** một đơn vị cần soi — câu hỏi, đoạn code, hoặc mô tả thiết kế.
- **Output:** nhiều insight (mỗi lens một góc) + một bản tổng hợp/hiển thị.
- **Cơ chế thô:** orchestrator nhận input → fan-out tới N lens worker chạy song song → mỗi worker trả insight theo lens của nó → orchestrator gom lại (lọc hoặc show hết).
- **Ẩn số lớn nhất:** ba câu OQ-4/5/6 (lens cố định?, streaming?, tổng hợp?) — quyết hình hài kỹ thuật, phải chốt trước Domain.

## Vì sao đáng đi tiếp
Đây đúng là bài toán fan-out + tổng-hợp của multi-agent orchestration — chính là thứ project sinh ra để học. Bản thân bộ skill workspace này (fanout) cũng là một hiện thân của cùng pattern.

## Router (lần gần nhất)
Độ rõ: mơ hồ ban đầu (chưa chốt MVP) → đang làm rõ ở PRD. Độ khả thi: khả thi rõ (không ẩn số chặn) → Nhánh C, đang ở GĐ2–4.

Trạng thái: đang đi tiếp. Bước kế: chốt OQ-4/5/6 → Domain (GĐ5).
