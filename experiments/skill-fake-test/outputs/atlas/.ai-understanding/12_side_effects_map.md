# 12 — Side Effects Map

> built_at: 2026-07-03T10:26:11Z · built_commit: n/a · scope: partial (bản scaled)

| Module / fn | DB write | External API | Queue | Email/Push | File write | Cache | Logs |
|---|---|---|---|---|---|---|---|
| DoseGeneratorService.generateForDay | ✅ `db.doseEvents.push` | – | – | – | – | – | – |
| ReminderService.dispatchDue | ✅ `db.reminders.push` | ✅ `pushProvider.send` (HTTP push/sms) | – | ✅ push | – | – | – |
| confirmDose | ✅ mutate `dose.status`, `dose.takenAt` | – | – | – | – | – | – |
| AdherenceService.rateFor | – (read-only) | – | – | – | – | – | – |
| canCaregiverView | – (read-only) | – | – | – | – | – | – |
| legacy.startOldCron | – | – | – | – | – | – | ✅ console.log (chỉ tick) |

Evidence:
- File path/Symbol: dose-generator.service.ts:39, reminder.service.ts:21-22, dose.controller.ts:16-17, providers.ts:3-6
- Mức chắc chắn: chắc chắn

## Dangerous operations (cần cẩn trọng khi sửa)
1. **`pushProvider.send`** — gọi ra ngoài (Expo/Twilio), tốn tiền/rate-limit. HIỆN gọi tối đa 5 lần/liều (BUG-3) và không có retry/error-handling (BUG-4). Nếu throw → cả batch còn lại không được gửi.
   - Evidence: reminder.service.ts:16-24, providers.ts:5 (`throw new Error('missing userId')`). Mức: chắc chắn.
2. **mutate `dose.status = 'taken'`** trong confirmDose KHÔNG kiểm ownership (BUG-5 IDOR) → side effect trên dữ liệu người khác.
   - Evidence: dose.controller.ts:14-17. Mức: chắc chắn.
3. **`db.doseEvents.push`** trong generator không idempotent — chạy generator 2 lần/ngày sẽ tạo trùng DoseEvent (id ghép có ngày+time nên trùng id, nhưng push vẫn thêm bản ghi mới, không upsert).
   - Evidence: dose-generator.service.ts:28-40 (push thẳng, không check tồn tại). Mức: một phần (chưa thấy caller gọi 2 lần nhưng cron 00:05 + thiếu guard idempotent là rủi ro).

## Quan sát về observability
Không có logger/metric/trace nào ngoài 1 `console.log` ở legacy dead code → khi push gửi trùng hoặc vỡ vòng lặp, KHÔNG có dấu vết để debug (đẩy sang 16_observability — scaled-out).
