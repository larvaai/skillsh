# MediRemind — ý tưởng thô (prose)

## Vấn đề
Người phải uống nhiều loại thuốc mỗi ngày — chủ yếu người già và người mắc bệnh mạn tính —
thường xuyên quên liều hoặc uống sai giờ. Một người điển hình phải uống 3–8 loại thuốc/ngày,
mỗi loại có lịch riêng, nên rất dễ bỏ sót. Con cái hoặc điều dưỡng chăm sóc họ (caregiver)
lại ở xa, không có cách nào biết người thân đã uống thuốc hay chưa, chỉ có thể gọi điện hỏi.

## Ý tưởng
MediRemind là một app nhắc uống thuốc và theo dõi mức độ tuân thủ (adherence). Nó phục vụ hai
nhóm người:

- **Patient** (người dùng chính): khai báo các loại thuốc và lịch uống, nhận nhắc nhở đúng giờ,
  và xác nhận "đã uống" ngay từ thông báo.
- **Caregiver** (người dùng phụ): con cái hoặc điều dưỡng, được liên kết với patient để theo dõi
  từ xa mức độ tuân thủ của họ. Caregiver chỉ-xem, không sửa được lịch thuốc.

Trọng tâm không chỉ là "kêu chuông" mà là **đo được** người dùng có uống đúng giờ hơn hay không,
và cho caregiver một bức tranh tin cậy về việc đó.

## Vì sao đáng làm
Uống thuốc không đều là nguyên nhân lớn khiến bệnh mạn tính trở nặng và phải tái nhập viện.
Nếu app kéo được tỉ lệ uống đúng giờ lên một cách đo được, giá trị với cả patient lẫn caregiver
là rõ ràng. Đây là ý tưởng **khả thi, rõ ràng** — miền nghiệp vụ dễ hình dung, quy mô MVP vừa phải,
không phải hệ thống cấp-cứu (life-critical), nên rủi ro kỹ thuật chấp nhận được.

## Ranh giới ngay từ đầu
- Clinic admin (quản trị phòng khám) **ngoài phạm vi MVP**.
- App **không dùng cho tình huống cấp cứu** — ghi rõ điều này cho người dùng.
- Dữ liệu thuốc là dữ liệu sức khoẻ nhạy cảm, nên bảo mật và kiểm soát truy cập là ràng buộc
  bắt buộc chứ không phải tính năng thêm.
