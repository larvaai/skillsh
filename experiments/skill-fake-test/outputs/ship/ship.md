# SHIP — MediRemind v1.0.0 (GĐ13 · Release Readiness & Rollout)

```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Test & Verification Report" lấy từ prompt/file bạn đưa (tóm tắt UAT của cấp trực tiếp), CHƯA qua cổng GĐ12 (skill /uat) — fixture cố ý thiếu codebase/uat-report.md.
- Rủi ro: (1) chưa truy vết ngược được về pipeline; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /uat trước để có "Test & Verification Report" đã qua cổng, có đủ 2 chữ ký.
```

> Nhận từ GĐ12 (tóm tắt UAT ngoài state, cấp trực tiếp đưa):
> UAT pass **18/20 AC** · 2 AC **BLOCKED** (permission trên confirm-dose · double-send reminder) ·
> **QA ký** · **Security TREO** (lỗ IDOR) — Security **CHƯA ký**.
> Đối chiếu Live Slice (GĐ8, `docs/skeleton-live-slice.md`): ô #5 xác nhận IDOR là **khiếm khuyết code thật** —
> `confirmDose` KHÔNG kiểm `dose.userId === req.userId`. NFR-1 (60s) và NFR-2 trên Postgres **chưa** chứng minh.
> Open-question CHƯA đóng (progress.json + definition-of-done): **OQ-A** (managed queue vs cron), **OQ-B** (retention NFR-4) —
> definition-of-done nêu rõ **phải đóng bằng ADR TRƯỚC cổng GĐ13**.

---

## 0) GÓC NHÌN LÃNH ĐẠO — đọc trước mọi thứ (không jargon)

**Sẵn sàng lên chưa:** CHƯA. Đây là lần **đầu lên production** một hệ chạm **dữ liệu sức khoẻ nhạy cảm** (NFR-4) với người dùng thật, nên xét ở mức rủi ro cao — full checklist, rollback phải test, lên từng bậc.

**CEO/CTO đang được đề nghị ký cái gì:** một cổng GO/NO-GO cho v1.0.0. Khuyến nghị của `ship` là **NO-GO tạm thời** — không phải bỏ release, mà là **hoãn cho tới khi vá 5 chốt** dưới đây. Lý do gọn để lãnh đạo quyết mà không cần đọc runbook:
1. **Bảo mật chưa ký:** có lỗ **IDOR** trên "xác nhận liều" — một người có thể xác nhận liều của người khác. Security đã **TREO** sign-off. Đây là dữ liệu y tế → không cho lên khi còn treo.
2. **2 tính năng đang khoá:** permission confirm-dose (chính là IDOR) và reminder **gửi trùng** (bệnh nhân nhận nhắc 2 lần) — 2/20 tiêu chí nghiệm thu BLOCKED.
3. **Đường lùi chưa thử thật:** rollback plan có nhưng **chưa test trên staging** — hệ quan trọng thì đây là điều kiện bắt buộc.
4. **Chưa có người trực sự cố (tên thật)** và **chưa xác nhận dashboard/alert đã bật** — nếu 2h sáng có sự cố thì chưa rõ ai cầm và cảnh báo có kêu không.
5. **Hai câu hỏi lớn còn treo:** dùng hàng đợi hay cron (OQ-A) và giữ dữ liệu bao lâu (OQ-B, liên quan bảo mật NFR-4) — luật dự án bắt phải chốt bằng ADR trước cổng này.

