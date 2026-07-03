# Tune — atlas (dựa trên grade 00-atlas, gói rebuild-hex-agent)

## §0 Chẩn đoán (≤6 câu)

Chỉ 2/7 tiêu chí mất điểm: #1 BẰNG CHỨNG = 0 (rớt gate, xương sống) và #7 TƯƠI = 1; năm tiêu chí còn lại đều 2/2, tổng 11/14. Nguyên nhân #1: mọi con số/anchor/invariant sai đều đến từ việc artifact dựng từ evidence-file A/B/C mà KHÔNG truy về code gốc (15 vs 14 SECRET_KEYS, freeze neo `bootstrap.py:28-53` thay vì `kernel.py:91`, invariant "ui ⊥ core" bị `ui/server.py:21` bác) — nhưng SKILL.md đã có luật "Không claim nào thiếu evidence" và Bước 2 đã ghi "đọc codebase", nên đây PHẦN LỚN là lỗi-của-lần-chạy (agent chạy tắt qua evidence trung gian), KHÔNG phải thiếu luật. Điểm tune được là chỗ luật MƠ HỒ: SKILL.md không định nghĩa "evidence" BẮT BUỘC là code gốc (cho phép hiểu evidence = tài liệu thứ cấp), không có bước tự-verify anchor trước khi in, và không nói cách hedge con số/danh mục — đó là khe hở SKILL để agent lách. Lỗi #7 (built_commit="n/a (không phải git repo)" trong khi repo LÀ git) cũng nửa-run nửa-SKILL: SKILL.md nêu `built_commit` nhưng không buộc chạy `git rev-parse` để lấy hash thật. Tóm lại: gate-fail chủ yếu lỗi lần-chạy; phần tune được là siết luật evidence="code gốc" + thêm self-check anchor để BỊT khe hở đã bị lách.

## §1 Fixture đề xuất (cố định cả thí nghiệm)

- **project**: `/Users/uspro/Desktop/namnson/hex_agent` (code GỐC — không phải evidence file, không phải `rebuild-hex-agent/`). Đây là điểm mấu chốt: fixture phải là repo thật để đo được tiêu chí 1 "đối chiếu code gốc".
- **chế độ chạy**: full build một lượt (Bước 2 của atlas), sinh `ATLAS.md` hợp nhất theo đúng form artifact hiện có.
- **git**: repo là git thật, HEAD = `63d5029` (2026-06-29); các variant PHẢI có quyền chạy `git -C <project> rev-parse --short HEAD`.
- **cấm dùng evidence trung gian**: variant KHÔNG được nhận evidence-A/B/C; nếu cho nhận thì phải cho cả baseline để giữ MỘT biến — mặc định: không phát evidence, ép mọi bản đọc code gốc.
- **ngân sách đọc**: giống nhau cho mọi bản (cùng số lượt Read / cùng trần token) để "một biến duy nhất" đúng nghĩa.
- **baseline**: atlas/SKILL.md hiện tại, cùng fixture trên.

## §2 Thước

- Rubric: `/Users/uspro/Desktop/skillsh/experiments/hex-rebuild-review/rubrics/00-atlas.rubric.md` (7 tiêu chí 0/1/2, chuẩn đối chiếu = code gốc `/Users/uspro/Desktop/namnson/hex_agent`).
- Cách chấm mỗi bản: chấm 4–7 trước (hình dạng), rồi spot-check tiêu chí 1–3 với **≥5 anchor `file:line` ngẫu nhiên** + đi lại **≥1 luồng trace** trên code gốc.
- **Luật xếp hạng**: loại hết bản RỚT GATE (bất kỳ tiêu chí 1/2/3 = 0) TRƯỚC; các bản còn lại xếp theo TỔNG; hoà tổng thì bản có diff nhỏ/robust hơn thắng.

## §3 Các hướng thử (mỗi hướng nhắm ĐÚNG MỘT tiêu chí đang mất điểm)

Chỉ 2 tiêu chí mất điểm → A/B/C nhắm tiêu chí 1 (ba khe hở khác nhau của cùng lỗi), D nhắm tiêu chí 7. Không tạo hướng cho tiêu chí đã 2/2 (phí agent).

### Hướng A — Định nghĩa evidence = CODE GỐC (nhắm tiêu chí 1)
Giả thuyết: luật "không claim nào thiếu evidence" quá mơ hồ về "evidence là gì" → agent tự cho evidence = tài liệu thứ cấp; chốt cứng evidence phải là code gốc thì con số/anchor không còn lấy từ file trung gian.

DIFF (sửa gạch đầu dòng trong "Luật cứng" của SKILL.md):
```
- **Không claim nào thiếu evidence.** Mọi nhận định kèm: file path · symbol · dòng/đoạn code · suy luận · độ chắc chắn.
+ **Không claim nào thiếu evidence, và evidence PHẢI là CODE GỐC.** Mọi nhận định kèm: file path · symbol · dòng/đoạn code (mở & đọc trực tiếp trong repo đích) · suy luận · độ chắc chắn.
+   Tài liệu thứ cấp (brief, evidence file, doc, README) KHÔNG phải evidence hợp lệ để chốt một claim về code — chỉ dùng làm gợi ý, rồi PHẢI mở đúng file:line trong repo xác nhận. Mọi con số/danh mục (số key, số event, số test…) phải đếm được trên code gốc; chưa đếm thì hedge "~N (chưa verify trên code, nguồn: <X>)" và đẩy vào 18_risks_and_unknowns.
```
Rủi ro: tốn token hơn (buộc mở file thật thay vì trích brief) — có thể chạm trần ngân sách trên repo lớn; nếu vậy phải cân bằng độ phủ.

