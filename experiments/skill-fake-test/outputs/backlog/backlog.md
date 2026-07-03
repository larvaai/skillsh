# Backlog — MediRemind (GĐ9 · Roadmap & Backlog Decomposition)

> Nguồn: Live Slice Report (GĐ8 `skeleton-live-slice.md`) · PRD (GĐ4 `prd.md`) · Domain Model (GĐ5 `domain-model.md`).
> Tham chiếu size/thứ tự (KHÔNG chọn lại): Architecture Brief (GĐ6) · Tech Decision (GĐ7).
> Vai: bẻ vision đã chứng minh chạy được thành Roadmap → Epic → Feature → Story → AC, trả lời **XÂY GÌ TRƯỚC, vì giá trị gì**.

```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Các "Live Slice Report / PRD / Domain" lấy từ file bạn trỏ trong prompt (fixture), KHÔNG đọc từ state/ đã qua cổng của skill này.
- Rủi ro: (1) chưa truy vết ngược tự động về state pipeline; (2) có thể lệch nếu file fixture khác bản thật đã gate; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo các file bạn đưa. Muốn chuẩn + traceability tự động: chạy /skeleton → /backlog trên state thật.
```

---

## GÓC NHÌN LÃNH ĐẠO (đọc trước — scan 2–3 phút)

### ROADMAP — MediRemind

**Business Objective** (nối GĐ1 / SM):
- **SM-1** — sau 30 ngày, on-time dose rate tăng **≥ 15 điểm phần trăm** so với baseline tự khai (đo bằng log xác nhận liều).
- **SM-2** — **≥ 60%** caregiver-link kích hoạt xem báo cáo trong tuần đầu.

**Product Goal** (nối GĐ2): patient nhắc-và-xác-nhận liều dễ dàng, caregiver theo dõi tuân thủ (chỉ-xem) — trên một luồng thống nhất, dữ liệu sức khoẻ được bảo vệ.

| Theme (mục tiêu nghiệp vụ) | Nối SM | R1 (MVP) | R2 | R3 |
|---|---|---|---|---|
| **T1 — Uống đúng & xác nhận liều** (tăng on-time dose rate) | SM-1 | EPIC-adherence-core · EPIC-scheduling | EPIC-reminder-timeliness | — |
| **T2 — Caregiver theo dõi tuân thủ** (kích hoạt caregiver-link) | SM-2 | EPIC-caregiver-view (link + xem báo cáo) | EPIC-caregiver-reporting (báo cáo sâu) | — |
| **T3 — Bảo vệ dữ liệu sức khoẻ** (điều kiện bắt buộc, không tự đứng một release) | NFR-4 | EPIC-security-baseline (audit-log + kiểm chủ sở hữu) | (retention — OQ-B còn treo) | — |

Lý do xếp release (1 dòng mỗi cái):
- **R1 gồm adherence-core + scheduling + caregiver-view + security-baseline** — vì slice GĐ8 ("Patient xác nhận một liều") đã chứng minh trục Scheduling→Reminders→Adherence chạy thật; MVP phải đủ để đo **cả SM-1 lẫn SM-2**, nên caregiver-link (SM-2) vào ngay R1 chứ không hoãn.
- **R2 gồm reminder-timeliness + caregiver-reporting** — timeliness 60s (NFR-1) là mài chất lượng trên luồng đã chạy, không chặn go-live MVP; báo cáo sâu là gia tăng giá trị sau khi có tín hiệu SM-2.
- **R3 để trống** — chưa đủ tín hiệu để cam kết; điền sau backlog refinement (đủ-là-đủ, không bịa cho kín ô).

**Điểm CTO/PO scan ra ngay:** MediRemind đang xây MVP để đo hai chỉ số ký kết (SM-1 tuân thủ, SM-2 caregiver); R1 mở bằng chính lát cắt đã chạy thật ở GĐ8 để gỡ rủi ro sớm, kèm một epic bảo mật bắt buộc vì dữ liệu sức khoẻ nhạy cảm.

---

## BACKLOG PHÂN RÃ (R1 — release gần nhất, sâu tới Story + AC)

> Mỗi Epic mở bằng **business value + trạng thái** (lãnh đạo dừng ở đây vẫn hiểu), rồi xuống Feature → Story → AC (dev hành động).
> AC dạng Given/When/Then, phản ánh **business rule bất biến từ Domain (GĐ5)**. Test ref chỉ là móc (GĐ12 lấp). DoD tách riêng, chỉ tham chiếu GĐ11.

