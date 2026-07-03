#!/usr/bin/env python3
"""push_boundary_guard.py — PreToolUse(Bash) guard cho biên KHÔNG-ĐẢO-NGƯỢC ra remote.

Chỉ soi lệnh `git push` (chỗ nội dung rời khỏi máy). Chặn hai thứ không lấy lại được:
  (a) secret rò trong diff sắp push — 5 pattern precision-first (AKIA, PEM, sk-ant,
      gh*_, key=quoted-value); quét added-line của commit CHƯA lên remote, bỏ qua
      tests/docs/fixtures.
  (b) history-rewrite / xoá nhánh bảo vệ — force-flag hoặc refspec `+`/`:`/--delete
      nhắm main|master.

Self-contained: stdlib, KHÔNG import hook_runtime/yaml/stage_detector. skillsh push
repo NGOÀI (repo khách trong /frame) nên root repo resolve từ `git -C <dir>` trong
lệnh, hoặc `cwd` của hook input — không có harness_paths.root() cố định.

Break-glass: ENABLED=False đầu file, hoặc env SKILLSH_PUSH_GUARD=off.
An toàn: chặn (exit 2) CHỈ khi phát hiện dương tính; git đọc lỗi = không diff = không
tín hiệu = cho qua; lỗi nội bộ bất ngờ = fail-OPEN (không brick push của solo vì bug hook).
"""
import json
import os
import re
import shlex
import subprocess
import sys

ENABLED = os.environ.get("SKILLSH_PUSH_GUARD", "on").lower() not in ("off", "0", "false")

# Nhánh không được rewrite/xoá.
_PROTECTED = {"main", "master"}

# 5 secret shape precision-first (mirror hex secret_scan_before_ship._PATTERNS). Mỗi cái
# đòi prefix đặc trưng hoặc key=quoted-value nên văn xuôi không false-match.
_PATTERNS = [
    ("aws-access-key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("pem-private-key", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----")),
    ("anthropic-key", re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("generic-secret", re.compile(
        r"""(?i)(?:api[_-]?key|apikey|api[_-]?secret|secret|token|credential)\s*[:=]\s*['"][A-Za-z0-9/+=_-]{16,}['"]""")),
]

# Bỏ qua khi quét: tests/fixtures/examples/docs/lockfile — chuẩn secret-scan, tránh tự
# chặn trên fixture giả của chính mình.
_EXCLUDE_RE = re.compile(
    r"(?:^|/)(?:tests?|spec|specs|fixtures?|examples?|samples?|mocks?|__tests__)(?:/|$)"
    r"|(?:^|/)test_[^/]*$|_test\.[a-z]+$|\.(?:md|lock)$",
    re.IGNORECASE)

_FORCE_FLAGS = {"--force", "-f", "--force-with-lease"}
_DELETE_FLAGS = {"--delete", "-d"}
_ENV_ASSIGN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")


def _tokens(command):
    try:
        return shlex.split(command)
    except ValueError:
        return command.split()


def _parse_git_push(toks):
    """(is_push, c_dir, after): bóc env-prefix VAR=val/sudo/env + option toàn cục của
    git (-C <dir>, -c k=v, --no-pager) trước subcommand. after = token sau 'push'."""
    i = 0
    while i < len(toks) and (_ENV_ASSIGN.match(toks[i]) or toks[i] in ("sudo", "env")):
        i += 1
    if i >= len(toks) or toks[i] != "git":
        return False, None, []
    i += 1
    c_dir = None
    while i < len(toks):
        t = toks[i]
        if t == "-C" and i + 1 < len(toks):
            c_dir = toks[i + 1]; i += 2; continue
        if t == "-c" and i + 1 < len(toks):
            i += 2; continue
        if t.startswith("-"):
            i += 1; continue
        break
    if i >= len(toks) or toks[i] != "push":
        return False, c_dir, []
    return True, c_dir, toks[i + 1:]


def _refspec_dst(spec):
    """Nhánh đích của refspec: '+src:dst'->dst, ':dst'->dst, 'src:dst'->dst,
    'branch'->branch; bỏ '+' đầu và refs/heads/."""
    spec = spec.lstrip("+")
    if ":" in spec:
        spec = spec.split(":", 1)[1]
    if spec.startswith("refs/heads/"):
        spec = spec[len("refs/heads/"):]
    return spec


