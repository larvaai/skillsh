# TUNE — skill `skeleton` (dựa trên chấm 08-skeleton.grade.md)

Nguồn: grade `experiments/hex-rebuild-review/grades/08-skeleton.grade.md` · rubric `rubrics/08-skeleton.rubric.md` · SKILL `/.claude/skills/skeleton/SKILL.md` · artifact `rebuild-hex-agent/pipeline/08-skeleton.md`.

## §0 Chẩn đoán (≤6 câu)

Artifact được **13/14, GATE ĐẠT** (3 xương sống 3·4·5 đều = 2); chỉ mất 1 điểm ở **Tiêu chí 1 — Mở đầu lãnh đạo** (=1) vì khối "Góc nhìn lãnh đạo" nhồi file:line + tên hàm (`supervisor/loop.py:_drive`, `delegation/manager.py:63`, `judge_acceptance`) và jargon stack (Python 3.11 · LangGraph · SQLite · SPIKE-1). Phần lớn là **lỗi-của-lần-chạy** (agent muốn khoe độ chặt nên dán anchor vào khối lãnh đạo), NHƯNG có **một lỗ SKILL thật, tunable**: luật khối lãnh đạo chỉ cấm "MỞ bằng tên framework/log tool" (line 24, 100) — nó KHÔNG cấm anchor `file:line`/tên-hàm/tên-stack **NẰM TRONG** khối, nên agent tự cho phép. Rubric mức-2 lại đòi "đọc RIÊNG khối này CTO ngoài hiểu, KHÔNG jargon" (không chỉ khúc mở đầu). Đây là **luật mơ hồ** (phạm vi "không jargon" bị thu hẹp về "mở đầu"), không phải luật mâu thuẫn hay thiếu hẳn — vậy đáng tune một nhát nhỏ để bịt kẽ, phần còn lại là kỷ luật lần chạy.

## §1 Fixture đề xuất (cố định cả thí nghiệm)

- **project**: `hex_agent` rebuild — thư mục `rebuild-hex-agent/`, code gốc đối chiếu tại `/Users/uspro/Desktop/namnson/hex_agent`.
- **Đầu vào GĐ trước** (nạp nguyên cho mọi variant, không đổi): `rebuild-hex-agent/pipeline/07-stack.md` (Tech Decision), `06-shape.md` (Architecture Brief), `05-idea-domain.md` (Domain), `00-understanding/REBUILD-BRIEF.md` + `ATLAS.md` + `evidence-A/B/C`.
- **Slice cố định**: `finish-by-evidence-tối-thiểu` (task 2 bước → plan → order deps → delegate 1 worker scope⊆parent → judge-by-evidence → FINISHED/BLOCKED, +resume SQLite dính SPIKE-1). Ép cùng slice để chỉ 1 biến (bản sửa SKILL) thay đổi — KHÔNG cho variant tự chọn slice khác.
- **mode/level**: chế độ tự-quyết (cổng CTO do người viết đóng vai, không hỏi user), độ dài ~1 trang, level người đọc = CTO/business ngoài + dev (như artifact gốc).
- **Ghi**: `experiments/runs/<ts>/fixture.txt` chép 5 dòng trên; mọi variant đọc đúng file này.

## §2 Thước

- Rubric: `/Users/uspro/Desktop/skillsh/experiments/hex-rebuild-review/rubrics/08-skeleton.rubric.md` (7 tiêu chí × 0/1/2, /14).
- Luật xếp: **loại hết bản rớt gate (tiêu chí 3/4/5 = 0) TRƯỚC, rồi mới xếp theo Tổng**; hoà Tổng → bản diff NHỎ/robust hơn thắng (ít rủi ro over-fit).
- Baseline = artifact hiện tại `08-skeleton.md` đã chấm 13/14 (Tiêu chí 1 = 1). Mọi variant phải kéo Tiêu chí 1 lên 2 mà KHÔNG làm tụt tiêu chí nào khác (đặc biệt không được rớt gate) mới đáng.
- Chấm mù: agent chấm chỉ thấy {slice, level, mode, output}, không thấy variant nào theo hướng nào.

## §3 Hướng thử A/B/C/D (mỗi hướng nhắm tiêu chí KHÁC — ở đây gốc chỉ mất 1 điểm nên A/B/C cùng đánh Tiêu chí 1 bằng 3 cơ chế luật khác nhau; D là đối chứng phòng thủ gate)

