# Rubric — 8 tiêu chí chấm một artifact SHAPE (GĐ6 — Solution Architecture)

Mỗi tiêu chí 0/1/2. Chuẩn gốc: `.claude/skills/shape/SKILL.md` (luật cứng + khung artifact + cổng GĐ6). Rubric chỉ biến hợp đồng đó thành thước đo được — không thêm tiêu chuẩn mới, không chép thước của explain sang.

Đối tượng chấm: một file shape (vd `rebuild-hex-agent/pipeline/06-shape.md`). Nguồn đối chiếu:
- Domain Model GĐ5 cùng pipeline (bounded context, rule bất biến, domain event, data ownership, open-Q).
- Requirement/NFR/PRD GĐ2–4 nếu có.
- Khi artifact có claim về code (hành vi, tên cơ chế, known gap): chuẩn đối chiếu là code gốc tại `/Users/uspro/Desktop/namnson/hex_agent`.

## 1. BÁM NGUỒN — mọi claim có nguồn kiểm được, không bịa, không tự khen (xương sống)

Luật gốc: "Bám nguồn" — mọi ranh giới module bám bounded context GĐ5, mọi NFR/security bám Requirement/PRD, NFR thiếu số → open-Q chứ không chế ngưỡng.

- 0 — có ít nhất MỘT claim bịa hoặc không truy được nguồn: module/boundary không nối về bounded context GĐ5 nào; context mới tự đẻ; NFR/ngưỡng số (P95, alert, retention...) không có ở GĐ trước mà vẫn được chốt như đã đòi; claim về code gốc sai khi đối chiếu `hex_agent` (cơ chế/tên/hành vi không tồn tại); hoặc lời tự khen không có bằng chứng kiểm được ("đã đóng mọi rủi ro" mà không chỉ ra đóng ở đâu). Bất kỳ claim bịa nào → tiêu chí này 0.
- 1 — đúng phần lớn nhưng 1–2 chỗ mơ hồ không gắn nhãn: một boundary trace lỏng (nói "bám GĐ5" nhưng không chỉ ra context nào), một con số/known-gap không rõ lấy từ đâu, một suy đoán viết như sự thật.
- 2 — mọi boundary chỉ ra được context GĐ5 tương ứng; mọi con số/NFR/known-gap có địa chỉ nguồn (GĐ5, PRD, hoặc code gốc) và khớp khi kiểm; mảnh thiếu được ghi open-Q rõ ("chưa có số → không bịa") thay vì lấp cho đẹp.

## 2. ĐỦ BỘ ARTIFACT & DÙNG ĐƯỢC NGAY (xương sống)

Luật gốc: "KHÔNG bao giờ bỏ một artifact đã liệt kê — chỉ rút gọn độ sâu. Bỏ artifact là rớt cổng." + câu tự soi "Dev đủ hành động chưa?".

- 0 — thiếu bất kỳ artifact nào trong bộ: Architecture Brief, C4 Context, C4 Container (khi có ≥2 module hoặc tích hợp ngoài — nếu gộp vào Context phải nêu rõ container nào tồn tại), Data Flow, Integration Model, Security Model, ADRs; HOẶC thiếu một trong bốn quyết định tối thiểu style / boundary / integration / auth khiến GĐ7 không có gì để hiện thực; HOẶC ô Brief bỏ trống không lý do (không có dòng "không áp dụng + lý do").
- 1 — đủ bộ nhưng có artifact mỏng hơn rủi ro nó phải đỡ: C4 Container chỉ liệt tên khối không nói giao thức giữa khối; Security chỉ một dòng trong khi dữ liệu nhạy/có delegation; 1–2 ô Brief nói nước đôi ("tùy trường hợp") thay vì quyết.
- 2 — đủ bộ, mỗi ô Brief là một quyết định đọc được hoặc "không áp dụng + lý do 1 dòng"; độ sâu tỉ lệ rủi ro (Đủ-là-đủ: ô rủi ro thấp vài chữ, ô rủi ro cao có phân tích); người nhận (dev/CTO chuẩn bị GĐ7) đọc xong biết module nào sở hữu gì, nối nhau ra sao, chặn ai bằng gì — cầm đi chọn stack được ngay.

## 3. ĐÚNG VAI GĐ6 — architecture trước, framework sau (xương sống)

Luật gốc: nguyên tắc cốt A3-#2 + "Không lấn vai" + điều 4 của cổng ("không tên framework nào bị chốt lén").

