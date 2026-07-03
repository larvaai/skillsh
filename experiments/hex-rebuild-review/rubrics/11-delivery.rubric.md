# Rubric — 7 tiêu chí chấm artifact GĐ11 delivery (Delivery Standards + DoR/DoD + PR Checklist)

Mỗi tiêu chí 0/1/2. Chuẩn gốc: `delivery/SKILL.md` (3 artifact, luật cứng, cổng GĐ11). Rubric chỉ biến hợp đồng đó thành thước đo được — không thêm tiêu chuẩn mới, không nắn theo bản artifact nào. Khi artifact có claim về hành vi/cấu trúc của code gốc, chuẩn đối chiếu là `/Users/uspro/Desktop/namnson/hex_agent`; khi claim dẫn artifact giai đoạn trước, chuẩn đối chiếu là file pipeline tương ứng trong gói.

## 1. BÁM BẰNG CHỨNG — không bịa, không tự khen (xương sống)

Mọi con số và claim truy được về một nguồn kiểm được: artifact GĐ trước có thật trong gói (module/owner/seam/event/CI/stack), hoặc code gốc `/Users/uspro/Desktop/namnson/hex_agent` (khi nói "bản gốc làm X", "file Y dòng Z"). Số chưa tồn tại (baseline, ngưỡng alert) phải ghi rõ là chưa có + địa chỉ sẽ đo, không được điền số cho đẹp.

- 0 — có claim bịa: nhắc module/owner/seam/API/event không tồn tại trong artifact nguồn; gán hành vi cho code gốc mà code không có; hoặc bịa số (baseline DORA, tỉ lệ, ngưỡng) không nguồn. Bất kỳ claim bịa nào → tiêu chí này 0.
- 1 — đúng phần lớn, nhưng 1–2 claim mơ hồ không dẫn nguồn, hoặc suy đoán không gắn nhãn "chưa chắc / open-Q", hoặc có câu tự khen ("chuẩn này rất vững") không kèm bằng chứng kiểm được.
- 2 — mọi claim có địa chỉ nguồn (GĐ nào / file nào / vị trí nào trong code gốc); chỗ chưa có số ghi tường minh là open question kèm nơi sẽ đo; không có lời tự khen thay cho bằng chứng.

## 2. ĐÚNG-ĐỦ BỘ CHUẨN + DoD LÀ LUẬT (xương sống)

Hợp đồng đòi đúng 3 artifact: Delivery Standards đủ 12 mục (Repository · Branching · Coding standard · Review policy · Testing pyramid · CI/CD · Environment · Secret · Feature flag · Migration · Observability · Incident — chỉ được rút độ sâu, KHÔNG được bỏ mục), DoR + DoD (DoD một khối, không cắt dòng, là luật: "không đạt → không release"), PR Checklist (có ô link story/requirement; ô không áp đánh N/A, không xoá ô).

- 0 — thiếu hẳn 1 trong 3 artifact; hoặc Standards bỏ mục không dấu vết; hoặc DoD bị cắt dòng / hạ thành gợi ý ("nên", "khuyến khích") thay vì luật chặn release; hoặc checklist không có ô link story.
- 1 — đủ 3 artifact nhưng lệch khuôn 1–2 chỗ: mục rủi ro cao (secret/migration/observability) chỉ 1 dòng chung chung trong khi bối cảnh là hệ nhiều team/nhạy cảm; DoD có khối nhưng không tuyên hệ quả; checklist thiếu ô của template.
- 2 — đủ đúng khuôn cả 3; độ sâu tỉ lệ rủi ro (mục rủi ro cao viết kỹ, mục quen gọn — đủ-là-đủ); DoD nguyên khối kèm hệ quả chặn release; checklist đủ ô, ô không áp ghi N/A.

## 3. DÙNG ĐƯỢC THẬT — cầm đi làm được ngay (xương sống)

