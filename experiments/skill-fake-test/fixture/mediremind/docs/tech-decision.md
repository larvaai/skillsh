# Tech Decision — MediRemind (GĐ7 · stack)

> Nguồn ràng buộc: BIBLE §7 (kiến trúc đã chốt) + §8 (ràng buộc chọn stack) + §6 (NFR).
> Đầu vào: Architecture Brief (GĐ6 shape). Đầu ra: bàn giao skeleton (GĐ8).
> Phạm vi: chọn **framework/runtime** cho Web/API app của modular monolith. KHÔNG chọn lại kiến trúc.

Kiến trúc đã chốt (BIBLE §7, KHÔNG mở lại ở đây):
- Modular monolith, 4 module = 4 bounded context (Scheduling · Reminders · Adherence · Identity & Access).
- Container: Web/API app · Reminder Worker (cron-driven) · Postgres · Redis (job queue) · Push/SMS provider (ngoài).

---

## 1. Tiêu chí & trọng số

Trọng số phản ánh ưu tiên trong BIBLE §8 ("tốc độ giao hàng > hiệu năng cực đại; tuyển người TS dễ")
và tính nhạy cảm NFR-4.

| # | Tiêu chí | Trọng số | Buộc từ |
|---|----------|----------|---------|
| C1 | Fit domain (job scheduling + push/SMS + Postgres) | 0.20 | §7, §8 |
| C2 | Fit team (3 dev, mạnh TypeScript, không Go/Java) | 0.25 | §8 |
| C3 | Fit scale (50k user, ~250k DoseEvent/ngày) | 0.15 | §6 NFR-3 |
| C4 | NFR khác (timeliness 60s, latency p95 ≤300ms, sensitivity at-rest+audit) | 0.20 | §6 NFR-1/2/4/5 |
| C5 | Tuyển người & maintainability | 0.20 | §8 |
|   | **Tổng** | **1.00** | |

Thang điểm mỗi ô: 1 (kém) – 5 (rất tốt). Điểm có trọng số = điểm × trọng số.

---

## 2. Phương án so sánh

Tất cả đều là ứng viên cho *Web/API app của một modular monolith TypeScript* — không xét ngôn ngữ ngoài TS
vì §8 nói rõ team không giỏi Go/Java và ưu tiên tuyển TS.

- **A — NestJS (Node/TS)**: framework có kiến trúc module sẵn (module/provider/DI), hợp modular monolith.
- **B — Fastify + cấu trúc module tự dựng (Node/TS)**: nhẹ, nhanh, ít khuôn.
- **C — NestJS + BullMQ (Redis) cho job**: chính là A nhưng chốt luôn cách xử lý OQ-A (job queue).

> C không phải "framework thứ ba" mà là A + một quyết định về job — tách ra để chấm riêng ảnh hưởng OQ-A.

---

## 3. Ma trận điểm

| Tiêu chí (trọng số) | A · NestJS | B · Fastify | C · NestJS+BullMQ |
|---|---|---|---|
| C1 Fit domain (0.20) | 4 → 0.80 | 3 → 0.60 | 5 → 1.00 |
| C2 Fit team TS (0.25) | 5 → 1.25 | 4 → 1.00 | 5 → 1.25 |
| C3 Fit scale (0.15) | 4 → 0.60 | 5 → 0.75 | 4 → 0.60 |
| C4 NFR khác (0.20) | 4 → 0.80 | 3 → 0.60 | 4 → 0.80 |
| C5 Tuyển & maintain (0.20) | 5 → 1.00 | 3 → 0.60 | 5 → 1.00 |
| **Tổng có trọng số** | **4.45** | **3.55** | **4.65** |

Ghi chú chấm điểm (bám ràng buộc, không tô hồng):
- **C2** A và C ăn điểm cao nhất: DI/module của Nest ánh xạ 1-1 với 4 bounded context §7, dev TS quen ngay.
- **C3** B nhỉnh: Fastify throughput cao hơn; nhưng 250k DoseEvent/ngày ≈ ~3 ghi/s trung bình —
  chưa phải bài toán ép hiệu năng, nên trọng số C3 để thấp (§8: hiệu năng cực đại KHÔNG ưu tiên).
- **C4** không phương án nào tự lo NFR-4 (mã hoá at-rest + audit-log) — đó là việc tầng hạ tầng/DB,
  không phải framework; chấm ngang, coi như trung tính.
- **C5** Nest có convention rõ → người mới đọc code nhanh; Fastify tự-dựng dễ mỗi dev một kiểu.

---

## 4. ADR-007 — Chọn framework cho Web/API app

- **Trạng thái:** Accepted (GĐ7).
- **Bối cảnh:** Đã chốt modular monolith 4 module (§7); cần framework để 3 dev TS build song song
  4 bounded context mà ranh giới không nhoè, ưu tiên tốc độ giao hàng (§8).
- **Quyết định:** Chọn **C — NestJS + BullMQ (Redis)**.
  - NestJS: mỗi bounded context = 1 Nest module, DI ép ranh giới rõ; điểm cao nhất C2/C5.
  - BullMQ trên Redis (đã có Redis trong container §7): dùng làm job queue cho Reminder Worker,
    đây chính là câu trả lời cho **OQ-A** (managed queue vs tự cron) — xem §5.
- **Hệ quả tích cực:** khuôn module khớp kiến trúc; tuyển TS dễ; job có retry/backoff sẵn của BullMQ,
  giúp về sau vá được lỗi "gửi reminder không retry" quan sát trong slice code hiện tại
  (`reminder.service.ts`).
- **Hệ quả phải chịu:** Nest có overhead học DI/decorators cho ai chưa quen; BullMQ buộc Redis là
  thành phần bắt buộc (đã nằm trong §7 nên chấp nhận được).
- **Phương án đã loại:**
  - **B Fastify tự-dựng** — nhanh hơn nhưng thiếu khuôn module → rủi ro ranh giới 4 context nhoè,
    ngược mục tiêu "3 team song song". Loại vì C2/C5 thấp, mà đó là 2 trọng số nặng nhất.
  - **A Nest thuần (không chốt job)** — tốt nhưng để **OQ-A treo**; kém C vì không giải quyết job scheduling
    vốn là lõi domain (Reminder Worker cron-driven, §7).

---

## 5. Open-Question — trạng thái sau GĐ7

- **OQ-A (managed job-queue vs tự cron — treo từ §7 / GĐ6):** **ĐÓNG** tại ADR-007 →
  dùng **BullMQ trên Redis** (managed-in-process queue) thay cho tự viết cron toàn cục.
  (Đối chiếu: slice hiện dùng cron thủ công ở `reminders/reminder.worker.ts` và còn tàn dư
  `legacy/old_reminder_cron.ts` dùng `setInterval` toàn cục — hướng BullMQ thay được cả hai.)
- **OQ-B (retention / giữ dữ liệu bao lâu cho NFR-4 §6):** **TREO — chưa đóng.**
  Đây là quyết định vận hành/tuân thủ (dữ liệu sức khoẻ nhạy cảm), KHÔNG thuộc lựa chọn framework,
  nên GĐ7 **không** đóng. Cần đưa vào Delivery Standards / retention policy ở giai đoạn sau.
  → **Để nguyên OQ-B treo.**

---

*Trace: BIBLE §6 (NFR) · §7 (kiến trúc) · §8 (ràng buộc stack). OQ-B để hở đúng chủ ý — không bịa quyết định retention.*
