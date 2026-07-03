# Flow Trace: Tính tỉ lệ tuân thủ (FAILURE / EDGE-CASE PATH)

## User-visible behavior
Ứng dụng hiển thị "bạn đã uống đúng X% số liều".

## Trigger
Gọi từ `confirmDose` (dose.controller.ts:19) sau khi xác nhận, hoặc route báo cáo (không thấy caller khác trong fixture).

## Step-by-step code path
1. **adherence.service.ts:9** — `events = db.doseEvents.filter(e => e.userId === userId)`.
2. **:12** — `taken = events.filter(status==='taken').length`.
3. **:16** — `denominator = events.length`.
4. **:18** — `return taken / denominator`.

## Side effects
Không (read-only).

## Failure / edge-case paths
- **BUG-6 (chia cho 0)**: user chưa có DoseEvent nào → `events.length === 0` → `taken/0 = NaN`. NaN này chảy thẳng vào response confirmDose (adherenceRate: NaN) → serialize JSON thành `null`, UI hiển thị sai.
  - Evidence: adherence.service.ts:11 comment + :18.
- **BUG-7 (đếm không nhất quán)**: mẫu số `events.length` gồm CẢ `skipped` (user chủ động bỏ — không nên tính là trượt) và CẢ `pending` (chưa tới giờ). → tỉ lệ bị kéo tụt sai lệch. Đúng ra mẫu số nên là các liều "đáng lẽ đã uống" = taken + missed (± tùy định nghĩa nghiệp vụ), loại pending & skipped.
  - Evidence: adherence.service.ts:14-16 comment + :16.

## Tests covering this flow
KHÔNG có. Critical untested: empty user (chia 0), phân loại mẫu số (skipped/pending), giá trị biên 0% và 100%.

## Evidence
- File path/Symbol: adherence.service.ts:8 rateFor, :16 denominator, :18 return
- Mức chắc chắn: chắc chắn
