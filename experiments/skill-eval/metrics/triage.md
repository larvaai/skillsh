<!-- Rubric chấm OUTPUT một phiên triage: có đúng một verdict hợp lệ + lý do + rủi ro, đi đủ reading-order, trung thực caller/callee, read-only & bàn giao đúng, và qua gate trước verdict mạnh. | gate: Tiêu chí 1 (VERDICT) — phải =2: kết bằng ĐÚNG MỘT verdict trong {giữ|sửa nhỏ|chuyển|xoá|rewrite|archive|cần đọc thêm} + đúng một câu lý do + đúng một câu rủi ro; thiếu bất kỳ mảnh nào, hoặc verdict mở/kép, hoặc verdict ngoài tập → 0 và rớt gate., Tiêu chí 3 (TRUNG THỰC CALLER) — phải ≥1: caller gắn nhãn độ tin cậy grep và KHÔNG suy 'grep 0 hit ⇒ chết ⇒ xoá'; suy vậy, hoặc khẳng định 'không ai gọi' từ grep rỗng → 0 và rớt gate., Tiêu chí 5 (GATE-TRƯỚC-VERDICT-MẠNH) — phải ≥1: mọi verdict xoá/rewrite/archive đều đã qua gate tương ứng (caller chắc chắn + API/DB/domain/live-slice đều KHÔNG với xoá; boundary sai rõ với rewrite; model sai gốc + phạm vi 1 file với archive); verdict mạnh mà caller còn yếu hoặc gate chưa trả lời → 0 và rớt gate. -->


# Rubric — 5 tiêu chí chấm một OUTPUT triage

Mỗi tiêu chí 0/1/2. Chuẩn gốc: `triage/SKILL.md` (quy tắc bắt buộc + reading-order + gate xoá + fix-now/bàn-giao). Rubric chỉ biến hợp đồng đó thành thước — không thêm tiêu chuẩn mới. Chấm cái khối `═══ TRIAGE ═══` / `═══ BÀN GIAO ═══` mà skill phát ra.

## 1. VERDICT — đúng một kết, đủ lý do + rủi ro (xương sống)

Phiên phải khép bằng ĐÚNG MỘT verdict trong `{giữ | sửa nhỏ | chuyển | xoá | rewrite | archive | cần đọc thêm}`, kèm **một câu lý do** + **một câu rủi ro khi hành động**. Không để "kết quả mở", không hai verdict.

- 0 — không có verdict, hoặc verdict mở/lửng, hoặc kết hai-ba verdict cùng lúc, hoặc verdict ngoài tập 7, hoặc thiếu câu lý do, hoặc thiếu câu rủi ro. (Dạng-ngắn `giữ` được miễn dòng rủi ro riêng — vẫn phải có verdict + lý do.)
- 1 — đúng một verdict trong tập + có lý do + có rủi ro, nhưng một mảnh yếu: lý do sáo/không gắn với file, hoặc rủi ro chung chung ("có thể ảnh hưởng") không nói cái gì vỡ.
- 2 — đúng một verdict hợp lệ; lý do một câu bám đúng file này; rủi ro một câu cụ thể (chỉ ra API/DB/UI/live-slice/caller nào vỡ). Nhiều file → mỗi file một khối riêng, không gộp.

## 2. READING-ORDER — đi đủ engine chẩn đoán

Dạng đầy đủ phải đi hết thứ tự field: Layer → Responsibility → Contract → Caller → Callee → State → SideEffect → (Core/Detail) → Risk → Decision. Thiếu field là chưa được nhảy tới DECISION. (Dạng-ngắn `giữ` chỉ hợp lệ khi rõ giữ: đúng tầng, không mùi sai, không dấu chết/dup — khi đó Layer + Responsibility + verdict là đủ.)

- 0 — nhảy thẳng tới verdict thiếu nhiều field xương sống (thiếu Layer/Responsibility/Caller/Risk), hoặc dùng dạng-ngắn cho ca có mùi sai tầng / nghi chết / user hỏi xoá-sửa-viết-lại (phải chạy engine đầy đủ mà lại tắt).
- 1 — đi gần đủ, sót 1 field phụ (vd thiếu Side effect hoặc Core/Detail) nhưng vẫn có Layer + Responsibility + Contract + Caller + Risk.
- 2 — đi đủ thứ tự field cho đúng dạng đã chọn; Layer có nêu tầng (+ cờ ⚠ SAI TẦNG nếu có); mỗi field trả lời thật, không để trống lấy lệ.

## 3. TRUNG THỰC CALLER/CALLEE — nhận độ tin cậy grep (xương sống)

Caller map bằng grep read-only, gắn nhãn `chắc chắn | một phần | có thể sót | KHÔNG tìm thấy`. Callee đọc trong file. TUYỆT ĐỐI không suy "0 grep hit ⇒ chết ⇒ xoá"; caller chưa rõ → phải hạ verdict mạnh xuống `cần đọc thêm`.

