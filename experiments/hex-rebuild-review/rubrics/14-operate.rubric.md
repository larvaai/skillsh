# Rubric — 8 tiêu chí chấm artifact 14-operate (Operate — GĐ14 LEARN)

Mỗi tiêu chí 0/1/2, tổng tối đa 16. Chuẩn gốc: `.claude/skills/operate/SKILL.md` (Luật cứng · Đầu vào · Thân — ba artifact · Tự soi · Cổng go/no-go + Bàn giao). Rubric chỉ biến hợp đồng đó thành thước đo được — không thêm chuẩn mới.

Khi artifact có claim về code (tên metric, file, dòng, cơ chế, hành vi), **chuẩn đối chiếu là code gốc `/Users/uspro/Desktop/namnson/hex_agent`** — không phải chính artifact, không phải tài liệu trung gian. Khi artifact dẫn số/quyết định từ giai đoạn trước (GĐ1 · GĐ9 · GĐ13), chuẩn đối chiếu là artifact nguồn của giai đoạn đó.

Cách chấm: đọc một lượt, chấm hình dạng (tiêu chí 4–8) trước; rồi spot-check tiêu chí 1–3 — chọn **ít nhất 5 con số/claim ngẫu nhiên** đối chiếu nguồn (code gốc hoặc artifact GĐ trước), và **đi lại một sự cố giả định** từ alert đến hậu kiểm trên giấy xem có tắc ở mắt xích nào không.

## 1. SỐ THẬT — đo bằng số, mọi con số có nguồn kiểm được, không bịa, không tự khen (xương sống)

Luật cứng: *"Đo bằng số, không cảm tính"* — mỗi con số trên dashboard phải có nguồn thật (monitoring, log, ticket, analytics, test) + so với ngưỡng/target; *"'Chạy ổn' không phải một chỉ số"*; chưa đo được → ghi `chưa có số` + cách lấy, KHÔNG bịa con số cho đẹp.

- 0 — có ít nhất một trong các lỗi sau: con số không có nguồn kiểm được hoặc bịa cho đẹp; tuyên "đạt / đang tốt" mà không có số chống lưng (tự khen kiểu "chạy ổn", "rất an toàn"); claim code (tên metric, `file:line`, cơ chế guard/alert) sai khi đối chiếu `/Users/uspro/Desktop/namnson/hex_agent`; ô chỉ số bị bỏ trống lặng lẽ — không số, không `chưa có số`, không cách lấy. Một lỗi là đủ → 0.
- 1 — spot-check các số đều có nguồn đúng, nhưng 1–2 chỗ hổng nhẹ: số nêu trần không kèm ngưỡng/target để biết tốt-hay-xấu; `chưa có số` không kèm cách lấy; suy đoán trình bày như số đo mà không gắn nhãn.
- 2 — mỗi con số có nguồn thật + ngưỡng/target đi kèm; số chưa đo được ghi `chưa có số` + cách lấy cụ thể (đếm gì, từ đâu, khi nào có); mọi claim code khớp code gốc; không có câu tự khen thay cho bằng chứng.

## 2. ĐÓNG VÒNG GĐ1 — Business đối chiếu THẲNG mục tiêu gốc CEO đã ký (xương sống)

Luật cứng: *"Business metric đối chiếu THẲNG mục tiêu gốc GĐ1 — đây là bản chất của GĐ14... Dashboard nào không nối ngược được về mục tiêu Business Case = chưa xong."* Không có mục tiêu gốc thì hỏi, KHÔNG bịa target.

- 0 — nhóm BUSINESS chỉ nêu số rời, không nối ngược được về mục tiêu Business Case GĐ1; hoặc target gốc bị bịa/biến dạng so với artifact nguồn GĐ1; hoặc kết luận "đạt / chưa đạt" không dựa trên phép so số-thực-vs-target nào.
- 1 — có nối về GĐ1 nhưng hụt một mắt: một mục tiêu gốc không có dòng đối chiếu riêng (target + số hiện + trạng thái); dòng ĐỌC-CHO-LÃNH-ĐẠO không nêu target-vs-hiện; hoặc trạng thái đạt/chưa nói mơ hồ ("nhìn chung tích cực") thay vì gọi thẳng.
- 2 — TỪNG mục tiêu gốc GĐ1 (đúng như nguồn) có: target gốc + số hiện (hoặc `chưa có số` + cách lấy) + trạng thái tường minh (đạt / chưa / vượt / chưa-kết-luận-được kèm vì sao); dòng ĐỌC-CHO-LÃNH-ĐẠO và câu trả lời cổng *"Đạt mục tiêu chưa?"* dùng đúng phép so đó — CEO nhìn một dòng biết cái mình ký có thành sự thật không.

