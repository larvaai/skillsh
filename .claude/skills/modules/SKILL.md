---
name: modules
description: Chia hệ thống thành module theo RANH GIỚI DOMAIN (bounded context + data ownership + change frequency), KHÔNG theo màn hình; gán mỗi module đúng 1 owner và 1 contract rõ để các team chạy song song không đạp lên nhau. Sinh hai artifact — Module Map (bounded context → module → team owner → phụ thuộc) và Module Contract (public API, domain event, data ownership, permission model, error code, SLA/SLO). Là GĐ10 (SỞ HỮU) của pipeline Idea→Operate. Dùng khi "chia module", "phân module cho team", "ai sở hữu phần nào", "vẽ module map", "định contract giữa các team", "ownership & ranh giới module", "trước khi nhiều team code song song cần chia gì".
---

# Modules — Chia module theo domain, gán owner + contract (GĐ10 pipeline Idea→Operate)

`modules` là **Giai đoạn 10 (Module & Team Ownership — SỞ HỮU)** của pipeline doanh nghiệp Idea→Operate. Nó nhận backlog đã phân rã (GĐ9) và biến domain thành **ranh giới sở hữu**: cắt hệ thống thành các module theo ranh giới domain, gán mỗi module đúng một team và một hợp đồng rõ để các team khác gọi vào — để nhiều team chạy delivery song song mà không giẫm nhau. Sinh đúng hai artifact: **Module Map** (bounded context → module → owner + phụ thuộc) và **Module Contract** (public API, domain events, data ownership, permission model, error codes, SLA/SLO) cho từng module.

Phân vai — `modules` không lấn skill khác:
- `idea` (GĐ0–5) chốt domain: bounded context, entity, rule, event, data ownership; dừng ở Domain Model. `modules` NHẬN cái đó làm ranh giới, KHÔNG định lại domain, KHÔNG hỏi lại WHY/WHAT.
- `backlog` (GĐ9) chốt epic→feature→story→AC. `modules` NHẬN backlog để biết feature nào rơi vào module nào; không viết lại story.
- `frame` build code một slice (GĐ8/11). `modules` KHÔNG code, chỉ vẽ ranh giới + contract để `delivery`/`frame` code bên trong.
- `delivery` (GĐ11) nhận Module Map + Contract để từng team build. `modules` bàn giao sang đó, không tự đặt chuẩn code.
- `review`/`triage` = soi gap/số phận file; `atlas`/`explain` = dựng và dạy hiểu code cũ. Không thuộc GĐ10.
- `partner` điều phối cả pipeline 15 giai đoạn; `modules` là một mắt xích, chạy độc lập HOẶC do `partner` gọi.

Chuỗi handoff: `idea(0–5) → shape(6) → stack(7) → skeleton(8) → backlog(9) → **modules(10)** → delivery(11) → uat(12) → ship(13) → operate(14 → về backlog 9)`.

Nguồn template đầy đủ (template + ví dụ): `quy-trinh-idea-to-operate.md`, mục **"## Giai đoạn 10 — Module & Team Ownership (SỞ HỮU)"**. Hệ lớn/rủi ro cao/nhiều team → mở file gốc lấy template đầy đủ.

## Luật cứng (đọc trước, vi phạm là sai)

