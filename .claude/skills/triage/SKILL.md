---
name: triage
description: Đọc ĐÚNG MỘT file qua một lăng kính cố định rồi ra QUYẾT ĐỊNH về số phận của nó — giữ / sửa nhỏ / chuyển / xoá / rewrite / archive — kèm lý do và rủi ro khi tác động. Read-only mặc định; mọi thay đổi code (trừ sửa-nhỏ-cô-lập) bàn giao sang `frame`. Dùng khi người dùng chỉ vào một file và hỏi giữ/xoá/sửa/viết-lại ("file này còn dùng không", "có nên bỏ file này", "file này nên sửa hay viết lại", "sửa nó có ảnh hưởng ai", "triage file X", "xét file này").
---

# Triage — Đọc một file, ra một quyết định

Một skill trong bộ skill. Các skill kia làm việc khác:
- `atlas` = dựng **nền hiểu biết** chung của codebase (sở hữu `.ai-understanding/`).
- `explain` = làm **user hiểu** code (sở hữu `user-state.json`).
- `frame` = đóng khung & build **một slice**, kỷ luật hỏi-trước-code (sở hữu `agent-state.json`).
- `partner` = chạy trọn **chuỗi giá trị** idea→release (sở hữu `pipeline-state.json`).
- `triage` = đọc **một file** rồi quyết định **số phận** nó. Chẩn đoán, không thi công.

Mantra: **"Đừng sửa dòng code, hãy sửa responsibility. Đọc file không phải để nhớ hết, mà để biết: nó là gì, nó hứa gì, nó ảnh hưởng ai, sửa nó có nguy hiểm không."**

Ranh giới với `explain` (chế độ why): `explain why` giải thích **lý do nghiệp vụ** của một phần CHO USER hiểu (dạy học). `triage` quyết định **số phận một FILE** để dọn/sửa (ra verdict). User muốn *hiểu* file để làm gì → trỏ `/explain`. User hỏi *giữ/sửa/xoá* → đây là `triage`.

## Quy tắc bắt buộc (đọc trước, vi phạm là sai)

- **Mỗi phiên kết thúc bằng ĐÚNG MỘT verdict** trong `{giữ | sửa nhỏ | chuyển | xoá | rewrite | archive | cần đọc thêm}` — 6 verdict gốc + `cần đọc thêm` là verdict-an-toàn khi chưa đủ căn cứ (nêu rõ thiếu gì). Mỗi verdict kèm **một câu lý do** + **một câu rủi ro khi hành động**. Không bao giờ để "kết quả mở".
- **READ-ONLY mặc định.** `triage` chẩn đoán + quyết định; **KHÔNG** tự rewrite domain/contract/API/DB. Hành động inline DUY NHẤT được phép là một fix nhỏ cô lập (xem fix-now). Mọi thứ khác → **BÀN GIAO sang `/frame`**, không tự code, không mô tả lại 4 phase của `frame` (chỉ trỏ sang).
- **Một file một verdict.** Mỗi file một khối ═══ TRIAGE ═══, không gộp.
- **Gate trước khi đụng logic một method.** KHÔNG khuyến nghị sửa logic tới khi trả lời được hết: method phục vụ use case nào? ai gọi? nó gọi ai? input/output? đổi state nào? side effect gì? sửa xong behavior nào đổi? Chưa đủ → verdict = `cần đọc thêm`.
- **Gate trước verdict `xoá` một biến/field** (dạng câu hỏi điều tra, phải trả lời cả hai chiều): set ở đâu? read ở đâu? ai consume? **có trong public API không? có trong DB schema không? có thuộc domain core không?** + **live slice active có cần không** (đọc `agent-state.json`). Chỉ `xoá` khi các câu API/DB/domain/live-slice đều là KHÔNG. Không xoá vì "chưa hiểu", không giữ vì "biết đâu sau cần".
- **`do_not_touch` đọc từ `agent-state.json`** (chỉ `frame` có field này). File/path trong `do_not_touch` chỉ được verdict `giữ` hoặc `cần đọc thêm` — không bao giờ xoá/chuyển/rewrite, và **không fix inline dù chỉ là typo**. Phạm vi/non-goals của `partner` đọc từ `pipeline-state.json.decisions[]` (entry non-scope đã `confirmed`) + `feasibility` — **không** có field `do_not_touch` ở file này.
- **Trung thực về caller/callee.** Map bằng grep read-only; gắn nhãn độ tin cậy (`chắc chắn` | `một phần` | `có thể sót` | `KHÔNG tìm thấy`). KHÔNG suy "0 grep hit ⇒ chết ⇒ xoá". Caller chưa rõ → hạ verdict mạnh (xoá/rewrite) xuống `cần đọc thêm`.
- **Chỉ ĐỌC state file của sibling** (user/agent/pipeline-state); TUYỆT ĐỐI không ghi đè. `triage` chỉ ghi `triage.json` của riêng nó. **Ngoại lệ duy nhất:** được APPEND (chỉ thêm dòng, không sửa/xoá dòng cũ) vào `99_changes.md` của `atlas` khi fix-now đụng code — đóng góp drift vào nền chung, không phải state riêng của sibling. **Không** cập nhật `state/current.json` (chỉ đọc nó để dò project).
- **Độ sâu output bám `user-state.json.level`** (L0–L2 ngôn ngữ thường, ít tên file/hàm; L6–L8 gọn, kỹ thuật) — NHƯNG level **KHÔNG** nới các gate xoá/sửa ở trên.

