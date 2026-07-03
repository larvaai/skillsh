# Rubric — 7 tiêu chí chấm một artifact `07-stack` (Tech Decision, GĐ7)

Mỗi tiêu chí 0/1/2. Chuẩn gốc: `.claude/skills/stack/SKILL.md` — mục "Luật cứng", template Tech Decision Matrix / ADR / Spike Result, khối "Góc nhìn lãnh đạo", "Tự soi trước khi chốt" và "Cổng go/no-go + Bàn giao". Rubric chỉ biến hợp đồng đó thành thước đo được — không thêm tiêu chuẩn mới, không mượn tiêu chí của skill khác.

Chuẩn đối chiếu cho claim về code gốc (gói `rebuild-hex-agent`): repo `/Users/uspro/Desktop/namnson/hex_agent`. Mọi câu kiểu "gốc dùng X", "gốc có N test", "gốc đã chạy resume được" phải kiểm lại được ở repo đó — trực tiếp, hoặc qua anchor `file:line` của evidence artifact trỏ về nó và trỏ ĐÚNG.

## 1. BẰNG CHỨNG — mọi con số & claim có nguồn kiểm được, không bịa, không tự khen (xương sống)

Áp cho: ô điểm ma trận, con số NFR, claim về stack/hành vi của code gốc, kết quả spike, các dấu ✔ ở phần cổng và mục "Tự soi".

- 0 — có claim bịa hoặc tự khen không bằng chứng: một con số không nguồn (NFR, số test, số đo hiệu năng); một "kết quả spike" chưa chạy nhưng trình bày như đã đo thật; một claim về code gốc sai khi đối chiếu `hex_agent` (hoặc anchor `file:line` trỏ sai chỗ); tự tuyên "đạt / PASS / ✔" cho điều chưa có bằng chứng kèm theo. Bất kỳ MỘT chỗ như vậy → tiêu chí này 0.
- 1 — đúng phần lớn nhưng còn 1–2 chỗ suy đoán/mơ hồ không gắn nhãn: ô điểm không giải thích được từ đâu ra, claim "gốc đã chạy được X" không có anchor, kết luận "rủi ro thấp" không dẫn về đâu.
- 2 — mọi số & claim truy về được nguồn (`file:line` của evidence, artifact GĐ trước, hoặc code gốc); số chưa có (vd NFR) → ghi open-Q rõ ràng chứ không điền đại; spike chưa chạy ghi rõ CHƯA CHẠY / TREO kèm địa chỉ sẽ đo, tuyệt không tính vào cột "đã đo".

## 2. MA TRẬN CÓ ĐIỂM — quyết định bằng điểm truy vết được, không theo "đang hot" (xương sống)

Đây là lý do skill `stack` tồn tại: "không có điểm số thì không phải quyết định, chỉ là ý thích".

- 0 — có hạng mục MỞ (Architecture Brief chưa ép sẵn) mà không có ma trận, hoặc ma trận không có điểm / không có trọng số; hoặc TỔNG tính lại bị sai đến mức đổi thứ hạng candidate; hoặc lý do chọn nêu ra không neo vào tiêu chí nào ("đang hot", "quen tay" đứng trần trụi thay vì hiện thành điểm của một tiêu chí như Fit team).
- 1 — đủ ma trận điểm + trọng số + TỔNG cho các hạng mục mở, nhưng: vài ô điểm không truy về được ràng buộc/NFR/team; trọng số không có lý do; TỔNG lệch nhỏ không đổi kết luận; hoặc mở ma trận giả / bịa candidate cho đủ cột ở hạng mục đã bị ràng buộc ép (lệch "Đủ-là-đủ").
- 2 — mỗi hạng mục mở có bảng: tiêu chí × trọng số × điểm từng candidate + TỔNG đúng số học + dòng "Chọn / Lý do / Đã loại"; trọng số có lý do neo về ràng buộc kiến trúc + NFR + rủi ro (ghi ra để truy vết); hạng mục bị ràng buộc ép → ma trận gọn hoặc 1 dòng "chọn X vì Y", không bảng giả.

