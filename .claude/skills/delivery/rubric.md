# Rubric — chấm một bản artifact `delivery` (GĐ11 Delivery / Implementation Standards)

Chuẩn gốc để chấm = `delivery/SKILL.md` + mục "## Giai đoạn 11 —" trong `quy-trinh-idea-to-operate.md`. Rubric chỉ biến hợp đồng đó thành thước — KHÔNG thêm tiêu chuẩn mới.

Mỗi tiêu chí chấm 0 / 1 / 2. Ba tiêu chí XƯƠNG SỐNG (gate) đánh dấu 🦴: #1, #2, #3.

**Đầu vào để chấm (fixture):** bộ artifact delivery (Delivery Standards + Definition of Done + PR Checklist) cần chấm · Module Map + Contract GĐ10 làm nguồn · project

## Tiêu chí

**1. 🦴 Đúng + đủ artifact đã liệt kê**
Sinh đủ 3 artifact GĐ11: **Delivery Standards** (đủ 12 mục: repo/branch/coding/review/test pyramid/CI-CD/env/secret/feature flag/migration/observability/incident, rút theo rủi ro) + **Definition of Ready + Definition of Done** (đủ dòng bắt buộc, kèm "không đạt → không release") + **PR Checklist** (9 dòng, có link story).
- 0: thiếu hẳn một artifact (vd không có DoD hoặc không có PR checklist), hoặc Delivery Standards rụng mục chuẩn cần cho mức rủi ro (vd hệ nhạy cảm mà không có secret/migration/rollback), hoặc lấn sang code slice / viết test-result.
- 1: đủ 3 artifact nhưng 1–2 mục sơ sài quá mức rủi ro, hoặc DoD thiếu 1 dòng lõi (test/CI/contract).
- 2: đủ 3 artifact, đủ 12 mục chuẩn sâu đúng mức rủi ro; DoD giữ nguyên khối, nêu rõ "không đạt → không release".

**2. 🦴 Đọc-được 3 tầng (lãnh đạo + dev)**
Standards + DoD MỞ bằng Góc nhìn lãnh đạo (DoD gói 1 khối + 4 chỉ số DORA, ngôn ngữ nghiệp vụ) RỒI mới tới chi tiết dev; 1 trang scan 2–3 phút; có mục "Tự soi trước khi chốt".
- 0: đổ thẳng pipeline/YAML/jargon, không có đoạn cho lãnh đạo; HOẶC exec đọc không biết on-track; HOẶC dev không đủ để hành động (không rõ branch/test tối thiểu/điều kiện merge).
- 1: có cả hai tầng nhưng lẫn thứ tự (mở bằng CI config), hoặc một tầng mỏng.
- 2: mở bằng DoD + DORA đọc được cho CTO/business, rồi dev đủ để biết branch/CI/PR-gate/"Done"; đúng thứ tự, 1 trang, có "Tự soi trước khi chốt".

**3. 🦴 Bám nguồn — dùng artifact GĐ trước, không bịa**
Dùng Module Map + Contract (GĐ10) + stack/CI đã có (skeleton GĐ8 / atlas); PR checklist "ảnh hưởng module khác?" / "update API contract?" nối vào Module Contract thật; không bịa module/stack/API mới. Nguồn hợp lệ = artifact GĐ trước ĐÃ qua cổng HOẶC input ngoài user cung cấp KÈM cảnh báo ⚠️; dùng input ngoài mà THIẾU cảnh báo → trừ điểm (không minh bạch nguồn); vẫn CẤM bịa cái user không đưa.
- 0: bịa module/contract/stack không có ở nguồn, hoặc bỏ qua hoàn toàn đầu vào GĐ10, hoặc dựng chuẩn mâu thuẫn `.ai-understanding/` khi brownfield.
- 1: bám nguồn phần lớn, 1 chỗ suy đoán không gắn nhãn, hoặc không nối checklist vào contract.
- 2: mọi chuẩn nối đúng Module Contract GĐ10; ô checklist nối thẳng contract; chỗ chưa có đầu vào thì nói rõ đang thiếu (giả định cần `modules` xác nhận), không bịa.

