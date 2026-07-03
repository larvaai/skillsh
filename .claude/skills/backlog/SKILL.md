---
name: backlog
description: Bẻ product vision đã có bằng chứng (live slice chạy thật, GĐ8) thành Roadmap → Epic → Feature → User Story → Acceptance Criteria có traceability về business value, để đội delivery biết XÂY GÌ TRƯỚC. Sinh Roadmap (theme × release) + Backlog phân rã + Release Plan. AC nằm DƯỚI story/feature, KHÔNG thay PRD; Definition of Done tách khỏi AC. Dùng khi "lập roadmap", "chia backlog", "phân rã epic/feature/story", "viết acceptance criteria", "kế hoạch release", "xây gì trước", "sprint tới build gì", hoặc khi vừa xong live slice và cần kế hoạch xây tiếp.
---

# Backlog — Roadmap & Backlog Decomposition (GĐ9 · PLAN)

`backlog` là GĐ9 của pipeline Idea→Operate. Nó nhận một product vision ĐÃ được chứng minh chạy được (Live Slice, GĐ8) và bẻ xuống thành cây việc làm được, đúng thứ tự, có đường nối ngược về business: `Roadmap Theme → Epic → Feature → User Story → Acceptance Criteria`. Nó trả lời đúng một câu hỏi: **WHAT FIRST — xây gì trước, vì giá trị gì.** Sinh ba artifact: **Roadmap** (theme × release), **Backlog** phân rã, và **Release Plan**.

Phân vai — mỗi skill lo một tầng, `backlog` không lấn:
- `idea` (GĐ0–5) chốt WHY / WHAT VALUE / Domain rồi dừng ở Domain Model. `backlog` nhận vision đã rõ làm đầu vào, KHÔNG mở lại business case, KHÔNG hỏi lại ROI/pain, KHÔNG viết lại PRD.
- `shape` (GĐ6) / `stack` (GĐ7) chốt kiến trúc & công cụ. `backlog` KHÔNG chọn framework, KHÔNG vẽ kiến trúc — chỉ tham chiếu để size feature thực tế.
- `skeleton` (GĐ8) — skill NGAY TRƯỚC — dựng một lát cắt sống chạy thật, bàn giao **Live Slice Report**. `backlog` nhận báo cáo đó làm bằng chứng "kiến trúc chạy được", rồi mới scale ra nhiều feature.
- `modules` (GĐ10) — skill NGAY SAU — chia module theo domain boundary + gán owner + contract. `backlog` liệt kê việc; `modules` gán việc cho module/team. `backlog` KHÔNG chia module, KHÔNG gán owner kỹ thuật.
- `frame` / `delivery` (GĐ11) đóng khung + code MỘT slice, và định nghĩa Definition of Done chi tiết. `backlog` KHÔNG code, KHÔNG viết đặc tả kỹ thuật slice, KHÔNG viết DoD chi tiết — chỉ ra kế hoạch để `frame` lần lượt lấy từng story.
- `partner` điều phối cả chuỗi; `backlog` chạy độc lập HOẶC do `partner` gọi.

Vai lõi: **bẻ vision thành Roadmap→Epic→Feature→Story→AC có traceability.** AC nằm DƯỚI story/feature — KHÔNG thay PRD (PRD là bản đồng thuận GĐ4 tầng trên; AC là điều kiện nghiệm thu từng behavior). Definition of Done tách khỏi AC — AC riêng từng story, DoD là chuẩn chất lượng chung mọi item (thuộc GĐ11), backlog chỉ tham chiếu DoD chứ không định nghĩa.

Playbook gốc (template + ví dụ đầy đủ): `quy-trinh-idea-to-operate.md`, mục "Giai đoạn 9". File này là bản hành động rút gọn; initiative lớn/rủi ro cao thì mở doc lấy khung phân rã đầy đủ.

## Luật cứng

