#!/usr/bin/env python3
"""skill_decision_report.py — biến telemetry của harness thành QUYẾT ĐỊNH giữ/bỏ/sửa.

READ-ONLY. Không sửa gì trong harness. Chỉ đọc:
  harness/plugins/*/skills/*/SKILL.md            → danh mục skill (mẫu số)
  harness/state/telemetry/invocations.jsonl      → skill nào được gọi, bao nhiêu lần
  harness/state/telemetry/subagent-outcomes.jsonl→ tín hiệu hiệu quả (thô)
  harness/state/telemetry/sessions.jsonl         → skills[] mỗi phiên (nguồn phụ)

Nó KHÔNG tự phán skill nào đáng bỏ. Nó áp đúng cổng-trung-thực của chính harness:
"không dùng = đáng bỏ" CHỈ đúng khi corpus đủ dày (mỗi skill-nhà trung bình ≥1 lần gọi)
VÀ chỉ với skill do harness viết (hs:* / hs-*). Dưới ngưỡng đó → đây là DANH SÁCH THEO DÕI,
không phải danh sách cắt. Lý do: telemetry PreToolUse:Skill không thấy skill chạy tay,
và chất lượng/chi phí không được đo — nên "kém hiệu quả" không suy được từ log.

Dùng:
  python3 skill_decision_report.py --harness ~/Desktop/namnson/hex_agent
  python3 skill_decision_report.py --harness <path> --days 90 --format md > report.md
  python3 skill_decision_report.py --harness <path> --format json
"""

import argparse
import json
import os
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

_NAME_RE = re.compile(r"^name:\s*(.+?)\s*$", re.MULTILINE)
_NON_SKILL_DIRS = {"_shared", "common"}


def _is_owned(name: str) -> bool:
    """Skill do harness viết: namespace trước ':' là 'hs' hoặc 'hs-<x>'."""
    if not name:
        return False
    ns = name.split(":", 1)[0]
    return ns == "hs" or ns.startswith("hs-")


def load_catalog(plugins_dir: Path):
    """Quét harness/plugins/*/skills/*/SKILL.md → (dir->plugin, slug->dir, owned set)."""
    dir2plugin, slug2dir, owned = {}, {}, set()
    if not plugins_dir.is_dir():
        return dir2plugin, slug2dir, owned
    for plugin in sorted(plugins_dir.iterdir()):
        sdir = plugin / "skills"
        if not sdir.is_dir():
            continue
        for d in sorted(p for p in sdir.iterdir() if p.is_dir()):
            if d.name in _NON_SKILL_DIRS:
                continue
            md = d / "SKILL.md"
            if not md.exists():
                continue
            dir2plugin[d.name] = plugin.name
            slug2dir.setdefault(d.name, d.name)
            try:
                head = md.read_text(encoding="utf-8")[:2000]
            except OSError:
                head = ""
            m = _NAME_RE.search(head)
            if m:
                name = m.group(1).strip()
                slug2dir[name] = d.name
                slug2dir[name.replace(":", "-")] = d.name
                if _is_owned(name):
                    owned.add(d.name)
    return dir2plugin, slug2dir, owned


def to_dir(skill: str, slug2dir: dict, dirs: set) -> str:
    """Đưa mọi định danh trong log về slug thư mục chuẩn (hs:plan / plan → plan)."""
    if not skill:
        return ""
    if skill in slug2dir:
        return slug2dir[skill]
    if skill in dirs:
        return skill
    hyphen = skill.replace(":", "-")
    if hyphen in dirs:
        return hyphen
    tail = skill.split(":")[-1]
    if _is_owned(skill) and tail in dirs:
        return tail
    return hyphen


def _iter_jsonl(path: Path, days: int):
    """Đọc jsonl, bỏ dòng hỏng, lọc theo cửa sổ ngày nếu bản ghi có 'ts'."""
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


