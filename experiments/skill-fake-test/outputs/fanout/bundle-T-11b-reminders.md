# CONTEXT BUNDLE — T-11b · Reminders module

> Nhóm song song: `pg-build` · Agent 2 · owner `delivery`
> Prompt gọn để giao cho sub-agent (DRY-RUN — không spawn). Bám template Bước 2 SKILL.md.

---

**Bạn build:** Sinh **Reminders module** theo contract — sở hữu `Reminder` (dose_event_id, channel: push|sms, sent_at). Tiêu thụ event `DoseEventGenerated` (từ Scheduling) → dispatch Reminder qua channel push|sms tới Push/SMS provider ngoài, qua Reminder Worker (cron-driven: cron 00:05 + quét mỗi phút). Ràng buộc cứng NFR-1: bắn trong ≤ 60s so với `scheduled_time`.

**Contract (bám đúng, KHÔNG đổi — nếu phải đổi thì DỪNG và bump version + review chéo):** nguồn sự thật là quan hệ event trong `docs/contracts/scheduling-v1.md` (Reminders là CONSUMER của `DoseEventGenerated`) + ranh giới `docs/module-map.md` §2 Reminders.
- Event TIÊU THỤ: `DoseEventGenerated` — payload `{ dose_event_id, schedule_id, scheduled_time, status: "pending" }` (do Scheduling phát). Bám đúng payload này để dispatch.
- Reminders KHÔNG có endpoint public trong bộ contract hiện có (scheduling-v1 / adherence-v1). Nó là consumer + worker. Nếu cần expose API (vd trạng thái gửi) → contract CHƯA định nghĩa → DỪNG, báo về, không tự bịa endpoint. (Xem CẢNH BÁO cuối bundle.)
- Không có bảng error-code riêng cho Reminders trong contract đọc được → dùng convention lỗi chung của codebase; nếu cần mã lỗi contract-level → báo về để bổ sung contract.

**Luật cần theo (trích, không đổ cả constitution):**
- conventions §1 — một file một chủ: chỉ GHI trong `src/reminders/`; GHI chéo là CẤM.
- module-map "Reminders · Does NOT own": KHÔNG sinh `DoseEvent` (thuộc Scheduling), KHÔNG chuyển trạng thái liều khi patient xác nhận (thuộc Adherence), KHÔNG ghi User/channel-contact/quyền (thuộc Identity).
- delivery-standards §2/§4/§8: TypeScript kiểu NestJS thu nhỏ; Unit + Integration (đường event → dispatch); smoke E2E slice xác-nhận-liều phải còn xanh; metric reminder-latency đo NFR-1 ≤ 60s.
- NFR-1 (task traces_to): reminder bắn ≤ 60s so scheduled_time — đây là ràng buộc chính của module này.
- folders.md: artifact code trỏ đúng path repo.

**Đích artifact (chỉ ghi vào đây):** `codebase/mediremind/src/reminders/`
(repo thật: `fixture/codebase/mediremind/src/reminders/` — có sẵn `reminder.service.ts`, `reminder.worker.ts`).

**KHÔNG build (ranh giới cứng):**
- KHÔNG đụng `src/scheduling/` (nhánh T-11a song song) — sinh DoseEvent là của Scheduling; bạn chỉ TIÊU THỤ event, không tự materialize liều.
- KHÔNG đụng `src/adherence/`, `src/identity/`.
- **OQ-A (managed job-queue vs tự cron) đang TREO** — CHƯA có ADR đóng. Module worker dính thẳng OQ-A. KHÔNG tự chốt hướng queue/cron; build theo cron-driven như module-map + pointer mô tả (cron 00:05 + mỗi phút) NHƯNG ghi rõ đây là tạm theo hiện trạng, chờ ADR OQ-A; KHÔNG chạm/khôi phục `src/legacy/old_reminder_cron.ts`.
- KHÔNG nới NFR-4 (audit-log + at-rest cho dữ liệu nhạy cảm).
- KHÔNG sửa contract; thiếu field/endpoint/error thì DỪNG, báo về.

**Xong thì:** ghi code vào đúng `src/reminders/`, có unit+integration test + đo được reminder-latency cho NFR-1, rồi trả về 1 tóm tắt: đã làm gì · gắn về event/contract nào (`DoseEventGenerated` consumer) · NFR-1 kiểm chứng ra sao · còn treo gì (nêu RÕ phụ thuộc OQ-A queue-vs-cron + việc Reminders chưa có contract endpoint/error riêng).

---

## CẢNH BÁO gói cho T-11b (ghi kèm để agent chính biết)

Bộ contract đọc được chỉ có `scheduling-v1.md` và `adherence-v1.md` — KHÔNG có `reminders-v1.md`. Reminders chỉ được mô tả gián tiếp (consumer của `DoseEventGenerated` + phần §2 module-map). So với T-11a (có contract riêng đầy đủ API/event/error), bundle T-11b MỎNG hơn về mặt contract. Live-run nên đóng khoảng trống này (thêm contract Reminders hoặc xác nhận Reminders là pure-consumer không public API) TRƯỚC khi bung, để hai nhánh cân về độ rõ. DRY-RUN nên tôi gói theo những gì có + đánh dấu rõ chỗ thiếu.
