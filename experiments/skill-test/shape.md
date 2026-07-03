```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Domain Model" lấy từ prompt/file bạn đưa, CHƯA qua cổng GĐ5 (skill /idea).
- Rủi ro: (1) chưa truy vết ngược được về pipeline; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /idea trước để có "Domain Model" đã qua cổng.
```

Domain đã rõ. Tôi nhận 4 bất biến bạn chốt làm ranh giới và sinh nguyên bộ SHAPE (GĐ6). Đây là kiến trúc để **rebuild** — tôi bám hiện trạng `hex_agent` (đã liếc `core/`, `docs/system-architecture.md`, `docs/reference/`) để không đề hình chửi nhau với thứ đang chạy, nhưng KHÔNG chốt framework — LangGraph/SQLite ở đây là **ràng buộc do domain ép**, còn chọn công cụ là việc `/stack` (GĐ7).

Domain nhận vào (4 bất biến → thành ranh giới GĐ6):
- **Kernel dùng chung + phiên chạy riêng** → tách `AgentKernel` (frozen, chia sẻ) khỏi `KernelSession` (sở hữu run state).
- **MỌI lời gọi LLM/tool phải qua một cửa `execute_tool`** → một chokepoint duy nhất; LLM cũng là capability `llm.chat`, không đường tắt.
- **Delegation đi cửa riêng** → chokepoint thứ hai, KHÔNG phải method của kernel.
- **SQLite là nguồn checkpoint** → SQLite = sự thật để resume; mọi thứ khác chỉ là projection.

---

## 1. ARCHITECTURE BRIEF — hex_agent (multi-agent microkernel)

**Góc nhìn lãnh đạo:** Một khối chạy duy nhất (single deployable, không phải cụm service) dựng theo kiểu *microkernel/hexagonal*: một lõi cứng nhỏ ở giữa, mọi thứ có thể thay được cắm quanh nó qua "cửa" (port). Giá trị kinh doanh của hình này: **mọi hành động của agent — gọi LLM, gọi tool, giao việc con — đều đi qua cửa kiểm soát, nên an toàn/nhật ký/khả năng khôi phục không bao giờ bị bỏ qua**, và có thể thay LLM/vector-store/UI mà không đụng lõi. Rủi ro lớn nhất (agent đệ quy mất kiểm soát, mất tiến trình khi crash, rò dữ liệu qua log) đã được khoá bằng ADR-002/003/005 dưới.

| Ô | Quyết định |
|---|---|
| **Architecture style** | Microkernel + Hexagonal (ports & adapters), **single deployable**. Không microservices — đây là 1 domain (điều phối agent), 1 runtime agent; tách service chỉ thêm tải vận hành. |
| **Module boundary** | **Core** (registry, event bus, session factory, chokepoint `execute_tool`, freeze) sở hữu lời gọi execution; **Graph/Orchestrator** sở hữu topology + vòng đời run + checkpoint; **Delegation** sở hữu đệ quy/scope; **Discipline** (JSON gate, budget, finish gate) dùng chung; **Adapter layer** (LLM · Tools/Safety · RAG · Control/Observability) cắm qua port. Core KHÔNG import ngược ra ngoài (trừ schemas) — vòng phụ thuộc bị cắt ở seam. |
| **Data ownership** | Core sở hữu registry + event stream. **Orchestrator sở hữu checkpoint (SQLite) — nguồn sự thật duy nhất để resume**; `checkpoint.json` chỉ là projection read-only cho UI. `session.state` chỉ chứa giá trị serializable (codec `encode/decode_session_state`). Không container nào ghi thẳng checkpoint ngoài orchestrator. |
| **Integration** | Nội bộ: gọi hàm in-process qua port (Protocol `@runtime_checkable`) + event bus. LLM: HTTP OpenAI-compatible (JSON-mode). RAG: vector store qua `VectorStorePort`. Control plane: `EventSinkPort` forward event ra transport (Kafka về sau — hiện in-process). Không HTTP giữa các module — chúng ở chung process. |
| **Auth** | Không phải app đa người dùng cuối. Ranh giới quyền thật là **capability scope của agent**: delegation con chỉ được tập capability ⊆ cha (least-privilege theo scope, enforce ở chokepoint delegation). "SSO/RBAC người dùng" — không áp dụng ở tầng này (là việc của lớp app gọi vào). |
| **Security** | Threat chính = agent/LLM làm điều ngoài ý (path traversal, đệ quy vô hạn, leo scope, rò secret ra log). Workspace jail cho mọi tool fs; scope-subset cho delegation; redact args trước khi ghi event. Dữ liệu: tool-args/prompt = **Confidential** (có thể chứa PII/secret). Chi tiết ở §4. |
| **Reliability** | Budget guard chặn trước mỗi step (max_steps, max_depth). Try/except bọc executor — **tool lỗi không được làm sập kernel**. Resume từ SQLite sau crash. Retry middleware có nhưng phải phân biệt idempotent trước khi bật cho tool có side-effect (open-Q). |
| **Performance** | Không mục tiêu latency ngặt (đây là agent runtime, không phải API online). LLM client lazy + JSON-mode. Không cần cache tầng này. Đủ-là-đủ: không đặt ngưỡng P95 vì domain không đòi. |
| **Observability** | Event stream append-only → JSONL + summary/metrics per run (`var/agent_runs/<run_id>/`); inspect CLI. Thread-safe. **Đây là xương sống — mọi call qua chokepoint tự phát `tool.requested → completed/failed`**, không có event = call đó đi lối tắt (sai). |
| **Deployment** | Single process, local-first (offline chạy được: smoke + tests không cần LLM/network). Container hoá được; RAG optional (Qdrant qua docker-compose). |
| **Compliance** | Không thu thập dữ liệu người dùng cuối trực tiếp → PDPA/GDPR không áp dụng ở lõi. Nhưng tool-args có thể chứa dữ liệu nhạy → retention của `events.jsonl` cần chốt (open-Q, xem §4). |

