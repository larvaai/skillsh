# Evidence A — Core Orchestration Loop (original hex_agent)

> Source: read-only investigation of `/Users/uspro/Desktop/namnson/hex_agent`. Every claim anchored to `file:line`. This is the mechanism the rebuild must reproduce: **task → plan → ordered steps → delegate to sub-agents → finish only when provably complete**.

## 1. The core loop
- Public facade: `orchestrator/loop.py:run()` [93-147] — builds `TaskEnvelope` + `KernelSession`, compiles LangGraph via `build_agent_graph()` (`graph/runtime.py:31-66`), streams until terminal, returns `_outcome()`.
- Supervisor driver: `supervisor/loop.py:_drive()` [157-241] — `while not state.is_terminal`:
  1. `o_decide(state, ctx, budget)` [171] → `OrchestratorDecision`
  2. route: `finished`→`judge_acceptance()`+`_terminate()` [184-190]; `continue`→`run_round()` [196]; `need_tool`→`run_tool()` [193]; `blocked/failed`→terminate [198-201]
  3. `apply_pending_commands()` [209] (roster changes)
  4. `state.round_no += 1` + `ctx.save(state)` [217-218] — atomic checkpoint
  5. guards: max_rounds, no-progress, repeat-decision [164-239]
- Terminal: `FINISHED` (all acceptance satisfied) / `BLOCKED` (guards) / `FAILED` (parse budget).

## 2. Planning / decomposition — two engines
- **Supervisor team compose**: `supervisor/graph.py:compose_team()` [107-124] → `SessionPlan` → list of `AgentSelection`; plan held as `TaskLoopState.selected_agents` + `TaskLoopState.turns`. Ordering is implicit via O's `next_agent_calls` per round.
- **Recursive decomposition**: `decompose_agent/solve.py:solve()` [258-301] walks a `Tree` (`tree.py:Tree` [21-51]) — nodes are a forest (parent) + DAG (`depends_on`), both acyclic [63-121]. `Tree.next_node()` [43-51] = leftmost pending node whose deps are all done (topo by depth,order).
  - Node status: pending→active→(done|blocked|decomposed) (`node.py:28`).
  - Leaf: `solve_leaf()` [80-121] — worker proposes → Gate-1 checks → PASS=done / FAIL=retry (K=3, K_LEAF=5); budget guard [91].
  - Decompose: `_decompose()` [132-185] — `worker.decompose()` → **Gate-2 `accept_decomposition()`** (pure structural, runs BEFORE tree mutation) [167]. Termination proof: μ(node)=len(done_when), every accepted child strictly shrinks it (`accept.py:52-128`); coverage-by-implication [101-127]; detects RENAME (Jaccard>0.80) / STUCK [165]. Parent's `done_when` becomes structural `all_children_done` [175]; synthetic reduce node added [187-201].
  - Reduce: `solve_reduce()` [204-224] — pure code, `run_reduce()` ops merge_json/pick/concat/manifest.
  - Closure: `_close_done_parents()` [229-253] re-asserts parent's ORIGINAL done_when; fail→COMPOSE_FAIL blocks.
- Data: `Node` frozen dataclass (`node.py:102-177`): id,parent,kind(work|reduce),status,depends_on,done_when(tuple[DoneWhen]),max_attempts,depth,order. `DoneWhen` (`node.py:50-100`): check,params,artifact — verdict keys forbidden [20] (gate alone writes verdicts).

## 3. Delegation — framework-neutral chokepoint
- `delegation/manager.py:DelegationManager.delegate()` [63-192]: validate policy (`policy.py:13-32`: depth≤max_depth, capability scope ⊆ parent, max_steps) → store request → resolve handler + child session → `Handler.run()` [160] → merge artifacts+result → close child → emit `delegation.finished`. Returns `DelegationResult`.
- Supervisor side: `supervisor/graph.py:run_round()` [218-337] — expand departments→agent calls, authority gate (assignments ⊆ selected agents) [265-268], skip completed turns (resume guard) [273-276], per assignment: Broker writes packet [278], build `DelegationPolicy` from O's `allowed_capabilities` [298], call `delegation_service.delegate()` [299] (the chokepoint), append `AgentTurn` + checkpoint after EACH turn [332].
- Scope: O sets `AgentAssignment.allowed_capabilities`; **Broker never widens scope** (`broker.py:1-8`); validated vs parent (`policy.py:25-26`).

