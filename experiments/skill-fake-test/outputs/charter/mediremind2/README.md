# mediremind2

**Bài toán (một câu):** Người phải uống nhiều loại thuốc mỗi ngày — chủ yếu người già và người bệnh mạn tính — hay quên liều hoặc uống sai giờ, còn caregiver (con cái, điều dưỡng) ở xa không có cách nào biết người thân đã uống chưa. MediRemind nhắc uống thuốc và ĐO được mức độ tuân thủ (adherence) cho cả patient lẫn caregiver.

## Kỳ vọng ban đầu (thô — mỏ neo cho Go/No-Go GĐ13)

> Ghi ngày 0, trước khi tinh chỉnh. Đây là "thế nào là ưng ý" để đối chiếu ở cổng release (xem `constitution/definition-of-done.md`).

- Patient khai báo được nhiều loại thuốc + lịch riêng cho mỗi loại, nhận nhắc đúng giờ, và bấm "đã uống" ngay từ thông báo.
- Caregiver được liên kết với patient, thấy được bức tranh tuân thủ TIN CẬY từ xa — chỉ-xem, không sửa được lịch thuốc.
- Tận mắt thấy tỉ lệ "uống đúng giờ" tăng lên MỘT CÁCH ĐO ĐƯỢC (không chỉ "kêu chuông").
- Dữ liệu thuốc là dữ liệu sức khoẻ nhạy cảm: bảo mật + kiểm soát truy cập là ràng buộc bắt buộc, không phải tính năng thêm.

### Ranh giới ngay từ đầu
- Clinic admin (quản trị phòng khám): NGOÀI phạm vi MVP.
- KHÔNG dùng cho tình huống cấp cứu (life-critical) — ghi rõ cho người dùng.

**Mode:** greenfield
**Ngày dựng:** 2026-07-03
**Board:** [progress/board.md](progress/board.md)

## Vào project
- Xem toàn cảnh bất cứ lúc nào: `/resume mediremind2`
- Bắt đầu brainstorm ý đầu: `/idea`
