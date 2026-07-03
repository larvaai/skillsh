# TUNE — skill `delivery` (dựa trên chấm artifact 11-delivery.md, gói rebuild-hex-agent)

> Chạy nguyên vẹn theo quy trình `tune/SKILL.md`: fixture cố định · MỘT biến duy nhất (bản sửa `delivery/SKILL.md`) · chấm mù bằng rubric · baseline trước · confirm bằng agent mới + fixture thứ hai chống over-fit.

---

## §0 Chẩn đoán (≤6 câu)

Artifact được chấm **14/14, đạt gate** (cả 3 xương sống 1·2·3 đều = 2) — không tiêu chí nào mất điểm, nên về mặt điểm số **không có đòn bẩy tune nào**. Điểm yếu thật DUY NHẤT ("SỬA TRƯỚC TIÊN" của grade) là D4 "0-secret" đo bằng Redactor key-only (redaction.py:41-63 chỉ match TÊN key, không soi VALUE) → secret nhúng trong value (Bearer token, URL có credential) lọt, khiến cổng "0-secret" có thể xanh-giả. Nhưng D1–D5 là **sản phẩm của LẦN CHẠY** cho riêng HexAgent — `delivery/SKILL.md` KHÔNG hề có khái niệm invariant-kiểm-được nào; SKILL chỉ nói "DoD là luật" và "test bám Contract GĐ10" ở mức tổng quát. Vậy lỗi D4-key-only là **lỗi-của-lần-chạy** (agent viết một dòng DoD chưa buộc test soi value), KHÔNG phải luật thiếu/mơ hồ/mâu thuẫn trong SKILL. Hai chỗ "sai chi tiết" khác grade nêu (đếm 15 vs 14 SECRET_KEYS; RuntimeEvent 14 vs 15 field) là lỗi phía người-chấm / thượng-nguồn ATLAS, cũng không đụng SKILL. **Kết luận: gần như toàn bộ điểm-yếu-còn-lại thuộc lần-chạy; SKILL delivery không có tiêu chí nào đang mất điểm để tune.**

---

## §1 Fixture đề xuất (cố định cả thí nghiệm)

Lặp lại được, giữ y hệt cho baseline + mọi variant:

- **project / input**: gói `rebuild-hex-agent` — dùng đúng bộ đầu vào GĐ trước đã có trong `rebuild-hex-agent/pipeline/`: `10-modules.md` (6 module · 6 owner · 2 seam công khai) + `08-skeleton.md` (CI tối thiểu lint→pytest→audit) + `07-stack.md` (Python 3.11·LangGraph·SQLite·OpenAI-compatible·pytest+Hypothesis+audit) + `09-backlog.md` (Story+AC). Anchor: `00-understanding/REBUILD-BRIEF.md` (7 invariant) + `ATLAS.md`.
- **code gốc đối chiếu**: `/Users/uspro/Desktop/namnson/hex_agent` (rubric dùng để verify claim code).
- **chế độ chạy**: tự-quyết (đóng vai CTO/Kiến trúc sư sở hữu chuẩn · Eng-manager mở cổng), KHÔNG hỏi user — đúng như lần chạy gốc, để so được.
- **tham số**: level đọc từ `user-state.json` nếu có; sinh đủ 3 artifact (Standards 12 mục · DoR/DoD · PR Checklist) mở bằng Góc nhìn lãnh đạo.
- **fixture thứ hai (cho Bước 5 confirm)**: một project domain khác chuẩn-rủi-ro-cao NHƯNG không có invariant kiểu HexAgent — ví dụ hệ **thanh toán nhiều team** (secret + migration + PII), để xem bản sửa có over-fit vào "5 invariant" của HexAgent không.

Ghi 3 hằng số (project/level/mode + chế-độ-tự-quyết) ra `experiments/runs/<ts>/fixture.txt`; không ai đổi giữa chừng.

---

## §2 Thước

- **Rubric chấm**: `/Users/uspro/Desktop/skillsh/experiments/hex-rebuild-review/rubrics/11-delivery.rubric.md` (7 tiêu chí 0/1/2; xương sống 1·2·3).
- **Luật xếp hạng**: **loại hết bản RỚT GATE trước** (bất kỳ tiêu chí 1/2/3 = 0 → loại dù tổng cao), **rồi xếp theo TỔNG**; hoà tổng → bản có **diff NHỎ/robust hơn** thắng (ít rủi ro over-fit vào đúng fixture này).
- Chấm **mù**: agent chấm chỉ thấy {project, level, mode, output}, không thấy variant nào theo hướng gì.

