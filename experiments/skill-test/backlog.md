```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Live Slice Report" lấy từ prompt/file bạn đưa, CHƯA qua cổng GĐ8 (skill /skeleton).
- Rủi ro: (1) chưa truy vết ngược được về pipeline; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /skeleton trước để có "Live Slice Report" đã qua cổng.
```

**backlog · GĐ9 — Roadmap & Backlog cho hex_agent**

Nền tôi bám: live slice *"chạy một task đơn qua kernel tới khi finish"* đã chạy trên staging → đây chính là **feature ĐẦU của R1**, và nó đã chứng minh sống được đúng xương sống kiến trúc: `orchestrator.run → compiled LangGraph → agent/tool node → execute_tool → finish → SQLite checkpoint`. Từ bằng chứng đó tôi mới scale ra các epic còn lại. Cái tôi đọc được từ repo (README/MAP/runtime-flow) cho thấy nhiều epic nền (E01–E10) đã có code — nên roadmap dưới đây là **kế hoạch build tiếp**, coi phần đã có là "đã proven", không phân rã lại.

---

### GÓC NHÌN LÃNH ĐẠO

**ROADMAP — hex_agent (multi-agent microkernel)**
- **Business Objective**: cho một task tự nhiên vào → hệ tự chạy tới kết quả *có kiểm soát, có bằng chứng, phục hồi được* — nền để bán được như một agent-runtime đáng tin, không phải demo.
- **Product Goal**: một đường chạy task ổn định, quan sát được realtime, và can thiệp/duyệt được khi rủi ro.

| Theme | R1 (MVP — proof→ổn định) | R2 (điều khiển & an toàn) | R3 (đa-agent & mở rộng) |
|---|---|---|---|
| **Chạy task tin cậy** | Single-task qua kernel tới finish + resume | Budget/discipline gate cứng | — |
| **Nhìn & can thiệp realtime** | Event log + inspect CLI | Control Plane: approval-gate + Control-Tower UI (E21) | Live intervention đa-agent |
| **Nhiều agent phối hợp** | (hoãn) | Delegation 1 tầng có scope | Agent-O TaskLoop + acceptance gate (E10) |

*(R1 vào trước vì slice GĐ8 đã chứng minh luồng chạy-tới-finish; R2 lấy đúng E21 đang "active/pending transport+UI" trong README làm trục kế; đa-agent E10 đẩy R3 vì phụ thuộc đường single-task ổn định trước.)*

---

### BACKLOG (R1 — phân rã tới Story+AC)

**Epic A — Chạy một task qua kernel tới finish, đáng tin**
*business value: biến slice-đã-sống thành đường chạy production ổn định — trạng thái: slice PASS, đang cứng hoá.*

- **Feature A1 — Run một task tới finish** *(thuộc Epic A · value: đầu-vào-ra-kết-quả đi qua đúng chokepoint · size: đã có, chỉ nghiệm thu lại như R1)*
  - Story: *"Là caller, tôi muốn submit một task và nhận kết quả cuối, để dùng hệ như một agent-runtime."*
    - AC: Given một TaskEnvelope hợp lệ / When gọi `orchestrator.run` / Then mọi LLM+tool call đi qua `execute_tool`, graph tới node `finish`, trả kết quả + `task_id`, ghi events.jsonl + summary.json.
    - AC (rule bất biến): Given bất kỳ hành động ngoài nào / Then KHÔNG có đường tắt vòng qua `execute_tool` (kể cả `llm.chat`).
    - Tasks (thô, để size): xác nhận facade `run`, guard→agent→tool→finish, event emit. · Test ref: TC-RUN-FINISH-001.

- **Feature A2 — Resume một task đang dở** *(value: không mất việc khi crash · size: 1 sprint · rủi ro: TRUNG BÌNH — checkpoint truth)*
  - Story: *"Là caller, tôi muốn resume một run đã dừng giữa chừng, để không chạy lại từ đầu."*
    - AC: Given một `run_id` có checkpoint trong `langgraph.sqlite` / When gọi `orchestrator.resume(run_id)` / Then graph tiếp từ state đã lưu, KHÔNG lặp lại step đã hoàn tất, `run_id ↔ thread_id` khớp.
    - AC (biên): Given checkpoint thiếu/hỏng / Then fail sạch có lỗi rõ, KHÔNG chạy nửa vời. · Tasks: SQLite checkpointer, projection JSON cho UI. · Test ref: TC-RESUME-001, TC-RESUME-CORRUPT-002.