### Hướng A — Luật cấm-anchor-trong-khối-lãnh-đạo (nhắm Tiêu chí 1)
**Giả thuyết:** Nếu luật cứng cấm THẲNG mọi `file:line`/tên-hàm/tên-stack nằm trong khối lãnh đạo (không chỉ "mở bằng"), agent sẽ đẩy anchor xuống phần kỹ thuật → Tiêu chí 1 lên 2.
**Diff (sửa Luật cứng, dòng 24 — thêm 1 câu vào cuối gạch đầu dòng "Hợp đồng đọc-được 3 tầng"):**
> … 1 trang, scan 2–3 phút. Không mở bằng tên framework/log tool. **Thêm: TRONG cả khối lãnh đạo cấm mọi anchor `file:line`, tên hàm, tên file, tên framework/DB, mã spike (vd `SPIKE-1`) — nếu cần nhắc "cái lõi đã chạy", nói bằng chức năng nghiệp vụ ("vòng lặp giao-việc", "cửa nghiệm-thu-bằng-bằng-chứng"), đẩy mọi anchor code xuống phần Chi tiết kỹ thuật. Kiểm: đọc riêng khối lãnh đạo mà thấy 1 chuỗi `x/y` kiểu file:line hoặc 1 tên hàm → chưa đạt.**
**Rủi ro:** cấm cứng tên-stack có thể làm khối lãnh đạo mất thông tin "đang tái dựng cái đã chạy" → phải diễn đạt lại bằng nghiệp vụ, nếu agent lười sẽ nói mơ hồ và tụt sang mức-1 kiểu khác.

### Hướng B — Ví dụ mẫu khối lãnh đạo "không anchor" (nhắm Tiêu chí 1)
**Giả thuyết:** Ví dụ hiện tại (dòng 165-170) đã sạch anchor nhưng ngắn/chung; thêm MỘT ví dụ khối lãnh đạo cho case brownfield-rebuild (có tiền lệ gốc) diễn đạt "cái lõi đã chạy" bằng nghiệp vụ sẽ cho agent mẫu calibrate, tự bỏ anchor mà không cần thêm luật cấm.
**Diff (thêm khối ngay dưới template, sau dòng 100 "Góc nhìn lãnh đạo (mở đầu report, bắt buộc)"):**
> **Ví dụ khối lãnh đạo cho rebuild có tiền lệ gốc (diễn đạt nghiệp vụ, KHÔNG anchor):**
> ```
> Bằng chứng : cái lõi (giao-việc → nghiệm-thu-bằng-bằng-chứng → dừng có phanh) ĐÃ chạy thật ở bản đang vận hành;
>              bản làm-lại chưa deploy — link staging ⏳ CHƯA CÓ.
> Trạng thái : 0/9 ô validate tick thật trên bản làm-lại; đường đi đã có tiền lệ chạy → rủi ro dựng THẤP.
>              Sẵn sàng đổ người vào build full: CHƯA (chưa có staging chạy thật).
> Giả định đã đổi: ẩn số kỹ thuật còn 1 cái (khôi-phục-giữa-chừng đúng-một-lần) — đã đóng khung để đo ngay trong slice.
> ```
> (Chú ý: không một tên file/hàm/framework nào trong khối — mọi anchor để phần kỹ thuật.)
**Rủi ro:** ví dụ mới có thể bị agent COPY nguyên văn thay vì viết cho case của mình (over-fit vào chính fixture rebuild), khó tổng quát sang case greenfield.

### Hướng C — Bước tự-soi thêm 1 câu "quét anchor khối lãnh đạo" (nhắm Tiêu chí 1)
**Giả thuyết:** Lỗi là kỷ luật cuối; thêm một câu tự-soi BẮT quét khối lãnh đạo tìm anchor trước khi chốt sẽ chặn rò mà không đụng luật cứng (diff nhỏ nhất, robust nhất).
**Diff (sửa mục "Tự soi trước khi chốt", câu tự-soi đầu — dòng 105 — thêm mệnh đề quét):**
> - Lãnh đạo (CTO/business ngoài) đọc RIÊNG khối "Góc nhìn lãnh đạo" có biết kiến trúc đã chứng minh hay chưa … (link staging + trạng thái checklist + giả định đã đổi, không jargon)? **Quét lại khối: nếu còn BẤT KỲ `file:line`, tên hàm, tên file, tên framework/DB, hay mã spike → CHƯA đạt, đẩy chúng xuống phần kỹ thuật rồi soi lại.**
**Rủi ro:** tự-soi là lời-nhắc-mềm, agent vẫn có thể bỏ qua khi "chạy ẩu" — hiệu lực yếu hơn luật cứng (A), có thể không kéo nổi điểm nếu nguyên nhân thật là agent không đọc kỹ mục tự-soi.

