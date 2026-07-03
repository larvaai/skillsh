# Flow Trace: Sinh liều mỗi sáng (HAPPY PATH)

## User-visible behavior
Mỗi sáng, hệ tạo sẵn các "liều" (DoseEvent) cho ngày hôm nay từ lịch uống thuốc của mọi user, để lát nữa còn nhắc.

## Trigger (route/event/job)
Cron 00:05 → `nightlyGenerate()` (reminder.worker.ts:9).

## Step-by-step code path
1. **reminder.worker.ts:9-13** `nightlyGenerate` — lấy `today = new Date()`, gom các userId distinct từ `db.schedules`, gọi `generator.generateForDay(uid, today)` cho từng user.
2. **dose-generator.service.ts:10-11** `generateForDay` — filter schedule của user đó.
3. **dose-generator.service.ts:17-18** — lấy `weekday = day.getDay()`; nếu không nằm trong `daysOfWeek` → skip. (⚠ giờ server, BUG-1)
4. **dose-generator.service.ts:22** — nếu `day < startDate` → skip. (⚠ không lọc endDate, BUG-2)
5. **dose-generator.service.ts:24-36** — với mỗi giờ trong `timesOfDay`, tạo DoseEvent status `pending`, id ghép `${s.id}-${YYYY-MM-DD}-${t}`.
6. **dose-generator.service.ts:39** — `db.doseEvents.push(...events)` → lưu.

## Side effects
- DB write: `db.doseEvents.push`. Không log, không event, không idempotency guard.

## Failure paths
- Không có try/catch. Nếu `timesOfDay` chứa chuỗi sai định dạng → `split(':').map(Number)` cho NaN → `setHours(NaN)` → scheduledTime Invalid Date (không được xử lý).
- Chạy 2 lần cùng ngày → push trùng bản ghi (không upsert).

## Tests covering this flow
KHÔNG có test nào (không tồn tại file test trong fixture). Cần: test daysOfWeek filter, startDate/endDate boundary, timezone, idempotency.

## Evidence
- File path/Symbol: reminder.worker.ts:9 nightlyGenerate; dose-generator.service.ts:10 generateForDay, :39 push
- Mức chắc chắn: chắc chắn (đọc trọn call chain)
