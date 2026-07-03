# Rubric — chấm một trang SHIP (skill `ship`, GĐ13 Release Readiness & Rollout)

Mỗi tiêu chí 0/1/2. Chuẩn gốc để chấm = `ship/SKILL.md` + `quy-trinh-idea-to-operate.md` mục "## Giai đoạn 13 —". Rubric chỉ biến hợp đồng đó thành thước đo — KHÔNG thêm tiêu chuẩn mới. Ba tiêu chí XƯƠNG SỐNG (gate): 1, 2, 3.

**Đầu vào để chấm (fixture):** trang ship (Go/No-Go + Runbook + Rollback + Rollout) cần chấm · Test & Verification Report GĐ12 + kỳ vọng ban đầu (README) + success metric làm nguồn

## 1. ĐÚNG + ĐỦ ARTIFACT (xương sống)

Có đủ bốn artifact ghép: **Go/No-Go Checklist** (mỗi dòng owner + trạng thái) + **Runbook** (deploy / kiểm tra sau deploy / rollback từng bước) + **Rollback Plan** (đã test nếu hệ quan trọng) + **Rollout Strategy** (alpha→pilot→beta→gradual→full).

- 0 — thiếu hẳn một artifact mà không ghi lý do; HOẶC checklist không có owner/trạng thái hay khuyết ô mà không ghi N/A; HOẶC thiếu một trong **4 thứ chặn** (rollback / monitoring+alert / incident owner / UAT+Security sign-off GĐ12); HOẶC runbook không có bước rollback; HOẶC rollout không có bậc thang.
- 1 — đủ bốn nhưng một phần sơ sài (rollback chỉ "revert" không nói cách lùi / mất dữ liệu / ai bấm; rollout thiếu tín hiệu tiến/lùi; runbook thiếu smoke check).
- 2 — đủ bốn, đúng danh mục doc; đủ 12 ô (ô không dùng ghi "N/A + lý do"); mỗi dòng Go/No-Go có owner thật + trạng thái thật; runbook có bước kiểm-tra-sau-deploy + ngưỡng rollback; rollback nêu tín hiệu + cách + xử lý dữ liệu + đã test (nếu quan trọng); rollout theo bậc kèm tín hiệu/tiêu chí đi tiếp mỗi bậc.

## 2. ĐỌC-ĐƯỢC 3 TẦNG — lãnh đạo mở đầu + dev hành động được (xương sống)

Mở bằng Góc nhìn lãnh đạo (quyết định GO/NO-GO + đường lùi + ai trực, ngôn ngữ nghiệp vụ), rồi mới tới chi tiết dev. Một trang.

- 0 — nhảy thẳng vào lệnh deploy/checklist kỹ thuật/jargon, không có đoạn lãnh đạo đọc được; HOẶC đầy jargon lãnh đạo không đọc được; HOẶC chỉ có tầng lãnh đạo mà runbook mơ hồ tới mức người trực không deploy/rollback được.
- 1 — có cả hai tầng nhưng lẫn (Go/No-Go mở bằng thuật ngữ; hoặc runbook đúng nhưng thiếu ngưỡng/bước cụ thể khiến người ngoài phải hỏi lại).
- 2 — MỞ bằng 1–3 dòng lãnh đạo (sẵn sàng chưa / ký gì / hỏng thì sao + ai trực), không jargon; RỒI tới runbook+rollback cụ thể để dev+người-trực hành động không cần tác giả; cả trang scan 2–3 phút.

## 3. BÁM NGUỒN — kéo từ GĐ trước, không bịa (xương sống)

Nguồn hợp lệ = artifact GĐ trước ĐÃ qua cổng HOẶC input ngoài user cung cấp KÈM cảnh báo ⚠️; dùng input ngoài mà THIẾU cảnh báo → trừ điểm (không minh bạch nguồn); vẫn CẤM bịa cái user không đưa.

- 0 — bịa "UAT/Security đã ký" khi report GĐ12 không có; hoặc bịa trạng thái checklist / kết quả rollback-test / số monitoring / flag không có căn cứ; hoặc bỏ qua known issue của uat.
- 1 — chủ yếu bám report GĐ12 nhưng một chỗ suy đoán không gắn nhãn (giả định pass / migration / flag mà không ghi "giả định / còn thiếu").
- 2 — mọi sign-off, tỷ lệ pass, gap, flag đều truy về được Test & Verification Report GĐ12 hoặc state; chỗ chưa có ghi rõ "CHƯA CÓ — chặn GO / còn thiếu, ai lo", không tô hồng.

