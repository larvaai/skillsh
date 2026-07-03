# Rubric — 7 tiêu chí chấm một bản `progress` (sổ tiến độ & đồ thị task)

Mỗi tiêu chí 0/1/2. Khung chung: `grade/meta-rubric.md`. Chuẩn gốc để chấm: `progress/SKILL.md` (mục "## Quy tắc bắt buộc", "## Trạng thái task", hai chế độ PLAN/ADVANCE, "## Schema — progress.json", "## board.md") + `constitution/definition-of-done.md` (điều kiện #3 do `progress` sở hữu, điều kiện #2 do `progress` ĐỌC). Rubric chỉ biến hợp đồng đó thành thước đo — KHÔNG thêm tiêu chuẩn mới.

**Đầu vào để chấm (fixture):** một thao tác `progress` cụ thể — mode (PLAN chia chunk kế / ADVANCE đóng một bước) · progress.json trước thao tác · constitution liên quan (folders.md để kiểm đích artifact, checkpoints/ để kiểm phiếu) · output (progress.json + board.md sau thao tác + khối in ra).

Tiêu chí **1 (Đúng+đủ output), 3 (Không bịa trạng thái), 4 (Đọc-được board)** là **xương sống (gate)**.

## 1. ĐÚNG + ĐỦ OUTPUT — schema chuẩn + board mirror (xương sống)

progress.json đúng schema và board.md là ảnh trung thành của nó. Mỗi task mới/sửa mang đủ trường bắt buộc: `id · viec · giai_doan · trang_thai · depends_on[] · parallel_group · owner · artifact`; `updated_at` cập nhật; khối in ra (PLAN "ĐÃ CHIA TASK" hoặc ADVANCE "ĐÓNG BƯỚC") đúng dạng.

- 0 — thiếu một trường xương của task (không có `depends_on`, hoặc thiếu `owner`, hoặc thiếu `artifact` đích), HOẶC `board.md` không được cập nhật / lệch hẳn progress.json (task có trong json mà board không có, trạng thái hai bên khác nhau), HOẶC không in khối kết quả theo mẫu.
- 1 — đủ trường nhưng một chỗ sơ sài: `artifact` để chung chung không theo `folders.md`, hoặc board thiếu khối "Đang ready" / "Song song sẵn sàng" ở đầu, hoặc `updated_at` không đổi.
- 2 — đủ mọi trường đúng schema; `artifact` trỏ path cụ thể theo `folders.md`; `board.md` mirror trọn (mọi task, đúng trạng thái, có khối ready + nhóm song song ở đầu); `updated_at` mới; khối in ra đúng mẫu PLAN/ADVANCE.

## 2. ĐỒ THỊ ĐÚNG — depends_on/parallel_group là DỮ LIỆU, không lời kể

Muốn hai việc song song thì cho chúng cùng `parallel_group` và `depends_on` giống nhau (thường cùng trỏ về task contract) — không "song song" bằng miệng. Điểm fan-out nhận đúng: task chỉ phụ thuộc CÙNG một đầu vào đã sẵn và không phụ thuộc lẫn nhau → chung nhóm.

- 0 — tuyên bố song song bằng lời/ghi_chu mà `parallel_group` để null hoặc `depends_on` không khớp; HOẶC cho chung `parallel_group` hai task thực ra phụ thuộc lẫn nhau (một cái `depends_on` cái kia); HOẶC bỏ sót điểm fan-out rõ (hai task cùng chờ contract đã freeze mà để tuần tự).
- 1 — đồ thị đúng phần lớn nhưng một cạnh phụ thuộc thiếu/thừa, hoặc một nhóm song song gán đúng nhưng không ghi chú "mở nhánh song song, chạy /fanout".
- 2 — mọi quan hệ song song/tuần tự nằm trong `depends_on`+`parallel_group` (không phải lời kể); điểm fan-out nhận đúng; nhóm song song đủ điều kiện được đánh dấu để `fanout` bung.

## 3. KHÔNG BỊA TRẠNG THÁI — bám phiếu & bám đồ thị (xương sống)

Mọi lần lật trạng thái truy được về sự thật: `done` chỉ khi `progress/checkpoints/<task-id>.md` tồn tại và verdict `PASS`; `ready` chỉ khi mọi `depends_on` đã `done`. Không chế trạng thái, không lật `done` khi thiếu phiếu — đây là cách ép Định-nghĩa-Xong.

- 0 — lật một task `done` khi phiếu checkpoint KHÔNG tồn tại hoặc verdict `FAIL` (bịa "đã xong"); HOẶC chuyển `ready` một task còn `depends_on` chưa `done`; HOẶC báo mở khóa/con trỏ dựa trên trạng thái không có trong đồ thị. **Đây là vi phạm nặng nhất** — đẩy nhánh sau trên nền chưa đạt.
- 1 — trạng thái chủ yếu đúng nhưng một chỗ suy đoán không kiểm phiếu (lật done mà không dẫn được phiếu PASS), hoặc quên chặn khi phiếu FAIL.
- 2 — mọi `done` dẫn được về phiếu PASS đúng path; mọi `ready` có đủ `depends_on` đã done; thiếu phiếu → GIỮ `in_progress` + bảo user chạy `/checkpoint <task-id>` (nếu FAIL nêu lý do trong phiếu); không một trạng thái nào không có nguồn.

## 4. ĐỌC-ĐƯỢC — board.md nắm được trong một liếc (xương sống)

`board.md` là bản người đọc: một bảng `id · việc · giai đoạn · trạng thái · phụ thuộc · nhóm song song · owner · artifact`, kèm khối "Đang ready" và "Song song sẵn sàng" ở đầu để đọc nhanh. Khối in ra (PLAN/ADVANCE) phẳng, quét được.

- 0 — board là JSON thô / không có bảng đọc-được, HOẶC không có khối ready ở đầu nên phải dò cả bảng mới biết làm gì kế, HOẶC khối in ra dày đặc không theo mẫu.
- 1 — có bảng nhưng thiếu một cột, hoặc khối ready/song song có mà lẫn, hoặc bảng đọc được nhưng cần đọc kỹ mới thấy task nào chạy được.
- 2 — bảng đủ cột, một liếc thấy ngay đang ready cái gì + nhóm nào song song được + ai owner + đích artifact; khối PLAN/ADVANCE ngắn, đúng mẫu, quét 30 giây ra việc kế.

## 5. ĐÚNG VAI — chỉ ghi đồ thị, KHÔNG cấp phiếu / KHÔNG sửa artifact

`progress` là chủ DUY NHẤT của progress.json + board.md và CHỈ ghi đồ thị. Nó ĐỌC phiếu (không tự cấp — việc của `checkpoint`), không bung agent (việc của `fanout`), không kiểm/sửa nội dung artifact, không lặp phân rã tầng sản phẩm của `backlog`.

- 0 — lấn vai: tự cấp/tự sửa phiếu checkpoint thay vì đọc, HOẶC sửa/kiểm nội dung artifact, HOẶC tự spawn agent chạy task, HOẶC đẻ Epic/Feature/Story trùng `backlog` thay vì task thực thi mỏng.
- 1 — chủ yếu đúng vai nhưng lấn nhẹ: bình phẩm chất lượng artifact như thể đang checkpoint, hoặc task phình thành mô tả sản phẩm thay vì việc-chạy-được.
- 2 — thuần ghi đồ thị: đọc phiếu để quyết lật done, tính ready/parallel, cập nhật con trỏ; task mỏng (một skill/agent làm gọn, một artifact rõ), có thể `traces_to` về story `backlog` mà không lặp nó; nhường checkpoint/fanout đúng ranh giới.

## 6. APPEND, KHÔNG XOÁ — đồ thị là lịch sử

Sửa `trang_thai` tại chỗ; không xoá task cũ. Lịch sử đồ thị được giữ nguyên qua các lần thao tác.

- 0 — xoá task cũ khỏi progress.json/board, HOẶC ghi đè mất trạng thái trước (task từng có biến mất), làm đứt lịch sử.
- 1 — giữ được task cũ nhưng một chỗ chỉnh lịch sử không cần (đổi `id`, viết lại `viec` cũ) khiến khó lần vết.
- 2 — mọi task cũ còn nguyên; chỉ `trang_thai`/`con_tro`/`updated_at` đổi tại chỗ; đồ thị đọc được như một lịch sử liền mạch.

## 7. CON TRỎ + MỞ KHÓA + BÀN GIAO — advance khép đúng vòng

Sau advance: mở khóa mọi task `todo` đã đủ `depends_on` done → `ready`; `con_tro.giai_doan` trỏ tới giai đoạn của task ready kế (luôn khớp task ready đầu tiên); nhóm song song vừa đủ ready → nhắc `/fanout`; kết bằng gợi ý đúng skill owner của task ready kế.

- 0 — không mở khóa task lẽ ra ready (depends_on đã done mà vẫn `todo`), HOẶC con trỏ không dời / trỏ sai giai đoạn, HOẶC không gợi ý bước kế nào.
- 1 — mở khóa đúng nhưng con trỏ lệch nhẹ, hoặc quên nhắc `/fanout` khi một nhóm song song vừa đủ ready, hoặc gợi ý bước kế chung chung không nêu skill owner.
- 2 — mở khóa trọn mọi task đủ điều kiện; con trỏ khớp task ready đầu tiên; nhóm song song đủ ready thì nhắc `/fanout`, ngược lại trỏ đúng `/<skill owner task ready kế>`; chỉ gợi ý, không tự chạy hộ.

## Gate

Tiêu chí **1, 3, 4** là xương sống. Bất kỳ cái nào = 0 → bản **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản đồ thị đẹp nhưng lật `done` khi thiếu phiếu PASS (tiêu chí 3 = 0) vẫn rớt — vì nó đẩy nhánh sau trên nền chưa đạt, phá đúng cái Định-nghĩa-Xong mà `progress` phải ép. Khi so nhiều bản: loại hết bản rớt gate TRƯỚC, rồi mới xếp phần còn lại theo tổng.

## Khung report (xếp nhiều bản cạnh nhau)

```
CHẤM: progress · <fixture: mode PLAN/ADVANCE · thao tác>
1 Đúng+đủ output      [n/2] — <lý do 1 câu>
2 Đồ thị đúng         [n/2] — <...>
3 Không bịa trạng thái[n/2] — <...>
4 Đọc-được board      [n/2] — <...>
5 Đúng vai            [n/2] — <...>
6 Append không xoá    [n/2] — <...>
7 Con trỏ+mở khóa     [n/2] — <...>
TỔNG: <n>/14   ·   GATE: đạt / RỚT ở <tiêu chí ...>
SỬA TRƯỚC TIÊN: <một câu — đòn bẩy lớn nhất để bản này tốt hơn>
```

## Vì sao 7 tiêu chí này

Ba xương sống đo *có ra đúng cấu trúc + trung thực + đọc được không* (schema+mirror, không bịa trạng thái, board đọc-được) — đúng ba trục A1/A2/A3 của meta-rubric áp vào một skill hạ tầng. Bốn cái sau đo *có giữ đúng kỷ luật đồ thị không*: đồ thị-là-dữ-liệu (song song không bằng miệng), đúng vai (không cấp phiếu, không sửa artifact — A4), append-không-xoá, và advance khép vòng (mở khóa + con trỏ + bàn giao — A5). Mỗi tiêu chí gấp một Luật cứng của SKILL.md thành một anchor-0: "Một chủ / không sửa artifact" → TC5; "Không lật done khi thiếu phiếu" → TC3; "depends_on/parallel_group là dữ liệu" → TC2; "Append không xoá" → TC6; "Con trỏ luôn khớp task ready đầu" → TC7. Gộp lại = trọn hợp đồng của `progress`, không hơn. Thêm tiêu chí thứ 8 chỉ khi có kiểu lỗi thật lặp lại mà 7 cái này không bắt được.
