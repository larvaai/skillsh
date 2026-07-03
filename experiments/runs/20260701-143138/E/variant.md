# E · Nguyên tắc viết

## editSummary
Sửa ở rule/principles.md (nơi SKILL.md trỏ tới bằng "cách nói"). Thêm một mục mới "NGUYÊN TẮC RIÊNG CHO LỜI GIẢI THÍCH (explain)" gồm 4 luật E1–E4: vấn-đề-trước-thuật-ngữ-sau ở cấp CÂU, câu ngắn phẳng, cấm tường-bullet, cấm trích số dòng ở mức thấp. Vì sao ở đây: SKILL.md đã dặn đọc principles.md trước khi trả lời và rubric tiêu chí 4 (lời văn, xương sống) chấm đúng những lỗi này; đặt luật cạnh nguyên tắc trình bày cũ để mọi câu explain phải qua. Sửa tối thiểu, không đụng SKILL.md, thang zoom hay bảng mức.

## changedSections
## NGUYÊN TẮC RIÊNG CHO LỜI GIẢI THÍCH (explain)

Bốn luật này chi phối CÁCH viết một câu explain. Vi phạm là lỗi lời văn, bị rubric bắt (tiêu chí 4).

E1. **Vấn đề trước, thuật ngữ sau.** Mỗi câu: nói cái ĐAU / cái việc đời thường trước, chỉ thả tên code sau khi chỗ đứng của nó đã rõ. Không mở câu bằng tên hàm/tên file/tên kiến trúc.

E2. **Câu ngắn, phẳng.** Mỗi câu một ý. Không câu lồng nhiều mệnh đề, không "mà trong đó / theo đó / nhờ vậy mà" nối dài. Đọc to hết hơi một lần là quá dài — cắt.

E3. **Cấm tường-bullet.** Không đổ một danh sách bullet dài thay cho lời kể. Luồng và ý tưởng kể bằng câu văn liền mạch. Bullet chỉ dùng khi liệt kê module ở tầng cuối, mỗi dòng một cụm ngắn — không phải để né việc viết câu.

E4. **Cấm trích số dòng ở mức thấp.** Dưới L4 không trích `file.py:123`, không dán số dòng. Tên file/hàm chỉ xuất hiện từ L4 trở lên, và cũng chỉ tên — không kèm số dòng trừ khi thật cần chỉ đúng chỗ.

## output (nguyên văn)
Bạn đang ở L3, nên mình đi kỹ luồng chạy rồi chạm nhẹ vào các phần. Mình mặc định kiểu overview vì bạn hỏi tổng thể; nếu muốn soi một luồng cụ thể thì nói nhé.

Vấn đề nó giải: khi bạn để nhiều "trợ lý AI" cùng làm việc và cùng gọi công cụ ngoài, rất dễ loạn — cái này gọi lung tung, cái kia lỡ tay đổi dữ liệu, và khi hỏng thì không biết chuyện gì đã xảy ra. Hệ này sinh ra để một tác vụ chạy có kỷ luật và soi lại được, cho người dựng hệ agent chứ không phải người dùng cuối.

Ý tưởng cốt lõi chỉ có một: mọi hành động ra thế giới ngoài phải chui qua đúng một cái cửa. Gọi mô hình AI cũng là "một hành động", không có đường tắt. Vì chỉ một cửa, nên mọi thứ đều được ghi lại, chặn được cái không cho phép, và không hành động nào lọt ra ngoài tầm nhìn.

Giờ đi một tác vụ từ lúc vào tới lúc ra, như một câu chuyện.

Một yêu cầu đi vào qua cửa công khai ổn định — chỗ để chạy mới hoặc chạy tiếp một việc dang dở. Trước mỗi lượt suy nghĩ có một trạm gác đếm số bước; hết ngân sách thì dừng, khỏi chạy vô tận. Qua gác, tới lượt "suy nghĩ": hệ hỏi mô hình AI xem nên làm gì tiếp, và bắt mô hình trả lời đúng một hành động ở dạng máy đọc được. Nếu mô hình trả lời sai định dạng, hệ sửa hoặc bắt thử lại, không để câu rác trôi vào trong. Hành động đó rẽ một trong bốn ngả: chạy một công cụ, giao việc cho một agent con, kết thúc, hoặc quay lại gác. Khi chạy công cụ, và cả khi gọi AI, tất cả đều đi qua cái cửa duy nhất kể trên — trong code nó tên là execute_tool. Tại cửa đó, hệ ghi lại "đã xin chạy", kiểm xem công cụ này có nằm trong phạm vi được phép của phiên không, rồi mới cho chạy qua một chuỗi lớp chắn (đo thời gian, chặn theo danh sách cấm, khống chế lặp, thu gọn kết quả dài). Một mẹo nhỏ nhưng quan trọng: dữ liệu đầu vào được sao chép sâu trước khi trao cho công cụ, nên công cụ có nghịch cũng không làm hỏng dữ liệu gốc của người gọi. Công cụ có nổ lỗi thì cửa nuốt lỗi, đóng gói thành một kết quả chuẩn, kernel không bao giờ sập theo.

Giao việc cho agent con thì đi một cửa RIÊNG, không phải cửa trên — đây là chỗ dễ nhầm nhất. Lý do tách: giao việc cần luật riêng về độ sâu, ngân sách và phạm vi năng lực trao xuống, nên nó có một chốt riêng thay vì nhét chung vào cửa công cụ. Khi việc xong hoặc thất bại, cả hai đều đi qua cùng một chỗ đóng sổ, nên một lần chạy hỏng vẫn được ghi nhận gọn gàng như một lần chạy trót lọt. Toàn bộ tiến trình được lưu vào một file cơ sở dữ liệu nhỏ cho mỗi lần chạy; đó mới là bản lưu thật để chạy tiếp, còn file hiển thị cho giao diện chỉ là bản chiếu để xem, không dùng để phục hồi.

Bây giờ soi qua các phần lớn, mỗi phần là một chặng trong luồng trên:

- core/ — cái lõi chung: cửa duy nhất execute_tool, sổ tra công cụ, khuôn dữ liệu chuẩn, và tách bạch phần "dùng chung, đóng băng" với phần "trạng thái của riêng một lần chạy".
- graph/ + orchestrator/ — bộ điều phối: dựng sơ đồ các bước gác/suy-nghĩ/công-cụ/giao-việc/kết-thúc, và cái facade ổn định để chạy/chạy-tiếp cùng file cơ sở dữ liệu lưu điểm.
- discipline/ + middleware/ — mấy lớp kỷ luật: bắt AI trả đúng định dạng, đếm ngân sách bước, thu gọn kết quả dài, chặn công cụ theo danh sách cấm.
- delegation/ — cửa giao việc riêng: luật độ sâu/ngân sách/phạm vi và sổ ghi tiến trình của agent con.
- llm/ + observability/ + control/ — nối mô hình AI vào như một năng lực, ghi lại mọi sự kiện để soi, và phần điều khiển thời gian thực đang làm dở.

Tất cả để phục vụ đúng một điều: nhiều agent làm việc mà vẫn kiểm soát được và soi lại được từng bước.

Bước tiếp cho bạn ở L3: bạn muốn mình giải thích kỹ trách nhiệm từng phần, hay có một module cụ thể bạn đang thắc mắc (vd cái cửa execute_tool bên trong, hay cửa giao việc riêng)?
