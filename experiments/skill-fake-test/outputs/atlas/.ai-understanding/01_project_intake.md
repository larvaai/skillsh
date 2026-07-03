# 01 — Project Intake

> built_at: 2026-07-03T10:26:11Z · built_commit: n/a · scope: partial (bản scaled)

## Project purpose
**MediRemind** — hệ nhắc uống thuốc & theo dõi tuân thủ (medication adherence). Từ lịch uống thuốc của bệnh nhân, hệ sinh ra từng "liều" (DoseEvent) cho mỗi ngày, gửi nhắc đúng giờ, cho bệnh nhân xác nhận đã uống, và tính tỉ lệ tuân thủ.

**Observed fact**, không phải assumption: toàn bộ danh từ trong code (Schedule, DoseEvent, adherence rate, streak, caregiver) mô tả một domain nhắc thuốc.

Evidence:
- File path: src/scheduling/schedule.entity.ts, src/scheduling/dose-event.entity.ts, src/adherence/adherence.service.ts, src/adherence/streak.ts, src/identity/caregiver.guard.ts
- Symbol: Schedule (medicationId, timesOfDay), DoseEvent (status, takenAt), AdherenceService.rateFor, currentStreak, canCaregiverView
- Suy luận từ bằng chứng: tên field + comment tiếng Việt ("Đến giờ uống thuốc", "tỉ lệ tuân thủ", "caregiver chỉ được XEM")
- Mức chắc chắn: chắc chắn

## Main users / actors
- **Patient** (bệnh nhân): nhận nhắc, bấm "Đã uống" → `confirmDose`.
- **Caregiver** (người chăm sóc): chỉ XEM dữ liệu adherence của patient nếu có `CaregiverLink` scope `view-only`.

Evidence:
- File path: src/adherence/dose.controller.ts (comment "patient bấm Đã uống"), src/identity/caregiver.guard.ts (canCaregiverView)
- Symbol: confirmDose (req.userId từ middleware auth), canCaregiverView(caregiverId, patientId)
- Mức chắc chắn: chắc chắn

## Main capabilities
1. Sinh liều theo lịch mỗi ngày (`DoseGeneratorService.generateForDay`).
2. Gửi nhắc liều sắp tới hạn (`ReminderService.dispatchDue`).
3. Xác nhận đã uống (`confirmDose`).
4. Tính tỉ lệ tuân thủ (`AdherenceService.rateFor`) + chuỗi ngày liên tiếp (`currentStreak`).
5. Phân quyền caregiver view-only (`canCaregiverView`).

## Runtime type
**Worker + API** (mixed). Có 2 cron job (nightly generate, every-minute dispatch) và 1 HTTP handler (`confirmDose`). Đây là một **slice demo** (comment `db.ts`: "Repo in-memory giả lập (slice demo). Thật sẽ là Postgres").

Evidence:
- File path: src/reminders/reminder.worker.ts (nightlyGenerate cron 00:05, everyMinute cron), src/adherence/dose.controller.ts (POST /doses/:id/confirm)
- Mức chắc chắn: chắc chắn

## Tech stack
- Language: **TypeScript**. Framework: KHÔNG rõ (không có package.json/Nestup/Express import trực tiếp — handler nhận `req` dạng plain object). 
- DB: hiện **in-memory** (`common/db.ts`), dự kiến Postgres (comment).
- Queue/cache/auth/deploy: KHÔNG có trong fixture (đẩy xuống 18).

Evidence:
- File path: src/common/db.ts (`export const db = { schedules: [], doseEvents: [], ... }`)
- Suy luận: không thấy import framework nào; `req` được type inline `{ params, userId }`
- Mức chắc chắn: một phần (fixture cắt gọn, thiếu file boot/config)

## How to run
**KHÔNG xác định được** từ fixture: không có package.json, tsconfig, README, script, entry `main`. Cron/worker được export dưới dạng function nhưng không thấy nơi đăng ký scheduler.

Evidence:
- Suy luận: `find . -type f` chỉ ra 12 file .ts trong src/, không file config gốc
- Mức chắc chắn: KHÔNG tìm thấy (đẩy xuống 18_risks_and_unknowns)
