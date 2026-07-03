# TUNE — skill `operate` (từ chấm 14-operate trong gói rebuild-hex-agent)

Nguồn: grade `grades/14-operate.grade.md` (TỔNG 13/16, RỚT GATE ở tiêu chí 1) · rubric `rubrics/14-operate.rubric.md` · SKILL `.claude/skills/operate/SKILL.md` · artifact `rebuild-hex-agent/pipeline/14-operate.md`. Quy trình bám `.claude/skills/tune/SKILL.md`.

## §0 — Chẩn đoán (≤6 câu)

Điểm mất tập trung ở **tiêu chí 1 (SỐ THẬT, xương sống) = 0** (kéo rớt gate dù tổng 13/16) và **tiêu chí 7 (ĐỌC-ĐƯỢC 3 TẦNG) = 1**; sáu tiêu chí còn lại đều 2. Lỗi tiêu chí 1 là **hỗn hợp**: phần lớn là **lỗi-của-lần-chạy** (agent tự nâng ba test PENDING ở GĐ12 — sandbox-escape, redact, false_finish-trên-smoke — thành số-đã-đo/"ĐẠT ở nền" và bịa "15 SECRET_KEYS" trong khi `redaction.py` có 14 key), nhưng có **một mầm lỗi-của-SKILL**: luật "Đo bằng số" chỉ cấm *bịa số cho đẹp* và bắt ghi `chưa có số`, nó **KHÔNG có luật cấm dùng kết quả một test CHƯA CHẠY như số đo-được**, cũng **không bắt số-an-toàn-biên phải trích `file:line`/`test-id + trạng thái PASS/PENDING`** — nên agent lách qua khe hở "test đã có, kết quả kỳ vọng = 0" mà vẫn thấy mình tuân luật. Lỗi tiêu chí 7 là **lỗi-của-SKILL rõ**: luật cứng viết "Mỗi artifact PHẢI (a) MỞ bằng Góc nhìn lãnh đạo" nhưng template §Thân chỉ đặt dòng lãnh-đạo mẫu cho **Dashboard**; Incident và Iteration trong template mở thẳng vào code-block kỹ thuật, để "Góc nhìn lãnh đạo" thành đoạn văn xuôi CUỐI mỗi artifact — model bắt chước template nên §2/§3 thiếu tầng lãnh đạo mở-đầu. Kết luận: tiêu chí 7 và cái khe "test-chưa-chạy" của tiêu chí 1 **đáng tune**; phần bịa "15 key" + tự khen "ĐẠT ở nền" thuần là chạy ẩu, tune chỉ giảm xác suất chứ không xoá hẳn.

## §1 — Fixture đề xuất (cố định cả thí nghiệm)

Giữ **nguyên** input đã sinh ra artifact được chấm, để so được với baseline thật:

- **Skill tune**: `operate` (chỉ biến = bản sửa `operate/SKILL.md`).
- **Project**: `hex_agent` (clean rebuild). Code gốc đối chiếu: `/Users/uspro/Desktop/namnson/hex_agent` (đặc biệt `control/redaction.py` = 14 SECRET_KEYS).
- **Đầu vào GĐ trước** (nguồn của artifact, đọc y như lần chạy gốc):
  - GĐ13 ship: `rebuild-hex-agent/pipeline/13-ship.md` (GO alpha nội bộ · write/delegation OFF · rollback = tắt flag `features.yaml` · alert cứng `false_finish_total>0` · incident owner 4 team · OQ-1 treo).
  - GĐ12 uat: `rebuild-hex-agent/pipeline/12-uat.md` (26 PASS / 2 PENDING; TC-SANDBOX-ESCAPE-001 = PENDING, TC-REDACT-* = PENDING — chính chỗ agent nâng khống).
  - GĐ9 backlog + GĐ1 idea: `rebuild-hex-agent/pipeline/09-backlog.md` + `ideas/hex-agent-rebuild.md` (M1 zero-false-finish · M2 bounded · M3 no-escalation · OQ-1 baseline chưa có số).
  - GĐ8 skeleton: `rebuild-hex-agent/pipeline/08-skeleton.md` (0/9 tick THẬT — code rebuild chưa chạy staging).
- **Mode/level**: artifact operate không có mode; cố định **chế độ tự-quyết** (người viết đóng vai CEO/CTO+PO, không hỏi user) đúng như lần chạy gốc — nếu không mỗi variant sẽ dừng hỏi và không so được.
- Ghi 3 hằng số (project · nguồn GĐ trước · chế độ tự-quyết) ra `experiments/runs/<ts>/fixture.txt`. Mọi variant đọc đúng file này; cấm đổi nguồn giữa chừng.

## §2 — Thước

