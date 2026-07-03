# Rubric — 7 tiêu chí chấm một bản `review` (rà soát gap)

Mỗi tiêu chí 0/1/2. Khung chung: `grade/meta-rubric.md`. Chuẩn gốc để chấm: `review/SKILL.md` (mục "## Quy tắc" + "## Ba chế độ review" + khung "## Bước 3 — Báo cáo gap" + thang mức Critical/Medium/Low). Rubric chỉ biến hợp đồng đó thành thước đo được — KHÔNG thêm tiêu chuẩn mới.

**Đầu vào để chấm (fixture):** project (codebase bản review đang soi, để kiểm bịa lỗ hổng) · scope (đối tượng đã chốt ở Bước 0: tính năng/module/endpoint/luồng) · mode (edge / error / permission / tổng thể) · output (nguyên văn báo cáo gap).

Tiêu chí **1 (Đúng+đủ output), 3 (Bám code), 4 (Đọc-được)** là **xương sống (gate)** — phủ đúng A1 / A2 / A3.

## 1. ĐÚNG + ĐỦ OUTPUT — đủ ba loại gap + gán mức (xương sống)

Ra đúng thứ review hứa: theo `mode` mà soi đủ loại gap tương ứng (edge → input/state/sequence chưa xử lý; error → error path bắt/xử lý/propagate; permission → access control bypass/thiếu), và MỖI gap được gán đúng một mức Critical/Medium/Low theo thang ở Bước 3. Chế độ "tổng thể" phải phủ cả ba loại theo thứ tự edge → error → permission.

- 0 — sai/thiếu loại gap so với `mode`: chạy "tổng thể" mà chỉ soi một loại (bỏ error hoặc permission); HOẶC có gap nhưng KHÔNG gán mức (thiếu nhãn Critical/Medium/Low), hoặc gán mức không theo thang (gọi mất-data là Low). Bỏ một loại bắt buộc ≠ soi nông hơn → 0.
- 1 — đủ loại theo `mode` và có gán mức, nhưng lệch: một loại soi qua loa so với rủi ro, hoặc 1–2 gap gán mức sai lệch một bậc.
- 2 — phủ đủ loại theo `mode` (tổng thể = cả ba đúng thứ tự); mỗi gap có mức đúng thang (Critical = production/mất data/security breach · Medium = hành vi sai case cụ thể không crash · Low = thiếu nhỏ/UX); độ phủ khớp phạm vi.

## 2. CHẾ ĐỘ — đúng lăng kính của mode

Bản review soi đúng câu hỏi của chế độ, không lẫn sang chế độ khác.

- 0 — sai chế độ: được gọi `permission` mà đi liệt edge case input; hoặc `error` mà chỉ soi thiếu null-check thay vì đường bắt/propagate/silent của lỗi.
- 1 — đúng chế độ nhưng lẫn: chế độ `edge` mà trộn vài mục permission chưa tách; hoặc soi đúng loại nhưng bỏ trục con của chế độ (error không xét "sau khi bắt thì làm gì / người dùng cuối nhận được gì").
- 2 — trọn lăng kính: edge quét input rỗng/null/âm/overflow/quá-dài/sai-type/concurrent + sequence ngoài thứ tự; error truy bắt-đúng-loại → xử-lý → propagate → cái người dùng cuối nhận; permission truy đúng-tầng (UI/API/DB) + bypass qua param/endpoint-khác/race.

## 3. BÁM CODE — mỗi gap là lỗ thật, không bịa (xương sống)

Mỗi gap phải có evidence bám code thật: `file · dòng/symbol · điều thiếu · hậu quả`. Không phát minh lỗ hổng ở code không tồn tại; chỗ nghi ngờ phải nằm ở "CÓ THỂ LÀ GAP", không trộn vào gap chắc chắn. Đây là gate nặng nhất — lỗi tệ nhất là báo một gap ở symbol không có thật hoặc ở nhánh code đã xử lý rồi mà không đọc kỹ.

- 0 — có gap bịa: trỏ file/symbol không tồn tại, HOẶC báo "thiếu xử lý" ở chỗ code đã có nhánh xử lý (không đọc kỹ), HOẶC một suy đoán chưa xác nhận bị xếp thẳng vào GAP chắc chắn thay vì "CÓ THỂ LÀ GAP". Bất kỳ gap bịa nào → 0.
- 1 — chủ yếu bám code, nhưng 1 gap thiếu evidence đủ (không chỉ được dòng/symbol), hoặc một nghi ngờ chưa gắn nhãn "chưa chắc".
- 2 — mọi gap trỏ đúng file · dòng/symbol có thật, điều-thiếu kiểm được trong code, hậu quả hợp lý; mọi phần chưa chắc nằm đúng ô "CÓ THỂ LÀ GAP" kèm câu cần xác nhận.

## 4. ĐỌC-ĐƯỢC — báo cáo theo đúng khung, nắm được ngay (xương sống)

Báo cáo theo khung Bước 3 (PHẠM VI · CHẾ ĐỘ · GAP TÌM ĐƯỢC · CÓ THỂ LÀ GAP · KHÔNG TÌM THẤY GAP), mỗi gap một dòng `[Mức] file·symbol — điều thiếu → hậu quả`; người dùng scan là biết nên lo cái gì trước.

- 0 — không theo khung (đổ một cục văn xuôi), HOẶC gap không có dạng điều-thiếu→hậu-quả nên không rõ vì sao đáng lo, HOẶC dày đặc/jargon không giải thích khiến người đọc không nắm được.
- 1 — có khung nhưng lệch: thiếu một mục (không ghi "KHÔNG TÌM THẤY GAP" dù đã kiểm), hoặc vài dòng thiếu mũi tên hậu quả, hoặc thứ tự mức lộn xộn khó scan.
- 2 — đủ khung; gap xếp theo mức (Critical trước); mỗi dòng gọn có đủ điều-thiếu → hậu-quả; đọc 2–3 phút là ra ưu tiên.

