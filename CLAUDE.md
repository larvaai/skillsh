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
