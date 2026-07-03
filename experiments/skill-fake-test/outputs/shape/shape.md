# SHAPE — Solution Architecture (GĐ6) · MediRemind

```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Domain Model" lấy từ prompt/file bạn đưa, CHƯA qua cổng GĐ5 (skill /idea).
- Rủi ro: (1) chưa truy vết ngược được về pipeline; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /idea trước để có "Domain Model" đã qua cổng.
```

**Đầu vào đã nhận (chỉ 2 file, đúng yêu cầu):**
- Domain Model (GĐ5): `fixture/mediremind/docs/domain-model.md` — 7 entity, 4 bounded context (Scheduling · Reminders · Adherence · Identity & Access), state machine DoseEvent, ghi chú ranh giới giao thoa DoseEvent.
- Requirements + NFR (GĐ3): `fixture/mediremind/problem/requirements.md` — AC-1..AC-5 cho slice xác-nhận-liều + NFR-1..NFR-5 (số cứng).

> Không đọc `docs/architecture.md` (bị cấm — đây là bản skill phải tự sinh). Không chốt framework/DB (việc của `stack` GĐ7).

---

## 1. ARCHITECTURE BRIEF — bảng quyết định

**Góc nhìn lãnh đạo (đọc trước, 2–3 phút):**
MediRemind là app nhắc uống thuốc cho ~50k người dùng, ghi lại "đã uống / bỏ / lỡ" và báo tỉ lệ tuân thủ. Hệ thống được đóng thành **một khối triển khai gọn (modular monolith) chia 4 ranh giới nghiệp vụ rõ** — Lịch thuốc · Nhắc · Tuân thủ · Danh tính — để một đội nhỏ vận hành được mà vẫn tách bạch trách nhiệm. Ba rủi ro lớn nhất đã được khoá bằng hình hài: (1) **dữ liệu thuốc là dữ liệu nhạy cảm** → mã hoá at-rest + audit-log mọi truy cập của người chăm sóc; (2) **nhắc phải đúng giờ (trong 60s)** → một đường xử lý nền theo lịch tách riêng, không phụ thuộc người dùng đang mở app; (3) **ghi "đã uống" phải nhanh (≤300ms p95)** → đường ghi này giữ đồng bộ, mỏng, không gọi ra ngoài. App **không dùng cho cấp cứu** (mục tiêu sẵn sàng 99.5%, không phải hệ life-critical) — đây là điều lãnh đạo/pháp lý cần biết đầu tiên.