def gather(harness: Path, days: int) -> dict:
    tele = harness / "harness" / "state" / "telemetry"
    plugins = harness / "harness" / "plugins"
    dir2plugin, slug2dir, owned = load_catalog(plugins)
    dirs = set(dir2plugin)

    counts, last_used, sessions = Counter(), {}, {}
    for rec in _iter_jsonl(tele / "invocations.jsonl", days):
        slug = to_dir(rec.get("skill", ""), slug2dir, dirs)
        if not slug:
            continue
        counts[slug] += 1
        ts = rec.get("ts", "")
        if slug not in last_used or ts > last_used[slug]:
            last_used[slug] = ts
        sessions.setdefault(slug, set()).add(rec.get("session"))

    total = sum(counts.values())
    owned_total = sum(n for s, n in counts.items() if s in owned)
    never_used = sorted(owned - set(counts))
    # Cổng-trung-thực của harness: chỉ tin "không dùng = cắt" khi corpus đủ dày.
    never_used_reliable = bool(owned) and owned_total >= len(owned)

    # Hiệu quả (thô): outcome của subagent. Phần lớn 'unknown' vì transcript chưa
    # flush lúc SubagentStop — là hạn chế THỜI ĐIỂM ghi, không phải phán chất lượng.
    oc = Counter()
    for rec in _iter_jsonl(tele / "subagent-outcomes.jsonl", days):
        oc[rec.get("outcome", "unknown")] += 1
    oc_total = sum(oc.values())
    definite = oc_total - oc.get("unknown", 0)

    # Nguồn phụ: sessions.jsonl có skills[] không.
    sess_tot = sess_with_skills = 0
    for rec in _iter_jsonl(tele / "sessions.jsonl", days):
        sess_tot += 1
        if rec.get("skills"):
            sess_with_skills += 1

    return {
        "harness": str(harness),
        "days": days,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "owned_skills": len(owned),
        "total_invocations": total,
        "distinct_used": len(counts),
        "owned_invocations": owned_total,
        "never_used_reliable": never_used_reliable,
        "used": [
            {
                "skill": s,
                "plugin": dir2plugin.get(s, "?"),
                "count": n,
                "sessions": len(sessions.get(s, set())),
                "last_used": last_used.get(s, "")[:10],
                "owned": s in owned,
            }
            for s, n in counts.most_common()
        ],
        "never_used": [
            {"skill": s, "plugin": dir2plugin.get(s, "?")} for s in never_used
        ],
        "plugin_coverage": _plugin_coverage(dir2plugin, counts),
        "outcomes": dict(oc),
        "outcome_total": oc_total,
        "definite_rate": round(definite / oc_total, 3) if oc_total else None,
        "sessions_total": sess_tot,
        "sessions_with_skills": sess_with_skills,
    }


def _plugin_coverage(dir2plugin: dict, counts: Counter) -> list:
    per = {}
    for slug, plugin in dir2plugin.items():
        d = per.setdefault(plugin, {"plugin": plugin, "skills": 0, "used": 0, "calls": 0})
        d["skills"] += 1
        if counts.get(slug):
            d["used"] += 1
            d["calls"] += counts[slug]
    return sorted(per.values(), key=lambda r: (-r["calls"], -r["used"], r["plugin"]))


def verdict(agg: dict) -> dict:
    """Quy tắc quyết định — áp cổng-trung-thực, không cắt trên dữ liệu mỏng."""
    reliable = agg["never_used_reliable"]
    if reliable:
        headline = "Đủ dữ liệu để đề cử CẮT các skill-nhà không dùng (vẫn là đề cử, người quyết)."
        unused_label = "CẮT (ứng viên)"
    else:
        headline = (
            "CHƯA đủ dữ liệu để cắt bất kỳ skill nào. "
            "%d skill-nhà không xuất hiện trong %d lần gọi (skill-nhà: %d) — quá mỏng. "
            "Đây là DANH SÁCH THEO DÕI, không phải cắt."
            % (len(agg["never_used"]), agg["total_invocations"], agg["owned_invocations"])
        )
        unused_label = "THEO DÕI (chưa cắt)"
    return {"reliable": reliable, "headline": headline, "unused_label": unused_label}


