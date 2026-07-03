# Rubric — chấm một bản `operate` (GĐ14 Operations & Measurement)

Mỗi tiêu chí 0/1/2. Chuẩn gốc để chấm = `operate/SKILL.md` + mục "## Giai đoạn 14 — Operations & Measurement" của `quy-trinh-idea-to-operate.md`. Rubric chỉ biến hợp đồng đó thành thước đo — KHÔNG thêm tiêu chuẩn mới. Ba tiêu chí 1–3 là XƯƠNG SỐNG (gate).

**Đầu vào để chấm (fixture):** bản Ops Dashboard (+ Incident Process + Iteration Loop) cần chấm · Go/No-Go & Runbook GĐ13 + success metric gốc GĐ1 (từ backlog/idea) làm nguồn đối chiếu

## 1. ĐÚNG + ĐỦ ARTIFACT (xương sống)

Sinh đủ ba artifact và mỗi cái đủ phần đã liệt kê: Ops Dashboard (đủ 4 nhóm Business·Product·Engineering[DORA]·Operations) + Incident Process (phát hiện→phân loại→owner→khắc phục→hậu kiểm) + Iteration Loop (nhịp review + đường về GĐ9).

- 0 — thiếu một artifact (Ops Dashboard / Incident Process / Iteration Loop), HOẶC Dashboard thiếu một trong 4 nhóm, HOẶC Engineering không phải DORA thật (thiếu cả 4 con số DORA), HOẶC Iteration không có đường về backlog.
- 1 — đủ ba artifact nhưng một phần sơ sài (DORA thiếu 1–2 chỉ số, metric để trần không ngưỡng, Incident gộp mất bước hậu kiểm ở hệ đáng lẽ cần).
- 2 — đủ ba artifact; Dashboard đủ 4 nhóm có số + ngưỡng/kỳ vọng; DORA đủ 4 chỉ số; Incident đủ phát-hiện→hậu-kiểm; Iteration có nhịp + đường về backlog; độ sâu khớp Đủ-là-đủ.

## 2. ĐỌC-ĐƯỢC 3 TẦNG (xương sống)

Mở bằng Góc nhìn lãnh đạo (nghiệp vụ, không jargon) rồi mới tới chi tiết dev; một trang scan 2–3 phút.

- 0 — không có "Góc nhìn lãnh đạo"/dòng ĐỌC-CHO-LÃNH-ĐẠO mở đầu, hoặc mở thẳng bằng jargon kỹ thuật/DORA; HOẶC dev không đủ để hành động (không rõ alert/owner/nơi đo DORA/item vòng kế).
- 1 — có cả hai tầng nhưng lệch: góc lãnh đạo lẫn jargon, hoặc chi tiết dev mỏng, hoặc sai thứ tự (kỹ thuật lên trước).
- 2 — mở bằng 1–3 con số CEO/CTO nhìn để biết on-track (ngôn ngữ nghiệp vụ), rồi chi tiết đủ cho dev/Ops; đúng thứ tự lãnh-đạo→kỹ thuật; một trang scan 2–3 phút.

## 3. BÁM NGUỒN — dùng artifact GĐ trước, không bịa (xương sống)

Business metric đối chiếu THẲNG mục tiêu gốc GĐ1; dùng monitoring/alert/incident-owner/rollback từ ship (GĐ13), không dựng lại/bịa. Nguồn hợp lệ = artifact GĐ trước ĐÃ qua cổng HOẶC input ngoài user cung cấp KÈM cảnh báo ⚠️; dùng input ngoài mà THIẾU cảnh báo → trừ điểm (không minh bạch nguồn); vẫn CẤM bịa cái user không đưa.

- 0 — bịa số liệu/incident/owner/target, HOẶC nhóm Business không đối chiếu mục tiêu gốc GĐ1 (đo lơ lửng), HOẶC dựng lại incident owner/alert thay vì lấy từ ship (GĐ13).
- 1 — bám nguồn phần lớn, một chỗ suy đoán/số mơ hồ không gắn nhãn `chưa có số`.
- 2 — mọi số bám dữ liệu thật hoặc gắn nhãn `chưa có số` + cách lấy; Business so thẳng target GĐ1; Incident kế thừa owner/alert/rollback từ GĐ13.

## 4. ĐỦ-LÀ-ĐỦ — không thủ tục thừa, không bỏ bước

