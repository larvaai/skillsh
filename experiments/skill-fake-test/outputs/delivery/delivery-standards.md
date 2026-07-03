# MediRemind — Delivery Standards + DoR/DoD + PR Checklist (GĐ11)

> Áp cho MỌI team (Scheduling · Reminders · Adherence · Identity & Access). Chốt một lần, mọi slice của `frame` đi qua cùng một cổng.
> Nguồn: Module Map (4 bounded context) + Module Contract Scheduling v1 + Adherence v1.

```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Module Map + Module Contract" lấy từ prompt/file bạn đưa (docs/module-map.md + docs/contracts/), CHƯA qua cổng GĐ10 (skill /modules).
- Rủi ro: (1) chưa truy vết ngược được về pipeline; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /modules trước để có "Module Map + Module Contract" đã qua cổng.
```

**Mảnh THIẾU cần `modules` xác nhận (không bịa cho đủ):**
- Chỉ có Module Contract cho **2/4** module: Scheduling v1, Adherence v1. **Reminders** và **Identity & Access** chưa có file contract riêng → mọi chuẩn chạm 2 module này (contract-test, permission model, audit-log) dựng trên Module Map, đánh dấu `⟳ giả định` bên dưới, cần contract chính thức khoá lại.
- Stack/framework, CI provider, secret vault cụ thể chưa có Tech Decision (GĐ7) / Live Slice (GĐ8) trong input → chuẩn dưới nêu YÊU CẦU (cái gì phải có) chứ không khoá công cụ; điền công cụ khi `stack`/`skeleton` chốt.

---

## Góc nhìn lãnh đạo (đọc 30 giây)

**Định nghĩa "Xong" gói trong 1 khối + 4 chỉ số DORA bắt đầu đo.** MediRemind chạm dữ liệu y tế (lịch sử uống thuốc) và quyền caregiver xem báo cáo của bệnh nhân — nên "Xong" ở đây khắt khe hơn một app thường: mọi item merge phải có test, giữ contract giữa 4 team, có log/metric, và **module Identity & Access thêm 1 dòng cứng — audit-log truy cập caregiver (NFR-4) phải chạy, không có ngoại lệ**.

Exec chỉ cần nhìn hai thứ để biết giao hàng on-track:

| Chỉ số DORA | Ý nghĩa nghiệp vụ | Ngưỡng khởi điểm đề xuất |
|---|---|---|
| Lead time | Từ commit đến chạy prod bao lâu | ngày, không phải tuần |
| Deployment frequency | Đội giao hàng bao dày | ≥ vài lần/tuần/module |
| Change failure rate | Bao nhiêu lần deploy phải sửa gấp | < 15% |
| Recovery time (MTTR) | Hỏng rồi bao lâu về bình thường | < 1 giờ (có feature flag + rollback) |

Câu hỏi lãnh đạo tự hỏi mỗi tuần: *Có PR nào merge mà chưa xanh CI, chưa link story, hoặc chạm liều/quyền mà bỏ audit không?* — Nếu không, đội đang giao hàng an toàn.

---

## ARTIFACT 1 — Delivery Standards (12 mục, áp mọi team)

Độ sâu theo rủi ro: mục chạm **liều thuốc, quyền caregiver, event cross-module** viết kỹ (Secret · Migration · Observability · Incident · Testing); mục quy ước thường rút gọn.

### 1. Repository
- **Mono-repo, 4 module theo đúng Module Map:** `scheduling/ · reminders/ · adherence/ · identity/` + `shared/` (chỉ contract types + event schema, KHÔNG logic domain).
- **Lý do:** 4 module đổi contract lẫn nhau (event `DoseEventGenerated` cross 3 module) — mono-repo cho phép đổi contract + consumer trong 1 PR, chạy contract-test toàn cục. **Loại multi-repo:** đổi 1 event schema phải mở 3 PR ở 3 repo, lệch version, khó giữ contract khi 4 team chạy song song.

### 2. Branching
- **Trunk-based + short-lived branch (≤ 2 ngày), PR ≤ ~400 dòng.** Merge vào `main` khi CI xanh.
- **Lý do:** 4 team song song, muốn deploy nhiều lần/tuần; branch ngắn giảm merge đau khi nhiều team chạm `shared/`. **Loại git-flow:** nhánh release dài → contract lệch giữa các team, tích hợp muộn mới lộ vỡ event.

