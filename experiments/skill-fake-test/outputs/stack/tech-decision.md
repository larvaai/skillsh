# MediRemind — Tech Decision Matrix + ADR (GĐ7 · `stack`)

> Nhận từ `shape` (GĐ6): `docs/architecture.md` (Architecture Brief đã qua cổng GĐ6).
> Ràng buộc đội: BIBLE §8 — **đội 3 dev, mạnh TypeScript**.
> NFR ràng buộc: §6 — NFR-1 (reminder ≤60s), NFR-2 (ghi liều ≤300ms p95), NFR-3 (50k user / ~250k DoseEvent/ngày), NFR-4 (mã hoá at-rest + kiểm soát truy cập + audit-log), NFR-5 (99.5%).
> Bàn giao sang `skeleton` (GĐ8).
> **OQ-A (managed queue vs tự cron) từ GĐ6 chuyển về đây → giải bằng ma trận + spike dưới.**

Nguồn hợp lệ: Architecture Brief này là artifact GĐ6 trong `docs/` của workspace (đã qua cổng) → KHÔNG cần block cảnh báo "đầu vào ngoài pipeline".

---

## ─── GÓC NHÌN LÃNH ĐẠO (đọc trước, 30 giây) ───

| | Chọn | Vì sao (ngôn ngữ nghiệp vụ) | Đã loại | Rủi ro / chi phí |
|---|---|---|---|---|
| **Nền backend** | **NestJS (Node/TypeScript) + PostgreSQL + Prisma** | Đội đã thạo TypeScript nên lên nhanh & rẻ; khung module/DI khớp đúng 4 module đã chốt; test tốt → giữ được luật bảo mật dữ liệu sức khoẻ. | **Spring Boot** (mạnh doanh nghiệp nhưng đội chưa quen → lên chậm); **Django** (mô hình module kém rõ, không cùng ngôn ngữ với đội). | Không khoá vendor; tuyển TypeScript dồi dào. Postgres đã bị kiến trúc ép sẵn, không phải rủi ro mới. |
| **Cách chạy nhắc liều** (OQ-A) | **Tự cron trong Reminder Worker + BullMQ trên Redis** (Redis đã có sẵn trong shape) | Không phải kéo thêm nhà cung cấp mới; dùng đúng Redis kiến trúc đã chốt; đội kiểm soát được retry để giữ cửa 60s. | **Managed queue (SQS/Cloud Tasks)** — độ tin cậy cao hơn nhưng thêm khoá cloud + chi phí, quá mức cho MVP 3 người. | ⚠️ **CÒN TREO:** cửa 60s (NFR-1) ở tải 250k liều/ngày **CHƯA đo thật**. Cần một spike ngắn ở GĐ8 để chốt; nếu spike trượt → lùi sang managed queue. |
| **Đẩy push / SMS** | **Firebase Cloud Messaging (push) + Twilio (SMS fallback)** | Hai nhà phổ biến, SDK sẵn, khớp đúng "push chính, SMS dự phòng" trong luồng dữ liệu. | Tự dựng gateway SMS — loại vì đắt & chậm, không thuộc giá trị lõi. | Phụ thuộc nhà thứ ba (đã nằm trong shape); chi phí theo lượng tin. |

**Một dòng cho CTO:** stack bám đúng thế mạnh đội (TypeScript) và đúng hình hài đã chốt (Postgres + Redis + worker tách). Một ẩn số duy nhất còn treo — reminder có kịp 60s ở tải thật không — được để hở đúng chủ ý và chuyển thành spike ở live slice (GĐ8), KHÔNG giả vờ đã chốt.

---

## 1. Các hạng mục cần chọn (rút từ Architecture Brief GĐ6)

| Hạng mục | Trạng thái trong shape | Cách xử lý ở GĐ7 |
|---|---|---|
| Ngôn ngữ + web framework | **CHƯA CHỐT** (mở) | Ma trận đầy đủ (§2.1) |
| Data store — Postgres | Đã **ép** bởi shape (`docs/architecture.md §1`) | 1 dòng lý do (§2.2) + chọn ORM bằng ma trận gọn |
| Job queue — Redis (substrate) đã ép; **cơ chế queue = OQ-A còn treo** | Nửa ép, nửa mở | Ma trận (§2.3) + **spike** (§4) vì gắn NFR-1 rủi ro cao |
| Auth / kiểm soát truy cập + audit-log (NFR-4) | Ràng buộc bởi shape (§6 Security Model) | Ma trận gọn (§2.4), neo vào NFR-4 |
| Push/SMS provider (ngoài) | Kiểu tích hợp đã ép (outbound API); nhà cụ thể mở | 1 dòng lý do (§2.5) |
| Deploy / hạ tầng | Shape ghi "cloud", không ép nhà | Ma trận gọn (§2.6) |

