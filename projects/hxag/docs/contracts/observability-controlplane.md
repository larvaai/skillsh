# Contract — Observability-ControlPlane (FROZEN 2026-07-03)

> Bám evidence gốc `control/events.py`, `control/emitter.py`, `control/redaction.py`, `control/snapshot.py`, `observability/event_log.py`.

## Public API
```python
class EventEmitter:
    def emit_event(self, event_type: str, *, session_id, actor, trace,
                   payload: dict | None = None) -> RuntimeEvent: ...
    # thứ tự CỐ ĐỊNH: (1) registry-gate → (2) seq-stamp → (3) redact → (4) fan-out sinks

class Redactor:
    def apply(self, event: RuntimeEvent, level: str) -> RuntimeEvent: ...  # → ui_payload che secret

def build_snapshot(events: list[dict], *, session_id: str) -> TaskLoopSnapshot: ...  # linear fold
def attach_to_bus(bus) -> None: ...    # EventLogger → events.jsonl + summary.json + metrics
```

## Data
```python
RuntimeEvent(event_type, session_id, actor, trace, redaction, event_id, seq,
             round_no, ..., payload, ui_payload)   # 14 fields, validate ở __post_init__
```

## Bất biến contract
- Event-type ∉ registry → raise `ControlContractError` TRƯỚC publish (fail-closed).
- `seq` monotonic gap-free per-run; resume phải khôi phục seq high-watermark **[review G11]**.
- UI đọc CHỈ `ui_payload` (không bao giờ raw `payload`); replay(events[0..n]) = snapshot(n) tất định.
- Redact TRƯỚC fan-out; 0 secret thô trong ui_payload.
- **[review G3]** freeze fail-closed nếu có write-capability enabled mà Redactor chưa active cho `tool.requested` → error `WRITE_TOOL_ENABLED_WITHOUT_REDACTION` (owner: Execution-Core phối hợp).

## Error code
`EVENT_UNKNOWN_TYPE` · `EVENT_SEQ_GAP` · `WRITE_TOOL_ENABLED_WITHOUT_REDACTION`.
