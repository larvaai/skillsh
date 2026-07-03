# Rubric — 6 tiêu chí chấm một lượt `fanout` (điều phối chạy song song)

Mỗi tiêu chí 0/1/2. Khung chung: `grade/meta-rubric.md`. Chuẩn gốc để chấm: `fanout/SKILL.md` (mục "## Quy tắc bắt buộc" + 6 bước Bước 0→5) và các file luật con nó bám (`constitution/folders.md` cho path artifact, `progress` sở hữu `progress.json`, `checkpoint` sở hữu phiếu). Rubric chỉ biến hợp đồng đó thành thước đo — KHÔNG thêm tiêu chuẩn mới.

`fanout` là skill hạ tầng/điều phối: nó KHÔNG sinh artifact pipeline và KHÔNG tự viết code — nó gói ngữ cảnh, bung agent song song, thu kết quả về, rồi nhờ `checkpoint` + `progress` đóng nhánh. Vì vậy A1 (đúng+đủ output) ở đây = gói ngữ cảnh đủ + thu artifact về đúng path; A4 = đúng vai điều phối, KHÔNG lấn `progress`/`checkpoint`.

**Đầu vào để chấm (fixture):** `progress.json` (đồ thị task + `parallel_group` + trạng thái `ready/todo/done` + `artifact` path mỗi task) · `constitution/` (folders.md + conventions liên quan) · phiếu checkpoint của task đầu-vào-chung (contract) · nguyên văn lượt fanout (prompt đã gói cho từng agent + tóm tắt thu về + các lệnh `/checkpoint`, `/progress` đã gọi).

Tiêu chí **1 (Gói + thu output), 2 (Bám nguồn — không bịa kết quả task con), 3 (Đọc-được)** là **xương sống (gate)** — phủ A1 / A2 / A3.

## 1. GÓI NGỮ CẢNH ĐỦ + THU ARTIFACT VỀ (A1, xương sống)

Mỗi task được gói một prompt gọn đủ 5 phần theo Bước 2 (constitution/luật liên quan + contract + spec task + đích artifact + ranh giới KHÔNG-build); agent về thì xác nhận artifact đã nằm đúng `artifact` path của task (Bước 4).

- 0 — gói thiếu mảnh bắt buộc: prompt KHÔNG nêu đích artifact path, HOẶC KHÔNG nêu contract để bám, HOẶC KHÔNG có ranh giới KHÔNG-build (agent tự do lấn phần nhánh khác); HOẶC đổ cả repo/toàn bộ constitution/task của nhánh khác vào một agent (vi phạm "gói GỌN"); HOẶC không thu artifact về (không xác nhận file nằm đúng path).
- 1 — đủ 5 phần cho từng task nhưng một phần sơ sài (ranh giới KHÔNG-build mơ hồ, hoặc trích luật thừa/thiếu), hoặc thu về nhưng không `ls`/không xác nhận đúng path cho đủ mọi nhánh.
- 2 — mỗi task một gói gọn đủ 5 phần đúng Bước 2 (đúng contract path + trích đúng conventions liên quan + spec task + đích artifact + KHÔNG-build cụ thể); output cô lập (mỗi agent chỉ ghi vào path của mình, không đụng path nhánh khác); mọi artifact thu về được xác nhận nằm đúng đích.

## 2. BÁM NGUỒN — KHÔNG BỊA KẾT QUẢ TASK CON (A2, xương sống)

Mọi thứ báo về (artifact đã tạo, tóm tắt "đã làm gì", trạng thái PASS/FAIL) phải truy được về kết quả THẬT của sub-agent và về file thật trên đĩa — không tự bịa kết quả một nhánh, không tự khẳng định PASS khi chưa có phiếu, không báo artifact ở path chưa tồn tại. **Đây là gate nặng nhất của cả suite.**

