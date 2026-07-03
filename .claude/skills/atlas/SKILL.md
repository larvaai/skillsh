---
name: atlas
description: 'Dựng & giữ bản đồ hiểu biết có bằng chứng cho TOÀN codebase, lưu vào .ai-understanding/ (20 artifact + index + scorecard + drift ledger) để mọi skill (explain/frame/triage/partner) tái dùng khỏi quét lại. Một lần đọc cả repo → xuất đủ artifact; sau đó chỉ cập nhật phần đổi. Dùng khi: "lập bản đồ", "atlas", "đọc hiểu toàn bộ", "map project", "build understanding", "hiểu code cũ/legacy", "dựng nền hiểu biết".'
---

# Atlas — Nền hiểu biết của codebase

Skill **nền** của bộ skill. Nó dựng `.ai-understanding/` — bản đồ hiểu biết có bằng chứng mà các skill khác ĐỌC để khỏi quét lại:
- `explain` đọc atlas để trả lời overview/flow/why mà không scan toàn repo.
- `frame` đọc atlas để bootstrap hiểu-biết trước khi cắt slice.
- `triage` trích `11_dependency_graph` / `12_side_effects_map` / `05_module_inventory` khi phán xử file.
- `partner` đọc `04_architecture_map` / `18_risks_and_unknowns` khi soi khả thi code cũ.

Phân vai với `explain`: **explain = hiểu CHO NGƯỜI (dạy, bám user-level L0–L8). atlas = hiểu CHO HỆ THỐNG (bằng chứng, bền vững, dùng chung).**

`atlas` **sở hữu** `.ai-understanding/` (gồm 20 artifact + `00_index` + `20_understanding_scorecard` + `99_changes` drift ledger). Nó chỉ ĐỌC code đích và KHÔNG đụng `user-state.json` / `agent-state.json` / `pipeline-state.json` / `triage.json` của skill khác.

## Mục tiêu

**Chứng minh đã hiểu hệ thống**, không tóm tắt file. Chỉ coi là hiểu khi trả lời được: (1) hệ thống giải quyết bài toán gì, (2) một hành vi thật đi từ đâu đến đâu trong code, (3) sửa một chỗ thì những phần nào có thể vỡ.

## Luật cứng (vi phạm là sai)

- **Một lần, đầy đủ.** Một lần chạy đọc toàn bộ codebase và sinh **đủ bộ 20 artifact (01–20)** + `00_index.md` trong cùng lượt (scorecard là artifact 20). Không chia nhỏ qua nhiều lượt — đã tốn token đọc cả repo thì xuất hết một thể.
- **Chạy một lần rồi tái dùng.** Nếu `.ai-understanding/` đã tồn tại → KHÔNG quét lại codebase. Đọc `99_changes.md` + `00_index.md`, báo đã build lúc nào / ở commit nào, rồi hỏi: *tái dùng* hay *refresh*. Mặc định tái dùng.
- **Read-only trên code đích.** `atlas` KHÔNG sửa bất kỳ file code nào của project. Chỉ ghi vào `<project-path>/.ai-understanding/`.
- **KHÔNG chép giá trị secret vào artifact (Đợt 3).** Gặp giá trị dạng secret — password / token / API key / connection string — kể cả hardcode trong file code thường: chỉ ghi **TÊN biến + vị trí** (`file:line`), TUYỆT ĐỐI không ghi giá trị. `.ai-understanding/` sống cạnh code khách và trôi theo commit → một giá trị lộ ở đây là lộ credential khách đứng tên mình. (Lớp path-based `permissions.deny` trong `settings.json` chặn Read `.env`/`*.pem`/`*.key`; luật này chặn nốt vector hardcode-trong-code mà guard theo path mù.)
- **Không claim nào thiếu evidence.** Mọi nhận định kèm: file path · symbol · dòng/đoạn code · suy luận · độ chắc chắn. Chưa đủ căn cứ → ghi vào `18_risks_and_unknowns.md`, KHÔNG ghi như fact. (Format ở `atlas-artifacts.md`.)
- **Tách facts khỏi assumptions.** Quan sát được ≠ giả định. Gắn nhãn rõ.
- **Trung thực về độ hiểu.** Tự chấm scorecard 0–5 theo bằng chứng thực tế, không cho điểm cao chỉ vì đã tạo đủ file.

