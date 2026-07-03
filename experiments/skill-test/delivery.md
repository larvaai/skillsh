```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Module Map + Module Contract" lấy từ prompt/mô tả bạn đưa (hệ multi-agent microkernel: core/kernel · delegation · graph · orchestrator/SQLite checkpoint · toolbox…), CHƯA qua cổng GĐ10 (skill /modules).
- Rủi ro: (1) chưa truy vết ngược được về pipeline; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /modules trước để có "Module Map + Module Contract" đã qua cổng.
```

Tôi đã liếc repo thật (`README.md`, `docs/code-standards.md`, `docs/reference/known-risks.md`, `.github/workflows/ci.yml`, `pyproject.toml`) để chuẩn khớp thực tế, không đặt luật trên giấy. Đây là **GĐ11 — chốt CHUẨN giao hàng an toàn**; tôi không code slice (đó là `/frame`) và không viết test-result/sign-off (đó là `/uat`).

---

## Góc nhìn lãnh đạo (đọc 30 giây)

**"Xong" của hex_agent = 1 khối Definition of Done bên dưới.** Không đạt đủ khối đó → không merge, không release. Vì đây là microkernel nơi *mọi* call đi qua một chokepoint và mọi run resume từ SQLite, DoD thêm 3 hàng rào riêng của hệ này: **(a) không có đường thực thi tool nào ngoài `execute_tool`**, **(b) state bỏ vào checkpoint phải serializable + có test resume**, **(c) tool đụng filesystem phải qua workspace jail**. Ba dòng này là chỗ hệ "vỡ âm thầm" nếu bỏ.

Từ hôm nay bắt đầu đo **4 chỉ số DORA**: lead time · deployment frequency · change-failure rate · recovery time — exec nhìn 4 số này để biết đội giao nhanh và ổn định không, khỏi đọc YAML.

---

## Artifact 1 — DELIVERY STANDARDS (12 mục, áp mọi team)

- **Repository:** mono-repo hiện tại (một package Python, epics E01–E21). Giữ nguyên — hệ chia theo *module domain* (kernel · delegation · graph · orchestrator · toolbox · rag · control), không chia repo. Lý do: một compiled LangGraph substrate + kernel chia sẻ đóng băng → tách repo sẽ cắt lineage event. Loại poly-repo.
- **Branching:** trunk-based + short-lived branch, PR ≤ ~400 dòng. Lý do: team nhỏ, invariant tập trung ở 6 file dễ vỡ nên muốn merge nhanh, review kỹ. Loại git-flow (nhánh dài → merge đau quanh `graph/state.py`).
- **Coding standard:** theo `docs/code-standards.md` — mỗi PR PHẢI bảo vệ các bất biến kiến trúc (§1.1 chokepoint, §1.3 freeze). UTF-8 no BOM. `var/` gitignored.
- **Review policy:** ≥1 reviewer là owner module bị đụng. PR chạm 1 trong 6 file dễ vỡ (`core/kernel.py`, `graph/state.py`, `orchestrator/loop.py|checkpoint.py`, `graph/runtime.py|nodes.py`, `delegation/policy.py|manager.py`, `safety/sandbox.py`+`toolbox/filesystem.py`) → **bắt buộc 2 reviewer**.
- **Testing pyramid:** ~70 unit / 20 integration / 10 e2e-smoke. **Contract test** cho ranh giới cross-module: delegation `scope con ⊆ scope cha`, envelope `CapabilityResult`, resume SQLite. Lý do đo tỉ lệ này: logic tập trung ở kernel/graph → dày unit + vài integration là đủ; loại "dồn e2e" (chậm, khó định vị vỡ invariant).
- **CI/CD pipeline:** giữ `ci.yml` đang chạy — `ruff check` → `pytest tests` → `pytest tests_audit` (chặn regress audit finding) → job RAG/Qdrant. Bổ sung điều kiện merge: **audit suite phải xanh**. CD: `run_smoke.py` deterministic (no LLM/network) là cổng khói.
- **Environment strategy:** dev (offline, backend RAG `memory`) / staging (Qdrant thật) / prod. Lý do 3 tầng: RAG có backend nặng tách riêng, cần staging thật trước prod.
- **Secret management:** 🔴 **rủi ro LIVE đã biết** — `core/kernel.py:79-82` ghi raw `args` vào `events.jsonl`. **Luật cứng: trước khi wire tool có write/MCP, phải redact (`args_digest` + `safe_preview`).** Secret không nằm trong repo, không nằm trong tool args log. (mảnh mở: nơi lưu secret store — open-Q cần bạn xác nhận.)
- **Feature flag:** capability bật/tắt qua `config/features.yaml` (loader pattern có sẵn). Middleware `retry`/`policy` mặc định *tắt* — coi như flag; bật retry chỉ khi tool khai báo `read_only/idempotent` (footgun LATENT đã biết).
- **Migration strategy:** không phải DB migration mà là **schema state** — `graph/state.py schema_version` hiện = 2. Đổi shape `session.state` → **tăng `schema_version` + thêm nhánh migrate + test resume**, forward-compatible. SQLite checkpoint là nguồn sự thật; `checkpoint.json` chỉ là projection UI, cấm resume từ nó.
- **Observability standard:** giữ thứ tự event `tool.requested → chain → tool.completed|failed` cho mọi call; log JSON `events.jsonl` + `summary.json` per run. Tối thiểu mỗi tool mới: emit đủ cặp event + inspect được qua `observability.inspect`.
- **Incident process:** on-call theo owner module. Recovery ưu tiên: đọc `events.jsonl` + SQLite (không tin `checkpoint.json`); rollback bằng tắt flag capability trong `features.yaml`.

