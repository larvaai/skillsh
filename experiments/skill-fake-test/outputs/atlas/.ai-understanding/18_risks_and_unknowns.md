# 18 — Risks & Unknowns

> built_at: 2026-07-03T10:26:11Z · built_commit: n/a · scope: partial (bản scaled)

## Risks (observed — có evidence trong code)
| # | Risk | Area | Severity | Evidence |
|---|---|---|---|---|
| BUG-5 | IDOR: confirmDose không kiểm ownership → xác nhận liều người khác; id lại đoán được | security/adherence | **NGHIÊM TRỌNG** | dose.controller.ts:14 (comment), :11 (find theo id); id format dose-generator.service.ts:29 |
| BUG-3 | Reminder không dedupe → gửi trùng tới 5 lần/liều | reminders | cao | reminder.service.ts:17 (comment), :12 (status không đổi sau gửi) |
| BUG-4 | pushProvider.send throw → vỡ cả vòng lặp, dose sau không gửi, không retry | reminders | cao | reminder.service.ts:19-21; providers.ts:5 (throw) |
| BUG-7 | Adherence tính mẫu số gồm cả skipped + pending → tỉ lệ sai | adherence | cao | adherence.service.ts:14-16 (comment) |
| BUG-6 | Adherence chia cho 0 → NaN rò vào response | adherence | trung bình | adherence.service.ts:11 (comment), :18 |
| BUG-1 | Generator dùng giờ server, bỏ qua Schedule.timezone → liều lệch giờ local | scheduling | cao | dose-generator.service.ts:15-17,27; schedule.entity.ts:9 |
| BUG-2 | Generator không lọc endDate → schedule hết hạn vẫn sinh liều | scheduling | cao | dose-generator.service.ts:20-22 |
| DEAD | legacy/old_reminder_cron.ts là dead code (0 caller) — nợ dọn dẹp, dùng setInterval global | legacy | thấp | grep 0 import; file comment "Không còn được import" |
| ARCH | Service/controller chạm db global trực tiếp, không repository, không transaction | architecture | trung bình | dose-generator.service.ts:39, dose.controller.ts:16 |

Tất cả 7 BUG-* được chú thích tường minh trong code (đây là fixture có bug cấy sẵn) → mức chắc chắn: **chắc chắn**.

## Unknowns (chưa đủ căn cứ — KHÔNG ghi như fact)
| Unknown | Why it matters | How to verify | Priority |
|---|---|---|---|
| Framework/runtime thật (Express? Nest? cron lib nào) | quyết định cách wire route/scheduler & middleware auth | tìm package.json + file boot ngoài fixture | cao |
| Nơi đăng ký cron (nightlyGenerate/everyMinute) | không chắc cron thật chạy | tìm scheduler registration | cao |
| Middleware auth cấp req.userId ở đâu | nền của mọi phân quyền | tìm middleware chain | cao |
| `canCaregiverView` có được gắn vào route nào không | nếu chưa → route caregiver có thể hở | grep caller ngoài fixture | cao |
| Postgres schema / migration | in-memory db chỉ là demo | tìm migration/ORM entity ngoài fixture | trung bình |
| Env/config, deploy | vận hành | tìm .env.example, docker, CI | thấp |

## Assumptions đang giả định (gắn nhãn rõ)
- Giả định có middleware auth cung cấp `req.userId` (dựa comment, không thấy code).
- Giả định cron được đăng ký ở tầng ngoài fixture.
- Giả định "thật sẽ là Postgres" (theo comment db.ts) — chưa có schema thực.

## Things not yet inspected
- Không có gì bị bỏ sót TRONG fixture (đã đọc cả 12 file). Phần thiếu nằm NGOÀI fixture (boot/config/test/auth) — fixture cố tình cắt gọn còn slice logic.