def _push_targets(after):
    """(is_force, is_delete, targets) từ token sau `push` (mirror protected_ref_guard)."""
    is_force = any(t in _FORCE_FLAGS or t.startswith("--force-with-lease=") for t in after)
    is_delete = any(t in _DELETE_FLAGS for t in after)
    for t in after:  # bundle ngắn: -fu = --force --set-upstream, -df = --delete --force
        if len(t) >= 2 and t.startswith("-") and not t.startswith("--"):
            bundle = t[1:]
            if "o" in bundle:  # -o<val> = --push-option, phần sau 'o' là giá trị
                bundle = bundle[:bundle.index("o")]
            is_force = is_force or "f" in bundle
            is_delete = is_delete or "d" in bundle
    positionals = [t for t in after if not t.startswith("-")]
    has_repo = any(t == "--repo" or t.startswith("--repo=") for t in after)
    refspecs = positionals if has_repo else positionals[1:]
    if any(s.startswith("+") for s in refspecs):
        is_force = True
    if any(s.startswith(":") for s in refspecs):
        is_delete = True
    targets = {_refspec_dst(s) for s in refspecs if _refspec_dst(s)}
    return is_force, is_delete, targets


def _resolve_root(c_dir, cwd):
    cwd = cwd or os.getcwd()
    base = c_dir if c_dir else cwd
    if base and not os.path.isabs(base):
        base = os.path.join(cwd, base)
    try:
        r = subprocess.run(["git", "-C", base, "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except Exception:
        pass
    return base


def _current_branch(root):
    try:
        r = subprocess.run(["git", "-C", root, "rev-parse", "--abbrev-ref", "HEAD"],
                           capture_output=True, text=True, timeout=10)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def _unpushed_diff(root):
    """Patch của commit chưa lên remote (tất cả, nếu repo không có remote). '' khi git
    lỗi — diff không kiểm được là không tín hiệu, không phải secret."""
    try:
        r = subprocess.run(
            ["git", "-C", root, "log", "--branches", "--not", "--remotes",
             "-p", "--no-color", "--max-count=200"],
            capture_output=True, text=True, timeout=30)
        return r.stdout if r.returncode == 0 else ""
    except Exception:
        return ""


def _added_lines(diff):
    """Nội dung dòng '+' của file không bị exclude, đã bỏ header."""
    out, excluded = [], False
    for line in (diff or "").splitlines():
        if line.startswith("+++ "):
            raw = line[4:].strip()
            path = raw[2:] if raw.startswith("b/") else raw
            excluded = bool(_EXCLUDE_RE.search(path))
            continue
        if line.startswith("--- "):
            continue
        if not excluded and line.startswith("+"):
            out.append(line[1:])
    return "\n".join(out)


def _scan(text):
    hits = []
    for name, rx in _PATTERNS:
        if rx.search(text or "") and name not in hits:
            hits.append(name)
    return hits


def _block(reason):
    sys.stderr.write("push-boundary-guard: " + reason + "\n")
    sys.exit(2)


def core(command, cwd):
    is_push, c_dir, after = _parse_git_push(_tokens(command))
    if not is_push:
        return  # không phải git push → không đụng
    root = _resolve_root(c_dir, cwd)

    # (b) force-push / xoá nhánh bảo vệ — chuỗi lệnh thuần; resolve current-branch khi
    # không có refspec tường minh (bare `git push --force`).
    is_force, is_delete, targets = _push_targets(after)
    if is_force or is_delete:
        if not targets:
            cur = _current_branch(root)
            if cur:
                targets = {cur}
        hit = sorted(t for t in targets if t in _PROTECTED)
        if hit:
            verb = "force-push/rewrite" if is_force else "xoá"
            _block("từ chối %s nhánh bảo vệ (%s) — rewrite/xoá nhánh này không lấy lại "
                   "được (mất commit người khác, không reflog remote). "
                   "Break-glass: SKILLSH_PUSH_GUARD=off." % (verb, ", ".join(hit)))

    # (a) secret trong diff sắp rời máy
    hits = _scan(_added_lines(_unpushed_diff(root)))
    if hits:
        _block("secret trong diff sắp push (%s). Gỡ khỏi commit (rotate credential nếu "
               "là thật) rồi push lại. Break-glass: SKILLSH_PUSH_GUARD=off." % ", ".join(hits))


def main():
    if not ENABLED:
        sys.exit(0)
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        sys.exit(0)  # stdin rác → không có căn cứ để chặn → cho qua
    if not isinstance(data, dict):
        sys.exit(0)
    tool_input = data.get("tool_input") or {}
    command = tool_input.get("command")
    if not isinstance(command, str) or not command.strip():
        sys.exit(0)
    cwd = data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or ""
    try:
        core(command, cwd)
    except Exception:
        # lỗi nội bộ bất ngờ → fail-OPEN. (SystemExit của _block là BaseException,
        # không lọt except này — exit 2 vẫn thoát đúng.)
        sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    main()
