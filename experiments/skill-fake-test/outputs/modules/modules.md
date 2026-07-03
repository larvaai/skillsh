# MediRemind — Module Map + Module Contracts (GĐ10 · modules)

> Nguồn: Domain Model (GĐ5, `docs/domain-model.md`) · Backlog (GĐ9, `docs/backlog.md`) · Architecture Brief (GĐ6, `docs/architecture.md`).
> Vai: `modules` = Chủ sở hữu (Kiến trúc sư + Eng managers) dựng artifact + trình bằng chứng. Người duyệt (mở cổng GO) = **CTO/user**.

```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Roadmap + Backlog (Epic→Feature→Story→AC)" lấy từ file bạn đưa (docs/backlog.md, docs/domain-model.md,
  docs/architecture.md), CHƯA qua cổng GĐ9 (skill /backlog) trong state.
- Rủi ro: (1) chưa truy vết ngược được về pipeline state; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật;
  (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo tài liệu của bạn. Muốn chuẩn + có traceability: chạy /backlog trước để có bản đã qua cổng.
```

---

# Artifact 1 — MODULE MAP

## Góc nhìn lãnh đạo (đọc trước — "ai chịu trách nhiệm cái gì khi có sự cố?")

MediRemind là **modular monolith** (một deploy, 4 module trong-mã theo 4 bounded context). Bốn team sở hữu bốn phần, không chồng chéo:

| Sự cố xảy ra ở… | Gọi ngay team | Team sở hữu |
|---|---|---|
| Lịch thuốc sai / liều không sinh ra / sinh sai giờ | **Team Scheduling** | thuốc, lịch, sinh liều |
| Không nhận được nhắc / nhắc bị lặp / nhắc trễ | **Team Reminders** | dispatch nhắc qua push/sms |
| Bấm "Đã uống" không ăn / báo cáo adherence sai | **Team Adherence** | trạng thái liều, tỉ lệ tuân thủ |
| Đăng nhập / phân quyền / caregiver xem được data không nên xem | **Team Identity & Access** | user, caregiver-link, quyền, audit-log |

Một dòng cho CTO: **4 module = 4 bounded context = 4 team**. Mỗi liều thuốc (DoseEvent) do Scheduling *sinh ra*, Reminders *đọc để nhắc*, Adherence *đổi trạng thái* — ba team chạm một entity nhưng mỗi team sở hữu đúng một trách nhiệm, ranh giới ở phần "Does NOT own" bên dưới.

## Bảng module × owner × sở hữu / KHÔNG sở hữu

| Module | Bounded context (GĐ5) | Owner | Sở hữu (data) | KHÔNG sở hữu |
|---|---|---|---|---|
| **Scheduling** | Scheduling | Team Scheduling | Medication, Schedule; **sinh** DoseEvent | dispatch nhắc · đổi trạng thái liều · user/quyền |
| **Reminders** | Reminders | Team Reminders | Reminder (lần nhắc đã bắn) | sinh liều · đổi trạng thái liều · user/quyền · dedupe business rule của liều |
| **Adherence** | Adherence | Team Adherence | **vòng đời trạng thái** DoseEvent (pending→taken/missed/skipped), AdherenceReport | sinh DoseEvent · gửi nhắc · user/quyền |
| **Identity & Access** | Identity & Access | Team Identity | User, CaregiverLink, quyền, audit-log truy cập | mọi data domain thuốc/liều/nhắc/report |

## Sơ đồ phụ thuộc (ai gọi ai — mọi phụ thuộc đi qua contract/event)

```
                         ┌────────────────────────────────────────────┐
                         │           Identity & Access                 │
                         │  (User · CaregiverLink · quyền · audit-log)  │
                         └──▲──────────▲──────────▲──────────▲──────────┘
   check permission / scope │          │          │          │  (mọi module gọi vào để xác thực)
                            │          │          │          │
              ┌─────────────┴───┐  ┌───┴──────┐  ┌┴──────────┴───┐
              │   Scheduling     │  │ Reminders │  │   Adherence    │
              │ Medication,      │  │ Reminder  │  │ DoseEvent-state│
              │ Schedule,        │  │           │  │ AdherenceReport│
              │ sinh DoseEvent   │  │           │  │                │
              └───────┬──────────┘  └────▲──────┘  └───────▲────────┘
                      │ event DoseEventGenerated │          │
                      │ (Scheduling phát)        │          │
                      └──────────────────────────┘          │
                            Reminder Worker (cron) đọc DoseEvent pending tới hạn
                            → Reminders dispatch;  Patient "Đã uống" → Adherence đổi trạng thái
```

