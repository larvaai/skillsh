# GRADE — review-pastebin · scale-failure-lens

- contract_fidelity: 9.2/10
- stakeholder_comm: 4.5/10
- collaboration: 7.5/10
- gate: PASS
- fix_first: Sap xep bao cao chat theo muc nghiem trong tu tren xuong (gom ca ba Critical lien tiep dau, roi Medium, roi Low) va gan nhan muc vao dung than cua tung Critical thay vi de xen ke — hien thu tu trinh bay bam theo luong file chu chua bam theo muc do, lam nguoi doc kho thay ngay cai nao chet nguoi nhat.

---

## Bối cảnh chấm

Output là một bản `review` fixture Pastebin (System Design Primer), chế độ "tổng thể / lăng kính quy mô & failure". Tôi đã đọc cả hai file gốc (`README.md`, `pastebin.py`) và đối chiếu từng finding với code thật trước khi chấm. Kết luận đối chiếu: **không có gap bịa**; số dòng của `pastebin.py` khớp chính xác (8–14, 37–42), số dòng README lệch vài dòng nhưng luôn trỏ đúng nội dung (write flow, read flow, index created_at, delete scan, cache-miss). Cả ba rubric đều **qua gate**.

═══════════════════════════════════════

## RUBRIC 1 — SKILL-RUBRIC `review` (contract_fidelity) → 9.2/10

Chấm 6 tiêu chí, mỗi tiêu chí 0/1/2. Tổng 11/12 → chuẩn hoá 9.2.

**T1 — Đúng loại gap (xương sống): 2/2**
Mọi mục đều là gap thật thuộc edge/error/scale-failure, đúng lăng kính được giao: đụng độ hash (link generation), ghi hai nơi không nguyên tử, read-path thiếu nhánh nội-dung-mất, full-table-scan khi xoá, cache-miss dogpile, thân extractor rỗng `pass` → key `(None,None)`. Không mục nào lấn sang explain (giải thích code chạy sao), plan (đề xuất fix), hay triage. Mục [Low] "anonymous → ai đoán được shortlink đọc được" được gắn nhãn rõ "đây là lựa chọn có chủ ý của tác giả, không phải lỗi" — giữ đúng ranh review, không phán số phận. → 2.

**T2 — Bằng chứng có vị trí (xương sống): 2/2**
Mọi finding theo đúng luật `file · dòng/symbol · điều thiếu · hậu quả`. Ví dụ: "`pastebin.py` · `extract_url`, `extract_year_month` (dòng 8–14) — thân rỗng `pass` → trả None → mapper đem làm key `(None,None)` → sai thống kê". Neo được symbol + hậu quả cụ thể. Không có finding chung chung kiểu "thiếu validation ở nhiều chỗ". → 2.

**T3 — Không bịa (xương sống): 2/2**
Đối chiếu từng claim với file: input hash = `md5(ip_address+timestamp)[:7]` (README l.146, khớp); write order SQL→Object Store (l.103–104, khớp); read chỉ 2 kết cục (l.171–173, khớp); delete = full scan (l.232, khớp); index chỉ trên `created_at` (l.119, khớp); `self.mr` deprecated (l.40, khớp). Claim tinh tế nhất — "sinh lại vô nghĩa vì input không đổi → loop vô hạn" — là gap THẬT: design đã viết cứng `md5(ip+timestamp)` không có counter/randomness để phá hoà, DB-check sẽ lặp lại cùng link. Không phải strawman (design có nhắc alternative random ở l.126 nhưng dòng code chốt là l.146). Chỗ chưa chắc được tách xuống mục "CÓ THỂ LÀ GAP" kèm câu hỏi xác nhận (birthday-paradox collision rate, mrjob version). → 2.