---

## 2. C4

**Context (bắt buộc):**
```
[Người vận hành / caller / UI]
        │  run() / resume()
        ▼
   ┌──────────────┐      llm.chat (HTTP, JSON-mode)   [LLM provider]
   │  hex_agent   │ ───────────────────────────────►
   │ (1 deployable)│      embed / search              [Vector store (Qdrant)]
   │              │ ───────────────────────────────►
   └──────────────┘      event forward                [Transport/UI (Kafka sau)]
        │  đọc/ghi
        ▼
   [SQLite checkpoint  +  events.jsonl]  (var/agent_runs/<run_id>/)
```
*Đọc:* hex_agent là một hộp; người/UI vào bằng `run/resume`; ra ngoài chỉ 3 đường (LLM, vector store, event transport) — ba đường này là ba điểm rủi ro tích hợp cần trông. Checkpoint + event nằm cạnh, SQLite là nguồn khôi phục.

**Container (bên trong hộp — kiểu công nghệ, không tên framework):**
```
run/resume façade (orchestrator)
     │
     ▼
Compiled state-graph runtime (1 substrate)   ── checkpoint ──► SQLite (nguồn sự thật)
     │  guard → agent → tool → delegate → finish/fail
     ├──► AgentKernel.execute_tool  ◄── CHOKEPOINT 1 (mọi LLM + tool)
     │        │  qua middleware chain (policy/retry/condense/timing)
     │        ├─► LLM adapter (llm.chat)
     │        └─► Tool port + Safety (workspace jail)
     ├──► Delegation service  ◄── CHOKEPOINT 2 (đệ quy, scope, budget) — RIÊNG, không thuộc kernel
     └──► Event bus ──► Observability (JSONL/summary) + Control emitter (redaction)
Discipline (JSON gate · budget · finish gate)  = dùng chung, không nhân bản
```
*Đọc:* Có đúng **một** graph substrate và **hai** cửa tách biệt — cửa 1 (`execute_tool`) cho execution, cửa 2 (delegation) cho đệ quy. Tách vậy để logic "quản scope/budget đệ quy" không lẫn vào logic "chạy một tool", và để delegation có node riêng trong graph.

---

## 3. Data Flow + Integration Model

**Data Flow — một task chạy (gắn vào domain event):**
`caller → run()` → graph tạo `KernelSession` (state riêng, kernel chia sẻ frozen) → **guard** kiểm budget → **agent** gọi `execute_tool("llm.chat", …)` (**qua chokepoint 1** → phát `tool.requested → tool.completed`) → JSON gate parse ra đúng một action → nếu là tool → **tool** node lại qua chokepoint 1 (jail check) → nếu là giao việc → **delegate** node qua **chokepoint 2** (validate scope ⊆ cha, depth) → mỗi bước ghi event → checkpoint state vào **SQLite** → lặp tới **finish/fail** đóng lifecycle đúng một lần. Crash giữa chừng → `resume()` đọc **SQLite** (không đọc `checkpoint.json`) chạy tiếp từ node dở.