Phụ thuộc rõ:
- **Scheduling → Identity** (đọc user để gắn `userId` chủ liều/lịch).
- **Reminders → Scheduling data (DoseEvent pending tới hạn, qua Reminder Worker cron)** + **→ Identity** (biết chủ liều để nhắc đúng người).
- **Adherence → Scheduling data (DoseEvent để đổi trạng thái)** + **→ Identity** (kiểm quyền chủ liều + caregiver view-only).
- **Identity & Access**: không phụ thuộc module nào; mọi module gọi vào nó để check permission/scope + ghi audit-log (điểm chốt bảo mật NFR-4, theo Architecture §6).

## Entity giao thoa DoseEvent — quyết định ranh giới + lý do

DoseEvent bị **3 module chạm** (Scheduling tạo · Reminders đọc · Adherence đổi trạng thái). Cắt như sau:

- **Scheduling SỞ HỮU việc SINH** DoseEvent (từ Schedule + timezone) và ghi bản ghi ban đầu `status=pending`.
- **Adherence SỞ HỮU vòng đời TRẠNG THÁI** DoseEvent (pending→taken/missed/skipped) — vì chuyển trạng thái + tính AdherenceReport là một trách nhiệm nghiệp vụ (bám Domain §4: "Adherence sở hữu việc chuyển trạng thái").
- **Reminders chỉ ĐỌC** DoseEvent tới hạn để dispatch; **không** đổi trạng thái, **không** sinh liều.

**Lý do tách trạng thái khỏi Scheduling (cách chia đã loại):** đã cân *gộp toàn bộ DoseEvent + trạng thái + adherence vào Scheduling* (một module "liều") — loại vì (1) Domain §4 tách rõ Scheduling (sinh) khỏi Adherence (chuyển trạng thái + tính report); (2) tần suất đổi khác nhau: quy tắc sinh lịch/timezone (Scheduling) đổi độc lập với quy tắc tính rate/mẫu số adherence (Adherence); (3) hai capability nghiệp vụ khác nhau, muốn hai team chạy song song (E1 vs E3). Ranh giới: cột `status`/`taken_at` của DoseEvent do **Adherence** ghi; các cột định danh liều (`schedule_id`, `scheduled_time`) do **Scheduling** ghi lúc sinh. Ghi-chéo đi qua contract, không hai team cùng UPDATE tự do một cột.

**Lý do KHÔNG tách Reminders vào Scheduling (cách chia đã loại):** đã cân *gộp dispatch nhắc vào Scheduling* — loại vì (1) Domain §5 tách Reminders thành context riêng; (2) Architecture §3 tách **Reminder Worker (cron-driven)** khỏi Web/API để giữ NFR-2 (≤300ms p95) — dispatch là đường nền bất đồng bộ, tần suất/áp lực vận hành khác request path của Scheduling; (3) tích hợp provider ngoài (push/sms) là ranh giới integration + failure domain riêng (E2 retry/bền vững).

**Lý do KHÔNG tách audit-log/permission thành module riêng (cách chia đã loại):** đã cân *tách "Security/Audit" riêng* — loại vì permission + caregiver-scope + audit đều bám thẳng entity User/CaregiverLink của **Identity & Access** (Domain §5) và Architecture §6 chỉ định Identity & Access là "điểm chốt kiểm quyền cho toàn hệ". Tách ra sẽ chia đôi quyền sở hữu bảng user/link.

---

# Artifact 2 — MODULE CONTRACTS

> Mỗi contract MỞ bằng 1 câu lãnh đạo (giữ phần nghiệp vụ nào · hỏng thì ai gọi ai), rồi tới chi tiết dev.
> Public API mô tả bằng OpenAPI-style để team khác gọi mà không cần đọc code bên trong.
> Độ sâu theo Đủ-là-đủ: 3 module lõi (Scheduling/Adherence/Identity) đầy đủ; Reminders là đường nền, một số ô gọn.

---

## CONTRACT — Scheduling · Owner: Team Scheduling · [LÕI]

**[Lãnh đạo]** Giữ toàn bộ **thuốc + lịch uống + việc sinh ra từng liều đúng giờ/đúng timezone**. Liều không sinh ra, sinh sai giờ, hoặc lịch hết hạn vẫn sinh → hỏi Team Scheduling.

