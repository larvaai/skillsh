# Rubric — 8 tiêu chí chấm artifact GĐ9 Backlog (rebuild-hex-agent)

Mỗi tiêu chí 0/1/2. Chuẩn gốc: `.claude/skills/backlog/SKILL.md` (hợp đồng GĐ9 — Luật cứng, Thân ba artifact, Tự soi, Cổng, Bàn giao). Rubric chỉ biến hợp đồng đó thành thước đo được — không thêm tiêu chuẩn mới, không mượn tiêu chí của explain.

Chuẩn đối chiếu khi artifact trích code làm bằng chứng (dạng `path:line` hoặc mô tả hành vi code): code gốc tại `/Users/uspro/Desktop/namnson/hex_agent`. Trích sai hoặc trích thứ không tồn tại = bịa.

Điểm tối đa: 16. Tiêu chí 1, 3, 5 là xương sống (gate).

## 1. ĐỌC-ĐƯỢC 3 TẦNG — leadership-first (xương sống)

Hợp đồng gọi đây là "lý do skill tồn tại — tuyệt đối không bỏ": Roadmap và MỖI Epic mở bằng Góc nhìn lãnh đạo (business value + trạng thái, ngôn ngữ nghiệp vụ), RỒI mới xuống Feature→Story→AC cho dev; cả gói scan 2–3 phút.

- 0 — không có tầng lãnh đạo mở đầu, HOẶC có ≥1 Epic không nói được business value bằng một câu nghiệp vụ (mở thẳng vào kỹ thuật: "dựng kernel", "làm adapter" mà không nói khối tiền này đổi lấy giá trị gì), HOẶC lãnh đạo đọc phần đầu xong vẫn không trả lời được "xây gì / vì giá trị gì / tới đâu" nếu không hỏi dev.
- 1 — có tầng lãnh đạo và mọi Epic có business value, nhưng jargon kỹ thuật lọt vào phần dành cho lãnh đạo ở 1–2 chỗ (tên class/file/pattern chưa được dịch nghĩa), hoặc trạng thái epic thiếu/mơ hồ, hoặc phần lãnh đạo dài quá mức scan 2–3 phút.
- 2 — Roadmap mở bằng Business Objective đo được + bảng theme×release tự đứng được cho CEO/CTO; mỗi Epic mở bằng business value + trạng thái bằng ngôn ngữ nghiệp vụ — lãnh đạo dừng ở tầng epic vẫn hiểu mỗi khối tiền đổi lấy gì; dev đọc tiếp xuống AC không phải đoán.

## 2. ĐỦ BA ARTIFACT + ĐÚNG CÂY TẦNG

Hợp đồng bắt sinh đúng ba artifact theo template GĐ9, và cấm bỏ tầng phân rã.

- 0 — thiếu hẳn một trong ba (Roadmap theme×release / Backlog phân rã / Release Plan), HOẶC backlog nhảy tầng (Epic → Task mà không có Feature+Story ở giữa).
- 1 — đủ ba nhưng một artifact thiếu thành phần bắt buộc của template: Roadmap không neo `Business Objective → Product Goal`; Release Plan thiếu điều kiện go-live (Release AC) hoặc thiếu phụ thuộc/rủi ro/mục hoãn; R1 không bao slice GĐ8.
- 2 — đủ ba, mỗi artifact đủ thành phần: Roadmap neo Objective/Goal + theme×release; Backlog đủ tầng Epic→Feature→Story→AC (Tasks/Test-ref chỉ là móc); Release Plan có mục tiêu nối success metric, thứ tự, Release AC, phụ thuộc, rủi ro, và mục CỐ TÌNH hoãn kèm lý do; R1 = MVP bao slice GĐ8.

## 3. AC DÙNG ĐƯỢC — dev cầm đi làm ngay (xương sống)

Đầu ra sống còn cho người nhận: story của release gần nhất phải đủ để `/frame` nhận một story và bắt tay code.

