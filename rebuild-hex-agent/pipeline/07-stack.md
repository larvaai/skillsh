# 07 — Stack: Tech Decision — HexAgent (clean rebuild)

> Skill `stack` · Giai đoạn 7 (Tech Decision / Framework Selection). Vào bằng **Architecture Brief GĐ6** (`pipeline/06-shape.md`), ra bằng **Tech Decision Matrix (có điểm) + ADR (có phương án đã loại) + Spike Result (cho ẩn số rủi ro cao)**. Chọn CÔNG CỤ hiện thực cái shape đã chốt — KHÔNG vẽ lại kiến trúc (việc GĐ6), KHÔNG viết code slice (việc GĐ8).
> Anchor: `00-understanding/REBUILD-BRIEF.md` + `evidence-A/B/C` + `ATLAS.md`. Đây là **rebuild có tham chiếu code gốc** (brownfield-informed): stack gốc quan sát được = Python · LangGraph · SQLite · Qdrant · OpenAI-compatible JSON-mode · SSE (`ATLAS.md:27`, `evidence-B:34`). Vì vậy "Fit team đã biết" và "Fit maintainability" phải tính cả stack đang có — không xé lẻ vô cớ.
> Chế độ tự-quyết: cổng go/no-go do người viết đóng vai **Kiến trúc sư / Tech-lead (chủ sở hữu) · CTO (người duyệt)** tự quyết GO, ghi rõ lý do + phương án đã loại. Không hỏi user.

---

## Góc nhìn lãnh đạo (đọc 60 giây, không cần biết code)

**Chọn gì.** Dựng HexAgent bằng **Python 3.11** (lõi), **LangGraph** làm bộ máy graph + resume, **SQLite** làm chân lý resume, một **LLM adapter kiểu OpenAI-compatible JSON-mode**, **pytest + Hypothesis (property-based) + audit-test** làm lưới an toàn, **SSE một chiều** cho control-plane realtime (sau MVP), và **RAG để tùy-chọn — mặc định TẮT** (bật bằng Qdrant *hoặc* pgvector khi thật cần).

**Vì sao cụm này, nói bằng tiếng nghiệp vụ.** Đây là bản *dựng lại sạch* của một hệ đã chạy được: chọn đúng bộ công cụ mà hệ gốc đã chứng minh vận hành → đội **lên nhanh, rủi ro thấp, rẻ**, và mỗi bất biến an-toàn (nhân đông cứng, hai cửa kiểm-quyền, "chỉ xong khi đủ bằng chứng", resume không chạy-lại-sai) đều có công cụ đỡ sẵn. Ba rủi ro chết người của một agent tự trị — báo-xong-khống, chạy-vô-hạn, rò-secret — đều được đóng bằng **kiến trúc GĐ6 + test property**, không bằng lời hứa. Không có món nào ở đây khoá cứng vào một nhà cung cấp: LLM đi qua chuẩn mở (đổi provider = đổi URL/key), SQLite là file, RAG tắt được.

**Rủi ro / chi phí lãnh đạo cần biết.** (1) **LangGraph** là phụ thuộc nặng nhất và là chỗ duy nhất còn *ẩn số thật*: "resume đúng một lần, không chạy lại gây tác dụng phụ" — đã đề xuất **spike 1–2 ngày đo thật** trước khi đổ người (SPIKE-1). (2) Ngưỡng tốc độ (P95) và ngưỡng cảnh báo lỗi **chưa có số** — đây là platform nội bộ, tải thấp, nên *không bịa*; để live-slice (GĐ8) đo. (3) RAG để mặc định tắt là quyết định *tiết kiệm*: chưa tốn hạ tầng vector cho tới khi có nhu cầu tri-thức thật. Tất cả còn-treo đã ghi thành open-Q có địa chỉ, không cái nào chặn việc dựng live slice.

---

## 0. Nối mạch — nhận gì từ GĐ6, chọn gì ở GĐ7

Từ **Bàn giao SHAPE→STACK** (`06-shape.md` §Bàn giao) rút ra các "ô còn để mở tool" — mỗi ràng buộc kiến trúc ép sẵn một phần lựa chọn:

| Ràng buộc từ Architecture Brief GĐ6 | Ô tool phải chốt ở GĐ7 | Ràng buộc đã ép tới đâu |
|---|---|---|
| Runtime hỗ trợ freeze-kernel + serializable-only state | (1) Ngôn ngữ/runtime lõi | Mở — nhưng brownfield ép mạnh về Python |
| Cần bộ máy graph + resume không side-effect | (2) Graph substrate / state machine | Mở — LangGraph (gốc) vs orchestrator tự viết |
| Embedded relational store = chân lý resume, tx atomic (ADR-005) | (3) Checkpoint store | ADR-005 đã ép "embedded relational" → SQLite ≫; vẫn chấm vs Postgres/Redis |
| LLM adapter JSON-mode + retry transient-vs-permanent | (4) LLM adapter | Ép "OpenAI-compatible JSON-mode" — chốt kiểu client, ghi 1 dòng |
| Vector store health-gated, offline-first, never raises (RAG optional) | (5) Vector KB (optional) | Mở — Qdrant vs pgvector vs none |
| 3-seam BE↔UI, event stream = push (sau MVP) | (6) Transport control-plane | Mở — SSE (gốc) vs WebSocket |
| Finish-by-evidence + guards + μ co ngặt cần *chứng minh*, không chỉ ví dụ | (7) Test stack | Mở — pytest + property (Hypothesis) + audit |