## Reading order — engine chẩn đoán (= thứ tự field output)

Vừa là **cách đọc nội bộ**, vừa là **thứ tự field trong khối output**. Đi đủ = chứng minh đã đọc xong; thiếu field nào = chưa được nhảy tới DECISION.

```
1 Layer          → File thuộc tầng nào? có logic SAI TẦNG không?
2 Responsibility → Chịu trách nhiệm gì? (một câu)
3 Public Contract → Export chính / input / output / enum-state / business rule
4 Caller         → Ai gọi nó? (grep, + nhãn độ tin cậy)
5 Callee         → Nó gọi ai? (dependency có sai tầng không?)
6 State          → Đổi state/field nào?
7 Side Effect    → I/O, DB, network, mutation, thứ tự phụ thuộc?
8 Internal Logic → Logic chạy sao? (theo frame method bên dưới, KHÔNG dòng-1→2→3→sửa)
8b Core/Detail   → Thứ định đụng là CORE (responsibility/contract) hay CHI TIẾT vụn?
9 Risk           → Sửa/xoá/chuyển phá API/DB/UI/live-slice ở đâu?
10 DECISION      → giữ | sửa nhỏ | chuyển | xoá | rewrite | archive | cần đọc thêm
```

**Đây KHÔNG phải "30 giây":** đường đầy đủ có grep caller + đọc state — chỉ chạy khi cần (xem Bước 3 tiered). Đường nhanh cho `giữ` mới là vài giây.

## Layer classification + mùi SAI TẦNG (bắt buộc nêu trong output)

Tầng: `Domain · Application/Use Case · Infrastructure · Interface/Controller/API · UI · Config · Test · Util`.

Mùi sai tầng (tín hiệu chính dẫn tới `chuyển`/`rewrite`):
- UI chứa business logic = sai → `chuyển` logic ra use case.
- Use case gọi thẳng OpenAI/HTTP/SDK = hơi dính infra → `chuyển` ra infra.
- Domain import React/Prisma/axios = **sai nặng** → `rewrite`/`chuyển`.

## Nhớ gì vs bỏ qua

- **NHỚ:** Export chính · Input · Output · Contract · Enum/State · Business Rule · Dependency · Side Effect.
- **BỎ QUA:** biến tạm, helper nhỏ, format string, mapping đơn giản, className UI.

## Frame cho mỗi class/function/method (cách đọc Internal Logic)

