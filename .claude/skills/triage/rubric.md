# Rubric — 6 tiêu chí chấm một bản `triage` (đọc một file, ra một verdict về số phận nó)

Mỗi tiêu chí 0/1/2. Khung chung: `grade/meta-rubric.md`. Chuẩn gốc để chấm: `triage/SKILL.md` (mục "Quy tắc bắt buộc" + "Reading order" + các gate xoá/sửa/logic + fix-now-vs-bàn-giao + khối output ═══ TRIAGE ═══/BÀN GIAO). Rubric chỉ biến hợp đồng đó thành thước đo được — KHÔNG thêm tiêu chuẩn mới.

**Đầu vào để chấm (fixture):** file được triage (đường dẫn thật) · project (để kiểm caller/callee thật + tồn tại state sibling) · level (`user-state.json.level`, chỉnh độ dài output) · state sibling nếu có (`agent-state.json` cho `do_not_touch`/slice active, `pipeline-state.json` cho scope) · output (nguyên văn khối ═══ TRIAGE ═══ / BÀN GIAO + mọi diff inline).

Tiêu chí **1 (Verdict đúng+đủ), 2 (Bám nguồn — không bịa caller), 3 (Đọc-được theo level)** là **xương sống (gate)**: rớt bất kỳ cái nào → rớt cả bản dù tổng cao.

## 1. VERDICT ĐÚNG + ĐỦ OUTPUT (xương sống — A1)

Phiên kết thúc bằng ĐÚNG MỘT verdict trong `{giữ | sửa nhỏ | chuyển | xoá | rewrite | archive | cần đọc thêm}`, kèm **một câu lý do** + **một câu rủi ro khi tác động**; verdict được suy ra từ engine chẩn đoán (Layer→…→Risk→DECISION) chứ không nhảy thẳng. Một file một khối ═══ TRIAGE ═══, không gộp.

- 0 — kết mở / không có verdict, HOẶC verdict ngoài 7 giá trị hợp lệ, HOẶC thiếu câu-lý-do hoặc câu-rủi-ro; HOẶC gộp nhiều file vào một khối; HOẶC phát verdict mạnh (xoá/rewrite/chuyển) khi khối chưa đi qua các field bắt buộc (Contract/Caller/Callee/State/Side-effect/Risk) — tức nhảy tới DECISION khi engine còn khuyết.
- 1 — có đúng một verdict hợp lệ kèm lý do + rủi ro, nhưng một field chẩn đoán còn sơ sài (Risk chung chung "có thể vỡ" không nói vỡ ở đâu; hoặc chọn dạng-đầy-đủ mà thiếu Core/Detail hay Scope-check).
- 2 — đúng một verdict hợp lệ; lý do + rủi ro mỗi thứ một câu cụ thể; đúng dạng khối (ngắn cho `giữ`, đầy đủ khi có dấu cần đổi) với đủ field theo Reading order; một file một khối.

## 2. BÁM NGUỒN — CALLER/CALLEE THẬT, KHÔNG BỊA (xương sống — A2)

Map caller/callee bằng grep read-only, gắn nhãn độ tin cậy (`chắc chắn | một phần | có thể sót | KHÔNG tìm thấy`); mọi claim về "còn dùng / không ai dùng / trong API / trong DB / slice cần" phải truy được về grep thật hoặc state sibling thật. Đây là gate nặng nhất của suite: bịa trạng thái file = 0.

- 0 — suy "0 grep hit ⇒ chết ⇒ xoá" (đúng luật cấm), HOẶC khẳng định "không ai gọi / còn dùng / có trong API-DB" mà không có grep/nguồn, HOẶC bịa caller/callee không tồn tại, HOẶC không gắn nhãn độ tin cậy cho caller khi verdict dựa vào nó, HOẶC báo đã đọc state (do_not_touch/slice) mà file/key đó không tồn tại.
- 1 — chủ yếu bám grep + state thật, nhưng một chỗ suy đoán độ tin cậy không gắn nhãn, hoặc lẫn một claim "còn/không còn dùng" chưa chỉ được nguồn.
- 2 — mọi caller/callee gắn đúng nhãn độ tin cậy; mọi claim API/DB/domain/slice truy được về grep hoặc state sibling thật; chỗ không xác minh được ghi rõ "không xác minh được", không ngụy tạo.