Nguyên tắc **đủ-là-đủ**: hạng mục shape đã ép (Postgres, kiểu tích hợp) → ghi 1 dòng, KHÔNG mở ma trận giả. Hạng mục mở + rủi ro cao (framework, queue) → ma trận đầy đủ, và queue thêm spike.

**Trọng số** (0–5, lặp cho mọi ma trận, do ràng buộc §8 + NFR quyết — KHÔNG đều nhau):
- Fit team (§8: đội 3 dev, mạnh TS) = **5** — đội nhỏ, ràng buộc mạnh nhất.
- Fit domain (4 module rõ, GĐ5/6) = **4**.
- Fit NFR (NFR-1/2/3 số cứng) = **5** cho hạng mục gắn NFR (queue), **3** cho hạng mục ít gắn.
- Fit enterprise/bảo mật (NFR-4: audit-log, kiểm quyền, mã hoá) = **4** — dữ liệu sức khoẻ nhạy cảm.
- Fit testing = **4** — luật bảo mật buộc test chặt.
- Fit maintainability (2 năm nữa) = **3**.
- Fit hiring/ecosystem = **2** — MVP, ít quan trọng hơn.

---

## 2. Tech Decision Matrix

### 2.1 Web framework + ngôn ngữ (mở, rủi ro cao → ma trận đầy đủ)

Điểm mỗi ô: 1–5. TỔNG = Σ(trọng số × điểm). Trọng số ghi trong ngoặc.

| Tiêu chí (trọng số) | NestJS (TS) | Spring Boot (Java) | Django (Python) |
|---|:---:|:---:|:---:|
| Fit team — §8 đội mạnh TS (5) | 5 | 2 | 3 |
| Fit domain — 4 module/DI rõ (4) | 5 | 5 | 3 |
| Fit NFR — ghi ≤300ms p95, async worker (3) | 4 | 5 | 4 |
| Fit bảo mật — guard/RBAC, hook audit-log (4) | 4 | 5 | 4 |
| Fit testing — unit/e2e/contract (4) | 5 | 4 | 4 |
| Fit maintainability 2 năm (3) | 4 | 4 | 3 |
| Fit hiring/ecosystem (2) | 4 | 4 | 4 |
| **TỔNG (có trọng số)** | **113** | **101** | **88** |

Chi tiết tổng: NestJS = 25+20+12+16+20+12+8 = **113**. Spring = 10+20+15+20+16+12+8 = **101**. Django = 15+12+12+16+16+9+8 = **88**.

**=> Chọn: NestJS (Node/TypeScript).**
- **Lý do:** thắng nhờ Fit team (đội đã thạo TS — trọng số nặng nhất §8) + Fit domain (module/DI khớp 4 bounded context) + Fit testing. Đủ NFR-2 (I/O async không chặn).
- **Đã loại — Spring Boot:** *điểm mạnh ghi nhận:* mạnh nhất về bảo mật doanh nghiệp + NFR (điểm 5 ở hai tiêu chí đó). *Thua ở:* Fit team — đội chưa thạo Java, learning curve làm chậm giao MVP 3 người. **Hợp nếu** đội có sẵn năng lực Java hoặc yêu cầu enterprise-Java bắt buộc.
- **Đã loại — Django:** *điểm mạnh:* nhanh cho CRUD, ecosystem chín. *Thua ở:* khác ngôn ngữ với đội (§8), mô hình module kém rõ cho 4 bounded context → dễ mờ ranh giới mà ADR-001 (GĐ6) đã buộc giữ. **Hợp nếu** đội là đội Python và domain đơn giản hơn.

### 2.2 Data store — PostgreSQL (đã bị shape ép → 1 dòng, không ma trận giả)

**Postgres đã được chốt ở GĐ6** (`architecture.md §1` data store, §5 integration, mã hoá at-rest NFR-4). GĐ7 KHÔNG chọn lại DB — chỉ ghi nhận: **PostgreSQL**, vì (a) shape đã ép, (b) dữ liệu domain quan hệ (Schedule → DoseEvent → AdherenceReport có khoá ngoại rõ), (c) hỗ trợ mã hoá at-rest cho NFR-4. Chọn **ORM** thì mở nhẹ:

