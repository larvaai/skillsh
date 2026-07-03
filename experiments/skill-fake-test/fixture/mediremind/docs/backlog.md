# Backlog & Roadmap — MediRemind (GĐ9 · backlog)

> Nguồn: BIBLE §3 (SM-1/SM-2) · §2 (personas) · §4 (entities) · §5 (contexts) · §6 (NFR) · §9 (slice).
> Đầu vào: Live Slice Report (GĐ8, `docs/skeleton-live-slice.md`). Đầu ra: đội delivery biết XÂY GÌ TRƯỚC.
> AC nằm DƯỚI story (Given/When/Then), KHÔNG thay PRD. Definition of Done tách riêng (§4 dưới).

## 1. Roadmap (theme × release)

| Theme \ Release | R1 · MVP core (proof→dùng được) | R2 · Caregiver & tin cậy | R3 · Đo & tinh chỉnh |
|---|---|---|---|
| **T-A Uống thuốc đúng giờ** (→SM-1) | E1 Sinh lịch & liều · E2 Nhắc đúng giờ · E3 Xác nhận liều | siết timeliness (NFR-1) | tối ưu theo dữ liệu adherence |
| **T-B Theo dõi từ xa** (→SM-2) | — | E4 Caregiver-link & báo cáo | thông báo caregiver |
| **T-C Tin cậy & tuân thủ** (→NFR-4/5) | audit-log tối thiểu | E5 Bảo mật dữ liệu sức khoẻ + retention (đóng OQ-B) | 99.5% availability |

Thứ tự build: **R1 trước** (đường sống SM-1: sinh liều → nhắc → xác nhận → tính adherence) — chính là
slice đã chứng minh ở GĐ8, giờ mở rộng thành đủ tính năng.

## 2. Backlog phân rã (Epic → Feature → Story → AC)

### E1 — Sinh lịch thuốc & DoseEvent  · Theme T-A · → **SM-1**
> Vì SM-1 đo on-time dose rate qua log xác nhận liều, trước hết phải có DoseEvent đúng để mà xác nhận.

- **F1.1 Tạo/sửa Schedule** (entity `Schedule` §4)
  - **US-1.1.1** *Là Patient, tôi muốn khai lịch uống 1 thuốc (giờ + ngày trong tuần) để app tự nhắc.*
    - AC-1: **Given** patient đã đăng nhập, **When** tạo Schedule với timesOfDay+daysOfWeek+startDate,
      **Then** Schedule được lưu gắn đúng `userId`.
    - AC-2: **Given** Schedule có `endDate` trong quá khứ, **When** hệ sinh liều cho hôm nay,
      **Then** KHÔNG sinh DoseEvent cho Schedule đã hết hạn. *(chặn khiếm khuyết end-date thấy ở slice)*
- **F1.2 Sinh DoseEvent theo timezone patient**
  - **US-1.2.1** *Là Patient ở múi giờ của tôi, tôi muốn liều rơi đúng giờ LOCAL.*
    - AC-1: **Given** Schedule timezone `Asia/Ho_Chi_Minh` và timesOfDay `["08:00"]`,
      **When** sinh liều, **Then** `scheduledTime` = 08:00 theo `s.timezone`, KHÔNG theo giờ server.
    - AC-2: **Given** hôm nay không nằm trong `daysOfWeek`, **When** sinh liều, **Then** không có DoseEvent.

### E2 — Nhắc đúng giờ  · Theme T-A · → **SM-1**
> On-time dose rate chỉ tăng nếu reminder tới đúng lúc và không phiền (không lặp).

- **F2.1 Dispatch reminder tới hạn**
  - **US-2.1.1** *Là Patient, tôi muốn nhận đúng MỘT nhắc cho mỗi liều tới hạn.*
    - AC-1: **Given** một DoseEvent `pending` tới hạn, **When** worker chạy nhiều lần trong cửa sổ,
      **Then** chỉ gửi Reminder **một lần** (dedupe theo doseEventId). *(chặn lỗi gửi lặp ở slice)*
    - AC-2 (NFR-1): **Given** `scheduled_time`, **When** đến giờ, **Then** Reminder bắn trong vòng **60s**.
- **F2.2 Bền vững khi provider lỗi**
  - **US-2.2.1** *Là Patient, tôi vẫn được nhắc dù một lần gửi thất bại.*
    - AC-1: **Given** `pushProvider.send` throw cho 1 liều, **When** dispatch lô nhiều liều,
      **Then** các liều còn lại VẪN được gửi (một lỗi không vỡ cả vòng), và liều lỗi được retry.
    - AC-2: **Given** hết retry, **When** vẫn lỗi, **Then** ghi log/audit để lần vết.

### E3 — Xác nhận liều & tính adherence  · Theme T-A · → **SM-1**
> Đây là chỗ SM-1 được ĐO: log "Đã uống" là nguồn on-time dose rate. Chính là slice GĐ8.

