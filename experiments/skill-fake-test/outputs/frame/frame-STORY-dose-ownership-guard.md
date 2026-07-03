# FRAME — MediRemind · slice `STORY-dose-ownership-guard`

> Artifact do skill `frame` sinh (GĐ: đóng khung một slice trước khi code).
> Nguồn prefill (Bước 1b): `backlog.json` + `backlog.md` (GĐ9) · `skeleton-live-slice.md` (GĐ8, ô #5 FAIL) ·
> `domain-model.md` (GĐ5) · `contracts/adherence-v1.md` (GĐ10). Code thật: `fixture/codebase/mediremind/`.
> **Đây là lượt FRAME — CHƯA code. Kết bằng khối CHỜ XÁC NHẬN, DỪNG, chờ user duyệt.**

---

## Vì sao chọn slice này

Trong backlog GĐ9 có 9 story. Tôi chọn **`STORY-dose-ownership-guard`** vì đây là slice sạch nhất để đóng khung:

- Nó vá **đúng một khiếm khuyết đã biết**: ô #5 của Live Slice Report GĐ8 (`confirmDose` KHÔNG kiểm
  `dose.userId === req.userId` → bất kỳ user đăng nhập nào cũng xác nhận được liều của người khác — IDOR).
  Bằng chứng trong code thật: `src/adherence/dose.controller.ts:14` có comment `BUG-5 (IDOR / permission)`.
- backlog `da_chot` ghi rõ: *"ownership-guard vào R1 để vá ô #5 GĐ8 trước khi build rộng"* → đúng thứ tự.
- Diff nhỏ, một file, contract đã có sẵn error code (`ADH-403-NOT-OWNER`, 403) trong `adherence-v1.md`.
- Chạm đúng một đường: `confirmDose` (Adherence + Identity). Không kéo theo DB thật / auth mới / feature mới.

---

## ═══ PHASE frame: Constitution + Understand + Slice + Pick ONE — mediremind (level L6, mặc định) ═══

### 1. Nói lại mình hiểu gì (restate)

- **Project**: MediRemind — app nhắc uống thuốc & đo tuân thủ (adherence). Kiến trúc GĐ6 = modular
  monolith, 4 bounded context (Scheduling · Reminders · Adherence · Identity & Access). Stack GĐ7 =
  NestJS + BullMQ (nhưng code slice hiện tại là TS thuần, `db` in-memory).
- **Slice GĐ8** ("Patient xác nhận một liều") đã chứng minh kiến trúc chạy: sinh liều → nhắc → `POST
  /doses/:id/confirm` → `pending→taken` → tính lại rate. 7 PASS / 1 PARTIAL / **1 FAIL**.