| Tiêu chí (trọng số) | Prisma | TypeORM |
|---|:---:|:---:|
| Fit team — TS-native, type-safe (5) | 5 | 4 |
| Fit domain — migration + quan hệ rõ (4) | 5 | 4 |
| Fit maintainability (3) | 4 | 3 |
| **TỔNG** | **57** | **45** |
Tổng: Prisma = 25+20+12 = **57**; TypeORM = 20+16+9 = **45**.

**=> Chọn: Prisma.** Lý do: type-safe TS-native (khớp §8), migration khai báo rõ. **Đã loại TypeORM:** *điểm mạnh:* linh hoạt hơn với query thô/decorator-entity. *Thua ở:* type-safety yếu hơn, migration dễ lệch. **Hợp nếu** cần active-record + query SQL phức tạp mà Prisma chưa đỡ.

### 2.3 Cơ chế job queue — OQ-A (nửa ép, rủi ro cao vì gắn NFR-1 → ma trận + spike)

Redis đã bị shape ép làm substrate (`architecture.md §1, §5`). OQ-A hỏi: quét-tới-hạn & gửi nhắc bằng **tự cron + thư viện queue trên Redis** hay **managed queue của cloud**? NFR-1 (≤60s) làm Fit NFR nặng **5**, Fit vận hành nặng **4**.

| Tiêu chí (trọng số) | Tự cron + BullMQ (trên Redis) | Managed queue (SQS / Cloud Tasks) | node-cron thuần, không queue lib |
|---|:---:|:---:|:---:|
| Fit team — §8 đội TS (5) | 5 | 3 | 4 |
| Fit NFR-1 — cửa 60s + retry (5) | 4 | 5 | 2 |
| Fit vận hành — dead-letter, quan sát (4) | 4 | 5 | 2 |
| Fit hạ tầng — dùng Redis đã có, không thêm nhà (4) | 5 | 2 | 5 |
| Fit maintainability (3) | 4 | 4 | 2 |
| **TỔNG (có trọng số)** | **93** | **80** | **64** |
Tổng: BullMQ = 25+20+16+20+12 = **93**; Managed = 15+25+20+8+12 = **80**; node-cron thuần = 20+10+8+20+6 = **64**.

**=> Chọn (tạm, chờ spike): Tự cron + BullMQ trên Redis.**
- **Lý do:** thắng nhờ Fit hạ tầng (dùng đúng Redis shape đã ép, không kéo thêm nhà) + Fit team (TS-native). BullMQ có retry/rate-limit/dead-letter — đủ công cụ giữ cửa 60s.
- **Đã loại — Managed queue:** *điểm mạnh ghi nhận:* điểm CAO NHẤT ở NFR-1 + vận hành (retry & độ tin cậy do cloud lo). *Thua ở:* thêm khoá vendor + chi phí + rời khỏi Redis mà shape đã chốt — quá mức cho MVP 3 người. **Điều kiện đảo chiều:** nếu spike NFR-1 (§4) trượt cửa 60s ở tải 250k/ngày → chuyển sang managed queue chính là đường lùi.
- **Đã loại — node-cron thuần không queue:** *điểm mạnh:* đơn giản nhất. *Thua ở:* không có retry/dead-letter → khó đạt 60s ổn định (đúng lý do GĐ6 ADR-002 đã loại busy-poll). **Không hợp** cho NFR-1 ở tải này.
- ⚠️ **Đây là lựa-chọn-tạm gắn spike:** điểm Fit NFR-1 của BullMQ (=4) là **ước lượng, CHƯA đo thật**. Chốt cứng phụ thuộc kết quả spike §4.

### 2.4 Auth / kiểm soát truy cập + audit-log (ràng buộc bởi NFR-4 → ma trận gọn)

Shape §6 đã định mô hình bảo mật (RBAC theo `User.role`, caregiver view-only, audit-log mọi truy cập caregiver). GĐ7 chỉ chọn **cách hiện thực**, neo NFR-4:

