# Rubric — chấm một bản chạy skill `stack` (GĐ7 · Tech Stack / Framework Selection)

7 tiêu chí, mỗi cái **0 / 1 / 2**. Chuẩn gốc để chấm = `stack/SKILL.md` + `quy-trinh-idea-to-operate.md` mục "## Giai đoạn 7 —". Rubric KHÔNG thêm tiêu chuẩn mới; chỉ biến hợp đồng đó thành thước đo. Ba tiêu chí **1, 2, 3 là XƯƠNG SỐNG (gate)**.

**Đầu vào để chấm (fixture):** bộ artifact stack (Tech Decision Matrix + ADR chọn framework, + Spike Result nếu có) cần chấm · Architecture Brief GĐ6 + Domain/NFR làm nguồn · tiêu chí fit domain/team/scale/NFR

## 1. ĐÚNG + ĐỦ ARTIFACT — Matrix + ADR (+ Spike) (xương sống)

Có đủ artifact GĐ7 đã liệt kê: Tech Decision Matrix **có điểm** (mỗi hạng mục rủi ro cao 1 bảng có điểm × trọng số + TỔNG + dòng Chọn/Lý do/Đã loại) + ADR (có phương án đã loại) cho mỗi lựa chọn lớn (+ Spike Result nếu ẩn số rủi ro cao).

- 0 — thiếu artifact cốt lõi: không có ma trận, HOẶC ma trận không có ĐIỂM (chỉ liệt kê candidate, "chọn NestJS vì hot"), HOẶC thiếu ADR cho lựa chọn lớn, HOẶC ẩn số NFR rủi ro cao mà không spike thực đo cũng không nêu lý do bỏ.
- 1 — có Matrix + ADR nhưng khuyết một mảnh: thiếu "đã loại & vì sao", hoặc spike nêu mà không có số đo, hoặc thiếu 1 hạng mục rủi ro cao đáng ra phải có ma trận.
- 2 — đủ: ma trận có điểm × trọng số ≥2 candidate + ADR (quyết định/bối cảnh/đã loại/hệ quả) + spike thực đo cho ẩn số rủi ro cao (hoặc ghi rõ vì sao không cần).

## 2. ĐỌC-ĐƯỢC 3 TẦNG — lãnh đạo + dev (xương sống)

Artifact MỞ bằng "Góc nhìn lãnh đạo" (chọn gì / vì sao / loại gì / rủi ro-chi phí, ngôn ngữ nghiệp vụ, KHÔNG bắt CEO đọc điểm số), RỒI mới tới ma trận điểm + ADR đủ để dev hành động. 1 trang, scan 2–3 phút.

- 0 — đổ thẳng ma trận/jargon lên đầu, không có băng lãnh đạo; HOẶC lãnh đạo đọc đầu vẫn không duyệt được; HOẶC dev thiếu thông tin dựng skeleton; HOẶC quá kỹ thuật để scan trong 2–3 phút.
- 1 — có cả hai tầng nhưng lệch: góc lãnh đạo còn lẫn jargon / phải lội kỹ thuật, hoặc dev thiếu 1 mảnh (stack cụ thể / hệ quả / spike).
- 2 — băng lãnh đạo 30 giây duyệt được trên niềm tin (quản được quyết định & chi phí) + dev có đủ điểm/ADR/spike để bắt tay dựng slice; gọn 1 trang. Mục "Tự soi trước khi chốt" được tôn trọng.

## 3. BÁM NGUỒN — dùng Architecture Brief GĐ6, không bịa (xương sống)

Danh sách candidate + trọng số tiêu chí neo vào **Architecture Brief (GĐ6)** thật (style / boundary / integration / auth / NFR có số) và Domain/NFR GĐ2–5. Chạy SAU khi có kiến trúc; không tự chế kiến trúc; không ràng buộc bịa. Nguồn hợp lệ = artifact GĐ trước ĐÃ qua cổng HOẶC input ngoài user cung cấp (prompt/file) KÈM cảnh báo ⚠️; dùng input ngoài mà THIẾU cảnh báo → trừ điểm (không minh bạch nguồn); vẫn CẤM bịa cái user không đưa.

- 0 — chọn stack khi CHƯA có/không đọc Architecture Brief (không dừng/bàn giao ngược `/shape`); HOẶC tiêu chí/ràng buộc/số spike bịa không truy được; HOẶC mâu thuẫn shape (đổi style/boundary).
- 1 — bám GĐ6 phần lớn, 1 chỗ tự suy ra ràng buộc/NFR không có trong Brief và không gắn nhãn.
- 2 — mọi trọng số & candidate & điểm truy ngược được về một dòng trong Brief/NFR/Domain; thiếu shape thì dừng đúng, bàn giao ngược `/shape`; chỗ chưa chắc gắn nhãn.

## 4. ĐỦ-LÀ-ĐỦ — độ sâu tỉ lệ rủi ro, không thủ tục thừa

- 0 — một cỡ cho mọi hạng mục: bắt ma trận 8 dòng + spike cho lựa chọn hiển nhiên (thừa), HOẶC việc rủi ro cao mà chỉ 1 dòng qua loa / không spike ẩn số hiệu năng (thiếu).
- 1 — có phân biệt nhưng độ sâu hơi lệch rủi ro ở 1 hạng mục (cầu toàn chỗ nhỏ, hoặc hời hợt chỗ rủi ro).
- 2 — độ sâu khớp rủi ro: hạng mục đã bị ràng buộc ép → ghi 1 dòng lý do; hạng mục lớn/rủi ro cao → đầy đủ + spike. Luôn còn matrix + ADR; không bỏ bước, chỉ rút gọn; "đang hot/quen tay" không dùng làm lý do.

