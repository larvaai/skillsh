# Rubric — 7 tiêu chí chấm artifact GĐ10 "Modules" (Module Map + Module Contract)

Mỗi tiêu chí 0/1/2. Chuẩn gốc: `modules/SKILL.md` (hợp đồng GĐ10 — Luật cứng, template hai artifact, Tự soi, Cổng go/no-go). Rubric chỉ biến hợp đồng đó thành thước đo được — không thêm tiêu chuẩn mới.

Chuẩn đối chiếu khi artifact có claim về code/hành vi hệ thống: code gốc tại `/Users/uspro/Desktop/namnson/hex_agent`. Chuẩn đối chiếu khi artifact trích giai đoạn trước: artifact pipeline thật (GĐ5 Domain, GĐ6 Shape, brief/evidence) trong cùng package. "Kiểm được" nghĩa là: người chấm mở đúng file/mục được trỏ và thấy đúng điều được claim.

## 1. BÁM NGUỒN — mọi claim & con số có nguồn kiểm được, không bịa, không tự khen (xương sống)

Ranh giới module phải trỏ về bounded context của Domain Model (GĐ5) đã có; định danh code (tên hàm/port/bảng/hằng số) phải tồn tại trong `/Users/uspro/Desktop/namnson/hex_agent` hoặc trong artifact GĐ trước được trích; con số (budget, depth, threshold, SLA) phải có nguồn hoặc được khai là chưa-có-số.

- 0 — có ít nhất một claim bịa: bounded context không tồn tại trong GĐ5; định danh/hành vi code không tìm được trong code gốc lẫn artifact trước; con số SLA/budget tự chế không nguồn; hoặc trích dẫn GĐ trước (vd "GĐ5 §5.5") mà mở ra không có nội dung đó. Tự khen ("đầy đủ", "sạch", "✔") ở mục Tự soi/Cổng mà không trỏ được tới bằng chứng cụ thể trong chính artifact → cũng tính 0.
- 1 — bám nguồn phần lớn, còn 1–2 claim mơ hồ không gắn nguồn hoặc không gắn nhãn "chưa chắc"/"open-Q".
- 2 — mọi claim trỏ được về nguồn (GĐ5/GĐ6/evidence/code gốc, có mục cụ thể); chỗ chưa có số ghi thành open-Q chuyển đúng giai đoạn (vd ngưỡng vận hành → Operate), không điền số cho đẹp.

## 2. SỞ HỮU SẠCH — mỗi module đúng 1 owner, mỗi data/event đúng 1 chủ, "Does NOT own" luôn hiện (xương sống)

Điều sống còn của hợp đồng GĐ10: các team chạy song song không giẫm nhau. Kiểm bằng đối chiếu chéo toàn bộ các contract với nhau.

- 0 — có module không owner, hai owner, hoặc "chung của mọi người"; hoặc một mảnh data/event xuất hiện ở mục Owns của HAI module; hoặc bất kỳ contract nào thiếu dòng "Does NOT own" (luật cứng: không bao giờ được bỏ).
- 1 — ownership đúng nhưng còn 1 chỗ nhập nhằng: một mảnh data/event không rõ chủ, hoặc "Does NOT own" chỉ phủ định chung chung mà không nói phần đó thuộc module/team nào.
- 2 — mỗi module nêu đúng 1 team owner bằng tên; Owns liệt kê cụ thể (bảng/state/event nào); đối chiếu chéo mọi contract không mảnh nào hai chủ; "Does NOT own" chỉ đích danh ai lo thay. (Một team sở hữu nhiều module vẫn đạt — module ≠ team — miễn mỗi module chỉ một owner.)

## 3. DÙNG ĐƯỢC THẬT — dev cầm contract code được trong ranh giới, không phải hỏi lại (xương sống)

Người nhận là team dev NGOÀI, không biết nội bộ. Thước: một team chỉ đọc contract của module mình + seam của module mình gọi — có bắt đầu code được không?

- 0 — bất kỳ module nào thiếu ô BẮT BUỘC (Owner · Responsibilities · Owns · Does NOT own · Public API), hoặc Public API chỉ nói tồn tại ("có API REST", "expose một port") mà không nêu tên seam + dữ liệu vào/ra → team phải hỏi lại mới làm được.
- 1 — đủ ô bắt buộc ở mọi module, nhưng seam của module lõi thiếu kiểu vào/ra, hoặc error code / permission ở module lõi ghi sơ sài không đủ để team gọi xử lý lỗi.
- 2 — mọi module đủ ô bắt buộc; module lõi/nhiều-team-gọi có Public API kèm request/response, error code công khai, permission model, và test contract nêu được cặp team nào test đối đầu cặp nào; module rìa rút gọn ĐỘ SÂU kèm 1 dòng lý do, không bỏ ô.

## 4. ĐỌC 3 TẦNG — Góc nhìn lãnh đạo trước, kỹ thuật sau

Theo luật cứng "hợp đồng đọc-được 3 tầng": mở bằng điều CEO/CTO nhìn ("ai chịu trách nhiệm cái gì khi có sự cố"), ngôn ngữ nghiệp vụ, rồi mới tới chi tiết dev.

