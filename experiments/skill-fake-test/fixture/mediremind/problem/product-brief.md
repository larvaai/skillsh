# Product Brief — MediRemind (GĐ2)

## Góc nhìn lãnh đạo (đọc trước)
MediRemind là app nhắc uống thuốc + theo dõi tuân thủ cho **patient** (người già/bệnh mạn tính) và
**caregiver** (theo dõi từ xa, chỉ-xem). Vòng giá trị lõi: patient khai thuốc & lịch → app nhắc đúng
giờ → patient xác nhận "đã uống" bằng một chạm → adherence được tính lại → caregiver xem báo cáo.
Thành công đo bằng **SM-1** (on-time dose rate +≥15 điểm phần trăm/30 ngày) và **SM-2** (≥60%
caregiver-link kích hoạt trong tuần đầu). Không phải hệ cấp-cứu.

## 1. Người dùng & việc cần làm (jobs)
- **Patient**: "Nhắc tôi uống đúng loại, đúng giờ, và cho tôi xác nhận nhanh mà không phải mở app lằng nhằng."
- **Caregiver**: "Cho tôi biết người thân có uống đủ và đúng giờ không, mà không phải gọi điện hỏi."

## 2. Trong phạm vi MVP
- Khai báo Medication + Schedule (nhiều loại, nhiều lần/ngày, theo ngày trong tuần).
- Sinh lịch liều (DoseEvent) và bắn Reminder qua push, có SMS fallback.
- **Xác nhận liều**: từ deep-link trong reminder, patient bấm "Đã uống" → liều pending→taken.
- Tính AdherenceReport và cho caregiver (đã liên kết) **xem** báo cáo.
- Liên kết Caregiver ↔ Patient (scope view-only).

## 3. Ngoài phạm vi MVP
- Clinic admin / cổng phòng khám.
- Chỉnh liều theo tư vấn y tế, kê đơn, tương tác thuốc.
- Bất kỳ tính năng cấp-cứu nào — app ghi rõ "không dùng cho cấp cứu".

## 4. Trải nghiệm cốt lõi (happy path)
1. Patient thêm thuốc + lịch.
2. Đến giờ, hệ bắn reminder (push; SMS nếu cần).
3. Patient mở deep-link, bấm "Đã uống" → liều chuyển sang *taken*.
4. Adherence được cập nhật; caregiver liên kết thấy báo cáo mới.

## 5. Ràng buộc sản phẩm
- Dữ liệu sức khoẻ nhạy cảm → quyền truy cập chặt, audit-log truy cập của caregiver.
- Caregiver **chỉ-xem**, không sửa lịch thuốc của patient.
- Nhắc phải kịp thời (xem NFR-1) — trễ nhắc làm hỏng giá trị lõi.

## 6. Chỉ số dẫn dắt
Bám SM-1 & SM-2 (xem business-case.md). Slice chứng minh giá trị sớm nhất = **xác nhận liều**.

## Truy vết
business-case.md → **product-brief.md (đây)** → requirements.md → prd.md.
