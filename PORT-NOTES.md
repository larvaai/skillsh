# PORT-NOTES — port lớp enforcement của sdlc-harness vào skillsh

Nhánh `feat/dot2-sign-evidence-gate`. Đây là bản ghi *port cái gì · từ đâu · vì sao · còn gì*.
Bản đồ 105-skill đầy đủ: `harness-skills-port-map.html`. Chẩn đoán gốc: `rigor-gap-...report.md`.

## Vì sao port lớp enforcement TRƯỚC (không phải skill)

So sánh brainstorm/plan/cook harness ↔ suite skillsh cho ra: 0 gap tuyệt đối về Ý TƯỞNG —
suite đã có đủ chặng (idea→operate). Cái thiếu là **tầng THỰC THI**: cổng chỉ là văn xuôi
trong SKILL.md, kỷ luật = mức kiên nhẫn của CTO lúc mệt. Đúng thứ hai review đã bắt thủng
thật (`ship.json` GO tự khai; `uat_signoff:false` mà project ở gd14). Nên port giá trị nhất
= **bộ máy cưỡng chế**, không phải chép lại skill đã có.

## 5-mảnh hạt nhân harness → ánh xạ vào skillsh

Bản đồ port kết luận: giữ được "evidence-gated pipeline" cần 5 mảnh không tách rời. Trạng thái:

| # | Mảnh hạt nhân (harness) | skillsh Đợt 2 | Trạng thái |
|---|---|---|---|
| 1 | Vòng xương sống có cổng | pipeline idea→operate + `gate_stage_guard` chặn nhảy cổng theo `progress.json` | ✅ |
| 2 | Hợp đồng artifact (schemas/artifact-*.json) | enum verdict đóng + hình-dạng `ship.json`/`uat.json`/`<x>.sign.json`; validator `check_pipeline.py` (thay JSON-Schema nặng — đúng downscope rigor-gap #14) | ✅ (nhẹ) |
| 3 | Gate enforcement đọc artifact trước bước "hard" (`gate_stage.py`) | `gate_ship.py` (PreToolUse:Bash) tại biên push — **PHẢI viết lại theo cơ chế chặn của harness đích, không bê được**; skillsh dùng Claude Code hook nên chặn được thật (exit 2 / permissionDecision=deny) | ✅ |
| 4 | Tam-phân hạng hook (telemetry/nudge/compliance) | telemetry `track_skill_invocation` · compliance `push_boundary_guard`+`gate_ship`+`gate_stage_guard` (fail-closed khi dương tính, fail-open khi lỗi nội bộ) | ✅ |
| 5 | State append-only có actor+ts | `state/trace/<ngày>.jsonl` (gitignore, như telemetry) | ✅ |

Không bê nguyên `gate_stage.py` của harness: nó đan chặt `hook_runtime`/`artifact_check`/
`stage_detector`/`harness_paths`/`guard_policy` (port_effort=high). skillsh port **ESSENCE**
theo phong cách tự-chứa của `push_boundary_guard` (stdlib, break-glass, fail-open-khi-bug).

## Đã thêm trong Đợt 2

| File | Vai | Chạy bởi |
|---|---|---|
| `bin/gatelib.py` | lõi dùng chung (sha, whoami, trace, atomic, read_sign) | các CLI |
| `bin/sign_gate.py` | biến chữ ký người → `<artifact>.sign.json` (+ `--check`) | **CON NGƯỜI** |
| `bin/check_pipeline.py` | audit ship.json chạy-tay (bản không-cần-push của gate) | người / skill |
| `.claude/hooks/gate_ship.py` | cổng bằng-chứng tại `git push` (tự-chứa) | hook PreToolUse:Bash |
| `.claude/hooks/gate_stage_guard.py` | chặn nhảy cổng theo đồ-thị task | hook PreToolUse:Skill |
| `.claude/hooks/tests/test_dot2_gates.py` | 15 ca test (có fixture thật) | `python3 …` |
| prose: `ship`/`skeleton`/`checkpoint`/`grade` SKILL.md | tự-suy-lại độc lập + grade-advisory | model |

Wiring: `.claude/settings.json` — Bash: push_boundary + gate_ship · Skill: track + gate_stage_guard.

## Ba sự-thật-thành-thật (copy NGUYÊN VĂN — để người mới không tin quá tay)

1. **Presence gate, không phải authentication.** Cổng chứng minh bước-ký ĐÃ CHẠY trên đúng
   nội-dung artifact (sha khớp), KHÔNG chứng minh AI hay người ký. `signed_by` là attribution.
2. **Chống-AI-tự-ký là LUẬT, không phải mật mã.** Nằm ở CLAUDE.md + prose skill ("AI không
   chạy sign_gate.py"). Cổng máy chỉ khoá được "sửa artifact SAU khi ký" (sha lệch → STALE).
3. **Tamper-VISIBLE, không tamper-proof.** `.sign.json` + trace là file trần trong git — sửa
   lộ trong diff, không chống sửa. Git là sàn tamper-evidence (Đợt 1), cổng đứng trên sàn đó.

Rủi ro port lớn nhất (từ bản đồ): nếu harness đích KHÔNG có hook PreToolUse chặn ở tool-call
thì lớp compliance sụp thành advisory → phải dời enforcement sang git pre-push/CI. skillsh
CÓ hook nên chặn được in-session; backstop transport (git pre-push) là Đợt 3.

## Đợt 3 — chưa làm (theo rigor-gap, đã downscope)

- **checkpoint-verdict-advance** (`advance.py`) — front-matter YAML {verdict, signed_by} trong
  phiếu .md; `advance.py` fail-closed thay hand-edit `progress.json`; chỉ `verdict==PASS` mới
  flip `done`. (Cần migrate phiếu sang front-matter trước — đổi prose checkpoint/progress.)
- **git pre-push backstop** — cùng luật gate_ship nhưng ở tầng transport, bắt evasion
  `sh -c 'git push'` mà hook in-session lọt.
- **one-owner-write-guard** — hook mini gác {`.claude/settings.json`, `.claude/hooks/*`}.
- **resume-pending-gates** — resume đọc `pipeline/*.json`, `cho_duyet:true` → in "ĐANG CHỜ KÝ",
  không tiến cử skill sau cổng.
- **bash-safety-floor**, **secret-read-guard** (permissions.deny cho `.env`/`*.pem`/`*.key`).

## Kiểm nhanh

```bash
python3 .claude/hooks/tests/test_dot2_gates.py     # 15 ca, phải 0 đỏ
python3 bin/check_pipeline.py                        # audit mọi ship.json trong repo
python3 bin/sign_gate.py --check rebuild-hex-agent/pipeline/ship.json
```
