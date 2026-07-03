# Tune — skill `uat` (từ chấm 12-uat.grade.md, gói rebuild-hex-agent)

## §0 Chẩn đoán (≤6 câu)

Bản chạy rớt **gate ở tiêu chí 1 (BẰNG CHỨNG)** = 0 vì hai lỗi bịa: (a) con số lãnh đạo "28/28 · 26 PASS · 2 PENDING" đảo ngược so với đếm bảng thật (35 dòng · 12 PASS · 23 PENDING), và (b) ~27 đường dẫn cột "Harness gốc" trỏ subdir không tồn tại (`tests/supervisor/…`, `tests/core/…`, `tests_audit/test_no_bypass_execute_tool.py`) trong khi `tests/` + `tests_audit/` gốc là thư mục PHẲNG; mất thêm 1 điểm ở tiêu chí 4 (jargon M1/S3.5.1/D2/ADR-006 rò vào khối lãnh đạo). Lỗi (a) — con số tự cộng sai, đảo tỉ lệ giữa 4 khối — thuần **lỗi-của-lần-chạy** (agent ẩu, không đếm lại bảng mình vừa viết); SKILL.md đã có luật "không bịa PASS" + "tự soi trước khi chốt" nhưng KHÔNG có bước ép đếm-lại-số-cho-khớp-bảng, nên đây là **lỗ luật đáng tune**. Lỗi (b) — SKILL.md tự thêm cột "Harness gốc" trỏ test file: template GĐ12 chuẩn chỉ có 5 mắt (Requirement→AC→TC→Result→Release), cột thứ 6 này là do agent tự bịa, KHÔNG phải luật trong SKILL — nhưng SKILL cũng THIẾU luật cấm trích path code chưa đối chiếu, nên tune được phần "gắn nhãn/đối chiếu". Lỗi (c) jargon-trong-khối-lãnh-đạo là lỗi-của-lần-chạy nhẹ nhưng SKILL chỉ nói "không jargon" chung chung, chưa liệt cấm cụ thể → tune được. Tóm: gate rớt vì 2 lỗi mà **1 lỗi thuần lần-chạy (con số) + 1 lỗi nửa-SKILL nửa-lần-chạy (path)** — tune được cả hai bằng cách siết luật, nhưng phải nói thẳng: nếu agent chịu đếm lại thì bản này lẽ ra 12/16 và chỉ suýt rớt.

## §1 Fixture đề xuất (cố định cả thí nghiệm)

- **Skill tune**: `uat`.
- **Project (input)**: gói rebuild-hex-agent — artifact GĐ12 dựng cho `hex-agent-rebuild`, code gốc đối chiếu tại `/Users/uspro/Desktop/namnson/hex_agent`.
- **Đầu vào cố định** (mọi variant đọc y hệt, không đổi giữa chừng):
  - `rebuild-hex-agent/pipeline/09-backlog.md` (Requirement/Story/AC gốc + Test ref TC-…),
  - `rebuild-hex-agent/pipeline/11-delivery.md` (DoD 9 dòng + invariant D1–D5 + test pyramid),
  - `rebuild-hex-agent/pipeline/10-modules.md` (2 seam contract),
  - code gốc `/Users/uspro/Desktop/namnson/hex_agent` để đối chiếu mọi trích test/path.
- **Nhiệm vụ**: sinh Test & Verification Report GĐ12 đầy đủ (Góc nhìn lãnh đạo · Mapping · Report lớp test · 2 sign-off · Cổng · Bàn giao).
- **Mode/level**: chế độ tự-quyết (đóng vai QA-lead · PO · CISO, không hỏi user), giống bản chạy gốc — để so 1:1.
- Ghi 4 hằng số này ra `experiments/runs/<ts>/fixture.txt`; mọi variant đọc đúng file này.

## §2 Thước

- Rubric: `/Users/uspro/Desktop/skillsh/experiments/hex-rebuild-review/rubrics/12-uat.rubric.md` (8 tiêu chí 0/1/2, tối đa 16; gate = tiêu chí 1·2·3).
- Luật xếp hạng: **loại hết bản rớt gate (bất kỳ tiêu chí 1/2/3 = 0) TRƯỚC, rồi mới xếp theo Tổng.** Hoà Tổng → bản diff nhỏ/robust hơn thắng (ít rủi ro over-fit).
- Đối chiếu code bắt buộc: mọi trích test file / số dòng / tên hàm phải kiểm được tại `/Users/uspro/Desktop/namnson/hex_agent`; không đối chiếu được = claim bịa = tiêu chí 1 về 0.

