# 11 — Delivery: Delivery Standards + Definition of Ready/Done + PR Checklist — HexAgent (clean rebuild)

> Skill `delivery` · Giai đoạn 11 (Delivery / Implementation Standards — BUILD). Nhận **Module Map + Module Contract GĐ10** (`pipeline/10-modules.md`: 6 module · 6 owner · 2 seam công khai · data ownership sạch) + **Live Slice Report GĐ8** (`pipeline/08-skeleton.md`: CI tối thiểu lint→pytest→audit + test stack pytest+Hypothesis+audit đã định) + **Tech Decision GĐ7** (`pipeline/07-stack.md`: Python 3.11 · LangGraph · SQLite · OpenAI-compatible JSON-mode · SSE · pytest+Hypothesis+audit-test) + **Backlog GĐ9** (`pipeline/09-backlog.md`: Story+AC để PR link ngược).
> Anchor gốc: `00-understanding/REBUILD-BRIEF.md` (7 invariant) + `evidence-A/B/C` + `ATLAS.md`. Chuẩn KHỚP stack/CI/test đã chốt (GĐ7/GĐ8) — KHÔNG bịa chuẩn mới, KHÔNG chọn lại stack.
> Chế độ tự-quyết: cổng go/no-go do người viết đóng vai **CTO / Kiến trúc sư (chủ sở hữu chuẩn) · Eng-manager (mở cổng)** tự quyết, ghi rõ lý do + phương án đã loại. Không hỏi user. `delivery` ĐẶT CHUẨN, KHÔNG code slice — code từng slice là `/frame`; không đào bug là `/review`; không viết test-result là `/uat`.

---

## ── GÓC NHÌN LÃNH ĐẠO (đọc trước, 60 giây — không cần biết code) ──

**Làm sao biết một thứ đã XONG và giao được an toàn?** Bằng đúng một khối **Definition of Done** — luật cứng cho MỌI item, không có ngoại lệ theo kích thước việc. Một thứ chưa đủ DoD thì **không release**, dù ai bảo "gần xong".

**DEFINITION OF DONE (mọi item, không cắt dòng nào):**

```
[ ] code review pass (đúng owner module — Module Map GĐ10)
[ ] test pass: unit + property(Hypothesis) + integration + audit-adversarial — CI xanh
[ ] contract giữ: không phá Public API/seam của module khác (Contract GĐ10)
[ ] 5 invariant-kiểm-được XANH (đây là điểm bán của sản phẩm — xem 5 dòng dưới)
[ ] observability có: mọi capability call phát tool.requested/completed vào events.jsonl
[ ] secret handling: 0 secret trong ui_payload (redact tại biên)
[ ] doc cập nhật (Public API / event schema / ADR nếu đổi quyết định lớn)
[ ] không giảm chất lượng (coverage không tụt, lint sạch)
[ ] merge xanh CI.        Không đạt DoD → KHÔNG release.
```

**5 invariant-kiểm-được là "Done thật" của sản phẩm này** — chúng chính là 3 lời hứa đắt nhất (không báo-xong-khống · không chạy-vô-hạn · không leo-quyền) biến thành **test chạy được**, không phải lời hứa:

| # | Invariant phải XANH (có test) | Test loại | Bám nguồn |
|---|---|---|---|
| **D1** | **Không call-site nào bypass `execute_tool`** — mọi hành động LLM/tool đi qua đúng một cửa | audit-adversarial | I1 · REBRIEF #2 · Contract Exec-Core "audit test cho MỌI module" |
| **D2** | **Scope child ⊆ parent** khi delegate — không leo thang quyền | property (Hypothesis) | I13/I14 · REBRIEF #4 · Contract Orch/Exec-Core |
| **D3** | **Resume round-trip XANH cùng `run_id`** — 0 side-effect re-run (SPIKE-1) | integration | I10/I11 · REBRIEF #6 · GĐ8 ô#5 SPIKE-1 |
| **D4** | **0 secret trong `ui_payload`** — redact tại biên trước fan-out | audit + property | I16 · REBRIEF #7 · Contract Control-Plane |
| **D5** | **Worker KHÔNG set verdict** — chỉ gate ghi acceptance | audit-adversarial | REBRIEF #5 · Contract Orch "worker chỉ đề xuất, GATE ghi" |

**Bốn chỉ số DORA — sức khoẻ giao hàng bắt đầu được đo.** Exec không đọc pipeline YAML; đọc 4 số này để biết đội giao hàng nhanh và ổn định không:

| Chỉ số DORA | Ý nghĩa (nghiệp vụ) | Đo ở đâu (delivery đặt móc, số baseline ở Operate GĐ14) |
|---|---|---|
| **Lead time** | Từ commit đến merge-xanh trên staging | CI timestamp (baseline OQ-1 → Operate) |
| **Deployment frequency** | Bao nhiêu lần lên staging/tuần | CD log (trunk-based → kỳ vọng cao) |
| **Change failure rate** | % PR gây rollback / hỏng CI sau merge | CI + incident log |
| **Recovery time (MTTR)** | Từ phát hiện sự cố đến khôi phục | Incident process (feature flag rollback nhanh) |

