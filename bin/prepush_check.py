#!/usr/bin/env python3
"""prepush_check.py — BACKSTOP tầng transport cho các gate push.

Vết: gate in-session (push_boundary_guard, gate_ship) chạy ở PreToolUse:Bash — chỉ soi
lệnh Bash mà MODEL gõ. Đường vòng: `sh -c 'git push'`, alias, script, hoặc push từ
terminal tay / công cụ khác → in-session hook KHÔNG fire. Git pre-push thì CHẠY CHO MỌI
push dù spawn kiểu gì → đây là lưới cuối, re-áp ĐÚNG luật của hai hook kia (import lại,
không chép lệch chuẩn) ngay tại điểm nội-dung rời máy.

Đọc stdin pre-push (`<local_ref> <local_sha> <remote_ref> <remote_sha>` mỗi dòng), với mỗi
ref sắp push:
  · SECRET  — quét added-line trong range sắp push (push_boundary_guard._scan/_added_lines)
  · SHIP    — ship.json GO đổi trong range → gate_ship._evaluate_ship (chữ ký/artifact/uat)
  · FORCE   — non-fast-forward vào nhánh bảo vệ (main/master)
  · DELETE  — xoá nhánh bảo vệ
Vi phạm → exit 1, git huỷ push. Break-glass: `SKILLSH_PREPUSH=off` hoặc `git push --no-verify`
(git bỏ qua hook native). FAIL-OPEN khi hook tự lỗi (không brick push solo vì bug).

Presence gate, tamper-visible: cùng bản chất honesty như gate_ship (xem gatelib).
"""
import os
import subprocess
import sys

_ZERO = "0" * 40


def _root():
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                       capture_output=True, text=True)
    return r.stdout.strip() or os.getcwd()


def _import_gates(root):
    sys.path.insert(0, os.path.join(root, ".claude", "hooks"))
    sys.path.insert(0, os.path.join(root, "bin"))
    import gate_ship as gs            # noqa: E402
    import push_boundary_guard as pbg  # noqa: E402
    return pbg, gs


def _log(root, extra):
    r = subprocess.run(["git", "-C", root, "log", "--no-color", "--max-count=500"] + extra,
                       capture_output=True, text=True, timeout=60)
    return r.stdout if r.returncode == 0 else ""


def _range_args(local_sha, remote_sha):
    """git-log args cho các commit sắp push: range nếu nhánh đã có, else new-only."""
    if not remote_sha or set(remote_sha) <= {"0"}:
        return [local_sha, "--not", "--remotes"]     # nhánh mới → chỉ commit chưa lên remote nào
    return ["%s..%s" % (remote_sha, local_sha)]


def _is_ancestor(root, a, b):
    return subprocess.run(["git", "-C", root, "merge-base", "--is-ancestor", a, b]).returncode == 0


def _branch(ref):
    return ref[len("refs/heads/"):] if ref.startswith("refs/heads/") else ref


def _fail(reason):
    sys.stderr.write("pre-push backstop: " + reason +
                     "\n(break-glass: SKILLSH_PREPUSH=off hoặc git push --no-verify)\n")
    sys.exit(1)


def check_ref(root, pbg, gs, local_ref, local_sha, remote_ref, remote_sha):
    prot = _branch(remote_ref) in pbg._PROTECTED
    # DELETE (local_sha toàn 0) vào nhánh bảo vệ
    if set(local_sha) <= {"0"}:
        if prot:
            _fail("từ chối XOÁ nhánh bảo vệ %s — không lấy lại được." % _branch(remote_ref))
        return
    # FORCE / non-ff vào nhánh bảo vệ
    if prot and remote_sha and set(remote_sha) > {"0"} and not _is_ancestor(root, remote_sha, local_sha):
        _fail("từ chối force-push/rewrite nhánh bảo vệ %s (non-fast-forward)." % _branch(remote_ref))

    rng = _range_args(local_sha, remote_sha)
    # SECRET — quét added-line trong range (đúng bộ pattern + exclude của push_boundary_guard)
    diff = _log(root, rng + ["-p"])
    hits = pbg._scan(pbg._added_lines(diff))
    if hits:
        _fail("secret trong commit sắp push (%s). Gỡ khỏi commit (rotate nếu là thật)."
              % ", ".join(hits))
    # SHIP — ship.json GO đổi trong range → đúng luật gate_ship
    files = set()
    for line in _log(root, rng + ["--name-only", "--pretty=format:"]).splitlines():
        p = line.strip()
        if p and gs._SHIP_RE.search(p):
            files.add(p)
    for ship_rel in sorted(files):
        reason, adv = gs._evaluate_ship(root, ship_rel)
        for a in adv:
            sys.stderr.write("[advisory] pre-push: %s\n" % a)
        if reason:
            _fail(reason.split("\n")[0] + " (chi tiết: bin/check_pipeline.py %s)" % ship_rel)


def main():
    if os.environ.get("SKILLSH_PREPUSH", "on").lower() in ("off", "0", "false"):
        sys.exit(0)
    try:
        root = _root()
        pbg, gs = _import_gates(root)
    except Exception:
        sys.exit(0)                    # không dựng được môi trường kiểm → fail-OPEN
    try:
        for line in sys.stdin.read().splitlines():
            parts = line.split()
            if len(parts) != 4:
                continue
            check_ref(root, pbg, gs, *parts)
    except SystemExit:
        raise                          # _fail exit 1 phải thoát đúng
    except Exception:
        sys.exit(0)                    # bug hook → fail-OPEN
    sys.exit(0)


if __name__ == "__main__":
    main()
