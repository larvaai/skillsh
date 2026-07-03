# idea-new-feature · cost-capacity-calculator — OUTPUT (skill: idea)

Chào bạn. Đây là ý tưởng thêm một tính năng MỚI cho chính repo **System Design Primer** — nên tôi coi đây là greenfield feature trên nền repo học tập. Tôi đã đọc README (mục lục chủ đề + Appendix) và các bài giải mẫu để bám bối cảnh, không suy diễn.

**Slug ý tưởng:** `cost-capacity-calculator` (ghi vào `state/project/system-design-primer/ideas/cost-capacity-calculator.json` — vùng state của skill, không đụng repo).
**Trạng thái đọc trước:** chưa có state cũ cho ý này (cold start). Mức người đọc lấy theo bối cảnh: L2 (hiểu nghiệp vụ, chưa rõ code flow) — nên tôi diễn giải bình dân, hạn chế thuật ngữ code.

Trước khi vào Router, tôi neo một điều tôi đã KIỂM CHỨNG trong repo (để không bịa): mỗi bài giải mẫu đều **tự tính tay** cùng một bộ số theo cùng một công thức. Ví dụ có thật:
- `pastebin`: 12.7 GB paste mới/tháng, ~450 GB trong 3 năm, 4 write/s, 40 read/s.
- `twitter`: 150 TB/tháng (10 KB/tweet × 500 triệu tweet/ngày × 30 ngày), 100 nghìn read/s.
- `mint`: 250 GB/tháng (50 byte/giao dịch × 5 tỷ giao dịch/tháng), 2.000 giao dịch/s.
- `web_crawler`: 2 PB/tháng (500 KB/trang × 4 tỷ link/tháng), 1.600 write/s.

Tất cả dùng chung một hằng số quy đổi lặp đi lặp lại trong README: **"2.5 triệu giây/tháng", "1 request/s = 2.5 triệu request/tháng"**, cộng bảng lũy thừa của 2 và bảng "Latency numbers" ở Appendix. Nói cách khác: ý tưởng của bạn là tự động hoá đúng cái việc mà repo đang dạy người ta làm bằng tay.

---

## Router — phân loại độ rõ + độ khả thi

**Độ rõ: RÕ RÀNG (khá).** Đã biết cho ai (người học đang đọc từng bài thiết kế), input là các giả định (số user, kích thước bản ghi, tỷ lệ read/write), output là QPS + storage + ước lượng cost. Ranh giới cũng khá rõ: một máy tính ước lượng gắn vào mỗi bài, không phải hệ thống production. Còn một chỗ chưa chốt: "cost" tính tới đâu (chỉ storage/QPS, hay kéo cả giá cloud thật) — đây là điểm sẽ hỏi ở GĐ2.

**Độ khả thi: KHẢ THI RÕ.** Không có ẩn số kỹ thuật hay business chặn đường:
- Công thức đã tồn tại và nhất quán trong repo (đủ 4 bài giải dùng chung cách tính) — không phải phát minh mới.
- Dữ liệu tham chiếu (powers of two, latency numbers, "2.5 triệu giây/tháng") có sẵn trong Appendix.
- Đây là repo tài liệu học, thêm một công cụ ước lượng là mở rộng tự nhiên, không đụng ràng buộc pháp lý/hạ tầng.

**→ Đi Nhánh C (đi qua GĐ1 → GĐ5).** Độ rõ đang khá cao nên tôi sẽ lướt nhanh, mỗi giai đoạn hỏi gọn, chỉ đào sâu chỗ còn ẩn số (định nghĩa "cost").

Tôi KHÔNG tự viết code, KHÔNG tự chọn framework, KHÔNG tự kill. Ta dừng lại ở Domain Model rồi bàn giao.

---

## GĐ1 — Business Discovery (WHY): tính năng này có đáng làm không?

Mục tiêu ở tầng này chỉ trả lời một câu: đáng bỏ công làm không, nói bằng cái đau cụ thể, chưa bàn cách làm.