### 3. Coding standard
- Formatter + linter chạy **trong CI, fail-closed** (không format = CI đỏ). Naming entity bám đúng tên trong contract (`DoseEvent`, `Schedule`, `Reminder`, `CaregiverLink`) — không đặt tên khác domain.
- Error code trả về đúng bộ mã trong contract (`SCH-*`, `ADH-*`); không tự chế mã mới ngoài contract.

### 4. Review policy
- **Mỗi PR ≥ 1 reviewer, phải là người KHÁC tác giả.** PR chạm `shared/` (contract/event) → thêm reviewer từ **module tiêu thụ event** (đổi `DoseEventGenerated` cần Reminders + Adherence duyệt).
- PR chạm module **Identity & Access** (quyền/audit) → bắt buộc reviewer của Team Identity.

### 5. Testing pyramid
- **Tỉ lệ mục tiêu: 70 unit · 20 integration · 10 e2e.**
- **Contract test — bắt buộc cho mọi event cross-module** (bám thẳng Module Contract GĐ10):
  - `DoseEventGenerated` (Scheduling phát → Reminders + Adherence tiêu thụ): test producer giữ payload `{ dose_event_id, schedule_id, scheduled_time, status:"pending" }`; test mỗi consumer đọc đúng payload đó.
  - `DoseConfirmed` `{ dose_event_id, taken_at }` và `DoseMissed` `{ dose_event_id }` (Adherence phát) → consumer test tương ứng.
- **NFR test cứng** (dẫn thẳng vào UAT GĐ12):
  - Reminders: dispatch trong **60s** so với `scheduled_time` (NFR-1).
  - Adherence: ghi xác nhận liều **≤ 300ms p95** (NFR-2, `POST /v1/dose-events/{id}/confirm`).
  - Scale: pipeline sinh DoseEvent chịu **~250k DoseEvent/ngày** (NFR-3) — load test ở staging.
- **Lý do 70/20/10:** logic domain (sinh DoseEvent theo timezone, state machine liều) nặng ở tầng unit; e2e ít vì đắt, chỉ giữ luồng vàng.

### 6. CI/CD pipeline
- **Pipeline yêu cầu (fail-closed từng chặng):** `lint → typecheck → unit → integration → contract-test(DoseEventGenerated, DoseConfirmed, DoseMissed) → build → deploy staging → smoke → (gate người) deploy prod`.
- Không có chặng nào skip được từ PR. `⟳ giả định` provider CI cụ thể (GitHub Actions / GitLab CI) chọn khi `stack` chốt.

### 7. Environment strategy
- **3 tầng: dev → staging → prod.** Staging phải có Postgres + Redis + **provider Push/SMS ở chế độ sandbox** (không bắn tin thật cho bệnh nhân).
- **Lý do:** Reminders gọi provider ngoài; cần staging bắn thử để đo NFR-1 mà không spam bệnh nhân thật. **Loại 2 tầng (chỉ dev→prod):** không có nơi đo NFR-1/NFR-3 trước prod trên dữ liệu y tế.

### 8. Secret management
- **Secret trong vault/secret-manager, KHÔNG trong repo, KHÔNG trong `.env` commit.** CI đọc secret qua injected env lúc runtime.
- Bí mật cần quản: khoá provider Push/SMS, connection string Postgres/Redis, khoá ký token Identity.
- **CI có bước secret-scan fail-closed** (chặn commit lộ khoá). Rủi ro cao vì lộ khoá provider = spam/lộ tin nhắn y tế.

### 9. Feature flag
- Mỗi luồng chạm bệnh nhân bọc sau flag để rollback nhanh không cần deploy: `reminder_dispatch` (tắt gửi nhắc), `dose_confirm` (tắt ghi xác nhận), `caregiver_report_access` (tắt caregiver xem report nếu nghi lộ quyền).
- **Lý do:** MTTR < 1h chỉ đạt được nếu tắt được luồng hỏng bằng flag thay vì chờ rollback build.

### 10. Migration strategy
- **Forward-only, mỗi migration KÈM rollback script; reversible hoặc expand-contract.** Không sửa cột đang dùng trực tiếp — thêm cột mới → backfill → chuyển đọc → bỏ cột cũ ở PR sau.
- Migration chạm bảng `dose_events` (Scheduling ghi gốc, Adherence ghi state) → **phối hợp 2 team**, không đổi lược đồ một phía.
- **Lý do:** DoseEvent do Scheduling sinh nhưng Adherence đổi state — migration một phía làm vỡ ranh giới data-ownership trong contract.

