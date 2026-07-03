# Roadmap + Backlog — HexAgent (GĐ9 PLAN)

> Bám epic gốc E01–E21 / P0–P4. AC nằm dưới story; DoD tách riêng (delivery). Nguồn: `rebuild-hex-agent/pipeline/09-backlog.md`.

## Roadmap (theme × release)
| Release | Theme | Epic | Điểm bán |
|---|---|---|---|
| **R1** | Foundation | E01 Kernel · E02 Discipline · E03 LLM · E04 Observability | nền an toàn, smoke offline |
| **R2** | Single-agent + Tools | E05 Graph/Resume · E06 Tools-Safety · E07 Skills · E08 RAG | agent đơn chạy tool có sandbox |
| **R3** | **Multi-agent (LÕI)** | E09 Roles · E10 TaskLoop+Delegation+Acceptance | **M1/M2/M3 — finish-by-evidence có biên** |
| **R4** | Control Plane | E21 (contracts→emitter→transport→UI) | quan sát/điều khiển realtime |

## Backlog phân rã (trích lõi)
**Epic E10 — TaskLoop+Delegation+Acceptance (R3, điểm bán):**
- Feature F-10.1 Plan/Decompose có chứng-minh-dừng
  - Story S-10.1.1: *Là* agent, *khi* nhận task nhiều bước, *thì* sinh cây plan với μ co ngặt mỗi lần chia.
    - AC: cây acyclic; mỗi accept giảm len(done_when); RENAME/STUCK bị chặn.
- Feature F-10.2 Acceptance-by-evidence
  - Story S-10.2.1: *khi* O tuyên FINISHED, *thì* mọi AC phải có ≥1 evidence THẬT (không scaffolding).
    - AC: `all_accepted()` chỉ true khi status=passed ∧ evidence_ids≠∅ ∧ kiểu-real. (M1)
- Feature F-10.3 Bounded finish
  - Story S-10.3.1: *khi* không tiến triển/hết budget, *thì* BLOCKED trong biên.
    - AC: max_rounds/no-progress/repeat/parse/depth đều chặn được (test). (M2)
- Feature F-10.4 Delegation scope-safe
  - Story S-10.4.1: *khi* delegate, *thì* scope con ⊆ cha, fail-closed.
    - AC: `delegation_rejected{scope}` khi con xin quyền ngoài cha. (M3)

## Release Plan
R1 (alpha nội bộ, write/delegation TẮT) → R3 build lõi + đóng 3 Critical review → pilot (bật write sau redact-before-write) → beta (bật delegation sau scope-property).

## Traceability
Mỗi Feature nối 1 business objective (M1/M2/M3 ở problem/business-case.md); mỗi Story thuộc 1 Feature; AC nối thẳng 5 domain-rule (docs/domain-model.md).

## Cổng GĐ9: backlog đủ để plan? → GO.