## 3. DÙNG ĐƯỢC THẬT — dev/Ops trực được ngay, CEO/CTO biết mình quyết gì (xương sống)

Tự soi của hợp đồng: *"Dev/Ops có đủ để hành động không (biết alert nào, ai là owner, DORA đo ở đâu, item nào vào vòng kế)?"* — artifact vận hành mà không trực được theo nó thì chỉ là văn.

- 0 — đọc xong vẫn phải hỏi lại mới vận hành được: không rõ alert nào bắt gì / ai nhận đầu tiên / khắc phục-lùi bằng gì; hoặc chỉ dẫn bằng tính từ không thao tác được ("theo dõi sát", "xử lý kịp thời", "escalate khi cần") — không tên, không ngưỡng, không người chịu trách nhiệm.
- 1 — mạch chính đủ nhưng 1–2 mắt xích mơ hồ: owner có tên nhưng không rõ vùng nào gọi ai; "cách lấy" số nêu chung chung ("từ log") không chỉ nguồn/công cụ cụ thể; item vòng kế có nhưng không rõ trỏ vào đâu.
- 2 — một sự cố giả định đi được trọn đường trên giấy: alert X (có ngưỡng) → ai nhận → phân loại theo gì → khắc phục/lùi bằng gì (theo Runbook GĐ13) → hậu kiểm đổ đi đâu; DORA và mỗi `chưa có số` đều có chỗ lấy thao tác được; mỗi item cải tiến trỏ đúng địa chỉ; CEO/CTO đọc xong biết chính xác điều mình phải quyết (đầu tư vòng kế vào đâu, mốc nào coi là đạt).

## 4. ĐỦ BỘ BA ARTIFACT ĐÚNG HÌNH — Dashboard 4 nhóm · Incident 5 bước · Iteration Loop, đủ-là-đủ

Luật cứng: *"KHÔNG bao giờ bỏ một trong ba artifact, chỉ rút gọn độ sâu"*; Dashboard đủ 4 nhóm (Business · Product · Engineering[DORA 4] · Operations) trên một màn hình, SỐNG (cập nhật được, không phải ảnh chụp một lần), mỗi nhóm ≥1 con số + ngưỡng; Incident đủ 5 bước (phát hiện → phân loại → owner → khắc phục → hậu kiểm); Iteration có nhịp + học được + về backlog. Độ sâu tỉ lệ RỦI RO/ẨN SỐ, không theo vị trí trong luồng.

- 0 — thiếu hẳn một trong ba artifact; hoặc Dashboard thiếu nhóm trong 4 nhóm; hoặc Incident đứt bước trong 5 bước (vd không có hậu kiểm/post-mortem) khiến quy trình không khép.
- 1 — đủ ba + đủ nhóm/bước nhưng lệch hình 1–2 chỗ: DORA thiếu chỉ số trong 4 mà không nêu lý do; dashboard không nói cập nhật theo nhịp nào (ảnh chụp một lần); độ sâu không tỉ lệ rủi ro — phình chỗ ít rủi ro (vd post-mortem dài khi 0 incident) hoặc mỏng chỗ rủi ro cao.
- 2 — đủ ba artifact đúng hình từng cái: 4 nhóm + DORA đủ 4 (hoặc rút gọn có lý do gắn quy mô hệ); dashboard SỐNG, ghi rõ nhịp cập nhật; Incident khép đủ 5 bước; độ sâu mỗi phần tỉ lệ đúng rủi ro/ẩn số của hệ, chỗ rút gọn nói vì sao đủ.

## 5. VÒNG HỌC VỀ BACKLOG — mỗi item truy về một con số, đổ đúng chỗ GĐ9

Hợp đồng: Iteration Loop là *"phần KHÔNG được bỏ — thiếu nó thì operate chỉ còn là giám sát, dashboard để ngắm"*: nhịp review rõ + ai dự; 1–3 item cải tiến ưu tiên, MỖI item kèm LÝ DO (số nào trỏ tới nó) + giữ traceability về roadmap GĐ9; không tự viết story.