---

### EPIC-adherence-core — Xác nhận liều & tính tuân thủ
- **Business value:** đây là trục sinh ra **SM-1** — mỗi lần xác nhận liều là một điểm dữ liệu on-time dose rate. Nối: SM-1 / Product Goal.
- **Trạng thái:** đang làm — lát cắt lõi đã chạy thật ở GĐ8 (`confirmDose` → `pending→taken` → `rateFor`), giờ scale ra đủ trạng thái + phòng thủ.
- **Nối GĐ8:** feature đầu tiên = chính slice đã PASS ở live slice.

#### FEAT-confirm-dose — Xác nhận một liều (feature đầu R1 = slice GĐ8)
- Thuộc EPIC-adherence-core · value: khởi điểm mọi phép đo SM-1 · size: 1 sprint (đã có slice sống, rủi ro kiến trúc thấp).

- **STORY-dose-confirm** — "Là **patient**, tôi muốn bấm *Đã uống* từ reminder, để liều được ghi nhận là đã uống và tỉ lệ tuân thủ của tôi được cập nhật."
  - `AC-dose-confirm-1`: **Given** patient đăng nhập (req.userId) và có một DoseEvent status=`pending` của chính mình / **When** gọi `POST /doses/:id/confirm` / **Then** DoseEvent chuyển `pending → taken`, set `taken_at`, trả 200 kèm adherenceRate tính lại (rule Domain: pending→taken là chuyển hợp lệ, `taken` là trạng thái kết thúc).
  - `AC-dose-confirm-2`: **Given** một DoseEvent đã ở trạng thái kết thúc (`taken`/`missed`/`skipped`) / **When** patient xác nhận lại / **Then** hệ từ chối (không đổi trạng thái lần hai) — chống xác nhận trùng (PRD §5 "chống xác nhận trùng").
  - `AC-dose-confirm-3` (rủi ro cao — biên latency): **Given** tải bình thường / **When** ghi xác nhận / **Then** ghi hoàn tất **≤ 300ms p95** (NFR-2). *(Slice đo ~15ms in-memory; AC này chốt lại mốc khi lên Postgres — "giả định đã đổi" GĐ8.)*
  - Tasks (thô, để size — đặc tả là /frame): controller `confirmDose` · dịch chuyển trạng thái trong Adherence · gọi `rateFor` · integration test.
  - Test ref: `TC-DOSE-CONFIRM-001`.

