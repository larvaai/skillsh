```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Go/No-Go Checklist + Runbook" lấy từ prompt/file bạn đưa, CHƯA qua cổng GĐ13 (skill /ship).
- Rủi ro: (1) chưa truy vết ngược được về pipeline; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /ship trước để có "Go/No-Go Checklist + Runbook" đã qua cổng.
```

Đây là **GĐ14 — Operate** cho `hex_agent`. Tôi đã đọc README + docs/ + liếc `core/`, `observability/`, `control/` để không bịa tên. Một cảnh báo quan trọng ngay từ đầu, vì nó chặn cột Business:

> **Chưa tìm thấy "mục tiêu gốc GĐ1" (Business Case CEO đã ký) trong repo.** `hex_agent` là một clean-rebuild kiểu harness/microkernel — docs có kiến trúc, epic spec, roadmap, nhưng KHÔNG có business objective đo được (giảm chi phí / tăng doanh thu / rút ngắn thời gian). Tôi **không bịa target**. Nhóm Business dưới đây để `chưa có số` + cần bạn/CEO cấp mục tiêu gốc thì dashboard mới "đóng vòng" được. Ba câu hỏi để lấp: (1) hệ này thay cái gì / phục vụ ai, chỉ số thành công là gì? (2) đã chạy production bao lâu, có số thật từ `observability/event_log` chưa? (3) đã có sự cố nào chưa?

---

### Artifact 1 — Ops Dashboard

```text
OPS DASHBOARD — hex_agent (multi-agent microkernel, sau <mốc chưa rõ>)
  ▸ ĐỌC CHO LÃNH ĐẠO (1 dòng): mục tiêu gốc GĐ1 = CHƯA CÓ SỐ (thiếu Business Case) →
    chưa kết luận "đạt/chưa" được; kỹ thuật: uptime & DORA đo được qua event_log + orchestrator.
  BUSINESS    : chưa có số — cần mục tiêu gốc GĐ1 (vd "giảm X% thời gian xử lý task" hoặc
                "% task agent tự đóng không cần người"). Cách lấy: chốt success metric với CEO,
                rồi tính từ observability/event_log (đếm run thành công / tổng run).
  PRODUCT     : task success rate (run finish qua finish_gate / tổng) · % task cần delegation ·
                skill/tool nào không ai gọi. Cách lấy: observability.inspect summary + đếm
                execute_tool theo tool_name. Hiện: chưa có số production.
  ENGINEERING : DORA — lead time (commit→deploy) · deploy frequency · change failure rate ·
                recovery time (MTTR). Hiện: chưa nối số thật — cách lấy ở khối dev bên dưới.
  OPERATIONS  : error rate (envelope lỗi / tổng execute_tool) · P95 latency mỗi tool-call ·
                uptime control-plane · incident count · checkpoint resume-fail rate.
                Cách lấy: event_log (events.jsonl) + orchestrator SQLite checkpoint.
```

**Góc nhìn lãnh đạo:** một màn hình, 4 nhóm — Business (đạt mục tiêu gốc?) · Product (agent có thực sự đóng được task, hay toàn phải giao người?) · Engineering (DORA — team giao hàng nhanh & an toàn?) · Operations (uptime/incident). Với hex_agent, hai dòng CTO nhìn đầu tiên là **task success rate** (Product) và **MTTR khi execute_tool/checkpoint hỏng** (Operations) — vì đây là hệ agent, "chạy được" nghĩa là task tự đóng và khi vỡ thì resume được từ SQLite checkpoint.

**Chi tiết cho dev/Ops — mỗi số lấy ở đâu (không bịa, chỉ ra đường lấy):**
- **Product & Operations** đo tại **`observability/event_log`** (`var/agent_runs/<run_id>/events.jsonl` + `summary.json`), truy vấn bằng `python -m observability.inspect summary latest`. Vì **mọi LLM/tool call đều qua `execute_tool`** (invariant trong README), đây là một điểm đo duy nhất, đáng tin — đếm envelope theo `tool_name` + trạng thái ra được error rate / adoption / P95 mà không cần vá thêm chỗ nào.
- **DORA** chưa có nguồn tự động. Cách lấy: lead time & deploy frequency từ git + CI; change failure rate & MTTR từ nhóm Incident bên dưới (đếm deploy gây incident / tổng deploy). Chọn đo DORA qua CI + incident log **thay vì** dựng APM riêng — vì hệ mới live, tải thấp, chưa đáng chi phí một stack observability đầy đủ (Đủ-là-đủ).
- **Resume-fail rate** là chỉ số đặc thù hex_agent: SQLite là "parent-graph checkpoint truth" → theo dõi số lần resume thất bại là tín hiệu sức khoẻ thật của hệ, đo tại `orchestrator/` checkpointer.

Dashboard này **SỐNG**: chạy lại `inspect summary` theo nhịp, không phải ảnh chụp một lần. Ngưỡng đề xuất khởi điểm (chỉnh sau khi có baseline): P95 execute_tool ≤ 300ms, error rate ≤ 1%, resume-fail = 0.

---

### Artifact 2 — Incident Process

