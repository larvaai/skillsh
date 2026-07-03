# frame-add-feature · strict-slice-discipline — OUTPUT (skill: frame)

═══ FRAME: TỪ CHỐI BUILD CẢ APP ═══
Mình sẽ không code nhiều tính năng cùng lúc — rate-limiting + auth đăng nhập + analytics dashboard là ba slice riêng, gộp lại là cách chắc chắn ra rác.
Quy tắc: mỗi lần đúng MỘT slice chạy được, có giá trị nhìn thấy.
Bạn giữ Scope/Boundary/Acceptance; mình lo Plan/Code/Refactor.
════════════════

Trước khi bàn ba tính năng đó, mình phải nói thẳng một chuyện về file bạn chỉ vào, vì nó đổi toàn bộ cuộc chơi.

**File `pastebin.py` này KHÔNG phải cái pastebin bạn đang hình dung.**

Mình đã đọc hết file (`/Users/uspro/Desktop/skillsh/experiments/skill-eval/fixtures/system-design-primer/solutions/system_design/pastebin/pastebin.py`, 47 dòng). Nó không có web server, không có route, không có màn hình đăng nhập, không có nơi người dùng gõ paste. Nó chỉ có đúng một class `HitCounts` chạy trên `mrjob` — một job MapReduce chạy theo mẻ (batch). Việc của nó: đọc từng dòng log cũ, moi ra cái URL và tháng-năm, rồi đếm mỗi URL được truy cập bao nhiêu lần trong tháng. Đầu ra là những dòng kiểu `(2016-01, url0) → 2`. Nó chạy một lần trên đống log rồi tắt, không phải một dịch vụ chạy liên tục.

Vì sao điều này quan trọng với ba yêu cầu của bạn:
- **Rate-limiting** chặn request theo thời gian thực. File này không nhận request nào — nó đọc log đã ghi sẵn. Không có chỗ để gắn.
- **Auth đăng nhập** cần một request có phiên người dùng để bảo vệ. File này không có endpoint, không có phiên. Không có chỗ để gắn.
- **Analytics dashboard** cần một web UI đọc số liệu. File này là phần *sinh ra số liệu thô*, không phải phần hiển thị. Dashboard sẽ là một project khác đọc output của nó.

Nói cách nghiệp vụ: bạn đang cầm cái **máy đếm lượt xem chạy đêm**, không phải cái **website pastebin**. Ba tính năng kia thuộc về website — website đó chưa tồn tại trong repo này (chỉ có tài liệu thiết kế mô tả nó ở `pastebin/README.md`, không có code).

Nên mình có hai lựa chọn trung thực để đề xuất, không phải giả vờ file này là thứ nó không phải.

**Còn một lỗ hổng thật ngay trong file này.** Hai hàm lõi `extract_url` và `extract_year_month` mới chỉ là khung rỗng (thân hàm là `pass`, trả về `None`). Nghĩa là job hiện tại chạy sẽ đếm ra rác: mọi URL thành `None`, mọi tháng thành `None`. Đây là slice sống, nhỏ, đúng bản chất file — và nó phải xong trước khi bất kỳ dashboard nào có số liệu đúng để hiển thị.

═══ PHASE FRAME: Constitution + Slice — pastebin (level L2) ═══

**Mình hiểu gì (nói lại):** File là một job phân tích log theo mẻ. Nó biến log truy cập thô thành bảng "URL nào, tháng nào, bao nhiêu lượt". Mapper/reducer/steps đã có sẵn và đúng khuôn `mrjob`. Chỗ hỏng duy nhất là hai hàm moi dữ liệu ra khỏi mỗi dòng log — chúng đang rỗng.

**Giả định mình đang ngầm tin (cần bạn xác nhận):**
- Bạn muốn cái *máy đếm lượt xem* này thật sự chạy đúng, chứ không phải mình dựng một website pastebin mới từ số 0.
- Một dòng log có định dạng cố định, chứa một URL và một dấu thời gian có năm-tháng. (Mình CHƯA biết định dạng thật — sẽ hỏi ở CONTRACT, chưa hỏi vội ở đây.)
- "Analytics" bạn cần khởi nguồn từ chính bảng đếm này; sửa hai hàm rỗng là bước làm cho analytics có số liệu đúng.

