# MediRemind — Test & Verification Report (GĐ12 · UAT)

_Phạm vi: slice **xác-nhận-liều** (AC-1..AC-5) + NFR-1..5. Release ứng viên: v1.0 (MVP)._

```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Delivery Standards + Definition of Done" lấy từ prompt/file bạn đưa
  (fixture/mediremind/codebase/delivery-standards.md + constitution/definition-of-done.md),
  CHƯA qua cổng GĐ11 chuẩn (state/project/<name>/pipeline/delivery.md của skill /delivery).
- Rủi ro: (1) chưa truy vết ngược được về pipeline state; (2) có thể lệch/mâu thuẫn với
  domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu
  phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /delivery trước để có
  "Delivery Standards + Definition of Done" đã qua cổng.
```

---

## 1) GÓC NHÌN LÃNH ĐẠO (đọc trước — 30 giây)

**Chưa đủ điều kiện trình go-live. Lý do gọn: hệ CHƯA CÓ tầng test nào để chứng minh — không có
bằng chứng, không phải không đạt.**

- **Tỷ lệ pass:** **0/5 AC có test tự động** trong repo (đã quét toàn `src/`, không có file
  `*.spec.ts` / `*.test.ts` / e2e / contract test nào). Không có test ⇒ không có kết quả PASS/FAIL
  để báo ⇒ mọi AC đang ở trạng thái **BLOCKED (chờ có test)**, không phải FAIL.
- **Hai chữ ký:** UAT sign-off (PO) = **CHỜ** · Security sign-off (Sec/CISO) = **CHỜ**. `uat` KHÔNG
  ký thay; report này chuẩn bị để hai vai đó ký khi điều kiện đủ.
- **Còn hở gì (1 dòng):** **5/5 AC đang hở test** + 5 NFR chưa có số đo (latency p95, timeliness 60s,
  scale 250k/ngày, audit-log, availability). Đây là **hở test** — chuyển `/review` để đào cho đủ case,
  rồi `/delivery`·`/frame` để viết test cho mỗi AC. Sau khi có test mới quay lại `uat` chốt kết quả.

> Điều kiện tối thiểu để MediRemind qua cổng GĐ12 (theo DoD GĐ11 + luật cổng constitution): mỗi AC có
> unit+integration test xanh, smoke E2E "xác-nhận-liều" xanh, NFR-2 đo p95, audit-log áp cho path
> caregiver (NFR-4). Hiện **chưa mảnh nào có bằng chứng** trong repo.

---

## 2) BẢNG MAPPING (xương traceability — Requirement → AC → Test Case → Result → Release Decision)

Nguồn Requirement/AC: `problem/requirements.md` (GĐ3) → `prd.md` (GĐ4). Chuẩn "đã verify": DoD trong
`constitution/definition-of-done.md` + `delivery-standards.md §DoD` (GĐ11). Mã TC là **mã dự kiến** —
chưa có file test tương ứng trong repo nên cột Test Case ghi mã + đánh dấu **[HỞ: chưa có test]**.

