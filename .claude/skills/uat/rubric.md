# Rubric — chấm một bản artifact của `uat` (Test & Verification Report, GĐ12)

Mỗi tiêu chí 0/1/2. Chuẩn gốc để chấm: `uat/SKILL.md` + `quy-trinh-idea-to-operate.md` mục "## Giai đoạn 12". Rubric chỉ biến hợp đồng đó thành thước đo — KHÔNG thêm tiêu chuẩn mới. Tiêu chí **1, 2, 3** là **xương sống (gate)**.

**Đầu vào để chấm (fixture):** bản Test & Verification Report cần chấm · Delivery Standards + DoD GĐ11 + PRD/Requirement/AC GĐ3–4 làm nguồn

## 1. ĐÚNG + ĐỦ ARTIFACT (xương sống)

Có đúng artifact GĐ12 với đủ các phần đã liệt kê: Góc nhìn lãnh đạo · bảng MAPPING (Requirement→AC→Test Case→Test Result→Release Decision) · REPORT lớp test · **UAT sign-off + Security sign-off**.

- 0 — thiếu một phần bắt buộc: không có mapping traceability, HOẶC thiếu 1 trong 2 chữ ký mà không ghi đang-chờ, HOẶC mapping đứt mắt (AC không nối tới Result), HOẶC sinh nhầm artifact giai đoạn khác.
- 1 — có đủ khối nhưng một mắt sơ sài (Result ghi PASS trơ không phạm vi/con số ở phần cần; hoặc mapping không nối tới test case cụ thể).
- 2 — đủ 5 mắt mapping + REPORT + 2 chữ ký (ký/chờ + ngày); AC nào chưa có test được ghi rõ là "hở", không giấu.

## 2. ĐỌC-ĐƯỢC 3 TẦNG (xương sống)

Mở bằng Góc nhìn lãnh đạo (pass rate + 2 chữ ký + 1 dòng hở, ngôn ngữ nghiệp vụ), RỒI mới tới bảng test cho dev. 1 trang, scan 2–3 phút.

- 0 — mở thẳng bằng bảng kỹ thuật/tên framework test; lãnh đạo đọc đoạn đầu không biết on-track; hoặc không có khối "Góc nhìn lãnh đạo"; hoặc dài quá 1 trang.
- 1 — có tầng lãnh đạo nhưng lẫn jargon, hoặc lẫn thứ tự, hoặc dev thiếu mắt xích để hành động (không rõ TC nào fail/hở ở đâu).
- 2 — MỞ bằng 1–3 thứ cho CEO/CTO (pass rate + 2 chữ ký + hở) bằng ngôn ngữ nghiệp vụ, RỒI mới tới bảng đủ cho dev lần lại; scan 2–3 phút.

## 3. BÁM NGUỒN — dùng artifact GĐ trước, không bịa (xương sống)

Requirement & AC TRÍCH từ Delivery (GĐ11) hoặc PRD/Requirement (GĐ3–4), nối tiếp sợi traceability; số liệu test không bịa. Nguồn hợp lệ = artifact GĐ trước ĐÃ qua cổng HOẶC input ngoài user cung cấp KÈM cảnh báo ⚠️; dùng input ngoài mà THIẾU cảnh báo → trừ điểm (không minh bạch nguồn); vẫn CẤM bịa cái user không đưa.

- 0 — bịa AC/Test Case/kết quả không có gốc; hoặc bịa số pass, tên chữ ký; hoặc dựng lại requirement từ đầu thay vì nối GĐ trước; hoặc bịa DoD khi không đọc được `delivery.md`.
- 1 — chủ yếu bám nguồn, 1 chỗ suy đoán không gắn nhãn giả định.
- 2 — mọi hàng mapping truy ngược được về artifact GĐ trước; chuẩn "đã verify" lấy từ DoD GĐ11; chỗ chưa có test đánh dấu hở thay vì ngụy tạo PASS.

## 4. ĐỦ-LÀ-ĐỦ — không thủ tục thừa, không bỏ bước

Số lớp test + độ sâu tỉ lệ rủi ro; không bỏ mapping/chữ ký; không nhồi lớp test vô nghĩa cho slice nhỏ.