- 0 — bịa: tóm tắt một nhánh mà agent đó không chạy/không trả về; khẳng định artifact "đã tạo" ở path chưa `ls` thấy; tự tuyên PASS/done cho một task khi chưa gọi `/checkpoint` (tự cấp phiếu — vi phạm luật vai); HOẶC bịa nhánh đầu-vào-chung "đã freeze/PASS" khi thực chưa có phiếu.
- 1 — chủ yếu bám thật, một chỗ mơ hồ không gắn nhãn (tóm tắt một nhánh suy đoán một phần "chắc là xong" mà chưa xác nhận file).
- 2 — mọi artifact báo về được xác nhận tồn tại đúng path; mọi tóm tắt gắn thẳng vào cái agent thật sự trả về; trạng thái PASS/FAIL đọc từ phiếu checkpoint thật, chỗ chưa chắc gắn nhãn rõ; không một dòng nào dựng trên nhánh chưa chạy.

## 3. ĐỌC-ĐƯỢC — tóm tắt điều phối nắm được ngay (A3, xương sống)

Khối fan-out và khối kết đọc được: một người mở lên là biết bung nhóm nào, mỗi agent làm task nào ra artifact nào, nhánh nào PASS/FAIL, cái gì vừa mở khóa. Theo mẫu Bước 3 + Bước 5.

- 0 — không có khối tóm tắt đọc-được; đổ một cục log agent thô không map task-id ↔ agent ↔ artifact; người đọc không biết đã bung nhóm nào hay nhánh nào xong.
- 1 — có khối nhưng lệch: thiếu map task-id↔artifact, hoặc không nêu cái gì được mở khóa sau khi đóng nhánh, hoặc dày jargon khó scan.
- 2 — khối FAN-OUT nêu rõ đầu-vào-chung (frozen/PASS) + mỗi agent → task-id → việc → artifact; khối kết nêu từng nhánh PASS/FAIL → done, cái gì mở khóa (vd task hợp-nhất phụ thuộc cả hai → ready), và bước kế; scan 30 giây là nắm.

## 4. ĐIỀU KIỆN FAN-OUT — chỉ bung khi CẢ nhóm ready + đầu vào chung đã freeze (A4)

Gấp luật cứng Bước 1 + hai luật "Chỉ bung khi CẢ nhóm ready" và "Đầu vào chung phải đã chốt": mọi task trong `parallel_group` phải `ready` (mọi `depends_on` đã `done`), và task đầu-vào-chung (contract) phải `done` + có phiếu checkpoint `PASS` trước khi bung.

- 0 — bung nhóm khi còn một task `todo`/chưa `ready` (một `depends_on` chưa `done`); HOẶC bung quanh một contract chưa freeze (đầu-vào-chung chưa `done` hoặc chưa có phiếu `PASS`) → hai agent build lệch nhau.
- 1 — nhóm ready và contract done, nhưng bỏ bước kiểm tường minh điều kiện (không nêu đã kiểm mọi task ready / chưa dẫn phiếu PASS của contract) — đúng kết quả nhưng thiếu kỷ luật kiểm.
- 2 — kiểm tường minh Bước 1 trước khi bung: xác nhận mọi task trong nhóm `ready` và dẫn được phiếu `PASS` của đầu-vào-chung; nếu thiếu điều kiện thì DỪNG, nói rõ thiếu gì + tiến cử làm nốt phụ thuộc, không bung ép.

## 5. ĐÚNG VAI ĐIỀU PHỐI — không tự ghi progress.json, không tự cấp phiếu, không tự code (A4)

Gấp ranh giới lõi của skill: `fanout` chỉ điều phối chạy; `progress` sở hữu `progress.json`, `checkpoint` sở hữu phiếu, mỗi sub-agent tự làm phần code/việc của nó. `fanout` gọi hai skill kia, không tự tay ghi.

- 0 — lấn vai: tự tay sửa/ghi `progress.json` (lật task `done`, mở khóa) thay vì gọi `/progress`; HOẶC tự viết phiếu checkpoint / tự tuyên PASS thay vì gọi `/checkpoint`; HOẶC tự viết code phần việc của một nhánh thay vì bung sub-agent làm.
- 1 — chủ yếu đúng vai, lỡ một chỗ lấn nhẹ (vd tự mô tả "đã lật done" như thể mình ghi, dù thực có gọi `/progress`), hoặc mô tả mập mờ ai ghi file.
- 2 — thuần điều phối: mọi thay đổi `progress.json` đi qua `/progress`, mọi phiếu đi qua `/checkpoint`, mọi phần việc do sub-agent làm; `fanout` chỉ gói ngữ cảnh, bung, thu về, và gọi hai skill kia — không tự chạm file hai skill đó sở hữu, không tự code.