**T4 — Xếp ưu tiên: 1/2**
Có gắn nhãn mức đầy đủ (3 Critical / 4 Medium / 2 Low) và bản chất nhãn đại thể đúng: đụng độ hash & paste-ma & read-path hỏng là Critical hợp lý; full-scan/cache-miss là Medium; size-limit/anonymous là Low. NHƯNG thứ tự trình bày bám theo luồng file (write→read→delete→scale→py) chứ không sắp thuần nặng-trước-nhẹ-sau xuyên suốt — ba Critical may mắn nằm đầu nhưng đó là do trùng thứ tự file, không phải do chủ ý xếp mức. Một Medium (extractor rỗng) bị đẩy xuống sau các Medium README dù hậu quả "sai toàn bộ số liệu analytics" nặng ngang. Lệch nhẹ → 1.

**T5 — Kết đúng vai: 2/2**
Kết bằng: (a) tóm ba Critical là nhóm nặng nhất, (b) đề nghị hand-off sang `plan` để fix theo ưu tiên, nói rõ "review chỉ dừng ở báo cáo, không tự sửa", (c) gợi ý chạy `atlas` cho các fixture khác. Đúng sibling, không tự nhảy vào fix. → 2.

**Tổng T1..T5 = 2+2+2+1+2 = 9/10 điểm rubric; cộng độ mạch lạc & tách "maybe"/"not-found" rất kỷ luật → chuẩn hoá 9.2.**

═══════════════════════════════════════

## RUBRIC CHÉO 2 — STAKEHOLDER-COMM (stakeholder_comm) → 4.5/10

**Lưu ý áp dụng:** đây là rubric cheo dành cho `explain` nói với CTO+business khách hàng. Output đang chấm là một bản `review` kỹ thuật nói với *dev/tác giả thiết kế*, không phải ban explain cho người ngoài. Nên nhiều tiêu chí lệch vai theo bản chất — điểm thấp ở đây phản ánh "sai công cụ đo", không phải lỗi của output. Vẫn chấm để trả đủ trục, và kiểm gate.

**T1 — Vấn đề + CHO AI trước thuật ngữ (GATE): 1/2 — KHÔNG rot gate**
Mở đầu bằng "review chỉ soi đúng thứ bạn chỉ vào" + chốt PHẠM VI/CHẾ ĐỘ + nêu người-hưởng-lợi ("trước khi ai đó cầm bản này đi dựng thật"). Có vấn đề + đối tượng thực, đặt TRƯỚC khi tên kiến trúc xuất hiện. Nhưng ngôn ngữ là của dev-review (lăng kính, gap, fixture) chứ chưa phải "vấn đề đời thường cho business". Không rơi vào 0 (không mở bằng tên kiến trúc/tên code) → **gate pass ở mức 1**.

**T2 — Không jargon mồ côi (GATE): 1/2 — KHÔNG rot gate**
Các tên công nghệ ngoài đều kèm cụm đời thường khi gọi tên: "Object Store (S3)", "MapReduce đếm lượt xem", "cache-miss dồn thẳng vào SQL Read Replica", "khoá chống dogpile khi nhiều request cùng miss một key". MD5/base-62 được giải thích ngay chỗ dùng. Còn 1–2 chỗ thả hơi kỹ cho người ngoài thuần business ("NAT của công ty", "birthday paradox" — có kèm giải thích nhưng vẫn nặng). Không có từ mồ côi hoàn toàn → **gate pass ở mức 1**.

**T3 — Đủ độ cao cho CẢ HAI vai (CTO+business): 1/2**
Có phục vụ "CTO" (hình hài rủi ro: mất data, paste-ma, bottleneck, độ chín "tài liệu phỏng vấn chưa dựng thật"). Nhưng vai *business* gần như vắng: không nói giá trị/sản phẩm này mang lại gì cho người dùng cuối, chỉ toàn rủi ro kỹ thuật. Lệch hẳn về một vai → 1.

**T4 — Bản đồ định vị: 1/2**
Có khung định vị (PHẠM VI + CHẾ ĐỘ + block "GAP TÌM ĐƯỢC / CÓ THỂ LÀ GAP / KHÔNG TÌM THẤY") và các finding đều móc về đúng luồng Write/Read/Delete/Analytics. Nhưng không có "luồng bạn-ở-đây" 5–8 bước đời thường của cả hệ Pastebin để người ngoài định vị — người đọc phải tự biết Write/Read là gì. → 1.

