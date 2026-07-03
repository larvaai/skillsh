# Business Case — MediRemind (GĐ1)

## Góc nhìn lãnh đạo (đọc trước)
Người mắc bệnh mạn tính và người già uống 3–8 loại thuốc/ngày, hay quên hoặc uống sai giờ; con
cái/điều dưỡng ở xa không biết người thân đã uống hay chưa. MediRemind nhắc đúng giờ, cho patient
xác nhận liều bằng một chạm, và cho caregiver theo dõi từ xa. **Chúng ta chỉ coi là thành công khi
đo được**: on-time dose rate tăng ≥ 15 điểm phần trăm sau 30 ngày (**SM-1**), và ≥ 60% caregiver-link
được kích hoạt xem báo cáo trong tuần đầu (**SM-2**). Đây không phải hệ cấp-cứu, mục tiêu khả dụng
đặt ở mức hợp lý (99.5%), đổi lại tốc độ giao hàng. Rủi ro chính là dữ liệu sức khoẻ nhạy cảm —
được xử lý như ràng buộc bắt buộc, không phải tính năng thêm.

## 1. Vấn đề nghiệp vụ
Uống thuốc không đều là nguyên nhân lớn khiến bệnh mạn tính trở nặng và tái nhập viện. Với người
uống nhiều loại thuốc, mỗi loại có lịch riêng, việc bỏ sót liều là chuyện thường ngày. Caregiver
hiện chỉ có cách gọi điện hỏi — không có dữ liệu tin cậy về mức độ tuân thủ.

## 2. Đối tượng hưởng lợi (personas)
- **Patient** (chính): người già + bệnh mạn tính, uống 3–8 loại thuốc/ngày, hay quên liều.
- **Caregiver** (phụ): con cái/điều dưỡng, theo dõi adherence của patient từ xa, quyền **chỉ-xem**.
- Clinic admin: **ngoài phạm vi MVP**.

## 3. Giá trị đề xuất
Tăng tỉ lệ uống thuốc đúng giờ (on-time dose rate) một cách **đo được**, và cho caregiver một bức
tranh tin cậy để yên tâm / can thiệp kịp thời.

## 4. Success metrics (đo được — nguồn cho toàn pipeline)
| Mã | Định nghĩa | Ngưỡng |
|----|-----------|--------|
| **SM-1** | Sau 30 ngày dùng, on-time dose rate tăng so với baseline tự khai; đo bằng log xác nhận liều trong app. | **≥ 15 điểm phần trăm** |
| **SM-2** | Caregiver-link được kích hoạt xem báo cáo trong tuần đầu. | **≥ 60%** |

## 5. Ràng buộc & phi-mục-tiêu
- **Không** phải hệ thống cấp-cứu; app ghi rõ "không dùng cho cấp cứu".
- Dữ liệu thuốc là **dữ liệu sức khoẻ nhạy cảm** → bảo mật, kiểm soát truy cập, audit-log là bắt buộc.
- MVP không bao gồm clinic admin.

## 6. Vì sao làm bây giờ / khả thi
Miền nghiệp vụ rõ, quy mô MVP vừa (mục tiêu 50k active user), đội nhỏ mạnh TypeScript. Rủi ro kỹ
thuật chấp nhận được vì không life-critical. Ý tưởng đã được phân loại **khả thi + rõ ràng** ở GĐ0.

## Truy vết
idea/mediremind.md → **business-case.md (đây)** → product-brief.md → requirements.md → prd.md.