- Rubric: `/Users/uspro/Desktop/skillsh/experiments/hex-rebuild-review/rubrics/14-operate.rubric.md` (8 tiêu chí × 0/1/2, tối đa 16; xương sống = 1,2,3).
- Luật xếp hạng: **loại hết bản rớt gate trước** (bất kỳ tiêu chí 1/2/3 = 0 → loại, dù tổng cao), **rồi mới xếp theo Tổng**; hoà Tổng → bản có DIFF NHỎ/ROBUST hơn thắng.
- Chấm mù: người chấm chỉ thấy {project, nguồn GĐ trước, chế độ, output.txt}, KHÔNG thấy variant theo hướng nào. Đối chiếu số về code gốc `/Users/uspro/Desktop/namnson/hex_agent` + artifact GĐ trước (đặc biệt spot-check ≥5 số + đi lại 1 sự cố giả định như rubric yêu cầu).

## §3 — Các hướng thử (mỗi hướng nhắm ĐÚNG MỘT tiêu chí đang mất điểm)

### Hướng A — Luật "test-chưa-chạy KHÔNG phải số đo" (nhắm tiêu chí 1, xương sống — chỗ rớt gate)

- **Giả thuyết:** nếu SKILL cấm rõ việc trình kết-quả một test PENDING/chưa-chạy như số-đo-được và bắt mỗi số-an-toàn-biên phải kèm trạng thái PASS/PENDING của test-id nguồn, agent sẽ hạ "0 sandbox-escape / 0 secret / false_finish trên smoke" xuống `chưa có số` → không rớt gate tiêu chí 1.
- **DIFF (thêm vào mục "Luật cứng", sau bullet "Đo bằng số, không cảm tính"):**
  ```
  - **Kết quả một test CHƯA CHẠY KHÔNG phải một con số.** Một test-case chưa PASS thật (PENDING/blocked/chưa có lượt chạy trên môi trường thật) thì kết-quả-kỳ-vọng của nó (vd "0 escape", "0 secret", "false_finish=0") KHÔNG được đưa lên dashboard như số-đã-đo, KHÔNG được dùng chống-lưng cổng GO, KHÔNG được viết "ĐẠT/đã chứng minh bằng số". Ghi `chưa có số` + trạng thái test nguồn (test-id + PASS/PENDING/chưa-chạy, ở GĐ nào) + khi nào đo được. Mỗi con số an-toàn-biên phải trích được nguồn kiểm: PASS thật ở GĐ nào, hoặc `file:line` code. "Test đã tồn tại" ≠ "đã đo".
  ```
- **Rủi ro:** thêm luật cứng thứ 8 có thể làm model quá dè dặt, hạ CẢ những số đã PASS thật xuống `chưa có số` (mất điểm tiêu chí 1 chiều ngược — số thật mà không dám tuyên); cần chấm xem có "under-claim" không.

### Hướng B — Template lãnh-đạo-trước cho CẢ ba artifact (nhắm tiêu chí 7)

- **Giả thuyết:** nếu template §Thân của Incident và Iteration cũng MỞ bằng một dòng "▸ ĐỌC CHO LÃNH ĐẠO" như Dashboard (thay vì để góc-nhìn-lãnh-đạo thành văn xuôi cuối bài), model sẽ đặt tầng lãnh đạo đúng đầu mỗi artifact → tiêu chí 7 lên 2.
- **DIFF (sửa hai code-block template trong §Thân — thêm 1 dòng mở đầu mỗi cái):**
  ```
  INCIDENT PROCESS
    ▸ ĐỌC CHO LÃNH ĐẠO (1 dòng): <số incident>; khi hỏng ai trực + lùi trong bao lâu (nối MTTR/DORA).
    1. Phát hiện   : ...
  ```
  ```
  ITERATION LOOP
    ▸ ĐỌC CHO LÃNH ĐẠO (1 dòng): đã đạt/chưa đạt mục tiêu GĐ1 + ba việc kế (CEO/CTO quyết đầu tư vào đâu).
    Nhịp review : ...
  ```
  Và sửa 1 câu ở "Luật cứng (a)" cho khớp template: *"Mỗi artifact MỞ bằng một dòng '▸ ĐỌC CHO LÃNH ĐẠO' riêng (kể cả Incident và Iteration), KHÔNG gộp chung vào khối lãnh đạo tổng đầu bài."*
- **Rủi ro:** ba dòng lãnh-đạo lặp có thể trùng khối "Góc nhìn lãnh đạo tổng" đầu bài → dài dòng, phạm điều kiện level-1 tiêu chí 7 "lan man quá mức đọc-90-giây"; cần giữ mỗi dòng đúng 1 câu.

### Hướng C — Tự-soi thêm bước "gạch số chưa-đo khỏi chống-lưng cổng GO" (nhắm tiêu chí 1, xương sống — góc khác A)

- **Giả thuyết:** lỗi rớt gate không chỉ ở dashboard mà ở **cổng GO viện số chưa-đo làm lý do** ("Nền R1 an toàn đã chứng minh BẰNG SỐ"); nếu bước Tự-soi buộc rà lại từng số trong khối cổng và loại số chưa-PASS khỏi lý do GO, agent sẽ không chống-lưng cổng bằng số ma → cứu tiêu chí 1 từ phía cổng.
- **DIFF (thêm 1 bullet vào "Tự soi trước khi chốt"):**
  ```
  - Khối CỔNG go/no-go: mọi con số dùng làm LÝ DO GO/NO-GO có phải số đã PASS thật (không phải kết-quả-kỳ-vọng của test PENDING) không? Số chưa đo → GỠ khỏi lý do cổng, chuyển thành `chưa có số` + để CEO/CTO quyết. Cổng KHÔNG được viết "đã chứng minh bằng số" nếu số đó chưa đo.
  ```
