# Contract: Adherence v1

> Module: Adherence (BIBLE §5). Owner: Team Adherence.
> Sở hữu: chuyển trạng thái DoseEvent, tính AdherenceReport. Bám entity §4, NFR §6.

## Public API

| Method | Endpoint | Mô tả | Auth |
|---|---|---|---|
| POST | `/v1/dose-events/{id}/confirm` | Patient xác nhận đã uống → pending→taken, ghi taken_at | patient (chủ) |
| POST | `/v1/dose-events/{id}/skip` | Patient bỏ liều → pending→skipped | patient (chủ) |
| GET | `/v1/adherence-reports?user_id=&period=` | Đọc AdherenceReport (user_id, period, rate) | patient (chủ) hoặc caregiver có CaregiverLink view-only |

## Domain event (phát ra)

- **`DoseConfirmed`** — payload: `{ dose_event_id, taken_at }`. Sinh khi liều pending→taken.
- **`DoseMissed`** — payload: `{ dose_event_id }`. Sinh khi hết cửa sổ mà vẫn pending → missed (batch).

## Data ownership

- SỞ HỮU (ghi): trạng thái `DoseEvent` (pending→taken|missed|skipped, taken_at); `AdherenceReport` (rate theo period).
- KHÔNG ghi: bản ghi gốc DoseEvent/scheduled_time (thuộc Scheduling), Reminder (thuộc Reminders), quyết định QUYỀN caregiver được xem report của patient nào (thuộc Identity & Access).
- Tiêu thụ event: `DoseEventGenerated` (từ Scheduling) để mở theo dõi trạng thái.

## Error code

| Code | HTTP | Nghĩa |
|---|---|---|
| `ADH-404-NOT-FOUND` | 404 | DoseEvent không tồn tại |
| `ADH-409-ALREADY-RESOLVED` | 409 | DoseEvent không còn ở trạng thái pending |
| `ADH-403-NOT-OWNER` | 403 | Không phải patient sở hữu liều |
| `ADH-403-NO-LINK` | 403 | Caregiver không có CaregiverLink view-only tới patient |

## NFR ràng buộc
- Ghi xác nhận liều: ≤ 300ms p95 (NFR-2).
- Truy cập report của caregiver phải qua audit-log (NFR-4) — quyền do Identity & Access cấp.
