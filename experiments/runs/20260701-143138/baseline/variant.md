# Baseline — giữ explain hiện tại

## editSummary
(giữ nguyên bản hiện tại)

## changedSections
(giữ nguyên)

## output (nguyên văn)
Mình đi theo mức của bạn (L3 — bạn đã hiểu entrypoint và happy path), nên mình dựng bản đồ luồng cho kỹ rồi mới điểm qua các phần. Chế độ: overview.

**Nó là cái gì (nói như cho người ngoài ngành)**
Đây là một cái "máy chạy việc" cho các trợ lý AI. Bạn giao cho nó một nhiệm vụ, nó tự suy nghĩ nhiều vòng, tự gọi công cụ (đọc/ghi file, chạy lệnh, tra cứu tài liệu), và khi cần thì giao bớt việc cho một trợ lý con — cho tới khi ra kết quả.

**Vấn đề nó sinh ra để giải — và cho ai**
Người xây các hệ trợ lý Ari kiểu này luôn sợ hai thứ: agent làm bậy (xoá nhầm file, chạy lệnh nguy hiểm, lộ bí mật), và khi máy chết giữa chừng thì mất sạch tiến độ. Người hưởng lợi là dev/đội kỹ thuật muốn dựng agent mà vẫn ngủ ngon: mọi hành động phải kiểm soát được, và chạy dở có thể chạy tiếp.

**Một ý tưởng cốt lõi**
Mẹo trung tâm rất đơn giản: bắt MỌI hành động ra thế giới bên ngoài đi qua đúng MỘT cái cửa. Không có cửa sau. Vì mọi thứ chui qua một chỗ, nên chỉ cần đứng gác ở cái cửa đó là kiểm soát được tất cả — ghi log, chặn lệnh cấm, đếm ngân sách, giới hạn quyền — mà không phải vá từng chỗ. Kể cả việc gọi chính mô hình AI cũng bị coi là "một công cụ" và cũng phải qua cửa đó.

**Bản đồ "bạn ở đây" — một task chạy từ đầu tới cuối (đây là cái để mọi chi tiết sau định vị)**

1. Bạn gọi vào một cửa công khai ổn định để bắt đầu (hoặc chạy tiếp) một task — lớp này là `orchestrator/loop.py`.
2. Nó chạy trên một sơ đồ trạng thái duy nhất (một graph biên dịch sẵn). Mỗi vòng, một chốt gác (`guard`) kiểm tra ngân sách trước: hết lượt thì dừng, còn thì đi tiếp.
3. Bước "suy nghĩ" (`agent`): hỏi mô hình AI xem làm gì tiếp, ép câu trả lời về đúng MỘT hành động dạng JSON.
4. Tuỳ hành động đó, nó rẽ sang một trong ba việc: chạy một công cụ, giao việc cho trợ lý con, hoặc kết thúc.
5. Đây là chỗ quan trọng nhất — cái cửa duy nhất mọi lời gọi AI và công cụ đều phải qua, code gọi là `execute_tool`. Trước khi chạy, nó kiểm tra công cụ này có nằm trong phạm vi quyền của phiên không, rồi cho đi qua một dãy lớp cắt ngang (đo giờ → chặn lệnh cấm → đếm ngân sách → thử lại → rút gọn kết quả).
6. Riêng "giao việc cho trợ lý con" (delegation) đi một cửa RIÊNG, cố ý tách khỏi cửa ở bước 5 — vì nó tạo ra cả một phiên con mới, chứ không chỉ là gọi một công cụ.
7. Khi định kết thúc, có một chốt chặn cuối: ví dụ đã sửa code mà chưa chạy kiểm tra thì chưa cho chốt "xong", đẩy quay lại làm tiếp.
8. Sau MỖI bước, trạng thái được ghi vào một file SQLite của run đó. Đây mới là "sự thật" để chạy tiếp: máy chết giữa chừng, gọi lại là đọc từ SQLite dựng lại đúng chỗ đang dở.

Để ý cách hai cái cửa phục vụ đúng nỗi sợ ban đầu: cửa ở bước 5 làm cho "agent làm bậy" thành chuyện gác một chỗ; SQLite ở bước 8 làm cho "chết giữa chừng mất tiến độ" biến mất.

**Các phần chính (mỗi phần là một bước ở bản đồ trên)**
- `core/` — cái lõi: chứa đúng cái cửa `execute_tool` (bước 5) và tách bạch giữa phần dùng chung đông cứng (kernel) với trạng thái riêng của từng run (session). Đây là chỗ "gác cửa" sống.
- `graph/` + `orchestrator/` — cái sơ đồ trạng thái và cửa công khai run/resume (bước 1–2, 8). SQLite checkpoint nằm ở đây.
- `middleware/` + `safety/` — các lớp cắt ngang quàng quanh cửa (bước 5): chặn lệnh cấm, đếm ngân sách, và nhốt thao tác file trong đúng thư mục làm việc.
- `discipline/` — luật kỷ luật dùng chung: ép câu trả lời về JSON (bước 3) và chốt chặn kết thúc (bước 7).
- `delegation/` (+ `supervisor/`) — cái cửa riêng cho việc giao trợ lý con (bước 6).
- `llm/`, `toolbox/`, `rag/`, `observability/` — các công cụ cụ thể chui qua cửa: gọi mô hình, thao tác file/terminal, tra cứu tài liệu, và ghi log mọi thứ đã qua cửa.

Ở mọi tầng, câu chuyện vẫn là một: một cửa để kiểm soát, một nguồn sự thật để chạy tiếp.

Bạn đang ở L3. Bạn muốn mình đi sâu vào trách nhiệm từng phần (ví dụ `core/` chia kernel với session thế nào), hay có một module cụ thể bạn đang thắc mắc?
