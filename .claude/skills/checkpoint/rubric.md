# Rubric — 6 tiêu chí chấm một phiếu `checkpoint`

Mỗi tiêu chí 0/1/2. Khung chung: `grade/meta-rubric.md`. Chuẩn gốc để chấm: `checkpoint/SKILL.md` (mục "## Quy tắc bắt buộc" + Bước 0–3) và `constitution/definition-of-done.md` (checklist mục bắt buộc theo giai đoạn mà checkpoint đối chiếu). Rubric chỉ biến hợp đồng đó thành thước đo được — KHÔNG thêm tiêu chuẩn mới.

**Đầu vào để chấm (fixture):** task (id + `giai_doan` + `owner` + `artifact` path, lấy từ `progress.json`) · artifact (nội dung file bản checkpoint đang xét) · definition-of-done.md (checklist giai đoạn tương ứng) · output (nguyên văn phiếu `progress/checkpoints/<id>.md` + khối in ra).

Tiêu chí **1 (Phiếu đúng+đủ), 2 (Bám Định-nghĩa-Xong, không bịa), 3 (Phiếu đọc-được)** là **xương sống (gate)**.

## 1. PHIẾU ĐÚNG + ĐỦ OUTPUT (xương sống)

Ra đúng cấu trúc phiếu checkpoint hứa: file ở đúng path `progress/checkpoints/<task-id>.md`, có verdict `PASS | FAIL` rõ ràng, và lý do cụ thể (không PASS/FAIL trống).

- 0 — sai/thiếu output xương: phiếu KHÔNG nằm ở `progress/checkpoints/<task-id>.md` (sai path hoặc không ghi file); HOẶC thiếu verdict PASS/FAIL; HOẶC verdict trống, không nêu lý do (vi phạm luật "Phán quyết có lý do"). Bỏ một phần bắt buộc của khung phiếu (Task/Giai đoạn/Artifact/Checklist/Verdict/Lý do) → tiêu chí này 0.
- 1 — đủ mặt nhưng lệch: có verdict + lý do nhưng thiếu một trường của khung (vd thiếu dòng "Kiểm lúc" ISO, hoặc FAIL mà thiếu mục "cần bổ sung"), hoặc khối in ra thiếu dòng gợi ý bước kế.
- 2 — trọn: phiếu đúng path, có đủ header (Task, Giai đoạn, Artifact, Kiểm lúc) + Checklist đánh dấu từng mục + Verdict PASS/FAIL + Lý do 1–2 câu; FAIL kèm danh sách "cần bổ sung" cụ thể; có in khối `═══ CHECKPOINT ═══` đạt `<n>/<m>` mục.

## 2. BÁM ĐỊNH-NGHĨA-XONG — không bịa "đủ mục" (xương sống)

Mọi ✓/✗ trên checklist đối chiếu ĐÚNG checklist giai đoạn của task (từ `definition-of-done.md`, khớp `giai_doan`), và mọi phán quyết truy được về artifact THẬT đã đọc — không đánh dấu đạt cho mục không kiểm, không bịa "đủ mục" khi chưa mở artifact. Đây là gate nặng nhất của cả suite: lỗi lặp nhiều nhất là "báo PASS/đủ-mục từ thứ không tồn tại".

- 0 — bịa hoặc sai nguồn: cấp PASS mà artifact KHÔNG tồn tại ở path (Bước 1 phải FAIL ngay "artifact chưa nằm ở <path>"); HOẶC đánh ✓ cho mục không có trong artifact; HOẶC dùng checklist SAI giai đoạn (kiểm Domain bằng checklist Contract); HOẶC kết luận "đủ mục" chung chung không nêu mục nào.
- 1 — chủ yếu bám nguồn nhưng một mục đánh dấu theo suy đoán không mở tới nơi, hoặc thiếu đối chiếu 1 mục bắt buộc của giai đoạn.
- 2 — mọi ✓ có bằng chứng trong artifact, mọi ✗ nêu chính xác thiếu gì; checklist đúng giai đoạn task; cổng đậm (GĐ8 live slice / GĐ13 release) ghi `PASS (chờ ký)` chờ chữ người thay vì tự PASS.

## 3. PHIẾU ĐỌC-ĐƯỢC (xương sống)

Owner đọc phiếu là biết ngay đạt/không và nếu FAIL thì phải sửa gì — verdict nổi bật, lý do một câu phẳng, mục thiếu liệt kê rõ.

- 0 — khó dùng: verdict lẫn trong văn, phải đọc kỹ mới biết PASS hay FAIL; HOẶC lý do FAIL mơ hồ ("chưa đủ", "cần hoàn thiện") không chỉ mục cụ thể để owner sửa; HOẶC dày đặc jargon/khối dài không scan được.
- 1 — đọc được nhưng còn rườm: lý do dài dòng, hoặc mục thiếu nêu chung chung phải đoán.
- 2 — verdict PASS/FAIL bật ngay đầu khối; lý do 1–2 câu phẳng; nếu FAIL, mỗi mục thiếu là một dòng hành động được cho owner; khối in ra scan trong vài giây.