| Tiêu chí (trọng số) | NestJS Guards + Passport (JWT/session) tự quản | Auth provider ngoài (Auth0/Clerk) |
|---|:---:|:---:|
| Fit bảo mật — RBAC + audit-log tại chỗ (4) | 5 | 4 |
| Fit team — cùng ngăn TS (5) | 5 | 4 |
| Fit NFR-4 — audit-log mọi truy cập caregiver ở tầng guard (4) | 5 | 3 |
| Fit chi phí/khoá vendor (2) | 5 | 3 |
| **TỔNG (có trọng số)** | **75** | **54** |
Tổng: tự quản = 20+25+20+10 = **75**; provider = 16+20+12+6 = **54**.

**=> Chọn: NestJS Guards + Passport, RBAC tại `Identity & Access` module.** Lý do: audit-log NFR-4 phải chặn **mọi** truy cập caregiver — đặt ở tầng guard trong-mã cho kiểm soát chặt & không rò dữ liệu sức khoẻ ra bên thứ ba. **Đã loại provider ngoài:** *điểm mạnh:* nhanh cho login/SSO xã hội, đỡ tự quản mật khẩu. *Thua ở:* dữ liệu truy cập nhạy cảm đi qua bên thứ ba làm khó bề audit-log tại-chỗ theo NFR-4 + thêm khoá vendor. **Hợp nếu** sau này cần SSO doanh nghiệp / social-login diện rộng.

### 2.5 Push/SMS provider (ngoài, kiểu tích hợp đã ép → 1 dòng)

Shape §5 đã ép **kiểu**: outbound API, "push chính, SMS fallback". GĐ7 chỉ chọn nhà: **Firebase Cloud Messaging (push) + Twilio (SMS fallback)** — hai nhà phổ biến, SDK Node sẵn, khớp đúng luồng "push|sms" ở data-flow §4. Không mở ma trận giả (đây không phải giá trị lõi & dễ đổi sau). **Đã loại:** tự dựng SMS gateway (đắt, chậm, ngoài giá trị lõi).

### 2.6 Deploy / hạ tầng (shape ghi "cloud", không ép nhà → ma trận gọn)

| Tiêu chí (trọng số) | Managed container (AWS ECS/Fargate) | PaaS (Render/Railway) | Kubernetes tự quản |
|---|:---:|:---:|:---:|
| Fit team — 3 dev, ít gánh ops (5) | 3 | 5 | 1 |
| Fit NFR-5 — 99.5% (4) | 4 | 4 | 4 |
| Fit maintainability (3) | 4 | 4 | 3 |
| Fit chi phí MVP (2) | 3 | 4 | 2 |
| **TỔNG (có trọng số)** | **49** | **61** | **34** |
Tổng: ECS = 15+16+12+6 = **49**; PaaS = 25+16+12+8 = **61**; K8s = 5+16+9+4 = **34**.

**=> Chọn: PaaS (Render/Railway) cho MVP.** Lý do: đội 3 dev — 99.5% không life-critical (NFR-5) nên đổi độ-phức-tạp-ops lấy tốc độ giao hàng. **Đã loại — ECS/Fargate:** *điểm mạnh:* kiểm soát hạ tầng & scale tốt hơn khi lớn. *Thua ở:* gánh ops nặng cho 3 người ở giai đoạn MVP. **Hợp nếu** vượt MVP, cần tuning scale/network sâu. **Đã loại — K8s tự quản:** gánh vận hành quá lớn cho đội 3 người ở MVP; để dành khi thật sự cần.

---

## 3. ADR — cho mỗi lựa chọn lớn

### ADR-003 — Chọn NestJS + PostgreSQL + Prisma cho nền backend
- **Bối cảnh:** modular monolith 4 module (GĐ6 ADR-001); đội 3 dev mạnh TypeScript (§8); NFR-2 ghi ≤300ms p95; NFR-4 bảo mật dữ liệu sức khoẻ.
- **Quyết định:** NestJS (Node/TS) + PostgreSQL + Prisma.
- **Lý do:** thắng ma trận §2.1 nhờ Fit team (TS) + Fit domain (module/DI khớp 4 context) + Fit testing; Postgres do shape ép; Prisma type-safe khớp §8.
- **Đã loại:** Spring Boot (mạnh enterprise/bảo mật nhưng đội chưa thạo Java → chậm); Django (khác ngôn ngữ, module kém rõ). Cả hai đều ghi nhận điểm mạnh (§2.1).
- **Hệ quả:** chuẩn hoá DI + test theo 4 module; cần guard RBAC ở `Identity & Access`; hiring TS dễ, không khoá vendor. Migration đi qua Prisma → giữ kỷ luật schema.

