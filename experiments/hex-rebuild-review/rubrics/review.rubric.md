# Rubric — 7 tiêu chí chấm một artifact REVIEW

Mỗi tiêu chí 0/1/2. Chuẩn gốc: `review/SKILL.md` — vai "người cố tình phá" báo cáo trung thực, quy tắc evidence (`file · dòng/symbol · điều thiếu · hậu quả`), tách gap thật khỏi "có thể là gap", không nuốt gap nhỏ, không đề xuất fix, 3 chế độ edge/error/permission (tổng thể = cả ba theo thứ tự), format báo cáo Bước 3, định nghĩa mức Critical/Medium/Low, gợi ý Bước 4 theo kết quả. Rubric chỉ biến hợp đồng đó thành thước đo được — không thêm tiêu chuẩn mới.

Chuẩn đối chiếu khi artifact có claim về code: code gốc tại `/Users/uspro/Desktop/namnson/hex_agent`. Một claim "kiểm được" = người chấm mở đúng file/symbol được trỏ và thấy đúng điều được mô tả — không phải tin lời artifact.

## 1. PHẠM VI & BA TRỤC — soi đúng cái đã khai, không sót trục

Hợp đồng: Bước 0 khai đối tượng + ngữ cảnh; "review tổng thể" = chạy đủ edge → error → permission.

- 0 — không khai phạm vi/chế độ ở đầu báo cáo; hoặc tuyên "tổng thể" nhưng có trục (edge, error, hoặc permission) không xuất hiện gap nào lẫn không được ghi nhận "đã soi, thấy ổn" — tức trục đó bị bỏ trắng.
- 1 — phạm vi + chế độ có khai nhưng một trục soi mỏng (chỉ 1 câu chiếu lệ, không có câu hỏi "điều gì xảy ra nếu" nào cho trục đó), hoặc báo cáo trôi ra ngoài phạm vi đã khai (soi thứ không thuộc đối tượng).
- 2 — phạm vi + chế độ khai rõ ngay đầu; mỗi trục trong chế độ đã chọn đều có kết quả kiểm được: hoặc gap cụ thể, hoặc mục "đã soi, thấy ổn" nêu đích danh phần đã kiểm.

## 2. BẰNG CHỨNG — mọi neo & con số kiểm được, không bịa (xương sống)

Hợp đồng: "Mỗi gap tìm được phải có evidence: `file · dòng/symbol · điều thiếu · hậu quả`."

- 0 — có claim bịa: neo tới file/symbol/dòng không tồn tại trong nguồn được trỏ; mô tả cơ chế ngược với code gốc tại `/Users/uspro/Desktop/namnson/hex_agent` khi đối chiếu; hoặc con số tổng hợp không khớp thân bài (đếm "12 gap / 3 Critical" nhưng danh sách liệt kê số khác). Bất kỳ một claim bịa nào → tiêu chí này 0.
- 1 — mọi claim đối chiếu đều đúng, nhưng 1–2 gap neo thiếu độ phân giải (chỉ tên file/artifact, không có dòng/symbol/mục cụ thể), hoặc 1 claim không kiểm được mà không gắn nhãn "chưa chắc".
- 2 — mỗi gap đủ bộ `file · dòng/symbol · điều thiếu · hậu quả`; chọn xác suất 3 neo bất kỳ đối chiếu nguồn đều khớp; mọi con số trong phần tóm tắt/cổng khớp đúng danh sách chi tiết.

## 3. KỊCH BẢN PHÁ — mỗi gap trả lời trọn "điều gì xảy ra nếu" (xương sống)

Hợp đồng: review đóng vai người cố tình phá — gap không phải lo ngại chung chung mà là đường phá dựng lại được.

- 0 — có gap mức Critical không nêu được kịch bản fail cụ thể (điều kiện kích hoạt + chuỗi diễn biến + hậu quả quan sát được); hoặc từ 1/3 tổng số gap trở lên chỉ là tính-từ-lo-ngại ("chưa đủ robust", "nên xử lý lỗi tốt hơn") không chỉ ra được điểm hỏng.
- 1 — mọi gap có điều-thiếu + hậu quả, nhưng vài kịch bản còn mơ hồ: hậu quả nêu chung ("có thể gây lỗi") không nói lỗi gì xảy ra với ai, hoặc điều kiện kích hoạt không dựng lại được từ mô tả.
- 2 — mỗi gap dựng lại được như một ca kiểm thử: input/state/sequence kích hoạt cụ thể → vì sao cơ chế hiện tại không chặn → hậu quả quan sát được; người đọc tái hiện được kịch bản mà không cần hỏi thêm.

## 4. THẬT vs NGHI — tách nhãn rõ, trung thực hai chiều

Hợp đồng: "Tách gap thực sự khỏi 'có thể là gap' — gắn nhãn rõ" + "Không bỏ qua gap chỉ vì nhỏ" + format có mục KHÔNG TÌM THẤY GAP.