- 0 — release gần nhất có story không có AC, HOẶC AC không kiểm được (Then là tính từ "nhanh/ổn định/tốt" không ngưỡng, không quan sát được bằng test/máy), HOẶC AC viết thành danh mục yêu cầu toàn sản phẩm (PRD thứ hai) thay vì behavior của đúng một story, HOẶC DoD bị trộn vào AC.
- 1 — đa số story release gần nhất có AC Given/When/Then kiểm được, nhưng 1–2 AC có Then mơ hồ, hoặc vài story thiếu Tasks thô để size / thiếu Test ref, hoặc story dạng user-story thiếu vế "để <giá trị>".
- 2 — mọi story release gần nhất có ≥1 AC Given/When/Then với Then kiểm được (kết quả cụ thể, có thể viết test), AC nằm DƯỚI đúng story của nó và phản ánh business rule Domain; kèm Tasks thô đủ để size + Test ref (TC-…) làm móc — một dev chưa dự pipeline vẫn nhận story đầu tiên và bắt đầu được.

## 4. ĐỦ-LÀ-ĐỦ — độ sâu tỉ lệ rủi ro, không phân rã thừa

- 0 — đổ Story+AC hàng loạt cho release xa (thứ hợp đồng cấm), HOẶC release gần nhất không được phân rã tới Story+AC, HOẶC viết story để lấp chỗ Domain còn treo thay vì ghi open question.
- 1 — đúng hướng nhưng lệch 1–2 chỗ: một epic release xa phân rã sâu không kèm lý do rủi ro; story rủi ro cao chỉ có 1 AC happy-path (thiếu biên/error); story quen thuộc lại gánh 4–5 AC.
- 2 — mật độ đúng luật: release gần nhất tới Story+AC, release giữa Feature+Story chính, release xa chỉ theme+epic; số AC tỉ lệ rủi ro (story mới/rủi ro cao phủ happy path + biên + error, story quen 1–2 AC); phân rã sâu ngoài release gần có nêu lý do (vd rủi ro/giá trị cao); Domain treo → open-Q, không bịa story.

## 5. TRACEABILITY & KHÔNG BỊA — mọi mắt xích, mọi con số có nguồn kiểm được (xương sống)

Hợp đồng: mỗi Epic nối ngược Business Objective/Product Goal; Feature→Epic; Story→Feature; AC→Story + business rule Domain; slice GĐ8 = feature ĐẦU TIÊN của release gần nhất; "giả định đã đổi" của GĐ8 phản ánh vào backlog; đứt mắt nào ghi rõ chỗ đứt, không bịa nối.

- 0 — có claim bịa, bất kỳ loại nào: epic/feature/story/AC không nối được về nguồn GĐ trước nào; con số/metric/tên rule tự chế không có trong artifact nguồn; trích code (`path:line` hoặc hành vi) sai khi đối chiếu `/Users/uspro/Desktop/namnson/hex_agent`; tự khen kiểu "đã phủ đủ X" trong khi đếm lại không khớp nội dung chính artifact; hoặc mắt xích đứt bị nối giả thay vì ghi rõ. Bất kỳ claim bịa nào → tiêu chí này 0.
- 1 — chuỗi liền phần lớn nhưng 1–2 tham chiếu mơ hồ không địa chỉ (trỏ "GĐ trước" chung chung, không nói file/mục nào), hoặc slice GĐ8 có làm feature đầu R1 / giả định-đã-đổi có phản ánh nhưng không chỉ ra được nối vào story/AC nào.
- 2 — mọi epic/feature/story/AC có địa chỉ nguồn kiểm được (artifact GĐ1–8 hoặc code gốc); trích code khớp code thật; slice GĐ8 đứng đúng vị trí feature đầu release gần nhất; từng "giả định đã đổi" GĐ8 chỉ ra được nó thành story/AC nào; chỗ chưa chắc gắn nhãn open-Q rõ ràng.

## 6. LÝ DO + PHƯƠNG ÁN ĐÃ LOẠI — quyết định lớn audit lại được

- 0 — thứ tự release / cắt MVP / hoãn epic không có lý do, hoặc lý do trang trí không audit được ("vì quan trọng", "cho hợp lý"), và không nêu được phương án đã loại nào.
- 1 — đa số quyết định lớn có lý do 1 dòng nhưng thiếu phương án đã loại, hoặc còn 1–2 quyết định lớn (đưa theme vào R nào, gộp/tách epic, park) trần không lý do.
- 2 — mỗi quyết định lớn (theme vào R1 hay R2, epic cắt khỏi MVP, gộp/tách epic, hoãn/park) có lý do kiểm được + phương án đã loại nêu tên kèm vì sao loại; thứ tự xếp theo giá trị/rủi ro, không theo độ khó kỹ thuật.

## 7. RANH GIỚI VAI — đúng việc GĐ9, không lấn

