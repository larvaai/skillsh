# TUNE — explain (gói rebuild-hex-agent) · vòng 2026-07-02

Nguồn chấm: `experiments/hex-rebuild-review/grades/explain.grade.md` (21/24, gate ĐẠT).
Artifact: `rebuild-hex-agent/explain/EXPLAIN.md`.
Thước dùng chấm variant: `experiments/hex-rebuild-review/rubrics/explain.rubric.md` (v2, thang 0–3, tổng 24).

## §0 Chẩn đoán (≤6 câu)

Ba khe mất điểm, tất cả nằm ở tiêu chí NON-GATE nên bản không rớt: tiêu chí 6 (nhất quán, =2), tiêu chí 7 (lời văn, =2), tiêu chí 1 (bám bằng chứng, =2). Tiêu chí 6: claim tuyệt đối "đúng MỘT cửa" (EXPLAIN.md:32) không được scope NGAY tại chỗ phát biểu ở Zoom 1 — hoà giải "delegation là cửa riêng" tới bước 4-5 mới nói, và đây là lỗi-của-SKILL vì chính ví dụ mẫu trong SKILL.md:205 dạy đúng câu tuyệt đối không-scope đó (SKILL.md:60 còn viết "cái cửa duy nhất" y hệt). Tiêu chí 7: câu-dài-nối-em-dash+chấm-phẩy lặp thành tật (EXPLAIN.md:32/46/48/62) DÙ luật E1–E4 đã có trong principles.md — nghĩa là E2 hiện tại ("đọc to hết hơi") quá mềm, không gọi đích danh pattern em-dash/chấm-phẩy chồng, đây là luật-mơ-hồ cấp SKILL. Tiêu chí 1: "0 rò state" (EXPLAIN.md:62) là thuộc-tính-thiết-kế trình bày như đã-đạt trên rebuild chưa-có-code mà không gắn nhãn "invariant, chưa đo" — nửa lỗi-lần-chạy (agent quên nhãn) nửa lỗi-SKILL (không có luật buộc gắn nhãn cho con-số/thuộc-tính chưa-đo, và ví dụ mẫu SKILL.md:218/224 cũng thả "0 rò state" trần y hệt). Kết: phần lớn là lỗi-của-SKILL vì ví dụ mẫu — thứ model calibrate theo mạnh nhất — đang NÊU GƯƠNG cả ba khe; đáng tune.

## §1 Fixture đề xuất (cố định cả thí nghiệm)

- **project**: `/Users/uspro/Desktop/namnson/hex_agent` (code gốc để spot-check tiêu chí 1) — nhưng artifact giải thích là bản rebuild trong gói `rebuild-hex-agent/`, đọc nguồn thượng nguồn `00-understanding/ATLAS.md` + `REBUILD-BRIEF.md` + `review/REVIEW.md`. Giữ NGUYÊN cặp này để khe "0 rò state / chưa-có-code" còn tồn tại (đổi sang project đã-có-code thì khe tiêu chí 1 biến mất, mất điểm thử).
- **level**: L3 (flow) — trùng fixture đã sinh artifact và ví dụ mẫu trọng tâm trong SKILL.
- **mode**: overview.
- **tham số**: mỗi variant sinh lại một EXPLAIN.md L3·overview cho cùng bản rebuild, tuân `proposed-SKILL.md` của chính nó. Ghi 3 hằng số ra `experiments/runs/<ts>/fixture.txt`.

## §2 Thước

Chấm bằng `experiments/hex-rebuild-review/rubrics/explain.rubric.md` (v2, 8 tiêu chí ×0–3 = 24; gate = tiêu chí 1/2/3). Luật xếp hạng: **loại bản rớt gate trước, còn lại xếp theo tổng; hoà tổng → bản diff NHỎ/ROBUST hơn thắng**. Chấm mù theo đúng "Cách chấm bắt buộc" của rubric (đọc thân trước, lập bảng kiểm thuật ngữ, spot-check ≥3 claim code, đọc tự-soi CUỐI).

## §3 Hướng thử (mỗi hướng một biến, nhắm một tiêu chí khác nhau)

Ba khe điểm đều thuộc phần model học từ VÍ DỤ MẪU trong SKILL.md → mỗi hướng sửa đúng một chỗ trong ví dụ/luật, không đụng cấu trúc thang zoom.

