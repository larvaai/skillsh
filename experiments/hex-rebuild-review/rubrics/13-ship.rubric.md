# Rubric — 8 tiêu chí chấm artifact GĐ13 `ship` (Go/No-Go + Runbook + Rollback + Rollout)

Mỗi tiêu chí 0/1/2, tổng tối đa 16. Chuẩn gốc DUY NHẤT: `ship/SKILL.md` (Luật cứng · Thân 4 artifact · Tự soi · Cổng GO/NO-GO). Rubric chỉ biến hợp đồng đó thành thước đo được — không thêm chuẩn mới. Khi artifact có claim về code, chuẩn đối chiếu là code gốc tại `/Users/uspro/Desktop/namnson/hex_agent`; claim về sign-off/kết quả test đối chiếu artifact GĐ12 (`pipeline/12-uat.md`) và các artifact GĐ trước được viện dẫn.

## 1. BẰNG CHỨNG — mọi con số & chữ ký có nguồn kiểm được, không bịa, không tự khen (xương sống)

Hợp đồng: "UAT+Security sign-off KÉO từ GĐ12 (không bịa 'đã ký')", "mảnh nào chưa có thì ghi thành giả định/open-Q, KHÔNG bịa là đã ký cho đủ".

- 0 — có BẤT KỲ một claim bịa: nâng chữ ký "ký-có-điều-kiện" thành "đã ký" trơn / bỏ rơi điều kiện của chữ ký; ghi "rollback đã test" mà không trỏ được test nào, chạy ở đâu, ngày nào; nêu tên hàm/file/flag/metric không tồn tại trong code gốc hoặc artifact nguồn; con số tóm tắt (vd "n/m dòng xanh") lệch với bảng thật khi đếm lại. Một claim bịa → tiêu chí này 0.
- 1 — đúng phần lớn nhưng còn 1 chỗ suy đoán/mơ hồ không gắn nhãn (vd "monitoring đã bật" mà không nói metric nào, đọc ở file nào; trích số test không ghi lấy từ GĐ12 hay tự đếm).
- 2 — mọi con số, chữ ký, trạng thái checklist trỏ được về nguồn (GĐ12/GĐ11/GĐ8/code gốc — có địa chỉ file/mục); chữ ký có điều kiện thì điều kiện đó đi theo suốt trang (thành rollout gate / dòng chặn), không rơi rớt; mảnh chưa có ghi tường minh "CHƯA CÓ / open-Q + địa chỉ ai đóng". Tự khen ("đã đầy đủ", "rất an toàn") không được tính là bằng chứng — mục Tự soi không thay được nguồn.

## 2. ĐỦ BỘ — 4 artifact trên một trang + 12 ô checklist, ô không dùng ghi N/A + lý do

Hợp đồng: "KHÔNG bao giờ bỏ một trong bốn artifact hay bỏ ô nào của checklist — chỉ rút gọn độ sâu; ô không áp dụng ghi N/A + lý do, không xoá."

- 0 — thiếu hẳn một trong bốn artifact (Go/No-Go · Rollback · Runbook · Rollout), hoặc checklist bị xoá ô (đếm không đủ 12 hạng mục của template).
- 1 — đủ 4 artifact + 12 ô nhưng có ô thiếu owner hoặc thiếu trạng thái, hoặc có ô N/A không kèm lý do; hoặc độ sâu không theo rủi ro (hệ đụng tiền/quyền/dữ liệu mà artifact mỏng như vá copy, không ghi vì sao dám rút gọn).
- 2 — đủ 4 artifact ghép một trang; 12/12 ô mỗi ô có hạng mục + owner cụ thể (tên người/team thật, không "TBD") + trạng thái `[x]`/`[ ]`/N/A; mọi N/A có lý do riêng cho ô đó; độ sâu từng phần tỉ lệ rủi ro và chỗ rút gọn có ghi lý do dám.

## 3. BỐN THỨ CHẶN — trạng thái THẬT của rollback · monitoring/alert · incident owner · sign-off (xương sống)

Hợp đồng: "Cổng chặt: khuyết là NO-GO. Bốn thứ không thương lượng — rollback (đã test nếu hệ quan trọng) · monitoring/alert đã bật · incident owner đã có tên · UAT + Security sign-off từ GĐ12. Thiếu một → NO-GO, không 'cho lên rồi vá sau'."

