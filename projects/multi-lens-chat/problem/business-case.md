# Business Case — multi-lens-chat (GĐ1)

## Vấn đề & ai đau
Người đau: chính chủ dự án, khi review code/thiết kế một mình. Một người nhìn thường bám một góc (kỹ thuật) và bỏ sót các góc khác — rủi ro bảo mật, trải nghiệm người dùng, giá trị business. Sót góc nhìn = lỗi lọt qua hoặc quyết định lệch.

## Vì sao là bây giờ
Đang muốn học kỹ thuật multi-agent orchestration (fan-out song song + tổng hợp), và có sẵn một bài toán thật để làm ca đầu: review đa góc nhìn. Học bằng một công cụ mình dùng thật thì động lực bền hơn học chay.

## Giá trị (thô)
Không cần ROI hình thức — đây là dự án cá nhân. Giá trị gồm hai phần: (1) học được pattern orchestrator + N worker song song, (2) có một công cụ review đa lens dùng thật. Altitude nhẹ: không stakeholder ngoài, không business case nặng.

## Chi phí (thô)
Nhỏ — một mình build, không deadline ngoài. Ẩn số chính nằm ở kỹ thuật (streaming, cách tổng hợp), sẽ lộ dần từ PRD → Domain → Architecture.

## Quyết định đã chốt
- NEED-1 (confirmed): xây multi-lens-chat, dùng cá nhân, ca đầu là review code đa lens.
- CASE-1 (confirmed): bỏ ước lượng ROI/ngân sách hình thức; giá trị = học + công cụ dùng thật.

Success metric đo được thuộc GĐ2–4 (PRD), đang chốt ở `prd.md`.