- 0 — bỏ mapping/chữ ký để "gọn", HOẶC hệ quan trọng mà cắt security/perf/DR không nêu lý do, HOẶC bắt slice nội bộ chạy đủ pentest/DR không cần thiết mà không ghi lý do.
- 1 — độ sâu hơi lệch rủi ro, hoặc bỏ lớp mà không ghi lý do.
- 2 — độ sâu khớp rủi ro; lớp bỏ có 1 dòng lý do; giữ trọn mapping + 2 chữ ký; slice nhỏ gọn, hệ quan trọng đủ NFR/số đo.

## 5. TRACEABILITY — nối GĐ trước ↔ sau

Mapping nối ngược PR/story (GĐ11) + requirement (GĐ3–4), nối xuôi tới Release Decision làm đầu vào cho `ship` (GĐ13).

- 0 — mapping đứt: có test result nhưng không gắn AC/requirement, hoặc không có Release Decision.
- 1 — nối một chiều (chỉ về trước hoặc chỉ về sau); hoặc một mắt lỏng (TC không mã, Release Decision chung chung).
- 2 — sợi liền: Requirement (GĐ3–4) → AC → TC có mã → Result → Release Decision → khối bàn giao ship (GĐ13); PR/story được tham chiếu.

## 6. CỔNG + PHÂN VAI ĐÚNG (A5)

Có cổng "Pass đủ điều kiện go-live chưa?"; người duyệt là QA lead + PO (UAT) + Security; `uat` không tự ký thay, không tự quyết Go/No-Go cuối, không đào gap sâu.

- 0 — không có cổng; hoặc AI tự ký thay PO/Security; hoặc tự phán "release/không release"; hoặc lấn sang đào edge case (việc `/review`).
- 1 — có cổng nhưng phân vai duyệt mờ (không rõ PO cho UAT, Security cho security sign-off), hoặc lấn nhẹ.
- 2 — cổng đúng câu hỏi GĐ12; AI kiểm điều kiện đủ để trình ký, KHÔNG tự ký; gap chuyển `/review`; NO-GO nêu lối đi, không phủ định cứng.

## 7. BÀN GIAO ĐÚNG SKILL KẾ

Khối bàn giao nêu đúng skill tiếp (`/ship` go-live; `/review` nếu còn nghi hở; `/frame`·`/delivery` nếu sửa AC fail), chỉ liệt kê không tự chọn hộ.

- 0 — không có khối bàn giao, hoặc trỏ sai skill (tự đào edge case thay vì `/review`; tự deploy thay vì `/ship`).
- 1 — có bàn giao nhưng thiếu một nhánh, hoặc tự chọn hộ user.
- 2 — liệt đủ nhánh kế đúng theo tình huống, để user quyết.

## Gate

Tiêu chí **1, 2, 3** là xương sống. Bất kỳ cái nào = 0 → bản **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 12/14 nhưng thiếu chữ ký Security (tiêu chí 1 = 0) hoặc bịa test result (tiêu chí 3 = 0) vẫn rớt — vì exec/khách sẽ ký nhầm cho lên. Khi so nhiều bản: loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Khung report (xếp nhiều bản cạnh nhau)

```text
Bản: <id>
1 Đúng+đủ artifact : _/2   2 Đọc-được 3 tầng : _/2   3 Bám nguồn : _/2   [3 xương sống]
4 Đủ-là-đủ        : _/2   5 Traceability   : _/2   6 Cổng+phân vai : _/2   7 Bàn giao : _/2
TỔNG: _/14   ·   GATE (1,2,3): PASS / RỚT ở <tiêu chí>
Ghi chú 1 dòng: <điểm mạnh / lỗi nặng nhất>
```

## Vì sao 7 tiêu chí này

Ba cái đầu (gate) đo *có đúng cái `uat` hứa không*: đúng artifact + đọc-được-3-tầng + không bịa. Bốn cái sau đo *có đúng kỷ luật pipeline không*: đủ-là-đủ, traceability nối hai đầu, cổng+phân vai, bàn giao. Gộp lại = toàn bộ hợp đồng của `uat`, không hơn. Chỉ thêm tiêu chí thứ 8 khi có một kiểu lỗi thật lặp lại mà 7 cái này không bắt được.
