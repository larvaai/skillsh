# Rubric — 6 tiêu chí chấm một bản `resume` (cửa vào read-only, in khối toàn cảnh)

Mỗi tiêu chí 0/1/2. Khung chung: `grade/meta-rubric.md`. Chuẩn gốc để chấm: `resume/SKILL.md` (mục "Quy tắc bắt buộc" + "Bước 1 Đọc" + "Bước 2 In khối toàn cảnh" + các nhánh project-trống / cổng-chờ-ký). Rubric chỉ biến hợp đồng đó thành thước đo được — KHÔNG thêm tiêu chuẩn mới.

Ba tiêu chí **1 (Khối toàn cảnh đủ mục), 2 (Bám trạng thái thật), 3 (Đọc-được)** là **xương sống (gate)** — phủ A1 / A2 / A3. Rớt bất kỳ cái nào → rớt cả bản dù tổng cao.

**Đầu vào để chấm (fixture):** project key + nội dung thật của `projects/<key>/` (constitution/, progress/progress.json, và bốn folder artifact problem·idea·docs·codebase) · nguyên văn khối toàn cảnh mà `resume` in ra. Đủ để đối chiếu từng dòng khối với con trỏ + tasks + artifact có thật.

## 1. KHỐI TOÀN CẢNH ĐỦ MỤC (A1 — xương sống)

In đúng một khối toàn cảnh theo mẫu Bước 2, đủ sáu mục bắt buộc: **Bức tranh lớn** · **Con trỏ (giai_doan + ghi_chu)** · **Đã chốt gần nhất (task done + artifact)** · **Sẵn sàng chạy (task ready)** · **Chạy song song được (nhóm, hoặc "chưa")** · **Tiến cử skill kế**. Bỏ một mục ≠ rút gọn.

- 0 — thiếu hẳn một mục xương của khối: KHÔNG có "Con trỏ đang ở đâu", HOẶC KHÔNG có "Sẵn sàng chạy" (task ready), HOẶC KHÔNG có dòng "→ Tiến cử". (Với project vừa charter: 0 nếu không rút gọn đúng — không nói "vừa dựng, chưa có ý" + không tiến cử `/idea`.)
- 1 — có đủ khung sáu mục nhưng một mục rỗng/lệch: "Đã chốt gần nhất" không kèm artifact, hoặc "Chạy song song được" bỏ trống thay vì ghi "chưa", hoặc có >1 task ready không cùng nhóm mà không liệt kê tối đa 3 để user chọn.
- 2 — đủ sáu mục đúng mẫu; mỗi mục một dòng cô đọng; nhiều ready không cùng nhóm → liệt kê tối đa 3; đúng nhánh đặc biệt (project trống → khối rút gọn; cổng chờ ký → nhắc "đang chờ bạn ký GO/NO-GO" thay vì tiến cử đi tiếp).

## 2. BÁM TRẠNG THÁI THẬT — KHÔNG BỊA (A2 — xương sống)

Mọi dòng trong khối truy được về `progress.json` + artifact có thật. **Chỉ báo done những task `progress.json` ghi done** (Quy tắc "Trung thực với tiến độ thật"); không suy diễn tiến độ từ việc "đã bàn tới". Con trỏ, "ready", nhóm song song tính đúng theo luật Bước 1 (ready = `trang_thai` ready HOẶC todo mà mọi `depends_on` đã done; nhóm song song = mọi task trong `parallel_group` đều ready).

- 0 — bịa trạng thái: báo một task done mà `progress.json` không ghi done (suy từ "đã bàn tới"); HOẶC "Bức tranh"/"Đã chốt" dẫn artifact/file không có thật; HOẶC tính "ready" sai luật (gọi ready một task còn `depends_on` chưa done), HOẶC gọi một `parallel_group` là "chạy song song được" khi có task trong nhóm chưa ready.
- 1 — chủ yếu bám thật, một chỗ suy đoán không gắn nhãn (vd đoán ghi_chú con trỏ, hoặc một-dòng-tổng-thể phóng đại hơn dòng đầu artifact) nhưng không sai trạng thái done/ready.
- 2 — mọi dòng nối được về con trỏ/tasks/artifact thật; done đúng đúng những gì `progress.json` ghi; ready + nhóm song song tính đúng luật; chỗ chưa chắc (nếu có) gắn nhãn thay vì khẳng định.

## 3. ĐỌC-ĐƯỢC (A3 — xương sống)

Người quay lại project liếc khối là nắm ngay "đang ở đâu, làm gì tiếp" — câu ngắn, phẳng, mỗi mục một dòng, không jargon thừa, không đổ nguyên JSON/đường dẫn dài.

- 0 — dày đặc/khó liếc: đổ nguyên progress.json hoặc danh sách toàn bộ tasks, tường bullet nhiều tầng, hoặc phải đọc kỹ mới ra được con trỏ và bước kế.
- 1 — đọc được nhưng còn rườm: vài dòng dài quá một ý, hoặc thừa định dạng, hoặc trộn chi tiết phụ vào mục chính.
- 2 — khối gọn một màn hình, mỗi mục một dòng cô đọng, "Bức tranh" 1–2 câu nghiệp vụ; liếc 15 giây ra được đang-ở-đâu + bước-kế.

## 4. CHỈ ĐỌC — KHÔNG TẠO/SỬA FILE (A4 — Luật cứng)

`resume` **read-only tuyệt đối**: không ghi bất kỳ file nào, kể cả `state/current.json`. Muốn dựng mới → đó là `charter`; muốn cập nhật task/con trỏ → đó là `progress`. Chỉ đọc, tính trong đầu, in ra.