- **Hợp đồng đọc-được 3 tầng (lý do skill tồn tại — tuyệt đối không bỏ).** Người đọc là đội DOANH NGHIỆP KHÁCH HÀNG — CEO/CTO, business, dev — người NGOÀI, không có kiến thức nội bộ. Với `backlog`, hợp đồng này KHÔNG phải một mục cuối trang mà là XƯƠNG SỐNG của từng artifact: Roadmap và mỗi Epic MỞ bằng **Góc nhìn lãnh đạo** (đúng 1–3 thứ CEO/CTO nhìn để biết on-track — business value + trạng thái, ngôn ngữ nghiệp vụ, không jargon), RỒI mới xuống Feature → Story → AC đủ cho DEV hành động. Cả gói scan 2–3 phút, một trang. Không viết cho riêng mình đọc. Một Epic không nói được business value bằng một câu nghiệp vụ → chưa sẵn sàng, làm rõ trước khi phân rã tiếp.
- **Đủ-là-đủ.** Độ sâu phân rã tỉ lệ RỦI RO/ẨN SỐ, không theo vị trí trong luồng. Release gần nhất → phân rã tới Story+AC cho sprint sắp tới. Release xa → chỉ theme + epic đặt tên. Story quen thuộc/rủi ro thấp → 1–2 AC; story mới/rủi ro cao → AC phủ happy path + biên + error. KHÔNG bao giờ bỏ tầng (không nhảy Epic → Task, luôn có Feature+Story ở giữa); chỉ rút gọn độ sâu. KHÔNG viết hàng loạt story khi PRD/Domain chưa rõ.
- **Không lấn vai.** Không hỏi lại WHY/ROI (đã chốt GĐ1). Không chọn stack/kiến trúc (GĐ6–7). Không chia module/gán owner kỹ thuật (GĐ10). Không viết code hay đặc tả kỹ thuật slice, không viết DoD chi tiết (GĐ11). Không tự viết Test Case chi tiết — chỉ đặt **Test ref** (TC-...) làm móc, để GĐ12 lấp. Gặp câu ngoài vai → ghi thành open question/mục bàn giao, trỏ về đúng skill, không tự làm.
- **AC nằm DƯỚI story/feature, KHÔNG thay PRD.** AC là behavior Given/When/Then của MỘT story cụ thể — không phải danh mục yêu cầu toàn sản phẩm. **Definition of Done tách khỏi AC**: AC = "story này đúng khi nào"; DoD = chuẩn chất lượng bắt buộc cho MỌI item (thuộc GĐ11), chỉ tham chiếu chứ không viết vào từng AC.
- **Mỗi quyết định lớn ghi LÝ DO + phương án đã loại.** Vì sao theme này vào R1 mà không R2; vì sao epic X cắt khỏi MVP; vì sao gộp/tách epic. Để sau audit lại được.
- **Cấm câu phủ định cứng khi phản biện** (kế thừa `partner`): không "không thể", "sai rồi", "không làm được". Thấy backlog quá tải/thứ tự sai/PRD chưa đủ để chia → nêu cụ thể chỗ vướng + đề một lối đi tiếp (cắt scope, đổi thứ tự, hoãn release), không dập.
- **Traceability là bắt buộc.** Mỗi Epic gắn ngược về **Business Objective / Product Goal** (từ GĐ1–4). Mỗi Feature thuộc một Epic. Mỗi Story thuộc một Feature. Mỗi AC thuộc một Story và phản ánh business rule bất biến từ Domain (GĐ5). Đứt một mắt = backlog "mồ côi", rớt cổng — ghi rõ chỗ đứt thay vì bịa nối.
- **Không tự ghi artifact vào repo code** trừ khi user đồng ý (theo `idea`). Mặc định ghi vùng state của skill. Greenfield mới ghi thẳng.

## Đầu vào — đọc trước khi phân rã

- **Live Slice Report (GĐ8, của `skeleton`) — nguồn CHÍNH.** Bằng chứng kiến trúc/stack chạy thật. Lấy: slice đã chạy thật (= feature ĐẦU TIÊN của release gần nhất), "Giả định đã đổi" (giả định PRD/Architecture phải đổi sau khi chạy → có thể thêm/bớt requirement, phản ánh vào backlog TRƯỚC khi chia), rủi ro kiến trúc còn lại.
- **PRD + Domain Model (GĐ4–5)** — goals, success metric, scope in/out, entity, lifecycle, business rule, domain event. Story bám hành động trên entity; AC bám business rule bất biến; scope in/out để không phân rã thứ đã cắt.
- **Architecture Brief + Tech Decision (GĐ6–7, nếu có)** — chỉ để size feature thực tế và biết ràng buộc thứ tự (feature nào chặn feature nào), KHÔNG chọn lại.
- `state/current.json` + `state/project/<project-name>/pipeline/` — artifact các GĐ trước của pipeline này.
- `.ai-understanding/` (atlas, nếu brownfield & có) — để tên epic/feature/story không đụng/mâu thuẫn code cũ.

