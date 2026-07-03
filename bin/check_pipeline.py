#!/usr/bin/env python3
"""check_pipeline.py — kiểm-tay artifact cổng pipeline (bản chạy-không-cần-push của gate_ship).

Cùng luật với hook gate_ship nhưng chạy chủ động bất cứ lúc nào — để audit trước khi
push, hoặc để /ship, /uat tự soi bản mình vừa sinh. KHÔNG sửa gì; chỉ đọc + phán.

    python3 bin/check_pipeline.py                 # quét mọi */pipeline/ship.json trong repo
    python3 bin/check_pipeline.py <file.json> ...  # kiểm đúng các file chỉ định

Mỗi ship.json GO được soi 3 điều HARD (FAIL) + cảnh báo (WARN):
  FAIL  A  chưa ký / chữ ký lệch sha (<ship>.sign.json)
  FAIL  B  artifact_path trỏ file không tồn tại
  FAIL  C  GO vô-điều-kiện nhưng uat.json cạnh đó uat_signoff=false (chữ ký ngược)
  WARN     nguồn thượng nguồn (uat/delivery/skeleton.json) không thấy cạnh ship.json

Exit code = số FAIL (0 = sạch) — cắm được vào script/CI chạy tay.
Presence gate: chứng minh bước-ký ĐÃ CHẠY, không chứng minh ai ký (xem gatelib).
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gatelib as G  # noqa: E402


def _is_go(ship):
    q = str(ship.get("quyet_dinh") or "").strip().lower()
    st = str(ship.get("trang_thai") or "").strip().lower()
    return q in G.VERDICTS_GO or st == "da_go"


def check_ship(path):
    """Trả (fails[], warns[], skipped_reason|None)."""
    ship, err = G.load_json(path)
    if err:
        return [], [], "đọc lỗi: %s" % err
    if not isinstance(ship, dict):
        return [], [], "không phải object JSON"
    if not _is_go(ship):
        return [], [], "không phải GO (quyet_dinh=%r) — không gác" % ship.get("quyet_dinh")

    fails, warns = [], []
    cond = str(ship.get("quyet_dinh") or "").strip().lower() == "go_co_dieu_kien"
    root = G.project_root()
    ship_dir = Path(path).parent

    # A. chữ ký
    state, sign = G.read_sign(path)
    if state == "UNSIGNED":
        fails.append("A chưa ký — thiếu %s.sign.json (ký: python3 bin/sign_gate.py %s --verdict go)"
                     % (Path(path).name, G.rel(path)))
    elif state == "STALE":
        fails.append("A chữ ký LỆCH SHA — ship.json sửa sau khi ký; ký lại nếu cố ý")
    elif state == "BADSIGN":
        fails.append("A .sign.json hỏng/thiếu artifact_sha256")
    elif state == "SIGNED" and str(sign.get("verdict") or "").lower() not in G.VERDICTS_GO:
        fails.append("A chữ ký verdict=%r không phải go/go_co_dieu_kien" % sign.get("verdict"))

    # B. artifact_path tồn tại
    ap = ship.get("artifact_path") or ship.get("artifact")
    if ap and not (root / ap).exists():
        fails.append("B artifact_path '%s' KHÔNG tồn tại — GO trên artifact rỗng" % ap)

    # C. chữ-ký-ngược với uat.json
    uat_p = ship_dir / "uat.json"
    if uat_p.is_file():
        uat, _ = G.load_json(uat_p)
        if isinstance(uat, dict) and uat.get("uat_signoff") is False and not cond:
            fails.append("C GO vô-điều-kiện nhưng uat.json.uat_signoff=false — chữ ký ngược "
                         "(đặt quyet_dinh='go_co_dieu_kien' nếu là GO có điều kiện)")

    # WARN nguồn thượng nguồn
    for name in ("uat.json", "delivery.json", "skeleton.json"):
        if not (ship_dir / name).is_file():
            warns.append("thiếu %s cạnh ship.json (nguồn thượng nguồn)" % name)
    return fails, warns, None


def discover(root):
    out = []
    for p in root.rglob("pipeline/*ship.json"):
        if ".git" in p.parts:
            continue
        out.append(p)
    return sorted(out)


def main():
    args = sys.argv[1:]
    root = G.project_root()
    targets = [Path(a) for a in args] if args else discover(root)
    if not targets:
        print("không thấy ship.json nào để kiểm.")
        return 0
    total_fail = 0
    for t in targets:
        fails, warns, skip = check_ship(t)
        rel = G.rel(t)
        if skip:
            print("—  %s  (%s)" % (rel, skip))
            continue
        if fails:
            total_fail += len(fails)
            print("✗  FAIL  %s" % rel)
            for f in fails:
                print("        · %s" % f)
        else:
            print("✓  OK    %s" % rel)
        for w in warns:
            print("        ⚠ %s" % w)
    G.trace("check_pipeline", status=("FAIL" if total_fail else "OK"),
            note="%d file, %d fail" % (len(targets), total_fail))
    print("\n%d file kiểm · %d FAIL" % (len(targets), total_fail))
    return total_fail


if __name__ == "__main__":
    sys.exit(main())
