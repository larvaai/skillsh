# B · Trigger mode

## editSummary
Sửa ở Bước 2 của explain/SKILL.md, ngay chỗ "Suy ra chế độ". Trước đây skill chỉ nói "suy ra chế độ từ cách diễn đạt" mà không liệt cụm từ nào kích mode nào, nên explain hay chọn nhầm (vd người hỏi "tại sao" nhưng bị kể overview). Tôi thêm một block liệt kê cụm KÍCH cho từng chế độ overview/flow/why — đúng cách skill review và teen mô tả trigger ("Kích bởi: ...") — và nói rõ: bắt được cụm nào thì chọn mode đó, không cụm nào rõ thì default overview. Với fixture mode=undefined (không có câu hỏi kèm cụm kích), quy tắc mới rơi về default overview, khớp câu "Nếu không chắc chế độ: mặc định overview" sẵn có.

## changedSections
Trong explain/SKILL.md, Bước 2 — Chọn chế độ và giải thích, đoạn mở đầu đổi từ:

"Suy ra chế độ từ cách người dùng diễn đạt. Có **ba** chế độ:"

thành:

"Suy ra chế độ từ cách người dùng diễn đạt. Mỗi chế độ có cụm từ KÍCH riêng — bắt được cụm nào thì chọn chế độ đó; không cụm nào rõ thì mặc định **overview**. Có **ba** chế độ:

```
overview — người hỏi muốn thấy toàn cảnh, chưa định vị được mình ở đâu.
           Kích bởi: "project này làm gì", "tổng quan", "cái này là cái gì", "giải thích giúp tôi repo này", "bắt đầu từ đâu", "kiến trúc thế nào"

flow     — người hỏi muốn theo một request/task chạy từ đầu vào tới đầu ra.
           Kích bởi: "luồng chạy thế nào", "chạy từ đâu tới đâu", "một request đi qua những gì", "gọi X thì sao", "đi qua từng bước", "happy path"

why      — người hỏi lý do TỒN TẠI của một phần, không hỏi cách nó chạy.
           Kích bởi: "tại sao cần X", "sao lại tách/có X", "X để làm gì", "bỏ X đi có được không", "vì sao thiết kế thế này"
```
"

(Các dòng "**overview** — người dùng muốn thấy toàn cảnh:" và phần mô tả ba chế độ phía dưới giữ nguyên. Câu cuối "Nếu không chắc chế độ: mặc định **overview**..." cũng giữ nguyên — block mới chỉ bổ sung, không thay nó.)

## output (nguyên văn)
Bạn đang ở L3 nên mình đi qua luồng chạy khá kỹ rồi chạm nhẹ vào các phần. Không có câu hỏi cụ thể kèm theo, nên mình kể toàn cảnh (overview).

Vấn đề nó giải, cho ai. Đây là bộ khung để dựng một hệ nhiều "agent AI" cùng làm việc — cho dev/team xây trợ lý tự động chạy nhiều bước (gọi model, đọc/ghi file, chạy lệnh, giao việc cho agent con). Cái đau khi tự xây kiểu này: mỗi chỗ trong code lại tự gọi model hay tự chạy tool theo cách riêng, thành ra không kiểm soát được — không log đồng nhất, không chặn được hành động nguy hiểm, và khi chạy nửa chừng bị dừng thì không biết đang ở đâu để chạy tiếp.

Ý tưởng cốt lõi. Mọi hành động ra-thế-giới-bên-ngoài (gọi model cũng tính là một hành động) đều phải đi qua đúng MỘT cái cửa. Vì chỉ có một cửa, nên chỉ cần đứng ở đó là log được hết, chặn được hết, đo được hết — không hành động nào lọt ra ngoài tầm nhìn. Đúng một ngoại lệ: việc giao-việc-cho-agent-con đi qua một cửa RIÊNG, cố ý tách ra để nó không lẫn với hành động thường.

Luồng một task chạy (đây là bản đồ "bạn ở đây"):
1. Một lời gọi vào từ facade run/resume ổn định (`orchestrator/loop.py`) — đây là đường vào bạn nên dùng.
2. Vào một đồ thị điều phối duy nhất đã biên dịch sẵn (LangGraph). Đồ thị chỉ lo "bước nào tới bước nào", không tự làm gì ra ngoài.
3. Trước mỗi lượt gọi model, một chốt chặn kiểm ngân sách (còn được chạy tiếp không, hay quá số bước cho phép rồi).
4. Bước "agent": gọi model, rồi ép câu trả lời của model về đúng MỘT hành động (một cổng JSON sửa/duyệt output). Model muốn gì cũng phải nói qua khuôn này.
5. Hành động đó rẽ về một trong ba: chạy một tool, giao việc cho agent con, hoặc kết thúc.
6. Cái cửa duy nhất — mọi lời gọi model và mọi tool đều chui qua đây. Code gọi nó là `execute_tool` (`core/kernel.py`). Đứng ở cửa này nó phát sự kiện (requested → completed/failed), kiểm phạm vi (tool này có nằm trong quyền của phiên không), chạy qua chuỗi middleware (đo giờ, chặn deny-list, chặn lặp, thử lại...). Kể cả model cũng chỉ là một "khả năng" tên `llm.chat`, không có đường tắt.
7. Nếu là giao-việc: đi cửa RIÊNG `delegate` (`delegation/manager.py`), không phải method của kernel — đây chính là lý do trong đồ thị có hẳn một node `delegate` tách bạch.
8. Khi kết thúc, một "finish gate" chặn lại nếu đã đổi code mà chưa chạy kiểm tra. Qua được thì task đóng, kết quả và checkpoint ghi xuống SQLite (`var/agent_runs/<run_id>/langgraph.sqlite`) — đây là nguồn sự thật để resume chạy tiếp.

Ở mỗi bước trên, giá trị vẫn là một: một cửa để nhìn-thấy-hết và kiểm-soát-hết, một nguồn sự thật để không mất dấu khi dừng giữa chừng.

Các phần chính (mỗi phần là một lớp trong luồng trên):
- `core/` — trái tim: cái cửa `execute_tool`, kernel dùng-chung-đóng-băng, và `session` giữ trạng thái của riêng từng lần chạy (một kernel chia sẻ, mỗi run một session).
- `graph/` + `orchestrator/` — đồ thị điều phối và facade run/resume + checkpoint SQLite.
- `delegation/` — cửa riêng để giao việc cho agent con, kèm luật về độ sâu và ngân sách.
- `discipline/` — các chốt dùng chung: cổng JSON, ngân sách vòng lặp, finish gate (dùng chung, không nhân bản mỗi nơi một bản).
- `control/` — lớp điều khiển thời gian thực đang làm dở: một đường phát sự kiện đã kiểm-tra + che-thông-tin-nhạy-cảm trước khi ra UI.
- `observability/` — ghi log sự kiện ra JSONL + tóm tắt, để soi lại một run.

Một lưu ý bám code: `control/` (E21) mới xong phần hợp đồng và EventEmitter, phần transport/UI còn dang dở — nên đừng coi lớp realtime này đã chạy đầy đủ.

Bạn đang ở L3. Bước tiếp mình gợi ý: mình giải thích kỹ trách nhiệm từng phần, hay có module cụ thể (vd cái cửa `execute_tool`, hay đường delegation) bạn đang thắc mắc muốn xem trước?
