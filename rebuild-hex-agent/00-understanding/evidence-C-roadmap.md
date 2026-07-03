# Evidence C — Roadmap, Epics & Clone-from-scratch plan (original hex_agent)

> Source: `docs/roadmap/`, `docs/harness-rebuild-guide.md`, `plans/.../clone-hex-agent-roadmap`, `CHANGELOG.md`, plus skillsh `roadmap-suite.md`/`roadmap-portfolio.md`.

## 1. Epic / phase map (E01–E21)
Phases: **P0 Foundation** (E01–E04) · **P1–P2 Single-agent+Tools** (E05–E08) · **P3 Multi-agent** (E09–E10) · **P4 Realtime Control** (E21, gathers E15/E16/E17/E18).

| Epic | Name | Phase | Status | Folder |
|---|---|---|---|---|
| E01 | Microkernel Core | P0 | ✓ | `core/` |
| E02 | Output Discipline | P0 | ✓ | `discipline/` |
| E03 | LLM Adapter | P0 | ✓ | `llm/` |
| E04 | Observability | P0 | ✓ | `observability/` |
| E05 | Single-agent Graph | P1 | ✓ | `graph/`,`orchestrator/` |
| E06 | Tools & Safety | P1–P2 | ✓ | `toolbox/`,`safety/`,`middleware/` |
| E07 | Skills System | P2 | ✓ | `skills/` |
| E08 | RAG (Qdrant) | P2 | ✓ | `rag/` |
| E09 | Roles & Lenses | P3 | ✓ | `roles/` |
| E10 | Multi-agent + Delegation | P3 | ✓ | `supervisor/`,`delegation/`,`adapters/` |
| E11 | Departments | P4 | ✗ park-with-trigger | — |
| E12 | IntentRouter/GlobalSupervisor | P4 | ✗ park | — |
| E13 | Software Factory | P4 | ✗ park | — |
| E14 | Ledger & Memory | P4 | ✗ park | — |
| E15 | Self-eval & Governance | P4 | ⚠ merged→E21 | — |
| E19 | Test Harness | cross | ✓ | `tests/`,`tests_audit/` (327 tests) |
| E20 | Labs | after | ✗ park | — |
| E21 | Realtime Control Plane | P4 | ⊕ partial (Phase A + B1) | `control/` |

E21 detail: Phase A (contracts: RuntimeEvent/RuntimeCommand/RuntimeCheckpoint/Permission/Redactor + 2 registries) ✓; Phase B1 (EventEmitter canonical path via EventSinkPort→BusEventSink) ✓; **pending**: control-store+command-queue+approval-checkpoint (B2–B14), transport (POST /api + SSE), Control-Tower UI, reliability. Supervisor emitter `default None` (`supervisor/graph.py:48`) — not wired to runtime.

## 2. Build sequence & why
Critical path: `E01 → E03 → E02 → E05 → E09 → E10 → E12`.
- S0 (P0): E01→E03→E02→E04 (kernel+adapter+discipline+observability). DoD: `run_smoke.py` offline deterministic.
- S1 (P1–P2): E06 ∥ E05 (tool chokepoint + single-agent loop).
- S2 (P2–P3): E07,E08 ∥ E09 (skills + RAG health-gated + role allowlist).
- S3–S4 (P3): E10 (TaskLoop O composes team, delegates, evidence-based acceptance).
- S5 (P4): E21 (contracts + emitter shipped; live control pending).
Walking skeleton evolves: S0 kernel+JSON+events → S1 single-agent loop w/ sandboxed tool chokepoint → S2 role allowlist + progressive skills + RAG health-gate → S3–S4 multi-agent TaskLoop finishes on evidence.

