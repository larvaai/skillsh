# Atlas — Template & luật cho 20 artifact

File này được skill `atlas` đọc. Nó định nghĩa: format evidence, thứ tự đọc, 20 artifact template, yêu cầu flow_traces, template index, và rubric scorecard.

Tất cả artifact ghi vào `<project-path>/.ai-understanding/`. Read-only trên code đích.

---

## 0. Luật evidence (bắt buộc cho mọi claim)

Mỗi nhận định trong mọi artifact phải kèm khối:

```text
Evidence:
- File path:
- Symbol / function / class / module:
- Dòng hoặc đoạn code liên quan:
- Suy luận từ bằng chứng:
- Mức chắc chắn:
```

Nhãn mức chắc chắn (dùng chung với skill `triage`): `chắc chắn` | `một phần` | `có thể sót` | `KHÔNG tìm thấy`.

- Không có evidence → KHÔNG được ghi như fact; đẩy xuống `18_risks_and_unknowns.md`.
- Tách **observed fact** (đọc được trong code) khỏi **assumption** (đang giả định). Gắn nhãn rõ.

Sai: `Project này dùng layered architecture.`
Đúng:
```text
Project có xu hướng layered vì controllers nhận HTTP, services xử lý logic, repositories chạm DB.
=> Flow HTTP → Controller → Service → Repository.
Evidence:
- File path: src/controllers/user.controller.ts, src/services/user.service.ts, src/repositories/user.repository.ts
- Symbol: UserController.create → UserService.create → UserRepository.insert
- Suy luận: tách tầng rõ theo tên & call chain
- Mức chắc chắn: chắc chắn
```

---

## 1. Thứ tự đọc (đọc MỘT lần, gom đủ cho cả 20 artifact)

```text
1  Project metadata   → package.json, README, pyproject, go.mod, Cargo.toml, composer.json…
2  Runtime entrypoints → main, server, app, cli, worker, routes
3  Configuration       → .env(.example), docker, build/framework config, schema
4  Folder/module       → src/, apps/, packages/, modules/, features/
5  Domain model        → entities, models, schema, migrations, types
6  API/contracts       → routes, controllers, DTOs, validators, RPC, events
7  Core flows          → trace 3–5 hành vi quan trọng end-to-end
8  Side effects        → DB write, external call, queue, email, file, cache
9  Tests               → unit, integration, e2e, smoke
10 Risks & unknowns    → phần chưa hiểu, phần nguy hiểm, phần thiếu test
```

---

## 2. Bộ 20 artifact (đánh số trong `.ai-understanding/`)

```text
00_index.md
01_project_intake.md
02_entrypoints_map.md
03_config_env_map.md
04_architecture_map.md
05_module_inventory.md
06_domain_model.md
07_data_model.md
08_api_contracts.md
09_flow_traces/            (folder, nhiều file)
10_state_and_lifecycle.md
11_dependency_graph.md
12_side_effects_map.md
13_error_handling_map.md
14_security_permission_map.md
15_test_map.md
16_observability_map.md
17_change_impact_map.md
18_risks_and_unknowns.md
19_glossary.md
20_understanding_scorecard.md
99_changes.md            (drift ledger — KHÔNG tính vào 20 artifact hiểu biết)
```

Mỗi artifact mở đầu bằng header:
```text
> built_at: <ISO 8601> · built_commit: <short-hash | n/a> · scope: <full | partial>
```

### 01_project_intake.md — project là gì, cho ai, chạy ở đâu
Mục: Project purpose · Main users/actors · Main capabilities · Runtime type (web/API/CLI/worker/library/monorepo/mobile/agent) · Tech stack (language/framework/db/queue/cache/auth/deploy) · How to run (install/dev/test/build/deploy) · Evidence.

### 02_entrypoints_map.md — hệ thống bắt đầu chạy từ đâu
Bảng: `| Entrypoint | Type | File | Trigger | Calls into |`. Liệt kê external entrypoints: API/web routes, CLI, webhook, queue consumer, cron, event listener. Evidence. (Không biết entrypoint = không biết module có bao giờ được gọi.)

