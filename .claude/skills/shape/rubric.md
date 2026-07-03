# Rubric — 7 tiêu chí chấm một bản `shape` (GĐ6 Solution Architecture)

Mỗi tiêu chí 0/1/2. Chuẩn gốc để chấm: `shape/SKILL.md` + `quy-trinh-idea-to-operate.md` mục "## Giai đoạn 6 — Solution Architecture (SHAPE)". Rubric chỉ biến hợp đồng đó thành thước đo — KHÔNG thêm tiêu chuẩn mới.

Ba tiêu chí đầu là XƯƠNG SỐNG (gate): rớt bất kỳ cái nào → rớt cả bản dù tổng cao.

**Đầu vào để chấm (fixture):** bộ artifact shape (Architecture Brief + C4 Context/Container + Data Flow + Integration + Security Model + ADR) cần chấm · Domain Model GĐ5 + Requirement/NFR GĐ2–4 làm nguồn đối chiếu

## 1. ĐÚNG + ĐỦ ARTIFACT (xương sống)

Có đủ bộ artifact đã liệt kê: Architecture Brief (bảng quyết định) + C4 (Context & Container) + Data Flow + Integration Model + Security Model + ADRs. Bỏ artifact ≠ rút gọn độ sâu.

- 0 — thiếu hẳn một artifact xương: không có bảng quyết định, HOẶC không có sơ đồ C4 Context nào, HOẶC không có ADR cho quyết định lớn (thiếu "phương án đã loại").
- 1 — đủ mặt nhưng một artifact quá sơ sài so với rủi ro (vd Data Flow gộp qua loa, Security chỉ một dòng ở hệ có dữ liệu nhạy cảm), hoặc ADR thiếu phương án-đã-loại.
- 2 — đủ cả bộ; mỗi ô bảng quyết định có giá trị hoặc ghi "không áp dụng + lý do"; ≥1 C4 Context; ADR có đủ Bối cảnh/Quyết định/Phương án loại/Hệ quả; độ sâu khớp rủi ro.

## 2. ĐỌC-ĐƯỢC-3-TẦNG (xương sống)

Mỗi artifact mở bằng Góc nhìn lãnh đạo (1–3 thứ, ngôn ngữ nghiệp vụ, không jargon) rồi mới tới chi tiết đủ cho dev; 1 trang, scan 2–3 phút.

- 0 — nhảy thẳng vào jargon kỹ thuật, không có đoạn lãnh đạo đọc được; HOẶC quá kỹ thuật đến mức business không nắm được hệ thống có hình gì; HOẶC dev đọc xong vẫn không rõ module nào sở hữu gì, nối ra sao.
- 1 — có cả hai tầng nhưng lệch: góc lãnh đạo còn jargon hoặc chìm dưới chi tiết, hoặc phần dev thiếu một mảnh hành động (thiếu boundary/integration cụ thể).
- 2 — mở bằng đúng 1–3 thứ CTO/business nhìn để biết on-track + C4 Context; rồi đủ style + boundary + integration + auth + sơ đồ để dev bước sang GĐ7.

## 3. BÁM NGUỒN — dùng artifact GĐ trước, không bịa (xương sống)

Module boundary bám bounded context GĐ5; ngưỡng NFR lấy từ Requirement/PRD GĐ2–4; không chế số, không chế ranh giới. Nguồn hợp lệ = artifact GĐ trước ĐÃ qua cổng HOẶC input ngoài user cung cấp KÈM cảnh báo ⚠️; dùng input ngoài mà THIẾU cảnh báo → trừ điểm (không minh bạch nguồn); vẫn CẤM bịa cái user không đưa.

- 0 — bịa: đẻ bounded context/NFR không có trong Domain/PRD; ranh giới module không nối được về bounded context nào hoặc mâu thuẫn Domain Model; HOẶC bỏ qua Domain đầu vào; HOẶC chọn framework (lấn GĐ7).
- 1 — chủ yếu bám nguồn, một chỗ suy đoán không gắn nhãn (vd ngưỡng NFR đoán mò mà không ghi "open-Q").
- 2 — mọi boundary bám bounded context GĐ5; mọi NFR/security bám Requirement/PRD; open-Q từ GĐ trước được đóng hoặc chuyển tiếp có nhãn "còn treo → GĐ7"; không đụng việc GĐ7.

## 4. ĐỦ-LÀ-ĐỦ — độ sâu tỉ lệ rủi ro, không thủ tục thừa