- **Responsibilities**: tạo/sửa Medication & Schedule của patient · sinh DoseEvent từ Schedule theo `timezone` + `daysOfWeek` + `timesOfDay` · KHÔNG sinh liều cho Schedule đã hết `endDate`.
- **Owns (data/event)**:
  - Bảng `medications`, `schedules`.
  - Bản ghi DoseEvent lúc **sinh mới** (các cột định danh: `schedule_id`, `scheduled_time`, `status=pending` ban đầu).
  - Phát event **`DoseEventGenerated`** (Reminders/Adherence lắng nghe).
- **Does NOT own**:
  - Chuyển trạng thái DoseEvent (pending→taken/missed/skipped) → **Adherence**.
  - Gửi nhắc → **Reminders**.
  - Danh tính user / kiểm quyền → **Identity & Access**.
- **Public API** (OpenAPI-style):
  - `POST /schedules` — tạo Schedule `{medicationId, timesOfDay[], daysOfWeek[], startDate, endDate?, timezone}` → `201 {scheduleId}`. Gắn `userId` từ token (Identity).
  - `PUT /schedules/{id}` — sửa Schedule (chỉ chủ sở hữu).
  - `POST /medications` — khai một thuốc `{name, dosage, form}` → `201 {medicationId}`.
  - `GET /schedules?userId=` — lịch của patient.
  - *(sinh DoseEvent là quá trình nền do Scheduling chạy theo lịch, không phải endpoint công khai.)*
- **Domain events**: **phát** `DoseEventGenerated {doseEventId, scheduleId, userId, scheduledTime}`; **nghe** — không.
- **Permission model**: chỉ **Patient chủ sở hữu** tạo/sửa Schedule & Medication của mình; Caregiver **không** (view-only, và không xem cấu hình lịch); kiểm qua Identity.
- **Error codes**: `SCHED_ENDDATE_IN_PAST` (Schedule hết hạn → không sinh liều — AC-1.1.2) · `SCHED_INVALID_TIMEZONE` · `SCHED_NOT_OWNER` (403).
- **SLA/SLO**: sinh DoseEvent phải kịp để Reminders bắn ≤60s so với `scheduledTime` (nền cho NFR-1); liều rơi đúng giờ LOCAL theo `schedule.timezone` (AC-1.2.1).
- **Test contract**: Reminders + Adherence phụ thuộc event `DoseEventGenerated` (contract test Scheduling↔Reminders, Scheduling↔Adherence): schema `{doseEventId, scheduleId, userId, scheduledTime}` ổn định.

---

## CONTRACT — Reminders · Owner: Team Reminders · [ĐƯỜNG NỀN / ĐỐI NGOẠI]

**[Lãnh đạo]** Giữ việc **bắn đúng một nhắc, đúng giờ, cho mỗi liều tới hạn**, qua push/sms bên thứ ba. Không nhận nhắc / nhắc lặp / nhắc trễ → hỏi Team Reminders.

- **Responsibilities**: dequeue liều tới hạn (Reminder Worker cron → Redis, Architecture §3) · gửi Reminder qua channel (push|sms) · dedupe theo `doseEventId` (đúng một nhắc/liều) · retry khi provider lỗi, một lỗi không vỡ cả lô.
- **Owns (data/event)**: bảng `reminders` (mỗi bản ghi = một lần nhắc đã bắn: `dose_event_id`, `channel`, `sent_at`) · phát event **`ReminderSent`** (Adherence/analytics có thể nghe).
- **Does NOT own**:
  - Sinh DoseEvent → **Scheduling**.
  - Chuyển trạng thái DoseEvent (kể cả pending→missed khi hết hạn) → **Adherence**.
  - Danh tính / kênh liên lạc của user, quyền → **Identity & Access**.
  - Chọn công nghệ queue (managed vs cron) — OQ-A còn treo ở GĐ7, ngoài phạm vi contract này.
