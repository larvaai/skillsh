#!/usr/bin/env python3
"""gatelib.py — hạt nhân dùng chung cho các CLI cổng-bằng-chứng Đợt 2.

Chỉ stdlib. Dùng bởi sign_gate.py / check_pipeline.py / advance.py (các CLI chạy
tay `python3 bin/<x>.py`). Hook PreToolUse (gate_ship.py) CỐ Ý tự-chứa, KHÔNG import
file này — để lỗi import không bao giờ brick một cổng chặn (mirror phong cách
push_boundary_guard.py). Enum/hình-dạng ở đây là NGUỒN THAM CHIẾU; hook giữ bản sao
inline và ghi chú "mirror gatelib".

Ba sự-thật-thành-thật (in thẳng để người mới không tin quá tay):
  1. Cổng là PRESENCE gate — chứng minh bước-ký ĐÃ CHẠY trên đúng nội-dung artifact
     (sha khớp), KHÔNG chứng minh AI hay người ký. `signed_by` là attribution
     (lấy từ git config / $USER), KHÔNG phải authentication.
  2. Bảo vệ chống-AI-tự-ký là LUẬT (CLAUDE.md + prose skill: "AI KHÔNG chạy
     sign_gate.py"), không phải mật mã. Cổng chỉ khoá được "sửa artifact sau khi ký".
  3. .sign.json là file trần trong git — tamper-VISIBLE (sửa lộ trong diff), không
     tamper-proof.
"""
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Enum quyết-định đóng (mirror skillsh: GO / NO_GO / GO_CO_DIEU_KIEN / CHO_DUYET).
VERDICTS_GO = ("go", "go_co_dieu_kien")          # cần chữ ký người
VERDICTS_ALL = ("go", "go_co_dieu_kien", "no_go", "cho_duyet")


def project_root() -> Path:
    """Gốc skillsh = $CLAUDE_PROJECT_DIR nếu có, else walk-up tìm .git, else cwd."""
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env and Path(env).is_dir():
        return Path(env).resolve()
    here = Path(__file__).resolve()
    for p in [here.parent] + list(here.parents):
        if (p / ".git").exists():
            return p
    return Path.cwd()


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path) -> str:
    """sha256 hex đầy đủ của bytes file. Ném FileNotFoundError nếu thiếu (chủ ý:
    ký một artifact không tồn tại là lỗi cần lộ)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def whoami() -> str:
    """Danh tính người ký, best-effort: git user.name <email> → $USER → getpass.
    Đây là ATTRIBUTION, không phải xác thực — ai chạy CLI cũng đóng được dấu này."""
    root = project_root()
    try:
        name = subprocess.run(["git", "-C", str(root), "config", "user.name"],
                              capture_output=True, text=True, timeout=5).stdout.strip()
        email = subprocess.run(["git", "-C", str(root), "config", "user.email"],
                               capture_output=True, text=True, timeout=5).stdout.strip()
        if name and email:
            return "%s <%s>" % (name, email)
        if name:
            return name
    except Exception:
        pass
    u = os.environ.get("USER") or os.environ.get("USERNAME")
    if u:
        return u
    try:
        import getpass
        return getpass.getuser()
    except Exception:
        return "unknown"


def load_json(path):
    """(data, None) hoặc (None, 'lý do') — không bao giờ ném."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f), None
    except FileNotFoundError:
        return None, "không tồn tại"
    except json.JSONDecodeError as e:
        return None, "JSON hỏng: %s" % e
    except OSError as e:
        return None, "đọc lỗi: %s" % e


def atomic_write(path, text: str) -> None:
    """Ghi qua temp + os.replace — phiên chết giữa chừng không để lại file nửa-ghi."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp.%d" % os.getpid())
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def sign_path(artifact) -> Path:
    """<artifact>.sign.json ngay cạnh artifact."""
    p = Path(artifact)
    return p.with_name(p.name + ".sign.json")


def rel(path) -> str:
    """Đường dẫn tương-đối-gốc để ghi vào trace/artifact cho gọn và ổn định."""
    try:
        return str(Path(path).resolve().relative_to(project_root()))
    except Exception:
        return str(path)


def trace(event: str, **fields) -> None:
    """Append 1 dòng JSONL vào state/trace/<ngày>.jsonl. Actor + ts luôn có.
    TELEMETRY: nuốt mọi lỗi — sổ audit hỏng không được làm hỏng lệnh chính."""
    try:
        rec = {"ts": now_iso(), "actor": whoami(), "event": event}
        rec.update({k: v for k, v in fields.items() if v is not None})
        d = project_root() / "state" / "trace"
        d.mkdir(parents=True, exist_ok=True)
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        with (d / ("%s.jsonl" % day)).open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


def read_sign(artifact):
    """Trạng thái chữ ký của artifact so với NỘI DUNG hiện tại của nó.
    Trả (state, sign_data):
      'UNSIGNED'  — không có .sign.json
      'STALE'     — có .sign.json nhưng sha lệch (artifact sửa sau khi ký)
      'BADSIGN'   — .sign.json hỏng/thiếu trường
      'SIGNED'    — có chữ ký, sha khớp nội dung hiện tại
    """
    sp = sign_path(artifact)
    data, err = load_json(sp)
    if err:
        return ("UNSIGNED" if err == "không tồn tại" else "BADSIGN"), None
    if not isinstance(data, dict) or "artifact_sha256" not in data:
        return "BADSIGN", data
    try:
        cur = sha256_file(artifact)
    except OSError:
        return "BADSIGN", data
    return ("SIGNED" if data.get("artifact_sha256") == cur else "STALE"), data
