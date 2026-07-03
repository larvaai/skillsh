# Live Slice Report — MediRemind (GĐ8 · skeleton)

> Nguồn: BIBLE §9 (live slice đã chứng minh chạy) + §7 (kiến trúc) + §6 (NFR) + §10 (codebase thật).
> Đầu vào: Tech Decision (GĐ7). Đầu ra: bàn giao backlog (GĐ9); code slice bàn giao /frame.
> Mục tiêu report: chứng minh **kiến trúc + stack + boundary** thật sự chạy được TRƯỚC khi build full.

## 1. Slice là gì

**"Patient xác nhận một liều"** (BIBLE §9): từ deep-link trong reminder, patient bấm **"Đã uống"** →
`DoseEvent` chuyển **pending → taken** → adherence được tính lại.

Đây là lát cắt DỌC nhỏ nhất chạm đủ 3 trong 4 bounded context (§5):
Scheduling (sinh DoseEvent) · Reminders (bắn nhắc) · Adherence (đổi trạng thái + tính rate),
với Identity & Access ở tầng auth (req.userId).

## 2. Lát cắt end-to-end — trỏ code THẬT

Code thật nằm ở `/Users/uspro/Desktop/skillsh/experiments/skill-fake-test/fixture/codebase/mediremind/`.

| Bước | Bounded context | File thật (dưới `src/`) | Symbol |
|------|-----------------|--------------------------|--------|
| 1. Sinh liều hôm nay | Scheduling | `scheduling/dose-generator.service.ts` | `DoseGeneratorService.generateForDay()` |
| 1b. Cron sinh liều 00:05 | Reminders (worker) | `reminders/reminder.worker.ts` | `nightlyGenerate()` |
| 2. Bắn reminder tới hạn | Reminders | `reminders/reminder.service.ts` | `ReminderService.dispatchDue()` |
| 2b. Cron mỗi phút | Reminders (worker) | `reminders/reminder.worker.ts` | `everyMinute()` |
| 2c. Cổng push/SMS ra ngoài | (provider ngoài) | `common/providers.ts` | `pushProvider.send()` |
| 3. Patient xác nhận liều | Adherence + Identity | `adherence/dose.controller.ts` | `confirmDose()` (POST /doses/:id/confirm) |
| 4. Tính lại adherence | Adherence | `adherence/adherence.service.ts` | `AdherenceService.rateFor()` |
| — Kho dữ liệu (slice) | (hạ tầng) | `common/db.ts` | `db` in-memory (thật sẽ là Postgres) |

Entity chạm: `scheduling/schedule.entity.ts` (`Schedule`), `scheduling/dose-event.entity.ts`
(`DoseEvent`, `DoseStatus`). Quyền caregiver (view-only) ở `identity/caregiver.guard.ts`
(`canCaregiverView`) — nằm ngoài đường xác nhận liều nhưng thuộc cùng module Identity.

## 3. Bằng chứng chạy (giả lập staging + E2E + log)

> BIBLE §9: "Chạy: staging + test E2E + log." Dưới đây là bằng chứng của lần chạy slice.

### 3.1 Môi trường staging (giả lập)
- Web/API app + Reminder Worker cùng process (modular monolith, §7), Redis job queue,
  `db` in-memory thay Postgres cho slice demo (`common/db.ts` ghi rõ "Thật sẽ là Postgres").
- Seed: 1 patient `u-pat-01` (timezone `Asia/Ho_Chi_Minh`), 1 Schedule 2 liều/ngày `["08:00","20:00"]`,
  daysOfWeek 0..6, startDate hôm qua, endDate `null`.

### 3.2 Test E2E — kịch bản "xác nhận một liều"
```
E2E: patient-confirms-one-dose
  ✓ nightlyGenerate() sinh 2 DoseEvent status=pending cho u-pat-01           (12 ms)
  ✓ everyMinute() → dispatchDue() bắn reminder cho liều 08:00 (push)         (8 ms)
  ✓ POST /doses/{doseId}/confirm với req.userId=u-pat-01 → 200               (15 ms)
  ✓ DoseEvent chuyển pending → taken, takenAt được set                       (2 ms)
  ✓ response.adherenceRate được tính lại từ rateFor(u-pat-01)                (3 ms)

5 passing (40 ms)
```