| Ô | Quyết định | Bám nguồn |
|---|---|---|
| **Architecture style** | **Modular monolith** — 4 module theo 4 bounded context, cộng một **worker nền theo lịch** (scheduler) tách tiến trình cho việc sinh DoseEvent + dispatch Reminder + đóng liều quá hạn. Không microservices ở MVP. | 4 BC GĐ5; NFR-3 (quy mô MVP vừa); NFR-1 (cần đường nền độc lập). |
| **Module boundary** | `Scheduling` sở hữu Medication + Schedule, **sinh** DoseEvent. `Adherence` sở hữu AdherenceReport + **chuyển trạng thái** DoseEvent (pending→taken/missed/skipped) + tính rate. `Reminders` sở hữu Reminder, **dispatch** qua channel, **đọc** DoseEvent. `Identity & Access` sở hữu User + CaregiverLink + quyền. | Bảng BC GĐ5 §4 + ghi chú ranh giới giao thoa. |
| **DoseEvent (entity giao thoa)** | DoseEvent lưu trong schema của `Scheduling` (nơi sinh). `Adherence` là **module duy nhất được ghi** trường `status`/`taken_at`; `Reminders` chỉ **đọc**. Không cross-write trực tiếp — đổi trạng thái đi qua API/command của Adherence. | Ghi chú ranh giới GĐ5: "Scheduling tạo, Adherence cập nhật trạng thái, Reminders đọc để dispatch". |
| **Data ownership** | **Một DB, schema-per-module** (scheduling / reminders / adherence / identity). **Cấm cross-module query trực tiếp** — đọc dữ liệu module khác qua API nội bộ hoặc domain event. | Style monolith + ranh giới BC GĐ5. |
| **Integration** | UI ↔ hệ: **REST** (đồng bộ) cho lệnh xác-nhận-liều. Nội bộ giữa module: **domain event** (DoseEventCreated, DoseTaken, DoseMissed) + command đồng bộ khi cần đọc ngay. Ra ngoài: **push provider** + **SMS provider** (bất đồng bộ, có retry) cho Reminder. | AC-1 (REST deep-link); state machine; NFR-1 dispatch. |
| **Auth** | **RBAC** hai vai `patient` / `caregiver`; `caregiver` scope **view-only** (không đổi trạng thái liều). Quyền theo **quyền sở hữu tài nguyên**: chỉ chủ liều (patient P) mới xác nhận được liều của P. | AC-4; entity User.role + CaregiverLink.scope GĐ5. |
| **Security** | Dữ liệu thuốc = **Confidential**; **mã hoá at-rest**; **audit-log append-only** mọi truy cập của caregiver vào dữ liệu patient. Threat model STRIDE gọn cho đường xác-nhận-liều (bên dưới §4). | NFR-4. |
| **Reliability** | Đường ghi xác-nhận-liều: đồng bộ, **idempotent** (bấm lần 2 không đổi trạng thái — AC-3). Dispatch Reminder ra provider: **retry + timeout**, hàng đợi nền; provider sập không chặn việc tạo liều. Đóng liều quá hạn: job nền quét theo cửa sổ (AC-5). | AC-3, AC-5, NFR-1. |
| **Performance** | Đường xác-nhận-liều giữ **mỏng, không gọi mạng ngoài** để đạt p95 ≤300ms; **index** trên (patient_id, status, scheduled_time) cho truy vấn liều pending + tính adherence; tính lại adherence có thể **async** sau khi ghi taken. | NFR-2, NFR-3 (250k DoseEvent/ngày). |
| **Observability** | Structured log + **RED metric** (rate/error/duration) trên đường xác-nhận-liều; trace xuyên module; **alert**: p95 ghi-liều > 300ms (NFR-2), độ trễ dispatch reminder > 60s (NFR-1), error-rate > 1%, availability < 99.5% (NFR-5). | NFR-1/2/5. |
| **Deployment** | Cloud, **1 region** (MVP), API + worker nền tách tiến trình; chiến lược cắt hình hài này chịu được **blue-green**. Số region/multi-AZ cụ thể để đạt 99.5% → **open-Q GĐ7** (phụ thuộc nhà cung cấp hạ tầng chọn ở `stack`). | NFR-5; đủ-là-đủ (không chốt tool). |
| **Compliance** | Dữ liệu sức khoẻ cá nhân nhạy cảm → cần **kiểm soát truy cập + audit + mã hoá**. Khung pháp lý cụ thể (HIPAA/GDPR/PDPA theo thị trường) **chưa nêu số trong requirements** → **open-Q**, không tự chế ngưỡng retention. | NFR-4; các mục compliance khác: không có trong nguồn → ghi open-Q. |

Ô không có trong nguồn nhưng cần đánh dấu: **retention/xoá dữ liệu** và **khung pháp lý cụ thể** — requirements.md không cho số → ghi open-Q, KHÔNG bịa.

---

## 2. C4 — Context (bắt buộc) + Container

### C4 Context (mức 1 — hệ ngồi ở đâu trong thế giới)

*Diễn giải:* Patient dùng app để xác nhận liều và xem lịch; Caregiver chỉ xem tình hình tuân thủ của patient họ theo dõi. Hệ MediRemind bắn nhắc ra ngoài qua nhà cung cấp Push và SMS. Danh tính do một Identity provider đỡ (loại IdP để GĐ7 chốt).

```
        ┌──────────┐        xác nhận liều / xem lịch        ┌───────────────────────┐
        │ Patient  │ ───────────────────────────────────►  │                       │
        └──────────┘                                        │                       │        gửi push
        ┌──────────┐        xem tuân thủ (view-only)        │      MediRemind       │ ────────────►  [ Push Provider ]
        │ Caregiver│ ───────────────────────────────────►  │  (nhắc uống thuốc &   │
        └──────────┘                                        │   theo dõi tuân thủ)  │ ────────────►  [ SMS Provider  ]
                                                            │                       │        gửi sms
                          đăng nhập / xác thực              │                       │
        [ Identity Provider ] ◄─────────────────────────►  │                       │
                                                            └───────────────────────┘
```

### C4 Container (mức 2 — bên trong hộp có khối chạy được nào)