## 4. ĐÚNG VAI — chỉ kiểm + phán, KHÔNG sửa, KHÔNG đụng đồ thị task (A4)

Checkpoint chỉ cấp phiếu. Không tự viết thêm vào artifact để "vá cho đạt"; không lật task/dời con trỏ trong `progress.json` (đó là `progress`); việc soi CODE sâu (gap/edge case/permission) thì tiến cử `/review`, không làm thay.

- 0 — lấn vai: tự sửa/bổ sung nội dung artifact cho đạt (vi phạm "Chỉ kiểm, không sửa"); HOẶC ghi/đụng `progress.json`, tự lật task `done` (vi phạm "Không đụng progress.json"); HOẶC tự đi soi code sâu như `review`/`grade` thay vì tiến cử.
- 1 — đúng vai phần lớn nhưng lấn nhẹ: lỡ đề xuất chỉnh câu chữ trong artifact, hoặc nói "đã mở nhánh sau" như thể tự làm phần của progress.
- 2 — thuần kiểm + phán: thấy thiếu thì ghi vào phiếu trả owner sửa, không tự sửa; không chạm progress.json; việc cần soi sâu ghi "→ tiến cử `/review`".

## 5. KẾT — trỏ `/progress` để advance sau PASS (A5)

Khối kết nối đúng bước tiếp: PASS → chạy `/progress` để lật `done` + mở nhánh kế; FAIL → owner (`<skill>`) sửa mục thiếu rồi `/checkpoint <task-id>` lại. Chỉ liệt kê, không tự làm thay.

- 0 — không có gợi ý bước kế, HOẶC trỏ sai (tự nói đã lật done, hoặc bỏ hẳn đường `/progress` sau PASS nên đồ thị không biết được phép chạy tiếp).
- 1 — có gợi ý nhưng lệch: chỉ nói PASS/FAIL mà không nêu rõ ai (`owner`/skill nào) làm gì tiếp, hoặc thiếu một trong hai nhánh.
- 2 — kết đủ hai nhánh: PASS → `/progress` để advance + mở nhánh; FAIL → owner skill sửa `<thiếu gì>` rồi `/checkpoint` lại; cổng đậm nhắc chờ user ký.

## Gate (tiêu chí xương sống)

Tiêu chí **1, 2, 3** là xương sống. Bất kỳ cái nào = 0 → phiếu **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một phiếu 8/10 nhưng cấp PASS cho artifact không tồn tại hoặc đánh ✓ cho mục không có thật (tiêu chí 2 = 0) vẫn rớt — vì `progress` sẽ mở nhầm nhánh sau dựa trên phiếu giả. Khi so nhiều bản: loại hết bản rớt gate TRƯỚC, rồi mới xếp phần còn lại theo tổng.

## Khung report (xếp nhiều bản cạnh nhau)

```
CHẤM: checkpoint · <task-id> · <giai_doan> · <PASS|FAIL>
1 Phiếu đúng+đủ       [n/2] — <lý do 1 câu>
2 Bám Định-nghĩa-Xong [n/2] — <...>
3 Phiếu đọc-được      [n/2] — <...>
4 Đúng vai            [n/2] — <...>
5 Kết (→/progress)    [n/2] — <...>
TỔNG: <n>/10   ·   GATE: đạt / RỚT ở <tiêu chí ...>
SỬA TRƯỚC TIÊN: <một câu — đòn bẩy lớn nhất để phiếu này tốt hơn>
```

## Vì sao các tiêu chí này

Ba xương sống đo *có ra đúng phiếu + trung thực + đọc được không* — cấu trúc phiếu đúng path & đủ verdict (1), mọi ✓/✗ bám Định-nghĩa-Xong thật của giai đoạn chứ không bịa "đủ mục" (2, gate nặng nhất vì `progress` tin phiếu để mở nhánh), owner đọc là biết sửa gì (3). Hai cái sau đo *có đúng vai gác cổng không* — chỉ kiểm+phán không sửa artifact và không đụng đồ thị task (4, gấp thẳng ba luật "Chỉ kiểm, không sửa" / "Không đụng progress.json" / tiến cử `/review`), và nối đúng bước kế `/progress` để advance (5). Gộp lại = trọn hợp đồng của `checkpoint` trong SKILL.md, không hơn. Skill hạ tầng đơn giản nên 5 tiêu chí là đủ (theo bất biến "skill đơn giản có thể 5"); thêm tiêu chí thứ 6 chỉ khi có kiểu lỗi thật lặp lại mà bộ này không bắt được.