> ⚠️ **Số baseline 4 chỉ số DORA CHƯA có** (platform nội bộ, chưa chạy production) → **OQ-1**, đo ở Operate (GĐ14), **KHÔNG bịa số**. delivery đặt **cách đo**; Operate đọc **số thật**.

**Một điều CTO phải nhớ.** Sản phẩm này không bán "tính năng đẹp" — bán **niềm tin rằng agent chỉ báo-xong khi thật xong, không đốt tiền vô hạn, không leo quyền**. Vì vậy **DoD ở đây có 5 dòng invariant-kiểm-được (D1–D5) mà DoD dự án bình thường KHÔNG có** — đó là cách ta biến điểm bán thành cổng cứng. PR nào chạm 5 ranh giới đó mà không có test xanh tương ứng = **không merge**, không cần tranh luận.

---

## ── CHI TIẾT KỸ THUẬT (cho dev) ──

## Artifact 1 — DELIVERY STANDARDS (chốt 1 lần, áp mọi team)

> Đủ-là-đủ: đây là **hệ quan trọng, nhiều team (6 owner), có biên an toàn/secret/resume** → viết **đủ 12 mục**, mục rủi ro cao (secret · migration · observability · test pyramid) viết kỹ; mục quen stack (repo · branch) gọn. Mỗi lựa chọn lớn ghi LÝ DO + phương án đã loại.

### 1. Repository
- **Mono-repo, một khối triển khai (modular monolith)** — 6 module = 6 package trong một repo `hex-agent-rebuild/`. Layout theo module GĐ10 (đúng 1 owner/package):
  ```
  src/orchestration/  src/execution_core/  src/discipline/
  src/tools_safety/   src/control_plane/   src/knowledge/   (+ src/ports/ = Protocol dùng chung)
  tests/  tests_audit/  config/  var/workspace/  (jail)  var/  (langgraph.sqlite, events.jsonl)
  ```
- **Lý do:** GĐ6 chốt modular monolith một-deployable (ADR-005); mono-repo giữ 6 module cùng nhịp release, contract-test cross-module chạy tại chỗ. **Loại poly-repo/microservice:** thêm biên mạng + version-skew contract giữa 6 team cho một hệ single-node — phá "in-process call qua PORT, KHÔNG mạng" (GĐ6 §integration). **Loại một package phẳng:** mất ranh giới owner GĐ10, không audit được "ai đổi module nào".
- **CODEOWNERS** ánh xạ package → team owner (GĐ10 `_index.json`): `src/orchestration/ → @team-orchestration`, `src/execution_core/ src/discipline/ src/knowledge/ → @team-platform`, `src/tools_safety/ → @team-safety`, `src/control_plane/ → @team-observability`. → PR tự gán đúng reviewer.

### 2. Branching
- **Trunk-based + short-lived branch**, PR ≤ ~400 dòng.
- **Lý do:** 6 team code song song trên nền domain-boundary sạch (mỗi team một package, ít đụng nhau) → nhánh ngắn + merge nhanh giảm drift. **Loại git-flow:** nhánh release/develop dài gây merge đau + trễ deploy, không hợp nhịp "deploy staging nhiều lần" mong muốn (DORA deployment frequency cao).
- Nhánh chạm **seam công khai** (`execute_tool`, `run_task_loop`, `DelegationManager.delegate`, `SafeToolPort`, `EventEmitter.emit`) → BẮT BUỘC contract-test xanh + review của **owner module đích**, không chỉ owner module nguồn.

### 3. Coding standard
- **UTF-8, no BOM** — mọi file `.py`/`.yaml`/`.json`; enforce ở CI (reject BOM). Newline LF.
- **Immutability mặc định:** entity/envelope là **frozen dataclass** (`@dataclass(frozen=True)`), validation trong `__post_init__` — theo bản gốc: `Node` (ATLAS:88), `RuntimeEvent` (ATLAS:95, 14 field), `RuntimeCommand` (ATLAS:96, 7 field, idempotency_key). Domain entity mới (Plan/DoneWhen/SessionIdentity/AcceptanceCriterion/Evidence) đi cùng khuôn.
- **Ranh giới module = Protocol (ports):** mọi cửa cross-module khai bằng `typing.Protocol` trong `src/ports/` (`ToolPort`, `DelegationPort`, `DelegationServicePort`, `EventSinkPort`, `SafeToolPort`, `RagPort`) — **cấm cross-module import trực tiếp implementation** (GĐ6 ADR-001/ADR-005; `control/ports.py:15` gốc). Module chỉ phụ thuộc *Protocol*, không phụ thuộc lớp cụ thể của module khác.
- **Lazy client:** mọi client I/O nặng/tùy chọn (LLM adapter, Qdrant/RAG) khởi tạo **lazy** (chỉ tạo khi gọi lần đầu) — theo GĐ7 (`lazy Qdrant uuid5`, LLM adapter lazy). RAG **health-gated, never raises** (Contract Knowledge). → import module không kéo kết nối mạng; test offline chạy được.
- **`SessionFactory.restore(**kw-only)`** — constructor DUY NHẤT của session, kw-only để không lẫn thứ tự lineage 7-field (evidence-B §2).
- Type hint bắt buộc trên Public API; format `ruff format` + lint `ruff` (fail-closed CI). Không docstring rườm; comment giải thích *tại sao*, không *cái gì*.

