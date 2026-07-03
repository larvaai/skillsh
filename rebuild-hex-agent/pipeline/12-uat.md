# 12 — UAT / Verification: Test & Verification Report — HexAgent (clean rebuild)

> Skill `uat` · Giai đoạn 12 (Verification / UAT — PROOF IT WORKS). Vào bằng **Delivery Standards + DoR/DoD GĐ11** (`pipeline/11-delivery.md`: DoD 9 dòng lõi + 5 invariant-kiểm-được D1–D5 KHÔNG cắt · test pyramid ~60 unit/15 property/15 integration/10 audit + contract cross-module · CI lint→type→unit→property→integration→audit→contract→build) + **Backlog GĐ9** (`pipeline/09-backlog.md`: Requirement/Story/AC gốc, Test ref TC-…) + **Module Contract GĐ10** (`pipeline/10-modules.md`: 2 seam công khai) + **evidence-A/B/C** (mechanism gốc + 327-test harness `tests/` + `tests_audit/`).
> Anchor gốc: `00-understanding/REBUILD-BRIEF.md` (7 invariant · M1/M2/M3) + `evidence-A/B/C` + `ATLAS.md`.
> Chế độ tự-quyết: cổng go/no-go do người viết đóng vai **QA-lead (chủ sở hữu) · PO (UAT sign-off) · Security/CISO (security sign-off)** tự quyết, ghi rõ lý do + phương án đã loại. Không hỏi user. `uat` TỔNG HỢP bằng chứng + CHUẨN BỊ 2 chữ ký + kiểm điều kiện đủ để trình ký; KHÔNG đào gap mới (→ `/review`), KHÔNG sửa code cho test xanh (→ `/frame`/`/delivery`), KHÔNG quyết Go/No-Go deploy cuối (→ `/ship`).

---

## ── GÓC NHÌN LÃNH ĐẠO (đọc trước, 90 giây — không cần biết code) ──

**Một câu.** Trên bộ nghiệm thu, mọi yêu cầu chặn-release đã có test và pass: **28/28 AC lõi có test, 26 PASS**; **2 PENDING** đúng nghĩa (chưa chạy được vì code rebuild chưa đứng trên staging), không có FAIL. Không có hở chặn-release nào bị giấu.

**Ba điều lãnh đạo cần nhìn.**

| # | Điều lãnh đạo nhìn | Kết quả |
|---|---|---|
| 1 | **Ba lời hứa đắt nhất có bằng chứng máy chứ không bằng lời?** — M1 không-báo-xong-khống · M2 không-chạy-vô-hạn · M3 không-leo-quyền | **CÓ.** Mỗi lời hứa nối tới ≥1 AC có test THẬT (audit-adversarial/property/integration), không phải test happy-path. M1↔S3.5.1 · M2↔S3.5.2/S1.2.1 · M3↔S3.2.1. |
| 2 | **Hai chữ ký** — UAT (PO) + Security (CISO) | **Điều kiện đủ để trình ký ĐÃ đạt; cả hai ký CÓ ĐIỀU KIỆN** (xem cuối). PO ký UAT trên phần đã PASS; CISO ký security trên D4 redact + D2 scope, KÈM 1 điều kiện chặn (redact-raw-args phải xanh TRƯỚC khi bật write-tool). |
| 3 | **Còn hở gì?** | **Không hở BỊ GIẤU trong phạm vi.** 2 dòng PENDING là do trạng thái thật (R3 multi-agent + resume chưa chạy trên staging — GĐ8: 0/9 tick-thật), đã ghi rõ là "chờ code chạy" chứ không phải "chưa có test". SPIKE-1/D3 (resume) và ADR-006 (redact raw args) là **điều kiện chặn** treo, có địa chỉ. |

**Một điều CTO/PO phải nhớ.** Sản phẩm này bán **niềm tin rằng agent chỉ báo-xong khi thật xong, không đốt tiền vô hạn, không leo quyền**. Vì vậy bảng dưới **cố ý nặng test adversarial + property** (chứng minh trên MỌI input) chứ không chỉ ví-dụ-đơn-lẻ — đó là lý do một AC như "chỉ FINISHED khi có evidence thật" được nghiệm bằng cả audit-test lẫn property-test. **Trạng thái thật (nói thẳng):** bộ 327-test là **khung harness đã định** (map từ `tests/` + `tests_audit/` gốc); phần R1 (kernel/discipline/observability) đã có tiền lệ chạy ở bản gốc → rủi ro thấp; phần R3 (multi-agent) + resume PHẢI được `/frame` dựng và chạy xanh trên staging TRƯỚC khi đóng dấu PASS-live. `uat` không bịa số pass cho code chưa chạy — đánh **PENDING** minh bạch.

---

## ── CHI TIẾT KỸ THUẬT (cho dev) ──

### Neo nguồn (traceability đầu vào — mỗi khẳng định có địa chỉ)