Thiếu Live Slice Report VÀ thiếu PRD/Domain → không đủ nền: nêu chính xác phần thiếu; nếu user ĐÃ đưa Live Slice Report trong prompt/file thì chạy kèm ⚠️ cảnh báo (theo mục "Đầu vào ngoài state" ngay dưới); nếu KHÔNG có gì thì mới gợi ý quay lại `skeleton`/`idea`/`partner` chốt trước, HOẶC chạy `backlog` ở độ sâu rút gọn cho phần đã rõ và ghi phần còn treo vào open question. KHÔNG tự bịa vision để phân rã.

## Đầu vào ngoài state (nới — nhận prompt/file thay cho artifact GĐ trước)

Không có Live Slice Report trong state VẪN chạy được nếu user mô tả trực tiếp trong prompt, dán nội dung, hoặc trỏ một file ngoài. Thứ tự ưu tiên: (1) đọc state pipeline; (2) không có thì nhận Live Slice Report từ prompt/file user đưa; (3) vẫn không có gì thì mới gợi ý chạy /skeleton.

Khi chạy bằng nguồn NGOÀI (không phải Live Slice Report của GĐ8 đã qua cổng), in NGUYÊN block cảnh báo này NGAY TRƯỚC khi làm, rồi VẪN tiếp tục — đây là cảnh báo, KHÔNG phải chặn:

```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Live Slice Report" lấy từ prompt/file bạn đưa, CHƯA qua cổng GĐ8 (skill /skeleton).
- Rủi ro: (1) chưa truy vết ngược được về pipeline; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /skeleton trước để có "Live Slice Report" đã qua cổng.
```

Nếu Live Slice Report user đưa thiếu mảnh quan trọng → vẫn chạy, ghi rõ mảnh thiếu thành open-Q, KHÔNG tự bịa cho đủ.

## Bước 0 — Xác định project

Lấy theo thứ tự ưu tiên (giống `idea`/`partner`):
1. Argument truyền vào (vd `/backlog /Users/foo/my-app`).
2. Đường dẫn/tên nhắc trong tin nhắn.
3. `state/current.json`.
4. Chưa có project/code → greenfield: hỏi một slug kebab-case ngắn, dùng làm `<project-name>`, không cần verify folder.

Có path thì xác nhận tồn tại:
```bash
ls <project-path> 2>/dev/null | head -5 || echo "NOT_FOUND"
```
`NOT_FOUND` → báo lỗi, hỏi lại. Rồi đọc `state/project/<project-name>/pipeline/skeleton.md` (Live Slice) làm nền.

## Thân — sinh đúng ba artifact (bám template GĐ9, thứ tự leadership-first)

Cây phân rã chuẩn của doc:
`Business Objective → Product Goal → Roadmap Theme → Initiative → Epic → (Capability nếu rất lớn) → Feature → User Story → AC → Engineering Task → Test ref`.
Task/Test-ref chỉ để trỏ sang GĐ11–12, không phải trọng tâm GĐ9.

### 1) Roadmap (Theme × Release) — tầng lãnh đạo

Bảng: mỗi hàng một **Theme** (mục tiêu nghiệp vụ), các cột là **Release** (3–4 mốc thời gian: R1 MVP, R2, R3…), mỗi ô vài epic. R1 = MVP, thường bao trọn slice đã chạy ở GĐ8. Đầu bảng neo về business: `Business Objective → Product Goal → Roadmap Theme`.

```text
ROADMAP — <sản phẩm>
Business Objective : <mục tiêu business đo được — nối GĐ1>.
Product Goal       : <mục tiêu sản phẩm — nối GĐ2>.
Theme "<tên>"  | R1 (MVP)      | R2            | R3
               | <epic/nhóm>   | <epic/nhóm>   | <epic/nhóm>
```

- **Đủ-là-đủ:** theme cho toàn tầm nhìn; epic điền dày cho **release gần nhất**, thưa dần cho release xa. Không cố điền hết mọi ô. Mỗi lựa chọn "epic này vào R1" ghi lý do 1 dòng.
- **Góc nhìn lãnh đạo:** đây CHÍNH là trang lãnh đạo đọc — một câu Business Objective có số + bảng theme×release để thấy ngay "đang xây gì, tới đâu, theo giá trị nào". Bảng này không tự đứng một mình cho CTO → chưa đạt.

### 2) Backlog phân rã (Epic → Feature → Story → AC)

