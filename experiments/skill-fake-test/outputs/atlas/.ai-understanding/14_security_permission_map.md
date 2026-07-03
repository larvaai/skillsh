# 14 — Security & Permission Map

> built_at: 2026-07-03T10:26:11Z · built_commit: n/a · scope: partial (bản scaled)

## Authentication
Danh tính user đến từ middleware auth phía ngoài — `confirmDose` nhận `req.userId` đã xác thực. Bản thân fixture KHÔNG chứa middleware auth (chỉ giả định có).

Evidence:
- File path: dose.controller.ts:8 (comment "req.userId đến từ middleware auth (đã xác thực danh tính)"), :10 (`req: { params, userId }`)
- Mức chắc chắn: một phần (middleware thật không có trong fixture → đẩy xuống 18)

## Authorization
- **Caregiver**: chỉ được XEM nếu có `CaregiverLink` scope `view-only`. Kiểm bằng `canCaregiverView`.
  - Evidence: caregiver.guard.ts:7-12. Mức: chắc chắn. NHƯNG: grep không ra caller → guard này CHƯA được gắn vào route nào trong fixture (risk: có thể route caregiver chưa được bảo vệ).
- **Patient confirm dose**: KHÔNG có ownership check → lỗ hổng.

## Sensitive operations
| Operation | Required permission | Code location | Risk |
|---|---|---|---|
| confirmDose (đổi status liều) | phải là chủ liều (dose.userId === req.userId) | dose.controller.ts:10-21 | **NGHIÊM TRỌNG — BUG-5 IDOR**: không check → mọi user đăng nhập xác nhận được liều người khác |
| xem adherence của patient | caregiver view-only link | caregiver.guard.ts | guard tồn tại nhưng chưa thấy được gọi ở route nào |
| gửi push | (nội bộ, cron) | reminder.service.ts | không permission — chạy dưới cron |

Evidence:
- File path/Symbol: dose.controller.ts:14 (comment "BUG-5 (IDOR / permission): KHÔNG kiểm dose.userId === req.userId")
- Mức chắc chắn: chắc chắn (bug được chú thích tường minh)

## Data isolation
Ranh giới per-user dựa trên `userId` field. NHƯNG confirmDose phá ranh giới này (IDOR). db in-memory global không có tầng row-level nào; isolation hoàn toàn phụ thuộc code check thủ công — mà chỗ quan trọng nhất (confirm) lại thiếu.

Evidence: dose.controller.ts:11 (`find(e => e.id === req.params.id)` — chỉ theo id, bỏ qua userId). Mức: chắc chắn.

## Kết luận bảo mật
Trục yếu nhất của hệ là **authorization ở confirmDose (IDOR)** + **guard caregiver chưa được wire**. Trước khi go-live phải: (1) thêm ownership check ở confirmDose, (2) xác minh route caregiver có gọi guard.