## 5. TRACEABILITY — nối GĐ trước ↔ sau

Mỗi lựa chọn có Lý do + phương án đã loại (audit được). Đầu vào trỏ rõ Architecture Brief GĐ6; đầu ra nêu ràng buộc kéo theo / ẩn số còn treo cho GĐ8.

- 0 — chọn stack không lý do / không nêu cái đã loại; không nối GĐ6 (không tham chiếu shape) hay GĐ8 (không nói bê gì sang); ADR treo lơ lửng.
- 1 — có nối một chiều (nhận từ shape HOẶC giao sang skeleton, thiếu chiều kia), hoặc có lý do nhưng thiếu phương án đã loại.
- 2 — rõ hai chiều: ràng buộc từ Architecture Brief dẫn vào từng lựa chọn; mỗi quyết định có lý do + đã loại + hệ quả; nêu NFR/mục tiêu spike + open question cần lát cắt GĐ8 chứng minh.

## 6. CỔNG + PHÂN VAI ĐÚNG (A5)

Cổng đúng câu doc (*"Stack đã chốt, sẵn sàng dựng live slice chưa?"*) + AI duyệt vai **CTO** theo A5, rà đủ điều kiện trước khi cho qua; skill không tự tuyên GO thay CTO; không lấn vai (vẽ lại kiến trúc GĐ6 / viết code GĐ8 / chọn hộ sprint GĐ9).

- 0 — không có cổng go/no-go, HOẶC tự cho qua khi thiếu (matrix không điểm / thiếu ADR / ẩn số chưa đo) mà vẫn "duyệt", HOẶC AI tự quyết GO thay CTO, HOẶC lấn vai.
- 1 — có cổng nhưng điều kiện duyệt lỏng / rà thiếu một điều, hoặc phân vai mờ (sai người duyệt), hoặc lấn vai nhẹ.
- 2 — cổng đúng câu + đúng người duyệt (CTO) + rà đủ (ma trận có điểm / ADR có cái đã loại / spike cho ẩn số cao / lựa chọn trong ràng buộc Brief) + skill chỉ chuẩn bị, không quyết thay, không lấn GĐ6/8/9.

## 7. BÀN GIAO — đúng skill kế

Khối bàn giao trỏ `skeleton` (GĐ8) là mạch chính; liệt kê `partner` / `frame` / đường lui về `shape`; nêu stack đã chốt + ràng buộc/ẩn số còn treo; chỉ liệt kê, KHÔNG tự chọn hộ. Ghi state vào vùng skill, không vào repo code trừ khi user đồng ý.

- 0 — không có khối bàn giao, HOẶC bàn giao sai skill (đẩy thẳng backlog/delivery, tự nhảy code), HOẶC tự chọn hộ, HOẶC ghi vào repo không hỏi.
- 1 — có bàn giao nhưng thiếu skeleton là mạch chính, hoặc thiếu stack đã chốt / ẩn số treo, hoặc thiếu đường lui về `shape`.
- 2 — trỏ đúng skeleton (GĐ8) là đường chính + partner/frame + lui `/shape` khi cần; nêu stack đã chốt + ràng buộc/ẩn số treo; chỉ liệt kê để user quyết; state đúng vùng skill.

## Luật gate

Tiêu chí **1, 2, 3** là xương sống. Bất kỳ cái = **0** → bản **RỚT GATE**, ghi rõ rớt ở đâu, dù TỔNG cao. Bản 12/14 nhưng chọn stack theo "hot" không điểm (tiêu chí 1 = 0), hoặc chọn khi chưa có kiến trúc (tiêu chí 3 = 0), vẫn rớt — vì lãnh đạo sẽ duyệt nhầm và dev dựng nhầm nền. So nhiều bản: loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Khung report (cố định — để xếp nhiều bản cạnh nhau)

```
BẢN: <id>
Gate: 1 Artifact [P/F] · 2 Đọc-3-tầng [P/F] · 3 Bám nguồn [P/F]  → <ĐẠT/RỚT>
Điểm: 1:_ 2:_ 3:_ 4:_ 5:_ 6:_ 7:_  = _/14
Rớt ở (nếu có): <tiêu chí xương sống + lý do 1 dòng>
Mạnh nhất: <1 dòng>   Yếu nhất / sửa 1 điều đáng nhất: <1 dòng>
```
Xếp hạng: bản ĐẠT gate trước, trong đó tổng cao hơn đứng trên; bản RỚT gate xếp cuối bất kể tổng.

## Vì sao các tiêu chí này

Ba tiêu chí gate đo *có ra đúng thứ + đọc được + trung thực không*; các tiêu chí sau đo *có đúng kỷ luật pipeline không* (đủ-là-đủ, không lấn vai, cổng/traceability, bàn giao). Gộp lại = trọn hợp đồng của `stack`, không hơn. Thêm một tiêu chí mới chỉ khi có một kiểu lỗi thật lặp lại mà bộ hiện tại không bắt được.
