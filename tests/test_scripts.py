#!/usr/bin/env python3
"""test_scripts.py — lưới bắt regression cho 3 ENGINE tất định của skillsh:
portfolio.py (normalizer/switch) · spine_check.py · gate_stage_guard.py (hook cổng).

Chạy:  python3 tests/test_scripts.py       (exit 0 = tất cả xanh, 1 = có đỏ)
Không cần pytest — stdlib thuần.

Mọi test HERMETIC: dựng fixture trong thư mục tạm rồi trỏ CLAUDE_PROJECT_DIR vào
đó, nên KHÔNG phụ thuộc state thật của repo — đổi ledger/progress thật không làm
vỡ test. Chỉ smoke-test cuối chạy engine trên project thật (chỉ kiểm không-crash).
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
HOOK = ROOT / ".claude" / "hooks" / "gate_stage_guard.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


spine = _load(SCRIPTS / "spine_check.py", "spine_check")
gate = _load(HOOK, "gate_stage_guard")

_fail = []


def ok(name, cond):
    print(("  ✓ " if cond else "  ✗ ") + name)
    if not cond:
        _fail.append(name)


def run(args, stdin=None, project_dir=None):
    env = dict(os.environ)
    if project_dir:
        env["CLAUDE_PROJECT_DIR"] = str(project_dir)
    p = subprocess.run([sys.executable, *args], input=stdin,
                       capture_output=True, text=True, env=env)
    return p.returncode, p.stdout, p.stderr


def mk_project(root, tasks, path="projects/demo"):
    root = Path(root)
    (root / path / "progress").mkdir(parents=True, exist_ok=True)
    (root / "state").mkdir(parents=True, exist_ok=True)
    (root / "state" / "current.json").write_text(
        json.dumps({"project": "demo", "path": path}), encoding="utf-8")
    (root / path / "progress" / "progress.json").write_text(
        json.dumps({"project": "demo", "tasks": tasks}), encoding="utf-8")
    return root


# ────────────────────────── spine_check.check() ──────────────────────────
def test_spine_unit():
    print("spine_check.check() — unit")
    clean = [
        {"id": "A", "viec": "root", "giai_doan": "gd1", "depends_on": []},
        {"id": "B", "viec": "mid", "giai_doan": "gd6", "depends_on": ["A"]},
        {"id": "C", "viec": "build", "giai_doan": "gd11_delivery",
         "depends_on": ["B"], "traces_to": ["E1"]},
    ]
    b, cy, o, mi = spine.check({"tasks": clean})
    ok("graph sạch → không lỗi", not any([b, cy, o, mi]))

    b, *_ = spine.check({"tasks": [
        {"id": "A", "depends_on": []},
        {"id": "B", "depends_on": ["ZZZ"]}]})
    ok("dep trỏ hư → bắt link đứt", len(b) == 1)

    _, cy, o, _ = spine.check({"tasks": [
        {"id": "A", "depends_on": []},
        {"id": "C", "depends_on": ["D"]},
        {"id": "D", "depends_on": ["C"]}]})
    ok("C↔D → bắt vòng lặp", len(cy) >= 1)
    ok("C,D không về gốc → bắt mồ côi", len(o) == 2)

    *_, mi = spine.check({"tasks": [
        {"id": "A", "depends_on": []},
        {"id": "E", "giai_doan": "gd12_uat", "depends_on": ["A"]}]})
    ok("bước chịu-lực thiếu traces_to → bắt", len(mi) == 1)


# ────────────────────────── gate.evaluate() ──────────────────────────
def test_gate_unit():
    print("gate_stage_guard.evaluate() — unit")
    done_dep = [
        {"id": "T-04", "viec": "Arch", "giai_doan": "gd6",
         "trang_thai": "done", "owner": "shape", "depends_on": []},
        {"id": "T-05", "viec": "Stack", "giai_doan": "gd7",
         "trang_thai": "pending", "owner": "stack", "depends_on": ["T-04"]},
    ]
    allow, _ = gate.evaluate({"tasks": done_dep}, "stack")
    ok("dep đã done → allow", allow is True)

    open_dep = [dict(done_dep[0], trang_thai="pending"), done_dep[1]]
    allow, reason = gate.evaluate({"tasks": open_dep}, "stack")
    ok("dep chưa done → deny", allow is False)
    ok("deny nêu đích danh blocker (T-04)", "T-04" in reason)

    allow, _ = gate.evaluate({"tasks": [dict(done_dep[0])]}, "shape")
    ok("skill không còn task chưa-done → allow", allow is True)

    allow, _ = gate.evaluate({"tasks": []}, "stack")
    ok("tasks rỗng → allow", allow is True)


# ────────────────────────── gate hook — full CLI ──────────────────────────
def test_gate_cli():
    print("gate_stage_guard.py — full stdin path")
    tasks = [
        {"id": "T-04", "viec": "Arch", "giai_doan": "gd6",
         "trang_thai": "pending", "owner": "shape", "depends_on": []},
        {"id": "T-05", "viec": "Stack", "giai_doan": "gd7",
         "trang_thai": "pending", "owner": "stack", "depends_on": ["T-04"]},
    ]
    with tempfile.TemporaryDirectory() as d:
        fx = mk_project(d, tasks)
        empty = Path(tempfile.mkdtemp())  # no state → fail-open

        def call(payload, pdir=fx):
            return run([str(HOOK)], stdin=payload, project_dir=pdir)

        rc, out, _ = call('{"tool_name":"Skill","tool_input":{"skill":"stack"}}')
        ok("/stack khi T-04 chưa done → deny", rc == 0 and '"permissionDecision": "deny"' in out)

        rc, out, _ = call('{"tool_name":"Skill","tool_input":{"skill":"shape"}}')
        ok("/shape (dep rỗng) → allow im lặng", rc == 0 and out.strip() == "")

        rc, out, _ = call('{"tool_name":"Skill","tool_input":{"skill":"explain"}}')
        ok("skill không-giai-đoạn → allow", rc == 0 and out.strip() == "")

        rc, out, _ = call('{"tool_name":"Skill","tool_input":{"skill":"stack"}}', pdir=empty)
        ok("fail-open: không state → allow", rc == 0 and out.strip() == "")

        rc, out, _ = call('not json {{{')
        ok("fail-open: stdin rác → allow", rc == 0 and out.strip() == "")

        rc, out, _ = call('{"tool_name":"Bash","tool_input":{"command":"ls"}}')
        ok("tool không phải Skill → allow", rc == 0 and out.strip() == "")


# ────────────────────────── portfolio.py — full CLI ──────────────────────────
def test_portfolio_cli():
    print("portfolio.py — normalizer/switch")
    ledger = {
        "schema_version": 1, "updated_at": "t", "current": "demo",
        "projects": [{
            "key": "demo", "path": "projects/demo", "state_path": "state/project/demo",
            "schema_version": 1, "mode": "greenfield", "giai_doan": "gd1",
            "cho_duyet": False, "aliases": ["demo", "demo-old"],
            "legacy_paths": ["old/demo"],
        }],
    }
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "state").mkdir()
        (d / "projects" / "demo").mkdir(parents=True)  # path phải tồn tại cho validate
        (d / "state" / "portfolio.json").write_text(json.dumps(ledger), encoding="utf-8")
        P = SCRIPTS / "portfolio.py"

        rc, out, _ = run([str(P), "resolve", "demo"], project_dir=d)
        ok("resolve key → đúng key", rc == 0 and json.loads(out)["key"] == "demo")

        rc, out, _ = run([str(P), "resolve", "demo-old"], project_dir=d)
        ok("resolve alias → cùng key", rc == 0 and json.loads(out)["key"] == "demo")

        rc, out, _ = run([str(P), "resolve", "old/demo"], project_dir=d)
        ok("resolve legacy-path → cùng key", rc == 0 and json.loads(out)["key"] == "demo")

        rc, _, _ = run([str(P), "resolve", "khong-co"], project_dir=d)
        ok("resolve tên lạ → exit 1", rc == 1)

        rc, _, _ = run([str(P), "validate"], project_dir=d)
        ok("validate ledger đúng → exit 0", rc == 0)

        rc, _, _ = run([str(P), "switch", "demo-old"], project_dir=d)
        cur = json.loads((d / "state" / "current.json").read_text(encoding="utf-8"))
        ok("switch alias → ghi current.json = key chuẩn", rc == 0 and cur["project"] == "demo")

        rc, _, _ = run([str(P), "switch", "khong-co"], project_dir=d)
        ok("switch tên lạ → từ chối (exit 1)", rc == 1)


# ────────────────────────── smoke: engine trên repo thật ──────────────────────────
def test_real_smoke():
    print("smoke — engine chạy trên state thật (chỉ kiểm không-crash)")
    rc, _, err = run([str(SCRIPTS / "portfolio.py"), "validate"], project_dir=ROOT)
    ok("portfolio validate trên repo thật không crash", rc in (0, 1) and "Traceback" not in err)
    rc, _, err = run([str(SCRIPTS / "spine_check.py"), "hxag"], project_dir=ROOT)
    ok("spine_check hxag không crash", rc in (0, 1) and "Traceback" not in err)


def main():
    for t in (test_spine_unit, test_gate_unit, test_gate_cli,
              test_portfolio_cli, test_real_smoke):
        t()
    print()
    if _fail:
        print("ĐỎ — %d test rớt: %s" % (len(_fail), "; ".join(_fail)))
        return 1
    print("XANH — tất cả test qua.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
