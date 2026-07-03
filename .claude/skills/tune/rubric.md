# Rubric — 7 tiêu chí chấm một lượt `tune` (meta: chỉnh skill bằng thí nghiệm song song)

Mỗi tiêu chí 0/1/2. Khung chung: `grade/meta-rubric.md`. Chuẩn gốc để chấm: `tune/SKILL.md` (7 bước + mục "## Luật cứng"). Rubric chỉ biến hợp đồng đó thành thước đo được — KHÔNG thêm tiêu chuẩn mới. Năm Luật cứng của `tune` (một-biến-duy-nhất · có-thước-trước · không-đụng-bản-thật · chấm-mù · thắng-phải-qua-confirm) được gấp thành các anchor-0 bên dưới: vi phạm luật cứng nào thì tiêu chí chứa nó = 0.

**Đầu vào để chấm (fixture):** skill được tune (vd `explain`) · fixture cố định của lượt (`experiments/runs/<ts>/fixture.txt`) · `<skill>/rubric.md` dùng làm thước · output của lượt tune (báo cáo cuối + thư mục `runs/<ts>/` chứa baseline/các variant/grade.txt).

Tiêu chí **1 (Đủ mục kết luận), 2 (Điểm từ grade thật), 3 (Đọc-được)** là **xương sống (gate)**: rớt bất kỳ cái nào → rớt cả bản dù tổng cao.

## 1. ĐỦ MỤC KẾT LUẬN — đúng + đủ output của một lượt tune (xương sống, A1)

Lượt tune phải giao đủ: (a) fixture cố định ghi ra file; (b) baseline đã chấm; (c) bảng so nhiều bản × tiêu chí (số cột tiêu chí lấy đúng từ `<skill>/rubric.md`); (d) bản thắng; (e) nói rõ thắng nhờ tiêu chí nào. Bỏ một mục ≠ rút gọn.

- 0 — thiếu hẳn một mục xương: KHÔNG có fixture cố định ghi ra file, HOẶC không có baseline đã chấm, HOẶC không có bảng so (chỉ tuyên bố một bản thắng mà không đặt các bản cạnh nhau theo tiêu chí), HOẶC không chỉ ra bản thắng.
- 1 — đủ mặt nhưng một mục sơ sài: bảng so thiếu cột Gate hoặc thiếu cột "bản này đổi gì", hoặc có bản thắng nhưng không nói thắng nhờ tiêu chí nào, hoặc baseline có output mà thiếu grade.txt.
- 2 — đủ cả bộ: fixture ghi ra file · baseline+grade · bảng so đủ cột (mỗi bản × tiêu chí + Tổng + Gate + 1 câu "đổi gì") · bản thắng · nêu rõ thắng nhờ tiêu chí nào so với baseline.

## 2. ĐIỂM TỪ GRADE THẬT — không bịa bằng chứng thí nghiệm (xương sống, A2)

Mọi con số trong bảng so phải truy được về một `grade.txt` thật của `grade <skill>` trên `output.txt` thật của bản đó, cùng một rubric `<skill>/rubric.md` cho MỌI bản. Không tự chế điểm, không xếp hạng bằng cảm tính.

- 0 — bịa bằng chứng: điền điểm mà không có `grade.txt`/`output.txt` đứng sau, HOẶC một bản chấm bằng rubric/tiêu chí khác bản còn lại (đổi thước giữa lượt), HOẶC output của variant KHÔNG tuân `proposed-SKILL.md` của chính nó (chạy bản gốc rồi gán cho variant → điểm vô nghĩa), HOẶC xếp hạng không khớp điểm đã ghi.
- 1 — điểm chủ yếu có nguồn nhưng một chỗ hở: một bản thiếu grade.txt mà vẫn cho điểm, hoặc một con số trong bảng lệch so với grade.txt, hoặc chưa nói rõ mọi bản dùng cùng một rubric.
- 2 — mỗi ô điểm nối được về grade.txt của đúng bản đó; mọi bản (kể cả baseline) dùng CÙNG một `<skill>/rubric.md`; mỗi output tuân đúng `proposed-SKILL.md` của nó; xếp hạng khớp điểm.