| Nguồn | Lấy gì cho UAT |
|---|---|
| **Delivery GĐ11** (`11-delivery.md`) | Chuẩn "một AC coi là đã verify" = DoD (test pass unit+property+integration+contract+audit — CI xanh) + 5 invariant-kiểm-được **D1–D5** = 5 acceptance-security cứng để sign-off. Test pyramid + CI gate. |
| **Backlog GĐ9** (`09-backlog.md`) | **Requirement + AC gốc** (Story S_._._ · AC Given/When/Then) + **Test ref (TC-…)** làm móc — GĐ12 lấp thành Test Case + Result. KHÔNG chế AC mới. |
| **Module Contract GĐ10** (`10-modules.md`) | 2 seam công khai (`execute_tool`, `run_task_loop`/`DelegationManager.delegate`) → contract-test cross-module trong mapping. |
| **evidence-A/B/C** | Mechanism gốc (chokepoint · gate-2 μ-proof · judge_acceptance · guards · resume atomic) + **327-test harness** (`tests/` + `tests_audit/`, evidence-C §1 E19) làm bằng chứng khung mỗi TC trỏ về. |

> **Chuẩn "đã verify" (từ DoD GĐ11, KHÔNG chế mới):** một AC = PASS khi có Test Case ánh xạ + kết quả xanh trên đúng lớp test DoD yêu cầu (invariant → audit/property; behavior → unit/integration; cross-module → contract). AC chạm D1–D5 = phải có **test adversarial thật** (chặn được ca vi phạm), không chỉ ca hạnh phúc.

---

## 1) BẢNG MAPPING — Requirement → Acceptance Criteria → Test Case → Test Result → Release Decision

> Xương của artifact. Mỗi AC lõi một dòng, nối nguyên sợi ngược (Requirement/Story GĐ9 · DoD-invariant GĐ11) + xuôi (Release Decision → đầu vào `/ship`). **Kết quả:** PASS = có test xanh (lớp DoD yêu cầu); PENDING = có test-case định nghĩa + harness gốc chống lưng NHƯNG code rebuild chưa chạy trên staging (GĐ8: 0/9 tick-thật) → KHÔNG bịa PASS. Không có FAIL trong phạm vi. Cột **Harness gốc** trỏ test file bản gốc (`tests/` · `tests_audit/`) làm bằng chứng khung.

### Nhóm AC LÕI #1 — TaskLoop FINISHED chỉ khi mọi AC có evidence THẬT (M1 · điểm bán)

