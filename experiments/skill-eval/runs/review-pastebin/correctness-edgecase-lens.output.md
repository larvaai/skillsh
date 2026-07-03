# review-pastebin · correctness-edgecase-lens — OUTPUT (skill: review)

Tôi vào vai skill `review`. Phạm vi hẹp rồi, chế độ rõ (tìm case dữ liệu/thứ tự mà code chưa xử lý đúng), nên tôi chạy thẳng và báo cáo. Tôi đọc để tìm lỗ hổng, không đọc để hiểu — và chỉ báo cáo, không đề xuất fix (fix là việc của bước lập kế hoạch sau).

Một lưu ý quan trọng trước khi vào: bài Pastebin này chủ yếu là **tài liệu thiết kế** (README) cộng đúng một file code thật là `pastebin.py`. File code đó chỉ hiện thực phần **đếm lượt xem (analytics MapReduce)**, và cả bốn hàm lõi đều đang là thân rỗng (`pass`). Phần "sinh shortlink", "lưu SQL/Object Store", "đọc paste", "xoá paste hết hạn" chỉ tồn tại dưới dạng mô tả trong README, chưa có code. Vì vậy tôi tách rõ: gap trên **code thật** (`pastebin.py`) và gap trên **thiết kế mô tả** (README) — cái sau gắn nhãn "trong thiết kế" để bạn biết đó là lỗ hổng ý tưởng chứ chưa phải dòng code chạy sai.

```
PHẠM VI: Bài thiết kế Pastebin — README.md (thiết kế) + pastebin.py (code đếm lượt xem)
CHẾ ĐỘ: edge (đúng/sai + edge case) — soi qua bốn hướng: key trùng, TTL hết hạn, input rỗng/quá dài, race khi tăng view count
```

GAP TÌM ĐƯỢC

[Critical] pastebin.py · `HitCounts.extract_url` và `extract_year_month` (dòng 8–13, thân `pass`) — Hai hàm này trả về `None`. `mapper` (dòng 16) gọi chúng rồi `yield (period, url), 1` với `period=None, url=None`. Log line rỗng, sai định dạng, hoặc thiếu timestamp không có nhánh xử lý nào → mọi dòng đổ dồn vào một khoá `(None, None)`. Hậu quả: thống kê lượt xem hàng tháng ra sai bét (một cục rác) thay vì báo lỗi, mà đây chính là use case "Service tracks analytics" README hứa.

[Critical] README.md · phần sinh shortlink (dòng 121–147) — Thiết kế tạo url bằng `base_encode(md5(ip_address + timestamp))[:7]` rồi kiểm trùng bằng cách hỏi SQL. Nhưng khi phát hiện trùng, README chỉ nói "generates another url" (dòng 101) — cùng một `ip_address + timestamp` sẽ cho **cùng một MD5**, nên "sinh lại" mà không đổi đầu vào sẽ trùng vô hạn. Không nêu nguồn ngẫu nhiên bổ sung cho lần retry, cũng không đặt trần số lần thử. Hậu quả (trong thiết kế): với hai request cùng IP trong cùng mốc thời gian, tạo paste có thể lặp vô tận hoặc ghi đè — mất paste.

[Critical] README.md · check-rồi-ghi khi tạo paste (dòng 99–105) — "Kiểm url có trùng không" và "Ghi vào bảng pastes" là hai bước tách rời, không nói tới khoá hay giao dịch nguyên tử. Hai request song song cùng sinh ra một shortlink sẽ cùng thấy "chưa trùng" rồi cùng ghi. Đây đúng là kiểu race bạn dặn soi. Bảng có `PRIMARY KEY(shortlink)` (dòng 116) nên DB sẽ chặn bản ghi thứ hai, nhưng thiết kế không mô tả xử lý lỗi khoá trùng đó → request thua cuộc nhận lỗi thô hoặc mất paste đã lưu ở Object Store. Hậu quả (trong thiết kế): tạo paste thỉnh thoảng thất bại khi tải cao, hoặc rác mồ côi trong Object Store.

[Medium] README.md · TTL / xoá paste hết hạn (dòng 230–232) — Việc xoá dựa trên `expiration_length_in_minutes` (một khoảng thời gian, dòng 59/116), nhưng bảng lại **không có cột thời điểm hết hạn tuyệt đối**; chỉ có `created_at` và độ dài. Muốn biết paste hết hạn chưa phải tự cộng `created_at + length` lúc quét — README nói "scan cho entry có expiration timestamp cũ hơn hiện tại" mà timestamp đó không tồn tại sẵn trong schema. Thêm nữa, use case (dòng 21–23) nói mặc định "không hết hạn" — biểu diễn "không hết hạn" bằng giá trị nào trong cột `int NOT NULL` (0? một số rất lớn?) không được định nghĩa. Hậu quả (trong thiết kế): job xoá có thể hiểu nhầm paste "vĩnh viễn" (length=0) là "đã hết hạn ngay" và xoá oan, hoặc bỏ sót.

