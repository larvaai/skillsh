#!/usr/bin/env python3
"""advance.py — lật một task sang `done` bằng SCRIPT fail-closed, thay hand-edit progress.json.

Meta-lỗi thủng thật (rigor-gap #3): verdict là chữ tự do "## Verdict: PASS", progress.json
lật `done` bằng tay → T-06 phiếu "PASS (chờ ký)" nhưng progress.json đã done, T-07..T-15 mở
khoá theo, cả 15 task done trong một buổi. Bản vá: verdict sống ở MỘT chỗ máy-đọc
(front-matter phiếu), và CHỈ script này lật `done` — chỉ khi verdict==PASS thật.

    python3 bin/advance.py <task-id> [--project <key>]
    python3 bin/advance.py --check <task-id> [--project <key>]   # chỉ soi, không ghi

Đòi (fail-closed — không đủ thì KHÔNG lật, exit ≠ 0):
  1. Phiếu `<workspace>/progress/checkpoints/<task-id>.md` có FRONT-MATTER:
        ---
        verdict: PASS | FAIL | PASS_PENDING_SIGNOFF
        signed_by: <người, rỗng khi chờ ký>
        artifact_sha256: <sha lúc chấm>   # tuỳ chọn — bật verdict-hash-binding
        ---
     Không có front-matter → REFUSE (buộc theo convention, không đoán từ prose).
  2. verdict == PASS (đúng chuỗi). FAIL / PASS_PENDING_SIGNOFF → không lật, in lối đi tiếp.
  3. Nếu front-matter có `artifact_sha256`: băm lại artifact của task (từ progress.json) —
     LỆCH → STALE, không lật (artifact đã sửa SAU khi chấm; verdict-hash-binding).

Lật xong: đổi `trang_thai`→"done" (atomic temp+os.replace), báo task nào vừa hết bị chặn
(depends_on đã done hết). KHÔNG tự dời/ghi con trỏ ngoài task này. Trace actor+ts.

HONESTY: script chỉ khoá "verdict phải máy-đọc + artifact khớp sha". `signed_by` là
attribution — ai điền cũng được; chống-AI-tự-ký vẫn là LUẬT (checkpoint/SKILL.md: cổng đậm
GĐ8/GĐ13 chờ user tự điền signed_by qua sign_gate/tay). Đây KHÔNG phải xác thực người ký.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gatelib as G  # noqa: E402

_VERDICTS = ("PASS", "FAIL", "PASS_PENDING_SIGNOFF")
_FM_RE = re.compile(r"\A﻿?---\s*\n(.*?)\n---\s*(?:\n|$)", re.S)
_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*?)\s*$")


def parse_front_matter(text):
    """{key:val} từ front-matter YAML-phẳng đầu file (regex, không cần PyYAML), hoặc None."""
    m = _FM_RE.match(text)
    if not m:
        return None
    out = {}
    for line in m.group(1).splitlines():
        km = _KEY_RE.match(line)
        if km:
            out[km.group(1)] = km.group(2).strip().strip('"').strip("'")
    return out


def resolve_project(root, key):
    """(workspace_rel, progress_path) — từ --project hoặc current.json."""
    if key:
        for cand in ("projects/%s" % key, "state/project/%s" % key):
            pj = root / cand / "progress" / "progress.json"
            if pj.is_file():
                return cand, pj
        return None, None
    cur, err = G.load_json(root / "state" / "current.json")
    if err or not isinstance(cur, dict):
        return None, None
    ws = cur.get("path") or cur.get("workspace")
    if not ws:
        return None, None
    pj = root / ws / "progress" / "progress.json"
    return ws, (pj if pj.is_file() else None)


def _unblocked(tasks, just_done):
    """id các task mà mọi depends_on đã done SAU khi just_done thành done."""
    done = {t["id"] for t in tasks if t.get("trang_thai") == "done"} | {just_done}
    out = []
    for t in tasks:
        if t.get("trang_thai") != "done" and t.get("id") != just_done:
            deps = t.get("depends_on") or []
            if deps and all(d in done for d in deps):
                out.append(t.get("id"))
    return out


def evaluate(root, ws, progress, task_id):
    """(ok, verdict|None, reason). Không ghi gì."""
    tasks = progress.get("tasks") or []
    task = next((t for t in tasks if t.get("id") == task_id), None)
    if task is None:
        return False, None, "không thấy task %s trong progress.json" % task_id
    if task.get("trang_thai") == "done":
        return False, None, "task %s đã done rồi — không lật lại" % task_id

    phieu = root / ws / "progress" / "checkpoints" / ("%s.md" % task_id)
    if not phieu.is_file():
        return False, None, ("chưa có phiếu %s — chạy /checkpoint %s trước"
                             % (G.rel(phieu), task_id))
    fm = parse_front_matter(phieu.read_text(encoding="utf-8"))
    if fm is None:
        return False, None, (
            "phiếu %s CHƯA có front-matter verdict — advance không đoán từ prose. "
            "Thêm đầu phiếu:\n---\nverdict: PASS|FAIL|PASS_PENDING_SIGNOFF\nsigned_by: \n---"
            % G.rel(phieu))
    verdict = (fm.get("verdict") or "").strip().upper()
    if verdict not in _VERDICTS:
        return False, None, "verdict=%r không thuộc enum %s" % (verdict, "/".join(_VERDICTS))
    if verdict == "FAIL":
        return False, verdict, "phiếu FAIL — owner %s sửa rồi /checkpoint lại" % task.get("owner", "?")
    if verdict == "PASS_PENDING_SIGNOFF":
        return False, verdict, ("phiếu PASS nhưng CHỜ KÝ (signed_by rỗng). Người duyệt điền "
                                "signed_by trong phiếu rồi chạy lại advance.")

    # verdict == PASS: kiểm hash binding nếu có
    declared = (fm.get("artifact_sha256") or "").strip()
    art_rel = task.get("artifact")
    if declared and art_rel:
        art_abs = root / ws / art_rel
        try:
            cur_sha = G.sha256_file(art_abs)
        except OSError:
            return False, verdict, ("phiếu khai artifact_sha256 nhưng artifact %s không đọc "
                                    "được — không xác nhận được nội dung đã chấm" % art_rel)
        if cur_sha != declared:
            return False, verdict, (
                "STALE — artifact %s đã ĐỔI sau khi chấm (sha %s… ≠ phiếu %s…). Verdict PASS "
                "không còn khớp nội dung. /checkpoint lại rồi advance."
                % (art_rel, cur_sha[:8], declared[:8]))
    return True, verdict, ""


def do(root, ws, progress_path, task_id, write):
    progress, err = G.load_json(progress_path)
    if err:
        sys.stderr.write("đọc progress.json lỗi: %s\n" % err); return 2
    ok, verdict, reason = evaluate(root, ws, progress, task_id)
    if not ok:
        sys.stderr.write("advance: %s\n" % reason)
        return 1
    tasks = progress["tasks"]
    if not write:
        unb = _unblocked(tasks, task_id)
        print("SẼ LẬT %s → done (verdict=PASS). Mở khoá: %s"
              % (task_id, ", ".join(unb) or "—"))
        return 0
    for t in tasks:
        if t.get("id") == task_id:
            t["trang_thai"] = "done"
            break
    G.atomic_write(progress_path, json.dumps(progress, ensure_ascii=False, indent=2) + "\n")
    unb = _unblocked(tasks, task_id)
    G.trace("advance", target=task_id, status="done",
            note="ws=%s unblocked=%s" % (ws, ",".join(unb) or "-"))
    print("✓ %s → done" % task_id)
    print("  mở khoá: %s" % (", ".join(unb) or "— (không task nào phụ thuộc)"))
    return 0


def main():
    ap = argparse.ArgumentParser(description="Lật task→done fail-closed theo phiếu checkpoint")
    ap.add_argument("task_id")
    ap.add_argument("--project", help="key project (mặc định: current.json)")
    ap.add_argument("--check", action="store_true", help="chỉ soi, không ghi progress.json")
    a = ap.parse_args()
    root = G.project_root()
    ws, pj = resolve_project(root, a.project)
    if pj is None:
        sys.stderr.write("không resolve được progress.json (project=%s). Dùng --project <key>.\n"
                         % (a.project or "current.json")); return 2
    return do(root, ws, pj, a.task_id, write=not a.check)


if __name__ == "__main__":
    sys.exit(main())
