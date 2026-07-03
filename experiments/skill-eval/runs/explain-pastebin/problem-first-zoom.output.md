# explain-pastebin · problem-first-zoom — OUTPUT (skill: explain)

Bạn đang ở **L2 (map)** — đã hiểu nghiệp vụ, chưa nắm luồng chạy. Nên tôi sẽ mở bằng vấn đề, rồi dẫn bạn qua tấm bản đồ luồng "bạn ở đây" của Pastebin. Tên module tôi chỉ nhắc như gợi ý, chưa mổ vào code.

**Vấn đề, và cho ai.** Bạn có một đoạn text — một đoạn log, một mẩu code, một ghi chú — và muốn đưa cho người khác xem. Dán thẳng vào chat thì dài, vỡ khung, khó copy lại. Cái cần là: bỏ đoạn text đó vào đâu đó, nhận về một cái link ngắn, gửi link đi, người kia mở link ra đọc đúng nội dung. Đó là Pastebin. Người hưởng lợi là bất kỳ ai cần chia sẻ một khối text qua một đường link — ở đây còn không cần đăng ký tài khoản, ai cũng dán được (anonymous). Cùng một bài toán là Bit.ly rút gọn link; khác đúng một chỗ: Pastebin phải **cất giữ cả nội dung**, còn Bit.ly chỉ nhớ giùm một cái link gốc.

**Ý tưởng cốt lõi (một câu).** Với mỗi đoạn text được dán vào, hệ thống bịa ra một cái tên ngắn 7 ký tự gần như không thể trùng, rồi ghi nhớ cặp "tên ngắn này → nội dung kia"; sau này ai cầm cái tên ngắn là moi lại được đúng nội dung. Cái khéo nằm ở chỗ tách làm hai kho: một kho nhỏ chỉ giữ *tấm thẻ tra cứu* (tên ngắn, ngày tạo, hạn dùng) để tìm cực nhanh, một kho lớn riêng giữ *nội dung text nặng*. Nhờ tách vậy, việc "tìm xem có paste này không" luôn nhanh, còn nội dung to bao nhiêu cũng không làm chậm khâu tra cứu. Với business, điều này đáng giá vì đọc phải nhanh (người ta click link là muốn thấy ngay) mà chi phí lưu trữ vẫn gọn.

**Luồng "bạn ở đây" — đi theo một paste từ lúc dán tới lúc người khác mở ra.** Thực ra có hai hành trình, tôi kể liền mạch cả hai vì chúng dùng chung một tấm bản đồ.

Khi bạn *dán một đoạn text mới*:

1. Trình duyệt của bạn gửi yêu cầu "tạo paste" tới cổng tiếp nhận đằng trước — vai trò của nó chỉ là cửa vào và đẩy tiếp yêu cầu vào trong (tài liệu gọi là **Web Server**, chạy như một trạm trung chuyển đứng chắn phía trước).

2. Yêu cầu được chuyển sang bộ phận chuyên lo việc *ghi* (**Write API**). Bộ phận này làm ba việc gọn: bịa ra một cái tên ngắn, kiểm tra tên đó chưa ai dùng, rồi cất dữ liệu.

3. Cái tên ngắn đó không bốc đại. Nó băm địa chỉ máy bạn cộng với mốc thời gian ra một chuỗi (bằng **MD5**), rồi mã lại thành các ký tự chữ-và-số an toàn cho URL (bằng **Base 62**, chỉ dùng a–z A–Z 0–9 nên link không dính ký tự lạ), và cắt lấy 7 ký tự đầu. Bảy ký tự kiểu này cho ra một số lượng tổ hợp khổng lồ — thừa sức cho hàng trăm triệu paste trong nhiều năm mà hầu như không trùng.

4. Trước khi chốt, hệ thống ngó vào kho thẻ tra cứu xem cái tên ngắn vừa bịa đã có ai chiếm chưa; trùng thì bịa lại. Kho thẻ này chính là bảng `pastes` — mỗi dòng là một tấm thẻ: tên ngắn, hạn dùng, ngày tạo, và đường dẫn trỏ tới chỗ để nội dung. Tên ngắn được đặt làm khóa chính, nên việc kiểm-trùng và tra-cứu về sau đều nhanh.

5. Nội dung text nặng thì không nhét vào bảng thẻ, mà đẩy sang một kho chứa file riêng (tài liệu gọi là **Object Store**, kiểu như Amazon S3). Tấm thẻ ở bước 4 chỉ giữ *đường dẫn* trỏ tới đây.

6. Xong, hệ thống trả về cho bạn cái tên ngắn — đó là link để đi khoe.

Khi người kia *mở link ra đọc*:

7. Link đi vào cùng cổng tiếp nhận ở bước 1, nhưng lần này được đẩy sang bộ phận chuyên lo việc *đọc* (**Read API**). Cố ý tách đọc và ghi thành hai phía riêng, vì lượng người đọc đông gấp nhiều lần người dán (bài toán giả định 10 lượt đọc cho mỗi 1 lượt ghi) — tách ra thì sau này bên đọc phình to mà không đụng bên ghi.

8. Bộ phận đọc cầm cái tên ngắn, tra vào bảng thẻ. Không thấy thẻ thì báo lỗi. Thấy thẻ thì lần theo đường dẫn trong thẻ, sang kho nội dung lấy đúng đoạn text về và trả cho người đọc.

Đó là toàn bộ luồng chính. Hai việc nền chạy âm thầm bên lề, không nằm trên đường đi của một request: một là **đếm lượt xem** để ra thống kê mỗi tháng — vì không cần realtime, hệ thống gom log của Web Server rồi cộng dồn theo kiểu chia-để-đếm (MapReduce); đây đúng là phần Python duy nhất có trong bài (`pastebin.py`, lớp `HitCounts`), phần còn lại chỉ là thiết kế trên giấy. Hai là **dọn paste hết hạn** — thỉnh thoảng quét bảng thẻ, thấy dòng nào quá hạn thì xóa.

**Vì sao hình hài này đáng (nhắc lại giá trị).** Bảy ký tự băm-rồi-mã cho link ngắn, gõ được, gần như không trùng — người dùng có thứ để chia sẻ. Tách kho-thẻ khỏi kho-nội-dung để tra cứu luôn nhanh dù nội dung nặng bao nhiêu. Tách phía-đọc khỏi phía-ghi để chịu được cảnh người đọc đông gấp bội người dán. Ba lựa chọn đó là cái làm một dịch vụ "dán text lấy link" đơn giản nhìn qua nhưng đứng vững khi hàng triệu người dùng.

---

Bạn muốn tôi đi sâu tiếp phần nào? Có hai hướng tự nhiên từ đây:

- **Đi kỹ luồng đọc/ghi từng bước một** — dừng lại sau mỗi bước để bạn kịp theo (đây là chế độ *flow*).
- **Điểm danh từng "phần" và trách nhiệm của nó** — Web Server, Write/Read API, kho thẻ, kho nội dung, lớp scale (cache, read-replica, CDN) — tức bước bạn lên mức L3–L4.

Hoặc nếu có một khúc cụ thể bạn đang gợn (ví dụ "sao lại cần cả cache lẫn read-replica", hay "tên ngắn trùng thì sao"), chỉ tôi khúc đó.

Sau lần này, bạn thấy mình đang ở mức nào? L0 locate / L1 scout / L2 map / L3 flow / L4 structure / L5 trace / L6 review / L7 plan / L8 architect
