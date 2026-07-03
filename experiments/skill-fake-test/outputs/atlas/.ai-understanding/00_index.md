# .ai-understanding — Index

> built_at: 2026-07-03T10:26:11Z · built_commit: n/a (không phải git repo)
> project: /Users/uspro/Desktop/skillsh/experiments/skill-fake-test/fixture/codebase/mediremind
> understanding level (agent): 4 (xem 20_understanding_scorecard.md)

> ⚠️ **BẢN SCALED (đại diện)** — codebase nhỏ (12 file TS, 6 module). Theo yêu cầu kiểm skill, KHÔNG sinh đủ bộ 20 artifact mà chỉ sinh mẫu đại diện: `00_index` + `20_understanding_scorecard` + 8 artifact nội dung + 4 flow trace. Các artifact còn lại (03/10/13/16/19...) được đánh dấu `todo (scaled-out)` bên dưới — nếu chạy full sẽ sinh nốt. Mỗi claim trong bản này đều kèm evidence.

## Artifacts
| # | Artifact | Status | Ghi chú |
|---|---|---|---|
| 01 | project_intake | done | MediRemind — hệ nhắc uống thuốc |
| 02 | entrypoints_map | done | 2 cron + 1 HTTP handler + 2 guard fn |
| 03 | config_env_map | todo (scaled-out) | Không có .env/package.json trong fixture; db in-memory |
| 04 | architecture_map | done | Feature-based layered, có vi phạm |
| 05 | module_inventory | done | 6 module: scheduling/reminders/adherence/identity/common/legacy |
| 06 | domain_model | done | Schedule · DoseEvent · Reminder · CaregiverLink |
| 07 | data_model | done | in-memory db (common/db.ts), thật sẽ là Postgres |
| 08 | api_contracts | done (partial) | 1 HTTP route + service methods |
| 09 | flow_traces/ | done | 4 flow: generate(happy) · dispatch(side-effect) · confirm(permission) · rate(failure) |
| 10 | state_and_lifecycle | todo (scaled-out) | DoseStatus: pending→taken/missed/skipped |
| 11 | dependency_graph | done (gọn) | trong architecture_map + module_inventory |
| 12 | side_effects_map | done | push send, db write, không log/metric |
| 13 | error_handling_map | todo (scaled-out) | tóm trong risks + flow dispatch |
| 14 | security_permission_map | done | IDOR ở confirmDose, guard caregiver |
| 15 | test_map | done (ngắn) | KHÔNG có test nào — mọi flow chưa được bảo vệ |
| 16 | observability_map | todo (scaled-out) | không logger/metric/trace (chỉ 1 console.log ở legacy) |
| 17 | change_impact_map | done (ngắn) | trong risks + module_inventory |
| 18 | risks_and_unknowns | done | 7 bug đã đánh dấu + dead code + unknowns |
| 19 | glossary | todo (scaled-out) | Dose vs Reminder, taken vs skipped vs missed |
| 20 | understanding_scorecard | done | tự chấm level 4 |

## Cách tái dùng
overview/flow/why và các skill khác (explain/frame/triage/partner) đọc folder này TRƯỚC khi quét code.
Đọc `99_changes.md` trước để biết artifact nào đang stale (có pending).
Chạy lại `/atlas` chỉ khi cần refresh (pending quá nhiều / thay đổi lớn), hoặc để sinh nốt các artifact `scaled-out` ở trên.

## 3 rủi ro lớn nhất (chi tiết ở 18)
1. **IDOR** ở `confirmDose` — bất kỳ user đăng nhập nào cũng xác nhận được liều người khác (BUG-5).
2. **Reminder gửi trùng 5 lần/liều + vỡ vòng lặp khi provider throw** (BUG-3, BUG-4) — không dedupe, không retry.
3. **0 test** — mọi flow (kể cả permission, tính adherence, dedupe) không được bảo vệ.