## 3. BÁO CÁO ĐỌC-ĐƯỢC — Son quét là nắm (xương sống, A3)

Báo cáo cuối cho người quyết: quét 2–3 phút thấy ngay bản nào thắng, hơn baseline bao nhiêu, thắng nhờ đâu, nên làm gì tiếp. Bảng so gọn, câu ngắn, không bắt người đọc tự dò các thư mục runs.

- 0 — phải tự đào `runs/<ts>/` mới hiểu kết quả; HOẶC đổ số liệu thô không có bảng/kết luận; HOẶC dày đặc, đọc xong vẫn không biết nên theo hướng nào.
- 1 — đọc được nhưng lệch: bảng có mà thiếu một câu chốt "nên merge gì", hoặc kết luận chìm dưới chi tiết log, hoặc câu dài rườm.
- 2 — mở bằng bản thắng + mức hơn baseline; bảng so gọn cạnh nhau; 1–2 câu khuyến nghị (merge nguyên bản thắng hay ghép ý 2 bản) rõ vì sao; scan 2–3 phút là đủ quyết.

## 4. MỘT BIẾN DUY NHẤT — thí nghiệm sạch (A4)

Mọi bản chạy trên CÙNG một fixture; chỉ khác ở bản sửa skill. Có baseline làm mốc. Mỗi hướng nhắm một tiêu chí yếu KHÁC nhau trong `<skill>/rubric.md`, không trùng hướng.

- 0 — đổi fixture giữa các bản (mỗi bản chạy đầu vào khác → không so được), HOẶC không có baseline làm mốc, HOẶC các variant khác nhau nhiều thứ cùng lúc ngoài bản sửa skill.
- 1 — cùng fixture + có baseline, nhưng hai hướng trùng nhau (phí một bản) hoặc hướng không nhắm vào tiêu chí yếu đọc từ baseline/grade.
- 2 — một fixture cố định cho mọi bản; baseline làm mốc; mỗi hướng một giả thuyết riêng nhắm một tiêu chí đang thấp/rớt gate; không trùng hướng.

## 5. KHÔNG ĐỤNG BẢN THẬT KHI ĐANG THỬ (A4)

Mỗi bản sửa nằm trong `experiments/runs/<ts>/<variant>/`; `<skill>/SKILL.md` thật chỉ được đổi ở Bước 6 sau khi có bản thắng đã confirm và Son đã chốt. Không ghi `state/current.json`; không tự sửa `<skill>/rubric.md` giữa lượt.

- 0 — sửa thẳng `<skill>/SKILL.md` thật trong lúc thí nghiệm (trước khi có bản thắng + confirm + chốt), HOẶC ghi đè `state/current.json`, HOẶC đổi `<skill>/rubric.md` giữa lượt (đổi thước giữa chừng).
- 1 — giữ bản thật nguyên nhưng để lịch sử thí nghiệm rò ra ngoài `experiments/runs/<ts>/`, hoặc đụng state khác (user-state) mà không cần.
- 2 — mọi bản sửa cô lập trong `runs/<ts>/<variant>/`; bản thật + rubric + state không bị đụng suốt lượt; lịch sử nằm trọn trong `runs/<ts>/`.

## 6. CHẤM MÙ + CONFIRM TRƯỚC KHI ĐỀ XUẤT MERGE (A4/A5)

Chấm chỉ thấy {fixture, output}, không thấy bản theo hướng nào (đặt tên A/B/C). Bản thắng phải qua Bước 5: chạy lại bằng agent MỚI trên đúng fixture + một fixture thứ hai cùng loại, để chắc điểm đến từ SỬA chứ không từ người viết hay từ over-fit.

