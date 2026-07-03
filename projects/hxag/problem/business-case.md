# Business Case — HexAgent (GĐ1 WHY)

## Ai đau + đau ở đâu (một câu cụ thể)
Đội xây agent tự-chạy-nhiều-bước đau vì agent **báo-xong-khống** (nói "xong" khi chưa xong → giao kết quả sai) và **chạy-vô-hạn đốt tiền** (lặp gọi LLM/tool tới khi cạn ví), cả hai xảy ra ở chỗ **không quan sát được và không tua lại được**.

## Chi phí nếu không làm (ước lượng thô)
- Mỗi lần báo-xong-khống lọt xuống hạ nguồn = giờ người truy vết + niềm tin vào tự-động-hoá giảm.
- Runaway không chặn = chi phí LLM tăng phi tuyến, không có trần dự đoán được.
- Không audit-được = mỗi sự cố phải dựng lại thủ công "nó đã làm gì".

## Success metric (đo được)
- **M1 — zero-false-finish:** `false_finish_total = 0` (mọi lần FINISHED đều có evidence thật cho từng AC). Oracle: `is_satisfied` (status=passed ∧ evidence_ids≠∅).
- **M2 — bounded:** 100% run kết thúc ở trạng thái terminal trong ngân sách (không có run "treo" / vượt trần âm thầm).
- **M3 — no-escalation:** 0 lần sub-agent vượt scope cha (`delegation_rejected{scope}` chặn đúng).

## Cổng GĐ1: đáng đầu tư đi tiếp không?
GO — đau rõ, đo được bằng M1/M2/M3, và có tiền lệ chạy thật ở repo gốc để de-risk.
