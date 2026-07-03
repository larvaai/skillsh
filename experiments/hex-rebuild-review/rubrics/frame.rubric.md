# Rubric — 8 tiêu chí chấm một artifact `frame` (đóng khung slice)

Mỗi tiêu chí 0/1/2. Chuẩn gốc: `frame/SKILL.md` (quy tắc bắt buộc + 4 PHASE + EXIT CRITERIA + vòng lặp lõi). Rubric chỉ biến hợp đồng đó thành thước đo được — không thêm tiêu chuẩn mới. Artifact frame là bản đóng khung MỘT slice (Scope/Boundary/Acceptance + Plan/Contract), CHƯA phải code.

Chuẩn đối chiếu khi artifact có claim về code: code gốc tại `/Users/uspro/Desktop/namnson/hex_agent`. Một anchor `file:line` chỉ được tính là đúng khi file tồn tại và đoạn code ở đó thật sự nói điều được gán cho nó.

## 1. MỘT SLICE — đúng một lát, không trôi build cả app (xương sống)

Hợp đồng sống còn của frame: "Đúng MỘT slice một lúc. Mọi thứ chưa làm → Parking Lot, KHÔNG code."

- 0 — scope gộp nhiều hơn một lát cắt có giá trị nhìn thấy (nhiều feature độc lập, nhiều luồng E2E song song); HOẶC không có mục Boundary/OUT; HOẶC có thứ bị đẩy ra ngoài mà không ghi về đâu (parking_lot / slice nào / epic nào). Scope kiểu "build hết A, B, C" → tiêu chí này 0.
- 1 — đúng một slice, nhưng boundary có lỗ: 1–2 thứ ngoài scope thiếu lý do hoặc thiếu đích; hoặc scope IN có 1 mục không phục vụ luồng của chính slice đó.
- 2 — đúng một slice mỏng chạy được E2E; mọi thứ OUT có cả **lý do** lẫn **địa chỉ** (parking_lot, slice kế, backlog item); slice không ôm hạ tầng nặng (DB thật/auth/LLM thật) khi luồng chưa cần.

## 2. CONSTITUTION — non_goals chốt trước, plan không vi phạm

Hợp đồng: "Constitution trước tiên. Chưa chốt non_goals thì KHÔNG phase code nào được chạy."

- 0 — không có non_goals; HOẶC plan/scope đụng thẳng một thứ chính artifact đã liệt là non-goal.
- 1 — có non_goals nhưng chung chung kiểu tính từ ("không làm phức tạp") thay vì hành vi cấm được ("KHÔNG resume", "KHÔNG auth"); hoặc thiếu coding_rules override cho project.
- 2 — non_goals là danh sách hành vi cấm cụ thể (≥3), đặt TRƯỚC plan; coding_rules ghi rõ; đọc plan xong đối chiếu lại không thấy bước nào chạm non-goal.

## 3. ACCEPTANCE ĐO ĐƯỢC — dev/CTO/PO cầm đi làm được ngay (xương sống)

Exit criteria FRAME đòi slice active đủ 4 trường: `user_action`, `system_behavior`, `visible_output`, ≥1 `acceptance`. Acceptance là oracle, không phải lời hứa.

- 0 — AC tường thuật, không có oracle PASS/FAIL ("hệ chạy ổn định", "code sạch"); HOẶC slice thiếu một trong 4 trường trên; HOẶC không chỉ được cách kiểm (chạy gì, nhìn đâu). Người nhận đọc xong vẫn không biết "xong" nghĩa là gì → 0.
- 1 — đa số AC đo được nhưng 1–2 AC mơ hồ, hoặc AC đo được mà thiếu nơi kiểm (loại test / lệnh chạy / file output cần nhìn).
- 2 — mọi AC dạng Given/When/Then (hoặc tương đương) có oracle rõ, mỗi AC chỉ được nơi kiểm; đủ 4 trường slice; một dev không dự cuộc họp nào vẫn dựng đúng và tự chấm PASS/FAIL được.

## 4. CONTRACT-TRƯỚC-CODE — plan tối thiểu, đúng vai frame

Hợp đồng: "Contract trước code", "Code không dùng field ngoài contract", Lock phrases (không over-engineer, không framework chung, không plugin), và ở stage frame thì KHÔNG viết code app.

- 0 — artifact chứa code app (frame chỉ được ra Plan/Contract); HOẶC plan đẻ field/API/seam ngoài contract đã chốt ở stage trước; HOẶC plan có bước over-engineering rõ (framework chung, plugin system, DB/auth khi slice chưa cần).
- 1 — plan đúng ranh giới nhưng còn 1–2 bước mơ hồ (không rõ file/module đích) hoặc thừa so với scope của slice.
- 2 — plan liệt bước cụ thể, mỗi bước gắn module/file đích; chỉ dùng contract/seam đã chốt; tối thiểu — bỏ bất kỳ bước nào là slice hỏng, thêm bước nào cũng là thừa; không một dòng code app.

## 5. FAKE-TRƯỚC-REAL — ranh giới fake/real tường minh

Hợp đồng: "Bản chạy đầu tiên là simulator tất định. KHÔNG gọi LLM thật, KHÔNG DB, KHÔNG auth tới khi slice thật sự cần."