- 0 — có tên framework/DB/lib/dịch vụ cụ thể bị CHỐT như một quyết định trong Brief hoặc ADR (vd "dùng NestJS/Postgres/LangGraph" đứng ở ô Quyết định); HOẶC lấn vai GĐ khác: hỏi lại/quyết lại WHY-WHAT-MVP (GĐ1–4), vẽ lại domain (GĐ5), viết code hay cắt slice (GĐ8+).
- 1 — không chốt lén nhưng có chỗ mấp mé: tên công nghệ cụ thể xuất hiện mà không gắn nhãn "mức loại" / "hiện trạng code cũ" / "việc GĐ7"; hoặc một câu trả lời non cho câu hỏi thuộc GĐ khác thay vì ghi open-Q chuyển đúng chỗ.
- 2 — công nghệ chỉ nêu ở mức LOẠI (in-process module, embedded relational store, vector store...); tên cụ thể nếu buộc phải nhắc chỉ đứng như ràng buộc/hiện trạng có nhãn kèm ghi chú "chốt cụ thể = GĐ7"; mọi câu thuộc GĐ khác thành open-Q có địa chỉ chuyển tiếp.

## 4. ĐỌC-ĐƯỢC-3-TẦNG — góc nhìn lãnh đạo đứng trước

Luật gốc: "Hợp đồng đọc-được-3-tầng (lý do skill tồn tại)" — mở bằng 1–3 thứ CEO/CTO nhìn để biết on-track, ngôn ngữ nghiệp vụ, rồi mới chi tiết dev; scan 2–3 phút.

- 0 — không có khối Góc nhìn lãnh đạo mở đầu, hoặc đoạn mở đầu dày jargon kỹ thuật (tên class/pattern chưa được neo nghĩa) khiến người nghiệp vụ đọc không ra "hệ có hình gì, vì sao hình đó hợp rủi ro"; hoặc chi tiết dev đứng trước phần lãnh đạo.
- 1 — có Góc nhìn lãnh đạo nhưng lệch: nhiều hơn 3 điều "nhìn để biết on-track", lẫn jargon chưa giải nghĩa, hoặc một số sơ đồ/bảng bên dưới không có diễn giải phẳng đi kèm (bắt lãnh đạo tự đoán mũi tên).
- 2 — mở bằng đúng 1–3 điều on-track bằng ngôn ngữ nghiệp vụ; mỗi sơ đồ C4/luồng có 1–2 câu diễn giải phẳng; đọc lướt 2–3 phút nắm được hình hài + rủi ro lớn nhất + vì sao hình này; chi tiết kỹ thuật đủ cho dev nằm SAU, không trộn ngược.

## 5. ADR — quyết định thật, có phương án đã loại

Luật gốc: "Không có phương án đã loại → chưa phải quyết định, chỉ là mặc định" + Đủ-là-đủ: tối thiểu ADR cho style, boundary, integration lớn, data ownership.

- 0 — một quyết định lớn (style / boundary / data ownership / integration lớn) không có ADR; HOẶC có ADR nhưng thiếu mục Phương án đã loại / thiếu VÌ SAO loại; HOẶC ADR chứa tên framework như quyết định (dính cả tiêu chí 3).
- 1 — đủ ADR cho các quyết định lớn nhưng có ADR yếu: phương án đã loại là bù nhìn (một dòng, không lý do thật, không ai từng cân nhắc nghiêm túc), hoặc Hệ quả chỉ toàn điểm được — không có mặt trái/đánh đổi nào.
- 2 — mỗi quyết định lớn một ADR đủ ô: Bối cảnh nêu ràng buộc truy được về Domain/NFR; Quyết định rõ; Phương án đã loại kèm lý do thật; Hệ quả có cả được lẫn mất; đọc danh sách ADR là dựng lại được "vì sao hệ thống có hình này".

## 6. DATA FLOW & DATA OWNERSHIP — gắn domain event, chủ dữ liệu rõ

Luật gốc: Data Flow "gắn mỗi bước vào một domain event GĐ5, bám data ownership GĐ5" + điều 2 của cổng ("data ownership rõ, không mơ hồ 'ai cũng đọc được'").

- 0 — Data Flow kể chung chung không gắn domain event GĐ5 nào (hoặc gắn event tự chế không có ở GĐ5); HOẶC data ownership mơ hồ: không nói module nào sở hữu state/bảng/luồng nào, hoặc mặc định "ai cũng đọc được".
- 1 — có gắn event và có chủ dữ liệu, nhưng 1–2 bước lệch (bước không nêu ai sở hữu dữ liệu tại bước đó; một loại dữ liệu không rõ chủ; luật cấm cross-module đọc/ghi trực tiếp không được nêu dù đã tách ownership).
- 2 — mỗi bước của luồng chính gắn đúng một domain event GĐ5 và nêu chủ dữ liệu tại bước đó; mọi loại dữ liệu/state có đúng một module sở hữu; ranh giới đọc/ghi (đi qua port, cấm cross-module trực tiếp) ghi thành luật.