- 0 — bỏ một artifact/nhóm chỉ số để "cho gọn", HOẶC phình thủ tục không tỉ lệ rủi ro (hệ nhỏ ổn định mà ép đủ 4 DORA + post-mortem dài, 3 trang).
- 1 — độ sâu hơi lệch rủi ro ở 1–2 chỗ.
- 2 — độ sâu tỉ lệ rủi ro/lưu lượng; hệ nhỏ vài dòng mỗi nhóm, hệ quan trọng đầy đủ; không bỏ artifact nào, chỉ rút gọn đúng chỗ.

## 5. TRACEABILITY — nối GĐ trước ↔ sau

- 0 — Business metric không nối được về GĐ1, HOẶC item cải tiến không truy về một chỉ số lệch, HOẶC Iteration không đẻ ra việc nào về GĐ9.
- 1 — có nối nhưng đứt một đầu (về GĐ1 rõ nhưng item mơ hồ không kèm lý do số, hoặc ngược lại).
- 2 — nối cả hai chiều: Business ↔ mục tiêu GĐ1, Incident ↔ runbook/owner GĐ13, mỗi item Iteration ↔ một chỉ số/drop/incident cụ thể, đường về GĐ9 rõ.

## 6. CỔNG + PHÂN VAI ĐÚNG (A5)

- 0 — thiếu cổng "Đạt mục tiêu chưa? Làm gì tiếp?", HOẶC skill tự quyết đầu tư vòng kế / tự tuyên "đạt, dừng" / tự chọn item lên roadmap hộ CEO/CTO / tự nhảy vào code fix / đề xuất tính năng mới.
- 1 — có cổng nhưng phân vai mờ (không rõ CEO/CTO duyệt theo nhịp) hoặc lấn vai nhẹ.
- 2 — cổng đúng câu; Ops/SRE+PO viết, CEO/CTO duyệt theo nhịp; skill chỉ trình + đề xuất, không tự quyết; không lấn vai frame/review/backlog/idea.

## 7. BÀN GIAO ĐÚNG SKILL KẾ

- 0 — không có khối bàn giao, HOẶC chỉ về skill sai (không nối lại `backlog` GĐ9).
- 1 — có bàn giao nhưng tự chọn hộ skill, hoặc thiếu artifact path / item về backlog.
- 2 — khối bàn giao nêu mục-tiêu-gốc + học-được + item (kèm lý do) + artifact path; `/backlog` (GĐ9) là đường chính đóng vòng, `/review`·`/idea`·`/partner`·`/frame` là nhánh phụ; liệt kê, không chọn hộ.

## Gate + khung report

Tiêu chí 1, 2, 3 là xương sống. Bất kỳ cái nào = 0 → bản **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao (vd 12/14 nhưng không nối business metric về mục tiêu GĐ1 → tiêu chí 3 = 0 → rớt, vì mất đúng bản chất GĐ14: đóng vòng với cái CEO đã ký). Khi so nhiều bản: loại hết bản rớt gate TRƯỚC, rồi mới xếp theo tổng. Hoà tổng thì bản có tiêu chí xương sống mạnh hơn thắng.

Khung report cố định (để xếp nhiều bản cạnh nhau):
```text
BẢN <id> — operate
  1 Artifact đúng+đủ (gate) : x/2  — <lý do 1 dòng>
  2 Đọc-được 3 tầng (gate)  : x/2  — <...>
  3 Bám nguồn (gate)        : x/2  — <...>
  4 Đủ-là-đủ                : x/2  — <...>
  5 Traceability            : x/2  — <...>
  6 Cổng + phân vai         : x/2  — <...>
  7 Bàn giao đúng skill kế  : x/2  — <...>
  GATE : PASS/FAIL (rớt ở tiêu chí nào)   TỔNG : xx/14
```

## Vì sao các tiêu chí này

Ba tiêu chí gate đo *có ra đúng thứ + đọc được + trung thực không*; các tiêu chí sau đo *có đúng kỷ luật pipeline không* (đủ-là-đủ, không lấn vai, cổng/traceability, bàn giao). Gộp lại = trọn hợp đồng của `operate`, không hơn. Thêm một tiêu chí mới chỉ khi có một kiểu lỗi thật lặp lại mà bộ hiện tại không bắt được.
