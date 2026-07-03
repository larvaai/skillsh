# Trace — trường `status` của một `DoseEvent`

- **Đối tượng**: `DoseEvent.status` (kiểu `DoseStatus = 'pending' | 'taken' | 'missed' | 'skipped'`)
- **Loại trace**: **state** — tìm TẤT CẢ chỗ `status` có thể thay đổi, không chỉ happy path.
- **Codebase**: `fixture/codebase/mediremind`
- **Nguồn**: trace từ file gốc — KHÔNG có `.ai-understanding/` (nên gợi ý chạy `atlas` sau để lưu lại cho lần sau).

---

## Tình huống đời thường (mental model trước khi vào code)

**TÌNH HUỐNG:** Một cuốn sổ theo dõi uống thuốc. Mỗi sáng, thư ký kẻ sẵn các ô cho từng cữ thuốc trong ngày, mỗi ô đóng dấu "chờ". Khi tới giờ, người nhắc gọi điện báo. Bệnh nhân uống xong thì tự tay tick vào ô, ô đổi thành "đã uống". Cuối cùng kế toán đếm số ô "đã uống" trên tổng số ô để ra điểm chuyên cần.

| Đời thường | Trong code |
|---|---|
| Ô trạng thái trong sổ | trường `status` của `DoseEvent` |
| Thư ký kẻ ô & đóng dấu "chờ" mỗi sáng | `DoseGeneratorService.generateForDay` (khởi tạo `status: 'pending'`) |
| Người nhắc gọi điện tới giờ | `ReminderService.dispatchDue` (chỉ ĐỌC ô "chờ", không sửa) |
| Bệnh nhân tự tay tick "đã uống" | `confirmDose` (ghi `status = 'taken'`) |
| Kế toán đếm điểm chuyên cần | `AdherenceService.rateFor`, `currentStreak` (chỉ ĐỌC) |

**Điều đáng chú ý ngay từ mental model:** trong đời có 4 loại dấu ('chờ', 'đã uống', 'lỡ', 'chủ động bỏ') nhưng code chỉ biết đóng đúng 2 dấu: `'pending'` (lúc kẻ ô) và `'taken'` (lúc tick). Không có bút nào viết được `'missed'` hay `'skipped'` — đây là phát hiện chính của trace state này.

---

## TỔNG HỢP

**ĐỐI TƯỢNG:** `DoseEvent.status`
**LOẠI:** state
**ĐƯỜNG ĐI (vòng đời của một ô status):**

```
[khai báo type] dose-event.entity.ts (DoseStatus, 4 giá trị)
      │
      ▼
[WRITE #1] dose-generator.service.ts · generateForDay → status = 'pending'   (điểm khởi tạo duy nhất)
      │
      ├──[READ] reminder.service.ts · dispatchDue   (lọc status === 'pending' để gửi nhắc — KHÔNG ghi)
      │
      ▼
[WRITE #2] dose.controller.ts · confirmDose → status = 'taken'   (điểm chuyển state duy nhất do người dùng kích)
      │
      ├──[READ] adherence.service.ts · rateFor      (đếm status === 'taken' / tổng)
      └──[READ] adherence/streak.ts · currentStreak (map 'taken'→1, 'skipped'→-1, còn lại→0)
```

### ĐIỂM THAY ĐỔI QUAN TRỌNG (mọi write point của `status`)

- **[W1]** `scheduling/dose-generator.service.ts` · `generateForDay` (dòng 33) — **[STATE CHANGE: → 'pending']** Sinh mới `DoseEvent` với `status: 'pending'`. Đây là chỗ DUY NHẤT tạo ra ô status. Chạy bởi cron 00:05 mỗi sáng (`reminder.worker.ts · nightlyGenerate`). Độ chắc: **cao**.
- **[W2]** `adherence/dose.controller.ts` · `confirmDose` (dòng 16) — **[STATE CHANGE: → 'taken']** Gán trực tiếp `dose.status = 'taken'` khi patient bấm "Đã uống" (POST /doses/:id/confirm). Đây là chỗ DUY NHẤT chuyển đổi state sau khởi tạo. Độ chắc: **cao**.