- 0 — làm ngược Đủ-là-đủ: hệ nhỏ mà đổ đủ 4 sơ đồ + chục ADR thủ tục; HOẶC hệ rủi ro cao mà bỏ Security/Data Flow; có bước/cảnh báo thừa.
- 1 — độ sâu lệch nhẹ so với rủi ro ở 1–2 phần.
- 2 — nặng ở ô có ẩn số/NFR, nhẹ ở ô quen; hệ nhỏ gọn nhưng KHÔNG bỏ phần nào; ô không liên quan ghi "không áp dụng + lý do", không bỏ trống.

## 5. KHÔNG LẤN VAI — SHAPE, không TOOLS

Chốt hình hài, KHÔNG chốt framework/DB/lib (đó là `stack` GĐ7); không làm lại domain (GĐ5); không viết code/cắt slice (GĐ8); không phân sprint.

- 0 — chốt tên framework/DB như một quyết định trong Brief/ADR, HOẶC viết code, HOẶC làm lại domain, HOẶC lập backlog.
- 1 — chủ yếu ở tầng shape, lỡ nhắc 1 tool như gợi ý chưa gắn nhãn "để GĐ7".
- 2 — thuần shape; tool chỉ xuất hiện dưới dạng ràng buộc chuyển cho `stack`.

## 6. TRACEABILITY + CỔNG + PHÂN VAI (A5)

Nối GĐ5→GĐ6→GĐ7; có "Tự soi trước khi chốt"; cổng đúng câu doc + AI tự duyệt trước khi mời user.

- 0 — không có cổng, HOẶC tự bấm GO thay user, HOẶC tự bàn giao khi chưa đủ artifact, HOẶC không nối open-Q GĐ trước, HOẶC dùng câu phủ định cứng khi phản biện.
- 1 — có cổng nhưng phân vai duyệt mờ / câu cổng lệch doc / thiếu "Tự soi trước khi chốt", hoặc traceability một chiều (chỉ nhận domain HOẶC chỉ bàn giao stack).
- 2 — cổng đúng câu doc ("Architecture đủ vững để chọn stack & dựng live slice chưa?"); AI duyệt vai CTO/Kiến trúc sư (+ Security song song), tự soi rồi mới xin user; đầu vào chỉ rõ nhận Domain/NFR nào, open-Q GĐ trước được chốt hoặc chuyển tiếp có địa chỉ; chờ user quyết.

## 7. BÀN GIAO ĐÚNG SKILL KẾ

Khối bàn giao liệt kê `/stack` (GĐ7) là đường chính, kèm ràng buộc lái stack + open-Q chuyển tiếp + artifact path; chỉ liệt kê, không tự chọn hộ.

- 0 — không có khối bàn giao, HOẶC chỉ sang sai skill (vd tự nhảy /frame code luôn hoặc /skeleton bỏ qua /stack).
- 1 — có bàn giao nhưng tự chọn hộ user, hoặc thiếu ràng buộc/open-Q/artifact path.
- 2 — nêu `/stack` (GĐ7) là đường chính + ràng buộc + open-Q; liệt kê lối rẽ (`/skeleton`, `/frame`, `/atlas`, `/partner`) để user quyết; có artifact path; KHÔNG tự chọn hộ.

## Gate

Tiêu chí 1, 2, 3 là xương sống. Bất kỳ cái nào = 0 → bản **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Bản 12/14 nhưng bịa context/NFR hoặc module không trace về bounded context nào (tiêu chí 3 = 0) vẫn rớt — vì đội khách sẽ dựng nhầm hình hài. Khi so nhiều bản: loại hết bản rớt gate TRƯỚC, rồi mới xếp phần còn lại theo tổng.

## Khung report (xếp nhiều bản cạnh nhau)

```
BẢN <id> — shape
1 Đúng+đủ artifact   : _/2   <1 dòng>
2 Đọc-được-3-tầng    : _/2   <1 dòng>
3 Bám nguồn          : _/2   <1 dòng>
4 Đủ-là-đủ           : _/2   <1 dòng>
5 Không lấn vai      : _/2   <1 dòng>
6 Traceability+Cổng  : _/2   <1 dòng>
7 Bàn giao           : _/2   <1 dòng>
TỔNG: __/14   ·   GATE: đạt / RỚT (rớt ở tiêu chí __)
```

## Vì sao 7 tiêu chí này

Ba xương sống đo *có ra đúng thứ + đọc được + trung thực không* (artifact, 3-tầng, bám nguồn). Bốn cái sau đo *có đúng kỷ luật pipeline không* (đủ-là-đủ, không lấn vai, traceability/cổng/phân vai, bàn giao). Gộp lại = trọn hợp đồng của `shape`, không hơn. Thêm tiêu chí thứ 8 chỉ khi có kiểu lỗi thật lặp lại mà 7 cái này không bắt được.
