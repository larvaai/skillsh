# Quy ước chung — luật bất biến của MediRemind

Mọi skill trong project này tuân đúng các luật dưới. Vi phạm là bug, không phải lựa chọn phong cách.

## 1. Một file một chủ

Mỗi file state có đúng một skill được GHI; skill khác chỉ ĐỌC. Đọc chéo thoải mái, ghi chéo là cấm.

```
progress/progress.json         chủ: progress    (đồ thị task + con trỏ resume)
progress/checkpoints/<id>.md   chủ: checkpoint  (phiếu đạt từng bước)
constitution/*.md              chủ: charter     (gieo một lần; sau đó chỉ sửa tay)
problem/ idea/ docs/ codebase/ chủ: skill giai đoạn sở hữu artifact đó (xem folders.md)
state/current.json             dùng chung       (con trỏ project đang mở)
```

## 2. Gate là dữ liệu, không phải lời kể

Kết thúc một bước phải để lại trạng thái máy đọc được, không phải câu văn "đã xong". Chuỗi cổng: artifact sinh ra → `checkpoint` cấp phiếu `PASS`/`FAIL` → `progress` lật task `done` và mở khóa phụ thuộc. Người ký GO/NO-GO ở các cổng đậm (live slice GĐ8, release GĐ13). AI chuẩn bị đủ để ký, không tự ký thay. Với MediRemind, cổng GĐ13 cần đủ 2 chữ ký CTO + PO — chưa đủ thì cổng chưa qua.

## 3. .md cho người, .json cho máy

Mỗi giai đoạn để lại một cặp: file `.md` cho người đọc, và trạng thái `.json` cho máy đọc (dashboard, resume). `progress.json` chỉ chứa dữ liệu; diễn giải nằm ở `board.md`.

## 4. Hợp đồng nạp-ngữ-cảnh (mọi skill làm ở Bước 0)

Trước khi làm bất cứ gì, mọi skill đọc theo thứ tự: `constitution/` (luật) → `progress/progress.json` (đang ở đâu, con trỏ, task nào mở) → artifact liên quan trong `problem`/`idea`/`docs`/`codebase`. Không hỏi lại điều đã có trong các file này. `resume` là bản in-ra-màn-hình của bước này cho người.

## 5. Giọng và nhịp hỏi

Tiếng Việt. Dùng khối `═══ ... ═══` cho output có cấu trúc; metadata tiến độ để ở dòng nội dung, không nhét vào dòng tiêu đề. Mỗi lượt hỏi tối đa 3 câu cùng một cụm chủ đề, ưu tiên AskUserQuestion, hỏi cụm đòn-bẩy-cao trước. Câu ngắn, từ dễ, bỏ chữ thừa — nhưng không cắt ý.

## 6. Không tự kill, không tự build

Ý tưởng chưa khả thi thì phản biện xây dựng + giữ hạt giá trị; chỉ user mới quyết kill. Chưa qua cổng thì không nhảy vào code. Cấm câu phủ-định-cứng ("không thể", "sai rồi") — luôn kèm một lối đi tiếp.

## 7. Mỗi quyết định lớn ghi lý do + phương án đã loại

Để sau này audit lại vì sao chọn hướng này. Từ GĐ6 trở đi (kiến trúc, stack, module) bắt buộc kèm `rationale` + `rejected_alternatives`. Ví dụ đã ghi: modular monolith (loại microservices vì đội nhỏ). Hai open-question kiến trúc/dữ liệu còn treo (OQ-A queue-vs-cron, OQ-B retention) phải đóng bằng ADR, không bỏ lửng.

## 8. Dữ liệu sức khoẻ là nhạy cảm (luật riêng MediRemind)

Dữ liệu thuốc + liều là dữ liệu sức khoẻ. Mọi truy cập của caregiver phải qua kiểm quyền (view-only scope) và ghi audit-log (NFR-4). Mã hoá at-rest bắt buộc. Không skill nào được nới lỏng luật này để "đi cho nhanh".
