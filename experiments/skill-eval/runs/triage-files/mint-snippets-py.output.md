# triage-files · mint_snippets.py — OUTPUT (skill: triage)

═══ TRIAGE: mint_snippets.py — system-design-primer (level L2) ═══

Tầng: Domain (minh hoạ) — thực chất là ĐOẠN CODE MẪU TRONG TÀI LIỆU HỌC, không phải code chạy thật. ⚠ Không sai tầng, nhưng sai "vai": nó là bản trích từ README của bài thiết kế Mint, sống tách khỏi tài liệu gốc.

Trách nhiệm: Phác hoạ ý tưởng "phân loại giao dịch theo người bán" và "ngân sách theo hạng mục" cho bài thiết kế hệ thống kiểu Mint — để minh hoạ cách nghĩ, không phải để nhập vào chạy.

Contract: Xuất ra 4 mảnh — enum `DefaultCategories` (các nhóm chi tiêu: nhà ở, ăn uống, xăng, mua sắm), lớp `Categorizer.categorize(transaction)` (nhận một giao dịch, trả về nhóm chi tiêu hoặc None), lớp `Transaction` (mốc thời gian + người bán + số tiền), lớp `Budget` (bản đồ hạng mục → hạn mức tiền, cho phép ghi đè một hạng mục).

Caller: KHÔNG tìm thấy caller trong code (chắc chắn — grep toàn repo, không file .py nào import `mint_snippets`, cũng không ai khởi tạo `Categorizer`/`Transaction`/`Budget` ngoài chính file này). Cùng bốn cái tên này CÓ xuất hiện trong `mint/README.md` (một phần — nhưng đó là tài liệu mô tả, không phải lời gọi code).

Callee: Tự thân, không import gì ngoài `enum`. Bên trong có một lời gọi tới `self.manual_overrides[...].peek_min()` — nhưng `manual_overrides` KHÔNG hề được gán trong `__init__`.

State: `Categorizer.categorize` ghi vào biến toàn cục `seller_category_map` (module-level) chứ không ghi vào `self.seller_category_map` — làm bẩn state dùng chung ở tầng module. `Budget.override_category_budget` sửa bản đồ hạn mức tại chỗ.

Side effect: Không I/O, không DB, không network. Chỉ mutation bộ nhớ (và đúng chỗ mutation đó là chỗ sai — xem dưới).

Core/Detail: Thứ hỏng nằm ở CORE của lớp `Categorizer` (đúng cái method thể hiện ý tưởng), không phải chi tiết vụn.

Rủi ro khi tác động: THẤP với hệ thống (không ai gọi, xoá/sửa không làm vỡ code nào). NHƯNG rủi ro NGƯỜI HỌC thì có thật: nếu ai copy đoạn này chạy, nhánh "người bán chưa có sẵn" sẽ NÉM LỖI ngay — `self.manual_overrides` chưa từng được định nghĩa (trong `__init__` nó tên là `seller_category_overrides_map`), và dòng gán lại ghi nhầm vào global `seller_category_map` thay vì `self.`. Đây là code đã LỆCH khỏi bản gốc trong README (bản README dùng đúng tên `seller_category_crowd_overrides_map` và ghi vào `self.`).

Scope-check: Không xác minh được live slice / do_not_touch — fixture repo này chưa từng chạy `frame`/`partner`, không có `agent-state.json`, `pipeline-state.json` hay `.ai-understanding/`. Coi như không ràng buộc scope; chẩn đoán dựa trên grep + bản chất tài liệu.

QUYẾT ĐỊNH: giữ — đây là đoạn code minh hoạ trong tài liệu học, cố tình rời rạc ("# ..." bỏ lửng, không có main), không phải phần mềm để chạy; xoá nó không có lợi (repo dùng nó để dạy), mà "sửa cho chạy đúng" cũng KHÔNG nên làm inline vì nó chạm ý tưởng cốt lõi của lớp `Categorizer` và cần khớp lại với README gốc — đó là việc cần đóng khung, không phải typo cô lập.

Bước kế: Không đụng gì. Nếu bạn muốn hiểu bài thiết kế Mint đang minh hoạ gì (cách phân loại giao dịch, cách gợi ý ngân sách) → chạy /explain về `mint_snippets.py` cùng README của nó. Nếu bạn muốn ĐỒNG BỘ đoạn code này về đúng như bản README (sửa `manual_overrides` → tham số đã khai báo, và ghi vào `self.` thay vì global) → đó là sửa chạm logic lõi, không inline được; chạy /frame với khung slice "đồng bộ mint_snippets.py khớp với README, sửa lỗi attribute/global trong Categorizer.categorize". (frame giữ kỷ luật hỏi-trước-code, mình không code thay.)
════════════════

Ghi chú độ tin cậy caller: đã grep toàn repo với đuôi .py/.md cho cả 4 export (`Categorizer`, `Transaction`, `Budget`, `DefaultCategories`) và tên module — không có lời gọi code nào (chắc chắn). Chỉ có trùng tên trong tài liệu README (một phần).