### A — nhắm tiêu chí 6 (nhất quán): scope claim tuyệt đối NGAY tại chỗ, sửa trong ví dụ mẫu
Giả thuyết: nếu ví dụ mẫu tự scope "một cửa" ngay câu ý-tưởng-cốt-lõi, artifact sinh ra sẽ scope theo → tiêu chí 6 lên 3.
DIFF (SKILL.md, sửa dòng "Ý tưởng cốt lõi (một câu)" trong ví dụ mẫu, ~dòng 205):
```
- > Mọi hành động ra thế giới bên ngoài đều phải đi qua đúng một cái cửa — không có
-   đường tắt — nên mọi thứ đều ghi log được, chặn được, và tua lại được từ một nguồn
-   sự thật duy nhất.
+ > Mọi lệnh gọi-tool và gọi-model đi qua đúng một cái cửa (giao-việc cho agent con cố
+   tình đi cửa TÁCH RIÊNG — để quyền không leo thang); nhờ vậy mọi hành động đều ghi
+   log được, chặn được, tua lại được từ một nguồn sự thật duy nhất.
```
Thêm 1 dòng dưới Luật neo #2 (SKILL.md:28): "Claim tuyệt đối (‘duy nhất’, ‘mọi’, ‘không bao giờ’) phải kèm phạm vi NGAY câu đó; ngoại lệ gọi tên là ngoại lệ + lý do."
Rủi ro: scope-ngay có thể làm câu ý-tưởng-cốt-lõi dài hơn → chạm tiêu chí 7 (câu dài). Giữ vế trong ngoặc thật ngắn.

### B — nhắm tiêu chí 7 (lời văn): mài E2 gọi đích danh pattern em-dash/chấm-phẩy chồng
Giả thuyết: E2 hiện quá mềm nên tật vẫn lọt; nêu đích danh pattern + trần số mệnh đề sẽ chặn được → tiêu chí 7 lên 3.
DIFF (principles.md, thay thân E2 — CHỈ một biến là luật lời văn):
```
- E2. **Câu ngắn, phẳng.** Mỗi câu một ý. Không câu lồng nhiều mệnh đề, không
-   "mà trong đó / theo đó / nhờ vậy mà" nối dài. Đọc to hết hơi một lần là quá dài — cắt.
+ E2. **Câu ngắn, phẳng — tối đa một dấu nối.** Mỗi câu một ý. CẤM chồng nhiều
+   em-dash (—) hoặc chấm-phẩy (;) trong một câu để nhồi mệnh đề; một câu dùng NHIỀU
+   NHẤT một dấu nối phụ. Ý thứ hai → tách thành câu mới. Không "mà trong đó / theo
+   đó / nhờ vậy mà" nối dài.
```
Rủi ro: over-fit thành văn cụt lủn, mất nhịp kể; giữ nguyên E1/E3/E4 để chỉ đo tác động của một luật.

### C — nhắm tiêu chí 1 (bám bằng chứng): buộc gắn nhãn thuộc-tính/con-số CHƯA-ĐO trên rebuild
Giả thuyết: khe duy nhất còn đứng ở tiêu chí 1 là "0 rò state" thiếu nhãn; một luật buộc gắn nhãn + sửa gương trong ví dụ mẫu sẽ đóng khe → tiêu chí 1 lên 3.
DIFF-1 (SKILL.md, thêm gạch đầu dòng dưới "Quy tắc", ~dòng 21):
```
+ - **Thuộc-tính-thiết-kế chưa đo phải gắn nhãn.** Con số/khẳng định là ĐÍCH thiết kế
+   (invariant) chứ chưa đo trên code hiện có → viết "(invariant đích, chưa đo)".
+   Không trình bày như đã-đạt. Áp cho mọi "0 …", "N …" gánh kết luận.
```
DIFF-2 (SKILL.md, sửa gương trong ví dụ mẫu ~dòng 218):
```
- ...nên nhiều run không giẫm lên nhau.
+ ...nên nhiều run không giẫm lên nhau (invariant đích — chưa đo trên bản này).
```
Rủi ro: nhãn rải nhiều nơi làm nặng văn (chạm tiêu chí 7); chỉ áp cho con-số/thuộc-tính GÁNH kết luận, không rải mọi câu.