## §3 Ba–năm hướng thử (mỗi hướng nhắm ĐÚNG MỘT tiêu chí đang mất điểm)

Baseline (bản đang có) = **rớt gate (tiêu chí 1 = 0), Tổng 12/16**. Các hướng nhắm tiêu chí KHÁC nhau.

### Hướng A — Ép "đếm-lại-số cho khớp bảng" (nhắm tiêu chí 1, lỗi con-số)
**Giả thuyết:** thêm một bước bắt-buộc đếm PASS/PENDING/FAIL TỪ BẢNG rồi mới điền khối lãnh đạo/cổng/bàn giao/json sẽ chặn lỗi con số đảo ngược.
**Diff (thêm vào cuối "## Tự soi trước khi chốt"):**
```
- **Đếm-lại-số (bắt buộc, làm CUỐI cùng trước khi chốt).** Con số ở khối lãnh đạo · cổng ·
  bàn giao · _index.json PHẢI đếm TỪ bảng Mapping, không viết tay:
  tổng AC = số dòng data trong bảng; PASS/PENDING/FAIL = đếm đúng dấu trong cột Result.
  Tổng = PASS+PENDING+FAIL. Bốn khối phải TRÙNG con số. Lệch một chỗ = artifact hỏng,
  sửa trước khi xuất. (Đây là kiểu lỗi nguy hiểm nhất: CTO cho lên production dựa số này.)
```
**Rủi ro:** agent vẫn có thể đếm ẩu; luật ép quy trình nhưng không tự chạy — nếu agent bỏ bước thì vô hiệu (nhưng làm rõ trách nhiệm, dễ bắt khi grade).

### Hướng B — Luật "trích code phải đối chiếu, không thì gắn nhãn" (nhắm tiêu chí 1, lỗi path bịa)
**Giả thuyết:** cấm điền test-file/số-dòng nếu chưa `ls`/đối chiếu code gốc, và cho phép để trống + gắn nhãn thay vì bịa path, sẽ chặn ~27 path harness không tồn tại.
**Diff (thêm 1 bullet vào "## Luật cứng"):**
```
- **Trích code/test phải ĐỐI CHIẾU được, không thì gắn nhãn — cấm bịa path.** Mọi tên test
  file · số dòng · tên hàm trong bảng phải kiểm được ở code gốc (ls/đọc thật) trước khi ghi.
  Chưa đối chiếu được → KHÔNG viết path đoán; để trống hoặc ghi "[test-ref chưa đối chiếu]".
  Nếu thêm cột trỏ harness/test file, mỗi ô phải là path THẬT (đúng cấu trúc thư mục gốc:
  kiểm phẳng/lồng bằng ls trước) — một path không tồn tại làm mất giá cả tờ bằng chứng.
```
**Rủi ro:** làm chậm/khắt khe hơn; agent lười có thể bỏ cột harness luôn (chấp nhận được — thà thiếu cột còn hơn cột bịa), nhưng đó là 5-mắt-chuẩn nên không mất điểm mapping.

### Hướng C — Danh sách CẤM cụ thể trong khối lãnh đạo (nhắm tiêu chí 4)
**Giả thuyết:** liệt kê rõ token bị cấm trong Góc nhìn lãnh đạo (mã story, mã invariant, mã ADR/SPIKE, tên test, số dòng) sẽ chặn jargon rò vào khối exec — "không jargon" chung chung đang bị lờ.
**Diff (sửa bullet "Hợp đồng đọc-được 3 tầng" trong "## Luật cứng", thêm câu cấm-cụ-thể):**
```
  (1) MỞ bằng Góc nhìn lãnh đạo … ngôn ngữ nghiệp vụ. CẤM trong khối này: mã story
  (S3.5.1), mã invariant/DoD (M1/D2/D4), mã ADR/SPIKE (ADR-006/SPIKE-1), tên/số test file,
  số dòng code, tên module kỹ thuật. Chỉ được: tỷ lệ pass · trạng thái 2 chữ ký · 1 dòng "còn hở gì"
  bằng lời nghiệp vụ. Jargon đẩy hết xuống khối "CHI TIẾT KỸ THUẬT".
```
**Rủi ro:** cấm quá tay khiến khối lãnh đạo mất neo tới rủi ro cụ thể (mất "3 lời hứa M1/M2/M3"); phải cho phép DIỄN GIẢI lời-hứa bằng lời (vd "không báo-xong khống") thay vì mã.