**Integration Model:**
| Đường | Pattern | Đồng bộ? | Ai chịu lỗi khi bên kia sập | Owner contract |
|---|---|---|---|---|
| caller ↔ hex_agent | in-process call (`run/resume`) | sync | façade | orchestrator |
| Graph ↔ LLM | HTTP OpenAI-compatible, JSON-mode | sync | LLM adapter (retry, lazy client); lỗi → `ok=False` không sập kernel | llm/adapter |
| Graph ↔ Tools/fs | port call + workspace jail | sync | SafeToolPort; try/except ở chokepoint | core + safety |
| Kernel ↔ Delegation | port call qua chokepoint riêng | sync | policy validate; vượt depth/scope → block | delegation/policy |
| Event bus ↔ Control transport | event forward (in-process → Kafka sau) | **async** | EventSink; mất transport KHÔNG chặn run | control/emitter |
| RAG ↔ Vector store | embed/search | sync, **optional** | RAG adapter; offline vẫn chạy (memory store) | rag/ports |

---

## 4. Security Model

**Góc nhìn lãnh đạo:** Dữ liệu nhạy nhất là **tool-args + prompt** (có thể chứa secret/PII) — hiện bị ghi thô vào `events.jsonl`; ai đọc được file run là đọc được. Có dấu vết audit (event append-only), nhưng cần **redact trước khi ghi** trước khi mở tool ghi/MCP ra ngoài. Đây là câu pháp lý/CTO hỏi đầu tiên và là rủi ro số 1 để rebuild làm đúng ngay.

- **Phân loại dữ liệu:** tool-args/prompt/LLM-output = **Confidential**; topology/metrics = Internal; smoke output = Public.
- **Auth model tầng này = capability scope**, không phải RBAC người dùng: mỗi agent có tập capability; **delegation con chỉ narrow, không mở rộng** (`scope ⊆ parent`). Enforce ở chokepoint 2 — bỏ qua `validate()` là leo quyền.
- **Audit:** event stream **append-only** per run là dấu vết bất biến; checkpoint = SQLite. `checkpoint.json` KHÔNG dùng làm audit (chỉ projection UI).
- **Threat model (STRIDE, luồng execute_tool + delegation):**
  - *Tampering/Elevation:* agent xin path tuyệt đối / leo scope → **workspace jail** (`resolve_in_workspace`) + scope-subset. Capability ngoài toolbox né được policy → phải bật policy gate hoặc bọc safety khi thêm tool ngoài (open-Q).
  - *Information disclosure:* raw args vào log → **redact/args_digest** trước khi bật write tool/MCP.
  - *DoS:* đệ quy/loop vô hạn → budget guard (max_steps/max_depth) chặn trước mỗi step.
- **Compliance/retention:** cần chốt retention `events.jsonl` chứa Confidential (open-Q → GĐ7).

---

## 5. ADRs

**ADR-001 — Microkernel + hexagonal, single deployable (không microservices)**
Bối cảnh: 1 domain điều phối agent, 1 runtime agent, cần thay LLM/store/UI mà không đụng lõi. · Quyết định: lõi cứng nhỏ + ports/adapters, chạy trong một process. · Loại: *microservices* (thêm tải vận hành cho 1 domain, không có nhu cầu scale độc lập); *plugin monolith không có seam* (mất khả năng swap adapter). · Hệ quả: được khả năng thay thế + biên rõ; mất: mọi thứ chung process → phải kỷ luật "core không import ngược".

**ADR-002 — Một chokepoint `execute_tool` cho MỌI LLM + tool**
Bối cảnh: cần observability/safety/envelope không bao giờ bị bỏ qua. · Quyết định: mọi call (kể cả LLM = `llm.chat`) đi qua `AgentKernel.execute_tool`; không đường tắt. · Loại: *cho node gọi thẳng adapter* (nhanh hơn nhưng mất trace/safety cho nhánh đó); *nhiều entrypoint theo loại call* (trùng lặp middleware). · Hệ quả: mọi hành vi truy vết + chặn được ở một chỗ; đánh đổi: chokepoint là điểm nóng, sửa nó vỡ rộng → phải bọc try/except + giữ thứ tự event.

**ADR-003 — Delegation là chokepoint RIÊNG, không phải method của kernel**
Bối cảnh: đệ quy cần quản scope/budget khác với execution một tool. · Quyết định: `DelegationService.delegate` tách khỏi kernel, có node `delegate` riêng trong graph. · Loại: *delegate là một capability qua execute_tool* (trộn quản-đệ-quy vào quản-tool, khó enforce scope-subset + depth). · Hệ quả: hai cửa rạch ròi, scope con ⊆ cha enforce một chỗ; đánh đổi: hai đường phải giữ đồng bộ event/lifecycle.