- 0 — chấm khi biết bản nào theo hướng nào (thiên vị hướng mình thích), HOẶC đề xuất merge một bản CHƯA qua confirm (bỏ Bước 5), HOẶC chỉ confirm trên đúng fixture gốc rồi kết luận (không loại được over-fit).
- 1 — có chấm mù nhưng confirm hụt: chỉ chạy lại trên fixture gốc, thiếu fixture thứ hai; hoặc confirm bằng chính agent cũ chứ không phải agent mới.
- 2 — chấm mù (tên A/B/C, không lộ hướng); bản thắng chạy lại bằng agent MỚI trên fixture gốc + một fixture thứ hai cùng loại; kết luận nói rõ điểm đến từ SỬA (hơn baseline ở cả hai) hay có mùi over-fit.

## 7. ĐÚNG VAI META — chờ Son chốt, không tự merge, không tạo skill mới (A5)

Tune tinh chỉnh PROMPT của một skill ĐÃ CÓ; kết bằng đề xuất + chờ Son quyết, chỉ merge SAU khi Son đồng ý. Không tạo skill mới (đó là `skill-creator`), không phán skill nên tồn tại hay không (`skill-define`), không code sản phẩm (`frame`/`partner`).

- 0 — tự merge đè `<skill>/SKILL.md` mà chưa chờ Son chốt, HOẶC lấn vai: tạo skill mới / phán một skill nên tồn tại hay không / đi code sản phẩm thay vì chỉnh prompt.
- 1 — đúng vai nhưng kết mờ: có đề xuất nhưng không nói rõ đang CHỜ Son chốt, hoặc gợi ý bước tiếp chung chung.
- 2 — kết bằng đề xuất merge (nguyên bản thắng hay ghép ý) + nêu rõ chờ Son chốt; chỉ merge sau khi Son đồng ý; nếu muốn đi tiếp thì trỏ vòng tune mới (baseline = bản vừa merge); không đụng việc `skill-creator`/`skill-define`/`frame`.

## Gate (tiêu chí xương sống)

Tiêu chí **1, 2, 3** là xương sống. Bất kỳ cái nào = 0 → lượt tune **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một lượt tune 12/14 nhưng điểm trong bảng không nối được về grade.txt thật (tiêu chí 2 = 0) vẫn rớt — vì cả kết luận "hướng nào thắng" dựng trên số bịa thì Son sẽ merge nhầm. Khi so nhiều lượt: loại hết bản rớt gate TRƯỚC, rồi mới xếp phần còn lại theo tổng.

## Khung report (xếp nhiều bản cạnh nhau)

```
CHẤM: tune · <skill được tune> · <fixture: runs/<ts>>
1 Đủ mục kết luận      [n] — <lý do 1 câu>
2 Điểm từ grade thật   [n] — <...>
3 Báo cáo đọc-được     [n] — <...>
4 Một biến duy nhất    [n] — <...>
5 Không đụng bản thật  [n] — <...>
6 Chấm mù + confirm    [n] — <...>
7 Đúng vai meta        [n] — <...>
TỔNG: <n>/14   ·   GATE: đạt / RỚT (rớt ở tiêu chí __)
SỬA TRƯỚC TIÊN: <một câu — đòn bẩy lớn nhất để lượt tune này tốt hơn>
```

## Vì sao 7 tiêu chí này

Ba xương sống đo *có ra đúng kết luận + trung thực + đọc được không*: đủ mục kết luận (A1), điểm từ grade thật không bịa (A2 — gate nặng nhất, vì cả lượt tune tồn tại chỉ để nói "hướng nào thắng bằng số"), báo cáo đọc-được (A3). Bốn cái sau đo *thí nghiệm có sạch và đúng vai không*: một-biến-duy-nhất và không-đụng-bản-thật (hai luật cứng giữ so sánh có nghĩa và bản thật an toàn), chấm-mù + confirm (hai luật cứng chống thiên vị và chống "agent giỏi ≠ sửa tốt"/over-fit), đúng vai meta (chờ Son chốt, không tự merge, không tạo skill mới). Gộp lại = trọn hợp đồng của `tune` (7 bước + 5 Luật cứng), không hơn. Thêm tiêu chí thứ 8 chỉ khi có kiểu lỗi thật lặp lại mà 7 cái này không bắt được.
