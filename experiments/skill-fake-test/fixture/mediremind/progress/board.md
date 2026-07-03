# Board — mediremind

Con trỏ: **gd11_delivery** — Delivery Standards xong; nhóm `pg-build` (T-11a Scheduling ∥ T-11b Reminders) READY, chạy `/fanout`; GĐ12 UAT todo. Còn 2 open-Q chưa đóng: OQ-A (managed queue vs cron), OQ-B (retention/NFR-4).
Ảnh của `progress.json` (nguồn sự thật). Cập nhật: 2026-07-03.

## Đang ready / in_progress
- **T-11a** · Sinh Scheduling module theo contract — owner `delivery` ∥ nhóm `pg-build`
- **T-11b** · Sinh Reminders module theo contract — owner `delivery` ∥ nhóm `pg-build`

## Song song sẵn sàng
- **pg-build** (T-11a ∥ T-11b) — MỞ: cả hai depends_on `T-08` (contract freeze GĐ10) + `T-11` (Delivery Standards) đã done. Bung `/fanout`, mỗi agent bám cùng Module Contract.

## Toàn đồ thị
| id | việc | giai đoạn | trạng thái | phụ thuộc | nhóm ∥ | owner | artifact |
|---|---|---|---|---|---|---|---|
| T-00 | Idea Brief | gd0 | ✅ done | — | — | idea | idea/mediremind.md |
| T-01 | Business Case + SM-1/SM-2 | gd1 | ✅ done | T-00 | — | idea | problem/business-case.md |
| T-02 | Product/Req/PRD (NFR-1..5) | gd2–4 | ✅ done | T-01 | — | idea | problem/prd.md |
| T-03 | Domain Model | gd5 | ✅ done | T-02 | — | idea | docs/domain-model.md |
| T-04 | Architecture (modular monolith, C4) | gd6 | ✅ done | T-03 | — | shape | docs/architecture.md |
| T-05 | Tech Decision Matrix | gd7 | ✅ done | T-04 | — | stack | docs/tech-decision.md |
| T-06 | Live Slice (xác nhận một liều) | gd8 | ✅ done | T-05 | — | skeleton | codebase/live-slice-report.md |
| T-07 | Roadmap + Backlog | gd9 | ✅ done | T-06 | — | backlog | docs/roadmap.md |
| T-08 | **Module Map + Contracts** (freeze cổng ∥) | gd10 | ✅ done | T-07 | — | modules | docs/contracts/module-contract-v1.md |
| T-11 | Delivery Standards + DoD + PR Checklist | gd11 | ✅ done | T-08 | — | delivery | codebase/delivery-standards.md |
| T-11a | Sinh Scheduling module | gd11 | 🟢 ready | T-08, T-11 | pg-build | delivery | codebase/mediremind/src/scheduling/ |
| T-11b | Sinh Reminders module | gd11 | 🟢 ready | T-08, T-11 | pg-build | delivery | codebase/mediremind/src/reminders/ |
| T-12 | UAT: Test & Verification Report + sign-off | gd12 | ⚪ todo | T-11a, T-11b | — | uat | codebase/uat-report.md |

Chuỗi thẳng T-00→…→T-08 (contract freeze GĐ10) → T-11 (Delivery Standards) rẽ đôi nhóm `pg-build` T-11a ∥ T-11b (chạy `/fanout`), rồi hợp nhất ở T-12 (UAT, đang todo). Còn treo: **OQ-A** (queue vs cron) và **OQ-B** (retention/NFR-4) — chưa artifact nào đóng, phải đóng bằng ADR trước cổng GĐ13.