## 7. INTEGRATION & SECURITY — biết ai chịu lỗi, chặn ai bằng gì

Luật gốc: Integration Model "mỗi tích hợp một dòng — pattern, đồng bộ/bất đồng bộ, ai chịu lỗi khi bên kia sập, retry/timeout/fallback, ai sở hữu contract" + Security Model "phân loại dữ liệu + auth model + audit + STRIDE gọn cho đường vào chính".

- 0 — một tích hợp ra ngoài (có mặt trong C4 Context) vắng khỏi Integration Model, hoặc có mặt nhưng không nói ai chịu lỗi khi bên kia sập/không có retry-timeout-fallback; HOẶC Security thiếu auth model (ai làm được gì) — dev không biết chặn ai bằng gì.
- 1 — đủ các đường tích hợp và có auth model, nhưng thiếu ô lẻ: một dòng integration thiếu sync/async hoặc chủ contract; security thiếu một lớp so với độ nhạy dữ liệu (không phân loại dữ liệu, không nói audit, hoặc dữ liệu nhạy/đường rủi ro cao mà không có threat model).
- 2 — mỗi tích hợp một dòng đủ 5 ô; open-Q integration còn treo từ GĐ trước được chốt tại đây hoặc ghi treo có địa chỉ; Security đủ theo rủi ro: phân loại dữ liệu + auth model (role↔quyền) + audit (cái gì bất biến) + STRIDE cho đường rủi ro nhất khi dữ liệu nhạy/nhiều tích hợp.

## 8. CỔNG & BÀN GIAO — go/no-go có kiểm, handoff có ràng buộc

Luật gốc: mục "Cổng go/no-go + AI duyệt" (kiểm 4 điều, câu hỏi cổng chuẩn) + mục "Bàn giao sang stack" (hình đã chốt, ràng buộc cho stack, open-Q chuyển tiếp, chỉ liệt kê không chọn hộ).

- 0 — không có khối cổng GĐ6; hoặc cổng không kiểm 4 điều mà vẫn tuyên GO; hoặc tự trôi sang GĐ7 (tự chốt stack/framework hộ trong phần bàn giao); hoặc bàn giao không có ràng buộc nào cho stack.
- 1 — có cổng + bàn giao nhưng hụt: thiếu câu hỏi cổng chuẩn ("Architecture đủ vững để chọn stack & dựng live slice chưa?"), quyết định cổng không nêu lý do, ràng buộc cho stack chung chung ("chọn gì cũng được"), hoặc open-Q chuyển tiếp không có địa chỉ (không rõ GĐ nào trả lời).
- 2 — khối cổng đủ: 4 điều duyệt được kiểm từng điều, câu hỏi cổng chuẩn, quyết định GO/NO-GO kèm lý do; bàn giao nêu hình đã chốt + ràng buộc cụ thể kiểm được cho stack + open-Q chuyển tiếp có địa chỉ; các lối đi tiếp chỉ liệt kê, không chọn hộ.

## Luật gate

Tiêu chí 1, 2, 3 là xương sống. Bất kỳ cái nào = 0 → artifact **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 14/16 nhưng có một boundary bịa không trace về GĐ5 (tiêu chí 1 = 0) vẫn rớt — vì mọi GĐ sau (stack, skeleton, backlog) sẽ xây trên ranh giới không có thật. Một bản văn hay nhưng thiếu Security Model (tiêu chí 2 = 0) vẫn rớt — hợp đồng nói thẳng "bỏ artifact là rớt cổng". Một bản chốt lén framework (tiêu chí 3 = 0) vẫn rớt — nó đã làm hộ việc của GĐ7 mà không qua tiêu chí có điểm của `stack`. Gate quan trọng hơn tổng: khi so nhiều bản shape, loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Vì sao 8 tiêu chí này

Ba cái đầu là ba điều sống còn của hợp đồng shape: **trung thực** (bám nguồn — mọi con số và ranh giới truy được về GĐ5/PRD/code gốc, không bịa, không tự khen), **đủ để dùng** (đủ bộ artifact, người nhận cầm đi chọn stack được ngay), và **đúng vai** (chốt HÌNH, không chốt CÔNG CỤ). Bốn cái giữa (3-tầng, ADR, data flow/ownership, integration/security) đo từng khối nội dung mà hợp đồng bắt artifact phải có — mỗi khối một thước riêng vì mỗi khối hỏng một kiểu khác nhau. Cái cuối (cổng & bàn giao) đo kỷ luật pipeline: shape không đứng một mình, nó phải qua cổng có kiểm và trao tay sạch cho GĐ7. Gộp lại = toàn bộ hợp đồng của shape, không hơn. Thêm tiêu chí thứ 9 chỉ khi có một kiểu lỗi thật lặp lại mà 8 cái này không bắt được.