- 0 — không có đường về backlog: không có item cải tiến; hoặc item không truy được về chỉ số lệch/drop/`chưa có số`/incident nào (ý tưởng từ trời rơi xuống); hoặc iteration loop chỉ là lời hứa "sẽ review định kỳ" không nhịp, không người dự.
- 1 — có nhịp + item + lý do nhưng lỏng một mắt: một item lý do chung chung ("nên cải thiện UX") không con số trỏ tới; item không nói đổ vào đâu trong backlog GĐ9; hoặc nhịp có tần suất nhưng không rõ ai dự.
- 2 — nhịp review rõ (tần suất + ai dự, lãnh đạo theo nhịp nào); mục "học được" rút từ chính dashboard/incident; mỗi item (1–3, có ưu tiên) truy được về đúng một chỉ số lệch/`chưa có số`/incident cụ thể và trỏ được chỗ đổ về GĐ9; item chỉ liệt kê + lý do, CHƯA phân rã story.

## 6. KẾ THỪA GĐ13 + ĐÚNG VAI — không dựng lại, không lấn, không tự kill

Hợp đồng: nhận alert/incident-owner/rollback từ `ship` (GĐ13) và *"xây tiếp, KHÔNG dựng lại từ đầu"*; thiếu nguồn thì nói rõ + hỏi (hoặc in cảnh báo ngoài-pipeline), KHÔNG bịa owner. Không code fix (→ `frame`), không viết story (→ `backlog`), không đào edge case từng dòng (→ `review`). Metric xấu → nêu con số + một lối đi tiếp, cấm "không thể / sai rồi / vô dụng"; quyết định sunset chỉ user chốt.

- 0 — dựng lại monitoring/alert/owner/rollback từ đầu như chưa có GĐ13, hoặc bịa incident owner/alert khi nguồn không có (không cảnh báo, không open-Q); hoặc lấn vai rõ: viết code fix, viết story/AC, tự đào edge case từng dòng thay vì hand off; hoặc phủ định cứng ("bỏ feature này đi", "vô dụng") / tự quyết sunset.
- 1 — kế thừa và đúng vai phần lớn, lấn nhẹ 1 chỗ: nêu lại alert/owner nhưng không dẫn nguồn GĐ13; hậu kiểm mô tả cách sửa chi tiết tới mức gần thành đặc tả code; một nhận xét metric xấu chưa kèm lối đi tiếp.
- 2 — alert/owner/rollback dẫn rõ nguồn GĐ13/GĐ trước và chỉ NỐI thêm thành quy trình; mọi việc ngoài vai chuyển thành action item / hand off đúng skill (`frame`/`backlog`/`review`); metric xấu nêu con số + đề xuất cải tiến hoặc sunset có lý do, quyền chốt để user.

## 7. ĐỌC-ĐƯỢC 3 TẦNG — góc nhìn lãnh đạo trước, chi tiết dev sau

Luật cứng số một của hợp đồng (*"lý do skill tồn tại — không bao giờ bỏ"*): người đọc là người NGOÀI (CEO/CTO, business, dev). Mỗi artifact MỞ bằng Góc nhìn lãnh đạo — đúng 1–3 con số, ngôn ngữ nghiệp vụ, không jargon — RỒI mới tới chi tiết kỹ thuật đủ để dev hành động; một trang, scan 2–3 phút. Thứ tự này là kỷ luật, không phải trang trí.

- 0 — không có tầng lãnh đạo; hoặc mở thẳng bằng chi tiết kỹ thuật (tên metric/hàm/file) rồi mới tới lãnh đạo; hoặc tầng lãnh đạo dày jargon chưa giải nghĩa đến mức CEO đọc xong vẫn không biết on-track hay không.
- 1 — có tầng lãnh đạo đúng thứ tự nhưng khuyết: nhiều hơn 3 con số hoặc lan man quá mức đọc-90-giây; một trong ba artifact thiếu góc nhìn lãnh đạo riêng; còn lẫn thuật ngữ kỹ thuật chưa dịch nghĩa ở tầng trên.
- 2 — tầng lãnh đạo 1–3 con số bằng ngôn ngữ nghiệp vụ, đứng riêng vẫn đủ để CEO/CTO nắm on-track không cần hỏi dev; cả ba artifact giữ thứ tự lãnh-đạo-trước-dev-sau; jargon chỉ xuất hiện từ phần dev trở xuống; toàn bài scan được 2–3 phút.