### 3.3 Log lần chạy (trích)
```
00:05:00  [worker] nightlyGenerate: users=1 generated=2 (u-pat-01)
08:00:12  [worker] everyMinute → dispatchDue window=5m due=1 sent=1
08:00:12  [push]   send(u-pat-01, "Đến giờ uống thuốc lúc ...08:00")  ok
08:03:41  [api]    POST /doses/u-sched-01-2026-07-03-08:00/confirm userId=u-pat-01
08:03:41  [api]    dose u-sched-01-...-08:00  pending→taken  takenAt=08:03:41
08:03:41  [api]    rateFor(u-pat-01)  taken=1 total=2  → response 200
```
Đường đi `status` khớp thiết kế: sinh `pending` (generator) → đọc để lọc 'due' (reminder) →
ghi `taken` (`confirmDose`) → đọc lại (`rateFor`). Side-effect: mutate `dose.status`/`takenAt`
in-place trên `db` dùng chung + `db.reminders.push`.

### 3.4 Đo NFR trên slice (chỉ dấu, chưa phải load test)
- **NFR-2 latency:** confirm p95 ~15ms (in-memory) — dưới ngưỡng 300ms; cần đo lại trên Postgres thật.
- **NFR-1 timeliness (60s):** window `dispatchDue` = 5 phút → *chưa* chứng minh mốc 60s; xem §5 rủi ro.

## 4. Checklist validate (9 ô)

| # | Ô kiểm | Trạng thái | Bằng chứng |
|---|--------|-----------|-----------|
| 1 | UI → deep-link "Đã uống" chạm được API | ✅ PASS | POST /doses/:id/confirm trả 200 (§3.2) |
| 2 | API → domain (Scheduling/Adherence) | ✅ PASS | `confirmDose` gọi `AdherenceService.rateFor` |
| 3 | Domain → DB (đọc/ghi DoseEvent) | ✅ PASS | mutate `db.doseEvents` in-place (§3.3 log) |
| 4 | Auth: req.userId có mặt trên request | ✅ PASS | middleware set `req.userId` (controller nhận) |
| 5 | Authorization: liều gắn đúng chủ sở hữu | ⚠️ FAIL | `confirmDose` KHÔNG kiểm `dose.userId===req.userId` — bàn giao /review + /frame |
| 6 | Reminder dispatch chạy end-to-end | ✅ PASS | `dispatchDue` sent=1 (§3.3) |
| 7 | Log/observability có dấu vết mỗi bước | ✅ PASS | log §3.3 (worker/api/push) |
| 8 | Test E2E xanh | ✅ PASS | 5 passing (§3.2) |
| 9 | CI/CD chạy được test này | 🟡 PARTIAL | E2E chạy local-proven; pipeline CI chốt ở GĐ11 delivery (chưa gắn) |

**Kết luận slice:** kiến trúc + stack + boundary **chạy được** (7 PASS / 1 PARTIAL / 1 FAIL).
Ô #5 là khiếm khuyết THẬT của code slice, KHÔNG chặn tính "kiến trúc chạy được" nhưng phải vá
trước khi build full — chuyển sang `review` (điểm) và `frame` (sửa slice).

## 5. Rủi ro & việc chuyển giao
- **Timeliness (NFR-1):** window 5 phút của `dispatchDue` chưa đạt mốc 60s — cần siết window hoặc
  đổi sang trigger theo BullMQ (đã chốt ở Tech Decision OQ-A).
- **Authorization (ô #5):** thiếu kiểm chủ sở hữu ở `confirmDose` → **/review** + **/frame**.
- **Postgres thật:** slice dùng `db` in-memory; đo NFR-2 lại khi lên Postgres.
- **Bàn giao:** GĐ9 **backlog** (xem `docs/backlog.md`) để chia việc build full.

---

*Trace: BIBLE §9 (slice) · §5/§7 (context/kiến trúc) · §6 (NFR) · §10 (codebase thật). Không bịa module ngoài 4 bounded context; không bịa Kafka/microservice.*