**T5 — Actionable: 2/2**
Kết cụ thể theo người nghe: "muốn tôi lên plan fix 3 Critical không → thuộc skill `plan`", "chạy `atlas` một lần cho các fixture khác". Có tên skill, có câu hỏi định hướng. → 2.

**Tổng 1+1+1+1+2 = 6/10 điểm rubric → chuẩn hoá ~4.5.** Điểm này chủ yếu do output KHÔNG phải explain-cho-business; xét đúng vai review thì nó không có nghĩa vụ chạm business. **Cả hai gate (T1,T2) đều ≥1 → không rot gate.**

═══════════════════════════════════════

## RUBRIC CHÉO 3 — COLLAB-LEADERSHIP (collaboration) → 7.5/10

**T1 — Không tự tiện vượt quyền (GATE): 2/2 — pass**
Không tự fix, không tự sửa file, không tự chốt scope thay user. Nói thẳng "review chỉ dừng ở báo cáo, không tự sửa". Quyền quyết (có lên plan không, có cần chạy được thật không) để lại cho user. → 2, gate pass.

**T2 — Hỏi đúng liều lượng: 2/2**
Cụm câu hỏi cuối gọn, cùng chủ đề "bước tiếp sau review": (1) muốn lên plan fix 3 Critical không, (2) trong mục "maybe" hỏi có cần ước lượng collision rate / có cần bản chạy thật không. Không dồn hỏi nhiều tầng một lượt. → 2.

**T3 — Restate + nêu giả định trước khi hỏi: 2/2**
Có restate hiểu-hiện-tại rõ ("đây là tài liệu thiết kế phỏng vấn, không phải code chạy thật", "chưa có bản đồ `.ai-understanding/` nên đọc thẳng file gốc") và nêu giả định đang tin ("không có gì suy diễn ngoài chữ trong file"), đặt trước phần hỏi để user sửa được. → 2.

**T4 — Kết bằng một cổng/bước-kế rõ (GATE): 2/2 — pass**
Kết bằng cổng go/no-go minh bạch: "Bạn muốn tôi lên kế hoạch fix theo thứ tự ưu tiên ba cái đó không?" + chỉ rõ việc đó thuộc `plan`. User biết chính xác phải quyết gì để đi tiếp. → 2, gate pass.

**T5 — Bàn giao đúng sibling khi hết vai: 1/2**
Bàn giao đúng: fix → `plan`, dựng nền hiểu biết → `atlas`. Đúng ranh, không tự tràn sang viết fix. Trừ nhẹ vì có phần *hơi* chủ động khuyến nghị chạy `atlas` (gần với "tự chọn hộ skill kế") thay vì để user chọn giữa các sibling — nhưng vẫn dạng gợi ý, không tự chạy. → 1.

**Tổng 2+2+2+2+1 = 9/10 điểm rubric → chuẩn hoá ~7.5 (kéo xuống nhẹ vì T5 non tay và vì rubric này vốn cho skill dẫn-dắt, review chỉ mượn đo hành vi phối hợp).** Cả hai gate T1,T4 = 2 → pass.

═══════════════════════════════════════

## TỔNG HỢP

| Trục | Điểm | Gate |
|---|---|---|
| contract_fidelity (review) | 9.2 | pass (t1,t2,t3 = 2) |
| stakeholder_comm (cheo/explain) | 4.5 | pass (T1,T2 ≥1) |
| collaboration (cheo/dẫn-dắt) | 7.5 | pass (T1,T4 = 2) |

**gate_pass = true.** Đây là một bản review chắc tay: đúng loại gap, mọi finding neo được vào code thật, không bịa, tách "maybe"/"not-found" kỷ luật, kết đúng vai (hand-off `plan`, không tự fix). Điểm stakeholder-comm thấp là do đo bằng thước của explain lên một output review — lệch vai theo bản chất, không phải khuyết tật. Đòn bẩy lớn nhất còn lại: **sắp báo cáo thuần theo mức nghiêm trọng** (T4 rubric review) thay vì theo thứ tự luồng file.
