# triage-files · pastebin.py — OUTPUT (skill: triage)

═══ TRIAGE: pastebin.py — system-design-primer (level L2) ═══

Tầng: Application/Use Case + Infrastructure (một job xử-lý-theo-mẻ, kiểu MapReduce). Không sai tầng — nó nằm đúng chỗ của một tác vụ chạy nền để đếm số liệu.

Trách nhiệm: Đọc log của web server, đếm mỗi đường link (paste) được xem bao nhiêu lần theo từng tháng — phục vụ use case "thống kê lượt xem trang" trong bản thiết kế Pastebin.

Contract:
- Chạy như một script độc lập: gõ file này lên là nó tự khởi động (`HitCounts.run()`).
- Đầu vào: từng dòng log (đưa vào ngầm bởi framework mrjob).
- Đầu ra: cặp khoá–số, dạng `(tháng, url) → tổng số lượt`. Ví dụ `(2016-01, url0) → 2`.
- Hai bước lõi: `mapper` bóc từng dòng log thành cặp `(tháng, url), 1`; `reducer` cộng dồn các số 1 lại theo từng cặp.

Caller: KHÔNG tìm thấy (grep toàn repo). Tên `HitCounts` / `extract_url` / `extract_year_month` chỉ xuất hiện ở chính file này và ở README của thư mục pastebin (bản chép trong tài liệu). Không có file Python nào import hay gọi nó, không có bộ lập lịch nào kích nó.
→ Quan trọng: 0 caller ở ĐÂY KHÔNG có nghĩa là "code chết". File này được thiết kế để chạy độc lập (có `if __name__ == '__main__'`), và cả repo là TÀI LIỆU HỌC thiết kế hệ thống — mỗi bài giải là một ví dụ đứng riêng, không phải một hệ thống có nhánh gọi nhau. Đây là "chắc chắn 0 caller trong repo" nhưng "KHÔNG suy ra là bỏ đi được".

Callee: Chỉ gọi thư viện ngoài `mrjob` (framework MapReduce) và hai hàm nội bộ của chính nó (`extract_url`, `extract_year_month`). Không đụng DB, không đụng domain của Pastebin.

State: Không đổi state nào của hệ thống. Job này chỉ đọc log rồi phát ra con số — nó không ghi ngược vào bảng paste, không sửa dữ liệu.

Side effect: Về nguyên tắc có I/O (đọc log, xuất kết quả ra output của mrjob), nhưng trong bản này việc đọc/ghi do framework lo. Bản thân file không tự mở kết nối mạng hay DB.

Core/Detail: Phần lõi (`mapper`/`reducer`/`steps`) là ĐÚNG và đầy đủ về mặt ý tưởng. Nhưng hai hàm phụ `extract_url` và `extract_year_month` đang là chỗ trống — thân hàm chỉ ghi `pass`, tức là CHƯA viết. Đây là chi tiết bỏ ngỏ CÓ CHỦ Ý: README ngay bên cạnh ghi rõ "Clarify with your interviewer how much code you are expected to write" (hãy hỏi người phỏng vấn xem cần viết bao nhiêu code) — đây là bài mẫu phỏng vấn, cố tình để trống phần bóc tách log cho người học tự điền.

Rủi ro khi tác động: Thấp. Không ai gọi file này nên sửa/xoá nó không làm vỡ chỗ nào khác trong repo. Rủi ro thật nằm ở HIỂU NHẦM: nếu tưởng nó là code chạy thật và "sửa cho chạy được", bạn sẽ phá mất ý đồ dạy học (để trống để người học điền).

Scope-check: Không có `agent-state.json` / `pipeline-state.json` / `user-state.json` trong fixture, không có thư mục `.ai-understanding/`. Không xác minh được live-slice hay do_not_touch — coi như không có ràng buộc slice. Không có scope `partner` để đối chiếu. (Đây là ca đọc file trên một repo tài liệu chưa từng chạy các skill kia — vẫn chẩn đoán được bằng grep + đọc nội dung.)

QUYẾT ĐỊNH: giữ — file làm đúng một việc rõ ràng (đếm lượt xem theo tháng bằng MapReduce), nằm đúng tầng, không ai phụ thuộc nên vô hại, và hai hàm để trống là CỐ Ý của bài mẫu chứ không phải lỗi cần vá.

Vì sao KHÔNG chọn nhãn khác:
- Không "sửa nhỏ": điền thân `extract_url`/`extract_year_month` là viết logic bóc tách định dạng log (business logic), không phải typo cô lập — vượt lằn ranh fix-inline, và ở đây còn là phần cố ý để trống.
- Không "xoá": tuy 0 caller, nhưng nó là script chạy độc lập + ví dụ trong tài liệu; không thuộc diện code chết.
- Không "cần đọc thêm": đã trả lời được đủ — nó là gì, hứa gì, ai phụ thuộc (không ai), sửa có nguy hiểm không (không).

Bước kế: Không cần làm gì. Nếu bạn (ở vai CTO/business) muốn HIỂU sâu hơn job này chạy thế nào từng bước để đánh giá phương án analytics → chạy /explain về "job đếm lượt xem của Pastebin". Nếu sau này muốn thật sự viết phần bóc tách log để job chạy ra số có nghĩa (điền hai hàm `extract_*`) → đó là viết logic mới, chạy /frame để đóng khung một slice, mình không code thay ở đây.
════════════════
