# Rubric — 7 tiêu chí chấm một bản `trace` (theo dấu data / state / side effect)

Mỗi tiêu chí 0/1/2. Khung chung: `grade/meta-rubric.md`. Chuẩn gốc để chấm: `trace/SKILL.md` (mục "## Quy tắc", "## Ba loại trace", các Bước 1.7 / 2 / 3 / 4). Rubric chỉ biến hợp đồng đó thành thước đo được — KHÔNG thêm tiêu chuẩn mới.

`trace` là skill đọc-hiểu (mức L5 trở lên): nó KHÔNG giải thích tổng quan, KHÔNG liệt gap, KHÔNG phán số phận file — nó điều tra một thứ cụ thể đi qua code. Rubric bám đúng ranh giới đó.

**Đầu vào để chấm (fixture):** project (codebase bản trace đang nói tới, để kiểm bịa) · đối tượng trace (biến/field/hàm/event/state cụ thể) · loại trace (data / state / effect) · output (nguyên văn câu trả lời của bản trace).

Tiêu chí **1 (Đúng+đủ đường đi), 3 (Bám code), 4 (Mức+lời văn)** là **xương sống (gate)** — phủ A1 / A2 / A3. Bất kỳ cái nào = 0 → cả bản RỚT GATE dù tổng cao.

## 1. ĐÚNG + ĐỦ ĐƯỜNG ĐI — trả trọn thứ trace hứa (xương sống · A1)

Bản trace phải trả đúng loại câu trả lời cho loại trace, đủ ba mảnh cốt lõi: đường đi đầu→cuối, điểm state đổi, side effect. Cụ thể theo loại (SKILL.md "Quy tắc đi"): **data** đi theo chiều truyền argument→parameter→return→caller; **state** liệt kê MỌI write point (assignment/mutation/dispatch), không chỉ happy path; **effect** đi theo chiều gọi tới mọi I/O, external call, shared state.

- 0 — thiếu một mảnh xương: không có ĐƯỜNG ĐI đầu→cuối (chỉ tả một điểm), HOẶC bỏ mục "điểm thay đổi quan trọng", HOẶC bỏ mục side effect; HOẶC trace state mà chỉ theo happy path bỏ sót write point khác; HOẶC không dừng ở boundary mà đoán tiếp qua external service/DB/event bus (SKILL.md Bước 2: gặp boundary phải ghi rõ, không đoán tiếp).
- 1 — có đủ ba mảnh nhưng một mảnh mỏng so với rủi ro: đường đi đứt một mắt giữa chừng, hoặc side effect nêu thiếu một I/O rõ ràng, hoặc boundary có nhắc nhưng không ghi rõ là boundary.
- 2 — trọn: ĐƯỜNG ĐI liền mạch A→B→C tới điểm ra hoặc boundary; ĐIỂM THAY ĐỔI QUAN TRỌNG liệt đủ (state: mọi write point); SIDE EFFECT liệt đủ hoặc ghi "không có"; boundary được đánh dấu rõ, dừng đúng chỗ.

## 2. TỔNG HỢP TRƯỚC — cấu trúc output đúng hợp đồng (A1)

SKILL.md Bước 3: tổng hợp là thứ người dùng đọc TRƯỚC, bằng chứng chi tiết (Bước 2) chỉ hiện khi được hỏi. Khối tổng hợp có ĐỐI TƯỢNG · LOẠI · ĐƯỜNG ĐI · ĐIỂM THAY ĐỔI · SIDE EFFECT · CHƯA RÕ/RỦI RO. Bước 1.7: trước khi vào code phải dựng tình huống đời thường + bảng ánh xạ.

- 0 — dump hết bằng chứng chi tiết ngay từ đầu không có khối tổng hợp lên trước (vi phạm Bước 3); HOẶC bỏ hẳn bước tình huống đời thường + bảng ánh xạ (vi phạm Bước 1.7, "không bỏ qua ngay cả khi người dùng có vẻ kỹ thuật").
- 1 — có tổng hợp lên trước nhưng thiếu một mục của khối (vd không có ĐƯỜNG ĐI một dòng, hoặc thiếu CHƯA RÕ/RỦI RO); hoặc có tình huống đời thường nhưng thiếu bảng ánh xạ đời thường→code.
- 2 — mở bằng tình huống đời thường + bảng ánh xạ; rồi khối tổng hợp đủ 6 mục; bằng chứng chi tiết chỉ để dành, kết bằng lời mời "muốn xem bằng chứng bước nào không".

