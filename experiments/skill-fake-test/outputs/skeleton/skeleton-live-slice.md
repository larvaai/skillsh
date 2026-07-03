# LIVE SLICE REPORT — "Patient xác nhận một liều" (MediRemind, GĐ8 PROOF)

> Nhận từ: Tech Decision GĐ7 (`tech-decision.md`) · Architecture Brief GĐ6 (`architecture.md`) · Domain Model GĐ5 (`domain-model.md`).
> Trạng thái tổng: **CHỜ BẰNG CHỨNG** — slice đã được định hình + đường đi E2E + checklist validate đã dựng, nhưng slice **CHƯA được build chạy thật** (chưa có staging, chưa có local-proven: không docker-compose/test E2E/log). Không tick khống ô nào chưa có bằng chứng.

---

## ── GÓC NHÌN LÃNH ĐẠO (đọc trước) ──

**Bằng chứng** : CHƯA CÓ. Chưa có link staging bấm được, cũng chưa đạt cấp local-proven (chưa có lệnh `docker compose up` + test E2E xanh + trích log thật). Thứ đang có trong repo mới là **một bản phác in-memory** (`db.ts` tự ghi: *"Repo in-memory giả lập (slice demo). Thật sẽ là Postgres"*) — theo luật skill, "chạy trên máy mà không có test/log = chưa đạt".

**Cấp bằng chứng** : *chưa đạt cấp nào* (mục tiêu tối thiểu để qua cổng GĐ8 = local-proven).

**Trạng thái** : **0/9 ô validate tick THẬT.** Sẵn sàng đổ người vào build full: **CHƯA** — xương sống kiến trúc (NestJS + BullMQ/Redis + Postgres đã chốt ở GĐ7) chưa được chứng minh chạy thật một lần nào; đổ người lúc này là xây trên nền chưa kiểm.

**Giả định đã đổi** : *chưa phát sinh giả định-đã-đổi từ việc chạy thật* — vì slice chưa chạy thật, chưa có gì buộc PRD/Architecture phải chỉnh. (Có sẵn 3 điểm rủi ro-kiến-trúc **đã lộ khi đọc code phác**, liệt kê ở "Rủi ro còn lại" — nhưng đó là quan sát tĩnh, không phải bằng chứng chạy.)

**Rủi ro còn lại** :
1. **Quyền truy cập trên đúng slice này chưa chứng minh** — code phác của `POST /doses/:id/confirm` KHÔNG kiểm `dose.userId === req.userId` (IDOR): bất kỳ user đăng nhập nào cũng xác nhận được liều của người khác. Đây đúng là tầng Auth mà slice phải chứng minh → phải kiểm ở bước build proof (giao `/frame`), không được để qua cổng khi chưa gỡ.
2. **Tầng DB thật (Postgres + mã hoá at-rest NFR-4) chưa hiện diện** — hiện là mảng in-memory, mất khi tắt tiến trình → cần kiểm ở bước build proof (schema thật + at-rest).
3. **NFR-1 timeliness ≤60s (Reminder Worker → BullMQ/Redis)** — nhánh dispatch chưa nằm trong slice xác-nhận-liều nhưng là rủi ro kiến trúc trọng yếu của hệ → kiểm ở perf/timeliness test **GĐ12 (UAT)**.

---

## ── CHI TIẾT KỸ THUẬT (cho dev) ──

**Slice** : "Patient xác nhận một liều" — patient đăng nhập → mở reminder/deep-link của một `DoseEvent` đang `pending` → bấm "Đã uống" → backend kiểm quyền (dose thuộc chính patient) → chuyển `pending → taken` + set `taken_at` → tính lại `AdherenceReport.rate` → trả trạng thái về UI. (Đây đúng slice dọc mà Domain Model GĐ5 §3 và Data Flow GĐ6 §4 chỉ định cho GĐ8.)

**Đường đi (E2E)** — mô tả từng chặng + trạng thái thật hiện tại:

