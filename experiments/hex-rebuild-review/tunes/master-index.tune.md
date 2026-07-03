# TUNE — master-index (quy ước gói) — dựa trên chấm artifact `rebuild-hex-agent/README.md`

> Vòng tune cho luật "master-index / cửa-vào gói". KHÔNG có SKILL.md riêng cho master-index — luật này SỐNG trong skill **`traceability`** (nó đã sở hữu vai "tháp kiểm soát đọc-được", hợp đồng 3-tầng, và bảng-trạng-thái-đọc-một-phát; xem `traceability/SKILL.md:8,21`). Mọi diff dưới đây sửa vào `.claude/skills/traceability/SKILL.md`.
> Bám quy trình `tune/SKILL.md`: fixture cố định · MỘT biến duy nhất (bản sửa SKILL) · chấm mù · baseline trước · confirm bằng agent mới chống over-fit.
> Nguồn chấm: `experiments/hex-rebuild-review/grades/master-index.grade.md` (RỚT GATE, 10/14).

---

## §0 Chẩn đoán (≤6 câu)

README rớt gate DUY NHẤT ở **tiêu chí 2 (KHỚP BẢNG–ARTIFACT — xương sống) = 0**: con số cửa-vào "26/28 PASS · 2 PENDING" (README:37, 68) khớp *headline tự-phong* của `12-uat.md:11` nhưng MÂU THUẪN bảng mapping "Xương của artifact" của chính file đó (đếm cột Result: **12 PASS / 23 PENDING / 35 dòng**; 4/6 nhóm AC lõi PENDING toàn bộ). Cùng con số đó kéo **tiêu chí 3 (TRUNG THỰC TRẠNG THÁI)** xuống 1 (23 treo bị rút thành "2" ở tầng đọc-nhanh → người đọc 90 giây lạc quan hơn một bậc); và **tiêu chí 1 (LINK & ĐỘ PHỦ)** còn 1 vì 2 file mồ-côi (`explain/EXPLAIN.grade.md`, `pipeline/ideas/hex-agent-rebuild.md`) không nằm trong cây index. Bốn tiêu chí còn lại đều 2/2 — README VỮNG về hình hợp đồng cửa-vào (3 tầng, dẫn-theo-vai, bảng-scan, trỏ-không-làm-thay), gãy đúng chỗ con-số-rollup.
Phân lỗi SKILL vs lần-chạy: **gốc mâu thuẫn là ở artifact upstream 12-uat.md** (headline tự cãi breakdown) — đó là lỗi của lần chạy `/uat`, KHÔNG tune được ở đây (đã có `uat.tune.md` lo). NHƯNG master-index có phần lỗi RIÊNG thuộc SKILL: README lấy số bằng cách **chép headline của summary** thay vì rollup từ breakdown, mà `traceability/SKILL.md` HIỆN thiếu luật buộc "con số cửa-vào phải rollup từ bảng chi tiết của artifact, không tin headline" và thiếu luật "tầng đọc-nhanh không được nói-nhẹ số-treo". Kết: một phần lỗi thuộc lần-chạy-uat (không tune ở file này), phần còn lại là lỗi-của-SKILL-traceability (luật mơ hồ + thiếu luật) → **TUNE ĐƯỢC phần đó.**

## §1 Fixture đề xuất (cố định cả thí nghiệm)

- **project**: `rebuild-hex-agent` — gói đầy đủ tại `/Users/uspro/Desktop/skillsh/rebuild-hex-agent/`.
- **task/tham số**: sinh lại **Master Index / README cửa-vào** cho cả gói (đúng việc lần chạy đã bị chấm) — tổng hợp trạng thái + cây link + bảng-trạng-thái + dẫn-theo-vai. KHÔNG dùng đường "đầu vào ngoài state"; đọc trực tiếp cây `rebuild-hex-agent/pipeline/*.md|*.json` + `00-understanding/` + `review/` + `frame/` + `explain/`.
- **Bẫy cố ý trong fixture (GIỮ NGUYÊN, đừng sửa artifact nguồn)**: `12-uat.md:11` để headline "28/28 có test, 26 PASS · 2 PENDING" tự-mâu-thuẫn với bảng mapping §1 (12 PASS / 23 PENDING); `uat.json` `ac_loi_6_nhom` có 4/6 nhóm PENDING toàn bộ; hai file mồ-côi `explain/EXPLAIN.grade.md` (11.6KB) + `pipeline/ideas/hex-agent-rebuild.md` tồn tại thật trên đĩa. Chính các bẫy này phân biệt các variant — variant tốt phải rollup ra 12/23 (không chép 26/2) và quét bắt được 2 mồ-côi.
- **Lặp lại được**: mọi variant đọc đúng cây trên, ghi output ra `experiments/runs/<ts>/<variant>/output.md` (đóng vai bản README ĐÃ SỬA theo `proposed-SKILL.md` của chính nó); không ai đụng/sửa artifact nguồn.

## §2 Thước

