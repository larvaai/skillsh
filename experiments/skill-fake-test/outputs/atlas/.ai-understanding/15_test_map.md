# 15 — Test Map

> built_at: 2026-07-03T10:26:11Z · built_commit: n/a · scope: partial (bản scaled)

## Test types found
**KHÔNG CÓ.** `find . -type f` chỉ ra 12 file .ts, không file nào là *.test.ts / *.spec.ts, không thư mục __tests__/test/e2e.

Evidence:
- File path: toàn bộ src/ (12 file, đã liệt kê ở 00_index); không match test pattern
- Mức chắc chắn: chắc chắn

| Module | Test files | What is covered | What is missing | Risk |
|---|---|---|---|---|
| scheduling | (không) | – | daysOfWeek filter, start/end-date, timezone, idempotency | cao |
| reminders | (không) | – | dedupe, partial-failure isolation, window boundary | cao |
| adherence | (không) | – | chia-0, phân loại mẫu số, IDOR ownership | cao |
| identity | (không) | – | canCaregiverView scope, có gắn vào route không | trung bình |
| streak | (không) | – | ranh giới chuỗi ngày, ngày rỗng | trung bình |

## How to run tests
KHÔNG xác định được — không có package.json/script/test runner trong fixture. (đẩy xuống 18)

## Critical untested paths (ưu tiên viết test)
1. **Permission (IDOR)** — confirmDose ownership (BUG-5).
2. **Dedupe reminder** (BUG-3) + **partial failure** (BUG-4).
3. **Adherence divide-by-zero + phân loại** (BUG-6, BUG-7).
4. **Timezone + end-date generator** (BUG-1, BUG-2).

Kết luận: độ phủ test = 0. Mọi flow trong 09 hiện KHÔNG được bất kỳ test nào bảo vệ. Đây là chặn go-live.