### Hướng D — Ép gắn nhãn PASS-live vs PENDING-harness rõ ràng (nhắm tiêu chí 1, sub-lỗi lẫn "đã chạy" vs "định nghĩa")
**Giả thuyết:** bản chạy đã làm khá tốt (PENDING minh bạch) nhưng dấu "D1 PASS" tựa file bịa; thêm luật buộc mỗi PASS phải trỏ test-đã-chạy-thật (không phải harness-gốc-kế-thừa) sẽ tách sạch PASS thật khỏi khung.
**Diff (thêm vào bullet Release Decision/Result trong "### 2) Bảng MAPPING"):**
```
- **Result chỉ được PASS khi test THẬT đã chạy xanh trên code đang nghiệm** (không phải
  "harness gốc đã có test cùng tên"). Kế thừa khung → PENDING (harness-defined), ghi nhãn
  "chờ chạy". Một dấu PASS tựa test chưa-đối-chiếu-được = tiêu chí 1 rớt gate.
```
**Rủi ro:** trùng vùng với B (cả hai chạm tiêu chí 1) — nếu chạy cả B lẫn D dễ phí một agent; chọn 1 trong 2 nếu muốn giữ mỗi hướng một tiêu chí. Ưu tiên B (bắt lỗi path — lỗi nặng hơn); D để dự phòng.

**Chọn để chạy song song (mỗi tiêu chí một hướng, không trùng):** A (số) · B (path) · C (jargon). D là biến thể của tiêu chí 1 — chỉ thêm nếu muốn kiểm riêng lỗi PASS-tựa-harness; khi đó gộp A+B thành một agent "siết bằng chứng" để không hai agent cùng đụng tiêu chí 1.

## §4 Ưu tiên

**Để sau** (nghiêng "tune nhẹ, không gấp"). Lý do: gate rớt chủ yếu vì lỗi-của-lần-chạy — con số đảo ngược là agent không đếm lại bảng mình vừa viết, không phải SKILL thiếu luật cốt lõi; SKILL.md GĐ12 vốn đã chặt (mapping 5 mắt, 2 chữ ký, PENDING minh bạch, Đủ-là-đủ, ranh giới vai đều 2 điểm). Đáng làm một vòng tune NHẸ chỉ để thêm 2 luật rẻ-mà-chặn-được-lỗi-nguy-hiểm (Hướng A "đếm-lại-số" + Hướng B "cấm bịa path"), vì đây đúng là kiểu lỗi làm CTO cho lên production dựa số sai — nhưng không phải viết lại skill.

## §5 Nhắc luật thí nghiệm (bắt buộc khi chạy)

- **Chấm mù:** agent chấm chỉ thấy {project, đầu-vào GĐ9/10/11, output.md}, KHÔNG thấy variant theo hướng nào.
- **Baseline trước:** chấm lại chính `rebuild-hex-agent/pipeline/12-uat.md` bằng rubric làm mốc (đã có: rớt gate, 12/16) TRƯỚC khi so variant.
- **Một biến duy nhất:** mọi variant cùng fixture §1, chỉ khác đúng đoạn diff của nó; agent phải TUÂN proposed-SKILL của chính nó khi sinh output.
- **Confirm bản thắng bằng agent MỚI + fixture thứ hai:** chạy lại proposed-SKILL thắng bằng agent mới trên (a) đúng fixture hex-agent, và (b) một project GĐ12 khác (vd một artifact uat của dự án khác trong `experiments/` hoặc dựng nhanh một slice nhỏ) — chống over-fit vào đúng bộ số/path của hex-agent. Chỉ hơn baseline ở cả hai mới đáng merge.