Với mỗi release gần nhất, mở mỗi Epic bằng **business value + trạng thái** (để lãnh đạo scan và dừng ở tầng epic vẫn hiểu), rồi mới xuống Feature/Story/AC (để dev hành động):

```text
BACKLOG ITEM (R1)
  Epic     : EPIC-<slug> — <tên> — business value: <nối Objective/Goal> — trạng thái.
  Feature  : FEAT-<slug> — <tên> — thuộc epic <...> — value — size (vừa một release/Program Increment).
  Story    : STORY-<slug> — "Là <role>, tôi muốn <hành động>, để <giá trị>."
  AC       : AC-<slug>-<n>: Given <bối cảnh> / When <hành động> / Then <kết quả kiểm được + rule bất biến>.
             (mỗi story 1–N AC; AC phản ánh business rule từ Domain GĐ5; story rủi ro cao → nhiều AC hơn.)
  Tasks    : <engineering task thô — để size, không phải đặc tả; đặc tả là việc /frame>.
  Test ref : TC-<...>   (chỉ đặt móc; GĐ12 lấp chi tiết.)
```

**ID bắt buộc cho mỗi story** (đây là cái `/frame` gọi khi build từng story, `/uat` map test, `/traceability` đối chiếu): mỗi Story có `id = STORY-<slug>` (slug kebab từ tên story, vd `STORY-case-create`), mỗi AC có `id = AC-<slug>-<n>`. Dùng cùng prefix `STORY-`/`AC-` với traceability spine của `partner` — MỘT định dạng duy nhất cho cả suite, không đặt kiểu khác (không `S1.2.1`).

Các tầng AC (doanh nghiệp lớn có thể nhiều tầng):
```text
Feature AC : feature xong khi <hành vi tổng của feature>.
Story AC   : từng behavior Given/When/Then.
Release AC : go-live khi pass UAT + security scan + perf test + có rollback (chi tiết ở GĐ12–13).
Definition of Done: chuẩn chất lượng MỌI item — tách khỏi AC, định nghĩa ở GĐ11, ở đây chỉ tham chiếu.
```

- **Đủ-là-đủ:** story **có AC** cho **sprint sắp tới**; feature cho **release gần nhất**; epic cho toàn roadmap. Story xa → chỉ đặt tên, refine sau (backlog refinement là việc liên tục). KHÔNG đổ hàng loạt story cho release xa khi chưa cần; Domain còn treo → ghi open question thay vì bịa story để lấp.
- **Góc nhìn lãnh đạo:** mỗi Epic mở bằng business value + trạng thái TRƯỚC khi xuống feature — lãnh đạo dừng ở tầng epic vẫn hiểu mỗi khối tiền đổi lấy giá trị gì; dev đọc tiếp xuống AC để hành động.

### 3) Release Plan

Với mỗi release: mục tiêu nghiệp vụ của release (nối success metric PRD), epic/feature nào vào, **thứ tự ưu tiên + LÝ DO** (vì sao release/feature này trước cái kia), điều kiện go-live (Release AC), phụ thuộc + rủi ro, và cái CỐ TÌNH hoãn sang release sau (kèm lý do). Đây là cầu nối sang `modules` (GĐ10, song song) và `frame`/`delivery` (GĐ11).

```text
RELEASE PLAN
  R1 (MVP) : <feature list> — mục tiêu: <nối success metric> — thứ tự + lý do: <...>
             — Release AC: <điều kiện go-live> — phụ thuộc: <...> — rủi ro: <...>.
  R2 / R3  : mục tiêu + epic chính (phác thô); hoãn <X> vì <lý do>.
```

- **Đủ-là-đủ:** chi tiết cho R1 (MVP); R2+ chỉ mục tiêu + epic chính. Không lập kế hoạch cứng cho thứ chưa tới.
- **Góc nhìn lãnh đạo:** trả lời "xây gì trước và vì sao" bằng ngôn ngữ giá trị — không phải bằng độ khó kỹ thuật.

**Traceability** (bắt buộc, mỏng cũng được): mỗi epic trỏ ngược Business Objective/Product Goal; mỗi feature/story trỏ requirement/PRD; mỗi AC là hành vi của đúng story đó + nối business rule Domain. Đứt một mắt xích → ghi rõ chỗ đứt, đừng bịa nối.

## Tự soi trước khi chốt

