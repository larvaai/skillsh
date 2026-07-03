---
name: delivery
description: Chuẩn hoá CÁCH giao hàng an toàn cho MỌI team — sinh Delivery Standards (repo/branch/coding standard, CI/CD, test pyramid, env, secret, migration, observability, incident) + Definition of Done + PR Checklist một lần, áp cho toàn dự án. Là GĐ11 pipeline Idea→Operate (BUILD), nhận Module Map + Contract từ `modules` (GĐ10), bàn giao sang `uat` (GĐ12). ĐẶT CHUẨN, KHÔNG code hộ — code từng slice là /frame. Dùng khi "chốt chuẩn delivery", "định nghĩa Done", "DoD", "PR checklist", "CI/CD & test strategy", "trước khi các team bắt đầu build cần thống nhất gì", "làm sao giao hàng an toàn", "delivery standards".
---

# Delivery — Chuẩn giao hàng an toàn (GĐ11: Delivery Standards + DoD + PR Checklist)

`delivery` là **GĐ11 (BUILD)** của pipeline Idea→Operate. Nó trả lời đúng câu hỏi lãnh đạo hay hỏi nhất khi đội bắt đầu code hàng loạt: *"Làm sao biết một thứ đã XONG và giao được an toàn?"* — bằng một khối **Definition of Done** đọc trong 30 giây, rồi mới tới chuẩn kỹ thuật cho dev. Nó sinh đúng ba artifact: **Delivery Standards + Definition of Done + PR Checklist**, chốt một lần, áp cho mọi team.

Ranh giới một câu: **`delivery` quyết HOW SAFELY — giao hàng an toàn thế nào — chứ không quyết build cái gì (backlog) hay build ra sao trong từng slice (`frame`).**

Phân vai — đứng đúng chỗ, không lấn:
- `modules` (GĐ10, skill trước) = chia module + Module Contract + owner → là **đầu vào** của `delivery`. Không vẽ lại module.
- `frame` = code THẬT từng slice theo chuẩn này. `delivery` KHÔNG code hộ, không chọn scope slice, không tự sinh migration script — chỉ đặt luật để mọi slice của `frame` đi qua cùng một cổng.
- `review` = đào gap/edge case/permission sâu của một luồng. `delivery` chỉ đặt luật test/PR, không tự soi bug.
- `uat` (GĐ12, **skill kế tiếp**) = dùng chuẩn test ở đây để chứng minh hệ chạy đúng (mapping AC→test→result, UAT + security sign-off).
- `partner` = điều phối trọn pipeline; `delivery` chạy độc lập được HOẶC do `partner` gọi.

Playbook gốc (template + ví dụ đầy đủ): `quy-trinh-idea-to-operate.md` ở gốc project, mục **"## Giai đoạn 11 — Delivery / Implementation (BUILD)"**. `delivery` bám đúng 3 artifact và các ô của giai đoạn đó — việc lớn/nhiều team thì mở file gốc lấy template đầy đủ; không tự thêm mục.

## Luật cứng

- **Hợp đồng đọc-được 3 tầng (LÝ DO skill tồn tại).** Người đọc là đội DOANH NGHIỆP KHÁCH HÀNG — CTO, business, dev — người NGOÀI, không có kiến thức nội bộ. Mọi artifact: MỞ bằng **Góc nhìn lãnh đạo** (đúng 1–3 thứ CEO/CTO nhìn để biết giao hàng có on-track — ở đây là khối Definition of Done + 4 chỉ số DORA), ngôn ngữ nghiệp vụ, không jargon; RỒI mới tới chi tiết kỹ thuật đủ để DEV hành động. 1 trang, scan 2–3 phút.
- **Đủ-là-đủ.** Độ sâu tỉ lệ RỦI RO/ẨN SỐ, không theo vị trí trong luồng. Team quen stack cũ / 1–2 module → Standards vài dòng mỗi mục. Nhiều team / hệ quan trọng (thanh toán, dữ liệu nhạy cảm) / stack mới → đầy đủ mọi mục (secret/migration/rollback/observability). KHÔNG bao giờ bỏ một mục chuẩn — chỉ rút gọn độ sâu.
- **Không lấn vai.** Không code slice (→ `frame`). Không đào bug/edge case (→ `review`). Không vẽ lại module (→ `modules`). Không chọn stack/framework mới (→ GĐ7 `stack`). Không viết test-result / sign-off (→ `uat`). `delivery` chỉ đặt CHUẨN + CỔNG.
- **Mỗi quyết định lớn ghi LÝ DO + phương án đã loại.** Vd "trunk-based vì team nhỏ, deploy nhiều lần/ngày; loại git-flow vì nhánh dài gây merge đau." Để sau audit được.
- **Cấm câu phủ định cứng khi phản biện** (kế thừa `partner`): không "không thể", "sai rồi", "không làm được". Luôn kèm một lối đi tiếp.
- **DoD là luật, không phải gợi ý.** Item không đạt Definition of Done → không release. Đây là cổng cứng của cả GĐ11.
- **KHÔNG tự ghi artifact vào repo code** trừ khi user đồng ý (theo `idea`). Mặc định ghi vùng state của skill. Chuẩn delivery có thể muốn nằm trong repo (vd `CONTRIBUTING.md`, `.github/`, `DELIVERY.md`) — nhưng HỎI user trước khi đặt vào repo đích. Chỉ greenfield mới ghi thẳng.

