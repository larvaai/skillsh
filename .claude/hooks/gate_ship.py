#!/usr/bin/env python3
"""gate_ship.py — PreToolUse(Bash) compliance hook: CỔNG BẰNG CHỨNG khi ship rời máy.

Đợt 2 của skillsh. Đứng cạnh push_boundary_guard (Đợt 1): guard đó chặn secret /
force-push; gate này chặn PHÁT-HÀNH-KHÔNG-CÓ-BẰNG-CHỨNG. Chỉ soi `git push`, và chỉ
CẮN khi trong các commit CHƯA lên remote có một `ship.json` (artifact máy của GĐ13)
tuyên GO. Push thường (sửa SKILL.md, cập nhật state, commit snapshot) đi qua sạch —
gate không đụng.

Khi có ship.json GO trong diff sắp push, đòi 3 điều (fail-closed, exit 2 nếu thiếu):
  A. CHỮ KÝ NGƯỜI còn tươi — `<ship>.sign.json` tồn tại, sha khớp nội dung ship.json
     hiện tại, verdict ∈ {go, go_co_dieu_kien}. Thiếu → "AI không được tự bấm GO";
     sha lệch → "sửa ship.json sau khi ký". (Vá đúng ship.json:110 — AI tự ký GO.)
  B. ARTIFACT KHÔNG RỖNG — `artifact_path` mà ship.json trỏ tới phải tồn tại.
     (Vá đúng meta-lỗi "báo GO khi 0 file/artifact tồn tại".)
  C. CHỮ-KÝ-KHÔNG-NGƯỢC — nếu cạnh đó có uat.json với `uat_signoff:false` mà ship
     tuyên GO vô-điều-kiện → chặn. (Vá đúng mâu thuẫn thật: uat.json uat_signoff=false
     trong khi ship.json trang_thai=da_go "✔ PO KÝ".)
Cảnh báo (KHÔNG chặn): artifact thượng nguồn (uat/delivery/skeleton) mà ship dẫn
nguồn nhưng không tồn tại → in [advisory].

HONESTY: presence gate — chứng minh bước-ký ĐÃ CHẠY trên đúng nội-dung ship.json,
KHÔNG chứng minh ai ký. Chống-AI-tự-ký là LUẬT ở CLAUDE.md, không phải mật mã ở đây.
Mọi phán quyết ghi vào state/trace/<ngày>.jsonl (actor + ts). Evasion `sh -c 'git push'`
lọt gate in-session vẫn bị git pre-push bắt ở tầng transport (Đợt sau).

Tự-chứa: chỉ stdlib, KHÔNG import gatelib/hook_runtime — lỗi import không được brick
cổng. Break-glass: SKILLSH_SHIP_GATE=off (hoặc ENABLED=False đầu file).
An toàn: chặn (exit 2) CHỈ khi dương tính rõ; git đọc lỗi / không resolve được =
không tín hiệu = cho qua; lỗi nội bộ bất ngờ = fail-OPEN (không brick push solo vì bug).
"""
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ENABLED = os.environ.get("SKILLSH_SHIP_GATE", "on").lower() not in ("off", "0", "false")

# mirror gatelib.VERDICTS_GO
_VERDICTS_GO = ("go", "go_co_dieu_kien")
# ship.json máy: basename ship.json nằm trong một thư mục pipeline/ (hoặc *ship.json ở pipeline/).
_SHIP_RE = re.compile(r"(?:^|/)pipeline/[^/]*ship\.json$")
_ENV_ASSIGN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
_HOOK = "gate_ship"


# ---- trace (self-contained, fail-open) -------------------------------------
def _trace(root, event, **fields):
    try:
        actor = os.environ.get("USER") or os.environ.get("USERNAME") or "unknown"
        rec = {"ts": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
               "actor": actor, "hook": _HOOK, "event": event}
        rec.update({k: v for k, v in fields.items() if v is not None})
        d = Path(root) / "state" / "trace"
        d.mkdir(parents=True, exist_ok=True)
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        with (d / ("%s.jsonl" % day)).open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


# ---- git push parsing (rút gọn từ push_boundary_guard) ----------------------
def _tokens(command):
    try:
        return shlex.split(command)
    except ValueError:
        return command.split()


def _parse_git_push(toks):
    i = 0
    while i < len(toks) and (_ENV_ASSIGN.match(toks[i]) or toks[i] in ("sudo", "env")):
        i += 1
    if i >= len(toks) or toks[i] != "git":
        return False, None
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
        return False, c_dir
    return True, c_dir


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