- **STORY-dose-ownership-guard** — "Là **patient**, tôi muốn chỉ mình xác nhận được liều của mình, để không ai (kể cả caregiver) ghi hộ liều của tôi." *(sinh từ khiếm khuyết THẬT ô #5 GĐ8 — "giả định đã đổi": authorization thiếu.)*
  - `AC-dose-ownership-guard-1`: **Given** một DoseEvent thuộc patient A / **When** một user B (khác chủ) gọi confirm / **Then** trả **403**, không đổi trạng thái (rule Domain: patient sở hữu dữ liệu thuốc của mình; caregiver `view-only`).
  - `AC-dose-ownership-guard-2`: **Given** caregiver đã link tới patient A / **When** caregiver gọi confirm liều của A / **Then** trả **403** — `CaregiverLink.scope = view-only`, caregiver không ghi.
  - Tasks: check `dose.userId === req.userId` trong `confirmDose` · error code 403.
  - Test ref: `TC-DOSE-OWNERSHIP-001`.
  - *Nối GĐ8:* ô #5 Live Slice FAIL ("`confirmDose` KHÔNG kiểm `dose.userId===req.userId`") → story này vá đúng chỗ đó trước khi build full.

#### FEAT-adherence-rate — Tính & hiển thị tỉ lệ tuân thủ
- Thuộc EPIC-adherence-core · value: biến các trạng thái liều thành **con số đo SM-1** · size: 1 sprint.

- **STORY-adherence-rate** — "Là **patient**, tôi muốn thấy tỉ lệ tuân thủ theo kỳ, để biết mình uống đúng đến đâu."
  - `AC-adherence-rate-1`: **Given** patient có n DoseEvent trong kỳ / **When** tính AdherenceReport / **Then** `rate` = tỉ lệ liều `taken` trên tổng liều ở trạng thái kết thúc, gắn `user_id` + `period` (rule Domain: AdherenceReport tính từ taken/missed/skipped).
  - Tasks: `AdherenceService.rateFor` mở rộng theo period · endpoint đọc report.
  - Test ref: `TC-ADHERENCE-RATE-001`.

- **STORY-dose-missed** — "Là **hệ thống**, tôi muốn đánh dấu liều quá hạn là `missed`, để tỉ lệ tuân thủ phản ánh đúng thực tế." *(rủi ro trung bình — lifecycle Domain.)*
  - `AC-dose-missed-1`: **Given** một DoseEvent `pending` đã quá hạn xác nhận / **When** job lifecycle chạy / **Then** chuyển `pending → missed` (rule Domain: quá hạn không xác nhận → missed; `missed` là trạng thái kết thúc, đưa vào mẫu số của rate).
  - Tasks: job quét quá hạn · chuyển trạng thái Adherence.
  - Test ref: `TC-DOSE-MISSED-001`.
  - *Open-Q:* "quá hạn" là bao lâu (grace window)? Domain/PRD chưa nêu con số cụ thể → **ghi open question**, chốt trước khi viết chi tiết AC biên.

---

### EPIC-scheduling — Khai thuốc, lịch & sinh liều
- **Business value:** không có Medication + Schedule + DoseEvent thì không có gì để nhắc/đo → đây là **điều kiện đầu vào cho SM-1**. Nối: SM-1 / Product Goal.
- **Trạng thái:** đang làm — generator đã chạy ở slice GĐ8 (`nightlyGenerate` sinh 2 DoseEvent); giờ mở phần khai thuốc/lịch cho patient.

#### FEAT-medication-schedule — Khai Medication & Schedule
- Thuộc EPIC-scheduling · value: patient tự dựng lịch uống · size: 1 sprint.

- **STORY-medication-create** — "Là **patient**, tôi muốn khai một loại thuốc (name, dosage, form), để lập lịch uống cho nó."
  - `AC-medication-create-1`: **Given** patient đăng nhập / **When** tạo Medication với name + dosage + form / **Then** Medication được tạo, thuộc sở hữu patient đó (rule Domain: một Medication thuộc đúng một patient).
  - Test ref: `TC-MEDICATION-CREATE-001`.

- **STORY-schedule-create** — "Là **patient**, tôi muốn đặt lịch uống (giờ trong ngày, ngày trong tuần, kỳ, timezone) cho một thuốc, để hệ sinh ra các liều cần uống."
  - `AC-schedule-create-1`: **Given** một Medication của patient / **When** tạo Schedule với `times_per_day[]`, `days_of_week[]`, `start_date`, `end_date`, `timezone` / **Then** Schedule gắn `medication_id` được lưu (rule Domain: Schedule thuộc một Medication).
  - `AC-schedule-create-2`: **Given** một Schedule đang hiệu lực / **When** đến ngày trong `days_of_week` / **Then** hệ sinh DoseEvent status=`pending` cho mỗi mốc `times_per_day` theo `timezone` của Schedule (rule Domain: Schedule generates DoseEvent; slice GĐ8 đã chứng minh `nightlyGenerate`).
  - Tasks: `DoseGeneratorService.generateForDay` · timezone handling · unit test theo daysOfWeek.
  - Test ref: `TC-SCHEDULE-CREATE-001`.
  - *Nối GĐ8:* generator đã chạy thật (log `nightlyGenerate: generated=2`) — story này là phần khai UI/API bọc quanh generator đã proven.

---

### EPIC-caregiver-view — Liên kết & theo dõi caregiver (chỉ-xem)
- **Business value:** đây là trục sinh ra **SM-2** — mỗi caregiver-link kích hoạt + mở báo cáo là một điểm dữ liệu SM-2. Nối: **SM-2** / Product Goal.
- **Trạng thái:** chưa bắt đầu — nằm ngoài slice GĐ8 (live slice chỉ chạm patient), nhưng BẮT BUỘC ở R1 vì MVP phải đo được SM-2.
- **Lý do vào R1 (ghi rõ):** SM-2 là một trong hai success metric ký kết; nếu hoãn caregiver sang R2 thì MVP không đo được SM-2 → R1 phải có link + xem báo cáo tối thiểu.

#### FEAT-caregiver-link — Liên kết caregiver ↔ patient (view-only)
- Thuộc EPIC-caregiver-view · value: kích hoạt quan hệ theo dõi (mẫu số của SM-2) · size: 1 sprint.

- **STORY-caregiver-link** — "Là **patient**, tôi muốn mời một caregiver theo dõi tuân thủ của tôi, để người thân nắm được tình hình uống thuốc."
  - `AC-caregiver-link-1`: **Given** patient và một user caregiver / **When** patient tạo CaregiverLink / **Then** CaregiverLink được tạo với `scope = view-only`, nối `caregiver_id`↔`patient_id` (rule Domain: CaregiverLink là view-only).
  - Test ref: `TC-CAREGIVER-LINK-001`.

#### FEAT-caregiver-report-view — Caregiver xem báo cáo tuân thủ
- Thuộc EPIC-caregiver-view · value: caregiver-link "kích hoạt" = có ít nhất một lần xem báo cáo (chính là hành vi SM-2 đo) · size: 1 sprint.

- **STORY-caregiver-view-report** — "Là **caregiver** đã được link, tôi muốn xem báo cáo tuân thủ của patient, để biết họ có uống đúng không." *(rủi ro cao — chạm dữ liệu sức khoẻ + quyền + audit.)*
  - `AC-caregiver-view-report-1`: **Given** caregiver có CaregiverLink `view-only` tới patient A / **When** caregiver mở AdherenceReport của A / **Then** trả report ở chế độ CHỈ-XEM, không cho thao tác ghi (rule Domain: caregiver chỉ đọc).
  - `AC-caregiver-view-report-2`: **Given** caregiver KHÔNG có link tới patient B / **When** caregiver cố xem report của B / **Then** trả **403** (chỉ patient đã link mới xem được).
  - `AC-caregiver-view-report-3`: **Given** caregiver truy cập dữ liệu patient / **When** mỗi lần đọc / **Then** ghi **audit-log** lần truy cập đó (NFR-4: audit-log MỌI truy cập của caregiver).
  - Tasks: `canCaregiverView` guard (đã có mầm ở `identity/caregiver.guard.ts` GĐ8) · endpoint report cho caregiver · audit-log hook.
  - Test ref: `TC-CAREGIVER-VIEW-001`.
  - *Nối GĐ8:* `identity/caregiver.guard.ts` (`canCaregiverView`) đã tồn tại trong codebase slice nhưng ngoài đường xác nhận liều — story này đưa nó vào luồng thật.

---

### EPIC-security-baseline — Nền bảo mật dữ liệu sức khoẻ
- **Business value:** dữ liệu thuốc là dữ liệu nhạy cảm; đây là **điều kiện bắt buộc để được go-live**, không phải tính năng bán được. Nối: **NFR-4** (ràng buộc bắt buộc, PRD §6/§7).
- **Trạng thái:** đang làm — một phần vá defect GĐ8 (kiểm chủ sở hữu), một phần audit-log caregiver.
- **Lưu ý vai:** epic này CHỈ đặt việc (WHAT); mã hoá at-rest / chi tiết bảo mật hạ tầng thuộc GĐ11 delivery — ở đây chỉ trỏ, không đặc tả.

#### FEAT-access-control — Kiểm soát truy cập theo vai
- Thuộc EPIC-security-baseline · value: đảm bảo đúng người thao tác đúng dữ liệu · size: gộp với các story quyền ở trên.

- **STORY-audit-caregiver-access** — "Là **hệ thống**, tôi muốn ghi audit-log mọi lần caregiver truy cập dữ liệu patient, để tuân thủ NFR-4."
  - `AC-audit-caregiver-access-1`: **Given** caregiver đọc bất kỳ dữ liệu patient nào / **When** truy cập xảy ra / **Then** một bản ghi audit (ai, patient nào, khi nào, tài nguyên gì) được lưu (NFR-4).
  - Tasks: audit-log middleware trên đường caregiver.
  - Test ref: `TC-AUDIT-CAREGIVER-001`.
  - *Ghi chú:* mã hoá at-rest + retention KHÔNG đặt thành story ở đây — retention là **OQ-B còn treo** (GĐ6/GĐ7), mã hoá at-rest là chuẩn hạ tầng GĐ11. Xem open question.

> **Story ownership-guard** (vá ô #5 GĐ8) đặt ở EPIC-adherence-core vì nó nằm trên đường xác nhận liều; về mặt bảo mật nó cũng thuộc theme T3 — traceability chéo ghi rõ ở đây thay vì nhân đôi story.

---

## RELEASE PLAN

### R1 (MVP) — đủ để đo SM-1 và SM-2
- **Feature list:** confirm-dose (+ ownership-guard) · adherence-rate (+ dose-missed) · medication-schedule · caregiver-link · caregiver-report-view · audit-caregiver-access.
- **Mục tiêu (nối success metric):** có đủ luồng để bắt đầu đo **SM-1** (on-time dose rate qua log xác nhận) và **SM-2** (caregiver-link kích hoạt + xem báo cáo).
- **Thứ tự ưu tiên + LÝ DO:**
  1. **confirm-dose trước** — đã có slice sống GĐ8, gỡ rủi ro kiến trúc sớm, mở ngay dòng dữ liệu SM-1.
  2. **ownership-guard ngay sau** — vá defect THẬT ô #5 GĐ8 trước khi build rộng (rủi ro bảo mật, làm sớm để không nợ kỹ thuật).
  3. **medication-schedule** — cung cấp dữ liệu đầu vào (thuốc/lịch/liều) cho confirm; generator đã proven nên đặt song song được.
  4. **adherence-rate + dose-missed** — biến trạng thái liều thành con số SM-1.
  5. **caregiver-link → caregiver-report-view → audit** — mở trục SM-2; report phụ thuộc có adherence-rate trước.
- **Release AC (điều kiện go-live — chi tiết ở GĐ12–13):** pass UAT các story R1 · security scan · có kiểm chủ sở hữu (ownership-guard) · audit-log caregiver hoạt động · có rollback. *(Mốc NFR cứng — timeliness 60s — KHÔNG đặt là điều kiện chặn R1: xem hoãn R2.)*
- **Phụ thuộc:** report-view ⟵ adherence-rate; confirm ⟵ có DoseEvent (medication-schedule / generator).
- **Rủi ro:**
  - **NFR-1 timeliness 60s chưa chứng minh** — slice dùng window `dispatchDue` = 5 phút (GĐ8 §3.4). Không chặn MVP chạy được nhưng ảnh hưởng chất lượng nhắc → chuyển thành EPIC-reminder-timeliness ở R2.
  - **Postgres thật** — slice dùng `db` in-memory; AC latency (`AC-dose-confirm-3`) phải đo lại khi lên Postgres.
  - **"quá hạn = bao lâu"** cho dose-missed chưa có con số Domain → open question.
- **DoD:** tham chiếu chuẩn chung ở GĐ11 delivery (không định nghĩa ở đây).

### R2 — mài chất lượng nhắc + báo cáo sâu (phác thô)
- **Mục tiêu:** đạt mốc timeliness NFR-1 (≤60s) và làm caregiver-reporting sâu hơn để giữ SM-2.
- **Epic chính:** EPIC-reminder-timeliness (siết window / dùng BullMQ theo Tech Decision OQ-A đã chốt) · EPIC-caregiver-reporting.
- **Hoãn khỏi R1 vì:** timeliness là tối ưu trên luồng đã chạy, không chặn go-live MVP; báo cáo sâu cần tín hiệu SM-2 từ R1 mới định hướng đúng.

### R3 — để trống (chưa cam kết)
- Chưa đủ tín hiệu; điền sau backlog refinement. **Đủ-là-đủ** — không bịa epic để kín ô.

---

## TRACEABILITY (chuỗi liền — đứt ở đâu ghi ở đó)

| Mắt xích | Nối về |
|---|---|
| EPIC-adherence-core → | **SM-1** (Business Objective GĐ1) · Product Goal |
| EPIC-scheduling → | **SM-1** (điều kiện đầu vào) |
| EPIC-caregiver-view → | **SM-2** (Business Objective GĐ1) |
| EPIC-security-baseline → | **NFR-4** (ràng buộc bắt buộc PRD §6/§7) |
| Mọi Feature → | thuộc đúng một Epic (ghi "thuộc EPIC-..." ở mỗi feature) |
| Mọi Story → | thuộc đúng một Feature |
| Mọi AC → | thuộc đúng một Story + phản ánh business rule Domain GĐ5 (đã ghi rule trong ngoặc mỗi AC) |
| Story đầu R1 (`STORY-dose-confirm`) → | = chính **Live Slice GĐ8** đã PASS |
| `STORY-dose-ownership-guard` → | vá **ô #5 GĐ8 FAIL** (giả định đã đổi) |
| Mỗi Story → | có **Test ref TC-...** làm móc cho GĐ12 |

**Chỗ đứt / còn treo (ghi rõ, không bịa nối):**
- **OQ — grace window cho `missed`:** Domain/PRD chưa nêu "quá hạn bao lâu → missed". `AC-dose-missed-1` để mốc định tính; cần con số trước khi viết AC biên → quay lại /idea hoặc /partner (GĐ5) nếu cần chốt.
- **OQ-B retention (mã hoá/giữ dữ liệu bao lâu):** còn treo từ GĐ6/GĐ7 — KHÔNG đặt thành story ở R1; chờ Delivery Standards (GĐ11) / quyết định tuân thủ.
- **NFR-1 60s:** chưa proven ở GĐ8 → đẩy thành epic R2, không giả vờ đã đạt.

---

## TỰ SOI (trước cổng)
- Lãnh đạo đọc được đoạn đầu? — có: Roadmap 1 bảng theme×release + mỗi epic mở bằng business value nối SM, ngôn ngữ nghiệp vụ.
- Dev đủ hành động? — story R1 đều có AC Given/When/Then + task thô + Test ref → giao được sang /frame.
- Đủ 3 artifact? — Roadmap ✓ · Backlog phân rã ✓ · Release Plan ✓. AC dưới story, DoD chỉ tham chiếu ✓.
- Đủ-là-đủ? — R1 sâu tới AC; R2 chỉ theme+epic; R3 trống; số AC theo rủi ro (ownership/report/latency nhiều AC hơn) ✓.
- Traceability liền? — Epic→SM, Feature→Epic, Story→Feature, AC→Story+rule Domain; chỗ treo ghi rõ ✓.
- Không lấn vai? — không chọn stack/kiến trúc (chỉ tham chiếu để size), không chia module/gán owner, không viết code/DoD chi tiết/Test Case chi tiết ✓.

---

## CỔNG GO/NO-GO

**Câu hỏi cổng (GĐ9):** *"Backlog đủ để lập kế hoạch delivery & phân module chưa?"*

Kèm:
- Release gần nhất (R1) đã có story + AC? — **Có** (mọi story R1 có AC Given/When/Then).
- Roadmap lãnh đạo đọc được? — **Có** (1 bảng theme×release nối SM-1/SM-2/NFR-4).
- Thứ tự release có lý do? — **Có** (mỗi bước ghi lý do; R1 mở bằng slice GĐ8).
- Còn open question Domain chặn không? — **Có 1 nhẹ** (grace window `missed`) + 1 vận hành treo (retention OQ-B); không chặn phân module R1 nhưng cần chốt trước khi viết AC biên `dose-missed`.

**AI duyệt (phân vai A5 — Product Owner + Tech lead):** AI đã tự soi ba xương sống — (1) đủ Roadmap + Backlog + Release Plan; (2) đọc-được 3 tầng; (3) mọi epic/feature/story/AC nối ngược nguồn GĐ trước, không bịa. Trình đánh giá + rủi ro ở trên. **AI KHÔNG tự tuyên bố pass** — đề nghị **PO (chủ sở hữu) + Tech lead** quyết go/no-go; nếu chấp nhận 2 open-Q ở trên là "không chặn R1" thì GO cho phân module + delivery R1.

---

## BÀN GIAO

```text
═══ BÀN GIAO — MediRemind · Backlog GĐ9 ═══
Đã chốt : Roadmap (3 theme × 3 release) · Backlog R1 (4 epic / 7 feature / 9 story có AC) · Release Plan R1 chi tiết + R2 phác.
Artifact: experiments/skill-fake-test/outputs/backlog/backlog.md
→ Chia module theo domain boundary + gán owner + contract (GĐ10, bước kế mặc định) : chạy /modules
→ Build ngay một story R1 đã có AC (đóng khung slice cho dev)                       : chạy /frame STORY-dose-confirm  (hoặc STORY-dose-ownership-guard để vá ô #5 GĐ8 trước)
→ Domain còn treo (grace window "missed") khiến AC biên chưa đặt được               : quay lại /idea hoặc /partner (GĐ5)
════════════════
```

Chỉ liệt kê — user (PO/Tech lead) quyết bước kế.
