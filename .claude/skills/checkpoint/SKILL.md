---
name: checkpoint
description: "Cổng kiểm một bước: xét artifact vừa sinh có đạt Định-nghĩa-Xong không (nằm đúng folder theo folders.md + đủ mục bắt buộc của giai đoạn + qua rubric nếu có), rồi cấp một phiếu PASS/FAIL vào progress/checkpoints/<task-id>.md. KHÔNG đụng đồ thị task, KHÔNG sửa artifact — chỉ kiểm và ra phán quyết kèm lý do cụ thể. Dùng khi: 'kiểm bước này', 'artifact này đủ chưa', 'checkpoint T-02', 'nghiệm thu bước', ngay trước khi progress lật một task sang done. Chỉ checkpoint được ghi phiếu; progress đọc phiếu để quyết có mở khóa nhánh sau không."
---

# Checkpoint — Phiếu đạt cho từng bước, gác Định-nghĩa-Xong

`checkpoint` là người gác cổng chất lượng ở cuối mỗi bước. Một task chỉ thực sự "xong" khi có artifact ĐỦ TỐT, không chỉ có artifact tồn tại. `checkpoint` kiểm điều đó và để lại một phiếu máy-đọc-được; `progress` dựa vào phiếu để lật `done` và mở nhánh sau. Tách vai để không ai vừa làm vừa tự chấm mình.

Ranh giới:
- `checkpoint` cấp phiếu (`progress/checkpoints/<id>.md`). `progress` lật task. Hai chủ, hai file, một chiều dữ liệu: phiếu → progress đọc → mở khóa.
- `review` soi CODE tìm gap/edge case; `grade` chấm chất lượng một bản explain. `checkpoint` xét một ARTIFACT giai đoạn có đủ mục Định-nghĩa-Xong chưa — nhẹ hơn, theo checklist cố định của giai đoạn. Việc cần soi code sâu thì checkpoint tiến cử `/review`, không làm thay.

## Quy tắc bắt buộc

- **Chỉ kiểm, không sửa.** Thấy thiếu → ghi rõ thiếu gì trong phiếu, trả về cho owner sửa. Không tự viết thêm vào artifact.
- **Phán quyết có lý do.** `FAIL` phải nêu chính xác mục nào thiếu; `PASS` liệt kê các mục đã đạt. Không PASS/FAIL trống.
- **Không đụng progress.json.** Không lật task, không dời con trỏ — đó là `progress`.
- **Kiểm theo giai đoạn.** Mỗi giai đoạn có checklist mục bắt buộc riêng trong `constitution/definition-of-done.md`. Dùng đúng checklist của `giai_doan` task đó.
- **Chấm chất lượng là ADVISORY.** Nếu owner của giai đoạn có rubric (`.claude/skills/<owner>/rubric.md`), checkpoint chạy `grade` để lấy điểm chất lượng và đính vào phiếu — nhưng điểm chỉ THAM KHẢO. Verdict PASS/FAIL vẫn do checklist cấu trúc (đủ mục + đúng path) quyết; một backbone-fail của grade là **cảnh báo to**, KHÔNG tự lật FAIL và KHÔNG ký thay user. Chất lượng sâu là thứ user cân khi ký (giữ warm-never-brick + user-giữ-GO).
- **Cổng đậm cần chữ người.** Live slice (GĐ8) và release (GĐ13) là cổng GO/NO-GO — `checkpoint` chuẩn bị đủ để ký, nhưng verdict cuối chờ user ký, ghi `PASS (chờ ký)` cho tới khi có.

## Bước 0 — Nạp ngữ cảnh

Đọc `constitution/definition-of-done.md` (checklist theo giai đoạn) + `progress.json` (lấy task theo id: `artifact` path, `giai_doan`, `owner`).

## Bước 1 — Kiểm artifact tồn tại đúng chỗ

```bash
ls projects/<key>/<artifact-path> 2>/dev/null && echo "CÓ" || echo "THIẾU"
```
`THIẾU` → verdict `FAIL` ngay, lý do "artifact chưa nằm ở <path>".

## Bước 2 — Kiểm mục bắt buộc

Mở artifact, đối chiếu checklist của `giai_doan` (từ `definition-of-done.md`). Ví dụ:
- Problem (1–4): có ai đau + đau ở đâu? có success metric đo được? có scope in/out?
- Domain (5): entity có identity+lifecycle? rule bất biến? event chính? ranh giới context?
- Architecture (6)/Stack (7): có quyết định + rationale + ≥1 rejected_alternative?
- Contract (10): interface đủ để hai bên build độc lập (endpoint/field/kiểu hoặc chữ ký hàm)?
- Build (11): artifact code trỏ đúng path? gắn được về contract + AC?

