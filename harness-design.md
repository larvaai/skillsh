# Harness đa-project — thiết kế skills, memory, folder

> Viết 2026-07-02, dựa trên file thật trong `skillsh/` (22 skill, 2 project trong `state/project/`, 2 roadmap có sẵn). Bản này trả lời 3 câu: cần skill gì, memory từng project thiết kế ra sao, folder chia thế nào.

## 0. Kết luận trước

Bạn không cần xây harness từ đầu. Bộ 22 skill hiện tại đã phủ đủ 15 giai đoạn cho **1 project**. Thứ còn thiếu là **lớp điều phối đa-project** (chính là cái `roadmap-portfolio.md` và `roadmap-suite.md` đã chẩn đoán) và **một đợt dọn chuẩn hoá** — vì dữ liệu thật hiện nay đã lộ 3 vết nứt sẽ vỡ khi thêm project thứ 3:

1. Cùng 1 project có 3 khoá khác nhau: thư mục `rebuild-hex-agent/`, state `state/project/hex_agent/`, còn `_index.json` ghi `"project": "hex-agent-rebuild"`.
2. Hai project dùng 2 schema state khác nhau: `multi-lens-chat` dùng `schema_version: 1` + `current_pillar/current_stage: "PRD"` (tiếng Anh), còn hex dùng `giai_doan: "gd14_operate"` (tiếng Việt). Bảng portfolio không đọc chéo được.
3. `user-state.json` tồn tại 2 nơi (`rebuild-hex-agent/` và `state/project/hex_agent/`) — không rõ bản nào là thật.

## 1. Bộ skill — cái gì đã có, cái gì phải build

### 1a. Đã có: 22 skill phủ đủ 15 giai đoạn (cho 1 project)

| GĐ | Tầng quyết định | Skill sở hữu | Artifact |
|---|---|---|---|
| 0–5 Idea → Business → Product → Requirements → PRD → Domain | WHY / WHAT VALUE / WHAT EXACTLY / WORLD MODEL | `idea` (kèm `partner` khi cần đi cả pipeline) | `pipeline/ideas/` + `05-idea-domain.md` |
| 6 Solution Architecture | SHAPE | `shape` | `06-shape.md` + `shape.json` |
| 7 Tech Stack | TOOLS | `stack` | `07-stack.md` + `stack.json` |
| 8 Live Slice | PROOF | `skeleton` | `08-skeleton.md` + `skeleton.json` |
| 9 Roadmap & Backlog (Epic→Feature→Story→AC) | WHAT FIRST | `backlog` | `09-backlog.md` + `backlog.json` |
| 10 Module & Ownership | — | `modules` | `10-modules.md` + `modules.json` |
| 11 Delivery / code | HOW SAFELY | `delivery` | `11-delivery.md` + `delivery.json` |
| 12 Verification / UAT | — | `uat` | `12-uat.md` + `uat.json` |
| 13 Release / Go-No-Go | SHIP | `ship` | `13-ship.md` + `ship.json` |
| 14 Operate & Measure → quay lại 9 | LEARN | `operate` | `14-operate.md` + `operate.json` |
| Xuyên suốt: hiểu repo | — | `atlas` (nền, ghi `.ai-understanding/`), `explain`, `teen`, `trace` | 20 artifact atlas |
| Xuyên suốt: kiểm soát chất lượng | — | `review`, `triage`, `traceability`, `grade`, `tune` | `_review.json`, `_traceability.md` |
| Meta | — | `frame`, `skill-define` | — |

Không build lại bất kỳ skill nào trong bảng này. Nguyên tắc giữ nguyên: **mỗi skill sở hữu đúng 1 file state**, skill khác chỉ đọc.

### 1b. Phải build: lớp portfolio (nhạc trưởng)

Đây là toàn bộ phần "CTO nhìn cả doanh nghiệp" còn thiếu. Theo đúng phân rã của `roadmap-suite.md`, tách thành component nhỏ thay vì 1 skill ôm hết:

| Component | Việc | Ghi gì |
|---|---|---|
| **normalizer** | Quy tắc duy nhất path ↔ khoá project. Chữa thẳng vết nứt #1. | bảng path↔key trong `portfolio.json` |
| **portfolio** | Sổ cái mọi project: key, path, giai đoạn, `cho_duyet`, `updated_at`. Nguồn sự thật cho mọi thứ bên dưới. | `state/portfolio.json` (file chủ mới duy nhất) |
| **switch** | Điểm vào duy nhất đổi con trỏ `current.json`, từ chối key ngoài sổ cái, in recap khi vào project. | `state/current.json` |
| **dashboard + router** | Bảng mỗi-dòng-một-project (project chờ duyệt nổi lên đầu) + tiến cử skill kế tiếp theo state. Chỉ tiến cử, không auto-run. | không ghi gì (read-only) |
| **priority-critic** | Khi ≥2 project cùng `cho_duyet: true` → phản biện thứ tự dựa trên số liệu thật (số ẩn số mở, số ngày im lặng). Chỉ đề xuất. | không ghi gì |

Luật của cả lớp: **read-only trên state của từng project**, chỉ được ghi `portfolio.json` + `current.json`. Quyền quyết scope và thứ tự vẫn ở bạn.

## 2. Memory từng project — 3 tầng

Tách theo câu hỏi mà mỗi tầng trả lời:

```
TẦNG 1 — Portfolio (CTO): "toàn công ty đang thế nào?"
  state/portfolio.json      sổ cái mọi project
  state/current.json        con trỏ: đang đứng ở project nào
                            shape chuẩn {project, path, mode, giai_doan, cho_duyet, updated_at}

TẦNG 2 — Project (PM/PO): "project này đang ở đâu, chờ quyết định gì?"
  state/project/<key>/
    pipeline-state.json     giai đoạn hiện tại + trạng thái gate từng GĐ
                            (cho_duyet, nguoi_ky, pass_rate… như gd12/gd13 của hex)
    user-state.json         mức hiểu của bạn với project này (L0–L8)
    <skill>-state.json      mỗi skill 1 file riêng (idea-state, review-state…)
    decisions + open_questions  nằm trong pipeline-state (mẫu tốt sẵn có:
                            multi-lens-chat với NEED-1/CASE-1/OQ-4..6)

TẦNG 3 — Repo (engineer): "code thực sự là gì?"
  <repo>/.ai-understanding/   20 artifact atlas + index + scorecard + drift ledger
  <workspace>/pipeline/       artifact 15 GĐ (nguồn: file .md; state: file .json)
```

Bốn luật memory, đều đã có tiền lệ trong bộ skill, giờ nâng thành luật chung:

1. **Một file một chủ.** Skill nào sở hữu file nào ghi rõ trong SKILL.md. Vi phạm là bug.
2. **Một project một khoá.** Khoá do normalizer cấp, dùng thống nhất ở cả 3 tầng. Hết cảnh `hex_agent` / `rebuild-hex-agent` / `hex-agent-rebuild`.
3. **Một schema cho mọi project.** Chuẩn hoá theo mẫu `multi-lens-chat` (`schema_version`, `decisions[]` có `rationale` + `rejected_alternatives` + `traces_to`, `open_questions[]` có `leverage`) nhưng thống nhất tên giai đoạn theo `gd00..gd14`. Có `schema_version` để di trú sau này.
4. **Gate là dữ liệu, không phải lời kể.** Mỗi GĐ kết thúc bằng trạng thái máy-đọc-được: `cho_duyet` → `nguoi_ky` → `gate: GO/NO-GO`. AI chuẩn bị đủ để ký, không tự ký thay (đúng mẫu signoff GĐ12 của hex).

## 3. Folder — chia như một công ty công nghệ

