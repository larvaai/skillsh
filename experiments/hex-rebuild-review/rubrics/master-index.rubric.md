# Rubric — 7 tiêu chí chấm Master Index (`rebuild-hex-agent/README.md`)

Mỗi tiêu chí 0/1/2. Chuẩn gốc là **hợp đồng cửa-vào** của Master Index: (a) quy ước **đọc-được-3-tầng** do chính README tuyên, (b) vai trò **cửa vào** — mọi link phải đúng, bảng trạng thái phải khớp nội dung thật của từng artifact được link, (c) **trung thực trạng thái** — không thổi phồng, không giấu treo. Rubric chỉ biến hợp đồng đó thành thước đo được — không thêm chuẩn mới, không chép tiêu chí của explain sang.

Cách kiểm: mở từng link trên filesystem; đối chiếu từng con số/claim với chính file được link. Claim về hành vi bản gốc đối chiếu code tại `/Users/uspro/Desktop/namnson/hex_agent`.

## 1. LINK & ĐỘ PHỦ — mọi cửa đều mở, mọi artifact đều có mặt (xương sống)

- 0 — ≥1 link trỏ tới file không tồn tại (link chết), hoặc có artifact nội-dung trong gói mà cây index không nhắc tới (file mồ côi — người đi từ cửa vào không bao giờ tìm thấy nó). Bất kỳ link chết nào → tiêu chí này 0.
- 1 — mọi link sống, nhưng độ phủ hụt nhẹ: thiếu link cho 1 artifact phụ, hoặc nhóm file máy-đọc (state JSON…) tồn tại mà không được nhắc là có.
- 2 — mọi link sống; mọi artifact người-đọc có link riêng kèm một dòng mô tả; file máy-đọc được nhắc gộp và nói rõ ai cần đọc; đường dẫn tương đối đúng để click được từ vị trí của README.

## 2. KHỚP BẢNG–ARTIFACT — mọi con số & claim có nguồn kiểm được (xương sống)

Mỗi con số/claim trong README (bảng trạng thái, mô tả từng link, đoạn góc-nhìn-lãnh-đạo) phải khớp nội dung thật của artifact được link; claim về code gốc phải khớp `/Users/uspro/Desktop/namnson/hex_agent`.

- 0 — ≥1 claim sai hoặc bịa: con số trong README khác con số trong artifact nguồn (ví dụ README ghi "26/28 PASS" mà file UAT ghi số khác, "12 gap · 3 Critical" mà file review đếm khác), mô tả link nói file chứa thứ nó không có, trạng thái cổng trong bảng khác kết luận trong file giai đoạn đó, hoặc claim về code gốc không đúng code. Bất kỳ claim bịa/sai số nào → tiêu chí này 0.
- 1 — mọi con số đúng, nhưng 1–2 chỗ diễn đạt mơ hồ không trace thẳng được về nguồn, đủ khiến người đọc suy ra lệch.
- 2 — mọi số & claim trace được về đúng artifact hoặc code gốc; trạng thái cổng khớp từng giai đoạn; chỗ ước lượng/chưa chắc được gắn nhãn là ước lượng.

## 3. TRUNG THỰC TRẠNG THÁI — không thổi phồng, không giấu treo (xương sống)

- 0 — có thổi phồng hoặc giấu treo: gọi gói/pipeline là "hoàn chỉnh / xong / chạy được" mà không kèm giới hạn ngay tại chỗ nói; nâng cổng có-điều-kiện thành GO sạch; một mục treo có thật trong artifact con (spike treo, tick 0/N, PENDING, điều kiện kèm GO, milestone chưa tuyên) không xuất hiện trong README hoặc chỉ nằm chỗ người-đọc-nhanh không bao giờ tới.
- 1 — trạng thái đúng và đủ nhưng phần treo bị nói nhẹ hoặc đặt sau phần khen: người đọc 90 giây có thể ra về lạc quan hơn thực tế một bậc.
- 2 — mọi mục treo hiện ngay ở tầng đọc-nhanh; GO nào có điều kiện thì điều kiện đứng cạnh chữ GO; có câu gọi thẳng tên "thiếu lớn nhất" và nói phần thiếu đã được đổ về đâu để xử tiếp.

## 4. ĐỌC-ĐƯỢC-3-TẦNG — chính README giữ quy ước nó tuyên