| Requirement (GĐ3–4) | Acceptance Criteria | Test Case (dự kiến) | Test Result | Release Decision |
|---|---|---|---|---|
| Slice xác-nhận-liều · SM-1 | **AC-1** DoseEvent `pending→taken`, ghi `taken_at`, adherence tính lại | `TC-DOSE-CONFIRM-001` **[HỞ: chưa có test]** | **BLOCKED** — không có unit/integration/E2E; observe: `dose.controller.confirmDose` có chuyển trạng thái nhưng `adherence.service.rateFor` chưa có test bảo vệ | **Chưa đủ** cho v1.0 — thiếu test bắt buộc theo DoD |
| NFR-2 (latency ≤300ms p95) | **AC-2** ghi xác nhận hoàn tất **≤300ms p95** | `TC-DOSE-CONFIRM-PERF-002` **[HỞ: chưa có perf test]** | **BLOCKED** — chưa có số đo p95 nào (yêu cầu cứng của DoD: "confirm-write đo p95") | **Chưa đủ** — NFR-2 chưa được kiểm chứng |
| Slice xác-nhận-liều | **AC-3** không xác nhận lại liều đã chốt (`taken/missed/skipped`) | `TC-DOSE-CONFIRM-IDEMPOTENT-003` **[HỞ: chưa có test]** | **BLOCKED** — chưa có test; contract có `ADH-409-ALREADY-RESOLVED` nhưng không có test chứng minh nó chặn double-confirm | **Chưa đủ** — hành vi idempotent chưa được verify |
| NFR-4 (kiểm soát truy cập) · caregiver view-only | **AC-4** chỉ chủ liều xác nhận được; caregiver **view-only** | `TC-DOSE-CONFIRM-AUTHZ-004` **[HỞ: chưa có test]** | **BLOCKED** — chưa có authz/permission test cho path confirm | **Chưa đủ** — quyền trên path xác-nhận chưa được verify (blocker theo NFR-4) |
| Slice xác-nhận-liều · adherence | **AC-5** liều quá hạn `pending→missed`, phản ánh vào adherence | `TC-DOSE-MISSED-005` **[HỞ: chưa có test]** | **BLOCKED** — chưa có test cho chuyển `pending→missed` (batch `DoseMissed` trong contract) | **Chưa đủ** — chuyển trạng thái missed chưa được verify |
| NFR-1 (timeliness ≤60s) | Reminder bắn trong 60s so với `scheduled_time` | `TC-REMINDER-LATENCY-006` **[HỞ: chưa có test]** | **BLOCKED** — chưa có test đo latency reminder | **Chưa đủ** — NFR-1 chưa kiểm chứng |
| NFR-3 (scale 250k/ngày) | 50k user · ~250k DoseEvent/ngày | `TC-SCALE-LOAD-007` **[HỞ: chưa có load test]** | **BLOCKED** — chưa có load/scale test | **Chưa đủ** — NFR-3 chưa kiểm chứng |
| NFR-4 (audit-log caregiver) | audit-log MỌI truy cập caregiver (DoD bắt buộc) | `TC-AUDIT-CAREGIVER-008` **[HỞ: chưa có test]** | **BLOCKED** — chưa có test audit-log; `caregiver.guard.canCaregiverView` tồn tại nhưng không có test | **Chưa đủ** — điều kiện DoD "audit-log mọi path caregiver" chưa verify |
| NFR-5 (availability 99.5%) | 99.5% (không life-critical) | `TC-AVAILABILITY-009` **[HỞ: chưa có ops readiness]** | **BLOCKED** — chưa có số đo/availability check | **Chưa đủ** — NFR-5 chưa kiểm chứng |

**Nối traceability:**
- Ngược lên: mỗi hàng AC-x trace về `requirements.md §1` (GĐ3) và `prd.md §5-6` (GĐ4); NFR trace về
  `requirements.md §2` + `delivery-standards.md §8 (Observability metric NFR)`.
- PR/story GĐ11: `delivery-standards.md` định "AC map tới NFR" (DoR) và DoD "Unit+integration xanh;
  smoke E2E slice xác-nhận-liều xanh". Không có PR/commit test nào trỏ tới được → **sợi traceability
  ĐỨT tại mắt "Delivery → Test"**: code có (build T-11a/T-11b), test-pyramid CHƯA có.
- Xuôi xuống: cột Release Decision là đầu vào cho `/ship` (GĐ13) — hiện toàn bộ "Chưa đủ".

---

## 3) TEST & VERIFICATION REPORT (lớp test + hai chữ ký)

### Bảng lớp test (Đủ-là-đủ theo rủi ro — MediRemind = dữ liệu sức khoẻ nhạy cảm NFR-4 ⇒ hệ RỦI RO CAO)

Vì đụng dữ liệu nhạy cảm + kiểm soát truy cập (NFR-4), slice này KHÔNG phải "slice nội bộ rủi ro thấp";
cần đủ các lớp dưới. Không lớp nào bỏ vì "gọn" — tất cả đang **THIẾU (chưa dựng)**, ghi rõ:

| Lớp test | Phạm vi cần | Pass/Fail | Ghi chú |
|---|---|---|---|
| unit | sinh DoseEvent, chuyển trạng thái, tính adherence rate (DoD §Unit) | **THIẾU** | 0 file unit test trong repo. `adherence.service.rateFor` không có test bảo vệ |
| integration | mỗi contract endpoint (confirm/skip/report) + domain event `DoseConfirmed`/`DoseMissed` | **THIẾU** | 0 file integration test |
| contract | scheduling-v1 · adherence-v1 (error code `ADH-403/404/409`) | **THIẾU** | contract có định error code nhưng không có contract test kiểm |
| e2e (smoke) | "Patient xác nhận một liều" — DoD gọi đây là smoke E2E **bắt buộc** | **THIẾU** | live slice GĐ8 có chạy staging nhưng repo hiện không có file test E2E |
| regression | — | **THIẾU** | chưa có baseline test để hồi quy |
| perf | confirm-write p95 (NFR-2) · reminder latency (NFR-1) | **THIẾU (bắt buộc)** | DoD yêu cầu "confirm-write đo p95"; chưa có số |
| security (SAST/DAST) | authz path confirm (AC-4) · at-rest encryption · audit-log (NFR-4) | **THIẾU (bắt buộc)** | hệ nhạy cảm → SAST/DAST là điều kiện Security sign-off, chưa chạy |
| a11y | (deep-link reminder → UI xác nhận) | **THIẾU** | ghi lý do: UI ngoài phạm vi slice backend hiện tại; đưa vào vòng có UI |
| UAT | PO nghiệm thu slice xác-nhận-liều theo AC-1..5 | **CHỜ** | chưa có test để PO dựa vào nghiệm thu |
| operational readiness | audit-log request-id, metric NFR (§8 delivery) | **THIẾU** | metric NFR-1/2/5 chưa có dashboard/số |
| DR/rollback | migration reversible (delivery §7) | **THIẾU** | thuộc `/ship` (GĐ13) — ghi để không im lặng |

