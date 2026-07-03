# review-pastebin · scale-failure-lens — OUTPUT (skill: review)

Trước khi rà, tôi chốt phạm vi và ngữ cảnh — vì review chỉ soi đúng thứ bạn chỉ vào.

PHẠM VI: Bài thiết kế Pastebin — `solutions/system_design/pastebin/README.md` (mô tả kiến trúc + luồng Write/Read/Analytics/Delete) và `pastebin.py` (job MapReduce đếm lượt xem).
CHẾ ĐỘ: tổng thể, nhìn qua một lăng kính cố định — **quy mô & failure**. Tức là tôi cố tình hỏi: khi một paste bỗng nóng, khi cache trượt, khi hai người sinh trùng link, khi một mắt xích chết — thiết kế này hụt ở đâu.

Lưu ý một điều để bạn không hiểu nhầm kết quả: đây là **tài liệu thiết kế phỏng vấn**, không phải code chạy thật. `pastebin.py` chỉ có đúng một job đếm lượt xem, còn Write/Read/Delete mới nằm ở dạng mô tả trong README. Nên "gap" ở đây nghĩa là **lỗ hổng trong thiết kế** — chỗ tài liệu nói sẽ làm nhưng chưa nói làm sao khi gặp tải lớn hoặc sự cố. Đó đúng là thứ cần soi trước khi ai đó cầm bản này đi dựng thật.

Chưa có bản đồ hiểu biết (`.ai-understanding/`) cho fixture này, nên tôi đọc thẳng từ hai file gốc. Không có gì được suy diễn ngoài chữ trong file.

═══════════════════════════════════════

PHẠM VI: Pastebin design (README.md + pastebin.py)
CHẾ ĐỘ: tổng thể (lăng kính quy mô/failure)

GAP TÌM ĐƯỢC

**[Critical]** `README.md` · luồng "User enters a block of text" (dòng 98–105, 121–147) — **Sinh link bằng MD5(ip + timestamp) sẽ đụng nhau khi một client bắn nhiều paste trong cùng một giây.** Tài liệu chỉ chống trùng bằng "kiểm tra DB, nếu trùng thì sinh lại link khác" (dòng 100–102). Nhưng đầu vào của hàm băm là `ip_address + timestamp`, và cắt còn 7 ký tự. Cùng một IP (ví dụ tất cả người dùng sau một NAT của công ty, hoặc một script tự động) trong cùng một mốc thời gian sẽ cho **cùng một đầu vào → cùng một link**. Sinh lại cũng vô nghĩa vì đầu vào không đổi, nên có nguy cơ lặp vô hạn hoặc ghi đè. → Hậu quả: hai paste khác nhau nhận cùng shortlink, người sau ghi đè hoặc đọc nhầm nội dung người trước — mất dữ liệu và lộ nội dung chéo giữa người dùng.

**[Critical]** `README.md` · luồng Write (dòng 103–105) — **Ghi hai nơi (SQL rồi Object Store) nhưng không nói chuyện gì xảy ra nếu bước hai hỏng.** Thứ tự là: lưu vào bảng `pastes` trong SQL, rồi lưu nội dung vào Object Store, rồi trả link. Nếu SQL ghi xong mà Object Store ghi trượt (S3 lỗi, timeout), link đã tồn tại trong DB nhưng nội dung không tồn tại. → Hậu quả: người đọc mở link hợp lệ nhưng nhận về nội dung rỗng/lỗi, và không có bước dọn hay rollback nào được mô tả. Đây là **paste "ma"** — tồn tại trên giấy tờ, trống rỗng trên thực tế.

**[Critical]** `README.md` · luồng Read (dòng 170–173) — **Đường đọc chỉ tính hai kết cục: có trong SQL thì lấy từ Object Store, không có thì báo lỗi. Thiếu hẳn kết cục "có trong SQL nhưng Object Store trả về lỗi/không có nội dung".** Với một hệ 100 triệu lượt đọc/tháng và có phần "xóa paste hết hạn", trường hợp link còn trong index nhưng nội dung đã bị xóa/không lấy được là chuyện sẽ xảy ra thường. → Hậu quả: lỗi không được xử lý ở đúng nhánh, người dùng nhận trải nghiệm hỏng thay vì một thông báo "paste đã hết hạn/không còn".

**[Medium]** `README.md` · "Service deletes expired pastes" (dòng 230–232) — **Cách xóa paste hết hạn là "quét toàn bộ bảng SQL tìm mốc thời gian cũ hơn hiện tại".** Trong khi phần thiết kế index (dòng 119) lại chỉ tạo index trên `created_at`, không phải trên trường hết hạn. Với 360 triệu shortlink trong 3 năm (dòng 66), một lần quét toàn bảng định kỳ là một cú đấm nặng vào chính DB đang phục vụ đọc/ghi. → Hậu quả: mỗi đợt dọn rác làm chậm hoặc nghẽn đường đọc thật, đúng lúc hệ đang tải cao — bottleneck tự gây ra.

**[Medium]** `README.md` · luồng Read + phần Scale (dòng 170–173, 267) — **Đường đọc mô tả ở Bước 3 đi thẳng SQL rồi Object Store, hoàn toàn không nhắc tới Memory Cache.** Cache chỉ được giới thiệu mãi ở Bước 4 (dòng 267) như một câu nói chung. Không có mô tả nào về: đọc thì tra cache trước hay DB trước, ghi mới thì có nạp vào cache không, một paste nóng đột ngột (dòng 43 "traffic không phân bố đều") thì lần đọc đầu tiên có làm sập replica không. → Hậu quả: khi một link viral, làn sóng đọc đầu tiên đều là cache-miss dồn thẳng vào SQL Read Replica — đúng kịch bản "hot paste" mà lăng kính này soi, và tài liệu chưa khép được.