Cái đau tôi thấy từ chính repo: mỗi bài giải, người học phải nhân chia tay cùng một bộ số (kích thước bản ghi × số sự kiện/tháng → storage; rồi chia "2.5 triệu giây/tháng" → QPS). Việc này lặp lại ở mọi bài, dễ sai số mũ (nhầm GB với TB, nhầm /ngày với /tháng), và khó thử "nếu user tăng gấp 10 thì sao". Người đọc muốn hiểu độ nhạy của con số thì phải tính lại từ đầu.

- **Ai đau:** người tự học đang luyện back-of-the-envelope; và người đọc kiểu CTO/business muốn ra nhanh một ước lượng dung lượng/chi phí mà không cần nhớ công thức.
- **Chi phí nếu không làm (thô):** không mất tiền trực tiếp, nhưng người học tính tay tốn thời gian mỗi bài và dễ ra số sai — làm giảm giá trị dạy học của repo ở đúng phần "estimation" mà repo tự nhận là kỹ năng cốt lõi.
- **Success metric (đo được, gợi ý):** người dùng nhập giả định của một bài (vd pastebin) và nhận lại đúng bộ số mà bài đó đã in sẵn (12.7 GB/tháng, 40 read/s...) — tức calculator tái tạo được kết quả tính tay hiện có. Đây là mốc "đúng" kiểm chứng được ngay bằng dữ liệu repo.

Đây là việc giá trị đã khá rõ và không lớn, nên tôi giữ GĐ1 gọn đúng mức "đủ-là-đủ", không dựng Business Case 10 mục.

---

```
═══ CỔNG GO / NO-GO — GĐ1 Business ═══  (CHỜ XÁC NHẬN)
Ý tưởng: cost-capacity-calculator — máy tính QPS/storage/cost gắn vào mỗi bài thiết kế.
Đáng làm vì: repo đã dạy tính tay bộ số này ở mọi bài; tự động hoá giảm sai số mũ + cho thử "nếu ×10".
Metric đề xuất: calculator tái tạo đúng số đã in sẵn trong 4 bài giải (pastebin/twitter/mint/web_crawler).

Câu hỏi cổng: "Đáng đầu tư đi tiếp GĐ2 (Product/PRD) không?"
────────────────────────────────────────────
```

Vì tôi đang mô phỏng (không tương tác thật), đây là cụm câu hỏi tôi sẽ đưa ra ở lượt này (dạng AskUserQuestion, ≤3 câu cùng chủ đề, chỉ hỏi tầng Business — chưa hỏi kiến trúc/DB/stack):

**Câu 1 — Đi tiếp hay dừng ở đây?**
- (A) Đáng làm, đi tiếp GĐ2.
- (B) Muốn tôi phản biện thêm phần "đáng làm" trước khi quyết.
- (C) Tự thấy chưa đáng, muốn dừng — (chỉ bạn mới quyết kill, tôi sẽ ghi lý do của bạn, không tự dập).

**Câu 2 — Người dùng chính của tính năng này là ai?**
- (A) Người tự học đang luyện estimation từng bài.
- (B) Người đọc business/CTO muốn ra số nhanh, không cần nhớ công thức.
- (C) Cả hai (nếu vậy tôi sẽ ưu tiên nhóm chính khi làm rõ MVP ở GĐ2).

**Câu 3 — "Cost" ở tên tính năng nên hiểu tới đâu?** *(để định biên MVP, chưa phải chốt cứng)*
- (A) Chỉ QPS + storage (bám đúng số repo đang có, an toàn nhất).
- (B) Thêm một lớp cost thô (vd nhân storage với đơn giá $/GB tự nhập).
- (C) Kéo cả bảng giá cloud thật — (tôi sẽ đánh dấu đây là ẩn số/nguồn dữ liệu ngoài repo, cân nhắc kỹ ở GĐ2, không hứa vội).

Bạn chọn xong Câu 1 = A thì tôi mở GĐ2 (Product Discovery → PRD): brainstorm AS-IS/TO-BE, chốt MVP + cái gì cố tình KHÔNG làm, dựa trên đáp án Câu 2–3. Ta vẫn đang trên lộ trình dừng ở GĐ5 Domain rồi bàn giao — chưa chạm code.
