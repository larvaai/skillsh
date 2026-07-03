# Rubric — explain: 8 tiêu chí chấm artifact giải thích (V2 ĐỀ XUẤT)

> **Trạng thái: v2 đề xuất, CHƯA thay thế `.claude/skills/grade/rubric.md` chính thức.**
> Lý do tồn tại: thước v1 (7 tiêu chí ×0/1/2 = 14) đã **bão hoà** — vòng tune 2026-07-01 (`experiments/runs/20260701-143138/RESULT.md`) cho nhiều bản cùng 14/14 không phân biệt được, và lộ 4 mâu thuẫn rubric↔skill. V2 dùng thang **0–3, 8 tiêu chí, tổng 24** để tách được nhóm dẫn đầu, và gỡ đủ 4 mâu thuẫn (bảng ở cuối file). Khi cần so ngang với các rubric khác trong bộ (thang 14), quy về **%** (điểm/24).

Mỗi tiêu chí 0/1/2/3. Chuẩn gốc: `.claude/skills/explain/SKILL.md` (Luật neo · thang zoom · bảng mức · ba chế độ · tự soi) và `rule/principles.md` (cách nói). Rubric chỉ biến hợp đồng đó thành thước đo được — không thêm tiêu chuẩn mới.

Chuẩn đối chiếu khi artifact có claim:
- **Claim về code** (file, symbol, hành vi, thứ tự, con số đo trên code) → **code gốc `/Users/uspro/Desktop/namnson/hex_agent`**, không phải chính artifact, không phải tài liệu trung gian.
- **Claim về thiết kế rebuild** (invariant, quyết định, gap) → artifact thượng nguồn trong gói (`00-understanding/ATLAS.md`, `REBUILD-BRIEF.md`, `review/REVIEW.md`) — và artifact phải khai báo mình đang dựa nguồn thứ cấp nào.

**Cách chấm (bắt buộc, theo thứ tự):**
1. Đọc THÂN bài trước, **chưa đọc mục tự soi** (nếu có) — chấm tiêu chí 4–8 theo những gì quan sát được, không theo nhãn artifact tự dán.
2. Lập **bảng kiểm thuật ngữ**: liệt kê MỌI tên code nội bộ + MỌI tên công nghệ ngoài xuất hiện trong thân bài, ghi vị trí xuất hiện đầu tiên và vị trí neo (nếu có) → chấm tiêu chí 2.
3. Spot-check **≥3 claim về code** trên code gốc, ưu tiên loại claim vòng trước hay sai: thứ tự hành vi bên trong chokepoint, vị trí guard (graph node hay middleware), trạng thái wire thật của middleware → chấm tiêu chí 1.
4. Cuối cùng mới đọc mục tự soi và đối chiếu từng dòng tự-khẳng-định với kết quả bước 1–3 — tự soi ghi ĐẠT mà người chấm chứng minh ngược lại → tiêu chí 1 = 0 (tự khen khống).

## 1. BÁM BẰNG CHỨNG — không bịa, không tự khen (xương sống)

Hợp đồng: explain "đọc code khi cần", chỗ chưa chắc phải gắn nhãn; artifact này còn tự tuyên bố "chỉ khẳng định điều evidence chống lưng" — tuyên bố đó cũng là claim phải kiểm.

- 0 — có ít nhất MỘT trong các lỗi sau: (a) claim bịa — file/symbol/API/hành vi không tồn tại trong code gốc, hoặc claim về thiết kế không có trong nguồn thượng nguồn đã khai; (b) claim sai bản chất — thứ tự/vị trí/cơ chế nói ngược code thật (vd nói scope-check chạy trước trong khi code gốc là deepcopy → publish → scope-check); (c) con số gánh kết luận ("N gap", "0 rò state", "N bước") không có nguồn kiểm được; (d) mục tự soi/tự đánh giá khẳng định ĐẠT một điều người chấm chứng minh là sai. Một cái là đủ → 0.
- 1 — spot-check không thấy bịa, nhưng có ≥2 chỗ suy đoán/khái quát trình bày như fact không nhãn không nguồn ("mọi X đều…", "không bao giờ Y…" mà không chỉ nơi kiểm), hoặc không khai báo đang dựa nguồn thứ cấp nào.
- 2 — mọi claim spot-check đều khớp; nguồn thứ cấp có khai báo; còn đúng 1 chỗ mơ hồ/suy đoán không nhãn.
- 3 — mọi claim truy được về nguồn: claim code khớp code gốc cả về **thứ tự và vị trí** (không chỉ "có tồn tại"); claim thiết kế chỉ đúng artifact thượng nguồn; chỗ chưa chắc gắn nhãn rõ; mọi con số có chỗ kiểm.

## 2. NEO — vấn đề trước, không thuật ngữ mồ côi, kể cả tên công nghệ ngoài (xương sống)

