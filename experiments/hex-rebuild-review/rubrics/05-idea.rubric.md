# Rubric — 8 tiêu chí chấm artifact 05-idea (Idea → Domain, GĐ0–5)

Mỗi tiêu chí 0/1/2, tổng tối đa 16. Chuẩn gốc: `.claude/skills/idea/SKILL.md` (Router, Nhánh C GĐ1→GĐ5, Quy tắc bắt buộc, Đủ-là-đủ, Bàn giao). Rubric chỉ biến hợp đồng đó thành thước đo được — không thêm chuẩn mới. Thước này chấm artifact Nhánh C (khả thi rõ, đi hết GĐ0–5); khi artifact có claim về code, chuẩn đối chiếu là code gốc tại `/Users/uspro/Desktop/namnson/hex_agent`.

## 1. BẰNG CHỨNG — không bịa, không tự khen (xương sống)

Mọi con số và claim về cơ chế/code phải có nguồn kiểm được — file:line trong code gốc, hoặc artifact trung gian (atlas/evidence) dẫn được về code. Ước lượng phải gắn nhãn ước lượng.

- 0 — có ≥1 claim bịa: nhắc file/hàm/hằng số/hành vi không tồn tại hoặc sai so với `/Users/uspro/Desktop/namnson/hex_agent`; hoặc trình ước lượng/giả định như số đo thật; hoặc tự khen không kiểm được ("đã chứng minh", "chắc chắn chạy") mà không trỏ về bằng chứng. Bất kỳ claim bịa nào → tiêu chí này 0.
- 1 — mọi claim kiểm lại đều đúng, nhưng 1–2 chỗ nêu số/cơ chế không kèm nguồn, hoặc suy đoán không gắn nhãn "chưa chắc"/open-Q.
- 2 — mọi con số (NFR, budget, metric…) và claim cơ chế đều neo nguồn kiểm được; chỗ chưa có số thật ghi rõ "ước lượng thô" hoặc open-Q; không có câu tự khen thiếu bằng chứng.

## 2. ĐỦ CHUỖI GĐ0–5 — không nhảy cóc, cổng nào cũng có người quyết

Hợp đồng: không bao giờ nhảy cóc giai đoạn, chỉ được RÚT GỌN độ sâu; mỗi giai đoạn kết bằng cổng go/no-go.

- 0 — thiếu hẳn một khối: không có Router (độ rõ × độ khả thi + nhánh được chọn), hoặc vắng một trong GĐ0-intake / GĐ1 / GĐ2–4 / GĐ5, hoặc có giai đoạn đi qua mà không ghi quyết định cổng.
- 1 — đủ Router + 4 khối giai đoạn + cổng, nhưng Router thiếu một trục (chỉ phân độ rõ hoặc chỉ độ khả thi), hoặc ≥1 cổng chỉ ghi "GO" trống không — không lý do, không ghi ai quyết.
- 2 — Router phân loại cả hai trục kèm căn cứ, nhánh chọn đúng logic bảng định tuyến; cả 4 khối giai đoạn hiện diện (được phép rút gọn theo Đủ-là-đủ, độ sâu tỉ lệ rủi ro); mỗi cổng ghi quyết định + lý do + ai quyết (user, hay vai tự-quyết được nêu tường minh).

## 3. GĐ1 — WHY bằng con số, không cảm tính

Đủ-là-đủ của GĐ1: vấn đề + ai đau + chi phí nếu không làm (ước lượng thô) + 1 success metric đo được.

- 0 — không có success metric đo được, hoặc kết luận "đáng làm" chỉ dựa tính từ ("rất cần", "tiềm năng lớn") không kèm con số/cách kiểm nào.
- 1 — có metric nhưng không nói kiểm bằng gì (đo ở đâu, oracle nào), hoặc thiếu một trong {ai đau, chi phí nếu không làm}.
- 2 — nêu rõ ai đau + đau gì; chi phí nếu không làm có ước lượng (gắn nhãn thô nếu chưa có số thật, kèm open-Q chỗ lấy số sau); ≥1 success metric kèm cách kiểm cụ thể (điều kiện pass/fail kiểm được).

## 4. GĐ2–4 — MVP cắt rõ, scope OUT thành chữ, open-Q có chỗ chốt

- 0 — không chỉ ra được MVP là gì trong một câu, hoặc hoàn toàn không có scope OUT (không nói cái gì CỐ TÌNH không làm).
- 1 — MVP và OUT đều có nhưng: OUT chỉ chung chung ("phần còn lại làm sau") không liệt kê từng mục, hoặc ≥1 open question treo mà không ghi sẽ chốt ở giai đoạn nào.
- 2 — MVP nêu được trong một câu rõ + đo bằng metric nào; OUT liệt kê từng mục thành chữ; có journey AS-IS → TO-BE; mỗi open-Q ghi rõ chốt ở đâu (GĐ5 / shape / skeleton / operate…).

## 5. GĐ5 — Domain Model đủ 5 mắt xích, entity ≠ bảng DB (xương sống)

Chuỗi bắt buộc của hợp đồng: `Bounded Context → Entity (identity + lifecycle) → Business Rule bất biến → Domain Event → Data Ownership`. Đây là thứ người nhận (`shape`, GĐ6) cầm đi làm ngay — thiếu là đứng hình.