## 3. ADR ĐỦ MẢNH — mỗi quyết định lớn có Bối cảnh · Quyết định · Lý do · Đã loại · Hệ quả, phản biện mềm

- 0 — có quyết định lớn không có ADR; hoặc ADR không có mục "Đã loại"; hoặc dùng câu phủ định cứng khi loại candidate ("X sai", "không dùng được") — luật cấm kế thừa từ `partner`.
- 1 — đủ ADR cho mọi quyết định lớn nhưng 1–2 bản còn hụt: thiếu Hệ quả hoặc Bối cảnh; Lý do không neo về tiêu chí thắng điểm trong ma trận; candidate bị loại chỉ có điểm yếu, không được ghi nhận điểm mạnh hay điều kiện đảo chiều.
- 2 — mỗi lựa chọn lớn đúng 1 ADR đủ 5 mảnh; "Đã loại" nêu thua-ở-tiêu-chí-nào + điểm mạnh thật của nó + điều kiện/ngưỡng đảo chiều ("hợp nếu…", "bật lại khi…"); "Hệ quả" nêu ràng buộc kéo theo (hiring, license, vendor-lock, migration path) — CTO đọc ADR là biết vì sao stack có mặt này mà không cần đọc code.

## 4. SPIKE CHO ẨN SỐ — rủi ro cao thì đo thật, không đoán; không spike thì ghi vì sao

- 0 — có ẩn số rủi ro cao (bảng điểm dựa trên giả định chưa chứng minh, NFR chưa chắc đạt, công nghệ mới với đội) bị bỏ qua: không spike, không lý do, quyết định vẫn khoá cứng trên đoán.
- 1 — nhận diện được ẩn số và có spike, nhưng thiếu một mảnh: không time-box, tiêu chí đạt không đo được bằng số/hành vi quan sát được, hoặc không có điều-kiện-đảo-chiều khi spike fail; hoặc các hạng mục quen không có nổi 1 dòng "không spike vì…".
- 2 — mỗi ẩn số rủi ro cao có SPIKE đủ: Câu hỏi cần chứng minh + Time-box + tiêu chí đạt đo được + Kết luận (hoặc trạng thái TREO kèm địa chỉ đo và điều kiện đảo chiều); hạng mục không spike có 1 dòng lý do ("stack quen, gốc đã chạy, ràng buộc ép sẵn"); không chỗ nào lấy đoán thay số đo.

## 5. GÓC NHÌN LÃNH ĐẠO — mở đầu 3 tầng đọc được, không jargon

- 0 — artifact không mở bằng khối Góc nhìn lãnh đạo (ma trận/ADR đứng trước); hoặc khối đầu thiếu ≥1 trong 4 mảnh: Chọn gì · Vì sao · Đã loại · Rủi ro/chi phí; hoặc viết dày jargon đến mức người không viết code không duyệt nổi.
- 1 — đủ 4 mảnh nhưng jargon kỹ thuật còn lọt lên phần "vì sao"/"rủi ro" (đáng lẽ hạ xuống phần kỹ thuật), hoặc dài vượt hẳn khung scan 30–60 giây.
- 2 — mở đầu đủ 4 mảnh bằng tiếng nghiệp vụ (lên nhanh/rẻ, nuôi được lâu, khoá vendor hay không, tốn gì khi sai); CEO/CTO đọc băng đầu là duyệt được lựa chọn trên niềm tin, không phải đọc điểm từng ô; chi tiết điểm số + kỹ thuật nằm phía dưới cho dev.

## 6. NEO KIẾN TRÚC + ĐÚNG VAI — mọi lựa chọn nằm trong ràng buộc GĐ6, không lấn sân