---

## §3 Hướng thử A/B/C/D (mỗi hướng nhắm ĐÚNG MỘT tiêu chí khác, diff tối thiểu)

> Lưu ý khung: baseline đã 14/14 nên các hướng dưới **không kỳ vọng tăng điểm trên fixture HexAgent** (không còn điểm để tăng) — mục tiêu là **giữ 14/14 trên fixture gốc VÀ nâng điểm/robust trên fixture thứ hai** (chống over-fit + bịt lỗ đo-được). Đây là lý do §4 xếp ưu tiên thấp.

### Hướng A — buộc chuẩn đo-được TỚI VALUE (nhắm **Tiêu chí 3 — DÙNG ĐƯỢC THẬT**)
- **Giả thuyết**: nếu SKILL yêu cầu mọi cổng "0-secret / 0-X" phải nói RÕ đo ở cấp nào (key vs value), agent sẽ không viết cổng xanh-giả như D4 key-only.
- **Diff (thêm 1 gạch đầu dòng vào "Luật cứng", sau dòng "DoD là luật")**:
  ```
  - **Cổng "0-X" phải nói ĐO Ở ĐÂU.** Mọi tiêu chí kiểu "0 secret / 0 leak / 0 bypass"
    ghi rõ kiểm ở cấp nào (tên field vs NỘI DUNG value; tĩnh vs động) — nếu công cụ hiện
    chỉ soi được một cấp, ghi cấp còn lại thành open-Q "chưa soi được → sẽ đo ở đâu",
    KHÔNG để cổng ngầm hiểu đã phủ hết.
  ```
- **Rủi ro**: có thể đẻ thêm chữ ở mọi cổng, làm loãng đoạn Góc-nhìn-lãnh-đạo (đụng Tiêu chí 6) nếu agent viết dài; giữ diff ở mức một câu để tránh.

### Hướng B — chốt danh sách 12 mục Standards ngay trong SKILL để tránh lệch-đếm (nhắm **Tiêu chí 2 — ĐÚNG-ĐỦ BỘ CHUẨN**)
- **Giả thuyết**: SKILL đã liệt kê 12 mục nhưng rải trong prose; đóng khung thành checklist đánh-số buộc agent tự-kiểm đủ-12 trước khi chốt, giảm rủi ro bỏ mục ở project ít-rủi-ro.
- **Diff (đổi block "Mười hai mục của template" ở Artifact 1 thành checklist đánh số + 1 câu tự-kiểm)**:
  ```
  12 mục BẮT BUỘC (rút độ sâu được, KHÔNG bỏ mục):
  1 Repository 2 Branching 3 Coding standard 4 Review policy 5 Testing pyramid
  6 CI/CD 7 Environment 8 Secret 9 Feature flag 10 Migration 11 Observability 12 Incident.
  Trước khi chốt: đếm lại đủ 12 số; thiếu số nào → bổ, không chốt.
  ```
- **Rủi ro**: baseline đã đủ 12 mục nên hướng này gần như không đổi điểm trên fixture gốc; giá trị chỉ lộ ở fixture project-nhỏ (dễ bỏ mục) — cần fixture thứ hai mới thấy, dễ "phí một agent" nếu chỉ chấm trên HexAgent.

### Hướng C — buộc kế thừa CI/stack GĐ7/GĐ8 tường minh, cấm dựng lại (nhắm **Tiêu chí 4 — NỐI CHUỖI PIPELINE**)
- **Giả thuyết**: nếu SKILL bắt trích DẪN NGUỒN cho CI + pyramid + owner (chứ chỉ "đọc để không bịa"), agent sẽ luôn nối chuỗi thay vì mô tả CI chung chung ở project thiếu artifact GĐ8.
- **Diff (thêm vào cuối mục "Đầu vào — đọc trước khi hỏi", trước đoạn "Không có artifact GĐ10…")**:
  ```
  - **Kế thừa phải trích nguồn.** CI/CD, test pyramid, owner/CODEOWNERS phải GHI RÕ
    lấy từ đâu (GĐ8 CI tối thiểu · GĐ7 test stack · GĐ10 owner) — không mô tả lại từ
    trí nhớ. Không có artifact GĐ đó → ghi "giả định, cần <skill> xác nhận", không bịa số.
  ```
