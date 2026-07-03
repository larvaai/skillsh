# Module Map — HexAgent (GĐ10) — FREEZE

> Cổng mở nhánh song song: sau khi contract freeze, các module không phụ thuộc nhau build song song (fanout). Nguồn: `rebuild-hex-agent/pipeline/10-modules.md`.

## Bản đồ (bounded context → module → owner → phụ thuộc)
| Module | Bounded context | Owner team | Phụ thuộc | Contract |
|---|---|---|---|---|
| **Execution-Core** | Execution-Core | Platform | — (nền) | [contracts/execution-core.md](contracts/execution-core.md) |
| **Orchestration** | Orchestration | Orchestration | Execution-Core | [contracts/orchestration.md](contracts/orchestration.md) |
| **Observability-ControlPlane** | Observability/Control-Plane | Observability | Execution-Core (event bus) | [contracts/observability-controlplane.md](contracts/observability-controlplane.md) |
| Discipline | Discipline | Platform | — | (json/finish/budget — logic thuần) |
| Tools-Safety | Tools & Safety | Safety | Execution-Core | (sandbox/policy — seam sau) |
| Knowledge | Knowledge | Observability | Execution-Core | (RAG optional, TẮT mặc định) |

## Seam công khai (chỉ 2 cửa — cấm bypass)
1. **Execution-Core** expose `execute_tool` — mọi hành động một cửa.
2. **Orchestration** expose `run_task_loop` + `DelegationManager.delegate`.
Cross-module đi qua đúng 2 seam này + event bus; tool gọi thẳng không qua execute_tool = vi phạm contract.

## Nhánh song song mở sau freeze
`pg-build`: **Execution-Core ∥ Orchestration ∥ Observability-ControlPlane** — cả ba chỉ phụ thuộc contract (đã freeze) + delivery-standards, KHÔNG phụ thuộc lẫn nhau ở tầng build (bám cùng contract). → `fanout`.

## Cổng GĐ10: ownership rõ + contract đủ để build độc lập? → GO (FREEZE).