- **Rủi ro:** trùng mục tiêu tiêu chí với Hướng A (cùng đánh tiêu chí 1) — nhưng khác ĐIỂM CAN THIỆP (A = luật cứng chặn từ đầu dashboard; C = tự-soi bắt ở cổng); nếu cả hai cùng qua thì so xem chặn-từ-đầu hay bắt-cuối hiệu quả hơn, KHÔNG chạy cả hai như một hướng.

### Hướng D — Bắt trích `file:line` cho mọi claim-code, kể cả số đếm cấu hình (nhắm tiêu chí 1 — riêng lỗi "15 vs 14 key")

- **Giả thuyết:** "15 SECRET_KEYS" sai vì agent đếm nhẩm/kế thừa "~15" của GĐ12 mà không mở code; nếu SKILL bắt mọi con số kể-số-cấu-hình (số key redact, số flag, số team owner) phải trích `file:line` code gốc và tự đếm lại, agent sẽ ra 14 → bớt một claim-code sai.
- **DIFF (thêm vào bullet "Đo bằng số" hoặc mục Đầu vào):**
  ```
  - **Số đếm cấu hình phải mở code đếm lại, không kế thừa số xấp xỉ.** Bất kỳ con số đếm phần tử trong code (số SECRET_KEYS, số flag, số allow-list…) phải trích `file:line` gốc và tự đếm — KHÔNG lấy số "~N"/ước lượng từ artifact GĐ trước. Số kế thừa có dấu "~" → mở code chốt số chính xác trước khi đưa lên dashboard.
  ```
- **Rủi ro:** hẹp — chỉ cứu đúng một loại lỗi (số đếm cấu hình); nếu artifact fixture chỉ có 1 chỗ dạng này thì cải thiện tiêu chí 1 rất nhỏ, có thể không đủ lật gate một mình (phải đi kèm A hoặc C). Đây là hướng "bổ trợ", cân nhắc bỏ nếu chỉ chạy 3 hướng.

> Bốn hướng nhắm hai tiêu chí đang mất điểm: **A, C, D → tiêu chí 1** (ba điểm-can-thiệp khác nhau: luật-đầu-nguồn / tự-soi-cổng / số-đếm-cấu-hình), **B → tiêu chí 7**. Nếu chỉ chạy 3 agent: giữ **A, B, C** (bỏ D vì hẹp nhất); D chỉ thêm khi muốn phủ luôn lỗi "15 key".

## §4 — Ưu tiên

**TUNE NGAY** (mức vừa — không khẩn nhưng đáng). Lý do: tiêu chí 1 làm artifact RỚT GATE và có một **khe hở lỗi-của-SKILL thật** (luật hiện tại cấm "bịa số cho đẹp" nhưng không cấm "dùng kết-quả test chưa-chạy như số đo") — đây là kiểu lỗi sẽ lặp ở mọi hệ chưa-chạy-đủ-thật, không chỉ hex_agent; thêm tiêu chí 7 là lỗi-template rõ ràng, sửa rẻ (thêm 2 dòng). Cảnh báo: phần bịa "15 key" + tự khen "ĐẠT ở nền" nghiêng về lỗi-của-lần-chạy — tune giảm xác suất chứ không đảm bảo hết, đừng kỳ vọng lật gate 100% chỉ bằng sửa prompt.

## §5 — Nhắc luật thí nghiệm

- **Có thước trước khi chạy:** rubric 14-operate đã có (`rubrics/14-operate.rubric.md`) — đủ điều kiện tune (không phải explain nên KHÔNG dùng skill `grade`; chấm bằng rubric này).
- **Baseline trước:** chấm lại chính artifact gốc `rebuild-hex-agent/pipeline/14-operate.md` bằng rubric → mốc 13/16 RỚT GATE. Mọi variant phải (a) qua gate và (b) ≥ 13 mới đáng theo.
- **Một biến duy nhất:** mọi variant cùng fixture §1, chỉ khác đoạn thêm/sửa vào `operate/SKILL.md`; không đụng bản thật trong khi thử (mỗi variant ở `experiments/runs/<ts>/<variant>/proposed-SKILL.md`).
- **Chấm mù:** người chấm không thấy variant theo hướng nào.
- **Confirm bản thắng bằng agent MỚI + fixture thứ hai:** chạy lại `proposed-SKILL.md` thắng bằng agent mới trên (a) đúng fixture hex_agent và (b) **một project thứ hai** có mục tiêu GĐ1 + có test PENDING chưa chạy (vd một hệ live-slice khác trong pipeline, hoặc case-mgmt mẫu trong SKILL) — để chắc điểm đến từ SỬA, không phải agent viết khéo. Chỉ hơn ở fixture gốc → nghi over-fit, xem lại diff.
