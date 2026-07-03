# Review — Rà soát gap: MediRemind (scheduling / reminders / adherence / identity)

PHẠM VI: 4 module — `src/scheduling`, `src/reminders`, `src/adherence`, `src/identity` (+ phụ thuộc `src/common`)
CHẾ ĐỘ: tổng thể (edge → error → permission)
NGỮ CẢNH: rà trước khi build tiếp; chưa có `.ai-understanding/` nên đọc thẳng từ file gốc (gợi ý chạy `atlas` sau).
NGUYÊN TẮC: chỉ báo gap, KHÔNG đề xuất/không viết fix. Đóng khung lát cắt fix là việc của `frame`.

---

## GAP TÌM ĐƯỢC

### [Critical]

- **`adherence/dose.controller.ts` · `confirmDose` · dòng 10–20** — Thiếu kiểm quyền sở hữu: không có `dose.userId === req.userId`. → **IDOR**: bất kỳ user đã đăng nhập nào cũng gọi `POST /doses/:id/confirm` với `id` bất kỳ để xác nhận liều của bệnh nhân khác, làm sai lệch dữ liệu y tế + adherence của người khác. Đây là lỗ hổng permission nghiêm trọng nhất trong slice.

- **`reminders/reminder.service.ts` · `dispatchDue` · dòng 21** — Không có bảo vệ lỗi quanh `await pushProvider.send(...)`. `pushProvider.send` có thể `throw` (provider timeout/lỗi, hoặc `userId` rỗng — xem `common/providers.ts` dòng 5). → Một dose lỗi làm **vỡ cả vòng lặp**; mọi dose còn lại trong `due` KHÔNG được gửi reminder trong lượt đó, không retry, không log. Với app nhắc uống thuốc, đây là mất liều nhắc → hậu quả sức khỏe.

- **`reminders/reminder.service.ts` · `dispatchDue` · dòng 11–24** — Không dedupe: không kiểm liều đã được gửi reminder chưa (bảng `db.reminders` có nhưng không được đọc lại). Worker chạy **mỗi phút** với `windowMinutes = 5` (dòng 9) → mỗi liều rơi vào cửa sổ 5 lần → **gửi lặp tới 5 push cho cùng một liều**. Người bệnh bị spam, mất tin cậy vào nhắc nhở.

- **`adherence/adherence.service.ts` · `rateFor` · dòng 9–18** — Chia cho 0: user chưa có `DoseEvent` nào → `events.length === 0` → `taken / 0 = NaN`. → `rateFor` được gọi trực tiếp trong `confirmDose` (dose.controller dòng 19) và trả thẳng ra response body → **API trả `adherenceRate: NaN`** (serialize JSON thành `null` hoặc lỗi tuỳ serializer). Case này chắc chắn xảy ra với user mới.

### [Medium]

- **`scheduling/dose-generator.service.ts` · `generateForDay` · dòng 17, 26–27** — Bỏ qua timezone: `day.getDay()` và `setHours(hh, mm)` chạy theo giờ **server**, không quy về `s.timezone` (field đã tồn tại ở `schedule.entity.ts` dòng 9 nhưng chưa dùng). → User ở timezone khác server nhận liều lệch giờ local; ở biên ngày (VD 23:00–01:00) còn có thể lệch cả `weekday` → sinh liều sai ngày hoặc thiếu/thừa ngày.

- **`scheduling/dose-generator.service.ts` · `generateForDay` · dòng 22** — Chỉ chặn `startDate`, KHÔNG lọc `endDate`. `Schedule.endDate` tồn tại (entity dòng 8) nhưng generator không dùng. → Lịch đã **hết hạn** (thuốc đã ngưng, `endDate` trong quá khứ) vẫn tiếp tục sinh liều mỗi ngày → nhắc uống thuốc đã ngừng: sai về mặt y tế.

- **`scheduling/dose-generator.service.ts` · `generateForDay` · dòng 28–36, 39** — Không idempotent: chạy `generateForDay` hai lần cho cùng user+ngày sẽ push trùng event vào `db.doseEvents` (id trùng nhưng không có kiểm tồn tại/upsert). `nightlyGenerate` (reminder.worker dòng 9–13) nếu bị chạy lại (retry cron, restart) → **nhân đôi liều** → nhân đôi reminder + sai adherence. Edge: cron chạy lặp là tình huống vận hành thường gặp.

- **`adherence/adherence.service.ts` · `rateFor` · dòng 14–16** — Mẫu số tính sai về mặt định nghĩa: `denominator = events.length` gồm **cả `skipped`** (liều user chủ động bỏ — không nên tính là trượt) và **cả `pending`** (chưa tới giờ, chưa thể taken). → Adherence rate bị kéo tụt sai; user mới có nhiều `pending` sẽ thấy tỉ lệ thấp giả tạo. Đây là gap logic domain, không crash.

- **`adherence/dose.controller.ts` · `confirmDose` · dòng 16–17** — Không kiểm trạng thái/thời gian trước khi lật `taken`: liều đã `taken`/`missed`/`skipped` vẫn bị ghi đè `taken` + cập nhật `takenAt`; liều `pending` ở **tương lai** (chưa tới giờ) cũng xác nhận được. → Cho phép "uống trước" phi lý và ghi đè lịch sử; mất tính toàn vẹn dữ liệu tuân thủ.

