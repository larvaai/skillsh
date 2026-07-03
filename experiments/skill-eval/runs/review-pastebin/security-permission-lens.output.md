# review-pastebin · security-permission-lens — OUTPUT (skill: review)

PHẠM VI: Bài thiết kế Pastebin — luồng tạo paste (Write API), luồng đọc paste (Read API), sinh shortlink, expiration, và analytics.
Nguồn đã đọc: `solutions/system_design/pastebin/README.md` và `solutions/system_design/pastebin/pastebin.py`.
CHẾ ĐỘ: permission (lăng kính bảo mật/quyền — paste riêng tư, expiration, lạm dụng, chống đoán URL)
Ngữ cảnh: bản thiết kế mẫu, rà trước khi coi là "đủ để ship".

Lưu ý: đây là tài liệu thiết kế (không phải code chạy được), nên hầu hết gap nằm ở tầng thiết kế — chỗ luồng chưa có nhánh xử lý quyền/lạm dụng. Mọi finding dưới đây đều trích đúng dòng trong file, không suy diễn ngoài văn bản.

GAP TÌM ĐƯỢC

  [Critical] README.md · dòng 146, khối "generate the unique url" (dòng 121–147) — Shortlink sinh từ `md5(ip_address + timestamp)` rồi cắt 7 ký tự đầu. Đây là hàm tất định (chính tài liệu nói ở dòng 129: "Base 62 is deterministic (no randomness involved)"), đầu vào lại đoán được: IP của người tạo + thời điểm tạo (độ phân giải giây/mili-giây là hữu hạn). → Kẻ tấn công biết (hoặc đoán hẹp) IP + khoảng thời gian có thể tái tạo hash và dò ra link của người khác. Với pastebin, link CHÍNH LÀ quyền đọc — không có tầng auth nào khác (account để "out of scope", dòng 32). Vậy toàn bộ mô hình bảo mật đặt lên một URL đoán được. Cần khoá riêng: dùng dữ liệu ngẫu nhiên thật (tài liệu chỉ nói "alternatively" ở dòng 126, không chốt), và không để đầu vào là thông tin quan sát được.

  [Critical] README.md · dòng 166–174 (Read API) — Luồng đọc chỉ có đúng một nhánh kiểm tra: "Checks the SQL Database for the generated url → nếu có thì fetch nội dung, else trả lỗi". KHÔNG có bước kiểm tra expiration khi đọc. → Một paste đã hết hạn nhưng chưa bị job dọn xoá vẫn còn dòng trong bảng `pastes` và vẫn còn nội dung trong Object Store, nên vẫn đọc được bình thường. Với người dùng đặt hạn để giới hạn thời gian lộ nội dung, đây là rò rỉ dữ liệu ngoài ý muốn. "Hết hạn" ở đây được xử lý như việc dọn rác nền, không phải như một cổng quyền lúc đọc.

  [Medium] README.md · dòng 230–232 (Service deletes expired pastes) — Cơ chế dọn hết hạn là "quét toàn bảng SQL tìm dòng có expiration cũ hơn hiện tại rồi xoá (hoặc đánh dấu)". Ba lỗ hổng cộng dồn: (1) không nêu tần suất quét → khoảng trống giữa hai lần quét là cửa sổ đọc lén paste đã hết hạn (gắn với Critical Read API ở trên); (2) "xoá HOẶC đánh dấu expired" bỏ ngỏ — nếu chỉ đánh dấu mà Read API (dòng 170–172) không đọc cờ đó thì việc hết hạn vô hiệu; (3) chỉ xoá dòng trong SQL, không nói xoá đối tượng trong Object Store (nội dung thật nằm ở đó theo dòng 104) → nội dung vẫn nằm lại, nếu đoán được đường dẫn `paste_path` thì vẫn lấy được.

  [Medium] README.md · dòng 88–106 (Write API) — Người dùng là ẩn danh (dòng 25) và luồng tạo paste không có bất kỳ chốt chống lạm dụng nào: không rate limit theo IP, không CAPTCHA, không giới hạn kích thước nội dung ở tầng nghiệp vụ (chỉ có giả định "1 KB mỗi paste" ở dòng 57, không phải ràng buộc bắt buộc), không quét nội dung độc hại/spam. → Một client có thể bơm paste không giới hạn (spam, host nội dung lạm dụng, làm phồng dung lượng Object Store vượt xa ước tính 12.7 GB/tháng ở dòng 265). Vì không có account, không có cách gắn trách nhiệm hay khoá người vi phạm.

  [Medium] README.md · dòng 99–102 (kiểm tra trùng shortlink) — Luồng kiểm tra trùng URL bằng cách tra SQL, "nếu trùng thì sinh URL khác", nhưng không nói kiểm-tra-rồi-ghi này có nguyên tử (atomic) không. → Hai write đồng thời cùng sinh ra một shortlink có thể cùng vượt qua bước check trước khi một trong hai kịp ghi, dẫn tới một paste ghi đè paste kia. Về quyền, đây là chuyện nghiêm trọng: người B có thể vô tình (hoặc cố ý, kết hợp với lỗ đoán URL ở Critical #1) chiếm shortlink và thay nội dung mà người A đang tin là của mình. `PRIMARY KEY(shortlink)` (dòng 116) chặn trùng ở tầng DB nhưng tài liệu không mô tả xử lý lỗi khi va khoá.

  [Low] pastebin.py · dòng 8–14 (`extract_url`, `extract_year_month`) — Hai hàm rút URL và mốc thời gian từ log là thân rỗng (`pass`), nên trả về `None`. Trong `mapper` (dòng 25–27) chúng được đưa thẳng vào cặp key `(period, url)` → mọi bản ghi thành `(None, None)`. → Analytics đếm hit (use case dòng 191–193) tạo ra số liệu vô nghĩa mà không hề báo lỗi. Đây là stub tài liệu, nhưng ở góc quyền/kiểm toán: nếu analytics dùng để phát hiện lạm dụng hay theo dõi truy cập bất thường thì nó đang mù hoàn toàn.

CÓ THỂ LÀ GAP (chưa chắc — cần xác nhận thêm)

  README.md · dòng 19–38 (Use cases / Out of scope) — "Đặt visibility" và "paste riêng tư" bị để ngoài phạm vi, còn người dùng luôn ẩn danh. Vậy MỌI paste đều là công khai-cho-ai-có-link. Câu hỏi cần chốt: người dùng fixture (phía CTO/business) có đang NGẦM tin rằng paste của họ là riêng tư không? Nếu có, thì kỳ vọng nghiệp vụ và thiết kế đang lệch nhau — cần xác nhận "riêng tư = chỉ dựa vào bí mật của URL" có được chấp nhận không, hay cần một tầng quyền thật.

  README.md · dòng 149–162 (REST API tạo paste qua HTTP) — Ví dụ `curl` tạo paste dùng `https://` nhưng tài liệu không nói rõ TLS bắt buộc trên toàn tuyến, cũng không nói nội dung paste được mã hoá khi lưu (at-rest) trong Object Store. Cần xác nhận: nội dung nhạy cảm có được bảo vệ khi truyền và khi lưu không, hay chỉ dựa vào bí mật URL.

  README.md · dòng 143 ("62^7 possible values") — Không gian 62^7 (~3.5 nghìn tỷ) so với 360 triệu shortlink trong 3 năm (dòng 66) cho mật độ lấp đầy ~0.01%. Con số này nghe an toàn trước dò ngẫu nhiên, NHƯNG chỉ đúng nếu shortlink thực sự ngẫu nhiên — mà Critical #1 cho thấy nó tất định và đoán được. Cần xác nhận lại sau khi vá cơ chế sinh URL: nếu chuyển sang ngẫu nhiên thật thì mật độ này mới là hàng rào chống dò brute-force hợp lệ.

KHÔNG TÌM THẤY GAP (đã soi, thấy ổn trong phạm vi lăng kính)

  README.md · dòng 111–119 (schema bảng `pastes` + index) — Cấu trúc bảng và việc đặt PRIMARY KEY trên `shortlink` là hợp lý ở tầng lưu trữ; không thấy vấn đề quyền riêng trong định nghĩa schema (vấn đề nằm ở cơ chế SINH shortlink, không ở schema).

  README.md · dòng 234–276 (Scale the design) — Phần scale (load balancer, cache, read replica, master-slave) không mở thêm bề mặt quyền mới ngoài những gì đã nêu; cache nội dung paste (dòng 267) có thể kéo dài thời gian sống của paste hết hạn trong bộ nhớ, nhưng đó là hệ quả của gap expiration đã ghi ở trên, không phải gap riêng.

GỢI Ý TIẾP THEO
Có gap [Critical] (cơ chế sinh URL đoán được, và đọc paste không kiểm expiration). Bạn muốn tôi lên kế hoạch fix theo thứ tự ưu tiên hai lỗ Critical này trước không? → sẽ bàn giao sang skill `plan`.
Ngoài ra: bạn muốn tôi đào sâu mục "paste riêng tư có đang bị hiểu nhầm là riêng tư không" (trong phần CÓ THỂ LÀ GAP) để xác nhận đây có thực sự là lệch kỳ vọng nghiệp vụ không?