- **Public API** (OpenAPI-style): **không có REST public** — Reminders là consumer nền, kích hoạt bởi Reminder Worker cron đọc DoseEvent pending tới hạn (Architecture §4). *(Ô Public-API rút gọn "không REST public" vì module không lộ interface đồng bộ ra ngoài — đây là đường nền, không phải rủi ro thấp bị bỏ.)*
- **Domain events**: **nghe** `DoseEventGenerated` (để biết liều nào sẽ tới hạn); **phát** `ReminderSent {doseEventId, channel, sentAt}`.
- **Permission model**: chỉ chạy nội bộ (Worker/hệ thống); không endpoint người-dùng. Gọi Identity để lấy kênh liên lạc hợp lệ của chủ liều nếu cần.
- **Error codes**: `RMD_PROVIDER_FAILED` (một liều lỗi → retry, không vỡ lô — AC-2.2.1) · `RMD_RETRY_EXHAUSTED` (hết retry → ghi audit — AC-2.2.2). Dedupe không tạo lỗi công khai, chỉ no-op lần thứ hai.
- **SLA/SLO**: Reminder bắn **≤60s** so với `scheduledTime` (NFR-1, AC-2.1.2) · **đúng một** nhắc/liều (dedupe theo `doseEventId`, AC-2.1.1) · scale ~250k DoseEvent/ngày (NFR-3).
- **Test contract**: dựa trên event `DoseEventGenerated` từ Scheduling (contract test Reminders↔Scheduling) · dedupe test theo `doseEventId`.

---

## CONTRACT — Adherence · Owner: Team Adherence · [LÕI]

**[Lãnh đạo]** Giữ **trạng thái từng liều (đã uống/bỏ/lỡ) và tỉ lệ tuân thủ**. Bấm "Đã uống" không ăn, hoặc báo cáo adherence sai số → hỏi Team Adherence.

- **Responsibilities**: chuyển trạng thái DoseEvent `pending→taken/missed/skipped` (an toàn quyền) · đánh `missed` khi quá hạn không xác nhận · tính AdherenceReport (`rate` theo `period`) đúng mẫu số.
- **Owns (data/event)**:
  - **Vòng đời trạng thái** DoseEvent — các cột `status`, `taken_at` (ghi khi patient xác nhận).
  - Bảng `adherence_reports` (`user_id`, `period`, `rate`).
  - Phát event **`DoseTaken`** / **`DoseMissed`** (analytics/caregiver notify về sau nghe).
- **Does NOT own**:
  - Sinh DoseEvent + cột định danh liều (`schedule_id`, `scheduled_time`) → **Scheduling**.
  - Gửi nhắc → **Reminders**.
  - Danh tính / kiểm quyền chủ liều & caregiver-scope → **Identity & Access** (Adherence gọi vào để kiểm, không tự định nghĩa quyền).
- **Public API** (OpenAPI-style):
  - `POST /doses/{id}/confirm` — patient bấm "Đã uống": `pending→taken`, set `takenAt` → `200`. **403** nếu liều thuộc user khác (AC-3.1.2).
  - `POST /doses/{id}/skip` — patient chủ động bỏ liều → `pending→skipped`.
  - `GET /adherence?userId=&period=` — trả AdherenceReport (`rate`); chưa có DoseEvent → giá trị xác định (0 hoặc "chưa có dữ liệu"), KHÔNG NaN (AC-3.2.1).
- **Domain events**: **nghe** `DoseEventGenerated` (biết liều mới để theo dõi/đánh missed khi quá hạn); **phát** `DoseTaken`, `DoseMissed`.
- **Permission model**: chỉ **Patient chủ liều** đổi trạng thái liều của mình (confirm/skip); **Caregiver view-only** đọc AdherenceReport của patient đã link (không đổi trạng thái) — kiểm qua Identity (`canCaregiverView`).
- **Error codes**: `DOSE_NOT_OWNER` (403 — confirm liều của người khác, AC-3.1.2) · `DOSE_ALREADY_FINALIZED` (liều không còn pending) · `ADH_NO_DATA` (không NaN, AC-3.2.1).
- **SLA/SLO**: ghi xác nhận liều **≤300ms p95** (NFR-2, đường sống SM-1) · mẫu số rate chỉ gồm `taken+missed`, loại `skipped/pending` (AC-3.2.2).
- **Test contract**: consume event `DoseEventGenerated` (Scheduling↔Adherence) · caregiver-view kiểm quyền qua Identity (`canCaregiverView`) là contract Adherence↔Identity · dose ownership test (403 cross-user).

---

## CONTRACT — Identity & Access · Owner: Team Identity · [LÕI · điểm chốt bảo mật NFR-4]

**[Lãnh đạo]** Giữ **ai là ai, ai được xem gì, và ghi lại mọi lần caregiver xem dữ liệu patient**. Đăng nhập hỏng, phân quyền sai, caregiver xem được data không nên xem → hỏi Team Identity. Đây là điểm chốt kiểm quyền toàn hệ (Architecture §6).