- 0 — thiếu một trong bốn mà artifact vẫn khuyến nghị GO không kèm điều kiện; HOẶC một trong bốn được ghi "xong" nhưng ruột rỗng khi soi (incident owner không có tên; "monitoring bật" không có metric/alert nào; hệ quan trọng mà rollback chưa test và điều đó không được nêu thành dòng chặn).
- 1 — đủ bốn thứ nhưng ≥1 cái trạng thái mơ hồ: rollback "sẽ test", alert có metric nhưng không có tín hiệu nào là "hỏng → lùi", phần treo (vd ngưỡng số chưa đo) không được đánh dấu tường minh.
- 2 — bốn thứ đều có trạng thái thật + kiểm được: rollback nói rõ đã test bằng gì/phạm vi nào (và phần CHƯA test được khoanh vùng); monitoring liệt kê metric/alert cụ thể + cái gì là alert cứng; incident owner có tên theo phân công thật; sign-off kéo nguyên trạng từ GĐ12. Mọi phần khuyết/treo được biến thành điều kiện chặn hoặc rollout gate, không giấu, không "vá sau".

## 4. DÙNG ĐƯỢC NỬA ĐÊM — Runbook + Rollback thao tác được không cần đoán, không cần tác giả (xương sống)

Hợp đồng: "Cụ thể tới mức người KHÁC (không phải tác giả) làm theo được lúc nửa đêm"; Rollback trả lời đủ 3 câu: tín hiệu nào thì lùi · lùi bằng cách nào · dữ liệu sinh ra trong lúc lỗi xử lý sao.

- 0 — runbook chỉ mô tả ý định ("deploy rồi kiểm tra, có vấn đề thì rollback") — không lệnh/bước/ngưỡng, người trực phải gọi tác giả mới làm được; hoặc Rollback Plan bỏ trống ≥1 trong 3 câu bắt buộc.
- 1 — có 3 khối đánh số (deploy → kiểm-sau-deploy → rollback) nhưng thiếu ≥1 trong: "kỳ vọng thấy gì" cho từng bước smoke · ngưỡng/tín hiệu "hỏng → rollback ngay" · ai bấm rollback · bước rollback trong Runbook khớp Rollback Plan; hoặc lệnh/đường dẫn chung chung không trỏ đúng seam/config thật của hệ.
- 2 — ba khối đánh số bước; mỗi bước kiểm-sau-deploy có kỳ vọng quan sát được (endpoint/metric/file nào phải ra gì); tín hiệu lùi liệt kê rõ và khớp giữa Runbook và Rollback Plan; ai bấm ghi theo vai thật; lệnh/file/flag dùng đúng tên tồn tại trong code gốc hoặc artifact nguồn; câu "dữ liệu lúc lỗi" nói rõ giữ/migrate ngược/bỏ và điểm không-lùi-được (nếu có).

## 5. ĐỌC 3 TẦNG — Góc nhìn lãnh đạo MỞ trang, đứng riêng vẫn quyết được

Hợp đồng: "Mọi artifact PHẢI mở bằng Góc nhìn lãnh đạo (ĐÚNG 1–3 thứ CEO/CTO nhìn để bấm GO: sẵn sàng chưa · ký cái gì · rủi ro tệ nhất + ai lo), ngôn ngữ nghiệp vụ, không jargon; rồi mới tới chi tiết kỹ thuật. Một trang, scan 2–3 phút."

- 0 — không có khối lãnh đạo mở đầu (trang mở thẳng bằng checklist/lệnh kỹ thuật), hoặc khối mở đầu đòi hiểu jargon nội bộ chưa được giải nghĩa (tên hàm, tên bảng, thuật ngữ hạ tầng trần) mới đọc nổi.
- 1 — có khối mở đầu nhưng thiếu một trong ba câu (sẵn sàng chưa · ký cái gì · hỏng thì lùi ra sao + ai trực), hoặc lãnh đạo vẫn phải đọc xuống phần dev mới trả lời được một trong ba câu, hoặc jargon lọt vài chỗ không giải nghĩa.
- 2 — đủ ba câu ngay đầu trang bằng ngôn ngữ nghiệp vụ; nói rõ phạm vi ký (ký cho cái gì, KHÔNG ký cho cái gì); đọc RIÊNG khối này trong 2–3 phút là bấm GO/NO-GO được mà không cần mở runbook hay hỏi dev.

## 6. LÝ DO + PHƯƠNG ÁN ĐÃ LOẠI — cho mỗi quyết định lớn

Hợp đồng: "Mỗi quyết định lớn ghi LÝ DO + phương án đã loại... Để sau audit được vì sao dám cho lên." Bốn quyết định lớn tối thiểu của trang SHIP: kiểu triển khai (blue-green/canary/rolling/flag) · cách rollback · nhịp rollout (mấy bậc, gộp hay không) · khuyến nghị GO/NO-GO/GO-có-điều-kiện.

- 0 — ≥1 trong bốn quyết định lớn để trần: chọn mà không ghi lý do.
- 1 — mọi quyết định lớn có lý do nhưng ≥1 cái thiếu phương án đã loại, hoặc phương án loại chỉ được nêu tên mà không nói vì sao loại.
- 2 — cả bốn quyết định có lý do + phương án đã loại + vì sao loại; lý do bám đặc thù thật của hệ (kiến trúc, dữ liệu, giai đoạn) chứ không phải lý do generic dán vào hệ nào cũng đúng.

