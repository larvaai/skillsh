---
name: tune
description: "Cải tiến BẤT KỲ skill nào đã có bằng thí nghiệm song song: cố định một fixture, chạy baseline, cho nhiều agent mỗi người thử một hướng sửa khác nhau, chấm mỗi bản bằng thước (`grade <skill>` đọc `<skill>/rubric.md`), rồi xếp hạng và đề xuất nên theo hướng nào. Dùng khi một skill chạy chưa đúng ý và muốn so nhiều cách sửa thay vì đoán. Ví dụ: `tune explain`, `tune shape`, `tune uat`."
---

# Tune — Chỉnh một skill bằng thí nghiệm song song

Tune không đoán cách sửa một skill — nó **thử nhiều cách cùng lúc rồi đo**. Giữ mọi thứ cố định trừ đúng một biến (bản sửa skill), cho vài agent mỗi người một hướng, chấm kết quả bằng cùng một thước, rồi cho thấy hướng nào thắng và thắng nhờ đâu.

Phân vai:
- `skill-define` — có đáng làm skill MỚI không (trước khi build).
- `skill-creator` — viết/đóng gói một SKILL.md thật.
- `tune` — làm một skill ĐÃ CÓ tốt hơn, bằng thí nghiệm + chấm điểm. Không tạo skill mới, không phán skill nên tồn tại hay không.
- `frame`/`partner` "spike/fake-first" — về build SẢN PHẨM/CODE. Tune tinh chỉnh PROMPT của skill. Khác nhau.

## Luật cứng (vi phạm là hỏng thí nghiệm)

- **Một biến duy nhất.** Mọi bản chạy trên cùng fixture. Chỉ khác ở bản sửa skill. Đổi fixture giữa các bản → không so được, làm lại.
- **Có thước trước khi chạy.** Thước là `grade <skill>`, đọc `<skill>/rubric.md`. Skill chưa có rubric riêng → `grade` vẫn chấm được bằng tiêu chí tạm suy từ `grade/meta-rubric.md`, NHƯNG điểm sẽ kém ổn định giữa các lần; nên tạo `<skill>/rubric.md` trước để thí nghiệm đáng tin. Cùng một lượt tune phải dùng CÙNG một rubric cho mọi bản.
- **Không đụng bản thật khi đang thử.** Mỗi bản sửa nằm trong thư mục riêng (`experiments/runs/<ts>/<variant>/`). `<skill>/SKILL.md` thật chỉ đổi ở Bước 6, sau khi có bản thắng đã qua confirm.
- **Chấm mù.** Người/agent chấm chỉ thấy {fixture, output}, KHÔNG thấy bản đó theo hướng nào. Tránh thiên vị hướng mình thích.
- **Thắng phải qua confirm.** Một bản có thể ăn điểm vì agent viết hay, không phải vì bản sửa tốt. Trước khi merge, chạy lại bản thắng bằng agent MỚI (Bước 5) để chắc điểm đến từ SỬA, không từ người viết.

## Bước 0 — Chốt mục tiêu và fixture

- **Skill cần tune**: từ argument, vd `tune explain`, `tune shape`. Không có → hỏi một lần.
- **Thước**: `grade <skill>` → `<skill>/rubric.md`. Đọc rubric trước để biết mỗi bản sẽ bị chấm bằng những tiêu chí nào (và tiêu chí nào là gate).
- **Fixture** (giữ cố định cả thí nghiệm): chính là mục **"Đầu vào để chấm"** trong `<skill>/rubric.md`. Mỗi loại skill có fixture khác nhau:
  - đọc-hiểu (explain/trace/teen): {project, level, mode}. Mặc định project lấy từ `state/current.json`; level từ `state/project/<name>/user-state.json` (không có thì chọn một mức và ghi rõ).
  - pipeline GĐ (shape/stack/uat…): {artifact GĐ trước làm nguồn} — vd tune `shape` thì fixture là Domain Model GĐ5 để mọi bản shape cùng bám một nguồn.
  - hạ tầng/meta (progress/checkpoint/skill-define…): {tình huống đầu vào cụ thể} — vd một progress.json + một task báo xong để chấm bản advance.

Tạo thư mục lượt `experiments/runs/<ts>/` và ghi fixture ra `experiments/runs/<ts>/fixture.txt`. Mọi bản đọc đúng file này — không ai được đổi fixture giữa chừng.

## Bước 1 — Baseline (bản đối chứng)

Chạy skill HIỆN TẠI trên fixture → lưu `runs/<ts>/baseline/output.txt`. Chấm bằng `grade <skill>` → `runs/<ts>/baseline/grade.txt`.

Đây là mốc: mọi bản sửa phải hơn cái này mới đáng theo. Không có baseline thì không biết một bản "8/14" là tiến hay lùi.

## Bước 2 — Chọn hướng thử (hypotheses)