**Đủ-là-đủ áp cho từng ô:** ô (3) và (4) đã bị ràng buộc ép gần hết → ma trận gọn + ghi rõ ràng buộc. Ô (1)(2)(5)(6)(7) mở hơn → ma trận đầy đủ. Ẩn số rủi ro cao **duy nhất** = LangGraph resume round-trip → SPIKE-1. NFR-số chưa có → **không spike bịa**, ghi open-Q sang GĐ8.

Thang điểm mọi ma trận: **1–5** (5 = khớp nhất). Trọng số do RÀNG BUỘC kiến trúc + rủi ro quyết, **không đều nhau**, ghi ra để truy vết. TỔNG = Σ(trọng số × điểm).

---

## 1. Tech Decision Matrix — ngôn ngữ/runtime lõi

> Ràng buộc GĐ6: freeze-kernel + serializable-only state + middleware chain có thứ tự. Brownfield: gốc là Python (`ATLAS.md:27`). "Fit team đã biết" nặng vì đây là rebuild — đội đã sống trong Python codebase gốc.

```text
TECH DECISION MATRIX — Ngôn ngữ/runtime lõi
Tiêu chí (trọng số)                                   | Python 3.11 | Go 1.2x | TypeScript/Node
Fit domain (freeze-kernel, dynamic middleware, LLM-first) (×5) |     5      |    3    |      4
Fit team đã biết (rebuild từ codebase Python gốc)      (×5)     |     5      |    2    |      3
Fit scale/NFR (loop tuần tự, tải thấp — không phải bài toán) (×2)|    4      |    5    |      4
Fit enterprise (auth/audit/log — đã có ở tầng kiến trúc) (×2)   |     4      |    4    |      4
Fit testing (property-based, audit test cho invariant)  (×4)    |     5      |    3    |      4
Fit hiring (thị trường tuyển)                           (×2)    |     4      |    4    |      5
Fit ecosystem (LangGraph, LLM SDK, vector client sẵn)   (×4)    |     5      |    2    |      4
Fit maintainability (2 năm nữa còn nuôi được; khớp gốc) (×4)    |     5      |    3    |      4
TỔNG (có trọng số, /140)                                        |    132     |    82   |     108
=> Chọn: Python 3.11
   Lý do: rebuild từ codebase Python gốc → đội thạo nhất, hệ sinh thái LangGraph/LLM/vector chín nhất
          trong Python, và test property-based (Hypothesis) mạnh để CHỨNG MINH bất biến (μ co ngặt, scope⊆parent).
   Đã loại: Go (mạnh về scale/throughput đồng thời & binary gọn — nhưng scale KHÔNG phải rủi ro của case này
            (loop tuần tự, tải thấp); đội chưa thạo, hệ sinh thái LangGraph/agent yếu hơn → lên chậm hơn, xé lẻ khỏi gốc).
            TypeScript/Node (hiring tốt nhất, ecosystem khá — nhưng xé rời khỏi codebase Python gốc = mất toàn bộ lợi thế
            rebuild; agent/graph tooling non hơn Python).
```

Chốt **3.11** (không 3.12/3.13): là mốc gốc quan sát được, ổn định, mọi lib (LangGraph, LLM SDK, qdrant/pgvector client, Hypothesis) hỗ trợ đầy đủ — không đuổi bản mới cho tới khi có lý do (Đủ-là-đủ). *(open-Q nhỏ: bản Python chính xác của gốc chưa neo được file:line → xác nhận ở skeleton, không chặn.)*

---

## 2. Tech Decision Matrix — Graph substrate / state machine

> Ràng buộc GĐ6: cần bộ máy chạy vòng lặp theo round + **resume không side-effect** từ SQLite (ADR-005). Đây là ô rủi ro cao nhất — LangGraph là phụ thuộc nặng và resume round-trip là ẩn số (DoD gốc: "resume round-trip", `evidence-C:44`).