## Đầu vào — đọc trước khi hỏi

- **Module Map + Module Contract (GĐ10, `modules`)** — nguồn chính. `state/project/<project-name>/pipeline/modules.md`. Lấy: có mấy module, mỗi module owner là ai, data/event mỗi module sở hữu, Public API/contract nào cần contract-test, event nào cross-module. Chuẩn test + PR checklist phải phủ đúng các ranh giới này (ô "update API contract?" và "ảnh hưởng module khác?" nối thẳng vào Contract GĐ10).
- **`state/current.json`** — project hiện hành.
- **Tech Decision Matrix (GĐ7 `stack`) / Live Slice Report (GĐ8 `skeleton`)** nếu có — đọc để lấy CI/CD + test pyramid ĐÃ dựng, không bịa lại chuẩn mới.
- **`.ai-understanding/`** (atlas, nếu brownfield) — CI/CD, test, convention ĐÃ tồn tại trong code; chuẩn mới phải KHỚP repo thật, không đặt luật trên giấy mâu thuẫn thực tế.
- **`state/project/<project-name>/user-state.json`** (của `explain`, chỉ ĐỌC) — `level` để hiệu chỉnh độ dài diễn giải; không hỏi lại mức.

Không có artifact GĐ10 trong state → nếu user ĐÃ đưa Module Map + Module Contract trong prompt/dán nội dung/trỏ file → chạy được, KÈM ⚠️ cảnh báo theo mục "Đầu vào ngoài state" ngay dưới; nếu KHÔNG có gì → mới gợi ý chạy `/modules` trước (hoặc đưa tay contract vào) và ghi rõ đây là giả định cần `modules` xác nhận. Dù nguồn nào, **không bịa module** user chưa đưa.

## Đầu vào ngoài state (nới — nhận prompt/file thay cho artifact GĐ trước)

Không có Module Map + Module Contract trong state VẪN chạy được nếu user mô tả trực tiếp trong prompt, dán nội dung, hoặc trỏ một file ngoài. Thứ tự ưu tiên: (1) đọc state pipeline; (2) không có thì nhận Module Map + Module Contract từ prompt/file user đưa; (3) vẫn không có gì thì mới gợi ý chạy /modules.

Khi chạy bằng nguồn NGOÀI (không phải Module Map + Module Contract của GĐ10 đã qua cổng), in NGUYÊN block cảnh báo này NGAY TRƯỚC khi làm, rồi VẪN tiếp tục — đây là cảnh báo, KHÔNG phải chặn:

```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Module Map + Module Contract" lấy từ prompt/file bạn đưa, CHƯA qua cổng GĐ10 (skill /modules).
- Rủi ro: (1) chưa truy vết ngược được về pipeline; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /modules trước để có "Module Map + Module Contract" đã qua cổng.
```

Nếu Module Map + Module Contract user đưa thiếu mảnh quan trọng → vẫn chạy, ghi rõ mảnh thiếu thành open-Q, KHÔNG tự bịa cho đủ.

## Bước 0 — Xác định project

Theo thứ tự ưu tiên (giống `idea`/`partner`):
1. Argument truyền vào (vd `/delivery /Users/foo/app`).
2. Đường dẫn/tên nhắc trong tin nhắn.
3. `state/current.json`.
4. Chưa có project/code → **greenfield**: hỏi một slug kebab-case ngắn, dùng làm `<project-name>`, không cần verify folder.

Có path thì xác nhận tồn tại:
```bash
ls <project-path> 2>/dev/null | head -5 || echo "NOT_FOUND"
```
`NOT_FOUND` → báo lỗi, hỏi lại.

## Thân — sinh 3 artifact theo template GĐ11

Chốt lần lượt, hỏi một cụm mỗi lượt (≤3 câu, ưu tiên AskUserQuestion khi là lựa chọn: repo layout? branching? env mấy tầng? migration có/không?). Mỗi artifact MỞ bằng Góc nhìn lãnh đạo rồi tới chi tiết dev.

