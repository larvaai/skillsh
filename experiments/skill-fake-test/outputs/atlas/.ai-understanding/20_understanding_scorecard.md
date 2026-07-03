# 20 — Understanding Scorecard

> built_at: 2026-07-03T10:26:11Z · built_commit: n/a · scope: partial (bản scaled)

## Level tự chấm: **4 / 5** (Sửa an toàn)

Chấm theo rubric ở atlas-artifacts.md §4, dựa trên chất lượng evidence và độ phủ flow THỰC TẾ — không phải chỉ vì đã tạo file.

## Ba câu hỏi "coi là hiểu" (SKILL.md §Mục tiêu)
1. **Hệ giải quyết bài toán gì?** ✅ Nhắc uống thuốc + theo dõi tuân thủ (Schedule → DoseEvent → Reminder → adherence). Evidence: 01_project_intake.
2. **Một hành vi thật đi từ đâu đến đâu?** ✅ Đã trace 4 flow end-to-end (generate/dispatch/confirm/rate). Evidence: 09_flow_traces/*.
3. **Sửa một chỗ thì gì vỡ?** ✅ Đã lập risks + side-effects + permission; biết BUG-5/3/4 là chặn go-live. Evidence: 12, 14, 18.

## Checklist artifact theo level
| Level | Artifact cần | Có? |
|---|---|---|
| 1 Bề mặt | 01, 02, 05 | ✅ |
| 2 Cấu trúc | 04, 11(gộp), 07 | ✅ (11 gộp trong 04/05) |
| 3 Flow | 09 (≥1 happy/failure/side-effect/permission), 08, 12, 13, 14 | ✅ 09 đủ 4 loại; 12,14 done; 08 partial; 13 scaled-out (tóm trong flow+risks) |
| 4 Sửa an toàn | 15, 17, 18 | ✅ 15 done, 18 done, 17 gộp (ngắn) |
| 5 Maintainer | decision notes, refactor candidates, prod debug map | ❌ chưa (không sinh ở bản scaled) |

## Vì sao 4 chứ không 5
- Đã đủ để **sửa code an toàn** (biết impact, risk, test-gap của mọi flow chính).
- CHƯA đạt 5 vì: (a) không dựng architecture-decision-notes/refactor-candidates/prod-debug-map; (b) nhiều unknown NGOÀI fixture (framework, wiring cron, middleware auth, Postgres schema) khiến chưa hiểu trade-off vận hành thật. Đây là giới hạn của fixture (slice cắt gọn), không phải chưa đọc kỹ.

## Vì sao không thấp hơn 4
- Không hạ xuống 3: đã có 15_test_map + 18_risks + impact (điều kiện level 4), và mọi claim có evidence file·symbol·dòng.
- Điểm mạnh nhất: 4 flow trace bám đúng call chain và chỉ ra chính xác 7 bug + dead code với evidence dòng.

## Lưu ý bản scaled
Đây là bản ĐẠI DIỆN: 8 artifact nội dung + 4 flow + index + scorecard, thay vì đủ 20. Các artifact 03/10/13/16/19 đánh dấu `todo (scaled-out)` trong 00_index. Nếu chạy full trên repo thật (có git + config + test) sẽ sinh nốt và có thể nâng độ chắc chắn nhiều unknown hiện tại.

Evidence tổng: 12/12 file đã đọc; grep xác nhận dead code + caller-less guard; mọi BUG map về file·dòng.
