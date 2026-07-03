# Board — multi-lens-chat

Con trỏ: **gd2_4_product_prd** — chờ chốt OQ-4/5/6 rồi qua Domain.
Ảnh của `progress.json` (nguồn sự thật). Cập nhật: 2026-07-03.

## Đang ready / in_progress
- **T-02** · Chốt PRD + MVP (đóng OQ-4/5/6) — owner `idea` → chạy `/idea`

## Song song sẵn sàng
- Chưa. Nhóm `pg-lens-workers` (T-07 ∥ T-08) chỉ mở sau khi **T-06 freeze contract** có phiếu PASS.

## Toàn đồ thị
| id | việc | giai đoạn | trạng thái | phụ thuộc | nhóm ∥ | owner | artifact |
|---|---|---|---|---|---|---|---|
| T-01 | Business Need + Case | gd1 | ✅ done | — | — | idea | problem/business-case.md |
| T-02 | Chốt PRD + MVP | gd2–4 | 🔵 in_progress | T-01 | — | idea | problem/prd.md |
| T-03 | Domain Model | gd5 | ⚪ todo | T-02 | — | idea | docs/domain-model.md |
| T-04 | Kiến trúc orchestrator+worker | gd6 | ⚪ todo | T-03 | — | shape | docs/architecture.md |
| T-05 | Chọn stack | gd7 | ⚪ todo | T-04 | — | stack | docs/tech-decision.md |
| T-06 | **Freeze contract** (cổng ∥) | gd10 | ⚪ todo | T-05 | — | modules | docs/contracts/worker-v1.md |
| T-07 | Build lens workers | gd11 | ⚪ todo | T-06 | pg-lens-workers | delivery | codebase/workers/ |
| T-08 | Build orchestrator | gd11 | ⚪ todo | T-06 | pg-lens-workers | delivery | codebase/orchestrator/ |
| T-09 | Tích hợp end-to-end | gd11 | ⚪ todo | T-07, T-08 | — | frame | codebase/integration.md |

Chuỗi phụ thuộc thẳng T-02→…→T-06, tới T-06 (contract freeze) rẽ đôi T-07 ∥ T-08 (chạy `/fanout`), rồi hợp nhất ở T-09. Live slice (GĐ8) + backlog (GĐ9) gộp gọn vào chuỗi này cho dễ đọc; mở đủ khi tới đó.