**[Medium]** `README.md` · phần Scale, câu về cache miss (dòng 267) — **Tài liệu giả định "SQL Read Replicas gánh được cache miss, miễn là replica không bị ngập vì replicate write".** Đây là một giả định treo, không có số nào đỡ. Với traffic có spike (dòng 43, 45) và một paste nóng, số cache-miss đồng thời có thể vượt xa mức 40 đọc/giây trung bình. → Hậu quả: giả định vỡ đúng lúc tải cao nhất, mà không có cơ chế dự phòng (ví dụ khóa chống dogpile khi nhiều request cùng miss một key) nào được nêu.

**[Medium]** `pastebin.py` · `extract_url`, `extract_year_month` (dòng 8–14) — **Hai hàm bóc dữ liệu từ dòng log đều là thân rỗng (`pass`), nên trả về `None`.** `mapper` (dòng 16–27) đem thẳng kết quả đó làm khóa `(period, url)` mà không kiểm tra dòng log có hợp lệ không. → Hậu quả: một dòng log méo (thiếu trường, format lạ) sẽ không bị loại mà lẫn vào kết quả thành khóa `(None, None)`, làm sai số liệu thống kê lượt xem. Với log ở quy mô hàng trăm triệu dòng/tháng, log rác là chuyện chắc chắn có.

**[Low]** `README.md` · REST API đọc paste (dòng 175–189) — **API đọc không có tham số phân trang hay giới hạn kích thước, mà mỗi paste tối đa chỉ giả định 1 KB (dòng 57).** Nhưng không nơi nào trong đường ghi (dòng 98–105) mô tả việc chặn nội dung quá khổ. → Hậu quả: một người dán một khối text rất lớn sẽ không bị chặn ở tầng nào được mô tả, phá vỡ giả định 1 KB/paste mà toàn bộ phép tính dung lượng (dòng 63–64) dựa vào.

**[Low]** `README.md` · phần "Out of scope" + toàn luồng (dòng 30–37) — **Người dùng là ẩn danh (dòng 24) và mọi thứ đăng nhập/quyền riêng tư đều nằm ngoài phạm vi.** Đây là lựa chọn có chủ ý của tác giả, không phải lỗi. Nhưng nó có nghĩa: bất kỳ ai đoán/quét được shortlink 7 ký tự đều đọc được nội dung, không có tầng chặn nào. → Hậu quả: nếu bản thiết kế này được bê nguyên đi dựng cho dữ liệu nhạy cảm, đây là lỗ hổng đọc trộm. Ghi lại để bạn quyết, vì "ẩn danh" hợp lý cho pastebin công cộng nhưng nguy hiểm nếu đổi bối cảnh.

CÓ THỂ LÀ GAP (chưa chắc)

`README.md` · sinh link (dòng 143–147) — **Nghi ngờ:** cắt 7 ký tự đầu của MD5 base-62 cho 62^7 giá trị, tài liệu nói "đủ cho 360 triệu link trong 3 năm". Về lý thuyết đủ, nhưng với hàm băm cắt ngắn thì xác suất đụng độ (birthday paradox) tăng nhanh khi số link tiến gần vài trăm triệu — chi phí "sinh lại khi trùng" (dòng 101) sẽ tăng dần theo thời gian. · Cần xác nhận thêm: bạn có muốn tôi ước lượng tỷ lệ đụng độ ở mốc 360 triệu link để biết chi phí sinh-lại có còn chấp nhận được không?

`pastebin.py` · `steps` (dòng 37–42) — **Nghi ngờ:** hàm gọi `self.mr(...)`, nhưng API `mrjob` bản mới dùng `MRStep`. Có thể là mã cũ không chạy được trên phiên bản hiện tại. · Cần xác nhận thêm: đây là fixture tài liệu nên có thể không quan trọng — bạn có cần bản này chạy thật không, hay chỉ soi thiết kế?

KHÔNG TÌM THẤY GAP (phần đã kiểm và thấy ổn trong khuôn khổ tài liệu)

- Phép tính dung lượng và throughput (dòng 56–76) nhất quán nội bộ: 1.27 KB/paste × 10 triệu = 12.7 GB/tháng, 4 ghi/s và 40 đọc/s khớp với tỷ lệ đọc/ghi 10:1.
- `reducer` (dòng 29–35 ở cả .py và README) cộng đúng các giá trị theo khóa — logic đếm không có lỗi rõ ở tầng gộp.
- Việc chọn RDBMS làm hash table lớn với khóa chính là `shortlink` (dòng 112–117) thực sự tạo ràng buộc duy nhất ở tầng DB — đúng như tài liệu nói, đây là chốt chặn cuối cho trùng link (dù đầu vào băm vẫn là điểm yếu, xem mục Critical đầu).

═══════════════════════════════════════

Gap Critical đang là nhóm nặng nhất: cả ba đều thuộc đúng lăng kính quy mô/failure bạn giao — đụng độ hash, ghi hai nơi không nguyên tử, và đường đọc thiếu nhánh nội dung mất. Bạn muốn tôi lên kế hoạch fix theo thứ tự ưu tiên ba cái đó không? Nếu muốn, việc đó thuộc skill `plan` — review chỉ dừng ở báo cáo, không tự sửa.

Và vì fixture này chưa có bản đồ hiểu biết, nếu bạn định soi tiếp các bài thiết kế khác trong repo (web_crawler, mint, twitter...), chạy `atlas` một lần sẽ giúp các lần review sau khỏi đọc lại từ đầu.