| Chặng | Slice phải chạm | Trạng thái thật (bằng chứng đọc từ code phác) |
|-------|-----------------|-----------------------------------------------|
| **UI** | Màn reminder/deep-link có nút "Đã uống" | CHƯA có UI trong repo (`src/` chỉ có tầng server). |
| **API** | `POST /doses/:id/confirm` | Có hàm phác `confirmDose` (`src/adherence/dose.controller.ts`) nhưng không phải endpoint NestJS thật (chưa có Nest module/controller/DI như ADR-007 chốt). |
| **Domain** | Chuyển `pending→taken`, set `takenAt` | Có logic (`dose.status='taken'; dose.takenAt=new Date()`) — đúng máy trạng thái Domain GĐ5. |
| **DB** | Postgres, mã hoá at-rest (NFR-4) | CHƯA — `src/common/db.ts` là mảng in-memory, tự ghi "Thật sẽ là Postgres". |
| **Auth** | Kiểm dose thuộc chính patient | CHƯA đạt — `confirmDose` bỏ kiểm `dose.userId === req.userId` (IDOR). `caregiver.guard.ts` có `canCaregiverView` cho nhánh caregiver view-only nhưng KHÔNG được gọi ở luồng confirm. |
| **Log** | Log/metric/trace của lần confirm | CHƯA có log/metric/trace nào. |
| **Test** | Test E2E slice xanh | CHƯA có test nào trong repo. |
| **CI/CD** | Pipeline xanh | CHƯA có config CI (không `.github/`, không workflow). |
| **Staging** | Link bấm được | CHƯA có. |
| **Monitor** | Observability (log/metric/trace) | CHƯA có. |

> Không tầng nào của lát cắt bị bỏ khỏi mô tả (đúng luật "không bỏ tầng"); nhưng phần lớn tầng hiện ở trạng thái *chưa build chạy thật* → checklist bên dưới để trống có chủ đích.

**Bằng chứng chạy** : *không có.* Không có link staging, không có lệnh local-proven (`docker compose up` + test E2E + trích log). Repo chưa có `package.json`/`tsconfig`/`docker-compose`/test/CI → chưa compile/chạy được như một app thật.

**Đã validate** (tick CHỈ khi có bằng chứng chạy thật — tất cả để trống vì chưa có bằng chứng):

```
[ ] architecture hợp lý       — chưa chạy thật lần nào để xác nhận modular monolith đứng được E2E
[ ] framework phù hợp         — ADR-007 chốt NestJS+BullMQ, nhưng repo chưa có app Nest thật để chứng minh
[ ] module boundary ổn        — code phác chưa dựng theo Nest module/DI; ranh giới 4 context chưa kiểm bằng chạy thật
[ ] auth chạy                 — RỚT ở đọc tĩnh: confirmDose thiếu kiểm chủ sở hữu (IDOR); chưa có bằng chứng chạy
[ ] DB schema hợp lý          — chưa có Postgres/schema thật; hiện in-memory
[ ] CI/CD xanh                — chưa có pipeline
[ ] test strategy thực tế     — chưa có test E2E/integration nào
[ ] observability đủ          — chưa có log/metric/trace
[ ] team hiểu flow delivery   — chưa có flow delivery chạy thật để team đi qua
```
**0/9 ô tick THẬT.** (Không ô nào được tick — không có staging/CI-xanh/test-pass/log-metric-trace để làm bằng chứng.)

**Lý do chọn slice** :
- Chọn **"Patient xác nhận một liều"** vì đây là lát cắt *mỏng nhất mà xuyên đủ tầng rủi ro cao nhất bằng ít code nhất*: chạm **Auth** (chủ sở hữu dữ liệu thuốc — chính là điểm nhạy NFR-4), **Domain** (máy trạng thái DoseEvent `pending→taken`), **DB ghi** (`taken_at`, cửa NFR-2 ≤300ms p95), và **tính lại AdherenceReport**. Domain Model GĐ5 §3 và Data Flow GĐ6 §4 đều chỉ đích danh slice này cho GĐ8.
- **Slice đã cân nhắc & loại**:
  - *"Gửi reminder tới hạn" (Worker→Redis→push)* — hấp dẫn vì chạm NFR-1 (≤60s) và BullMQ mới chốt, nhưng KHÔNG chạm write-path xác nhận của patient / máy trạng thái / quyền chủ-sở-hữu; là nhánh nền, để kiểm timeliness ở GĐ12. Loại khỏi slice-proof đầu tiên vì rủi ro auth+domain-write quan trọng hơn cho cổng "đổ người".
  - *"Caregiver xem báo cáo adherence"* — chỉ đọc + view-only, không chạm write/máy-trạng-thái; nhẹ rủi ro hơn slice confirm. Loại.
  - *"Sinh DoseEvent từ Schedule ban đêm"* — batch nền, không có UI/Auth theo phiên người dùng. Loại.

