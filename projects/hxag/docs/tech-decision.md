# Tech Decision Matrix — HexAgent (GĐ7 TOOLS)

> Chỉ chọn công cụ SAU khi kiến trúc chốt (GĐ6). Mỗi quyết định có điểm + rationale + phương án đã loại. Nguồn: `rebuild-hex-agent/pipeline/07-stack.md`.

## Ma trận (điểm 1–5, trọng số theo NFR)
| Quyết định | Chọn | Đã loại (điểm) | Vì sao chọn |
|---|---|---|---|
| Ngôn ngữ lõi | **Python 3.11** (5) | Go (3) / TS (3) | hệ sinh thái LLM/agent chín, frozen dataclass + Protocol đủ, team thạo |
| Graph/substrate | **LangGraph + SQLite checkpointer** (4) | orchestrator tự viết (3) | resume/checkpoint sẵn; ẩn số resume-atomic → SPIKE GĐ8 |
| Checkpoint store | **SQLite (per-run)** (5) | Postgres (3) / Redis (2) | embedded, là chân-lý-resume; không cần server cho single-node |
| LLM adapter | **OpenAI-compatible JSON-mode** (5) | function-calling riêng (3) | JSON-mode gate parse ổn, đi qua execute_tool như một tool |
| Vector KB | **Qdrant (lazy, mặc định TẮT)** (4) | pgvector (3) / none (3) | health-gated, offline-first; chỉ bật khi có consumer tri-thức |
| Transport control-plane | **SSE** (4) | WebSocket (3) | một chiều BE→UI đủ cho v1; đơn giản hơn WS |
| Test | **pytest + Hypothesis (property) + audit** (5) | chỉ unit (3) | invariant cần property-test (scope⊆parent, replay=snapshot) |

## ADR
- **ADR-101 Python 3.11.** Loại Go/TS: chậm hơn về hệ sinh thái agent, không đáng đổi.
- **ADR-102 LangGraph+SQLite.** Loại orchestrator tự viết: tốn thời gian dựng resume; giữ đường lùi nếu SPIKE-1 fail.
- **ADR-103 JSON-mode qua execute_tool.** Loại tool-calling riêng: sẽ tạo đường vòng quanh chokepoint.

## Spike treo
- **SPIKE-1 (U1):** LangGraph+SQLite resume round-trip — (a) không re-emit tool.requested bước đã done, (b) round_no liên tục, (c) crash giữa transaction không nửa-ghi. Time-box 1–2 ngày, đo ở GĐ8; fail → đảo sang ADR-102 phương án B.

## Cổng GĐ7: stack chốt? → GO (SPIKE-1 treo có địa chỉ).