## 4. ĐỦ-LÀ-ĐỦ — độ sâu tỉ lệ rủi ro, không thủ tục thừa

- 0 — máy móc: bắt vá nhỏ đi đủ 5 bậc rollout + rollback-test rườm + 12 dòng đầy; HOẶC ngược lại, hệ quan trọng mà rút gọn ẩu — rollback không test, migration không có backward script, rollout không chia bậc.
- 1 — độ sâu phần lớn hợp lý, thừa/thiếu ở 1–2 chỗ.
- 2 — nặng đúng chỗ rủi ro (migration, nhiều bên phụ thuộc), nhẹ đúng chỗ quen (nhiều N/A, gộp bậc rollout, full ngay có lý do); không bỏ artifact/ô nào, phần rút gọn có lý do 1 dòng.

## 5. TRACEABILITY — nối GĐ12 ↔ GĐ14

- 0 — không nối GĐ12 (không nhắc report/sign-off) và không nối GĐ14 (không nói đo gì / bàn giao gì sau release).
- 1 — nối một đầu (nhận từ `uat` HOẶC bàn giao `operate`), thiếu đầu kia.
- 2 — kéo rõ từ GĐ12 (sign-off + pass rate + known issue) và chuyển rõ sang GĐ14 (đã lên pha nào, monitoring bật, metric/ngưỡng cần theo dõi, đóng vòng target GĐ1).

## 6. CỔNG + PHÂN VAI ĐÚNG (A5)

- 0 — `ship` tự bấm GO/NO-GO thay Người duyệt (CTO+PO); hoặc không có cổng go/no-go; hoặc NO-GO là điểm chết / dùng câu phủ định cứng, không kèm điều kiện chuyển thành GO; hoặc lấn vai (tự sửa code / kiểm lại test / dựng ops dashboard).
- 1 — có cổng nhưng phân vai mờ (không rõ CTO+PO quyết), hoặc khuyến nghị lẫn với quyết định, hoặc đề xuất thiếu lý do + phương án đã loại.
- 2 — cổng hỏi đúng Người duyệt (CTO+PO); `ship` chỉ khuyến nghị kèm lý do + phương án loại; NO-GO luôn kèm thiếu-gì / ai-làm / bao-lâu để GO lại; không lấn vai skill khác.

## 7. BÀN GIAO ĐÚNG SKILL KẾ

- 0 — không có khối bàn giao, hoặc chỉ sai skill (đẩy về `idea`/`frame` thay vì `operate`).
- 1 — có bàn giao sang `operate` nhưng tự chọn hộ user, hoặc thiếu ngữ cảnh (không nói theo dõi gì / đường lùi về `uat` khi gặp gap).
- 2 — khối bàn giao sang `operate` (GĐ14) kèm metric/alert cần theo dõi + đường quay `uat` khi hở chất lượng + quay `/ship` khi tới mốc mở pha rollout kế; chỉ liệt kê, không quyết hộ.

## Gate

Tiêu chí 1, 2, 3 là xương sống. Bất kỳ cái nào = 0 → bản SHIP **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Lý do: một bản 12/14 nhưng thiếu rollback (tc1=0) hoặc bịa security sign-off (tc3=0) sẽ khiến lãnh đạo ký nhầm cho lên một release không lùi được — nguy hiểm hơn một bản gọn mà thiếu điểm phụ. Khi so nhiều bản: loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Khung report (xếp nhiều bản cạnh nhau)

```
BẢN <id> — ship — TỔNG __/14   GATE: ĐẠT / RỚT (rớt ở tc__)
  1 Đúng+đủ artifact (gate)  : _/2    · 2 Đọc-được 3 tầng (gate) : _/2   · 3 Bám nguồn GĐ12 (gate) : _/2
  4 Đủ-là-đủ                 : _/2    · 5 Traceability          : _/2   · 6 Cổng + phân vai       : _/2
  7 Bàn giao                 : _/2
  Mạnh:  <1 dòng>
  Thủng: <1 dòng — ưu tiên chỗ rớt gate>
```

## Vì sao các tiêu chí này

Ba tiêu chí gate đo *có ra đúng thứ + đọc được + trung thực không*; các tiêu chí sau đo *có đúng kỷ luật pipeline không* (đủ-là-đủ, không lấn vai, cổng/traceability, bàn giao). Gộp lại = trọn hợp đồng của `ship`, không hơn. Thêm một tiêu chí mới chỉ khi có một kiểu lỗi thật lặp lại mà bộ hiện tại không bắt được.
