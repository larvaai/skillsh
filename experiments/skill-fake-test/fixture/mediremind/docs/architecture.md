# MediRemind — Architecture Brief (GĐ6)

> Nguồn sự thật: BIBLE §7 (kiến trúc đã chốt hình hài), §5 (bounded context = ranh giới module),
> §6 NFR (đặc biệt NFR-4). **Chưa chốt framework** (đó là GĐ7 / skill `stack`).
> Open-Q "managed queue vs cron" CÒN TREO → GĐ7.

## 1. Architecture Brief

| Mục | Quyết định | Bám |
|-----|-----------|-----|
| **Kiến trúc style** | Modular monolith (một deploy, ranh giới module rõ trong mã) | §7: đội nhỏ, chọn thay vì microservices |
| **Ranh giới module** | 4 module = 4 bounded context: Scheduling · Reminders · Adherence · Identity & Access | §5, §7 |
| **Data store** | Postgres (dữ liệu domain) · Redis (job queue) | §7 |
| **Xử lý nền** | Reminder Worker (cron-driven) đọc DoseEvent tới hạn → phát Reminder | §7 |
| **Tích hợp ngoài** | Push/SMS provider (bên thứ ba) | §7 |
| **Framework/ngôn ngữ** | **CHƯA CHỐT** — chuyển GĐ7 | §7 (chưa chốt framework) |
| **Timeliness** | Reminder ≤ 60s so với scheduled_time | NFR-1 |
| **Latency** | Ghi xác nhận liều ≤ 300ms p95 | NFR-2 |
| **Scale (MVP)** | 50k active user · ~250k DoseEvent/ngày | NFR-3 |
| **Bảo mật** | Nhạy cảm sức khoẻ → mã hoá at-rest, kiểm soát truy cập, audit-log truy cập caregiver | NFR-4 |
| **Availability** | 99.5% (không life-critical; app ghi "không dùng cho cấp cứu") | NFR-5 |

## 2. C4 — Context

```
                    ┌─────────────────────────────────────────┐
    Patient  ─────► │                                         │
   (uống thuốc)     │            MediRemind System            │ ──► Push/SMS provider
                    │      (nhắc liều & theo dõi adherence)   │      (bên thứ ba)
   Caregiver ─────► │                                         │
   (chỉ-xem)        └─────────────────────────────────────────┘
```

- **Patient** — người dùng chính, xác nhận liều.
- **Caregiver** — người dùng phụ, chỉ-xem báo cáo adherence của patient.
- **Push/SMS provider** — hệ ngoài, MediRemind đẩy Reminder qua đó.

## 3. C4 — Container

```
┌──────────────────────────── MediRemind (modular monolith) ────────────────────────────┐
│                                                                                        │
│   ┌───────────────────────┐         ┌──────────────────────────┐                       │
│   │   Web/API app         │         │   Reminder Worker         │                       │
│   │   (4 module bên trong)│         │   (cron-driven)           │                       │
│   │  ┌─────────────────┐  │         │  đọc DoseEvent tới hạn    │                       │
│   │  │ Identity&Access │  │         │  → phát Reminder          │                       │
│   │  │ Scheduling      │  │         └───────────┬──────────────┘                       │
│   │  │ Reminders       │  │                     │                                       │
│   │  │ Adherence       │  │                     │ enqueue / dequeue job                 │
│   │  └─────────────────┘  │                     ▼                                       │
│   └──────────┬────────────┘         ┌──────────────────────────┐                       │
│              │  read/write          │   Redis (job queue)       │                       │
│              ▼                      └──────────────────────────┘                       │
│   ┌───────────────────────┐                                                            │
│   │   Postgres            │  ◄── mã hoá at-rest (NFR-4)                                 │
│   └───────────────────────┘                                                            │
└────────────────────────────────────────────────────────────────────────────────────────┘
            │                                          │
            ▼ (Reminder dispatch)                      │
   ┌───────────────────────┐                           │
   │  Push/SMS provider    │ ◄─────────────────────────┘
   │  (ngoài)              │
   └───────────────────────┘
```

Container (BIBLE §7): **Web/API app** · **Reminder Worker (cron-driven)** · **Postgres** · **Redis (job queue)** · **Push/SMS provider (ngoài)**. Bên trong Web/API app là 4 module theo 4 bounded context.

## 4. Data Flow — "sinh liều → nhắc → xác nhận → tính adherence"

```
1. Scheduling: Schedule tới mốc giờ → sinh DoseEvent (status=pending) ─────► Postgres
2. Reminder Worker (cron): quét DoseEvent pending tới hạn → enqueue job ──► Redis
3. Reminders: dequeue → gửi Reminder (push|sms) ──────────────────────────► Push/SMS provider
                                                    (mục tiêu ≤ 60s / NFR-1)
4. Patient bấm "Đã uống" trong reminder (deep-link)
     → Adherence: DoseEvent pending → taken, set taken_at ────────────────► Postgres
                                                    (ghi ≤ 300ms p95 / NFR-2)
5. Adherence: tính lại AdherenceReport (rate) ────────────────────────────► Postgres
```