def render_md(agg: dict) -> str:
    v = verdict(agg)
    L = []
    L.append("# Báo cáo quyết định skill — %s" % agg["harness"])
    L.append("_Sinh %s · cửa sổ %d ngày · READ-ONLY_" % (agg["generated_at"][:16], agg["days"]))
    L.append("")
    L.append("## Kết luận")
    L.append(v["headline"])
    L.append("")
    L.append(
        "Đã dùng %d/%d skill (%d lần gọi). %d skill chưa từng xuất hiện trong log. "
        "Hiệu quả đo được: %s%% run subagent có kết cục rõ (còn lại 'unknown')."
        % (
            agg["distinct_used"], agg["owned_skills"], agg["total_invocations"],
            len(agg["never_used"]),
            int((agg["definite_rate"] or 0) * 100),
        )
    )
    L.append("")

    L.append("## Skill được gọi nhiều nhất (đáng tin)")
    L.append("")
    L.append("| skill | plugin | lần gọi | phiên | lần cuối |")
    L.append("|---|---|--:|--:|---|")
    for r in agg["used"]:
        L.append("| %s | %s | %d | %d | %s |" % (
            r["skill"], r["plugin"], r["count"], r["sessions"], r["last_used"]))
    L.append("")

    L.append("## Độ phủ theo plugin")
    L.append("")
    L.append("| plugin | skill | đã dùng | lần gọi |")
    L.append("|---|--:|--:|--:|")
    for r in agg["plugin_coverage"]:
        L.append("| %s | %d | %d | %d |" % (
            r["plugin"], r["skills"], r["used"], r["calls"]))
    L.append("")

    L.append("## Chưa dùng trong log — %s" % v["unused_label"])
    L.append("")
    if not v["reliable"]:
        L.append(
            "_Cổng-trung-thực: chỉ tin 'không dùng = cắt' khi lần-gọi-skill-nhà ≥ "
            "số-skill-nhà (%d ≥ %d). Hiện CHƯA đạt, nên danh sách dưới là để THEO DÕI._"
            % (agg["owned_invocations"], agg["owned_skills"])
        )
        L.append("")
    by_plugin = {}
    for r in agg["never_used"]:
        by_plugin.setdefault(r["plugin"], []).append(r["skill"])
    for plugin in sorted(by_plugin):
        L.append("- **%s**: %s" % (plugin, ", ".join(sorted(by_plugin[plugin]))))
    L.append("")

    L.append("## Điều telemetry KHÔNG đo (đừng đọc nhầm là phủ đủ)")
    L.append("")
    L.append("- Chi phí token/tiền mỗi skill — không quy được.")
    L.append("- Đúng/sai, chất lượng ngữ nghĩa mỗi run — chỉ biết chạy/exit thô.")
    L.append("- Skill chạy TAY (đọc SKILL.md thủ công) — hook chỉ thấy Skill-tool + slash.")
    L.append("- %d/%d phiên không ghi skills[] — nguồn phụ thủng."
             % (agg["sessions_total"] - agg["sessions_with_skills"], agg["sessions_total"]))
    L.append("")
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Skill keep/cut/fix report (read-only)")
    ap.add_argument("--harness", default=os.environ.get("HARNESS_ROOT", "~/Desktop/namnson/hex_agent"),
                    help="đường dẫn gốc repo chứa harness/")
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--format", choices=["md", "json"], default="md")
    args = ap.parse_args(argv)
    harness = Path(os.path.expanduser(args.harness)).resolve()
    agg = gather(harness, args.days)
    if args.format == "json":
        print(json.dumps(agg, ensure_ascii=False, indent=2))
    else:
        print(render_md(agg))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