### 11. Observability standard
- **Log JSON có `correlation_id`** xuyên `DoseEventGenerated → Reminder gửi → DoseConfirmed` để truy một liều từ sinh đến xác nhận.
- **Metric tối thiểu mỗi module:**
  - Scheduling: `dose_event_generated_total`, độ trễ sinh so với ngày chạy.
  - Reminders: `reminder_dispatch_latency_p95` (canh NFR-1 60s), `reminder_send_failed_total`.
  - Adherence: `dose_confirm_latency_p95` (canh NFR-2 300ms), `adherence_rate`.
  - Identity: `caregiver_report_access_total` + **audit-log truy cập caregiver (NFR-4)** — bắt buộc, không phải tuỳ chọn.

### 12. Incident process
- On-call theo module (mỗi Team owner giữ module mình). Severity theo tác động bệnh nhân: **nhắc thuốc không bắn (Reminders) = sev cao** — bệnh nhân bỏ liều.
- Quy trình: phát hiện (metric/alert) → tắt flag liên quan → thông báo → hotfix hoặc rollback → hậu kiểm (postmortem không đổ lỗi). `⟳ giả định` kênh on-call cụ thể chốt khi có tổ chức vận hành.

---

## ARTIFACT 2 — Definition of Ready + Definition of Done

### Góc nhìn lãnh đạo
**Đây là "Xong" gói trong 1 khối** — exec không đọc code, đọc khối này để tin mọi thứ merge đều đạt cùng một mức. **Không đạt DoD → không release. Đây là cổng cứng, không phải gợi ý.**

### DEFINITION OF READY (item được phép vào sprint)
```
[ ] có Acceptance Criteria rõ (nối ngược story GĐ9)
[ ] ước lượng
[ ] phụ thuộc rõ (module nào, event nào bị chạm)
[ ] đủ context để bắt đầu (contract của module liên quan đã có / hoặc ghi rõ đang chờ)
```

### DEFINITION OF DONE (BẮT BUỘC mọi item — không cắt dòng nào bất kể kích thước việc)
```
[ ] code review pass (reviewer khác tác giả; chạm shared/ → có reviewer module tiêu thụ event)
[ ] test pass: unit + integration xanh
[ ] contract giữ: mọi event cross-module (DoseEventGenerated / DoseConfirmed / DoseMissed)
    qua contract-test, không đổi payload ngầm
[ ] observability có: log JSON + metric tối thiểu của module
[ ] doc cập nhật (bao gồm OpenAPI/contract nếu API đổi)
[ ] không giảm chất lượng (coverage không tụt, lint xanh)
[ ] merge xanh CI (mọi chặng fail-closed đã qua)
```
**Dòng cứng thêm theo rủi ro (không được bỏ khi việc chạm vùng đó):**
```
[ ] chạm liều/quyền → security check: input validation + phân quyền đúng error code (SCH-403 / ADH-403 / ADH-403-NO-LINK)
[ ] chạm Identity & Access → audit-log truy cập caregiver (NFR-4) chạy, có test
```
> **Không đạt DoD → không release.**

DoR rút gọn được nếu backlog đã chuẩn; **DoD tuyệt đối không rút theo kích thước việc.**

---

## ARTIFACT 3 — PR Checklist

> Công cụ dev (không cần góc nhìn lãnh đạo riêng — giá trị lãnh đạo nằm ở DoD + DORA phía trên). Mỗi PR **link story/requirement** = sợi traceability nối ngược GĐ9/GĐ2–4. Ô không áp → đánh **N/A**, KHÔNG xoá ô.

```
[ ] link story/requirement (nối ngược GĐ9)
[ ] có test (unit/integration; contract-test nếu chạm event cross-module)
[ ] breaking change? (nếu có → đã thông báo team tiêu thụ)
[ ] update API contract? (đổi Public API / payload event → cập nhật contract Scheduling/Adherence)
[ ] có migration? (chạm dose_events → phối hợp Scheduling + Adherence)
[ ] security impact? (chạm liều/quyền → validate + error code đúng)
[ ] observability (log/metric)? (metric tối thiểu module + correlation_id)
[ ] ảnh hưởng module khác? (chạm DoseEventGenerated → Reminders + Adherence; chạm quyền → Identity)
[ ] rollback plan nếu rủi ro cao? (feature flag tương ứng: reminder_dispatch / dose_confirm / caregiver_report_access)
```

