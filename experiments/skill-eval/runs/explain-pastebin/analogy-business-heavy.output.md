# explain-pastebin · analogy-business-heavy — OUTPUT (skill: explain)

**Pastebin là cái máy gì — và nó gánh nỗi đau nào**

Hình dung bạn vừa viết một đoạn ghi chú dài — một đoạn code, một log lỗi, một khối văn bản — và muốn gửi cho đồng nghiệp. Dán thẳng vào chat thì vỡ định dạng, dài lê thê, người nhận phải cuộn mỏi tay. Cái đau ở đây là: văn bản dài thì cồng kềnh, mà thứ dễ chuyền tay nhau lại là một đường link ngắn gọn.

Pastebin chính là cái máy giải nỗi đau đó. Bạn đổ một khối chữ vào, nó cất giữ hộ, rồi trả lại cho bạn **một đường link ngắn**. Ai cầm link đó mở ra là thấy nguyên văn. Giống như bạn gửi đồ vào tủ gửi đồ ở siêu thị: đồ nằm trong tủ, tay bạn chỉ cầm một cái thẻ số nhỏ, đưa thẻ cho ai là người đó lấy được đồ. Người hưởng lợi là bất kỳ ai cần chia sẻ một mẩu văn bản mà không muốn kéo theo cả cục — lập trình viên, người viết lách, hay chỉ là người cần "quăng tạm" một đoạn text ở đâu đó. Ở đây người dùng còn không cần đăng ký tài khoản, cứ vào là dùng.

**Ý tưởng thông minh cốt lõi (một câu)**

Thay vì bắt người ta chuyền cả khối chữ nặng nề, ta tách làm hai: **chữ thì cất một nơi, cái thẻ ngắn để lấy chữ thì chuyền tay**. Cả hệ thống xoay quanh việc phát ra một cái thẻ ngắn không trùng với ai, và luôn tìm lại đúng khối chữ khi có người đưa thẻ.

Vì sao đáng giá với business: link ngắn thì dễ dán, dễ nhớ, dễ gửi — đó là trải nghiệm bán được. Và vì phần lớn hành vi là *đọc lại* chứ không phải *viết mới* (bài toán giả định 10 lượt đọc mới có 1 lượt viết), nên nếu việc "đưa thẻ lấy chữ" mà nhanh và rẻ, cả dịch vụ vừa mượt vừa nhẹ chi phí.

**Luồng "bạn đang ở đây" — kể như một câu chuyện**

Có hai chuyến đi trong nhà này. Chuyến gửi chữ vào, và chuyến lấy chữ ra.

*Chuyến GỬI (tạo paste):*

1. Người dùng đổ một khối chữ vào và bấm gửi. Yêu cầu này đi tới **cửa trước của dịch vụ** — chỗ tiếp nhận mọi khách vào.
2. Cửa trước chuyển việc "ghi mới" sang **quầy chuyên xử lý viết**. Có hai quầy tách riêng: một quầy chỉ lo ghi, một quầy chỉ lo đọc — để việc đọc đông đúc không giẫm chân việc ghi.
3. Quầy ghi làm ra **một cái thẻ ngắn** (bảy ký tự, kiểu `foobar`). Nó phải chắc cái thẻ này chưa ai dùng — nên nó **ngó vào sổ cái xem có trùng không**; trùng thì làm lại cái khác.
4. Xong, nó cất mọi thứ vào hai chỗ. Khối chữ nặng — đưa vào **kho chứa nội dung** (một cái kho lớn chuyên ôm các tệp). Còn cái thẻ ngắn cùng vài thông tin nhỏ (thẻ trỏ tới đâu, tạo lúc nào, khi nào hết hạn) — ghi vào **sổ cái** để tra cứu nhanh.
5. Cuối cùng nó trả cái thẻ ngắn về cho người dùng. Chuyến gửi kết thúc ở đây.

*Chuyến LẤY (xem paste):*

6. Ai đó cầm link mở ra. Yêu cầu "đọc" này đi tới cửa trước, rồi được đẩy sang **quầy chuyên xử lý đọc**.
7. Quầy đọc lật **sổ cái** tìm cái thẻ. Có thì nó theo chỉ dẫn trong sổ, vào **kho chứa nội dung** lấy đúng khối chữ ra và trả về. Không có thì báo lỗi "không tìm thấy".