- 0 — không có tầng lãnh đạo đứng đầu file, hoặc tầng đó dày jargon code (tên hàm/file/framework chưa được neo) khiến người không biết code đọc không nổi; hoặc README tuyên quy ước 3 tầng mà chính nó vi phạm.
- 1 — có tầng đọc-nhanh nhưng dài quá mức 90-giây nó hứa, lẫn thuật ngữ chưa neo, hoặc ranh giới các tầng mờ.
- 2 — tầng lãnh đạo tự đứng được: đọc xong nắm hệ-là-gì, giải-nhu-cầu-gì, trạng-thái-thật mà không cần biết code; thuật ngữ kỹ thuật chỉ vào từ tầng dưới hoặc được neo bằng lời thường trước khi dùng; quy ước 3 tầng được tuyên rõ để artifact con theo.

## 5. DẪN ĐƯỜNG THEO VAI — mỗi người nhận biết đi đâu ngay

- 0 — không có mục "cách đọc theo vai", hoặc trỏ sai cửa cho vai (dev bị dẫn vào tài liệu chiến lược, lãnh đạo bị dẫn vào contract kỹ thuật).
- 1 — có đường đọc theo vai nhưng thiếu vai chính (lãnh đạo / CTO-kiến trúc / dev), hoặc chỉ liệt kê file mà không có thứ tự đọc kèm lý do.
- 2 — mỗi vai chính có đường đọc cụ thể tới đúng file với thứ tự có nghĩa; riêng dev, chỉ từ mục này đã cầm đủ bộ bắt-tay-làm: slice được đóng khung + contract module + chuẩn Done.

## 6. BẢNG TRẠNG THÁI ĐỌC MỘT PHÁT — vị trí pipeline scan được

- 0 — không có bảng trạng thái theo giai đoạn; hoặc bảng bỏ sót giai đoạn đã có artifact; hoặc dùng ký hiệu không chú giải khiến bảng không tự đọc được.
- 1 — bảng đủ giai đoạn nhưng thiếu chú giải ký hiệu, hoặc thiếu câu "đang đứng ở giai đoạn nào / cổng nào đắt nhất".
- 2 — đủ mọi giai đoạn, mỗi giai đoạn một dòng (artifact + trạng thái cổng + ghi chú ngắn); ký hiệu có chú giải; nêu rõ đang ở đâu và cổng đắt nào chưa qua — nhìn 10 giây ra được bức tranh.

## 7. ĐÚNG VAI CỬA-VÀO — trỏ, không làm thay

- 0 — README thành nguồn chân lý thứ hai: chép lại nguyên khối nội dung của artifact con (sẽ lệch khi artifact con đổi), hoặc chứa quyết định/thiết kế mới không tồn tại trong bất kỳ artifact nào.
- 1 — chủ yếu trỏ, nhưng có 1–2 đoạn sa vào chi tiết lẽ ra thuộc artifact con.
- 2 — mỗi artifact một dòng tóm + link; phần ruột riêng của README chỉ là tổng hợp trạng thái + điều hướng; mọi ý trong README đều có nguồn là một artifact trong gói hoặc code gốc.

## Luật gate

Tiêu chí 1, 2, 3 là xương sống. Bất kỳ cái nào = 0 → Master Index **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Vì đây là cửa vào cả gói: link chết làm người nhận lạc ngay từ cửa (1); số sai hay claim bịa ở cửa làm người đọc tin nhầm cả gói — không ai đối chiếu lại từng artifact sau khi đã tin trang đầu (2); thổi phồng hay giấu treo ở cửa là chỗ nguy hiểm nhất để dối, vì CTO/PO quyết đi-tiếp-hay-dừng dựa trên chính trang này (3). Một bản 12/14 nhưng có một con số không khớp artifact nguồn (tiêu chí 2 = 0) vẫn rớt. Khi so nhiều bản: loại hết bản rớt gate trước, rồi mới xếp theo tổng /14.

## Vì sao 7 tiêu chí này

Ba cái đầu đo *cửa vào có tin được không* (mở được, khớp bằng chứng, trung thực) — đúng ba mệnh đề của hợp đồng Master Index. Bốn cái sau đo *cửa vào có dùng được không* (giữ quy ước 3 tầng nó tự tuyên, dẫn đúng người vào đúng cửa, trạng thái scan một phát, và chỉ trỏ chứ không mọc thành nguồn chân lý thứ hai). Gộp lại = trọn hợp đồng cửa-vào, không hơn: không chép 7 tiêu chí của explain, không thêm chuẩn ngoài hợp đồng. Thêm tiêu chí thứ 8 chỉ khi xuất hiện một kiểu lỗi thật lặp lại mà 7 cái này không bắt được.