- **FAIL đó (ô #5)** là điều slice này phải đóng: `confirmDose` set `dose.status='taken'` mà không hề
  kiểm liều có thuộc `req.userId` không. Đây là lỗ hổng phân quyền (IDOR), không phải lỗi luồng.
- **Story backlog**: `STORY-dose-ownership-guard` — *"Là patient, tôi muốn chỉ mình xác nhận được liều
  của mình, để không ai ghi hộ liều của tôi."* AC id: `AC-dose-ownership-guard-1`, `AC-dose-ownership-guard-2`.
  (Trong fixture `backlog.md` cùng story hiện dạng US-3.1.1 AC-1/AC-2; tôi dùng id mà `backlog.json` GĐ9 sinh.)

### 2. Giả định mình đang ngầm tin (assumptions — chờ user xác nhận/sửa)

- **A1** — `DoseEvent` đã có `userId` (đọc entity `dose-event.entity.ts:6` → có). Vậy kiểm quyền chỉ cần
  so `dose.userId === req.userId`, KHÔNG cần join sang Schedule/Medication. *(Đã kiểm code, coi là chắc.)*
- **A2** — Ownership check nằm **ngay trong `confirmDose`** (guard cục bộ), CHƯA rút ra
  `CaregiverGuard`/Nest guard chung — vì slice hiện là TS thuần, chưa lên Nest. Rút guard chung = over-engineer
  cho slice này → parking_lot.
- **A3** — Trả **403** với error code `ADH-403-NOT-OWNER` theo contract `adherence-v1.md`. Slice hiện trả
  string thô (`{status:404, body:'not found'}`); tôi giữ **cùng shape** (`{status, body}`), chỉ thêm nhánh 403 —
  KHÔNG đổi shape response 200/404 đang có (giữ contract & behavior hiện tại).
- **A4** — Đây là **slice `kind:"feature"`** (không phải live slice): KHÔNG chạm Postgres/BullMQ/auth thật;
  `req.userId` coi như đã do middleware set (như slice GĐ8 mô tả). Fake `db` in-memory giữ nguyên.
- **A5** — Chỉ chặn ownership cho **patient chủ liều**. Nhánh **caregiver được xem** (view-only) là chuyện
  của `STORY-caregiver-view-report` khác → KHÔNG kéo vào đây.

### 3. Khung slice (đủ 4 trường bắt buộc của FRAME)

| Trường | Nội dung |
|---|---|
| **user_action** | Patient đã đăng nhập gọi `POST /doses/:id/confirm` để xác nhận một liều. |
| **system_behavior** | Trước khi đổi trạng thái, hệ kiểm `dose.userId === req.userId`. Khớp → `pending→taken` + set `takenAt` + tính rate (như cũ). Không khớp chủ → trả **403** (`ADH-403-NOT-OWNER`), KHÔNG đổi trạng thái. Không tồn tại → 404 (như cũ). |
| **visible_output** | Chủ liều: `200 {id, status:'taken', adherenceRate}` (không đổi so với hiện tại). Không phải chủ: `403` + không có side-effect nào lên `db`. |
| **acceptance** | **AC-dose-ownership-guard-1** (chủ liều): patient là chủ → confirm → `pending→taken`, `takenAt` set, 200. **AC-dose-ownership-guard-2** (không phải chủ): liều thuộc user khác → **403**, trạng thái KHÔNG đổi (đóng ô #5 GĐ8). |

### 4. ~5 slice ở tầm nhìn (chỉ 1 active; còn lại parked/parking_lot — KHÔNG code kỳ này)

| Slice | Story | Trạng thái |
|---|---|---|
| **Ownership guard cho confirmDose** | `STORY-dose-ownership-guard` | **active** (kỳ này) |
| Xác nhận liều (happy path) | `STORY-dose-confirm` | done (đã chạy ở GĐ8) |
| Tính adherence rate an toàn (không NaN) | `STORY-adherence-rate` | parked |
| Đánh dấu liều quá hạn `missed` | `STORY-dose-missed` | parked (open-Q: grace window chưa chốt) |
| Caregiver xem báo cáo (view-only + audit) | `STORY-caregiver-view-report` | parked |

### 5. Mình sẽ KHÔNG làm gì (non-goals của slice này)

- KHÔNG rút guard chung / Nest guard / decorator `@Roles` (over-engineer — chưa lên Nest).
- KHÔNG đụng nhánh caregiver view-only (story khác).
- KHÔNG đổi shape response 200/404 hiện có; KHÔNG thêm field ngoài contract `adherence-v1.md`.
- KHÔNG thêm Postgres/auth thật/BullMQ; KHÔNG sửa `reminder.*`, `scheduling/*`, `legacy/*`.
- KHÔNG sửa `skip`/`report` endpoint dù cùng file contract — chỉ `confirm`.

---

## Contract dự kiến (sẽ chốt ở PHASE contract, CHƯA phải bây giờ)

```
confirmDose(req: { params:{id}, userId })
  input : dose id (path), req.userId (từ middleware)
  output: 200 { id, status:'taken', adherenceRate }        // chủ liều
  errors: 404 NOT_FOUND (liều không tồn tại — giữ nguyên)
          403 ADH-403-NOT-OWNER (dose.userId !== req.userId — MỚI)
  example in : id="u-sched-01-...-08:00", userId="u-pat-01" (là chủ) → 200 taken
  example in : cùng id, userId="u-pat-99" (không phải chủ)         → 403, không đổi db
```
File dự kiến đụng (khai trước, chốt ở contract): `src/adherence/dose.controller.ts` (thêm nhánh 403).
Test dự kiến (Stage 7): chủ→200+taken · không-chủ→403+không-đổi-trạng-thái · không-tồn-tại→404 (giữ).

---

## DoD từ delivery (tách RIÊNG — user nhận riêng, KHÔNG trộn vào acceptance)

Nguồn: `backlog.md §4` (Definition of Done). backlog GĐ9 nêu DoD chung; chưa có `pipeline/delivery.md`
(GĐ11 chưa chạy) nên đây là DoD mức backlog:

> mã + test (unit/E2E) xanh · qua PR review · đạt AC của story · không vi phạm NFR liên quan ·
> **có log/audit nếu chạm dữ liệu nhạy cảm (NFR-4)** · cập nhật doc nếu đổi contract.

Câu hỏi cho user: **bạn có nhận DoD này làm điều kiện đóng slice không?** (đặc biệt: slice này chạm phân
quyền dữ liệu sức khoẻ → có cần ghi log mỗi lần từ-chối-403 để lần vết không, hay để sau?)

---

## ─── CHỜ XÁC NHẬN ───

**Hiểu hiện tại:** Slice = vá lỗ hổng phân quyền ô #5 GĐ8 trong `confirmDose` — kiểm `dose.userId===req.userId`,
sai chủ thì 403 (`ADH-403-NOT-OWNER`), không đổi trạng thái. Story `STORY-dose-ownership-guard` (R1, backlog GĐ9).

**Giả định:** (A1) `DoseEvent.userId` đã đủ để kiểm quyền, không cần join · (A2) guard cục bộ trong controller,
không rút guard chung · (A3) giữ shape response cũ, chỉ thêm nhánh 403 · (A4) slice feature, không chạm hạ tầng thật.

**Sẽ đụng file:** `src/adherence/dose.controller.ts` (thêm nhánh 403 trước khi mutate) + một test cho slice.
KHÔNG đụng: `reminders/*`, `scheduling/*`, `identity/caregiver.guard.ts`, `legacy/*`, contract khác.

**Mình sẽ KHÔNG:** rút guard chung · đụng nhánh caregiver · đổi shape 200/404 · thêm DB/auth/BullMQ ·
sửa endpoint skip/report · build story nào khác.

**Hai thứ bạn (product owner / kiến trúc sư) giữ quyền quyết:**
1. **Acceptance (bạn giữ):** AC-dose-ownership-guard-1 (chủ→200 taken) + AC-dose-ownership-guard-2 (không-chủ→403,
   không đổi trạng thái). Đúng chưa, hay bạn muốn thêm/bớt?
2. **DoD từ delivery (bạn có nhận làm điều kiện đóng slice không?):** DoD chung backlog §4 — và riêng: có ghi
   audit-log khi từ-chối-403 ngay kỳ này không, hay đẩy sang `STORY-audit-caregiver-access`?

Chờ bạn xác nhận. **Mình sẽ KHÔNG viết code tới khi bạn duyệt.** (XÁC NHẬN / sửa)

════════════════

---

### Ghi chú thực thi (cho người kiểm skill, không phải cho user)

- Đây là **điểm DỪNG bắt buộc** theo SKILL.md §"Vòng lặp lõi" bước 5 và EXIT CRITERIA của FRAME: không sang
  CONTRACT tới khi `non_goals ∈ confirmed`, `domain.user_journey` chốt, đúng 1 slice active đủ 4 trường, và
  **user duyệt**. Chưa có lượt user duyệt trong mô phỏng này → dừng đúng ở đây, `awaiting_confirmation: true`.
- Không viết code (đúng "hỏi-trước-xác-nhận-trước-khi-viết"). Contract mới ở dạng *dự kiến*, chưa chốt vào
  `confirmed[]`.
- Bước 4b (drift vào `.ai-understanding/99_changes.md`): **bỏ qua** — codebase chưa chạy `/atlas`
  (`fixture/codebase/mediremind/.ai-understanding/` không tồn tại). Đúng quy định "không có → bỏ qua, KHÔNG tạo mới".
