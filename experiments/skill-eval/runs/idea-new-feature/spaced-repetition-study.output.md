# idea-new-feature · spaced-repetition-study — OUTPUT (skill: idea)

Đã đọc repo trước khi phân loại (README.md — mục lục chủ đề; thư mục `solutions/system_design/`) để không bịa. Vài mốc tôi bám vào:

- Repo này là **tài liệu học** (README là mục lục các chủ đề: scalability, CAP, consistency/availability, DNS, CDN, load balancer, DB replication/sharding, cache, asynchronism, TCP/UDP/RPC/REST, security) cộng vài bài giải mẫu (`mint`, `pastebin`, `twitter`, `web_crawler`, `social_graph`, `sales_rank`, `query_cache`, `scaling_aws`).
- **Repo ĐÃ có sẵn spaced repetition rồi**: mục "Anki flashcards" (README dòng 46–59) ship 3 bộ thẻ `.apkg` trong `resources/flash_cards/`, dùng đúng cơ chế lặp lại ngắt quãng qua app Anki. Đây là va chạm trực tiếp với ý tưởng được giao.

Chưa tìm thấy state `idea` nào cho project này → đây là ý mới, cold start.

Vào Router.

═══ ROUTER — spaced-repetition-study (chế độ học lặp lại ngắt quãng) ═══
Độ rõ:     **mơ hồ** — mới có tên tính năng, chưa rõ "chế độ học" này SỐNG Ở ĐÂU và CHẠY BẰNG GÌ. Repo hiện là tài liệu tĩnh (Markdown + vài file `.py` bài giải), không có app/runtime để "chạy" một chế độ ôn tập tương tác. Cũng chưa rõ thẻ lấy từ đâu: bịa tay, hay rút tự động từ chủ đề trong README.
Độ khả thi: **chưa rõ** — không phải "làm được / không làm được", mà là còn một ẩn số chặn đường: repo đã có Anki deck spaced-repetition sẵn, nên "làm thêm một cái nữa" chỉ đáng nếu nó GIẢI được cái Anki chưa giải. Chưa biết cái đó là gì thì chưa định được hình tính năng.

→ Vào **Nhánh B — SPIKE**. Nhưng theo quy tắc Nhánh B: ý còn mơ hồ thì **làm rõ nhu cầu trước, rồi mới đặt ẩn số spike** — spike quanh một nhu cầu còn mờ = học nhầm thứ. Nên lượt này tôi hỏi 3 câu gọt đúng feature trước, chưa chốt time-box vội.
════════════════

Tôi CHƯA tự build, CHƯA tự kill. Chỉ đang gọt cho đúng nhu cầu. Ba câu dưới đây (mô phỏng khối AskUserQuestion):

┌─ CÂU HỎI 1/3 — Cái đau thật là gì? ─────────────────────────
│ Anki deck sẵn có trong repo đã cho ôn thẻ ngắt quãng rồi. Vậy cái
│ khó chịu bạn muốn xử là gì?
│  A. Anki là app ngoài, phải rời repo — muốn ôn NGAY trong repo khi đang đọc.
│  B. Deck Anki là thẻ chết, không link về đúng chủ đề/bài giải để đọc sâu lại.
│  C. Không đo được "mình yếu chủ đề nào" (vd hay quên sharding, cache).
│  D. Khác (bạn mô tả).
└──────────────────────────────────────────────────────────────

┌─ CÂU HỎI 2/3 — Thẻ đến từ đâu? ─────────────────────────────
│ Nguồn nội dung thẻ quyết định độ khả thi rất nhiều.
│  A. Viết tay một bộ thẻ nhỏ (câu hỏi/đáp) do người soạn.
│  B. Rút tự động từ các chủ đề/heading trong README (VD hỏi "CAP theorem là gì?").
│  C. Rút từ các bài giải trong solutions/ (pastebin, twitter, web_crawler...).
│  D. Chưa nghĩ tới — bạn gợi ý giúp.
└──────────────────────────────────────────────────────────────

┌─ CÂU HỎI 3/3 — Nó chạy trên nền gì? ────────────────────────
│ Repo giờ là tài liệu tĩnh, chưa có chỗ để "chạy" chế độ học tương tác.
│  A. Chỉ cần thứ tĩnh: thêm file Markdown/checklist ôn tập, không cần chạy gì.
│  B. Một script CLI Python nhỏ (repo đã có sẵn Python) hỏi–đáp ở terminal.
│  C. Một trang web tĩnh nhúng trong repo (GitHub Pages).
│  D. Chưa quyết — muốn nghe tôi phản biện từng lựa chọn.
└──────────────────────────────────────────────────────────────

Vì sao chưa đặt time-box spike ngay: ẩn số lớn nhất bây giờ KHÔNG phải kỹ thuật ("spaced repetition có chạy được không" — Anki đã chứng minh chạy được). Ẩn số là **giá trị**: tính năng mới này hơn gì bộ Anki đã có sẵn trong repo? Trả lời xong 3 câu trên, tôi mới đặt đúng ẩn số cần kiểm chứng và đề xuất một time-box (kiểu "1–2 ngày dựng thử bản nhỏ nhất để biết X có đáng không, kết quả có thể vứt"), rồi quay lại Router đánh giá lại độ khả thi.

Tôi sẽ không tự chọn hướng thay bạn, cũng không tự bỏ ý này — chờ bạn.

═══ CHỜ XÁC NHẬN ═══
Trả lời 3 câu trên (mỗi câu chọn A/B/C/D, hoặc mô tả tự do). Sau đó tôi gọt lại feature và đặt ẩn số spike.
════════════════
