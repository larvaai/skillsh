# Rubric — chấm một bản chạy skill `modules` (GĐ10)

Mỗi tiêu chí 0/1/2. Chuẩn gốc để chấm: `modules/SKILL.md` + `quy-trinh-idea-to-operate.md` mục "## Giai đoạn 10 — Module & Team Ownership". Rubric chỉ biến hợp đồng đó thành thước đo — KHÔNG thêm tiêu chuẩn mới. 7 tiêu chí; 3 tiêu chí đầu là XƯƠNG SỐNG (gate).

**Đầu vào để chấm (fixture):** bộ artifact modules (Module Map + Module Contract) cần chấm · Domain Model GĐ5 + backlog GĐ9 làm nguồn

## 1. ĐÚNG + ĐỦ ARTIFACT (xương sống)

Sinh đủ hai artifact: **Module Map** (bounded context → module → owner + phụ thuộc) và **Module Contract** cho MỌI module. Mỗi contract có tối thiểu Owner + Responsibilities + Owns + Does NOT own + Public API.

- 0 — thiếu một artifact (không có Module Map HOẶC thiếu Contract của ≥1 module); hoặc contract thiếu ô lõi (Owner / Owns / **Does NOT own** / Public API) không phải do rút gọn có chủ đích.
- 1 — đủ hai artifact nhưng một vài ô sơ sài hoặc thiếu ô phụ (event/permission/error code/SLA/SLO/test contract) ở nơi lẽ ra cần.
- 2 — đủ Module Map + Contract cho mọi module; mỗi module đúng 1 owner + ranh giới does-NOT-own rõ; contract đủ ô, ô rủi ro thấp được rút gọn hợp lý chứ không bỏ; REST mô tả bằng OpenAPI.

## 2. ĐỌC-ĐƯỢC 3 TẦNG (xương sống)

Mở bằng Góc nhìn lãnh đạo ("ai sở hữu cái gì / gọi ai khi sự cố") rồi mới tới chi tiết dev; 1 trang, scan 2–3 phút.

- 0 — không có Góc nhìn lãnh đạo, HOẶC đâm thẳng vào API/schema/event/OpenAPI; hoặc dev đọc contract vẫn không đủ để gọi vào module (thiếu API/permission/error/does-NOT-own).
- 1 — có cả hai tầng nhưng lệch: góc lãnh đạo còn kỹ thuật/mờ, hoặc phần dev thiếu một mảnh hành động được.
- 2 — mở bằng 1–3 thứ CEO/CTO nhìn bằng ngôn ngữ nghiệp vụ (không jargon); rồi contract đủ API/event/data-ownership/permission cho dev; gọn 1 trang.

## 3. BÁM NGUỒN — dùng artifact GĐ trước, không bịa (xương sống)

Ranh giới bám Domain Model (GĐ5) + phủ hết feature backlog (GĐ9), không bịa. Nguồn hợp lệ = artifact GĐ trước ĐÃ qua cổng HOẶC input ngoài user cung cấp KÈM cảnh báo ⚠️; dùng input ngoài mà THIẾU cảnh báo → trừ điểm (không minh bạch nguồn); vẫn CẤM bịa cái user không đưa.

- 0 — bịa bounded context/entity/event không có trong domain (GĐ5) hay backlog (GĐ9); hoặc có feature GĐ9 không rơi vào module nào (feature mồ côi); hoặc mâu thuẫn code cũ (khi có atlas); hoặc tự chế ranh giới không dựa domain.
- 1 — chủ yếu bám nguồn, một chỗ suy đoán không gắn nhãn.
- 2 — mọi module/data/event truy về được bounded context (GĐ5) và capability (GĐ9); mọi feature GĐ9 có đúng một chủ; chỗ chưa chắc gắn nhãn.

## 4. CHIA THEO DOMAIN, KHÔNG THEO MÀN HÌNH

- 0 — ranh giới module đi theo màn hình/tính năng UI (mỗi màn hình một module) thay vì bounded context + data ownership; HOẶC một bảng/data bị chia cho hai module.
- 1 — phần lớn theo domain, một module lệch sang cắt theo màn hình.
- 2 — mọi module chia theo bounded context / data ownership / change frequency; ranh giới ra ngoài (Does NOT own) hiện rõ; lệch 1-context-1-module đều có lý do.

