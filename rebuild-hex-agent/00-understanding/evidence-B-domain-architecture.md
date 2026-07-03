# Evidence B — Domain Model & Architecture (original hex_agent)

> Source: `docs/domain-rebuild-v0.md`, `docs/system-architecture.md`, `docs/reference/{runtime-flow,known-risks}.md`, `MAP.md`, `PROPOSAL_kernel_seams.md`, `core/`, `control/`. Anchored to file:line / doc-section.

## 0. One-liner
Hexagonal (microkernel) multi-agent **glass-box** system: a single **frozen** `AgentKernel` forces every capability call through one chokepoint (`execute_tool`), an event-log-first control plane makes runs fully replayable/resumable, and a pure-consumer UI reads a read-model behind 3 sealed seams.

## 1. Bounded contexts (DOM-1, `domain-rebuild-v0.md:26-65`)
- **(A) Execution Core** `core/` — `AgentKernel.execute_tool` = the single chokepoint; in-process event bus → RuntimeEvent.
- **(B) Control Plane** `control/` — EventEmitter (validate→seq→redact→fan-out), RuntimeEvent envelope, TaskLoopSnapshot read-model, RuntimeCommand + registries. The SEAM = 3 pieces.
- **(C) UI** `ui/` — pure consumer of read-model; **NO imports from core/**, no business logic.
- Core invariant ARC-1: `UI ⊥ core/`.

## 2. Core entities / aggregates
**Execution core:** `AgentKernel` (frozen shared runtime; owns registry, event bus, middleware; `core/kernel.py:76-89`); `KernelSession` (per-run mutable state; chokepoint `session.execute_tool`; `core/session.py:49-85`); `SessionIdentity` (immutable 7-field lineage: session_id/run_id/task_id/agent_id/parent_session_id/delegation_id/depth); `SessionFactory` (only constructor; enforces child scope ⊆ parent; `restore()` kw-only, `session.py:188-194`); `StateStore` (per-run dict, deep-copy isolation); `TaskEnvelope` (user_request/context/metadata/task_id, `schemas.py:11-26`); `ToolRequest`/`ToolCallContext` (6 lineage fields + `allowed_capabilities`); `CapabilityResult` (ok/capability/feature/data/error/metadata — every tool returns this).
- Step→Run→Task: **Run** = `SessionIdentity.run_id` (no class); **Step** = one `execute_tool` call (no first-class entity; `max_steps` a knob not enforced in core); **Checkpoint(core)** = StateStore.snapshot dict + identity + caps, restored via SessionFactory.restore. ⚠️ distinct from `control.RuntimeCheckpoint` (approval gate) and `orchestrator.Checkpoint` (UI projection).

**Control plane:** `RuntimeEvent` (frozen, 14 fields, all validation in `__post_init__`; `control/events.py:113+`); `Actor` (type∈{human,agent,tool,system,runtime}+id — attribution only); `TraceContext` (trace/span/parent_span); `RedactionInfo` (level∈{public,ui_safe,internal,secret,restricted}); `SessionSeq` (per-session monotonic, RLock, start 1); `EventEmitter` (gate→seq→redact→fan-out; `emitter.py:53+`); `TaskLoopSnapshot` (read-model, 9 fields, `build_snapshot` fold; `snapshot.py:88+`); `AgentView` (one agent node, status∈{pending,waiting,running,done,failed}); `RuntimeCommand` (frozen, 7 fields, idempotency_key); `IssuedBy` (attribution ≠ authz, DEC-8); `CommandAck`; `RuntimeCheckpoint` (approval gate, risk∈{low,medium,high,dangerous}, status∈{waiting,approved,rejected,expired,auto_approved}); `Permission` (per-agent caps, effective_from∈{immediately,next_turn,next_checkpoint}); `Redactor` (15 SECRET_KEYS, recursive mask '[REDACTED]', no mutate); `EventReplayBuffer` (ring maxlen=2048, dedup by event_id, needs_resync).

## 3. Event & command catalogs (closed, config-driven)
- Events loaded from `config/runtime_event_types.yaml` (~50 types, enumerable). Families: session.*, agent.* (advisory, NOT folded), tool.* (`tool.requested/completed/failed`), permission/checkpoint/approval.*, command.*, artifact.*, **loop.*** (folded into snapshot), delegation.*. ⚠️ Known mismatch: kernel emits `tool.requested/completed` but registry declares `tool.call_requested/before_call/after_call` — reconcile.
- Commands: 16 closed types in `config/runtime_command_types.yaml`. apply_at ∈ {immediate (only StopAgentTurn), immediate_if_waiting, next_checkpoint}. Null-permission group (v0 UI): Pause/Resume/StopAgentTurn/SubmitPrompt.

## 4. Architecture style — hexagonal/microkernel
- **Frozen kernel + mutable session.** Freeze at `core/bootstrap.py:28-53` before first run; after freeze no registry/middleware change, only session state mutates.
- **Ports (protocols):** `ToolPort` (name+execute), `DelegationPort` (name+can_handle+run), `DelegationServicePort` (available_targets+delegate), `EventSinkPort` (`control/ports.py:15`, single transport point).
- **Single chokepoint `execute_tool` (`core/kernel.py:106-150`):** builds ToolRequest → publish `tool.requested` (with lineage+args) → scope-check (tool ∈ allowed_capabilities else fail) → middleware chain (outer→inner: Timing→PolicyGate→BudgetGuard→Retry→Condense→core) → publish `tool.completed|failed` → return CapabilityResult. Guarantees: traced, scope-checked, normalized envelope, exceptions never escape.
- **Three seams (BE↔UI, DOM-2, frozen contract CASE-4):**
  1. Event stream: `RuntimeEvent.as_dict()` canonical; UI reads only `ui_payload`; `GET /api/stream` SSE (+ proposed `?since=seq` resync).
  2. Snapshot read-model: `TaskLoopSnapshot` fold of loop/approval/permission/checkpoint events; terminal status never overwritten; `GET /api/snapshot`.
  3. Command channel: `RuntimeCommand`→`CommandAck`; `POST /api/commands` (IDE backend has token authz; console path proposed).

## 5. Subsystems / ownership
core (chokepoint, registry, session), control (event validate/redact/read-model/commands), discipline (json_gate/finish_gate/budget/condense — pure logic), toolbox (sandboxed fs/terminal/code-intel), safety (workspace jail + deny-list + SafeToolPort), middleware (policy/budget/retry/timing/condense), observability (EventLogger→jsonl/summary/metrics), orchestrator (run/resume façade + LangGraph + SQLite), graph (LangGraph topology + AgentState), supervisor (multi-agent TaskLoop, Agent-O, broker, evidence), delegation (policy/scope/manager), roles (specs/lenses/allowlist), rag (Qdrant vector KB), ui (HTTP/SSE console), llm (OpenAI-compatible JSON-mode adapter), features (plugin loader). v0 scope keeps core/control/toolbox/safety/discipline; supervisor/delegation/roles/rag exist but deferred in v0.

## 6. Security / safety
- Scope: per-session `frozenset` allowed_capabilities; enforced in execute_tool; child ⊆ parent on delegation (SessionFactory).
- Workspace jail: `safety/sandbox.py resolve_in_workspace` — all paths must be relative_to `var/workspace/`.
- Redaction: `ui_payload` redacted before leaving emitter; 15 hardcoded SECRET_KEYS; raw payload never leaves. Known gap: `tool.requested` logs raw args to jsonl (redact before enabling write tools).
- Permission/authz (DEC-8): `issued_by` = attribution only; real authz = `requires_permission` + checkpoint; today `supervisor/command_bridge.py` trust-O bypass (enforcement proposed). `UpdateAgentPermission` always human-gated.
- Policy deny-list: `middleware/policy.py PolicyGate` fail-closed.

## 7. Reliability / observability / invariants
- EventLogger subscribes tool.*/task.* → events.jsonl + summary.json + metrics (tool_calls/llm_calls/failures/blocks/parse_errors).
- Resume: `langgraph.sqlite` per run = TRUTH; `checkpoint.json` = UI projection, never read for resume; `orchestrator.loop.resume` → SessionFactory.restore → stream(None).
- Replay: `build_snapshot(events)` linear fold, deterministic on seq order, terminal-status guarded; EventReplayBuffer resync.
- **Enforced invariants (i–vi):** (i) all actions via execute_tool→tool.requested/completed; (ii) seq monotonic gap-free per run; (iii) redact before fan-out; (iv) risky action needs approval gate [partial]; (v) replay(events[0..n])=Snapshot(n) deterministic; (vi) resume from any checkpoint (SQLite truth). Plus: freeze kernel before first session; scope shrink on delegation; UI ⊥ core; kernel stateless (state only in session).

## 8. Rebuild strategy (domain-rebuild-v0.md §4)
Preserve: frozen-kernel/mutable-session, single execute_tool chokepoint, events first-class, control-plane seals BE↔UI, redact-before-fan-out, SQLite-truth resume, scope-shrink delegation. v0 Phase 1 = read-only run timeline (single-agent, no delegation, thin UI, AC-1..AC-6).