### Artifact 1 — Delivery Standards (chuẩn hoá 1 lần, áp mọi team)

Mười hai mục của template:
```text
Repository · Branching · Coding standard · Review policy · Testing pyramid
· CI/CD pipeline · Environment strategy · Secret management · Feature flag
· Migration strategy · Observability standard · Incident process.
```
Đủ-là-đủ: CI/CD chạy được + test pyramid có tỉ lệ + env/secret rõ. Team quen stack → mỗi mục 1 dòng (vd "Branching: trunk-based, PR ≤400 dòng"), chỉ mục rủi ro (migration, secret, feature flag) viết kỹ. Hệ quan trọng / nhiều team → đủ 12 mục: secret ở đâu, migration reversible thế nào, flag bật/tắt ra sao, log/metric tối thiểu. Mỗi lựa chọn lớn (branching model, test pyramid tỉ lệ, môi trường) ghi LÝ DO + phương án đã loại. Testing pyramid bám Contract GĐ10 (event cross-module → contract test).

**Góc nhìn lãnh đạo:** *sức khoẻ giao hàng kiểu DORA bắt đầu được đo* — lead time · deployment frequency · change failure rate · recovery time. Exec không đọc pipeline YAML; đọc 4 chỉ số này để biết đội có giao hàng nhanh và ổn định không.

### Artifact 2 — Definition of Ready + Definition of Done

```text
DEFINITION OF READY (item được phép vào sprint):
  có AC · ước lượng · phụ thuộc rõ · đủ context để bắt đầu.
DEFINITION OF DONE (item được coi là xong — bắt buộc MỌI item):
  code review pass · test pass (unit+integration) · contract giữ · observability có
  · doc cập nhật · không giảm chất lượng · merge xanh CI. (Không đạt DoD → không release.)
```
Đủ-là-đủ: DoD là hàng rào tối thiểu — **không cắt dòng nào bất kể kích thước việc** (chỉ Standards mới rút theo rủi ro). Việc rủi ro cao thêm dòng (vd "security scan 0 high" cho module thanh toán). DoR nhẹ hơn, rút gọn được nếu backlog đã chuẩn.

**Góc nhìn lãnh đạo:** *Definition of Done gói trong 1 khối.* Exec không đọc code — đọc DoD để biết "xong" nghĩa là gì và tin rằng mọi thứ merge đều đạt cùng một mức.

### Artifact 3 — PR Checklist

```text
[ ] link story/requirement   [ ] có test   [ ] breaking change? (đã thông báo)
[ ] update API contract?      [ ] có migration?   [ ] security impact?
[ ] observability (log/metric)?  [ ] ảnh hưởng module khác?   [ ] rollback plan nếu rủi ro cao?
```
Đủ-là-đủ: mỗi PR **link tới story/requirement** — sợi traceability nối ngược GĐ9/GĐ2–4. Ô "update API contract?" và "ảnh hưởng module khác?" bám thẳng Module Contract GĐ10. Ô nào không áp cho project (vd chưa có migration) → đánh dấu N/A, KHÔNG xoá ô.

**Góc nhìn lãnh đạo:** không cần cho checklist — nó là công cụ dev. Giá trị cho lãnh đạo nằm ở DoD + 4 chỉ số DORA phía trên.

## Tự soi trước khi chốt

Trước khi đóng cổng, tự hỏi:
- Lãnh đạo đọc đoạn MỞ (DoD + 4 chỉ số DORA) có hiểu giao hàng on-track không, không vướng jargon, không cần đọc code?
- Dev có đủ để hành động: biết branch thế nào, CI chạy gì, test tối thiểu ra sao, PR qua cổng nào, "Done" là gì — đủ để bắt đầu slice?
- Có ĐÚNG + ĐỦ 3 artifact (Delivery Standards đủ 12 mục · DoR/DoD · PR Checklist), DoD giữ nguyên khối không cắt?
- Chuẩn có bám Module Contract GĐ10 (contract test cho event cross-module, ô checklist nối vào contract thật) không, hay bịa?
- Mỗi quyết định lớn có LÝ DO + phương án đã loại?
Vướng ô nào → sửa trước khi chốt, không đẩy cổng.

## Cổng go/no-go + phân vai

Cổng GĐ11 (từ doc): ***"Item đạt Definition of Done chưa? Chuẩn delivery đủ để mọi team giao hàng an toàn, song song chưa?"***

Phân vai (A5): **CTO / Kiến trúc sư** sở hữu chuẩn delivery (viết artifact). **Reviewer được chỉ định** duyệt PR theo checklist; **Team owner mỗi module** giữ chất lượng module mình. `delivery` (AI) DRAFT chuẩn + checklist + cổng + tự soi; user giữ quyền GO. AI **không tự tuyên bố pass / không tự mở cổng** thay CTO — trình bày khối cổng rồi xin quyết định.

