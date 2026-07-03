#!/usr/bin/env python3
"""config_write_guard.py — gác các FILE-GATE (guard the guards).

Đợt 3 của skillsh. Vết: "một chủ một file" mới chỉ là chỉ-dẫn cho model; `.claude/hooks/*`
và chính `.claude/settings.json` tự sửa được trong phiên → một agent "tiện tay" có thể TẮT
gate rồi làm bậy, hoặc sửa hook để nhả. Hook này chặn MỌI đường ghi (Write/Edit/MultiEdit +
shell-write) vào tập hằng:
    .claude/settings.json · .claude/settings.local.json · .claude/hooks/**

Đây là những file mà FLOW THƯỜNG (skill chạy việc) KHÔNG bao giờ ghi — chỉ người-cấu-hình
ghi. Nên chặn cứng in-session là đúng phạm trù (khác progress.json/phiếu/current.json là
thứ owner-skill PHẢI ghi — KHÔNG gác ở đây).

Break-glass: sửa gate là việc CÓ chủ đích của người → làm bằng editor NGOÀI phiên, hoặc
SKILLSH_CONFIG_GUARD=off. Chống traversal (resolve realpath). Fail-closed khi khớp; FAIL-OPEN
khi hook tự lỗi (không brick phiên vì bug). Tamper-VISIBLE: sửa gì cũng lộ trong git diff.
"""
import json
import os
import re
import sys
from pathlib import Path

ENABLED = os.environ.get("SKILLSH_CONFIG_GUARD", "on").lower() not in ("off", "0", "false")


def _project_root():
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parents[2]


def _guarded(root):
    return [
        (root / ".claude" / "settings.json").resolve(),
        (root / ".claude" / "settings.local.json").resolve(),
        (root / ".claude" / "hooks").resolve(),      # thư mục → gác cả cây con
    ]


def _is_guarded(path_abs, guards):
    p = Path(path_abs).resolve()
    for g in guards:
        if p == g:
            return True
        try:                                         # p nằm dưới thư mục hooks/
            p.relative_to(g)
            return True
        except ValueError:
            continue
    return False


# shell-write: đích ghi nằm trong .claude/hooks | .claude/settings*  (coarse, chấp nhận
# over-block một lệnh ĐỌC qua redirect — dùng Read tool).
_WRITE_REGION_RE = re.compile(
    r"(?:>>?|tee\b|dd\b[^|;&]*of=|sed\b[^|;&]*-i|cp\b|mv\b|install\b|truncate\b)[^|;&]*"
    r"\.claude/(?:hooks/|settings(?:\.local)?\.json)")


def _block(reason):
    sys.stderr.write("config-write-guard: " + reason + "\n")
    sys.exit(2)


def main():
    if not ENABLED:
        sys.exit(0)
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        sys.exit(0)
    if not isinstance(data, dict):
        sys.exit(0)
    try:
        root = _project_root()
        guards = _guarded(root)
        tool = data.get("tool_name")
        ti = data.get("tool_input") or {}
        msg = ("đây là FILE-GATE (settings.json / .claude/hooks/*) — flow thường không ghi "
               "vào đây. Sửa gate là việc có chủ đích: dùng editor NGOÀI phiên, hoặc "
               "SKILLSH_CONFIG_GUARD=off. (mọi sửa vẫn lộ trong git diff.)")
        if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
            fp = ti.get("file_path") or ti.get("notebook_path")
            if isinstance(fp, str) and fp:
                ap = fp if os.path.isabs(fp) else str(root / fp)
                if _is_guarded(ap, guards):
                    _block("chặn ghi %s — %s" % (fp, msg))
        elif tool == "Bash":
            cmd = ti.get("command")
            if isinstance(cmd, str) and _WRITE_REGION_RE.search(cmd):
                _block("chặn shell-write vào file-gate — %s" % msg)
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)  # hook tự lỗi → FAIL-OPEN
    sys.exit(0)


if __name__ == "__main__":
    main()
