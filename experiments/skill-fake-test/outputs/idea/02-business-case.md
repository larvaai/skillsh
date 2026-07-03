# Business Case — MediRemind (GĐ1 Business Discovery — WHY)

> Mục tiêu: ý tưởng này có ĐÁNG làm không, bằng con số, không phải cảm tính.
> Rút gọn "Đủ-là-đủ": vấn đề + ai đau + chi phí nếu không làm + success metric đo được.
> Số cứng lấy từ BIBLE §3 (không tự bịa).

## 1. Vấn đề (WHY bây giờ)
Uống thuốc không đều (poor adherence) là một trong những nguyên nhân lớn khiến bệnh mạn tính
trở nặng và bệnh nhân phải **tái nhập viện**. Người uống 3–8 loại thuốc/ngày, mỗi loại lịch riêng,
rất dễ bỏ sót; caregiver ở xa không có tín hiệu nào ngoài gọi điện hỏi.

## 2. Ai đau & đau thế nào
- **Patient:** quên liều / sai giờ → hiệu quả điều trị giảm, rủi ro sức khoẻ tăng.
- **Caregiver:** lo lắng, không có dữ liệu tin cậy để can thiệp đúng lúc; can thiệp muộn.

## 3. Chi phí nếu KHÔNG làm (ước lượng thô)
- Với patient: bệnh nặng lên → chi phí y tế + tái nhập viện (chi phí cao, ngoài kiểm soát của app
  nhưng là động lực chính của giá trị).
- Với caregiver: thời gian + căng thẳng cho việc theo dõi thủ công qua điện thoại.
- *(Con số tuyệt đối về chi phí y tế không có trong input fixture — để mở, đánh dấu open-Q định lượng.
  Giá trị được neo bằng success metric đo-trong-app ở dưới, không phụ thuộc con số y tế ngoài.)*

## 4. Success metric (đo được) — từ BIBLE §3
- **SM-1 (chính):** Sau **30 ngày** dùng, **on-time dose rate tăng ≥ 15 điểm phần trăm** so với
  baseline tự khai; đo bằng **log xác nhận liều trong app**. → Đây là bằng chứng "app thực sự kéo
  được tỉ lệ uống đúng giờ lên", đúng trọng tâm "đo được" của ý tưởng.
- **SM-2 (phụ, kích hoạt caregiver):** **≥ 60% caregiver-link được kích hoạt** xem báo cáo trong
  **tuần đầu**. → Đo giá trị nhánh caregiver có thật sự được dùng.

## 5. Giá trị cốt lõi
Tăng **on-time dose rate** (tỉ lệ uống đúng giờ), đo được, cho patient; và một **bức tranh tuân thủ
tin cậy** cho caregiver. Cả hai đều có metric riêng ở trên → giá trị không phải cảm tính.

## 6. Quyết định + phương án đã loại
- **Chọn:** đo tuân thủ dựa trên **log xác nhận liều trong app** (self-report có mốc thời gian).
  Lý do: khả thi ở MVP, không cần tích hợp thiết bị / IoT / pill-dispenser.
- **Đã loại (ghi để audit):** đo tuân thủ bằng cảm biến hộp thuốc / thiết bị đếm viên — chính xác hơn
  nhưng đẩy chi phí + độ khó phần cứng lên cao, ngoài phạm vi MVP. Không phủ định vĩnh viễn: có thể là
  hướng nâng cấp độ tin cậy đo lường sau này.

## 7. Cổng GĐ1
*"Đáng đầu tư đi tiếp không?"* → **CÓ.** Có metric đo được (SM-1, SM-2), pain rõ, chi phí-nếu-không-làm
đủ lớn. Đi tiếp GĐ2–4 (Product → Requirements → PRD).

**Open-Q mang theo:** [OQ-cost] định lượng chi phí y tế / ROI tuyệt đối — chưa có số trong input; không
chặn đi tiếp vì giá trị đã neo bằng SM-1/SM-2 đo-trong-app.