Người nhận hành động được không cần hỏi lại: dev biết branch thế nào, CI chạy gì theo thứ tự nào, test tối thiểu gồm loại gì tỉ lệ bao nhiêu, PR qua cổng nào, "Done" là gì; CTO/PO đọc đoạn mở là biết giao hàng có on-track không.

- 0 — chuẩn viết bằng tính từ không thao tác được ("test đầy đủ", "review cẩn thận", "log hợp lý") — không có con số, tên, thứ tự, người chịu trách nhiệm; dev đọc xong vẫn phải tự quyết chuẩn.
- 1 — phần lớn thao tác được nhưng 1–2 chuẩn hổng: có tỉ lệ pyramid nhưng không rõ loại test nào cho ranh giới nào; có checklist nhưng ô mơ hồ không biết tick dựa vào gì; có DoD nhưng không rõ ai xác nhận.
- 2 — mỗi chuẩn thao tác được ngay: branching model + giới hạn PR cụ thể, pipeline CI có thứ tự bước và luật chặn, pyramid có tỉ lệ + loại test gắn với rủi ro cụ thể, checklist copy-dùng-được, DoD chỉ rõ ai xác nhận cái gì.

## 4. NỐI CHUỖI PIPELINE — kế thừa, không dựng lại

`delivery` nhận GĐ10 (Module Map + Contract) làm nguồn chính, kế thừa CI/test đã dựng (GĐ8/GĐ7), nối PR về story (GĐ9), và bàn giao sang `uat` (GĐ12). Chuẩn test/PR phải phủ đúng ranh giới của Contract GĐ10 (seam công khai, event cross-module → contract test; review theo owner thật).

- 0 — đứt chuỗi: bịa lại CI/stack khác GĐ7/GĐ8, chuẩn nhắc module/seam không có trong Module Map, review policy không theo owner GĐ10, hoặc không có bàn giao sang `uat`.
- 1 — nối được mạch chính nhưng 1 mắt xích lỏng: ô checklist "update API contract? / ảnh hưởng module khác?" không trỏ vào seam/contract thật; contract test nói chung chung không nêu cặp module; bàn giao có nhưng thiếu thứ `uat` cần (chuẩn test dẫn vào verification).
- 2 — sợi liền hai đầu: ngược (owner/CODEOWNERS = GĐ10, contract test = đúng seam/event GĐ10, CI = GĐ8, stack/test = GĐ7, PR link story = GĐ9) và xuôi (khối bàn giao nói rõ `uat` nhận gì, việc treo nào cần verify).

## 5. LÝ DO + PHƯƠNG ÁN ĐÃ LOẠI — audit được

Mỗi quyết định lớn (repo layout, branching, test pyramid, env, secret, migration, flag, quyết định ở tầng cổng) ghi lý do gắn bối cảnh dự án + phương án đã loại kèm vì sao loại.

- 0 — quyết định lớn trần: chọn branching/pyramid/migration mà không có lý do, hoặc lý do khẩu hiệu ("best practice", "chuẩn ngành") không gắn bối cảnh, và không nêu phương án nào bị loại.
- 1 — phần lớn quyết định có lý do, nhưng 1–2 quyết định lớn thiếu phương án đã loại, hoặc phương án loại nêu tên mà không nói vì sao loại.
- 2 — mọi quyết định lớn audit được: lý do nói bằng bối cảnh thật của dự án (số team, độ nhạy dữ liệu, stack đã chốt), phương án loại có tên + lý do loại cụ thể.

## 6. ĐỌC ĐƯỢC 3 TẦNG — lãnh đạo trước, dev sau

Artifact MỞ bằng Góc nhìn lãnh đạo — khối Definition of Done + 4 chỉ số DORA — bằng ngôn ngữ nghiệp vụ, không jargon; RỒI mới tới chi tiết kỹ thuật cho dev. Đoạn mở đứng riêng vẫn đủ để CEO/CTO biết giao hàng on-track.

