```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Architecture Brief" lấy từ prompt/file bạn đưa, CHƯA qua cổng GĐ6 (skill /shape).
- Rủi ro: (1) chưa truy vết ngược được về pipeline; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /shape trước để có "Architecture Brief" đã qua cổng.
```

**stack (GĐ7) · hex_agent — Chọn stack rebuild cho một shape đã chốt**

Kiến trúc bạn đưa (microkernel · 1 graph biên dịch dùng chung · `execute_tool` chokepoint · SQLite checkpoint · cần Python) ÉP sẵn phần lớn lựa chọn — nên đây là bài "xác nhận stack + neo lý do", không phải bài mở ma trận rộng. Tôi bám luôn code thật: hex_agent hiện đã chạy `langgraph`, `langgraph-checkpoint-sqlite`, `openai`, `PyYAML` trên Python 3.11+ (`pyproject.toml`), graph biên dịch ở `graph/runtime.py`, checkpoint SQLite ở `orchestrator/`.

─── GÓC NHÌN LÃNH ĐẠO (đọc trước, 30 giây) ───
**Chọn**: giữ **Python 3.11+ / LangGraph (graph biên dịch + SQLite checkpointer) / OpenAI-compatible SDK / PyYAML** làm nền rebuild; đóng gói bằng `pyproject.toml` + Ruff + Pytest.
**Vì sao**: kiến trúc đã chốt (một graph dùng chung, checkpoint SQLite, chokepoint execute_tool) chính là mô hình LangGraph sinh ra để làm — đổi nền = viết lại chính thứ đang chạy được. "Cần Python" trong đề bài đã khoá ngôn ngữ; phần còn lại là chọn cái nuôi được lâu và rẻ.
**Đã loại**: framework agent dựng-sẵn nặng (LangChain Agent / CrewAI / AutoGen) — tiện lúc đầu nhưng giấu mất cửa `execute_tool` và cách checkpoint, đúng thứ kiến trúc này coi là bất khả xâm phạm; Temporal/Redis cho checkpoint — mạnh nhưng nặng hạ tầng, thừa cho một checkpoint đơn tiến-trình.
**Rủi ro/chi phí**: rủi ro chính KHÔNG phải chọn sai tool mà là **khoá vào LangGraph ở lớp graph** và **giới hạn ghi đồng thời của SQLite** — cả hai đã cô lập sau seam (`graph/runtime.py`, `orchestrator/` checkpointer port), đổi được sau; còn 1 ẩn số cần đo (SQLite checkpoint dưới nhiều run song song) → đề xuất spike 1 ngày trước khi đổ người.

---

**Hạng mục cần chọn** (rút từ mô tả kiến trúc):
- Ngôn ngữ → **đã ép "cần Python"** → ghi 1 dòng.
- Graph runtime + checkpoint → **đã ép "một graph biên dịch dùng chung + SQLite checkpoint"** → đây là hạng mục lớn, mở ma trận (vì "graph framework nào" vẫn là câu mở).
- LLM client → ép bởi JSON-mode + adapter đã có → ghi 1 dòng.
- Packaging/quality tooling → thấp rủi ro → ghi gọn.

**Ràng buộc ghi thẳng (không mở ma trận giả):**
- *Ngôn ngữ = Python 3.11+* — đề bài ép "cần chạy Python"; code thật đã `requires-python = ">=3.11"`. Không mở ma trận đa-ngôn-ngữ.
- *LLM = OpenAI-compatible SDK qua `llm/adapter.py`* — kiến trúc ép mọi call qua `execute_tool` + JSON-mode ở lớp LLM; adapter lazy đã tồn tại. Giữ.
- *Packaging = `pyproject.toml` + Ruff + Pytest* — chuẩn Python hiện đại, đội đã dùng (`[tool.ruff]`, `[tool.pytest.ini_options]`). Giữ.

```text
TECH DECISION MATRIX — Graph runtime + Checkpoint (hạng mục lớn)
Tiêu chí (trọng số)                                  | LangGraph+SQLite | Custom state-machine | Temporal
Fit kiến trúc (1 graph biên dịch dùng chung)  (×3)   |        5         |         4            |    3
Fit chokepoint (execute_tool bọc được, seam giữ) (×3)|        5         |         5            |    3
Fit checkpoint/resume (SQLite là truth)        (×3)  |        5         |         3            |    5
Fit team (đã thạo — code đang chạy nền này)    (×2)  |        5         |         2            |    2
Fit maintainability (2 năm còn nuôi được)      (×2)  |        4         |         2            |    4
Fit hạ tầng (nhẹ, đơn tiến-trình đủ)           (×1)  |        5         |         5            |    2
TỔNG (có trọng số)                                   |       68         |        50            |   54
=> Chọn: LangGraph + langgraph-checkpoint-sqlite.
   Lý do: khớp thẳng "graph biên dịch dùng chung + SQLite checkpoint"; đội đã chạy nền này (giảm rủi ro rebuild).
   Đã loại: Custom state-machine (kiểm soát tối đa + nhẹ nhất, nhưng phải tự viết checkpoint/resume — tốn & dễ lệch, chỉ đáng nếu muốn bỏ hẳn phụ thuộc ngoài); Temporal (bền bỉ mạnh & resume tốt, nhưng kéo theo server/worker — thừa hạ tầng cho checkpoint đơn tiến-trình, hợp khi lên nhiều node).
```
*Trọng số: 3 tiêu chí "Fit kiến trúc / chokepoint / checkpoint" nặng ×3 vì đó là thứ kiến trúc đã CHỐT — chúng lái quyết định, không phải sở thích.*

