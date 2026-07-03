# Rubric — 8 tiêu chí chấm một Test & Verification Report (GĐ12 · uat)

Mỗi tiêu chí 0/1/2. Chuẩn gốc: `.claude/skills/uat/SKILL.md` (hợp đồng GĐ12 — bảng mapping 5 mắt, hai chữ ký, đọc-được 3 tầng, Đủ-là-đủ, ranh giới vai). Rubric chỉ biến hợp đồng đó thành thước đo được — không thêm tiêu chuẩn mới, không mượn tiêu chí của explain.

Khi artifact có claim về code/test (tên file, số dòng, tên test suite): chuẩn đối chiếu là code gốc tại `/Users/uspro/Desktop/namnson/hex_agent`. Trích dẫn không đối chiếu được = claim bịa.

Thang: mỗi tiêu chí 0 / 1 / 2 · tổng tối đa 16 · 3 tiêu chí xương sống (gate) — xem "Luật gate" cuối file.

## 1. BẰNG CHỨNG — kết quả test không bịa, mọi con số kiểm được (xương sống)

`uat` bán đúng một thứ: bằng chứng thật. PASS chỉ được đánh khi test thật đã chạy xanh; số liệu phải có nguồn.

- 0 — có ít nhất một kết quả/con số không có nguồn kiểm được: đóng dấu PASS cho code/test chưa chạy; pass-rate ở khối lãnh đạo không khớp với đếm dòng trong bảng mapping; trích test file / số dòng / tên hàm không tồn tại trong code gốc `/Users/uspro/Desktop/namnson/hex_agent`; hoặc tự khen ("đã test đầy đủ", "an toàn tuyệt đối") không kèm bằng chứng. Bất kỳ claim bịa nào → tiêu chí này 0.
- 1 — mọi kết quả có nguồn nhưng 1–2 chỗ mơ hồ không gắn nhãn: không phân biệt rõ "test đã chạy xanh" với "test mới định nghĩa/kế thừa harness", hoặc một con số lệch nhỏ giữa các khối (lãnh đạo · mapping · cổng) chưa được giải thích.
- 2 — mọi PASS ứng với test đã chạy thật; code chưa chạy → PENDING/BLOCKED nói thẳng kèm lý do trạng thái; mọi con số (tổng AC, pass, pending, fail) cộng khớp nhau ở cả ba khối; mọi trích dẫn code/test đối chiếu được với code gốc; chỗ chưa chắc được gắn nhãn rõ.

## 2. MAPPING 5 MẮT — sợi truy vết liền, không chế yêu cầu (xương sống)

Xương của artifact: `Requirement → Acceptance Criteria → Test Case → Test Result → Release Decision`, mỗi AC một dòng, Requirement/AC TRÍCH từ artifact giai đoạn trước.

- 0 — thiếu hẳn bảng mapping; hoặc mắt xích đứt hàng loạt (AC không nối về Requirement nguồn, TC không có Result, Result không có Release Decision); hoặc Requirement/AC tự chế — không trích được về backlog/PRD/DoD của giai đoạn trước; hoặc AC chưa có test bị im lặng bỏ qua (không đánh dấu hở).
- 1 — bảng có đủ 5 mắt cho phần lớn dòng nhưng vài dòng thiếu 1 mắt (vd Release Decision để trống), hoặc 1–2 AC không chỉ ra được nguồn gốc (story/requirement nào).
- 2 — mỗi AC trong phạm vi một dòng đủ 5 mắt; Requirement/AC có địa chỉ nguồn cụ thể (mã story, file pipeline GĐ trước); AC chưa có test → để trống Test Case + đánh dấu hở (gap) rõ ràng + trỏ `/review`, không im lặng, không tự moi case mới rồi coi như đủ.

## 3. HAI CHỮ KÝ + DÙNG ĐƯỢC NGAY (xương sống)

Report chưa có đường tới hai chữ ký, hoặc người nhận đọc xong không biết làm gì tiếp = chưa phải artifact GĐ12.

- 0 — thiếu hẳn một trong hai mục sign-off (UAT của PO / Security của Sec-CISO); hoặc AI tự ký thay người thật như chuyện đã rồi mà không ghi vai-ngày-điều kiện; hoặc điều kiện go-live nói chung chung đến mức dev/PO/CTO cầm report không biết việc tiếp theo là gì (không trỏ TC, flag, hạng mục cụ thể nào).
- 1 — có đủ hai mục sign-off với trạng thái, nhưng 1 chữ ký thiếu ai/ngày/điều kiện; hoặc điều kiện go-live có nhưng một phần chung chung ("cần thêm test") không có địa chỉ TC/việc cụ thể.
- 2 — cả UAT sign-off + Security sign-off có trạng thái rõ (đã ký / ký có điều kiện / CHỜ, kèm vai + ngày + điều kiện); chữ ký treo ghi rõ đang chờ ai; mọi điều kiện go-live trỏ đúng TC/flag/việc có địa chỉ — dev biết phải làm test nào xanh, PO/CTO biết đang chặn ở đâu, `ship` nhận được điều kiện dùng được ngay.

## 4. ĐỌC-ĐƯỢC 3 TẦNG — lãnh đạo trước, dev sau

- 0 — không có khối Góc nhìn lãnh đạo mở đầu, hoặc mở thẳng bằng bảng kỹ thuật/jargon; đọc riêng khối đầu không trả lời được "cho lên được chưa".
- 1 — có khối lãnh đạo mở đầu nhưng lẫn jargon kỹ thuật (mã TC, tên test file, số dòng code) hoặc thiếu 1 trong 3 thứ bắt buộc: tỷ lệ pass · trạng thái hai chữ ký · một dòng "còn hở gì".
- 2 — mở bằng khối lãnh đạo đủ 3 thứ (tỷ lệ pass · hai chữ ký · còn hở gì) bằng ngôn ngữ nghiệp vụ, đọc riêng ~90 giây là biết có nên cho lên không; chi tiết mapping + lớp test cho dev nằm sau; toàn artifact scan được 2–3 phút.