### ADR-004 — Chọn tự cron + BullMQ trên Redis cho Reminder Worker (đóng OQ-A, có điều kiện)
- **Bối cảnh:** OQ-A còn treo từ GĐ6 (ADR-002 chốt "tách worker + dùng queue", chưa chốt công nghệ). NFR-1 buộc reminder ≤60s ở tải 250k DoseEvent/ngày (NFR-3). Redis đã bị shape ép làm substrate.
- **Quyết định:** tự cron trong Reminder Worker + **BullMQ** làm lớp queue trên Redis đã có.
- **Lý do:** thắng ma trận §2.3 nhờ Fit hạ tầng (dùng đúng Redis, không thêm nhà) + Fit team (TS) + có retry/dead-letter đủ cho cửa 60s.
- **Đã loại:** managed queue (điểm NFR-1/vận hành cao nhất nhưng thêm khoá vendor + chi phí, rời Redis đã chốt — đây cũng là **đường lùi** nếu spike trượt); node-cron thuần (thiếu retry, khó đạt 60s ổn định — cùng lý do GĐ6 loại busy-poll).
- **Hệ quả + ẩn số:** **quyết định này CÓ ĐIỀU KIỆN** — phụ thuộc spike §4 xác nhận cửa 60s ở tải thật. Nếu spike trượt → kích hoạt đường lùi managed queue. Đây là ẩn số bê sang GĐ8 chứng minh.

### ADR-005 — Chọn RBAC tại-chỗ (NestJS Guards + Passport) cho auth + audit-log
- **Bối cảnh:** NFR-4 + Security Model GĐ6 §6 — caregiver view-only, audit-log **mọi** truy cập caregiver, mã hoá at-rest; `Identity & Access` là điểm chốt kiểm quyền.
- **Quyết định:** RBAC + audit-log tại tầng guard trong `Identity & Access` module, dùng Passport (JWT/session).
- **Lý do:** giữ dữ liệu truy cập nhạy cảm trong hệ, audit-log tại-chỗ NFR-4 chặt hơn, không rò qua bên thứ ba; cùng ngăn TS với đội (§2.4).
- **Đã loại:** auth provider ngoài (Auth0/Clerk) — nhanh cho SSO/social nhưng khó audit-log tại-chỗ theo NFR-4 + khoá vendor. Ghi nhận điểm mạnh; hợp nếu sau cần SSO doanh nghiệp.
- **Hệ quả:** tự quản vòng đời token + hashing mật khẩu; guard là nơi bắt-buộc đi qua cho mọi truy cập caregiver để NFR-4 không bị lách.

*(Push/SMS provider và deploy = quyết định nhỏ/dễ đổi — ghi trong §2.5–2.6, không nâng thành ADR riêng theo luật đủ-là-đủ.)*

---

## 4. Spike — chỉ cho ẩn số rủi ro cao (OQ-A / NFR-1)

Chỉ có **một** ẩn số rủi ro cao: BullMQ tự cron có giữ được reminder ≤60s ở tải thật không (NFR-1 × NFR-3). Các hạng mục còn lại stack quen + biên NFR dư → KHÔNG spike.

```
SPIKE — Reminder timeliness (OQ-A / NFR-1)
Câu hỏi   : Với ~250k DoseEvent/ngày (NFR-3), Reminder Worker (cron + BullMQ/Redis)
            có phát reminder trong ≤60s so với scheduled_time (NFR-1) không?
Time-box  : 1–2 ngày (code ném-đi).
Cách đo   : seed ~250k DoseEvent pending rải theo giờ; cron quét mỗi 10–15s → enqueue →
            dispatcher đo delay(enqueue→gửi); lấy p95 & max của delay trong 1 giờ cao điểm.
Đo được   : ⏳ CHƯA ĐO — spike CHƯA chạy trong bản này (đây là bài test skill trên dữ liệu giả;
            không có môi trường để seed & đo thật).
Kết luận  : TREO. Bảng §2.3 chọn BullMQ ở mức "tạm, chờ spike". Chốt cứng khi có số p95 thật:
            p95 ≤ 60s → giữ BullMQ; trượt → kích hoạt đường lùi managed queue (ADR-004).
```

> **Trung thực:** ô Fit-NFR-1 của BullMQ (=4) là **ước lượng chưa đo**. Theo luật cứng "còn ẩn số → spike thực đo, không đoán", số này phải được thay bằng p95 đo thật ở GĐ8 trước khi coi OQ-A đã đóng cứng. `stack` nêu spike + time-box; dev chạy ở live slice rồi báo số.