## 3. BÁM CODE — không bịa path/hàm (xương sống · A2)

Mọi bước trace phải bám code thật. SKILL.md "Quy tắc": mỗi bước có evidence `file · dòng/symbol · điều xảy ra · độ chắc chắn`; tách quan sát khỏi suy luận, gắn nhãn khi suy; chỗ không rõ ghi "chưa rõ", không đoán mò. Nguồn hợp lệ = code gốc HOẶC flow artifact trong `.ai-understanding/` còn tươi (xác minh bằng file gốc khi cần). **Đây là gate nặng nhất của cả suite.**

- 0 — bịa: nhắc file/hàm/dòng/đường-truyền không có trong code; HOẶC suy đoán một mắt xích mà KHÔNG gắn nhãn (trộn suy luận vào quan sát); HOẶC gặp chỗ mờ mà đoán mò thay vì ghi "chưa rõ"; HOẶC dùng artifact `.ai-understanding/` đã stale (có `99_changes.md` pending ở phần liên quan) như sự thật mà không xác minh file gốc.
- 1 — chủ yếu bám code, một chỗ suy đoán/mơ hồ không gắn nhãn, hoặc một bước thiếu evidence `file · symbol`.
- 2 — mọi bước có evidence `file · dòng/symbol · điều xảy ra · độ chắc chắn`; quan sát tách rõ khỏi suy luận (suy luận có nhãn); chỗ chưa chắc ghi "chưa rõ"; artifact chỉ dùng khi còn tươi, dẫn xuất được về file gốc.

## 4. MỨC + LỜI VĂN — L5+ và đọc-được (xương sống · A3)

`trace` chạy ở mức L5 trở lên: người đọc kỹ thuật, được phép có tên file/hàm/symbol. Nhưng lời văn vẫn phẳng, câu ngắn, mỗi câu một ý (chuẩn `explain/rule/principles.md`) — điều tra không phải là cớ để dày đặc.

- 0 — sai mức hoặc khó đọc: hạ xuống dưới L5 (né hết tên symbol làm người kỹ thuật không lần được), HOẶC dày đặc — tường bullet nối dài, câu lồng nhiều mệnh đề, jargon không neo, làm mất mạch điều tra.
- 1 — đúng mức nhưng lời văn còn rườm ở vài chỗ, hoặc mức lệch nhẹ (chỗ quá thô chỗ quá sâu).
- 2 — đúng L5+: tên symbol/dòng dùng đúng chỗ để lần theo; lời văn phẳng, câu ngắn, mạch điều tra rõ; định dạng chỉ dùng khi giúp đọc.

## 5. ĐÁNH DẤU NỔI BẬT — state change & side effect không lẫn (A1/A3)

SKILL.md "Quy tắc": side effect và state change phải được đánh dấu nổi bật, không để lẫn vào mô tả thông thường (nhãn `[STATE CHANGE]` / `[SIDE EFFECT]` / `[TRANSFORM]` ở Bước 2).

- 0 — state change hoặc side effect bị chôn lẫn trong văn mô tả thường, không có nhãn/không nổi bật — người đọc lướt qua sẽ không thấy điểm nguy hiểm.
- 1 — có đánh dấu nhưng không nhất quán: một số điểm có nhãn, một số bị bỏ sót.
- 2 — mọi điểm state đổi và mọi side effect đều được đánh dấu nổi bật, tách khỏi mô tả thường; người đọc quét một lượt là thấy hết chỗ có tác động.

## 6. KHÔNG LẤN VAI — trace, không explain / review / triage (A4)

`trace` điều tra một thứ cụ thể. Nó KHÔNG kể tổng quan hệ thống (đó là `explain`), KHÔNG liệt kê gap/edge case còn thiếu (đó là `review`), KHÔNG phán giữ-sửa-xoá một file (đó là `triage`).