- 0 — slice gọi LLM thật / DB thật / auth khi luồng chưa cần; HOẶC không nói phần nào fake phần nào thật (người build không biết mình đang test luồng hay test model).
- 1 — có fake tất định nhưng ranh giới mờ ở 1 chỗ: không ghi điều kiện nào thì chuyển sang real, hoặc phần "thật" trong slice không nói rõ vì sao được phép thật.
- 2 — ghi tường minh: cái gì fake (và fake tất định — cùng input ra cùng output), cái gì thật và vì sao cần thật ngay, điều kiện/thời điểm chuyển từng phần fake sang real.

## 6. BÁM BẰNG CHỨNG — không bịa, không tự khen, không tick khống (xương sống)

Mọi con số và claim phải có nguồn kiểm được: anchor `file:line` vào code gốc `/Users/uspro/Desktop/namnson/hex_agent`, hoặc trỏ vào artifact stage trước có thật. Ẩn số phải mang nhãn open question, không được kể như đã làm.

- 0 — ≥1 claim bịa: anchor `file:line` không tồn tại hoặc đoạn code đó không nói điều được gán; nhắc artifact/AC/invariant stage trước mà file nguồn không có; tick "đã làm/đã chứng minh" cho thứ slice chưa chạm; tự khen không kèm bằng chứng ("rủi ro thấp" mà không chỉ được vì sao). Bất kỳ claim bịa nào → tiêu chí này 0.
- 1 — đúng phần lớn nhưng 1 chỗ suy đoán không gắn nhãn, hoặc anchor mơ hồ (chỉ tên file không định vị được, số dòng lệch xa).
- 2 — mọi claim truy được về nguồn kiểm được; chỗ chưa chắc gắn nhãn open question rõ ràng kèm nơi sẽ kiểm; không có lời tự khen đứng không.

## 7. GIẢ ĐỊNH & RỦI RO — lộ sáng, có nơi kiểm

Vòng lặp lõi của frame bắt buộc "liệt kê giả định Claude đang ngầm tin" ở mọi cổng.

- 0 — không nêu giả định/rủi ro nào; HOẶC một giả định ngầm quyết định cả scope (vd: "fake plan sẽ khớp parser thật") mà không được nói ra.
- 1 — có nêu nhưng thiếu ràng buộc: rủi ro không có nơi kiểm (AC nào bắt, test nào bắt) hoặc không có hướng giảm.
- 2 — giả định + rủi ro liệt rõ; mỗi cái hoặc có nơi kiểm trong slice (trỏ AC/test cụ thể) hoặc được đẩy thành open question có địa chỉ; rủi ro mang từ boundary sang ghi rõ "KHÔNG gỡ trong slice này".

## 8. CỔNG & BÀN GIAO — quyết định có dấu vết, bước kế rõ

Hợp đồng: mọi cổng kết bằng khối chờ xác nhận đủ 4 trường (hiểu hiện tại / giả định / sẽ đụng file / sẽ KHÔNG) và DỪNG. Ở chế độ tự-quyết, cổng phải thay bằng: quyết định + lý do + phương án đã loại. Xong slice phải chỉ off-ramp (bước kế / skill kế).

- 0 — không có cổng: artifact trôi thẳng từ scope sang plan sang kết mà không có điểm quyết định nào; HOẶC không có bàn giao (đọc xong không biết lượt sau làm gì, bằng skill nào).
- 1 — có cổng nhưng khuyết trường: thiếu phương án đã loại (chế độ tự-quyết) hoặc khối xác nhận thiếu trường (chế độ thường); bàn giao chung chung ("tiếp tục build") không trỏ bước/skill cụ thể.
- 2 — cổng đủ: chế độ thường có khối 4 trường + DỪNG; chế độ tự-quyết có quyết định + lý do + phương án đã loại kèm vì sao loại; bàn giao trỏ đích cụ thể (lượt BUILD theo plan, slice kế, hoặc skill kế trong pipeline) và mang theo open question chưa gỡ.

## Luật gate (tiêu chí xương sống)

Tiêu chí 1, 3, 6 là xương sống. Bất kỳ cái nào = 0 → artifact **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 14/16 nhưng có anchor bịa (tiêu chí 6 = 0) vẫn rớt — vì cả chuỗi stage sau sẽ xây trên claim sai. Một bản văn hay nhưng AC không đo được (tiêu chí 3 = 0) cũng rớt — vì dev cầm về không dựng được, artifact chỉ là văn. Gate quan trọng hơn tổng: khi so nhiều bản frame, loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Vì sao 8 tiêu chí này

Ba cái đầu đo *khung có đúng cái frame hứa không*: một slice (kỷ luật sống còn — lý do skill này tồn tại), non_goals trước tiên, acceptance đo được để người nhận cầm đi làm ngay. Hai cái giữa đo *kỷ luật đường tới code*: contract-trước-code + plan tối thiểu, fake-trước-real. Ba cái cuối đo *có trung thực và có dấu vết không*: bám bằng chứng (mọi claim kiểm được trên code gốc), giả định lộ sáng, cổng + bàn giao có địa chỉ. Gộp lại = toàn bộ hợp đồng của frame cho một artifact đóng khung, không hơn. Thêm tiêu chí thứ 9 chỉ khi có một kiểu lỗi thật lặp lại mà 8 cái này không bắt được.