## 5. KHÔNG ĐỀ XUẤT FIX — CHỈ BÁO CÁO, KHÔNG TỰ CODE

Review chỉ báo cái tìm thấy. KHÔNG viết đoạn sửa, KHÔNG đề xuất cách fix, KHÔNG tự code. Đóng khung fix là việc của `frame`.

- 0 — vi phạm luật cứng: viết code sửa/patch, HOẶC kèm "cách fix: làm A rồi B" cho gap, HOẶC tự sửa file trong lúc review.
- 1 — chủ yếu chỉ báo cáo, nhưng lỡ nhét 1 câu gợi-ý-hướng-sửa chưa tách rõ khỏi phần mô tả gap.
- 2 — thuần báo cáo: chỉ nêu điều-thiếu + hậu quả; mọi việc sửa được đẩy sang gợi ý gọi `frame`, không có dòng code hay bước fix nào.

## 6. TÁI DÙNG NGUỒN + KHÔNG BỎ GAP NHỎ

Đọc `.ai-understanding/` liên quan trước khi đọc file gốc (theo Bước 1); tách gap thật khỏi "có thể là gap" bằng nhãn rõ; và KHÔNG bỏ qua gap chỉ vì nhỏ — ghi lại để người dùng quyết.

- 0 — làm ngược luật cứng: bỏ qua/nuốt một gap nhỏ đã thấy (không ghi), HOẶC gộp gap-chắc-chắn và nghi-ngờ vào chung một khối không phân nhãn.
- 1 — có tách nhãn và không bỏ gap nhỏ, nhưng bỏ qua `.ai-understanding/` sẵn có (quét lại từ đầu) mà không nhắc, hoặc phân nhãn chưa nhất quán.
- 2 — tái dùng artifact `.ai-understanding/` liên quan trước (hoặc gợi ý `atlas` nếu chưa có); gap thật vs "có thể là gap" tách rõ; gap nhỏ vẫn được ghi ở đúng mức Low, không nuốt.

## 7. KẾT — gợi ý bước tiếp đúng theo kết quả

Kết theo Bước 4: có gap Critical hoặc muốn sửa → gợi ý `frame` để đóng khung fix; sạch (không tìm thấy gap) → hỏi review phần khác hoặc đóng khung tính năng tiếp; có nghi ngờ → hỏi đào sâu. Chỉ gợi ý, không tự làm bước sau.

- 0 — không có gợi ý; HOẶC gợi ý sai vai: tự nhảy vào sửa/đóng khung thay vì mời gọi `frame`, hoặc chốt "đã fix" thay user.
- 1 — có gợi ý nhưng chung chung / không khớp kết quả (có Critical mà không nhắc `frame`; sạch mà không mời review phần khác).
- 2 — kết đúng theo kết quả: có Critical → mời `frame` đóng khung fix theo ưu tiên; sạch → mời review phần khác hoặc `frame` tính năng tiếp; còn nghi ngờ → hỏi đào sâu; chỉ liệt kê, để user quyết.

## Gate (tiêu chí xương sống)

Tiêu chí **1, 3, 4** là xương sống (A1 đúng+đủ output · A2 bám code không bịa · A3 đọc-được). Bất kỳ cái nào = 0 → bản review **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 12/14 nhưng bịa một gap ở symbol không tồn tại (tiêu chí 3 = 0) vẫn rớt — vì người đọc sẽ đi sửa một lỗ hổng không có thật và bỏ công vô ích. Gate quan trọng hơn tổng: khi so nhiều bản, loại hết bản rớt gate trước, rồi mới xếp phần còn lại theo tổng.

## Khung report (xếp nhiều bản cạnh nhau)

```
CHẤM: review · <project> · <scope> · <mode>
1 Đúng+đủ output   [n] — <lý do 1 câu>
2 Chế độ           [n] — <...>
3 Bám code         [n] — <...>
4 Đọc-được         [n] — <...>
5 Không đề xuất fix [n] — <...>
6 Tái dùng+gap nhỏ [n] — <...>
7 Kết              [n] — <...>
TỔNG: <n>/14   ·   GATE: đạt / RỚT ở <tiêu chí ...>
SỬA TRƯỚC TIÊN: <một câu — đòn bẩy lớn nhất để bản này tốt hơn>
```

## Vì sao 7 tiêu chí này

Bốn cái đầu đo *bản review có ra đúng thứ nó hứa không* — đủ ba loại gap có gán mức (A1), đúng lăng kính chế độ, mỗi gap là lỗ thật bám code (A2), báo cáo đọc được theo khung (A3). Ba cái sau đo *có đúng vai review không* — không lấn sang fix/code (A4, luật cứng "Không đề xuất fix"), tái dùng nguồn và không nuốt gap nhỏ (A4, hai luật cứng còn lại), kết bằng bàn giao đúng skill (A5). Gộp lại = trọn hợp đồng của `review`, không hơn. Bốn luật cứng trong "## Quy tắc" của SKILL.md đều đã gấp thành anchor-0: "mỗi gap có evidence" ở TC3, "tách gap thật khỏi có-thể-là-gap" + "không bỏ gap nhỏ" ở TC6, "không đề xuất fix" ở TC5, "tái dùng `.ai-understanding/`" ở TC6. Thêm tiêu chí thứ 8 chỉ khi có một kiểu lỗi thật lặp lại mà 7 cái này không bắt được.