```
skillsh/                          ← văn phòng CTO (harness, không phải code sản phẩm)
├── .claude/skills/               ← 22 skill + lớp portfolio mới
├── state/                        ← TẦNG 1+2: memory điều hành
│   ├── portfolio.json
│   ├── current.json
│   └── project/<key>/            ← memory từng project (mục 2)
├── projects/<key>/               ← bàn làm việc từng project (workspace, KHÔNG chứa code)
│   ├── README.md                 ← 1 trang: project là gì, đang GĐ nào, link code repo
│   ├── pipeline/                 ← artifact 15 GĐ
│   │   ├── ideas/                ← GĐ0: mỗi idea 1 cặp .md + .json + _index
│   │   ├── 01-business.md … 14-operate.md
│   │   ├── <stage>.json          ← state máy đọc của từng GĐ
│   │   ├── _index.json           ← tổng hợp project (nguồn cho portfolio.json)
│   │   ├── _traceability.md/json ← Epic→Feature→Story→AC→code→test
│   │   └── _review.json _grade.json
│   ├── explain/  review/  00-understanding/
│   └── (frame/ uat/ … theo skill nào đã chạy)
├── roadmap-portfolio.md  roadmap-suite.md   ← roadmap của chính harness
└── experiments/                  ← skill-test, skill-eval (đã có)

<code repo thật, nơi khác, vd ~/Desktop/namnson/hex_agent>
└── .ai-understanding/            ← TẦNG 3: atlas sống cạnh code
```

Ba nguyên tắc chia:

- **Code ở repo, giấy tờ ở workspace, memory điều hành ở `state/`.** Trừ `.ai-understanding/` phải sống cạnh code (vì trôi theo commit), mọi artifact giấy tờ nằm trong `projects/<key>/` để xoá/lưu trữ 1 project là xoá 1 thư mục, không vương vãi.
- **`.md` cho người, `.json` cho máy** — cặp đôi từng giai đoạn, đúng mẫu `rebuild-hex-agent/pipeline/` đang làm. Dashboard chỉ đọc `.json`.
- **Việc dọn cụ thể:** chuyển `rebuild-hex-agent/` → `projects/hex-agent/`, hợp nhất 2 bản `user-state.json` về `state/project/hex-agent/`, migrate `multi-lens-chat` sang schema chung. Làm 1 lần, trước khi thêm project mới.

## 4. Nhịp vận hành CTO

- **Vào ngày làm việc:** `/portfolio` → bảng tổng → project nào `cho_duyet` nổi đầu → chọn 1 → switch → router tiến cử skill kế → chạy skill đó. Không bao giờ phải nhớ "hôm trước đang dở gì" — state nhớ hộ.
- **Cuối mỗi giai đoạn:** skill sở hữu GĐ đó ghi artifact `.md` + state `.json`, đặt `cho_duyet: true`. Bạn đọc, ký (hoặc NO-GO kèm lý do). Không ký thì pipeline đứng — đó là tính năng, không phải lỗi.
- **GĐ14 → quay lại GĐ9:** item từ operate đẩy về backlog thành epic/story mới (hex đang làm đúng: I-1 đóng R3, I-2 SPIKE resume, I-3 OQ-1 DORA). Vòng LEARN khép kín.
- **Hàng tuần:** chạy priority-critic trên các project cùng chờ duyệt + `grade` chấm chất lượng artifact. Có thể đặt scheduled task chạy `/portfolio` mỗi sáng.

## 5. Thứ tự build (giữ nguyên logic roadmap có sẵn)

1. **Dọn + normalizer** — thống nhất khoá và schema cho 2 project hiện có. Nền sai thì mọi thứ trên vô nghĩa (đúng Feature 4 của `roadmap-portfolio.md`).
2. **`portfolio.json` + bảng tổng hợp** — dùng được ngay, không phụ thuộc gì khác.
3. **switch + router** — chuyển ngữ cảnh an toàn, tiến cử skill kế.
4. **priority-critic** — thêm cuối, không chặn 3 bước đầu.

Mỗi bước dùng chính `skill-define` để định nghĩa, `skill-eval` trong `experiments/` để test — harness tự xây bằng quy trình của nó.