Đó là toàn bộ trái tim của Pastebin: phát thẻ khi gửi, đưa thẻ lấy chữ khi đọc. Sổ cái là cuốn danh bạ "thẻ nào ứng với chữ nào"; kho chứa là nơi chữ thật sự nằm.

**Hai việc phụ chạy nền — vẫn phục vụ cùng một giá trị**

Ngoài hai chuyến chính, có hai người làm việc lặng lẽ phía sau:

- **Người đếm lượt xem.** Dịch vụ muốn biết mỗi paste được xem bao nhiêu lần mỗi tháng. Thay vì đếm ngay lúc có khách (làm chậm khách), nó để cửa trước ghi lại mọi lượt ghé vào một cuốn nhật ký, rồi *cuối kỳ mới gom sổ đếm một lượt*. Đây chính là mẩu code Python duy nhất chạy được trong bài (`pastebin.py`): nó đọc từng dòng nhật ký, rút ra "tháng nào, link nào", rồi cộng dồn thành "tháng 1, link X: 12 lượt". Chọn đếm gộp cuối kỳ vì bài toán nói thẳng: thống kê không cần tức thời — nên đừng bắt khách chờ chỉ để đếm.
- **Người dọn rác.** Paste có thể đặt hạn dùng. Một tiến trình quét sổ cái, thấy cái nào quá hạn thì xóa (hoặc đánh dấu hết hạn) — để kho không phình mãi.

**Vì sao hình hài này đáng tin (nhắc lại giá trị)**

Tách *chữ nặng* khỏi *thẻ nhẹ* nghĩa là mỗi thứ nằm đúng chỗ tối ưu của nó: sổ cái nhỏ gọn nên tra rất nhanh, kho chứa thì cứ việc phình to chứa nội dung mà không làm chậm việc tra thẻ. Tách quầy đọc khỏi quầy ghi nghĩa là lượng đọc khổng lồ (gấp 10 lần ghi) không đè lên việc ghi. Và đẩy việc đếm lượt ra chạy nền nghĩa là khách luôn được phục vụ nhanh. Ba lựa chọn này cùng phục vụ một lời hứa: *đưa thẻ là ra chữ, nhanh và rẻ, ở quy mô hàng trăm triệu lượt mỗi tháng.*

---

*Ghi chú nhỏ:* tài liệu này chủ yếu là **bản thiết kế** (nó vẽ hình hài hệ thống và bàn cách nới rộng khi tải tăng — thêm bộ chia tải, thêm bộ nhớ đệm, nhân bản sổ cái). Phần code thật chỉ có đúng một mẩu: người-đếm-lượt-xem. Phần "tạo thẻ", "cửa trước", "hai quầy đọc/ghi" là mô tả kiến trúc, không phải code chạy được trong repo — nên mình kể chúng như hình hài, không chỉ vào dòng code cụ thể.

---

Bạn đang ở mức **L2 (map)** — hiểu nghiệp vụ, đang muốn nắm luồng chạy. Mình vừa đi qua trọn hai chuyến gửi/lấy ở mức bản đồ. Bạn muốn đi tiếp theo hướng nào:

- **Đào sâu một chuyến** — ví dụ soi kỹ chuyến gửi: cái thẻ ngắn được sinh ra thế nào, vì sao lại là bảy ký tự, làm sao chắc không trùng?
- **Xem phần nới rộng quy mô** — khi hàng trăm triệu lượt đọc đổ vào, bản thiết kế thêm những gì (bộ nhớ đệm, nhân bản, chia tải) và vì sao?
- **Chỉ đọc mẩu code có thật** — đi qua `pastebin.py` (người-đếm-lượt-xem) từng bước bằng lời.

Và sau lần này, bạn thấy mình đang ở mức nào? *L0 locate / L1 scout / L2 map / L3 flow / L4 structure / L5 trace / L6 review / L7 plan / L8 architect* — để mình ghi lại, lần sau nói đúng tầm bạn cần.
