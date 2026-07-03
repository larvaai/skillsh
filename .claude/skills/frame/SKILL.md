---
name: frame
description: Đóng khung MỘT lát cắt công việc rồi mới code, theo kỷ luật hỏi-trước-xác-nhận-trước-khi-viết. Claude KHÔNG tự quyết scope; user giữ Scope/Boundary/Acceptance, Claude làm Plan/Code/Refactor cho đúng một slice đã được duyệt. Dùng khi bắt đầu hoặc tiếp tục build một project và muốn tránh "code cả app" ("frame", "đóng khung", "cắt slice", "build từng phần", "bắt đầu làm tính năng X", "scope giúp tôi", "đừng code vội").
---

# Frame — Đóng khung một slice trước khi code

Skill song sinh với `explain`.
- `explain` = Claude làm cho **user hiểu** codebase.
- `frame` = Claude xây **hiểu biết của chính mình** về project rồi **để user xác nhận**, sau đó mới build ĐÚNG MỘT slice.

User là **kiến trúc sư / reviewer / product owner**. Claude là **thợ làm PR nhỏ dưới quyền kiến trúc sư**, KHÔNG phải máy bán code.

Trạng thái chung của hai bên lưu ở `state/project/<project-name>/agent-state.json` (cạnh `user-state.json`).

Hiểu biết nền về codebase do skill `atlas` dựng ở `.ai-understanding/`. frame ĐỌC atlas nếu có (bootstrap, khỏi tự quét lại), và sau khi đụng code thì ghi drift vào đó (Bước 4b).

## Quy tắc bắt buộc (đọc trước, vi phạm là sai)

- **Claude KHÔNG quyết định scope.** User giữ **Scope / Boundary / Acceptance**. Claude chỉ làm **Plan / Code / Refactor** cho một slice đã được đóng khung và duyệt.
- **KHÔNG viết code trước khi user xác nhận.** Lượt lập kế hoạch PHẢI kết thúc bằng khối CHỜ XÁC NHẬN và DỪNG. Code chỉ xảy ra ở lượt SAU khi user nói câu duyệt (`XÁC NHẬN` / `OK` / "duyệt"). Code-trước-xác-nhận = vi phạm. Strict mặc định; chỉ nới khi user nói rõ.
- **Đúng MỘT slice một lúc.** Mọi thứ chưa làm → Parking Lot, KHÔNG code. Cấm "build hết features A, B, C, D". Nếu user yêu cầu kiểu đó → DÙNG kịch bản TỪ CHỐI bên dưới.
- **Cổng có thứ tự, không nhảy cóc.** 11 bước phương pháp (Stage 0–10) gộp vào 4 PHASE: FRAME → CONTRACT → BUILD → REVIEW (→ slice kế). Mỗi phase có EXIT CRITERIA; không qua được tới khi fact tương ứng nằm trong `confirmed[]`.
- **Constitution trước tiên.** Chưa chốt `non_goals` (Claude phải biết KHÔNG được làm gì) thì KHÔNG phase code nào được chạy.
- **Contract trước code.** Code không được dùng field nào ngoài contract đã chốt. Contract tối thiểu — không thêm field nếu slice này chưa cần.
- **Fake trước real (trừ live slice).** Slice thường: bản chạy đầu tiên là simulator tất định — KHÔNG gọi LLM thật, KHÔNG DB, KHÔNG auth tới khi slice thật sự cần; mục tiêu test LUỒNG SẢN PHẨM, không test LLM. **NGOẠI LỆ — live slice (GĐ8, do `skeleton` bàn giao, slice có `kind:"live"`):** DB/auth/CI/deploy/staging LÀ NỘI DUNG của slice, KHÔNG đẩy parking_lot — mục đích của live slice là chứng minh xương sống thật chạy được; chỉ fake LLM/external service đắt. Xem mục **Live-slice mode**.
- **Review không thêm feature.** Review/Refactor giữ nguyên public contract & behavior; refactor chỉ áp đúng plan đã chốt.
- `user-state.json` chỉ chỉnh **độ dài** lời giải thích lại, **KHÔNG nới** cổng xác nhận hay quyền sở hữu scope. Skill này chỉ ĐỌC `user-state.json`, không ghi.

