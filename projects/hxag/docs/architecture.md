# Architecture Brief — HexAgent (GĐ6 SHAPE) — draft v1

## Góc nhìn lãnh đạo
Hệ có hình = **hexagonal modular monolith**: nhân đông cứng (kernel) + session sống, 6 module ánh xạ 1–1 bounded context GĐ5. Hai bệnh chết người (báo-xong-khống + runaway) được đóng bằng kiến trúc.

## Architecture Brief (bảng quyết định)
| Ô | Quyết định |
|---|---|
| Style | Modular monolith, hexagonal (ports & adapters) |
| Module boundary | 6 module bám bounded context GĐ5; cross-module qua seam công khai |
| Data ownership | state chỉ ở Session; kernel stateless; event-log + SQLite = nguồn audit/resume |
| Integration | in-process event bus; delegation qua chokepoint riêng |
| Auth/scope | allowed_capabilities per session, enforce ở execute_tool; scope con ⊆ cha |
| Security | redact `ui_payload` tại biên; sandbox jail cho tool; STRIDE cho luồng delegate |
| Reliability | budget + guards (max bước/no-progress/repeat/depth) + finish-gate |
| Observability | event-log-first; mỗi call phát tool.requested/completed; replay=snapshot |

## C4 Context
`[Người giao task] → (HexAgent) → [LLM provider] [Tool sandbox] [Vector KB (optional)]`

## C4 Container
Orchestration · Execution-Core · Discipline · Tools-Safety · Observability-ControlPlane · Knowledge — nói chuyện qua event bus + 2 seam (execute_tool, DelegationManager.delegate).

## ADRs (mỗi quyết định lớn: rationale + phương án đã loại)
- **ADR-001 Hexagonal frozen-kernel + mutable-session.** Rationale: nhân đông cứng + state chỉ ở session → 0 rò state giữa run. *Đã loại:* shared mutable core — loại vì state bleed giữa các run đồng thời, không isolate được.
- **ADR-002 Single execute_tool chokepoint.** Rationale: thêm trace/scope/observability một lần, áp cho mọi call. *Đã loại:* rải call-site ở từng nơi gọi tool — loại vì không đảm bảo mọi hành động đều bị trace/scope-check (dễ có đường vòng).
- **ADR-003 Delegation chokepoint riêng (không phải method của kernel).** Rationale: multi-agent auditable, tách khỏi tool path. *Đã loại:* delegate như một method của kernel — loại vì trộn quyền tool-exec với quyền spawn-agent, khó audit scope con⊆cha riêng.
- **ADR-004 Evidence-based acceptance + bounded finish.** Rationale: chống báo-xong-khống + runaway. *Đã loại:* để LLM tự tuyên "xong" (self-report) — loại vì đó chính là bệnh M1; và bỏ guard (tin agent tự dừng) — loại vì mở đường runaway.

## Cổng GĐ6: đủ vững để chọn stack? → GO (sau khi vá ADR).
