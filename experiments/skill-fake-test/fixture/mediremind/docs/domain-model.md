# MediRemind — Domain Model (GĐ5)

> Nguồn sự thật: BIBLE §4 (entities), §5 (bounded contexts). Không thêm entity/field ngoài BIBLE.

## 1. Entities

MediRemind có 7 entity domain.

| # | Entity | Thuộc tính (từ BIBLE §4) | Ghi chú |
|---|--------|--------------------------|---------|
| 1 | **User** | role: `patient` \| `caregiver` | Chủ thể của mọi dữ liệu; patient sở hữu dữ liệu thuốc, caregiver chỉ-xem. |
| 2 | **Medication** | name, dosage, form | Loại thuốc patient phải uống. |
| 3 | **Schedule** | medication_id, times_per_day[], days_of_week[], start_date, end_date, timezone | Lịch uống của một Medication; sinh ra DoseEvent. |
| 4 | **DoseEvent** | schedule_id, scheduled_time, status: `pending` \| `taken` \| `missed` \| `skipped`, taken_at | Một lần cần uống ở một mốc giờ cụ thể. |
| 5 | **Reminder** | dose_event_id, channel: `push` \| `sms`, sent_at | Lần nhắc đã bắn cho một DoseEvent. |
| 6 | **CaregiverLink** | caregiver_id, patient_id, scope: `view-only` | Liên kết một caregiver theo dõi một patient, chỉ-xem. |
| 7 | **AdherenceReport** | user_id, period, rate | Tỉ lệ tuân thủ tổng hợp theo kỳ. |

## 2. Quan hệ giữa entities

```
User (patient) ──1─── owns ──*── Medication
Medication     ──1─── has  ──*── Schedule
Schedule       ──1─── generates ──*── DoseEvent
DoseEvent      ──1─── triggers  ──*── Reminder
User (caregiver) ──*── CaregiverLink ──*── User (patient)   (view-only)
User           ──1─── has  ──*── AdherenceReport            (period, rate)
```

- **User (patient) → Medication**: một patient có nhiều Medication; mỗi Medication thuộc một patient.
- **Medication → Schedule**: một Medication có nhiều Schedule (`medication_id`).
- **Schedule → DoseEvent**: một Schedule sinh nhiều DoseEvent (`schedule_id`), mỗi DoseEvent gắn một `scheduled_time`.
- **DoseEvent → Reminder**: một DoseEvent có thể phát nhiều Reminder (`dose_event_id`), mỗi Reminder qua một `channel` (push \| sms).
- **CaregiverLink**: nối `caregiver_id` với `patient_id`, `scope = view-only` — caregiver chỉ đọc, không sửa dữ liệu thuốc.
- **AdherenceReport**: gắn `user_id`, tổng hợp theo `period` ra `rate`.

## 3. Trạng thái DoseEvent

`status ∈ { pending, taken, missed, skipped }` (BIBLE §4).

```
                 ┌────────────────► taken     (patient bấm "Đã uống"; ghi taken_at)
                 │
 (sinh mới) ─► pending ─────────────► skipped   (patient chủ động bỏ liều)
                 │
                 └────────────────► missed     (quá hạn không xác nhận)
```

- **pending**: DoseEvent vừa được Schedule sinh ra tại `scheduled_time`, chưa có phản hồi.
- **pending → taken**: patient xác nhận đã uống (live slice GĐ8 "Patient xác nhận một liều"); set `taken_at`.
- **pending → skipped**: patient chủ động bỏ liều.
- **pending → missed**: hết thời hạn mà không xác nhận.
- `taken` / `missed` / `skipped` là trạng thái kết thúc; AdherenceReport tính `rate` từ tỉ lệ các trạng thái này.

## 4. Bounded contexts (BIBLE §5)

4 bounded context, tương ứng ranh giới module ở kiến trúc GĐ6.

| Bounded context | Entity sở hữu | Trách nhiệm |
|-----------------|---------------|-------------|
| **Scheduling** | Medication, Schedule | Quản lý thuốc & lịch; **sinh DoseEvent** từ Schedule. |
| **Reminders** | Reminder | **Dispatch Reminder** cho DoseEvent qua channel (push \| sms). |
| **Adherence** | AdherenceReport | **Chuyển trạng thái DoseEvent** (pending→taken/missed/skipped) & **tính AdherenceReport**. |
| **Identity & Access** | User, CaregiverLink | Quản lý User, CaregiverLink & quyền truy cập. |

**Ghi chú ranh giới:** DoseEvent do **Scheduling** sinh ra nhưng **Adherence** sở hữu việc chuyển trạng thái của nó — đây là entity giao thoa giữa hai context (Scheduling tạo, Adherence cập nhật trạng thái, Reminders đọc để dispatch).