`Purpose → Input → Validation → Load Data → Decision → State Change → Dependency Call → Side Effect → Output → Error.` KHÔNG đọc kiểu "dòng 1→2→3→thấy kỳ→sửa luôn".

## Phân loại biến/field + khi nào xoá

| Loại field | Xử lý |
|---|---|
| Core Domain | giữ |
| Contract/API | cực kỳ cẩn thận (đụng = phá hợp đồng) |
| UI State (nằm trong domain) | chuyển về UI |
| Infrastructure (nằm trong use case) | chuyển về infra |
| Integration | giữ nếu module còn scope |
| Dead | xoá có kiểm soát |
| Temporary | không cần nhớ lâu, bỏ qua |

Verdict `xoá` field CHỈ khi qua hết gate xoá ở trên + live slice không cần.

## Fix-now (inline) vs BÀN-GIAO → frame

**Fix inline NGAY** — chỉ khi rơi đúng vào danh sách lỗi nhỏ cô lập VÀ file KHÔNG trong `do_not_touch` VÀ không ngoài scope `partner`:
- typo · sai tên biến · thiếu `return` · điều kiện obvious · format sai · validation nhỏ · type sai rõ ràng.

**NGAY CẢ typo:** nếu file ∈ `do_not_touch` hoặc ngoài scope `partner` → KHÔNG inline, verdict = `giữ` + ghi chú lý do đóng băng.

**KHÔNG fix inline — BÀN GIAO sang `/frame`** khi đụng bất kỳ thứ nào: business logic · state transition · public API · DB schema · domain model · dependency flow · module boundary. **`xoá` field/dead code LUÔN là bàn giao** (dù đã qua gate xoá) — không bao giờ tự xoá inline.

Lằn ranh **đóng**: 7 case trên được inline, **mọi thứ khác** → `frame`. Một "sửa nhỏ" hóa ra chạm business logic/contract → tự động chuyển thành BÀN GIAO.

## Trigger Refactor / Rewrite / Archive

- **Refactor** (code xấu + model ĐÚNG): logic/flow/domain đúng nhưng code rối, method dài, tên xấu, duplication, sai vị trí nhẹ. Công thức: behavior giữ nguyên, structure sạch hơn, test/typecheck pass. → BÀN GIAO `frame`.
- **Rewrite** (logic đúng + boundary SAI): ý tưởng đúng nhưng boundary sai, logic sai tầng, phụ thuộc chéo, state sai chỗ, thêm feature mới rất khó. Công thức: Freeze old → Extract lesson → Pick live slice → Design minimal domain → Build clean skeleton → Port logic tốt → Bỏ phần xấu. → BÀN GIAO `frame`, từng slice.
- **Archive** (model SAI gốc): không hiểu core flow, domain model sai gốc, entity sai hết, không có live slice rõ (kiểm `pipeline-state.json`), AI generate quá nhiều, càng sửa càng loạn. Vẫn giữ: `LESSONS.md`, `REWRITE_NOTES.md`, ý tưởng đúng. **Một file xấu KHÔNG đủ căn cứ archive cả module** — phạm vi rộng hơn file → trỏ `/partner`.

## Bảng quyết định nhanh

```
Code xấu + model đúng             → Refactor (→ frame)
Logic đúng + boundary sai         → Rewrite từng slice (→ frame)
Model sai gốc                     → Archive + làm lại
Biến phục vụ module đã bỏ         → Xoá có kiểm soát (→ frame)
Biến domain core                  → Giữ
Biến UI nằm trong domain          → chuyển ra UI (→ frame)
Biến infra nằm trong use case     → chuyển ra infra (→ frame)
Method chưa rõ caller/side effect → cần đọc thêm (CHƯA sửa)
Method sai rõ so với contract     → đụng contract → BÀN GIAO frame (+ test)
```

## Bước 0 — Xác định FILE và PROJECT

`triage` cần CẢ hai: **file** để đọc, **project** để map state + grep caller/callee.

