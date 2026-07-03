# Meta-rubric — khuôn chung cho MỌI rubric chấm skill

File này là hợp đồng chung mà mọi `<skill>/rubric.md` phải theo, và là chuẩn `grade` đọc mỗi lần chấm bất kỳ skill nào. Mục tiêu: một câu trả lời của BẤT KỲ skill nào cũng chấm được bằng cùng MỘT loại thước — để `tune` xếp nhiều bản cạnh nhau mà so được.

Nguyên tắc gốc (không đổi): **rubric chỉ biến HỢP ĐỒNG của skill thành thước đo — KHÔNG thêm tiêu chuẩn mới.** Chuẩn gốc để chấm một skill luôn là `<skill>/SKILL.md` (+ file luật con nó trỏ tới, + `quy-trinh-idea-to-operate.md` nếu là skill pipeline GĐ, + `constitution/definition-of-done.md` nếu bước có Định-nghĩa-Xong). Rubric chỉ diễn giải cái đó thành 0/1/2, không phát minh chuẩn mới.

## Bất biến mọi rubric phải giữ

1. **Thang 0/1/2.** Mỗi tiêu chí 3 mức, mỗi mức một anchor CỤ THỂ (0 = lỗi thấy được, 1 = đúng nhưng lệch, 2 = trọn). Không dùng thang khác.
2. **5–8 tiêu chí.** Đủ phủ 5 trục dưới, không phình. Skill đơn giản (checkpoint, skill-define) có thể 5; skill pipeline thường 7.
3. **Có gate.** Các tiêu chí phủ trục A1–A3 là XƯƠNG SỐNG. Bất kỳ tiêu chí gate = 0 → cả bản RỚT GATE dù tổng cao. Khi so nhiều bản: loại hết bản rớt gate TRƯỚC, rồi mới xếp phần còn lại theo tổng.
4. **Khung report cố định** (xem mẫu dưới) — để `tune` xếp nhiều bản cạnh nhau.
5. **Nêu "Đầu vào để chấm"** — rubric ghi rõ `grade` cần gì để chấm skill này (vd explain: project/level/mode/output; shape: artifact + Domain Model GĐ5). Đây cũng là **fixture** mà `tune` giữ cố định.
6. **"Vì sao các tiêu chí này"** — một đoạn cuối buộc rubric về đúng hợp đồng, chặn phình tiêu chí (thêm tiêu chí thứ n+1 chỉ khi có kiểu lỗi thật lặp lại mà bộ hiện tại không bắt được).

## 5 trục phổ quát — mọi rubric phải phủ

Mỗi skill đặc tả 5 trục này theo hợp đồng RIÊNG của nó. Ba trục đầu (A1–A3) là GATE.

**A1. ĐÚNG + ĐỦ OUTPUT (gate)** — ra đúng thứ skill hứa, đủ mọi mục bắt buộc.
- Skill sinh artifact (pipeline): đủ các phần đã liệt kê + đúng path theo `folders.md`.
- Skill đọc-hiểu (explain/trace/teen): trả đúng loại câu trả lời, đủ ý cốt lõi cho phạm vi hỏi.
- Skill hạ tầng (progress/checkpoint/resume): đúng cấu trúc file/phiếu/khối.
- Bỏ một phần bắt buộc ≠ rút gọn độ sâu → tiêu chí này 0.

**A2. BÁM NGUỒN — KHÔNG BỊA (gate)** — mọi claim/số/tên file/kết quả truy được về input thật (code, artifact GĐ trước ĐÃ qua cổng, hoặc input user cung cấp KÈM ⚠️). Bịa cái không có nguồn = 0. **Đây là gate nặng nhất của cả suite** — lỗi lặp nhiều nhất là "báo số/PASS/artifact từ thứ không tồn tại". Chỗ chưa chắc phải gắn nhãn, không ngụy tạo.

**A3. ĐỌC-ĐƯỢC (gate)** — đúng đối tượng đọc là nắm được.
- Skill artifact pipeline: đọc-được-3-tầng (mở bằng Góc nhìn lãnh đạo → chi tiết cho dev, ~1 trang, scan 2–3 phút).
- Skill đọc-hiểu: đúng mức user (L0–L8) + lời văn phẳng, câu ngắn.
- Dày đặc / jargon không giải thích / sai mức = 0.

