# Idea Brief — MediRemind (GĐ0 Idea Intake)

> Cửa vào SỚM NHẤT. Bản này chốt phân loại Router + ranh giới ban đầu, trước khi đi
> Business → Product → PRD → Domain. Nguồn: ý tưởng thô `idea/mediremind.md` + BIBLE §1-3.

## 1. Một câu
MediRemind — app nhắc uống thuốc và **đo được** mức tuân thủ (adherence) cho người phải uống
nhiều loại thuốc mỗi ngày, cho phép người chăm sóc từ xa theo dõi tin cậy.

## 2. Ai đau
- **Patient** (người dùng chính): người già + bệnh mạn tính, uống 3–8 loại thuốc/ngày, mỗi loại
  lịch riêng → hay quên liều / uống sai giờ.
- **Caregiver** (người dùng phụ): con cái / điều dưỡng ở xa, hiện chỉ có cách gọi điện hỏi, không
  có bức tranh tin cậy về việc người thân đã uống thuốc chưa.

## 3. Ý tưởng cốt lõi
Không chỉ "kêu chuông" mà **đo** người dùng có uống đúng giờ hơn không, và cho caregiver một bức
tranh đáng tin. Ba mảnh: (a) khai báo thuốc + lịch, (b) nhắc đúng giờ + xác nhận "đã uống" ngay từ
thông báo, (c) tổng hợp tuân thủ + chia sẻ chỉ-xem cho caregiver.

## 4. Ranh giới ngay từ đầu (từ ý tưởng thô)
- **Out of scope MVP:** Clinic admin (quản trị phòng khám).
- **Không dùng cho tình huống cấp cứu** — phải ghi rõ cho người dùng (đây KHÔNG phải hệ life-critical).
- **Dữ liệu thuốc = dữ liệu sức khoẻ nhạy cảm** → bảo mật + kiểm soát truy cập là RÀNG BUỘC bắt buộc,
  không phải tính năng thêm.
- Caregiver **chỉ-xem**, không sửa được lịch thuốc của patient.

## 5. Phân loại Router
| Trục | Kết quả | Vì sao |
|------|---------|--------|
| Độ rõ | **rõ ràng** | Đã biết cho ai (patient/caregiver), input (thuốc+lịch), output (nhắc + báo cáo tuân thủ), ranh giới MVP (không clinic admin, không cấp cứu). |
| Độ khả thi | **khả thi rõ** | Miền dễ hình dung, MVP vừa phải, không life-critical → không có ẩn số kỹ thuật/business chặn đường. |

**→ Nhánh C** (khả thi rõ): đi thẳng GĐ1 → GĐ5, brainstorm/làm rõ dọc đường. Vì độ rõ = rõ ràng,
tốc độ đi qua Nhánh C ở chế độ **lướt nhanh** — mỗi giai đoạn vẫn ghi đủ "Đủ-là-đủ", không hỏi sâu
những gì ý tưởng thô đã trả lời.

Không có ẩn số nào cần spike (Nhánh B), không có điểm bất-khả-thi nào cần làm rõ (Nhánh A).

## 6. Cổng GĐ0 → GĐ1
*"Ý tưởng đủ rõ để bắt đầu định giá business chưa?"* → **CÓ.** Đi tiếp GĐ1.