### Hướng D — Đối chứng phòng-thủ-gate: tách "bằng-chứng-gốc" khỏi "tick" mạnh hơn (nhắm Tiêu chí 4, giữ gate)
**Giả thuyết (phòng thủ, không nhắm điểm-mất):** Sửa để kéo Tiêu chí 1 (A/B/C) không được vô tình làm mờ luật "gốc-đã-chạy ≠ tick rebuild" khiến Tiêu chí 4 tụt; hướng này thử SIẾT rõ ranh giới đó để chắc gate không lung lay khi rút anchor khỏi khối lãnh đạo.
**Diff (thêm 1 câu vào Luật cứng "Chạy thật, không mockup", dòng 25):**
> … ô nào chưa chạy thật thì để trống + ghi thẳng là rủi ro còn lại. **Với rebuild/brownfield: bằng chứng chạy ở bản GỐC (anchor `file:line`) CHỈ là tiền-lệ-đường-đi để ước lượng rủi ro dựng, TUYỆT ĐỐI không được đếm là ô tick của bản rebuild — trình riêng thành cột "G (gốc)" tách khỏi cột "R (rebuild)", tick chỉ tính trên R.**
**Rủi ro:** hướng này KHÔNG nhắm điểm đang mất (Tiêu chí 1) nên có thể không đổi tổng; chỉ đáng chạy như bản đối chứng để phát hiện regression gate — nếu A/B/C không làm tụt gate thì D là dư.

> Ghi chú xếp hướng: A/B/C cùng đánh Tiêu chí 1 vì đó là điểm mất DUY NHẤT (không có tiêu chí khác đang <2 để chia hướng). Ba cơ chế khác nhau (luật cấm cứng · ví dụ mẫu · tự-soi) để xem cách nào kéo điểm rẻ và ít over-fit nhất. D là đối chứng gate. Nếu Son chỉ muốn 3 agent: bỏ D.

## §4 Ưu tiên

**"để sau" (nghiêng về "không đáng tune gấp").** Lý do: grade đã 13/14 và gate đạt; điểm mất duy nhất là 1 nấc ở Tiêu chí 1, mà nguyên nhân **phần lớn thuộc lần-chạy** (agent tự dán anchor vào khối lãnh đạo dù luật đã bảo "không mở bằng framework"). Chỉ có một kẽ hở SKILL nhỏ (phạm vi "không jargon" chưa phủ toàn khối) đáng bịt bằng một câu (Hướng A hoặc C) — làm gộp khi tune vòng khác, không cần mở một thí nghiệm 4-agent riêng cho 1 điểm.

## §5 Nhắc luật thí nghiệm

- **Chấm mù**: agent chấm chỉ nhận {slice, level, mode, output.txt}, không biết variant theo hướng nào; đặt tên A/B/C/D trung tính.
- **Baseline trước**: chấm lại artifact hiện tại `08-skeleton.md` bằng rubric để chốt mốc 13/14 (Tiêu chí 1 = 1) trong cùng lượt, mọi variant phải hơn mốc này.
- **Một biến duy nhất**: mọi variant cùng fixture §1 (cùng slice, cùng đầu vào GĐ7/6/5), chỉ khác bản sửa SKILL; variant KHÔNG được đổi slice.
- **Confirm bản thắng bằng agent MỚI**: chạy `proposed-SKILL.md` của bản thắng bằng agent mới trên (a) đúng fixture rebuild, và (b) **fixture thứ hai khác** — vd một slice greenfield (không có tiền lệ gốc, phải viết khối lãnh đạo từ 0) để chắc bản sửa không over-fit vào riêng case brownfield-anchor. Vẫn hơn baseline ở CẢ HAI → mới merge.
- **Không đụng SKILL thật khi đang thử**: mỗi bản sửa nằm trong `experiments/runs/<ts>/<variant>/proposed-SKILL.md`; `skeleton/SKILL.md` chỉ đổi sau khi có bản thắng qua confirm và Son chốt.
