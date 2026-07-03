#!/usr/bin/env python3
"""bash_safety.py — PreToolUse(Bash) lưới cuối chống lệnh phá-máy (bash-safety-floor).

Đợt 3 của skillsh. Chép nguyên tinh thần precision-first của hex bash_safety_guard: chỉ
chặn dạng LITERAL rõ ràng phá cả máy, hiếm khi là thao tác hợp lệ. frame live-slice (GĐ8)
là chỗ DUY NHẤT skillsh thật sự chạy scaffold/deploy trên máy — đây là lưới cho ca đó.

Chặn (exit 2) khi khớp một trong:
  · rm -rf/-fr vào root `/`, thư mục hệ thống (/etc /usr /bin /sys …), hoặc bare `~`/`$HOME`
  · rm recursive với biến quote THIẾU guard `:?`  (vd `rm -rf "$DIR/"` khi DIR có thể rỗng)
  · fork bomb  :(){ :|:& };:
  · dd / mkfs / shred / wipefs nhắm /dev/…
  · `curl|wget … | sh|bash`  (chạy script tải về, không đọc)
  · chmod/chown -R vào `/`
  · ghi đè /etc/passwd|/etc/shadow

HONESTY (bán đúng giá): guard chạy TRƯỚC shell expansion nên chỉ bắt dạng literal/biến-quote;
KHÔNG bắt được `rm -rf $X` khi X rỗng expand thành `/` (dùng `${X:?}` để tự chặn). Đây là
LƯỚI, không phải tường.

Tự-chứa: chỉ stdlib. Break-glass: SKILLSH_BASH_SAFETY=off. FAIL-OPEN tuyệt đối khi hook tự
lỗi — skillsh không có test-suite-hook, một crash fail-closed sẽ brick MỌI Bash của solo.
"""
import json
import os
import re
import sys

ENABLED = os.environ.get("SKILLSH_BASH_SAFETY", "on").lower() not in ("off", "0", "false")

_SYS_DIRS = r"(?:etc|usr|bin|sbin|lib|lib64|boot|sys|proc|dev|var|opt|root|System|Library|Applications)"
_PATTERNS = [
    ("rm-rf-root", re.compile(
        r"\brm\s+(?:-[a-zA-Z]*\s+)*-?[a-zA-Z]*(?:rf|fr|r\s+-\S*f|f\s+-\S*r)[a-zA-Z]*\s+"
        r"(?:-[a-zA-Z]+\s+)*(?:/|~|\$HOME)\s*(?:$|[;&|])")),
    ("rm-rf-sysdir", re.compile(
        r"\brm\s+(?:-\S+\s+)*-\S*(?:rf|fr)\S*\s+(?:-\S+\s+)*/%s\b" % _SYS_DIRS)),
    ("rm-rf-unguarded-var", re.compile(
        r"""\brm\s+(?:-\S+\s+)*-\S*(?:rf|fr)\S*\s+(?:-\S+\s+)*['"]?\$\{?[A-Za-z_][A-Za-z0-9_]*\}?/?['"]?\s*(?:$|[;&|])""")),
    ("fork-bomb", re.compile(r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:")),
    ("disk-writer", re.compile(r"\b(?:dd|mkfs\S*|shred|wipefs)\b[^|;&]*\b(?:of=)?/dev/\w")),
    ("pipe-to-shell", re.compile(r"\b(?:curl|wget)\b[^|]*\|\s*(?:sudo\s+)?(?:ba)?sh\b")),
    ("chmod-r-root", re.compile(r"\bch(?:mod|own)\s+(?:-\S+\s+)*-\S*R\S*\s+(?:-\S+\s+)*/\s*(?:$|[;&|])")),
    ("overwrite-passwd", re.compile(r">\s*/etc/(?:passwd|shadow|sudoers)\b")),
]
# rm biến-quote CÓ guard :? thì THA (đã tự bảo vệ)
_GUARDED_VAR = re.compile(r"\$\{[A-Za-z_][A-Za-z0-9_]*:\?")


def scan(command):
    """Tên pattern đầu tiên khớp, hoặc None."""
    if not command:
        return None
    for name, rx in _PATTERNS:
        m = rx.search(command)
        if not m:
            continue
        if name == "rm-rf-unguarded-var" and _GUARDED_VAR.search(m.group(0)):
            continue  # có :? → an toàn, tha
        return name
    return None


def main():
    if not ENABLED:
        sys.exit(0)
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        sys.exit(0)
    if not isinstance(data, dict):
        sys.exit(0)
    try:
        command = (data.get("tool_input") or {}).get("command")
        if not isinstance(command, str):
            sys.exit(0)
        hit = scan(command)
        if hit:
            sys.stderr.write(
                "bash-safety: chặn lệnh dạng phá-máy (%s). Nếu THẬT sự cố ý, chạy ngoài phiên "
                "hoặc SKILLSH_BASH_SAFETY=off. Với rm biến, dùng ${VAR:?} để tự chặn biến rỗng.\n"
                % hit)
            sys.exit(2)
    except Exception:
        sys.exit(0)  # hook tự lỗi → FAIL-OPEN, không brick Bash của solo
    sys.exit(0)


if __name__ == "__main__":
    main()
