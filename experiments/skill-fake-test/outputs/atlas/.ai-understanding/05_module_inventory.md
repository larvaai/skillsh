# 05 — Module Inventory

> built_at: 2026-07-03T10:26:11Z · built_commit: n/a · scope: partial (bản scaled)

| Module | Responsibility | Public API | Internal files | Depends on | Used by | Risk |
|---|---|---|---|---|---|---|
| scheduling | định nghĩa lịch + sinh liều theo ngày | DoseGeneratorService.generateForDay, Schedule, DoseEvent | schedule.entity.ts, dose-event.entity.ts, dose-generator.service.ts | common/db | reminders.worker | **cao** (BUG-1 timezone, BUG-2 end-date) |
| reminders | gửi nhắc + wiring cron | ReminderService.dispatchDue, nightlyGenerate, everyMinute | reminder.service.ts, reminder.worker.ts | scheduling, common/db, common/providers | (scheduler đăng ký — không thấy) | **cao** (BUG-3 dedupe, BUG-4 retry) |
| adherence | xác nhận liều + tính tỉ lệ/streak | confirmDose, AdherenceService.rateFor, currentStreak | dose.controller.ts, adherence.service.ts, streak.ts | common/db, scheduling(entity) | (router — không thấy) | **cao** (BUG-5 IDOR, BUG-6 chia 0, BUG-7 đếm sai) |
| identity | phân quyền caregiver | canCaregiverView | caregiver.guard.ts | common/db | (route caregiver — không thấy caller) | trung bình (chưa được gọi ở đâu) |
| common | hạ tầng chung: db + provider | db, pushProvider | db.ts, providers.ts | scheduling(entity, cho type) | mọi service | trung bình (db in-memory global) |
| legacy | cron nhắc bản cũ | startOldCron, stopOldCron | old_reminder_cron.ts | common/db (import nhưng không dùng) | **KHÔNG AI** (dead code) | thấp về chức năng, nợ dọn dẹp |

Evidence:
- File path/Symbol: xem từng file đã đọc; call chain qua import statements
- Grep xác nhận: `grep -rn "legacy\|canCaregiverView\|currentStreak"` → 0 caller ngoài file định nghĩa → identity/legacy/streak hiện KHÔNG được wire vào
- Mức chắc chắn: 
  - responsibility + depends-on: **chắc chắn** (đọc import + code)
  - "used by" cho identity/reminders (nơi scheduler/router đăng ký): **KHÔNG tìm thấy** (fixture cắt phần boot)

## Notes
- **Core domain**: scheduling + adherence (mang luật nghiệp vụ). 
- **Infra/adapter**: common (db, provider).
- **Dead / chưa wire**: legacy (chắc chắn dead), identity + streak (định nghĩa nhưng chưa thấy caller trong fixture).
- Module reminders là nơi tập trung nhiều side effect nhất (gọi provider ngoài) → xem 12.
