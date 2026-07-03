#!/usr/bin/env python3
"""skill_usage_report.py — theo dõi việc dùng skill của CHÍNH skillsh.

READ-ONLY. Đọc:
  .claude/skills/*/SKILL.md           → kiểm kê skill (tất cả là skill-nhà của Son)
  state/telemetry/invocations.jsonl   → skill nào được gọi, bao nhiêu lần (do hook ghi)

In: skill được gọi (xếp theo tần suất) + skill CHƯA dùng trong log. Áp cổng-trung-thực
giống harness hex_agent: "chưa dùng = đáng cắt" CHỈ đáng tin khi số lần gọi ≥ số skill
(mỗi skill trung bình có ≥1 cơ hội chạy). Dưới ngưỡng → DANH SÁCH THEO DÕI, không cắt.
Nhắc luôn: hook chỉ thấy skill gọi qua Skill-tool / slash, KHÔNG thấy skill đọc tay.

Dùng:
  python3 skill-governance/skill_usage_report.py                 # tự dò gốc skillsh
  python3 skill-governance/skill_usage_report.py --project <path> --days 30
  python3 skill-governance/skill_usage_report.py --format json
"""

import argparse
import json
import os
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


def _default_project() -> Path:
    """Gốc skillsh: $CLAUDE_PROJECT_DIR nếu có, else lên 1 cấp từ skill-governance/."""
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[1]


def inventory(project: Path) -> set:
    """Tên mọi skill có SKILL.md dưới .claude/skills/."""
    sdir = project / ".claude" / "skills"
    if not sdir.is_dir():
        return set()
    return {d.name for d in sdir.iterdir()
            if d.is_dir() and (d / "SKILL.md").exists()}


def _iter_records(path: Path, days: int):
    if not path.exists():
        return
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    for line in path.open(encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except (ValueError, TypeError):
            continue
        if not isinstance(rec, dict):
            continue
        ts = rec.get("ts")
        if ts:
            try:
                if datetime.fromisoformat(ts) < cutoff:
                    continue
            except ValueError:
                pass
        yield rec


def _norm(skill: str) -> str:
    """Chuẩn hoá định danh log về tên thư mục skill (bỏ tiền tố, lấy đuôi sau ':')."""
    s = (skill or "").strip().lstrip("/")
    s = re.split(r"\s+", s)[0] if s else s
    return s.split(":")[-1]


def gather(project: Path, days: int) -> dict:
    skills = inventory(project)
    log = project / "state" / "telemetry" / "invocations.jsonl"
    counts, last_used, sessions, vias = Counter(), {}, {}, Counter()
    unknown = Counter()  # tên trong log không khớp skill nào (đổi tên / gõ nhầm)
    for rec in _iter_records(log, days):
        name = _norm(rec.get("skill", ""))
        if not name:
            continue
        counts[name] += 1
        vias[rec.get("via", "?")] += 1
        ts = rec.get("ts", "")
        if name not in last_used or ts > last_used[name]:
            last_used[name] = ts
        sessions.setdefault(name, set()).add(rec.get("session"))
        if name not in skills:
            unknown[name] += 1

    used_known = {s: n for s, n in counts.items() if s in skills}
    total = sum(counts.values())
    known_total = sum(used_known.values())
    never_used = sorted(skills - set(used_known))
    never_used_reliable = bool(skills) and known_total >= len(skills)
    return {
        "project": str(project),
        "days": days,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skills_total": len(skills),
        "distinct_used": len(used_known),
        "total_invocations": total,
        "known_invocations": known_total,
        "via": dict(vias),
        "never_used_reliable": never_used_reliable,
        "used": [
            {"skill": s, "count": n, "sessions": len(sessions.get(s, set())),
             "last_used": last_used.get(s, "")[:10]}
            for s, n in sorted(used_known.items(), key=lambda kv: (-kv[1], kv[0]))
        ],
        "never_used": never_used,
        "unknown_names": dict(unknown),
    }


def render_md(a: dict) -> str:
    L = []
    L.append("# Việc dùng skill — skillsh")
    L.append("_Sinh %s · cửa sổ %d ngày · READ-ONLY_" % (a["generated_at"][:16], a["days"]))
    L.append("")
    if a["total_invocations"] == 0:
        L.append("Chưa có lần gọi nào trong log. Hook đã cài; số sẽ xuất hiện khi bạn "
                 "dùng skill qua `/tên-skill` hoặc Skill-tool trong Claude Code.")
        L.append("")
        L.append("_Kiểm kê: %d skill trong .claude/skills/._" % a["skills_total"])
        return "\n".join(L)
    L.append("Đã dùng %d/%d skill · %d lần gọi. %d skill chưa xuất hiện trong log."
             % (a["distinct_used"], a["skills_total"], a["total_invocations"],
                len(a["never_used"])))
    L.append("")
    L.append("## Skill được gọi")
    L.append("")
    L.append("| skill | lần gọi | phiên | lần cuối |")
    L.append("|---|--:|--:|---|")
    for r in a["used"]:
        L.append("| %s | %d | %d | %s |" % (r["skill"], r["count"], r["sessions"], r["last_used"]))
    L.append("")
    label = "CẮT (ứng viên)" if a["never_used_reliable"] else "THEO DÕI (chưa cắt)"
    L.append("## Chưa dùng — %s" % label)
    L.append("")
    if not a["never_used_reliable"]:
        L.append("_Cổng-trung-thực: chỉ tin 'chưa dùng = cắt' khi số-lần-gọi ≥ số-skill "
                 "(%d ≥ %d). Chưa đạt → danh sách dưới là để THEO DÕI, không cắt. Hook cũng "
                 "không thấy skill đọc tay._" % (a["known_invocations"], a["skills_total"]))
        L.append("")
    L.append(", ".join(a["never_used"]) if a["never_used"] else "_(không có)_")
    if a["unknown_names"]:
        L.append("")
        L.append("## Tên lạ trong log (không khớp skill nào — đổi tên?/gõ nhầm?)")
        L.append("")
        L.append(", ".join("%s×%d" % (k, v) for k, v in a["unknown_names"].items()))
    L.append("")
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="skillsh skill-usage report (read-only)")
    ap.add_argument("--project", default=None, help="gốc skillsh (mặc định: tự dò)")
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--format", choices=["md", "json"], default="md")
    args = ap.parse_args(argv)
    project = Path(os.path.expanduser(args.project)).resolve() if args.project else _default_project()
    a = gather(project, args.days)
    print(json.dumps(a, ensure_ascii=False, indent=2) if args.format == "json" else render_md(a))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