```text
TECH DECISION MATRIX — Graph substrate / state machine
Tiêu chí (trọng số)                                   | LangGraph | Orchestrator tự viết (state machine thuần)
Fit domain (round loop + checkpoint/resume built-in)  (×5) |    5      |    3   (phải tự dựng resume, dễ sai atomic)
Fit team đã biết (gốc dùng LangGraph)                 (×5) |    5      |    2
Fit scale/NFR (tải thấp, tuần tự)                     (×2) |    4      |    5   (nhẹ hơn, ít phụ thuộc)
Fit enterprise (checkpointer SQLite, stream API sẵn)  (×3) |    5      |    3
Fit testing (deterministic replay, resume test)       (×4) |    4      |    3
Fit maintainability (bớt code tự nuôi vs bớt lệ thuộc lib)(×4)|   4      |    3   (ít lib nhưng nhiều code nhà tự giữ)
Fit ecosystem/vendor (khoá vào 1 lib graph)           (×3) |    3      |    5   (0 lock, nhưng tự gánh)
TỔNG (có trọng số, /130)                                    |   114     |   87
=> Chọn: LangGraph (+ SQLite checkpointer)
   Lý do: gốc đã chạy trên LangGraph → resume/checkpoint/stream có SẴN, khớp trực tiếp ADR-005 (SQLite = truth).
          Tự viết orchestrator = tự gánh lại đúng phần khó & dễ sai nhất (checkpoint atomic + resume không re-run).
   Đã loại: Orchestrator tự viết — điểm mạnh thật: 0 vendor-lock, runtime nhẹ, toàn quyền kiểm soát thứ tự.
            Thua ở: phải TỰ dựng lại resume-atomic (đúng chỗ ADR-005 cảnh báo "JSON nửa-ghi → re-run sai"),
            đội chưa có sẵn, lên chậm. Điều kiện đảo chiều: nếu SPIKE-1 cho thấy LangGraph resume KHÔNG đạt
            "một-lần, không side-effect" → cân nhắc lại (xem SPIKE-1 + ADR-002).
```

**⚠️ Đây là ô có ẩn số rủi ro cao → BẮT BUỘC SPIKE-1 (§7).** Điểm "Fit domain=5" của LangGraph *giả định* resume round-trip đạt; spike xác nhận trước khi khoá.

---

## 3. Tech Decision Matrix — Checkpoint store

> **Ràng buộc GĐ6 (ADR-005) đã ép**: "embedded relational store = chân lý resume, transaction atomic". Đây là hạng mục *bị ràng buộc ép gần hết* → ma trận gọn (4 tiêu chí liên quan), ghi rõ ràng buộc, không mở ma trận giả 8 dòng.

```text
TECH DECISION MATRIX — Checkpoint store (ADR-005 đã ép "embedded relational + atomic")
Tiêu chí (trọng số)                                   | SQLite | Postgres | Redis
Fit domain (embedded, atomic tx, single-file truth)   (×5) |   5   |    4     |   2  (in-mem, không phải relational-truth)
Fit deployment (single deployable, cloud/on-prem, 0 service) (×4)| 5 |   2     |   3
Fit team đã biết (gốc = langgraph.sqlite)             (×4) |   5   |    3     |   3
Fit maintainability/ops (backup = copy file, 0 server) (×3) |   5   |    3     |   3
TỔNG (có trọng số, /80)                                     |   80  |   47     |   40
=> Chọn: SQLite (langgraph.sqlite = chân lý resume; checkpoint.json = projection UI, KHÔNG đọc để resume)
   Lý do: khớp trực tiếp ADR-005 + shape "single deployable" — embedded, atomic tx (commands+round+save một transaction),
          không cần dịch vụ ngoài, backup = copy file, đúng như gốc.
   Đã loại: Postgres — mạnh thật khi cần concurrency cao / multi-writer / query phân tích; nhưng thêm một service phải
            vận hành (ngược "single deployable"), thừa cho một-tiến-trình tải thấp. Điều kiện bật lại: khi chuyển
            multi-instance hoặc cần audit-query nặng ngoài event-log → migrate SQLite→Postgres qua cùng port checkpointer.
            Redis — nhanh, hợp cache/queue; nhưng KHÔNG phải relational-truth atomic bền, sai vai "chân lý resume".
```

---

## 4. LLM adapter — ràng buộc đã ép, ghi một dòng (không mở ma trận giả)

> Ràng buộc GĐ6 đã ép: "LLM adapter JSON-mode + retry-classify transient-vs-permanent"; gốc = OpenAI-compatible JSON-mode (`evidence-B:34`, `evidence-C:66`). LLM là **capability đi QUA `execute_tool`** (ADR-002), không phải call trực tiếp — nên đây là chọn *kiểu client*, không chọn *provider cứng*.

**Chọn: một LLM adapter kiểu OpenAI-compatible JSON-mode**, lazy-init, có phân loại retry transient-vs-permanent (khớp middleware Retry của GĐ6), đặt sau port `execute_tool`.
**Ràng buộc ép:** shape đã chốt "LLM-as-capability qua execute_tool" + "JSON-mode" → adapter chỉ cần nói được JSON-mode và trả `CapabilityResult` chuẩn.
**Hệ quả / lợi ích:** chuẩn OpenAI-compatible = **đổi provider không đổi code** (chỉ đổi base-URL + key: OpenAI, Azure, hay bất kỳ endpoint tương thích, kể cả self-host) → **0 vendor-lock cứng**. Model cụ thể + endpoint = cấu hình runtime, không chốt ở đây (không bịa).
*(Không mở ma trận: ràng buộc đã ép đúng một lựa chọn hợp lý; mở 3 cột giả sẽ vi phạm "không bịa candidate cho đủ".)*