## 3. ĐỌC-ĐƯỢC THEO LEVEL (xương sống — A3)

Độ sâu + loại từ ngữ bám `user-state.json.level`: L0–L2 ngôn ngữ thường, ít tên file/hàm; L6–L8 gọn, kỹ thuật. Lời văn phẳng, câu ngắn, đúng đối tượng đọc là nắm được số phận file.

- 0 — sai mức rõ (L0–L2 mà đổ đầy tên hàm/tên file/jargon; hoặc L6–L8 mà dài dòng vòng vo), HOẶC dày đặc jargon không giải thích đến mức người đọc không hiểu verdict và vì sao.
- 1 — đọc được nhưng lệch mức nhẹ ở 1–2 chỗ, hoặc còn rườm.
- 2 — khớp level: đúng từ ngữ, đúng độ sâu; đọc xong nắm ngay file là gì + verdict + vì sao, không phải giải mã.

## 4. GATE TRƯỚC KHI ĐỤNG LOGIC / XOÁ — kỷ luật chẩn đoán (A4)

Không khuyến nghị sửa logic một method tới khi trả lời được: use case? ai gọi? gọi ai? input/output? đổi state nào? side effect? behavior nào đổi? — chưa đủ thì verdict = `cần đọc thêm`. Verdict `xoá` một biến/field chỉ khi qua hết gate xoá (set/read/consume ở đâu + KHÔNG trong public API + KHÔNG trong DB schema + KHÔNG thuộc domain core + slice active KHÔNG cần). Caller chưa rõ thì hạ verdict mạnh xuống `cần đọc thêm`.

- 0 — khuyên sửa logic method khi chưa trả lời đủ chuỗi câu hỏi; HOẶC verdict `xoá` field mà chưa qua đủ gate xoá (thiếu kiểm API/DB/domain/slice); HOẶC giữ verdict mạnh (xoá/rewrite) dù caller nhãn `một phần`/`KHÔNG tìm thấy` thay vì hạ xuống `cần đọc thêm`; HOẶC xoá vì "chưa hiểu" / giữ vì "biết đâu sau cần".
- 1 — qua gate nhưng nêu thiếu một mắt (vd kiểm được API/DB nhưng quên đối chiếu slice active, dù đáng lẽ có agent-state để kiểm).
- 2 — mọi verdict logic/xoá đều đóng đủ gate tương ứng trước khi phát; caller yếu → tự hạ xuống `cần đọc thêm` và nói rõ thiếu gì; dùng `cần đọc thêm` như verdict-an-toàn đúng chỗ thay vì đoán liều.

## 5. READ-ONLY + FIX-NOW ĐÚNG LẰN RANH + DO_NOT_TOUCH (A4 — luật cứng)

Read-only mặc định. Hành động inline DUY NHẤT được phép là fix nhỏ cô lập (typo · sai tên biến · thiếu return · điều kiện obvious · format · validation nhỏ · type sai rõ) VÀ file không trong `do_not_touch` VÀ không ngoài scope `partner`. Mọi thứ đụng business logic/state/API/DB/domain/boundary — và MỌI verdict xoá field/dead code — LUÔN bàn giao `frame`, không tự code. File ∈ `do_not_touch` chỉ được `giữ`/`cần đọc thêm`, không fix inline dù chỉ typo.

- 0 — tự sửa/rewrite code ngoài 7 case fix-now (đụng logic/contract/API/DB/domain mà vẫn code inline), HOẶC tự xoá field/dead code inline thay vì bàn giao, HOẶC fix inline trên file ∈ `do_not_touch` (hoặc ngoài scope `partner`), HOẶC ghi đè state sibling / `state/current.json`.
- 1 — giữ read-only đúng nhưng lằn ranh mờ: một "sửa nhỏ" thực ra chạm contract/logic mà không tự chuyển thành bàn giao, hoặc mô tả lại 4 phase của `frame` thay vì chỉ trỏ sang.
- 2 — chỉ inline khi rơi đúng fix-now + ngoài do_not_touch + trong scope; mọi thứ khác (kể cả xoá dead code) phát khối BÀN GIAO không tự code; file đóng băng thì `giữ` + ghi lý do; chỉ ghi `triage.json`/append `99_changes.md` đúng phạm vi cho phép.

