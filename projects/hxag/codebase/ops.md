# Operations & Measure — HexAgent (GĐ14 LEARN)

> Ops Dashboard (4 nhóm) + Incident + Iteration Loop → quay lại GĐ9. Nguồn: `rebuild-hex-agent/pipeline/14-operate.md`.

## Ops Dashboard (một màn hình)
**Business (đối chiếu THẲNG mục tiêu GĐ1):**
- M1 `false_finish_total` — mục tiêu **0**. (chưa có số production — cần alpha chạy thật)
- M2 % run terminal trong ngân sách — mục tiêu **100%**.
- M3 `delegation_rejected{scope}` chặn đúng — mục tiêu **0 escalation**.

**Product:** % task đạt FINISHED · số round TB/task · tỉ lệ runaway-blocked · độ sâu decompose TB · % AC pass lần đầu.

**Engineering (DORA + observability gốc):** deploy freq · lead time · CFR · MTTR · và `tool_calls`/`llm_calls`/`parse_errors`/`same_tool_blocks`/`policy_blocks`/`tool_failures` (từ summary.json).

**Operations:** uptime · resume success rate · sandbox-escape attempts (mục tiêu **0**) · secret-in-ui_payload (mục tiêu **0**).

## Incident Process (playbook)
- **"AC passed nhưng kết quả sai"** (honor-system gap) → freeze run, dump events.jsonl, soi provenance evidence (G1 guard log), thêm verifier độc lập.
- **"runaway không bị chặn"** → kiểm guard nào miss (no-progress proxy? repeat signature?), pin version + tắt flag.
- **"secret rò trong log"** → xoay key, kiểm freeze-gate G3, bổ sung SECRET_KEYS.

## Iteration Loop (LEARN → quay lại GĐ9)
Task đề xuất cho vòng backlog kế:
- **I-1:** đo SPIKE-1 resume atomic trên staging rebuild (chặn ĐÓNG R1) → `/frame`.
- **I-2:** chạy test module trên CI rebuild để tuyên M1/M2/M3 bằng số thật → `/backlog` refine + `/fanout`.
- **I-3:** set baseline OQ-1 (DORA + NFR-số P95/alert) qua ≥1 tuần alpha → `/operate`.
- **I-4:** verifier độc lập cho honor-system (judge≠doer) → backlog E15→E21.

## Cổng GĐ14: đạt mục tiêu? → GO mở vòng kế (đạt MỘT PHẦN — lõi chạy ở nền/spec, M1/M2/M3 chờ số rebuild). Vòng đóng về GĐ9.