### 03_config_env_map.md — phụ thuộc config/env nào
Bảng env: `| Env var | Used in | Purpose | Required? | Default | Risk |`. Config files (package.json, tsconfig, docker-compose, schema…). Runtime assumptions (cần DB? queue? API key? migrate trước boot?). Evidence.

### 04_architecture_map.md — hình dáng hệ thống
Observed style (layered/hexagonal/MVC/feature-based/event-driven/pipeline/plugin/monolith/modular monolith/microservices/mixed). Bảng layer: `| Layer | Responsibility | Example files | Allowed to depend on |`. Dependency direction. Architecture violations (controller gọi thẳng DB, domain import framework, circular dep…). Evidence.

### 05_module_inventory.md — từng module chịu trách nhiệm gì
Bảng: `| Module | Responsibility | Public API | Internal files | Depends on | Used by | Risk |`. Notes: module nào core domain / infra / chỉ adapter / quá to / không rõ responsibility.

### 06_domain_model.md — khái niệm nghiệp vụ (bắt buộc nếu có business logic)
Bảng concept: `| Concept | Meaning | Code representation | Important fields | Rules |`. Domain relationships. Domain invariants (luật không được phá). Evidence.

### 07_data_model.md — dữ liệu lưu thế nào
Storage (Postgres/Redis/S3/vector/fs/browser). Bảng entity: `| Entity/Table | Purpose | Important fields | Relations | Constraints |`. Migrations (ở đâu, áp dụng thế nào). Dangerous fields (status/role/balance/permission/parentId/deletedAt). Evidence.

### 08_api_contracts.md — các phần nói chuyện bằng contract gì
HTTP: `| Method | Path | Handler | Input | Output | Auth | Side effects |`. Internal service: `| Service | Method | Input | Output | Throws | Side effects |`. Event/Queue: `| Event | Producer | Consumer | Payload | Retry |`. External API (Stripe/OpenAI/GitHub/Slack/email…). Evidence.

### 09_flow_traces/ — chứng minh hiểu hành vi thật (QUAN TRỌNG NHẤT)
Mỗi flow một file, vd `09_flow_traces/create_task_flow.md`. Bắt buộc trace ≥ 4 flow: **1 happy path + 1 failure path + 1 side-effect path + 1 permission/security path**. Format từng flow:
```text
# Flow Trace: <tên>
## User-visible behavior
## Trigger (route/event/job)
## Step-by-step code path
  mỗi bước: File · Function · Input · việc gì xảy ra
  (request → validate → service/use case + business rules → repository/DB → response)
## Side effects (event? log? queue? cache invalidation?)
## Failure paths (invalid input, unauthorized, DB error, not found…)
## Tests covering this flow (test file + test còn thiếu)
## Evidence
```

### 10_state_and_lifecycle.md — object sống/đổi trạng thái/bị xóa thế nào
State machine cho object quan trọng: liệt kê states + bảng transition `| From | To | Trigger | Guard | Side effects |`. Lifecycle (created/updated/deleted/archived/read by). Illegal transitions (done→pending? failed→done?). Evidence.

### 11_dependency_graph.md — cái gì phụ thuộc cái gì
Module dependency graph (dạng `a → b → c`). External deps: `| Dependency | Used by | Purpose | Replaceable? | Risk |`. Circular dependencies (nếu có). High-risk deps (đổi là ảnh hưởng nhiều module). Evidence.

### 12_side_effects_map.md — code nào gây tác động thật
Bảng: `| Module | DB write | External API | Queue | Email | File write | Cache | Logs |`. Dangerous operations (xóa data, charge tiền, gửi email, gọi LLM tốn phí, đổi permission, start job, đổi status). Evidence.

### 13_error_handling_map.md — lỗi xử lý thế nào
Error types. Bảng error flow: `| Error source | Where thrown | Where caught | User response | Log? | Retry? |`. Failure behavior (fail open/closed? retry? dead-letter? rollback? partial success?). Evidence. (Production chết vì failure path, không phải happy path.)

