# UAT Sign-off — MediRemind (GĐ12)

> Chủ sở hữu duyệt: **Product Owner (PO)**. `uat` KHÔNG ký thay — phiếu này ở trạng thái **CHỜ**
> cho tới khi PO thật ký. Đây là bằng chứng "nghiệp vụ nghiệm thu slice xác-nhận-liều theo AC-1..5".

## Trạng thái: ⏳ CHỜ KÝ — CHƯA ĐỦ ĐIỀU KIỆN TRÌNH KÝ

## Phạm vi nghiệm thu
Slice **xác-nhận-liều** (AC-1..AC-5) — release ứng viên v1.0 (MVP).

## Bảng nghiệm thu theo AC (PO đánh dấu Chấp nhận / Từ chối khi có kết quả test)

| AC | Điều kiện chấp nhận | Test Result hiện tại | PO chấp nhận? |
|----|---------------------|----------------------|---------------|
| AC-1 | pending→taken, ghi taken_at, adherence tính lại | BLOCKED (chưa có test) | ⬜ chưa xét |
| AC-2 | ghi xác nhận ≤300ms p95 (NFR-2) | BLOCKED (chưa đo p95) | ⬜ chưa xét |
| AC-3 | không xác nhận lại liều đã chốt | BLOCKED (chưa có test) | ⬜ chưa xét |
| AC-4 | chỉ chủ liều xác nhận; caregiver view-only | BLOCKED (chưa có authz test) | ⬜ chưa xét |
| AC-5 | quá hạn → missed, phản ánh adherence | BLOCKED (chưa có test) | ⬜ chưa xét |

## Điều kiện ĐỦ để PO ký (checklist trình ký)
- [ ] AC-1..AC-5 có Test Result thật (PASS), không còn BLOCKED-vì-thiếu-test.
- [ ] Smoke E2E "Patient xác nhận một liều" xanh (bắt buộc theo DoD GĐ11).
- [ ] AC-2 có số p95 thật ≤ 300ms.
- [ ] Không AC blocker nào FAIL (nếu có FAIL: fix→re-test hoặc tách khỏi scope v1.0 — ghi rõ).

**Lý do CHỜ (không phủ định cứng):** slice chưa có tầng test nào để PO dựa vào nghiệm thu → chưa đủ
điều kiện trình ký. Đường đi: dựng test cho AC-1..5 (qua `/review`→`/frame`/`/delivery`) → `/uat`
điền Test Result → trình phiếu này cho PO.

---

Người ký (PO): __________________________  Tên: ____________  Ngày: __________  Chữ ký: __________