> **KHÔNG có write point nào cho `'missed'` và `'skipped'`.** Hai giá trị này được KHAI BÁO trong type `DoseStatus` và được ĐỌC ở `rateFor`/`currentStreak`, nhưng không hàm nào trong codebase từng GHI chúng. Trong toàn bộ code, một ô chỉ đi được `'pending' → 'taken'` (hoặc kẹt mãi ở `'pending'`). Độ chắc: **cao** (đã quét toàn bộ 12 file `src/`).

### SIDE EFFECT TÌM ĐƯỢC

Đi kèm mỗi lần status đổi:

- **Tại [W1] `generateForDay`** — **[SIDE EFFECT]** `db.doseEvents.push(...events)` (dòng 39): các event mới (status='pending') được đẩy vào store dùng chung `db.doseEvents`. Đây là shared mutable state mà `dispatchDue`, `rateFor`, `currentStreak` cùng đọc.
- **Tại [W2] `confirmDose`** — **[SIDE EFFECT]** đi kèm `dose.takenAt = new Date()` (dòng 17): cùng một action ghi thêm timestamp. Vì `dose` là tham chiếu tới object nằm trong `db.doseEvents`, việc gán mutate thẳng vào shared store (không copy).
- **Tại [W2] `confirmDose`** — **[SIDE EFFECT gián tiếp]** gọi `adherence.rateFor(dose.userId)` (dòng 19) ngay sau khi đổi status, để trả `adherenceRate` trong response. Tức mỗi lần status→'taken' kéo theo một lượt tính lại tỉ lệ tuân thủ.
- **Ở nhánh ĐỌC (không đổi status nhưng phụ thuộc status):** `dispatchDue` gửi push qua `pushProvider.send` (I/O ra ngoài) cho các dose `status === 'pending'`, và `db.reminders.push(...)`. Không sửa status nhưng là side effect được KÍCH bởi giá trị status.

### CHƯA RÕ / RỦI RO

- **[RỦI RO — state không đầy đủ, chắc chắn]** `'missed'` và `'skipped'` không bao giờ được ghi ⇒ (a) liều bị bỏ lỡ vẫn kẹt ở `'pending'` mãi (không có bút nào chuyển sang `'missed'` khi quá giờ); (b) `rateFor` (dòng 15–17) tính mẫu số = tổng mọi event gồm cả `'pending'` chưa tới giờ ⇒ tỉ lệ tuân thủ bị kéo tụt sai (khớp BUG-6/BUG-7 ghi trong file); (c) `currentStreak` có nhánh xử lý `'skipped'` (→ -1) nhưng nhánh đó chết vì không data nào từng mang `'skipped'`.
- **[RỦI RO — quyền, chắc chắn]** [W2] `confirmDose` KHÔNG kiểm `dose.userId === req.userId` (comment BUG-5, IDOR): bất kỳ user đã đăng nhập nào cũng đổi được `status` liều của người khác. Đây là write point mở cho mọi caller — trace state cần đánh dấu vì nó nới rộng "ai có thể ghi vào status".
- **[BOUNDARY]** `db` là repo in-memory giả lập (`common/db.ts`, comment "Thật sẽ là Postgres"). Mọi mutation status hiện chỉ nằm trong process; bản thật sẽ là ghi DB — không trace tiếp qua boundary này.
- **[Đã loại]** `legacy/old_reminder_cron.ts` — không import ở đâu, chỉ `console.log`, không đụng `status`. Không nằm trên đường đi.
- **[Không liên quan tới status]** `identity/caregiver.guard.ts` (`canCaregiverView`) chỉ gác quyền XEM báo cáo, không đọc/ghi `status`.

---