---

## 5. Tech Decision Matrix — Vector KB (optional)

> Ràng buộc GĐ6: RAG **health-gated, offline-first, never raises, NGOÀI lõi MVP**. Nghĩa là mặc định hệ chạy KHÔNG cần vector store. Ô này về bản chất hỏi: "khi bật RAG thì dùng gì" + "mặc định có bật không".

```text
TECH DECISION MATRIX — Vector KB (chỉ khi bật RAG; mặc định = none)
Tiêu chí (trọng số)                                   | none (default off) | Qdrant | pgvector
Fit domain (RAG optional, offline-first, never raises)(×5) |   5 (loop chạy dù thiếu) |   4   |   4
Fit deployment (0 hạ tầng thêm cho MVP)               (×4) |   5   |    2 (thêm 1 service) | 3 (dùng chung Postgres NẾU có)
Fit team đã biết (gốc = Qdrant, uuid5 ids)            (×3) |   —   |    5   |   2
Fit scale (số tài liệu KB — chưa có nhu cầu thật)     (×2) |   —   |    5   |   3
Fit maintainability (ít bộ phận động = dễ nuôi)       (×3) |   5   |    3   |   4 (đỡ hơn Qdrant nếu đã có Postgres)
TỔNG (có trọng số, /85)                                     |  70*  |   61   |   57
=> Chọn: NONE cho MVP (RAG tắt); khi bật → Qdrant là mặc định (khớp gốc), pgvector là lối rẻ nếu đã kéo Postgres vào.
   *TỔNG "none" chỉ so trên các tiêu chí áp dụng được — nó thắng vì Đủ-là-đủ (YAGNI): chưa có nhu cầu tri-thức thật ở MVP.
   Lý do: shape đặt RAG "ngoài lõi MVP, never raises" → không kéo hạ tầng vector vào tới khi có consumer thật.
          Cổng health-gate + port giữ chỗ để bật sau mà không sửa lõi.
   Đã loại (cho MVP): Qdrant — mạnh & khớp gốc, nhưng thêm một service phải vận hành cho tính năng chưa dùng (thừa).
            pgvector — rẻ hơn NẾU đã có Postgres; nhưng ta chọn SQLite (§3) nên pgvector = phải kéo cả Postgres vào chỉ vì RAG → không đáng.
   Điều kiện bật: khi có nhu cầu tri-thức thật → mặc định Qdrant (khớp gốc, uuid5 ids); chọn pgvector CHỈ nếu lúc đó đã có Postgres vì lý do khác.
```

---

## 6. Tech Decision Matrix — Transport control-plane (sau MVP)

> Ràng buộc GĐ6: 3-seam BE↔UI, **event stream = push một chiều** BE→UI; snapshot = pull; command = push nhỏ. UI là **pure consumer** (UI ⊥ core). Gốc = SSE (`GET /api/stream`, `ATLAS.md:53`). Đây là seam *sau MVP* nên rủi ro trung bình.

```text
TECH DECISION MATRIX — Transport event-stream (BE→UI, push một chiều)
Tiêu chí (trọng số)                                   | SSE | WebSocket
Fit domain (push MỘT CHIỀU BE→UI; command đi qua POST riêng) (×5) |  5  |  3 (song công là thừa; 3 seam vốn tách chiều)
Fit reliability (resync ?since=seq, auto-reconnect built-in) (×4) |  5  |  3 (phải tự dựng reconnect/resync)
Fit team đã biết (gốc = SSE)                          (×3) |  5  |  2
Fit enterprise (chạy qua HTTP/proxy/LB dễ, auth như HTTP thường)(×3)| 5 |  3 (upgrade handshake, proxy phức tạp hơn)
Fit maintainability (đơn giản, ít trạng thái kết nối) (×3) |  5  |  3
Fit scale (nhiều client — chưa phải bài toán)         (×1) |  4  |  4
TỔNG (có trọng số, /95)                                     |  91 |  56
=> Chọn: SSE cho event-stream (+ POST /api/commands cho command, GET /api/snapshot cho pull)
   Lý do: 3 seam của GĐ6 vốn ĐÃ tách chiều (stream=push, command=push-riêng, snapshot=pull) → không cần song công của WS.
          SSE cho resync ?since=seq + auto-reconnect gần như miễn phí, chạy qua proxy/LB/auth-HTTP đơn giản, khớp gốc.
   Đã loại: WebSocket — mạnh khi cần hai chiều realtime độ trễ thấp (chat, collab, game); ở đây là thừa năng lực,
            phải tự dựng reconnect/resync và xử lý handshake qua hạ tầng. Điều kiện đảo chiều: nếu sau này cần
            UI đẩy lệnh tần suất cao / hai chiều thật-thời-gian → cân nhắc WS cho riêng seam đó, giữ stream vẫn SSE.
```

---

## 7. Test stack + Spike

### 7a. Tech Decision Matrix — Test stack