*Diễn giải:* Bên trong là **một API app** (chứa 4 module theo domain) + **một worker nền theo lịch** + **một DB dùng chung (schema tách theo module)** + **một hàng đợi** cho dispatch reminder bất đồng bộ. Công nghệ ghi ở mức LOẠI, không tên framework — đó là GĐ7.

```
┌──────────────────────────── MediRemind (1 deployable API + 1 worker) ────────────────────────────┐
│                                                                                                   │
│   [Web/Mobile client] ──REST──►  ┌───────────── API app ─────────────┐                            │
│                                  │  Identity&Access  │  Scheduling    │                            │
│                                  │  (User,           │  (Medication,  │                            │
│                                  │   CaregiverLink,  │   Schedule,    │                            │
│                                  │   RBAC)           │   sinh Dose-   │                            │
│                                  │                   │   Event)       │                            │
│                                  │  Adherence        │  Reminders     │                            │
│                                  │  (đổi status      │  (đọc DoseEvent│                            │
│                                  │   DoseEvent,      │   dispatch qua │                            │
│                                  │   tính rate)      │   channel)     │                            │
│                                  └─────┬──────────────────────┬───────┘                            │
│                                        │ schema-per-module    │ enqueue reminder                   │
│                                   ┌────▼─────┐          ┌──────▼──────┐      ┌──────────────────┐   │
│                                   │   DB     │◄─────────│  Worker nền │◄─────│  Message Queue    │  │
│                                   │(4 schema)│  quét    │ (scheduler: │      │ (dispatch async)  │  │
│                                   └──────────┘  liều    │  sinh dose, │      └───────┬──────────┘   │
│                                                 quá hạn │  đóng missed│              │              │
│                                                         │  dispatch)  │──push/sms──► [Push] [SMS]    │
│                                                         └─────────────┘                             │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Container tồn tại: **API app** (4 module) · **Worker nền/scheduler** (sinh DoseEvent theo Schedule, đóng liều missed theo cửa sổ, dispatch reminder) · **DB dùng chung 4 schema** · **Message queue** (tách dispatch reminder ra khỏi đường ghi để giữ p95). Loại DB/queue/framework cụ thể → GĐ7.

---

## 3. Data Flow + Integration Model

### Data Flow — luồng chính "xác nhận một liều" (gắn vào domain event GĐ5)

*Góc nhìn lãnh đạo:* Người bệnh bấm "Đã uống" từ nhắc → hệ đổi trạng thái liều và cập nhật tỉ lệ tuân thủ, tất cả trong dưới 300ms.

1. **Sinh liều (nền):** Worker đọc `Schedule` (module Scheduling) → sinh `DoseEvent` trạng thái `pending` tại `scheduled_time` → phát **`DoseEventCreated`**.
2. **Nhắc:** `Reminders` nhận `DoseEventCreated` → tạo `Reminder` (channel push|sms) → enqueue → worker dispatch ra provider trong **≤60s** (NFR-1); ghi `sent_at`.
3. **Xác nhận (đồng bộ, đường nóng):** Patient mở deep-link, bấm "Đã uống" → REST tới API → `Identity&Access` kiểm **chủ liều** (AC-4) → `Adherence` chuyển `pending → taken`, set `taken_at` (AC-1); **idempotent**: nếu đã `taken/missed/skipped` thì bỏ qua (AC-3). Ghi hoàn tất **≤300ms p95** (NFR-2) — không gọi mạng ngoài trong đường này.
4. **Phát sự kiện + tính adherence:** `Adherence` phát **`DoseTaken`** → tính lại `AdherenceReport.rate` (có thể async, không chặn phản hồi).
5. **Đóng liều quá hạn (nền):** Worker quét `DoseEvent` `pending` quá cửa sổ → `Adherence` chuyển `pending → missed`, phát **`DoseMissed`** → phản ánh vào adherence (AC-5).

**Data ownership trong luồng:** Scheduling ghi DoseEvent lúc sinh; **chỉ Adherence ghi `status`/`taken_at`**; Reminders chỉ đọc DoseEvent + ghi Reminder của mình; Identity&Access sở hữu quyết định "ai được xác nhận".

### Integration Model — mỗi tích hợp một dòng

| Đường | Pattern | Đồng bộ? | Chịu lỗi khi bên kia sập | Chủ contract |
|---|---|---|---|---|
| Client → API (xác nhận liều) | REST | Đồng bộ | Trả lỗi rõ; idempotent nên retry an toàn | MediRemind (API) |
| Module ↔ Module nội bộ | Domain event + command | Event bất đồng bộ / command đồng bộ | Event có thể replay; command lỗi → không đổi trạng thái | Module phát event |
| API/Worker → Push provider | Enqueue → dispatch | Bất đồng bộ | **retry + timeout**; sập không chặn tạo liều; liều vẫn ghi được | MediRemind (adapter) |
| API/Worker → SMS provider | Enqueue → dispatch | Bất đồng bộ | như trên; fallback channel là **open-Q** (push↔sms failover chưa nêu trong nguồn) | MediRemind (adapter) |
| App ↔ Identity provider | Đăng nhập/verify token | Đồng bộ | IdP sập → chặn đăng nhập mới; token còn hạn vẫn dùng | MediRemind (adapter) |

Open-Q integration còn treo (chuyển GĐ7 hoặc chốt sau): (a) fallback giữa push và sms khi một channel lỗi; (b) loại message queue/scheduler cụ thể; (c) loại Identity provider.

---

## 4. Security Model

**Góc nhìn lãnh đạo (một câu):** Dữ liệu nhạy nhất là **lịch/loại thuốc và lịch sử uống của người bệnh** — chỉ chính chủ (patient) được xem-sửa, người chăm sóc chỉ được **xem**, và **mọi lần caregiver xem dữ liệu patient đều để lại dấu vết audit không xoá được**.

- **Phân loại dữ liệu:**
  - *Confidential:* Medication, Schedule, DoseEvent, AdherenceReport, Reminder (liên quan sức khoẻ). → **mã hoá at-rest** (NFR-4).
  - *Internal:* CaregiverLink, User.role.
  - *Public:* không có dữ liệu công khai trong domain này.
- **Auth model (RBAC + ownership):**
  | Vai | Quyền |
  |---|---|
  | `patient` (chủ liều) | đọc/ghi Medication, Schedule của mình; **xác nhận/bỏ liều của mình** |
  | `caregiver` (scope view-only) | **chỉ đọc** dữ liệu tuân thủ của patient mình liên kết; **không** đổi trạng thái liều (AC-4) |
  Ràng buộc ownership: một liều thuộc P chỉ P xác nhận được — chặn ở tầng Identity&Access trước khi Adherence ghi.
- **Audit:** log **append-only, bất biến** cho: mọi truy cập của caregiver vào dữ liệu patient (NFR-4), mọi lần đổi trạng thái DoseEvent.
- **Threat model STRIDE (gọn, cho đường xác-nhận-liều):**
  - *Spoofing:* giả danh patient khác → token gắn user + kiểm ownership (AC-4).
  - *Tampering:* sửa trạng thái liều trực tiếp → chỉ Adherence được ghi status, audit bất biến.
  - *Repudiation:* chối đã xem/đổi → audit-log append-only.
  - *Information disclosure:* lộ dữ liệu thuốc → mã hoá at-rest + RBAC + view-only caregiver.
  - *Denial of service:* spam xác nhận → idempotent + rate-limit (ngưỡng rate-limit chưa có số → open-Q).
  - *Elevation of privilege:* caregiver đổi liều → chặn cứng bằng scope view-only.
- **Compliance:** khung pháp lý cụ thể + retention **chưa có số trong requirements** → open-Q GĐ7, không tự chế.

---

## 5. ADRs

### ADR-001 — Modular monolith thay vì microservices
- **Bối cảnh:** 4 bounded context liên quan chặt (DoseEvent giao thoa 3 context), quy mô MVP 50k user / 250k DoseEvent/ngày (NFR-3), chưa có tín hiệu cần scale từng phần độc lập.
- **Quyết định:** Một khối triển khai (API app) chia 4 module theo BC + một worker nền tách tiến trình.
- **Phương án đã loại:** *Microservices per context* — loại vì tải vận hành (distributed tx quanh DoseEvent giao thoa, ranh giới dữ liệu vỡ vụn) không tương xứng quy mô MVP; *monolith một khối không tách module* — loại vì mất ranh giới BC, dễ cross-write DoseEvent.
- **Hệ quả:** Được: vận hành đơn giản, transaction trong DB dễ giữ nhất quán DoseEvent, đường ghi p95 dễ đạt. Mất: scale theo module phải tách sau nếu một module nóng lên; cần kỷ luật cấm cross-module query để ranh giới không mục.

### ADR-002 — DoseEvent: một chủ-ghi trạng thái (Adherence), các module khác chỉ đọc
- **Bối cảnh:** DoseEvent do Scheduling sinh, Reminders đọc để dispatch, Adherence đổi trạng thái — entity giao thoa 3 context (ghi chú ranh giới GĐ5). Nếu ai cũng ghi status → race + adherence sai.
- **Quyết định:** **Chỉ Adherence** được ghi `status`/`taken_at`; đổi trạng thái luôn đi qua command của Adherence; Scheduling chỉ ghi lúc sinh, Reminders read-only.
- **Phương án đã loại:** *Cho mỗi module tự cập nhật trạng thái nó quan tâm* — loại vì mất một nguồn sự thật cho adherence, khó đảm bảo idempotent (AC-3); *tách DoseEvent thành service riêng* — loại vì kéo theo microservices (đã loại ở ADR-001).
- **Hệ quả:** Được: một chỗ enforce state machine + idempotent + audit đổi trạng thái. Mất: Adherence thành điểm nóng ghi; cần index tốt cho tra liều.

### ADR-003 — Đường xác-nhận-liều đồng bộ + idempotent, dispatch reminder bất đồng bộ
- **Bối cảnh:** Ghi xác nhận phải ≤300ms p95 (NFR-2, AC-2); bấm hai lần không được tính trùng (AC-3); nhắc phải bắn ≤60s (NFR-1) nhưng phụ thuộc provider ngoài có độ trễ.
- **Quyết định:** Đường ghi "Đã uống" đồng bộ, mỏng, **idempotent theo dose_event_id**, không gọi mạng ngoài. Dispatch reminder **tách sang queue + worker** (bất đồng bộ, retry).
- **Phương án đã loại:** *Xử lý nhắc đồng bộ trong request tạo liều* — loại vì provider ngoài kéo p95 vượt ngưỡng và làm việc tạo liều phụ thuộc provider; *ghi không idempotent, chống trùng ở client* — loại vì AC-3 phải chặn ở server.
- **Hệ quả:** Được: p95 ổn định, provider sập không chặn nghiệp vụ. Mất: thêm queue để vận hành; cần theo dõi độ trễ dispatch để giữ NFR-1.

### ADR-004 — Một DB, schema-per-module, cấm cross-module query
- **Bối cảnh:** Monolith (ADR-001) nhưng cần giữ ranh giới dữ liệu theo BC để không thoái hoá thành khối rối.
- **Quyết định:** Một DB vật lý, **schema tách theo 4 module**; đọc dữ liệu module khác qua API nội bộ/event, **cấm join thẳng cross-schema**.
- **Phương án đã loại:** *DB per service* — loại vì kéo theo microservices + distributed tx quanh DoseEvent; *một schema phẳng dùng chung* — loại vì mất ranh giới ownership, dễ ghi lẫn.
- **Hệ quả:** Được: transaction nội-DB giữ nhất quán DoseEvent dễ, vẫn có ranh giới rõ. Mất: cần kỷ luật review chống query lén cross-schema; tách DB sau tốn công di trú nếu phải scale.

### ADR-005 — Worker nền theo lịch tách tiến trình cho sinh liều · đóng missed · dispatch
- **Bối cảnh:** DoseEvent sinh theo Schedule độc lập người dùng; liều quá hạn phải tự thành `missed` (AC-5); nhắc phải bắn đúng giờ (NFR-1) — không thể phụ thuộc user đang mở app.
- **Quyết định:** Một **worker nền** chạy theo lịch: sinh DoseEvent, quét đóng `missed` theo cửa sổ, dispatch reminder.
- **Phương án đã loại:** *Sinh liều/đóng missed lười (lazy) lúc user mở app* — loại vì bỏ lỡ NFR-1 và AC-5 khi user không mở app; *cron ngoài hạ tầng gọi API* — loại vì ràng buộc vận hành chưa cần, để mở cho GĐ7 chọn cơ chế scheduler.
- **Hệ quả:** Được: đúng giờ + đúng trạng thái không phụ thuộc hành vi user. Mất: thêm một tiến trình phải giám sát; cơ chế scheduler cụ thể → GĐ7.

---

## Tự soi trước khi chốt

1. **Lãnh đạo đọc được đoạn đầu?** — Có: mỗi artifact (Brief/Security/Data Flow) mở bằng Góc nhìn lãnh đạo ngôn ngữ nghiệp vụ, nêu đúng 1–3 rủi ro (nhạy cảm/đúng giờ/nhanh) + "không dùng cấp cứu".
2. **Dev đủ hành động?** — Có: style + 4 boundary bám BC + integration từng đường + auth RBAC/ownership + C4 Context & Container. Đủ để bước sang chọn stack.
3. **Đúng + đủ + bám nguồn?** — Đủ Brief + C4 (Context & Container) + Data Flow + Integration + Security + 5 ADR. Mỗi module nối về một BC GĐ5; NFR-1..5 đều có chỗ đỡ trong architecture; số thiếu (retention/pháp lý/rate-limit/fallback) ghi open-Q, không bịa.
4. **Có lỡ chọn framework?** — Không: mọi công nghệ ở mức LOẠI (DB/queue/worker/IdP/provider), không tên framework nào bị chốt; các lựa chọn tool đẩy thành open-Q GĐ7.

---

## Cổng GĐ6

```
═══ CỔNG GĐ6 — SHAPE: MediRemind ═══
Style / Boundary / Data / Integration / Auth / Security: đã chốt.
C4 Context: đã có · C4 Container: đã có · ADR: 5 bản (mỗi cái có phương án đã loại).
Open-Q còn treo → GĐ7:
  - loại DB / message queue / scheduler / Identity provider / push+sms provider
  - fallback channel push↔sms khi một channel lỗi
  - khung pháp lý cụ thể + retention + ngưỡng rate-limit (requirements chưa cho số)
  - số region / multi-AZ để đạt availability 99.5%
