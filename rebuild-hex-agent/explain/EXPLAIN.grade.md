# EXPLAIN.grade — Chấm bản `explain/EXPLAIN.md` (HexAgent rebuild)

> Skill `grade` · Giai đoạn "chấm" của pipeline Idea→Operate.
> Chấm **một bản explain** theo đúng hợp đồng của explain (7 tiêu chí × 0/1/2, 3 tiêu chí xương sống = gate).
> Chuẩn gốc: `.claude/skills/explain/SKILL.md` (mức L0–L8 + 3 chế độ) + `explain/rule/principles.md` (cách nói) + `.claude/skills/grade/rubric.md` (7 anchor điểm).
> Đối tượng chấm: `rebuild-hex-agent/explain/EXPLAIN.md` — fixture: project = hex-agent-rebuild · level = **L3** (`user-state.json`) · mode = **overview**.
> Không bịa: mọi claim "khớp code / không khớp" đối chiếu evidence gốc `00-understanding/evidence-A-core-loop.md` + `evidence-B-domain-architecture.md` (anchor `file:line` bản gốc).

---

## ── GÓC NHÌN LÃNH ĐẠO (đọc 60 giây — không cần biết code) ──

1. **Kết luận.** Bản explain này **ĐẠT** — 14/14 điểm, qua cả 3 cổng xương sống (đúng mức người đọc, dễ đọc, không bịa). Nó là một bản mẫu tốt để so các bản khác chấm theo.
2. **Vì sao tin được điểm này.** Điều nguy hiểm nhất khi giải thích code là **nói cho oai mà bịa** — người đọc tin nhầm rồi ra quyết định sai. Tôi đã soi từng tên kỹ thuật trong bản explain (execute_tool, decompose gate, delegation, nghiệm-thu-bằng-bằng-chứng, event log, guards, SQLite resume, redact) và **đối chiếu với bằng chứng gốc**: mọi cái đều có thật, không có claim treo. Đây là lý do nó qua cổng "không bịa".
3. **Còn một điểm mài (không phải lỗi chặn).** Bản explain kết bằng một mục "Tự soi trước khi gửi" khá dài. Nó hữu ích cho tác giả nhưng là *phần bếp núc*, người đọc (CTO/business) không cần. Đòn bẩy lớn nhất để bản này gọn hơn: cắt/ẩn mục tự-soi đó khỏi bản giao cho người đọc.

---

## Cách chấm (đủ-là-đủ, theo rủi ro)

Rủi ro lớn nhất khi chấm một bản explain = **bỏ sót một claim bịa** (gate 5). Vì vậy phần nặng nhất của lần chấm này dồn vào việc kiểm từng tên code trong bản explain có thật trong evidence không. Ba cổng xương sống (Mức · Lời văn · Bám code) được soi kỹ; bốn tiêu chí còn lại đối chiếu nhanh theo anchor rubric. Không map lại repo (việc của `atlas`), không tìm gap thiết kế (việc của `review`) — chỉ đo bản explain bám hợp đồng explain tới đâu.

---

## Report (khung cố định — để nhiều bản xếp cạnh nhau so được)

```
CHẤM: explain · hex-agent-rebuild · L3 · overview

1 Mức        [2] — dừng đúng "Zoom 2 kỹ + chạm Zoom 3"; mỗi tên code (execute_tool/delegation/decompose gate/judge_acceptance/AgentKernel) chỉ gọi tên SAU khi neo vào một bước — khớp hành vi L3.
2 Chế độ     [2] — overview trọn: làm gì + cho ai (dev nền tảng) + vì sao tồn tại (báo-xong-khống & chạy-vô-hạn); theo đúng thang zoom 0→3.
3 Đủ ý       [2] — nắm cốt lõi: task→plan→sắp thứ tự→giao con→nghiệm-thu-bằng-bằng-chứng→có biên; nêu rõ "hai chốt đối nhau"; không thiếu ý gốc trong brief.
4 Lời văn    [2] — câu ngắn, phẳng; luồng kể bằng câu văn đánh số, bullet chỉ ở tầng module; không trích số dòng ở mức thấp (tuân E4).
5 Bám code   [2] — mọi tên/hành vi khớp evidence: execute_tool chokepoint (B:27), AgentKernel/KernelSession (B:2,§2), accept_decomposition + μ-proof + RENAME/STUCK (A:20), next_node leftmost-pending (A:17), DelegationManager.delegate scope⊆parent (A:26), judge_acceptance real-evidence-vs-scaffolding (A:32), tool.requested/completed→events.jsonl (B:44), redact-tại-emitter (B:39), PolicyGate fail-closed + var/workspace jail (B:38,41), SQLite=truth resume (B:45), RAG/Qdrant health-gated optional (B:34), UI⊥core (B:12). Không claim bịa.
6 Ranh giới  [2] — dạy người hiểu theo mức; mục "Neo về gói rebuild" hand off sang review/frame/atlas như sibling, KHÔNG tự làm việc của họ.
7 Kết        [2] — kết đúng L3: mời đi sâu Zoom 3 (lên L4) hoặc chọn một luồng cụ thể bằng chế độ `flow`, kèm câu hỏi định hướng.

TỔNG: 14/14   GATE: đạt
SỬA TRƯỚC TIÊN: không có lỗi chặn. Đòn bẩy gọt duy nhất — cắt/ẩn mục "Tự soi trước khi gửi" (dòng 91–98) khỏi bản giao người đọc: nó là checklist bếp núc của tác giả, không phải nội dung cho CTO/business.
```