> Ràng buộc GĐ6: hệ này *sống bằng bất biến* — μ(node) co ngặt, scope con ⊆ cha, finish-bất-khả-khi-thiếu-evidence, seq monotonic gap-free, replay=snapshot deterministic. Đây là những *tính chất phổ quát* ("với MỌI input hợp lệ…") → chỉ test ví-dụ là chưa đủ; cần **property-based**. Gốc có 327 test + `tests_audit/` (`evidence-C:25`).

```text
TECH DECISION MATRIX — Test stack
Tiêu chí (trọng số)                                   | pytest+Hypothesis+audit | pytest-only (example-based) | unittest stdlib
Fit domain (chứng minh INVARIANT phổ quát: μ↓, scope⊆, seq gap-free) (×5) | 5 |  2 (ví dụ lẻ, sót biên) | 2
Fit team đã biết (gốc = pytest + tests_audit)         (×4) |   5   |    5     |   2
Fit testing depth (property + fuzz + replay-determinism) (×5) | 5 |    3     |   2
Fit maintainability (fixtures, param, plugin ecosystem)(×3) |   5   |    5     |   3
Fit ecosystem (Hypothesis, coverage, xdist sẵn Python)(×2) |   5   |    4     |   2
TỔNG (có trọng số, /95)                                     |   90  |   62     |   40
=> Chọn: pytest + Hypothesis (property-based) + audit-test layer (mô phỏng tests_audit gốc)
   Lý do: bất biến của hệ là mệnh đề "với MỌI input hợp lệ…" → Hypothesis sinh input đối kháng để BẮT phản ví dụ
          (μ không co, scope leo, seq nhảy) mà test ví-dụ bỏ sót. audit-test giữ tầng kiểm luồng delegate/redaction.
   Đã loại: pytest-only ví-dụ — nền tốt (giữ làm lớp dưới) nhưng một mình không chứng minh được tính phổ quát.
            unittest stdlib — 0 phụ thuộc nhưng thiếu param/fixture/plugin & không có property-based → yếu cho case này.
```

### 7b. SPIKE-1 — LangGraph resume round-trip (ẩn số rủi ro cao DUY NHẤT)

```text
SPIKE RESULT — LangGraph resume round-trip (checkpoint atomic, không side-effect re-run)
Câu hỏi   : LangGraph + SQLite checkpointer có cho resume "một-lần-đúng" không —
            commands+round+save land trong MỘT transaction atomic (ADR-005), và resume cùng run_id
            KHÔNG chạy-lại các bước đã done (0 side-effect re-run)? Nếu không đạt → phải cân nhắc orchestrator tự viết (§2).
Time-box  : 1–2 ngày. Dựng graph tối thiểu (2–3 node) + SQLite checkpointer, chạy tới giữa chừng,
            kill, resume, kiểm: (a) không re-emit tool.requested của bước đã done; (b) round_no liên tục;
            (c) crash GIỮA transaction không để lại checkpoint nửa-ghi (atomicity).
Đo được   : ⏳ CHƯA CHẠY — đây là ẩn số mang sang GĐ8 (live slice là nơi rẻ nhất để đo thật, đúng DoD gốc "resume round-trip").
            stack KHÔNG tự build sản phẩm; đề xuất time-box + tiêu chí đạt, để skeleton/dev chạy rồi báo số.
Kết luận  : TREO — chốt LangGraph có ĐIỀU KIỆN: nếu spike ở GĐ8 cho thấy resume KHÔNG đạt tiêu chí (a)(b)(c),
            mở lại §2 (orchestrator tự viết) qua đường lui /shape? KHÔNG — đây là lựa chọn TOOL, đảo chiều trong GĐ7,
            không đụng shape. Rủi ro chấp nhận được: gốc ĐÃ chạy LangGraph+SQLite resume nên xác suất đạt cao;
            spike chỉ để xác nhận trên bản rebuild, không phải khám phá từ số 0.
```

**Các ẩn số KHÔNG spike (ghi rõ lý do — Đủ-là-đủ):**
- **NFR số (P95 loop, ngưỡng alert error-rate):** chưa có số, platform nội bộ tải thấp, loop tuần tự → *không bịa*. Đo ở GĐ8/Operate. (open-Q OQ-1, kế thừa GĐ6.)
- **SQLite / LLM-adapter / pytest / SSE:** stack quen, gốc đã chạy, ràng buộc ép sẵn → không spike.

---

## 8. ADRs — mỗi quyết định lớn một bản ghi (đều có phương án đã loại)

