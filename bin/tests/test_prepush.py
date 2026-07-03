#!/usr/bin/env python3
"""test_prepush.py — test THẬT cho git pre-push backstop (repo tạm + bare remote).

Chạy: python3 bin/tests/test_prepush.py   → exit 0 nếu 0 đỏ.
Dựng repo git tạm + remote bare, cài .githooks/pre-push (core.hooksPath), rồi push THẬT —
kể cả `sh -c 'git push'` để chứng minh backstop bắt được vector evasion mà PreToolUse hook
in-session bỏ lọt. Không đụng repo skillsh thật.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_PASS, _FAIL = 0, 0


def check(name, cond):
    global _PASS, _FAIL
    if cond:
        _PASS += 1; print("  ✓ %s" % name)
    else:
        _FAIL += 1; print("  ✗ %s" % name)


def git(work, *args, env=None):
    e = dict(os.environ, **(env or {}))
    return subprocess.run(["git", "-C", str(work), *args], capture_output=True, text=True, env=e)


def setup(tmp):
    """Dựng work-repo (có gate files + hook) + bare remote, commit baseline, push main."""
    bare = Path(tmp) / "origin.git"
    work = Path(tmp) / "work"
    subprocess.run(["git", "init", "--bare", "-b", "main", str(bare)], capture_output=True)
    subprocess.run(["git", "init", "-b", "main", str(work)], capture_output=True)
    for rel in ["bin/gatelib.py", "bin/prepush_check.py",
                ".claude/hooks/push_boundary_guard.py", ".claude/hooks/gate_ship.py",
                ".githooks/pre-push"]:
        dst = work / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(_ROOT / rel, dst)
    os.chmod(work / ".githooks" / "pre-push", 0o755)
    git(work, "config", "user.email", "t@t"); git(work, "config", "user.name", "t")
    git(work, "config", "core.hooksPath", ".githooks")
    git(work, "remote", "add", "origin", str(bare))
    (work / "README.md").write_text("# demo\n", encoding="utf-8")
    git(work, "add", "-A"); git(work, "commit", "-m", "baseline")
    r = git(work, "push", "-u", "origin", "main")
    return work, r.returncode


def commit(work, files: dict, msg="c"):
    for rel, content in files.items():
        p = work / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    git(work, "add", "-A"); git(work, "commit", "-m", msg)


def drop_last(work):
    git(work, "reset", "--hard", "HEAD~1")


def make_ship(work, signed=True):
    """Commit pipeline/ship.json GO (+ artifact); ký hợp lệ nếu signed."""
    (work / "pipeline").mkdir(exist_ok=True)
    (work / "pipeline" / "ship.md").write_text("# ship\n", encoding="utf-8")
    ship = {"quyet_dinh": "go", "artifact_path": "pipeline/ship.md"}
    (work / "pipeline" / "ship.json").write_text(json.dumps(ship), encoding="utf-8")
    if signed:
        sha = hashlib.sha256((work / "pipeline" / "ship.json").read_bytes()).hexdigest()
        (work / "pipeline" / "ship.json.sign.json").write_text(
            json.dumps({"verdict": "go", "artifact_sha256": sha, "signed_by": "human"}),
            encoding="utf-8")
    git(work, "add", "-A"); git(work, "commit", "-m", "ship")


def main():
    print("Đợt 3 · git pre-push backstop — test (repo tạm + bare remote)")
    akia = "AKIA" + "I" * 16                      # dựng động, tránh literal secret trong source

    with tempfile.TemporaryDirectory() as tmp:
        work, base_rc = setup(tmp)
        check("baseline push (sạch) → OK", base_rc == 0)

        # SECRET
        commit(work, {"config.py": "KEY = '%s'\n" % akia}, "add secret")
        check("push commit chứa secret → BỊ CHẶN", git(work, "push", "origin", "main").returncode != 0)
        # evasion: git gọi qua `sh -c` — pre-push vẫn chạy
        ev = subprocess.run(["sh", "-c", "git -C '%s' push origin main" % work],
                            capture_output=True, text=True)
        check("`sh -c 'git push'` (evasion) → VẪN BỊ CHẶN", ev.returncode != 0)
        check("--no-verify → BỎ QUA hook (git native break-glass)",
              git(work, "push", "--no-verify", "origin", "main").returncode == 0)
        # đã push secret bằng --no-verify; đưa remote về sạch cho các ca sau
        git(work, "reset", "--hard", "HEAD~1")
        git(work, "push", "--no-verify", "--force", "origin", "main")

        # SHIP GO chưa ký
        make_ship(work, signed=False)
        check("push ship.json GO CHƯA KÝ → BỊ CHẶN", git(work, "push", "origin", "main").returncode != 0)
        drop_last(work)

        # SHIP GO đã ký hợp lệ
        make_ship(work, signed=True)
        check("push ship.json GO ĐÃ KÝ (sha khớp) → OK", git(work, "push", "origin", "main").returncode == 0)

        # SKILLSH_PREPUSH=off
        commit(work, {"config2.py": "KEY = '%s'\n" % akia}, "secret2")
        check("SKILLSH_PREPUSH=off → BỎ QUA (env break-glass)",
              git(work, "push", "origin", "main", env={"SKILLSH_PREPUSH": "off"}).returncode == 0)
        git(work, "reset", "--hard", "HEAD~1")
        git(work, "push", "--no-verify", "--force", "origin", "main")

        # thay đổi thường
        commit(work, {"README.md": "# demo v2\n"}, "normal")
        check("push thay đổi thường → OK", git(work, "push", "origin", "main").returncode == 0)

        # force-push nhánh bảo vệ
        git(work, "commit", "--amend", "-m", "rewrite")   # đổi HEAD → non-ff
        check("force-push (non-ff) nhánh main → BỊ CHẶN",
              git(work, "push", "--force", "origin", "main").returncode != 0)

    print("\n%d xanh · %d đỏ" % (_PASS, _FAIL))
    return _FAIL


if __name__ == "__main__":
    sys.exit(main())