- **Rủi ro**: baseline vốn đã nối chuỗi hai đầu (grade xác nhận Tiêu chí 4 = 2) → trên HexAgent không tăng điểm; chỉ hữu ích cho project brownfield thiếu GĐ trước.

### Hướng D — mẫu Góc-nhìn-lãnh-đạo có cả bảng DORA "chưa có số" (nhắm **Tiêu chí 6 — ĐỌC ĐƯỢC 3 TẦNG**)
- **Giả thuyết**: cho SKILL một mini-mẫu 60-giây (DoD một khối + bảng 4 DORA kèm cột "số baseline chưa có → đo ở Operate") để agent calibrate, giảm rủi ro đoạn mở lẫn jargon hoặc bịa số DORA.
- **Diff (thêm 1 block ví dụ ngắn ngay dưới "Góc nhìn lãnh đạo" của Artifact 1)**:
  ```
  Mẫu 60-giây (đọc riêng vẫn đủ): 1) DoD gói MỘT khối; 2) bảng 4 DORA:
  cột [chỉ số | ý nghĩa nghiệp vụ | ĐO Ở ĐÂU]; số baseline CHƯA chạy prod → ghi
  "chưa có → OQ, đo ở Operate GĐ14", KHÔNG điền số cho đẹp.
  ```
- **Rủi ro**: baseline đã làm đúng đoạn mở (Tiêu chí 6 = 2, có ⚠️ số DORA chưa có) → mẫu này chỉ là bảo hiểm cho lần chạy khác; nếu agent copy máy móc mẫu vào project không hợp có thể phản tác dụng.

*(4 hướng nhắm 4 tiêu chí khác nhau: 3 / 2 / 4 / 6. Không hướng nào nhắm 1/5/7 vì các tiêu chí đó không có tín hiệu yếu trong grade — thêm sẽ trùng phí agent.)*

---

## §4 Ưu tiên

**KHÔNG ĐÁNG TUNE (để sau nếu muốn robust).** Artifact đạt **14/14, gate pass**, và điểm-yếu-thật duy nhất (D4 key-only) là **lỗi-của-lần-chạy** — một dòng DoD chưa buộc test soi value — chứ KHÔNG phải luật thiếu/mơ hồ/mâu thuẫn trong `delivery/SKILL.md` (SKILL không có khái niệm invariant nào để mà sai). Theo luật `tune` "grade cao & lỗi thuộc lần-chạy → không đáng tune". Nếu vẫn muốn một vòng bảo-hiểm-chống-over-fit, chạy **Hướng A** (đo-được-tới-value) — hướng duy nhất chạm được lỗi thật ở cấp SKILL — và chỉ merge nếu nó giữ 14/14 trên HexAgent VÀ không làm hỏng đoạn mở trên fixture thứ hai.

---

## §5 Nhắc luật thí nghiệm (bắt buộc khi chạy)

- **Baseline trước**: chạy `delivery` HIỆN TẠI trên fixture → chấm bằng rubric → mốc 14/14. Không có baseline thì không biết variant là tiến hay lùi.
- **Một biến duy nhất**: mọi variant cùng fixture (cùng project + đầu vào GĐ trước + chế-độ-tự-quyết + level), chỉ khác bản sửa SKILL; đổi fixture giữa chừng → làm lại.
- **Chấm mù**: agent chấm chỉ thấy {project, level, mode, output.txt}, không thấy variant theo hướng nào.
- **Confirm bản thắng bằng agent MỚI + fixture thứ hai**: chạy lại `proposed-SKILL.md` của bản thắng trên (a) HexAgent và (b) project thanh-toán-nhiều-team ở §1; chỉ hơn ở fixture gốc = có mùi over-fit → xem lại diff. Vì baseline đã kịch trần, phép confirm ở đây quan trọng hơn "tăng điểm" — nó chứng minh bản sửa KHÔNG làm rớt điểm ở domain khác.
- **Không đụng bản thật khi đang thử**: mỗi variant nằm trong `experiments/runs/<ts>/<variant>/`; `delivery/SKILL.md` thật chỉ đổi sau khi có bản thắng đã qua confirm và Son chốt.
