#!/usr/bin/env python3
"""spine_check.py — biến "sợi traceability" từ đọc-bằng-mắt thành KIỂM-BẰNG-MÁY.

partner/traceability mô tả "gate suy ra từ decisions" + "node mồ côi" như việc
Claude NÊN làm — không có runtime nào thật sự parse đồ-thị rồi báo. Script này
parse `progress.json` (task-graph: depends_on + traces_to) và tìm CHÍNH XÁC:
  • link đứt   — depends_on trỏ tới task không tồn tại
  • vòng lặp   — A phụ thuộc B phụ thuộc … về lại A
  • mồ côi     — task không nối được về một gốc (depends_on rỗng) qua chuỗi
  • thiếu vết  — task giai-đoạn chịu-lực (build gd11 / uat gd12) không có traces_to

READ-ONLY tuyệt đối: chỉ đọc + báo, KHÔNG sửa. Mỗi lỗi kèm skill nên gọi để vá
(nhắc, không làm hộ — đúng hợp đồng control-tower của skillsh).

Dùng:
  python3 scripts/spine_check.py            # project đang đứng (state/current.json)
  python3 scripts/spine_check.py <key>      # resolve qua portfolio rồi kiểm
exit 0 = sợi liền · exit 1 = có chỗ đứt/mồ côi.
"""

import json
import os
import sys
from pathlib import Path

LOAD_BEARING = {"gd11_delivery", "gd12_uat"}  # bước phải có traces_to


def project_dir() -> Path:
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    return Path(env) if env else Path(__file__).resolve().parents[1]


def _load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def workspace_for(root: Path, key: str | None):
    """Đường-dẫn workspace: từ arg (resolve qua portfolio) hoặc current.json."""
    if key:
        pf = _load(root / "state" / "portfolio.json")
        for proj in pf.get("projects", []):
            cands = [proj.get("key"), proj.get("path"), proj.get("state_path")] \
                + proj.get("aliases", []) + proj.get("legacy_paths", [])
            if any(str(c).strip().rstrip("/").lower() == key.strip().rstrip("/").lower()
                   for c in cands if c):
                return proj["path"]
        sys.stderr.write("KHÔNG KHỚP key '%s' trong sổ cái.\n" % key)
        sys.exit(1)
    cur = _load(root / "state" / "current.json")
    return cur.get("path") or cur.get("workspace")


def check(progress: dict):
    """Trả (broken, cycles, orphans, missing_traces) — mỗi cái là list mô tả."""
    tasks = progress.get("tasks") or []
    ids = {t.get("id") for t in tasks}
    by_id = {t.get("id"): t for t in tasks}

    broken, missing_traces = [], []
    for t in tasks:
        for dep in t.get("depends_on") or []:
            if dep not in ids:
                broken.append("%s '%s' phụ thuộc %s — KHÔNG tồn tại."
                              % (t.get("id"), t.get("viec", "?"), dep))
        if t.get("giai_doan") in LOAD_BEARING and not t.get("traces_to"):
            missing_traces.append("%s '%s' (%s) thiếu traces_to — không neo về yêu cầu/epic."
                                  % (t.get("id"), t.get("viec", "?"), t.get("giai_doan")))

    # vòng lặp + reachability qua DFS trên depends_on
    WHITE, GREY, BLACK = 0, 1, 2
    color = {i: WHITE for i in ids}
    cycles = []

    def dfs(nid, stack):
        color[nid] = GREY
        for dep in by_id[nid].get("depends_on") or []:
            if dep not in by_id:
                continue
            if color[dep] == GREY:
                cycles.append(" → ".join(stack + [nid, dep]))
            elif color[dep] == WHITE:
                dfs(dep, stack + [nid])
        color[nid] = BLACK

    for i in ids:
        if color.get(i) == WHITE:
            dfs(i, [])

    # mồ côi: không có đường depends_on nào dẫn về một gốc (depends_on rỗng)
    roots = {t.get("id") for t in tasks if not (t.get("depends_on") or [])}
    orphans = []
    if roots:
        def reaches_root(nid, seen):
            deps = [d for d in (by_id[nid].get("depends_on") or []) if d in by_id]
            if not deps:
                return nid in roots
            return any(d not in seen and reaches_root(d, seen | {nid}) for d in deps)
        for t in tasks:
            tid = t.get("id")
            if tid not in roots and not reaches_root(tid, set()):
                orphans.append("%s '%s' — không nối được về gốc nào."
                               % (tid, t.get("viec", "?")))
    return broken, cycles, orphans, missing_traces


def main() -> int:
    root = project_dir()
    key = sys.argv[1] if len(sys.argv) > 1 else None
    ws = workspace_for(root, key)
    prog_path = root / ws / "progress" / "progress.json"
    if not prog_path.exists():
        sys.stderr.write("Không có %s — chưa có task-graph để kiểm.\n" % prog_path)
        return 1
    progress = _load(prog_path)
    broken, cycles, orphans, missing = check(progress)

    proj = progress.get("project", ws)
    n = len(progress.get("tasks") or [])
    print("SPINE CHECK — %s (%d task)" % (proj, n))
    problems = 0

    def section(title, items, fixer):
        nonlocal problems
        if items:
            problems += len(items)
            print("\n✗ %s  → vá bằng: %s" % (title, fixer))
            for it in items:
                print("   • " + it)

    section("LINK ĐỨT (depends_on trỏ hư)", broken, "/progress (sửa depends_on)")
    section("VÒNG LẶP phụ thuộc", cycles, "/progress (gỡ chu trình)")
    section("TASK MỒ CÔI (không nối về gốc)", orphans, "/progress hoặc /backlog")
    section("THIẾU traces_to (bước chịu lực)", missing, "/backlog (neo Story→AC→Epic)")

    if problems == 0:
        print("\n✓ Sợi liền: không link đứt, không vòng lặp, không mồ côi, "
              "bước chịu lực đều có vết.")
        return 0
    print("\n%d chỗ cần vá (báo cáo read-only — spine_check không tự sửa)." % problems)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