> **OQ-B (retention) còn treo** từ GĐ6 §6 — giữ dữ liệu thuốc/audit-log bao lâu. Đây là câu hỏi **chính sách dữ liệu**, KHÔNG phải lựa-chọn-công-cụ → `stack` KHÔNG tự đóng (không lấn vai). Ghi lại làm open-question kéo sang, cần một quyết định chính sách/`shape` bổ sung.

---

## Tự soi trước khi chốt

- **Lãnh đạo đọc được băng đầu?** Có — bảng Góc nhìn lãnh đạo: chọn gì / vì sao (nghiệp vụ) / loại gì / rủi ro, không bắt đọc điểm.
- **Dev đủ hành động?** Có — 6 ma trận có điểm + 3 ADR (stack cụ thể + hệ quả) + spike có time-box & cách đo. Đủ để bắt tay dựng skeleton (GĐ8).
- **Bám nguồn, không bịa?** Mọi trọng số & candidate truy về Architecture Brief GĐ6 / §8 team / §6 NFR. Ẩn số NFR-1 gắn nhãn CHƯA-ĐO thay vì bịa số. OQ-B để hở đúng chủ ý.

---

## Cổng go/no-go + Bàn giao

**Cổng (bám doc GĐ7):** *"Stack đã chốt, sẵn sàng dựng live slice chưa?"*

**Rà theo A5 (người duyệt = CTO; `stack` = người duyệt kỹ thuật rà, KHÔNG tự tuyên GO):**
1. Mỗi hạng mục rủi ro cao có ma trận **có điểm** — ✅ (framework, queue, auth, deploy).
2. Mỗi lựa chọn lớn có ADR kèm phương án đã loại — ✅ (ADR-003/004/005).
3. Ẩn số rủi ro cao đã có spike thực đo — ⚠️ **CHƯA**: spike NFR-1 mới có time-box + cách đo, **chưa có số p95 thật**. Theo luật, OQ-A chỉ đóng CỨNG khi có số. → **Cổng CHƯA đủ điều kiện qua bằng bàn giấy; cần spike ở GĐ8 (hoặc trước) trả về p95.**
4. Mọi lựa chọn nằm trong ràng buộc Architecture Brief — ✅ (Postgres/Redis/worker/tích hợp đúng shape).

**Phán quyết của `stack`:** matrix + ADR đã đủ để **bắt đầu** live slice; nhưng OQ-A/NFR-1 còn treo vì thiếu số đo. `stack` KHÔNG tự tuyên "chốt" — trình lên **CTO** câu cổng, kèm cảnh báo ẩn số §4. CTO quyết: (a) GO có điều kiện — dựng skeleton GĐ8 và ĐO NFR-1 ngay trong slice đó; hoặc (b) chạy spike riêng trước rồi mới GO.

```
═══ BÀN GIAO — MediRemind · Tech Stack (GĐ7) ═══
Stack đã chốt     : Backend = NestJS (Node/TS) · DB = PostgreSQL + Prisma · Queue = tự cron + BullMQ/Redis (tạm, chờ spike NFR-1) ·
                    Auth = NestJS Guards + Passport RBAC tại Identity&Access · Push/SMS = FCM + Twilio · Deploy = PaaS (MVP)
Ràng buộc kéo theo : hiring TS dễ · không khoá vendor ở backend · guard RBAC bắt buộc cho mọi truy cập caregiver (NFR-4) ·
                    Push/SMS + PaaS phụ thuộc nhà thứ ba (theo shape)
Ẩn số còn treo    : OQ-A/NFR-1 — reminder ≤60s ở 250k/ngày CHƯA đo (spike §4, đo ở/trước GĐ8; trượt → lùi managed queue) ·
                    OQ-B retention — câu hỏi chính sách, không thuộc stack, cần shape/policy đóng
Artifact          : experiments/skill-fake-test/outputs/stack/tech-decision.md
→ Dựng live slice / walking skeleton end-to-end (GĐ8) + đo NFR-1 để đóng OQ-A: chạy /skeleton
→ Cần điều phối trọn pipeline tới release: chạy /partner
→ Muốn code ngay một slice nhỏ thử stack: chạy /frame
→ Nếu OQ-B/retention lộ ra thiếu quyết định kiến trúc-dữ liệu: quay lại /shape
════════════════
```
