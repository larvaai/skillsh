#!/usr/bin/env python3
"""test_dot2_gates.py — test thật cho cổng-bằng-chứng Đợt 2 (stdlib, KHÔNG cần pytest).

Chạy:  python3 .claude/hooks/tests/test_dot2_gates.py
Exit 0 = tất cả xanh; ≠0 = số ca fail. Mọi ca dựng fixture tạm, KHÔNG đụng repo thật —
trừ 1 ca cố ý dí gate vào rebuild-hex-agent/pipeline/ship.json THẬT để chứng minh nó
bắt đúng lỗi lịch sử (ship GO tự khai, chưa có chữ ký).
"""
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve()
_ROOT = _HERE.parents[3]                     # …/skillsh
sys.path.insert(0, str(_ROOT / ".claude" / "hooks"))
sys.path.insert(0, str(_ROOT / "bin"))
import gate_ship                              # noqa: E402

_PASS, _FAIL = 0, 0


def check(name, cond):
    global _PASS, _FAIL
    if cond:
        _PASS += 1
        print("  ✓ %s" % name)
    else:
        _FAIL += 1
        print("  ✗ %s" % name)


def run_gate(root, paths, command="git push origin main"):
    """(verdict, stderr): 'pass' hoặc 'block'."""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stderr(buf):
            gate_ship.core(command, str(root), unpushed_paths=paths)
        return "pass", buf.getvalue()
    except SystemExit as e:
        return ("block" if e.code == 2 else "pass"), buf.getvalue()


def mkship(root, verdict="go", artifact_ok=True, uat_signoff=None):
    """Dựng pipeline/ship.json (+ artifact + uat.json tuỳ chọn). Trả path tương đối."""
    pdir = Path(root) / "pipeline"
    pdir.mkdir(parents=True, exist_ok=True)
    if artifact_ok:
        (pdir / "13-ship.md").write_text("# ship\n", encoding="utf-8")
    ship = {"project": "t", "giai_doan": "gd13_ship", "quyet_dinh": verdict,
            "artifact_path": "pipeline/13-ship.md"}
    (pdir / "ship.json").write_text(json.dumps(ship, ensure_ascii=False), encoding="utf-8")
    if uat_signoff is not None:
        (pdir / "uat.json").write_text(
            json.dumps({"giai_doan": "gd12_uat", "uat_signoff": uat_signoff}),
            encoding="utf-8")
    return "pipeline/ship.json"


def sign(root, ship_rel, verdict="go", tamper_after=False):
    """Ký ship.json bằng sign_gate.py (subprocess, CLAUDE_PROJECT_DIR=root)."""
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(root))
    r = subprocess.run(
        [sys.executable, str(_ROOT / "bin" / "sign_gate.py"),
         str(Path(root) / ship_rel), "--verdict", verdict],
        capture_output=True, text=True, env=env)
    if tamper_after:
        p = Path(root) / ship_rel
        d = json.loads(p.read_text())
        d["_tampered"] = True                 # đổi nội dung → sha lệch chữ ký
        p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return r