## Bước 0 — Xác định project

Lấy đường dẫn project theo thứ tự ưu tiên:
1. Argument truyền vào (vd: `/atlas /Users/foo/my-app`).
2. Tên/đường dẫn nhắc trong tin nhắn.
3. `state/current.json` nếu có.
4. Nếu vẫn không rõ: hỏi *"Bạn muốn dựng atlas cho project nào?"*

Xác nhận folder tồn tại:
```bash
ls <project-path> 2>/dev/null | head -5 || echo "NOT_FOUND"
```
Nếu `NOT_FOUND`: báo lỗi và hỏi lại. Folder đích = `<project-path>/.ai-understanding/`.

## Bước 1 — Freshness check (tránh dựng lại vô ích)

```bash
ls <project-path>/.ai-understanding/ 2>/dev/null
```
- Đã có → đọc `99_changes.md` (`last_synced_commit` + pending) và `00_index.md`, so với `git -C <project-path> rev-parse --short HEAD 2>/dev/null`.
  - Khớp & không pending → báo "atlas còn tươi", DỪNG (không build lại).
  - Lệch commit hoặc có pending → ưu tiên **targeted update** (xem Drift); chỉ **full re-build** khi pending quá nhiều / thay đổi lớn / user yêu cầu.
  - Không git repo → hỏi user tái dùng/refresh.
- Chưa có → sang Bước 2 (full build).

## Bước 2 — Full build (một lượt)

1. **Đọc template.** Mở `atlas-artifacts.md` (cùng thư mục skill này): format evidence, thứ tự đọc 10 bước, 20 template, yêu cầu flow_traces, template index/ledger, rubric scorecard.
2. **Đọc codebase theo thứ tự đọc 10 bước** — đọc một lần, gom đủ dữ kiện cho cả 20 artifact (metadata → entrypoints → config → structure → domain → contracts → flows → side effects → tests → risks).
3. **Sinh đủ 20 artifact** vào `.ai-understanding/` theo template, mỗi claim kèm evidence. Trace tối thiểu 4 flow: ≥1 happy path, 1 failure path, 1 side-effect path, 1 permission/security path.
4. **Ghi `00_index.md`** (mục lục + trạng thái + `built_at` + `built_commit`), **`20_understanding_scorecard.md`** (tự chấm 0–5 + lý do + evidence), và **`99_changes.md`** (status `clean`, `last_synced_commit` = built_commit, chưa có pending).
5. **Báo cáo ngắn**: đã dựng ở đâu, scorecard mấy, 2–3 rủi ro lớn nhất, và nhắc các skill khác sẽ tái dùng folder này.

## Drift & cập nhật incremental (`99_changes.md`)

`atlas` sở hữu drift ledger; đây là cách giữ artifact khỏi stale mà không phải re-build toàn bộ.
- **Ai ghi drift:** `frame`/`triage` sau khi đụng code → APPEND một dòng `pending` (file đổi + artifact cần update, suy từ `17_change_impact_map`). Git hook (`hooks/post-commit`, tùy chọn) → append **Raw inbox** dòng thô cho commit ngoài agent.
- **`atlas` cập nhật:** đọc `99_changes.md`; với mỗi `pending` (và mỗi dòng Raw inbox đã fold) → sửa đúng các artifact liên quan, đổi status `applied`, rồi **bump `last_synced_commit`** = commit hiện tại. CHỈ `atlas` được bump.
- **Targeted update** thay cho full re-build khi pending còn ít; pending quá nhiều / thay đổi lớn → chạy lại full Bước 2.

## Bước 3 — Cập nhật state

Ghi `state/current.json` (cùng shape với explain/frame, full path):
```json
{ "project": "<project-path>", "updated_at": "<ISO 8601>" }
```
`atlas` KHÔNG ghi `user-state.json` (mức user là của `explain`). Nếu user mới, có thể gợi ý `/explain` để học lại codebase theo mức của họ.