**Ví dụ PR đã điền (mẫu cho đội):**
```
PR — feat(scheduling): POST /v1/schedules sinh DoseEvent + phát DoseEventGenerated
[x] link Story "Tạo lịch uống thuốc"
[x] test: unit (sinh theo timezone) + integration + contract-test(DoseEventGenerated payload)
[ ] breaking change — N/A (endpoint mới)
[x] update API contract — thêm POST /v1/schedules vào Scheduling v1
[x] migration: bảng schedules + dose_events (phối Team Adherence vì Adherence ghi state)
[x] security: validate times_per_day/date-range → SCH-400-*; chủ sở hữu → SCH-403-NOT-OWNER
[x] observability: log correlation_id + metric dose_event_generated_total
[x] ảnh hưởng module khác: Reminders + Adherence tiêu thụ DoseEventGenerated → đã thêm reviewer 2 team
[x] rollback: sau flag (sinh dừng nếu tắt Scheduling job)
Reviewer: Tech lead Team Scheduling + reviewer Reminders + reviewer Adherence — DoD ✔
```

---

## Tự soi trước khi chốt

- Lãnh đạo đọc đoạn MỞ (DoD 1 khối + 4 chỉ số DORA) có hiểu giao hàng on-track không, không vướng jargon? → Có: khối DORA + câu hỏi tuần bằng ngôn ngữ nghiệp vụ.
- Dev đủ để hành động (branch thế nào, CI chạy gì, test tối thiểu, PR qua cổng nào, "Done" là gì)? → Có: 12 mục Standards + pyramid có tỉ lệ + pipeline có chặng + DoD liệt kê.
- Đủ + đúng 3 artifact (Standards 12 mục · DoR/DoD · PR Checklist 9 dòng), DoD giữ nguyên khối không cắt? → Có.
- Chuẩn bám Module Contract GĐ10 (contract-test cho event cross-module, ô checklist nối contract thật) hay bịa? → Bám: dùng đúng event `DoseEventGenerated/DoseConfirmed/DoseMissed`, error code `SCH-*/ADH-*`, NFR-1/2/3/4 từ contract; chỗ thiếu (contract Reminders/Identity) đã đánh dấu `⟳ giả định`, không bịa payload.
- Mỗi quyết định lớn có LÝ DO + phương án đã loại? → Có: repo (loại multi-repo), branching (loại git-flow), env (loại 2 tầng).

---

## Cổng go/no-go (GĐ11)

> ***"Item đạt Definition of Done chưa? Chuẩn delivery đủ để 4 team (Scheduling · Reminders · Adherence · Identity) giao hàng an toàn, song song chưa?"***

**Phân vai (A5):**
- **CTO / Kiến trúc sư** SỞ HỮU chuẩn delivery này (duyệt artifact).
- **Reviewer được chỉ định** duyệt từng PR theo checklist.
- **Team owner mỗi module** giữ chất lượng module mình (Scheduling/Reminders/Adherence/Identity).
- `delivery` (AI) đã DRAFT chuẩn + checklist + cổng + tự soi. **AI KHÔNG tự tuyên bố pass / không tự mở cổng.** Trình khối này, chờ CTO + Team owner quyết GO.

**Điều kiện GO đề xuất:** chấp nhận 12 mục Standards + DoR/DoD + PR Checklist; đóng 2 mảnh thiếu (contract Reminders + Identity, hoặc chấp nhận chạy với `⟳ giả định`); khoá công cụ CI/vault khi `stack`/`skeleton` chốt.

---

## Bàn giao sang uat (GĐ12)

```
═══ BÀN GIAO — Delivery Standards MediRemind ═══
Đã chốt (chờ CTO duyệt): Delivery Standards (12 mục) + DoR/DoD + PR Checklist (áp 4 team)
Artifact: experiments/skill-fake-test/outputs/delivery/delivery-standards.md
→ Chứng minh hệ làm đúng (mapping AC→test→result, UAT + security sign-off): chạy /uat (GĐ12)
→ Code từng slice theo chuẩn này: chạy /frame
→ Đào gap sâu (edge case, error path, permission caregiver) một luồng trước khi verify: chạy /review
═══════════════════
```
Chỉ liệt kê — không tự chọn hộ skill nào chạy tiếp.
