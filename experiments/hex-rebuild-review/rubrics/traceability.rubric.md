# Rubric — 8 tiêu chí chấm một Traceability Report

Mỗi tiêu chí 0/1/2, tối đa 16. Chuẩn gốc: `traceability/SKILL.md` (luật cứng + 4 khối thân report) và các mục nó bám của `quy-trinh-idea-to-operate.md` (C1 sợi traceability, C2 security đan giai đoạn, D1 dashboard, D2 đủ-là-đủ, D3 cổng). Rubric chỉ biến hợp đồng đó thành thước đo được — không thêm tiêu chuẩn mới.

Chuẩn đối chiếu ngoài: khi report có claim về code (neo `file:line`, hành vi hàm, invariant), đối chiếu với code gốc tại `/Users/uspro/Desktop/namnson/hex_agent`. Claim code sai chuẩn này tính là bịa.

## 1. BÁM BẰNG CHỨNG — mọi trạng thái có nguồn kiểm được (xương sống)

Luật "Không bịa" của hợp đồng: chỉ báo dựa trên artifact/state THẬT đọc được.

- 0 — có ít nhất một trạng thái/con số/claim không nguồn: tuyên ✓/GO/PASS cho một giai đoạn mà không trỏ được vào artifact/state thật (file `pipeline/*.md|json`, `ideas/*`, hoặc mô tả user đưa kèm cảnh báo ngoài-state); con số (kiểu 0/9, 26/28) không khớp file nguồn; claim code (neo `file:line`) sai khi đối chiếu `/Users/uspro/Desktop/namnson/hex_agent`; hoặc chỗ đọc-không-ra bị đoán thành đã-có/đã-thiếu. Bất kỳ claim bịa nào → tiêu chí này 0.
- 1 — trạng thái chính đều có nguồn nhưng 1–2 chỗ neo mơ hồ ("theo backlog" mà không nói file/mục nào), hoặc một ô đáng ghi "không rõ" lại bị bỏ trống không nhãn.
- 2 — mọi ✓/~/✗, mọi PASS/PENDING/GO, mọi con số trỏ được về nguồn kiểm được; chỗ không đọc được ghi rõ "không rõ"; nếu soi bằng đầu vào ngoài state thì in đúng khối ⚠ cảnh báo TRƯỚC report rồi mới báo.

## 2. GÓC NHÌN LÃNH ĐẠO — mở bằng 3 câu trả lời đúng 3 việc

Hợp đồng đọc-được-3-tầng: report MỞ bằng tầng lãnh đạo, RỒI mới tới chi tiết.

- 0 — report mở thẳng bằng bảng chi tiết/kỹ thuật; hoặc đọc hết phần mở vẫn không biết một trong ba điều: đang ở GĐ nào · thiếu lớn nhất là gì · cổng đắt (GĐ8 live slice, GĐ13 go/no-go) đã qua chưa.
- 1 — có phần lãnh đạo trả lời đủ 3 việc nhưng dài quá mức scan 2–3 phút, hoặc trộn chi tiết tầng dev (tên test case, `file:line`) vào tầng lãnh đạo khiến CEO/CTO phải lọc.
- 2 — 2–3 câu (hoặc ý ngắn tương đương) đầu tiên trả lời trọn: đang ở GĐ mấy · thiếu lớn nhất một câu · trạng thái từng cổng đắt; sau đó mới tới bảng cho PO/dev; toàn report gọn cỡ 1 màn hình chính, scan 2–3 phút.

## 3. DASHBOARD — đủ 15 giai đoạn theo D1

- 0 — thiếu giai đoạn (không phủ GĐ0–5 gộp qua `idea` + GĐ6–14 mỗi giai đoạn một dòng), hoặc có dòng không mang trạng thái ✓/~/✗, hoặc không có cột skill bổ sung.
- 1 — đủ giai đoạn + trạng thái nhưng hụt một mảnh: không ghi cổng kế, never-skip không đánh dấu `*`, hoặc 2 cổng đắt không hiện ngay ở đầu dashboard.
- 2 — mỗi giai đoạn một dòng với đủ: trạng thái ✓/~/✗ nhất quán với phần chữ bên dưới (không chỗ nói ✓ chỗ nói thiếu), skill bổ sung, cổng kế; `*` đánh dấu never-skip; header dashboard nêu "đang ở GĐ n" + trạng thái 2 cổng đắt.

## 4. SỢI TRACEABILITY — truy từng mắt xích, gọi tên chỗ đứt

Theo C1: Business Objective → Product Goal → Requirement → PRD → Epic → Feature → Story → AC → Test Case → PR → Release → Metric.

- 0 — chỉ chép lại chuỗi mà không truy item nào; hoặc phán "đứt / không đứt" mà không đưa bằng chứng theo mắt xích.
- 1 — có truy nhưng lửng: kiểm vài mắt xích rồi khái quát phần còn lại, hoặc chỗ đứt nêu chung chung ("backlog chưa nối business") không gọi đích danh item nào đứt với cái gì.
- 2 — truy đủ chuỗi cho các item đang sống, mỗi mắt xích có kết luận nối/không kèm neo nguồn; chỗ đứt gọi đích danh (feature/story/AC nào, đứt khỏi mắt xích nào); phân biệt rõ "đứt chuỗi" với "nối-nhưng-chưa-có-số/PENDING" và với "mắt xích chưa tồn tại vì chưa tới lúc" (vd PR khi chưa code).

## 5. BẮT ĐÚNG THIẾU — never-skip đủ, không flag oan (xương sống)