- 0 — nghi ngờ được trình như khẳng định (suy đoán không có evidence chống lưng nằm chung danh sách gap thật, không nhãn); hoặc chiều ngược lại: chỉ báo gap to, không có chỗ cho gap nhỏ lẫn vùng-đã-soi-thấy-ổn — người đọc không phân biệt được "chưa soi" với "soi rồi, sạch".
- 1 — có tách hai mục nhưng ranh giới mờ: 1–2 mục "có thể là gap" thiếu câu hỏi cần-xác-nhận, hoặc 1 gap trong danh sách thật thực chất là suy đoán chưa kiểm.
- 2 — ba vùng rạch ròi: gap thật (có evidence), "có thể là gap" (kèm đúng câu hỏi cần xác nhận thêm), và vùng đã kiểm thấy ổn nêu đích danh; gap nhỏ vẫn được ghi để người dùng quyết.

## 5. PHÂN MỨC — Critical/Medium/Low theo đúng định nghĩa hợp đồng

Hợp đồng: Critical = lỗi production / mất data / security breach; Medium = hành vi sai trong case cụ thể, không crash; Low = thiếu sót nhỏ / UX / inconsistency.

- 0 — có gap gán mức ngược định nghĩa nghiêm trọng: hậu quả là mất data/security breach nhưng không xếp mức cao nhất, hoặc inconsistency thuần cosmetic xếp Critical; hoặc gap không được phân mức.
- 1 — đa số đúng mức nhưng 1–2 gap lệch một bậc so với hậu quả chính nó mô tả, hoặc dùng thang tự chế mà không nêu cách ánh xạ về thang hợp đồng.
- 2 — mỗi gap gán mức mà chính hậu quả nêu trong gap biện minh được theo định nghĩa hợp đồng; nếu dùng bậc trung gian thì khai rõ ánh xạ; đọc mức là đoán được loại hậu quả và ngược lại.

## 6. DÙNG ĐƯỢC NGAY — người nhận xếp được việc, bước tiếp đúng kết quả (xương sống)

Hợp đồng: Bước 4 — gợi ý theo kết quả (có Critical → đề nghị lên kế hoạch fix theo ưu tiên; có nghi-ngờ → đề nghị đào sâu xác nhận; sạch → đề nghị phần khác).

- 0 — đọc xong dev/CTO/PO không biết bắt đầu từ đâu: gap không xếp ưu tiên, không địa chỉ xử lý, không bước tiếp; hoặc bước tiếp mâu thuẫn kết quả (có Critical mà kết luận "ổn, ship được" không điều kiện); hoặc trỏ sang skill/nơi xử lý không tồn tại trong hệ.
- 1 — có ưu tiên + bước tiếp nhưng chung chung ("nên fix sớm", "cần chú ý") — không nói gap nào đóng trước, đóng ở đâu; hoặc bước tiếp chỉ phủ một phần kết quả (quên nhánh cho các gap không-Critical hoặc cho mục nghi-ngờ).
- 2 — mỗi gap có địa chỉ xử lý cụ thể; thứ tự làm suy ra được thẳng từ mức + hậu quả; bước tiếp khớp từng nhánh kết quả theo Bước 4; người nhận lập được danh sách việc ngay mà không phải đọc lại nguồn.

## 7. ĐÚNG VAI — báo cáo, không fix hộ, không lấn skill khác

Hợp đồng: "Không đề xuất fix — chỉ báo cáo những gì tìm thấy"; fix là việc của skill build. Review cũng không dạy-hiểu (explain), không phán giữ/xoá file (triage), không dựng bản đồ (atlas).

- 0 — viết code fix, viết spec giải pháp chi tiết thay chỗ skill build, hoặc phần lớn nội dung là giải thích-cho-hiểu / phán số phận file thay vì tìm lỗ hổng.
- 1 — chủ yếu đúng vai nhưng lấn nhẹ: mô tả hướng sửa vượt mức trỏ-việc (đi vào thiết kế cơ chế thay thế) ở một vài gap, hoặc chen đoạn giảng giải dài không phục vụ việc chỉ ra lỗ hổng.
- 2 — thuần báo cáo: gap + evidence + hậu quả + nơi xử lý; mọi việc sửa được bàn giao đúng skill có thật, ranh giới với explain/triage/atlas giữ sạch.

## Luật gate (tiêu chí xương sống)

Tiêu chí 2, 3, 6 là xương sống. Bất kỳ cái nào = 0 → artifact **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 12/14 nhưng có một neo bịa (tiêu chí 2 = 0) vẫn rớt — vì một gap bịa làm người đọc nghi ngờ cả 11 gap thật còn lại, và review sống bằng lòng tin vào evidence. Một bản neo chuẩn nhưng gap Critical không có kịch bản phá (tiêu chí 3 = 0) cũng rớt — danh sách lo-ngại không kiểm được thì không phải review, là đoán. Gate quan trọng hơn tổng: khi so nhiều bản, loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Vì sao 7 tiêu chí này

Ba cái đầu tiên của lõi nghề review: soi đúng chỗ đã hứa (1), nói có sách (2), phá có kịch bản (3) — đây là *review có tìm được lỗ hổng thật không*. Hai cái giữa đo *báo cáo có trung thực và cân đúng không* (4 tách thật/nghi, 5 phân mức) — sai ở đây thì gap thật cũng dẫn tới quyết định sai. Hai cái cuối đo *artifact có sống được sau khi rời tay người viết không* (6 dùng được ngay, 7 đúng vai — không giẫm chân skill khác trong pipeline). Gộp lại = toàn bộ hợp đồng của `review/SKILL.md`, không hơn. Thêm tiêu chí thứ 8 chỉ khi có một kiểu lỗi thật lặp lại mà 7 cái này không bắt được.