**A4. ĐỦ-LÀ-ĐỦ + KHÔNG LẤN VAI** — độ sâu tỉ lệ rủi ro (không thủ tục thừa, không bỏ bước); và ở ĐÚNG VAI, không làm việc skill khác (không lấn GĐ trước/sau, không tự code khi chỉ được đóng khung, không tự cấp phiếu khi chỉ ghi tiến độ…).

**A5. KỶ LUẬT: CỔNG/PHÂN VAI/TRACEABILITY + BÀN GIAO** — cổng đúng câu (nếu skill có cổng), AI tự duyệt rồi mới mời user, KHÔNG tự ký/tự GO thay user; nối traceability GĐ trước↔sau; kết bằng khối bàn giao trỏ ĐÚNG skill kế, chỉ liệt kê không chọn hộ. Skill không có cổng/handoff nặng (vd teen) thì trục này thu về "kết đúng: gợi ý bước tiếp hợp lý, không lấn".

**Luật cứng riêng của skill:** mỗi SKILL.md có mục "Luật cứng / Quy tắc bắt buộc" → gấp mỗi luật cứng vào tiêu chí liên quan làm một anchor-0 (vi phạm luật cứng = tiêu chí đó 0). Vd `tune` "một biến duy nhất", `frame` "hỏi-xác-nhận trước khi viết", `charter` "chạy một lần".

## Khung report chuẩn

```
CHẤM: <skill> · <fixture: định danh bản / đầu vào>
1 <Tên tiêu chí>   [n/2] — <lý do 1 câu>
2 <...>            [n/2] — <...>
...
TỔNG: <n>/<max>   ·   GATE: đạt / RỚT ở <tiêu chí ...>
SỬA TRƯỚC TIÊN: <một câu — đòn bẩy lớn nhất để bản này tốt hơn>
```

Không thêm khen/chê ngoài khung. `grade` chỉ chấm + chỉ đòn bẩy lớn nhất; không tự viết bản vá (đó là `tune`).

## Ánh xạ trục → tiêu chí (gợi ý — skill tự đặt tên tiêu chí)

- **Skill pipeline GĐ** (idea·shape·stack·skeleton·backlog·modules·delivery·uat·ship·operate): 7 tiêu chí quen — 1 Đúng+đủ artifact (A1,gate) · 2 Đọc-được-3-tầng (A3,gate) · 3 Bám nguồn (A2,gate) · 4 Đủ-là-đủ (A4) · 5 Không lấn vai / Traceability (A4/A5) · 6 Cổng+phân vai (A5) · 7 Bàn giao (A5).
- **Skill đọc-hiểu** (explain·trace·triage·review·teen): tiêu chí bám hợp đồng riêng (vd explain: Mức·Chế độ·Đủ ý·Lời văn·Bám code·Ranh giới·Kết), gate ở Mức+Lời văn+Bám code (A3+A3+A2).
- **Skill hạ tầng/điều phối** (charter·progress·checkpoint·resume·fanout·frame·partner): A1 = đúng cấu trúc/việc; A2 = không bịa trạng thái; A3 = đọc-được; A4 = đúng vai (progress không tự cấp phiếu; checkpoint không sửa artifact; frame không tự quyết scope); A5 = nối đúng skill kế.
- **Skill meta** (tune·skill-define·spar): A1 = đủ mục kết luận/bảng so; A2 = không bịa bằng chứng thí nghiệm; A4 = đúng vai meta (không tự merge khi chưa confirm); A5 = trỏ đúng (skill-creator…).

## Ranh giới của một rubric

Rubric CHẤM output của skill; nó không mô tả lại cách chạy skill, không sửa SKILL.md. Một rubric tốt là thứ hai người chấm mù đọc xong cho cùng một bản gần cùng điểm. Nếu hai tiêu chí luôn cùng lên-xuống → gộp; nếu một tiêu chí không bao giờ phân biệt được bản tốt/xấu → bỏ.
