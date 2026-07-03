# CONTEXT BUNDLE — T-11a · Scheduling module

> Nhóm song song: `pg-build` · Agent 1 · owner `delivery`
> Prompt gọn để giao cho sub-agent (DRY-RUN — không spawn). Bám template Bước 2 SKILL.md.

---

**Bạn build:** Sinh **Scheduling module** theo contract — sở hữu `Medication`, `Schedule`; là nơi DUY NHẤT sinh `DoseEvent` (materialize từ Schedule.times_per_day[] × days_of_week[] trong [start_date→end_date], theo timezone), khởi tạo mỗi DoseEvent với `status=pending` + `scheduled_time`, rồi phát domain event `DoseEventGenerated`.

**Contract (bám đúng, KHÔNG đổi — nếu phải đổi thì DỪNG và bump version + review chéo):** `docs/contracts/scheduling-v1.md`
- Public API:
  - `POST /v1/medications` (name, dosage, form) — auth patient
  - `POST /v1/schedules` (medication_id, times_per_day[], days_of_week[], start_date, end_date, timezone) — auth patient
  - `GET /v1/schedules/{id}` — auth patient (chủ)
  - `GET /v1/dose-events?date=` — auth patient (chủ)
- Domain event PHÁT: `DoseEventGenerated` — payload `{ dose_event_id, schedule_id, scheduled_time, status: "pending" }`. Consumer: Reminders (dispatch), Adherence (mở theo dõi).
- Error code dùng ĐÚNG bảng: `SCH-400-INVALID-TIMES`, `SCH-400-BAD-DATERANGE`, `SCH-404-NOT-FOUND`, `SCH-403-NOT-OWNER`.

**Luật cần theo (trích, không đổ cả constitution):**
- conventions §1 — một file một chủ: chỉ GHI trong `src/scheduling/`; đọc chéo được, GHI chéo là CẤM.
- module-map "Scheduling · Does NOT own": KHÔNG ghi trạng thái DoseEvent sau pending (thuộc Adherence), KHÔNG gửi Reminder (thuộc Reminders), KHÔNG ghi User/quyền (thuộc Identity). `User.id` chỉ ĐỌC tham chiếu.
- delivery-standards §2/§4: TypeScript kiểu NestJS thu nhỏ; có Unit (logic sinh DoseEvent) + Integration (mỗi endpoint + event `DoseEventGenerated`); lint/format phải xanh; PR chỉ đụng 1 module.
- NFR: sinh DoseEvent đủ SỚM để Reminders đạt NFR-1 (bắn ≤ 60s so scheduled_time); scale mục tiêu NFR-3 ~250k DoseEvent/ngày.
- folders.md: artifact code trỏ đúng path repo; đặt sai folder = chưa đạt Định-nghĩa-Xong.

**Đích artifact (chỉ ghi vào đây):** `codebase/mediremind/src/scheduling/`
(repo thật: `fixture/codebase/mediremind/src/scheduling/` — có sẵn `schedule.entity.ts`, `dose-event.entity.ts`, `dose-generator.service.ts`).

**KHÔNG build (ranh giới cứng):**
- KHÔNG đụng `src/reminders/` (nhánh T-11b song song) — dispatch/worker là của Reminders.
- KHÔNG đụng `src/adherence/`, `src/identity/` — chuyển trạng thái liều + quyền không thuộc bạn.
- KHÔNG quyết open-question đang treo: OQ-A (managed queue vs cron) — đó là việc của ADR, không quyết trong module này; KHÔNG chạm/khôi phục `src/legacy/old_reminder_cron.ts`.
- KHÔNG nới NFR-4 (dữ liệu sức khoẻ nhạy cảm: at-rest encryption + audit-log truy cập caregiver) để "đi cho nhanh".
- KHÔNG sửa contract; nếu contract thiếu thứ cần → DỪNG, báo về, không tự bịa field.

**Xong thì:** ghi code vào đúng `src/scheduling/`, đảm bảo unit+integration test theo test-pyramid, rồi trả về 1 tóm tắt: đã làm gì · gắn về contract/AC nào (scheduling-v1 API + `DoseEventGenerated`) · NFR liên quan (NFR-1 timeliness, NFR-3 scale) · còn treo gì (vd phụ thuộc OQ chưa đóng).
