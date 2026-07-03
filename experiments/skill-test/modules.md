```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Roadmap + Backlog (Epic→Feature→Story→AC)" lấy từ prompt/file bạn đưa, CHƯA qua cổng GĐ9 (skill /backlog).
- Rủi ro: (1) chưa truy vết ngược được về pipeline; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /backlog trước để có "Roadmap + Backlog (Epic→Feature→Story→AC)" đã qua cổng.
```

Project: `/Users/uspro/Desktop/namnson/hex_agent` (verified). Tôi bám ranh giới THẬT trong repo (README + docs/reference/runtime-flow.md + MAP.md), không bịa. Vì bạn muốn **nhiều team làm song song**, tôi cắt module theo **bounded context + data/ownership + tần suất đổi + ranh giới an toàn**, KHÔNG theo màn hình UI.

Một ẩn số đã ghi thành open-Q (không tự bịa): bạn chưa đưa backlog Epic→Feature→Story→AC, nên tôi map theo *năng lực* mà repo đang có (E01–E10, E21) chứ chưa kiểm chéo được "mọi feature rơi đúng một module".

---

## Artifact 1 — MODULE MAP

**GÓC NHÌN LÃNH ĐẠO** (khi có sự cố, gọi ai?)

| Module | Team owner | Sở hữu gì | KHÔNG sở hữu gì |
|---|---|---|---|
| **Kernel** (nhân) | Team Platform | Mọi lời gọi tool/LLM đi qua `execute_tool`; registry; envelope; session/state | Không tự chạy LLM thật, không điều phối luồng, không lo delegation |
| **Orchestration** (điều phối) | Team Runtime | LangGraph substrate, topology, SQLite checkpoint (run/resume) | Không định nghĩa tool, không gọi model thật |
| **LLM Adapter** | Team Platform | Cổng ra model (JSON-mode, lazy) | Không quyết prompt nghiệp vụ, không giữ state |
| **Tools & Safety** | Team Capabilities | Toolbox, sandbox, middleware quanh mỗi tool call | Không sở hữu chokepoint kernel (chỉ cắm vào) |
| **Delegation** (đa-agent) | Team Multi-Agent | Chokepoint `delegate` RIÊNG, policy độ sâu/budget, progress store | Không dùng đường `execute_tool` của kernel (cửa riêng — ranh giới cứng) |
| **Knowledge/RAG** | Team Data | Qdrant + memory, retrieval | Không giữ vòng đời run |
| **Control Plane** (E21) | Team Realtime | Event envelope, emitter, redaction, approval-gate, permission per-agent | Không thực thi tool; chỉ quan sát/can thiệp |
| **Observability & UI** | Team DX | event_log, inspect CLI, console UI | Read-only với run state, không đổi luồng |

```text
MODULE MAP (bounded context → module → owner → phụ thuộc)
  Kernel          ← ctx "capability runtime"  · Team Platform     · LÕI; mọi module gọi execute_tool
  Orchestration   ← ctx "run lifecycle"       · Team Runtime      · → Kernel (chạy tool), → Delegation (node delegate), → checkpoint SQLite
  LLM Adapter     ← ctx "model egress"        · Team Platform     · ← Kernel gọi qua capability llm.chat
  Tools & Safety  ← ctx "capabilities"        · Team Capabilities · cắm vào Kernel registry + middleware
  Delegation      ← ctx "multi-agent"         · Team Multi-Agent  · CỬA RIÊNG (không qua execute_tool); tạo child session
  Knowledge/RAG   ← ctx "retrieval"           · Team Data         · expose như tool qua Kernel
  Control Plane   ← ctx "realtime control"    · Team Realtime     · nghe event từ Orchestration/Kernel; gate action
  Obs & UI        ← ctx "observability/DX"    · Team DX           · đọc event_log + state (read-only)
```

**Lý do 3 lằn ranh dễ gộp nhầm (đã loại):**
- **Delegation KHÔNG gộp vào Kernel** — dù cùng "chạy agent". Loại vì repo cố ý tách chokepoint: `execute_tool` (tool/LLM) vs `DelegationServicePort.delegate` (cửa riêng, node graph riêng). Gộp lại là phá invariant lõi.
- **Orchestration tách khỏi Kernel** — `core/` framework-agnostic, không import LangGraph. Team Runtime đổi topology/graph mà không đụng nhân. Gộp sẽ trói nhân vào LangGraph.
- **Control Plane (E21) tách riêng** — tần suất đổi cao (đang active, transport/UI pending) khác hẳn nhân đã ổn định. Đã cân gộp vào Observability, loại vì Control có quyền *can thiệp* (approval-gate, permission), Obs chỉ *đọc* — ranh giới security khác nhau.

