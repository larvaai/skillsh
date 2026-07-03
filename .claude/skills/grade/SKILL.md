---
name: grade
description: "Chấm chất lượng output của BẤT KỲ skill nào theo đúng hợp đồng của chính skill đó — đọc `<skill>/rubric.md` (khung chung ở `grade/meta-rubric.md`), cho mỗi tiêu chí 0/1/2, áp gate (các tiêu chí xương sống = 0 thì rớt cả bản), ra điểm để so nhiều bản một cách nhất quán. Dùng khi cần so nhiều bản của một skill xem bản nào tốt hơn, hoặc kiểm một artifact/câu trả lời có bám hợp đồng không. Là cây thước cho skill `tune`. Ví dụ: `grade explain`, `grade shape`, `grade uat`."
---

# Grade — Chấm output của một skill theo rubric của skill đó

Grade trả lời đúng một câu hỏi: *bản này bám HỢP ĐỒNG của skill tới đâu?* Điểm ra để **so nhiều bản một cách nhất quán** — đây là cây thước cho skill `tune`.

Grade KHÔNG tự nghĩ ra tiêu chuẩn. Chuẩn để chấm luôn là `<skill>/SKILL.md` (+ file luật con của nó) — grade chỉ đo mức độ output làm đúng cái skill đã hứa. Rubric là bản diễn giải hợp đồng đó thành thang 0/1/2.

Phân vai: `review` đọc CODE tìm gap. `triage` phán số phận một file. `grade` đọc một OUTPUT (artifact, câu giải thích, phiếu, report…) và chấm nó theo rubric. `checkpoint` gác Định-nghĩa-Xong (đúng path + đủ mục) — grade đo CHẤT LƯỢNG bên trong, sâu hơn cấu trúc.

## Cần gì để chấm (đầu vào)

- **skill** — chấm skill nào (từ argument, vd `grade shape`). BẮT BUỘC — quyết rubric nào được dùng.
- **fixture** — đầu vào mà skill đó cần để tạo output, khai ở mục "Đầu vào để chấm" trong `<skill>/rubric.md`. Vd `explain` cần {project, level, mode}; `shape` cần {artifact + Domain Model GĐ5 làm nguồn đối chiếu}.
- **output** — nguyên văn bản cần chấm.

Thiếu cái nào thì suy từ context/state (`state/current.json`, `state/project/<name>/…`); vẫn không rõ thì hỏi đúng một lần rồi chấm. Nếu đang chấm cho `tune`: mọi thứ do tune truyền vào, không hỏi lại.

## Bước 0 — Gom đầu vào

Xác định `skill`, fixture, và lấy nguyên văn output cần chấm.

## Bước 1 — Đọc chuẩn để chấm

Đọc trước khi chấm:
- `grade/meta-rubric.md` — khung chung: 5 trục phổ quát, luật gate, khung report. LUÔN đọc.
- `<skill>/rubric.md` — rubric riêng của skill: danh sách tiêu chí + anchor 0/1/2 + tiêu chí nào là gate + "Đầu vào để chấm". Đây là thước chính.
- `<skill>/SKILL.md` (+ file luật con nó trỏ tới, vd `explain/rule/principles.md`; + `quy-trinh-idea-to-operate.md` nếu là skill GĐ; + `constitution/definition-of-done.md` nếu bước có Định-nghĩa-Xong) — nguồn gốc của mọi tiêu chí, để hiểu anchor cho đúng.

**Chưa có `<skill>/rubric.md`?** Dừng-mềm: dựng tiêu chí TẠM từ `meta-rubric.md` (đặc tả 5 trục theo hợp đồng skill), chấm được nhưng ghi rõ đầu report `⚠️ rubric tạm — nên tạo <skill>/rubric.md để điểm ổn định giữa các lần`. Đường chuẩn là mỗi skill có rubric riêng.

Đọc nguồn thật ở mức vừa đủ để kiểm tiêu chí **Bám nguồn (A2)** — với `explain`/`review` là đọc code; với skill pipeline là đọc artifact GĐ trước mà bản này lẽ ra phải bám. Không map cả repo (đó là `atlas`); có `.ai-understanding/` thì đọc để đối chiếu nhanh.

## Bước 2 — Chấm từng tiêu chí

Cho mỗi tiêu chí trong `<skill>/rubric.md` điểm 0/1/2 theo anchor, kèm **một câu** lý do. Rồi áp **gate**: tiêu chí xương sống (thường là 3 tiêu chí phủ trục A1 Đúng+đủ / A2 Bám nguồn / A3 Đọc-được) mà = 0 → cả bản **rớt gate**, dù tổng cao. Gate quan trọng hơn tổng.

## Bước 3 — Xuất report

Report phẳng, khung cố định theo `meta-rubric.md` (để nhiều bản xếp cạnh nhau so được):

```
CHẤM: <skill> · <fixture: định danh bản / đầu vào>

1 <Tên tiêu chí 1>   [n] — <lý do 1 câu>
2 <Tên tiêu chí 2>   [n] — <...>
...

TỔNG: <n>/<max>   GATE: <đạt | rớt: tiêu chí ...>
SỬA TRƯỚC TIÊN: <một câu — đòn bẩy lớn nhất để bản này tốt hơn>
```

Tên và số tiêu chí lấy đúng từ `<skill>/rubric.md` (explain 7 tiêu chí gate 1/4/5; shape/uat 7 tiêu chí gate 1/2/3; checkpoint có thể 5…). Không thêm khen/chê ngoài khung. Grade không sửa output, không viết bản vá dài — chỉ chấm và chỉ ra đòn bẩy lớn nhất. Thử bản vá là việc của `tune`.

## Ghi kết quả

Grade không đụng state chung của skill khác. Chạy lẻ: chỉ in report. Chạy trong `tune`: ghi report vào `experiments/runs/<ts>/<variant>/grade.txt` theo đường dẫn tune chỉ định.

## Chế độ in-flow (advisory) — do checkpoint gọi

`checkpoint` gọi grade ngay tại cổng go/no-go của một bước (Bước 2b của checkpoint): grade chấm artifact giai đoạn theo `<owner>/rubric.md`, trả **TỔNG + GATE + đòn-bẩy-sửa-trước** để checkpoint đính vào phiếu. Đây là điểm THAM KHẢO cho user — grade **không tự lật FAIL, không ký thay, không chặn pipeline** (đúng warm-never-brick + user-giữ-GO). Không có rubric cho giai đoạn đó → grade báo "n/a", checkpoint bỏ qua. Grade vẫn read-only: chỉ chấm và in, checkpoint mới là chỗ ghi phiếu.

## Ranh giới

- Grade chấm MỘT skill mỗi lần, theo đúng rubric của skill đó — không trộn tiêu chí của skill khác.
- Grade không phán skill nên tồn tại hay không (`skill-define`), không viết/sửa SKILL.md (`skill-creator`/`tune`), không tìm bug trong code sản phẩm (`review`).
- Grade chấm output của skill trong SUITE này. Không dùng grade cho skill của bên thứ ba (docx/pdf…) — chúng không có hợp đồng trong `.claude/skills/`.