## 5. ĐỦ-LÀ-ĐỦ — lớp test theo rủi ro, bỏ có lý do

- 0 — bỏ một lớp test mà không ghi lý do (im lặng bỏ); hoặc nhồi lớp hệ không cần chỉ để bảng trông đầy (vd pentest/DR đầy đủ cho slice nội bộ chưa expose); hoặc chọn lớp không ăn nhập mức rủi ro (hệ đụng tiền/quyền/secret mà chỉ unit happy-path).
- 1 — bộ lớp hợp lý phần lớn nhưng 1 lớp bỏ/hoãn thiếu lý do, hoặc lý do bỏ không nối về mức rủi ro của hệ.
- 2 — bộ lớp test khớp rủi ro hệ (hệ quan trọng → đủ lớp chứng minh mạnh: property/adversarial/contract; slice nhỏ → tối thiểu unit+integration+UAT); mỗi lớp bỏ/hoãn/N-A có đúng 1 dòng lý do; không lớp thừa cho có.

## 6. RANH GIỚI — đúng vai uat

- 0 — lấn vai rõ: tự đào gap/edge case mới rồi coi như đã đủ (việc `review`); sửa hoặc chỉ đạo sửa code cho test xanh (việc `frame`/`delivery`); tự quyết deploy/Go-No-Go cuối thay `ship`.
- 1 — chủ yếu đúng vai, lấn nhẹ 1–2 chỗ (vd chèn gợi ý fix code cụ thể vào dòng mapping).
- 2 — chỉ tổng hợp bằng chứng + chuẩn bị hai chữ ký + nêu điều kiện đủ để trình ký; gap → trỏ `/review`; AC fail cần sửa code → trỏ `/frame`; quyết deploy cuối → trỏ `/ship`.

## 7. LÝ DO + PHƯƠNG ÁN ĐÃ LOẠI — audit lại được

- 0 — quyết định lớn (Release Decision, quyết cổng, bỏ/hoãn lớp test) không có lý do; hoặc không một quyết định lớn nào ghi phương án đã loại.
- 1 — quyết định lớn có lý do nhưng phương án đã loại chỉ xuất hiện ở một phần, hoặc lý do loại chung chung ("không cần thiết") không giải thích vì sao.
- 2 — mỗi quyết định lớn ghi lý do + ít nhất một phương án đã loại kèm vì sao loại — người sau audit lại được đường ra quyết định.

## 8. CỔNG & BÀN GIAO — có lối đi, không phủ định cứng, không chọn hộ

- 0 — thiếu khối cổng GO/NO-GO hoặc khối bàn giao sang `ship`; hoặc dùng phủ định cứng trơ trọi ("không go được", "fail là hết") không kèm lối đi; hoặc tự chọn hộ user skill chạy tiếp.
- 1 — có đủ hai khối nhưng thiếu trường (pass · gap · hai chữ ký · câu trả lời "đủ điều kiện go-live?"), hoặc còn chỗ phán chết một AC/kết quả mà không kèm lối đi.
- 2 — khối cổng đủ trường và trả lời thẳng câu hỏi cổng (đủ / go-live có điều kiện / chưa — cần gì); khối bàn giao liệt kê các lối đi (`/ship`, `/review`, `/frame`) để user chọn; mọi FAIL/thiếu/treo đều kèm đúng một lối đi tiếp (fix + re-test / tách scope / go-live có điều kiện / chuyển skill).

## Luật gate

Tiêu chí 1, 2, 3 là xương sống. Bất kỳ cái nào = 0 → artifact **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một report 14/16 nhưng có một dấu PASS bịa (tiêu chí 1 = 0) vẫn rớt — vì CTO sẽ cho lên production dựa trên con số không có thật. Gate quan trọng hơn tổng: khi so nhiều bản, loại hết bản rớt gate trước, rồi mới xếp theo tổng.

Vì sao chọn 3 cái này làm xương sống:
- **Tiêu chí 1 (bằng chứng)** — cả artifact là một tờ bằng chứng; một số bịa làm mất giá toàn bộ tờ giấy, và là kiểu lỗi nguy hiểm nhất vì người đọc không tự kiểm được.
- **Tiêu chí 2 (mapping 5 mắt)** — điều sống còn nhất trong hợp đồng skill: SKILL.md gọi đây là "xương của artifact — không có là sau khó audit"; đứt sợi truy vết thì report chỉ còn là danh sách test rời rạc.
- **Tiêu chí 3 (hai chữ ký + dùng được)** — mục đích tồn tại của GĐ12 là trình được hai chữ ký và trao điều kiện go-live có địa chỉ cho `ship`; report không dẫn tới hành động là report trang trí.

## Vì sao 8 tiêu chí này

Ba cái đầu (gate) đo *ba lời hứa sống còn của uat*: bằng chứng thật, sợi truy vết liền, chữ ký + hành động. Hai cái giữa (4, 5) đo *hình dạng artifact đúng hợp đồng*: đọc-được 3 tầng và Đủ-là-đủ theo rủi ro. Ba cái cuối (6, 7, 8) đo *kỷ luật vai và cách chốt*: không lấn sibling, quyết định audit lại được, cổng + bàn giao có lối đi. Gộp lại = toàn bộ luật cứng trong `uat/SKILL.md`, không hơn. Thêm tiêu chí thứ 9 chỉ khi có một kiểu lỗi thật lặp lại mà 8 cái này không bắt được.