```text
ADR-001 — Ngôn ngữ lõi = Python 3.11
Bối cảnh   : Rebuild từ codebase Python gốc; shape cần freeze-kernel + serializable state + middleware động + test property.
Quyết định : Python 3.11 cho toàn lõi.
Lý do      : thắng điểm ở Fit-team-đã-biết (rebuild) + Fit-ecosystem (LangGraph/LLM/vector chín nhất) + Fit-testing (Hypothesis).
Đã loại    : Go (mạnh scale/binary gọn — scale không phải rủi ro; đội chưa thạo, ecosystem agent yếu → chậm, xé khỏi gốc);
             TypeScript/Node (hiring tốt nhất — nhưng rời khỏi codebase Python gốc = mất lợi thế rebuild).
Hệ quả     : hiring Python dồi dào; nuôi tiếp trực tiếp trên nền gốc; GIL không phải vấn đề (loop tuần tự, IO-bound LLM).
             open-Q: bản Python chính xác của gốc → xác nhận ở skeleton.

ADR-002 — Graph substrate = LangGraph (+ SQLite checkpointer)  [CÓ ĐIỀU KIỆN qua SPIKE-1]
Bối cảnh   : Cần round-loop + resume-không-side-effect từ SQLite (ADR-005 GĐ6). Gốc dùng LangGraph. Resume round-trip = ẩn số.
Quyết định : LangGraph làm bộ máy graph/state + SQLite checkpointer; checkpoint.json chỉ là projection UI.
Lý do      : resume/checkpoint/stream có SẴN, khớp trực tiếp ADR-005; tự viết lại = tự gánh đúng phần khó & dễ sai nhất.
Đã loại    : Orchestrator tự viết (state machine thuần) — mạnh: 0 vendor-lock, runtime nhẹ, toàn quyền thứ tự.
             Thua: phải tự dựng resume-atomic (đúng chỗ ADR-005 cảnh báo), đội chưa có sẵn, chậm hơn.
Hệ quả     : + lên nhanh, khớp gốc. − phụ thuộc một lib graph (vendor-lock mức lib, KHÔNG cloud) → cô lập sau port graph
             để đổi được sau. RÀNG BUỘC: SPIKE-1 phải PASS ở GĐ8 trước khi khoá cứng; nếu fail → mở lại orchestrator tự viết.

ADR-003 — Checkpoint store = SQLite (embedded, atomic)
Bối cảnh   : ADR-005 GĐ6 ép "embedded relational = chân lý resume, tx atomic"; shape = single deployable.
Quyết định : SQLite (langgraph.sqlite) = chân lý resume duy nhất; commands+round+save trong một transaction.
Lý do      : embedded, atomic, 0 service, backup=copy file, khớp gốc & shape.
Đã loại    : Postgres (mạnh concurrency/query-nặng — thừa & ngược single-deployable; migrate sau qua cùng port nếu multi-instance);
             Redis (nhanh nhưng không phải relational-truth atomic bền — sai vai chân-lý-resume).
Hệ quả     : + vận hành cực nhẹ. − single-writer/single-node (chấp nhận: chưa phải bài toán); migration path SQLite→Postgres giữ mở qua port checkpointer.

ADR-004 — LLM adapter = OpenAI-compatible JSON-mode client (qua execute_tool)
Bối cảnh   : shape ép "LLM-as-capability qua execute_tool + JSON-mode + retry-classify". Gốc = OpenAI-compatible adapter.
Quyết định : một adapter OpenAI-compatible JSON-mode, lazy-init, retry transient-vs-permanent, đặt sau port execute_tool.
Lý do      : ràng buộc GĐ6 ép sẵn; chuẩn mở = đổi provider chỉ đổi base-URL+key.
Đã loại    : SDK khoá cứng một vendor (vd chỉ một provider độc quyền) — loại vì tạo vendor-lock cloud không cần thiết;
             chuẩn OpenAI-compatible cho cùng khả năng mà giữ tự do đổi endpoint.
Hệ quả     : + 0 vendor-lock cứng (OpenAI/Azure/self-host tương thích đều chạy). − model/endpoint cụ thể = config runtime (chưa chốt, không bịa).

ADR-005 — Vector KB = NONE ở MVP (Qdrant khi bật, pgvector là lối rẻ nếu đã có Postgres)
Bối cảnh   : shape đặt RAG "optional, health-gated, offline-first, never raises, NGOÀI lõi MVP". Gốc = Qdrant.
Quyết định : MVP không kéo vector store; giữ port RAG + health-gate. Bật sau → mặc định Qdrant; pgvector chỉ nếu lúc đó đã có Postgres.
Lý do      : YAGNI/Đủ-là-đủ — chưa có consumer tri-thức thật; loop chạy trọn không cần RAG.
Đã loại (cho MVP) : Qdrant (khớp gốc, mạnh — nhưng thêm service cho tính năng chưa dùng); pgvector (rẻ nếu có Postgres —
             nhưng ta chọn SQLite nên pgvector = phải kéo cả Postgres chỉ vì RAG → không đáng).
Hệ quả     : + hạ tầng MVP tối giản. − khi bật RAG phải dựng vector store + cổng health-gate (đã chừa chỗ ở kiến trúc).

ADR-006 — Transport control-plane = SSE (event-stream), POST/GET cho command/snapshot
Bối cảnh   : shape = 3 seam đã tách chiều (stream push / command push-riêng / snapshot pull), UI ⊥ core, sau MVP. Gốc = SSE.
Quyết định : SSE cho event-stream (GET /api/stream, resync ?since=seq); POST /api/commands; GET /api/snapshot.
Lý do      : push một-chiều khớp seam; SSE cho reconnect/resync gần miễn phí, chạy qua proxy/LB/auth-HTTP đơn giản, khớp gốc.
Đã loại    : WebSocket — mạnh cho hai-chiều realtime độ-trễ-thấp; ở đây thừa năng lực, phải tự dựng reconnect/resync.
             Điều kiện đảo chiều: nếu cần UI đẩy lệnh tần suất cao/song công thật → cân nhắc WS cho riêng seam đó.
Hệ quả     : + đơn giản, ít trạng thái kết nối, hợp hạ tầng HTTP. − không song công (không cần ở MVP).

ADR-007 — Test stack = pytest + Hypothesis (property-based) + audit-test
Bối cảnh   : hệ sống bằng bất biến phổ quát (μ↓, scope⊆, finish-by-evidence, seq gap-free, replay=snapshot). Gốc: 327 test + tests_audit.
Quyết định : pytest (nền) + Hypothesis (property-based cho invariant) + một tầng audit-test (luồng delegate/redaction).
Lý do      : bất biến = "với MỌI input hợp lệ…" → cần sinh input đối kháng để bắt phản ví dụ; ví-dụ đơn lẻ sót biên.
Đã loại    : pytest-only ví-dụ (giữ làm lớp dưới, không đủ chứng minh phổ quát); unittest stdlib (thiếu param/fixture/property).
Hệ quả     : + chứng minh được các bất biến an-toàn bằng test, không bằng lời hứa. − property-test cần viết generator + shrink cẩn thận (chi phí một lần).
```

