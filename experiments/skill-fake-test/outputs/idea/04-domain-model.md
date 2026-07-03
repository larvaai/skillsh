# Domain Model — MediRemind (GĐ5 World Model) — **DỪNG Ở ĐÂY**

> Đi từ NGÔN NGỮ NGHIỆP VỤ (PRD) sang: Bounded Context → Entity (identity + lifecycle) →
> Business Rule bất biến → Domain Event → Data Ownership. Entity **không** phải bảng DB — chưa có
> schema, chưa có kiến trúc. Đây là tín hiệu DỪNG của `idea`; kiến trúc là GĐ6 (`/shape`).
>
> Model tự sinh từ PRD (không đọc `docs/domain-model.md` — file đó bị cấm để test skill có tự
> dựng được domain không).

## 1. Bounded Contexts (ranh giới nghiệp vụ)
Bốn context, chia theo trách nhiệm nghiệp vụ khác nhau + tần suất thay đổi khác nhau:

| Context | Trách nhiệm | Sở hữu dữ liệu chính |
|---------|-------------|----------------------|
| **Identity & Access** | ai là ai, patient↔caregiver liên kết & quyền, audit truy cập | User, CaregiverLink, AuditEntry |
| **Scheduling** | thuốc + lịch của patient, sinh ra các liều cần uống | Medication, Schedule, DoseEvent (tạo) |
| **Reminders** | bắn nhắc cho từng liều tới giờ qua kênh push/SMS | Reminder |
| **Adherence** | chuyển trạng thái liều theo xác nhận, tính tuân thủ | DoseEvent (đổi trạng thái), AdherenceReport |

> Ghi chú ranh giới: **DoseEvent** được **Scheduling sinh ra** nhưng **Adherence chuyển trạng thái**.
> Đây là điểm giao cần contract rõ ở GĐ6 (ai được đổi status) — đánh dấu open-Q kiến trúc, không
> giải ở tầng domain.

## 2. Entities (identity + lifecycle)

### User
- **Identity:** user_id.
- **Thuộc tính:** role ∈ {patient, caregiver}, thông tin đăng nhập/danh tính.
- **Lifecycle:** registered → active → (deactivated).

### Medication
- **Identity:** medication_id (thuộc về một patient).
- **Thuộc tính:** name, dosage, form (viên/nước/…).
- **Lifecycle:** created → (edited) → archived (ngừng dùng).

### Schedule
- **Identity:** schedule_id (gắn với một medication).
- **Thuộc tính:** số lần/ngày + các mốc giờ, ngày nào trong tuần, ngày bắt đầu/kết thúc, **múi giờ**.
- **Lifecycle:** active → (paused) → ended (qua end_date).

### DoseEvent  *(entity trung tâm của "đo tuân thủ")*
- **Identity:** dose_event_id (sinh từ schedule cho một mốc giờ cụ thể).
- **Thuộc tính:** scheduled_time, status, taken_at.
- **Lifecycle (state machine):**
  `pending` → `taken` (patient xác nhận trong cửa sổ) · `skipped` (patient chủ động bỏ) · `missed`
  (hết cửa sổ chưa xác nhận). Trạng thái cuối là bất biến (không quay lại pending).

### Reminder
- **Identity:** reminder_id (gắn một dose_event).
- **Thuộc tính:** channel ∈ {push, sms}, sent_at.
- **Lifecycle:** scheduled → sent → (failed → retry/fallback SMS).

### CaregiverLink
- **Identity:** cặp (caregiver_id, patient_id).
- **Thuộc tính:** scope = view-only, trạng thái mời/kích hoạt.
- **Lifecycle:** invited → active → (revoked).

### AdherenceReport
- **Identity:** (user_id, period) — hoặc report_id.
- **Thuộc tính:** period, on-time dose rate (và số taken/missed/skipped).
- **Lifecycle:** dẫn xuất (derived) — tính lại khi DoseEvent đổi trạng thái; không phải entity ghi tay.

### AuditEntry (Identity & Access)
- **Identity:** audit_id.
- **Thuộc tính:** actor (caregiver), patient_id, hành động, thời điểm.
- **Lifecycle:** append-only (không sửa/xoá) — phục vụ NFR-4.