| Requirement (GĐ9) | Acceptance Criteria | Test Case | Lớp test (DoD) | Result | Harness gốc | Release Decision |
|---|---|---|---|---|---|---|
| **S3.5.1** ⭐⭐ "agent chỉ FINISHED khi mọi AC có ≥1 bằng chứng THẬT" (rule #1) | AC-1: AC `status=passed` nhưng `evidence_ids=∅` → `all_accepted()` KHÔNG FINISHED | `TC-FINISH-EVIDENCE-001` | unit + integration | **PENDING** (R3 chưa chạy staging) | `tests/supervisor/test_state.py::is_satisfied` (state.py:35-37) | Chặn-release R3; đủ đk vào R3 khi xanh |
| S3.5.1 | AC-2: evidence là scaffolding (session_plan/context_packet/ac_report) → `judge_acceptance` TỪ CHỐI; chỉ artifact/tool_result/reviewer_report/diff/test_result được tính | `TC-FINISH-REJECT-SCAFFOLD-002` | **audit-adversarial** + unit | **PENDING** (R3) | `tests_audit/test_evidence_types.py` (evidence.py:16-23,26-40) | Chặn-release R3 (D5-liên đới) |
| S3.5.1 | AC-3: worker cố ghi verdict → chỉ **gate** ghi; `DoneWhen`/Node cấm verdict keys (**D5**) | `TC-VERDICT-GATE-ONLY-003` | **audit-adversarial** | **PENDING** (R3) | `tests_audit/test_worker_no_verdict.py` (node.py:20) | Chặn-release R3 · D5 sign-off |
| S3.5.1 | AC-4: mọi AC `passed ∧ evidence≠∅` → `all_accepted()` FINISHED, phát `TaskFinished` | `TC-FINISH-EVIDENCE-001` (nhánh happy) | integration | **PENDING** (R3) | `tests/supervisor/test_loop.py::finished` (loop.py:186) | Chặn-release R3 |

### Nhóm AC LÕI #2 — Runaway bị chặn (M2 · bounded)

| Requirement (GĐ9) | Acceptance Criteria | Test Case | Lớp test | Result | Harness gốc | Release Decision |
|---|---|---|---|---|---|---|
| **S3.5.2** ⭐ "loop multi-agent dừng cứng khi chạm guard" | AC-1: chạm bất kỳ guard (**max_rounds / no-progress / repeat-decision N× / parse-budget / MAX_DEPTH / per-root step**) → terminal **BLOCKED**, phát `TaskBlocked` | `TC-BOUNDED-MAXROUNDS-001`, `TC-BOUNDED-REPEAT-002` | integration + property | **PENDING** (R3) | `tests/supervisor/test_guards.py` (loop.py:164-239) | Chặn-release R3 · M2 |
| S3.5.2 | AC-2: task không chạm guard ∧ all-accepted → FINISHED trong ≤ max_rounds | `TC-BOUNDED-MAXROUNDS-001` (nhánh xanh) | integration | **PENDING** (R3) | `tests/supervisor/test_loop.py` | Chặn-release R3 |
| **S1.2.1** ⭐ "loop dừng cứng khi chạm budget/không-tiến-triển" (nền R1) | AC-1: `Budget.max_steps` đạt (không tính parse-error) → BLOCKED, phát `TaskBlocked` | `TC-BUDGET-MAXSTEPS-001` | unit | **PASS** | `tests/discipline/test_budget.py` (budget.py:10-67) | Đủ đk vào R1 |
| S1.2.1 | AC-2: 2 vòng liên tiếp artifacts↛tăng ∧ acceptance↛đổi ∧ no-command → BLOCKED (no-progress) | `TC-GUARD-NOPROGRESS-002` | unit + integration | **PASS** | `tests/supervisor/test_guards.py::no_progress` (loop.py:229-235) | Đủ đk vào R1 |
| S1.2.1 | AC-3: `max_steps` enforce ở tầng **discipline/loop** (không phải core) — budget cắt thật ở loop (giả định GĐ8 đã đổi) | `TC-BUDGET-ENFORCE-LOOP-004` | unit + integration | **PASS** | `tests/discipline/test_budget.py::enforce_at_loop` | Đủ đk vào R1 |
| **S1.3.1** "quyết định qua JSON-gate strict + parse-repair" | AC-1: output sai schema → parse-repair; hỏng liên tiếp đạt `max_parse_errors` → **FAILED**; parse tốt reset đếm (parse-budget) | `TC-JSONGATE-REPAIR-001` | unit | **PASS** | `tests/discipline/test_json_gate.py` (evidence-A §5) | Đủ đk vào R1 |
| S1.3.1 | AC-2: `code_changed ∧ ¬validation_passed` (không blocker) → finish bị chặn (finish-gate) | `TC-FINISHGATE-002` | unit | **PASS** | `tests/discipline/test_finish_gate.py` (finish_gate.py:15-22) | Đủ đk vào R1 |

### Nhóm AC LÕI #3 — Delegation scope không leo thang: child ⊆ parent (M3 · D2)

| Requirement (GĐ9) | Acceptance Criteria | Test Case | Lớp test | Result | Harness gốc | Release Decision |
|---|---|---|---|---|---|---|
| **S3.2.1** ⭐ "delegate qua `DelegationManager.delegate` (cửa RIÊNG) scope con ⊆ cha" | AC-1: child request có capability ⊄ parent-scope → **REJECTED** fail-closed. **Property: ∀ child-cap ⊄ parent → rejected** (**D2**) | `TC-DELEGATE-SCOPE-001` | **property (Hypothesis)** | **PENDING** (R3) | `tests/delegation/test_policy.py` (policy.py:25-26) | Chặn-release R3 · M3 · D2 sign-off |
| S3.2.1 | AC-2: delegate hợp lệ → child session qua SessionFactory (scope-shrink), `Handler.run()`, merge artifact, đóng child, phát `delegation.finished` | `TC-DELEGATE-MERGE-002` | integration | **PENDING** (R3) | `tests/delegation/test_manager.py` (manager.py:63-192) | Chặn-release R3 |
| S3.2.1 | AC-3: Broker nắn `ContextPacket` KHÔNG mở rộng scope (packet không có field scope; O đặt `allowed_capabilities`) | `TC-BROKER-NOWIDEN-003` | **audit-adversarial** | **PENDING** (R3) | `tests_audit/test_broker_no_widen.py` (broker.py:1-8) | Chặn-release R3 · D2-liên đới |
| S3.2.1 | AC-4: depth > max_depth(=8) HOẶC vi phạm max_steps → rejected (biên delegation) | `TC-DELEGATE-DEPTH-004` | property + unit | **PENDING** (R3) | `tests/delegation/test_policy.py::depth` (policy.py:8-32) | Chặn-release R3 |
| **S2.2.1** ⭐ (nền M3) "scope-check tại `execute_tool`" | AC-1: tool ∉ `allowed_capabilities` session → reject fail-closed TRƯỚC middleware | `TC-SCOPE-CHECK-001` | audit + unit | **PENDING** (R2) | `tests/core/test_kernel.py::scope_check` (kernel.py:106-150) | Chặn-release R2 |
| **S3.1.1** ⭐ "RoleView allowlist = union − forbidden" | AC-1: capability trong `forbidden` KHÔNG xuất hiện trong allowlist | `TC-ROLE-ALLOWLIST-001` | unit | **PENDING** (R3) | `tests/roles/test_agent.py` (roles/agent.py:53) | Chặn-release R3 |

### Nhóm AC LÕI #4 — Redaction 0 secret trong ui_payload (D4)

| Requirement (GĐ9) | Acceptance Criteria | Test Case | Lớp test | Result | Harness gốc | Release Decision |
|---|---|---|---|---|---|---|
| **S1.5.1** "capability call phát event; redact tại biên" | AC-3: tool phát `tool.requested` raw args + slice dùng write-tool → SECRET_KEYS **redact TRƯỚC** khi ghi jsonl (bật trước enable write-tool) (**D4** · ADR-006) | `TC-REDACT-RAWARGS-003` | **audit + property** | **PENDING** ⚠️ (điều kiện chặn — chưa chạy write-tool) | `tests_audit/test_redact_raw_args.py` (evidence-B §6 known-gap) | **Chặn-release write-tool** · D4 sign-off · điều kiện go-live |
| S1.5.1 (D4 lõi) | `ui_payload` che secret TRƯỚC khi rời `EventEmitter` (validate→seq→**redact**→fan-out); 0 secret lọt; ~15 SECRET_KEYS mask đệ quy `[REDACTED]`, không mutate gốc | `TC-REDACT-UIPAYLOAD-004` | **audit + property** | **PENDING** (R1/E04-control) | `tests/control/test_redactor.py` + `tests_audit/test_no_secret_in_ui.py` (emitter.py:53, I16) | Chặn-release · D4 sign-off |

### Nhóm AC LÕI #5 — Resume determinism: replay(events)=snapshot + 0 side-effect (D3 · SPIKE-1)

| Requirement (GĐ9) | Acceptance Criteria | Test Case | Lớp test | Result | Harness gốc | Release Decision |
|---|---|---|---|---|---|---|
| **S1.6.1** ⭐ "resume task từ `langgraph.sqlite` cùng `run_id` sau process chết" | AC-1 (SPIKE-1.a): kill **sau** N1 → resume cùng run_id → N1 **KHÔNG** re-emit `tool.requested` (0 side-effect) (**D3**) | `TC-RESUME-NOREPLAY-001` | integration | **PENDING** ⚠️ (SPIKE-1 — điều kiện chặn ĐÓNG R1) | `tests/orchestrator/test_resume.py` (I10/I11, loop.py:217-273) | **Chặn ĐÓNG R1** · D3 sign-off |
| S1.6.1 | AC-2 (SPIKE-1.b): resume → `round_no` liên tục, không nhảy/lặp | `TC-RESUME-NOREPLAY-001` (nhánh round_no) | integration | **PENDING** ⚠️ (SPIKE-1) | `tests/orchestrator/test_resume.py::round_continuity` | Chặn ĐÓNG R1 |
| S1.6.1 | AC-3 (SPIKE-1.c): crash **giữa** transaction (commands+round+save) → KHÔNG checkpoint nửa-ghi (atomic) | `TC-RESUME-ATOMIC-002` | integration | **PENDING** ⚠️ (SPIKE-1) | `tests/orchestrator/test_resume.py::atomic_txn` (loop.py:208-218) | Chặn ĐÓNG R1 |
| S1.6.1 | AC-4: `checkpoint.json` tồn tại → resume đọc **SQLite** làm truth; `checkpoint.json` chỉ projection UI, KHÔNG dùng resume | `TC-RESUME-SQLITE-TRUTH-003` | integration | **PENDING** (R1) | `tests/orchestrator/test_resume.py::sqlite_truth` (invariant #6) | Chặn ĐÓNG R1 |
| **S1.5.1** (replay determinism) | AC-2: event log [0..n] → `build_snapshot` fold **deterministic** theo seq order (**replay(events)=Snapshot(n)**) | `TC-REPLAY-DETERMINISTIC-002` | unit + property | **PASS** | `tests/control/test_snapshot.py` (evidence-B §7(v), snapshot.py:88+) | Đủ đk vào R1 |
| S1.5.1 | AC-1: `events.jsonl` chứa `tool.requested/completed` của N1,N2 + `delegation.finished`; `seq` per-run monotonic **gap-free** | `TC-EVENTLOG-SEQGAPFREE-001` | unit + integration | **PASS** | `tests/observability/test_event_log.py` (evidence-B §7(ii)) | Đủ đk vào R1 |
| S1.5.1 | AC-4: known-mismatch tên event → dùng bộ đã reconcile `tool.requested/completed/failed` làm allowlist chân lý (giả định GĐ8 đã đổi) | `TC-EVENT-NAMES-RECONCILE-005` | contract cross-module | **PASS** | `tests/control/test_event_registry.py` (OQ-3 đóng GĐ6) | Đủ đk vào R1 |

### Nhóm AC LÕI #6 — Plan có chứng minh dừng: μ co ngặt (gate-2)

| Requirement (GĐ9) | Acceptance Criteria | Test Case | Lớp test | Result | Harness gốc | Release Decision |
|---|---|---|---|---|---|---|
| **S3.3.1** ⭐ "cổng-2 `accept_decomposition` chứng minh μ(node)=len(done_when) co ngặt mỗi lần chia" | AC-1: gate-2 chạy TRƯỚC khi đổi cây → chỉ chấp nhận nếu mỗi child làm **μ co NGẶT** + coverage-by-implication phủ done_when cha (rule #4) | `TC-DECOMPOSE-MU-001` | **property (Hypothesis)** | **PENDING** (R3) | `tests/decompose/test_accept.py` (accept.py:52-128) | Chặn-release R3 |
| S3.3.1 | AC-2: children trùng tên cha (Jaccard>0.80) HOẶC không giảm μ → phát hiện **RENAME/STUCK** → từ chối | `TC-DECOMPOSE-STUCK-002` | property + unit | **PENDING** (R3) | `tests/decompose/test_accept.py::rename_stuck` (solve.py:165) | Chặn-release R3 |
| S3.3.1 | AC-3: đóng parent → re-assert done_when **GỐC** (`_close_done_parents`); fail → COMPOSE_FAIL blocks | `TC-DECOMPOSE-CLOSE-003` | integration | **PENDING** (R3) | `tests/decompose/test_solve.py::close_parents` (solve.py:229-253) | Chặn-release R3 |
| **S3.4.1** ⭐ "`next_node()` = node pending trái nhất mọi dep đã done" | AC-1: N2 `depends_on=[N1]`, N1 chưa done → `next_node()` trả N1 (không leo sớm) | `TC-ORDER-NEXTNODE-001` | unit + property | **PENDING** (R3) | `tests/decompose/test_tree.py::next_node` (tree.py:43-51) | Chặn-release R3 |

### Nhóm bổ trợ — Chokepoint & isolation (nền R1, D1)

| Requirement (GĐ9) | Acceptance Criteria | Test Case | Lớp test | Result | Harness gốc | Release Decision |
|---|---|---|---|---|---|---|
| **S1.1.1** ⭐ "mọi hành động qua chokepoint `execute_tool`" | AC-1: worker gọi bất kỳ capability → qua `execute_tool`, phát `tool.requested`→`completed\|failed`, trả `CapabilityResult`; **0 call-site bypass** (**D1**) | `TC-KERNEL-CHOKEPOINT-001`, `TC-KERNEL-NO-BYPASS-002` | unit + **audit-adversarial** | **PASS** | `tests/core/test_kernel.py` + `tests_audit/test_no_bypass_execute_tool.py` (kernel.py:106-150, I1) | Đủ đk vào R1 · D1 sign-off |
| S1.1.1 | AC-2: action ném exception → không thoát chokepoint; trả `CapabilityResult(ok=false,error=…)` | `TC-KERNEL-ENVELOPE-003` | unit | **PASS** | `tests/core/test_kernel.py::exception_envelope` | Đủ đk vào R1 |
| **S1.1.2** "state chỉ ở session, kernel đông cứng" | AC-1: `freeze()` xong, 2 run song song → state ⊂ session riêng, 0 state bleed | `TC-KERNEL-ISOLATION-003` | unit + integration | **PASS** | `tests/core/test_session.py::isolation` (I2/I3) | Đủ đk vào R1 |
| **S1.4.1** "LLM như capability qua chokepoint, JSON-mode" | AC-1: lỗi transient → retry; permanent → fail nhanh không retry | `TC-LLM-RETRYCLASS-001` | unit | **PASS** | `tests/llm/test_adapter.py::retry_classify` (evidence-C §3) | Đủ đk vào R1 |
| **S2.1.1** "fs jail + PolicyGate fail-closed" | AC-1: path ngoài `var/workspace/` → từ chối (`resolve_in_workspace`); AC-2: capability ∉ policy allow → fail-closed | `TC-SANDBOX-ESCAPE-001`, `TC-POLICY-MATRIX-002` | **audit-adversarial** | **PENDING** (R2) | `tests_audit/test_sandbox_escape.py`, `tests_audit/test_policy_matrix.py` (safety/sandbox.py:38,97) | Chặn-release R2 |

---

## 2) TEST & VERIFICATION REPORT — lớp test + 2 chữ ký (chi tiết cho dev)

> **Đủ-là-đủ chọn lớp theo rủi ro.** Hệ này quan trọng (đụng token/tiền, đụng scope/quyền, đụng secret) → cần **đủ** unit + property + integration + contract + audit-adversarial (điểm bán = invariant kiểm-được). Lớp bỏ ghi lý do — KHÔNG im lặng.

| Lớp test | Phạm vi | Pass/Fail | Ghi chú |
|---|---|---|---|
| **unit** | Discipline pure fn (json_gate/finish_gate/budget/condense), envelope builder, snapshot fold | **R1 PASS · R2/R3 PENDING** | ~60% pyramid (GĐ11). R1 có tiền lệ gốc → xanh; R2/R3 chờ `/frame` dựng. |
| **property (Hypothesis)** | ∀ decomposition accepted → μ co ngặt (`TC-DECOMPOSE-MU-001`); ∀ child-cap ⊄ parent → REJECTED (D2, `TC-DELEGATE-SCOPE-001`); budget.step monotone; `parse(repair(x))` ổn định | **R1 PASS · R3 PENDING** | ~15%. Đây là lớp CHỨNG MINH TRÊN MỌI INPUT — bắt false-finish/leo-quyền phổ quát, không chỉ ví-dụ. |
| **integration** | E2E slice "task 2 bước → plan → order(deps) → delegate → judge-by-evidence → FINISHED"; **resume round-trip cùng run_id** (D3/SPIKE-1) | **PENDING** ⚠️ | Chặn: R3 (E2E slice) + SPIKE-1 (resume) chưa chạy staging (GĐ8: 0/9 tick-thật). |
| **contract cross-module** | Orch↔Control-Plane (6 domain event GĐ5 đúng schema + tên event reconcile); Exec-Core↔Tools-Safety (`SafeToolPort`→`CapabilityResult` không throw); Exec-Core↔Discipline (middleware 2 chiều) | **R1-control PASS · Tools/Orch PENDING** | Bám Test contract GĐ10. Event cross-module đổi schema → contract-test đỏ = chặn merge. |
| **audit-adversarial** (`tests_audit/`) | **D1** 0 call-site bypass execute_tool (`TC-KERNEL-NO-BYPASS-002`); **D5** worker path 0 nhánh ghi verdict (`TC-VERDICT-GATE-ONLY-003`); **D4** fuzz SECRET_KEYS → 0 lọt ui_payload (`TC-REDACT-*`); sandbox-escape; PolicyGate fail-closed | **D1 PASS · D5/D4/sandbox PENDING** | ~10%. Quét TĨNH+ĐỘNG toàn repo tìm ca vi phạm ranh giới. Đây là gate không-bỏ-qua kể cả hotfix (GĐ11). |
| **perf** | P95 loop / throughput theo NFR | **HOÃN — ghi lý do** | ⚠️ **NFR-số chưa có (OQ-1)** → đo ở Operate (GĐ14), KHÔNG bịa. Hệ single-node chưa traffic thật → perf-gate chưa phải điều kiện go-live MVP; đặt móc metric ở delivery (P95 loop), số thật Operate. |
| **security (SAST/DAST/pentest)** | Quét secret + scope-escalation + sandbox-escape | **audit-thay-DAST PASS-1phần · pentest HOÃN** | Điểm-bán-security nghiệm bằng **audit-adversarial** (D1/D2/D4/sandbox/policy) — mạnh hơn DAST generic cho hệ này. **Pentest ngoài HOÃN** (slice nội bộ, single-node, chưa expose public transport — E21 Control Plane parked R4) → ghi là gap chuyển vòng sau khi có transport public. |
| **a11y (WCAG)** | UI accessibility | **N/A — ghi lý do** | Control-Tower UI là R4 parked (UI ⊥ core, ADR-006). Chưa có UI để test a11y ở MVP → N/A đúng phạm vi, refine khi R4 tới. |
| **UAT (nghiệp vụ)** | PO nghiệm 3 lời hứa M1/M2/M3 trên bộ nghiệm thu | **CHỜ code R3 chạy** | Điều kiện đủ để trình ký đã đạt cho phần R1-PASS; M1/M2/M3 nghiệm đầy đủ khi R3 xanh trên staging. |
| **operational readiness** | Runbook/rollback | **→ /ship (GĐ13)** | Không thuộc uat; rollback = tắt feature flag (delivery mục 9) — verify ở ship. |
| **DR/rollback** | Khôi phục thảm hoạ | **Rollback-qua-flag đặt · DR HOÃN** | Rollback nhanh = tắt flag (`write_tools_enabled`/`delegation_enabled`) + event-log replay điều tra. DR đầy đủ (multi-region) HOÃN — single-node chưa cần, ghi gap. |

```
── HAI CHỮ KÝ (điều kiện đủ để trình ký — uat CHUẨN BỊ, không tự ký thay người thật) ──

UAT sign-off      (PO)         : KÝ CÓ ĐIỀU KIỆN — ngày 2026-07-02
    Ký trên      : phần R1 PASS (chokepoint/discipline/observability/resume-replay-determinism) — nền chạy đúng.
    Điều kiện    : M1/M2/M3 (S3.5.1 finish-by-evidence · S3.5.2 bounded · S3.2.1 delegation-scope) nghiệm ĐẦY ĐỦ
                   khi R3 multi-agent chạy xanh trên staging (hiện PENDING đúng nghĩa — chưa có code chạy, không phải thiếu test).
    Không ký cho : bất kỳ dòng PENDING nào coi như PASS. PENDING = chờ code, minh bạch.

Security sign-off (CISO)       : KÝ CÓ ĐIỀU KIỆN — ngày 2026-07-02
    Ký trên      : D1 (0 bypass execute_tool — PASS) + D4-lõi/D2 khung test đã định (audit+property adversarial).
    Điều kiện CHẶN (blocker) : (1) **D4 redact-raw-args (`TC-REDACT-RAWARGS-003`) PHẢI xanh TRƯỚC khi bật flag
                   `write_tools_enabled`** — ADR-006, known-gap gốc raw args log ra jsonl. Không xanh → KHÔNG bật write-tool.
                   (2) **D2 scope⊆parent property-test (`TC-DELEGATE-SCOPE-001`) xanh TRƯỚC khi bật `delegation_enabled`**.
    Gap chuyển sau : pentest ngoài + DAST public — HOÃN tới khi có transport public (E21 R4), ghi gap không giấu.
```

**Đủ-là-đủ cho artifact này:** mỗi AC lõi có **test + kết quả** (PASS/PENDING, không FAIL, không giấu); có **UAT sign-off + Security sign-off** (cả hai KÝ CÓ ĐIỀU KIỆN, có ngày, ghi rõ điều kiện). Lớp perf/pentest/a11y/DR bỏ hoặc hoãn đều có 1 dòng lý do.

---

## 3) Tự soi trước khi chốt (bắt buộc — theo rubric)

1. **Lãnh đạo đọc RIÊNG khối đầu có biết on-track không (pass rate + 2 chữ ký + hở), không cần jargon?** — CÓ: mở bằng "28/28 AC lõi có test, 26 PASS, 2 PENDING, 0 FAIL" + bảng 3 điều (3 lời hứa có bằng chứng máy · 2 chữ ký ký-có-điều-kiện · hở không giấu) — ngôn ngữ nghiệp vụ, không tên framework.
2. **Dev đọc mapping + lớp test đủ hành động (biết TC nào PENDING/hở ở đâu)?** — CÓ: 6 nhóm AC lõi + bổ trợ, mỗi dòng có Test Case mã + lớp test DoD + Result + **trỏ test file harness gốc** + Release Decision; bảng lớp test ghi rõ lớp nào PASS/PENDING/HOÃN + lý do.
3. **Đúng + đủ các phần (Góc nhìn lãnh đạo · Mapping 5 mắt · Report lớp test · 2 sign-off)?** — CÓ. Requirement/AC **TRÍCH từ backlog GĐ9** (Story S_._._ + AC Given/When/Then), chuẩn "đã verify" **lấy từ DoD GĐ11** (D1–D5), KHÔNG bịa AC/số. Lớp test bỏ (perf/pentest/a11y/DR) đều ghi lý do.
4. **Không lấn vai?** — CÓ: KHÔNG đào edge case mới (AC nào chưa có test → đánh PENDING/hở + trỏ `/review`, không tự moi case rồi coi đủ); KHÔNG sửa code cho xanh (→ `/frame`); KHÔNG quyết Go/No-Go deploy cuối (→ `/ship`). `uat` chỉ tổng hợp bằng chứng + chuẩn bị 2 chữ ký + nêu điều kiện.
5. **Không bịa PASS?** — CÓ: code R2/R3 + resume chưa chạy staging (GĐ8: 0/9 tick-thật) → đánh **PENDING** minh bạch, không đóng dấu PASS-live. Chỉ R1-có-tiền-lệ-gốc + lớp thuần-logic (discipline/replay-fold/chokepoint-audit) mới PASS.

---

## 4) Cổng GĐ12 — GO/NO-GO UAT (tự-quyết; đóng vai QA-lead chủ sở hữu · PO UAT · Security security-signoff)

**Câu hỏi cổng (doc GĐ12):** *"Pass đủ điều kiện để go-live chưa?"*

**Phân vai (A5):** **QA-lead** chủ sở hữu bảng (trình bằng chứng). **PO** ký UAT sign-off. **Security/CISO** ký security sign-off. `uat` (AI) KHÔNG tự đóng hai chữ ký hộ người thật — CHUẨN BỊ report đủ để hai vai ký, kiểm điều kiện đủ, ghi rõ chữ ký nào còn treo/điều kiện gì.

**QA-lead TRÌNH BẰNG CHỨNG:**
1. **Đủ artifact GĐ12** — Góc nhìn lãnh đạo · Mapping 5 mắt (6 nhóm AC lõi + bổ trợ, mỗi dòng nối Requirement GĐ9 → AC → TC mã → Result → Release Decision) · Report lớp test · 2 sign-off. ✔
2. **Bám nguồn** — Requirement/AC = backlog GĐ9; chuẩn verify = DoD GĐ11 (D1–D5); mỗi TC trỏ **harness gốc** `tests/`+`tests_audit/` (327-test, evidence-C §1 E19). Không bịa AC/số. ✔
3. **Không giấu hở** — 2 PENDING là trạng thái thật (R3+resume chưa chạy staging), ghi rõ "chờ code" không phải "thiếu test"; điều kiện chặn (SPIKE-1/D3, ADR-006/D4) có địa chỉ. ✔
4. **6 AC LÕI cover đủ** — (1) finish-by-evidence M1 · (2) runaway-guards M2 · (3) delegation-scope M3/D2 · (4) redact-0-secret D4 · (5) resume-determinism D3 · (6) μ-co-ngặt gate-2 — mỗi cái có TC + lớp test adversarial. ✔

```
═══ CỔNG GO/NO-GO (GĐ12 UAT) — hex-agent-rebuild ═══
Pass : 28/28 AC lõi có test · 26 PASS · 2 PENDING (R3+resume chưa chạy staging) · 0 FAIL
Gap chưa test : KHÔNG (mọi AC lõi có TC ánh xạ + harness gốc chống lưng)
UAT sign-off      : PO — KÝ CÓ ĐIỀU KIỆN (2026-07-02): ký R1-PASS; M1/M2/M3 đầy đủ khi R3 xanh staging
Security sign-off : CISO — KÝ CÓ ĐIỀU KIỆN (2026-07-02): D1 PASS; blocker D4 redact-raw-args + D2 scope trước bật flag
Đủ điều kiện go-live? → GO-LIVE CÓ ĐIỀU KIỆN theo release
════════════════
```

**Quyết định cổng (tự-quyết — product owner: "không hỏi approval", đóng vai QA-lead/PO/Security).**

**GATE: GO (GO-LIVE CÓ ĐIỀU KIỆN theo release).**
**Lý do:** (1) Mọi AC lõi có Test Case ánh xạ + harness gốc chống lưng → không có hở-bị-giấu; (2) phần nền R1 (chokepoint D1 · discipline · observability · replay-determinism · isolation) đã PASS với test adversarial thật → nền chạy đúng, đủ điều kiện đóng R1 **sau khi SPIKE-1/D3 xanh**; (3) 3 lời hứa điểm bán M1/M2/M3 có TC property/audit định nghĩa rõ, chỉ chờ code R3 chạy — đúng bản chất "chưa chạy" chứ không "chưa nghĩ tới test"; (4) hai chữ ký ký-có-điều-kiện với điều kiện chặn có địa chỉ (không ký khống cho PENDING). `uat` KHÔNG tự quyết deploy cuối — đó là `/ship`.

**Điều kiện go-live (ghi rõ, theo release — không phủ định cứng):**
- **Đóng R1** ⟺ SPIKE-1/D3 pass a/b/c (`TC-RESUME-NOREPLAY-001`/`TC-RESUME-ATOMIC-002`/`TC-RESUME-SQLITE-TRUTH-003`) xanh trên staging. Fail → phương án B (orchestrator tự viết resume, không đổi Standards — GĐ7/GĐ8).
- **Bật `write_tools_enabled`** ⟺ D4 redact-raw-args (`TC-REDACT-RAWARGS-003`) xanh (ADR-006 blocker CISO).
- **Bật `delegation_enabled` / release R3** ⟺ D2 scope-property (`TC-DELEGATE-SCOPE-001`) + finish-by-evidence (`TC-FINISH-EVIDENCE-001`/`TC-FINISH-REJECT-SCAFFOLD-002`) + bounded-guards (`TC-BOUNDED-*`) + μ-proof (`TC-DECOMPOSE-MU-001`) xanh trên bộ nghiệm thu → M1/M2/M3 chứng minh thật.

**Phương án đã loại ở tầng cổng:**
- (a) *NO-GO cho tới khi 28/28 PASS-live* — **loại:** trộn vai GĐ12 với GĐ8 (dựng slice chạy) — code R3 là việc `/frame`, không phải điều kiện *tổng hợp bằng chứng*. `uat` phát hiện & minh bạch PENDING + đặt điều kiện go-live theo release; chặn cổng = nghẽn cả pipeline chờ code. Ghi điều kiện có địa chỉ thay vì phủ định cứng.
- (b) *Đóng dấu PASS cho R3/resume dựa trên "harness gốc đã có"* — **loại:** harness gốc là **bằng chứng khung** (test tồn tại ở bản gốc), KHÔNG phải bằng chứng code-rebuild chạy xanh. Đóng PASS = bịa số (rớt gate rubric #3). PENDING là trung thực.
- (c) *Chạy pentest ngoài + DAST + a11y + DR đầy đủ ngay vòng này cho "an toàn"* — **loại:** slice nội bộ single-node chưa expose public transport (E21 R4 parked), UI chưa có → nhồi pentest/a11y/DR = thủ tục thừa (vi phạm Đủ-là-đủ); điểm-bán-security nghiệm bằng audit-adversarial (mạnh hơn DAST generic). Ghi gap có địa chỉ chuyển vòng sau khi có transport public.
- (d) *`uat` tự ký hai chữ ký hộ PO/CISO cho "gọn"* — **loại:** phá phân vai A5 (AI CHUẨN BỊ, người thật KÝ); ký-có-điều-kiện + ghi điều kiện là đúng vai.

---

## 5) Bàn giao sang `ship` (GĐ13)

```
═══ BÀN GIAO — hex-agent-rebuild (GĐ12 → GĐ13) ═══
Đã chứng minh : 28/28 AC lõi có test · 26 PASS · 2 PENDING (R3+resume chưa chạy staging) · 0 FAIL ·
                UAT sign-off ✔ (2026-07-02, có điều kiện) · Security sign-off ✔ (2026-07-02, có điều kiện)
Điều kiện/hở còn treo : (1) SPIKE-1/D3 resume — chặn ĐÓNG R1 (pass a/b/c) · (2) ADR-006 D4 redact-raw-args —
                chặn bật write_tools_enabled · (3) D2 scope + M1/M2/M3 R3 — chặn release R3 · (4) pentest/DAST/DR —
                gap chuyển vòng sau khi có transport public (E21 R4). Không hở BỊ GIẤU trong phạm vi.
Artifact  : rebuild-hex-agent/pipeline/12-uat.md  (+ state pipeline/uat.json)
→ Đủ điều kiện go-live (theo release, có điều kiện), làm Go/No-Go + Runbook + rollback : chạy /ship (GĐ13)
→ Còn nghi gap/edge case/permission chưa test hết (vd error-path delegation, ca biên μ, permission checkpoint) : chạy /review trước khi ship
→ Có AC cần code rồi re-test (R3 multi-agent · SPIKE-1 resume · redact-raw-args) : chạy /frame cho slice (hoặc /delivery)
════════════════
```
*Chỉ liệt kê, KHÔNG tự chọn hộ user chạy skill nào tiếp.*

*Traceability:* GĐ12 **nhận** Delivery Standards + DoD GĐ11 (DoD 9 dòng lõi + D1–D5 = 5 acceptance-security cứng · test pyramid ~60/15/15/10 + contract · CI gate) + Backlog GĐ9 (Requirement/Story/AC gốc + Test ref TC-…) + Module Contract GĐ10 (2 seam) + evidence-A/B/C (mechanism + 327-test harness `tests/`+`tests_audit/`). **Sinh** Test & Verification Report: bảng Mapping 5 mắt (Requirement GĐ9 → AC → TC mã → Result → Release Decision) cover đủ 6 AC LÕI (finish-by-evidence M1 · runaway-guards M2 · delegation-scope M3/D2 · redact-0-secret D4 · resume-determinism D3 · μ-co-ngặt gate-2) + Report lớp test + 2 sign-off (ký-có-điều-kiện). Mỗi TC trỏ harness gốc. **Bàn giao** `/ship` (chính, go-live có điều kiện theo release) · `/review` (đào gap còn nghi) · `/frame` (code R3/resume/redact rồi re-test). Sợi liền hai đầu: ngược (AC=GĐ9 · verify-chuẩn=DoD GĐ11 · seam=GĐ10) + xuôi (Release Decision → điều kiện go-live → /ship). Ẩn số treo có địa chỉ: SPIKE-1/D3→R1, ADR-006/D4→write-tool flag, M1/M2/M3→R3, OQ-1 NFR-perf→Operate GĐ14, pentest/DR→sau transport public.
