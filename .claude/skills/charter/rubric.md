# Rubric — 6 tiêu chí chấm một bản `charter` (dựng project mới)

Mỗi tiêu chí 0/1/2. Khung chung: `grade/meta-rubric.md`. Chuẩn gốc để chấm: `charter/SKILL.md` (7 bước dựng + mục "## Quy tắc bắt buộc") và `charter/assets/constitution/definition-of-done.md` (Định-nghĩa-Xong mà khung project phải chuẩn bị để giữ). Rubric chỉ biến hợp đồng đó thành thước đo được — KHÔNG thêm tiêu chuẩn mới.

`charter` là skill hạ tầng chạy MỘT LẦN: nó không sinh artifact pipeline, không brainstorm, không code — nó chỉ dựng đúng cái khung (6 folder + constitution + progress.json rỗng + board + README + memory + current.json) rồi buông và tiến cử skill kế. Vì thế thước ở đây đo *có dựng đúng+đủ khung không*, *có bám seed / không bịa không*, *khung có đọc-được không*, *có chạy đúng một lần và đúng vai không*, *có bàn giao đúng không*.

Tiêu chí **1 (Đúng+đủ khung), 2 (Bám seed — không bịa), 3 (Đọc-được)** là **xương sống (gate)**: rớt bất kỳ cái nào → rớt cả bản dù tổng cao.

**Đầu vào để chấm (fixture):** `<key>`/slug + một câu vấn đề user đưa (hoặc argument `/charter <key>`) · `mode` (greenfield/brownfield, hoặc dữ kiện để suy ra) · trạng thái `projects/<key>/` trước khi chạy (đã tồn tại hay chưa — để kiểm luật "chạy một lần") · output charter dựng ra (cây thư mục + nội dung `progress.json` / `board.md` / `README.md` / `state/current.json` / dòng memory + khối bàn giao).

## 1. ĐÚNG + ĐỦ KHUNG (xương sống)

Dựng đủ mọi output SKILL.md hứa, đúng path, đúng cấu trúc: 6 folder (`problem`, `idea`, `docs`, `codebase`, `constitution`, `progress/checkpoints`) + constitution 4 file + `progress/progress.json` (con trỏ `gd0_intake`, đúng schema, 1 task seed T-01) + `progress/board.md` + `README.md` (có mục **Kỳ vọng ban đầu**) + một memory `project` + dòng trỏ trong `MEMORY.md` + `state/current.json`. Bỏ một thành phần bắt buộc ≠ rút gọn.

- 0 — thiếu hẳn một mảnh xương: thiếu ≥1 trong 6 folder, HOẶC không có `progress.json`, HOẶC không tạo/không copy đủ constitution 4 file, HOẶC không có `README.md`, HOẶC không trỏ `state/current.json`. (Thiếu một thành phần bắt buộc = 0.)
- 1 — có đủ các mảnh lớn nhưng lệch một chi tiết bắt buộc: `progress.json` sai schema/thiếu con trỏ hoặc thiếu task seed T-01; HOẶC `README.md` có nhưng thiếu mục **Kỳ vọng ban đầu**; HOẶC thiếu memory / dòng trỏ MEMORY.md; HOẶC thiếu `board.md`.
- 2 — đủ trọn bộ, đúng path, đúng cấu trúc: 6 folder + 4 file constitution + `progress.json` (schema_version, project, mode, `con_tro.giai_doan=gd0_intake`, đúng 1 task seed T-01, `updated_at`) + `board.md` + `README.md` (một câu vấn đề + **Kỳ vọng ban đầu** + mode + ngày + link board) + memory + dòng MEMORY.md + `state/current.json` trỏ đúng key.

## 2. BÁM SEED — GIEO Y BẢN, KHÔNG BỊA (xương sống)

Constitution copy nguyên 4 file seed từ `assets/constitution/` — KHÔNG tự chế/viết lại luật. `progress.json` khởi tạo TỐI THIỂU — KHÔNG bịa task tương lai. Kỳ vọng/vấn đề trong README bám đúng lời user đưa, không tự thêu dệt. Slug/tên project bám argument hoặc mô tả user, không tự đổi.