Luật neo là "luật cứng, đứng trên mọi mức và mọi chế độ" của hợp đồng: neo trước – tên sau; bản đồ "bạn ở đây" trước mọi chi tiết; jargon chỉ sống ở tầng nó được neo. "Thuật ngữ" trong hợp đồng là MỌI thuật ngữ — vòng tune #2 cho thấy lỗ hổng thật nằm ở **tên công nghệ ngoài thả trần** (`LangGraph`, `SQLite`, `Qdrant`, `JSON`, `CLI`…), không chỉ tên code nội bộ.

- 0 — mở đầu phần kể bằng thuật ngữ kiến trúc hoặc tên code ("hexagonal", "chokepoint", `AgentKernel`…) trước khi nói VẤN ĐỀ gì + CHO AI; HOẶC ≥1 tên code nội bộ được gọi trước khi neo (câu trước nó chưa nói: nằm bước nào trong luồng + ngăn vấn đề gì); HOẶC không có bản đồ luồng một-cái-liếc để thuật ngữ trỏ về.
- 1 — tên nội bộ neo đủ, nhưng ≥2 tên công nghệ ngoài thả trần ở vùng business phải đọc (Zoom 0–2) không kèm cụm đời thường; hoặc jargon rò xuống tầng zoom thấp hơn tầng nó được neo ở ≥2 chỗ.
- 2 — tên nội bộ neo đủ; tên ngoài chỉ 1 chỗ trần hoặc rò tầng 1 chỗ; phần còn lại có gloss đời thường.
- 3 — bảng kiểm thuật ngữ (bước 2 cách chấm) sạch tuyệt đối: mọi tên — nội bộ lẫn công nghệ ngoài — chỉ xuất hiện SAU khi có chỗ đứng (vị trí trong luồng + lợi ích/vấn đề nó ngăn); tên ngoài luôn kèm cụm đời thường ("một sổ ghi bền — SQLite") hoặc được giấu ở tầng thấp; không tầng nào bị rò jargon từ tầng trên.

## 3. BA KHÁN GIẢ — CTO/business/dev đều dùng được thật (xương sống)