---

## Artifact 2 — MODULE CONTRACT (module lõi + 2 module ranh giới cứng; các module rìa ghi gọn)

**MODULE CONTRACT — Kernel**  ·  Owner: Team Platform
```
[Lãnh đạo]      : giữ "một cửa duy nhất" cho mọi hành động. Tool/LLM lỗi → hỏi Team Platform trước.
Responsibilities: resolve tool name → executor; chạy execute_tool; quản session/state, envelope.
Owns            : execute_tool chokepoint · CapabilityRegistry · TaskEnvelope/ToolRequest/CapabilityResult · KernelSession/state.
Does NOT own    : LLM thật (LLM Adapter) · điều phối luồng (Orchestration) · delegation (Delegation, cửa riêng) · tool cụ thể (Tools&Safety).
Public API      : execute_tool(ToolRequest)→CapabilityResult · registry.register/resolve · session.complete_task/fail_task. (đặc tả interface độc lập ngôn ngữ)
Domain events   : phát tool-invoked/tool-result qua event bus (Obs + Control nghe).
Permission      : mọi capability đi qua middleware (safety cắm ở đây); LLM là capability llm.chat, không đường tắt.
Error codes     : TOOL_NOT_FOUND (NullToolPort fallback) · CAPABILITY_DENIED.
SLA/SLO         : critical path — mọi call qua đây; giữ overhead middleware thấp, thread-safe.
Test contract   : contract test cho mọi module cắm registry (executor phải trả CapabilityResult hợp lệ).
```

**MODULE CONTRACT — Delegation**  ·  Owner: Team Multi-Agent
```
[Lãnh đạo]      : giữ luồng agent-giao-việc-cho-agent-con. Lỗi delegate → Team Multi-Agent, KHÔNG phải Team Platform.
Responsibilities: chokepoint delegate riêng · policy depth/budget/capability-scope · child session · progress store.
Owns            : DelegationServicePort.delegate · delegation policy · progress store (ordered, idempotent).
Does NOT own    : execute_tool (KHÔNG đi qua kernel chokepoint — ranh giới cứng) · topology graph (Orchestration inject node delegate).
Public API      : delegate(request)→result · store.read_progress. (OpenAPI/interface độc lập ngôn ngữ)
Domain events   : phát delegation-progress (Control/Obs nghe).
Permission      : policy chặn vượt depth/budget/scope.
Error codes     : DELEGATION_DEPTH_EXCEEDED · DELEGATION_BUDGET_EXCEEDED · TARGET_AMBIGUOUS.
Test contract   : concurrency + resume test (repo đã có tests/ cho delegation).
```

**MODULE CONTRACT — Orchestration**  ·  Owner: Team Runtime
```
[Lãnh đạo]      : giữ vòng đời một run (chạy/dừng/resume). Run treo/không resume được → Team Runtime.
Responsibilities: compiled StateGraph 1-substrate · topology guard→agent→tool/delegate/finish · facade run/resume · SQLite checkpoint.
Owns            : graph runtime · orchestrator facade · var/agent_runs/<run_id>/langgraph.sqlite (checkpoint = nguồn sự thật parent-graph).
Does NOT own    : execute_tool (Kernel) · delegate impl (Delegation) · UI hiển thị (Obs&UI).
Public API      : run(task)→run_id · resume(run_id) · run_agent(...) (back-compat).
Error codes     : RESUME_CHECKPOINT_MISSING · GRAPH_INVALID_TRANSITION.
SLA/SLO         : checkpoint durability (run phải resume được sau crash).
Test contract   : resume test đọc checkpoint SQLite; contract với Kernel qua node tool.
```