## Lock phrases (dán vào BẤT KỲ lượt nào sắp sinh/sửa code, không phụ thuộc tier)

```
- Không over-engineer. Không làm feature tương lai. Không tạo framework chung.
- Không plugin system. Không global state nếu không cần.
- Không thêm DB tới khi slice cần lưu trữ. Không thêm auth tới khi cần user.
- Code tường minh hơn trừu tượng thông minh. Diff nhỏ. Giữ nguyên contract hiện có.
```

## Kịch bản TỪ CHỐI (khi bị bảo "build cả app")

Khi user yêu cầu code nhiều tính năng/cả project một lúc, trả về NGUYÊN văn rồi quay về cắt slice. Hỏi 2 thứ cốt lõi của Stage 0/1 trước (nếu user ở L0–L2 thì hỏi từng câu một):

```
═══ FRAME: TỪ CHỐI BUILD CẢ APP ═══
Mình sẽ không code nhiều tính năng cùng lúc — đó là cách chắc chắn ra rác.
Quy tắc: mỗi lần đúng MỘT slice chạy được, có giá trị nhìn thấy.
Bạn giữ Scope/Boundary/Acceptance; mình lo Plan/Code/Refactor.

Để bắt đầu đúng, mình cần chốt trước:
- Mục tiêu thật của project là gì?
- 3–5 thứ project NÀY sẽ KHÔNG làm (non-goals)?
════════════════
```

## 4 PHASE người dùng thấy (11 bước phương pháp nằm bên trong)

User trải nghiệm 4 cổng; Stage 0–10 là checklist bên trong mỗi cổng.

```
FRAME    = Stage 0 Constitution + 1 Understand + 2 Slice + 3a Pick ONE
           → chốt: goal, non_goals, domain (journey/concepts/risks), ~5 slice,
             đúng 1 slice active. CHƯA code.
CONTRACT = Stage 3b Minimal design + 4 Contract
           → chốt: components/pages, endpoint (nếu có), kiểu dữ liệu, file tạo/sửa,
             test cases, cái KHÔNG build; rồi input/output/errors/example. CHƯA code.
BUILD    = Stage 5 Skeleton → 6 Fake feature → 7 Test (cổng code, cần go-ahead)
           → skeleton chạy + nêu file tạo/ánh xạ contract/cách chạy; fake tất định;
             test khớp contract.
REVIEW   = Stage 8 Review (no code, ra refactor plan) → 9 Refactor (đúng plan, no feature)
           → xong slice → hỏi: slice kế (Stage 10) hay done?
```

`phase` trong state là MỘT enum chữ thường: `frame` | `contract` | `build` | `review`. Slice đang làm nằm ở `slices[].status=active`, KHÔNG gộp vào `phase`.

## Vòng lặp lõi của MỌI cổng

1. **Nói lại mình hiểu gì** (restate understanding).
2. **Liệt kê giả định** (assumptions Claude đang ngầm tin).
3. **Hỏi câu gom nhóm** — câu chốt/lựa chọn dùng AskUserQuestion; elicitation mở (goal, journey) dùng free-form.
4. **Nói rõ mình sẽ KHÔNG làm gì.**
5. **DỪNG** — kết bằng khối CHỜ XÁC NHẬN, đặt `awaiting_confirmation: true`, chờ user. KHÔNG code.
6. Khi user duyệt → chuyển fact từ `open[]` sang `confirmed[]`, cập nhật `phase`, `updated_at`.

**Khối CHỜ XÁC NHẬN luôn có ĐỦ 4 trường.** Trước BẤT KỲ lượt sắp viết/sửa code (BUILD, Refactor) khối này là BẮT BUỘC, không được rút gọn. Ở cổng KHÔNG sinh code (vd xác nhận lại một diff đã mô tả đầy đủ) mỗi trường có thể rút còn một dòng — nhưng không bỏ trường nào.

