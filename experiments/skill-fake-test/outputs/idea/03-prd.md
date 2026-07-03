# PRD (rút gọn 1 trang) — MediRemind (GĐ2–4: Product Discovery → Requirements → PRD)

> GĐ2–4 gộp: đây là chỗ BRAINSTORM cách tiếp cận trước khi chốt. Không viết 14 mục PRD cứng —
> chỉ "Đủ-là-đủ": MVP rõ + đo bằng metric nào + scope-out thành chữ + NFR có số + open-Q còn treo.
> Success metric kế thừa GĐ1 (không hỏi lại ROI). Chưa chọn stack/kiến trúc (đó là GĐ6+).

---

## A. Product Discovery (WHAT VALUE)

### A.1 Ai dùng
- **Patient** (chính): khai báo thuốc + lịch, nhận nhắc, xác nhận "đã uống".
- **Caregiver** (phụ): liên kết với patient, **chỉ-xem** báo cáo tuân thủ từ xa.

### A.2 Journey AS-IS → TO-BE
- **AS-IS:** patient tự nhớ (hoặc note giấy / báo thức chung) → hay quên; caregiver gọi điện hỏi
  "uống thuốc chưa?" → dữ liệu rời rạc, không tin cậy, can thiệp muộn.
- **TO-BE:** patient khai thuốc + lịch một lần → app nhắc đúng giờ từng liều → patient bấm "Đã uống"
  ngay trên thông báo → app tính tuân thủ → caregiver mở app thấy báo cáo tin cậy, không cần gọi hỏi.

### A.3 Brainstorm — 2 hướng cho "cách đo tuân thủ" (rủi ro đo lường cao → cân ≥2 hướng)
| Hướng | Mô tả | Chọn? |
|-------|-------|-------|
| **H1 — Xác nhận thủ công theo liều** | Mỗi DoseEvent có nút "Đã uống"; không bấm trong cửa sổ cho phép → tính là miss. | **CHỌN** — khả thi MVP, đúng metric SM-1 (log xác nhận liều), không cần phần cứng. |
| H2 — Suy luận tự động (vị trí/thiết bị/cảm biến) | App tự đoán đã uống. | Loại khỏi MVP — chi phí + độ chính xác + quyền riêng tư cao; giữ làm hướng nâng cấp sau. |

### A.4 MVP (làm gì)
1. Patient khai báo **Medication** (tên, liều, dạng) + **Schedule** (mấy lần/ngày, ngày nào trong tuần, khoảng ngày, múi giờ).
2. Hệ **sinh các liều cần uống** (DoseEvent) theo lịch.
3. **Nhắc đúng giờ** từng liều (push; SMS là fallback khi cần).
4. Patient **xác nhận "Đã uống"** ngay từ thông báo (chuyển liều pending→taken); không xác nhận trong cửa sổ → **missed**; có thể **skip** chủ động.
5. Hệ **tính tuân thủ** (on-time dose rate) theo kỳ.
6. **Liên kết caregiver** (chỉ-xem) → caregiver mở **báo cáo tuân thủ** của patient.
7. Ghi **audit-log** mọi lần caregiver truy cập dữ liệu patient.

### A.5 CỐ TÌNH không làm (out-of-scope MVP) — ghi thành chữ
- Clinic admin / quản trị phòng khám.
- Tình huống **cấp cứu** (app hiển thị disclaimer "không dùng cho cấp cứu").
- Caregiver **không** được sửa lịch thuốc (chỉ-xem).
- Đo tuân thủ tự động bằng phần cứng / cảm biến (H2).
- Tích hợp EHR / hồ sơ bệnh án bệnh viện, thanh toán, kê đơn.

---

## B. Requirements (WHAT EXACTLY) — chỉ cái quan trọng

### B.1 Functional (rút gọn)
- FR-1 Patient CRUD Medication + Schedule (của chính mình).
- FR-2 Hệ sinh DoseEvent từ Schedule cho khoảng thời gian sắp tới.
- FR-3 Gửi Reminder cho mỗi DoseEvent tới giờ; SMS fallback.
- FR-4 Patient xác nhận liều: pending → taken / skipped; hết cửa sổ chưa xác nhận → missed.
- FR-5 Tính AdherenceReport (on-time dose rate) theo kỳ cho một patient.
- FR-6 Caregiver liên kết với patient (scope view-only) và xem AdherenceReport.
- FR-7 Ghi audit-log mọi truy cập dữ liệu patient bởi caregiver.