**Non-goals — 3 thứ project NÀY (slice này) sẽ KHÔNG làm:**
1. KHÔNG dựng web server / endpoint / màn hình đăng nhập.
2. KHÔNG làm auth, KHÔNG làm rate-limiting (không có request để chặn/xác thực trong một batch job).
3. KHÔNG dựng dashboard UI trong file này — hiển thị là project riêng đọc output, để sau.

**Slice mình đề xuất cắt ra (đúng MỘT lát, sống được):**
> **Slice 1 — "Moi đúng URL và tháng-năm từ một dòng log để job đếm ra số thật."**
> - Hành động: chạy job trên vài dòng log mẫu.
> - Hệ thống làm: `extract_url` trả về URL trong dòng; `extract_year_month` trả về chuỗi `YYYY-MM`; mapper phát ra `(period, url) → 1`; reducer cộng lại.
> - Nhìn thấy: thay vì `(None, None) → 5`, ra `(2016-01, url0) → 2`, `(2016-01, url1) → 1`.
> - Chấp nhận (nháp, chốt kỹ ở CONTRACT): (a) dòng hợp lệ ra đúng url + đúng tháng; (b) dòng rỗng/hỏng không làm job crash; (c) output khớp đúng khuôn ví dụ đã có trong docstring của file.

**Ba tính năng bạn hỏi → mình để vào Parking Lot, KHÔNG code:**
- Rate-limiting → cần một web service; project khác.
- Auth đăng nhập → cần endpoint + phiên user; project khác.
- Analytics dashboard → cần web UI đọc output của job này; slice sau, sau khi job cho số đúng.

**Mình sẽ KHÔNG làm gì ở lượt này:** không viết một dòng code nào; không thêm web/DB/auth; không đụng mapper/reducer/steps (chúng đã đúng); không tự chọn định dạng log khi chưa hỏi bạn.

Mình cần bạn quyết một việc trước (câu hỏi gom nhóm — bạn ở mức map nghiệp vụ nên mình hỏi từng câu một, câu này trước):

**Câu hỏi 1 (chốt hướng):** Bạn muốn đi hướng nào?
- **A. Sửa cho cái máy đếm này chạy đúng** (Slice 1 ở trên) — đúng bản chất file, nhỏ, cho ra số thật làm nền cho analytics sau này.
- **B. Bạn thật sự muốn một website pastebin có đăng nhập / rate-limit / dashboard** — nếu vậy đây là một project MỚI, không nằm trong file này; mình sẽ frame lại từ đầu, cắt slice sống đầu tiên của *web app* (ví dụ: "tạo paste → nhận link", chưa auth chưa dashboard).

(Chọn A hay B, hoặc sửa lại slice mình đề xuất.)

─── CHỜ XÁC NHẬN ───
Hiểu hiện tại: `pastebin.py` là batch job MapReduce đếm lượt xem URL theo tháng; hai hàm moi dữ liệu (`extract_url`, `extract_year_month`) đang rỗng nên job cho ra rác. Không có web/auth/dashboard trong file.
Giả định: bạn muốn máy đếm này chạy đúng (hướng A), không phải mình dựng website mới; một dòng log có URL + timestamp (định dạng thật hỏi ở CONTRACT).
Sẽ đụng file: CHƯA đụng file nào ở lượt này. Nếu bạn duyệt Slice 1, dự kiến chỉ sửa `pastebin.py` (hai hàm rỗng); mapper/reducer/steps giữ nguyên.
Mình sẽ KHÔNG: viết code bây giờ; làm rate-limiting / auth / dashboard (đã park); thêm web/DB/auth; đụng phần MapReduce đã đúng.
Chờ bạn xác nhận. Mình sẽ KHÔNG viết code tới khi bạn duyệt. (XÁC NHẬN / chọn A hay B / sửa)