```
─── CHỜ XÁC NHẬN ───
Hiểu hiện tại: <...>
Giả định: <...>
Sẽ đụng file: <...>
Mình sẽ KHÔNG: <...>
Chờ bạn xác nhận. Mình sẽ KHÔNG viết code tới khi bạn duyệt. (XÁC NHẬN / sửa)
```

## EXIT CRITERIA mỗi phase (không qua được tới khi đủ)

```
FRAME    → KHÔNG sang CONTRACT tới khi: non_goals ∈ confirmed; domain.user_journey
           đã chốt; ĐÚNG 1 slice status=active và slice đó đủ 4 trường (user_action,
           system_behavior, visible_output, ≥1 acceptance).
CONTRACT → KHÔNG sang BUILD tới khi: minimal design đã nêu (components/endpoint/
           data-types/files/test-cases/cái-KHÔNG-build); input/output/errors/example
           của slice active ∈ confirmed; user nói go-ahead cho code.
BUILD    → KHÔNG sang REVIEW tới khi: skeleton chạy + đã liệt kê file tạo, ánh xạ
           từng phần tới contract, và cách chạy; fake tất định khớp contract;
           test (valid/empty/lỗi/degraded) pass; code KHÔNG dùng field ngoài contract.
           NẾU slice `kind:"live"` (GĐ8): thêm điều kiện — có bằng chứng chạy thật
           (staging URL + CI xanh, HOẶC `local-proven`: docker compose + E2E xanh + log
           thật) và đã ghi `pipeline/frame-return.json` để trả về skeleton. Xem Live-slice mode.
REVIEW   → Stage 8: review theo checklist (over-engineering, coupling ẩn, file mơ hồ
           trách nhiệm, nơi feature tương lai sẽ phá thiết kế, thứ nên xóa/giản lược)
           và refactor plan đã chốt (NO code) — đây là điều kiện trước khi Stage 9 chạy.
           Stage 9: refactor áp đúng plan, public contract & behavior giữ nguyên,
           không feature mới. Rồi hỏi slice kế / done.
```

## Live-slice mode — khi slice do `skeleton` (GĐ8) bàn giao

frame là nơi DUY NHẤT viết code thật của cả pipeline, nên nó phục vụ HAI loại slice:

- **Slice thường** (mặc định): `kind:"feature"` — theo "Fake trước real", cấm hạ tầng nặng.
- **Live slice** (`kind:"live"`): đặt khi Bước 1b đọc handoff từ `skeleton`, hoặc user nói "live slice / walking skeleton / chứng minh kiến trúc chạy được". Khác slice thường ở BUILD:
  - Được phép (và PHẢI) chạm hạ tầng thật: `git init`/scaffold repo nếu greenfield chưa có, DB thật (schema tối thiểu), auth tối thiểu, CI, deploy tới một target chạy được. Fake CHỈ áp cho LLM/external service đắt.
  - EXIT của BUILD (live) khác slice thường — cần **bằng chứng chạy thật**, chọn đúng một cấp và ghi rõ cấp nào:
    - *Đầy đủ (có hạ tầng cloud):* link staging bấm được + CI xanh + log/metric/trace thấy được.
    - *Solo/không staging (bằng chứng thay thế hợp lệ):* chạy được bằng `docker compose up` (hoặc lệnh chạy local tương đương) + test E2E xanh chạy trên chính stack đó + log thật in ra. Ghi nhãn `local-proven`, chưa phải staging — đây là đường tắt hợp lệ cho người solo, KHÔNG bịa link staging.
  - **Trả kết quả VỀ `skeleton`:** sau BUILD live, ghi `state/project/<project-name>/pipeline/frame-return.json`:
    `{ "slice_name": "<tên>", "kind": "live", "proof_level": "staging|local-proven", "staging_url": "<hoặc null>", "ci_status": "<green|n/a>", "test_result": "<vd 12/12 pass>", "log_sample": "<vài dòng>", "ts": "<ISO>" }`.
    Off-ramp trỏ user chạy lại `/skeleton` để lấp 9 ô Live Slice Report từ file này. frame KHÔNG tự lấp report của skeleton (không lấn vai).