- 0 — làm việc GĐ khác: mở lại WHY/ROI (GĐ1), chọn/so lại stack hay kiến trúc (GĐ6–7), chia module/gán owner kỹ thuật (GĐ10), viết code/đặc tả kỹ thuật slice/DoD chi tiết (GĐ11), hoặc viết Test Case chi tiết thay vì chỉ đặt Test ref (GĐ12).
- 1 — chủ yếu đúng vai nhưng lấn nhẹ 1–2 chỗ: Tasks chi tiết tới mức thành đặc tả kỹ thuật; nhắc quyết định stack kèm bàn thêm ưu nhược thay vì chỉ tham chiếu để size; gợi ý ranh giới module vượt mức "trỏ sang GĐ10".
- 2 — đúng vai trọn: kiến trúc/stack chỉ tham chiếu để size feature + ràng buộc thứ tự; DoD chỉ trỏ GĐ11; Test ref chỉ móc TC-; câu ngoài vai ghi thành open question/mục bàn giao trỏ đúng skill, không tự làm.

## 8. CỔNG + BÀN GIAO — trình đánh giá, không tuyên pass suông, không chọn hộ

- 0 — không có cổng hoặc không có khối bàn giao; HOẶC tuyên "pass/GO" suông không kèm trình đánh giá + rủi ro + open-Q còn treo; HOẶC bàn giao tự quyết bước kế thay người duyệt (chỉ đưa một đường, ép đi tiếp).
- 1 — có cổng + bàn giao nhưng thiếu mảnh: không dùng đúng câu hỏi cổng doc GĐ9 ("Backlog đủ để lập kế hoạch delivery & phân module chưa?"); không nêu open-Q còn treo hoặc rủi ro kèm quyết định; bàn giao thiếu lựa chọn (chỉ /modules, không có đường /frame hoặc đường quay lại khi Domain treo).
- 2 — cổng dùng đúng câu doc GĐ9 kèm các câu phụ (R1 có story+AC? roadmap đọc được? thứ tự có lý do? open-Q Domain nào chặn?); trình đánh giá + rủi ro + open-Q trước khi ra quyết định; bàn giao liệt kê đủ lựa chọn (/modules mặc định · /frame build ngay · đường quay /idea·/partner) để người giữ vai PO/Tech-lead quyết.

## Luật gate (tiêu chí xương sống)

Tiêu chí 1, 3, 5 là xương sống. Bất kỳ cái nào = 0 → artifact **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 14/16 nhưng có một AC dẫn `path:line` không tồn tại trong code gốc (tiêu chí 5 = 0) vẫn rớt — vì đội delivery sẽ xây kế hoạch trên bằng chứng giả. Gate quan trọng hơn tổng: khi so nhiều bản, loại hết bản rớt gate trước, rồi mới xếp theo tổng.

Vì sao chọn đúng ba cái này làm gate:
- **Tiêu chí 5 (traceability & không bịa)** — mọi con số, mọi mắt xích, mọi trích code phải có nguồn kiểm được; backlog "mồ côi" hay nối giả là thứ hợp đồng gọi thẳng là rớt cổng.
- **Tiêu chí 1 (đọc-được 3 tầng)** — hợp đồng tự tuyên đây là "lý do skill tồn tại — tuyệt đối không bỏ"; mất tầng lãnh đạo thì artifact chỉ còn là danh sách việc cho dev, sai bản chất GĐ9.
- **Tiêu chí 3 (AC dùng được)** — GĐ9 trả lời "XÂY GÌ TRƯỚC"; nếu dev không cầm story+AC của release gần nhất đi `/frame` được ngay thì câu trả lời đó rỗng, dù trình bày đẹp đến đâu.

## Vì sao 8 tiêu chí này

Bốn cái đầu đo *artifact có đúng cái backlog hứa không*: tầng lãnh đạo đọc được (1), đủ ba artifact đúng cây tầng (2), AC đủ cho dev hành động (3), độ sâu đúng luật đủ-là-đủ (4). Bốn cái sau đo *có trung thực và đúng vai không*: mọi mắt xích và con số có nguồn (5), quyết định audit lại được (6), không lấn GĐ khác (7), cổng và bàn giao trả quyền quyết cho người duyệt (8). Gộp lại = toàn bộ Luật cứng + Thân + Cổng + Bàn giao của `backlog/SKILL.md`, không hơn. Thêm tiêu chí thứ 9 chỉ khi có một kiểu lỗi thật lặp lại mà 8 cái này không bắt được.
