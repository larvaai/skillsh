---
name: trace
description: Theo dấu data, state, hoặc side effect qua codebase. Dùng khi người dùng muốn biết một giá trị đi từ đâu đến đâu, state thay đổi ở chỗ nào, hoặc gọi một hàm thì có gì xảy ra ngoài ý muốn. Mức L5 trở lên.
---

# Trace — Theo dấu data, state, side effect

Trace không giải thích — trace điều tra. Claude và người dùng cùng đi theo một thứ cụ thể qua code, dừng lại ở mỗi điểm thay đổi, ghi nhận những gì thực sự xảy ra.

## Quy tắc
- Tái dùng `.ai-understanding/` trước: đọc flow artifacts nếu có, chỉ đọc file gốc khi cần xác minh hoặc artifact không đủ chi tiết.
- Mỗi bước trace phải có evidence: `file · dòng/symbol · điều xảy ra · độ chắc chắn`.
- Tách quan sát được khỏi suy luận — gắn nhãn rõ khi suy.
- Nếu một chỗ không rõ: ghi là "chưa rõ", không đoán mò.
- Side effect và state change phải được đánh dấu nổi bật, không để lẫn vào mô tả thông thường.

## Ba loại trace

```
data   — Theo một giá trị cụ thể từ điểm vào đến điểm ra.
         Kích bởi: "X đi đâu", "giá trị này được truyền thế nào", "ai nhận Y"

state  — Tìm tất cả chỗ một state có thể thay đổi.
         Kích bởi: "X thay đổi ở đâu", "tại sao state này bị reset", "ai có thể ghi vào Z"

effect — Liệt kê mọi thứ xảy ra khi gọi một hàm/action.
         Kích bởi: "gọi X thì có gì xảy ra", "side effect của Y là gì", "hàm này đụng đến gì"
```

Nếu không chắc loại: hỏi *"Bạn đang theo dấu một giá trị, tìm chỗ state thay đổi, hay muốn biết side effect của một hàm?"*

## Bước 0 — Xác định project

Lấy đường dẫn project theo thứ tự ưu tiên:
1. Argument truyền vào.
2. Tên/đường dẫn nhắc trong tin nhắn.
3. `state/current.json` nếu có.
4. Nếu vẫn không rõ: hỏi.

## Bước 1 — Xác định đối tượng trace

Hỏi hoặc suy ra từ câu của người dùng:
- **Đối tượng**: tên biến, field, hàm, event, hoặc state cụ thể.
- **Điểm bắt đầu**: người dùng biết nó xuất phát từ đâu không? Nếu không, tìm điểm khởi tạo đầu tiên.
- **Đích hoặc triệu chứng**: họ muốn biết nó đi đến đâu, hay đang thấy hành vi lạ ở đâu đó?

Nếu đối tượng còn mơ hồ: hỏi thêm một câu trước khi bắt đầu trace.

## Bước 1.7 — Dựng tình huống đời thường

Trước khi vào code, dựng một tình huống đời thường tương đương và bảng ánh xạ:

```
TÌNH HUỐNG: <1–2 câu mô tả bằng ngôn ngữ đời thường, không dùng tên kỹ thuật>

Đời thường              | Trong code
------------------------|---------------------------
<vai trò / hành động>   | <tên class/function/file>
...                     | ...
```

Mục đích: giúp người dùng có mental model trước khi gặp tên kỹ thuật. Không bỏ qua bước này ngay cả khi người dùng có vẻ kỹ thuật — tình huống đời thường giúp phát hiện khi code KHÔNG hoạt động như người ta tưởng.

## Bước 1.5 — Kiểm tra artifact

Đọc `<project-path>/.ai-understanding/00_index.md` và các flow artifact nếu có.
- Còn tươi và có flow liên quan: bắt đầu từ artifact, xác minh bằng file gốc khi cần.
- Có `99_changes.md` pending ở phần liên quan: coi artifact đó là stale, đọc file gốc.
- Chưa có: trace từ file gốc, gợi ý chạy `atlas` sau để lưu lại cho lần sau.

## Bước 2 — Trace từng bước

Đi theo đối tượng qua code, mỗi bước ghi:

```
[i] <file> · <symbol/dòng>
    Xảy ra: <mô tả ngắn>
    [STATE CHANGE] / [SIDE EFFECT] / [TRANSFORM] — nếu có
    Độ chắc chắn: cao / trung bình / thấp
    Chưa rõ: <ghi nếu có>
```

Quy tắc đi:
- **data**: đi theo chiều truyền — argument → parameter → return → caller.
- **state**: tìm tất cả write point (assignment, mutation, dispatch) — không chỉ happy path.
- **effect**: đi theo chiều gọi — hàm chính → mọi hàm nó gọi → I/O, external call, shared state.

Dừng khi: đến điểm ra, hết chuỗi gọi, hoặc gặp boundary (external service, DB, event bus) — ghi rõ là boundary, không đoán tiếp.

## Bước 3 — Tổng hợp (lên đầu output, trước bằng chứng)

Tổng hợp là thứ người dùng đọc TRƯỚC. Bằng chứng chi tiết (Bước 2) chỉ hiện khi được hỏi.

```
ĐỐI TƯỢNG: <tên>
LOẠI: data / state / effect
ĐƯỜNG ĐI: <A> → <B> → <C> → ...

ĐIỂM THAY ĐỔI QUAN TRỌNG
  [i] <file · symbol> — <điều xảy ra>

SIDE EFFECT TÌM ĐƯỢC
  <liệt kê, hoặc "không có">

CHƯA RÕ / RỦI RO
  <liệt kê, hoặc "không có">
```

Sau tổng hợp, hỏi: *"Bạn muốn xem bằng chứng chi tiết cho bước nào không?"* — chỉ mở rộng bước được chỉ định, không dump hết.

## Bước 4 — Gợi ý

Sau tổng hợp, hỏi theo những gì vừa tìm được:
- Nếu thấy state change bất ngờ: *"Bạn muốn tôi tìm tất cả chỗ có thể ghi vào state này không?"*
- Nếu thấy side effect ngoài ý muốn: *"Bạn muốn xem side effect này ảnh hưởng đến phần nào khác không?"*
- Nếu có chỗ chưa rõ: *"Có một đoạn tôi chưa chắc ở [X] — bạn muốn tôi đào sâu vào đó không?"*
- Nếu trace sạch: *"Bạn muốn review edge case của luồng này, hay trace một path khác?"* → gợi ý skill `review`.

## Bước 5 — Cập nhật state

Ghi `state/current.json`:
```json
{ "project": "<project-path>", "updated_at": "<ISO 8601>" }
```