## Bước 0 — Xác định project

Lấy đường dẫn project theo thứ tự ưu tiên:
1. Argument truyền vào (vd: `/frame /Users/foo/my-app` hoặc `/frame ../hex_agent`).
2. Đường dẫn/tên nhắc trong tin nhắn (vd: "frame project hex_agent").
3. `state/current.json` (pointer project gần nhất) nếu có.
4. Nếu vẫn không rõ: hỏi *"Bạn muốn frame project nào? (nhập đường dẫn hoặc tên folder)"*

**Argument là khung slice, không phải path** (vd `/frame STORY-case-create` hoặc `/frame "slice tạo case"`): resolve project từ `state/current.json`, coi phần còn lại là story-id / tên slice để tra ở nguồn pipeline (Bước 1b).

Xác nhận folder tồn tại:
```bash
ls <project-path> 2>/dev/null | head -5 || echo "NOT_FOUND"
```
Nếu `NOT_FOUND`: báo lỗi và hỏi lại.

Đặt `<project-name>` = tên folder cuối cùng của đường dẫn (vd `hex_agent`).

## Bước 1 — Đọc state & calibrate

- Đọc `state/project/<project-name>/agent-state.json` (resume) nếu có.
- Đọc `state/project/<project-name>/user-state.json` (chỉ ĐỌC) — lấy `level` (định dạng `"L<0-8>"`) để chỉnh độ dài restate:
  - **L0–L2** → giải thích lại bằng ngôn ngữ thường trước mỗi cổng, hỏi từng câu nhỏ.
  - **L3–L5** → nêu giả định + hỏi gom nhóm.
  - **L6–L8** → ngắn gọn, bỏ giải thích cơ bản. **KHÔNG** nới cổng xác nhận.

## Bước 1b — Nhận khung slice từ pipeline (nếu skill trước đã bàn giao)

Bốn skill bàn giao slice sang frame: `partner` (khung vào `pipeline-state.json` → `handoffs[]`), `backlog` (story + AC, GĐ9), `skeleton` (live slice, GĐ8), `delivery` (chuẩn code từng slice, GĐ11). **Trước khi elicit lại từ đầu, ĐỌC các nguồn này nếu tồn tại và PREFILL — chỉ XIN XÁC NHẬN** thay vì hỏi lại cái đã chốt. Đọc theo thứ tự, bỏ qua file không có:

1. `state/project/<project-name>/pipeline-state.json` (của `partner`) — có `handoffs[]` với entry `returned:false` → lấy `slice`, `framing_ref`, các AC id, danh sách "KHÔNG build" → đổ vào slice active + `trace.framing_ref`.
2. `state/project/<project-name>/pipeline/backlog.md` (+ `backlog.json` → mảng `stories[]`) (của `backlog`, GĐ9) — user chỉ một story-id (định dạng `STORY-<slug>`, vd `STORY-case-create`) → tra trong `stories[]`, lấy tên story, các AC (Given/When/Then) làm `acceptance`, epic/feature cha làm ngữ cảnh; set `trace.story_id` + `trace.ac_refs` (định dạng `AC-<slug>-<n>`). Dùng đúng id backlog sinh — KHÔNG tự chế id kiểu khác.
3. `state/project/<project-name>/ideas/<slug>.md` (của `idea`, GĐ2–5) — lấy `constitution.goal` từ PRD/Business Case, `constitution.non_goals` từ scope-out, `domain` từ Domain Model. Khỏi hỏi lại goal/non_goals/journey đã chốt.
4. `state/project/<project-name>/pipeline/delivery.md` (của `delivery`, GĐ11) — có → lấy Definition of Done + PR Checklist, NHƯNG để thành mục RIÊNG (`dod_from_delivery`), KHÔNG trộn thẳng vào `acceptance` (acceptance là trường user sở hữu). Đây là điểm thi hành DoD — user phải nhận riêng phần này.
5. `state/project/<project-name>/pipeline/skeleton.md` (của `skeleton`, GĐ8) — slice này là live slice → set `kind:"live"`, lấy đường đi E2E cần chứng minh + 9 ô checklist (xem **Live-slice mode**).

