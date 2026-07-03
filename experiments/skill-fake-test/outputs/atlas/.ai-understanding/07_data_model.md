# 07 — Data Model

> built_at: 2026-07-03T10:26:11Z · built_commit: n/a · scope: partial (bản scaled)

## Storage
**In-memory** — object `db` với 4 mảng, mutable global. Comment tường minh: "Repo in-memory giả lập (slice demo). Thật sẽ là Postgres".

Evidence:
- File path: src/common/db.ts:4-10
- Symbol: `export const db = { schedules, doseEvents, reminders, caregiverLinks }`
- Mức chắc chắn: chắc chắn

## "Tables" (mảng in-memory)
| Entity/Table | Purpose | Important fields | Relations | Constraints |
|---|---|---|---|---|
| schedules | lịch uống thuốc | userId, medicationId, timesOfDay, daysOfWeek, startDate, endDate, timezone | 1→N doseEvents | không có; không index; không unique |
| doseEvents | từng liều | scheduleId, userId, scheduledTime, status, takenAt | N←schedules, 1→N reminders | id ghép chuỗi `${s.id}-${YYYY-MM-DD}-${t}` |
| reminders | nhắc đã gửi | doseEventId, channel, sentAt | N←doseEvents | không unique theo doseEventId (→ BUG-3 trùng) |
| caregiverLinks | quyền xem | caregiverId, patientId, scope | N↔N user | scope kiểm bằng string 'view-only' |

Evidence:
- File path: db.ts (khai báo shape), dose-generator.service.ts:29 (id format), reminder.service.ts:22 (reminder record)
- Mức chắc chắn: chắc chắn

## Migrations
KHÔNG có (in-memory). Khi lên Postgres sẽ cần migration — chưa tồn tại trong fixture.
Evidence: không thấy file migration/schema. Mức: KHÔNG tìm thấy → đẩy xuống 18.

## Dangerous fields
- `DoseEvent.status` — điều khiển toàn bộ logic reminder (chỉ gửi 'pending') và adherence. Đổi sai → gửi nhầm hoặc tính sai tỉ lệ.
- `CaregiverLink.scope` — quyết định quyền xem. So sánh bằng string thô ('view-only'), dễ typo/mở rộng scope sai.
- `Schedule.endDate` (null nghĩa vô thời hạn) — hiện KHÔNG được generator dùng (BUG-2).

Evidence: reminder.service.ts:12 (filter status pending), caregiver.guard.ts:11 (scope==='view-only'), dose-generator.service.ts:22 (chỉ chặn startDate). Mức: chắc chắn.
