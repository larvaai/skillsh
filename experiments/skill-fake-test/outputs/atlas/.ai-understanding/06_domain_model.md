# 06 — Domain Model

> built_at: 2026-07-03T10:26:11Z · built_commit: n/a · scope: partial (bản scaled)

## Concepts
| Concept | Meaning | Code representation | Important fields | Rules |
|---|---|---|---|---|
| Schedule | lịch uống một thuốc của một user | `interface Schedule` (schedule.entity.ts) | timesOfDay[], daysOfWeek[], startDate, endDate, timezone | endDate=null → vô thời hạn; timezone HIỆN chưa dùng |
| DoseEvent | một liều cụ thể tại một thời điểm | `interface DoseEvent` (dose-event.entity.ts) | scheduledTime, status, takenAt | status ∈ {pending, taken, missed, skipped}; taken → set takenAt |
| Reminder | bản ghi đã gửi nhắc | inline type trong db.reminders (db.ts) | doseEventId, channel, sentAt | channel ∈ {push, sms} |
| CaregiverLink | quan hệ caregiver↔patient | inline type db.caregiverLinks (db.ts) | caregiverId, patientId, scope | chỉ scope 'view-only' cho phép xem |

Evidence:
- File path/Symbol: schedule.entity.ts (Schedule), dose-event.entity.ts (DoseEvent + DoseStatus type), common/db.ts (reminders/caregiverLinks inline shape)
- Mức chắc chắn: chắc chắn

## Domain relationships
`Schedule (1) → (N) DoseEvent` qua `scheduleId`. `DoseEvent (1) → (N) Reminder` qua `doseEventId`. `Caregiver (N) ↔ (N) Patient` qua `CaregiverLink`.

Evidence:
- File path: dose-generator.service.ts:30 (`scheduleId: s.id`), reminder.service.ts:22 (`doseEventId: e.id`), db.ts:9 (caregiverLinks)
- Mức chắc chắn: chắc chắn

## Domain invariants (luật không được phá — quan sát + suy luận)
1. **Một DoseEvent chỉ nên có 1 reminder push đã gửi** — HIỆN BỊ PHÁ (BUG-3): không dedupe → tối đa 5 reminder/liều. (observed bug, không phải invariant được enforce)
2. **DoseEvent chỉ được sinh cho schedule còn hiệu lực** (day trong [startDate, endDate]) — HIỆN BỊ PHÁ (BUG-2): end-date không được lọc.
3. **scheduledTime phải theo timezone của user** — HIỆN BỊ PHÁ (BUG-1): dùng giờ server.
4. **taken ⇒ takenAt != null** — được giữ đúng (confirmDose set cả hai). Evidence: dose.controller.ts:16-17.

Evidence: các comment BUG-* trong dose-generator.service.ts:15,20 và reminder.service.ts:17. Mức: chắc chắn (bug được chú thích tường minh trong code).

## Domain ambiguity cần làm rõ (→ glossary)
- `missed` vs `skipped`: `skipped` = user chủ động bỏ; `missed` = quên/không phản hồi. Adherence hiện tính SAI vì gộp cả hai vào mẫu số (BUG-7).
  Evidence: adherence.service.ts:14-16, dose-event.entity.ts:1. Mức: chắc chắn.
