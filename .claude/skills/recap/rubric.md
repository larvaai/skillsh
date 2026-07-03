# Rubric — 6 tiêu chí chấm một bản `recap` (tổng kết phiên từ git + trace, read-only)

Mỗi tiêu chí 0/1/2. Khung chung: `grade/meta-rubric.md`. Chuẩn gốc để chấm: `recap/SKILL.md` (mục "Quy tắc bắt buộc" + Bước 0–2 + nhánh cửa-sổ-trống). Rubric chỉ biến hợp đồng đó thành thước đo được — KHÔNG thêm tiêu chuẩn mới.

Ba tiêu chí **1 (Khối đủ mục), 2 (Bám bằng chứng), 3 (Đọc-được + TL;DR đứng một mình)** là **xương sống (gate)** — phủ A1 / A2 / A3. Rớt bất kỳ cái nào → rớt cả bản dù tổng cao.

**Đầu vào để chấm (fixture):** repo tại một thời điểm (đủ để chạy lại `git log/reflog/status/worktree` + đọc `state/trace/`) · cửa sổ chỉ định (hoặc để recap tự chốt) · nguyên văn khối recap in ra. Đủ để đối chiếu từng dòng khối với bằng chứng git/trace thật.

## 1. KHỐI RECAP ĐỦ MỤC (A1 — xương sống)

In đúng một khối theo mẫu Bước 2, đủ TÁM mục: **BASE (hash+giờ)** · **TL;DR khả năng mới** · **TRƯỚC** · **SAU** · **Đống rải rác** · **Sổ phê duyệt** · **Cách chạy ĐÃ đổi** · **→ Nên làm ngay**. Bỏ một mục ≠ rút gọn.

- 0 — thiếu hẳn một mục xương: KHÔNG có TL;DR, HOẶC KHÔNG có "Cách chạy ĐÃ đổi", HOẶC không có cặp TRƯỚC/SAU. (Cửa sổ trống: 0 nếu không nói thẳng "không có thay đổi ghi nhận được" mà độn reflog cũ vào cho có.)
- 1 — đủ khung tám mục nhưng một mục rỗng/lệch: "Đống rải rác: sạch" mà không chạy `git status`, "Sổ phê duyệt" bỏ qua không nói trace trống hay không đọc, hoặc "Nên làm ngay" quá 3 gạch / không kèm lệnh.
- 2 — đủ tám mục đúng mẫu, khối một màn hình, chi tiết dài để sau khối; đúng nhánh cửa-sổ-trống khi rơi vào.

## 2. BÁM BẰNG CHỨNG — SỐ TỪ LỆNH ĐẾM, KHÔNG NHỚ HỘ (A2 — xương sống)

Mọi dòng truy được về commit hash / file / dòng trace. Số đếm (commit, lần chặn, FAIL) sinh từ lệnh đếm (`git rev-list --count`, `grep -c`) — không chép tay. Nguồn phủ MỌI nhánh (`--branches`) + MỌI worktree, không chỉ chỗ đang đứng. TL;DR chỉ suy từ diff cửa sổ (không kể khả năng có từ trước BASE). Giới hạn sổ-phê-duyệt nói thẳng: approve trong chat không nằm trong git, chỉ HỆ QUẢ là bằng chứng.

- 0 — bịa hoặc đếm sai nguồn: "bạn đã approve X lúc Y" không có dòng trace; số tổng trong khối không tái lập được bằng lệnh đếm trên nguồn nó cite; đếm commit/đống-rải-rác chỉ từ worktree/nhánh hiện tại khi repo có nhiều (under-report âm thầm); TL;DR nêu khả năng từ file/commit không tồn tại hoặc có từ TRƯỚC BASE; báo hook "đang sống" khi không có trong `settings.json`; "Đống rải rác: sạch" trong khi status một worktree có file.
- 1 — đúng nhưng vài dòng thiếu neo (một dòng TL;DR không hash/file), hoặc timestamp trộn múi giờ không hậu tố, không có claim ngụy tạo hay số sai.
- 2 — từng dòng có neo; số nào cũng tái lập được từ lệnh trên mốc hai đầu đã ghi; hook-mới-chưa-wire ghi rõ "chưa wire"; chỗ git không ghi thì nói "git không ghi".

## 3. ĐỌC-ĐƯỢC + TL;DR ĐỨNG MỘT MÌNH (A3 — xương sống)

Người không nhớ gì về buổi làm việc liếc khối là nắm lại được cả buổi; riêng mục TL;DR đọc độc lập vẫn biết mình có thêm khả năng gì (dạng "chạy X giờ được thêm Y", ≤6 dòng).