## 7. ROLLOUT CÓ BẬC — mỗi bậc một cổng nhỏ có tín hiệu đo được

Hợp đồng: bậc thang "internal alpha → pilot → beta → gradual → full"; mỗi bậc ghi ai/phạm vi · quan sát bao lâu · tín hiệu tiến/dừng · đường lùi ở bậc đó; gộp/bỏ bậc phải ghi lý do dám.

- 0 — rollout full ngay không ghi lý do, hoặc bậc thang chỉ là danh sách tên bậc không có nội dung (không tín hiệu, không đường lùi).
- 1 — có bậc nhưng ≥1 bậc thiếu tín hiệu tiến/dừng quan sát được (chỉ "theo dõi thấy ổn thì lên") hoặc thiếu đường lùi riêng của bậc; hoặc gộp/bỏ bậc không ghi lý do.
- 2 — mỗi bậc đủ bốn cột: phạm vi/ai · quan sát bao lâu · tín hiệu tiến/dừng cụ thể (metric, điều kiện, kết quả test có tên) · đường lùi; số bậc và cách chia bậc có lý do theo rủi ro; điều kiện mở bậc kế nối được về đúng blocker/điều kiện còn treo ở nguồn (GĐ12) nếu có.

## 8. ĐÚNG VAI & CỔNG ĐÚNG PHÂN QUYỀN — ship không tự bấm GO, NO-GO không phủ định cứng, bàn giao đúng

Hợp đồng: "`ship` KHÔNG tự bấm GO — chuẩn bị đủ + khuyến nghị, CTO+PO quyết"; "Không lấn vai" (không code tính năng, không kiểm lại chất lượng test GĐ12, không dựng ops dashboard dài hạn); "NO-GO luôn kèm điều kiện để chuyển thành GO — thiếu gì · ai làm · bao lâu"; kết bằng khối bàn giao "chỉ liệt kê, không tự chọn hộ".

- 0 — lấn vai rõ (viết/sửa code tính năng; chấm lại/kiểm lại kết quả test của GĐ12 thay vì nhận nguyên; dựng ops dashboard dài hạn của GĐ14); HOẶC ship tự bấm GO — không trình khối cổng, không tách khuyến nghị khỏi quyết định, quyết định không có người ký + vai; HOẶC dùng phủ định cứng ("không được deploy", "không thể lên") không kèm điều kiện chuyển GO.
- 1 — đúng vai nhưng lệch nhẹ: khối cổng thiếu thành phần (sẵn sàng / còn chặn / rollout / khuyến nghị + lý do); điều kiện chuyển GO có "thiếu gì" nhưng thiếu "ai làm / bao lâu"; bàn giao thiếu hoặc chọn hộ user bước kế.
- 2 — trình cổng đủ khối; khuyến nghị (của ship) và quyết định (của Người duyệt) tách bạch — nếu chạy chế độ tự-quyết thì ghi rõ ai đóng vai Người duyệt + ngày ký, không để ship ký ẩn danh; mọi dòng chặn/điều kiện có địa chỉ đủ ba mảnh thiếu gì · ai · xong khi nào; kết bằng khối bàn giao sang `operate` chỉ liệt kê lựa chọn.

## Luật gate

Tiêu chí 1, 3, 4 là xương sống. Bất kỳ cái nào = 0 → artifact **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một trang 14/16 nhưng nâng chữ ký có-điều-kiện thành đã-ký-trơn (tiêu chí 1 = 0) vẫn rớt — vì CTO sẽ ký GO trên nền giả. Tương tự: bốn thứ chặn rỗng ruột (tiêu chí 3 = 0) nghĩa là hợp đồng "khuyết là NO-GO" bị phá; runbook không thao tác được (tiêu chí 4 = 0) nghĩa là lúc 2 giờ sáng người trực đoán mò — đúng cái mà GĐ13 tồn tại để tránh. Gate quan trọng hơn tổng: khi so nhiều bản, loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Vì sao 8 tiêu chí này

Ba cái đầu tiên trong nhóm sự-thật (1, 2, 3) đo *trang này có phải sự thật đủ để ký không* — bằng chứng có nguồn, đủ bộ 4 artifact + 12 ô, và bốn thứ chặn có trạng thái thật. Hai cái giữa (4, 5) đo *hai người đọc chính có dùng được không* — dev trực cầm đi thao tác lúc nửa đêm, lãnh đạo đọc 3 phút là quyết được. Ba cái cuối (6, 7, 8) đo *quyết định có audit được và đúng phân vai không* — lý do + phương án loại, rollout chia rủi ro có cổng nhỏ, và cổng GO thuộc về người duyệt chứ không phải AI. Gộp lại = toàn bộ hợp đồng của `ship`, không hơn. Thêm tiêu chí thứ 9 chỉ khi có một kiểu lỗi thật lặp lại mà 8 cái này không bắt được.