### Hướng B — Thêm bước "verify anchor" trước khi in (nhắm tiêu chí 1)
Giả thuyết: agent copy `file:line` từ nguồn nhớ mà không kiểm → anchor trỏ nhầm hàm (freeze về `bootstrap.py:28-53`); thêm một self-check bắt buộc grep/đọc lại từng anchor xương sống trước khi ghi sẽ bắt lỗi trỏ-nhầm.

DIFF (chèn một sub-bước vào Bước 2 Full build, sau mục 3 "Sinh đủ artifact"):
```
+ 3b. **Self-verify anchor (bắt buộc, trước khi coi là xong).** Với mọi anchor xương sống (7 bất biến, mỗi chokepoint/gate/guard, mọi con số trong contract), mở lại đúng `file:line` và xác nhận symbol/hành vi khớp claim. Ghi kết quả một dòng "anchor spot-check: N/N khớp" vào 20_understanding_scorecard.md. Anchor không khớp → sửa hoặc hạ xuống 18_risks_and_unknowns; KHÔNG in như fact.
```
Rủi ro: có thể thành "diễn" (agent tự khai đã verify mà không thật) nếu không kèm sản phẩm kiểm được — nên buộc ghi dòng spot-check ra scorecard để chấm được.

### Hướng C — Bảng đối chiếu số/danh mục (nhắm tiêu chí 1)
Giả thuyết: lỗi tập trung ở con số/danh mục (14 key, số event, số test) bị bê nguyên từ nguồn thứ cấp và in như fact; buộc mỗi con số đi kèm LỆNH đếm cụ thể sẽ chặn số stale.

DIFF (thêm gạch đầu dòng vào "Luật cứng"):
```
+ **Mọi con số phải đếm được, kèm cách đếm.** Mỗi con số/danh mục (số SECRET_KEYS, số event/command type, số test…) ghi kèm cách đếm trên code gốc (vd "14 key — đếm `control/redaction.py:16-33`", "count `def test_` = `grep -rc 'def test_'`"). Không có cách đếm → không được in con số như fact; hedge + đẩy vào unknowns với priority.
```
Rủi ro: trùng một phần với A (A cũng nói con số phải đếm) — nếu chạy cả A và C, tách rõ: A = định nghĩa evidence tổng quát, C = riêng con số + LỆNH đếm; nếu ngân sách hẹp, gộp C vào A và dùng slot cho hướng khác.

### Hướng D — Neo phiên bản bằng git thật (nhắm tiêu chí 7)
Giả thuyết: tiêu chí 7 mất điểm vì agent tự phán "không phải git repo" mà không chạy lệnh; buộc chạy `git rev-parse` và ghi kết quả sẽ sửa built_commit + mở đường drift.

DIFF (sửa Bước 2 mục 4 "Ghi 00_index.md"):
```
- **Ghi `00_index.md`** (mục lục + trạng thái + `built_at` + `built_commit`), ...
+ **Ghi `00_index.md`** (mục lục + trạng thái + `built_at` + `built_commit`). LẤY built_commit bằng `git -C <project-path> rev-parse --short HEAD 2>/dev/null`; có hash → ghi hash + ISO date của HEAD; rỗng (thật sự không git) → ghi "n/a — <lý do đã kiểm: không có .git>". CẤM tự phán "không phải git repo" khi chưa chạy lệnh.
```
Rủi ro: hẹp — chỉ nhấc tiêu chí 7 từ 1→2 (0.5–1 điểm), không cứu gate; đáng chạy kèm A/B nhưng một mình D không đổi kết cục gate.

## §4 Ưu tiên

**Để sau (thiên về "không đáng tune nếu chỉ vì lần chạy này").** Grade cao (11/14, 5/7 tiêu chí đạt trần) và bản chất gate-fail là lỗi-của-lần-chạy: SKILL.md đã yêu cầu đọc codebase + evidence cho mọi claim, agent lại chạy tắt qua evidence file. Chỉ nên bỏ 1 agent thử hướng A (siết evidence="code gốc") vì đó là khe hở SKILL thật đã bị lách; nếu chạy lại đúng fixture (code gốc, không phát evidence trung gian) mà baseline đã tự qua gate thì KHÔNG đáng tune tiếp — vấn đề là quy trình chạy, không phải prompt.

## §5 Nhắc luật thí nghiệm

- **Baseline trước:** chạy atlas/SKILL.md hiện tại trên fixture code-gốc, chấm bằng rubric → mốc. Rất có thể baseline tự qua gate khi bị ép đọc code gốc (không phát evidence) — nếu vậy dừng, kết luận lỗi-lần-chạy.
- **Một biến duy nhất:** mọi variant cùng project (code gốc), cùng chế độ full-build, cùng ngân sách đọc, cùng KHÔNG-có evidence trung gian; chỉ khác bản sửa SKILL.
- **Chấm mù:** người/agent chấm chỉ thấy {project, output}, không thấy variant theo hướng nào; đặt tên A/B/C/D.
- **Confirm bản thắng bằng agent MỚI + fixture thứ hai:** chạy lại proposed-SKILL của bản thắng bằng agent mới trên (a) `hex_agent` và (b) một repo khác (vd một repo Python thật khác trong máy) để chắc điểm đến từ SỬA, không từ agent giỏi hay over-fit đúng repo này. Chỉ hơn ở fixture gốc → nghi over-fit, xem lại diff.
- **Không đụng bản thật khi thử:** mỗi bản nằm trong `experiments/runs/<ts>/<variant>/`; chỉ merge vào `atlas/SKILL.md` sau khi bản thắng qua confirm.