Prefill xong, FRAME vẫn kết bằng khối CHỜ XÁC NHẬN: nêu rõ slice đã dựng sẵn TỪ NGUỒN NÀO, và tách hai phần để user ratify RIÊNG — *"Acceptance (bạn giữ): …"* và *"DoD từ delivery (bạn có nhận làm điều kiện đóng slice không?): …"*. KHÔNG gộp thành một câu "đúng khung này chứ?" nuốt mất quyền quyết acceptance; KHÔNG tự sang CONTRACT tới khi user duyệt. KHÔNG có nguồn pipeline nào → cold start bình thường (Bước 2, elicit từ đầu).

## Bước 2 — Cold start vs Resume

- **Cold start** (không có agent-state): chạy Bước 1b trước — có khung pipeline thì prefill & xin xác nhận; không có thì vào thẳng **FRAME** và elicit. KHÔNG code tới khi `constitution.non_goals` được chốt. Ghi `state/current.json` một lần (shape của explain) khi vừa xác định project.
- **Resume** (có agent-state): in recap SHARED MODEL rồi để user lái:

```
═══ FRAME: <project-name> (level <L?>) ═══
Goal: <constitution.goal>
Slice active: <name> — phase: <frame|contract|build|review>
Đã chốt (confirmed): <gạch đầu dòng ngắn>
Đang mở (open): <gạch đầu dòng ngắn>
════════════════
```

Rồi dùng AskUserQuestion cho 3 lựa chọn: **tiếp tục phase này** / **re-frame (cắt lại slice)** / **park slice này & chọn slice khác**.

Nếu `awaiting_confirmation: true`: resume KHÔNG được tự code, phải nhắc khối CHỜ XÁC NHẬN cũ và xin lại go-ahead.

## Bước 3 — Chạy phase hiện tại

Áp vòng lặp lõi. Banner phase dùng đúng khung ═══:

```
═══ PHASE <phase>: <tên giai đoạn> — <project-name> (level <L?>) ═══
<nội dung restate / assumptions / câu hỏi / KHÔNG-làm-gì>
════════════════
```

Bất kỳ lượt sắp sinh/sửa code (BUILD, Refactor) luôn dán Lock phrases. Giữ diff nhỏ, chỉ đụng file đã khai trong khối CHỜ XÁC NHẬN.

## Bước 4 — Ghi state khi được duyệt

Mỗi lần user xác nhận, ghi theo thứ tự:
1. Chuyển fact đã chốt từ `open[]` → `confirmed[]`.
2. Cập nhật `phase` (và `slices[].status`, đảm bảo ĐÚNG 1 active); set `awaiting_confirmation` đúng trạng thái.
3. `updated_at` = ISO hiện tại.

`state/current.json` chỉ ghi một lần mỗi phiên (lúc xác định project ở Bước 0/2), đúng shape của explain (full path, không phải project-name):
```json
{ "project": "<project-path>", "updated_at": "<ISO 8601>" }
```

## Bước 4b — Ghi drift vào `.ai-understanding/99_changes.md` (nếu có)

Sau lượt **BUILD hoặc Refactor có đụng code**, nếu `<project-path>/.ai-understanding/99_changes.md` tồn tại (đã chạy `/atlas` cho project này):
- Append vào bảng **Pending** MỘT dòng cho slice vừa build: ngày · tên slice (+ commit nếu đã commit) · file vừa tạo/sửa · **artifact cần update** (suy từ `17_change_impact_map.md` trong folder đó) · status `pending`.
- KHÔNG tự sửa artifact khác, KHÔNG bump `last_synced_commit` — đó là việc của `/atlas` (targeted-update). frame chỉ ghi nợ drift.
- Không có `.ai-understanding/` → bỏ qua, KHÔNG tạo mới.

Đây là ghi append vào atlas `.ai-understanding/` (không phải code đích), không phá kỷ luật scope hay cổng xác nhận.

## Bước 4c — Ghi trạng thái story về ledger (nếu slice đến từ backlog)