## 3. Business Rules bất biến
- **BR-1 (quyền caregiver):** Caregiver **chỉ-xem** — không tạo/sửa/xoá Medication, Schedule, hay đổi
  trạng thái DoseEvent của patient.
- **BR-2 (liên kết trước khi xem):** Caregiver chỉ thấy dữ liệu của patient khi tồn tại **CaregiverLink
  active** giữa hai bên.
- **BR-3 (audit bắt buộc):** Mọi lần caregiver truy cập dữ liệu patient **phải** ghi một AuditEntry
  (không có đường đọc "im lặng").
- **BR-4 (cửa sổ on-time — trả lời OQ-1 của PRD):** Một DoseEvent chỉ tính **taken đúng giờ** nếu
  xác nhận trong **cửa sổ cho phép quanh scheduled_time**; ngoài cửa sổ mà có xác nhận = taken-trễ;
  hết cửa sổ không xác nhận = **missed**. *(Độ rộng cửa sổ chính xác là số cấu hình/NFR — chốt ở spec
  GĐ6; domain chỉ khẳng định RULE tồn tại và biên trạng thái.)*
- **BR-5 (trạng thái cuối bất biến):** DoseEvent đã ở taken/missed/skipped thì không quay về pending.
- **BR-6 (sở hữu dữ liệu):** Medication/Schedule thuộc về **đúng một patient**; không patient nào
  thấy/sửa thuốc của patient khác.
- **BR-7 (không cấp cứu):** Hệ không đảm bảo giao nhắc tức thời kiểu life-critical; app hiển thị
  disclaimer "không dùng cho cấp cứu" (đồng bộ NFR-5).

## 4. Domain Events (đặt tên)
- **MedicationScheduled** — schedule mới được lập cho một medication.
- **DoseEventGenerated** — hệ sinh một liều cần uống (Scheduling → Reminders/Adherence).
- **ReminderSent** — đã bắn nhắc cho một liều.
- **DoseTaken** / **DoseSkipped** / **DoseMissed** — chuyển trạng thái liều (nguồn tính adherence).
- **AdherenceRecomputed** — báo cáo tuân thủ được tính lại sau khi liều đổi trạng thái.
- **CaregiverLinked** / **CaregiverRevoked** — liên kết caregiver bật/tắt.
- **PatientDataAccessed** — caregiver truy cập dữ liệu patient (sinh AuditEntry).

## 5. Data Ownership (ai sở hữu gì)
- **Identity & Access** sở hữu: User, CaregiverLink, AuditEntry (nguồn sự thật về quyền + audit).
- **Scheduling** sở hữu: Medication, Schedule; **tạo** DoseEvent.
- **Adherence** sở hữu vòng đời trạng thái của DoseEvent + AdherenceReport.
- **Reminders** sở hữu: Reminder.
- Ranh giới ghi/đọc DoseEvent giữa Scheduling và Adherence là **contract cần chốt ở GĐ6** (open-Q).

## 6. Open questions còn treo (chuyển GĐ6+, KHÔNG giải ở idea)
- **OQ-2/NFR số cứng** (giây/ms/số user) → spec NFR.
- **OQ-3 realtime vs batch** cho sinh DoseEvent + dispatch reminder → kiến trúc `/shape`.
- **OQ-4 retention** dữ liệu sức khoẻ bao lâu (NFR-4) → security spec GĐ6.
- **Ranh giới ghi DoseEvent** Scheduling↔Adherence → contract module GĐ6/GĐ10.
- **Độ rộng cửa sổ on-time (BR-4)** → cấu hình/NFR.

## 7. Cổng GĐ5 — DỪNG
*"Domain đủ rõ để định hình kiến trúc & ranh giới module chưa?"* → **CÓ.**
- Entity có identity + lifecycle ✔ · business rule bất biến liệt kê ✔ · domain event đặt tên ✔ ·
  ranh giới context + data ownership rõ ✔.
- Các câu còn lại đều là câu **kiến trúc/spec** (đúng tầng GĐ6+), không phải lỗ hổng domain.

→ **DỪNG. Không đi tiếp Architecture. Không code. Không tự kill.** Bàn giao ở file kèm.
