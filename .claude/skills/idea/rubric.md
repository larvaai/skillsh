# Rubric — 7 tiêu chí chấm một bản `idea` (GĐ0–5: Idea Intake → Business → Product/PRD → Domain Model)

Mỗi tiêu chí 0/1/2. Khung chung: `grade/meta-rubric.md`. Chuẩn gốc để chấm: `idea/SKILL.md` (Router A/B/C · Quy tắc bắt buộc · Đủ-là-đủ mỗi giai đoạn · Bàn giao sau GĐ5) + `quy-trinh-idea-to-operate.md` mục GĐ0–5 nếu ý lớn cần template đầy đủ + `constitution/definition-of-done.md` (mục bắt buộc tối thiểu cho Idea/Domain). Rubric chỉ biến hợp đồng đó thành thước đo — KHÔNG thêm tiêu chuẩn mới.

**Đầu vào để chấm (fixture):** ý tưởng/tính năng gốc + ngữ cảnh user cung cấp (pain/user thật, ràng buộc) · project (greenfield hay brownfield — để kiểm bịa nhu cầu và kiểm nơi ghi artifact) · nhánh Router mong đợi (A/B/C) · giai đoạn dừng (`gd0`…`gd5_domain`/`done_handoff`) · output (nguyên văn các khối hội thoại + artifact `ideas/<slug>.md` bản `idea` sinh ra).

Tiêu chí **1 (Đúng+đủ artifact theo GĐ), 3 (Bám nguồn — không bịa nhu cầu), 2 (Đọc-được-3-tầng)** là **xương sống (gate)**: rớt bất kỳ cái nào → rớt cả bản dù tổng cao.

## 1. ĐÚNG + ĐỦ ARTIFACT THEO GIAI ĐOẠN (xương sống — A1)

Artifact đủ mọi mục bắt buộc của các giai đoạn ĐÃ chạy, theo Đủ-là-đủ của mỗi GĐ và mục tối thiểu ở `definition-of-done.md`. Bỏ một mục bắt buộc ≠ rút gọn độ sâu.

- GĐ1 Business: vấn đề + ai đau + chi phí nếu không làm (ước lượng thô) + ≥1 success metric ĐO ĐƯỢC.
- GĐ2–4 Product/PRD: MVP nêu rõ + đo bằng metric nào + scope out ghi thành chữ + open-Q còn treo có địa chỉ chốt.
- GĐ5 Domain: entity có identity + lifecycle; business rule bất biến liệt kê; domain event chính đặt tên; ranh giới context + ai sở hữu dữ liệu nào.

Chấm:
- 0 — thiếu hẳn một mục xương của GĐ đã chạy: GĐ1 không có metric đo được (chỉ "cải thiện trải nghiệm"); HOẶC GĐ2–4 không nêu scope-out; HOẶC GĐ5 có entity mà thiếu identity/lifecycle, hoặc thiếu business rule bất biến, hoặc coi entity = bảng DB (nhảy PRD → schema); HOẶC (Nhánh B) spike mà không nêu ẩn số cụ thể cần kiểm chứng.
- 1 — đủ mặt nhưng một GĐ sơ sài so với rủi ro: metric mơ hồ không đo được rạch ròi, hoặc domain event thiếu tên, hoặc data ownership bỏ trống ở hệ nhiều context.
- 2 — đủ mọi mục bắt buộc của các GĐ đã chạy; metric đo được; scope-out thành chữ; entity có identity+lifecycle; rule bất biến + event + ranh giới context rõ; độ sâu khớp rủi ro.

## 2. ĐỌC-ĐƯỢC-3-TẦNG (xương sống — A3)

Artifact + các khối hội thoại mở bằng Góc nhìn lãnh đạo (vấn đề/giá trị bằng ngôn ngữ nghiệp vụ, không jargon) rồi mới tới chi tiết cho dev; ~1 trang, scan 2–3 phút; hiệu chỉnh theo `level` trong `user-state.json` nếu có (L0–L2 bình dân hơn, L6–L8 gọn).

- 0 — nhảy thẳng vào jargon domain/kỹ thuật, không có tầng lãnh đạo đọc-được ai-đau-vì-sao-đáng-làm; HOẶC dày đặc, tường bullet, đọc xong không nắm được ý tưởng là gì; HOẶC sai mức user rõ rệt.
- 1 — có cả hai tầng nhưng lệch: góc lãnh đạo còn jargon hoặc chìm dưới chi tiết domain, hoặc phần dev thiếu một mảnh (rule/ranh giới cụ thể).
- 2 — mở bằng đúng vài thứ CTO/business nhìn để biết đáng-làm + hình dạng nhu cầu; rồi đủ MVP + scope + entity/rule/event cho dev/`/shape` bước tiếp; câu ngắn, phẳng.

## 3. BÁM NGUỒN — KHÔNG BỊA NHU CẦU (xương sống — A2)

