# Board — mediremind

Con trỏ: **gd11_delivery** — Delivery Standards xong; nhóm `pg-build` (T-11a Scheduling ∥ T-11b Reminders). T-11a báo xong nhưng CHỜ phiếu checkpoint → giữ `in_progress`; T-11b vẫn `ready`. GĐ12 UAT todo. Còn 2 open-Q chưa đóng: OQ-A (managed queue vs cron), OQ-B (retention/NFR-4).
Ảnh của `progress.json` (nguồn sự thật). Cập nhật: 2026-07-03T14:30:00Z.

## Đang ready / in_progress
- **T-11a** · Sinh Scheduling module theo contract — owner `delivery` ∥ nhóm `pg-build` — 🔵 **in_progress**: báo xong nhưng THIẾU phiếu checkpoint PASS → chưa lật done, chạy `/checkpoint T-11a` trước.
- **T-11b** · Sinh Reminders module theo contract — owner `delivery` ∥ nhóm `pg-build` — 🟢 ready.

## Song song sẵn sàng
- **pg-build** (T-11a ∥ T-11b) — MỞ: cả hai depends_on `T-08` (contract freeze GĐ10) + `T-11` (Delivery Standards) đã done. Đây là điểm fan-out; mỗi agent bám cùng Module Contract. T-11a hiện đang chờ phiếu, T-11b còn chạy được.

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
| T-11a | Sinh Scheduling module | gd11 | 🔵 in_progress (chờ phiếu) | T-08, T-11 | pg-build | delivery | codebase/mediremind/src/scheduling/ |
| T-11b | Sinh Reminders module | gd11 | 🟢 ready | T-08, T-11 | pg-build | delivery | codebase/mediremind/src/reminders/ |
| T-12 | UAT: Test & Verification Report + sign-off | gd12 | ⚪ todo | T-11a, T-11b | — | uat | codebase/uat-report.md |

Chuỗi thẳng T-00→…→T-08 (contract freeze GĐ10) → T-11 (Delivery Standards) rẽ đôi nhóm `pg-build` T-11a ∥ T-11b, rồi hợp nhất ở T-12 (UAT, đang todo). T-11a đã báo xong nhưng bị GIỮ vì thiếu phiếu checkpoint PASS (Định-nghĩa-Xong yêu cầu đủ artifact + phiếu + progress). Còn treo: **OQ-A** (queue vs cron) và **OQ-B** (retention/NFR-4) — chưa artifact nào đóng, phải đóng bằng ADR trước cổng GĐ13.

---

## Nhật ký chạy skill (PLAN + ADVANCE) — 2026-07-03T14:30:00Z

```
═══ ĐÃ CHIA TASK — sau cổng T-11 (Delivery Standards, GĐ11) ═══
Tuần tự: T-08 (contract freeze) → T-11 (Delivery Standards)
Song song (pg-build): T-11a Scheduling ∥ T-11b Reminders  — cùng chờ T-08 + T-11 (đã done)
  - T-11a  owner=delivery  artifact=codebase/mediremind/src/scheduling/  depends_on=[T-08,T-11]
  - T-11b  owner=delivery  artifact=codebase/mediremind/src/reminders/   depends_on=[T-08,T-11]  traces_to=NFR-1
Ready ngay: T-11a, T-11b (cả nhóm pg-build đủ ready → điểm fan-out, chạy /fanout)
════════════════
```

```
═══ ĐÓNG BƯỚC — T-11a ✗ (BỊ GIỮ) ═══
Artifact: codebase/mediremind/src/scheduling/   Phiếu: THIẾU (progress/checkpoints/T-11a.md không tồn tại)
Không lật done: Định-nghĩa-Xong đòi đủ 3 (artifact + phiếu PASS + progress). Mới có báo xong, chưa có phiếu.
Hành động: chạy /checkpoint T-11a — kiểm code trỏ đúng path repo (pointer.md) + test theo test-pyramid + không nới NFR-4 (quyền caregiver + audit-log).
Trạng thái: T-11a giữ in_progress. T-11b vẫn ready. Con trỏ: gd11_delivery (chưa dời — T-12 còn bị chặn bởi T-11a + T-11b).
→ Kế: /checkpoint T-11a  (có phiếu PASS thì gọi lại /progress để lật done)
════════════════
```