Hợp đồng: người nghe là đội khách hàng trộn CTO + business + dev, "Không bỏ rơi ai" — business thấy giá trị, CTO thấy hình hài, dev thấy đường vào code; giá trị business lặp lại ở MỖI tầng zoom (Luật neo #3). "Dùng được thật" = đọc xong, mỗi vai biết mình vừa hiểu gì và làm gì tiếp, không phải mở lại nguồn.

- 0 — ≥1 vai trắng tay: không có câu chuyện giá trị (vấn đề + cho ai + vì sao đáng) cho business; không có hình hài một-cái-liếc (luồng + ranh giới phần) cho CTO; hoặc không có đường vào code (phần nào của luồng nằm ở module/thư mục nào) cho dev. HOẶC có tầng zoom thuần kỹ thuật — không trả lời được "để làm gì cho ai".
- 1 — cả ba vai có mặt nhưng ≥1 vai chỉ được chiếu lệ: đường vào code chỉ là danh sách thư mục không map về bước trong luồng; hoặc giá trị business nói một lần ở đầu rồi rơi mất ở các tầng sau.
- 2 — cả ba vai được phục vụ, giá trị lặp ở hầu hết tầng; hụt nhẹ 1 chỗ (một tầng quên nhắc giá trị, hoặc dev thiếu "đọc tiếp ở đâu").
- 3 — mỗi tầng zoom đều trả lời "để làm gì cho ai"; dev có đường vào cụ thể (module → bước trong luồng → đọc gì tiếp); CTO thấy hình hài + ranh giới + cái gì đối trọng cái gì; business theo được từ câu đầu tới câu cuối; người nhận cầm artifact là hành động được ngay (biết hỏi gì tiếp, mở file nào tiếp).

## 4. MỨC — đúng độ sâu, tách TRÍCH DẪN khỏi GỌI TÊN ĐÃ NEO

Gỡ mâu thuẫn v1 #1. Hai luật tách bạch: (a) **trích dẫn code** — số dòng, chữ ký hàm, khối code, tên biến nội bộ — chỉ từ **L4** trở lên; (b) **gọi tên module/entrypoint ĐÃ NEO** — được phép từ **L2**, và là yêu cầu ở L3 (bảng mức: L3 dừng ở Zoom 2 kỹ + chạm Zoom 3, trách nhiệm từng phần). Tên CHƯA neo không chấm ở đây — đó là lỗi tiêu chí 2, không phạt kép.

- 0 — trích dẫn code (số dòng/chữ ký/khối code) khi level < L4; HOẶC độ sâu lệch ≥2 tầng zoom so với bảng mức (vd L3 mà dừng ở Zoom 1, hoặc L1 mà đổ Zoom 3).
- 1 — đúng tầng dừng nhưng độ kỹ sai ở nhiều đoạn: L3 mà sa vào cơ chế bên trong thuộc L4+ (chi tiết cài đặt, tham số hàm), hoặc chạm Zoom 3 quá mỏng (điểm danh module mà không nói trách nhiệm + ranh giới).
- 2 — đúng tầng dừng, đúng luật gọi-tên-vs-trích-dẫn, lệch nhẹ 1–2 chỗ.
- 3 — khớp trọn hành vi mức trong bảng SKILL (với L3: Zoom 2 kỹ, mỗi bước đời thường; chạm Zoom 3 với trách nhiệm từng phần); không đoạn nào quá nông hay quá sâu; ranh giới gọi-tên/trích-dẫn sạch tuyệt đối toàn bài.

## 5. CHẾ ĐỘ & VAI — chấm theo cấu trúc quan sát được, không theo nhãn

Gỡ mâu thuẫn v1 #2: **nhãn mode artifact tự dán (ở tiêu đề/header/câu mở) KHÔNG được dùng làm bằng chứng** — người chấm suy chế độ từ cấu trúc thân bài. Nhãn đúng không cứu bài sai cấu trúc; nhãn sai không đánh rớt bài đúng cấu trúc. Tiêu chí này cũng giữ RANH GIỚI vai explain (dạy hiểu theo mức — không làm việc atlas/trace/review/triage).

- 0 — cấu trúc sai chế độ: cần overview mà đổ một cục chi tiết không theo thang zoom / chi tiết đứng trước bản đồ; nhảy cóc tầng zoom; HOẶC lấn hẳn vai skill khác (liệt kê gap/edge case như `review`, đào side-effect từng dòng như `trace`, phán giữ/sửa/xoá như `triage`, dựng bản đồ evidence cho hệ thống như `atlas`).
- 1 — đúng chế độ nhưng vỡ kỷ luật ở ≥1 chỗ: ba nhịp LÀM GÌ/CHO AI/VÌ SAO dán thành khối liệt kê trên đầu thay vì dệt vào lời kể (hợp đồng cấm rõ); Zoom 1 có nhiều hơn MỘT ý tưởng cốt lõi; hoặc lấn vai nhẹ vài đoạn.
- 2 — cấu trúc chuẩn chế độ, kỷ luật giữ được, sai lệch đúng 1 chỗ nhỏ.
- 3 — người chấm che nhãn đi vẫn gọi đúng tên chế độ chỉ từ cấu trúc: Zoom 0–1 không tên code, đúng một ý cốt lõi; Zoom 2 là câu chuyện 5–8 bước đánh số; Zoom 3 mỗi module trỏ về một bước; thuần vai explain từ đầu đến cuối, việc vượt vai chỉ xuất hiện dưới dạng con trỏ sang skill/artifact khác.

## 6. NHẤT QUÁN NỘI TẠI — claim tuyệt đối phải có phạm vi

Tiêu chí MỚI, gỡ mâu thuẫn v1 #3 ("cửa DUY NHẤT" vs thực tế 2 chokepoint tool/delegation). Lỗi này lặp qua nhiều bản nên đủ điều kiện "kiểu lỗi thật mà thước cũ không bắt được".

- 0 — ≥1 cặp phát biểu mâu thuẫn trực tiếp không được hoà giải trong bài (vd "MỌI hành động ra ngoài đi qua đúng MỘT cửa" rồi vài đoạn sau "giao-việc đi một cửa RIÊNG" mà câu đầu không hề giới hạn phạm vi); hoặc con số/danh mục lệch nhau giữa các mục của cùng artifact.
- 1 — không mâu thuẫn trực tiếp, nhưng ≥2 claim tuyệt đối ("duy nhất", "mọi", "không bao giờ", "0 …") không được scope trong khi chính bài có ngoại lệ ở chỗ khác — người đọc phải tự hoà giải.
- 2 — các claim tuyệt đối đều có phạm vi, còn đúng 1 chỗ mơ hồ nhỏ (scope nói muộn, ở đoạn khác).
- 3 — mọi claim tuyệt đối được scope NGAY TẠI CHỖ phát biểu ("một cửa cho mọi lệnh gọi-tool; giao-việc cố tình đi cửa tách riêng — và vì sao tách"); ngoại lệ được gọi tên là ngoại lệ kèm lý do; số liệu/danh mục nhất quán xuyên suốt, kể cả giữa thân bài và mục tự soi.

## 7. LỜI VĂN — câu ngắn phẳng; bullet chỉ ở vùng được phép

Gỡ mâu thuẫn v1 #4 bằng hoà giải E3 — định nghĩa rõ **vùng định dạng được phép**: (a) danh sách ĐÁNH SỐ cho bản đồ luồng Zoom 2 (hợp đồng yêu cầu "5–8 bước, đánh số"); (b) bullet cho điểm danh module ở tầng zoom cuối. Ngoài hai vùng đó, tường bullet bị phạt như v1.

- 0 — tường bullet / cấu trúc lồng nhiều tầng NGOÀI vùng được phép; câu dài chồng mệnh đề dày đặc kiểu học thuật; trích số dòng làm trang trí; đọc mệt dù nội dung đúng.
- 1 — đọc được nhưng rườm: câu dài nối gạch-ngang lặp thành tật; định dạng thừa (đậm/ngoặc/nháy chồng nhau); hoặc meta chen vào THÂN bài kể ("theo Luật neo…", "ở chế độ overview…" giữa câu chuyện — header/metadata của file KHÔNG tính là thân bài).
- 2 — câu ngắn phẳng phần lớn, định dạng đúng vùng, còn 1–2 chỗ rườm.
- 3 — câu ngắn, phẳng, đơn giản hoá HÌNH THỨC chứ không cắt nội dung; đánh số/bullet chỉ đúng hai vùng được phép và thật sự giúp đọc; không meta trong thân bài; business đọc trơn không vấp.

## 8. KẾT — bước tiếp đúng mức, mở đúng cánh cửa

Hợp đồng: sau khi giải thích, đưa gợi ý theo bảng mức; L5–L8 trả ngắn rồi hand off đúng sibling (`trace`/`review`/`frame`/`partner`).

- 0 — không có gợi ý bước tiếp; hoặc gợi ý sai mức/sai skill (vd L3 mà đẩy sang `partner`, hoặc hand off khi level < L5 thay vì gợi ý đào sâu).
- 1 — có gợi ý nhưng chung chung ("muốn biết thêm cứ hỏi") hoặc lệch nhẹ so với hành vi mức trong bảng.
- 2 — gợi ý đúng tinh thần mức (vd L3: mời đi sâu trách nhiệm module để lên L4, hoặc chọn một luồng cụ thể xem chế độ flow); nếu trỏ sibling thì trỏ đúng.
- 3 — gợi ý đúng mức VÀ mở lựa chọn thật: ≥2 hướng cụ thể nêu đích danh (luồng nào, module nào), mỗi hướng nói rõ đi bằng chế độ/skill nào, và nối thẳng vào điều bài vừa dạy — người đọc chỉ việc chọn.

## Luật gate

Tiêu chí **1, 2, 3** là xương sống. Bất kỳ cái nào = 0 → artifact **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 21/24 nhưng bịa hành vi code (tiêu chí 1 = 0) vẫn rớt — vì explain là artifact người ta ĐỌC ĐỂ TIN: CTO quyết dựa trên nó, dev mở code theo nó, một claim bịa lan thành quyết định sai ở stage sau. Gate quan trọng hơn tổng: khi so nhiều bản, loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Vì sao 8 tiêu chí này

Ba tiêu chí gate đo ba lời hứa sống còn: **bám bằng chứng thật** (1 — không bịa, không tự khen; mọi con số và claim kiểm được trên code gốc hoặc nguồn thượng nguồn đã khai), **Luật neo** (2 — luật cứng duy nhất mà hợp đồng tự tuyên bố "đứng trên mọi mức và mọi chế độ; vi phạm là lỗi"), **ba khán giả dùng được thật** (3 — "Không bỏ rơi ai" là định nghĩa người nhận của explain; một explain mà business rớt hoặc dev không có đường vào code thì viết hay đến đâu cũng vô dụng). Năm tiêu chí còn lại đo phần kỷ luật: đúng mức (4), đúng chế độ + đúng vai (5), không tự mâu thuẫn (6), lời văn đúng gu (7), kết mở đúng cửa (8).

So với v1: tiêu chí 6 là tiêu chí MỚI duy nhất — thêm vì kiểu lỗi "cửa duy nhất vs 2 chokepoint" đã lặp qua nhiều bản mà 7 tiêu chí cũ không bắt được (đúng điều kiện v1 tự đặt cho việc thêm tiêu chí thứ 8). Bốn mâu thuẫn rubric↔skill của vòng 2026-07-01 được gỡ tại: #1 → tiêu chí 4 (tách trích-dẫn/gọi-tên-đã-neo), #2 → tiêu chí 5 (chấm cấu trúc, không chấm nhãn), #3 → tiêu chí 6 (consistency), #4 → tiêu chí 7 (vùng định dạng được phép). Thang 0–3 thay 0/1/2 để mức 3 giữ chỗ cho "sạch tuyệt đối" — trần đủ cao để các bản 14/14 cũ phân hoá được. Thêm tiêu chí thứ 9 chỉ khi có một kiểu lỗi thật lặp lại mà 8 cái này không bắt được.
