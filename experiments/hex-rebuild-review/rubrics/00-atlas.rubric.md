# Rubric — 00-atlas: 7 tiêu chí chấm bản đồ hiểu biết nền

Mỗi tiêu chí 0/1/2, tổng tối đa 14. Chuẩn gốc: `.claude/skills/atlas/SKILL.md` (mục tiêu · luật cứng · bước full build). Rubric chỉ biến hợp đồng đó thành thước đo được — không thêm tiêu chuẩn mới.

Khi artifact có claim về code (file, dòng, symbol, hành vi, con số), **chuẩn đối chiếu là code gốc `/Users/uspro/Desktop/namnson/hex_agent`** — không phải chính artifact, không phải tài liệu trung gian.

Cách chấm: đọc artifact một lượt, chấm tiêu chí 4–7 (hình dạng, kỷ luật) trước; rồi spot-check tiêu chí 1–3 trên code gốc — mỗi lần chấm chọn **ít nhất 5 anchor `file:line` ngẫu nhiên** để đối chiếu và **đi lại ít nhất 1 luồng trace** từ đầu đến cuối.

## 1. BẰNG CHỨNG — mọi claim kiểm được, không bịa, không tự khen (xương sống)

Luật cứng: *"Không claim nào thiếu evidence"* + *"Trung thực về độ hiểu"*. Mọi nhận định kèm file path · symbol · dòng/đoạn · suy luận · độ chắc chắn.

- 0 — có ít nhất một claim bịa: file/symbol/dòng/hành vi không tồn tại hoặc sai bản chất khi đối chiếu code gốc; hoặc con số/danh mục (số test, số event, số field…) không có nguồn kiểm được; hoặc scorecard/mức-hiểu tự chấm cao hơn bằng chứng chống lưng (tự nhận L4/L5 mà không chỉ ra bằng chứng tương xứng). Một claim bịa là đủ → 0.
- 1 — mọi claim có nguồn và spot-check khớp, nhưng còn 1–2 chỗ suy đoán/khái quát trình bày như fact không kèm anchor hoặc độ chắc (vd "mọi tool đều…", "khoảng ~N event" mà không chỉ nơi kiểm).
- 2 — mọi nhận định có nguồn đúng format hợp đồng (path · symbol · dòng · suy luận · độ chắc); dùng nguồn thứ cấp (evidence file, brief) thì khai báo rõ là thứ cấp và hạ độ chắc tương ứng; chỗ chưa đủ căn cứ nằm ở mục risks/unknowns chứ không đội lốt fact; ≥5 anchor spot-check đều khớp code gốc.

## 2. TRACE — chứng minh hiểu bằng ≥4 luồng thật (xương sống)

Hợp đồng: hiểu = *"một hành vi thật đi từ đâu đến đâu trong code"*; full build bắt buộc trace tối thiểu 4 flow: ≥1 happy path · 1 failure path · 1 side-effect path · 1 permission/security path.

- 0 — thiếu bất kỳ loại nào trong 4 loại luồng; hoặc cái gọi là "trace" chỉ là danh sách module/mô tả tĩnh, không đi bước-theo-bước từ điểm vào đến kết cục; hoặc người chấm đi lại một luồng trên code gốc thì thấy sai mắt xích bản chất (bước không tồn tại, thứ tự sai).
- 1 — đủ 4 loại và đi theo bước, nhưng có luồng đứt mắt xích: bước nhảy không anchor, hoặc không chỉ rõ tại bước nào state đổi / side effect bắn ra / ranh giới an toàn được kiểm.
- 2 — ≥4 luồng đủ 4 loại; mỗi luồng đi từ điểm vào đến kết cục, từng bước có anchor code và gọi tên được chỗ đổi state, chỗ gây side effect, chỗ qua ranh giới (gate / chokepoint / permission); luồng người chấm đi lại trên code gốc khớp hoàn toàn.

## 3. DÙNG ĐƯỢC THẬT — người nhận cầm đi làm ngay, khỏi quét lại (xương sống)

Hợp đồng: atlas là NỀN để explain/frame/triage/partner (và stage sau của pipeline) tái dùng *"khỏi quét lại"*; hiểu = trả lời được 3 câu: hệ giải bài toán gì · một hành vi đi từ đâu đến đâu · sửa một chỗ thì vỡ đâu.

- 0 — người nhận (dev/CTO/stage kế) đọc xong vẫn phải tự quét code gốc mới làm việc được: thiếu câu trả lời cho ≥1 trong 3 câu hợp đồng (không có intake/bài toán; không có luồng; không có change-impact), hoặc change-impact chỉ là câu chung chung không chỉ vùng vỡ cụ thể.
- 1 — trả lời đủ 3 câu nhưng khó cầm đi làm: impact map kiểu "ảnh hưởng nhiều nơi" thiếu vùng và mức risk cụ thể, không có điều hướng ai-đọc-mục-nào, hoặc open question chuyển tiếp không kèm cách verify.
- 2 — trả lời đủ 3 câu; change-impact chỉ rõ *sửa X → kiểm Y, risk mức nào*; nói rõ stage/skill nào tái dùng mục nào; open question chuyển tiếp có cách verify + ưu tiên — cầm artifact là bắt tay ngay việc kế tiếp mà không mở lại code gốc trừ chỗ đã được đánh dấu unknown.

## 4. ĐỦ BỘ MỘT LƯỢT — phủ trọn nội dung hợp đồng, không hẹn lượt sau

Luật cứng: *"Một lần, đầy đủ"* — một lượt sinh đủ bộ hiểu biết theo thứ tự đọc của hợp đồng (metadata → entrypoints → config → structure → domain → contracts → flows → side effects → tests → risks) + index + scorecard + chỗ ghi drift.