[Medium] README.md · đọc paste không kiểm hết hạn (dòng 166–174) — Luồng đọc chỉ kiểm "url có trong SQL không", nếu có thì lấy nội dung từ Object Store, không thì báo lỗi. Không có bước kiểm paste đã hết hạn chưa. Vì việc xoá là một job quét chạy định kỳ (không tức thời), sẽ có cửa sổ thời gian paste đã quá hạn nhưng chưa bị job xoá. Hậu quả (trong thiết kế): người dùng vẫn đọc được paste đáng lẽ đã hết hạn cho tới khi job dọn chạy — sai kỳ vọng "hết hạn".

[Medium] README.md · input rỗng / quá dài khi tạo paste (dòng 88–105, 152–154) — Tính toán dung lượng giả định "1 KB content per paste" và `paste_path varchar(255)`, nhưng luồng Write API không mô tả bất kỳ validate nào cho `paste_contents`: rỗng thì sao, vượt giới hạn kích thước thì sao, `expiration_length_in_minutes` âm hoặc phi số thì sao. Hậu quả (trong thiết kế): paste rỗng vẫn tốn một shortlink; paste khổng lồ phá vỡ giả định dung lượng/chi phí; expiration âm làm paste "hết hạn trong quá khứ" ngay khi tạo.

[Low] README.md · pseudocode `base_encode` (dòng 133–141) — Đoạn mẫu thiếu dấu `:` sau `while num > 0` (dòng 136) và với `num = 0` (ví dụ hash toàn 0) vòng lặp không chạy lần nào → trả chuỗi rỗng, không đủ 7 ký tự. Đây là pseudocode minh hoạ nên nhẹ, nhưng vẫn là một edge (đầu vào 0) không được xử lý.

[Low] pastebin.py · `steps` dùng `self.mr(...)` (dòng 40) — Trong `mrjob` bản mới, API là `MRStep(...)` chứ không phải `self.mr(...)`; cách này đã lỗi thời. Không phải lỗi đúng/sai theo bốn lăng kính bạn giao, nhưng nó khiến file khó chạy được thật để mà kiểm các gap trên — ghi lại để bạn quyết.

CÓ THỂ LÀ GAP (chưa chắc)

README.md · phân tích lượt xem đọc từ log Web Server (dòng 191–193) — MapReduce đếm hit từ log. Nếu tầng Cache/CDN phục vụ paste phổ biến (dòng 267) mà không ghi log về Web Server, các lượt đọc đó sẽ không được đếm. Cần xác nhận thêm: log dùng để đếm có bao gồm cả lượt phục vụ từ cache/CDN không?

README.md · độ dài shortlink so với không gian khoá (dòng 143) — Lấy 7 ký tự base62 cho 62^7 ≈ 3.5 nghìn tỷ giá trị, thừa cho 360 triệu link/3 năm. Nhưng vì key sinh từ MD5(IP+timestamp) chứ không phải cấp phát tuần tự, xác suất trùng (nghịch lý sinh nhật) cao hơn nhiều so với "còn chỗ trống". Cần xác nhận thêm: tỷ lệ va chạm kỳ vọng ở mức 360 triệu key có chấp nhận được với vòng retry ở trên không?

KHÔNG TÌM THẤY GAP

Phần REST API contract (dòng 149–189): hình dạng request/response cho tạo và đọc paste nhất quán, trường trả về khớp schema — không thấy lỗ hổng trong phạm vi bốn lăng kính.

Reducer đếm tổng (pastebin.py dòng 29–35): `sum(values)` cho mỗi khoá là đúng về mặt gộp — sai (nếu có) nằm ở khoá do mapper sinh, không ở bước cộng.

---

Gợi ý bước tiếp (bạn chọn):

- Có gap Critical (đếm view ra rác, sinh key trùng, race check-rồi-ghi). Bạn muốn tôi bàn giao sang bước lập kế hoạch để xếp thứ tự fix theo mức nghiêm trọng không?
- Có hai mục "có thể là gap" chưa rõ (log cache/CDN có được đếm không; tỷ lệ va chạm key). Bạn muốn tôi đào sâu một trong hai để xác nhận nó có thực sự là gap không?
- Hay bạn muốn tôi đổi lăng kính, chạy lại phạm vi này ở chế độ error (các đường lỗi khi SQL/Object Store fail) hoặc permission (paste ẩn danh, ai được đọc/xoá cái gì)?
