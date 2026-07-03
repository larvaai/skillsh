#!/usr/bin/env python3
"""track_skill_invocation.py — ghi mỗi lần gọi skill vào
state/telemetry/invocations.jsonl. Bản self-contained cho skillsh (không phụ
thuộc runtime harness). TELEMETRY: fail-open tuyệt đối — không bao giờ chặn phiên.

Bắt hai đường (đăng ký trong .claude/settings.json):
  - PreToolUse, matcher "Skill"  → model gọi skill qua Skill-tool
      stdin: {tool_name:"Skill", tool_input:{skill|name}, session_id}
  - UserPromptExpansion          → bạn gõ /skill (slash command)
      stdin: {command_name:"atlas", command_args, hook_event_name} (host mới)
             hoặc {command:"/atlas ..."} (host cũ, đọc dự phòng)

Dedup theo (session|skill|phút): một lần gọi lỡ kích cả hai đường chỉ ghi 1 dòng.
Mọi lỗi (stdin rác, đĩa đầy, thiếu quyền) đều nuốt → in {"continue": true}, exit 0.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def _project_dir() -> Path:
    """Gốc project = $CLAUDE_PROJECT_DIR nếu có, else suy từ vị trí file
    (.claude/hooks/<đây> → lên 2 cấp)."""
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[2]


def _telemetry_dir() -> Path:
    d = _project_dir() / "state" / "telemetry"
    d.mkdir(parents=True, exist_ok=True)
    return d


def extract_skill(data: dict):
    """(skill_name, via) từ payload hook. '' nếu không phải lần gọi skill."""
    if data.get("tool_name") == "Skill":
        inp = data.get("tool_input") or {}
        skill = inp.get("skill") or inp.get("name") or ""
        return str(skill).strip(), "PreToolUse:Skill"
    if (data.get("command_name") or data.get("command")
            or data.get("hook_event_name") == "UserPromptExpansion"):
        raw = str(data.get("command_name") or data.get("command") or "").strip().lstrip("/")
        skill = re.split(r"\s+", raw)[0] if raw else ""
        return skill, "UserPromptExpansion"
    return "", ""


def _append_once(rec: dict, key: str) -> None:
    """Ghi 1 dòng jsonl, bỏ qua nếu key (session|skill|phút) đã thấy."""
    tele = _telemetry_dir()
    dedup = tele / ".dedup"
    dedup.mkdir(exist_ok=True)
    marker = dedup / re.sub(r"[^A-Za-z0-9._-]", "_", key)
    if marker.exists():
        return
    with (tele / "invocations.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    marker.write_text("", encoding="utf-8")


def main() -> None:
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        if isinstance(data, dict):
            skill, via = extract_skill(data)
            if skill:
                now = datetime.now(timezone.utc)
                session = data.get("session_id") or os.environ.get("CLAUDE_SESSION_ID") or ""
                minute = now.strftime("%Y-%m-%dT%H:%M")
                _append_once(
                    {"ts": now.isoformat(), "skill": skill, "session": session, "via": via},
                    "%s|%s|%s" % (session, skill, minute),
                )
    except Exception:  # noqa: BLE001 — telemetry không bao giờ được ném ngược vào hook
        pass
    # Fail-open: luôn cho phiên chạy tiếp.
    sys.stdout.write(json.dumps({"continue": True}))


if __name__ == "__main__":
    main()