## 3. Clone-from-scratch roadmap (7 phases, code-neo anchored, DoD gates)
1. **Microkernel + Observability** (E01,E04): `AgentKernel.execute_tool` chokepoint (`core/kernel.py:63`), registry, schemas, EventBus, JSONL+summary. DoD `run_smoke.py`. Pitfall: raw-args logging leak (`core/kernel.py:125`).
2. **LLM + Discipline** (E03,E02): LLM-as-capability via execute_tool, JSON-mode, transient-vs-permanent retry, json_gate+condense+budget+finish-gate as SHARED modules. DoD parse-repair + budget (max_steps).
3. **Toolbox + Safety** (E06): fs_read/write/list (sandbox jail), terminal_run (argv-only), SafeToolPort per-tool policy, PolicyGate fail-closed, workspace containment (`safety/sandbox.py:38,97`). DoD sandbox-escape + policy-matrix.
4. **Graph Runtime + Resume** (E05): LangGraph substrate, serializable `AgentState` (schema v2), SQLite checkpoint = truth (`orchestrator/checkpoint.py`), resume same run_id. DoD resume round-trip. checkpoint.json = read-only projection of SQLite.
5. **Skills + RAG** (E07,E08): skills progressive-disclosure (render-contract vs render-full), RAG health-gate (never raises, offline-first), lazy Qdrant uuid5 ids, feature plugin pattern. DoD ingest/search optional, tests skip if Qdrant down.
6. **Roles + Delegation** (E09,E10): `RoleView` allowlist = union−forbidden (`roles/agent.py:53`), `DelegationManager` SEPARATE chokepoint (`delegation/manager.py:63`), `TaskLoop` round-based (`supervisor/loop.py`), evidence-based acceptance (`judge_acceptance`), session scope child ⊆ parent. DoD TaskLoop reaches FINISHED, no privilege escalation.
7. **Control Plane** (E21 A+B1): contracts-first (RuntimeEvent envelope, RuntimeCommand, Redactor 14-key mask, registries allowlist), EventEmitter canonical path gate→seq→redact→fanout via EventSinkPort. DoD 0 secret in ui_payload; DEC-7 authz≠attribution.

### 17 load-bearing invariants (I1–I17)
- I1 `execute_tool` single chokepoint (observability/safety/envelope added once).
- I2/I3 `freeze()` + `KernelSession` → 0 state bleed between runs.
- I10/I11 `AgentState` serializable-only + SQLite-truth → safe resume, no side-effect re-run.
- I13/I14 delegation chokepoint separate + scope child ⊆ parent → auditable multi-agent, no privilege escalation.
- I16/I17 redact at boundary + attribution ≠ authz → realtime control without secret leak, don't trust self-report.

## 4. Future epics — park-with-trigger (YAGNI discipline)
All future epics gate-in 🟢 (deps allow) but parked until metric thresholds hit AND a consumer is in-progress. Thaw protocol: Detect (run metric commands) → Confirm trigger → re-eval deps (mandatory) → choose cheapest altitude (YAGNI) → plan on existing seam → cook to DoD. Known deadlocks: E11↔E12 cycle (break: E11 registry-only when E12 enters design); E12↔E13 boundary (E13=fixed pipeline+handoff audit, E12=route many tasks). E15 self-eval NOT a separate epic — merged into E21 (tighten judge_acceptance evidence types); judge≠doer only pays when a separate verifier exists (today Agent O self-scores = honor-system).

## 5. skillsh roadmap format (for mirroring)
`roadmap-suite.md` (detailed) + `roadmap-portfolio.md` (slim) — a multi-project orchestration harness over the 12 VN skills. 4 phases: P0 data-foundation+harness (canonical-key normalizer, portfolio.json, acceptance-first testkit), P1 data-isolation+migration, P2 orchestration core (/switch,/dashboard,/router), P3 intelligence (portfolio-critical-thinking, lifecycle). AC style = **oracle-based [GATE]** (regex/diff-state/fixture PASS-FAIL, not narrative); read-only invariant (diff state after run = empty); phase = component owner. Top risk = basename collision silently overwrites → hash+verify at normalizer.

## Key anchor index
- `core/kernel.py:63` execute_tool · `:125` raw-args log
- `core/session.py:48` freeze · `:163` scope ⊆ parent
- `discipline/{json_gate,budget}.py`
- `llm/adapter.py` JSON-mode/lazy/retry-classify
- `observability/event_log.py:102` attach_to_bus
- `graph/state.py` AgentState v2 · `orchestrator/checkpoint.py:31-32,139` SQLite truth
- `safety/sandbox.py:38,97` · `middleware/PolicyGate` fail-closed
- `roles/agent.py:53` allowlist · `roles/spec.py:45,49` unused dept/route fields
- `delegation/manager.py:63` delegate chokepoint · `supervisor/loop.py:70` run_task_loop seam
- `control/events.py:113` · `control/emitter.py:53` · `control/ports.py:15` · `supervisor/graph.py:48` emitter default None
- `supervisor/evidence.py`, `supervisor/state.py:29,36` acceptance