## 4. Finish / acceptance gate
- Completion: `supervisor/loop.py:_drive()` [186] `if state.all_accepted()` (`state.py:107-108`) — all `acceptance_checks.is_satisfied` (status=="passed" AND evidence_ids non-empty, `state.py:35-37`).
- Acceptance gate: `supervisor/graph.py:judge_acceptance()` [357-382] — O provides `acceptance_status` [{id,status,evidence_ids}]; each cited evidence must resolve on Blackboard AND be REAL evidence (not scaffolding) [373]. Non-evidence: session_plan/context_packet/ac_report (`evidence.py:16-23`); real: artifact/tool_result/reviewer_report/diff/test_result [20]. Only "passed" honored with ≥1 valid evidence [370].
- Prevents premature finish: O must emit "finished" [184]; if not all_accepted, denied [186-191].
- Prevents runaway: max_rounds [164]; no-progress guard (artifacts didn't grow AND acceptance unchanged AND no commands) [229-235]; repeat-decision guard (same signature N× → BLOCKED) [237-238]; parse-error budget [172-173].
- Finish gate (agent level): `discipline/finish_gate.py:check_finish()` [15-22] blocks final if `code_changed` but `!validation_passed` (unless finish_reason="blocker").

## 5. Budget & guardrails
- Loop budget `discipline/budget.py:Budget` [10-67]: max_steps (parse errors don't consume), max_parse_errors (CONSECUTIVE, resets on good parse), max_same_tool_calls.
- Delegation budget `policy.py` [8-32]: per-delegation max_steps=100, max_depth=8.
- Decompose budgets `decompose_agent/budget.py`: root max_steps; per-node K=3/K_LEAF=5; parse max=8; MAX_DEPTH=6 (`solve.py:34`).
- Guards: `graph/nodes.py:guard_node()` [40-48] checks steps≥max before agent call; tool-repeat [116-126]; delegation depth+scope [manager.py:80]; decompose depth [solve.py:270] / step [91,150,210]. Hard stops: MAX_DEPTH + per-root step budget.

## 6. State / checkpoint / resume
- Supervisor state `supervisor/state.py:TaskLoopState` [81-156] — primitives only; `encode/decode_taskloop_state()` [119-156]; checkpoint to SQLite `checkpoint_store.save()` [loop.py:218].
- Agent graph state `graph/state.py:AgentState` (LangGraph dict): messages, budget(dict), last_action, session_state, route.
- Decompose state: `Tree` (YAML checkpoint) + `Journal` audit log.
- Resume: `orchestrator/loop.py:resume()` [217-273] — SQLite checkpoint via `open_checkpointer(run_id)` [246], legacy JSON fallback [227], resumes graph from `next` [260-269]. `supervisor/loop.py:resume_task_loop()` [117-154] loads Blackboard, validates identity, calls `_drive()` if not terminal.
- Safety: commands + round + save in ONE atomic txn [208-218]; idempotency keys track applied commands [state.py:98].

## 7. Key contracts / schemas
- `TaskEnvelope` (core.schemas): user_request, task_id.
- `OrchestratorDecision` (`supervisor/contracts.py:54-65`): decision∈{continue,need_tool,finished,blocked,failed}, next_agent_calls, tool_requests, acceptance_status, commands. `parse_decision()` strict JSON gate [117-182].
- `AgentAssignment` [45-51]: agent_id, objective, scope_of_work, allowed_capabilities, target_kind(agent|department).
- `ContextPacket` [69-83]: target_agent_id, objective, briefing, source_ids — NO scope field (Broker shapes context only).
- `DelegationRequest/Result` (core.schemas): outcome(success|rejected|failed), artifacts, summary, error; progress via `DelegationProgress`.
- `Node`/`DoneWhen` (decomposition) — see §2.
- `AcceptanceCheck` (`state.py:28-49`): id,text,status(pending|passed|failed),evidence_ids; is_satisfied.
- `evidence.py:evidence_type_of()` [26-40] — real vs scaffolding evidence.

## Core immutables (invariants a faithful rebuild must keep)
- Node status transitions via `tree.set_status()` + `rebuild_children()`.
- Worker never writes verdicts — gate alone assigns outcome.
- Broker never sets scope — O alone controls capability boundaries.
- O never calls tools directly — supervisor executes via kernel.
- Checkpoint atomic: roster + commands + round land together.