Trước khi đưa cổng, tự hỏi và sửa nếu vướng:
- **Lãnh đạo đọc được đoạn đầu?** Roadmap + business value mỗi epic có ngôn ngữ nghiệp vụ, không jargon, scan 2–3 phút ra "xây gì / vì giá trị gì / tới đâu" mà không cần hỏi dev?
- **Dev đủ để hành động?** Story sprint tới có AC Given/When/Then cụ thể, task thô để size, Test ref — đủ để giao sang `frame` và bắt tay code?
- **Đúng + đủ các phần?** Có đủ **Roadmap + Backlog phân rã + Release Plan**? Story release gần nhất đều có AC? AC nằm DƯỚI story (không lẫn/thành PRD thứ hai)? DoD tách riêng (chỉ tham chiếu)?
- **Đủ-là-đủ?** Release gần nhất sâu tới AC, release xa chỉ theme+epic; số AC tỉ lệ rủi ro; không đổ story cho release xa; không bỏ tầng?
- **Traceability liền?** Epic→Objective/Goal, Feature→Epic, Story→Feature, AC→Story, AC↔business rule Domain — không mắt nào đứt?
- **Không lấn vai?** Không chọn stack, không chia module, không viết code/đặc tả slice/DoD chi tiết, không viết Test Case chi tiết?

## Cổng go/no-go + AI duyệt

Cổng (đúng câu doc GĐ9): **"Backlog đủ để lập kế hoạch delivery & phân module chưa?"**
Kèm: release gần nhất đã có story+AC? Roadmap lãnh đạo đọc được? Thứ tự release có lý do? Còn open question Domain nào chặn không?

**AI DUYỆT theo phân vai A5:** người duyệt GĐ9 là **Product Owner (chủ sở hữu) + Tech lead**. AI đóng vai trợ lý cả hai — trước khi bàn giao, tự kiểm ba xương sống: (1) đủ Roadmap + Backlog + Release Plan; (2) đọc-được 3 tầng; (3) mọi epic/feature/story nối ngược nguồn GĐ trước, không bịa; cộng soát traceability + tính khả thi thô của thứ tự release. Vướng một cái → nêu rõ đúng phần thiếu, sửa, KHÔNG bàn giao vội. AI KHÔNG tự tuyên bố pass — trình đánh giá + rủi ro, để user (đóng vai PO/Tech lead) quyết go/no-go.

## Bàn giao sang modules (GĐ10)

Qua cổng → khối bàn giao (chỉ liệt kê, không tự chọn hộ user):
```text
═══ BÀN GIAO — <sản phẩm> · Backlog GĐ9 ═══
Đã chốt : Roadmap (<n> theme × <m> release) · Backlog release gần nhất (<k> epic / <f> feature / <s> story có AC) · Release Plan R1.
Artifact: state/project/<project-name>/pipeline/backlog.md
→ Chia module theo domain boundary + gán owner + contract (GĐ10, bước kế mặc định): chạy /modules
→ Build ngay một story đã có AC của R1 (đóng khung slice cho dev)                 : chạy /frame <STORY-id>  (rồi /delivery khi vào build chuẩn GĐ11)
→ Domain còn treo khiến story chưa đặt được AC                                    : quay lại /idea hoặc /partner (GĐ5)
════════════════
```
`modules` (GĐ10) là bước kế mặc định của pipeline; `frame` khi muốn build ngay một story. Chỉ liệt kê, để user quyết.

## State

Ghi artifact vào `state/project/<project-name>/pipeline/backlog.md` (Roadmap + Backlog + Release Plan — Góc nhìn lãnh đạo trước, chi tiết sau, một trang scan được). KHÔNG vào repo code trừ khi user đồng ý; greenfield mới ghi thẳng `<project>/`.

Cập nhật `state/current.json`:
```json
{ "project": "<project-path>", "updated_at": "<ISO 8601>" }
```