### 14_security_permission_map.md — quyền, auth, data access
Authentication (identity tạo ở đâu, verify ở đâu, gắn current user ở đâu). Authorization (role model, permission check, ownership check, admin bypass). Sensitive operations: `| Operation | Required permission | Code location | Risk |`. Data isolation (user/workspace/tenant/admin boundary). Evidence.

### 15_test_map.md — hệ thống được test nào bảo vệ
Test types found. Bảng: `| Module | Test files | What is covered | What is missing | Risk |`. How to run tests (command, env, known failures). Critical untested paths (payment, permission, deletion, status transition, retry, LLM parsing). Evidence.

### 16_observability_map.md — quan sát hệ thống khi chạy thật
Logging (logger, log points quan trọng, redaction). Metrics (request/job duration, error count, LLM cost, payment failure, queue depth). Tracing (request/correlation/job/run ID). Debugging path (production lỗi thì xem đâu trước). Evidence.

### 17_change_impact_map.md — sửa một chỗ ảnh hưởng đâu
Vài change scenario điển hình của project (vd: thêm status mới, đổi LLM provider, thêm role) → liệt kê file/khu vực bị ảnh hưởng + risk. Bảng impact radius: `| Change | Low-level files | Domain impact | API impact | DB impact | Test impact | Risk |`. (Đây là cái phân biệt agent ĐỌC code với agent SỬA được code an toàn.)

### 18_risks_and_unknowns.md — trung thực về phần chưa hiểu
Unknowns: `| Unknown | Why it matters | How to verify | Priority |`. Risks: `| Risk | Area | Severity | Evidence |`. Assumptions đang giả định. Things not yet inspected (folder/module/job chưa đọc). (Agent giỏi nói "chắc phần này, chưa chắc phần kia, đây là cách kiểm chứng".)

### 19_glossary.md — thống nhất ngôn ngữ nội bộ
Bảng: `| Term | Meaning in this project | Code location | Notes |`. Chú ý từ dễ hiểu sai (Project vs git project, Run vs Task, Done vs Decomposed, User vs Member, Workspace vs Organization).

### 20_understanding_scorecard.md — tự chấm độ hiểu
Xem rubric mục 4. Ghi level đạt được (0–5) + lý do + evidence + checklist artifact bắt buộc của level đó.

### 99_changes.md — drift ledger (thay đổi chưa kịp vào artifact)
Sổ ghi thay đổi code CHƯA cập nhật vào artifact + **artifact nào cần update**. Không tính vào 20 artifact hiểu biết; là cơ chế giữ artifact khỏi stale mà không phải re-map toàn bộ. Template ở mục 5.

---

## 3. Template `00_index.md`

```text
# .ai-understanding — Index

> built_at: <ISO 8601> · built_commit: <short-hash | n/a>
> project: <project-path>
> understanding level (agent): <0–5> (xem 20_understanding_scorecard.md)

## Artifacts
| # | Artifact | Status | Ghi chú |
|---|---|---|---|
| 01 | project_intake | done/partial/todo | |
| 02 | entrypoints_map | | |
| … | … | | |
| 20 | understanding_scorecard | | |

## Cách tái dùng
overview/flow/why và các skill khác đọc folder này TRƯỚC khi quét code.
Đọc `99_changes.md` trước để biết artifact nào đang stale (có pending).
Chạy lại `/atlas` chỉ khi cần refresh (pending quá nhiều / thay đổi lớn).
```

---

## 4. Rubric scorecard (0–5) — tự chấm trung thực

Tạo đủ file KHÔNG tự động = level cao. Level dựa trên chất lượng evidence và độ phủ flow.