- 0 — lấn vai rõ: chuyển sang giải thích tổng quan app làm gì / vì sao tồn tại (explain); HOẶC liệt kê danh sách edge case / lỗ hổng còn thiếu như một bản rà soát (review); HOẶC ra phán quyết số phận file giữ/sửa/xoá (triage).
- 1 — chủ yếu đúng vai, lỡ lấn nhẹ một câu (vd chèn một nhận xét tổng quan hoặc một gợi ý sửa) không gắn cho skill khác.
- 2 — thuần trace: chỉ theo dấu đối tượng qua code, không tổng quan, không liệt gap, không phán file; nhận xét ngoài phạm vi (nếu có) được đẩy sang skill đúng dưới dạng gợi ý ở Bước 4.

## 7. KẾT — gợi ý bước tiếp đúng theo cái vừa tìm (A5)

SKILL.md Bước 4: sau tổng hợp, gợi ý theo đúng thứ vừa tìm — state change bất ngờ → tìm mọi chỗ ghi vào state; side effect ngoài ý → xem ảnh hưởng phần khác; có chỗ chưa rõ → đào sâu; trace sạch → gợi ý `review` edge case hoặc trace path khác. Nếu chưa có `.ai-understanding/`, gợi ý chạy `atlas` để lưu lại.

- 0 — không có gợi ý bước tiếp, HOẶC gợi ý sai (trỏ skill không liên quan / không khớp cái vừa tìm), HOẶC tự làm tiếp thay vì mời (vd tự nhảy sang review liệt gap).
- 1 — có gợi ý nhưng chung chung, không bám cái vừa tìm được (vd luôn nói "muốn xem gì nữa không" bất kể kết quả).
- 2 — gợi ý khớp phát hiện: đúng một trong các nhánh Bước 4 (tìm write point / xem ảnh hưởng / đào chỗ chưa rõ / `review` khi sạch); trỏ `review` hoặc trace path khác đúng lúc; nhắc `atlas` nếu chưa có artifact — chỉ mời, không tự làm.

## Gate

Tiêu chí **1 (Đúng+đủ đường đi · A1), 3 (Bám code · A2), 4 (Mức+lời văn · A3)** là xương sống. Bất kỳ cái nào = 0 → bản trace **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 12/14 nhưng bịa một mắt xích đường truyền (tiêu chí 3 = 0) vẫn rớt — vì người đọc sẽ tin nhầm data đi tới chỗ nó không tới. Gate quan trọng hơn tổng: khi so nhiều bản, loại hết bản rớt gate TRƯỚC, rồi mới xếp phần còn lại theo tổng.

## Khung report (xếp nhiều bản cạnh nhau)

```
CHẤM: trace · <project> · <đối tượng> · <loại: data/state/effect>
1 Đúng+đủ đường đi   [n] — <lý do 1 câu>
2 Tổng hợp trước     [n] — <...>
3 Bám code           [n] — <...>
4 Mức+lời văn        [n] — <...>
5 Đánh dấu nổi bật   [n] — <...>
6 Không lấn vai      [n] — <...>
7 Kết                [n] — <...>
TỔNG: <n>/14   ·   GATE: <đạt | rớt: tiêu chí ...>
SỬA TRƯỚC TIÊN: <một câu — đòn bẩy lớn nhất để bản này tốt hơn>
```

## Vì sao 7 tiêu chí này

Ba xương sống đo *bản trace có ra đúng thứ + trung thực + đọc được không*: đường đi đầy đủ (A1), bám code không bịa (A2), đúng mức L5+ và lời văn phẳng (A3) — đúng ba trục gate của meta-rubric. Bốn cái sau đo *có đúng kỷ luật điều tra của trace không*: cấu trúc tổng-hợp-trước (Bước 3) + tình huống đời thường (Bước 1.7); đánh dấu nổi bật state/side-effect; không lấn sang explain/review/triage; kết bằng gợi ý bám phát hiện. Mỗi tiêu chí truy được về một mục trong `trace/SKILL.md`, không có chuẩn mới. Thêm tiêu chí thứ 8 chỉ khi có một kiểu lỗi thật lặp lại mà 7 cái này không bắt được.
