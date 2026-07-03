# PRD — MediRemind (GĐ4)

## Góc nhìn lãnh đạo (đọc trước)
PRD gộp Business + Product + Requirements thành một hợp đồng để bước sang Domain (GĐ5). MediRemind
nhắc uống thuốc và đo tuân thủ cho **patient** và **caregiver (chỉ-xem)**. Thành công đo bằng
**SM-1** (on-time dose rate +≥15 điểm phần trăm sau 30 ngày) và **SM-2** (≥60% caregiver-link kích
hoạt trong tuần đầu). Slice giá trị lõi = **xác nhận liều**. 5 NFR có số cứng ràng buộc timeliness
(≤60s), latency (≤300ms p95), scale (50k user / 250k DoseEvent/ngày), sensitivity (mã hoá + audit-log),
availability (99.5%). Không phải hệ cấp-cứu.

## 1. Mục tiêu & Success metrics
- **SM-1**: sau 30 ngày, on-time dose rate tăng **≥ 15 điểm phần trăm** so với baseline tự khai; đo bằng log xác nhận liều.
- **SM-2**: **≥ 60%** caregiver-link kích hoạt xem báo cáo trong tuần đầu.

## 2. Personas
- **Patient** (chính) · **Caregiver** (phụ, view-only) · Clinic admin **ngoài MVP**.

## 3. Phạm vi
**Trong**: khai Medication + Schedule → sinh DoseEvent → bắn Reminder (push, SMS fallback) →
xác nhận liều → tính AdherenceReport → caregiver xem báo cáo · liên kết Caregiver↔Patient (view-only).
**Ngoài**: clinic admin, kê đơn/tương tác thuốc, mọi tính năng cấp-cứu.

## 4. Domain entities (chốt cho GĐ5)
- **User** (role: patient | caregiver)
- **Medication** (name, dosage, form)
- **Schedule** (medication_id, times_per_day[], days_of_week[], start_date, end_date, timezone)
- **DoseEvent** (schedule_id, scheduled_time, status: pending|taken|missed|skipped, taken_at)
- **Reminder** (dose_event_id, channel: push|sms, sent_at)
- **CaregiverLink** (caregiver_id, patient_id, scope: view-only)
- **AdherenceReport** (user_id, period, rate)

## 5. Functional requirements (tóm; chi tiết AC ở requirements.md)
Slice trọng tâm **xác-nhận-liều** với AC-1..AC-5: xác nhận đúng liều pending, ghi nhanh (NFR-2),
chống xác nhận trùng, chỉ chủ liều xác nhận được (caregiver view-only), và liều quá hạn → missed.

## 6. Non-functional requirements
| Mã | Yêu cầu |
|----|---------|
| NFR-1 | Reminder bắn trong 60s so với scheduled_time. |
| NFR-2 | Ghi xác nhận liều ≤ 300ms p95. |
| NFR-3 | 50k active user, ~5 liều/user/ngày ≈ 250k DoseEvent/ngày. |
| NFR-4 | Mã hoá at-rest, kiểm soát truy cập, audit-log mọi truy cập của caregiver. |
| NFR-5 | Availability 99.5% (không life-critical). |

## 7. Rủi ro & phi-mục-tiêu
Dữ liệu sức khoẻ nhạy cảm là rủi ro chính → xử lý như ràng buộc bắt buộc. App không dùng cho cấp cứu.

## Truy vết
requirements.md → **prd.md (đây)** → domain (GĐ5) → shape (GĐ6).
