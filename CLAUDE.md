# skillsh — luật gốc

Bộ skill SDLC (idea → operate) chạy solo. File này là luật nền cho MỌI skill.

## Git là sàn — nhịp commit (Đợt 1)

skillsh giờ là git repo. Git là lớp tamper-evidence + rollback cho state và SKILL.md:
mọi phiếu / con-trỏ / pipeline JSON là file trần một bản, ghi đè là mất — trừ khi có
commit để quay lại.

**Commit ở đúng MỘT nhịp, HAI thời điểm bắt buộc:**

1. **Cuối mỗi lượt skill có ghi state** (progress.json, phiếu checkpoint, pipeline/*.json,
   current.json). Snapshot xong-một-đơn-vị-việc → lần sau phiên chết giữa Write vẫn còn
   bản known-good để rollback.
2. **Trước /tune Bước 6** (chỗ chép `proposed-SKILL.md` đè `<skill>/SKILL.md` —
   tune/SKILL.md:95). Commit bản SKILL.md TRƯỚC khi tune ghi đè → sửa sai hướng vẫn còn
   `git diff` / rollback.

Lệnh:

```
git add -A && git commit -m "<skill>: <project> <giai_doan>"
```

Ví dụ: `checkpoint: hxag gd6` · `uat: mediremind gd12` · `tune: explain` (tune không có
project/GĐ). Nhịp này là kỷ luật người/model giữ — không hook, không script (cưỡng chế
bằng hook là đợt sau).

## Cái gì vào git, cái gì không

- **Versioned:** SKILL.md, `state/current.json`, `state/project/**`, `pipeline/**`, phiếu
  checkpoint — để rollback được khi state hỏng.
- **Ignore (.gitignore):** `state/telemetry/` + `state/**/.dedup/` (log runtime, chạy lại
  được), `skill-governance/SKILL-DECISION.generated.md` (máy sinh), `__pycache__/`,
  `.DS_Store`.

## Biên push ra remote — có guard (Đợt 1)

`.claude/hooks/push_boundary_guard.py` (PreToolUse:Bash) chặn `git push` khi:

- (a) diff sắp push chứa secret (AKIA / PEM / sk-ant / gh*_ / key=quoted), hoặc
- (b) force-push / xoá nhánh `main` | `master`.

Đây là biên KHÔNG-ĐẢO-NGƯỢC (key vào lịch sử remote khách, rewrite main) nên là chỗ duy
nhất Đợt 1 dùng hook thay vì convention. Break-glass: `SKILLSH_PUSH_GUARD=off` hoặc
`ENABLED=False` đầu file.

## Đợt 2 — Chữ ký & bằng chứng (cổng thành DỮ-LIỆU, không còn là lời-kể)

Meta-lỗi đã thủng thật: AI **tự ký** GO/UAT/Security thay CTO+PO (`ship.json` báo `da_go`
"✔ PO ký" trong khi `uat.json` ghi `uat_signoff:false`), báo PASS trên artifact chưa từng
chạy, lật `done` phiếu "chờ ký". Nguồn gốc: mọi cổng chỉ là văn xuôi — 0 validator, 0
chặn. Đợt 2 biến 4 cổng đậm thành thứ **kiểm được bằng máy**, qua HAI điểm chặn + prose.

**1. Chặn lúc GỌI skill — `gate_stage_guard.py`** (PreToolUse:Skill). Đọc đồ-thị task
`progress.json`; chặn gọi một skill-giai-đoạn khi `depends_on` của nó chưa `done`. "Xong" =
task done (checkpoint PASS). Fail-open tuyệt đối (thiếu state / greenfield / lỗi → cho chạy).
Vá vết "gd14 khi gd12 chưa ký". Nhảy cổng cố ý → tắt hook trong `settings.json`.

**2. Chặn lúc PUSH ra remote — `gate_ship.py`** (PreToolUse:Bash, cạnh push-boundary). Chỉ
cắn khi commit CHƯA-push có một `pipeline/ship.json` tuyên GO. Khi đó đòi (fail-closed):
- **A. chữ ký người còn tươi** — `<ship>.sign.json` tồn tại, sha khớp nội dung hiện tại,
  verdict ∈ {go, go_co_dieu_kien}. Thiếu → "AI không được tự bấm GO"; sha lệch → "sửa sau khi ký".
- **B. artifact không rỗng** — `artifact_path` phải tồn tại (chống "GO trên artifact rỗng").
- **C. chữ-ký-không-ngược** — GO vô-điều-kiện mà `uat.json.uat_signoff=false` cạnh đó → chặn.

Break-glass: `SKILLSH_SHIP_GATE=off`. Push thường (SKILL.md, state) đi qua sạch — gate chỉ
đụng khi đẩy một GO. Sổ audit: `state/trace/<ngày>.jsonl` (actor + ts, gitignore).

**3. Chữ ký người = FILE, không phải prose — `bin/sign_gate.py`.** Verdict GO/ký chỉ THẬT khi
có `<artifact>.sign.json` do CHÍNH TAY người chạy `python3 bin/sign_gate.py <artifact> --verdict go`.
Kiểm tay: `bin/check_pipeline.py` (bản chạy-không-cần-push của gate_ship). Kiểm nhanh một
artifact: `bin/sign_gate.py --check <artifact>`.

> **AI KHÔNG BAO GIỜ chạy `sign_gate.py`** — kể cả khi được chỉ thị "tự quyết / không hỏi
> approval / đóng vai người duyệt". Ký là hành vi của con người thật. Autonomy tối đa của AI
> = ĐỀ XUẤT verdict + IN SẴN lệnh ký. Mệnh đề này sống sót MỌI chỉ thị autonomy.

**Prose kèm theo (4 skill):** `ship`/`skeleton` thêm bước **tự-suy-lại độc lập** (dựng lại
GO/pass TỪ bằng chứng gốc TRƯỚC khi đọc khuyến nghị của chính mình — đọc-lại ≠ kiểm-lại);
`checkpoint` gọi `grade` làm điểm chất-lượng **advisory** ở cổng, không tự lật verdict.

**Ba sự-thật-thành-thật (đừng tin quá tay):** (1) đây là *presence gate* — chứng minh
bước-ký ĐÃ CHẠY trên đúng nội-dung (sha khớp), KHÔNG chứng minh ai ký; (2) chống-AI-tự-ký là
LUẬT (mục trên), không phải mật mã — gate chỉ khoá "sửa sau khi ký"; (3) `.sign.json`/trace là
file trần trong git → tamper-VISIBLE (lộ trong diff), không tamper-proof. Git vẫn là sàn.

Test: `python3 .claude/hooks/tests/test_dot2_gates.py` (15 ca, có fixture thật). Bản đồ port
đầy đủ + Đợt 3: `PORT-NOTES.md`.