Ghi con trỏ pipeline `state/project/<project-name>/pipeline/backlog.json` để `partner` và lần chạy sau resume được:
```json
{
  "project": "<path>", "giai_doan": "gd9_backlog", "cho_duyet": false,
  "nguon": ["gd8_live_slice", "gd4_prd", "gd5_domain"],
  "roadmap": { "themes": ["Xử lý hồ sơ nhanh"], "releases": ["R1","R2","R3"] },
  "backlog": { "epics": 2, "features": 5, "stories_co_ac": 8 },
  "stories": [
    { "id": "STORY-case-create", "epic": "EPIC-intake", "feature": "FEAT-case-form",
      "story": "Là nhân viên, tôi muốn tạo hồ sơ, để bắt đầu quy trình duyệt.",
      "ac": ["AC-case-create-1", "AC-case-create-2"], "test_ref": "TC-CASE-CREATE-001",
      "release": "R1", "status": "todo" }
  ],
  "da_chot": ["R1 = Intake & Review (lý do: bằng chứng slice ở GĐ8)"],
  "dang_mo": ["escalation SLA: cần domain rule cụ thể — chốt trước khi viết story R2"],
  "handoff_ke": "modules",
  "artifact_path": "state/project/<project-name>/pipeline/backlog.md"
}
```
`cho_duyet: true` = đã đưa cổng, đang chờ user — resume không tự đi tiếp, nhắc lại cổng cũ và xin go/no-go.

## Ví dụ Case Management (rút gọn)

```text
Nguồn: Live Slice "Tạo một Case mới" PASS (GĐ8) · PRD + Domain (Case·Reviewer·StatusHistory, rule
       "reviewer không tự duyệt case mình tạo", "case > 7 ngày → tự Escalated").

GÓC NHÌN LÃNH ĐẠO
ROADMAP
  Business Objective : Giảm 40% thời gian xử lý hồ sơ.
  Product Goal       : Xử lý hồ sơ trên một màn hình thống nhất.
  Theme "Xử lý hồ sơ nhanh" | R1 (MVP)        | R2            | R3
                            | Intake & Review | Search & SLA  | Reporting
  (R1 vào trước vì slice GĐ8 đã chứng minh luồng tạo/duyệt chạy thật.)

BACKLOG (R1)
  Epic    : Case Intake & Review — value: cắt thời gian nhập/duyệt hồ sơ — trạng thái: đang làm.
  Feature : Create Case — thuộc epic trên — value: khởi tạo hồ sơ chuẩn — size: 1 sprint.
  Story   : "Là NV vận hành, tôi muốn tạo hồ sơ khách hàng mới, để bắt đầu quy trình xét duyệt."
  AC      : Given login quyền Case Creator / When nhập đủ field bắt buộc + Submit
            / Then tạo Case trạng thái Draft, ghi audit CaseCreated, hiện mã Case.
  Tasks   : API POST /cases · Case aggregate · bảng cases · form · unit+integration test · audit log.
  Test ref: TC-CASE-CREATE-001   (Create Case = chính slice đã chạy thật ở GĐ8 → đưa lên đầu R1.)

RELEASE PLAN
  R1 (MVP): Create Case → Find/Filter → Approve/Reject → Audit log. Mục tiêu: tạo+duyệt ≤7 phút.
            Thứ tự: Create Case trước (đã có slice sống, gỡ rủi ro sớm); Approve sau (phụ thuộc Case tồn tại).
            Release AC: pass UAT + security scan + có rollback. Hoãn Reporting sang R3 (BI không chặn go-live).
            Rủi ro: tải đồng thời nhiều reviewer (perf GĐ12). DoD: xem GĐ11.

Cổng: R1 có story+AC · roadmap 1 trang đọc được · thứ tự có lý do → đủ để phân module & lập delivery.
Bàn giao: chia module Case/Identity/Audit theo boundary → /modules (GĐ10); hoặc build "Create Case" → /frame.
AC "reviewer không tự duyệt" nối thẳng business rule Domain GĐ5 — traceability liền.
```

## Khi làm trong project workspace (`projects/<key>/`)

Nhận diện: user chỉ định `projects/<key>`, hoặc gói ngữ cảnh từ `resume`/`fanout` trỏ tới đó, hoặc `state/current.json` có trường `workspace`. Khi ấy:
- Bước 0 đọc thêm: `projects/<key>/constitution/` (nhất là `folders.md` + `definition-of-done.md`) và `progress/progress.json` — tìm task đang mở giao cho skill này (trường `owner`).
- Artifact người-đọc ghi vào ĐÍCH của task (trường `artifact` trong `progress.json`, đặt theo `folders.md`) — KHÔNG ghi bản chính vào `state/`. State máy riêng của skill (file json trạng thái) vẫn ở `state/project/<key>/` như cũ.
- Xong việc: báo user chạy `/checkpoint <task-id>` lấy phiếu rồi `/progress` đóng bước. Không tự lật done, không tự ghi `progress.json` — file đó một chủ (`progress`).