- **`identity/caregiver.guard.ts` · `canCaregiverView` — KHÔNG được gọi ở bất kỳ đâu** — `grep` toàn slice: hàm chỉ được định nghĩa, không route/controller nào gọi. → Guard "caregiver chỉ view-only" **chưa được gắn vào luồng nào**; nếu có route báo cáo adherence cho caregiver (adherence rate là dữ liệu nhạy cảm) thì hiện chưa có chốt chặn. Gap permission ở tầng "check đúng chỗ chưa".

### [Low]

- **`scheduling/dose-generator.service.ts` · dòng 25** — `t.split(':').map(Number)` không phòng thủ input xấu: `timesOfDay` chứa chuỗi sai định dạng (`"8"`, `"25:00"`, `""`) → `hh/mm` là `NaN` hoặc quá biên; `setHours(NaN, ...)` cho `Invalid Date`, event vẫn được push với `scheduledTime` hỏng. Không validate lúc nhập lịch.

- **`reminders/reminder.service.ts` · dòng 12** — Cửa sổ due dùng `>= now` (bao gồm chính `now`) và không xử lý liều **đã quá hạn** (`scheduledTime < now`, vẫn `pending`): liều bị bỏ lỡ do worker gián đoạn (downtime) sẽ **không bao giờ** được nhắc lại vì rơi ra ngoài cửa sổ `[now, now+5m]`. → Mất nhắc âm thầm sau downtime.

- **`adherence/streak.ts` · `currentStreak` · dòng 4–18** — Không xử lý ngày **không có** dose event (gap ngày): `days` chỉ gồm các ngày có event; nếu bỏ hẳn một ngày (không có liều nào) thì ngày đó biến mất khỏi chuỗi thay vì cắt streak. Ngoài ra ngày `pending` (chưa tới giờ, giá trị 0) làm `ok=false` → streak bị cắt oan bởi ngày hiện tại chưa hoàn tất. Edge case định nghĩa streak.

- **`reminders/reminder.service.ts` · dòng 22 & `common/db.ts` dòng 9** — Kênh log cứng `channel: 'push'` trong khi type db cho phép `'push' | 'sms'`; không có nhánh sms/fallback khi push fail. Inconsistency nhỏ, chưa gây lỗi.

---

## CÓ THỂ LÀ GAP (chưa chắc — cần xác nhận thêm)

- **`scheduling/dose-generator.service.ts` · dòng 10–11** — `generateForDay` nhận `userId` và filter `db.schedules` theo user; nhưng không thấy tầng nào kiểm caller được phép sinh liều cho `userId` đó. Trong slice, hàm chỉ gọi từ cron nội bộ (`nightlyGenerate`) nên có thể an toàn. · Cần xác nhận: có route nào expose generator ra ngoài cho client gọi kèm `userId` tuỳ ý không? Nếu có → thành gap permission.

- **`identity/caregiver.guard.ts` · dòng 11** — Chỉ chấp nhận `scope === 'view-only'`; `scope` là `string` tự do (db.ts dòng 9). · Cần xác nhận: tập giá trị scope hợp lệ (có `'full'`/`'manage'` không?). Nếu có scope cao hơn view-only mà vẫn cần xem được, guard này sẽ **từ chối nhầm** caregiver hợp lệ (false-deny).

- **`reminders/reminder.worker.ts` · dòng 10, 17** — `nightlyGenerate` và `everyMinute` là async nhưng không thấy nơi bắt lỗi khi Promise reject (cron runner không rõ trong slice). · Cần xác nhận: cron runner có nuốt lỗi âm thầm không? Nếu có → lỗi generate/dispatch mất dấu, không alert.

---

## KHÔNG TÌM THẤY GAP (đã kiểm, thấy ổn trong phạm vi slice)

- `scheduling/schedule.entity.ts`, `scheduling/dose-event.entity.ts` — chỉ là interface/type; định nghĩa rõ ràng, không có logic để hở. (Lưu ý: các field `timezone`/`endDate` đã khai báo nhưng chưa được consumer dùng — đã tính vào gap ở generator, không phải lỗi của entity.)
- `reminders/reminder.worker.ts` · dòng 11 — dedupe user bằng `new Set(...)` trước khi generate: đúng, không sinh trùng theo user.
- `adherence/dose.controller.ts` · dòng 11–12 — nhánh 404 khi không tìm thấy dose: có xử lý, đúng.

---

## Bước tiếp theo (gợi ý, KHÔNG tự làm)

Có 4 gap **Critical** (IDOR ở `confirmDose`; vỡ vòng lặp khi push lỗi; gửi reminder trùng ×5; chia-cho-0 ra `NaN`). Đề xuất đóng khung lát cắt fix theo thứ tự ưu tiên bằng skill **`frame`** — mỗi lát cắt một gap, bắt đầu từ IDOR (rủi ro dữ liệu y tế + quyền riêng tư cao nhất). Review này chỉ báo cáo; việc quyết scope và viết code thuộc `frame`.