- 0 — bịa hoặc lệch nguồn: tự viết lại nội dung constitution thay vì copy seed (chế luật riêng); HOẶC nhồi task tương lai vào `progress.json` (task GĐ1–14 mà `progress` mới được chia); HOẶC bịa Kỳ vọng ban đầu / một câu vấn đề mà user không hề nói; HOẶC tự đặt lại vấn đề khác ý user.
- 1 — chủ yếu bám seed nhưng một chỗ lệch nhẹ: sửa/định dạng lại constitution một file, HOẶC thêm 1–2 task suy đoán ngoài T-01, HOẶC diễn giải Kỳ vọng thêm chi tiết user chưa xác nhận mà không gắn nhãn thô/tạm.
- 2 — constitution y hệt 4 seed; `progress.json` đúng một task seed T-01, con trỏ gd0, không task tương lai nào; Kỳ vọng ban đầu + một câu vấn đề chép/derive trung thực từ input user (thô cũng ghi thô, không thêu); slug derive kebab-case đúng từ tên user đưa.

## 3. ĐỌC-ĐƯỢC — board/README người đọc nắm ngay (xương sống)

`board.md` và `README.md` là trang người-đọc: mở ra biết ngay project là gì, đang ở đâu (con trỏ GĐ0), làm gì tiếp. Câu ngắn, phẳng, không bắt user đọc `progress.json` thô để hiểu.

- 0 — trang người-đọc không nắm được: `board.md` chỉ là JSON dump / trống trơn không diễn giải; HOẶC `README.md` không nói được project giải bài gì, không có con trỏ/lối vào; HOẶC dày đặc jargon, người mở lần đầu không biết bấm gì tiếp.
- 1 — đọc-được nhưng lệch: board có con trỏ + bảng task nhưng thiếu một câu vấn đề hoặc lối vào tiếp; hoặc README đủ mục nhưng rườm/khó scan.
- 2 — `board.md` một trang: tên project + một dòng vấn đề + con trỏ hiện tại + bảng task (chỉ T-01) + nhắc bước tiếp; `README.md` một trang scan trong 1–2 phút: project là gì + Kỳ vọng ban đầu + mode + ngày + link board + câu nhắc "vào bằng `/resume`, brainstorm bằng `/idea`". `board.md` diễn giải, `progress.json` là nguồn — tách rõ.

## 4. CHẠY MỘT LẦN + PROGRESS TỐI THIỂU (Luật cứng)

Kiểm tồn tại TRƯỚC khi dựng: `projects/<key>/` đã có → DỪNG, không tạo đè/không xoá, tiến cử `/resume <key>`. `progress.json` giữ ở mức tối thiểu (một task seed + con trỏ gd0), không phình.

- 0 — vi phạm luật cứng: project đã tồn tại mà vẫn tạo đè / ghi đè / xoá dữ liệu cũ; HOẶC bỏ hẳn bước kiểm tồn tại; HOẶC `progress.json` khởi tạo phình (nhiều task, con trỏ không ở gd0).
- 1 — có kiểm tồn tại và không đè, nhưng xử lý mờ: gặp project đã có mà không nói rõ dừng / không tiến cử `/resume`; hoặc progress hơi quá mức tối thiểu (thừa field không cần).
- 2 — chạy đúng một lần: kiểm tồn tại trước; đã có → dừng sạch + tiến cử `/resume <key>`; chưa có → dựng; `progress.json` đúng mức tối thiểu (T-01 + con trỏ gd0_intake), không bịa thêm.

## 5. KHÔNG LẤN VAI — CHỈ DỰNG KHUNG, KHÔNG ĐỤNG PROJECT KHÁC (Luật cứng)

`charter` chỉ dựng khung của đúng key này: KHÔNG brainstorm, KHÔNG viết PRD, KHÔNG code, KHÔNG chia task tương lai (việc `progress`), KHÔNG cập nhật `progress.json` tiếp sau khi khởi tạo (buông cho `progress`), KHÔNG migrate/sửa project khác.

