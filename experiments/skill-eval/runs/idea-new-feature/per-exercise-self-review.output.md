# idea-new-feature · per-exercise-self-review — OUTPUT (skill: idea)

Tôi là skill **`idea`**. Việc của tôi ở đây: nhận ý tưởng tính năng mới cho repo *System Design Primer*, phân loại xem nó rõ tới đâu và có làm được không, rồi dẫn bạn qua từng tầng nghiệp vụ (WHY → WHAT → WORLD MODEL) và **dừng lại ở Domain** để bàn giao. Tôi không tự viết code, không tự khai tử ý tưởng.

Tôi đã đọc repo để không nói vống. Bối cảnh tôi thấy: `README.md` là một cuốn cẩm nang học thiết kế hệ thống — mục lục các chủ đề (scalability, cache, CDN, load balancer, database, asynchronism...) cộng phần "How to approach a system design interview question" gồm 4 bước (làm rõ use case/ràng buộc → thiết kế mức cao → đi sâu từng thành phần → mở rộng quy mô). Bên `solutions/system_design/` có 9 bài giải mẫu (pastebin, twitter, web_crawler, mint, query_cache, sales_rank, scaling_aws, social_graph, cộng một `template`), mỗi bài là một `README.md` viết theo đúng 4 bước đó, kèm một file `.py`.

Ý tưởng mang vào: **per-exercise-self-review** — với mỗi bài thiết kế, cho người học một checklist/rubric để **tự chấm lời giải của chính mình**.

---

═══ ROUTER — per-exercise self-review ═══

**Độ rõ: hơi mơ hồ.** Ý lớn thì nắm được — người học tự cham bai mình. Nhưng mấy chỗ then chốt chưa chốt: chấm cái gì (chấm bài học tự viết ra, hay chấm mức hiểu bài mẫu?), chấm bằng cách nào (checklist tick tay, hay rubric có điểm, hay ai đó/cái gì đó chấm hộ?), sống ở đâu (một checklist chung cho mọi bài, hay mỗi bài `solutions/.../<tên>/` một rubric riêng?).

**Độ khả thi: khả thi rõ.** Đây là thêm nội dung Markdown vào một repo vốn toàn Markdown — không có ẩn số kỹ thuật nào chặn. Cẩm nang lại sẵn khung để bám: 4 bước "How to approach" đã là bộ tiêu chí tự nhiên để dựng checklist. Không có gì phải spike.

**→ Đi Nhánh C (đi qua GĐ1 → GĐ5).** Vì độ rõ còn hơi mơ hồ, tôi sẽ hỏi kỹ hơn một chút ở mỗi tầng chứ không lướt.

════════════════

Trước khi bàn "đáng làm không" (GĐ1 — WHY), tôi cần bạn gỡ đúng **một** khúc mơ hồ lớn nhất: rubric này chấm cái gì. Chấm nhầm đối tượng thì cả tính năng lệch, nên đây là câu phải chốt trước.

**Câu hỏi (GĐ0 → GĐ1) — chọn giúp tôi từng ý:**

**1. Rubric tự-chấm này soi vào cái gì?**
- (A) **Chấm bài người học tự viết** — người học đọc đề (vd "Design Pastebin"), tự viết lời giải của mình, rồi lấy rubric ra tự soi xem thiếu bước nào so với bài mẫu.
- (B) **Chấm mức hiểu bài mẫu** — người học đọc lời giải mẫu có sẵn, rubric là bộ câu tự kiểm ("mình có giải thích được vì sao chọn SQL không?") để biết mình đã thấm chưa.
- (C) **Cả hai** — vừa tự chấm bài mình viết, vừa tự kiểm mức hiểu bài mẫu.

**2. Cùng-đau nhất mà tính năng này gỡ là gì?** (đây là phần WHY, tôi cần một câu đau thật)
- (A) **Học một mình không có ai chấm** — repo dạy rất kỹ nhưng người học tự luyện không biết lời giải của mình đạt hay hụt, thiếu vòng phản hồi.
- (B) **Đọc lời giải mẫu thì gật gù nhưng không giữ lại được** — thiếu công cụ tự kiểm để biết đã thật sự hiểu hay chỉ đọc lướt.
- (C) Một cái đau khác — bạn nói rõ giúp.

**3. Một bản rubric — dùng chung cho mọi bài, hay riêng từng bài?**
- (A) **Một rubric chung** dựa trên 4 bước "How to approach", áp cho mọi bài thiết kế.
- (B) **Mỗi bài một rubric riêng** đặt cạnh từng `solutions/system_design/<tên>/`, có tiêu chí đặc thù của bài đó (vd Pastebin: có tính ra dung lượng lưu trữ và cách sinh link ngắn không).
- (C) **Chung làm khung + riêng vài dòng đặc thù mỗi bài.**

Bạn trả lời cụm này xong, tôi tóm lại phần WHY (ai đau, đau cỡ nào, đo bằng gì) rồi mới xin **cổng: "Đáng đầu tư đi tiếp không?"** trước khi bước sang bàn cách làm (GĐ2–4).

---

Một lưu ý để bạn yên tâm về ranh giới: tôi sẽ dừng ở tầng Domain (chốt các "thực thể" nghiệp vụ như *Bài tập / Rubric / Tiêu chí / Lần tự chấm*, và luật bất biến giữa chúng), rồi bàn giao. Tôi **không** đụng tới chuyện dựng bằng công cụ gì hay viết file thật vào repo — đó là việc của `/frame` hoặc `/partner` sau này, và tôi sẽ hỏi bạn trước khi ghi bất cứ artifact nào vào chính repo *System Design Primer*.

═══ CHỜ XÁC NHẬN ═══
Đang đợi bạn chọn ở 3 câu trên (nhất là câu 1 — rubric chấm cái gì). Chọn xong tôi chốt WHY và đưa cổng go/no-go.
════════════════