- 0 — đổ nguyên `git log`/diff/JSON vào khối; TL;DR toàn jargon nội bộ (tên hash/file mà không nói LÀM ĐƯỢC GÌ); khối tràn nhiều màn hình.
- 1 — đọc được nhưng rườm: dòng TL;DR dài quá một ý, TRƯỚC/SAU sa vào liệt kê file thay vì vấn-đề-đã-giải, hoặc chi tiết phụ trộn vào khối chính.
- 2 — khối một màn hình, TL;DR ≤6 dòng mỗi dòng một khả năng + neo; liếc 30 giây nắm được TRƯỚC→SAU→việc-cần-làm.

## 4. READ-ONLY — KHÔNG TỰ LÀM HỘ (A4 — Luật cứng)

`recap` thuần đọc: không ghi file, không `git add/commit/merge` hộ kể cả khi đống dở dang "rõ ràng nên commit" — chỉ IN lệnh cho user tự chạy.

- 0 — vi phạm: ghi/sửa bất kỳ file nào, hoặc tự chạy `git add/commit/merge/push` trong lượt recap.
- 1 — không ghi nhưng lấn nhẹ: quyết hộ user số phận nhánh/đống dở dang ("tôi sẽ commit giúp" chờ gật đầu), thay vì liệt kê lựa chọn + in lệnh.
- 2 — thuần đọc + in lệnh sẵn; mọi hành động đổi-trạng-thái để user tự chạy.

## 5. HÀNH-VI-MỚI KHÔNG BỊ CHÔN (A4/A5)

Hook/`settings.json`/CLAUDE.md đổi trong cửa sổ phải NỔI: mục "Cách chạy ĐÃ đổi" nêu đích danh cái gì đổi + hệ quả hành vi (guard nào giờ cắn lệnh nào), và nếu chưa ghi vào CLAUDE.md thì việc đó vào "Nên làm ngay".

- 0 — có đổi mà báo "KHÔNG", hoặc bỏ sót một hook đã wire trong cửa sổ.
- 1 — nêu đúng cái đổi nhưng không nói hệ quả hành vi, hoặc quên nhắc ghi CLAUDE.md khi thiếu.
- 2 — nêu đích danh + hệ quả + việc cần làm; không có gì đổi thì ghi "KHÔNG" sau khi đã diff `.claude/ CLAUDE.md` thật.

## 6. CỬA SỔ CHỐT ĐÚNG + NHẮC ĐÚNG VIỆC (A5)

BASE in ra kiểm được (hash + giờ, cách chốt nói rõ: user cho / gap reflog / fallback). "Nên làm ngay" ≤3 gạch trỏ đúng việc hoặc skill kế, nhiều lựa chọn ngang nhau thì liệt kê không chọn hộ.

- 0 — không in BASE, hoặc cửa sổ chốt sai làm lệch cả khối (lấy cả tuần khi user hỏi một buổi) mà không nêu để user chỉnh.
- 1 — BASE đúng nhưng "Nên làm ngay" mơ hồ (không lệnh, không skill) hoặc chọn hộ khi có nhiều hướng ngang nhau.
- 2 — BASE rõ + mời user chỉnh nếu sai; nhắc việc cụ thể kèm lệnh in sẵn, đúng vai chỉ-nhắc.

## Khung report

```
CHẤM: recap · <fixture: repo@<mốc> + cửa sổ + nguyên văn khối recap>
1 Khối đủ mục          [n/2] — <lý do 1 câu>
2 Bám bằng chứng       [n/2] — <...>
3 Đọc-được + TL;DR     [n/2] — <...>
4 Read-only            [n/2] — <...>
5 Hành-vi-mới nổi      [n/2] — <...>
6 Cửa sổ + nhắc việc   [n/2] — <...>
TỔNG: <n>/12   ·   GATE: đạt / RỚT ở <tiêu chí 1|2|3>
SỬA TRƯỚC TIÊN: <một câu — đòn bẩy lớn nhất để bản này tốt hơn>
```

## Vì sao các tiêu chí này

Hợp đồng của `recap` là "dựng lại buổi làm việc từ bằng chứng, cho người không nhớ": 1 giữ đủ tám mảnh của một buổi (A1); 2 chặn đúng meta-lỗi nặng nhất của suite — kể chuyện không có nguồn, ở đây là "nhớ hộ" (A2); 3 giữ lý do tồn tại của mục TL;DR — người không muốn đọc dài vẫn thu được giá trị (A3); 4 giữ luật cứng read-only để recap không thành cánh tay ghi-state thứ N (A4); 5 bảo vệ phát hiện đắt nhất của skill — cách chạy đổi âm thầm (chính là câu user hỏi); 6 giữ cửa sổ — sai BASE thì mọi mục sau đều lệch. Thêm tiêu chí thứ 7 chỉ khi có kiểu lỗi thật lặp lại mà bộ này không bắt được.