---

## Ghi chú chi tiết cho dev (vì sao mỗi cổng qua)

### Gate 1 — Mức (L3): qua
Hợp đồng L3 = "Zoom 2 kỹ + chạm Zoom 3, mỗi thuật ngữ code neo vào bước trong luồng trước khi gọi tên" (`explain/SKILL.md:87-90`). Bản explain làm đúng:
- Zoom 0–1 hoàn toàn không có tên code (kiểm dòng 17–34) — đúng "vấn đề trước, thuật ngữ sau".
- Zoom 2 có 8 bước đánh số; mỗi tên code xuất hiện *sau* khi bước đã mô tả nó làm gì / ngăn gì: `decompose gate` ở bước 2, `next_node` (ngầm) ở bước 3, `DelegationManager.delegate` ở bước 4, `execute_tool` ở bước 5, `event log`/`events.jsonl` ở bước 6, `judge_acceptance` ở bước 7, `guards`/`max_steps` ở bước 8.
- `AgentKernel`/`KernelSession` được giữ tới Zoom 3 — đúng "jargon chỉ sống ở tầng nó được neo" (`SKILL.md:30`).
Không có chỗ nào thả tên code dưới ngưỡng → không rơi anchor 0 của rubric.

### Gate 4 — Lời văn: qua
Theo `principles.md` E1–E4:
- E2 (câu ngắn phẳng): câu trong Zoom 0–2 mỗi câu một ý; không thấy chuỗi "mà trong đó / theo đó" nối dài quá tay.
- E3 (cấm tường-bullet thay lời kể): luồng chính kể bằng 8 câu đánh số có văn, KHÔNG phải bullet cụt; bullet chỉ dùng để điểm danh module ở Zoom 3 — đúng ngoại lệ cho phép.
- E4 (cấm trích số dòng ở mức thấp): bản explain không dán `file.py:line` nào trong thân giải thích; chỉ trỏ tên artifact (`REVIEW.md`, `ATLAS.md §7`) ở mục neo — hợp lệ.
Điểm trừ tiềm năng duy nhất: mục "Tự soi" cuối bài hơi dày định dạng, nhưng đó là phụ lục tách khỏi thân giải thích, không kéo tiêu chí xuống 1.

### Gate 5 — Bám code (không bịa): qua — đã soi từng claim
Bảng đối chiếu (claim trong explain → anchor evidence gốc):

| Claim trong EXPLAIN.md | Bằng chứng | Verdict |
|---|---|---|
| cửa vào ổn định = hàm `run` / `resume` | A:6 `orchestrator/loop.py:run()`; A:47 `resume()` | khớp |
| `decompose gate` = `accept_decomposition`, chứng minh dừng μ(node), phát hiện RENAME/STUCK | A:20 (`accept.py:52-128`, Jaccard>0.80, STUCK) | khớp |
| chọn "bước sẵn-sàng-nhất" ngoài-cùng-trái, deps đã xong | A:17 `Tree.next_node()` leftmost pending, topo by depth,order | khớp |
| `delegation` = `DelegationManager.delegate`, luật quyền con ⊆ cha | A:26,28; B:6-ownership; brief invariant 4 | khớp |
| `chokepoint execute_tool`, LLM cũng là "tool" đi qua cửa này | B:6, B:27 "every capability call through one chokepoint"; B:44 metrics llm_calls; brief I2 (LLM/tool/… một cửa) | khớp |
| `tool.requested/completed` ghi xuống `events.jsonl` (event log) | B:21, B:44 EventLogger→events.jsonl | khớp |
| che (redact) secret ngay tại biên trước khi ra UI | B:39 `ui_payload` redacted before leaving emitter, 15 SECRET_KEYS | khớp |
| `judge_acceptance`: mỗi AC "đạt" phải trỏ ≥1 bằng chứng THẬT, không phải scaffolding; worker không tự ghi verdict | A:32; brief invariant 5 | khớp |
| FINISHED + SQLite = chân lý tua-lại (`resume`) | A:47; B:45 `langgraph.sqlite` = TRUTH | khớp |
| guards: `max_steps`, no-progress, repeat-decision N× → BLOCKED | A:34,37-41 | khớp |
| `AgentKernel` "nhân đông cứng" tách `KernelSession` "session sống" → 0 rò state | B:2 (kernel.py:76-89 / session.py:49-85); brief invariant 1 | khớp |
| Tools&Safety: `var/workspace/` jail + `PolicyGate` đóng-mặc-định (fail-closed) | B:38,41 | khớp |
| RAG (Qdrant) health-gated, ngoài đường tới FINISHED | B:34 (rag Qdrant, deferred v0); brief bounded context Knowledge (optional) | khớp |
| UI không được import `core/` | B:12 ARC-1 `UI ⊥ core/` | khớp |