- **Responsibilities**: quản lý User (patient/caregiver) & xác thực · quản lý CaregiverLink (tạo, chấp nhận, scope view-only) · cấp quyết định phân quyền cho mọi module (chủ sở hữu? caregiver-view?) · ghi audit-log truy cập caregiver (NFR-4).
- **Owns (data/event)**:
  - Bảng `users` (role: patient|caregiver), `caregiver_links` (`caregiver_id`, `patient_id`, `scope=view-only`), `audit_log`.
  - Phát event **`CaregiverLinkActivated`** (đo SM-2 — link được kích hoạt).
- **Does NOT own**:
  - Dữ liệu thuốc/lịch/liều/nhắc/report — thuộc Scheduling/Reminders/Adherence. Identity chỉ **cấp danh tính + phán quyết truy cập**, KHÔNG lưu nội dung domain thuốc.
- **Public API** (OpenAPI-style):
  - `POST /auth/login`, `POST /auth/register` → token mang `userId` + `role`.
  - `POST /caregiver-links` — patient mời caregiver → link `pending`.
  - `POST /caregiver-links/{id}/accept` — caregiver chấp nhận → link `active` view-only (tính "được kích hoạt", SM-2 — AC-4.1.1).
  - `GET /permissions/check?userId=&resourceOwnerId=&action=` — API nội bộ các module gọi để kiểm quyền + `canCaregiverView`.
  - *(audit-log ghi tự động khi caregiver truy cập; không endpoint public để sửa audit.)*
- **Domain events**: **phát** `CaregiverLinkActivated {caregiverId, patientId}`; **nghe** — không.
- **Permission model** (định nghĩa quyền cho toàn hệ):
  - **Patient**: toàn quyền trên dữ liệu của chính mình (thuốc, lịch, liều, report).
  - **Caregiver**: **view-only** AdherenceReport của patient đã link; KHÔNG sửa gì; mọi lần xem → **audit-log** (NFR-4, AC-4.2.2).
  - Truy cập ngoài chủ sở hữu (không phải chủ, không phải caregiver-link hợp lệ) → **chặn**.
- **Error codes**: `AUTH_INVALID_CREDENTIALS` (401) · `PERM_DENIED` (403 — không phải chủ & không caregiver-link) · `LINK_ALREADY_EXISTS` · `LINK_NOT_ACTIVE`.
- **SLA/SLO**: `permissions/check` là đường nóng (mọi request domain gọi qua) → phải nhanh, không phá NFR-2 (≤300ms p95 tổng request) · audit-log ghi cho MỌI truy cập caregiver (không mất bản ghi — NFR-4).
- **Test contract**: mọi module gọi `permissions/check` → contract test (Identity↔Scheduling, ↔Adherence, ↔Reminders) · caregiver-view trả `canCaregiverView` đúng theo link + ghi audit (Identity↔Adherence).

---

# Kiểm chéo Backlog GĐ9 → Module (mọi feature có đúng một chủ, không mồ côi, không hai chủ)

| Epic/Feature (GĐ9) | Module chủ | Ghi chú ranh giới |
|---|---|---|
| E1 · F1.1 Tạo/sửa Schedule | **Scheduling** | — |
| E1 · F1.2 Sinh DoseEvent theo timezone | **Scheduling** | sinh liều đúng LOCAL time |
| E2 · F2.1 Dispatch reminder tới hạn (dedupe, ≤60s) | **Reminders** | đọc DoseEvent pending (data Scheduling) qua Worker |
| E2 · F2.2 Bền vững khi provider lỗi (retry) | **Reminders** | failure domain provider ngoài |
| E3 · F3.1 Xác nhận một liều (403 an toàn quyền) | **Adherence** (đổi trạng thái) + **Identity** (kiểm 403) | Adherence sở hữu chuyển trạng thái; Identity phán quyền |
| E3 · F3.2 Tính AdherenceReport đúng (không NaN) | **Adherence** | — |
| E4 · F4.1 Tạo & kích hoạt CaregiverLink | **Identity & Access** | link view-only, đo SM-2 |
| E4 · F4.2 Caregiver xem báo cáo (view-only + audit) | **Identity** (kiểm quyền + audit) + **Adherence** (trả report data) | Identity: `canCaregiverView` + audit-log; Adherence: nội dung report |
| E5 · F5.1 Mã hoá at-rest + kiểm soát truy cập | **Identity & Access** (kiểm soát truy cập) — mã hoá at-rest là hạ tầng Postgres, áp cho MỌI module (delivery/GĐ11) | không phải một module đơn lẻ "sở hữu" mã hoá; kiểm soát truy cập thuộc Identity |
| E5 · F5.2 Retention policy | **cross-cutting — CHƯA CÓ CHỦ** | ⚠️ OQ-B (khoảng retention) CHƯA chốt (Backlog F5.2 + Architecture §6). Không tự gán chủ / không bịa. Xem Open-Q dưới. |

