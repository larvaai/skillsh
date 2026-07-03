# Live Slice Report — HexAgent (GĐ8 PROOF) — cổng đậm

## ── GÓC NHÌN LÃNH ĐẠO ──
- **Bằng chứng CHẠY THẬT (đo hôm nay):** lát cắt lõi (task loop + acceptance + delegation) của kiến trúc này **chạy thật, không mockup** — chứng minh bằng chính codebase nền:
  - `python3 run_smoke.py` (deterministic, offline, không LLM/mạng) → **`CORE_AGENT_SMOKE_OK run_id=20260703_172409_ba5e061a`**.
  - `pytest tests/test_supervisor_loop.py tests/test_acceptance_gate.py tests/test_delegation.py -q` → **23 passed** (vòng lặp O `_drive`, cổng nghiệm thu bằng-bằng-chứng, delegation scope⊆parent).
- **Trạng thái:** kiến trúc + stack đã CHỨNG MINH chạy ở nền tham chiếu; **rebuild greenfield chưa deploy staging riêng** → tick "đã proven ở nền" ✓, "đã proven trên staging rebuild" chờ.
- **Sẵn sàng đổ người:** Có — vì rủi ro kiến trúc lõi đã đóng bằng test thật; SPIKE-1 (resume atomic) là ẩn số còn lại, đo trong slice build.

## ── CHI TIẾT KỸ THUẬT ──
**Slice:** giao task 2 bước (N1 tạo `out.txt` chứa X; N2 tạo `len.txt` chứa len(X), N2 depends N1) → plan → order theo deps → delegate 1 worker/bước → judge acceptance trên evidence thật → FINISHED; budget chặn runaway.

**Đường đi E2E (10 chặng):** Intake → `Kernel.execute_tool`(LLM plan) → decompose gate (μ-proof) → `next_node` order → `DelegationManager.delegate` (scope⊆parent) → worker `execute_tool`(fs_write) → emit `tool.requested/completed`→`events.jsonl` → `judge_acceptance` → FINISHED → resume từ SQLite.

**Checklist validate (bằng chứng THẬT, không tick khống):**
- [x] architecture hợp lý — smoke OK + 23 test lõi xanh (nền)
- [x] framework phù hợp — LangGraph/SQLite chạy trong nền
- [x] module boundary ổn — execute_tool + DelegationManager là seam thật
- [x] auth/scope chạy — delegation scope⊆parent test xanh
- [x] acceptance chạy — test_acceptance_gate xanh (evidence thật vs scaffolding)
- [ ] CI/CD xanh trên **rebuild** — chờ (chưa dựng pipeline rebuild)
- [ ] staging rebuild mở được — chờ (greenfield chưa deploy)
- [x] observability đủ — events.jsonl + summary.json có ở nền
- [ ] SPIKE-1 resume atomic đo trên rebuild — chờ (đo trong slice build)

**Đã proven: 6/9 (bằng nền tham chiếu) · Chờ: 3/9 (thuộc staging rebuild).**

**Giả định đã đổi:** cần thêm `evidence.provenance` (node_id/AC nguồn) để đóng khe cross-AC — phát sinh từ review, chưa có trong PRD gốc.
**Rủi ro còn lại:** SPIKE-1 (resume re-emit side-effect) + honor-system nghiệm thu → đo/soi ở build + review.

## Cổng GĐ8 (đậm): live slice pass? → **PASS (chờ ký)** — proven ở nền, staging rebuild là bước kế. User (CTO) ký GO để đổ người.