---

## Artifact 2 — DEFINITION OF READY / DONE

**Definition of Ready** (được vào sprint): có AC · có ước lượng · phụ thuộc module rõ · biết đụng file dễ vỡ nào chưa.

**Definition of Done** (BẮT BUỘC mọi item — không đạt → không release):
```
[ ] code review pass (2 reviewer nếu chạm file dễ vỡ)
[ ] test pass: unit + integration + contract của module đụng tới
[ ] CI xanh: ruff + tests + tests_audit (audit KHÔNG được regress)
[ ] chokepoint giữ: không có đường thực thi tool ngoài execute_tool; LLM vẫn là capability llm.chat
[ ] state serializable + có test resume nếu đổi shape session.state (schema_version bump)
[ ] filesystem tool đi qua resolve_in_workspace (workspace jail)
[ ] observability: cặp tool.requested/completed đủ, không log secret raw
[ ] doc cập nhật (code-standards / runtime-flow nếu đổi topology hoặc invariant)
```

---

## Artifact 3 — PR CHECKLIST
```
[ ] link story/requirement          [ ] có test (unit+integration)
[ ] breaking change? (đã báo owner)  [ ] update contract? (envelope / delegation scope / event order)
[ ] có migration state? (schema_version bump + test resume)   [ ] security impact? (jail / redact args)
[ ] observability (event pair đủ)?   [ ] ảnh hưởng module khác? (kernel/graph/orchestrator lan rộng)
[ ] rollback plan nếu rủi ro cao? (tắt flag capability)       [ ] chạm file dễ vỡ? → 2 reviewer
```
Ô nào không áp cho PR đó → đánh **N/A**, không xoá ô.

---

## Tự soi trước khi chốt
- Lãnh đạo đọc khối MỞ (DoD + 4 DORA) hiểu on-track không jargon — ✔.
- Dev đủ hành động: branch, CI chạy gì, test tối thiểu, cổng PR, "Done" là gì — ✔.
- Đủ 3 artifact, DoD giữ nguyên khối không cắt — ✔.
- Bám thực tế repo (ci.yml, code-standards, known-risks 6 file + risk LIVE args log) chứ không bịa — ✔.
- Quyết định lớn có lý do + phương án loại (branching, repo, test tỉ lệ) — ✔.
- Mảnh còn mở: **secret store ở đâu** — chưa có trong mô tả, để open-Q, không tự bịa.

---

## Cổng GO/NO-GO (GĐ11)

> *"Item đạt Definition of Done chưa? Chuẩn delivery đủ để mọi team giao hàng an toàn, song song chưa?"*

Chuẩn đã bám 6 invariant thật + risk LIVE của hệ. **Tôi DRAFT — không tự tuyên bố pass.** Quyền GO thuộc **CTO/Kiến trúc sư** (sở hữu chuẩn), owner mỗi module giữ chất lượng phần mình. Bạn cần chốt: (1) secret store đặt đâu; (2) đồng ý bắt buộc 2 reviewer cho 6 file dễ vỡ không. Duyệt xong tôi ghi artifact.

```
═══ BÀN GIAO — Delivery Standards hex_agent ═══
Đã chốt: Delivery Standards (12 mục) + DoR/DoD + PR Checklist (áp mọi team)
Artifact: state/project/hex_agent/pipeline/delivery.md
→ Chứng minh hệ làm đúng (mapping AC→test→result, UAT + security sign-off): chạy /uat (GĐ12)
→ Code từng slice theo chuẩn này: chạy /frame
→ Đào gap sâu (edge case, error path, permission) một luồng: chạy /review
═══════════════════
```
Tôi chỉ liệt kê — bạn quyết chạy skill nào tiếp.
