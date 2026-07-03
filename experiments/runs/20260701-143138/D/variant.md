# D · Backbone overview

## editSummary
Chỗ sửa: chèn một mục mới "Xương sống overview — ba nhịp trước khi zoom" NGAY TRƯỚC "Thang PHÓNG TO (zoom)" trong explain/SKILL.md.
Vì sao: cho chế độ overview một xương sống nhẹ 3 nhịp (LÀM GÌ / CHO AI / VÌ SAO TỒN TẠI) làm kim chỉ nam định hướng đặt trước thang zoom, để câu trả lời không bao giờ chỉ có kỹ thuật mà quên giá trị (khớp gate Chế độ tiêu chí 2: "làm gì + cho ai + vì sao tồn tại"). Chốt rõ đây KHÔNG phải template bắt buộc điền, KHÔNG phải ba câu mở bài cứng — phải dệt vào Zoom 0–1 tự nhiên — nên không cứng hoá, không xung đột Luật neo. Sửa tối thiểu, không đụng phần còn lại của skill.

## changedSections
## Xương sống overview — ba nhịp trước khi zoom

Trước khi bước vào thang zoom, tự trả lời ba nhịp này cho chính project (đây là kim chỉ nam định hướng, KHÔNG phải template bắt buộc điền, KHÔNG phải ba câu mở bài cứng):

- **LÀM GÌ** — một câu đời thường: cái máy này làm việc gì.
- **CHO AI** — ai là người hưởng lợi / người dùng thật.
- **VÌ SAO TỒN TẠI** — vấn đề gốc khiến nó phải sinh ra (không có nó thì đau ở đâu).

Ba nhịp này là cái xương để câu chuyện overview treo vào — nó bảo đảm câu trả lời không bao giờ chỉ có kỹ thuật mà quên mất giá trị. Dệt chúng vào lời kể tự nhiên qua Zoom 0–1 (và nhắc lại "cho ai / vì sao" ở mỗi tầng — Luật neo #3), đừng liệt kê thành ba gạch đầu dòng dán lên đầu câu trả lời.

(Mục này được chèn ngay TRƯỚC tiêu đề sẵn có "## Thang PHÓNG TO (zoom) — khung kể của chế độ overview".)

## output (nguyên văn)
Nói gọn một câu: đây là một bộ khung để chạy "nhân viên AI" — bạn giao một việc, nó tự suy nghĩ, tự gọi công cụ, tự làm tới khi xong hoặc bỏ cuộc. Người hưởng lợi là dev dựng agent muốn một cái lõi gọn, chạy lại được, quan sát được — thay vì một mớ lời gọi LLM rải khắp nơi. Nó tồn tại vì cái đau lớn nhất của loại hệ này là mất kiểm soát: LLM gọi lung tung, không đếm được chi phí, chết giữa chừng không chạy tiếp được. Cả project xoay quanh một mẹo để trị cái đau đó — mọi hành động ra ngoài (gọi LLM hay gọi tool) đều phải chui qua đúng MỘT cái cửa, nên chỗ nào cũng đo được, chặn được, ghi lại được.

Giờ nhìn một việc chạy từ đầu tới cuối, đây là bản đồ "bạn đang ở đây":

1. Có người giao việc — qua facade `orchestrator.run/resume`, hoặc UI, hoặc smoke test.
2. Việc chạy trên đúng một đồ thị đã biên dịch (một "substrate" LangGraph dùng chung). LangGraph chỉ lo điều phối; cái lõi không hề biết tới nó.
3. Trước mỗi lượt nghĩ, có một chốt chặn ngân sách — node `guard`: hết số bước cho phép thì cho `fail` luôn, khỏi cháy tiền.
4. Node `agent` hỏi LLM một câu, ép model trả về JSON và chỉ lấy đúng MỘT hành động (cái "cổng JSON" của `discipline/`): hoặc gọi tool, hoặc giao việc con, hoặc kết thúc.
5. Node `tool` chạy công cụ đó, gói kết quả thành một phong bì chuẩn (envelope) rồi nối lại vào hội thoại, quay về `guard` cho lượt sau.
6. Nếu model chọn giao việc, node `delegate` đẩy sang một cái cửa RIÊNG (`DelegationServicePort.delegate`, hiện thực ở `delegation/manager.py`) — cố ý tách khỏi cửa chính, nên delegation có node riêng.
7. Khi model nói "xong", node `finish` áp một "cổng kết thúc" dùng chung: đổi code mà chưa validate thì chưa cho xong, đẩy ngược về làm tiếp; đạt thì đóng task, END.
8. Suốt đường đi, mỗi transition ghi checkpoint vào SQLite — đó là nguồn sự thật để `resume()` chạy tiếp một run dở.

Cái cửa duy nhất ở bước 4–5 tên trong code là `AgentKernel.execute_tool` (`core/kernel.py`). LLM ở đây cũng chỉ là một "năng lực" (`llm.chat`), không có đường tắt — nên nó cũng phải qua cửa như mọi tool. Bên trong cửa, thứ tự luôn cố định: phát sự kiện `tool.requested` → kiểm tra tool có nằm trong phạm vi được phép không → chạy qua chuỗi middleware cross-cutting (đo giờ, chặn theo policy, đếm ngân sách, retry, rút gọn kết quả) → phát `tool.completed`/`tool.failed`. Lỗi của tool không bao giờ làm sập lõi. Chính vì mọi thứ đi qua một cửa nên toàn bộ observability, budget, safety mới gắn được một chỗ thay vì vá khắp nơi — đó là giá trị bước 4 phục vụ.

Xuống một bậc, các thư mục map thẳng vào luồng trên:

- `core/` — cái lõi microkernel: `AgentKernel` là runtime chia sẻ, đóng băng (frozen) sau khi khởi động; còn state và vòng đời của từng run sống trong `KernelSession` tách riêng. Đây là chủ của cái cửa bước 4–5.
- `graph/` — các node ở bước 3–7 (`guard/agent/tool/delegate/finish/fail`) và phần biên dịch đồ thị; state của graph chỉ chứa thứ serialize được để checkpoint.
- `orchestrator/` — facade `run/resume` bước 1 + checkpointer SQLite bước 8.
- `delegation/` — cái cửa riêng ở bước 6 (manager, policy độ sâu/ngân sách, registry, progress store).
- `discipline/` — mấy cái cổng dùng chung: cổng JSON bước 4, cổng kết thúc bước 7, và budget bước 3.
- `control/` — tầng đang làm dở (realtime control plane, epic E21): các "hợp đồng" cho event/command/permission để sau này người ở ngoài can thiệp và xem run realtime; phần lớn mới là contract, transport/UI chưa xong.
- Vòng ngoài: `llm/` (adapter JSON-mode), `observability/` (event log + CLI inspect), `adapters/`, `middleware/`, `safety/`.

Bạn đang ở L3 — nắm entrypoint và happy path. Bạn muốn tôi đi sâu trách nhiệm của một phần cụ thể (ví dụ vì sao `core/` cố tình tách `AgentKernel` frozen khỏi `KernelSession`, hay cửa delegation khác cửa chính chỗ nào), hay có node/module nào trong luồng trên bạn đang thắc mắc?