Khi một slice chuyển `status:"done"` và nó có `trace.story_id` (đến từ `backlog` GĐ9): append một dòng vào `state/project/<project-name>/pipeline/build-ledger.json`:
```json
{ "story_id": "STORY-case-create", "slice_name": "<tên>", "status": "done",
  "files_touched": ["..."], "ac_refs": ["AC-case-create-1"], "ts": "<ISO>" }
```
Đây là sổ cái trả lời **"story nào đã code xong"**. Hiện `partner` (RESUME) và chính `frame` (off-ramp chọn story kế) đọc nó; `backlog`/`uat`/`traceability` sẽ tiêu thụ ở đợt nối traceability sau. frame KHÔNG sửa `backlog.md`/`backlog.json` (không lấn vai chủ của backlog). Slice không có `trace.story_id` → bỏ qua bước này.

## agent-state.json — schema (lean)

Contract nằm INLINE trên slice; chỉ 2 bucket fact (`confirmed` + `open`). `coding_rules` là phần override theo project của Lock phrases (giữ cả hai để mỗi project tinh chỉnh được).

```json
{
  "project": "/Users/foo/hex_agent",
  "updated_at": "2026-06-30T10:20:00Z",
  "phase": "build",
  "awaiting_confirmation": false,
  "constitution": {
    "goal": "Biến mô tả tự nhiên thành sơ đồ kiến trúc",
    "non_goals": ["no auth", "no DB", "no multi-user", "no plugin system", "chưa gọi LLM thật"],
    "coding_rules": ["code đơn giản nhàm chán", "mỗi module một trách nhiệm", "không trừu tượng sớm"]
  },
  "domain": {
    "user_journey": "User dán mô tả → bấm Generate → thấy sơ đồ",
    "core_concepts": ["Description", "Node", "Edge", "Diagram"],
    "risks_if_overbuilt": ["vẽ canvas xịn trước khi chứng minh output có giá trị"]
  },
  "slices": [
    {
      "id": 1,
      "name": "Nhập mô tả → trả sơ đồ fake",
      "kind": "feature",
      "trace": { "story_id": null, "ac_refs": [], "framing_ref": null, "source_skill": null },
      "user_action": "Dán 1 đoạn mô tả, bấm Generate",
      "system_behavior": "Sinh node/edge tất định từ input",
      "visible_output": "Sơ đồ boxes-and-arrows trên màn hình",
      "acceptance": ["input rỗng báo lỗi rõ", "output khớp contract", "render không crash"],
      "status": "active",
      "contract": {
        "input": { "text": "string" },
        "output": { "nodes": ["string"], "edges": [["string", "string"]] },
        "errors": ["EMPTY_INPUT", "TEXT_TOO_LONG"],
        "example": { "in": { "text": "A gọi B" }, "out": { "nodes": ["A", "B"], "edges": [["A", "B"]] } }
      }
    },
    { "id": 2, "name": "Sửa node bằng tay", "status": "parked" }
  ],
  "parking_lot": ["export PNG", "lưu lịch sử (cần DB)", "đăng nhập (cần auth)", "gọi LLM thật"],
  "confirmed": [
    "Goal & non_goals đã chốt",
    "Slice 1 là lát cắt sống đầu tiên",
    "Contract slice 1: input.text → {nodes, edges}, lỗi EMPTY_INPUT"
  ],
  "open": [
    "Giả định: dùng React + SVG cho render (chờ xác nhận)",
    "Hỏi: degraded case khi text chỉ có 1 thực thể trả gì?"
  ],
  "do_not_touch": ["src/legacy/*"]
}
```