### 4. Review policy
- Mỗi PR ≥1 approval của **owner module** (CODEOWNERS auto-request). PR chạm ≥2 module → cần approval của **mọi owner đích**.
- PR chạm **5 ranh giới invariant (D1–D5)** → review BẮT BUỘC có **audit/property-test đính kèm xanh** trước khi bấm approve; reviewer xác nhận test thật chặn được ca vi phạm (adversarial), không chỉ ca hạnh phúc.
- Reviewer KHÔNG tự-approve PR của chính mình. Không self-merge khi CI đỏ.

### 5. Testing pyramid  (bám Test contract GĐ10 + test stack GĐ7)
- **Tỉ lệ mục tiêu ~ 60 unit / 15 property / 15 integration / 10 audit-adversarial.** Đây KHÔNG phải pyramid cổ điển: hệ này *đặc biệt nặng property + audit* vì điểm bán là bất biến kiểm-được (D1–D5), không phải bề rộng feature.
  - **unit** (`pytest`): hàm thuần Discipline (json_gate/finish_gate/budget/condense), builder envelope, fold snapshot.
  - **property** (`Hypothesis`): ∀ decomposition accepted → μ(node) co ngặt (REBRIEF #4/plan); ∀ child-cap ⊄ parent → delegate REJECTED (D2); `budget.step` đơn điệu giảm remaining; `parse(repair(x))` ổn định.
  - **integration**: E2E slice "task 2 bước → plan → order(deps) → delegate → judge-by-evidence → FINISHED"; **resume round-trip cùng run_id** (D3/SPIKE-1: kill sau N1 → resume → không re-emit `tool.requested` của N1 · round_no liên tục · crash giữa txn không để checkpoint nửa-ghi).
  - **audit-adversarial** (`tests_audit/`): quét TĨNH + ĐỘNG toàn repo tìm ca vi phạm ranh giới — (a) **D1**: 0 call-site gọi tool/LLM ngoài `execute_tool` (grep AST + runtime assert bus); (b) **D5**: worker path không có nhánh nào ghi `acceptance_status.verdict` (chỉ gate); (c) **D4**: fuzz payload có SECRET_KEYS → 0 lọt ui_payload; (d) sandbox-escape (path traversal → SANDBOX_PATH_ESCAPE); (e) PolicyGate deny-list fail-closed.
- **Contract test cross-module** (event/API giữa module — bám Contract GĐ10): Orch↔Control-Plane (6 domain event GĐ5 đúng schema); Exec-Core↔Tools-Safety (`SafeToolPort` trả `CapabilityResult`, không throw); Exec-Core↔Discipline (middleware 2 chiều). Event cross-module đổi schema → contract test đỏ = chặn merge.
- **Lý do nặng property+audit:** false-finish/leo-quyền/rò-secret là lỗi *phổ quát trên mọi input*, ví-dụ-đơn-lẻ (pytest thường) không chứng minh được → cần property (Hypothesis sinh phản-ví-dụ) + audit (quét toàn call-site). **Loại pytest-only:** chứng minh cục bộ, bỏ lọt đúng 3 bệnh chết người (GĐ7 ADR-007). **Loại e2e-heavy/Selenium UI:** UI control-plane là sau-MVP (ADR-006), e2e dày giờ = phí.

### 6. CI/CD pipeline  (bám CI tối thiểu GĐ8 ô#6 — không bịa mới)
```
lint (ruff + no-BOM check) → type (mypy Public API) → unit → property(Hypothesis)
  → integration(E2E slice + resume round-trip D3) → audit-adversarial(D1/D4/D5 + sandbox/policy)
  → contract-test(cross-module event/API GĐ10) → build
```
- **Gate cứng (fail = chặn merge):** BẤT KỲ bước nào đỏ → PR không merge. **audit-adversarial + property là gate không-bỏ-qua** kể cả hotfix (đây là điểm bán). CI xanh là điều kiện cần của DoD.
- **CD:** merge trunk xanh → deploy **staging** tự động (single-deployable, `run_smoke.py` offline deterministic + E2E slice). Production: sau-MVP + go/no-go GĐ13 `/ship` (không thuộc delivery).
- **Lý do:** GĐ8 đã định "CI tối thiểu lint + pytest + audit-test"; delivery chỉ **chuẩn hoá + thêm thứ tự gate + đưa property/contract vào**, không dựng CI khác. **Loại deploy-thẳng-prod:** hệ chưa có baseline NFR (OQ-1), production gate là việc của `/ship` GĐ13.

### 7. Environment strategy
- **3 tầng: `dev` (local) · `staging` (CI deploy) · `prod` (sau-MVP, GĐ13).**
- Config qua **env var + `config/*.yaml`** (event/command catalog config-driven, closed allowlist — GĐ6 OQ-2 đóng). Không hard-code endpoint/model. LLM `model/endpoint = config runtime`, chuẩn OpenAI-compatible → 0 vendor-lock cứng (GĐ7).
- `var/workspace/` = **workspace jail** (mọi path tool phải `relative_to` — Contract Tools-Safety); tách theo run.
- **Lý do:** đủ tách dev/staging để chạy E2E slice thật (GĐ8 cần staging); prod hoãn đúng kỷ luật sau-MVP. **Loại thêm tầng UAT/pre-prod riêng:** thừa cho hệ single-node chưa có traffic thật; gộp vào staging + gate GĐ12/13.

### 8. Secret management  (redact — rủi ro cao, viết kỹ)
- Secret (LLM key/token) **CHỈ ở env var / secret store**, **KHÔNG trong repo**, không trong `config/*.yaml` commit. CI quét secret (reject nếu match SECRET_KEYS pattern).
- **Redact TẠI biên (Redactor, ~15 SECRET_KEYS):** `ui_payload` được che secret **trước khi rời `EventEmitter`** (validate→seq→**redact**→fan-out) — raw payload KHÔNG bao giờ rời emitter (Contract Control-Plane · REBRIEF #7 · I16). Mask đệ quy `'[REDACTED]'`, không mutate gốc.
- ⚠️ **Ràng buộc chặn ADR-006 (GĐ6/GĐ8 ô#8):** known-gap gốc — `tool.requested` từng log **raw args** ra jsonl. **Redact raw args PHẢI hoạt động TRƯỚC khi bật write-tool** (`fs_write`/`terminal_run`). Đây là **điều kiện chặn** cho mọi PR bật write-tool: có test 0-secret-in-jsonl xanh mới merge. Điều phối **Team Safety ↔ Team Observability**.
- **Lý do:** redact-tại-biên gắn secret-handling **một lần cho tất cả** ở đúng chokepoint control-plane, không rải rác mỗi tool. **Loại redact-ở-UI:** raw đã rời biên = đã rò vào log/transport; che ở UI là quá muộn (phá I16).

### 9. Feature flag
- **Flag cho slice rủi ro cao** để bật/tắt + rollback nhanh không cần redeploy. Ví dụ đặt tên: `write_tools_enabled` (gate write-tool sau khi redact xanh), `delegation_enabled` (bật multi-agent LÕI R3), `rag_enabled` (Knowledge optional, default OFF ở MVP — GĐ7 YAGNI).
- Flag đọc từ config runtime; default **an toàn nhất** (write/delegation/rag OFF cho tới khi test ranh giới xanh).
- **Lý do:** cho phép merge sớm (trunk-based) mà chưa "bật" hành vi nguy hiểm; rollback = tắt flag (giảm MTTR/DORA). **Loại nhánh dài để giữ tính năng chưa bật:** ngược trunk-based, gây drift.

### 10. Migration strategy
- **Đối tượng migration = SQLite checkpoint schema (`langgraph.sqlite`) + `AgentState` schema (v2)** — đây là **chân lý resume**, đổi schema mà không cẩn thận = hỏng resume (phá I10/I11).
- **Forward-only + phiên bản hoá schema `AgentState` (schema_version).** Resume đọc phải tương thích ngược ≥1 version (đọc được checkpoint cũ hoặc từ chối tường minh, KHÔNG re-run side-effect). Có **rollback script** cho mỗi migration DB.
- Migration chạy trong **cùng transaction atomic** như checkpoint (commands+round+save một txn — Contract Orch · evidence-A §6). `checkpoint.json` = projection UI, KHÔNG đọc để resume → migrate an toàn (chỉ SQLite là truth).
- **Lý do:** resume-đúng là D3 (điểm bán); schema drift là rủi ro âm thầm cao nhất. **Loại migration destructive/không-version:** một lần đổi schema là mọi run đang chạy resume sai — không chấp nhận. (Nếu tương lai SQLite→Postgres multi-instance: migrate qua cùng port checkpoint — GĐ7 ràng buộc.)

### 11. Observability standard  (event-log-first — viết kỹ)
- **Event-log-first (I3/glass-box):** mọi capability call phát `tool.requested` / `tool.completed` / `tool.failed` (bộ 3 chuẩn đã reconcile — OQ-3 đóng GĐ6); EventLogger append `events.jsonl` + `summary.json` + `metrics` (tool_calls/llm_calls/failures/blocks/parse_errors).
- **seq monotonic gap-free per-run**; `build_snapshot(events)` = linear fold **deterministic theo seq**, terminal-status guarded (replay(events[0..n]) = Snapshot(n)).
- Metric loop tối thiểu cho DORA/incident: `task_finished_total`, `task_blocked_total{reason}`, `false_finish_total` (= 0 là điểm bán), `delegation_rejected_total{reason}`, `parse_error_total`, `budget_tripped_total`.
- **Lý do:** event log = nguồn audit + replay + resume; là *cơ sở* để đo cả 5 invariant lẫn 4 DORA. **Loại log free-text rải rác:** không replay/audit được, không fold thành snapshot.

### 12. Incident process
- **On-call theo owner module** (GĐ10): sự cố loop/acceptance → Team Orchestration; chokepoint/session/resume → Team Platform; rò secret/audit lệch → Team Observability; escape jail/policy → Team Safety.
- **Rollback = tắt feature flag** (mục 9) trước, rồi điều tra bằng **event log replay** (`build_snapshot` tái dựng trạng thái tại seq sự cố). MTTR đo từ phát hiện → khôi phục.
- Sự cố chạm invariant (false-finish / leo-quyền / rò-secret) = **P1**: dừng bật flag liên quan, thêm audit/property-test bắt đúng ca đó vào regression trước khi bật lại.
- **Lý do:** owner rõ (không "sự cố của mọi người"); replay-from-log cho điều tra không phá hiện trường. (Ngưỡng alert/error-rate production **chưa có số → OQ-1 → Operate**, KHÔNG bịa.)

---

## Artifact 2 — DEFINITION OF READY + DEFINITION OF DONE

> DoD là **hàng rào tối thiểu — KHÔNG cắt dòng nào bất kể kích thước việc** (chỉ Standards mới rút theo rủi ro). DoR nhẹ hơn, rút gọn được vì backlog GĐ9 đã chuẩn (Story+AC sẵn).

### DEFINITION OF READY (item được phép vào sprint)
```
[ ] có AC (nằm DƯỚI story — backlog GĐ9, KHÔNG viết lại PRD)
[ ] có ước lượng (vừa 1–2 sprint; E10 đã cắt F3.2–F3.5 cho vừa — GĐ9)
[ ] phụ thuộc rõ (module đích + seam chạm; nếu chạm seam công khai → ghi owner cần điều phối)
[ ] đủ context để bắt đầu (invariant nào bị chạm? cần test loại nào: unit/property/integration/audit?)
```

### DEFINITION OF DONE (mọi item — bắt buộc, không cắt dòng nào)
```
[ ] code review pass — approval của OWNER module (CODEOWNERS GĐ10); chạm ≥2 module → mọi owner đích
[ ] test pass: unit + property(Hypothesis) + integration + contract + audit-adversarial — CI XANH
[ ] contract giữ — không phá Public API/seam module khác (Contract GĐ10); contract-test cross-module xanh
[ ] 5 invariant-kiểm-được XANH nếu PR chạm ranh giới (điểm bán — có test THẬT, adversarial):
      D1 · không call-site nào bypass execute_tool         (audit-adversarial)
      D2 · scope child ⊆ parent khi delegate                (property/Hypothesis)
      D3 · resume round-trip xanh cùng run_id, 0 side-effect (integration/SPIKE-1)
      D4 · 0 secret trong ui_payload (redact tại biên)       (audit + property)
      D5 · worker KHÔNG set verdict — chỉ gate ghi acceptance (audit-adversarial)
[ ] observability có — capability call phát tool.requested/completed vào events.jsonl; seq gap-free
[ ] doc cập nhật — Public API / event schema / ADR (nếu đổi quyết định lớn)
[ ] không giảm chất lượng — coverage không tụt, lint (ruff) + no-BOM + type sạch
[ ] merge xanh CI
```
> **Không đạt DoD → KHÔNG release.** Đây là cổng cứng của cả GĐ11.
> **Việc rủi ro cao thêm dòng:** PR bật **write-tool** (`fs_write`/`terminal_run`) → thêm `[ ] redact raw args xanh (0-secret-in-jsonl) TRƯỚC khi bật flag write_tools_enabled` (ADR-006). PR đổi **checkpoint/AgentState schema** → thêm `[ ] migration forward-only + rollback script + resume tương thích ≥1 version`.

**Vì sao DoD này khác DoD dự án thường:** dòng D1–D5 là 5 invariant của REBUILD-BRIEF (#2/#4/#5/#6/#7) biến thành test — chúng KHÔNG có trong DoD chung chung. Bỏ chúng = "Done" mất nghĩa cho sản phẩm này (dev sẽ merge code phá đúng điểm bán mà CI vẫn xanh).

---

## Artifact 3 — PR CHECKLIST

> Mỗi PR **link tới story/requirement** (sợi traceability ngược GĐ9→GĐ2–4). Ô "update API contract?" + "ảnh hưởng module khác?" bám THẲNG Module Contract GĐ10. Ô không áp → đánh **N/A**, KHÔNG xoá ô.

```
### PR — <feat|fix|refactor>(<module>): <mô tả 1 dòng>

[ ] link story/requirement  → S_._._ (backlog GĐ9)   |  epic E__  |  invariant chạm: D_ / none
[ ] có test — unit / property(Hypothesis) / integration / audit-adversarial (đánh loại nào áp dụng)
[ ] breaking change? → nếu CÓ: đã thông báo owner module đích + version bump
[ ] update API contract? → seam nào đổi (execute_tool / run_task_loop / DelegationManager.delegate /
                            SafeToolPort / EventEmitter.emit)? contract-test cross-module xanh? (N/A nếu nội bộ module)
[ ] có migration? → checkpoint/AgentState schema đổi? forward-only + rollback script? (N/A nếu không đụng DB)
[ ] security impact? → chạm scope/allowed_capabilities / sandbox / secret? (D4 redact xanh nếu chạm ui_payload/args)
[ ] observability (log/metric)? → phát tool.requested/completed đúng? metric mới cần? seq gap-free?
[ ] ảnh hưởng module khác? → module nào (GĐ10)? owner nào cần review? (N/A nếu chỉ trong package mình)
[ ] rollback plan nếu rủi ro cao? → sau feature flag nào (write_tools_enabled / delegation_enabled / rag_enabled)?
```

**Ví dụ minh hoạ (rút gọn) — PR đầu R1, story S1.1.1 chokepoint:**
```
### PR — feat(execution_core): execute_tool chokepoint + tool.requested/completed

[x] link story → S1.1.1 (F1.1 chokepoint, E01) | invariant chạm: D1
[x] có test — unit(envelope build) + audit-adversarial(0 call-site bypass execute_tool)
[ ] breaking change — N/A (module mới)
[x] update API contract? → expose execute_tool(ToolRequest)→CapabilityResult (seam DUY NHẤT); contract-test Exec-Core↔Control-Plane (tool.* schema) xanh
[ ] có migration? — N/A (chưa đụng SQLite)
[x] security impact? → scope-check tại execute_tool (capability ∉ allowed_capabilities → fail-closed); chưa bật write-tool
[x] observability → phát tool.requested/completed vào events.jsonl; seq gap-free test
[x] ảnh hưởng module khác? → Control-Plane (nhận tool.*) — review @team-observability
[ ] rollback — N/A (chưa có hành vi nguy hiểm; write-tool sau flag write_tools_enabled)
Reviewer: @team-platform (owner) + @team-observability (seam đích) — DoD ✔ D1 audit xanh · ✔ contract giữ · ✔ observability.
```
> **Góc nhìn lãnh đạo cho checklist:** không cần — nó là công cụ dev. Giá trị cho lãnh đạo nằm ở **DoD + 4 chỉ số DORA** phía trên.

---

## Tự soi trước khi chốt (bắt buộc — theo rubric)

1. **Lãnh đạo đọc RIÊNG đoạn MỞ (DoD 1 khối + 4 DORA) có biết giao hàng on-track không, không vướng jargon?** — CÓ: DoD gói 1 khối 9 dòng + bảng D1–D5 (điểm bán thành test) + bảng 4 DORA (kèm ⚠️ số baseline chưa có = OQ-1). Không mở bằng YAML.
2. **Dev đủ hành động: branch thế nào · CI chạy gì · test tối thiểu · PR qua cổng nào · "Done" là gì?** — CÓ: 12 mục Standards có layout repo + thứ tự CI gate + tỉ lệ pyramid + PR checklist 9 dòng + DoD.
3. **Đúng + ĐỦ 3 artifact (Standards đủ 12 mục · DoR/DoD · PR Checklist), DoD giữ nguyên khối không cắt?** — CÓ: 12 mục (mục rủi ro cao secret/migration/observability/test viết kỹ, mục quen gọn); DoR 4 dòng + DoD 9 dòng lõi (không cắt) + dòng-thêm theo rủi ro; PR checklist 9 dòng có link story.
4. **Chuẩn bám Module Contract GĐ10 (contract-test cho event cross-module, ô checklist nối contract thật), không bịa?** — CÓ: CODEOWNERS = owner GĐ10; contract-test = 6 event GĐ5 + SafeToolPort + middleware (Test contract GĐ10); ô "update API contract/ảnh hưởng module khác" liệt kê đúng 2 seam GĐ10 + SafeToolPort/EventEmitter; CI = CI tối thiểu GĐ8; stack = GĐ7 (không chọn lại).
5. **Mỗi quyết định lớn có LÝ DO + phương án đã loại?** — CÓ: repo (loại poly-repo/phẳng), branching (loại git-flow), test pyramid (loại pytest-only/e2e-heavy), redact (loại redact-ở-UI), CI (loại deploy-thẳng-prod), env (loại tầng UAT thừa), migration (loại destructive), flag (loại nhánh dài).
6. **Không lấn vai?** — CÓ: đặt CHUẨN + CỔNG, KHÔNG code slice (→ `/frame`), KHÔNG viết test-result/sign-off (→ `/uat`), KHÔNG đào bug (→ `/review`), KHÔNG vẽ lại module/chọn lại stack.

**Open-Q mang sang sau (không bịa):**
- **OQ-1** (kế thừa) — baseline 4 chỉ số DORA (lead time · deploy freq · change-failure · MTTR) + ngưỡng alert/error-rate + P95 loop **chưa có số** → delivery đặt *cách đo*; **số thật đo ở Operate (GĐ14)**, KHÔNG bịa.
- **OQ-M1** (kế thừa GĐ10) — nếu Skills (E07) phình thành catalog động có state → tách khỏi Discipline thành package/owner riêng → cập nhật CODEOWNERS + contract-test khi thaw.
- **SPIKE-1** (từ GĐ8) — D3 (resume round-trip) là **điều kiện chặn đóng R1**: phải pass a/b/c (không re-emit tool.requested của bước đã done · round_no liên tục · crash giữa txn không nửa-ghi) TRƯỚC khi đóng R1; fail → phương án B orchestrator tự viết (không đổi Standards, chỉ đổi implementation module Orchestration).

---

## Cổng GĐ11 — DELIVERY (tự-quyết; đóng vai CTO/Kiến trúc sư chủ sở hữu chuẩn · Eng-manager mở cổng)

**Câu hỏi cổng (doc GĐ11):** *"Item đạt Definition of Done chưa? Chuẩn delivery đủ để mọi team giao hàng an toàn, song song chưa?"*

**Phân vai (A5):** **CTO / Kiến trúc sư** sở hữu chuẩn (viết 3 artifact này). **Reviewer được chỉ định (owner module)** duyệt PR theo checklist. **Team owner mỗi module** giữ chất lượng module mình (GĐ10). `delivery` (AI) DRAFT chuẩn + checklist + cổng + tự soi; KHÔNG tự tuyên "đã Done" cho item nào (chưa có PR thật) — chỉ đặt luật để mọi item đi qua cùng cổng.

**Chủ sở hữu (CTO/Kiến trúc sư) TRÌNH BẰNG CHỨNG:**
1. **Đủ 3 artifact** — Delivery Standards (12 mục) · DoR/DoD (DoD không cắt dòng) · PR Checklist (9 dòng, có link story). ✔
2. **DoD phản ánh 5 invariant-kiểm-được** — D1 (bypass execute_tool) · D2 (scope⊆parent) · D3 (resume round-trip) · D4 (0 secret ui_payload) · D5 (worker không set verdict), mỗi cái gắn loại test THẬT. ✔
3. **Bám nguồn GĐ trước** — CODEOWNERS/owner = GĐ10; contract-test = Test contract GĐ10; CI = CI tối thiểu GĐ8; stack/test = GĐ7; PR link story = backlog GĐ9. Không bịa module/stack/API mới. ✔
4. **Chuẩn đủ cho 6 team song song** — mỗi package 1 owner + review-theo-owner + seam chạm cần owner đích + audit-adversarial chặn đúng 3 bệnh chết người → team code song song không phá ranh giới nhau. ✔ (⚠️ số DORA baseline chưa có = OQ-1, không chặn cổng — đặt cách đo là đủ để bắt đầu.)

```
═══ CỔNG GĐ11 — DELIVERY: HexAgent (clean rebuild) ═══
3 artifact: Delivery Standards (12 mục, rủi ro cao secret/migration/observability/test viết kỹ) ·
            DoR (4) + DoD (9 dòng lõi KHÔNG cắt + dòng-thêm theo rủi ro) · PR Checklist (9 dòng, link story).
DoD lõi điểm bán (có test): D1 bypass-execute_tool · D2 scope⊆parent · D3 resume-round-trip ·
                            D4 0-secret-ui_payload · D5 worker-không-set-verdict.
Test pyramid: ~60 unit / 15 property(Hypothesis) / 15 integration / 10 audit-adversarial + contract cross-module.
CI: lint(no-BOM)→type→unit→property→integration(+resume)→audit-adversarial→contract→build (mọi bước đỏ = chặn merge).
Bám nguồn: owner=GĐ10 · contract-test=Test-contract GĐ10 · CI=GĐ8 · stack/test=GĐ7 · link story=backlog GĐ9. Không bịa.
Open-Q: OQ-1 (số DORA/alert → Operate) · OQ-M1 (Skills tách → cập CODEOWNERS) · SPIKE-1 (D3 chặn đóng R1).
Câu hỏi cổng: Item đạt DoD chưa? Chuẩn đủ để 6 team giao hàng an toàn, song song chưa?
════════════════
```

**Quyết định cổng (tự-quyết — product owner: "không hỏi approval", đóng vai CTO/Eng-manager).**
**GATE: GO.** Lý do: đủ 3 artifact với DoD là cổng cứng phản ánh đúng 5 invariant-kiểm-được (điểm bán → test thật); chuẩn bám 4 nguồn GĐ trước đã-qua-cổng (owner GĐ10 · test-contract GĐ10 · CI GĐ8 · stack/test GĐ7) + link story GĐ9 → không bịa; mỗi package 1 owner + review-theo-owner + audit-adversarial chặn 3 bệnh chết người → **6 team code song song không phá ranh giới nhau**. `delivery` KHÔNG tự tuyên item nào "Done" (chưa có PR) — chỉ đặt luật; đúng phân vai A5.

**Phương án đã loại ở tầng cổng:**
- (a) *Chặn GO tới khi có số baseline DORA / SPIKE-1 pass* — **loại:** số DORA là để *đo sức khoẻ vận hành* (Operate GĐ14), không phải điều kiện *đặt chuẩn*; SPIKE-1 là rủi ro *thực-thi-R1* (chặn đóng R1, không chặn việc chốt chuẩn để 6 team bắt đầu). Chặn cổng = trộn vai GĐ11 với GĐ8/14, nghẽn 6 team chờ. Ghi OQ-1 + SPIKE-1 có địa chỉ thay vì chặn.
- (b) *Nới DoD (bỏ property/audit cho hotfix chạy nhanh)* — **loại:** D1–D5 là điểm bán; nới đúng cổng chặn 3 bệnh chết người = cho phép merge code phá điểm bán mà CI vẫn xanh (false-safe). DoD không cắt dòng bất kể kích thước việc (luật cứng GĐ11).
- (c) *Áp pyramid cổ điển 70/20/10 unit-nặng cho "chuẩn"* — **loại:** hệ này bán bất-biến-kiểm-được, không bán bề-rộng-feature; unit-nặng bỏ lọt lỗi *phổ quát trên mọi input* (false-finish/leo-quyền/rò-secret) → cố ý nghiêng property+audit (GĐ7 ADR-007), có lý do ghi rõ.

---

## Bàn giao sang `uat` (GĐ12)

```
═══ BÀN GIAO — Delivery Standards hex-agent-rebuild · GĐ11 xong ═══
Đã chốt   : Delivery Standards (12 mục) + DoR/DoD (DoD 9 dòng lõi + 5 invariant-kiểm-được D1–D5 KHÔNG cắt) +
            PR Checklist (9 dòng, link story GĐ9). Áp mọi team; DoD = cổng cứng "không đạt → không release".
Artifact  : rebuild-hex-agent/pipeline/11-delivery.md  (+ state pipeline/delivery.json)
Test pyramid dẫn vào UAT : ~60 unit / 15 property / 15 integration / 10 audit + contract cross-module →
            uat map AC(GĐ9)→Test Case→Result trên đúng bộ này; D1–D5 = 5 acceptance-security cứng để sign-off.
Theo dõi  : · SPIKE-1/D3 resume-round-trip — điều kiện chặn đóng R1 (phải pass a/b/c) — uat verify
            · ADR-006 redact-raw-args TRƯỚC bật write-tool (D4) — Safety↔Observability — uat security sign-off
            · OQ-1 số DORA/alert threshold → Operate (GĐ14), không bịa · OQ-M1 Skills tách → cập CODEOWNERS
→ Chứng minh hệ làm ĐÚNG (mapping AC→test→result, UAT + security sign-off): chạy /uat (GĐ12)
→ Code từng slice theo chuẩn này (vd S1.1.1 chokepoint / S1.6.1 SPIKE-1): chạy /frame
→ Đào gap sâu (edge case, error path, permission) một luồng trước khi verify: chạy /review
════════════════
```
*Chỉ liệt kê, KHÔNG tự chọn hộ user chạy skill nào tiếp.*

*Traceability:* GĐ11 **nhận** Module Map + Contract GĐ10 (6 module · 6 owner · 2 seam · Test contract) + Live Slice GĐ8 (CI tối thiểu lint→pytest→audit) + Tech Decision GĐ7 (Python 3.11·LangGraph·SQLite·OpenAI-compatible·pytest+Hypothesis+audit·SSE) + Backlog GĐ9 (Story+AC để PR link ngược) → sinh **Delivery Standards + DoR/DoD + PR Checklist**: CODEOWNERS ánh xạ owner GĐ10 · contract-test = 6 event GĐ5/SafeToolPort/middleware (Test contract GĐ10) · DoD 5 invariant-kiểm-được = REBRIEF #2/#4/#5/#6/#7 thành test · PR link story ngược GĐ9→GĐ2–4 · test pyramid dẫn xuôi vào UAT GĐ12 → **bàn giao** `/uat` (chính) + `/frame` (code slice) + `/review` (đào gap). Sợi liền hai đầu: ngược (owner/contract/story) + xuôi (test pyramid → uat sign-off). Ẩn số treo có địa chỉ: OQ-1→Operate, SPIKE-1/D3→R1+uat, OQ-M1→modules sau.