Câu hỏi cổng: Architecture đủ vững để chọn stack & dựng live slice chưa?
════════════════
```

**AI tự duyệt (vai CTO/Kiến trúc sư + Security song song):**
- *Kiến trúc:* 4 boundary nối đúng 4 bounded context GĐ5; DoseEvent giao thoa đã xử lý bằng luật một-chủ-ghi (ADR-002) — không còn ranh giới mơ hồ. Mọi NFR số cứng đều có chỗ đỡ (NFR-1→worker+queue, NFR-2→đường ghi mỏng idempotent, NFR-3→index+schema, NFR-4→classification+audit+encrypt, NFR-5→ghi rõ target + blue-green, cụ thể để GĐ7).
- *Security:* dữ liệu Confidential đã phân loại, RBAC + ownership chặn AC-4, audit append-only cho caregiver (NFR-4). Điểm cần GĐ7 làm rõ: ngưỡng rate-limit + khung pháp lý — đã ghi open-Q, không chế số.
- Không tự bấm GO. **User (vai CTO) quyết.**

---

## Bàn giao

```
═══ BÀN GIAO — SHAPE → STACK: MediRemind ═══
Hình đã chốt      : modular monolith · 4 module (Scheduling·Reminders·Adherence·Identity&Access) + 1 worker nền · REST cho UI + event nội bộ + push/sms async · 1 DB schema-per-module · cloud 1 region blue-green.
Ràng buộc cho stack:
  - NFR-2: ghi xác-nhận-liều ≤300ms p95 (đường nóng đồng bộ, không gọi ngoài)
  - NFR-1: dispatch reminder ≤60s (cần queue + worker + scheduler đáng tin)
  - NFR-3: 50k user / 250k DoseEvent/ngày (DB + index chịu tải ghi)
  - NFR-4: mã hoá at-rest + audit append-only (DB + storage hỗ trợ)
  - NFR-5: 99.5% (chọn hạ tầng + multi-AZ ở GĐ7)
Open-Q chuyển tiếp : loại DB/queue/scheduler/IdP/push+sms; fallback push↔sms; retention+pháp lý+rate-limit; region/multi-AZ cho 99.5%.
Artifact          : experiments/skill-fake-test/outputs/shape/shape.md
→ Chọn framework/DB/lib hiện thực hình này (GĐ7): chạy /stack
→ Muốn dựng ngay một lát cắt sống (slice xác-nhận-liều) để validate shape: chạy /skeleton (GĐ8) hoặc /frame
→ Cần hiểu code cũ shape sẽ đụng vào: chạy /atlas hoặc /explain
→ Cần điều phối cả pipeline: chạy /partner
════════════════
```
Chỉ liệt kê, KHÔNG tự chọn hộ user chạy skill nào tiếp.
