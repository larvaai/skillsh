# Flow Trace: Bắn reminder tới hạn (SIDE-EFFECT PATH)

## User-visible behavior
Đến gần giờ uống, bệnh nhân nhận thông báo push "Đến giờ uống thuốc".

## Trigger
Cron mỗi phút → `everyMinute()` (reminder.worker.ts:16) → `reminders.dispatchDue(new Date())`.

## Step-by-step code path
1. **reminder.service.ts:10** — `cutoff = now + windowMinutes(5)*60s`.
2. **reminder.service.ts:11-13** — filter DoseEvent `status==='pending'` và `scheduledTime` trong [now, cutoff].
3. **reminder.service.ts:16-24** — vòng lặp `due`:
   - **:21** `await pushProvider.send(userId, msg)` — GỌI RA NGOÀI (side effect chính).
   - **:22** `db.reminders.push({doseEventId, channel:'push', sentAt:now})` — ghi bản ghi đã gửi.
   - **:23** `sent++`.
4. **:25** trả về số đã gửi.

## Side effects
- **External push** (`pushProvider.send`) — providers.ts:3.
- **DB write** `db.reminders.push`.
- KHÔNG log, KHÔNG metric.

## Failure paths (đây là nơi hệ dễ chết trong prod)
- **BUG-3 (dedupe)**: worker chạy mỗi phút, window 5 phút, dose vẫn `pending` (status không đổi sau khi gửi) → cùng một liều lọt vào `due` tới 5 lần → gửi trùng 5 push. Evidence: reminder.service.ts:17 comment + logic (không đổi status, không check db.reminders).
- **BUG-4 (retry/error)**: `pushProvider.send` có thể `throw` (providers.ts:5 khi thiếu userId, hoặc provider timeout). Vì `await` trong for không có try/catch → **exception vỡ cả vòng lặp**, các dose sau trong `due` KHÔNG được gửi, không retry, không dead-letter. Evidence: reminder.service.ts:19-21 comment + thiếu try/catch.

## Tests covering this flow
KHÔNG có. Critical untested: dedupe, partial-failure isolation, window boundary.

## Evidence
- File path/Symbol: reminder.service.ts:9 dispatchDue; providers.ts:3 send
- Mức chắc chắn: chắc chắn
