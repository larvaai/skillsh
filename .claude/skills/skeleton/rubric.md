# Rubric — chấm một Live Slice Report do `skeleton` (GĐ8) sinh

Mỗi tiêu chí 0/1/2. Chuẩn gốc để chấm = `skeleton/SKILL.md` + `quy-trinh-idea-to-operate.md` mục "## Giai đoạn 8 —". Rubric chỉ biến hợp đồng đó thành thước đo — KHÔNG thêm tiêu chuẩn mới.

7 tiêu chí. Ba tiêu chí **XƯƠNG SỐNG (gate)**: 1, 2, 3 — đánh dấu ⛔. Rớt bất kỳ cái nào → rớt cả bản dù tổng cao.

**Đầu vào để chấm (fixture):** Live Slice Report cần chấm · Tech Decision GĐ7 + Architecture Brief GĐ6 + Domain/PRD GĐ2–5 làm nguồn · frame-return.json nếu có

## 1. ⛔ ĐÚNG + ĐỦ ARTIFACT — Live Slice Report

Có đủ các phần template GĐ8: slice là gì · đường đi E2E xuyên đủ tầng (UI→API→domain→DB→auth→log→test→CI/CD→staging→monitor) · link staging · checklist "đã validate" · giả định đã đổi · rủi ro còn lại.

- 0 — thiếu phần cốt lõi: không có đường đi E2E đủ tầng (bỏ tầng), HOẶC không có link staging chạy thật, HOẶC không có checklist validate; HOẶC tick khống (tick ô mà không có bằng chứng chạy thật); HOẶC "slice" chỉ là mockup/demo giả.
- 1 — đủ khung nhưng 1 mảnh yếu: checklist tick không kèm bằng chứng rõ, hoặc thiếu "giả định đã đổi" / "rủi ro còn lại", hoặc 1 tầng mô tả mờ.
- 2 — đủ 6 phần, slice chạy thật xuyên đủ tầng, checklist tick CÓ bằng chứng (staging mở được / CI xanh / test pass / có log-metric-trace), rủi ro còn lại kèm nơi kiểm.

## 2. ⛔ ĐỌC-ĐƯỢC 3 TẦNG — lãnh đạo mở đầu, dev hành động được

- 0 — mở thẳng bằng jargon kỹ thuật (tên framework/log tool), không có "Góc nhìn lãnh đạo"; HOẶC lãnh đạo đọc đoạn đầu KHÔNG biết kiến trúc đã chứng minh chưa / có nên đổ người vào không; HOẶC dev đọc không đủ để chạy lại full flow.
- 1 — có mở cho lãnh đạo nhưng lẫn jargon, dài quá 1 trang, hoặc thiếu 1 trong 3 thứ (link chạy được / trạng thái validate / giả định đã đổi); hoặc phần dev thiếu vài mảnh để hành động.
- 2 — MỞ bằng đúng 1–3 thứ lãnh đạo cần (link staging chạy được + trạng thái checklist validate + giả định đã đổi), ngôn ngữ nghiệp vụ; RỒI mới tới chi tiết đủ cho dev. 1 trang, scan 2–3 phút.

## 3. ⛔ BÁM NGUỒN — dùng Tech Decision/Architecture GĐ trước, không bịa

- 0 — slice hiện thực bằng stack KHÁC Tech Decision GĐ7, hoặc validate boundary KHÁC Architecture/Domain đã chốt, hoặc khẳng định "chạy thật" mà không có bằng chứng (bịa link/kết quả test/checkbox).
- 1 — bám nguồn phần lớn, 1 chỗ suy đoán không gắn nhãn, hoặc chỗ nối tới Domain/Architecture mờ.
- 2 — mọi thứ nối đúng stack GĐ7 + boundary GĐ6 + domain/PRD GĐ2–5; chỗ chưa chắc gắn nhãn rõ; giả định đã đổi ghi rõ để cập nhật ngược PRD/backlog.

Nguồn hợp lệ = artifact GĐ trước ĐÃ qua cổng HOẶC input ngoài user cung cấp KÈM cảnh báo ⚠️; dùng input ngoài mà THIẾU cảnh báo → trừ điểm (không minh bạch nguồn); vẫn CẤM bịa cái user không đưa.

## 4. ĐỦ-LÀ-ĐỦ — độ sâu tỉ lệ rủi ro, không thủ tục thừa

