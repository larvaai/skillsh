# MediRemind — Module Map

> Nguồn: BIBLE §5 (bounded contexts), §4 (entities), §7 (kiến trúc modular monolith).
> Ranh giới module = 4 bounded context. Mỗi module 1 owner + 1 contract.

## Kiến trúc nền
Modular monolith (BIBLE §7). Container: Web/API app · Reminder Worker (cron-driven) · Postgres · Redis (job queue) · Push/SMS provider (ngoài). Ranh giới module = 4 bounded context §5.

## Bảng module

| Module | Bounded context §5 | Owns (entity §4) | Owner |
|---|---|---|---|
| Scheduling | Scheduling | Medication, Schedule; sinh DoseEvent | Team Scheduling |
| Reminders | Reminders | Reminder | Team Reminders |
| Adherence | Adherence | DoseEvent (state), AdherenceReport | Team Adherence |
| Identity & Access | Identity & Access | User, CaregiverLink | Team Identity |

---

## 1. Scheduling
- **Bounded context:** Scheduling (§5).
- **Owner:** Team Scheduling.
- **Owns:** `Medication`, `Schedule`; là nơi DUY NHẤT sinh `DoseEvent` (từ Schedule.times_per_day[] × days_of_week[] trong khoảng start_date→end_date, theo timezone).
- **Public dependency:** phát domain event `DoseEventGenerated` cho Reminders & Adherence tiêu thụ.
- **Does NOT own:**
  - Trạng thái `DoseEvent` (pending→taken/missed/skipped) — thuộc **Adherence**.
  - Việc gửi `Reminder` — thuộc **Reminders**.
  - `User` / quyền — thuộc **Identity & Access**.

## 2. Reminders
- **Bounded context:** Reminders (§5).
- **Owner:** Team Reminders.
- **Owns:** `Reminder` (dose_event_id, channel: push|sms, sent_at). Dispatch qua Reminder Worker (cron-driven) → Push/SMS provider ngoài. Ràng buộc NFR-1: bắn trong 60s so với scheduled_time.
- **Does NOT own:**
  - Sinh `DoseEvent` — thuộc **Scheduling**.
  - Chuyển trạng thái liều khi patient xác nhận — thuộc **Adherence**.
  - `User` / channel-contact của user / quyền — thuộc **Identity & Access**.

## 3. Adherence
- **Bounded context:** Adherence (§5).
- **Owner:** Team Adherence.
- **Owns:** chuyển trạng thái `DoseEvent` (pending→taken|missed|skipped, taken_at); tính `AdherenceReport` (user_id, period, rate). Ghi xác nhận liều theo NFR-2 (≤ 300ms p95).
- **Does NOT own:**
  - Định nghĩa/sinh `DoseEvent` gốc — thuộc **Scheduling**.
  - Gửi nhắc — thuộc **Reminders**.
  - Kiểm quyền caregiver được xem report của patient nào — thuộc **Identity & Access** (Adherence chỉ tính; Identity quyết ai xem).

## 4. Identity & Access
- **Bounded context:** Identity & Access (§5).
- **Owner:** Team Identity.
- **Owns:** `User` (role: patient | caregiver), `CaregiverLink` (caregiver_id, patient_id, scope: view-only); mô hình quyền + audit-log truy cập caregiver (NFR-4).
- **Does NOT own:**
  - `Medication` / `Schedule` / `DoseEvent` — thuộc **Scheduling**/**Adherence**.
  - `AdherenceReport` (nội dung/số liệu) — thuộc **Adherence** (Identity chỉ cấp quyền xem).
  - `Reminder` — thuộc **Reminders**.