## 8. CỔNG + BÀN GIAO + LÝ DO/PHƯƠNG ÁN ĐÃ LOẠI — trình cổng, không tự quyết hộ

Hợp đồng: cổng GĐ14 = *"Đạt mục tiêu chưa? Làm gì tiếp?"*; phân vai A5 — chủ sở hữu Ops/SRE + PO, người duyệt CEO/CTO theo nhịp; `operate` KHÔNG tự quyết đầu tư vòng kế, KHÔNG tự tuyên "đạt mục tiêu rồi, dừng", KHÔNG tự chọn item lên roadmap; khối bàn giao đủ khuôn (mục tiêu gốc · học được · item · artifact) + liệt kê các lối đi (`/backlog` · `/review` · `/idea`·`/partner` · `/frame`), không chọn hộ. Mỗi quyết định lớn (nhịp review, ngưỡng alert, chọn metric…) ghi LÝ DO + phương án đã loại. Chế độ tự-quyết phải ghi tường minh ai đóng vai gì.

- 0 — không có khối cổng hoặc khối bàn giao; hoặc tự tuyên "đạt, dừng" / tự chốt đầu tư vòng kế mà không có phân vai lẫn ủy quyền tự-quyết ghi rõ; hoặc bàn giao ép đúng một đường (chỉ `/backlog`, không lối khác); hoặc các quyết định lớn trần — không lý do, không phương án loại.
- 1 — đủ cổng + bàn giao + phân vai nhưng thiếu mảnh: câu hỏi cổng không đúng doc GĐ14; 1–2 quyết định lớn có lý do nhưng không nêu phương án đã loại (hoặc nêu tên mà không nói vì sao loại); bàn giao thiếu một lối đi của khuôn.
- 2 — cổng dùng đúng câu hỏi + phân vai rõ (hoặc tự-quyết ghi tường minh: ai ủy quyền, đóng vai gì, quyết định vẫn audit được); khối bàn giao đủ khuôn + đủ các lối đi để người giữ vai quyết; mọi quyết định lớn có lý do gắn bối cảnh thật + phương án đã loại kèm vì sao loại.

## Luật gate (tiêu chí xương sống)

Tiêu chí 1, 2, 3 là xương sống. Bất kỳ cái nào = 0 → artifact **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 14/16 nhưng có một con số bịa hoặc một câu "đạt rồi" không số chống lưng (tiêu chí 1 = 0) vẫn rớt — vì đây là chỗ CEO quyết đầu tư vòng kế; số ma ở GĐ14 chính là "báo-xong-khống" ở tầng quản trị. Một bản dashboard đẹp nhưng Business không nối ngược được về mục tiêu GĐ1 (tiêu chí 2 = 0) vẫn rớt — vì đóng vòng với cái CEO đã ký là bản chất của GĐ14; mất nó thì operate chỉ còn là giám sát. Một bản đủ mục nhưng không trực được theo nó (tiêu chí 3 = 0) vẫn rớt — vì artifact vận hành mà sự cố xảy ra không biết ai làm gì thì chỉ là văn. Gate quan trọng hơn tổng: khi so nhiều bản, loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Vì sao 8 tiêu chí này

Ba cái đầu là gate vì chúng là ba cách chết của một artifact operate: số không thật (1), số thật nhưng không trả lời được câu CEO ký gì (2), trả lời được nhưng không ai vận hành theo được (3). Hai cái giữa đo *artifact có đúng cái operate hứa không*: đủ ba artifact đúng hình theo luật đủ-là-đủ (4), và vòng học thật sự khép về backlog thay vì dashboard để ngắm (5). Ba cái cuối đo *chỗ đứng và kỷ luật*: kế thừa GĐ13 + đúng vai + không tự kill (6) giữ operate là GĐ14 của pipeline chứ không phải bản giám sát rơi từ trời; đọc-được 3 tầng (7) là lý do skill tồn tại cho người ngoài; cổng + lý do + phương án loại (8) giữ quyền quyết ở CEO/CTO và giữ mọi quyết định audit lại được. Gộp lại = toàn bộ Luật cứng + Thân + Tự soi + Cổng của `operate/SKILL.md`, không hơn. Thêm tiêu chí thứ 9 chỉ khi có một kiểu lỗi thật lặp lại mà 8 cái này không bắt được.