Mọi pain/user/số/entity/rule truy được về input thật: ngữ cảnh user cung cấp, code cũ (`.ai-understanding/` nếu brownfield), hoặc GĐ trước ĐÃ qua cổng. Input ngoài user đưa phải kèm cảnh báo ⚠️; chỗ chưa chắc gắn nhãn open-Q, KHÔNG ngụy tạo nhu cầu/con số. Đây là gate nặng nhất của cả suite.

- 0 — bịa nhu cầu/user/con số user không đưa (vd tự chế "tiết kiệm 40% chi phí" không nguồn); HOẶC entity/rule mâu thuẫn domain code cũ trong `.ai-understanding/`; HOẶC metric/pain không nối được về bất kỳ input nào; HOẶC bỏ qua ngữ cảnh user đã cung cấp.
- 1 — chủ yếu bám nguồn, một chỗ suy đoán không gắn nhãn (một con số đoán mò không ghi "ước lượng thô/open-Q", hoặc một rule tự thêm không hỏi).
- 2 — mọi pain/metric/entity/rule bám ngữ cảnh user hoặc GĐ trước; ước lượng ghi rõ là ước lượng; open-Q từ GĐ trước được đóng hoặc chuyển tiếp có nhãn; không chế nhu cầu.

## 4. ĐỦ-LÀ-ĐỦ + HỎI ĐÚNG TẦNG — độ sâu tỉ lệ rủi ro (A4)

Độ sâu mỗi GĐ tỉ lệ rủi ro/ẩn số, không phải vị trí trong luồng; KHÔNG nhảy cóc GĐ; mỗi GĐ chỉ hỏi câu thuộc tầng đó; một cụm ≤3 câu mỗi lượt.

- 0 — làm ngược Đủ-là-đủ: việc nhỏ/đã rõ mà đổ đủ 14 mục PRD + 10 mục Business Case thủ tục; HOẶC nhảy cóc GĐ (bỏ GĐ1 nhảy thẳng Domain); HOẶC hỏi sai tầng (GĐ1 hỏi kiến trúc/DB/deadline, GĐ2–4 hỏi lại ROI đã chốt hoặc hỏi stack, GĐ5 hỏi sprint/kiến trúc); HOẶC dồn hỏi hết một lúc (>3 câu / nhiều cụm cùng lượt).
- 1 — độ sâu lệch nhẹ ở 1–2 GĐ, hoặc một câu hỏi lỡ sai tầng nhưng đã ghi nhận thành open-Q mang sang đúng tầng.
- 2 — nặng ở GĐ có ẩn số, nhẹ ở phần quen (ghi 1 dòng lý do khi rút gọn/bỏ); không nhảy cóc; mỗi lượt một cụm ≤3 câu đúng tầng; câu lỡ sai tầng được đẩy thành open-Q.

## 5. KHÔNG LẤN VAI — DỪNG ĐÚNG GĐ5, KHÔNG TỰ KILL/TỰ BUILD (A4)

`idea` chỉ lo GĐ0–5. Không tự viết code, không chọn kiến trúc/framework/DB (GĐ6+ — `/shape`/`/stack`); không tự kill; không tự ghi artifact vào repo brownfield khi chưa hỏi.

- 0 — trôi qua GĐ5: chốt kiến trúc/framework/DB/schema hoặc viết code; HOẶC tự kill (tự nói "nên bỏ ý này" khi user chưa nói dừng); HOẶC dùng câu phủ định cứng khi phản biện ("không thể"/"sai rồi"/"không làm được") không kèm lối đi tiếp; HOẶC tự ghi artifact vào repo brownfield mà chưa hỏi user (chỉ greenfield mới ghi thẳng `<project>/ideas/`).
- 1 — chủ yếu đúng vai, lỡ nhắc 1 tool/kiến trúc như gợi ý chưa gắn nhãn "để GĐ6", hoặc một câu phản biện gần chạm phủ định cứng nhưng vẫn có lối đi.
- 2 — thuần GĐ0–5, dừng đúng ở Domain; tool/kiến trúc chỉ xuất hiện dưới dạng ràng buộc chuyển cho `/shape`; không khả thi thì phản biện + giữ điểm hay + hướng thay thế, chỉ ghi `killed` khi user tự nói dừng; artifact ghi đúng vùng state (hoặc greenfield/đã-hỏi).

## 6. ROUTER + CỔNG + PHÂN VAI (A5)

Chạy Router (rõ/mơ hồ × khả thi) → đúng một nhánh A/B/C; mỗi GĐ ở Nhánh C có cổng đúng câu doc + AI tự tóm tắt-hiểu rồi mới hỏi go/no-go, KHÔNG tự bấm GO; quyết định lớn ghi lý do + phương án đã loại.