- 0 — lấn vai: brainstorm ý / viết PRD / sinh domain / code trong `idea/` hay `docs/` thay vì để folder trống; HOẶC chia task GĐ sau (lấn `progress`); HOẶC đụng/migrate/sửa một project khác ngoài `<key>`.
- 1 — chủ yếu đúng vai nhưng lỡ một bước: điền sẵn một chút nội dung định hướng vào folder lẽ ra để trống, hoặc gợi ý cách brainstorm hơi sâu (nên để `/idea`).
- 2 — thuần dựng khung: folder `problem/idea/docs/codebase` để trống cho skill sau, chỉ tạo cấu trúc + seed + con trỏ; không lấn `idea`/`progress`; chỉ chạm đúng `projects/<key>/`, `state/current.json`, `MEMORY.md`.

## 6. BÀN GIAO ĐÚNG SKILL KẾ

Kết bằng khối bàn giao: nêu `/idea` (brainstorm ý đầu) và `/resume <key>` (xem toàn cảnh) là hai đường kế; chỉ tiến cử, KHÔNG tự chạy tiếp `idea`.

- 0 — không có khối bàn giao, HOẶC tự chạy tiếp `idea`/tự brainstorm luôn thay vì dừng chờ user, HOẶC trỏ sai skill.
- 1 — có bàn giao nhưng thiếu một lối (chỉ `/idea` hoặc chỉ `/resume`), hoặc mờ ranh giới "chỉ tiến cử không tự chạy".
- 2 — khối bàn giao gọn: xác nhận đã dựng (6 folder + constitution + progress con trỏ gd0_intake) + một câu bài toán + tiến cử `/idea` (đường chính) và `/resume <key>` (lối xem toàn cảnh); dừng lại, để user quyết, không tự chạy tiếp.

## Gate

Tiêu chí **1 (Đúng+đủ khung — A1)**, **2 (Bám seed, không bịa — A2)**, **3 (Đọc-được — A3)** là xương sống. Bất kỳ cái nào = 0 → bản **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản dựng đủ 6 folder + bàn giao đẹp nhưng tự chế lại constitution thay vì copy seed (tiêu chí 2 = 0) vẫn rớt — vì mọi project sau sẽ chạy trên luật sai chuẩn. Khi so nhiều bản: loại hết bản rớt gate TRƯỚC, rồi mới xếp phần còn lại theo tổng.

## Khung report (xếp nhiều bản cạnh nhau)

```
CHẤM: charter · <key> · <mode>
1 Đúng+đủ khung      [n/2] — <lý do 1 câu>
2 Bám seed–không bịa [n/2] — <...>
3 Đọc-được           [n/2] — <...>
4 Chạy-1-lần+tối thiểu[n/2] — <...>
5 Không lấn vai      [n/2] — <...>
6 Bàn giao           [n/2] — <...>
TỔNG: <n>/12   ·   GATE: đạt / RỚT ở <tiêu chí ...>
SỬA TRƯỚC TIÊN: <một câu — đòn bẩy lớn nhất để bản này tốt hơn>
```

## Vì sao các tiêu chí này

Ba xương sống đo *có dựng ra đúng+đủ khung không* (1), *khung có trung thực với seed và ý user không* (2), *người mở project có nắm được ngay không* (3) — đúng ba trục gate A1/A2/A3 của meta-rubric, và cũng là ba chỗ hỏng làm cả suite chạy trên nền sai (thiếu folder → skill sau không có chỗ đặt artifact; chế luật riêng → constitution lệch chuẩn; board không đọc-được → không ai biết đang ở đâu). Ba cái sau đo *có đúng kỷ luật của một skill chạy-một-lần không*: chạy một lần + progress tối thiểu (4, gấp luật cứng "chạy một lần" và "progress.json tối thiểu"), không lấn vai + không đụng project khác (5, gấp luật cứng "không đụng project khác" và ranh giới với `idea`/`progress`), bàn giao đúng và không tự chạy tiếp (6). Gộp lại = trọn hợp đồng 7 bước của `charter`, không hơn. Đây là skill hạ tầng đơn giản nên 6 tiêu chí là đủ (meta-rubric cho phép 5–8); thêm tiêu chí thứ 7 chỉ khi có một kiểu lỗi thật lặp lại mà 6 cái này không bắt được.