Không tìm thấy claim treo hay tên bịa → gate 5 giữ 2, không rơi anchor 0.

### Bốn tiêu chí còn lại (2/3/6/7): đối chiếu nhanh
- **Chế độ (2)**: overview đủ ba nhịp làm-gì / cho-ai / vì-sao — anchor rubric "2" đạt.
- **Đủ ý (3)**: đủ đúng phạm vi overview L3, không thừa; "hai chốt đối nhau" là ý cốt lõi và đã nêu rõ.
- **Ranh giới (6)**: không dựng `.ai-understanding/` (chỉ ĐỌC nó), không liệt gap (chỉ trỏ sang `review/REVIEW.md`), không phán số phận file — đúng vai explain.
- **Kết (7)**: gợi ý đúng mức L3 + hand off `flow` — anchor "2".

---

## Cổng go/no-go của stage chấm (tự-quyết — không hỏi approval)

**Vai người duyệt:** Người chấm (độc lập) — đóng vai reviewer trung lập của skill `grade`, không phải tác giả bản explain.

**Quyết định:** **GO** — chấp nhận bản `EXPLAIN.md` là "ĐẠT gate, 14/14".

**Lý do:**
- Cả 3 cổng xương sống (1 Mức · 4 Lời văn · 5 Bám code) đều = 2; không cổng nào 0 → không rớt gate.
- Rủi ro cao nhất (bịa code) đã được khử bằng đối chiếu từng-claim với evidence gốc, không dựa cảm tính.
- Bản explain khớp gần như 1:1 với ví dụ mẫu L3 trong `explain/SKILL.md:202-226` (cùng cấu trúc zoom, cùng cách neo tên code).

**Phương án đã loại (và vì sao):**
- *Hạ tiêu chí 4 (Lời văn) xuống 1 vì mục "Tự soi" dài.* Loại — mục đó là phụ lục tách khỏi thân giải thích, không làm thân khó đọc; rubric anchor 1 dành cho "đọc được nhưng còn rườm" *ở phần giải thích*, không phải ở checklist bếp núc. Ghi lại thành đòn bẩy "SỬA TRƯỚC TIÊN" thay vì trừ điểm.
- *Hạ tiêu chí 3 (Đủ ý) vì không nhắc chi tiết resume/checkpoint nguyên tử.* Loại — ở mức overview L3, "SQLite = chân lý tua-lại" là đủ; đi sâu checkpoint nguyên tử là việc của L4+/`trace`, thừa so với phạm vi câu hỏi.
- *Nâng thành "cần sửa bắt buộc".* Loại — không có lỗi chặn nào; grade không sửa explain (đó là việc `tune`), chỉ chấm + chỉ đòn bẩy.

**Open-Q mang sang stage sau (nếu chuỗi chạy tiếp):**
- OQ-G1: Bản explain nêu "`review/REVIEW.md` (12 gap, 3 Critical)" và "`frame/slice-01-...`". Grade KHÔNG kiểm nội dung hai file đó (ngoài phạm vi chấm explain) — nếu cần bảo đảm con số 12 gap / 3 Critical đúng, đó là việc đối chiếu ở stage `traceability`, không phải ở đây.
- OQ-G2: Điểm này chấm cho *đúng một bản*. Muốn dùng làm thước cho `tune` (so nhiều biến thể), cần chạy lại grade trên từng biến thể với cùng fixture rồi loại bản rớt gate trước, xếp theo tổng sau.
