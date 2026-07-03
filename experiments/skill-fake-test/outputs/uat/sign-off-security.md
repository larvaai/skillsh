# Security Sign-off — MediRemind (GĐ12)

> Chủ sở hữu duyệt: **Security / CISO**. `uat` KHÔNG ký thay — phiếu này ở trạng thái **CHỜ** cho tới
> khi Security thật ký. MediRemind đụng **dữ liệu sức khoẻ nhạy cảm (NFR-4)** ⇒ đây là chữ ký bắt buộc,
> không được bỏ qua dù slice nhỏ.

## Trạng thái: ⏳ CHỜ KÝ — CHƯA ĐỦ ĐIỀU KIỆN TRÌNH KÝ

## Phạm vi bảo mật cần verify (bám NFR-4 + delivery-standards §6)

| Mục | Yêu cầu (nguồn) | Bằng chứng hiện tại | Đạt? |
|-----|-----------------|---------------------|------|
| Kiểm soát truy cập path xác-nhận | AC-4: chỉ chủ liều; caregiver view-only (contract `ADH-403-NOT-OWNER`) | Chưa có authz test cho path confirm | ⬜ chưa xét |
| At-rest encryption | NFR-4: mã hoá dữ liệu thuốc at-rest | Chưa có bằng chứng/kiểm chứng | ⬜ chưa xét |
| Audit-log truy cập caregiver | NFR-4 + DoD: audit-log MỌI path truy cập caregiver | Chưa có audit-log test / bằng chứng | ⬜ chưa xét |
| SAST | quét static (delivery: hệ nhạy cảm) | Chưa chạy | ⬜ chưa xét |
| DAST | quét động | Chưa chạy | ⬜ chưa xét |
| Secret không commit | delivery §6 | Chưa kiểm | ⬜ chưa xét |

## Điều kiện ĐỦ để Security ký (checklist trình ký)
- [ ] SAST: 0 high/critical (hoặc waiver có lý do).
- [ ] DAST: 0 high/critical trên endpoint confirm/report.
- [ ] AC-4 authz PASS (không xác nhận được liều của người khác — chống IDOR).
- [ ] Audit-log áp cho MỌI path truy cập caregiver, có bằng chứng.
- [ ] At-rest encryption cho dữ liệu thuốc có bằng chứng.
- [ ] Không secret trong commit.

**Lý do CHỜ (không phủ định cứng):** chưa chạy SAST/DAST và chưa có authz/audit-log test cho path
nhạy cảm → chưa đủ điều kiện trình Security ký. Đường đi: `/review` xác định gap permission/audit →
dựng test + chạy quét → `/uat` điền kết quả → trình phiếu này cho Security/CISO.

> Ghi chú chuyển vòng: đây là **hở test bảo mật**, không phải kết luận "không an toàn". Việc đào sâu
> lỗ hổng là của `/review`; `uat` chỉ đánh dấu hở và chuẩn bị phiếu.

---

Người ký (Sec/CISO): __________________________  Tên: ____________  Ngày: __________  Chữ ký: __________