## Bàn giao sang uat (GĐ12)

```
═══ BÀN GIAO — Delivery Standards <project-name> ═══
Đã chốt: Delivery Standards + DoR/DoD + PR Checklist (áp mọi team)
Artifact: state/project/<project-name>/pipeline/delivery.md
→ Chứng minh hệ làm đúng (mapping AC→test→result, UAT + security sign-off): chạy /uat (GĐ12)
→ Code từng slice theo chuẩn này: chạy /frame
→ Đào gap sâu (edge case, error path, permission) một luồng trước khi verify: chạy /review
═══════════════════
```
Chỉ liệt kê, KHÔNG tự chọn hộ user chạy skill nào tiếp.

## State

Ghi artifact rút gọn vào `state/project/<project-name>/pipeline/delivery.md` (Delivery Standards + DoR/DoD + PR Checklist, mỗi phần MỞ bằng Góc nhìn lãnh đạo). Cập nhật `state/current.json`:
```json
{ "project": "<project-path>", "updated_at": "<ISO 8601>" }
```
Ghi metadata `state/project/<project-name>/pipeline/delivery.json`:
```json
{ "giai_doan": "gd11_delivery", "artifact": "pipeline/delivery.md",
  "cho_duyet": false, "nhan_tu": "modules", "ban_giao": "uat",
  "quyet_dinh_lon": [ "branching: trunk-based (loại git-flow)" ],
  "updated_at": "<ISO 8601>" }
```
`cho_duyet: true` = đã đưa cổng, chờ user; resume không tự đi tiếp. KHÔNG ghi vào repo code trừ khi user đồng ý (vd đưa PR Checklist vào `.github/`, DoD vào `CONTRIBUTING.md`).

## Ví dụ Case Management (rút gọn)

```text
Góc nhìn lãnh đạo: Definition of Done 1 khối + 4 chỉ số DORA bắt đầu đo
                   (lead time · deploy freq · change-failure · recovery).
                   Exec chỉ cần nhìn: có PR nào merge mà chưa xanh CI / chưa link story không?

DELIVERY STANDARDS
  Repo: mono-repo 3 module (Case · Notification · Identity theo Module Map GĐ10).
  Branching: trunk-based + short-lived branch. Lý do: team nhỏ, deploy nhiều lần/ngày;
             loại git-flow (release chậm, nhiều merge đau).
  Test pyramid: 70 unit / 20 integration / 10 e2e. CI: lint→unit→integration→contract(Case↔Notification)→build.
  Env: dev/staging/prod. Secret: vault, KHÔNG trong repo. Migration: forward-only + rollback script.
  Observability: log JSON + metric created_total, latency P95. Feature flag `case_create` để rollback nhanh.
  Incident: on-call Team A.

DEFINITION OF DONE (mọi item): review pass · unit+integration xanh · contract Case↔Notification giữ
  · log/metric có · doc + OpenAPI cập nhật · merge xanh CI. Không đạt → không release.

PR #1832 — feat(case): POST /cases tạo case Draft
  [x] link Story "Create Case"   [x] test unit+integration   [ ] breaking change
  [x] update OpenAPI (POST /cases)   [x] migration: bảng cases   [x] security: validate + audit CaseCreated
  [x] observability: log+metric created_total   [ ] ảnh hưởng module khác   [x] rollback: sau flag `case_create`
  Reviewer: Tech lead Team A — DoD ✔ tests xanh · ✔ contract giữ · ✔ doc cập nhật.

Cổng: PR đầu đạt DoD, CI xanh, checklist áp thật, chuẩn đủ cho các team chạy song song → sang /uat.
```

## Khi làm trong project workspace (`projects/<key>/`)

Nhận diện: user chỉ định `projects/<key>`, hoặc gói ngữ cảnh từ `resume`/`fanout` trỏ tới đó, hoặc `state/current.json` có trường `workspace`. Khi ấy:
- Bước 0 đọc thêm: `projects/<key>/constitution/` (nhất là `folders.md` + `definition-of-done.md`) và `progress/progress.json` — tìm task đang mở giao cho skill này (trường `owner`).
- Artifact người-đọc ghi vào ĐÍCH của task (trường `artifact` trong `progress.json`, đặt theo `folders.md`) — KHÔNG ghi bản chính vào `state/`. State máy riêng của skill (file json trạng thái) vẫn ở `state/project/<key>/` như cũ.
- Xong việc: báo user chạy `/checkpoint <task-id>` lấy phiếu rồi `/progress` đóng bước. Không tự lật done, không tự ghi `progress.json` — file đó một chủ (`progress`).