---

## ── CỔNG GO/NO-GO (A5) ──

**Câu hỏi cổng (doc GĐ8):** ***"Live slice pass chưa?"***

**Trình lên người duyệt:**
- **Chủ sở hữu** (dựng slice): Tech lead + 1–2 dev.
- **Người duyệt (mở cổng): CTO.** `skeleton` KHÔNG tự tuyên "pass" thay CTO.

**Trạng thái trình CTO:** 0/9 ô validate có bằng chứng; slice chưa chạy thật (chưa staging, chưa local-proven). Theo luật "ô rủi ro cao còn trống → mặc định **chưa pass**". Đây **chưa đạt cổng GĐ8** — chưa được scale ra nhiều module.

**Lối đi tiếp (không phủ định cứng — nêu đường tiến):**
1. **Build proof cho đúng slice này** → giao `/frame` với slice `kind:"live"` (loại được phép chạm hạ tầng thật): dựng app NestJS tối thiểu + BullMQ/Redis + Postgres thật (mã hoá at-rest), viết `POST /doses/:id/confirm` **có kiểm `dose.userId === req.userId`** (gỡ IDOR), thêm 1 test E2E "patient confirm liều của mình = 200, confirm liều người khác = 403", thêm log lần confirm.
2. **Chọn cấp bằng chứng khả thi**: nếu chưa có cloud → nhắm **local-proven** (`docker compose up` postgres+redis+app + test E2E xanh + trích log) — đủ qua cổng GĐ8 cho đội solo. Có cloud → dựng staging + CI xanh.
3. **Nhận `frame-return.json`** rồi quay lại lấp Report (proof_level, link/log, ci_status, test_result) và trình CTO lại.

---

## ── BÀN GIAO ──

```
═══ BÀN GIAO — Live Slice: "Patient xác nhận một liều" (TRẠNG THÁI: CHỜ BẰNG CHỨNG) ═══
Đã chứng minh   : CHƯA — slice mới được định hình + đường đi E2E + checklist; chưa có staging/local-proven, 0/9 ô.
Giả định đã đổi : chưa phát sinh từ chạy thật (3 rủi ro kiến trúc lộ khi đọc code phác, đã ghi ở Rủi ro còn lại).
Code thật slice : /Users/uspro/Desktop/skillsh/experiments/skill-fake-test/fixture/codebase/mediremind/src
                  (hiện là bản PHÁC in-memory + 7 bug chú thích; BUG-5 IDOR nằm ngay trong slice confirm) → build proof qua /frame
Artifact        : /Users/uspro/Desktop/skillsh/experiments/skill-fake-test/outputs/skeleton/skeleton-live-slice.md
Rủi ro còn lại  : IDOR trên confirm (kiểm ở bước build /frame) · Postgres+at-rest chưa hiện diện (build /frame) · NFR-1 ≤60s timeliness (kiểm ở GĐ12 UAT)
→ Build/chứng minh slice bằng CODE THẬT (dựng infra thật + test E2E + log): chạy /frame  ← BƯỚC KẾ BẮT BUỘC trước khi qua cổng
→ Sau khi slice pass thật, phân rã roadmap + backlog (Epic→Feature→Story→AC) cho R1 (GĐ9): chạy /backlog
→ Cần điều phối cả pipeline / traceability đủ: chạy /partner
════════════════
```

---

*Ghi chú trung thực (theo luật "PROVE, đừng MOCK"): bản Report này CỐ Ý để checklist 0/9 và cổng "chưa pass". Đầu vào GĐ8 chỉ có tài liệu + một bản phác in-memory (`db.ts` tự nhận là giả lập) chưa có test/log/staging, nên KHÔNG có bằng chứng hợp lệ để tick bất kỳ ô nào. Tick lúc này sẽ khiến lãnh đạo tin nhầm "kiến trúc đã chứng minh" và đổ ngân sách vào nền chưa chạy thật — đúng thứ cổng GĐ8 sinh ra để chặn.*