Mỗi mục đánh ✓ (đạt) hoặc ✗ (thiếu, nêu cụ thể).

## Bước 2b — Chấm chất lượng (advisory, nếu có rubric)

Nếu `.claude/skills/<owner>/rubric.md` tồn tại (owner = `owner` của task), chạy `grade <owner>` trên artifact để lấy: **TỔNG điểm**, **GATE (đạt/rớt + tiêu chí nào)**, **đòn bẩy sửa-trước-tiên**. Đính cả ba vào phiếu.

Đây là THAM KHẢO cho user, KHÔNG phải cổng: điểm thấp / backbone-fail → in cảnh báo to trong phiếu, nhưng verdict cấu trúc Bước 2 vẫn là cái quyết PASS/FAIL. Không có rubric cho giai đoạn đó → bỏ qua bước này, ghi "grade: n/a".

## Bước 3 — Cấp phiếu

Ghi `projects/<key>/progress/checkpoints/<task-id>.md`. **Verdict sống ở FRONT-MATTER máy-đọc
ở ĐẦU phiếu (Đợt 3)** — đây là chỗ DUY NHẤT `advance.py` đọc để lật `done`, không đoán từ prose:
```markdown
---
verdict: PASS | FAIL | PASS_PENDING_SIGNOFF
signed_by:
artifact_sha256: <sha256 của artifact lúc chấm — bật verdict-hash-binding>
---
# Phiếu checkpoint — <task-id>
- Task: <việc>
- Giai đoạn: <giai_doan>
- Artifact: <path>
- Kiểm lúc: <ISO 8601>

## Checklist (<giai_doan>)
- [x] <mục 1 đạt>
- [x] <mục 2 đạt>
- [ ] <mục thiếu — nêu cụ thể>

## Grade (advisory): <TỔNG/max · GATE đạt|rớt: … · n/a nếu không có rubric>
Sửa trước tiên: <đòn bẩy lớn nhất, hoặc "—">

## Verdict (đọc-cho-người — nguồn máy là front-matter): PASS | FAIL
Lý do: <1–2 câu>
Nếu FAIL, cần bổ sung: <danh sách cụ thể để owner sửa>
```

- `verdict` ∈ enum đóng. Lấy `artifact_sha256` = `python3 -c "import hashlib;print(hashlib.sha256(open('<artifact>','rb').read()).hexdigest())"` (hoặc `bin/sign_gate.py` cho cổng đậm). Sửa artifact sau khi chấm → sha lệch → `advance.py` báo STALE, KHÔNG lật.
- **Cổng đậm (GĐ8 live-slice · GĐ13 release):** verdict = `PASS_PENDING_SIGNOFF`, `signed_by` để RỖNG. `advance.py` sẽ KHÔNG lật cho tới khi Người duyệt tự điền `signed_by` (AI KHÔNG điền thay — xem CLAUDE.md Đợt 2). Cổng thường: `signed_by` có thể để rỗng, verdict `PASS` là đủ.

In khối:
```
═══ CHECKPOINT — <task-id>: <PASS|FAIL> ═══
Artifact: <path>
Đạt: <n>/<m> mục   |   Thiếu: <mục hoặc "—">
Grade (tham khảo): <TỔNG/max · GATE …  |  n/a>
→ PASS: chạy `python3 bin/advance.py <task-id>` để lật done (fail-closed, đọc front-matter) + mở nhánh kế
→ FAIL: owner <skill> sửa <thiếu gì> rồi /checkpoint <task-id> lại
════════════════
```

> **Lật `done` KHÔNG bằng tay.** `/progress` (ADVANCE) và người dùng lật task qua
> `bin/advance.py <task-id>` — script đọc front-matter phiếu, chỉ `verdict: PASS` + sha khớp
> mới lật, ghi atomic. Đây là chỗ vá vết T-06 ("PASS chờ ký" mà progress.json đã done).

## Vì sao vai này tách riêng

Yêu cầu project: "mỗi bước xong phải có artifact". Nếu skill làm việc tự đánh dấu xong, "xong" dễ thành lời kể. Tách `checkpoint` khỏi `progress` biến "xong" thành một phiếu có checklist — `progress` không bao giờ mở nhánh song song (BE/FE) khi contract chưa có phiếu PASS.