- **F3.1 Xác nhận một liều (an toàn quyền)**
  - **US-3.1.1** *Là Patient, tôi bấm "Đã uống" và chỉ liều CỦA TÔI đổi trạng thái.*
    - AC-1: **Given** patient đăng nhập là chủ liều, **When** POST /doses/:id/confirm,
      **Then** DoseEvent `pending→taken`, `takenAt` được set, trả 200.
    - AC-2 (quyền): **Given** liều thuộc user KHÁC, **When** confirm, **Then** trả **403**, KHÔNG đổi trạng thái.
      *(đóng khiếm khuyết authorization ô #5 của Live Slice Report)*
- **F3.2 Tính AdherenceReport đúng**
  - **US-3.2.1** *Là Patient/Caregiver, tôi muốn adherence rate phản ánh đúng thực tế.*
    - AC-1: **Given** user chưa có DoseEvent nào, **When** tính rate, **Then** trả giá trị xác định
      (vd 0 hoặc "chưa có dữ liệu"), KHÔNG phải NaN. *(chặn chia-cho-0 ở slice)*
    - AC-2: **Given** có liều `skipped`/`pending`, **When** tính rate, **Then** mẫu số chỉ gồm liều
      "đáng lẽ đã uống" (taken + missed), KHÔNG kéo `skipped`/`pending` vào làm sai số.

### E4 — Caregiver-link & báo cáo  · Theme T-B · → **SM-2**
> SM-2 đo ≥60% caregiver-link được kích hoạt xem báo cáo tuần đầu → cần link + route báo cáo view-only.

- **F4.1 Tạo & kích hoạt CaregiverLink** (entity `CaregiverLink` §4, scope view-only)
  - **US-4.1.1** *Là Patient, tôi mời một caregiver để họ THEO DÕI (chỉ-xem) adherence của tôi.*
    - AC-1: **Given** patient mời caregiver, **When** caregiver chấp nhận, **Then** tạo CaregiverLink
      scope `view-only`, và link tính là "được kích hoạt" (đo SM-2).
- **F4.2 Caregiver xem báo cáo (view-only + audit)**
  - **US-4.2.1** *Là Caregiver, tôi xem AdherenceReport của patient tôi được liên kết — và chỉ họ.*
    - AC-1: **Given** có CaregiverLink hợp lệ, **When** caregiver mở báo cáo,
      **Then** thấy AdherenceReport của đúng patient đó (`canCaregiverView` = true).
    - AC-2 (NFR-4): **Given** caregiver truy cập dữ liệu patient, **When** mọi lần xem,
      **Then** ghi **audit-log** truy cập. **Then** caregiver KHÔNG sửa được gì (view-only).

### E5 — Bảo mật dữ liệu sức khoẻ & retention  · Theme T-C · → **NFR-4** (nền cho SM-1/SM-2)
> Dữ liệu thuốc là nhạy cảm; không có E5 thì SM không thể triển khai thật ra ngoài.

- **F5.1 Mã hoá at-rest + kiểm soát truy cập** (NFR-4)
  - **US-5.1.1** *Là hệ thống, dữ liệu thuốc được mã hoá at-rest và chỉ chủ dữ liệu/caregiver-link đọc.*
    - AC-1: **Given** dữ liệu thuốc/liều, **When** lưu, **Then** mã hoá at-rest; truy cập ngoài chủ sở hữu
      bị chặn (trừ CaregiverLink view-only).
- **F5.2 Retention policy** *(đóng OQ-B đang treo ở Tech Decision)*
  - **US-5.2.1** *Là hệ thống tuân thủ, dữ liệu được giữ đúng thời hạn đã định rồi xoá/ẩn danh.*
    - AC-1: **Given** một khoảng retention đã CHỐT, **When** dữ liệu quá hạn, **Then** được xoá/ẩn danh
      theo policy. **Note:** khoảng retention (OQ-B) **CHƯA chốt** — cần quyết trước khi build F5.2.

## 3. Truy vết Epic → business value

| Epic | Nối ngược | Vì sao |
|------|-----------|--------|
| E1 Sinh lịch & liều | **SM-1** | Không có DoseEvent đúng thì không có gì để xác nhận/đo on-time rate |
| E2 Nhắc đúng giờ | **SM-1** + NFR-1 | Nhắc đúng & không lặp là điều kiện để dose rate tăng |
| E3 Xác nhận & adherence | **SM-1** | Log "Đã uống" CHÍNH là nguồn đo on-time dose rate ≥15 điểm |
| E4 Caregiver-link & báo cáo | **SM-2** | Đo ≥60% caregiver-link kích hoạt xem báo cáo tuần đầu |
| E5 Bảo mật & retention | NFR-4 (nền SM-1/SM-2) | Dữ liệu sức khoẻ nhạy cảm — điều kiện để chạy thật ngoài đời |

## 4. Definition of Done (tách khỏi AC)

Một Story = Done khi: mã + test (unit/E2E) xanh · qua PR review · đạt AC của story · không vi phạm NFR
liên quan · có log/audit nếu chạm dữ liệu nhạy cảm (NFR-4) · cập nhật doc nếu đổi contract.
*(DoD áp cho MỌI story; AC là điều kiện riêng từng story — hai thứ khác nhau.)*

## 5. Release Plan (tóm tắt)
- **R1 (MVP core):** E1 + E2 + E3 → đủ đường sống SM-1, dùng được cho patient.
- **R2 (Caregiver & tin cậy):** E4 + E5 + siết NFR-1 → mở SM-2 và đưa ra ngoài an toàn (đóng OQ-B ở F5.2).
- **R3 (Đo & tinh chỉnh):** tối ưu theo dữ liệu adherence + availability 99.5% (NFR-5).

---

*Trace: mọi Epic nối SM-1/SM-2 (BIBLE §3); AC dùng entity/NFR có thật (§4/§6); OQ-B để hở đúng chủ ý (F5.2). Không bịa persona/metric ngoài BIBLE.*