- Dùng `experiments/hex-rebuild-review/rubrics/master-index.rubric.md` (7 tiêu chí 0/1/2, tối đa 14; xương sống = 1, 2, 3).
- Luật xếp hạng: **loại hết bản rớt gate trước** (bất kỳ tiêu chí 1/2/3 = 0), **rồi mới xếp theo tổng /14**. Hoà tổng → bản diff NHỎ/ROBUST hơn thắng (ít rủi ro over-fit vào đúng fixture này).
- Đối chiếu ngoài: claim code đối chiếu `/Users/uspro/Desktop/namnson/hex_agent`; claim số đối chiếu file `pipeline/*.md|*.json` nguồn (mở đúng bảng mapping, đếm cột Result — không đọc headline).

## §3 Các hướng thử (mỗi hướng nhắm ĐÚNG MỘT tiêu chí đang mất điểm)

Ba tiêu chí mất điểm: **#2 Khớp bảng–artifact (gate, kéo rớt)** · **#3 Trung thực trạng thái** · **#1 Link & độ phủ**. Các hướng nhắm KHÁC nhau. A/B dồn vào #2 (gate — nặng nhất) qua hai cơ chế khác nhau; C nhắm #3; D nhắm #1. (Chú ý phân vai với `traceability.tune.md`: hướng A ở kia là "đếm-lại-ở-nguồn cho _traceability report"; hướng A ở ĐÂY hẹp hơn — luật riêng cho **rollup con-số vào cửa-vào README**, khác artifact, khác tiêu chí rubric.)

### Hướng A — Luật "rollup từ breakdown, KHÔNG chép headline" (nhắm tiêu chí 2)

**Giả thuyết:** Buộc mọi con-số-cửa-vào phải rollup từ BẢNG CHI TIẾT của artifact được link (không tin dòng headline/tóm-tắt của artifact đó), và cờ mâu thuẫn khi headline cãi breakdown, sẽ chặn đúng bug "26/28 chép từ headline tự-cãi".

**Diff (thêm vào mục "## Luật cứng" của `traceability/SKILL.md`, sau bullet "Không bịa"):**
```
- **Số cửa-vào rollup từ BREAKDOWN, không chép HEADLINE.** Mọi con số tổng đưa lên trang cửa-vào
  (x/y PASS, n PENDING, k cổng GO) phải được đếm/rollup từ BẢNG CHI TIẾT của artifact được link
  (vd cột Result của bảng mapping `12-uat.md`), KHÔNG lấy từ dòng headline/"một câu" tự-phong của
  chính artifact đó. Nếu headline của artifact cãi breakdown của nó (vd headline "26 PASS" nhưng
  bảng đếm 12 PASS) → lấy số BREAKDOWN + cờ một dòng "headline nguồn lệch bảng, đã dùng số bảng".
```

**Rủi ro:** Rollup thủ công có thể lệch nếu bảng nguồn mập mờ (dòng gộp/điều kiện); cần dặn "neo file:mục đã đếm" để người chấm truy lại được, kẻo tự tạo một con số mới không nguồn (lại rơi vào chính tiêu chí 2).

### Hướng B — Ví dụ mẫu một dòng bảng-trạng-thái "số-rollup-khớp-neo" (nhắm tiêu chí 2)

**Giả thuyết:** Cho một ví dụ MẪU cách viết ô số ở bảng-trạng-thái cửa-vào (số đã rollup + neo đã kiểm), calibrate bằng example (như hướng "ví dụ mẫu" của `tune explain`), sẽ khiến agent bắt chước format "rollup + neo" thay vì chép headline.

**Diff (thêm vào "## Ví dụ Case Management (rút gọn)" của `traceability/SKILL.md`, một dòng minh hoạ ô-số-cửa-vào):**
```
Ví dụ ô số cửa-vào ĐÚNG (rollup từ bảng chi tiết, không chép headline artifact):
  "GĐ12 UAT: 12 PASS / 23 PENDING  [đếm cột Result bảng mapping 12-uat.md §1]"
  — KHÔNG viết "26/28 PASS · 2 PENDING": đó là headline một-câu của 12-uat.md, tự cãi bảng của chính nó.
```

