# 02 — Entrypoints Map

> built_at: 2026-07-03T10:26:11Z · built_commit: n/a · scope: partial (bản scaled)

Hệ thống bắt đầu chạy từ đâu.

| Entrypoint | Type | File | Trigger | Calls into |
|---|---|---|---|---|
| `nightlyGenerate()` | Cron | src/reminders/reminder.worker.ts:9 | cron 00:05 mỗi ngày | DoseGeneratorService.generateForDay (mỗi userId) |
| `everyMinute()` | Cron | src/reminders/reminder.worker.ts:16 | cron mỗi phút | ReminderService.dispatchDue(new Date()) |
| `confirmDose(req)` | HTTP handler | src/adherence/dose.controller.ts:10 | POST /doses/:id/confirm | AdherenceService.rateFor, mutate db.doseEvents |
| `canCaregiverView(cId,pId)` | Guard fn | src/identity/caregiver.guard.ts:7 | gọi từ route báo cáo (không thấy caller trong fixture) | db.caregiverLinks |
| `startOldCron()` / `stopOldCron()` | Cron (LEGACY, dead) | src/legacy/old_reminder_cron.ts:6,13 | không được import ở đâu | chỉ console.log |

Evidence:
- File path: reminder.worker.ts (comment "cron 00:05 mỗi ngày", "cron mỗi phút"), dose.controller.ts (comment "POST /doses/:id/confirm"), caregiver.guard.ts, legacy/old_reminder_cron.ts
- Symbol: nightlyGenerate, everyMinute, confirmDose, canCaregiverView, startOldCron/stopOldCron
- Suy luận: worker.ts export 2 async fn kèm comment cron; controller export confirmDose kèm route comment
- Mức chắc chắn: 
  - cron + confirmDose: **chắc chắn** (comment + call chain rõ)
  - nơi ĐĂNG KÝ scheduler / router: **KHÔNG tìm thấy** (fixture không có file boot) → đẩy xuống 18
  - `canCaregiverView` có caller thật hay không: **KHÔNG tìm thấy** (không grep ra nơi gọi trong fixture)

## Ghi chú
Không biết entrypoint được đăng ký ở đâu = không chắc cron thật sự chạy đúng lịch trong prod. Đây là slice demo nên nơi wiring bị cắt.
`startOldCron` là **dead code** (comment: "Không còn được import ở đâu"). Xác nhận: không file nào import `legacy/`.