- 0 — có lựa chọn mâu thuẫn ràng buộc Architecture Brief GĐ6 (vd brief ép embedded relational làm chân lý resume mà chốt store khác vai); hoặc artifact vẽ lại style/boundary của kiến trúc; hoặc viết code sản phẩm; hoặc thiếu brief mà tự chế kiến trúc để chọn tool thay vì dừng/cảnh báo.
- 1 — nằm trong ràng buộc nhưng 1–2 hạng mục không chỉ ra được ràng buộc nào ép hay mở nó; hoặc bối cảnh brownfield/rebuild mà "Fit team" / "Fit maintainability" không tính stack đang tồn tại trong code gốc; hoặc lấn vai nhẹ (bàn lại scope, phân rã backlog, đặt chuẩn delivery).
- 2 — có nối mạch rõ: từng ràng buộc GĐ6 → ô tool phải chốt (ép tới đâu, mở chỗ nào); hạng mục bị ép ghi thẳng "chọn X vì ràng buộc Y"; rebuild thì Fit team/maintainability tính cả stack gốc, không xé lẻ vô cớ; nếu chọn tool làm lộ vấn đề kiến trúc → ghi open-Q trả ngược `/shape`, không tự vá.

## 7. BÀN GIAO DÙNG ĐƯỢC — dev cầm đi dựng skeleton ngay, không phải chọn lại (xương sống)

- 0 — thiếu khối cổng/bàn giao; hoặc ≥1 hạng mục mà Architecture Brief đòi chốt bị bỏ ngỏ — không quyết cũng không ghi open-Q; hoặc chốt mơ hồ đến mức không dựng được ("một web framework hiện đại", "DB quan hệ nào đó") khiến người nhận phải tự chọn lại.
- 1 — có khối bàn giao và stack cụ thể từng hạng mục, nhưng hụt một mảnh: thiếu "ràng buộc kéo theo"; ẩn số còn treo không có địa chỉ (đo ở đâu, tiêu chí đạt là gì, fail thì đảo chiều thế nào); hoặc cổng không rà đủ 4 điều kiện của hợp đồng (ma trận có điểm · ADR có phương án loại · spike hoặc lý do · nằm trong ràng buộc GĐ6).
- 2 — khối bàn giao đủ và hành động được: mỗi hạng mục → công cụ cụ thể (hoặc open-Q có địa chỉ); "ràng buộc kéo theo" nêu hiring/license/vendor/migration; ẩn số còn treo kèm nơi đo + điều kiện đảo chiều; cổng rà đủ 4 điều kiện rồi mới đặt câu hỏi cổng "Stack đã chốt, sẵn sàng dựng live slice chưa?"; đội dựng skeleton (GĐ8) bắt tay làm ngay không phải mở lại vòng chọn.

## Luật gate (tiêu chí xương sống)

Tiêu chí 1, 2, 7 là xương sống. Bất kỳ cái nào = 0 → artifact **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 12/14 nhưng điền một con số spike chưa hề đo (tiêu chí 1 = 0) vẫn rớt — vì GĐ8 sẽ dựng skeleton trên một con số ma. Một bản văn hay nhưng hạng mục mở không có điểm (tiêu chí 2 = 0) vẫn rớt — đó là ý thích, không phải quyết định. Gate quan trọng hơn tổng: khi so nhiều bản, loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Vì sao 7 tiêu chí này

Ba cái giữa (2, 3, 4) đo *quyết định có được làm đúng cách stack hứa không*: chọn bằng điểm có trọng số, mỗi quyết định lớn có ADR kèm phương án đã loại, ẩn số thì đo chứ không đoán. Hai cái (5, 6) đo *viết cho đúng người đọc và đứng đúng chỗ trong pipeline*: mở bằng tầng lãnh đạo, mọi lựa chọn neo về Architecture Brief GĐ6, không lấn vai shape/skeleton/frame. Hai cái còn lại (1, 7) đo *trung thực và trao tay được* — đầu vào của niềm tin (không bịa, không tự khen) và đầu ra của giá trị (dev/CTO cầm đi làm ngay). Gộp lại = toàn bộ luật cứng + cổng của `stack/SKILL.md`, không hơn. Thêm tiêu chí thứ 8 chỉ khi có một kiểu lỗi thật lặp lại mà 7 cái này không bắt được.