```text
INCIDENT PROCESS
  1. Phát hiện : alert error-rate execute_tool vượt ngưỡng · resume-fail > 0 ·
                 control-plane (control/) không phát event. Ai nhận đầu tiên: on-call Ops.
  2. Phân loại : SEV theo ảnh hưởng — SEV1 hệ không nhận task / checkpoint hỏng mất state;
                 SEV2 một lớp tool/skill chết; SEV3 lỗi lẻ tự phục hồi.
  3. Owner     : incident owner (⚠️ CHƯA phân công vì thiếu ship.md GĐ13 — cần chỉ định 1 người
                 làm điều phối + kênh escalation trước khi coi là sẵn sàng).
  4. Khắc phục : dùng Runbook/rollback GĐ13 (⚠️ chưa có trong state) — tạm thời: resume run từ
                 SQLite checkpoint; tắt feature qua config/features.yaml nếu lỗi khu trú ở plugin.
  5. Hậu kiểm  : post-mortem không đổ lỗi → nguyên nhân gốc → action item về Iteration/backlog.
```

**Góc nhìn lãnh đạo:** khi có sự cố, **ai chịu trách nhiệm và mất bao lâu phục hồi** (nối thẳng recovery time trong DORA). Điểm cần lãnh đạo biết ngay: hệ có sẵn hai đường lùi rẻ — **resume từ SQLite checkpoint** và **tắt feature qua `config/features.yaml`** — nhưng **chưa có người trực được chỉ định**. Chưa lấp owner thì chưa gọi là vận hành được.

**Trạng thái hiện tại:** *0 incident production đã ghi.* Hai mảnh còn thiếu (đến từ việc bỏ qua GĐ13): **incident owner** và **Runbook/rollback đã ký**. Đây là open-Q, không bịa: cần chốt owner + xác nhận alert đã bật thật trước khi tuyên bố sẵn sàng. Tôi **không nhảy vào sửa code** — mỗi hậu kiểm chỉ ra action item cho backlog.

---

### Artifact 3 — Iteration Loop

```text
ITERATION LOOP
  Nhịp review : 2 tuần — Ops/SRE + PO dự; CTO theo tháng (E21 control-plane đang active nên
                nhịp 2 tuần hợp lý, không để 1 tuần vì tải còn thấp, không để 1 tháng vì realtime
                control đang thay đổi nhanh).
  Học được    : chỉ số nào lệch (task success rate thấp? tool nào error nhiều?) · skill/tool
                nào không ai gọi · incident dạy điều gì.
  Về backlog  : 1–3 item cải tiến → roadmap kế (GĐ9), mỗi item kèm số trỏ tới nó, giữ traceability.
```

**Góc nhìn lãnh đạo:** sau mỗi nhịp, một câu — *"đã đạt/chưa mục tiêu, ba việc tiếp theo là gì"* — để CEO/CTO biết vòng kế đầu tư vào đâu. Quyết định này là của CEO/CTO, không phải của `operate`.

Item ứng viên cho vòng kế (dựa trên trạng thái repo, **chưa phân rã story** — để /backlog làm):
1. **Nối số Business thật** — lý do: cột Business đang `chưa có số`, chưa đóng được vòng với GĐ1. Đây là item ưu tiên 1.
2. **Hoàn tất E21 Realtime Control Plane** (transport / Control-Tower UI / reliability đang pending theo README) — lý do: đây là nguồn observability realtime cho chính dashboard này.
3. **Auto-hoá DORA** từ CI + incident log — lý do: DORA hiện đo thủ công.

---

### Cổng go/no-go

Cổng GĐ14: *"Đạt mục tiêu chưa? Làm gì tiếp?"* — **hiện chưa mở được** vì thiếu mục tiêu gốc GĐ1 và incident owner. Không phải "no-go", mà là **thiếu đầu vào để đối chiếu**. Tôi không tự tuyên đạt/không đạt.

```text
═══ BÀN GIAO — hex_agent (GĐ14 → vòng kế) ═══
Mục tiêu gốc GĐ1 : CHƯA CÓ SỐ — thiếu Business Case; cần CEO cấp success metric mới đối chiếu được
Học được         : mọi call qua execute_tool → 1 điểm đo tin cậy; checkpoint SQLite = đường lùi rẻ;
                   nhưng chưa có owner/Runbook đã ký & chưa có baseline production
Item cải tiến    : (1) nối số Business thật về GĐ1  (2) hoàn tất E21 control-plane (nguồn observ.)
                   (3) auto-hoá DORA từ CI + incident log — CHƯA phân rã
Artifact         : state/project/hex_agent/pipeline/operate.md (đề xuất — chưa ghi, chờ bạn gật)
→ Đưa item cải tiến vào roadmap kế & phân rã story: chạy /backlog (GĐ9)
→ Sự cố phát lộ lỗ hổng cần đào gap/edge case sâu: chạy /review
→ Item cần nghĩ lại từ nhu cầu/giá trị (vd định nghĩa success metric): chạy /idea hoặc /partner
→ Cần build ngay slice cải tiến nhỏ đã rõ: chạy /frame
════════════════
```

**Ba việc để tôi hoàn tất vòng đo (bạn quyết, tôi không tự chọn):** (a) cấp **mục tiêu gốc GĐ1** để lấp cột Business; (b) chỉ định **incident owner** + xác nhận alert đã bật; (c) cho phép tôi **ghi artifact** vào `state/project/hex_agent/pipeline/operate.md` (mặc định tôi chưa ghi vào repo code).

