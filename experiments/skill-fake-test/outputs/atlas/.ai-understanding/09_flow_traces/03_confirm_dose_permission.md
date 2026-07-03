# Flow Trace: Xác nhận đã uống (PERMISSION / SECURITY PATH)

## User-visible behavior
Bệnh nhân bấm "Đã uống" trên một liều → liều chuyển 'taken', trả về tỉ lệ tuân thủ mới.

## Trigger
HTTP POST /doses/:id/confirm → `confirmDose(req)` (dose.controller.ts:10). `req.userId` do middleware auth cấp.

## Step-by-step code path
1. **dose.controller.ts:11** — `db.doseEvents.find(e => e.id === req.params.id)` — tìm liều theo **id** (chỉ id, KHÔNG kèm userId).
2. **:12** — nếu không thấy → 404.
3. **:16-17** — set `dose.status='taken'`, `dose.takenAt=new Date()`.
4. **:19** — `adherence.rateFor(dose.userId)` (không phải req.userId!) → tính lại tỉ lệ.
5. **:20** — trả 200 { id, status, adherenceRate }.

## Side effects
- Mutate `dose.status`, `dose.takenAt` (DB write).

## Failure / security paths
- **BUG-5 (IDOR)**: bước 1-3 KHÔNG kiểm `dose.userId === req.userId`. Bất kỳ user đăng nhập nào biết/đoán được id liều đều xác nhận được liều của người khác. id lại **đoán được** vì ghép `${scheduleId}-${YYYY-MM-DD}-${HH:MM}` (dose-generator.service.ts:29) → enumerable. Đây là lỗ hổng nghiêm trọng nhất của hệ.
  - Evidence: dose.controller.ts:14 comment "BUG-5 (IDOR / permission)"; id format ở dose-generator.service.ts:29.
- Nếu `adherence.rateFor` chạy với user chưa có dose → NaN (BUG-6) rò rỉ vào response.

## Tests covering this flow
KHÔNG có. Critical untested: ownership check (chưa tồn tại nên chưa test được), 404 path, NaN trong response.

## Evidence
- File path/Symbol: dose.controller.ts:10 confirmDose, :11 find, :16 mutate
- Mức chắc chắn: chắc chắn
