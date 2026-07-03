# Rubric — chấm một Traceability Report

Mỗi tiêu chí 0/1/2. Chuẩn gốc: `traceability/SKILL.md` + `quy-trinh-idea-to-operate.md` (C1 sợi · C2 security · D1 dashboard · D2 đủ-là-đủ · D3 cổng). Rubric chỉ biến hợp đồng đó thành thước đo, không thêm tiêu chuẩn mới.

**Đầu vào để chấm (fixture):** project/slug · các file pipeline state (state/project/<name>/pipeline/*.json + ideas/_index.json) + progress.json · bản Traceability Report cần chấm

## 1. ĐÚNG BỨC TRANH — dashboard khớp thực tế (xương sống)
- 0 — báo sai: cho một artifact CHƯA có là "✓", hoặc báo thiếu cái thật ra đã có; hoặc bỏ sót giai đoạn.
- 1 — đúng phần lớn, lệch 1 ô hoặc 1 trạng thái `~`/`✗`.
- 2 — mọi giai đoạn 0–14 có trạng thái đúng (✓/~/✗), khớp state/artifact thật; cái không đọc được ghi "không rõ".

## 2. ĐỌC-ĐƯỢC-3-TẦNG — lãnh đạo + dev (xương sống)
- 0 — không có góc nhìn lãnh đạo mở đầu, hoặc chỉ là bảng kỹ thuật khó đọc, CTO/PO không nắm được "đang ở đâu, thiếu gì".
- 1 — có mở lãnh đạo nhưng mờ, hoặc chi tiết gap thiếu cho dev/PO.
- 2 — mở bằng 2–3 câu lãnh đạo (đang ở GĐ mấy · thiếu lớn nhất · cổng đắt qua chưa), rồi dashboard + gap đủ cho dev/PO hành động; 1 màn hình scan được.

## 3. BÁM NGUỒN — không bịa (xương sống)
- 0 — kết luận "đã có/đã thiếu/đứt" không dựa artifact thật; đoán trạng thái.
- 1 — chủ yếu bám nguồn, 1 chỗ suy đoán không gắn nhãn.
- 2 — mọi trạng thái bám state/artifact thật đọc được (hoặc input ngoài user đưa KÈM cảnh báo ⚠️); cái chưa chắc gắn nhãn "không rõ". Kết luận từ nguồn ngoài state mà THIẾU cảnh báo → trừ về mức này; vẫn CẤM bịa cái không có nguồn.

## 4. SỢI TRACEABILITY — chỉ đúng mắt xích đứt
- 0 — không kiểm chuỗi C1, hoặc chỉ liệt kê giai đoạn mà không truy liên kết.
- 1 — có kiểm nhưng chung chung ("thiếu liên kết") không chỉ ra item nào đứt ở đâu.
- 2 — truy chuỗi Business Objective→…→Metric, chỉ ra mắt xích đứt CỤ THỂ (feature nào chưa nối objective, story nào thiếu AC, requirement nào chưa có test).

## 5. ĐỦ-LÀ-ĐỦ ĐÚNG — không flag oan, không sót never-skip
- 0 — flag oan giai đoạn rút gọn hợp lệ là "thiếu", HOẶC bỏ sót một never-skip vắng mặt.
- 1 — phần lớn đúng, lệch một chỗ (oan nhẹ hoặc sót một never-skip phụ).
- 2 — không đòi làm thừa cho việc nhỏ; bắt đủ 4 never-skip (Story/AC · DoD · test mapping · rollback+monitoring) khi chúng vắng, dù việc nhỏ.

## 6. NHẮC ĐÚNG SKILL — mỗi gap trỏ đúng chỗ bổ sung
- 0 — không nhắc skill, hoặc trỏ sai skill cho gap.
- 1 — có nhắc nhưng lệch skill hoặc chung chung.
- 2 — mỗi gap trỏ đúng skill (idea/shape/…/operate), theo đúng thứ tự phụ thuộc; không tự chọn hộ, không tự làm giai đoạn.

## 7. ĐÚNG VAI — read-only, không lấn
- 0 — tự sinh/sửa artifact giai đoạn (việc skill kia), hoặc dẫn từng bước như partner, hoặc đi chấm chất lượng như grade.
- 1 — chủ yếu đúng vai, lấn nhẹ.
- 2 — chỉ soi + báo + nhắc; read-only trên artifact skill khác; phân biệt rõ với partner (dẫn) và grade (chấm chất lượng).

## Gate (xương sống)
Tiêu chí 1, 2, 3 là xương sống. Bất kỳ cái nào = 0 → report **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một report 12/14 nhưng báo sai trạng thái (tc1=0) vẫn rớt — vì lãnh đạo sẽ quyết nhầm dựa trên bức tranh sai.

## Khung report chấm (để so nhiều bản)
```
CHẤM: traceability · <project/slug>
1 Đúng bức tranh   [n] — <lý do 1 câu>
2 Đọc-3-tầng       [n] — <...>
3 Bám nguồn        [n] — <...>
4 Sợi traceability [n] — <...>
5 Đủ-là-đủ         [n] — <...>
6 Nhắc đúng skill  [n] — <...>
7 Đúng vai         [n] — <...>
TỔNG: <n>/14   GATE: <đạt | rớt: tiêu chí ...>
SỬA TRƯỚC TIÊN: <đòn bẩy lớn nhất>
```

## Vì sao các tiêu chí này

Ba tiêu chí gate đo *có ra đúng thứ + đọc được + trung thực không*; các tiêu chí sau đo *có đúng kỷ luật pipeline không* (đủ-là-đủ, không lấn vai, cổng/traceability, bàn giao). Gộp lại = trọn hợp đồng của `traceability`, không hơn. Thêm một tiêu chí mới chỉ khi có một kiểu lỗi thật lặp lại mà bộ hiện tại không bắt được.
