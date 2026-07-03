# FIXTURE BIBLE — MediRemind (nguồn sự thật DUY NHẤT)

> Mọi artifact fake PHẢI bám file này. KHÔNG được bịa số/thực thể mâu thuẫn.
> Dự án giả lập đang ở **giữa GĐ11 (delivery/build)** của pipeline Idea→Operate.
> `project key = mediremind`.

## 1. Bức tranh
MediRemind — app nhắc uống thuốc & theo dõi tuân thủ (adherence) cho người phải uống
nhiều loại thuốc mỗi ngày (người già + bệnh mạn tính) và người chăm sóc (caregiver) theo dõi từ xa.

## 2. Personas
- **Patient** (chính): uống 3–8 loại thuốc/ngày, hay quên liều.
- **Caregiver** (phụ): con cái/điều dưỡng, theo dõi adherence của patient từ xa, chỉ-xem.
- Clinic admin: NGOÀI MVP.

## 3. Giá trị & Success metric (GĐ1 / PRD)
- Giá trị: tăng tỉ lệ uống thuốc đúng giờ (on-time dose rate).
- **SM-1 (đo được):** Sau 30 ngày dùng, on-time dose rate tăng ≥ 15 điểm phần trăm so với
  baseline tự khai; đo bằng log xác nhận liều trong app.
- **SM-2:** ≥ 60% caregiver-link được kích hoạt xem báo cáo trong tuần đầu.

## 4. Domain entities (GĐ5)
- **User** (role: patient | caregiver)
- **Medication** (name, dosage, form)
- **Schedule** (medication_id, times_per_day[], days_of_week[], start_date, end_date, timezone)
- **DoseEvent** (schedule_id, scheduled_time, status: pending|taken|missed|skipped, taken_at)
- **Reminder** (dose_event_id, channel: push|sms, sent_at)
- **CaregiverLink** (caregiver_id, patient_id, scope: view-only)
- **AdherenceReport** (user_id, period, rate)

## 5. Bounded contexts (GĐ5→6)
- **Scheduling** — Medication, Schedule, sinh DoseEvent.
- **Reminders** — dispatch Reminder qua channel.
- **Adherence** — chuyển trạng thái DoseEvent, tính AdherenceReport.
- **Identity & Access** — User, CaregiverLink, quyền.

## 6. NFR (GĐ2–4) — số CỨNG, mọi skill lấy từ đây
- **NFR-1 timeliness:** Reminder phải bắn trong vòng 60s so với scheduled_time.
- **NFR-2 latency:** ghi xác nhận liều ≤ 300ms p95.
- **NFR-3 scale (MVP):** 50k active user, ~5 liều/user/ngày ≈ 250k DoseEvent/ngày.
- **NFR-4 sensitivity:** dữ liệu thuốc là nhạy cảm sức khoẻ → mã hoá at-rest, kiểm soát truy cập,
  audit-log cho mọi truy cập của caregiver.
- **NFR-5 availability:** 99.5% (không phải life-critical; app ghi rõ "không dùng cho cấp cứu").

## 7. Kiến trúc (GĐ6) — ĐÃ CHỐT hình hài (chưa chốt framework)
- Modular monolith (đội nhỏ, chọn thay vì microservices).
- Container: Web/API app · Reminder Worker (cron-driven) · Postgres · Redis (job queue) ·
  Push/SMS provider (ngoài).
- Ranh giới module = 4 bounded context ở mục 5.
- **Open-Q kiến trúc còn treo → GĐ7:** dùng managed job-queue hay tự cron? (chuyển cho stack)

## 8. Ràng buộc chọn stack (GĐ7) — input cho skill `stack`, KHÔNG phải quyết định sẵn
- Đội: 3 dev, mạnh TypeScript, chưa ai giỏi Go/Java.
- Cần: mobile push + SMS fallback; job scheduling; Postgres.
- Ưu tiên: tốc độ giao hàng > hiệu năng cực đại; tuyển được người TS dễ.
  (skill `stack` tự chấm matrix & chọn — KHÔNG chép sẵn ở đây.)

## 9. Live slice (GĐ8) — ĐÃ chứng minh chạy
- Slice: **"Patient xác nhận một liều"** — từ deep-link trong reminder, patient bấm "Đã uống",
  DoseEvent pending→taken, adherence tính lại.
- Chạy: staging + test E2E + log. (Live Slice Report do fixture dựng.)

## 10. Codebase thật (cho code-skills) — nằm ở fixture/codebase/mediremind/
Slice dọc "sinh DoseEvent hôm nay → gửi reminder → xác nhận liều → tính adherence", viết TS kiểu NestJS thu nhỏ.
Đây là code THẬT có khuyết tật CÀI SẴN (xem ANSWER-KEY.md). Các file: xem cây thư mục đó.

## 11. Trạng thái pipeline HIỆN TẠI (cho progress/resume/traceability)
- GĐ0–9: XONG (idea→domain→shape→stack→skeleton→backlog đủ artifact).
- GĐ10 modules: XONG (module-map + contracts).
- GĐ11 delivery: ĐANG (delivery-standards vừa xong; đang build workers/controllers).
- GĐ12 uat: **CHƯA** (planted gap).
- GĐ13 ship: **CHƯA ký** (planted gap).
- GĐ14 operate: chưa.
- Con trỏ progress: `gd11_delivery`.

## 12. GAP CÀI SẴN cho traceability (đừng "sửa" khi dựng fixture — để nguyên)
- G-1: THIẾU hẳn `uat.md` (GĐ12) dù code đang build → chain đứt Req→Test.
- G-2: `ship.md` tồn tại nhưng cổng GO/NO-GO CHƯA có 2 chữ ký (CTO+PO) → cổng chưa qua.
- G-3: 2 open-question chưa đóng: OQ-A (managed queue vs cron — treo từ GĐ6), OQ-B (giữ dữ liệu
  bao lâu / retention cho NFR-4) — không artifact nào đóng.
- G-4: Rollback plan trong ship.md CHƯA test (ghi "chưa chạy thử").