**ADR-004 — SQLite là nguồn checkpoint duy nhất; `checkpoint.json` chỉ là projection**
Bối cảnh: cần resume đúng sau crash, không chạy lại node có side-effect. · Quyết định: `resume()` chỉ đọc SQLite; `run_id == thread_id`; JSON chỉ để UI đọc. · Loại: *JSON làm nguồn resume* (không giao dịch, dễ lệch → chạy lại/mất tiến trình); *hai nguồn song song* (nhập nhằng sự thật). · Hệ quả: khôi phục tin cậy; ràng buộc: mọi thứ vào `session.state` phải serializable (codec) — nhét object thô → vỡ resume âm thầm.

**ADR-005 — Kernel frozen chia sẻ + session sở hữu run state**
Bối cảnh: nhiều run song song không được rò state, config không được đổi giữa chừng. · Quyết định: `AgentKernel.freeze()` đóng băng registry/config trước session đầu; mỗi run một `KernelSession` riêng. · Loại: *state chạy nằm trong kernel* (rò giữa run); *tạo kernel mới mỗi run* (mất chia sẻ registry/adapter, tốn khởi tạo). · Hệ quả: an toàn đồng thời; đánh đổi: thêm capability/middleware phải xong TRƯỚC freeze.

*(Framework ép bởi domain — LangGraph substrate, SQLite checkpointer, OpenAI-compatible HTTP — ghi làm **ràng buộc** cho GĐ7, KHÔNG chốt ở đây; xem khối bàn giao.)*

---

## Tự soi (trước cổng)
1. **Lãnh đạo đọc được đoạn đầu?** Có — mỗi artifact mở bằng Góc nhìn lãnh đạo bằng ngôn ngữ nghiệp vụ.
2. **Dev đủ hành động?** Có — style + boundary + data ownership + integration + scope-auth + C4 Context & Container + data flow gắn node thật.
3. **Đủ + đúng các phần?** Brief · C4 (Context+Container) · Data Flow · Integration · Security · 5 ADR (đều có phương án loại). Mỗi module nối về một seam/context thật trong domain.
4. **Lỡ chốt framework?** Không — LangGraph/SQLite/Qdrant nêu như *ràng buộc do domain ép*, đẩy sang GĐ7.

---

```
═══ CỔNG GĐ6 — SHAPE: hex_agent ═══
Style / Boundary / Data / Integration / Auth(scope) / Security: đã chốt.
C4 Context + Container: đã có · ADR: 5 bản (mỗi cái có phương án đã loại).
Open-Q còn treo → GĐ7:
  - Retry middleware: chỉ retry tool read_only/idempotent — chốt khi wire.
  - Redact/args_digest cho events.jsonl trước khi bật write-tool/MCP.
  - Retention events.jsonl (chứa Confidential) — ngưỡng bao lâu.
  - Policy/deny gate cho capability ngoài toolbox.
Câu hỏi cổng: Architecture đủ vững để chọn stack & dựng live slice chưa?
════════════════
```

Đây là điểm bạn (giữ vai CTO) quyết GO/NO-GO. Tôi không tự bấm GO. Thấy boundary lệch hay ADR thiếu phương án loại → nói, tôi vá trước khi bàn giao.

```
═══ BÀN GIAO — SHAPE → STACK: hex_agent ═══
Hình đã chốt      : Microkernel/hexagonal, single deployable · ~5 vùng (core · graph/orchestrator · delegation · discipline · adapters) · 2 chokepoint · checkpoint SQLite · event async ra transport.
Ràng buộc cho stack: (1) substrate điều phối phải có checkpoint bền + resume theo thread_id (LangGraph + SQLite checkpointer là hiện trạng — GĐ7 xác nhận/thay); (2) LLM OpenAI-compatible, JSON-mode, lazy; (3) port là Protocol runtime-checkable để swap adapter; (4) offline chạy được (smoke/test không cần network); (5) audit append-only.
Open-Q chuyển tiếp : retry-idempotency · redaction log · retention · deny gate ngoài toolbox (4 mục trên).
Artifact          : (chưa ghi vào repo — theo luật, hỏi trước khi ghi vào hex_agent; mặc định state/project/hex_agent/pipeline/shape.md)
→ Chọn framework/DB/lib hiện thực hình này (GĐ7): chạy /stack
→ Muốn dựng ngay một lát cắt sống để validate shape: chạy /skeleton (live slice GĐ8) hoặc /frame
→ Cần hiểu sâu code cũ shape sẽ đụng vào: chạy /atlas hoặc /explain
→ Cần điều phối cả pipeline: chạy /partner
════════════════
```

Muốn tôi ghi artifact này vào `state/project/hex_agent/pipeline/shape.md` để có traceability, hay để nguyên đây? (Không ghi thẳng vào repo `hex_agent` trừ khi bạn đồng ý.)