- **Feature A3 — Quan sát một run** *(value: thấy được hệ đã làm gì · size: nhỏ, đã có event_log/inspect)*
  - Story: *"Là dev vận hành, tôi muốn liệt kê run và xem tóm tắt/sự kiện, để chẩn đoán khi có lỗi."*
    - AC: Given một run đã chạy / When `python -m observability.inspect summary <run>` / Then in đúng số step, tool đã gọi, kết quả cuối; `list` thấy run mới. · Test ref: TC-INSPECT-001.

*Feature AC (tổng): A xong khi một task chạy tới finish, resume được sau crash, và mọi bước đọc lại được qua inspect.*
*Release AC (R1 go-live): pass UAT luồng run+resume + security scan (path-jail toolbox) + có rollback. DoD chi tiết: tham chiếu GĐ11 (/delivery), không viết ở đây.*

---

### RELEASE PLAN

- **R1 (MVP)**: A1 Run→finish · A2 Resume · A3 Observe. **Mục tiêu**: một task bất kỳ chạy tới kết quả và phục hồi được sau gián đoạn.
  **Thứ tự + lý do**: A1 trước (đã có slice sống → nghiệm thu lại, gỡ rủi ro nền sớm) → A2 (resume phụ thuộc run đã chạy + checkpoint truth) → A3 (đọc lại, không chặn go-live nhưng cần cho vận hành). **Phụ thuộc**: A2 cần SQLite checkpoint (đã có trong `orchestrator/checkpoint.py`). **Rủi ro**: đúng-đắn checkpoint khi resume (đẩy test kỹ ở GĐ12).
- **R2**: Control Plane E21 (approval-gate cho hành động rủi ro + Control-Tower UI + transport) và discipline gate cứng (budget/finish_gate). **Hoãn** vì cần đường single-task ổn định làm nền để cắm event/command vào.
- **R3**: Đa-agent — Agent-O TaskLoop + delegation có scope + acceptance-evidence gate (E10). **Hoãn** vì phụ thuộc R1 ổn định + R2 có kênh can thiệp; đa-agent mà nền chưa vững thì rủi ro nhân lên.

---

### TỰ SOI (trước cổng)
- Lãnh đạo đọc được đoạn đầu? — có: 1 Objective + bảng theme×release + value/trạng thái mỗi epic, ngôn ngữ nghiệp vụ.
- Dev đủ hành động? — R1 có Story + AC Given/When/Then + task thô + Test ref → giao được sang /frame.
- Đủ 3 artifact? — Roadmap ✓ · Backlog phân rã ✓ · Release Plan ✓. AC nằm DƯỚI story ✓; DoD chỉ tham chiếu ✓.
- Đủ-là-đủ? — R1 sâu tới AC; R2/R3 chỉ theme+epic; không đổ story cho release xa ✓.
- Traceability? — Epic A → Objective (task→kết quả tin cậy); Feature→Epic; Story→Feature; AC "không đường tắt qua execute_tool" nối thẳng nguyên tắc kiến trúc thật của repo. **Một mắt CÒN TREO**: chưa có PRD/Domain Model chính thức trong state (đầu vào từ prompt) → AC đang neo vào runtime-flow/README thật, chưa vào Domain GĐ5. Ghi thành open-Q, không bịa nối.
- Không lấn vai? — không chọn stack, không chia module, không code, không DoD chi tiết ✓.

**Open questions (không tự quyết)**:
1. Chưa có Domain Model GĐ5 chính thức → các AC business-rule đang mượn từ nguyên tắc code; nên chốt Domain trước khi viết story R2/R3.
2. E21 (Control Plane) README ghi "transport/UI/reliability pending" — cần xác nhận scope R2 lấy tới đâu.

---

### CỔNG GO/NO-GO
**"Backlog đủ để lập kế hoạch delivery & phân module chưa?"** — R1 đã có story+AC; roadmap 1 trang đọc được; thứ tự release có lý do. Chặn nhẹ: Domain GĐ5 còn treo (không chặn R1, có thể chặn AC R2). Tôi KHÔNG tự tuyên bố pass — bạn (vai PO + Tech lead) quyết go/no-go cho R1.

```
═══ BÀN GIAO — hex_agent · Backlog GĐ9 ═══
Đã chốt : Roadmap (3 theme × 3 release) · Backlog R1 (1 epic / 3 feature / 4 story có AC) · Release Plan R1.
Nguồn   : Live Slice (prompt, NGOÀI pipeline) + README/MAP/runtime-flow thật.
→ Chia module theo domain boundary + owner + contract (GĐ10, bước kế mặc định) : chạy /modules
→ Build ngay "Resume một task" (A2) — đóng khung slice cho dev                  : chạy /frame  (rồi /delivery khi vào build chuẩn GĐ11)
→ Domain còn treo khiến AC R2 chưa neo được business rule                       : quay lại /idea hoặc /partner (GĐ5)
════════════════
```