Theo D2: chỉ báo THIẾU khi (a) never-skip vắng, hoặc (b) GĐ sau sẽ mù vì thiếu đầu vào. Đây là việc sống còn của một tháp kiểm soát: sót thì lọt lỗ, flag oan thì mất lòng tin.

- 0 — bỏ sót một never-skip vắng mặt mà không báo (Story+AC GĐ9 · DoD GĐ11 · test mapping GĐ12 · rollback+monitoring GĐ13); HOẶC flag oan — báo "thiếu" một giai đoạn rút gọn hợp lệ mà không chỉ ra được GĐ sau nào sẽ mù.
- 1 — không sót never-skip, nhưng ranh giới nói chưa sạch: có chỗ dùng lẫn `~` và `✗`, hoặc một rút-gọn hợp lệ không được nói rõ vì sao hợp lệ (đọc xong vẫn tưởng là thiếu).
- 2 — cả 4 never-skip được điểm danh đích danh có/vắng; mọi `✗` đều kèm lý do thuộc một trong hai điều kiện D2; rút gọn hợp lệ được ghi là hợp lệ kèm lý do, không đòi làm thừa.

## 6. GAP → HÀNH ĐỘNG — người nhận cầm đi làm được ngay (xương sống)

- 0 — có gap không trỏ skill nào để bổ sung; trỏ SAI skill so với mapping pipeline (vd thiếu AC lại nhắc /modules); hoặc report tự LÀM hộ gap (tự viết AC, tự sửa rollback…) thay vì nhắc.
- 1 — mỗi gap có skill nhưng thiếu vế "vì sao GĐ sau sẽ mù" hoặc không có thứ tự ưu tiên — người nhận phải tự suy ra làm gì trước; hoặc khối bàn giao cuối thiếu/lệch (không liệt kê lối /partner, /grade).
- 2 — mỗi gap đúng một dòng đủ 3 vế: thiếu gì → vì sao GĐ sau mù → chạy skill nào (đúng skill của giai đoạn đó), never-skip đánh dấu bắt buộc, có ưu tiên; kết bằng khối bàn giao liệt kê skill để user tự chạy, KHÔNG tự chọn hộ; dev/CTO/PO đọc xong biết ngay lệnh kế tiếp.

## 7. CỔNG & SECURITY — D3 + C2 đủ mặt

- 0 — không có mục trạng thái cổng, hoặc không có mục security đan giai đoạn.
- 1 — có cả hai nhưng hụt: cổng chưa qua không ghi ai duyệt; security kiểm không đủ 7 điểm C2 (data classification GĐ1 · threat model GĐ6 · secret GĐ8 · scan GĐ11 · SAST/DAST GĐ12 · checklist go/no-go GĐ13 · monitoring GĐ14) mà không nói vì sao bỏ; hoặc open-Q còn treo không nhắc tới.
- 2 — bảng cổng phủ các giai đoạn kèm trạng thái + người duyệt; 7 điểm security C2 điểm danh từng điểm (kể cả "hoãn/thay thế có lý do" ghi rõ lý do); open-Q còn treo liệt kê tường minh.

## 8. ĐÚNG VAI — kiểm không làm, nhắc không dẫn

- 0 — lấn vai: sinh/sửa artifact của giai đoạn khác (viết AC, sửa backlog, chỉnh runbook…), tự chạy hoặc tự quyết chạy skill khác, dẫn từng-bước-tiếp-theo như `partner`, hoặc phủ định cứng — phán "hỏng" mà không kèm lối bổ sung.
- 1 — chủ yếu đúng vai nhưng lấn nhẹ: khuyên vượt mức nhắc ("nên chọn phương án B"), hoặc sa vào chấm chất lượng nội dung một artifact (việc của `grade`) thay vì độ đầy đủ + liên kết.
- 2 — read-only trọn vẹn: chỉ đọc + báo + nhắc; mỗi chỗ đứt/thiếu đều kèm lối bổ sung; quyền chạy skill để lại cho user; file duy nhất của nó là snapshot `pipeline/_traceability.md` + `.json`.

## Luật gate (tiêu chí xương sống)

Tiêu chí 1, 5, 6 là xương sống. Bất kỳ cái nào = 0 → report **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một report 14/16 nhưng tuyên GO cho một giai đoạn không có state (tiêu chí 1 = 0) vẫn rớt — vì CEO/CTO sẽ ra quyết định trên bức tranh sai. Tương tự: sót một never-skip (5 = 0) là tháp kiểm soát lọt đúng cái nó sinh ra để bắt; gap không trỏ được skill (6 = 0) là report đọc xong không ai làm gì được. Gate quan trọng hơn tổng: khi so nhiều bản, loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Vì sao 8 tiêu chí này

Tiêu chí 1 đo *có trung thực với bằng chứng không* — nền của mọi thứ còn lại. Tiêu chí 2–4 đo *report có đúng hình hợp đồng không* (3 tầng lãnh đạo-trước, dashboard D1, sợi C1). Tiêu chí 5–7 đo *phần kiểm có đúng luật kiểm không* (D2 never-skip + không flag oan, gap→skill dùng được, cổng D3 + security C2). Tiêu chí 8 đo *có ở đúng vai kiểm-không-làm không*. Gộp lại = toàn bộ hợp đồng của `traceability`, không hơn. Thêm tiêu chí thứ 9 chỉ khi có một kiểu lỗi thật lặp lại mà 8 cái này không bắt được.
