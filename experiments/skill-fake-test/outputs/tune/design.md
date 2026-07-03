# Thiết kế thí nghiệm `tune teen` (dry-run) — fixture `streak.ts`

Đây là bản THIẾT KẾ (chưa chạy 5 variant). Nó chỉ rõ, theo đúng
`.claude/skills/tune/SKILL.md`, thí nghiệm sẽ cố định gì, đo bằng gì, thử những
hướng nào, chấm mù ra sao, và confirm bản thắng thế nào — để khi bấm chạy thật
chỉ việc thực thi, không phải quyết thêm.

Skill cần tune: **teen** (`.claude/skills/teen/SKILL.md`).
Loại skill: đọc-hiểu (giống explain/trace/triage) — không sinh artifact pipeline.

---

## CẢNH BÁO CHẶN (đọc trước — quyết định độ tin của cả lượt)

`teen` **CHƯA CÓ `teen/rubric.md`**. Kiểm thực tế: chỉ 13 skill có
`rubric.md` (shape, explain, checkpoint, uat, backlog, skeleton, traceability,
operate, spar, delivery, stack, ship, modules) — teen KHÔNG nằm trong đó.

Tune Bước 0 và Luật cứng #2 ("Có thước trước khi chạy") nói: thước là
`grade teen` đọc `teen/rubric.md`. Không có rubric riêng thì `grade` vẫn chấm
được bằng **tiêu chí tạm suy từ `grade/meta-rubric.md`**, NHƯNG SKILL.md ghi rõ
"điểm sẽ kém ổn định giữa các lần; nên tạo `teen/rubric.md` trước để thí nghiệm
đáng tin".

→ Hệ quả cho thiết kế này: mục **"Thước"** bên dưới có HAI đường.
- **Đường chuẩn (khuyến nghị):** làm một lượt-riêng tạo `teen/rubric.md` TRƯỚC,
  rồi mới chạy tune. Luật cứng #? của tune cấm sửa rubric giữa lượt, nên việc tạo
  rubric phải xong TRƯỚC baseline — không được chen vào giữa.
- **Đường tạm (nếu chạy ngay):** dùng "rubric tạm teen" mà thiết kế này chốt sẵn
  ở §Thước, đóng băng nó trong `fixture.txt` để mọi variant + baseline bị chấm
  bằng ĐÚNG một thước. Chấp nhận điểm kém ổn định, ghi ⚠️ ở mọi grade.txt.

Thiết kế dưới đây chạy được theo đường tạm, và nêu rõ đường chuẩn tốt hơn.

---

## Bước 0 — Chốt mục tiêu và fixture

### Mục tiêu tune
Làm `teen` giải thích `streak.ts` "tốt hơn" = bám sát hơn hợp đồng teen:
người-không-biết-code đọc xong HIỂU đoạn này giải quyết vấn đề gì và giải quyết
thế nào, mà KHÔNG bị (a) tên kỹ thuật lọt vào, (b) analogy/ví dụ ngoài project,
(c) đọc-từng-dòng thay vì nêu-vấn-đề-trước.

### Fixture (CỐ ĐỊNH cả thí nghiệm — một biến duy nhất)
Ba mảnh, đóng băng trong `experiments/runs/<ts>/fixture.txt`:

1. **project / đoạn code:** đúng file
   `experiments/skill-fake-test/fixture/codebase/mediremind/src/adherence/streak.ts`
   (19 dòng, hàm `currentStreak` — đếm số ngày liên tiếp gần nhất mà mọi liều
   trong ngày đều "taken"). Toàn văn được CHÉP vào fixture.txt để mọi agent đọc
   đúng một nguồn, không ai tự mở file khác.
2. **phần muốn hiểu:** cả hàm `currentStreak` (đủ ngắn, không cần cắt nhỏ).
3. **mức người đọc (mode ngầm của teen):** teen chỉ có MỘT chế độ — "người không
   biết code". Không có tham số level như explain. Cố định: *người dùng
   mediremind, biết ứng dụng nhắc uống thuốc là gì, KHÔNG biết lập trình.* Ghi
   thẳng câu này vào fixture để mọi variant cùng nhắm một đối tượng.

