# Contract — Execution-Core (FROZEN 2026-07-03)

> Interface đủ để build độc lập. Bám evidence gốc `core/kernel.py`, `core/session.py`, `core/schemas.py`.

## Public API (chữ ký hàm)
```python
class AgentKernel:
    def execute_tool(self, tool_name: str, args: dict | None = None,
                     *, context: ToolCallContext | None = None) -> dict: ...
    def freeze(self) -> None: ...            # sau freeze: cấm đổi registry/middleware
    def use(self, middleware: ToolMiddleware) -> None: ...

class KernelSession:
    identity: SessionIdentity                 # frozen 7-field lineage
    allowed_capabilities: frozenset[str]
    def execute_tool(self, name: str, args: dict) -> dict: ...  # → kernel.execute_tool với context

class SessionFactory:
    def create_root(...) -> KernelSession: ...
    def create_child(self, parent, *, allowed_capabilities) -> KernelSession: ...  # scope ⊆ parent (fail-closed)
    def restore(self, *, identity, state, allowed_capabilities) -> KernelSession: ...  # kw-only
```

## Envelope (mọi tool trả)
```python
CapabilityResult(ok: bool, capability: str, feature: str|None,
                 data: dict, error: str|None, metadata: dict)  # .as_dict()
```

## Bất biến contract (bên gọi được đảm bảo)
- Mọi call phát `tool.requested` (trước) + `tool.completed|failed` (sau) qua event bus.
- Scope-check: `tool_name ∉ allowed_capabilities` → trả `ok=False` (không raise).
- Sau `freeze()`: registry/middleware bất biến; chỉ session state đổi.
- Exception của tool KHÔNG thoát kernel (bọc try/except → ok=False).

## Error code
`CAP_OUTSIDE_SCOPE` · `CAP_NOT_FOUND` · `KERNEL_FROZEN_MUTATION`.
