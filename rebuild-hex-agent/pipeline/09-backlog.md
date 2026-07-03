# 09 — Backlog: Roadmap · Backlog phân rã · Release Plan — HexAgent (clean rebuild)

> Skill `backlog` · Giai đoạn 9 (PLAN). Vào bằng **Live Slice Report GĐ8** (`pipeline/08-skeleton.md`) + **PRD/Domain GĐ5** (`pipeline/05-idea-domain.md`) + **Architecture GĐ6** (`06-shape.md`) + **Tech Decision GĐ7** (`07-stack.md`). Ra bằng **ba artifact**: Roadmap (theme × release) · Backlog phân rã (Epic→Feature→Story→AC) · Release Plan.
> Anchor gốc: `00-understanding/REBUILD-BRIEF.md` (7 invariant, epic gốc E01–E21 / P0–P4) + `evidence-A/B/C`.
> Chế độ tự-quyết: cổng go/no-go do người viết đóng vai **Product Owner (chủ sở hữu) + Tech-lead (duyệt)** tự quyết, ghi rõ lý do + phương án đã loại. Không hỏi user.
> Vai lõi GĐ9 = **bẻ vision thành Roadmap→Epic→Feature→Story→AC có traceability, trả lời "XÂY GÌ TRƯỚC, vì giá trị gì".** KHÔNG chọn stack/kiến trúc (GĐ6–7), KHÔNG chia module/gán owner (GĐ10), KHÔNG code/viết DoD chi tiết (GĐ11).

---

## ── GÓC NHÌN LÃNH ĐẠO (đọc trước, 90 giây — không cần biết code) ──

**Ta đang lập kế hoạch xây gì trước.** Live slice GĐ8 đã đóng khung xong lát cắt lõi (*giao 1 task → agent plan → delegate 1 sub-agent → chỉ FINISHED khi có bằng chứng thật, có phanh chặn chạy-vô-hạn*). Bây giờ ta bẻ cả tầm nhìn thành một cây việc-làm-được, đúng thứ tự, mỗi khối tiền đổi lấy giá trị gì. Kế hoạch bám đúng **epic gốc E01–E21** và **thứ tự pha P0→P4** của bản gốc — không chế mới.

**Ba điều lãnh đạo cần nhìn.**
1. **Business Objective (đo được, nối GĐ1):** **M1 "Zero false-finish"** — trong bộ nghiệm thu, số lần agent đạt `FINISHED` mà thiếu bằng chứng thật = **0**. Kèm M2 "Bounded" (mọi task về terminal ≤ max_rounds) và M3 "No-escalation" (0 delegation scope con ⊄ cha). Đây là ba lời hứa đắt nhất của sản phẩm, và **cả ba chỉ được chứng minh xong ở R3** — nơi vòng lặp multi-agent LÕI chạy thật.
2. **Đâu là tiền-đặt-cọc, đâu là điểm-bán.** R1–R2 (Foundation + Single-agent+Tools) là **nền an toàn** — kernel một-cửa, kỷ luật JSON/budget, tool sandbox, resume từ SQLite. Chúng KHÔNG phải điểm bán, nhưng thiếu chúng thì điểm bán không đứng được. **R3 (Multi-agent TaskLoop + Delegation + Acceptance) MỚI là điểm bán** — chính là chỗ M1/M2/M3 thành sự thật. Vì vậy **mọi Story lõi (taskloop / acceptance / delegation) được ưu tiên R3** và đánh dấu **⭐ LÕI**.
3. **Xây gì trước và vì sao.** Thứ tự **không** theo độ khó kỹ thuật mà theo *gỡ-rủi-ro-rẻ-nhất-trước*: R1 dựng nền + biến live-slice GĐ8 thành feature đầu tiên (đã có tiền lệ chạy ở gốc → rủi ro thấp); R2 mở tool an toàn (điều kiện để worker làm việc thật); R3 ráp lõi multi-agent (nơi trả về toàn bộ giá trị sản phẩm); R4 (Control Plane realtime) **cố ý hoãn** vì UI chỉ là người-tiêu-thụ read-model, không chặn go-live của lõi.

**Một dòng cho sếp.** Nếu R3 về đích — agent thật sự *chỉ dừng khi có bằng chứng* và *không bao giờ chạy vô hạn hay leo quyền* — thì sản phẩm đã có lõi bán được; R4 (bảng điều khiển realtime) là mở rộng an toàn quanh lõi đã chắc, làm sau.

**Trạng thái hôm nay (nói thẳng).** Chưa dòng code rebuild nào chạy trên staging (GĐ8: 0/9 tick-thật) → toàn bộ backlog ở trạng thái **planned/chưa-bắt-đầu**; feature đầu R1 = chính slice GĐ8 đang chờ `/frame` dựng. Ẩn số chặn thật sự **duy nhất**: SPIKE-1 (LangGraph resume "một-lần-đúng") — nằm trong R1 và phải đo trước khi R1 đóng.

---

## ── CHI TIẾT (cho dev) ──

### Neo nguồn (traceability đầu vào — mỗi khẳng định có địa chỉ)

| Nguồn | Lấy gì cho backlog |
|---|---|
| **Live Slice GĐ8** (`08-skeleton.md`) | Slice `finish-by-evidence-tối-thiểu` = **feature ĐẦU TIÊN của R1** (đúng luật "slice GĐ8 → feature đầu release gần nhất"). 4 "giả định đã đổi" (SPIKE-1 thành go/no-go, reconcile tên event, redact-raw-args, max_steps-enforce-ở-discipline) → phản ánh thành Story/AC bên dưới. |
| **PRD/Domain GĐ5** (`05-idea-domain.md`) | Business Objective M1/M2/M3; Scope IN/OUT (OUT = R4 hoãn + park-with-trigger); 5 business rule bất biến → nguồn cho AC; 6 domain event → mốc hành vi Story. |
| **REBUILD-BRIEF** | Epic gốc E01–E21, thứ tự P0–P4, 7 invariant. Roadmap R1–R4 bám thẳng bản đồ này (không chế epic mới). |
| **Architecture GĐ6 / Stack GĐ7** | Chỉ để **size feature + ràng buộc thứ tự** (feature nào chặn feature nào). KHÔNG chọn lại (đã chốt Python 3.11·LangGraph·SQLite). |

---

## 1) ROADMAP (Theme × Release) — tầng lãnh đạo

```text
ROADMAP — HexAgent (clean rebuild)
Business Objective : M1 "Zero false-finish" = 0 lần FINISHED thiếu evidence thật trong bộ nghiệm thu
                     (phụ: M2 Bounded — mọi task về terminal ≤ max_rounds; M3 No-escalation — 0 scope con ⊄ cha). [nối GĐ1]
Product Goal       : Một agent tự-điều-phối: giao 1 mục tiêu → tự plan → order → delegate sub-agent
                     → chỉ FINISHED khi mọi AC có bằng chứng thật, không chạy vô hạn. [nối GĐ2]
```

