# ANSWER KEY — chỉ dành cho GRADER, KHÔNG đưa cho test-agent

Đo "hiệu quả" của skill = recall các khuyết tật/gap CÀI SẴN dưới đây.

## A. Khuyết tật code (cho `review`, một phần cho `trace`/`triage`)
| ID | File | Loại | Mô tả |
|----|------|------|-------|
| BUG-1 | scheduling/dose-generator.service.ts | timezone | Dùng giờ server (`day.getDay()`, `setHours`) không quy về `s.timezone` → user timezone khác nhận liều sai giờ local. |
| BUG-2 | scheduling/dose-generator.service.ts | logic/date | Không lọc `endDate` → schedule đã hết hạn vẫn sinh liều. |
| BUG-3 | reminders/reminder.service.ts | dedupe | Không kiểm reminder đã gửi → mỗi liều bị gửi lặp (~5 lần do window 5' × cron 1'). |
| BUG-4 | reminders/reminder.service.ts | error path | `pushProvider.send` throw → vỡ vòng lặp, các dose còn lại không gửi, không retry. |
| BUG-5 | adherence/dose.controller.ts | permission/IDOR | Không kiểm `dose.userId === req.userId` → user xác nhận liều người khác. (nghiêm trọng nhất) |
| BUG-6 | adherence/adherence.service.ts | divide-by-zero | `events.length === 0` → `taken/0 = NaN`. |
| BUG-7 | adherence/adherence.service.ts | logic | Mẫu số gồm cả `skipped` và `pending` → rate sai (kéo tụt). |

**Chuẩn review:** tốt = bắt ≥5/7, BẮT BUỘC có BUG-5 (permission) trong nhóm Critical. Bỏ BUG-5 = kém.

## B. Trace (đối tượng: `status` của một DoseEvent, hoặc `adherenceRate`)
Đường đi đúng cho `status`: sinh 'pending' ở `dose-generator.service.ts` → đọc để lọc 'due' ở
`reminder.service.ts` → ghi 'taken' ở `dose.controller.ts:confirmDose` → đọc lại ở
`adherence.service.ts:rateFor`. Điểm side-effect: mutate `dose.status`/`takenAt` in-place trên `db`
(shared in-memory), đồng thời `db.reminders.push`. Trace tốt phải nêu mutate in-place + shared db.

## C. Triage (file: src/legacy/old_reminder_cron.ts)
Verdict đúng ≈ **xoá** (hoặc archive): không được import ở đâu (grep 0 caller), đã bị thay bởi
`reminders/reminder.worker.ts`, dùng setInterval toàn cục, không test. Triage tốt phải grep caller
và thấy 0 → verdict xoá/archive, KHÔNG "giữ".

## D. Traceability (gap pipeline — khớp BIBLE mục 12)
Phải báo: G-1 thiếu `uat.md` (GĐ12) · G-2 ship chưa 2 chữ ký · G-3 hai open-Q chưa đóng
(OQ-A queue/cron, OQ-B retention) · G-4 rollback chưa test. Traceability tốt = bắt ≥3/4, buộc có G-1.

## E. Grade (chấm bản explain lỗi ở fixture/flawed-explain.md)
Bản explain đó CỐ Ý lỗi:
- Nhảy thẳng jargon "orchestrator/idempotent/DAG" không neo (rớt tiêu chí Lời-văn / 3-tầng).
- BỊA: nói có "Kafka event bus" và "microservice Notification riêng" — code KHÔNG hề có
  (modular monolith, không Kafka) → rớt tiêu chí Bám-code.
- Không có phần "vấn đề trước / cho ai".
Grade tốt = **RỚT GATE**, chỉ ra đúng: rớt Bám-code (bịa Kafka/microservice) + rớt Lời-văn/3-tầng.
Grade kém = cho điểm cao hoặc không bắt phần bịa.

## F. Skills không có answer-key cứng (chấm theo rubric/contract của chính skill)
shape, stack, backlog, modules, delivery, uat, ship, operate, skeleton, idea, explain(bản đúng),
teen, atlas, frame, charter, checkpoint, progress, resume, fanout, partner, spar, skill-define, tune.