- 0 — suy "0 hit = chết = xoá/rewrite", hoặc khẳng định "không ai gọi / dead" từ một grep rỗng, hoặc caller không gắn nhãn độ tin cậy khi ra verdict mạnh.
- 1 — có map caller + có nhãn, nhưng nhãn lỏng: bỏ qua các đường dễ sót (re-export, DI, dynamic import, route string, reflection) mà không cân nhắc, hoặc callee nêu qua loa.
- 2 — caller có nhãn đúng độ tin cậy, có cân nhắc đường dễ sót khi nhãn `có thể sót`; callee đọc từ trong file (tin cậy cao) + soi dependency sai tầng; grep rỗng chỉ kết luận "chưa thấy caller", không kết luận "chết".

## 4. READ-ONLY + BÀN GIAO đúng cách

Mặc định read-only: triage chẩn đoán, KHÔNG tự rewrite domain/contract/API/DB. Inline chỉ cho fix-now cô lập (typo/tên biến/thiếu return/điều kiện obvious/format/validation nhỏ/type sai rõ) và chỉ khi file ∉ `do_not_touch` + trong scope. Mọi thứ khác (chuyển/xoá/rewrite/archive/sửa-không-nhỏ) → phát khối BÀN GIAO → `/frame`, không tự code, không mô tả lại 4 phase của frame. `do_not_touch` → chỉ được `giữ`/`cần đọc thêm`, không fix dù là typo.

- 0 — tự code/rewrite/xoá inline thứ ngoài fix-now (đụng business logic/contract/API/DB/domain/boundary), hoặc fix inline file trong `do_not_touch`, hoặc tự xoá field/dead-code inline (luôn phải bàn giao), hoặc mô tả lại phase của frame thay vì trỏ sang.
- 1 — đúng hướng read-only nhưng lệch nhẹ: bàn giao đúng nhưng khối BÀN GIAO thiếu mảnh (thiếu KHÔNG-đụng/caller đã map), hoặc gọi một fix "nhỏ" mà thật ra chạm nhẹ contract nhưng chưa tự nâng thành bàn giao.
- 2 — verdict mạnh → phát khối BÀN GIAO đủ (verdict/tầng/lý do/rủi ro/caller-callee đã map/KHÔNG-đụng) + trỏ `/frame`, không code thay; fix-now chỉ khi đúng 7 case cô lập + ngoài `do_not_touch` + trong scope; state chỉ ghi `triage.json` append khi user chọn, không ghi đè sibling.

## 5. GATE-TRƯỚC-VERDICT-MẠNH — không xoá/rewrite/archive khi chưa đủ căn cứ (xương sống)

Verdict mạnh phải qua gate tương ứng trước khi phát:
- `xoá` field/biến: trả lời cả hai chiều set-ở-đâu / read-ở-đâu / ai-consume, và **API? DB schema? domain core? live-slice active cần?** — chỉ xoá khi tất cả là KHÔNG; caller phải `chắc chắn`.
- đụng logic một method: trả được use case? ai gọi? gọi ai? input/output? đổi state? side effect? behavior nào đổi? — chưa đủ → `cần đọc thêm`.
- `rewrite`: chứng minh boundary/logic sai tầng rõ (không chỉ code xấu — code xấu + model đúng là refactor).
- `archive`: model sai gốc + phạm vi đúng một file (module rộng hơn → trỏ `/partner`).

- 0 — ra verdict mạnh (xoá/rewrite/archive) khi caller còn yếu/`có thể sót`, hoặc gate xoá chưa trả lời hết API/DB/domain/live-slice, hoặc đụng logic method mà chưa trả đủ 7 câu, hoặc archive cả module chỉ từ một file xấu.
- 1 — có ý thức gate: trả lời phần lớn câu gate nhưng sót một nhánh (vd quên soi DB schema, hoặc quên đọc live-slice trong `agent-state.json`) nhưng verdict vẫn có căn cứ chính.
- 2 — mỗi verdict mạnh đều truy hết gate của nó trước khi phát; caller `chắc chắn` cho xoá; thiếu bất kỳ căn cứ nào thì tự hạ xuống `cần đọc thêm` và nêu rõ thiếu gì. Level user (L0–L8) chỉ đổi độ dài, KHÔNG nới gate.

## Gate (tiêu chí xương sống)

Tiêu chí **1, 3, 5** là xương sống.
- **1 = 0** (thiếu/mở/kép verdict, hoặc thiếu lý do/rủi ro) → rớt gate.
- **3 = 0** (suy "0 hit = chết", khẳng định dead từ grep rỗng) → rớt gate.
- **5 = 0** (verdict mạnh chưa qua gate / caller yếu) → rớt gate.

Bất kỳ cái nào = 0 → OUTPUT **rớt gate**, ghi rõ rớt ở đâu dù TỔNG cao. Gate quan trọng hơn tổng: khi so nhiều bản, loại hết bản rớt gate trước rồi mới xếp theo tổng. Lý do: triage sai ở ba chỗ này gây hành động phá code thật (xoá nhầm, sửa nhầm, bàn giao sai) — nguy hiểm hơn một bản đọc thiếu field.

## Vì sao 5 tiêu chí này

Hai cái đầu đo *phiên có ra đúng hình dạng hợp đồng không* (một verdict đủ lý-do-rủi-ro; đi đủ reading-order). Ba cái sau đo *có trung thực & an toàn không* (không bịa caller, không tự code, không xoá liều). Gộp lại = toàn bộ quy tắc bắt buộc của triage, không hơn. Thêm tiêu chí thứ 6 chỉ khi có kiểu lỗi thật lặp lại mà 5 cái này không bắt được.