**Không feature mồ côi** (mọi feature có ≥1 module chủ). **F3.1 và F4.2 chạm hai module có chủ ý**: Identity phán quyền, module data thực thi — ranh giới đã tách (Identity không lưu data domain; module data không tự định nghĩa quyền), không phải "hai chủ một trách nhiệm".

## Open-Q còn hở (không bịa cho đủ)

- **OQ-B (retention) — F5.2 chưa có chủ module rõ.** Khoảng retention CHƯA chốt (Backlog F5.2 ghi rõ "CHƯA chốt", Architecture §6 "chưa artifact nào đóng"). Retention là cross-cutting (chạm data của Scheduling + Adherence + audit-log của Identity). **Đề nghị:** chốt policy (quay GĐ7/quyết định) trước, rồi gán chủ vận hành (nhiều khả năng Identity giữ audit-retention + mỗi module data lo phần của mình theo policy chung ở GĐ11 delivery). Ghi thành open-Q, KHÔNG tự quyết.
- **OQ-A (managed queue vs cron)** — còn treo ở GĐ7 (Architecture §7). Không ảnh hưởng ranh giới module (Reminders sở hữu dispatch bất kể công nghệ queue), chỉ ảnh hưởng lựa chọn hạ tầng GĐ7. Ghi để nhìn thấy, không chốt ở GĐ10.

---

# CỔNG GO/NO-GO (GĐ10)

**Câu hỏi cổng:** *"Ownership & contract đã rõ để 4 team chạy delivery SONG SONG chưa?"*

**Bằng chứng trình (vai Chủ sở hữu — Kiến trúc sư + EM):**
- ✅ Mỗi module đúng **1 owner** (Scheduling/Reminders/Adherence/Identity — không module "chung").
- ✅ Không data/event bị **hai module cùng sở hữu**: DoseEvent tách rõ (Scheduling sở hữu SINH + cột định danh; Adherence sở hữu TRẠNG THÁI + `taken_at`); Reminder/AdherenceReport/User-Link mỗi cái một chủ.
- ✅ Mỗi contract có **Owner + Responsibilities + Owns + Does NOT own + Public API** (ô lõi đủ); 3 module lõi có thêm event/permission/error/SLA/test-contract; Reminders rút gọn ô Public-API có lý do (đường nền, không REST public).
- ✅ Mọi **phụ thuộc đi qua contract/event** (event `DoseEventGenerated`/`ReminderSent`/`DoseTaken`; API nội bộ `permissions/check`) — không gọi chéo tuỳ tiện (giữ kỷ luật modular monolith, ADR-001).
- ✅ **Mọi feature GĐ9 có chủ** (bảng kiểm chéo ở trên), không mồ côi, không hai-chủ-một-trách-nhiệm.
- ⚠️ **Điểm còn lỏng cần user biết trước khi GO:** F5.2 retention (OQ-B) chưa có chủ vì policy chưa chốt — không phải lỗi ranh giới module, là ẩn số upstream (GĐ7). GO được cho R1 (E1–E3, không đụng retention); F5.2 chờ chốt OQ-B.

**Quyết định GO là của user (CTO/Người duyệt) — `modules` KHÔNG tự tuyên bố GO.** Nếu GO cho R1 build song song: 4 team chạy được. Nếu muốn khoá cả R2/F5.2 trước GO: chốt OQ-B trước.

```text
═══ BÀN GIAO — mediremind · GĐ10 xong (chờ user duyệt GO) ═══
Đã chốt   : 4 module · mỗi module 1 owner + contract · ranh giới does-NOT-own rõ · data ownership sạch (DoseEvent tách sinh/trạng-thái).
Artifact  : experiments/skill-fake-test/outputs/modules/modules.md
Theo dõi  : OQ-B retention (F5.2) chưa có chủ — chờ chốt policy (GĐ7); OQ-A queue-tech treo GĐ7 (không đụng ranh giới).
→ 4 team bắt đầu code song song, cần chuẩn giao hàng + DoD: chạy /delivery (GĐ11) — mỗi slice đóng khung bằng /frame
→ Chỉ build ngay MỘT slice trong một module: chạy /frame
→ Ranh giới đụng code cũ, cần hiểu trước khi module đụng vào: chạy /atlas hoặc /explain
════════════════
```