```text
ADR-001 — Chọn LangGraph + SQLite checkpointer cho graph runtime
Bối cảnh   : kiến trúc chốt microkernel · một graph biên dịch dùng chung · execute_tool chokepoint ·
             SQLite là checkpoint truth · cần Python. Code hex_agent hiện đã chạy nền này.
Quyết định : Python 3.11+ · LangGraph (>=1.2,<1.3) · langgraph-checkpoint-sqlite · OpenAI-compatible SDK · PyYAML.
Lý do      : khớp 3 tiêu chí ×3 (fit kiến trúc/chokepoint/checkpoint); đội đã thạo; nhẹ hạ tầng.
Đã loại    : Custom state-machine (điểm mạnh: nhẹ + không phụ thuộc; thua ở checkpoint/resume phải tự nuôi);
             Temporal (điểm mạnh: bền bỉ + resume; thua ở nặng hạ tầng, thừa cho đơn tiến-trình).
Hệ quả     : khoá mềm vào LangGraph ở lớp graph (đã cô lập sau graph/runtime.py, đổi được); SQLite giới hạn
             ghi đồng thời (1 writer) — cần đo dưới tải song song; hiring Python dồi dào; không vendor lock cloud.
```

```text
SPIKE RESULT — SQLite checkpoint dưới nhiều run song song  (ẩn số DUY NHẤT còn treo)
Câu hỏi  : với N run/graph chạy đồng thời ghi checkpoint vào 1 SQLite (var/.../langgraph.sqlite),
           có nghẽn "database is locked" / resume có toàn vẹn không?
Time-box : 1 ngày.
Đo được  : [CHƯA CHẠY] — cần đội đo & báo số (thời gian ghi P95, tỉ lệ lock, resume đúng sau kill).
Kết luận : nếu đạt → chốt SQLite; nếu nghẽn → đổi checkpointer sang Postgres backend của LangGraph
           (đã có sẵn, đổi ở orchestrator port, KHÔNG đụng graph). Đây là điểm cần live slice chứng minh.
```

**Tự soi:** (1) Lãnh đạo đọc băng đầu duyệt được — chọn gì / loại gì / rủi ro, không jargon ✔. (2) Dev đủ để hành động — có ma trận có điểm + ADR có hệ quả + spike chỉ rõ đường lùi (Postgres backend) ✔. (3) Truy vết được — mọi ô neo vào kiến trúc đã chốt + code thật, không "đang hot"; nhưng ẩn số SQLite song song CHƯA có số đo thật → ma trận CHƯA đủ tin ở đúng điểm này.

**Cổng: "Stack đã chốt, sẵn sàng dựng live slice chưa?"** — Theo phân vai, **CTO** giữ quyết định GO; tôi (vai người duyệt) rà thấy: ma trận có điểm ✔ · ADR có phương án đã loại ✔ · mọi lựa chọn nằm trong ràng buộc kiến trúc ✔ · **NHƯNG ẩn số rủi ro cao (SQLite dưới tải song song) chưa có spike thực đo** → theo luật, **chưa nên tuyên GO cứng**. Đề nghị: duyệt stack "có điều kiện" và chạy spike 1 ngày ngay đầu live slice. Bạn (CTO) quyết: **GO có điều kiện** hay **chờ số spike rồi mới GO**?

```text
═══ BÀN GIAO — hex_agent · Tech Stack (GĐ7) ═══
Stack đã chốt      : Ngôn ngữ=Python 3.11+ · Graph=LangGraph · Checkpoint=langgraph-checkpoint-sqlite ·
                     LLM=OpenAI-compatible SDK (llm/adapter, JSON-mode) · Config=PyYAML ·
                     Packaging=pyproject.toml · Lint=Ruff · Test=Pytest
Ràng buộc kéo theo : khoá mềm LangGraph ở lớp graph (cô lập sau graph/runtime.py) · SQLite 1-writer ·
                     hiring Python dễ · không vendor lock cloud
Ẩn số còn treo     : SQLite checkpoint dưới nhiều run song song — spike 1 ngày; đường lùi = Postgres
                     checkpointer đổi ở orchestrator port, không đụng graph
Artifact           : state/project/hex_agent/pipeline/stack.md  (chưa ghi — đầu vào ngoài pipeline; xác nhận rồi ghi)
→ Dựng live slice end-to-end chứng minh stack + kiến trúc (gồm spike SQLite): chạy /skeleton (GĐ8)
→ Cần điều phối tiếp trọn pipeline tới release: chạy /partner
→ Muốn code ngay một slice nhỏ thử stack: chạy /frame
→ Kiến trúc lộ vấn đề khi chọn tool: quay lại /shape
════════════════
```