| Theme (mục tiêu nghiệp vụ) | R1 · P0 Foundation | R2 · P1–P2 Single-agent+Tools | R3 · P3 Multi-agent (LÕI) | R4 · P4 Control Plane |
|---|---|---|---|---|
| **T1 · "Không bao giờ báo-xong-khống"** (evidence-based finish) | E02 finish-gate + budget (nền kỷ luật) | — | **⭐ E10 Acceptance-by-evidence** (điểm bán M1) | E21 siết dần evidence types (từ E15→E21) |
| **T2 · "Không bao giờ chạy vô hạn"** (bounded loop) | E01 kernel + E02 budget/guard | E05 graph loop có guard | **⭐ E10 TaskLoop guards** (max_rounds/no-progress/repeat) | E21 lệnh Pause/Stop realtime |
| **T3 · "Không leo thang quyền"** (delegation an toàn) | E01 chokepoint execute_tool | E06 scope-check + policy fail-closed | **⭐ E09 Roles + E10 Delegation scope⊆parent** (điểm bán M3) | E21 approval-checkpoint (park) |
| **T4 · "Chạy được, quan sát được, khôi phục được"** (glass-box + resume) | E04 event-log-first · E05 SQLite resume (SPIKE-1) | E06 tool events · E07 skills · E08 RAG (optional) | E10 delegation.finished vào event log | **E21 Control-Tower UI + SSE + redaction** |

**Đủ-là-đủ (mật độ điền theo release gần):** R1 điền dày (phân rã tới Story+AC); R2 vừa (Feature + Story chính, AC cho sprng đầu); R3 phân rã Story+AC cho các Story ⭐ LÕI (rủi ro/giá trị cao nhất) + đặt tên phần còn lại; R4 chỉ theme + epic (E21) — release xa, refine sau. **Không cố điền hết mọi ô.**

**Lý do xếp release (mỗi dòng 1 lý do — audit lại được):**
- **R1 = P0 Foundation vào trước** vì (a) live-slice GĐ8 đã chứng minh đường đi cả 9 tầng ở gốc → dựng lại rủi ro thấp; (b) SPIKE-1 (resume) là ẩn số cao **duy nhất**, phải đo sớm-rẻ ngay trong nền; (c) mọi release sau đứng trên kernel + event-log + resume này. **Loại** phương án "làm multi-agent trước cho nhanh ra điểm bán" — sẽ dựng lõi trên nền chưa có chokepoint/observability/resume, rủi ro sập nền, không audit được.
- **R2 = Single-agent + Tools vào giữa** vì worker ở R3 cần **tool thật chạy an toàn** (fs_read/write sandbox, policy fail-closed) mới tạo được *evidence thật* để judge; và loop đơn (E05) là bàn đạp cho loop đa (E10). **Loại** "gộp R2 vào R3" — sẽ nhồi tool-safety + multi-agent cùng lúc, khó cô lập lỗi.
- **R3 = Multi-agent LÕI** vì đây là nơi M1/M2/M3 **thật sự** được chứng minh (delegation + acceptance-by-evidence + guards đầy đủ). Đặt sau R1–R2 vì phụ thuộc chokepoint + tool + resume đã chắc. **Đây là release trả về điểm bán.**
- **R4 = Control Plane hoãn cuối** vì UI là **consumer** của read-model (ARC-1: UI ⊥ core), không phải cơ chế lõi; event-log-first (R1) đã đủ để audit/replay cho MVP. **Loại** "làm Control-Tower UI ở R1 cho đẹp demo" — phình sang seam BE↔UI + transport, không đổi bản chất rủi ro lõi loop, vi phạm Đủ-là-đủ (theo ADR-006 GĐ6, Scope OUT GĐ5).
- **Park-with-trigger (KHÔNG vào R1–R4):** E11 Departments · E12 IntentRouter · E13 Software Factory · E14 Ledger/Memory · E20 Labs — YAGNI, chỉ thaw khi metric-threshold + có consumer (`evidence-C §4`). Ghi ở đây để lãnh đạo biết *đã cố tình để ngoài*, không phải bỏ sót.

---

## 2) BACKLOG PHÂN RÃ (Epic → Feature → Story → AC)

> Đọc thế nào: mỗi **Epic** mở bằng *business value + trạng thái* (lãnh đạo dừng ở đây vẫn hiểu); rồi **Feature → Story → AC** cho dev hành động. **AC nằm DƯỚI story** dạng Given/When/Then, phản ánh business rule bất biến Domain GĐ5. **Definition of Done tách riêng** (chỉ tham chiếu GĐ11, xem cuối mục). **Test ref** chỉ là móc (TC-…), GĐ12 lấp. **Tasks** là engineering-task thô để *size*, KHÔNG phải đặc tả (đặc tả là việc `/frame`).
> **⭐ = Story LÕI** (taskloop/acceptance/delegation) — ưu tiên R3.

### ══ RELEASE R1 · P0 Foundation (phân rã dày tới Story+AC) ══

#### EPIC E01 — Microkernel Core
> **Business value:** một cánh cửa DUY NHẤT cho mọi hành động → mọi thứ về sau (audit, safety, scope) chỉ cần gắn một lần vào cửa đó thay vì rải khắp nơi. Đây là nền của cả ba lời hứa sản phẩm. — **Trạng thái:** planned (feature F1.1 = chính slice GĐ8). — *nối Business Objective qua invariant I1.*