**Lý do lớp bỏ/hoãn (Đủ-là-đủ, không im lặng):**
- a11y hoãn: slice hiện là backend (deep-link + API); đưa a11y vào vòng khi có UI xác-nhận thật.
- DR/rollback thuộc cổng GĐ13 (`/ship`) — nêu ở đây để đủ, không tự làm.
- Không lớp bắt buộc nào (unit/integration/e2e/perf/security) được bỏ — tất cả là **THIẾU thật**, phải dựng.

### Hai chữ ký

```
UAT sign-off      : <PO — TÊN>      ngày ____   →  CHỜ  (chưa đủ điều kiện trình ký: 0/5 AC có test)
Security sign-off : <Sec/CISO — TÊN> ngày ____   →  CHỜ  (chưa đủ điều kiện trình ký: chưa có SAST/DAST,
                                                          chưa verify authz AC-4 + audit-log NFR-4)
```

> `uat` KHÔNG tự đóng hai chữ ký hộ người thật. Report này chỉ đủ điều kiện **trình ký** khi bảng
> mapping có Test Result thật (không còn BLOCKED-vì-thiếu-test) và hai lớp bắt buộc perf + security có số.

---

## Cổng GO/NO-GO (GĐ12)

```
═══ CỔNG GO/NO-GO (GĐ12 UAT) — mediremind ═══
Pass: 0/5 AC có test · 0 PASS            Gap chưa test: 9 (AC-1..5 + NFR-1/3/4 audit-log/5)
UAT sign-off: PO — CHỜ                    Security sign-off: Sec/CISO — CHỜ
Đủ điều kiện go-live? → CHƯA — cần: (1) viết unit+integration+smoke E2E cho AC-1..5;
   (2) đo NFR-2 p95 + NFR-1 latency; (3) SAST/DAST + verify authz AC-4 + audit-log NFR-4;
   rồi quay lại /uat chốt Test Result + trình 2 chữ ký.
═══════════════
```

**Lối đi tiếp (không phủ định cứng):** hệ chưa "không release được" — nó **chưa có bằng chứng để xét**.
Đường đi: `/review` đào đủ case/edge/permission cho slice xác-nhận-liều (đặc biệt AC-3 double-confirm,
AC-4 quyền, NFR-4 audit-log) → `/frame`·`/delivery` viết test theo test-pyramid cho từng AC → chạy CI
(lint→unit→integration→build theo delivery §3) → quay lại `/uat` điền Test Result thật → trình PO + Security ký.

---

## Bàn giao

```
═══ BÀN GIAO — mediremind (GĐ12 → ?) ═══
Đã chứng minh: 0/5 AC PASS · UAT chờ · Security chờ
Điều kiện/hở còn treo: 5/5 AC hở test + 5 NFR chưa đo; sợi Delivery→Test đang ĐỨT (code có, test-pyramid chưa)
Ngoài phạm vi uat (2 open-Q của project CHƯA đóng, ghi để ship không bỏ sót): OQ-A (queue vs cron),
   OQ-B (retention NFR-4) — phải đóng bằng ADR trước cổng GĐ13.
Artifact: outputs/uat/uat-report.md (+ sign-off-uat.md, sign-off-security.md)
→ Còn nghi gap/edge case/permission chưa test hết (đúng tình huống hiện tại): chạy /review trước
→ Có AC chưa có test / cần viết test rồi re-verify: chạy /frame cho slice test (hoặc /delivery)
→ CHỈ khi mọi AC blocker PASS + 2 chữ ký đủ: mới chạy /ship (GĐ13) làm Go/No-Go + Runbook + rollback
═══════════════
```

_Chỉ liệt kê — user quyết chạy skill nào tiếp. `uat` không tự chọn hộ, không tự quyết go/no-go._