def main():
    print("Đợt 2 · cổng bằng chứng — test")

    # --- gate_ship.core ---
    print("[gate_ship]")
    with tempfile.TemporaryDirectory() as t:
        mkship(t, verdict="go")
        v, err = run_gate(t, ["pipeline/ship.json"])
        check("GO chưa ký → BLOCK", v == "block" and "chữ ký" in err.lower())

    with tempfile.TemporaryDirectory() as t:
        rel = mkship(t, verdict="go")
        sign(t, rel, "go")
        v, err = run_gate(t, ["pipeline/ship.json"])
        check("GO + ký hợp lệ + artifact có → PASS", v == "pass")

    with tempfile.TemporaryDirectory() as t:
        rel = mkship(t, verdict="go")
        sign(t, rel, "go", tamper_after=True)
        v, err = run_gate(t, ["pipeline/ship.json"])
        check("ký rồi SỬA ship.json (sha lệch) → BLOCK", v == "block" and "sha" in err.lower())

    with tempfile.TemporaryDirectory() as t:
        rel = mkship(t, verdict="go", artifact_ok=False)
        sign(t, rel, "go")
        v, err = run_gate(t, ["pipeline/ship.json"])
        check("artifact_path thiếu → BLOCK", v == "block" and "rỗng" in err)

    with tempfile.TemporaryDirectory() as t:
        rel = mkship(t, verdict="go", uat_signoff=False)
        sign(t, rel, "go")
        v, err = run_gate(t, ["pipeline/ship.json"])
        check("GO vô-điều-kiện + uat_signoff=false → BLOCK (chữ ký ngược)",
              v == "block" and "ngược" in err)

    with tempfile.TemporaryDirectory() as t:
        rel = mkship(t, verdict="go_co_dieu_kien", uat_signoff=False)
        sign(t, rel, "go_co_dieu_kien")
        v, err = run_gate(t, ["pipeline/ship.json"])
        check("GO-có-điều-kiện + uat chưa ký → PASS (điều kiện sống)", v == "pass")

    with tempfile.TemporaryDirectory() as t:
        mkship(t, verdict="no_go")
        v, err = run_gate(t, ["pipeline/ship.json"])
        check("NO_GO → PASS (không gác)", v == "pass")

    with tempfile.TemporaryDirectory() as t:
        mkship(t, verdict="go")
        v, err = run_gate(t, ["pipeline/ship.json"], command="ls -la")
        check("lệnh không phải git push → PASS", v == "pass")

    with tempfile.TemporaryDirectory() as t:
        mkship(t, verdict="go")
        v, err = run_gate(t, ["docs/readme.md"])   # ship.json không trong diff
        check("push thường (không có ship.json trong diff) → PASS", v == "pass")

    # --- break-glass (subprocess, env off) ---
    print("[break-glass]")
    with tempfile.TemporaryDirectory() as t:
        mkship(t, verdict="go")
        payload = json.dumps({"tool_input": {"command": "git push"}, "cwd": t})
        # ép hook lấy unpushed từ git thật sẽ [] (t không phải repo) → nên test core path
        # ở đây chỉ khẳng định ENABLED=off khiến main() exit 0 ngay.
        env = dict(os.environ, SKILLSH_SHIP_GATE="off")
        r = subprocess.run([sys.executable, str(_ROOT / ".claude/hooks/gate_ship.py")],
                           input=payload, capture_output=True, text=True, env=env)
        check("SKILLSH_SHIP_GATE=off → exit 0", r.returncode == 0)

    # --- fixture THẬT: ship.json lịch sử của rebuild-hex (GO tự khai, chưa ký) ---
    print("[fixture thật]")
    real = _ROOT / "rebuild-hex-agent" / "pipeline" / "ship.json"
    if real.is_file():
        v, err = run_gate(_ROOT, ["rebuild-hex-agent/pipeline/ship.json"])
        check("ship.json THẬT (da_go, chưa ký) → BLOCK", v == "block")
        # và check_pipeline chạy tay cũng phải FAIL nó
        r = subprocess.run([sys.executable, str(_ROOT / "bin/check_pipeline.py"),
                            str(real)], capture_output=True, text=True)
        check("check_pipeline trên ship.json THẬT → FAIL (exit>0)", r.returncode > 0)
    else:
        print("  (bỏ qua — không thấy fixture thật)")

    # --- sign_gate roundtrip ---
    print("[sign_gate]")
    with tempfile.TemporaryDirectory() as t:
        rel = mkship(t, verdict="go")
        env = dict(os.environ, CLAUDE_PROJECT_DIR=t)
        art = str(Path(t) / rel)
        r = sign(t, rel, "go")
        check("sign_gate ghi .sign.json (exit 0)", r.returncode == 0
              and (Path(t) / "pipeline/ship.json.sign.json").is_file())
        r = subprocess.run([sys.executable, str(_ROOT / "bin/sign_gate.py"), "--check", art],
                           capture_output=True, text=True, env=env)
        check("sign_gate --check → SIGNED", r.returncode == 0 and "SIGNED" in r.stdout)
        r = subprocess.run([sys.executable, str(_ROOT / "bin/sign_gate.py"), art,
                            "--verdict", "banana"], capture_output=True, text=True, env=env)
        check("verdict sai enum → exit 2", r.returncode == 2)

    print("\n%d xanh · %d đỏ" % (_PASS, _FAIL))
    return _FAIL


if __name__ == "__main__":
    sys.exit(main())
