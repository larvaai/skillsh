# Contract: Scheduling v1

> Module: Scheduling (BIBLE §5). Owner: Team Scheduling.
> Sở hữu: Medication, Schedule; sinh DoseEvent. Bám entity §4, NFR §6.

## Public API

| Method | Endpoint | Mô tả | Auth |
|---|---|---|---|
| POST | `/v1/medications` | Tạo Medication (name, dosage, form) | patient |
| POST | `/v1/schedules` | Tạo Schedule (medication_id, times_per_day[], days_of_week[], start_date, end_date, timezone) | patient |
| GET | `/v1/schedules/{id}` | Đọc một Schedule | patient (chủ) |
| GET | `/v1/dose-events?date=` | Liệt kê DoseEvent đã sinh cho một ngày | patient (chủ) |

## Domain event (phát ra)

- **`DoseEventGenerated`** — payload: `{ dose_event_id, schedule_id, scheduled_time, status: "pending" }`.
  - Sinh khi Scheduling materialize DoseEvent từ Schedule cho ngày chạy.
  - Consumer: **Reminders** (để dispatch), **Adherence** (để mở trạng thái theo dõi).

## Data ownership

- SỞ HỮU (ghi): `Medication`, `Schedule`, bản ghi gốc `DoseEvent` (khởi tạo status=pending, scheduled_time).
- KHÔNG ghi: trạng thái sau pending của DoseEvent (thuộc Adherence), Reminder (thuộc Reminders).
- Đọc tham chiếu: `User.id` (chủ sở hữu Schedule) — chỉ đọc, không ghi (thuộc Identity & Access).

## Error code

| Code | HTTP | Nghĩa |
|---|---|---|
| `SCH-400-INVALID-TIMES` | 400 | times_per_day[] rỗng hoặc giờ không hợp lệ |
| `SCH-400-BAD-DATERANGE` | 400 | end_date < start_date |
| `SCH-404-NOT-FOUND` | 404 | Schedule không tồn tại |
| `SCH-403-NOT-OWNER` | 403 | Không phải patient sở hữu Schedule |

## NFR ràng buộc
- Sinh DoseEvent phải đủ sớm để Reminders đạt NFR-1 (bắn trong 60s so với scheduled_time).
- Scale mục tiêu (NFR-3): ~250k DoseEvent/ngày (50k user × ~5 liều).