**Rủi ro:** Ví dụ lấy đúng con số fixture này → mùi over-fit; agent có thể học "case này = 12/23" thay vì học nguyên tắc rollup-từ-bảng. Bước 5 confirm trên fixture thứ hai là bắt buộc để lộ over-fit. (Cùng cơ chế calibrate nhưng KHÁC vị trí/nội dung với A — A là luật-cứng, B là example; giữ tách để đo cơ chế nào ăn điểm #2 chắc hơn.)

### Hướng C — Luật "tầng đọc-nhanh không nói-nhẹ số-treo" (nhắm tiêu chí 3)

**Giả thuyết:** Buộc số-treo (PENDING/tick-0/spike) hiện ở tầng đọc-nhanh phải là con số ĐÃ ROLLUP đầy đủ (không rút gọn nhỏ hơn breakdown), sẽ chặn bug "23 treo bị nói thành 2" ở tầng lãnh đạo.

**Diff (bổ sung vào bullet "Hợp đồng đọc-được-3-tầng" trong "## Luật cứng" của `traceability/SKILL.md`, thêm câu cuối):**
```
  Số-treo (PENDING / tick-0/N / spike / cổng-có-điều-kiện) nêu ở tầng đọc-nhanh phải là con số ĐÃ
  ROLLUP đầy đủ từ breakdown — KHÔNG được rút xuống thấp hơn số thật (vd không viết "2 PENDING" khi
  bảng có 23). Nói-nhẹ số-treo ở cửa = người đọc 90 giây lạc quan hơn một bậc → cấm.
```

**Rủi ro:** Chỉ chữa #3, KHÔNG gỡ gate (#2). Nếu chạy một mình, README vẫn rớt gate — C phải ghép cùng A/B mới lên điểm thật; giữ C riêng để đo phần đóng góp của nó vào #3.

### Hướng D — Luật "quét mồ-côi: mọi artifact người-đọc phải có mặt trong cây index" (nhắm tiêu chí 1)

**Giả thuyết:** Buộc bước quét toàn cây gói (`find` mọi `*.md` người-đọc) và đối chiếu với cây link, sẽ bắt được file mồ-côi (`explain/EXPLAIN.grade.md`, `pipeline/ideas/hex-agent-rebuild.md`) trước khi chốt cửa-vào.

**Diff (thêm 1 mục vào block "### Tự soi trước khi chốt (bắt buộc)" của `traceability/SKILL.md`):**
```
5. Đã quét TOÀN cây gói (mọi `*.md` người-đọc) và đối chiếu với cây link chưa? Mọi artifact người-đọc
   có mặt trong index (không mồ-côi) chưa? File máy-đọc (JSON) được nhắc gộp + nói ai cần đọc chưa?
```

**Rủi ro:** Chỉ chữa #1 (nâng 1→2), KHÔNG gỡ gate; là hướng "nhẹ nhất". Quét thừa có thể kéo file dài nếu agent liệt kê cả file meta/grade không đáng trỏ riêng — dặn "mồ-côi grade/meta có thể nhắc-gộp thay vì trỏ riêng".

**Ghi chú ghép:** A (hoặc B) gỡ gate #2 + C nâng #3 + D nâng #1 là bộ có khả năng lên 13–14/14. Bước 6 cân nhắc merge A+C nếu cả hai qua confirm (cả hai cùng chạm con-số-treo, ghép nhau tự nhiên).

## §4 Ưu tiên

**TUNE NGAY** — nhưng ghép chung một vòng với `uat`. README rớt GATE (tiêu chí xương sống #2 = 0), loại lỗi nặng nhất theo rubric: CTO/PO quyết đi-tiếp dựa trên chính con số cửa-vào, sai ở cửa = cả gói bị tin nhầm gần-xanh trong khi 3 điểm-bán M1/M2/M3 đều PENDING. Phần tune-được (rollup-từ-breakdown + không-nói-nhẹ-treo) thuộc lỗi-của-SKILL-traceability, đòn bẩy hẹp và rẻ (một luật cứng gỡ gate). Lưu ý: gốc con-số-mâu-thuẫn nằm ở `12-uat.md` (lỗi lần chạy uat) — sửa luật master-index chặn việc CHÉP số cãi-nhau lên cửa, nhưng phải sửa song song nguồn ở `uat.tune.md` mới hết tận gốc.

## §5 Nhắc luật thí nghiệm (bắt buộc theo tune/SKILL.md)

- **Baseline trước:** chạy lại việc-sinh-Master-Index HIỆN TẠI (theo `traceability/SKILL.md` chưa sửa) trên fixture §1 → `runs/<ts>/baseline/output.md`, chấm bằng thước §2. Bản đã có (`rebuild-hex-agent/README.md`, 10/14 RỚT GATE) dùng làm mốc — mọi variant phải hơn mốc (tối thiểu: gỡ gate #2).
- **Một biến duy nhất:** mọi variant cùng fixture §1, chỉ khác bản sửa `traceability/SKILL.md`. Không ai đổi artifact nguồn hay fixture giữa chừng. Mỗi variant phải TUÂN `proposed-SKILL.md` của chính nó khi viết `output.md`, không viết theo bản gốc.
- **Chấm mù:** agent chấm chỉ thấy {project=rebuild-hex-agent, "sinh Master Index cửa-vào", output.md}, KHÔNG thấy variant theo hướng nào (đặt tên A/B/C/D trung tính).
- **Confirm agent mới + fixture thứ hai:** bản thắng chạy lại bằng agent MỚI trên (a) fixture §1 và (b) một gói pipeline thứ hai có state đầy đủ (hoặc chèn một bẫy headline-cãi-breakdown ở artifact KHÁC, vd review hoặc operate). Chỉ hơn ở fixture gốc → mùi over-fit (nhất là hướng B ví-dụ-mẫu), xem lại diff. Hơn ở cả hai → điểm đến từ SỬA, đáng merge vào `traceability/SKILL.md`.