- 0 — cắt tầng E2E để cho ngắn, HOẶC phình mọi tầng đều dài như nhau bất kể rủi ro, HOẶC phình slice thành nhiều feature không cần cho việc chứng minh.
- 1 — độ sâu hơi lệch rủi ro ở 1–2 chỗ, hoặc còn vài dòng thủ tục thừa.
- 2 — không tầng nào bị bỏ; slice "mỏng nhất mà xuyên đủ tầng"; tầng rủi ro cao mô tả kỹ/tick thật, tầng quen một dòng; lý do chọn slice + slice đã loại ghi rõ.

## 5. TRACEABILITY — nối GĐ7 ↔ GĐ9

- 0 — không thấy nhận gì từ GĐ7, hoặc không nêu giả định-đã-đổi để feed ngược PRD/Architecture, hoặc không chỉ ra bàn giao gì cho GĐ9.
- 1 — nối một chiều (chỉ nhận, HOẶC chỉ giao).
- 2 — nối hai chiều rõ: nhận Tech Decision GĐ7 làm thứ cần chứng minh → chứng minh → giả định đổi feed ngược PRD/Arch + slice-tiếp/backlog gói sẵn cho GĐ9; rủi ro còn lại chỉ nơi kiểm (GĐ12).

## 6. CỔNG + PHÂN VAI — đúng câu hỏi, đúng người duyệt (A5)

- 0 — không có cổng, hoặc AI tự tuyên "pass"/GO thay CTO, hoặc pass mà chưa chạy thật.
- 1 — có cổng nhưng sai câu hỏi / mờ người duyệt (không nêu CTO), hoặc dùng câu phủ định cứng khi chưa pass.
- 2 — cổng đúng "Live slice pass chưa?"; Chủ sở hữu = Tech lead + dev, Người duyệt = CTO; AI trình checklist + chờ CTO quyết GO; chưa pass thì để ô trống + nêu lối đi tiếp, không phủ định cứng.

## 7. BÀN GIAO — đúng skill kế

- 0 — không có khối bàn giao, hoặc chỉ sai skill (vd tự phân rã backlog thay vì trỏ `/backlog`; tự gõ code thay vì trỏ `/frame`; tự nhảy build full).
- 1 — có bàn giao nhưng thiếu 1 nhánh (quên `/frame` cho code slice, hoặc quên `/backlog`), hoặc tự chọn hộ user, hoặc thiếu artifact path.
- 2 — khối bàn giao liệt kê đủ: `/backlog` (GĐ9) là đường chính, code thật slice → `/frame`, `/partner` nếu cần điều phối; chỉ liệt kê, không chọn hộ; có artifact path.

## Khung report (xếp nhiều bản cạnh nhau)

```text
BẢN <id> — Live Slice Report: <tên slice>
1 Đúng+đủ artifact ⛔  : _/2  — <1 dòng>
2 Đọc-được 3 tầng ⛔   : _/2  — <1 dòng>
3 Bám nguồn ⛔         : _/2  — <1 dòng>
4 Đủ-là-đủ            : _/2  — <1 dòng>
5 Traceability        : _/2  — <1 dòng>
6 Cổng + phân vai      : _/2  — <1 dòng>
7 Bàn giao đúng        : _/2  — <1 dòng>
TỔNG /14 = __   ·   GATE: <PASS / RỚT ở tiêu chí #_>
Mạnh nhất : <1 dòng>
Yếu nhất  : <1 dòng>
Sửa 1 việc: <đòn bẩy đơn lẻ tăng điểm nhiều nhất>
```

## Luật gate

Tiêu chí 1, 2, 3 là xương sống. Bất kỳ cái nào = 0 → bản Live Slice Report **RỚT GATE**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 12/14 nhưng tick khống checklist (tiêu chí 1 = 0) vẫn rớt — vì lãnh đạo sẽ tin nhầm "kiến trúc đã chứng minh" và đổ ngân sách vào nền chưa chạy thật; hoặc mở bằng jargon lãnh đạo không đọc được (2 = 0); hoặc bịa stack không khớp GĐ7 (3 = 0) → vẫn rớt. So nhiều bản: loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Vì sao các tiêu chí này

Ba tiêu chí gate đo *có ra đúng thứ + đọc được + trung thực không*; các tiêu chí sau đo *có đúng kỷ luật pipeline không* (đủ-là-đủ, không lấn vai, cổng/traceability, bàn giao). Gộp lại = trọn hợp đồng của `skeleton`, không hơn. Thêm một tiêu chí mới chỉ khi có một kiểu lỗi thật lặp lại mà bộ hiện tại không bắt được.
