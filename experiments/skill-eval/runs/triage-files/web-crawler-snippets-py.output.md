# triage-files · web_crawler_snippets.py — OUTPUT (skill: triage)

═══ TRIAGE: web_crawler_snippets.py — system-design-primer (level L2) ═══

Tầng: Tài liệu / Đáp án mẫu (một bản phác Domain + Application của "Crawler Service" chép ra từ README) — không phải code đang chạy trong hệ thống nào. Không có mùi sai tầng.
Trách nhiệm: Phác khung một dịch vụ thu thập trang web (web crawler): xếp hàng link cần cào, bỏ trùng bằng "chữ ký" trang, và đẩy việc sang hai hàng đợi đánh chỉ mục — để minh hoạ cho phần học "thiết kế web crawler", không để chạy thật.
Contract:
  - Ba lớp chính: `PagesDataStore` (nơi cất link và link đã cào), `Page` (một trang: url, nội dung, link con, chữ ký), `Crawler` (bộ điều phối vòng lặp cào).
  - Đầu vào thực tế: chưa có. Mọi phương thức "lá" (add/remove/extract/insert/crawled_similar/create_signature) chỉ là khung rỗng, thân là `pass` — chưa viết logic. Đây là chủ ý của một đáp án phỏng vấn ("clarify how much code you're expected to write"), KHÔNG phải code chết.
  - Quy tắc nghiệp vụ đã mã hoá: lấy trang ưu tiên cao nhất → nếu đã gặp trang giống (trùng chữ ký) thì hạ ưu tiên để tránh lặp vô hạn → nếu chưa, thì cào và đẩy hai job đánh chỉ mục.
Caller: KHÔNG tìm thấy (mức chắc chắn cao). Grep toàn repo: ngoài chính file này, chỉ có README.md (bản tiếng Anh + tiếng Trung) chứa lại đúng đoạn code này — tức file .py là bản chép ra từ tài liệu, không có file .py nào import hay gọi nó. Đây là repo học liệu nên "0 caller" KHÔNG có nghĩa là chết cần xoá.
Callee: Trong file, `Crawler` gọi các phương thức của `data_store` (PagesDataStore) và hai hàng đợi `reverse_index_queue` / `doc_index_queue` được truyền vào lúc khởi tạo. Không dependency sai tầng.
State: Không đổi state thật (mọi thao tác ghi/xoá link đều là `pass`). `Page` tự tính `self.signature` lúc tạo.
Side effect: Trên giấy thì có (ghi/đọc NoSQL, đẩy job sang hàng đợi), nhưng vì thân rỗng nên chạy thật KHÔNG gây side effect nào.
Core/Detail: Thứ đáng chú ý nằm ở CORE (vòng lặp `crawl()` — trách nhiệm chính của file), không phải chi tiết vụn.
Rủi ro khi tác động: thấp — file không được ai gọi, sửa nó không làm vỡ API/DB/UI nào. Rủi ro duy nhất là làm lệch nó khỏi README đi kèm (README là nguồn gốc của đoạn code này).

Một điểm cần nêu (không tự sửa): vòng lặp `crawl()` ở bản .py gọi `extract_max_priority_page()` HAI lần mỗi vòng — một lần đầu vòng, một lần thừa ở cuối vòng (dòng 73). Lần gọi thừa này lấy ra một trang rồi vứt đi không xử lý, nên có thể bỏ sót trang. Bản trong README KHÔNG có dòng thừa này. Đây là mâu thuẫn giữa file .py và tài liệu gốc, đụng vào logic lõi của bản phác — nên KHÔNG sửa tay ở đây mà bàn giao (xem Bước kế). (Vài khác biệt khác so với README như chữ ký tính trong `Page` thay vì trong `Crawler`, hay có thêm field `pages` — chỉ là biến thể trình bày, không phải lỗi.)

Scope-check: Không xác minh được live slice / do_not_touch — repo fixture này chưa từng chạy `frame`/`partner` nên không có agent-state/pipeline-state. Ngoài ra, `state/current.json` đang trỏ tới project khác (`hex_agent`), KHÔNG phải fixture này → cảnh báo lệch project; không có ràng buộc scope nào áp lên file này. Coi như học liệu tự do, không đóng băng.

QUYẾT ĐỊNH: giữ — đây là đáp án mẫu để học, đúng vai trò của nó, không ai phụ thuộc vào nó và không có mùi sai tầng; chỉ đọc-rồi-thôi nên không ghi state.
Bước kế: Nếu bạn muốn dùng đoạn này để chạy thật (không chỉ để học), thì lần gọi `extract_max_priority_page()` thừa ở dòng 73 nên được rà lại — vì nó chạm logic lõi, hãy đưa sang khung build có kỷ luật: → /frame "sửa vòng lặp crawl() cho khớp thiết kế README (bỏ lần lấy trang thừa cuối vòng), kèm test vòng lặp không bỏ sót trang". Nếu chỉ muốn HIỂU rõ vì sao thiết kế crawler chạy như vậy (không sửa gì) → /explain về "luồng crawl() và cách tránh lặp vô hạn bằng chữ ký trang".
════════════════