**Nếu (sau khi vá) lên mà hỏng:** tắt cờ `confirm_dose_v2` + `reminder_dispatch_v2` → bệnh nhân quay lại luồng cũ trong vài phút; dữ liệu liều đã ghi giữ nguyên, không mất. Người trực: **CHƯA phân công tên** (chốt #4).

> Tóm tắt một dòng cho cổng: **khuyến nghị NO-GO — vá 5 chốt, mỗi chốt có người + mốc bên dưới → rồi mở cổng lại.**

---

## 1) GO/NO-GO CHECKLIST — trái tim của trang (12 ô · owner · trạng thái)

Ký hiệu: `[x]` xong · `[ ]` chưa (dòng đỏ = chưa được ký) · `N/A + lý do`.

| # | Hạng mục | Owner | Trạng thái |
|---|----------|-------|-----------|
| 1 | **Release note** v1.0.0 | PO | `[ ]` chưa soạn — chờ chốt scope 2 AC BLOCKED có nằm trong v1.0.0 hay tách v1.0.1 |
| 2 | **Deployment plan** (blue-green, xem Runbook) | Release manager / Team Adherence | `[ ]` bản nháp có; chưa duyệt vì rollback chưa test |
| 3 | **Rollback plan** (đã test nếu hệ quan trọng) | Team Adherence + Team Reminders | `[ ]` **CHẶN** — có kế hoạch nhưng **CHƯA test staging**. Hệ quan trọng ⇒ bắt buộc test |
| 4 | **Data migration plan** (DoseEvent → Postgres, first prod) | Team Scheduling | `[ ]` chưa có script forward+backward đã chạy staging; slice hiện dùng `db` in-memory (live slice §3.1) |
| 5 | **Feature flag plan** | Release manager | `[ ]` **giả định** cần 2 cờ `confirm_dose_v2`, `reminder_dispatch_v2` — fixture chưa định nghĩa cờ nào; phải tạo trước khi rollout theo bậc |
| 6 | **User communication** (40+ patient/caregiver) | PO | `[ ]` chưa gửi — phụ thuộc release note |
| 7 | **Training material** | PO | `N/A + lý do`: app patient-facing tự phục vụ, luồng "Đã uống" 1 chạm; không có nhân viên nội bộ cần training. (Ghi lại phòng khi có clinic-admin ở release sau) |
| 8 | **Support playbook** | PO / Support | `[ ]` chưa có kịch bản xử lý "bệnh nhân báo nhận nhắc 2 lần" và "xác nhận liều nhầm" |
| 9 | **Monitoring dashboard + alert rule** | Team Reminders / SRE | `[ ]` **CHẶN** — metric ĐÃ ĐỊNH NGHĨA (delivery §8: reminder-latency NFR-1, confirm-write p95 NFR-2, availability NFR-5) nhưng **chưa có bằng chứng dashboard + alert đã BẬT** trên production |
| 10 | **Incident owner đã phân công (tên)** | CTO | `[ ]` **CHẶN** — chưa có tên người trực + số điện thoại/kênh on-call. delivery §9 mới là khung Sev, chưa gán người |
| 11 | **UAT sign-off** | QA | `[x]` **QA đã ký** (18/20 AC pass) — *nguồn: tóm tắt ngoài state, chưa qua cổng /uat; 2 AC còn BLOCKED* |
| 12 | **Security sign-off** | CISO / Security | `[ ]` **CHẶN** — **TREO** vì lỗ IDOR trên confirm-dose. Security **CHƯA ký** |

**Phụ — điều kiện cổng riêng MediRemind (definition-of-done "Cổng GĐ13"):**

| # | Hạng mục | Owner | Trạng thái |
|---|----------|-------|-----------|
| P1 | **OQ-A** đóng bằng ADR (managed queue vs cron) | shape/stack | `[ ]` **CHẶN** — còn `open` (progress.json), liên quan `src/legacy/old_reminder_cron.ts` và NFR-1 60s |
| P2 | **OQ-B** đóng bằng ADR (retention NFR-4) | idea/PO | `[ ]` **CHẶN** — còn `open`; dữ liệu y tế nhạy cảm chưa có luật giữ/xoá |

**Đọc 10 giây (cho CTO):** 9 dòng ĐỎ / 1 xanh (UAT) / 1 N/A. Trong đó **6 dòng CHẶN cứng**: rollback chưa test (3), monitoring/alert chưa bật (9), incident owner chưa tên (10), Security chưa ký (12), OQ-A (P1), OQ-B (P2).

---

## 2) ROLLBACK PLAN — đường lùi (viết TRƯỚC khi lên)

**Góc nhìn lãnh đạo:** *"Nếu hỏng, tắt 2 cờ → bệnh nhân quay lại luồng nhắc/xác nhận cũ trong < 5 phút; liều đã ghi giữ nguyên, không mất dữ liệu. Người trực: <chốt #10>."*

- **Tín hiệu nào thì lùi (ngưỡng số):**
  - `confirm-write p95 > 300ms` (NFR-2) kéo dài **> 10 phút**, HOẶC
  - `reminder-latency > 60s` (NFR-1) trên > 5% liều trong **> 15 phút**, HOẶC
  - error rate API `/doses/:id/confirm` > 2% trong **> 10 phút**, HOẶC
  - phát hiện **bất kỳ** truy cập chéo chủ sở hữu (IDOR) trên log audit → lùi **ngay lập tức**, không chờ ngưỡng.
- **Lùi bằng cách nào:**
  - **Bước 1 (tức thì):** tắt cờ `confirm_dose_v2` và `reminder_dispatch_v2` → route về hành vi cũ. *(Giả định cờ — chốt #5.)*
  - **Bước 2 (nếu cờ không đủ):** redeploy bản trước qua blue-green (switch trỏ về môi trường **blue**). Chọn **tắt-cờ trước, switch-blue sau** vì tắt cờ rẻ và tức thì; loại phương án "rollback DB ngay" vì rủi ro hơn và thường không cần (xem xử lý dữ liệu).
- **Dữ liệu sinh ra trong lúc lỗi xử lý sao:**
  - Bản ghi `DoseEvent` chuyển `pending→taken` trong lúc lỗi: **GIỮ**, không migrate ngược — trạng thái liều là dữ liệu bệnh nhân thật, xoá gây sai adherence. Backward script chỉ dùng khi migration schema (chốt #4) tạo cột không tương thích bản cũ.
  - **Điểm không lùi được (point of no return):** khi migration Postgres đã đổi kiểu cột không backward — phải có backward script test trước, hoặc dừng ở forward-compatible.
- **Đã test chưa:** **CHƯA** — đây là **dòng CHẶN GO** (hệ quan trọng, first prod). Điều kiện: chạy full rollback drill trên **staging**, ghi *"đã test rollback staging ngày __, PASS"* rồi mới đủ điều kiện qua ô #3.

*Lý do rollback chọn tắt-cờ làm chính:* release lần đầu, đội nhỏ (3 dev, delivery §BIBLE 8) → cần đường lùi rẻ nhất, nhanh nhất; canary/rollback-DB phức tạp hơn mức đội chịu được ở lần đầu.

---

## 3) RUNBOOK — cẩm nang cho dev trực (người KHÁC làm theo được lúc nửa đêm)

**Kiểu triển khai: blue-green.** *Lý do chọn:* zero-downtime cho luồng nhắc chạy 24/7 (cron mỗi phút, live slice §3.3), switch/rollback tức thì bằng đổi trỏ môi trường. *Loại canary:* đội 3 dev nhỏ, chưa có hạ tầng chia % traffic tự động ở lần đầu — quản canary tốn hơn giá trị nó mang lại; chia % để cho pha rollout (mục 4) thay vì ở tầng deploy.

### A. Các bước DEPLOY
1. Đóng băng merge vào `main` (delivery §1: main protected, squash-merge).
2. Chạy **migration** trên **green** (Postgres): `migrate up` — forward-only, versioned (delivery §7). Kỳ vọng: version tăng, smoke check schema PASS.
3. Deploy artifact vào môi trường **green** (Web/API + Reminder Worker cùng process — modular monolith, live slice §3.1). Cờ `confirm_dose_v2`, `reminder_dispatch_v2` **để TẮT**.
4. Chưa switch traffic. Green nhận 0% người dùng thật.

### B. KIỂM TRA SAU DEPLOY (smoke — phải XANH trước khi mở rộng)
Chạy đúng E2E slice bắt buộc (delivery §4 "smoke E2E") trên green:
1. `nightlyGenerate()` sinh DoseEvent `pending` — health worker xanh.
2. `everyMinute() → dispatchDue()` bắn **đúng 1** reminder cho 1 liều due (kỳ vọng: **không double-send** — đây là AC BLOCKED, phải xanh trước khi tin).
3. `POST /doses/{id}/confirm` với `userId` **đúng chủ** → 200, `pending→taken`, `takenAt` set.
4. `POST /doses/{id}/confirm` với `userId` **KHÁC chủ** → kỳ vọng **403** (kiểm IDOR đã vá — ô #5 live slice / AC BLOCKED). Nếu trả 200 ⇒ **DỪNG, không switch**.
5. `rateFor(user)` trả adherence đúng.
6. Health endpoint + 3 metric (reminder-latency, confirm-write p95, availability) đang chảy vào dashboard.
- **Ngưỡng "hỏng, rollback ngay":** bất kỳ smoke nào đỏ, hoặc bước 4 trả 200 (IDOR còn), hoặc metric confirm p95 > 300ms.

### C. Các bước ROLLBACK (khớp mục 2 — ai bấm)
1. **Người trực (chốt #10) bấm:** tắt cờ `confirm_dose_v2` + `reminder_dispatch_v2`.
2. Nếu chưa đủ: switch blue-green trỏ về **blue** (bản cũ).
3. Kiểm dữ liệu: `DoseEvent` đã ghi giữ nguyên; chỉ chạy backward migration nếu schema green không tương thích blue.
4. Xác nhận smoke trên blue xanh, thông báo kênh incident, mở ticket hậu kiểm.

---

## 4) ROLLOUT STRATEGY — lên DẦN, mỗi bậc một cổng nhỏ (5 bậc)

*Chọn đủ 5 bậc:* first production + chạm dữ liệu người dùng thật + dữ liệu y tế nhạy cảm ⇒ **không bật 100% một phát**. (Nếu sau này chỉ đổi copy sau cờ, có thể gộp bậc — không phải lần này.)

| Bậc | Ai / % | Quan sát | Tín hiệu TIẾN bậc kế | Đường lùi ở bậc đó |
|-----|--------|----------|----------------------|--------------------|
| 1. Internal alpha | Đội nội bộ (3 dev + PO), ~5 user | 2 ngày | 0 IDOR trên audit-log · 0 double-send · confirm p95 < 300ms | tắt cờ (chưa có người ngoài) |
| 2. Pilot group | 1 nhóm ~10 patient + caregiver tình nguyện | 1 tuần | error < 1% · reminder-latency < 60s ≥95% liều · PO OK · không phàn nàn nhắc-trùng | tắt cờ → luồng cũ song song |
| 3. Beta | ~25% patient | 1 tuần | SM-1 chỉ dấu không xấu đi · p95 giữ · 0 sự cố bảo mật | tắt cờ, giữ dữ liệu liều |
| 4. Gradual | 50% → 75% | vài ngày mỗi nấc | availability ≥ 99.5% · metric ổn định qua tải cao hơn | tắt cờ |
| 5. Full | 100% | liên tục (bàn giao /operate) | đã qua bậc 4 sạch | tắt cờ (vẫn giữ tới khi /operate xác nhận ổn định) |

**Góc nhìn lãnh đạo:** *"Lên theo 5 bậc, mỗi bậc có ngưỡng số để tiến hoặc lùi; đường lùi mọi bậc là tắt cờ, quay lại quy trình cũ song song — rủi ro chia nhỏ, không có cú 100% một phát."*

---

## Tự soi trước khi chốt
- Lãnh đạo đọc mục 0 biết ngay: **chưa cho lên**, ký cổng NO-GO tạm, hỏng thì tắt cờ + ai trực (đang khuyết). ✔
- Người trực cầm mục 2+3 thao tác được: bước deploy/smoke/rollback đánh số, có ngưỡng số. ✔ (còn phụ thuộc chốt tên người + cờ thật)
- Đủ 4 artifact + 12 ô (+2 ô cổng riêng): Go/No-Go · Rollback · Runbook · Rollout — đủ; ô không dùng ghi N/A. ✔
- 4 thứ chặn: rollback **CHƯA test** · monitoring/alert **CHƯA xác nhận bật** · incident owner **CHƯA tên** · Security **CHƯA ký** → **cả 4 đều thiếu ⇒ NO-GO**. ✔ (nêu rõ, không tô hồng)
- **Không tự bấm GO** — chỉ khuyến nghị; CTO + PO quyết. ✔

---

## CỔNG GO / NO-GO — MediRemind v1.0.0

```
═══ CỔNG GO / NO-GO — MediRemind v1.0.0 ═══
Sẵn sàng: 1/12 dòng checklist xong (UAT) · rollback CHƯA test · monitoring CHƯA xác nhận bật · trực sự cố CHƯA có tên
Còn chặn (6 chốt cứng + 2 nghiệp vụ):
  1) Security sign-off — TREO vì IDOR trên confirm-dose (CISO chưa ký)
  2) Rollback Plan — chưa test staging (hệ quan trọng ⇒ bắt buộc)
  3) Monitoring dashboard + alert — chưa bằng chứng đã BẬT trên production
  4) Incident owner — chưa gán tên người + kênh on-call
  5) OQ-A (managed queue vs cron) — ADR chưa đóng (bắt buộc trước GĐ13)
  6) OQ-B (retention NFR-4) — ADR chưa đóng (bắt buộc trước GĐ13)
  (+ 2 AC BLOCKED: permission confirm-dose = chính IDOR · double-send reminder)
Rollout (khi được GO): 5 bậc, bắt đầu internal alpha → pilot → beta → gradual → full
Khuyến nghị của ship: NO-GO (tạm) — vì đủ 4 thứ chặn cứng đều thiếu + Security treo trên dữ liệu y tế + luật dự án bắt đóng OQ-A/OQ-B trước cổng.
  Phương án đã loại: "GO-có-điều-kiện, vá sau khi lên" — LOẠI, vì lỗ IDOR là truy cập chéo dữ liệu sức khoẻ, không được cho lên rồi vá.
  Điều kiện để chuyển thành GO (thiếu gì · ai làm · xong khi):
    - Vá IDOR confirm-dose (kiểm dose.userId===req.userId) → Team Adherence + /frame; Security re-test & ký → CISO · xong khi Security sign-off ✔
    - Vá double-send reminder → Team Reminders + /frame · xong khi AC pass 20/20 (chạy lại /uat)
    - Test rollback drill trên staging → Team Adherence+Reminders · xong khi log "PASS ngày __"
    - Bật dashboard + alert (3 metric NFR) → SRE/Team Reminders · xong khi alert kêu thử được
    - Gán incident owner (tên + on-call) → CTO · xong khi có tên trong checklist ô #10
    - Đóng OQ-A + OQ-B bằng ADR → shape/stack + PO · xong khi 2 ADR merge
    → rồi mở CỔNG lại (chạy /uat để có report qua cổng, rồi /ship)
→ Người duyệt (CTO + PO) quyết: GO / NO-GO?
════════════════
```

> `ship` KHÔNG tự bấm GO. Trên đây là khuyến nghị + điều kiện; quyết định go-live thuộc **CTO + PO**.
> 2 AC BLOCKED và IDOR là **gap chất lượng** → trả ngược **/uat** (và **/review** để đào lỗ permission sâu) — `ship` không tự vá code.

---

## BÀN GIAO (chỉ kích hoạt SAU khi CTO+PO ký GO — hiện đang NO-GO)

```
═══ BÀN GIAO — MediRemind v1.0.0 (mẫu, dùng khi đã ký GO) ═══
Đã lên: <pha rollout hiện tại> bắt đầu <ngày>   Runbook + Rollback: outputs/ship/ship.md
Đang trực sự cố: <incident owner — chốt ô #10>   Monitoring/alert: 3 metric (reminder-latency ≤60s · confirm p95 ≤300ms · availability ≥99.5%) + audit-log IDOR
→ Vận hành, đo metric sau release, đóng vòng với Business Case GĐ1 (SM-1 on-time +≥15đpt / SM-2 caregiver-link ≥60%): chạy /operate
→ Rollout còn pha sau chưa mở: quay lại /ship khi tới mốc mở pha kế
→ Rollout gặp sự cố cần lùi: theo Rollback Plan (mục 2); sự cố lớn → /operate xử incident
→ Phát hiện gap chất lượng phải kiểm lại: quay về /uat (hoặc /review để đào lỗi sâu)
════════════════
```
**Hiện tại chưa bàn giao được** — cổng đang NO-GO, chờ CTO+PO quyết sau khi 6 chốt được vá.

---

*State (nếu ghi vào vùng skill): `giai_doan: gd13_ship` · `quyet_dinh: cho_duyet` (đã trình cổng, chờ CTO+PO — khuyến nghị NO-GO).*
*Nguồn: tóm tắt UAT ngoài state (prompt) + `docs/skeleton-live-slice.md` (GĐ8) + `problem/prd.md` + `docs/domain-model.md` + `codebase/delivery-standards.md` + `docs/module-map.md` + `progress/progress.json` + `constitution/definition-of-done.md`. Chưa có `codebase/uat-report.md` (GĐ12) — chạy /uat để có report qua cổng.*