### B.2 NFR (có số) — **tự derive từ bản chất bài toán; cần đối chiếu chuẩn cứng của dự án ở GĐ6/§NFR**
| ID | Loại | Ngưỡng (đề xuất) | Lý do derive |
|----|------|------------------|--------------|
| NFR-1 | Timeliness | Reminder bắn **≤ ~1 phút** so với giờ hẹn | "Nhắc uống thuốc" mất giá trị nếu trễ nhiều; ngưỡng chính xác là số cứng của dự án — **open-Q, chốt ở GĐ6/spec NFR**. |
| NFR-2 | Latency ghi xác nhận | phản hồi "đã uống" **≤ vài trăm ms p95** | Bấm từ thông báo phải mượt; con số p95 chính xác chốt ở spec NFR. |
| NFR-3 | Scale (MVP) | vài chục nghìn active user, ~vài liều/user/ngày → ~hàng trăm nghìn DoseEvent/ngày | Suy từ persona "người già + bệnh mạn tính", 3–8 thuốc/ngày; con số cứng chốt ở spec. |
| NFR-4 | Sensitivity/Security | dữ liệu thuốc nhạy cảm → **mã hoá at-rest + kiểm soát truy cập + audit-log** truy cập caregiver | Ràng buộc bắt buộc nêu ngay từ ý tưởng thô. |
| NFR-5 | Availability | cao nhưng **không** life-critical (app ghi rõ "không dùng cấp cứu") | Ý tưởng thô khẳng định không phải hệ cấp-cứu → không cần mức life-critical. |

> Ghi chú trung thực: các ngưỡng SỐ CỨNG (giây/ms/số user cụ thể) là tài sản của spec NFR dự án
> (GĐ6). `idea` derive khoảng hợp lý + đánh dấu open-Q; KHÔNG tự đóng đinh con số ở tầng này.

---

## C. PRD one-pager (WHAT — chốt)

- **Goal:** kéo on-time dose rate lên đo được cho patient; cho caregiver bức tranh tuân thủ tin cậy từ xa.
- **Success metric (kế thừa GĐ1):**
  - SM-1: sau 30 ngày, on-time dose rate **+≥15 điểm %** vs baseline tự khai (đo bằng log xác nhận liều).
  - SM-2: **≥60%** caregiver-link kích hoạt xem báo cáo trong tuần đầu.
- **Scope IN:** khai thuốc+lịch · sinh liều · nhắc (push, SMS fallback) · xác nhận liều · tính tuân thủ · caregiver chỉ-xem · audit-log.
- **Scope OUT:** clinic admin · cấp cứu · caregiver sửa lịch · đo tự động bằng phần cứng · EHR/thanh toán/kê đơn.
- **Rollout thô:** internal → nhóm pilot nhỏ (patient thật + caregiver) → mở rộng dần. (chi tiết là GĐ13 `/ship`.)

### Open questions còn treo (mang sang GĐ5/GĐ6)
- **OQ-1 (→GĐ5 Domain):** "on-time" định nghĩa chính xác thế nào? cửa sổ cho phép quanh giờ hẹn là bao nhiêu → biên giữa **taken đúng giờ** vs **taken trễ** vs **missed**. Trả lời ở business rule GĐ5.
- **OQ-2 (→spec NFR/GĐ6):** ngưỡng số cứng NFR-1/2/3 (giây, ms, số user).
- **OQ-3 (→GĐ6/kiến trúc):** sinh DoseEvent + dispatch reminder chạy realtime hay theo lô (batch/cron)? Đây là câu **kiến trúc**, KHÔNG trả lời ở tầng idea.
- **OQ-4 (→GĐ6/security spec):** giữ dữ liệu sức khoẻ bao lâu (retention) cho NFR-4? treo.

### Cổng GĐ2–4
*"Hướng sản phẩm & MVP đủ rõ chưa?"* → **CÓ** (MVP A.4 + scope-out A.5 rõ, có brainstorm A.3).
*"PRD đủ tin cậy để đi Domain chưa?"* → **CÓ**, các open-Q đều có chỗ đóng ở GĐ5 hoặc GĐ6, không cái nào chặn. Đi tiếp GĐ5.
