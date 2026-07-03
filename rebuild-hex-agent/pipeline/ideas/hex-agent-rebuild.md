# hex-agent-rebuild — bản rút gọn Business → Domain

> Bản slim của `pipeline/05-idea-domain.md`. Anchor: `00-understanding/REBUILD-BRIEF.md` + evidence-A/B/C.

## Góc nhìn lãnh đạo
Agent tự-điều-phối: giao 1 task → tự plan → chia bước có thứ tự → delegate cho sub-agent → **chỉ FINISHED khi mọi tiêu chí nghiệm thu có bằng chứng thật**, và **không chạy vô hạn**. Rebuild sạch của `hex_agent`, giữ nguyên vòng lặp lõi. Điểm bán = diệt "báo-xong-khống" và "runaway/leo-thang-quyền".

## Business (WHY)
- **Đau:** false-finish (báo xong khống → làm lại, mất niềm tin) + runaway (đốt token không biên).
- **Success metric M1 (gate):** zero false-finish — 0 lần FINISHED khi có AC thiếu evidence thật (`all_accepted()` = mọi AC passed ∧ evidence≠∅, `state.py:35-37`).
- **Phụ:** M2 bounded (luôn tới terminal ≤ max_rounds), M3 no-escalation (0 delegation scope con ⊄ cha).
- **Cổng GĐ1: GO.** Cơ chế gốc đã chạy (rủi ro thấp); false-finish & bounded là khác biệt sản phẩm.
- Open-Q: OQ-1 baseline chi phí/false-finish thực chưa có số → Operate (không bịa).

## Product / PRD (WHAT)
- **MVP = "Giao 1 task, agent plan + delegate + finish CÓ BIÊN"**: accept → decompose(+gate-2 chứng minh dừng μ co ngặt) → order(next_node) → delegate(scope-check) → judge(evidence) → finish/blocked. Nền: một chokepoint `execute_tool`, event-log-first, SQLite=chân lý resume.
- **Scope OUT:** Control-Tower UI + transport + approval B2–B14, RAG(E08), Skills(E07), Departments/IntentRouter/Factory/Ledger/Labs (park-with-trigger), enforcement authz đầy đủ.
- **NFR (số):** per-delegation max_steps=100/max_depth=8; decompose MAX_DEPTH=6, K=3/K_LEAF=5; 0 secret trong ui_payload (15 SECRET_KEYS); resume SQLite-truth 0 side-effect; seq monotonic gap-free; replay=snapshot deterministic.
- **Cổng GĐ2–4: GO ×2.** MVP cắt đúng lõi; PRD neo file:line, open-Q có chỗ chốt.

## Domain (WORLD MODEL) — DỪNG ở đây
- **6 Bounded Context:** Orchestration · Execution Core · Discipline · Tools&Safety · Observability/Control-Plane · Knowledge(optional).
- **Entities (identity+lifecycle):** Task/Goal · Plan · Node(work|reduce) · DoneWhen · DependencyEdge · Run · Session/SessionIdentity · Delegation · AcceptanceCriterion · Evidence · Budget · Event · Command · Checkpoint · Permission.
- **5 Rule BẤT BIẾN:** (1) chỉ FINISHED khi mọi AC có evidence thật; (2) worker không tự ghi verdict — chỉ gate ghi; (3) scope child ⊆ parent; (4) plan phải có chứng minh dừng μ co ngặt; (5) mọi hành động qua execute_tool.
- **6 Domain Event:** TaskAccepted → PlanDecomposed → NodeDelegated → AcceptanceJudged → TaskFinished / TaskBlocked.
- **Data ownership:** cây kế hoạch+AC+Evidence → Orchestration; session state+lineage → Execution Core; event/command/redaction → Observability/Control-Plane; SQLite resume-truth → Orchestration/graph; budget → Discipline/Delegation; sandbox+policy → Tools&Safety.
- **Cổng GĐ5: GO — Domain đủ rõ để định hình kiến trúc → DỪNG.**

## Bàn giao
→ /shape + /stack (GĐ6+, có Domain đầu vào) · /frame (build 1 slice) · /explain (ATLAS đã dựng).
Open-Q sang shape: OQ-2 danh mục event/command, OQ-3 reconcile tên event, ranh giới v0 vs full.