- 0 — thiếu hẳn ≥1 mảng lớn (vd không có domain model/bất biến, không có side-effects map, không có security/permission map, không có test & observability map, không có scorecard), hoặc artifact tự hẹn "lượt sau bổ sung phần còn lại".
- 1 — các mảng đều có mặt nhưng 1–2 mảng chỉ điểm danh cho có (vd test map chỉ ghi "có ~N test" mà không nói cái gì được bảo vệ), hoặc thiếu một thành phần quản trị (mục lục/trạng thái · scorecard · chỗ ghi drift) mà không nêu lý do.
- 2 — một lượt phủ đủ mọi mảng của hợp đồng với nội dung thật; thành phần quản trị đầy đủ; nếu hình thức khác bộ-20-file chuẩn của atlas thì phải khai báo mapping tương đương + lý do ngay trong artifact (không được im lặng bỏ hình thức chuẩn).

## 5. TÁCH BIẾT / CHƯA BIẾT — facts ≠ assumptions, unknowns có đường verify

Luật cứng: *"Tách facts khỏi assumptions"* + *"Chưa đủ căn cứ → ghi vào risks_and_unknowns, KHÔNG ghi như fact"*.

- 0 — giả định/suy đoán trộn lẫn quan sát không nhãn ở nhiều chỗ; hoặc không có mục risks/unknowns dù phạm vi đọc rõ ràng chưa phủ hết (artifact tự nhận chưa mở X nhưng vẫn khẳng định chắc nịch về X).
- 1 — có tách và có mục unknowns, nhưng nhãn không nhất quán (vài chỗ suy đoán vẫn viết giọng khẳng định), hoặc unknown liệt kê suông không nói vì sao quan trọng / verify bằng cách nào.
- 2 — nhãn fact/assumption/độ-chắc nhất quán toàn artifact; mỗi unknown có lý do quan trọng + cách verify + ưu tiên; nói thẳng "chắc theo nguồn nào" (theo evidence ≠ theo re-read code gốc).

## 6. ĐÚNG VAI ATLAS — hiểu cho hệ thống, không lấn skill khác

Hợp đồng: atlas = hiểu CHO HỆ THỐNG (bằng chứng, bền vững, dùng chung) — dạy theo mức người là việc của explain; phán số phận file là triage; cắt slice và sửa code là frame. Read-only trên code đích.

- 0 — làm việc của skill khác: dạy dài theo mức người học (explain), phán giữ/sửa/xoá file (triage), viết hoặc đề xuất code sửa (frame), tự quyết scope build; hoặc sửa/đề nghị sửa code đích (vi phạm read-only).
- 1 — đúng vai chính nhưng lấn nhẹ: đôi đoạn sa vào giọng dạy-học hoặc khuyến nghị hành động vượt vai ghi-nhận, nhưng phần lõi vẫn là bản đồ + bằng chứng.
- 2 — thuần bản đồ hiểu biết: ghi nhận + bằng chứng + rủi ro; mọi việc vượt vai chỉ xuất hiện dưới dạng open-Q / handoff chỉ đích danh stage/skill nhận.

## 7. TƯƠI & CẬP NHẬT ĐƯỢC — neo phiên bản + đường chống stale

Hợp đồng: index ghi `built_at` + `built_commit`; drift ledger (`99_changes`, `last_synced_commit`) để cập nhật phần đổi thay vì dựng lại; freshness check trước khi tái dùng.

- 0 — không ghi dựng lúc nào, từ nguồn/phiên bản nào; không có bất kỳ cơ chế nào để biết atlas còn tươi hay đã stale khi code gốc đổi.
- 1 — có built_at + nguồn nhưng neo phiên bản không kiểm được (không có commit hash mà cũng không nêu lý do), hoặc không nói cách cập nhật khi nguồn đổi (drift ghi vào đâu, ai được bump).
- 2 — ghi rõ built_at · neo phiên bản nguồn (commit, hoặc lý-do-không-có kèm mô tả trạng thái nguồn) · scope đã phủ/chưa phủ; có chỗ ghi drift + quy tắc cập nhật phần đổi — đọc header là biết ngay "còn tin được không, cập nhật thế nào".

## Luật gate

Tiêu chí 1, 2, 3 là xương sống. Bất kỳ cái nào = 0 → artifact **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 12/14 nhưng có claim bịa (tiêu chí 1 = 0) vẫn rớt — vì atlas là NỀN: mọi stage sau xây trên nó, một anchor bịa sẽ lan thành quyết định kiến trúc sai. Gate quan trọng hơn tổng: khi so nhiều bản atlas, loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Vì sao 7 tiêu chí này

Ba tiêu chí gate đo đúng ba lời hứa sống còn của atlas: **bằng chứng thật** (1 — nền không bịa thì stage sau mới dám tin), **chứng minh hiểu bằng trace** (2 — mục tiêu hợp đồng là *"chứng minh đã hiểu hệ thống, không tóm tắt file"*), **dùng lại được** (3 — atlas tồn tại để skill khác khỏi quét lại; không dùng được thì dựng làm gì). Bốn tiêu chí còn lại đo phần kỷ luật của hợp đồng: đủ bộ một lượt (4), tách biết/chưa biết (5), đúng vai (6), chống stale (7). Gộp lại = toàn bộ mục tiêu + luật cứng của `atlas/SKILL.md`, không hơn. Thêm tiêu chí thứ 8 chỉ khi có một kiểu lỗi thật lặp lại mà 7 cái này không bắt được.