- 0 — thiếu hẳn 1 trong 5 mắt xích; hoặc entity trình bày như schema DB (cột, kiểu dữ liệu, khoá ngoại) thay vì identity + lifecycle.
- 1 — đủ 5 mắt xích nhưng có lỗ: ≥1 entity thiếu identity hoặc lifecycle; rule viết như mô tả tính năng thay vì điều-bất-biến-không-được-phá; event chỉ có tên mà không nói khi nào phát; hoặc có khối dữ liệu không rõ chủ / hai chủ.
- 2 — mỗi entity có identity + lifecycle ghi được thành trạng thái; mỗi rule phát biểu dạng bất biến kiểm được (điều kiện + ai enforce); mỗi event có tên + thời điểm phát; mỗi khối dữ liệu có đúng một context sở hữu.

## 6. DỪNG ĐÚNG VAI — hết Domain là dừng, không build, không kill (xương sống)

Quy tắc bắt buộc của hợp đồng: dừng đúng GĐ5; KHÔNG viết code, KHÔNG chọn kiến trúc/framework/DB (đó là GĐ6+); KHÔNG tự kill ý tưởng; bàn giao liệt kê lựa chọn, không chọn hộ.

- 0 — artifact chốt kiến trúc/framework/DB cụ thể như quyết định của mình, vẽ schema, viết code, tự quyết kill ý tưởng, hoặc không có khối bàn giao.
- 1 — dừng đúng Domain nhưng lấn nhẹ: nêu công nghệ cụ thể bằng giọng đã-chốt (thay vì open-Q hoặc tham chiếu hiện trạng bản gốc), hoặc bàn giao chọn hộ đúng một đường đi tiếp thay vì liệt kê để user quyết.
- 2 — dừng đúng GĐ5; mọi việc thuộc GĐ6+ ghi thành open-Q hoặc park kèm điều kiện kích hoạt; khối bàn giao nêu domain đã chốt + artifact path + liệt kê ≥2 lối đi tiếp (shape/stack · frame · atlas/explain) để người nhận tự quyết.

## 7. ĐÚNG TẦNG — mỗi giai đoạn chỉ trả lời câu của tầng đó

Hợp đồng: GĐ1 hỏi giá trị/pain, không bàn kiến trúc/DB/deadline; GĐ2–4 không mở lại ROI đã chốt, không bàn stack; GĐ5 hỏi ranh giới domain, không bàn sprint/kiến trúc cụ thể. Nội dung lạc tầng phải thành open-Q mang sang đúng tầng.

- 0 — lạc tầng nặng và kết luận non tại chỗ: GĐ1 chốt chuyện kiến trúc/DB/deadline; GĐ2–4 mở lại ROI hoặc chốt stack; GĐ5 chốt sprint/framework.
- 1 — chủ yếu đúng tầng, có 1–2 chỗ nội dung tầng sau xuất hiện sớm mà chưa được đẩy thành open-Q về đúng tầng.
- 2 — mỗi giai đoạn chỉ chứa nội dung tầng mình; thứ thuộc tầng sau nếu xuất hiện thì được ghi nhận là open-Q kèm nơi chốt, không trả lời non.

## 8. AUDIT ĐƯỢC — quyết định lớn có lý do + phương án đã loại

Hợp đồng: mỗi quyết định lớn ghi lý do + phương án đã loại, để sau này audit vì sao chọn hướng này. Độ rộng brainstorm tỉ lệ rủi ro: việc quen thuộc → 1 hướng + lý do; ý mới/rủi ro cao → ≥2 hướng + vì sao loại hướng kia.

- 0 — các quyết định lớn (chọn nhánh Router, chốt MVP, chốt ranh giới context) không có lý do, hoặc cả artifact không có bất kỳ phương án đã loại nào.
- 1 — có lý do + phương án đã loại ở một số cổng nhưng không đều khắp các quyết định lớn; hoặc lý do loại chỉ là nhãn một câu ("không cần") không nói theo hướng đó thì mất/được gì.
- 2 — mỗi cổng/quyết định lớn ghi lý do chọn + ≥1 phương án đã loại kèm vì sao loại (nêu được mất gì nếu theo); phần rủi ro cao có ≥2 hướng được cân nhắc trước khi chốt.

## Luật gate

Tiêu chí 1, 5, 6 là xương sống. Bất kỳ cái nào = 0 → artifact **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 14/16 nhưng bịa file:line (tiêu chí 1 = 0) vẫn rớt — vì `shape` sẽ xây kiến trúc trên bằng chứng giả. Một bản đủ mọi thứ nhưng GĐ5 thiếu mắt xích (tiêu chí 5 = 0) vẫn rớt — người nhận không có gì để định hình kiến trúc. Một bản domain đẹp nhưng tự chốt luôn framework (tiêu chí 6 = 0) vẫn rớt — nó đã cướp quyết định của GĐ6 và của user. Gate quan trọng hơn tổng: khi so nhiều bản, loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Vì sao 8 tiêu chí này

Tiêu chí 1 đo *có trung thực không* — mọi thứ phía sau vô nghĩa nếu bằng chứng giả. Tiêu chí 2–5 đo *có đi đúng con đường idea hứa không*: đủ chuỗi Router→GĐ5, và mỗi giai đoạn đạt đúng chuẩn Đủ-là-đủ của chính nó (WHY có số, MVP + OUT rõ, Domain đủ 5 mắt xích). Tiêu chí 6–8 đo *có giữ kỷ luật của hợp đồng không*: dừng đúng vai, hỏi đúng tầng, quyết định audit được. Gộp lại = toàn bộ hợp đồng của `idea` cho một artifact Nhánh C, không hơn. Artifact Nhánh A (làm rõ nhu cầu) hoặc Nhánh B (spike) có hình khác — cần thước riêng, không ép vào thước này. Thêm tiêu chí thứ 9 chỉ khi có một kiểu lỗi thật lặp lại mà 8 cái này không bắt được.