### D — nhắm tiêu chí 5 (chế độ & vai): cấm dán nhãn mode vào câu/tiêu đề mở
Giả thuyết: mâu thuẫn rubric↔skill #2 (vòng trước) chưa fix trong SKILL; artifact đang dán "chế độ overview · mức L3" ở header (EXPLAIN.md:1) — cấm dán nhãn mode giúp bài được chấm-theo-cấu-trúc, giảm rủi ro grader lệch → khoá tiêu chí 5 ở 3 robust hơn.
DIFF (SKILL.md, thêm dưới "Tự soi trước khi gửi", ~dòng 192):
```
+ - KHÔNG dán nhãn chế độ ("chế độ overview/flow") vào câu mở hay tiêu đề như bằng chứng
+   mode. Chế độ phải đọc ra được TỪ CẤU TRÚC (Zoom 0–1 không tên code → luồng đánh số →
+   module). Nhãn tự dán không cứu bài sai cấu trúc.
```
Rủi ro: tiêu chí 5 đang là 3 rồi (grade); hướng này CỦNG CỐ chứ khó tăng điểm — có thể "để sau" nếu cần dồn agent cho A/B/C. Giữ để đo xem có phụ-thu tiêu chí nào không.

### E (tuỳ chọn, chỉ nếu còn agent) — sửa RUBRIC làm đối tượng: siết mức-3 tiêu chí 1 định nghĩa "nhãn chưa-đo"
Giả thuyết: thước là một phần của hệ; grade cho 2 vì mức-3 đòi "chỗ chưa chắc gắn nhãn rõ" nhưng chưa nêu ví dụ CHUẨN nhãn cho thuộc-tính-thiết-kế-rebuild — làm rõ anchor giúp chấm nhất quán giữa lens.
DIFF (rubrics/explain.rubric.md, tiêu chí 1 mức-3, dòng 25): thêm cuối câu: "— với claim thiết-kế-rebuild chưa có code, ‘gắn nhãn rõ’ = ghi ‘invariant đích, chưa đo’ ngay tại con số."
Biến ở đây là THƯỚC, không phải explain → chạy tách, KHÔNG trộn cùng lượt chấm A–D (đổi thước giữa chừng là hỏng thí nghiệm). Rủi ro: sửa thước rồi tự chấm bằng thước đã sửa = vòng lặp thiên vị; phải để agent chấm-mù thứ hai xác nhận.

## §4 Ưu tiên

**Tune ngay — hướng A và B; C tune ngay nếu còn agent; D+E để sau.**
Lý do: grade 21/24 nhưng ba khe A/B/C là lỗi-của-SKILL (ví dụ mẫu và luật E2 đang nêu gương xấu), sửa nhỏ đóng khe kéo 21→23–24 mà không đụng cấu trúc — đáng tune. D chỉ củng cố tiêu chí đã 3, E là việc mài thước tách bạch; cả hai không phải đòn bẩy chính nên xếp sau.

## §5 Nhắc luật thí nghiệm

- **Chấm mù**: grader chỉ thấy {project, level, mode, output}, không thấy variant theo hướng nào; theo đúng "Cách chấm bắt buộc" của rubric (thân trước, tự-soi cuối).
- **Baseline trước**: chạy explain HIỆN TẠI trên fixture, chấm, làm mốc — không có baseline thì "23/24" vô nghĩa. (Baseline kỳ vọng = 21/24 khớp grade hiện có; nếu lệch, nghi nhiễu-agent, chạy lại.)
- **Một biến duy nhất**: A sửa ví-dụ+neo#2, B sửa E2, C sửa quy-tắc+gương, D sửa tự-soi, E sửa THƯỚC — không hướng nào đụng biến của hướng khác; A–D chấm bằng CÙNG thước gốc, E chấm tách.
- **Confirm bản thắng**: chạy `proposed-SKILL.md` bản thắng bằng agent MỚI trên (a) đúng fixture và (b) fixture thứ hai khác domain (vd `nocode_platform` như vòng trước) — hơn baseline ở CẢ HAI mới là điểm-từ-SỬA, không phải agent-viết-giỏi hay over-fit vào hex.