## 5. ĐỦ-LÀ-ĐỦ — độ sâu theo rủi ro, không thủ tục thừa

- 0 — bơm thủ tục thừa đều cho module phụ (SLA/SLO/test contract cho cái một team ít đổi) HOẶC rút gọn tới mức bỏ ô lõi ở module rủi ro cao.
- 1 — độ sâu hợp lý phần lớn, 1–2 chỗ thừa/thiếu.
- 2 — module lõi/nhiều team → contract đầy đủ; module phụ → gọn kèm lý do; không bỏ phần contract nào, chỉ rút gọn độ sâu.

## 6. TRACEABILITY — nối GĐ trước ↔ sau + ownership sạch + quyết định có lý do

Nối feature/domain → module, ownership không chồng, và ghi lý do + phương án đã loại cho mỗi lần gộp/tách.

- 0 — không nối được contract về domain/backlog; HOẶC data/event bị hai module cùng sở hữu; HOẶC có phần domain không module nào đỡ; HOẶC gộp/tách không kèm lý do.
- 1 — nối được nhưng lỏng, hoặc một phụ thuộc không đi qua contract, hoặc lý do gộp/tách mỏng / thiếu phương án đã loại ở vài chỗ.
- 2 — mỗi module đúng một owner, không chồng data/event, mọi phụ thuộc qua contract; sợi nối GĐ9/GĐ5 → GĐ11 rõ; mỗi gộp/tách có lý do + cách chia đã loại.

## 7. CỔNG + PHÂN VAI + BÀN GIAO

- 0 — thiếu cổng go/no-go, HOẶC AI tự tuyên bố GO/"đạt" thay CTO/user, HOẶC không bàn giao / bàn giao sai skill kế (không phải `delivery`).
- 1 — có cổng + bàn giao nhưng lệch: phân vai duyệt mờ, hoặc trình cổng thiếu bằng chứng, hoặc khối bàn giao tự chọn hộ skill tiếp / thiếu artifact path.
- 2 — cổng đúng câu doc + AI đóng vai Chủ sở hữu (Kiến trúc sư/EM trình bằng chứng, user/CTO giữ quyền GO) + bàn giao đúng sang `delivery` (GĐ11, nhắc `frame` cho slice) kèm artifact path; chỉ liệt kê, không chọn hộ.

## Gate & cách xếp nhiều bản

Tiêu chí **1, 2, 3** là xương sống. Bất kỳ cái nào = 0 → bản **RỚT GATE**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 12/14 nhưng bịa module không có trong domain (tiêu chí 3 = 0), hoặc thiếu Contract (tiêu chí 1 = 0), hoặc không đọc-được cho lãnh đạo (tiêu chí 2 = 0) vẫn rớt. Khi so nhiều bản: **loại hết bản rớt gate trước**, rồi mới xếp phần còn lại theo tổng (tối đa 14). Gate quan trọng hơn tổng.

## Khung report (cố định — xếp nhiều bản cạnh nhau)

```text
Bản: <id>          Tổng: <..>/14     Gate: PASS / RỚT (tiêu chí <n>)
1 Artifact      : <0/1/2> — <lý do 1 dòng>
2 Đọc-3-tầng    : <0/1/2> — <...>
3 Bám nguồn     : <0/1/2> — <...>
4 Chia-domain   : <0/1/2> — <...>
5 Đủ-là-đủ      : <0/1/2> — <...>
6 Traceability  : <0/1/2> — <...>
7 Cổng/bàn giao : <0/1/2> — <...>
Một dòng chốt   : <giữ / sửa gì trước khi dùng>
```

## Vì sao các tiêu chí này

Ba tiêu chí gate đo *có ra đúng thứ + đọc được + trung thực không*; các tiêu chí sau đo *có đúng kỷ luật pipeline không* (đủ-là-đủ, không lấn vai, cổng/traceability, bàn giao). Gộp lại = trọn hợp đồng của `modules`, không hơn. Thêm một tiêu chí mới chỉ khi có một kiểu lỗi thật lặp lại mà bộ hiện tại không bắt được.