## 6. BUNG SONG SONG THẬT + ĐÓNG TỪNG NHÁNH ĐÚNG THỨ TỰ (A5)

Gấp Bước 3 (bung TẤT CẢ agent trong MỘT lượt để song song thật) + Bước 5 (đóng từng nhánh: `/checkpoint <task>` → PASS thì `/progress` advance; một nhánh FAIL không chặn nhánh khác đóng).

- 0 — không thực sự song song (bung tuần tự từng agent, chờ xong cái này mới cái kia); HOẶC bỏ hẳn bước đóng nhánh (thu artifact xong không `/checkpoint` + `/progress` nhánh nào); HOẶC một nhánh FAIL kéo chặn cả các nhánh PASS không cho đóng.
- 1 — bung song song và có đóng nhánh, nhưng thứ tự/đối xử lệch: đóng nhưng không nêu `/checkpoint` trước `/progress`, hoặc không nói rõ nhánh FAIL quay lại sửa rồi checkpoint lại, hoặc thiếu nêu cái gì được mở khóa.
- 2 — mọi sub-agent bung trong một lượt (nhiều tool call cùng message) để chạy đồng thời thật; mỗi nhánh về thì `/checkpoint <task-id>` rồi PASS mới `/progress` advance đúng thứ tự; nhánh FAIL giữ mở + nêu cần sửa gì mà không chặn nhánh PASS đóng; kết bằng khối mở-khóa + trỏ bước kế (`/progress` hoặc `/resume`).

## Gate (tiêu chí xương sống)

Tiêu chí **1 (Gói + thu output), 2 (Bám nguồn — không bịa kết quả task con), 3 (Đọc-được)** là xương sống — phủ A1 / A2 / A3. Bất kỳ cái nào = 0 → lượt fanout **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một lượt 10/12 nhưng bịa kết quả một nhánh chưa chạy (tiêu chí 2 = 0) vẫn rớt — vì `progress`/`checkpoint` phía sau sẽ đóng nhầm một task không có artifact thật. Khi so nhiều bản: loại hết bản rớt gate TRƯỚC, rồi mới xếp phần còn lại theo tổng.

## Khung report (xếp nhiều bản cạnh nhau)

```
CHẤM: fanout · <parallel_group / fixture>
1 Gói+thu output   [n/2] — <lý do 1 câu>
2 Bám nguồn        [n/2] — <...>
3 Đọc-được         [n/2] — <...>
4 Điều kiện fanout [n/2] — <...>
5 Đúng vai         [n/2] — <...>
6 Song song+đóng   [n/2] — <...>
TỔNG: <n>/12   ·   GATE: đạt / RỚT ở <tiêu chí ...>
SỬA TRƯỚC TIÊN: <một câu — đòn bẩy lớn nhất để bản này tốt hơn>
```

## Vì sao 6 tiêu chí này

Ba xương sống đo *có ra đúng thứ + trung thực + đọc được không*: gói ngữ cảnh đủ và thu artifact về (A1), không bịa kết quả nhánh con (A2 — lỗi lặp nặng nhất của suite: báo PASS/artifact từ thứ không tồn tại), và tóm tắt điều phối đọc-được (A3). Ba cái sau đo *có đúng kỷ luật điều phối không*: chỉ bung khi cả nhóm ready + đầu vào đã freeze (Bước 1), đúng vai — không tự ghi `progress.json`/không tự cấp phiếu/không tự code (ranh giới lõi), và bung song song thật + đóng từng nhánh đúng cổng theo thứ tự (Bước 3+5). Sáu tiêu chí này gấp trọn năm Quy tắc bắt buộc và sáu bước của `fanout`, không hơn. Thêm tiêu chí thứ 7 chỉ khi có một kiểu lỗi thật lặp lại mà sáu cái này không bắt được.