---

## 9. Tự soi trước khi chốt (bắt buộc — trả lời được cả ba mới chốt)

1. **Lãnh đạo đọc được băng đầu?** — CÓ. "Góc nhìn lãnh đạo" 60s: chọn gì (Python+LangGraph+SQLite+…) · vì sao (rebuild trên nền đã chạy → nhanh/rẻ/an-toàn) · đã loại gì (Go/TS, Postgres/Redis, WebSocket, RAG-mặc-định-bật) · rủi ro (LangGraph resume = spike; NFR chưa có số; RAG tắt để tiết kiệm). Không bắt CEO đọc điểm số.
2. **Dev đủ hành động?** — CÓ. 7 hạng mục đều có ma trận có-điểm × trọng số (hoặc 1 dòng ràng-buộc-ép cho LLM adapter) + 7 ADR (stack cụ thể + hệ quả + migration path) + SPIKE-1 với tiêu chí đạt rõ. Đủ để đội bắt tay dựng skeleton mà không phải chọn lại.
3. **Đúng + đủ + truy vết?** — CÓ. Mỗi ô điểm neo về một ràng buộc Architecture Brief GĐ6 / evidence gốc; không "đang hot"; ẩn số rủi ro cao (LangGraph resume) có spike time-box; NFR-số thiếu → open-Q không bịa; không sửa lại kiến trúc GĐ6.

---

## 10. Cổng GĐ7 — STACK (tự-quyết, đóng vai Kiến trúc sư/Tech-lead + CTO duyệt)

**AI duyệt (vai CTO theo A5) rà đủ 4 điều trước khi cho qua:**
1. Mỗi hạng mục rủi ro cao có ma trận **có điểm** × trọng số + TỔNG + dòng Chọn/Lý do/Đã loại — ✔ (7 ma trận; LLM adapter ghi 1 dòng vì ràng buộc ép, đúng Đủ-là-đủ).
2. Mỗi lựa chọn lớn có ADR kèm phương án đã loại + hệ quả — ✔ (ADR-001…007).
3. Ẩn số rủi ro cao có spike thực đo *hoặc* ghi rõ vì sao chưa — ✔ (SPIKE-1 time-box, treo có địa chỉ sang GĐ8; NFR-số ghi open-Q, không bịa).
4. Mọi lựa chọn nằm trong ràng buộc Architecture Brief GĐ6 — ✔ (không đổi style/boundary; SQLite khớp ADR-005; LLM-qua-execute_tool khớp ADR-002; SSE khớp 3-seam).

```
═══ CỔNG GĐ7 — STACK: HexAgent (clean rebuild) ═══
Ngôn ngữ = Python 3.11 · Graph = LangGraph (+SQLite checkpointer, spike-gated) · Checkpoint = SQLite ·
LLM = OpenAI-compatible JSON-mode adapter (qua execute_tool) · Vector = NONE ở MVP (Qdrant khi bật) ·
Transport = SSE · Test = pytest + Hypothesis + audit.
Ma trận có điểm: 6 bảng (lang/graph/checkpoint/vector/transport/test) + 1 dòng ràng-buộc-ép (LLM adapter). ADR: 7 bản (đều có phương án đã loại).
Spike: SPIKE-1 LangGraph resume round-trip — time-box 1–2 ngày, TREO sang GĐ8 (đo ở live slice, rẻ nhất).
Open-Q còn treo → sau: OQ-1 NFR-số (P95/alert) đo ở GĐ8/Operate; model/endpoint LLM = config runtime; điều kiện bật RAG.
Câu hỏi cổng: Stack đã chốt, sẵn sàng dựng live slice chưa?
════════════════
```