**FILE** theo thứ tự ưu tiên:
1. Argument (`/triage src/user/UserService.ts`).
2. Đường dẫn/tên file nhắc trong tin nhắn ("xét file UserService").
3. Không rõ → hỏi *"Bạn muốn triage file nào? (nhập đường dẫn file)"*.

Xác nhận file tồn tại:
```bash
ls <file-path> 2>/dev/null | head -1 || echo "NOT_FOUND"
```
`NOT_FOUND` → báo lỗi và hỏi lại.

**PROJECT** (để tìm state sibling): ưu tiên git root / folder chứa của FILE → tên nhắc trong tin → `state/current.json`. Đặt `<project-name>` = tên folder cuối của project path. **Nếu** `<project-name>` từ file KHÔNG có thư mục `state/project/<project-name>/` nhưng `current.json` trỏ tới một project CÓ chứa file này → ưu tiên project-name của `current.json` (để tìm được state sibling). Nếu file nằm ngoài project trong `current.json` → cảnh báo lệch.

## Bước 1 — Đọc state sibling (chỉ ĐỌC) để calibrate & gate

- `user-state.json` → lấy `level` (`"L<0-8>"`) chỉnh **độ dài** output. Không hỏi lại mức.
- `agent-state.json` (của `frame`) → `slices[]` nơi `status=="active"`; soi `contract` inline (input/output/errors/example) + `acceptance` của slice đó; lấy `do_not_touch[]`. Một field "live slice cần" ⇔ nó xuất hiện trong contract đó hoặc được slice active tham chiếu.
- `pipeline-state.json` (của `partner`) → scope/non-goals từ `decisions[]` (entry non-scope đã `confirmed`) + `feasibility`.
- `.ai-understanding/` (của `atlas`, nếu có) → đọc `11_dependency_graph.md` + `12_side_effects_map.md` + `05_module_inventory.md` để bổ trợ map caller/callee và đánh giá rủi ro (vẫn grep để xác minh, không tin tuyệt đối).

**Fail mềm (không tê liệt):** file/key vắng → coi như không ràng buộc, nêu rõ "không xác minh được live slice / do_not_touch", và **vẫn chẩn đoán dựa trên grep + scope partner**. Chỉ hạ verdict mạnh (xoá/rewrite) xuống `cần đọc thêm` khi **bằng chứng caller (grep) yếu**, không phải chỉ vì thiếu agent-state. (Đây là ca brownfield-cleanup chưa từng chạy `frame` — đừng để nó vô dụng.)

## Bước 2 — Map caller/callee (grep, trung thực)

- **Callee** (nó gọi ai): đọc thẳng trong file → tin cậy cao.
- **Caller** (ai gọi nó): grep tên export trên project (lặp `--include` từng đuôi, KHÔNG dùng brace `{a,b}`):
```bash
grep -rn "<tên-export>" <project-path> \
  --include='*.ts' --include='*.tsx' --include='*.js' --include='*.jsx' \
  --include='*.py' --include='*.go' 2>/dev/null | head -30
```
Gắn nhãn: `chắc chắn` | `một phần` | `có thể sót` (re-export, DI container, dynamic import, route bằng string, reflection) | `KHÔNG tìm thấy`. Không khẳng định "không ai gọi" từ một grep rỗng.

## Bước 3 — Phát khối ═══ TRIAGE ═══ (tiered)

Pass rẻ trước: đọc Layer + Responsibility + lướt Contract.

- **Nếu rõ là `giữ`** (đúng tầng, không mùi sai, không dấu chết/dup) → phát **dạng ngắn**, DỪNG. Không grep caller, không đọc agent/pipeline-state, không ghi gì:
```
═══ TRIAGE: <tên-file> (<layer>) ═══
Trách nhiệm: <một câu>
QUYẾT ĐỊNH: giữ — <lý do một câu>
════════════════
```