### Ngữ cảnh project cho fixture (để chấm tiêu chí "không bịa" + "không analogy")
teen cấm analogy ngoài project và buộc giải thích "bằng chính những gì project
đang làm". Nên fixture kèm 2 dòng ngữ cảnh THẬT rút từ chính file:
- `DoseEvent` = một lần theo lịch phải uống một liều; có `scheduledTime` và
  `status` ∈ {taken, skipped, (khác)}.
- mediremind = ứng dụng theo dõi tuân thủ uống thuốc (adherence). "streak" =
  chuỗi ngày giữ được kỷ luật uống đủ.
Không thêm gì ngoài file — để agent nào bịa API/hành vi ngoài 19 dòng này thì
rớt tiêu chí Bám-nguồn khi chấm.

### Thao tác tạo lượt
```
mkdir -p experiments/runs/<ts>/
# ghi fixture.txt gồm: toàn văn streak.ts + phần-muốn-hiểu + đối-tượng-đọc
#   + 2 dòng ngữ cảnh project + (đường tạm) toàn văn "rubric tạm teen" §Thước.
```
Mọi variant đọc đúng file này. KHÔNG ai đổi fixture giữa chừng (Luật cứng #1).
Ranh giới state (Bước 7 tune): KHÔNG ghi `state/current.json`, chỉ ĐỌC nếu cần.

---

## Thước — `grade teen` (định nghĩa rõ vì teen thiếu rubric)

Vì không có `teen/rubric.md`, thiết kế này chốt sẵn **"rubric tạm teen"** =
5 trục của `meta-rubric.md` đặc tả theo đúng 5 Quy-tắc-cứng + 6 Bước của
`teen/SKILL.md`. Đóng băng nguyên văn vào `fixture.txt`; mọi bản (baseline + A–E)
chấm bằng đúng thước này (Luật cứng #2: cùng lượt = cùng rubric).

Thang 0/1/2 mỗi tiêu chí. Tổng /12. Gate = tiêu chí 1, 2, 3.

```
1 VẤN-ĐỀ-TRƯỚC (A1, gate) — có nêu "đoạn này giải quyết vấn đề gì" bằng MỘT câu
    đời thường TRƯỚC khi đi vào cách chạy; và cách-chạy kể theo vấn-đề→giải-pháp,
    KHÔNG phải đọc-từng-dòng.
    0 = đi thẳng vào "dòng này làm...", không có câu nêu vấn đề, hoặc nêu sai vấn đề.
    1 = có nêu vấn đề nhưng mờ / lẫn với cách chạy.
    2 = một câu vấn đề rõ, rồi mới giải-pháp, đúng thứ tự Feynman.

2 KHÔNG-TÊN-KỸ-THUẬT (A3, gate — gói Quy-tắc-cứng #1,#2) — lời giải KHÔNG chứa
    function/loop/variable/class/method/array/reduce/map/object/key/sort... Nếu
    buộc nhắc một tên: có giải thích nó là gì, chỉ nhắc một lần.
    0 = có ≥1 tên kỹ thuật dùng trần không giải thích (kể cả "mảng", "vòng lặp"
        nếu dùng như thuật ngữ).
    1 = sạch phần lớn, lọt 1 tên nhẹ nhưng có ngữ cảnh.
    2 = hoàn toàn bằng lời thường; tên kỹ thuật (nếu có) được gỡ nghĩa trước, một lần.

3 BÁM-NGUỒN-KHÔNG-BỊA (A2, gate) — mọi điều nói về hành vi đoạn code truy được
    về đúng 19 dòng streak.ts. Không gán hành vi không có (vd "gửi thông báo",
    "lưu DB") — file chỉ TÍNH một con số.
    0 = có claim bịa hành vi ngoài file.
    1 = đúng phần lớn, 1 chỗ suy đoán không gắn nhãn.
    2 = mọi claim khớp code; chỗ chưa chắc gắn nhãn "chưa chắc".

4 KHÔNG-ANALOGY-NGOÀI-PROJECT (A4 — Quy-tắc-cứng #5) — giải thích bằng chính
    việc mediremind đang làm, KHÔNG mượn "giống như người gác cổng/xếp hàng...".
    0 = có ≥1 analogy/tình huống thay thế ngoài context uống thuốc.
    1 = chủ yếu bám project, lỡ một hình ảnh ngoài lề.
    2 = hoàn toàn bằng ngữ cảnh thật (ngày, liều, uống đủ, chuỗi ngày).

5 CHẠY-BẰNG-LỜI + KẾT (A5 thu gọn — Bước 4,5,6) — có đi qua flow thật theo thứ
    tự xảy ra bằng lời (không ký hiệu code), có MỘT câu kết "vì sao quan trọng"
    theo context, và gợi ý bước tiếp hợp lý (không lấn sang explain/trace vô cớ).
    0 = không chạy bằng lời, HOẶC không có câu kết, HOẶC gợi ý sai skill/lấn vai.
    1 = có chạy + kết nhưng cụt hoặc gợi ý chung chung.
    2 = chạy bằng lời đúng thứ tự (mới→cũ theo cách hàm duyệt), kết một câu theo
        context, gợi ý đúng (vd "muốn biết nó được gọi ở đâu → trace/explain").
```

Đầu vào để chấm (khai đúng như grade cần): {đoạn code streak.ts · đối-tượng-đọc ·
output nguyên văn}. Đây cũng chính là fixture tune giữ cố định.

> Ghi chú độ tin: đây là rubric TẠM. Mọi `grade.txt` mở đầu bằng
> `⚠️ rubric tạm — nên tạo teen/rubric.md để điểm ổn định giữa các lần`.

---

## Bước 1 — Baseline (bản đối chứng)

Chạy `teen` HIỆN TẠI (bản `teen/SKILL.md` gốc, KHÔNG sửa gì) trên fixture.txt.
- Lưu `runs/<ts>/baseline/output.txt`.
- Chấm bằng rubric tạm teen (chấm mù, chỉ thấy {code, output}) →
  `runs/<ts>/baseline/grade.txt`.

Baseline là mốc: mọi variant phải HƠN cái này mới đáng theo. Dự đoán điểm yếu
baseline (để Bước 2 nhắm): teen SKILL.md mạnh về luật nhưng KHÔNG có 1 output
mẫu cho code TS kiểu reduce/sort; rủi ro cao nhất là tiêu chí 2
(lọt "mảng"/"gộp"/"sắp xếp") và tiêu chí 1 (trượt sang mô tả từng bước reduce).
Baseline thật sẽ xác nhận — KHÔNG được đoán thay số.

---

## Bước 2 — Chọn hướng thử (mỗi hướng nhắm MỘT tiêu chí yếu khác nhau)

Đọc `baseline/grade.txt`, mỗi hướng đánh vào một tiêu chí thấp/rớt gate. Một
biến duy nhất = mỗi variant chỉ khác baseline ở đúng một sửa đổi nhỏ trong
`proposed-SKILL.md`. 5 hướng (A–E):

| Var | Nhắm tiêu chí yếu | Sửa 1-biến trong proposed-SKILL.md | Giả thuyết |
|-----|-------------------|-------------------------------------|-----------|
| A | 2 KHÔNG-TÊN-KỸ-THUẬT | Thêm **danh sách cấm mở rộng cho TS/JS**: reduce, map, object, key, sort, array, index → kèm 1 câu "cách nói thường tương ứng" cho mỗi từ. | Baseline lọt tên vì luật chỉ liệt kê function/loop/variable chung; bơm từ-cấm sát ngôn ngữ sẽ chặn. |
| B | 1 VẤN-ĐỀ-TRƯỚC | Thêm **một output MẪU tốt** cho đúng dạng "đếm chuỗi ngày liên tiếp" (few-shot), mở bằng câu nêu vấn đề, để model calibrate thứ tự Feynman. | Có mẫu neo thứ tự vấn-đề→giải-pháp mạnh hơn mọi lời dặn trừu tượng. |
| C | 4 KHÔNG-ANALOGY | Siết Quy-tắc-cứng #5 thành **checklist tự-kiểm trước khi trả**: "gạch mọi câu có 'giống như / như thể / tưởng tượng'". | Cấm rõ + bước tự-rà chặn analogy tốt hơn một dòng luật hiện có. |
| D | 5 CHẠY-BẰNG-LỜI+KẾT | Thêm **khung 3 nhịp bắt buộc cho Bước 4**: "duyệt ngày mới nhất trước → gặp ngày hỏng thì dừng → đó là lý do con số ra vậy", buộc chạy đúng chiều hàm. | Baseline hay chạy bằng lời chung chung, bỏ chi tiết "duyệt ngược từ mới→cũ và dừng ở ngày hỏng" — chi tiết cốt lõi của streak. |
| E | 3 BÁM-NGUỒN | Thêm luật **"chỉ nói hành vi có trong đoạn; mọi điều ngoài đoạn phải gắn nhãn 'chưa chắc / ngoài đoạn này'"** + cấm gán "gửi/ lưu/ thông báo". | Chống bịa hành vi (file chỉ TÍNH một số, không I/O) — lỗi bịa là gate nặng nhất suite. |

Mỗi hướng = một variant, đặt tên A–E để chấm mù. Không trùng hướng (mỗi cái một
tiêu chí khác). Nếu baseline bất ngờ đã max một tiêu chí nào đó → bỏ variant tương
ứng, thay bằng hướng nhắm tiêu chí còn yếu (quyết sau khi có baseline thật).

---

## Bước 3 — Chạy song song

Giao mỗi variant A–E cho MỘT agent, **gửi cả 5 trong một lượt** (5 Task cùng một
tin nhắn) để chạy đồng thời. Mỗi agent nhận đúng:
- `teen/SKILL.md` gốc (bản thật hiện tại).
- "rubric tạm teen" (§Thước) + `grade/meta-rubric.md` — biết sẽ bị chấm bằng gì.
- fixture — đọc `runs/<ts>/fixture.txt` (không tự mở file khác).
- ĐÚNG MỘT hướng của nó (KHÔNG thấy hướng của 4 bản kia).

Mỗi agent ghi vào `runs/<ts>/<variant>/`:
1. `proposed-SKILL.md` — teen đã sửa theo hướng của nó, **sửa tối thiểu** đủ để
   thử (không viết lại toàn bộ SKILL.md).
2. `output.txt` — đóng vai teen ĐÃ SỬA đó chạy trên fixture. Phải tuân
   `proposed-SKILL.md` của CHÍNH NÓ, không phải bản gốc (nếu không, vô nghĩa).

Ranh giới cứng gửi kèm mỗi agent: KHÔNG đụng `teen/SKILL.md` thật (Luật cứng #3 —
bản thật chỉ đổi ở Bước 6 sau confirm), KHÔNG ghi state.

---

## Bước 4 — Chấm mù và xếp hạng

Với baseline + A–E: chạy `grade teen` chỉ với {fixture, output.txt}, người chấm
KHÔNG thấy variant đó theo hướng nào (che nhãn A–E khi đưa output cho agent
chấm) → `runs/<ts>/<variant>/grade.txt`. Cùng một rubric tạm cho tất cả.

Gom bảng so (6 cột = 5 tiêu chí + tổng):

```
Bản       1 2 3 4 5  Tổng  Gate        Bản này đổi gì
Baseline  . . . . .  ../10 ..          (gốc)
A         . . . . .  ../10 ..          từ-cấm TS/JS mở rộng
B         . . . . .  ../10 ..          thêm output mẫu few-shot
C         . . . . .  ../10 ..          checklist chặn analogy
D         . . . . .  ../10 ..          khung 3 nhịp chạy-bằng-lời
E         . . . . .  ../10 ..          luật bám-đoạn + cấm gán I/O
```
(Tổng /10 vì 5 tiêu chí × 2; sửa lại nếu rubric tạm đổi số tiêu chí.)

Xếp hạng đúng thứ tự tune: (1) loại HẾT bản rớt gate (tiêu chí 1/2/3 = 0) trước;
(2) còn lại xếp theo Tổng; (3) hoà Tổng → bản **diff nhỏ/robust hơn** thắng (sửa
ít, ít nguy cơ over-fit đúng fixture streak.ts này).

---

## Bước 5 — Confirm bản thắng (chống "agent giỏi ≠ sửa tốt")

Lấy `proposed-SKILL.md` của bản thắng, giao **agent MỚI** chạy trên:
- (a) đúng fixture gốc `streak.ts`, và
- (b) **fixture thứ hai cùng loại** — một đoạn TS khó khác trong mediremind
  (đề xuất: một hàm cũng dùng reduce/sort/duyệt-ngược nhưng khác domain, ví dụ
  một hàm tính "tỉ lệ tuân thủ 7 ngày" nếu có; nếu repo không có sẵn, chọn một
  đoạn ~15-25 dòng cùng phong cách trong `mediremind/src/`). Fixture-2 phải cố
  định trước khi chạy, ghi `runs/<ts>/confirm/fixture2.txt`.
Chấm lại cả hai bằng cùng rubric tạm teen.
- Vẫn HƠN baseline ở CẢ HAI → điểm đến từ SỬA, đáng merge.
- Chỉ hơn ở fixture gốc → mùi over-fit (vd variant B mẫu quá khớp streak); xem
  lại diff hoặc đổi fixture thử lại, KHÔNG merge vội.

---

## Bước 6 — Đề xuất và merge (chờ Son chốt)

Báo cáo ngắn: bảng so + bản thắng + thắng nhờ tiêu chí nào + 1–2 câu "merge
nguyên bản thắng hay ghép ý 2 bản" (ví dụ điển hình: ghép A "từ-cấm TS/JS" vào
D "khung 3 nhịp" nếu cả hai đều đẩy điểm mà không đụng nhau — nhưng chỉ đề xuất,
KHÔNG tự merge). Chờ Son đồng ý → chép `proposed-SKILL.md` bản thắng đè
`teen/SKILL.md`, giữ nguyên `runs/<ts>/` làm lịch sử.

---

## Kiểm Luật cứng của tune (tự-rà thiết kế này có phạm không)

- [x] **Một biến duy nhất** — mọi variant cùng fixture.txt; mỗi variant chỉ khác
      ở một sửa đổi nhỏ trong proposed-SKILL.md.
- [~] **Có thước trước khi chạy** — teen THIẾU rubric.md; đã chốt "rubric tạm
      teen" đóng băng vào fixture, cùng một thước cho mọi bản. Đường chuẩn hơn:
      tạo teen/rubric.md ở lượt riêng TRƯỚC baseline. (dấu ~ = làm được nhưng
      kém-tin hơn đường chuẩn — đây là friction, không phải vi phạm.)
- [x] **Không đụng bản thật khi thử** — teen/SKILL.md chỉ đổi ở Bước 6 sau confirm.
- [x] **Chấm mù** — che nhãn A–E khi chấm.
- [x] **Thắng phải qua confirm** — Bước 5 chạy agent mới trên 2 fixture.
- [x] **Không ghi state** (Bước 7) — chỉ đọc, mọi thứ nằm trong runs/<ts>/.
- [x] **Không sửa rubric giữa lượt** — rubric tạm đóng băng TRƯỚC baseline.