```text
[0] Không hiểu      — chỉ tóm tắt README, không evidence, không biết entrypoint.

[1] Bề mặt          — biết tech stack, folder chính, cách run; chưa trace được flow.
    Cần: 01_project_intake, 02_entrypoints_map, 05_module_inventory.

[2] Cấu trúc        — biết module phụ thuộc nhau thế nào, architecture style, data model chính.
    Cần thêm: 04_architecture_map, 11_dependency_graph, 07_data_model.

[3] Flow            — trace được hành vi thật end-to-end; biết happy + failure path + side effects.
    Cần thêm: 09_flow_traces/ (≥1 happy/failure/side-effect/permission),
              08_api_contracts, 12_side_effects_map, 13_error_handling_map, 14_security_permission_map.

[4] Sửa an toàn     — biết sửa chỗ nào ảnh hưởng đâu, test nào phải chạy, risk ở đâu.
    Cần thêm: 15_test_map, 17_change_impact_map, 18_risks_and_unknowns.

[5] Như maintainer  — hiểu trade-off kiến trúc, vì sao tổ chức như vậy, chỗ nào giữ/refactor/không đụng.
    Cần thêm (mở rộng): architecture_decision_notes, refactor_candidates, production_debug_map.
```

Ngưỡng dùng thực tế: trước khi cho **sửa code** cần ≥ level 3; trước **refactor** cần ≥ 4; trước **đổi architecture** cần 5.

Trong `20_understanding_scorecard.md` ghi: level tự chấm, checklist artifact đã đủ chưa, và 1 câu lý do + evidence cho mức đó.

---

## 5. Template `99_changes.md` (drift ledger)

`atlas` tạo file này lúc build (status `clean`); sau đó skill nào đổi code sẽ APPEND một dòng pending.

```text
# 99_changes — Pending changes & artifact drift

> last_synced_commit: <short-hash>   # artifact phản ánh đúng tới commit này
> current_commit: <short-hash>
> status: clean | dirty (N pending)

## Pending (chưa cập nhật vào artifact)
| # | Date | Change (commit/PR/mô tả) | Files đổi | Artifact cần update | Status |
|---|------|--------------------------|-----------|---------------------|--------|
| 1 | 2026-07-01 | feat: thêm status `archived` cho Task (abc1234) | task.model.ts, task.service.ts | 06_domain_model, 07_data_model, 10_state_and_lifecycle, 17_change_impact | pending |

## Artifact đang stale (tổng hợp nhanh)
- 10_state_and_lifecycle.md — thiếu transition cho `archived`

## Quy ước
- Mỗi lần đổi code → thêm một dòng pending. Cột "Artifact cần update" suy từ 17_change_impact_map.
- Cập nhật xong artifact → đổi status dòng đó thành `applied`, bump last_synced_commit = current_commit.
- Pending quá nhiều / thay đổi lớn → chạy `/atlas` refresh (full).

## Raw inbox (git hook tự ghi — agent phân loại lên Pending rồi xóa dòng ở đây)
| Date | Commit | Subject | Files |
|------|--------|---------|-------|
```

Ai ghi vào đây:
- `frame`/`triage` khi đổi code → append dòng **Pending** (đã map sang artifact).
- `atlas` khi targeted-update → đổi `applied` + bump `last_synced_commit`; và fold **Raw inbox** → Pending.
- Git hook (tùy chọn) → append **Raw inbox** dòng thô cho commit xảy ra ngoài agent; agent fold sau.

---

## 6. Git hook (tùy chọn) — bắt thay đổi ngoài agent

Script: `hooks/post-commit` (cùng thư mục skill). Chỉ ghi raw vào Raw inbox khi `.ai-understanding/99_changes.md` đã tồn tại; chưa `map` thì im lặng bỏ qua.

Cài per-repo:
```bash
cp <skill>/hooks/post-commit <project>/.git/hooks/post-commit
chmod +x <project>/.git/hooks/post-commit
```
Hạn chế: chỉ chạy khi `git commit` (sửa chưa commit không bắt); không tự map sang artifact (cần agent). Lần `atlas`/`explain`/`frame`/`triage` sau sẽ fold Raw inbox → Pending.