Đây đúng slice dọc đã chứng minh chạy ở GĐ8 ("Patient xác nhận một liều").

## 5. Integration Model

| Tích hợp | Kiểu | Chiều | Ghi chú |
|----------|------|-------|---------|
| Web/API ↔ Postgres | DB connection | 2 chiều | Store domain data; mã hoá at-rest (NFR-4). |
| Web/API ↔ Redis | Job queue | 2 chiều | Enqueue/dequeue job nhắc liều. |
| Reminder Worker → Redis | Job queue | 1 chiều (producer) | Cron quét DoseEvent tới hạn, đẩy job. |
| Reminders → Push/SMS provider | API ngoài | 1 chiều (outbound) | Gửi push, fallback sms. |

**Cách quản job scheduling giữa Worker và Redis là OPEN-Q còn treo** (xem §7 dưới).

## 6. Security Model (bám NFR-4)

Dữ liệu thuốc là **dữ liệu nhạy cảm sức khoẻ**. Mô hình bảo mật bám thẳng NFR-4:

- **Mã hoá at-rest**: dữ liệu domain trong Postgres được mã hoá at-rest.
- **Kiểm soát truy cập**: phân quyền theo `User.role`. Patient sở hữu & toàn quyền trên dữ liệu thuốc của mình; **caregiver chỉ-xem** (`CaregiverLink.scope = view-only`) và chỉ với patient đã link.
- **Audit-log cho truy cập caregiver**: MỌI lần caregiver truy cập dữ liệu patient được ghi audit-log (theo NFR-4).
- **Ranh giới bảo mật**: module **Identity & Access** là điểm chốt kiểm quyền cho toàn hệ; các module khác gọi qua nó để xác thực scope.

> **OQ-B (retention) còn treo:** giữ dữ liệu thuốc/audit-log bao lâu để đủ NFR-4 — CHƯA có quyết định trong tài liệu này (chưa artifact nào đóng).

## 7. Open Questions (còn treo → GĐ7)

- **OQ-A — Managed queue vs tự cron:** dùng managed job-queue hay tự cron cho Reminder Worker? Ảnh hưởng độ tin cậy NFR-1 (≤60s) & vận hành. **CÒN TREO → chuyển GĐ7 (skill `stack`).** KHÔNG chốt ở đây.

## 8. ADRs

### ADR-001 — Modular monolith thay vì microservices

- **Trạng thái:** Đã chốt (GĐ6).
- **Bối cảnh:** Đội 3 dev, MVP, 4 bounded context. Cần ranh giới rõ nhưng không muốn chi phí vận hành nhiều service.
- **Quyết định:** Một **modular monolith** — một deploy, 4 module trong-mã theo 4 bounded context (Scheduling · Reminders · Adherence · Identity & Access).
- **Phương án đã loại:**
  - *Microservices (mỗi bounded context 1 service):* loại — đội quá nhỏ để gánh chi phí vận hành/deploy/observability của nhiều service; ranh giới in-code đã đủ cho MVP.
  - *Big-ball-of-mud monolith (không ranh giới module):* loại — mất khả năng tách sau này & làm mờ data ownership giữa 4 context.
- **Hệ quả:** Ranh giới phải giữ kỷ luật trong mã (module không gọi chéo tuỳ tiện); có thể tách service về sau nếu scale vượt MVP.

### ADR-002 — Xử lý nhắc liều bằng Reminder Worker + job queue (tách khỏi Web/API)

- **Trạng thái:** Đã chốt hình hài; **cơ chế queue cụ thể còn treo (OQ-A → GĐ7)**.
- **Bối cảnh:** NFR-1 buộc Reminder bắn ≤ 60s so với scheduled_time, ở scale ~250k DoseEvent/ngày (NFR-3). Việc quét & gửi nhắc không nên chặn request path của Web/API (giữ NFR-2 ≤300ms p95).
- **Quyết định:** Tách **Reminder Worker (cron-driven)** riêng khỏi Web/API app, dùng **Redis làm job queue** trung gian giữa việc quét-tới-hạn và việc gửi Reminder.
- **Phương án đã loại:**
  - *Gửi Reminder đồng bộ trong request Web/API:* loại — chặn request path, phá NFR-2 và không đảm bảo được NFR-1 khi tải cao.
  - *Quét DB liên tục không qua queue (busy-poll trực tiếp gửi):* loại — khó kiểm soát retry/độ trễ, dội tải Postgres, khó đạt cửa 60s ổn định.
- **Hệ quả:** Cần một cơ chế job-queue — **managed queue hay tự cron vẫn là OQ-A còn treo, quyết ở GĐ7**; ADR này chỉ chốt việc *tách worker + dùng queue*, không chốt công nghệ queue.