- **Nếu có dấu cần đổi** (mùi sai tầng / nghi chết / dup / user hỏi xoá-sửa-viết-lại) → chạy **engine đầy đủ** (grep caller + đọc state) rồi phát **dạng đầy đủ**:
```
═══ TRIAGE: <tên-file> — <project-name> (level <L?>) ═══

Tầng: <Domain|Application|Infra|Interface/API|UI|Config|Test|Util> [+ ⚠ SAI TẦNG: <gì>]
Trách nhiệm: <một câu>
Contract: <export chính / input / output / enum-state>
Caller: <ai gọi> — <chắc chắn|một phần|có thể sót|KHÔNG tìm thấy>
Callee: <nó gọi ai / dependency chính> [+ dependency sai tầng?]
State: <đổi field/state nào / không đổi> [+ phân loại field load-bearing]
Side effect: <I/O, DB, network, mutation / không>
Core/Detail: <thứ định đụng là core hay chi tiết>
Rủi ro khi tác động: <thấp|vừa|cao> — <cái gì vỡ, một câu cụ thể>
Scope-check: <in do_not_touch? trong slice active? ngoài scope partner? / không xác minh được>

QUYẾT ĐỊNH: <giữ | sửa nhỏ | chuyển | xoá | rewrite | archive | cần đọc thêm> — <một câu lý do>
Bước kế: <inline-fix mô tả diff nhỏ | → /frame <khung slice> | → /explain về <phần> | cần đọc thêm <gì>>
════════════════
```

## Bước 4 — Hành động theo verdict

- **giữ** → phát khối, dừng. Không hỏi, không ghi state.
- **sửa nhỏ (inline)** → chỉ khi thuộc fix-now + không trong do_not_touch + trong scope. Mô tả diff nhỏ rồi áp. Không ghi `triage.json`. Nếu `<project>/.ai-understanding/99_changes.md` tồn tại → append MỘT dòng `pending` (file vừa sửa + artifact cần update); KHÔNG bump `last_synced_commit` (việc của `/atlas`); folder không có thì bỏ qua.
- **chuyển / xoá / rewrite / archive / sửa-không-nhỏ** → KHÔNG tự code. Phát khối BÀN GIAO (truyền sẵn khung cho `frame`), rồi dùng **AskUserQuestion** một cổng xác nhận 3 lối:
  - **bàn giao `/frame`** → append 1 dòng `triage.json`.
  - **chỉ ghi nhận** → append 1 dòng `triage.json`.
  - **xem `/explain`** → KHÔNG ghi.

```
═══ BÀN GIAO → frame: <tên-file> ═══
Verdict: <chuyển|xoá|rewrite|archive>   Tầng: <…>
Lý do: <…>                              Rủi ro: <…>
Caller/Callee đã map: <tóm tắt + độ tin cậy>
KHÔNG đụng: <do_not_touch nếu có>
→ Bạn chạy: /frame <khung slice>. (frame giữ kỷ luật hỏi-trước-code, mình không code thay.)
════════════════
```

## State — read-only mặc định + log tùy chọn (lean)

`triage` **không sở hữu state bắt buộc**. Verdict `giữ`/`sửa nhỏ`/`cần đọc thêm` hoặc đọc-rồi-thôi → **không ghi gì**. KHÔNG cập nhật `state/current.json`. KHÔNG ghi đè ba file sibling.

CHỈ khi user chọn **bàn giao** hoặc **ghi nhận** cho một verdict non-trivial (`xoá`/`chuyển`/`rewrite`/`archive`) → append ĐÚNG MỘT dòng vào `state/project/<project-name>/triage.json` (append-only, để cleanup sweep truy vết và `partner` tiêu thụ).

```json
[
  { "file": "src/ui/LegacyChart.tsx", "layer": "UI", "decision": "xoá", "reason": "module dashboard cũ ngoài scope (pipeline non-goals); grep 0 caller (chắc chắn), không trong API/DB, slice active không cần", "at": "2026-06-30T10:40:00Z" },
  { "file": "src/usecase/billing.ts", "layer": "Application", "decision": "chuyển", "reason": "gọi thẳng Stripe SDK (infra dính use case); tách ra adapter, behavior giữ nguyên", "at": "2026-06-30T10:42:00Z" }
]
```
