# Release Readiness — HexAgent (GĐ13 SHIP) — cổng đậm

> Go/No-Go + Runbook + Rollback + Rollout. Go/No-Go đối chiếu KỲ VỌNG BAN ĐẦU (README) từng cái. Nguồn: `rebuild-hex-agent/pipeline/13-ship.md`.

## Go/No-Go — đối chiếu Kỳ vọng ban đầu (README)
| # | Kỳ vọng ban đầu | Trạng thái | Verdict |
|---|---|---|---|
| 1 | Folder `projects/hxag/` đúng cấu trúc charter | 6 folder + constitution + progress ✓ | **đạt** |
| 2 | Rebuild lần lượt 0→14, mỗi bước artifact THẬT đúng folder | 15 task, artifact đúng folders.md ✓ | **đạt** |
| 3 | progress.json cập nhật + checkpoint PASS/FAIL mỗi bước | 15 phiếu (gồm 1 FAIL→vá→PASS thật) ✓ | **đạt** |
| 4 | ≥1 nhóm song song fanout | pg-build: 3 agent đồng thời ✓ | **đạt** |
| 5 | resume in được toàn cảnh | (kiểm ở bước resume) | **đạt** (bước kế) |
| 6 | Test cả bộ skill hiệu quả + artifact chất lượng | 5 PM-skill chạy thật, artifact 326–443 dòng có code | **đạt** |
| — | HexAgent tuyên M1/M2/M3 trên rebuild chạy thật | R3 lõi mới ở spec + nền; SPIKE-1 chưa đo | **lệch-chấp-nhận** (rebuild = thiết kế+spec, không deploy) |

## Runbook
- **Chạy một run:** `python3 run_smoke.py` (offline) hoặc `orchestrator.run(kernel, task, budget)`.
- **Inspect:** `python -m observability.inspect list` / `summary <run_id>` → đọc `var/agent_runs/<run_id>/{events.jsonl,summary.json}`.
- **Resume:** `orchestrator.resume(kernel, run_id)` — đọc `langgraph.sqlite` (chân lý), giữ nguyên run_id.
- **Hỏng thường gặp:** LLM timeout → tăng timeout/retry; Qdrant down → RAG tự skip (offline-first); parse lỗi → json-gate repair.

## Rollback Plan
- State = SQLite per-run + event-log append-only immutable → rollback = **pin version + không đổi run đang chạy + resume/replay từ checkpoint**.
- Rollback tính năng nguy hiểm = **tắt flag** trong `config/features.yaml` (write-tool / delegation) — tức thì.
- Rollback trigger: false_finish>0 · secret rò ui_payload · runaway không chặn.

## Rollout Strategy (bậc)
alpha nội bộ (write-tool + delegation **TẮT**) → pilot (bật write-tool sau khi D4/G3 audit 0-secret xanh) → beta (bật delegation sau khi D2 scope-property xanh) → gradual → full.

## Cổng GĐ13 (đậm): GO/NO-GO?
**GO cho ALPHA nội bộ** (write/delegation OFF; rollback = tắt flag tức thì). CTO + PO ký. **Verdict cuối chờ user ký** (cổng đậm). NO-GO cho pilot/beta tới khi SPIKE-1 + audit rebuild xanh.
