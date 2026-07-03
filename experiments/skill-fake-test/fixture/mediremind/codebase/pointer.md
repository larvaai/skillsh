# codebase/ — con trỏ tới code thật (GĐ11–14)

MediRemind đã qua live slice (GĐ8) và đang build (GĐ11). Code THẬT nằm ngoài workspace 6-folder, trỏ như dưới.

## Repo code thật

```
/Users/uspro/Desktop/skillsh/experiments/skill-fake-test/fixture/codebase/mediremind
```

Slice dọc đã dựng (viết TypeScript kiểu NestJS thu nhỏ):
"sinh DoseEvent hôm nay → gửi reminder → xác nhận liều → tính adherence".

Cây thư mục theo đúng 4 bounded context (GĐ5→6):

```
src/
├── scheduling/        Medication · Schedule · sinh DoseEvent
│   ├── schedule.entity.ts
│   ├── dose-event.entity.ts
│   └── dose-generator.service.ts     ◄ nhánh pg-build: Scheduling module
├── reminders/         dispatch Reminder qua channel (push|sms)
│   ├── reminder.service.ts
│   └── reminder.worker.ts            ◄ nhánh pg-build: Reminders module (cron 00:05 + mỗi phút)
├── adherence/         chuyển trạng thái DoseEvent · tính AdherenceReport
│   ├── dose.controller.ts            (POST /doses/:id/confirm)
│   ├── adherence.service.ts
│   └── streak.ts
├── identity/          User · CaregiverLink · quyền
│   └── caregiver.guard.ts
├── common/
│   ├── db.ts                         (in-memory store cho slice)
│   └── providers.ts                  (push/sms provider ngoài)
└── legacy/
    └── old_reminder_cron.ts          (bản cron cũ — ứng viên triage/xoá)
```

## Ánh xạ module ↔ bounded context ↔ nhánh build

| Bounded context (GĐ5) | Thư mục code | Nhánh GĐ11 (pg-build) | Owner |
|---|---|---|---|
| Scheduling | `src/scheduling/` | T-11a sinh Scheduling module | delivery |
| Reminders | `src/reminders/` | T-11b sinh Reminders module | delivery |
| Adherence | `src/adherence/` | (đã có từ live slice GĐ8) | frame |
| Identity & Access | `src/identity/` | (đã có từ live slice GĐ8) | frame |

## Ghi chú cho code-skills

- Đây là code THẬT có khuyết tật CÀI SẴN. `/atlas` dựng `.ai-understanding/` cạnh repo trên; `/review` `/trace` `/triage` `/explain` đọc trực tiếp từ đó.
- `src/legacy/old_reminder_cron.ts` là ứng viên triage (giữ/xoá/rewrite) — liên quan OQ-A (managed queue vs cron).
- Chưa có: `delivery-standards.md` (GĐ11 vừa xong, đang build modules), `uat-report.md` (GĐ12 CHƯA), `runbook.md` (GĐ13 CHƯA ký), `ops.md` (GĐ14 chưa).