**4. Đủ-là-đủ (không thủ tục thừa)**
Độ sâu tỉ lệ rủi ro, không theo vị trí luồng. Team quen → Standards rút vài dòng; hệ quan trọng → đầy đủ. DoD/PR checklist KHÔNG rút theo kích thước việc.
- 0: áp full chuẩn nặng (luôn 12 mục dày) cho việc nhỏ, HOẶC cắt bước/bỏ DoD để cho ngắn.
- 1: có ý đủ-là-đủ nhưng áp chưa nhất quán, 1–2 chỗ thừa/thiếu.
- 2: nêu rõ mục nào rút / mục nào giữ theo rủi ro; DoD giữ nguyên đủ dòng bất kể kích thước việc; không bỏ mục nào.

**5. Traceability — nối GĐ trước ↔ sau**
Mỗi PR link story/requirement (nối ngược GĐ9/GĐ2–4); "ảnh hưởng module khác" nối Contract GĐ10; DoD "contract giữ" + test pyramid dẫn thẳng vào UAT GĐ12.
- 0: không có sợi link nào; PR checklist bỏ dòng link requirement.
- 1: có sợi traceability nhưng đứt một đầu (chỉ ngược, không xuôi sang uat).
- 2: PR link story (ngược GĐ9/2–4), chuẩn bám contract GĐ10, test pyramid dẫn vào UAT GĐ12; sợi liền hai đầu.

**6. Cổng + phân vai đúng (A5)**
Cổng đúng câu doc ("Item đạt DoD chưa?"); CTO/Kiến trúc sư sở hữu chuẩn, reviewer chỉ định duyệt PR, team owner giữ chất lượng module; AI draft + xin GO, KHÔNG tự tuyên bố pass thay người duyệt.
- 0: không có cổng go/no-go, hoặc `delivery` tự tuyên bố "đã Done"/mở cổng thay người, hoặc lấn vai (code slice / đào bug / vẽ lại module).
- 1: có cổng nhưng câu hỏi mờ hoặc phân vai AI-duyệt-chuẩn vs người-duyệt-PR mờ.
- 2: cổng "Item đạt DoD chưa?" rõ + phân vai đúng; AI chỉ trình khối + tự soi, chờ owner/CTO quyết.

**7. Bàn giao đúng skill kế**
Khối bàn giao trỏ `/uat` (GĐ12) là chính, kèm `/frame` (code slice) + `/review` (đào gap); chỉ liệt kê, không tự chọn hộ.
- 0: không có khối bàn giao, hoặc trỏ sai (vd tự code slice thay vì `/frame`, bỏ qua `/uat`).
- 1: có bàn giao nhưng thiếu skill kế chính (`uat`) hoặc tự chọn hộ user.
- 2: liệt kê đúng `/uat` (chính) + `/frame` + `/review`, để user quyết, không chọn hộ.

## Luật gate

Tiêu chí 1, 2, 3 là xương sống (🦴). Bất kỳ cái nào = 0 → bản **RỚT gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Ba xương sống bảo đảm: sinh đúng artifact, đọc-được cho cả lãnh đạo lẫn dev, và bám nguồn thật. Một bản đủ 7 mục nhưng bịa contract GĐ10 (tiêu chí 3 = 0) vẫn rớt — vì dev sẽ build sai ranh giới. Khi so nhiều bản: loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Khung report (cố định, để xếp nhiều bản cạnh nhau)

```
BẢN: <id>
🦴1 Đúng+đủ artifact   : _/2  — <1 dòng>
🦴2 Đọc-được 3 tầng    : _/2  — <1 dòng>
🦴3 Bám nguồn          : _/2  — <1 dòng>
 4 Đủ-là-đủ            : _/2  — <1 dòng>
 5 Traceability        : _/2  — <1 dòng>
 6 Cổng + phân vai     : _/2  — <1 dòng>
 7 Bàn giao            : _/2  — <1 dòng>
TỔNG: _/14   GATE: PASS/FAIL (rớt nếu bất kỳ 🦴 = 0)
Điểm mạnh nhất: <1 dòng>   Sửa trước tiên: <1 dòng>
```

## Vì sao 7 tiêu chí này

Ba cái đầu đo *có đúng cái delivery hứa không* (đủ artifact, đọc được 3 tầng, bám GĐ10) — nên là gate. Bốn cái sau đo *có gọn + nối đúng chuỗi không* (đủ-là-đủ, traceability, cổng/vai, bàn giao). Gộp lại = toàn bộ hợp đồng GĐ11, không hơn.