- 0 — vi phạm read-only: ghi/sửa bất kỳ file nào (`progress.json`, `current.json`, artifact…), HOẶC tự tạo file/folder mới, HOẶC "cập nhật con trỏ / đánh dấu done" trong lượt resume.
- 1 — không ghi file nhưng lấn nhẹ vai: tự đề xuất chỉnh nội dung một artifact, hoặc diễn giải lại luật constitution như thể sửa nó, thay vì chỉ đọc-và-kể.
- 2 — thuần đọc: chỉ nạp constitution + progress.json + đầu mục artifact rồi in khối; không đụng file nào; khi cần đổi trạng thái thì trỏ sang `charter`/`progress`, không tự làm.

## 5. CHỈ TIẾN CỬ — KHÔNG TỰ CHẠY, KHÔNG HỎI LẠI ĐIỀU ĐÃ CÓ (A4/A5 — Luật cứng)

Kết bằng tiến cử một skill kế (nói "nên chạy `/idea`"), user tự chạy; **không tự mở skill kế**. Và **không hỏi lại điều đã có trong file** — con trỏ, quyết định đã chốt, task đang mở thì đọc ra, không hỏi.

- 0 — tự chạy skill kế thay user (mở `idea`/`shape`… ngay trong lượt resume), HOẶC hỏi lại điều đã nằm sẵn trong file (hỏi "project này đang ở giai đoạn nào?" trong khi progress.json có con trỏ).
- 1 — chỉ tiến cử nhưng lấn nhẹ: giục/quyết hộ user nên chạy cái nào trước khi có >1 lựa chọn hợp lệ, hoặc hỏi một chi tiết lẽ ra đọc được từ artifact.
- 2 — dừng đúng ở mức tiến cử: nêu skill kế (và `/fanout` nếu có nhóm song song sẵn sàng), nhiều ready thì liệt kê để user chọn; không tự chạy, không hỏi lại cái đã có.

## 6. TIẾN CỬ ĐÚNG SKILL KẾ THEO CON TRỎ (A5)

Skill kế suy đúng từ `owner` của task ready đầu tiên (idea→`/idea`, shape→`/shape`, modules→`/modules`, delivery→`/delivery`…); có nhóm song song sẵn sàng → tiến cử `/fanout`; con trỏ ở cổng chờ ký → KHÔNG tiến cử đi tiếp mà nhắc chờ ký.

- 0 — tiến cử sai skill so với owner task ready (vd con trỏ ở Domain/idea mà tiến cử `/skeleton`), HOẶC bỏ qua nhóm song song đã sẵn sàng mà vẫn tiến cử một skill đơn, HOẶC tiến cử đi tiếp khi con trỏ đang ở cổng chờ user ký GO/NO-GO.
- 1 — tiến cử skill hợp lý nhưng lệch: đúng họ nhưng không khớp owner chính xác, hoặc có nhóm song song mà chỉ nhắc mờ không nêu `/fanout`.
- 2 — tiến cử khớp owner task ready đầu tiên; nhóm song song sẵn sàng → nêu `/fanout`; cổng chờ ký → nhắc "đang chờ bạn ký" thay vì tiến cử tiếp; project trống → tiến cử `/idea`.

## Gate

Tiêu chí **1, 2, 3** là xương sống (A1 đúng+đủ output · A2 bám nguồn không bịa · A3 đọc-được). Bất kỳ cái nào = 0 → bản **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản khối đẹp, tiến cử gọn (4·5·6 đều 2) nhưng báo một task done mà progress.json không ghi done (tiêu chí 2 = 0) vẫn rớt — vì user sẽ tin nhầm mình đã qua bước đó. Khi so nhiều bản: loại hết bản rớt gate TRƯỚC, rồi mới xếp phần còn lại theo tổng.

## Khung report

```
CHẤM: resume · <project key / fixture>
1 Khối đủ mục       [n/2] — <lý do 1 câu>
2 Bám trạng thái    [n/2] — <...>
3 Đọc-được          [n/2] — <...>
4 Chỉ đọc           [n/2] — <...>
5 Chỉ tiến cử       [n/2] — <...>
6 Tiến cử đúng      [n/2] — <...>
TỔNG: <n>/12   ·   GATE: đạt / RỚT ở <tiêu chí ...>
SỬA TRƯỚC TIÊN: <một câu — đòn bẩy lớn nhất để bản này tốt hơn>
```

## Vì sao các tiêu chí này

Ba xương sống đo *có in đúng thứ resume hứa, trung thực với state, và liếc-được không* (khối đủ mục, bám trạng thái thật, đọc-được) — trùng ba trục gate A1/A2/A3 của meta-rubric. Ba cái sau đo *có giữ đúng vai read-only-chỉ-tiến-cử không*: tiêu chí 4 gấp luật cứng "read-only tuyệt đối" (ghi file = 0), tiêu chí 5 gấp hai luật "chỉ tiến cử không tự chạy" + "không hỏi lại điều đã có" (đây là nơi resume hay lấn sang `progress`/`charter`), tiêu chí 6 đo tiến cử có đúng con trỏ + xử đúng cổng chờ ký không. Gộp lại = trọn hợp đồng của `resume`, không hơn: mọi tiêu chí truy về "Quy tắc bắt buộc" hoặc "Bước 1/Bước 2" trong SKILL.md, không phát minh chuẩn mới. Thêm tiêu chí thứ 7 chỉ khi có kiểu lỗi thật lặp lại mà sáu cái này không bắt được.