- 0 — không chạy Router / phân nhánh sai (khả thi rõ mà đẩy vào spike, hoặc chưa-rõ-khả-thi mà nhảy thẳng GĐ1); HOẶC không có cổng go/no-go giữa các GĐ; HOẶC tự bấm GO / tự trôi sang GĐ kế thay user; HOẶC (Nhánh B ý còn mơ hồ) đặt ẩn số spike trước khi làm rõ nhu cầu.
- 1 — có Router + cổng nhưng câu cổng lệch doc, hoặc phân vai duyệt mờ, hoặc quyết định lớn thiếu "phương án đã loại".
- 2 — Router rõ → đúng nhánh; mỗi GĐ tóm tắt-hiểu rồi cổng đúng câu ("Đáng đầu tư đi tiếp không?" / "Hướng sản phẩm & MVP đủ rõ chưa?" / "PRD đủ tin cậy chưa?" / "Domain đủ rõ để định hình kiến trúc & ranh giới module chưa?"); AI tự soi rồi mới xin user; quyết định lớn kèm lý do + phương án loại; chờ user quyết.

## 7. CỔNG DỪNG DOMAIN + BÀN GIAO (A5)

Ở GĐ5, cổng "Domain đủ rõ để định hình kiến trúc chưa" = DỪNG; kết bằng khối Bàn giao trỏ `/shape` (GĐ6) là đường chính + artifact path, liệt kê lối rẽ (`/partner`/`/frame`/`/atlas`/`/explain`), không tự chọn hộ.

- 0 — không có khối bàn giao; HOẶC tự trôi sang Architecture khi domain đã đủ (không dừng ở cổng GĐ5); HOẶC bàn giao khi domain chưa đủ (cổng chưa qua); HOẶC trỏ sai đường (nhảy thẳng `/frame` code bỏ qua `/shape` khi ý cần kiến trúc bài bản).
- 1 — có bàn giao nhưng tự chọn hộ user chạy skill nào, hoặc thiếu artifact path / thiếu domain-đã-chốt trong khối.
- 2 — cổng GĐ5 đúng câu doc → Có = DỪNG; khối bàn giao nêu domain đã chốt + artifact path, `/shape` là đường chính, liệt kê lối rẽ để user quyết; Chưa = quay lại làm rõ phần domain thiếu, không tự đoán tiếp.

## Gate

Tiêu chí **1 (Đúng+đủ artifact theo GĐ — A1), 3 (Bám nguồn/không bịa nhu cầu — A2), 2 (Đọc-được-3-tầng — A3)** là xương sống. Bất kỳ cái nào = 0 → bản **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Bản 12/14 nhưng bịa nhu cầu/con số user không đưa (tiêu chí 3 = 0), hoặc entity thiếu identity/lifecycle (tiêu chí 1 = 0), vẫn rớt — vì `/shape` phía sau sẽ định hình kiến trúc trên một domain bịa. Khi so nhiều bản: loại hết bản rớt gate TRƯỚC, rồi mới xếp phần còn lại theo tổng.

## Khung report (xếp nhiều bản cạnh nhau)

```
CHẤM: idea · <ý tưởng / project> · <nhánh A|B|C> · <giai đoạn dừng>
1 Đúng+đủ artifact/GĐ   [n/2] — <lý do 1 câu>
2 Đọc-được-3-tầng       [n/2] — <...>
3 Bám nguồn/không bịa   [n/2] — <...>
4 Đủ-là-đủ + hỏi tầng   [n/2] — <...>
5 Không lấn vai/dừng GĐ5[n/2] — <...>
6 Router+Cổng+phân vai  [n/2] — <...>
7 Cổng-dừng + Bàn giao  [n/2] — <...>
TỔNG: <n>/14   ·   GATE: đạt / RỚT ở tiêu chí <...>
SỬA TRƯỚC TIÊN: <một câu — đòn bẩy lớn nhất để bản này tốt hơn>
```

## Vì sao 7 tiêu chí này

Ba xương sống đo *có ra đúng thứ + đọc được + trung thực không*: đủ artifact theo GĐ (đúng cái `idea` hứa, đủ mục Domain/PRD bắt buộc), đọc-được-3-tầng (CTO lẫn dev đều nắm), bám nguồn/không bịa nhu cầu (gate nặng nhất — chặn chế pain/số/rule mà `/shape` sẽ tin nhầm). Bốn cái sau đo *có đúng kỷ luật của `idea` không*: đủ-là-đủ + hỏi đúng tầng (không thủ tục thừa, không nhảy cóc), không lấn vai (dừng đúng GĐ5, không tự kill/tự build/tự chọn kiến trúc), Router+cổng+phân vai (phân nhánh đúng, không tự GO), cổng-dừng-Domain + bàn giao (DỪNG đúng chỗ rồi trỏ `/shape`). Gộp lại = trọn hợp đồng của `idea`, không hơn. Mỗi Luật cứng trong SKILL.md đã gấp thành một anchor-0 (không tự kill / không tự build / không tự tạo file repo / dừng đúng Domain / đủ-là-đủ / hỏi đúng tầng / cấm phủ định cứng / mỗi quyết định ghi phương án loại / một cụm ≤3 câu). Thêm tiêu chí thứ 8 chỉ khi có kiểu lỗi thật lặp lại mà 7 cái này không bắt được.
