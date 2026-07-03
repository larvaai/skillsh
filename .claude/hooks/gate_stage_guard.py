#!/usr/bin/env python3
"""gate_stage_guard.py — biến CỔNG từ lời-kể thành DỮ-LIỆU-chặn-được.

Vết rò thật (harness-design.md:78): project rebuild đã ở gd14 trong khi gd12
uat_signoff=false — cổng chỉ là ghi chú, ai cũng nhảy qua được. Hook này đọc
đồ-thị task trong `progress.json` và CHẶN việc gọi một skill-giai-đoạn khi
bước trước nó chưa `done`. "Xong" ở skillsh = task done (checkpoint PASS +
artifact đúng chỗ), nên depends_on chưa done = cổng trước chưa đóng.

CLASS: compliance-nhẹ — ON, blocking, nhưng FAIL-OPEN tuyệt đối: thiếu state,
project greenfield chưa có progress, skill không phải chủ giai đoạn, hay BẤT KỲ
lỗi nào → CHO CHẠY. Thà bỏ sót một cổng còn hơn brick phiên của bạn (đúng tinh
thần warm-never-brick của skillsh). Thông điệp chặn luôn kèm lối đi tiếp.

Đăng ký: PreToolUse matcher "Skill" (cạnh track_skill_invocation.py).
  stdin: {tool_name:"Skill", tool_input:{skill|name}, session_id}
Chặn bằng JSON permissionDecision=deny; cho chạy = im lặng exit 0.
"""

import json
import os
import sys
from pathlib import Path

# Skill là CHỦ một giai đoạn pipeline (khớp trường `owner` trong progress.json).
# Chỉ những skill này mới bị soi cổng; mọi skill khác (charter/progress/checkpoint/
# explain/grade/review/atlas/partner/resume/trace/triage/tune/teen/spar…) cho qua.
STAGE_OWNERS = {
    "idea", "shape", "stack", "skeleton", "backlog",
    "modules", "delivery", "uat", "ship", "operate", "fanout", "frame",
}


def project_dir() -> Path:
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[2]


def _load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def load_current_progress(root: Path):
    """(progress_dict, workspace_path) của project đang đứng, hoặc (None, None)."""
    cur_p = root / "state" / "current.json"
    if not cur_p.exists():
        return None, None
    cur = _load_json(cur_p)
    path = cur.get("path") or (cur.get("workspace"))
    if not path:
        return None, None
    prog = root / path / "progress" / "progress.json"
    if not prog.exists():
        return None, None
    return _load_json(prog), path


def evaluate(progress: dict, skill: str):
    """(allow: bool, reason: str). Đóng-đô DỮ LIỆU:
    tìm task ĐẦU TIÊN do `skill` sở hữu mà chưa done (= bước skill sắp làm);
    nếu một depends_on của nó chưa done → CHẶN, nêu đích danh bước còn thiếu.
    Mọi trường hợp không xác định được → CHO CHẠY."""
    tasks = progress.get("tasks") or []
    if not tasks:
        return True, ""
    by_id = {t.get("id"): t for t in tasks}

    target = None
    for t in tasks:
        if t.get("owner") == skill and t.get("trang_thai") != "done":
            target = t
            break
    if target is None:
        # skill không có task chưa-done nào → không phải đang tiến bước → cho qua
        return True, ""

    unmet = []
    for dep_id in target.get("depends_on") or []:
        dep = by_id.get(dep_id)
        if dep is not None and dep.get("trang_thai") != "done":
            unmet.append(dep)
    if not unmet:
        return True, ""

    lines = [
        "⛔ CỔNG CHƯA ĐÓNG — không nên chạy /%s (bước '%s', %s) khi bước trước chưa xong:"
        % (skill, target.get("viec", target.get("id", "?")), target.get("giai_doan", "?")),
    ]
    for d in unmet:
        lines.append("   • %s '%s' (%s) đang %s — chưa done."
                     % (d.get("id"), d.get("viec", "?"), d.get("giai_doan", "?"),
                        d.get("trang_thai", "?")))
    lines.append("Lối đi tiếp: đóng bước trên trước (làm xong + /checkpoint cấp PASS), "
                 "rồi chạy lại /%s. Nếu cố ý nhảy cổng, tắt hook này trong "
                 ".claude/settings.json." % skill)
    return False, "\n".join(lines)


def _deny(reason: str) -> None:
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False))


def main() -> None:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        if not isinstance(data, dict) or data.get("tool_name") != "Skill":
            return  # không phải gọi skill → im lặng cho qua
        inp = data.get("tool_input") or {}
        skill = str(inp.get("skill") or inp.get("name") or "").strip()
        # tách "plugin:skill" nếu có
        skill = skill.split(":")[-1]
        if skill not in STAGE_OWNERS:
            return  # skill không phải chủ giai đoạn → cho qua
        root = project_dir()
        progress, _ = load_current_progress(root)
        if progress is None:
            return  # không có state để soi → fail-open
        allow, reason = evaluate(progress, skill)
        if not allow:
            _deny(reason)
    except Exception:  # noqa: BLE001 — cổng không bao giờ được brick phiên
        return  # fail-open


if __name__ == "__main__":
    main()