## 6. KẾT — BÀN GIAO ĐÚNG SKILL + KHÔNG LẤN VAI (A5)

Verdict non-trivial (chuyển/xoá/rewrite/archive/sửa-không-nhỏ) kết bằng khối BÀN GIAO → `/frame` kèm khung slice (verdict/tầng/lý do/rủi ro/caller-callee đã map/KHÔNG-đụng), rồi một cổng xác nhận 3 lối (bàn giao/ghi nhận/xem explain) — không tự code thay. User muốn *hiểu* file để làm gì → trỏ `/explain`. Phạm vi rộng hơn một file (archive cả module) → trỏ `/partner`, không tự phán.

- 0 — verdict non-trivial mà không có khối bàn giao / tự nhảy vào code thay `frame`; HOẶC lấn vai: tự archive/rewrite cả module từ một file, giải thích nghiệp vụ dài như `explain`, hay đào data-flow sâu như `trace`; HOẶC user hỏi "hiểu file để làm gì" mà không trỏ `/explain`.
- 1 — có bàn giao nhưng thiếu một mảnh khung slice (thiếu KHÔNG-đụng, hoặc caller/callee đã map), hoặc tự chọn hộ lối thay vì mời cổng 3 lối, hoặc trỏ skill kế hơi lệch.
- 2 — khối BÀN GIAO đủ khung + cổng 3 lối để user quyết; trỏ `/frame` cho thi công, `/explain` khi user muốn hiểu, `/partner` khi phạm vi vượt một file; thuần vai chẩn đoán, không code, không lấn skill khác.

## Gate

Tiêu chí **1 (Verdict đúng+đủ output), 2 (Bám nguồn — không bịa caller), 3 (Đọc-được theo level)** là xương sống. Bất kỳ cái nào = 0 → bản **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 10/12 nhưng suy "0 grep hit ⇒ xoá" (tiêu chí 2 = 0) vẫn rớt — vì sẽ xoá nhầm file còn sống. Khi so nhiều bản: loại hết bản rớt gate TRƯỚC, rồi mới xếp phần còn lại theo tổng.

## Khung report (xếp nhiều bản cạnh nhau)

```
CHẤM: triage · <file> · <project> · <level>
1 Verdict đúng+đủ    [n/2] — <lý do 1 câu>
2 Bám nguồn caller   [n/2] — <...>
3 Đọc-được theo level[n/2] — <...>
4 Gate logic/xoá     [n/2] — <...>
5 Read-only+fix-now  [n/2] — <...>
6 Bàn giao+không lấn [n/2] — <...>
TỔNG: <n>/12   ·   GATE: đạt / RỚT ở <tiêu chí ...>
SỬA TRƯỚC TIÊN: <một câu — đòn bẩy lớn nhất để bản này tốt hơn>
```

## Vì sao các tiêu chí này

Ba xương sống đo *có ra đúng một verdict đọc được + trung thực không*: verdict đúng+đủ (A1), caller/callee bám grep thật không bịa (A2 — gate nặng nhất vì lỗi hay gặp là "0 hit ⇒ xoá"), đọc-được theo level (A3). Ba cái sau đo *có đúng kỷ luật của triage không*: gate logic/xoá chặn phán liều (A4), read-only + fix-now đúng lằn ranh + tôn trọng do_not_touch (A4, gấp các luật cứng của SKILL), và kết bằng bàn giao đúng skill không lấn vai (A5). Gộp lại = trọn hợp đồng của `triage`, không hơn. Sáu tiêu chí (không phải bảy như skill pipeline) vì triage không sinh artifact nhiều-phần và không có cổng ký GO/NO-GO — nén "đủ-là-đủ" và "kỷ luật read-only" vào tiêu chí 4–5, "bàn giao" và "không lấn vai" vào tiêu chí 6. Thêm tiêu chí thứ 7 chỉ khi có một kiểu lỗi thật lặp lại mà sáu cái này không bắt được.
