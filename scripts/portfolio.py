#!/usr/bin/env python3
"""portfolio.py — normalizer + switch cho lớp portfolio của skillsh.

Chữa vết nứt #1 (một project mang nhiều khoá/đường-dẫn): mọi alias, legacy-path,
hay khoá-cũ của một project đều resolve về ĐÚNG MỘT key nhờ sổ cái
`state/portfolio.json`. Không có file này thì không gì nối được 5 cái tên của
cùng một project lại với nhau.

Luật lớp (harness-design.md:47): READ-ONLY trên state từng project. Script này
CHỈ được ghi hai chỗ: `state/portfolio.json` (không đụng ở bản này) và
`state/current.json` (qua lệnh `switch`). Không bao giờ ghi vào projects/<key>/
hay state/project/<key>/.

Lệnh:
  resolve <alias>   in ra {key, path, state_path, giai_doan} của project khớp alias/path/key
  list              bảng mỗi-dòng-một-project (project cho_duyet=true nổi lên đầu)
  validate          kiểm current.json.project có trong sổ cái + path mỗi project tồn tại
  switch <alias>    đổi con trỏ current.json sang project (TỪ CHỐI key ngoài sổ cái)

Read-only trừ `switch`. Fail-rõ-ràng: lỗi in ra stderr + exit 1, không nuốt im.
"""

import json
import os
import sys
from pathlib import Path


def project_dir() -> Path:
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[1]


def _portfolio_path() -> Path:
    return project_dir() / "state" / "portfolio.json"


def load_portfolio() -> dict:
    p = _portfolio_path()
    if not p.exists():
        sys.stderr.write("LỖI: %s không tồn tại — chưa dựng sổ cái.\n" % p)
        sys.exit(1)
    return json.loads(p.read_text(encoding="utf-8"))


def resolve(pf: dict, needle: str):
    """Khớp needle với key | aliases | legacy_paths | path | state_path.
    Chuẩn hoá: bỏ dấu / đuôi, so không phân biệt hoa-thường."""
    n = (needle or "").strip().rstrip("/").lower()
    for proj in pf.get("projects", []):
        candidates = [proj.get("key", ""), proj.get("path", ""), proj.get("state_path", "")]
        candidates += proj.get("aliases", [])
        candidates += proj.get("legacy_paths", [])
        for c in candidates:
            if str(c).strip().rstrip("/").lower() == n:
                return proj
    return None


def cmd_resolve(pf: dict, needle: str) -> int:
    proj = resolve(pf, needle)
    if not proj:
        sys.stderr.write("KHÔNG KHỚP: '%s' không thuộc project nào trong sổ cái.\n" % needle)
        return 1
    print(json.dumps({
        "key": proj["key"],
        "path": proj["path"],
        "state_path": proj["state_path"],
        "giai_doan": proj.get("giai_doan"),
        "cho_duyet": proj.get("cho_duyet", False),
    }, ensure_ascii=False))
    return 0


def cmd_list(pf: dict) -> int:
    projs = sorted(pf.get("projects", []),
                   key=lambda p: (not p.get("cho_duyet", False), p.get("key", "")))
    cur = pf.get("current")
    print("KEY              CHỜ  GIAI ĐOẠN            PATH")
    for p in projs:
        mark = "→" if p["key"] == cur else " "
        print("%s %-14s %-4s %-20s %s" % (
            mark, p["key"], "●" if p.get("cho_duyet") else " ",
            p.get("giai_doan", "-"), p["path"]))
    return 0


def cmd_validate(pf: dict) -> int:
    root = project_dir()
    ok = True
    cur_path = root / "state" / "current.json"
    if cur_path.exists():
        cur = json.loads(cur_path.read_text(encoding="utf-8")).get("project")
        if not resolve(pf, cur or ""):
            sys.stderr.write("SAI: current.json trỏ '%s' — không có trong sổ cái.\n" % cur)
            ok = False
    for p in pf.get("projects", []):
        wp = root / p["path"]
        if not wp.exists() and p.get("schema_version", 1) != 0:
            sys.stderr.write("THIẾU: workspace %s (project %s) không tồn tại.\n" % (p["path"], p["key"]))
            ok = False
    print("OK — sổ cái nhất quán." if ok else "CÓ VẤN ĐỀ (xem trên).")
    return 0 if ok else 1


def cmd_switch(pf: dict, needle: str) -> int:
    proj = resolve(pf, needle)
    if not proj:
        sys.stderr.write("TỪ CHỐI: '%s' không trong sổ cái — switch chỉ nhận key đã đăng ký.\n" % needle)
        return 1
    root = project_dir()
    cur = {
        "project": proj["key"],
        "path": proj["path"],
        "mode": proj.get("mode", "greenfield"),
        "giai_doan": proj.get("giai_doan"),
        "cho_duyet": proj.get("cho_duyet", False),
        "updated_at": pf.get("updated_at"),
    }
    (root / "state" / "current.json").write_text(
        json.dumps(cur, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("→ current = %s (%s) · GĐ %s" % (proj["key"], proj["path"], proj.get("giai_doan")))
    return 0


def main() -> int:
    args = sys.argv[1:]
    if not args:
        sys.stderr.write(__doc__)
        return 1
    pf = load_portfolio()
    cmd = args[0]
    if cmd == "resolve" and len(args) >= 2:
        return cmd_resolve(pf, args[1])
    if cmd == "list":
        return cmd_list(pf)
    if cmd == "validate":
        return cmd_validate(pf)
    if cmd == "switch" and len(args) >= 2:
        return cmd_switch(pf, args[1])
    sys.stderr.write("Lệnh không hợp lệ. Xem: resolve|list|validate|switch\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