**Các module rìa (contract gọn — một team, tần suất đổi/rủi ro thấp hơn; vẫn đủ ô bắt buộc):**
- **LLM Adapter** — Owner Team Platform · Owns: cổng model JSON-mode, lazy client · Does NOT own: prompt nghiệp vụ, state · Public API: `chat(messages)→json` (gọi qua capability `llm.chat`). Gọn vì một cổng ra, một team.
- **Tools & Safety** — Owner Team Capabilities · Owns: toolbox, sandbox, ToolMiddleware · Does NOT own: kernel chokepoint (chỉ cắm registry) · Public API: mỗi tool implement `ToolPort`. Error: `SANDBOX_VIOLATION`.
- **Knowledge/RAG** — Owner Team Data · Owns: Qdrant + memory retrieval · Does NOT own: run lifecycle · Public API: expose như tool qua Kernel registry. Gọn vì offline-capable, cắm qua registry.
- **Control Plane (E21)** — Owner Team Realtime · Owns: RuntimeEvent envelope, emitter (validated/redacted/sequenced), approval-gate checkpoint, per-agent Permission · Does NOT own: thực thi tool · Public API: emit/subscribe event · redaction boundary. Error: `EVENT_SCHEMA_INVALID`. (Đầy đủ hơn vì đang active + có quyền can thiệp + security boundary.)
- **Obs & UI** — Owner Team DX · Owns: event_log, inspect CLI, console UI · Does NOT own: đổi run state (read-only) · Public API: `inspect list/summary`, UI đọc facade. Gọn vì read-only.

---

## Tự soi (trước khi trình cổng)
- **Lãnh đạo đọc được?** Bảng module × owner mở đầu trả lời thẳng "sự cố ở đâu gọi ai", không jargon. ✔
- **Dev đủ hành động?** Mỗi contract lõi có Public API + Owns + Does NOT own + event/error → team code trong ranh giới không phải hỏi lại. ✔
- **Chia theo domain, không theo màn hình?** Mỗi module = một bounded context của repo (kernel/graph/delegation/…), không phải cụm màn hình. Không module hai owner. ✔
- **Bám nguồn?** Ranh giới bám runtime-flow (2 chokepoint tách biệt) + MAP.md, không bịa context mới. ✔
- **Open-Q còn treo (KHÔNG tự bịa):** chưa có backlog GĐ9 → chưa kiểm chéo "mọi feature rơi đúng một module". `middleware/`, `adapters/`, `roles/`, `features/` tôi xếp vào module gần nhất (Tools&Safety / Kernel-ports / Multi-Agent) — cần bạn xác nhận owner khi có backlog.

---

## Cổng GO/NO-GO (GĐ10)
Câu hỏi: **"Ownership & contract đã rõ để các team chạy delivery SONG SONG chưa?"**

Bằng chứng tôi trình (đóng vai Kiến trúc sư — KHÔNG tự tuyên GO):
- Mỗi module đúng 1 owner; không data/event bị hai module cùng sở hữu (checkpoint SQLite chỉ Orchestration; registry chỉ Kernel; delegate chỉ Delegation).
- Mọi phụ thuộc đi qua contract/event, không gọi lén nội bộ (Delegation cửa riêng là ranh giới cứng đã tôn trọng).
- Còn lỏng: owner của `middleware/adapters/roles/features` chờ backlog GĐ9 xác nhận.

Quyết định GO là của **bạn (vai CTO)**. Bạn duyệt GO thì tôi mở khối bàn giao; chưa GO thì chỉ tôi ô cần siết.

```text
═══ BÀN GIAO — hex_agent · GĐ10 (chờ bạn duyệt GO) ═══
Đã chốt   : 8 module · mỗi module 1 owner + contract · does-NOT-own rõ · 2 chokepoint tách biệt được tôn trọng.
Theo dõi  : Control Plane (E21) đang active — contract có thể đổi; owner middleware/adapters/roles chờ backlog.
→ Nhiều team code song song, cần chuẩn giao hàng + DoD: chạy /delivery (GĐ11) — mỗi slice đóng khung bằng /frame
→ Chỉ build ngay MỘT slice trong một module: chạy /frame
→ Ranh giới đụng code cũ, cần hiểu trước khi module đụng vào: chạy /atlas hoặc /explain
════════════════
```
(Chưa ghi artifact vào repo `hex_agent` — mặc định không đụng repo code. Muốn tôi ghi `state/.../pipeline/modules.md` hoặc `hex_agent/docs/modules.md`, nói một tiếng.)