- 0 — mở thẳng bằng chi tiết kỹ thuật (pipeline YAML, layout thư mục, tên hàm) hoặc đoạn mở dày jargon đến mức người không đọc code không hiểu; không có Góc nhìn lãnh đạo.
- 1 — có đoạn mở nhưng khuyết: thiếu 1 trong 2 (khối DoD / 4 DORA), hoặc lẫn thuật ngữ nội bộ chưa được giải nghĩa, hoặc dài quá mức đọc-60-giây.
- 2 — đoạn mở gọn, đọc riêng trong ~60 giây hiểu "xong nghĩa là gì + đo sức khoẻ giao hàng bằng gì"; jargon chỉ xuất hiện từ phần dev trở xuống; toàn bài scan được 2–3 phút.

## 7. ĐÚNG VAI + CỔNG ĐÚNG PHÂN VAI

`delivery` đặt CHUẨN + CỔNG, không làm việc skill khác: không code slice/migration script (→ `frame`), không đào bug/edge case (→ `review`), không vẽ lại module (→ `modules`), không chọn lại stack (→ GĐ7), không viết test-result/sign-off (→ `uat`). Cổng GĐ11 trình câu hỏi cổng + bằng chứng + phân vai; AI không tự tuyên pass / tự mở cổng thay CTO — trừ khi có ủy quyền tự-quyết tường minh được ghi lại kèm vai đóng thay.

- 0 — làm việc skill khác (viết code slice, tự sinh migration script, viết test-result, chọn lại stack, vẽ lại module); hoặc tự tuyên GO mà không có khối cổng lẫn ủy quyền ghi rõ.
- 1 — đúng vai chính nhưng lấn nhẹ, hoặc khối cổng thiếu 1 mảnh (thiếu câu hỏi cổng, thiếu bằng chứng trình theo, hoặc phân vai ai-quyết không rõ).
- 2 — đúng vai trọn: chỉ đặt chuẩn + cổng; khối cổng đủ câu hỏi + bằng chứng + phân vai; quyền quyết nằm ở người giữ vai (hoặc chế độ tự-quyết được ghi tường minh: ai ủy quyền, đóng vai gì, lý do quyết định vẫn audit được).

## Luật gate (tiêu chí xương sống)

Tiêu chí 1, 2, 3 là xương sống. Bất kỳ cái nào = 0 → artifact **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 12/14 nhưng bịa seam/số (tiêu chí 1 = 0) vẫn rớt — vì 6 team sẽ build trên chuẩn ma. Một bản văn hay nhưng DoD bị cắt thành gợi ý (tiêu chí 2 = 0) vẫn rớt — vì "Done" mất nghĩa là mất cổng cứng của cả GĐ11. Một bản đủ mục nhưng toàn tính từ (tiêu chí 3 = 0) vẫn rớt — vì chuẩn không thao tác được thì không ai giao hàng theo nó. Gate quan trọng hơn tổng: khi so nhiều bản, loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Vì sao 7 tiêu chí này

Ba cái đầu là gate vì chúng là ba cách chết của một bộ chuẩn delivery: chuẩn bịa (1), chuẩn không còn là luật (2), chuẩn không dùng được (3). Hai cái giữa đo *chỗ đứng trong pipeline*: nối chuỗi (4) giữ delivery là GĐ11 kế thừa GĐ7–10 chứ không phải văn bản rơi từ trời; lý do + phương án loại (5) giữ chuẩn audit được về sau. Hai cái cuối đo *hình dạng hợp đồng*: đọc-được 3 tầng (6) là lý do skill tồn tại cho người ngoài; đúng vai + cổng (7) giữ delivery không code hộ và không tự mở cổng. Gộp lại = toàn bộ hợp đồng của `delivery/SKILL.md`, không hơn. Thêm tiêu chí thứ 8 chỉ khi có một kiểu lỗi thật lặp lại mà 7 cái này không bắt được.