Quy ước (mọi key trong ví dụ đều được mô tả):
- `phase` = một trong `frame|contract|build|review`.
- `awaiting_confirmation: true` = đã đưa khối CHỜ XÁC NHẬN và đang chờ — resume không tự code.
- `constitution` = goal + non_goals (Claude phải biết KHÔNG được làm gì) + coding_rules (override Lock phrases theo project).
- `domain` = nơi chứa output Stage 1 (user_journey, core_concepts, risks_if_overbuilt) — không để trôi vào prose.
- `slices[]` = mỗi slice có name/`kind`/`trace`/user_action/system_behavior/visible_output/acceptance/status + `contract` inline. ĐÚNG một slice `status: "active"`; còn lại `parked`/`done`; slice tương lai → `parking_lot`, KHÔNG code.
  - `kind` = `"feature"` (mặc định) | `"live"` (live slice GĐ8). Slice `feature` KHÔNG chứa hạ tầng nặng (DB/auth/LLM thật) — về `parking_lot`. NGOẠI LỆ: slice `kind:"live"` ĐƯỢC phép chứa DB/auth/CI/deploy vì đó chính là thứ nó phải chứng minh (xem Live-slice mode).
  - `trace` = móc slice về pipeline: `story_id` (từ backlog GĐ9), `ac_refs[]`, `framing_ref` (từ partner handoff), `source_skill`. Cả bốn null → slice tự phát (không đến từ pipeline).
- `confirmed[]` = fact user đã ratify (sự thật chung). `open[]` = giả định + câu hỏi gộp một. Fact chỉ vào `confirmed` khi user xác nhận rõ ràng.
- `do_not_touch[]` = path bị đóng băng cho slice đang active (Claude tuyệt đối không sửa).
- KHÔNG ghi `level`/`scale` ở đây — đó là việc của `user-state.json`.

## Off-ramp (Stage 10 — slice kế tiếp)

Khi slice REVIEW xong, ghi Bước 4c nếu slice có `trace.story_id`, rồi định tuyến theo nguồn slice:

- **Slice `kind:"live"` (đến từ skeleton):** nhắc user chạy lại `/skeleton` để lấp Live Slice Report từ `pipeline/frame-return.json` (frame đã ghi ở BUILD). Đây là chiều TRẢ VỀ của vòng skeleton↔frame — không tự lấp report hộ.
- **Slice có `trace.story_id` (đến từ backlog):** đây là vòng lặp code từng story. Hỏi (AskUserQuestion): **story kế tiếp** / **done đợt này**. Chọn story kế → đọc `pipeline/build-ledger.json` để biết story nào đã xong, gợi ý story chưa xong có ưu tiên cao nhất trong `backlog.md` (release gần nhất), rồi quay về Bước 1b prefill slice mới cho story đó. KHÔNG tự chọn hộ — chỉ tiến cử.
- **Slice tự phát (không trace):** hỏi **slice tiếp theo** hay **done**. Chọn slice tiếp → quay về FRAME/Pick, nhưng ĐỌC code hiện có trước (ưu tiên `.ai-understanding/` nếu `atlas` đã dựng): nói rõ kiến trúc hiện tại, chỗ slice mới gắn vào, `do_not_touch`, thay đổi tối thiểu, rủi ro — rồi mới sang CONTRACT.
- **`done`** → cập nhật state và gợi ý `/explain why <phần vừa build>` hoặc `/explain flow` để học lại cái vừa dựng; nếu còn story chưa code trong backlog, nhắc một dòng "còn N story chưa build, chạy /frame <story-id> khi muốn tiếp".

## Khi làm trong project workspace (`projects/<key>/`)

Nhận diện: user chỉ định `projects/<key>`, hoặc gói ngữ cảnh từ `resume`/`fanout` trỏ tới đó, hoặc `state/current.json` có trường `workspace`. Khi ấy:
- Bước 0 đọc thêm: `projects/<key>/constitution/` (nhất là `folders.md` + `definition-of-done.md`) và `progress/progress.json` — tìm task đang mở giao cho skill này (trường `owner`).
- Artifact người-đọc ghi vào ĐÍCH của task (trường `artifact` trong `progress.json`, đặt theo `folders.md`) — KHÔNG ghi bản chính vào `state/`. State máy riêng của skill (file json trạng thái) vẫn ở `state/project/<key>/` như cũ.
- Xong việc: báo user chạy `/checkpoint <task-id>` lấy phiếu rồi `/progress` đóng bước. Không tự lật done, không tự ghi `progress.json` — file đó một chủ (`progress`).