- **Feature F1.1 — `execute_tool` single chokepoint** — thuộc E01 — value: mọi capability call (LLM/tool) đi qua đúng một cửa, đính kèm observability/scope/envelope một lần — size: 1 sprint. *(= một phần slice đã đóng khung GĐ8.)*
  - **Story S1.1.1** ⭐(nền cho lõi): "Là *một builder giao task*, tôi muốn *mọi hành động của agent đi qua một chokepoint `execute_tool`*, để *về sau chỉ cần gắn audit/scope/policy một chỗ, không rò đường vòng*."
    - **AC-1** — Given kernel đã `freeze()` trước run đầu / When worker gọi bất kỳ capability (LLM hoặc tool) / Then request đi qua `execute_tool`, phát `tool.requested` (kèm lineage) rồi `tool.completed|failed`, trả về `CapabilityResult` chuẩn hoá; **không** call-site nào gọi tool/LLM ngoài chokepoint (kiểm bằng audit-test). *(rule bất biến #5 Domain; I1.)*
    - **AC-2** — Given một action ném exception / When chạy qua middleware chain / Then exception **không** thoát ra ngoài chokepoint; trả `CapabilityResult(ok=false, error=…)`. *(envelope guarantee, evidence-B §4.)*
    - Tasks (size): dựng `AgentKernel` + `KernelSession`; `ToolPort`; middleware chain outer→inner (Timing→PolicyGate→BudgetGuard→Retry→Condense→core); audit-test "no bypass".
    - Test ref: `TC-KERNEL-CHOKEPOINT-001`, `TC-KERNEL-NO-BYPASS-002`.
  - **Story S1.1.2** (isolation): "Là *builder chạy nhiều task*, tôi muốn *state chỉ nằm ở session, kernel đông cứng*, để *hai run không rò state cho nhau*."
    - **AC-1** — Given kernel `freeze()` xong / When chạy 2 run song song / Then state mỗi run ⊂ session riêng, sau run không còn residue trên kernel (0 state bleed). *(I2/I3.)*
    - Tasks: `SessionFactory` là constructor duy nhất; `StateStore` deep-copy isolation.
    - Test ref: `TC-KERNEL-ISOLATION-003`.

#### EPIC E02 — Output Discipline
> **Business value:** biến "dừng" thành thứ *có biên cứng* và biến "hoàn thành" thành thứ *bị chặn nếu chưa validate* — trực tiếp chống hai bệnh chết người (báo-xong-khống, chạy-vô-hạn) ở tầng logic thuần. — **Trạng thái:** planned. — *nối M1 + M2.*

- **Feature F1.2 — Budget & guard (bounded loop nền)** — thuộc E02 — value: loop có phanh cứng, không đốt token vô hạn — size: 1 sprint.
  - **Story S1.2.1** ⭐: "Là *người trả tiền token*, tôi muốn *loop dừng cứng khi chạm budget/không-tiến-triển*, để *một task hỏng không đốt tới trần chi phí*."
    - **AC-1** — Given `Budget.max_steps` đặt trước run / When số step (không tính parse-error) đạt max / Then loop dừng ở **BLOCKED**, phát `TaskBlocked`. *(rule bounded; evidence-A §5.)*
    - **AC-2** — Given hai vòng liên tiếp artifacts không tăng ∧ acceptance không đổi ∧ không có command / When guard chạy / Then dừng BLOCKED (no-progress guard). *(evidence-A §4.)*
    - **AC-3 (giả định GĐ8 đã đổi)** — Given `max_steps` / When enforce / Then enforce **ở tầng discipline/loop** (không phải core — core coi là knob) — kiểm budget cắt thật ở loop. *(feed-ngược GĐ8 §5.)*
    - Tasks: `discipline/budget.py` (max_steps không-tính-parse-error, max_parse_errors CONSECUTIVE, max_same_tool_calls); no-progress guard; repeat-decision guard (chữ ký lặp N× → BLOCKED).
    - Test ref: `TC-BUDGET-MAXSTEPS-001`, `TC-GUARD-NOPROGRESS-002`, `TC-GUARD-REPEAT-003`.
- **Feature F1.3 — JSON gate + finish-gate** — thuộc E02 — value: quyết định của agent luôn parse được; không được "finish" khi code đổi mà chưa validate — size: 1 sprint.
  - **Story S1.3.1**: "Là *hệ điều phối*, tôi muốn *mọi quyết định của agent qua JSON-gate strict + parse-repair*, để *lỗi format không làm sập loop mà bị đếm vào parse-budget*."
    - **AC-1** — Given output không đúng JSON schema / When `parse_decision` chạy / Then thử parse-repair; hỏng liên tiếp đạt `max_parse_errors` → **FAILED**; parse tốt reset đếm. *(evidence-A §5.)*
    - **AC-2** — Given `code_changed=true ∧ validation_passed=false` / When agent xin finish (không phải finish_reason="blocker") / Then finish bị chặn (finish-gate). *(evidence-A §4.)*
    - Tasks: `json_gate`; `finish_gate.check_finish`; condense (context).
    - Test ref: `TC-JSONGATE-REPAIR-001`, `TC-FINISHGATE-002`.

#### EPIC E03 — LLM Adapter
> **Business value:** cho agent "suy nghĩ" (đề xuất plan/quyết định) qua một adapter chuẩn, retry đúng loại lỗi → ổn định, đổi model không đụng lõi. — **Trạng thái:** planned. — *nền cho plan/decompose.*

- **Feature F1.4 — LLM-as-capability (JSON-mode)** — thuộc E03 — value: LLM gọi QUA `execute_tool` như một capability, JSON-mode, phân loại retry — size: 1 sprint.
  - **Story S1.4.1**: "Là *worker*, tôi muốn *gọi LLM như một capability qua chokepoint ở JSON-mode*, để *plan/quyết định luôn có cấu trúc và lỗi tạm-thời được retry còn lỗi vĩnh-viễn thì fail nhanh*."
    - **AC-1** — Given LLM call qua `execute_tool` / When lỗi transient (rate-limit/timeout) / Then retry theo policy; lỗi permanent (auth/4xx) → fail ngay, không retry. *(evidence-C §3.)*
    - **AC-2** — Given JSON-mode / When trả về / Then output parse được bởi JSON-gate (nối F1.3). 
    - Tasks: `llm/adapter.py` JSON-mode + lazy client + retry-classify.
    - Test ref: `TC-LLM-RETRYCLASS-001`.

#### EPIC E04 — Observability
> **Business value:** hộp-kính — mọi việc agent làm để lại dấu vết audit + replay được; đây là điều kiện để sau này chứng minh "không báo-xong-khống" bằng máy chứ không bằng lời. — **Trạng thái:** planned. — *nối T4 + M1 (evidence là audit).*

- **Feature F1.5 — Event-log-first (jsonl + summary + metrics)** — thuộc E04 — value: mọi capability call phát event → nguồn audit/replay/resume — size: 1 sprint.
  - **Story S1.5.1**: "Là *người vận hành/audit*, tôi muốn *mọi capability call phát `tool.requested/completed` vào `events.jsonl` với seq monotonic gap-free*, để *replay lại đúng trạng thái và truy vết được từng bước*."
    - **AC-1** — Given slice chạy N1,N2 / When hoàn tất / Then `events.jsonl` chứa `tool.requested/completed` của N1,N2 + `delegation.finished`; `seq` per-run monotonic **gap-free**. *(evidence-B §7 (ii).)*
    - **AC-2** — Given event log [0..n] / When `build_snapshot` fold / Then kết quả deterministic theo seq order (replay = snapshot). *(evidence-B §7 (v).)*
    - **AC-3 (giả định GĐ8 đã đổi)** — Given tool phát `tool.requested` với raw args, và slice dùng write-tool `fs_write` / When log / Then SECRET_KEYS được **redact TRƯỚC** khi ghi jsonl (bật trước khi enable write-tool). *(feed-ngược GĐ8 §5; known-gap evidence-B §6.)*
    - **AC-4 (giả định GĐ8 đã đổi — reconcile OQ-3)** — Given known-mismatch tên event (kernel phát `tool.requested/completed` vs registry khai `tool.call_requested/before_call/after_call`) / When dựng slice / Then dùng bộ tên **đã reconcile** `tool.requested/completed/failed` làm allowlist chân lý. *(feed-ngược GĐ8 §5, evidence-B §3.)*
    - Tasks: `EventLogger` subscribe tool.*/task.* → jsonl+summary+metrics; seq per-run RLock; redactor 15 SECRET_KEYS.
    - Test ref: `TC-EVENTLOG-SEQGAPFREE-001`, `TC-REPLAY-DETERMINISTIC-002`, `TC-REDACT-RAWARGS-003`.

#### EPIC E05 — Single-agent Graph + Resume *(P1 — đặt ở R1 vì mang SPIKE-1, ẩn số cao nhất, phải đo sớm-rẻ)*
> **Business value:** khôi phục — nếu process chết giữa chừng, task chạy tiếp đúng chỗ, không làm lại, không gây tác dụng phụ. SQLite là chân lý resume. — **Trạng thái:** planned, **chứa ẩn số chặn R1 (SPIKE-1).** — *nối T4 + I10/I11.*

- **Feature F1.6 — SQLite-truth resume (SPIKE-1)** — thuộc E05 — value: resume đúng run_id, 0 side-effect re-run — size: 1 sprint (rủi ro cao).
  - **Story S1.6.1** ⭐(rủi ro cao, nhiều AC): "Là *builder chạy task dài*, tôi muốn *resume task từ `langgraph.sqlite` cùng `run_id` sau khi process chết*, để *không phải chạy lại từ đầu và không gây tác dụng phụ lặp*."
    - **AC-1 (SPIKE-1.a)** — Given kill process **sau** N1 / When resume cùng `run_id` từ SQLite / Then N1 **không** re-emit `tool.requested` (không chạy lại side-effect). *(I10/I11; điều-kiện go/no-go GĐ8 ô 5.)*
    - **AC-2 (SPIKE-1.b)** — Given resume / When tiếp tục / Then `round_no` liên tục, không nhảy/lặp.
    - **AC-3 (SPIKE-1.c)** — Given crash **giữa** transaction (commands+round+save) / When khôi phục / Then **không** để checkpoint nửa-ghi (atomic). *(evidence-A §6, loop.py:208-218.)*
    - **AC-4** — Given `checkpoint.json` tồn tại / When resume / Then resume đọc **SQLite** làm truth, `checkpoint.json` chỉ là projection UI, KHÔNG dùng để resume. *(invariant #6.)*
    - Tasks: LangGraph substrate + serializable `AgentState` v2; SQLite checkpointer; `resume()` từ `next`; atomic txn.
    - Test ref: `TC-RESUME-NOREPLAY-001`, `TC-RESUME-ATOMIC-002`, `TC-RESUME-SQLITE-TRUTH-003`.
    - **Ghi chú go/no-go:** đây là **SPIKE-1** — 3 tiêu chí a/b/c là điều kiện đóng R1. Fail → mở lại "orchestrator tự viết resume" (phương án B GĐ7), **không đụng shape/kiến trúc**. (open-Q OQ-STACK-1.)

---

### ══ RELEASE R2 · P1–P2 Single-agent + Tools (phân rã vừa: Feature + Story chính, AC cho sprint đầu) ══

#### EPIC E06 — Tools & Safety
> **Business value:** cho worker *làm việc thật* (đọc/ghi file, chạy lệnh) nhưng bị nhốt trong sandbox và chặn bởi policy fail-closed → tool tạo ra được **evidence thật** cho judge, mà không cho agent thoát jail. — **Trạng thái:** planned (điều kiện để R3 có evidence thật). — *nối T3 + M3 nền + rule scope.*

- **Feature F2.1 — Sandboxed fs tools + PolicyGate fail-closed** — thuộc E06 — value: fs_read/write/list bị nhốt `var/workspace/`, terminal argv-only, policy chặn mặc-định-cấm — size: 1 sprint.
  - **Story S2.1.1**: "Là *builder lo an toàn*, tôi muốn *mọi truy cập file bị nhốt trong workspace jail và policy fail-closed*, để *agent không đọc/ghi ngoài vùng cho phép*."
    - **AC-1** — Given path trỏ ra ngoài `var/workspace/` / When `fs_write/fs_read` / Then bị từ chối (workspace containment, `resolve_in_workspace`). *(evidence-B §6.)*
    - **AC-2** — Given capability không có trong policy allow / When gọi / Then **fail-closed** (mặc định cấm), phát `tool.failed`. *(PolicyGate.)*
    - Tasks: `fs_read/write/list` jail; `terminal_run` argv-only; `SafeToolPort` per-tool policy; `PolicyGate` fail-closed. Test ref: `TC-SANDBOX-ESCAPE-001`, `TC-POLICY-MATRIX-002`.
- **Feature F2.2 — Scope-check tại execute_tool** — thuộc E06 — value: worker chỉ dùng được capability trong `allowed_capabilities` của session — size: nhỏ. *(chuẩn bị cho delegation R3.)*
  - **Story S2.2.1** ⭐(nền cho M3): "Là *hệ điều phối*, tôi muốn *scope-check tại `execute_tool` theo `allowed_capabilities`*, để *một worker không tự dùng tool ngoài scope được cấp*."
    - **AC-1** — Given tool ∉ `allowed_capabilities` session / When gọi qua chokepoint / Then reject fail-closed trước khi vào middleware. *(rule #3 nền; evidence-B §4.)*
    - Test ref: `TC-SCOPE-CHECK-001`.

#### EPIC E07 — Skills System *(P2)*
> **Business value:** agent nạp "kỹ năng" theo tiết-lộ-tăng-dần (chỉ mở đủ context cần) → tiết kiệm token, mở rộng năng lực mà không phình prompt. — **Trạng thái:** planned (mở rộng, không chặn lõi). — *Scope: R2, không thuộc finish-loop lõi.*

- **Feature F2.3 — Progressive-disclosure skills** — thuộc E07 — value: render-contract vs render-full theo nhu cầu — size: 1 sprint.
  - **Story S2.3.1** (đặt tên, AC refine sau — Đủ-là-đủ, R2 chưa tới sprint): "Là *worker*, tôi muốn *nạp skill ở dạng contract trước, full khi cần*, để *không tốn token cho skill chưa dùng*." — *AC: refine ở backlog-refinement trước sprint R2.*

#### EPIC E08 — RAG (Qdrant, optional) *(P2)*
> **Business value:** tra cứu tri thức nền cho agent, nhưng **health-gated + offline-first** — Qdrant sập thì hệ vẫn chạy, chỉ mất tra-cứu. — **Trạng thái:** planned, **optional** (ngoài lõi MVP, Scope GĐ5). — *nối Knowledge context.*

- **Feature F2.4 — Health-gated RAG** — thuộc E08 — value: ingest/search optional, không bao giờ raise — size: 1 sprint.
  - **Story S2.4.1** (đặt tên): "Là *worker*, tôi muốn *RAG health-gate không bao giờ ném lỗi khi Qdrant down*, để *hệ vẫn chạy offline-first*." — *AC refine sau; test skip nếu Qdrant down.*

---

### ══ RELEASE R3 · P3 Multi-agent — LÕI CỦA SẢN PHẨM (phân rã Story ⭐ tới AC; phần còn lại đặt tên) ══

> **Đây là release trả về điểm bán.** Mọi Story dưới đây là ⭐ LÕI (taskloop/acceptance/delegation) — nơi M1/M2/M3 được chứng minh thật. Phân rã tới AC vì rủi ro/giá trị cao nhất.

#### EPIC E09 — Roles & Lenses
> **Business value:** mỗi agent chỉ nhìn/làm được đúng phần việc của vai nó (allowlist = union − forbidden) → nền cho "không leo thang quyền". — **Trạng thái:** planned (điều kiện cho delegation an toàn). — *nối T3 + M3.*

- **Feature F3.1 — RoleView allowlist** — thuộc E09 — value: capability của agent = union − forbidden theo role — size: 1 sprint.
  - **Story S3.1.1** ⭐: "Là *hệ điều phối*, tôi muốn *mỗi agent có `RoleView` allowlist = union − forbidden*, để *vai quyết định đúng bộ capability, không dư quyền*."
    - **AC-1** — Given role có `forbidden` capabilities / When tính allowlist / Then allowlist = union role-caps − forbidden; capability trong forbidden **không** xuất hiện. *(roles/agent.py:53.)*
    - Tasks: `RoleView`; spec role (bỏ field dept/route chưa dùng). Test ref: `TC-ROLE-ALLOWLIST-001`.

#### EPIC E10 — TaskLoop + Delegation + Acceptance ⭐⭐ (LÕI của LÕI)
> **Business value:** **đây là sản phẩm.** Agent-O soạn đội, chia việc theo phụ thuộc, giao qua *một cửa giao-việc riêng* với scope con ⊆ cha, và **chỉ tuyên FINISHED khi mọi AC có bằng chứng thật**, có phanh chặn chạy-vô-hạn. M1/M2/M3 sống hay chết ở đây. — **Trạng thái:** planned — **release then chốt lõi.** — *nối thẳng cả 3 business objective.*

- **Feature F3.2 — Delegation chokepoint (scope child ⊆ parent)** — thuộc E10 — value: giao việc cho sub-agent qua cửa RIÊNG, auditable, không leo quyền — size: 1–2 sprint.
  - **Story S3.2.1** ⭐ (rủi ro cao, nhiều AC): "Là *hệ điều phối*, tôi muốn *delegate qua `DelegationManager.delegate` (cửa RIÊNG, không phải method kernel) với scope con ⊆ cha*, để *multi-agent auditable và sub-agent không leo quyền vượt cha*."
    - **AC-1** — Given child request có capability ⊄ parent-scope / When `delegate` validate policy / Then **REJECTED** fail-closed (property-test: MỌI child-cap ⊄ parent → rejected). *(rule #3 Domain; policy.py:25-26; GĐ8 ô 4.)*
    - **AC-2** — Given delegate hợp lệ / When chạy / Then tạo child session qua SessionFactory (scope-shrink), `Handler.run()`, merge artifact, đóng child, phát `delegation.finished`. *(evidence-A §3.)*
    - **AC-3** — Given Broker nắn context / When soạn `ContextPacket` / Then Broker **KHÔNG** mở rộng scope (packet không có field scope; O đặt `allowed_capabilities`). *(Core immutable evidence-A.)*
    - **AC-4** — Given depth > max_depth (=8) HOẶC vi phạm max_steps / When delegate / Then rejected (biên delegation). *(policy.py:8-32.)*
    - Tasks: `DelegationManager.delegate`; `DelegationPolicy` từ O's `allowed_capabilities`; Broker packet; checkpoint sau MỖI turn. Test ref: `TC-DELEGATE-SCOPE-001`(property), `TC-DELEGATE-MERGE-002`, `TC-BROKER-NOWIDEN-003`.
- **Feature F3.3 — Plan/Decompose có chứng-minh-dừng (gate-2)** — thuộc E10 — value: agent chia task thành cây, mỗi lần chia *chắc chắn tiến gần đích* (μ co ngặt) → không chia lòng vòng — size: 1–2 sprint.
  - **Story S3.3.1** ⭐: "Là *hệ điều phối*, tôi muốn *cổng-2 `accept_decomposition` (thuần cấu trúc, chạy TRƯỚC khi đổi cây) chứng minh μ(node)=len(done_when) co ngặt mỗi lần chia*, để *plan không bao giờ chia vô hạn và phủ đủ done_when cha*."
    - **AC-1** — Given decompose đề xuất children / When gate-2 chạy TRƯỚC khi đổi cây / Then chỉ chấp nhận nếu mỗi child làm μ co **NGẶT** + coverage-by-implication phủ done_when cha. *(rule #4 Domain; accept.py:52-128.)*
    - **AC-2** — Given children trùng tên cha (Jaccard > 0.80) HOẶC không giảm μ / When gate-2 / Then phát hiện **RENAME/STUCK** → từ chối. *(evidence-A §2.)*
    - **AC-3** — Given cây decomposed / When đóng parent / Then re-assert done_when GỐC của parent (`_close_done_parents`); fail → COMPOSE_FAIL blocks. *(evidence-A §2.)*
    - Tasks: `Tree` forest+DAG acyclic; `accept_decomposition` μ-proof; synthetic reduce node. Test ref: `TC-DECOMPOSE-MU-001`(property μ↓), `TC-DECOMPOSE-STUCK-002`.
- **Feature F3.4 — Order steps (`next_node`, không leo sớm)** — thuộc E10 — value: bước có thứ tự đúng phụ thuộc — size: nhỏ.
  - **Story S3.4.1** ⭐: "Là *hệ điều phối*, tôi muốn *`next_node()` = node pending trái nhất mà mọi dependency đã done (topo depth,order)*, để *không chạy bước sau trước bước trước (không leo sớm)*."
    - **AC-1** — Given N2 `depends_on=[N1]`, N1 chưa done / When `next_node()` / Then trả N1 (không bao giờ N2 trước N1). *(tree.py:43-51.)*
    - Test ref: `TC-ORDER-NEXTNODE-001`.
- **Feature F3.5 — Acceptance-by-evidence + FINISHED có biên** — thuộc E10 — value: **điểm bán M1** — chỉ FINISHED khi mọi AC có bằng chứng THẬT; guard chặn runaway — size: 1–2 sprint.
  - **Story S3.5.1** ⭐⭐ (giá trị cao nhất, nhiều AC — chính là M1): "Là *builder giao task*, tôi muốn *agent chỉ tuyên FINISHED khi mọi AcceptanceCriterion có ≥1 bằng chứng THẬT*, để *không bao giờ nhận "xong" khống*."
    - **AC-1** — Given một AC `status="passed"` nhưng `evidence_ids=∅` / When `all_accepted()` / Then **KHÔNG** FINISHED (evidence rỗng không tính). *(rule #1; state.py:35-37.)*
    - **AC-2** — Given AC dẫn evidence là scaffolding (session_plan/context_packet/ac_report) / When `judge_acceptance` / Then evidence bị **từ chối**; chỉ artifact/tool_result/reviewer_report/diff/test_result được tính. *(rule #1; evidence.py:16-23.)*
    - **AC-3** — Given worker cố ghi verdict / When gate chạy / Then verdict chỉ do **gate** ghi; `DoneWhen`/Node cấm verdict keys. *(rule #2; node.py:20.)*
    - **AC-4** — Given mọi AC `passed ∧ evidence≠∅` / When `all_accepted()` / Then **FINISHED**, phát `TaskFinished`. *(domain event.)*
    - Tasks: `judge_acceptance`; `AcceptanceCheck.is_satisfied`; Blackboard evidence resolve; `evidence_type_of`. Test ref: `TC-FINISH-EVIDENCE-001`, `TC-FINISH-REJECT-SCAFFOLD-002`, `TC-VERDICT-GATE-ONLY-003`.
  - **Story S3.5.2** ⭐ (M2 — bounded): "Là *người trả token*, tôi muốn *loop multi-agent dừng cứng khi chạm guard*, để *task hỏng về BLOCKED chứ không chạy vô hạn*."
    - **AC-1** — Given chạm bất kỳ guard (max_rounds / no-progress / repeat-decision N× / parse-budget / MAX_DEPTH / per-root step) / When loop chạy / Then về terminal **BLOCKED**, phát `TaskBlocked`. *(evidence-A §4-5.)*
    - **AC-2** — Given task không chạm guard và all-accepted / When loop / Then về FINISHED trong ≤ max_rounds (M2). 
    - Test ref: `TC-BOUNDED-MAXROUNDS-001`, `TC-BOUNDED-REPEAT-002`.

*(E10 là feature lớn nhất — cắt thành 4 feature F3.2–F3.5 để mỗi feature vừa 1 Program Increment/1–2 sprint, KHÔNG nhồi cả E10 vào một feature. Đây là chỗ live-slice GĐ8 `finish-by-evidence-tối-thiểu` được scale ra: slice đó chạm đúng F3.2+F3.3+F3.4+F3.5 ở quy mô tối thiểu.)*

---

### ══ RELEASE R4 · P4 Control Plane (chỉ theme + epic — release xa, refine sau) ══

#### EPIC E21 — Realtime Control Plane
> **Business value:** bảng-điều-khiển realtime để người vận hành *nhìn* agent đang làm gì và *can thiệp* (pause/stop) — mà không rò secret. Mở rộng an toàn quanh lõi đã chắc, KHÔNG chặn go-live MVP. — **Trạng thái:** parked-đến-R4 (E21 gốc mới partial: Phase A + B1 ✓; B2–B14/transport/UI/reliability pending). — *nối T4 + I16/I17.*

- Epic-level (chưa phân rã Story — Đủ-là-đủ, release xa): contracts (RuntimeEvent/RuntimeCommand/RuntimeCheckpoint/Permission/Redactor) → EventEmitter canonical path (gate→seq→redact→fan-out) → transport (POST /api + SSE `?since=seq` resync) → Control-Tower UI (pure consumer, UI ⊥ core) → reliability (EventReplayBuffer, needs_resync) → approval-checkpoint + siết evidence types (E15 merged→E21). Redact tại biên: 0 secret trong `ui_payload`; `issued_by` = attribution ≠ authz (DEC-8).
- *Story + AC: refine khi R4 tới. Ẩn số NFR-số (P95 loop, ngưỡng alert error-rate) — OQ-1 — đo ở Operate, không bịa số bây giờ.*

---

### Các tầng AC & Definition of Done (tách bạch — theo hợp đồng skill)

```text
Story AC   : từng behavior Given/When/Then ở trên (nằm DƯỚI mỗi story, phản ánh business rule Domain GĐ5).
Feature AC : feature xong khi mọi story của nó pass AC + tích hợp chạy (vd F3.5 xong khi acceptance-by-evidence
             + bounded cùng chạy end-to-end trên một task 2 bước — chính là slice GĐ8 ở quy mô thật).
Release AC : go-live khi pass UAT + security scan + perf test + có rollback (CHI TIẾT ở GĐ12 uat + GĐ13 ship).
Definition of Done: chuẩn chất lượng bắt buộc cho MỌI item (coding standard, test pyramid, CI xanh, observability,
                    code review, migration…) — ĐỊNH NGHĨA ở GĐ11 (/delivery), ở đây CHỈ THAM CHIẾU, không viết lại.
```

> **Lưu ý luật cứng:** AC ở trên là *behavior của một story cụ thể*, KHÔNG phải danh mục yêu cầu toàn sản phẩm (đó là PRD GĐ4, đã có). DoD **không** trộn vào AC — DoD là việc GĐ11. `backlog` chỉ đặt **Test ref** (TC-…) làm móc; Test Case chi tiết là việc GĐ12 (uat).

---

## 3) RELEASE PLAN

```text
RELEASE PLAN — HexAgent (clean rebuild)

R1 · P0 Foundation  (E01 Kernel · E02 Discipline · E03 LLM · E04 Observability · E05 Graph/Resume-SPIKE1)
  Feature: F1.1 chokepoint · F1.2 budget/guard · F1.3 json/finish-gate · F1.4 LLM-as-capability
           · F1.5 event-log-first · F1.6 SQLite-resume(SPIKE-1).
  Mục tiêu (nối success metric): dựng nền chạy được một task 2 bước về FINISHED có event-log + resume;
           chứng minh SPIKE-1 (resume 0 side-effect). Đây là biến live-slice GĐ8 thành thật.
  Thứ tự + lý do: F1.1 chokepoint trước (mọi thứ gắn vào cửa này) → F1.5 event-log (audit nền) →
           F1.6 SPIKE-1 SỚM (ẩn số cao nhất, đo rẻ trong nền, fail thì đổi resume-impl không đụng shape) →
           F1.2/F1.3/F1.4 kỷ luật+LLM (chạy song song được sau khi có chokepoint).
  Release AC: task 2 bước về FINISHED/BLOCKED thật trên staging · SPIKE-1 pass a/b/c · events.jsonl seq gap-free
             · redact-raw-args bật · CI xanh (→ /delivery) · pass UAT tối thiểu + có rollback (GĐ12–13).
  Phụ thuộc: none (nền). Rủi ro: SPIKE-1 (R1 nội bộ) — có phương án B (orchestrator tự viết resume).
  DoD: xem GĐ11.

R2 · P1–P2 Single-agent + Tools  (E06 Tools&Safety · E07 Skills · E08 RAG)
  Mục tiêu: worker làm việc thật an toàn (fs sandbox + policy fail-closed + scope-check) → tạo được evidence thật;
           skills + RAG (optional, health-gated) mở rộng năng lực.
  Epic chính: E06 (chặn R3 — không có tool an toàn thì R3 không có evidence thật để judge); E07/E08 mở rộng.
  Thứ tự + lý do: E06 trước E07/E08 (E06 là điều kiện cho R3; E08 optional để cuối). 
  Hoãn sang R2 (không R1): tool-safety KHÔNG cần cho việc chứng minh nền loop chạy (slice GĐ8 dùng tool tối thiểu).
  Release AC: sandbox-escape test pass · policy-matrix pass · scope-check fail-closed · RAG test skip khi Qdrant down.

R3 · P3 Multi-agent — LÕI  (E09 Roles · E10 TaskLoop+Delegation+Acceptance)  ⭐ RELEASE ĐIỂM BÁN
  Mục tiêu (nối M1/M2/M3): agent-O soạn đội, delegate scope⊆parent, chỉ FINISHED khi evidence thật, bounded.
           → đây là nơi M1 zero-false-finish + M2 bounded + M3 no-escalation ĐƯỢC CHỨNG MINH.
  Epic chính: E10 (lõi của lõi, cắt F3.2 delegation · F3.3 decompose-μ · F3.4 order · F3.5 acceptance+bounded);
           E09 roles (nền quyền).
  Thứ tự + lý do: E09 → F3.3 decompose → F3.4 order → F3.2 delegation → F3.5 acceptance+bounded
           (dựng từ "chia đúng" → "xếp đúng" → "giao an toàn" → "chấm-bằng-bằng-chứng + phanh"). F3.5 sau cùng vì
           nó là gate hội tụ mọi thứ (cần cả delegation + tool-evidence + guards có mặt).
  Story ⭐ LÕI ưu tiên: S3.5.1 (acceptance-by-evidence, M1) · S3.5.2 (bounded, M2) · S3.2.1 (delegation scope, M3)
           · S3.3.1 (μ-proof) · S3.4.1 (order). Đây là các story cắt điểm-bán → xây trước phần đặt-tên khác.
  Release AC: TaskLoop đạt FINISHED trên task thật · property-test scope⊆parent pass · property-test μ↓ pass
           · zero false-finish trên bộ nghiệm thu (M1) · no privilege escalation (M3) · pass UAT + security + perf + rollback.
  Phụ thuộc: R1 (chokepoint+resume+event) + R2 (tool an toàn → evidence thật). Rủi ro: R3 judge = honor-system
           một phần (O tự chấm) → siết evidence types ở R4/Operate (không chặn R3 go-live, đã ghi rủi ro GĐ8 R3).

R4 · P4 Control Plane  (E21)  — HOÃN CÓ CHỦ ĐÍCH
  Mục tiêu: bảng điều khiển realtime (xem + pause/stop) không rò secret. Mở rộng an toàn quanh lõi.
  Epic chính: E21 (contracts→emitter→transport→UI→reliability→approval-checkpoint; E15 merged→E21).
  Hoãn sang R4 vì: UI là consumer read-model (UI ⊥ core), event-log-first R1 đã đủ audit cho MVP; go-live lõi
           KHÔNG phụ thuộc UI. (ADR-006 GĐ6; Scope OUT GĐ5.) Ẩn số NFR-số (OQ-1) đo ở Operate — không bịa.

PARK-WITH-TRIGGER (ngoài R1–R4, YAGNI): E11 Departments · E12 IntentRouter · E13 SoftwareFactory · E14 Ledger/Memory
  · E20 Labs. Thaw khi metric-threshold + có consumer đang làm (evidence-C §4). Ghi để lãnh đạo biết đã cố ý để ngoài.
```

---

## 4) Tự soi trước khi chốt (bắt buộc — theo rubric)

1. **Lãnh đạo đọc đoạn đầu có biết "xây gì / vì gì / tới đâu"?** — CÓ: Roadmap 1 câu Business Objective có số (M1) + bảng theme×release; mỗi Epic mở bằng business value nghiệp vụ (không jargon); phân biệt rõ tiền-đặt-cọc (R1–R2) vs điểm-bán (R3) vs hoãn (R4). Scan 2–3 phút ra kế hoạch.
2. **Dev đủ để `frame` một slice?** — CÓ: Story sprint R1 + Story ⭐ R3 có AC Given/When/Then cụ thể (nối rule bất biến Domain), Tasks thô để size, Test ref làm móc.
3. **Đủ + đúng ba artifact?** — CÓ: Roadmap (theme×release) + Backlog phân rã (Epic→Feature→Story→AC đúng tầng, không nhảy Epic→Task) + Release Plan (R1 chi tiết, R2–R4 mục tiêu+epic). AC nằm DƯỚI story (không thành PRD thứ hai); DoD tách riêng (chỉ trỏ GĐ11).
4. **Đủ-là-đủ?** — CÓ: R1 phân rã tới Story+AC (dày); R2 Feature+Story chính (vừa, vài story chỉ đặt tên); R3 Story ⭐ tới AC + phần khác đặt tên; R4 chỉ theme+epic. Số AC tỉ lệ rủi ro (S3.5.1/S1.6.1 nhiều AC; story quen 1 AC). Không đổ story cho R4. Mỗi quyết định release có lý do 1 dòng.
5. **Traceability liền?** — CÓ: Business Objective(M1) → Theme(T1–T4) → Epic(E01–E21) → Feature → Story → AC → Task → Test ref; AC nối business rule Domain GĐ5 (#1–#5); story đầu R1 = live-slice GĐ8; 4 "giả định GĐ8 đã đổi" phản ánh thành AC (F1.2-AC3, F1.5-AC3/AC4, F1.6). Chỗ treo (SPIKE-1, OQ-1 NFR) ghi rõ open-Q thay vì bịa.
6. **Không lấn vai?** — CÓ: không chọn lại stack/kiến trúc (chỉ tham chiếu để size+thứ tự); không chia module/gán owner kỹ thuật (đó là GĐ10); không viết code/đặc tả slice; không viết DoD chi tiết (trỏ GĐ11); không viết Test Case chi tiết (chỉ Test ref, GĐ12 lấp).

---

## 5) Cổng GĐ9 (tự-quyết; đóng vai Product Owner chủ sở hữu · Tech-lead duyệt)

**Câu hỏi cổng (doc GĐ9):** *"Backlog đủ để lập kế hoạch delivery & phân module chưa?"*
Kèm: release gần nhất (R1) đã có Story+AC? Roadmap lãnh đạo đọc được? Thứ tự release có lý do? Còn open-question Domain nào chặn?

**Trình cổng (chủ sở hữu = PO + Tech-lead):**
- Ba artifact đủ: Roadmap (4 theme × 4 release) · Backlog R1 phân rã tới AC (5 epic / 7 feature / ~10 story có AC) + R3 story ⭐ tới AC · Release Plan R1 chi tiết + R2–R4 mục tiêu.
- Story R1 đều có AC Given/When/Then; Story ⭐ LÕI R3 (acceptance/delegation/decompose/order/bounded) có AC nối thẳng business rule Domain.
- Thứ tự release có lý do + phương án đã loại (R1-first, R4-hoãn, park-with-trigger).
- Open-question còn treo: (a) SPIKE-1 resume — nằm TRONG R1, phải đo trước khi đóng R1 (không chặn *lập kế hoạch*, chặn *đóng R1*); (b) OQ-1 NFR-số — đo ở Operate. **Không** có open-Q Domain nào khiến story R1/R3 chưa đặt được AC.

```
═══ CỔNG GĐ9 — BACKLOG: HexAgent (clean rebuild) ═══
Artifact     : Roadmap (4 theme × 4 release) · Backlog phân rã (R1: 5 epic/7 feature/~10 story có AC; R3: 5 story ⭐ LÕI có AC) · Release Plan (R1 chi tiết, R2–R4 mục tiêu+epic).
R1 story+AC  : ĐỦ — mọi story R1 có AC Given/When/Then nối rule bất biến Domain GĐ5.
Story ⭐ LÕI : acceptance-by-evidence (M1) · bounded (M2) · delegation scope (M3) · μ-proof · order — ưu tiên R3, có AC.
Traceability : Objective→Theme→Epic→Feature→Story→AC→Task→Test-ref liền; story đầu R1 = live-slice GĐ8; giả định GĐ8 phản ánh vào AC.
Open-Q treo  : SPIKE-1 resume (trong R1, đo trước khi đóng R1) · OQ-1 NFR-số (→ Operate). Không open-Q Domain chặn AC.
Câu hỏi cổng : Backlog đủ để lập kế hoạch delivery & phân module chưa?
════════════════
```

**Quyết định cổng (tự-quyết — product owner: "không hỏi approval").**

**GATE: GO.** Backlog **đủ** để phân module (GĐ10) và lập delivery (GĐ11). Lý do: (1) ba artifact đủ, đọc-được 3 tầng; (2) R1 phân rã tới Story+AC — đội delivery lấy được ngay việc đầu tiên (= slice GĐ8); (3) Story lõi R3 đã có AC nối thẳng M1/M2/M3 và business rule Domain → `modules` biết ranh giới nào cần contract chặt (Orchestration/Execution-Core/Delegation); (4) không open-Q Domain nào chặn việc đặt AC — hai open-Q còn lại (SPIKE-1, NFR-số) có địa chỉ đo rõ và không chặn *việc lập kế hoạch*.

**Điều kiện kèm theo (ghi rõ, không phải chặn cổng GĐ9):** SPIKE-1 phải pass a/b/c **trước khi ĐÓNG R1** (không phải trước khi lập kế hoạch) — nếu fail, đổi resume-impl sang phương án B (orchestrator tự viết), backlog R1 không đổi cấu trúc (chỉ đổi task nội bộ F1.6).

**Phương án đã loại ở tầng cổng:**
- (a) *Chờ SPIKE-1 pass rồi mới chốt backlog* — **loại**: SPIKE-1 là rủi ro *thực thi trong R1*, không phải điều kiện *lập kế hoạch*; chặn cổng GĐ9 vì nó = trộn vai GĐ8/GĐ11 vào GĐ9, làm nghẽn phân-module (GĐ10 chạy song song được ngay).
- (b) *Phân rã đầy đủ Story+AC cho cả R2/R3/R4 để "backlog hoàn chỉnh"* — **loại**: cầu toàn, vi phạm Đủ-là-đủ; Domain R4 (NFR-số) còn treo → viết AC bây giờ = bịa; refine ở backlog-refinement khi release tới.
- (c) *Đưa E21 Control Plane lên R2 cho "demo đẹp sớm"* — **loại**: E21 là consumer read-model, không chặn go-live lõi; kéo lên = phình transport/UI, trễ điểm-bán R3, vi phạm thứ-tự-gỡ-rủi-ro.

---

## 6) Bàn giao sang modules (GĐ10)

```
═══ BÀN GIAO — HexAgent (clean rebuild) · Backlog GĐ9 ═══
Đã chốt : Roadmap (4 theme × 4 release) · Backlog release gần nhất R1 (5 epic / 7 feature / ~10 story có AC)
          + Story ⭐ LÕI R3 (acceptance-by-evidence · bounded · delegation-scope · μ-proof · order) có AC · Release Plan R1.
Artifact: rebuild-hex-agent/pipeline/09-backlog.md (+ state pipeline/backlog.json)
Open-Q  : SPIKE-1 resume (đo trước khi ĐÓNG R1) · OQ-1 NFR-số (→ Operate). Không open-Q Domain chặn AC.
→ Chia module theo domain boundary + gán owner + contract (GĐ10, bước kế mặc định)          : chạy /modules
   (gợi ý ranh giới cần contract chặt: Orchestration ↔ Execution-Core ↔ Delegation — nơi rule #1/#3 sống)
→ Build ngay một story đã có AC của R1 (đóng khung slice cho dev — vd S1.6.1 SPIKE-1 hoặc S1.1.1 chokepoint) : chạy /frame
   (rồi /delivery khi vào build chuẩn GĐ11 — định DoD + CI/CD + test pyramid cho ô #6/#7 GĐ8)
→ Domain còn treo khiến story chưa đặt được AC (hiện KHÔNG có — chỉ NFR-số treo)              : quay lại /idea hoặc /partner (GĐ5)
════════════════
```

*Traceability:* GĐ9 **nhận** Live Slice GĐ8 (`08-skeleton.md`: slice `finish-by-evidence-tối-thiểu` PASS-đóng-khung + 4 giả-định-đã-đổi) + PRD/Domain GĐ5 (M1/M2/M3, 5 rule bất biến, scope IN/OUT) + epic gốc E01–E21 (REBUILD-BRIEF). **Sinh** Roadmap (bám P0→P4) + Backlog (Epic→Feature→Story→AC, slice GĐ8 = feature đầu R1, giả-định-GĐ8 → AC) + Release Plan (thứ tự gỡ-rủi-ro-rẻ-nhất, Story ⭐ LÕI ưu tiên R3). **Bàn giao** liệt kê việc → `/modules` gán module/owner/contract (GĐ10, mặc định); `/frame` build một story R1; đường quay `/idea` khi Domain treo. Không mắt xích nào đứt: mọi open-Q còn lại (SPIKE-1, NFR-số) có địa chỉ đo, không bịa nối.