## BẰNG CHỨNG CHI TIẾT (Bước 2 — theo từng điểm)

```
[0] scheduling/dose-event.entity.ts · type DoseStatus (dòng 1) + interface DoseEvent.status (dòng 8)
    Xảy ra: khai báo 4 giá trị hợp lệ 'pending'|'taken'|'missed'|'skipped'; status là field bắt buộc.
    Độ chắc chắn: cao
    Chưa rõ: type cho phép 4 giá trị nhưng chưa nói giá trị nào thực sự được dùng (xem [1]..[6]).

[1] scheduling/dose-generator.service.ts · generateForDay (dòng 28–35)
    Xảy ra: tạo object DoseEvent mới với status: 'pending', takenAt: null.
    [STATE CHANGE] → 'pending' (khởi tạo)
    [SIDE EFFECT] db.doseEvents.push(...events) (dòng 39) — ghi vào shared store.
    Độ chắc chắn: cao
    Kích bởi: reminder.worker.ts · nightlyGenerate (cron 00:05) → generator.generateForDay(uid, today).

[2] reminders/reminder.service.ts · dispatchDue (dòng 11–13)
    Xảy ra: filter e.status === 'pending' (chỉ ĐỌC status để chọn dose cần nhắc). KHÔNG ghi status.
    [SIDE EFFECT] pushProvider.send(...) (I/O ngoài, dòng 21) + db.reminders.push(...) (dòng 22).
    Độ chắc chắn: cao
    Chưa rõ: không có bước nào sau khi gửi nhắc để chuyển 'pending' → 'missed' nếu quá hạn.

[3] adherence/dose.controller.ts · confirmDose (dòng 16–17)
    Xảy ra: dose.status = 'taken'; dose.takenAt = new Date().
    [STATE CHANGE] → 'taken' (chuyển state duy nhất do người dùng kích, POST /doses/:id/confirm)
    [SIDE EFFECT] mutate thẳng object trong db.doseEvents (dose là reference); gọi rateFor (dòng 19).
    Độ chắc chắn: cao
    Rủi ro: dòng 14 comment BUG-5 — thiếu check dose.userId === req.userId (IDOR).

[4] adherence/adherence.service.ts · rateFor (dòng 12–18)
    Xảy ra: đếm status === 'taken' (tử số) / events.length (mẫu số). Chỉ ĐỌC status.
    Độ chắc chắn: cao
    Rủi ro: mẫu số gồm cả 'pending'/'skipped' (BUG-7) và chia 0 khi rỗng → NaN (BUG-6).

[5] adherence/streak.ts · currentStreak (dòng 7)
    Xảy ra: map status: 'taken'→1, 'skipped'→-1, còn lại→0 để tính chuỗi ngày. Chỉ ĐỌC status.
    Độ chắc chắn: cao
    Chưa rõ: nhánh 'skipped'→-1 không bao giờ chạy vì không data nào mang 'skipped'.

[6] Quét write point còn lại
    Xảy ra: grep toàn bộ src/ cho phép gán '.status =' và literal 'missed'/'skipped'.
    Kết quả: chỉ [1] và [3] ghi status; 'missed' & 'skipped' chỉ xuất hiện ở type-decl [0], read [4], read [5].
    Độ chắc chắn: cao (12/12 file trong src/ đã đọc)
```

---

## GỢI Ý BƯỚC TIẾP

- State này KHÔNG sạch: có 2 giá trị chết (`'missed'`, `'skipped'`) không có nguồn ghi. Nên `review` luồng vòng đời dose để xác định thiếu transition nào (ai/khi nào chuyển 'pending'→'missed', endpoint nào tạo 'skipped').
- Write point [3] `confirmDose` mở cho mọi user (IDOR) — đáng trace tiếp "ai có thể ghi vào status" ở tầng auth/middleware.
- Chưa có `.ai-understanding/` cho codebase này — chạy `atlas` để lưu flow, lần trace sau khỏi quét lại 12 file.