def _unpushed_paths(root):
    """Đường dẫn (relative-root) các file mà commit CHƯA lên remote động vào.
    '' khi git lỗi → không tín hiệu, không chặn."""
    try:
        r = subprocess.run(
            ["git", "-C", root, "log", "--branches", "--not", "--remotes",
             "--name-only", "--pretty=format:", "--max-count=400"],
            capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            return []
        seen, out = set(), []
        for line in r.stdout.splitlines():
            p = line.strip()
            if p and p not in seen:
                seen.add(p); out.append(p)
        return out
    except Exception:
        return []


# ---- đánh giá một ship.json -------------------------------------------------
def _is_go(ship):
    q = str(ship.get("quyet_dinh") or "").strip().lower()
    st = str(ship.get("trang_thai") or "").strip().lower()
    return q in _VERDICTS_GO or st == "da_go"


def _find_sibling(root, ship_rel, basename):
    """Tìm file cùng thư mục pipeline với ship.json (vd uat.json)."""
    p = (Path(root) / ship_rel).parent / basename
    return p if p.is_file() else None


def _evaluate_ship(root, ship_rel):
    """Trả (block_reason|None, advisories[]). Chỉ trả reason khi vi phạm HARD rõ."""
    adv = []
    ship_abs = Path(root) / ship_rel
    ship = _load_json(ship_abs)
    if not isinstance(ship, dict):
        return None, adv            # đọc không ra → không tín hiệu
    if not _is_go(ship):
        return None, adv            # không phải GO → không gác

    cond = str(ship.get("quyet_dinh") or "").strip().lower() == "go_co_dieu_kien"

    # A. chữ ký người còn tươi
    sp = ship_abs.with_name(ship_abs.name + ".sign.json")
    sign = _load_json(sp)
    if not isinstance(sign, dict) or "artifact_sha256" not in sign:
        return ("ship.json (%s) tuyên GO nhưng CHƯA có chữ ký người (%s.sign.json). "
                "AI KHÔNG được tự bấm GO — người thật ký bằng:\n"
                "    python3 bin/sign_gate.py %s --verdict go\n"
                "Break-glass: SKILLSH_SHIP_GATE=off." % (ship_rel, ship_rel, ship_rel)), adv
    try:
        if sign.get("artifact_sha256") != _sha256(ship_abs):
            return ("ship.json (%s) đã SỬA sau khi ký (sha lệch chữ ký) — GO không còn "
                    "khớp nội dung đã ký. Ký lại nếu thay đổi là chủ ý:\n"
                    "    python3 bin/sign_gate.py %s --verdict go\n"
                    "Break-glass: SKILLSH_SHIP_GATE=off." % (ship_rel, ship_rel)), adv
    except OSError:
        pass
    if str(sign.get("verdict") or "").strip().lower() not in _VERDICTS_GO:
        return ("ship.json (%s) tuyên GO nhưng chữ ký ghi verdict=%r (không phải go/"
                "go_co_dieu_kien). Break-glass: SKILLSH_SHIP_GATE=off."
                % (ship_rel, sign.get("verdict")), adv)

    # B. artifact_path không rỗng
    ap = ship.get("artifact_path") or ship.get("artifact")
    if ap:
        ap_abs = Path(root) / ap
        if not ap_abs.exists():
            return ("ship.json (%s) tuyên GO nhưng artifact_path trỏ '%s' KHÔNG tồn tại — "
                    "báo GO trên artifact rỗng. Break-glass: SKILLSH_SHIP_GATE=off."
                    % (ship_rel, ap)), adv

    # C. chữ-ký-không-ngược với uat.json cạnh đó (chỉ chặn khi GO vô-điều-kiện)
    uat_p = _find_sibling(root, ship_rel, "uat.json")
    if uat_p and not cond:
        uat = _load_json(uat_p)
        if isinstance(uat, dict) and uat.get("uat_signoff") is False:
            return ("ship.json (%s) tuyên GO vô-điều-kiện nhưng uat.json cạnh đó ghi "
                    "uat_signoff=false (UAT CHƯA ký) — chữ ký ngược. Nếu là GO-có-điều-kiện "
                    "thì đặt quyet_dinh='go_co_dieu_kien'; nếu không, chờ UAT ký. "
                    "Break-glass: SKILLSH_SHIP_GATE=off." % ship_rel), adv

    # advisory: nguồn thượng nguồn dẫn tên artifact nhưng không tồn tại
    for name in ("uat.json", "delivery.json", "skeleton.json"):
        sib = _find_sibling(root, ship_rel, name)
        if sib is None:
            adv.append("không thấy %s cạnh ship.json (nguồn thượng nguồn) — kiểm bằng chứng GĐ trước" % name)
    return None, adv


def _block(reason):
    sys.stderr.write("ship-gate: " + reason + "\n")
    sys.exit(2)


def core(command, cwd, unpushed_paths=None):
    """None ⇒ cho qua; gọi _block (exit 2) khi vi phạm. unpushed_paths tiêm được để test."""
    is_push, c_dir = _parse_git_push(_tokens(command))
    if not is_push:
        return
    root = _resolve_root(c_dir, cwd)
    paths = unpushed_paths if unpushed_paths is not None else _unpushed_paths(root)
    ships = [p for p in paths if _SHIP_RE.search(p)]
    if not ships:
        return                       # push không mang ship.json → không gác
    for ship_rel in ships:
        reason, adv = _evaluate_ship(root, ship_rel)
        for a in adv:
            sys.stderr.write("[advisory] ship-gate: %s\n" % a)
            _trace(root, "gate_advisory", target=ship_rel, note=a)
        if reason:
            _trace(root, "gate_block", target=ship_rel, status="BLOCKED",
                   note=reason.split("\n")[0])
            _block(reason)
        _trace(root, "gate_pass", target=ship_rel, status="PASS")


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
    tool_input = data.get("tool_input") or {}
    command = tool_input.get("command")
    if not isinstance(command, str) or not command.strip():
        sys.exit(0)
    cwd = data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or ""
    try:
        core(command, cwd)
    except SystemExit:
        raise                        # _block exit 2 phải thoát đúng
    except Exception:
        sys.exit(0)                  # bug hook → fail-OPEN
    sys.exit(0)


if __name__ == "__main__":
    main()