**Quyết định cổng (tự-quyết — product owner: "không hỏi approval").**
**GATE: GO.** Lý do: 7 hạng mục đều có quyết định truy-vết-được (ma trận có điểm hoặc ràng-buộc-ép ghi rõ), mỗi lựa chọn lớn có ADR + phương án đã loại, ẩn số rủi ro cao duy nhất (LangGraph resume) có spike time-box với tiêu chí đạt rõ và được đặt đúng chỗ rẻ nhất để đo (GĐ8), mọi lựa chọn nằm trong ràng buộc GĐ6. Đây là rebuild trên nền đã chạy → rủi ro tổng thấp; các món đều tránh vendor-lock cứng (LLM chuẩn mở, SQLite là file, RAG tắt được).
**Phương án đã loại ở tầng cổng:** (a) chờ chạy xong SPIKE-1 rồi mới GO — loại: spike là để *xác nhận trên bản rebuild* (gốc đã chạy LangGraph+SQLite resume), không phải khám phá từ 0; treo có địa chỉ + điều-kiện-đảo-chiều rõ đủ để đi tiếp mà không mù. (b) chốt luôn RAG=Qdrant cho MVP để "đỡ phải quyết sau" — loại: vi phạm Đủ-là-đủ/YAGNI, kéo hạ tầng cho tính năng chưa có consumer. (c) đợi có NFR-số rồi mới chọn checkpoint/transport — loại: các lựa chọn này do ràng buộc kiến trúc + deployment quyết, không do P95; NFR-số là để *tinh chỉnh* ở GĐ8, không chặn stack.

---

## 11. Bàn giao sang `skeleton` (GĐ8)

```
═══ BÀN GIAO — STACK → SKELETON: HexAgent (clean rebuild) · Tech Stack (GĐ7) ═══
Stack đã chốt      : Python 3.11 · LangGraph (+SQLite checkpointer) · SQLite = chân lý resume · LLM = OpenAI-compatible
                     JSON-mode adapter (qua execute_tool) · Vector = NONE ở MVP (port+health-gate giữ chỗ; Qdrant khi bật) ·
                     Transport = SSE (event-stream) + POST/GET (command/snapshot) · Test = pytest + Hypothesis + audit.
Ràng buộc kéo theo : LangGraph = vendor-lock mức-lib (cô lập sau port graph, đổi được) · SQLite single-writer/single-node
                     (migrate SQLite→Postgres qua cùng port nếu multi-instance) · LLM model/endpoint = config runtime ·
                     hiring Python dồi dào · pytest+Hypothesis cần viết generator/shrink (chi phí một lần).
Ẩn số còn treo    : • SPIKE-1 LangGraph resume round-trip (atomic + 0 side-effect re-run) — ĐO Ở LIVE SLICE (DoD gốc "resume round-trip").
                      Điều-kiện-đảo-chiều: fail → mở lại orchestrator tự viết (§2), KHÔNG đụng shape.
                    • OQ-1: NFR-số (P95 loop, ngưỡng alert error-rate) — đo ở GĐ8/Operate, không bịa.
                    • Model/endpoint LLM cụ thể + bản Python chính xác của gốc — xác nhận ở skeleton.
Gợi ý lát cắt sống : "accept → plan/decompose(+gate2 μ↓) → next_node → delegate(scope⊆parent) → judge_by_evidence → finish/blocked"
                     xuyên Facade→Orchestration→Execution-Core(execute_tool)→SQLite checkpoint→event-log; chèn resume ở giữa để DÍNH LUÔN SPIKE-1.
Artifact          : rebuild-hex-agent/pipeline/07-stack.md
→ Dựng live slice / walking skeleton end-to-end để chứng minh stack + kiến trúc (đo luôn SPIKE-1): chạy /skeleton
→ Cần điều phối tiếp trọn pipeline tới release: chạy /partner
→ Muốn code ngay một slice nhỏ để thử stack: chạy /frame
→ Kiến trúc lộ ra vấn đề khi chọn tool (không xảy ra ở lượt này): quay lại /shape
════════════════
```
*Traceability:* GĐ7 nhận Architecture Brief GĐ6 (`06-shape.md`: 6 module, 6 ADR, ràng buộc-cho-stack) + evidence gốc (`evidence-B:34`, `evidence-C`, `ATLAS.md:27` stack quan sát) → sinh 7 quyết định (6 ma trận có điểm + 1 ràng-buộc-ép) + 7 ADR (đều có phương án đã loại) + SPIKE-1 → bàn giao `skeleton` (GĐ8). SPIKE-1 + OQ-1 (NFR-số) + config LLM chuyển tiếp có địa chỉ; không cái nào đứt chuỗi.