- 0 — artifact đâm thẳng vào endpoint/schema/sơ đồ; không có phần lãnh đạo mở đầu Map, hoặc phần "lãnh đạo" viết bằng jargon (seam, chokepoint, OpenAPI, event-sourcing) không giải nghĩa — CTO không-code đọc không trả lời được "hỏng ở X thì gọi ai".
- 1 — có mở bằng góc nhìn lãnh đạo nhưng lẫn jargon chưa neo nghĩa, hoặc một số contract thiếu dòng lãnh đạo mở đầu, hoặc đọc xong vẫn phải suy ra "sự cố gọi ai" thay vì thấy ngay.
- 2 — Map mở bằng bảng module × team owner + mỗi module một dòng "sở hữu gì / KHÔNG sở hữu gì" ngôn ngữ nghiệp vụ; mỗi contract mở bằng dòng lãnh đạo "giữ phần nghiệp vụ nào, hỏng thì hỏi ai" TRƯỚC API/event/error; thuật ngữ kỹ thuật xuất hiện lần đầu có neo nghĩa đời thường; phần lãnh đạo scan được 2–3 phút.

## 5. CHIA THEO DOMAIN — không theo màn hình, mỗi gộp/tách có lý do + phương án đã loại

- 0 — có module cắt theo màn hình/tab/cụm UI hoặc theo tầng kỹ thuật thuần (kiểu "module frontend/backend") thay vì bounded context; hoặc có gộp/tách khác ánh xạ mặc định mà không ghi lý do nào.
- 1 — ranh giới bám domain nhưng còn 1 quyết định gộp/tách chỉ có lý do dạng tính từ ("gọn hơn", "hợp lý hơn") không nêu tiêu chí domain, hoặc có lý do mà thiếu phương án đã cân-và-loại.
- 2 — mỗi module trỏ về đúng bounded context GĐ5 nguồn; mọi gộp/tách khác mặc định ghi lý do bằng tiêu chí của hợp đồng (data ownership · change frequency · team ownership · security/integration boundary) KÈM phương án đã loại + vì sao loại — đủ để CTO audit lại ranh giới mà không cần hỏi người viết.

## 6. PHỦ FEATURE — kiểm chéo backlog, không mồ côi, không hai chủ, nguồn ngoài phải cảnh báo

- 0 — không có bảng kiểm chéo feature→module; hoặc có feature/epic mồ côi hay thuộc hai module mà không giải thích; hoặc dùng nguồn NGOÀI pipeline (chưa qua cổng GĐ9) mà không in block cảnh báo ⚠️ theo mẫu của hợp đồng.
- 1 — có kiểm chéo nhưng sót mục không được giải thích, hoặc có cảnh báo nguồn ngoài nhưng thiếu rủi ro/nêu đường chuẩn hoá, hoặc phần chưa cấp module không ghi lý do.
- 2 — mọi feature (hoặc epic — khi thiếu GĐ9, kèm block cảnh báo đủ: nguồn thay thế + rủi ro + đường chuẩn hoá) map vào đúng MỘT module trong bảng đối chiếu; mục chưa cấp module ghi rõ vì sao (park/YAGNI) và khi nào cấp lại.

## 7. ĐÚNG VAI + CỔNG — không lấn skill khác, cổng trình bằng chứng, bàn giao mở lối

- 0 — lấn vai: viết code/pseudo-code triển khai, định lại domain (đẻ context mới), viết lại story, đặt chuẩn delivery/DoD, chọn stack; HOẶC không có khối cổng / cổng không trình bằng chứng; HOẶC tự tuyên GO khi không có ủy quyền tự-quyết ghi rõ.
- 1 — đúng vai và có cổng, nhưng bằng chứng thiếu 1 trong 4 mục (mỗi module 1 owner · không data/event hai chủ · không feature mồ côi · mọi phụ thuộc qua contract/seam), hoặc khối bàn giao tự chọn hộ bước tiếp thay vì liệt kê lựa chọn.
- 2 — đúng vai trọn (chỉ vẽ ranh giới + contract); cổng nêu câu hỏi GĐ10 + trình đủ 4 bằng chứng, mỗi bằng chứng trỏ được vào nội dung artifact; nếu tự quyết GO thì có ủy quyền ghi rõ + lý do + phương án đã loại ở tầng cổng; bàn giao liệt kê các lối đi tiếp (delivery/frame/…) để người duyệt tự chọn.

## Luật gate

Tiêu chí 1, 2, 3 là xương sống. Bất kỳ cái nào = 0 → artifact **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 12/14 nhưng bịa một bounded context không có trong GĐ5 (tiêu chí 1 = 0) vẫn rớt — vì mọi team sẽ code theo một ranh giới không tồn tại. Một bản có mảnh data hai chủ (tiêu chí 2 = 0) vẫn rớt — vì đúng cái GĐ10 tồn tại để chặn (hai team giẫm nhau) đã hỏng. Một bản thiếu Public API đo được (tiêu chí 3 = 0) vẫn rớt — vì "chạy song song" chỉ là lời hứa khi team không code được trong ranh giới. Gate quan trọng hơn tổng: khi so nhiều bản, loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Vì sao 7 tiêu chí này

Ba gate đo *artifact có đáng tin và dùng được không*: bám nguồn (1 — không bịa, mọi con số có gốc), sở hữu sạch (2 — điều sống còn hợp đồng GĐ10 hứa: team song song không giẫm nhau), dùng được thật (3 — dev cầm đi code được ngay). Bốn cái sau đo *có đúng hình dạng hợp đồng không*: đọc 3 tầng (4 — lý do skill tồn tại: viết cho CTO/business/dev ngoài), chia theo domain (5 — luật A3-#3 kèm audit-trail lý do), phủ feature (6 — sợi trace về GĐ9), đúng vai + cổng (7 — không lấn sibling, không tự trôi sang GĐ11). Gộp lại = toàn bộ Luật cứng + Tự soi + Cổng của `modules/SKILL.md`, không hơn. Thêm tiêu chí thứ 8 chỉ khi có một kiểu lỗi thật lặp lại mà 7 cái này không bắt được.