- **Hợp đồng đọc-được 3 tầng (LÝ DO skill này tồn tại).** Người đọc artifact là đội của DOANH NGHIỆP KHÁCH HÀNG — CTO, business, dev — người NGOÀI, không biết nội bộ. Mỗi artifact PHẢI: (1) MỞ bằng **Góc nhìn lãnh đạo** — đúng 1–3 thứ CEO/CTO nhìn để biết on-track (ở đây: "ai chịu trách nhiệm cái gì khi có sự cố"), ngôn ngữ nghiệp vụ, không jargon; (2) RỒI mới tới chi tiết kỹ thuật đủ để dev hành động; (3) 1 trang, scan 2–3 phút. Không viết cho riêng mình đọc.
- **Domain trước module — chia theo DOMAIN, không theo màn hình** (A3-#3). Ranh giới module bám: `bounded context · data ownership · change frequency · team ownership · integration boundary · security boundary · operational responsibility`. "Màn hình A cần gì" KHÔNG phải tiêu chí chia — một màn hình có thể chạm nhiều module; đừng biến mỗi màn hình/tab thành một module.
- **Mỗi module đúng 1 owner + 1 contract.** Không có module "chung của mọi người". Contract nói rõ module SỞ HỮU gì và KHÔNG sở hữu gì — ranh giới ra ngoài ("Does NOT own") phải hiện.
- **Đủ-là-đủ.** Độ sâu contract tỉ lệ RỦI RO/ẨN SỐ, không theo vị trí trong luồng. Module quen, ít đổi, một team → contract gọn. Module lõi/nhiều team gọi/security nặng → contract đầy đủ (thêm domain event, permission, error code, SLA/SLO, test contract). KHÔNG bao giờ bỏ phần contract nào — chỉ rút gọn độ sâu; **Owner + Owns + Does NOT own + Public API là BẮT BUỘC luôn** ("Does NOT own" là dòng chặn hai team giẫm nhau, không bao giờ được bỏ).
- **Không lấn vai.** Không định lại domain (việc `idea`/GĐ5), không viết story (việc `backlog`), không chọn stack (GĐ7), không code (việc `frame`/`delivery`), không đào edge case (`review`).
- **Mỗi quyết định lớn ghi LÝ DO + phương án đã loại.** Vì sao gộp/tách một module thế này (vd "tách Notification vì đổi tần suất khác Case core"), đã cân cách chia nào khác + loại vì sao (vd "đã cân gộp vào Case, loại vì hai team khác nhau") — để CTO audit lại ranh giới sau.
- **KHÔNG tự ghi artifact vào repo code** trừ khi user đồng ý. Mặc định ghi vào vùng state của skill (xem State). Muốn đưa vào repo đích → hỏi trước; greenfield thì ghi thẳng repo được.
- **Cấm câu phủ định cứng khi phản biện** (kế thừa `partner`/`idea`): không "không thể", "sai rồi", "không làm được". Ranh giới lệch → nêu một lối chia khác kèm lý do, luôn có đường đi tiếp.

## Đầu vào — đọc trước khi vẽ

- Artifact GĐ trước: **backlog** (GĐ9) — `state/project/<project-name>/pipeline/backlog.md` (hoặc file GĐ9 tương đương). Lấy epic/feature/story để biết năng lực nào cần một module nào gánh, và để kiểm chéo: mọi feature GĐ9 phải rơi vào đúng một module.
- **Domain Model** (GĐ5, từ `idea`) — `state/project/<project-name>/ideas/<slug>.md` hoặc pipeline: bounded context, entity, data ownership, domain event. Đây là XƯƠNG SỐNG để cắt module. Ranh giới module PHẢI bám bounded context của domain.
- `state/current.json` — pointer project gần nhất; `state/project/<project-name>/pipeline/` — các artifact GĐ khác đã có.
- `state/project/<project-name>/user-state.json` (của `explain`, chỉ ĐỌC) — lấy `level` để chỉnh độ dài diễn giải, không hỏi lại mức.
- `.ai-understanding/` (của `atlas`, nếu brownfield) — ranh giới module/ownership đã tồn tại trong code, tránh vẽ contract mâu thuẫn với thực tế.

Thiếu domain rõ → KHÔNG tự đoán bounded context. Nêu là ẩn số, đề nghị quay lại `idea` (GĐ5) làm rõ trước. Thiếu Roadmap + Backlog (Epic→Feature→Story→AC) trong state: nếu user ĐÃ đưa nó trong prompt/file → chạy kèm ⚠️ cảnh báo (theo mục "Đầu vào ngoài state" dưới đây); nếu KHÔNG có gì → mới gợi ý chạy /backlog (GĐ9). Không tự bịa mảnh thiếu.

## Đầu vào ngoài state (nới — nhận prompt/file thay cho artifact GĐ trước)

Không có Roadmap + Backlog (Epic→Feature→Story→AC) trong state VẪN chạy được nếu user mô tả trực tiếp trong prompt, dán nội dung, hoặc trỏ một file ngoài. Thứ tự ưu tiên: (1) đọc state pipeline; (2) không có thì nhận Roadmap + Backlog (Epic→Feature→Story→AC) từ prompt/file user đưa; (3) vẫn không có gì thì mới gợi ý chạy /backlog.

Khi chạy bằng nguồn NGOÀI (không phải Roadmap + Backlog (Epic→Feature→Story→AC) của GĐ9 đã qua cổng), in NGUYÊN block cảnh báo này NGAY TRƯỚC khi làm, rồi VẪN tiếp tục — đây là cảnh báo, KHÔNG phải chặn:

```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Roadmap + Backlog (Epic→Feature→Story→AC)" lấy từ prompt/file bạn đưa, CHƯA qua cổng GĐ9 (skill /backlog).
- Rủi ro: (1) chưa truy vết ngược được về pipeline; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /backlog trước để có "Roadmap + Backlog (Epic→Feature→Story→AC)" đã qua cổng.
```

Nếu Roadmap + Backlog (Epic→Feature→Story→AC) user đưa thiếu mảnh quan trọng → vẫn chạy, ghi rõ mảnh thiếu thành open-Q, KHÔNG tự bịa cho đủ.

## Bước 0 — Xác định project

Lấy project theo thứ tự ưu tiên (giống `idea`/`partner`):
1. Argument truyền vào (vd `/modules /Users/foo/my-app`).
2. Đường dẫn/tên nhắc trong tin nhắn.
3. `state/current.json` nếu có.
4. Chưa có project/code (greenfield) → hỏi một slug kebab-case ngắn, dùng làm `<project-name>`, không cần verify folder.

Có path thì xác nhận tồn tại:
```bash
ls <project-path> 2>/dev/null | head -5 || echo "NOT_FOUND"
```
`NOT_FOUND` → báo lỗi, hỏi lại.

## Thân — sinh Module Map rồi Module Contract

Bám đúng template mục "Giai đoạn 10" của `quy-trinh-idea-to-operate.md`. Mỗi artifact MỞ bằng Góc nhìn lãnh đạo, rồi tới chi tiết dev. Độ sâu theo Đủ-là-đủ.

Chủ sở hữu / Người duyệt: **Kiến trúc sư + Eng managers**, duyệt bởi **CTO**. Chạy song song: backlog (GĐ9), chuẩn delivery (GĐ11).

### Artifact 1 — Module Map (bounded context → module → team owner → phụ thuộc)

Đi từ Domain Model: mỗi **bounded context** → một (hoặc gộp thành một) **module**; gán **1 team owner**; vẽ **phụ thuộc** (ai gọi ai) để thấy ranh giới integration. Kiểm chéo backlog: mọi feature GĐ9 rơi vào đúng một module — **không feature mồ côi, không feature thuộc hai module**.

```text
MODULE MAP
  <Module>  ← bounded context <tên>  · Owner: Team <...>  · phụ thuộc → <module khác> (qua contract/event nào)
  ...  (module × team owner × phụ thuộc)
```

- **Góc nhìn lãnh đạo (mở đầu Map):** bảng *module × team owner* + một dòng mỗi module "sở hữu gì / KHÔNG sở hữu gì". Trả lời tức thì câu CTO hỏi khi có sự cố: **"ai chịu trách nhiệm cái gì?"** — không jargon.
- **Đủ-là-đủ:** hệ nhỏ 2–4 module → bảng ngắn. Hệ nhiều team → thêm sơ đồ phụ thuộc + đánh dấu ranh giới security/integration. KHÔNG bỏ module nào khỏi bản đồ.
- Mỗi lần gộp/tách khác cách chia "hiển nhiên" → ghi **lý do + cách chia đã loại**.

### Artifact 2 — Module Contract (mỗi module một contract)

Theo template GĐ10; đủ các ô (rút gọn ô nào rủi ro thấp, KHÔNG bỏ ô):

```text
MODULE CONTRACT — <module>
  Owner            : team đúng 1.
  Responsibilities : module làm gì (1–3 dòng).
  Owns (data/event): bảng nào · vòng đời trạng thái nào · event nào phát ra (data ownership — sợi từ GĐ5).
  Does NOT own     : ranh giới ra ngoài (cái thuộc module/team khác lo).
  Public API       : REST → mô tả bằng OpenAPI (chuẩn interface độc lập ngôn ngữ); nêu endpoint chính.
  Domain events    : phát ra / lắng nghe.
  Permission model : ai được gọi gì (role → quyền).
  Error codes      : mã lỗi công khai.
  SLA/SLO          : nếu module có ràng buộc vận hành (module lõi/đối ngoại/critical path).
  Test contract    : hợp đồng test với module gọi (contract test giữa team).
```

- **Góc nhìn lãnh đạo (mở đầu mỗi Contract):** một câu — module này *giữ phần nghiệp vụ nào*, và khi hỏng thì *ai gọi ai* — TRƯỚC khi tới OpenAPI/event/error code.
- **Đủ-là-đủ:** BẮT BUỘC mọi module: Owner + Responsibilities + Owns + Does NOT own + Public API. Các dòng còn lại (event, permission, error code, SLA/SLO, test contract) — ghi khi có: module lõi/nhiều team gọi/đối ngoại → ghi đủ; module rìa một team dùng → ghi gọn hoặc "không có", kèm 1 dòng vì sao gọn. "Does NOT own" không bao giờ được bỏ.
- Contract REST mô tả interface bằng **OpenAPI** — để team khác gọi mà không cần đọc code bên trong.

## Tự soi trước khi chốt

Trước khi đóng hai artifact, tự hỏi — vướng câu nào thì SỬA trước, không chốt:
- **Lãnh đạo đọc được đoạn đầu không?** Module Map + đầu mỗi contract có nói được "ai sở hữu cái gì / gọi ai khi sự cố" bằng ngôn ngữ nghiệp vụ, không đâm thẳng vào endpoint/schema?
- **Dev đủ để hành động chưa?** Mỗi contract có đủ Public API + event + data ownership + ranh giới "does NOT own" + permission/error code (cho module lõi) để một team code trong ranh giới mà không phải hỏi lại?
- **Đúng + đủ các phần chưa?** Có đủ Module Map + Module Contract cho MỌI module; contract đủ các ô (rút gọn ô rủi ro thấp, không bỏ ô lõi)? Feature GĐ9 map hết vào module chưa?
- **Chia theo domain, không theo màn hình?** Mỗi module bám một bounded context, không phải một cụm màn hình? Có module nào hai owner không?
- **Bám nguồn?** Ranh giới bám Domain Model (GĐ5) + phủ hết feature backlog (GĐ9), không bịa context mới?

## Cổng go/no-go + Bàn giao sang `delivery`

**Cổng (câu hỏi doc GĐ10):** *"Ownership & contract đã rõ để các team chạy delivery SONG SONG chưa?"*

**AI DUYỆT theo phân vai (A5):** GĐ10 có Chủ sở hữu = Kiến trúc sư + Eng managers (viết artifact), Người duyệt = **CTO** (mở cổng). `modules` đóng vai Chủ sở hữu: dựng artifact, tự soi, TRÌNH BẰNG CHỨNG (mỗi module đúng một owner; không data/event bị hai module cùng sở hữu; không feature mồ côi; mọi phụ thuộc đi qua contract) — nhưng **KHÔNG tự tuyên bố GO**. Quyết định GO là của user (đóng vai CTO/Người duyệt). Chưa GO → nêu đúng ô còn lỏng (ranh giới lệch / contract thiếu ô / feature chưa có chủ / owner đôi), đề xuất một cách chia lại, KHÔNG tự trôi sang GĐ11.

GO rồi → khối bàn giao (chỉ liệt kê, KHÔNG tự chọn hộ user):
```text
═══ BÀN GIAO — <project-name> · GĐ10 xong ═══
Đã chốt   : <n> module · mỗi module 1 owner + contract · ranh giới does-NOT-own rõ · data ownership sạch.
Artifact  : state/project/<project-name>/pipeline/modules.md
Theo dõi  : <phụ thuộc/SLA rủi ro nếu có>
→ Nhiều team bắt đầu code song song, cần chuẩn giao hàng + DoD: chạy /delivery (GĐ11) — mỗi slice đóng khung bằng /frame
→ Chỉ build ngay MỘT slice trong một module: chạy /frame
→ Ranh giới đụng code cũ, cần hiểu trước khi module đụng vào: chạy /atlas hoặc /explain
════════════════
```

Không tự chọn hộ skill nào tiếp — chỉ liệt kê, để user quyết.

## State — ghi artifact + cập nhật con trỏ

- Ghi hai artifact vào `state/project/<project-name>/pipeline/modules.md` (Module Map + toàn bộ Module Contract). **KHÔNG vào repo code** trừ khi user đồng ý; greenfield thì ghi thẳng repo được (`<project>/docs/modules.md` hoặc nơi user chỉ).
- Cập nhật `state/current.json`:
```json
{ "project": "<project-path>", "updated_at": "<ISO 8601>" }
```
- Ghi con trỏ pipeline `state/project/<project-name>/pipeline/_index.json`: `giai_doan: "gd10_modules"`, danh sách module + owner, `cho_duyet` (true khi đã đưa cổng, đang chờ CTO/user), `updated_at` — để `delivery`/`partner` resume đúng chỗ. `cho_duyet: true` = resume KHÔNG tự đi tiếp, nhắc lại khối cổng.

## Ví dụ Case Management (rút gọn — cùng case với doc)

```text
Từ Domain (GĐ5): bounded context Case · Notification · Identity.
Từ Backlog (GĐ9): feature Create Case, Review, Search.

GÓC NHÌN LÃNH ĐẠO: Sự cố ở luồng hồ sơ → gọi Team A; ở thông báo → Team B; ở đăng nhập → Team C.
                   Mỗi phần một team, không chồng chéo.

MODULE MAP
  Case Management  ← context Case      · Owner: Team A · lõi (nhiều module nghe event của nó); phụ thuộc → Identity (đọc user)
  Notification     ← context Notify    · Owner: Team B · nghe event từ Case
  Identity         ← context Identity  · Owner: Team C · cấp danh tính/quyền; mọi module gọi để check permission
  (Lý do gộp Search vào Case: cùng data ownership "cases"; đã loại cách tách Search riêng vì sẽ chia đôi
   quyền sở hữu bảng cases. Đã cân gộp Notification vào Case — loại vì hai team, tần suất đổi khác nhau.)

MODULE CONTRACT — Case Management            Owner: Team A
  [Lãnh đạo]       : giữ toàn bộ vòng đời hồ sơ; hồ sơ lỗi → hỏi Team A.
  Responsibilities : tạo/cập nhật case · theo dõi trạng thái · giao reviewer.
  Owns             : bảng cases · vòng đời CaseStatus · event CaseCreated/CaseApproved/CaseEscalated.
  Does NOT own     : gửi thông báo (Team B) · danh tính người dùng (Team C) · thanh toán.
  Public API       : POST /cases · GET /cases · PATCH /cases/{id}/status  (đặc tả OpenAPI).
  Domain events    : phát CaseCreated, CaseApproved; nghe — không (module lõi).
  Permission       : Creator tạo · Reviewer duyệt · Auditor đọc · Admin cấu hình.
  Error codes      : CASE_REQUIRED_ATTACHMENT_MISSING · CASE_SELF_REVIEW_FORBIDDEN.
  Test contract    : Notification dựa trên event CaseApproved (contract test A↔B).

Cổng: mỗi module một owner, cases chỉ Team A sở hữu, phụ thuộc đi qua event/contract, 3 team chạy song song
      → trình bằng chứng, user (CTO) duyệt GO → bàn giao /delivery.
```

## Khi làm trong project workspace (`projects/<key>/`)

Nhận diện: user chỉ định `projects/<key>`, hoặc gói ngữ cảnh từ `resume`/`fanout` trỏ tới đó, hoặc `state/current.json` có trường `workspace`. Khi ấy:
- Bước 0 đọc thêm: `projects/<key>/constitution/` (nhất là `folders.md` + `definition-of-done.md`) và `progress/progress.json` — tìm task đang mở giao cho skill này (trường `owner`).
- Artifact người-đọc ghi vào ĐÍCH của task (trường `artifact` trong `progress.json`, đặt theo `folders.md`) — KHÔNG ghi bản chính vào `state/`. State máy riêng của skill (file json trạng thái) vẫn ở `state/project/<key>/` như cũ.
- Xong việc: báo user chạy `/checkpoint <task-id>` lấy phiếu rồi `/progress` đóng bước. Không tự lật done, không tự ghi `progress.json` — file đó một chủ (`progress`).
