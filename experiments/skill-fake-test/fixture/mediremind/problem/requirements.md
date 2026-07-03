# Requirements — MediRemind (GĐ3)

## Góc nhìn lãnh đạo (đọc trước)
Yêu cầu cốt lõi của MVP xoay quanh slice **xác-nhận-liều** (patient bấm "Đã uống" từ reminder →
DoseEvent pending→taken → adherence tính lại) — đây là slice chứng minh giá trị SM-1 sớm nhất và
cũng là live slice đã chạy được ở GĐ8. Dưới đây là Acceptance Criteria dạng Given/When/Then cho
slice đó, kèm 5 NFR có **số cứng** (timeliness, latency, scale, sensitivity, availability) mà mọi
skill hạ nguồn phải lấy làm chuẩn.

## 1. Functional — slice xác-nhận-liều (Acceptance Criteria)

**AC-1 — Xác nhận đúng liều đang chờ**
- **Given** một DoseEvent ở trạng thái `pending` cho patient P với thời gian dự kiến hôm nay,
- **When** patient P mở deep-link trong reminder và bấm "Đã uống",
- **Then** DoseEvent chuyển `pending → taken`, `taken_at` = thời điểm bấm, và adherence của P được tính lại.

**AC-2 — Ghi nhận nhanh (bám NFR-2)**
- **Given** patient P bấm "Đã uống" trên một liều pending,
- **When** hệ ghi xác nhận,
- **Then** thao tác ghi hoàn tất trong **≤ 300ms ở p95**.

**AC-3 — Không xác nhận lại liều đã chốt**
- **Given** một DoseEvent đã ở trạng thái `taken` (hoặc `missed`/`skipped`),
- **When** patient bấm "Đã uống" lần nữa trên cùng liều đó,
- **Then** hệ **không** đổi trạng thái lần hai và không tính trùng vào adherence.

**AC-4 — Chỉ chủ liều mới xác nhận được**
- **Given** một DoseEvent thuộc patient P,
- **When** một user khác P (kể cả caregiver liên kết) cố xác nhận liều đó,
- **Then** hệ **từ chối** thao tác; caregiver có scope **view-only**, không đổi được trạng thái liều.

**AC-5 — Liều không được xác nhận đúng hạn → missed**
- **Given** một DoseEvent `pending` mà đã qua cửa sổ cho phép,
- **When** không có xác nhận nào tới,
- **Then** DoseEvent chuyển `pending → missed` và được phản ánh vào adherence.

## 2. Non-Functional Requirements (số CỨNG — §6 BIBLE)
| Mã | Loại | Yêu cầu |
|----|------|---------|
| **NFR-1** | Timeliness | Reminder phải bắn **trong vòng 60s** so với `scheduled_time`. |
| **NFR-2** | Latency | Ghi xác nhận liều **≤ 300ms p95**. |
| **NFR-3** | Scale (MVP) | **50k active user**, ~5 liều/user/ngày ≈ **250k DoseEvent/ngày**. |
| **NFR-4** | Sensitivity | Dữ liệu thuốc nhạy cảm → **mã hoá at-rest**, kiểm soát truy cập, **audit-log** mọi truy cập của caregiver. |
| **NFR-5** | Availability | **99.5%** (không life-critical; app ghi rõ "không dùng cho cấp cứu"). |

## Truy vết
product-brief.md → **requirements.md (đây)** → prd.md → domain (GĐ5).