Mỗi hướng là MỘT giả thuyết "sửa thế này thì skill tốt hơn", **nhắm một tiêu chí YẾU khác nhau trong `<skill>/rubric.md`**. Đọc baseline/grade.txt xem tiêu chí nào đang thấp/rớt gate → mỗi hướng đánh vào một điểm yếu đó. Mặc định 3–5 hướng (Son sửa/thêm/bớt tuỳ ý). Ví dụ khung (tự đổi theo skill):

```
Nhắm tiêu chí rớt gate  -> sửa luật/mục để bản không còn phạm anchor-0 của gate đó
Thêm ví dụ mẫu          -> 1 output mẫu tốt cho tình huống trọng tâm, để model calibrate
Thêm trigger/checklist  -> cụm từ/danh mục buộc skill không bỏ mục bắt buộc (A1)
Siết bám nguồn (A2)     -> luật "mọi số/tên phải trích nguồn, chưa chắc thì gắn nhãn"
Nguyên tắc đọc-được(A3) -> câu ngắn, mở bằng góc nhìn lãnh đạo, cấm tường bullet + số dòng
```

Một hướng = một variant. Đặt tên A/B/C… để chấm mù. Trùng hướng thì phí một agent.

## Bước 3 — Chạy song song

Giao mỗi variant cho MỘT agent, **gửi tất cả trong một lượt để chạy song song** (Claude Code: nhiều Task trong cùng một tin nhắn). Mỗi agent nhận:
- `<skill>/SKILL.md` + file luật con của nó (vd `explain/rule/principles.md`) hiện tại.
- `<skill>/rubric.md` + `grade/meta-rubric.md` (biết sẽ bị chấm bằng gì).
- fixture — đọc `runs/<ts>/fixture.txt`.
- đúng MỘT hướng của nó (không thấy hướng của bản khác).

Mỗi agent làm đúng hai việc, ghi vào `runs/<ts>/<variant>/`:
1. `proposed-SKILL.md` — bản skill đã sửa theo hướng của nó. Sửa tối thiểu đủ để thử hướng, không viết lại toàn bộ.
2. `output.txt` — đóng vai skill ĐÃ SỬA đó, chạy trên fixture. **Phải tuân `proposed-SKILL.md` của chính nó, không phải bản gốc** — nếu không, thí nghiệm vô nghĩa.

## Bước 4 — Chấm và xếp hạng

Với mỗi variant và baseline: chạy `grade <skill>` chỉ với {fixture, output.txt} → `grade.txt`. Chấm mù, không nhìn hướng.

Gom thành một bảng so (số cột tiêu chí lấy đúng từ `<skill>/rubric.md`):

```
Bản       1 2 3 4 5 6 7  Tổng  Gate       Bản này đổi gì
Baseline  . . . . . . .  ../14 ..         (gốc)
A         . . . . . . .  ../14 ..         <1 câu>
B         . . . . . . .  ../14 ..         <1 câu>
...
```

Xếp hạng: (1) loại hết bản rớt gate; (2) còn lại xếp theo Tổng; (3) hoà Tổng thì bản có diff NHỎ/ROBUST hơn thắng — sửa ít, ít rủi ro over-fit vào đúng fixture này.

## Bước 5 — Confirm bản thắng (chống nhầm "agent giỏi ≠ sửa tốt")

Lấy `proposed-SKILL.md` của bản thắng, chạy bằng agent MỚI trên: (a) đúng fixture, và (b) một fixture thứ hai khác (project/artifact khác cùng loại). Chấm lại bằng `grade <skill>`.
- Vẫn hơn baseline ở cả hai → điểm đến từ SỬA, đáng merge.
- Chỉ hơn ở fixture gốc → có mùi over-fit; xem lại diff hoặc đổi fixture thử lại.

## Bước 6 — Đề xuất và merge

Báo cáo ngắn cho Son:
- Bảng so + bản thắng + thắng nhờ tiêu chí nào.
- 1–2 câu: nên merge nguyên bản thắng, hay ghép ý của 2 bản — nói rõ vì sao.

Chờ Son chốt. Son đồng ý → chép `proposed-SKILL.md` bản thắng đè `<skill>/SKILL.md` (và/hoặc sửa file luật con), giữ nguyên `experiments/runs/<ts>/` làm lịch sử. Muốn đi tiếp → chạy vòng mới từ Bước 1, lấy bản vừa merge làm baseline mới.

## Bước 7 — Ranh giới state

Tune KHÔNG ghi `state/current.json` — nó thao tác trên SKILL, không phải "đang làm việc trên project X"; ghi đè sẽ khiến skill lần sau hiểu nhầm fixture. Fixture chỉ ĐỌC từ state, không ghi lại. Lịch sử thí nghiệm nằm trọn trong `experiments/runs/<ts>/`. Không đụng `user-state.json` hay state của skill khác. Tune cũng KHÔNG tự sửa `<skill>/rubric.md` giữa lượt (đổi thước giữa chừng = hỏng so sánh); muốn sửa rubric thì làm ở lượt riêng, trước khi chạy baseline.
