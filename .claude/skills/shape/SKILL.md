---
name: shape
description: Quyết HÌNH HÀI hệ thống — architecture style, ranh giới module, data ownership, integration, auth/security, reliability, observability — TRƯỚC khi chọn framework. Sinh Architecture Brief + C4 (Context & Container) + Data Flow + Integration Model + Security Model + ADRs. Là GĐ6 (Solution Architecture) của pipeline Idea→Operate, nhận Domain Model từ `idea` (GĐ5), bàn giao sang `stack` (GĐ7). Dùng khi "định hình kiến trúc", "shape hệ thống", "chốt architecture", "vẽ C4", "ranh giới module", "modular monolith hay microservices", "chọn kiến trúc trước khi chọn framework", "domain xong rồi, kiến trúc thế nào".
---

# Shape — Solution Architecture (GĐ6): quyết hình hài hệ thống trước khi chọn framework

`shape` là **giai đoạn 6** của pipeline Idea→Operate. Vào bằng Domain Model (GĐ5), ra bằng **Architecture Brief + C4 (Context & Container) + Data Flow + Integration Model + Security Model + ADRs**. Một câu: chốt hệ thống có HÌNH HÀI gì — style, ranh giới module, ai sở hữu dữ liệu nào, nối với nhau cách nào, chặn ai bằng gì — **trước** khi bàn framework.

Phân vai — `shape` chỉ lo GĐ6, không lấn:
- `idea` = GĐ0–5, dừng ở Domain Model. `shape` **nhận** Domain đó, không hỏi lại WHY/WHAT, không làm lại domain.
- `stack` = GĐ7, chọn framework/DB/lib **hiện thực** cái shape này. `shape` chốt HÌNH, `stack` chốt CÔNG CỤ — "dùng NestJS/Postgres" là việc của `stack`, KHÔNG chốt ở đây.
- `partner` = điều phối cả chuỗi 15 giai đoạn; gọi `shape` khi tới GĐ6. `shape` cũng chạy độc lập được (có Domain Model là chạy).
- `frame` / `skeleton` (GĐ8) = đóng khung một lát cắt / dựng live slice để code. `shape` không viết code, chỉ định hình.
- `atlas`/`explain` = hiểu code cũ. Brownfield thì `shape` ĐỌC `.ai-understanding/`, không dựng lại.

Nguyên tắc cốt: **Architecture trước, framework sau** (A3-#2). Chọn style/boundary/integration/security vì domain và NFR đòi, không vì "team quen React/Spring". Framework là chuyện của `stack`.

Playbook gốc: `quy-trinh-idea-to-operate.md` ở gốc project, mục "## Giai đoạn 6 — Solution Architecture (SHAPE)". Lấy template + ví dụ Case Management từ đó, không tự chế khung mới. `shape` bám đúng các ô của mục đó (Mục tiêu / Chủ sở hữu-Người duyệt / Artifact / Đủ-là-đủ / Góc nhìn lãnh đạo / Cổng).

## Luật cứng

- **Hợp đồng đọc-được-3-tầng (lý do skill tồn tại — không bao giờ bỏ).** Người đọc artifact là đội của DOANH NGHIỆP KHÁCH HÀNG — CTO, business, dev — người NGOÀI, không biết nội bộ. Mọi artifact PHẢI: (1) MỞ bằng **Góc nhìn lãnh đạo** — ĐÚNG 1–3 thứ CEO/CTO nhìn để biết on-track, ngôn ngữ nghiệp vụ, không jargon; (2) RỒI mới tới chi tiết kỹ thuật đủ để DEV hành động; (3) 1 trang, scan 2–3 phút. Không viết cho riêng mình đọc.
- **ADR là nơi lãnh đạo quản rủi ro mà không cần đọc code.** Mỗi quyết định lớn → 1 ADR: *Quyết định · Bối cảnh · Lựa chọn · Phương án đã loại (vì sao) · Hệ quả*. Đọc danh sách ADR + "cái đã loại" là hiểu "vì sao hệ thống có hình này", truy vết được. Không có phương án đã loại → chưa phải quyết định, chỉ là mặc định.
- **Đủ-là-đủ.** Độ sâu mỗi phần tỉ lệ RỦI RO/ẨN SỐ, không theo vị trí trong luồng. Domain nhỏ/quen, một service, không tích hợp lạ → mỗi ô bảng vài dòng + 1 C4 Context + 2–3 ADR là đủ. Nhiều context, tích hợp bên thứ ba, dữ liệu nhạy cảm, NFR ngặt → đầy đủ C4 Container + Data Flow + Security Model + ADR dày. **KHÔNG bao giờ bỏ một artifact đã liệt kê — chỉ rút gọn độ sâu.** Bỏ artifact là rớt cổng.
- **Architecture trước, framework sau.** Đang bàn kiến trúc mà buột chọn "dùng React/NestJS/Postgres" → dừng, ghi thành đề mục cho `stack`, không chốt ở đây. Một ADR KHÔNG được chứa tên framework như một quyết định — chỉ được nêu như ràng buộc nếu Domain/NFR ép.
- **Không lấn vai.** Không hỏi lại WHY/WHAT/MVP (đã chốt GĐ1–4). Không làm lại domain (GĐ5). Không chọn stack (GĐ7). Không viết code / cắt slice (GĐ8/11). Lỡ đụng câu thuộc GĐ khác → ghi thành open question, chuyển đúng chỗ, không trả lời non.
- **Bám nguồn.** Mọi ranh giới module bám bounded context GĐ5; mọi NFR/security bám Requirement/PRD. Không bịa NFR, không đẻ context mới không có trong domain. NFR thiếu số → ghi open-Q, không chế ngưỡng.
- **Không tự ghi artifact vào repo code.** Mặc định ghi vào `state/project/<project-name>/pipeline/shape.md`. Muốn đưa vào repo đích → HỎI user trước. Chỉ greenfield mới ghi thẳng `<project>/`.
- **Cấm câu phủ định cứng khi phản biện** (kế thừa `partner`): không "không thể", "sai rồi", "không làm được". Nêu ràng buộc → kèm một lối đi tiếp.
- **Một cụm câu hỏi mỗi lượt** (≤3 câu cùng chủ đề, ưu tiên AskUserQuestion khi là lựa chọn), không dồn.

## Đầu vào — đọc trước khi hỏi

- Domain Model (GĐ5) từ `idea`: `state/project/<project-name>/ideas/<slug>.md` (+ `<slug>.json`) — lấy bounded context, entity, aggregate, business rule bất biến, domain event, data ownership, open-Q còn treo. Đây là NGUỒN RANH GIỚI: mỗi module boundary GĐ6 phải nối lại được về một bounded context GĐ5, không tự vẽ lại.
- Requirement + NFR + PRD (GĐ2–4) trong cùng file ý: lấy các con số NFR (P95, uptime, số user, compliance) — chúng lái architecture style + reliability + performance + security. Thiếu số → ghi open-Q, không bịa.
- `state/current.json` — project đang mở.
- `.ai-understanding/` (của `atlas`, nếu brownfield) — kiến trúc/ràng buộc code cũ, để không đề kiến trúc chửi nhau với hiện trạng.

Nếu user ĐÃ đưa Domain Model trong prompt hoặc file → chạy được ngay, kèm ⚠️ cảnh báo (theo mục "Đầu vào ngoài state" bên dưới); nếu KHÔNG có gì trong state lẫn prompt/file → mới gợi ý bàn giao ngược `/idea` (hoặc `/partner`) chốt GĐ5. Dù nguồn nào, KHÔNG tự bịa domain — mảnh thiếu ghi thành open-Q.

## Đầu vào ngoài state (nới — nhận prompt/file thay cho artifact GĐ trước)

Không có Domain Model trong state VẪN chạy được nếu user mô tả trực tiếp trong prompt, dán nội dung, hoặc trỏ một file ngoài. Thứ tự ưu tiên: (1) đọc state pipeline; (2) không có thì nhận Domain Model từ prompt/file user đưa; (3) vẫn không có gì thì mới gợi ý chạy /idea.

Khi chạy bằng nguồn NGOÀI (không phải Domain Model của GĐ5 đã qua cổng), in NGUYÊN block cảnh báo này NGAY TRƯỚC khi làm, rồi VẪN tiếp tục — đây là cảnh báo, KHÔNG phải chặn:

```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Domain Model" lấy từ prompt/file bạn đưa, CHƯA qua cổng GĐ5 (skill /idea).
- Rủi ro: (1) chưa truy vết ngược được về pipeline; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /idea trước để có "Domain Model" đã qua cổng.
```

Nếu Domain Model user đưa thiếu mảnh quan trọng → vẫn chạy, ghi rõ mảnh thiếu thành open-Q, KHÔNG tự bịa cho đủ.

## Bước 0 — Xác định project

Theo thứ tự (giống `idea`/`partner`):
1. Argument truyền vào (vd `/shape /Users/foo/my-app` hoặc `/shape loyalty-app`).
2. Đường dẫn/slug nhắc trong tin nhắn.
3. `state/current.json`.
4. Chưa có → hỏi một slug kebab-case ngắn; nếu là ý mới hoàn toàn (chưa qua `idea`) → chỉ về `/idea` trước, vì `shape` cần Domain Model làm đầu vào.

Có path thì xác nhận tồn tại:
```bash
ls <project-path> 2>/dev/null | head -5 || echo "NOT_FOUND"
```
`NOT_FOUND` → báo lỗi, hỏi lại. Có nhiều `<slug>` trong `ideas/_index.json` → liệt kê, hỏi shape cho ý nào.

## Thân — sinh bộ artifact SHAPE (bám template GĐ6)

Thứ tự đúng (A3-#2, không đảo): `Requirement + NFR + Domain → Architecture style → Principles → Integration pattern → Deployment model → (rồi mới bàn giao) Framework(GĐ7)`.

Hỏi từng cụm (≤3 câu, AskUserQuestion cho câu chốt) → tóm tắt hiểu → chốt từng ô. Ô nào rủi ro cao thì brainstorm ≥2 hướng, ghi vì sao loại. **Mỗi artifact MỞ bằng 1–3 dòng Góc nhìn lãnh đạo rồi mới tới chi tiết dev.** Độ sâu theo Đủ-là-đủ.

### 1. Architecture Brief — bảng quyết định (bám đúng khung doc GĐ6)

Điền lần lượt, mỗi dòng bám một đòi hỏi từ Domain/NFR:
```text
ARCHITECTURE BRIEF — <tên>
Architecture style : modular monolith | microservices | event-driven | serverless — theo domain complexity + quy mô đội, không theo mốt.
Module boundary    : module nào sở hữu nghiệp vụ nào — bám bounded context GĐ5 (một context ≠ một module được, nhưng phải giải thích).
Data ownership     : DB chung | DB per service | schema-per-module; ai đọc/ghi bảng nào; cấm cross-module query trực tiếp nếu đã tách.
Integration        : REST | GraphQL | event | queue | batch — cho từng đường: UI↔hệ thống, nội bộ giữa module, ra bên thứ ba.
Auth               : RBAC | ABAC | SSO | OAuth — ai làm được gì.
Security           : threat model (STRIDE) · phân loại dữ liệu · audit.
Reliability        : retry · timeout · circuit breaker · fallback.
Performance        : caching · indexing · async.
Observability      : log · metric · trace · alert (kèm ngưỡng alert).
Deployment         : cloud | on-prem | hybrid.
Compliance         : PDPA/GDPR · retention.
```
**Đủ-là-đủ:** chọn được style + boundary + integration + auth/security. Ô rủi ro thấp → vài chữ. Ô nào không liên quan (vd không compliance) → ghi "không áp dụng + lý do 1 dòng", KHÔNG bỏ trống. Không bịa NFR chưa ai đòi.
**Góc nhìn lãnh đạo:** bảng này ĐÃ là góc nhìn lãnh đạo — mỗi dòng một quyết định nghiệp vụ đọc được, không cần đọc code. Đặt nó lên ĐẦU brief, kèm 1–2 câu "hệ thống có hình gì và vì sao hình đó hợp với rủi ro/quy mô này".

### 2. C4 — Context (bắt buộc) + Container (khi có nhiều module/tích hợp)

- **C4 Context** (BẮT BUỘC, kể cả việc nhỏ, vẽ tay/ASCII cũng tính): hệ thống là một hộp, xung quanh là ai dùng + hệ thống ngoài nào nối vào (CRM, SSO, Notification...). Ai gọi ai. Đây là bức tranh cho lãnh đạo — "hệ thống ngồi ở đâu trong thế giới", quản rủi ro tích hợp không cần hiểu kỹ thuật.
- **C4 Container**: bên trong hộp có những khối chạy được nào (app/service/DB/queue/adapter) + công nghệ ở mức LOẠI (không tên framework — đó là GĐ7), nói chuyện với nhau qua giao thức gì. Bật khi có ≥2 module hoặc tích hợp bên ngoài; rủi ro thấp có thể gộp vào Context nhưng phải nêu rõ container nào tồn tại.

Diễn giải mỗi sơ đồ bằng 1–2 câu phẳng, không để lãnh đạo tự đoán mũi tên. Không có sơ đồ = chưa đạt cổng.

### 3. Data Flow + Integration Model

- **Data Flow**: một luồng nghiệp vụ chính đi xuyên các container — dữ liệu vào đâu, ai sở hữu, ra sao (vd "tạo case → lưu → phát CaseCreated → thông báo"). Kể bằng câu, **gắn mỗi bước vào một domain event GĐ5**; bám data ownership GĐ5.
- **Integration Model**: mỗi tích hợp ra ngoài một dòng — pattern (REST/event/batch), đồng bộ hay bất đồng bộ, ai chịu lỗi khi bên kia sập, có retry/timeout/fallback không, ai sở hữu contract. Bám open-Q integration còn treo từ PRD/Domain (chốt luôn ở đây).

### 4. Security Model

Phân loại dữ liệu (Public/Internal/Confidential) + auth model (RBAC/ABAC + role ↔ quyền) + audit (cái gì phải bất biến/append-only) + threat model (STRIDE gọn cho đường vào chính) + compliance nếu có.
**Đủ-là-đủ:** dữ liệu nhạy cảm/nhiều tích hợp → làm đủ threat model + classification. Nội bộ, ít nhạy cảm → vài dòng: auth model + có/không audit, ghi lý do gọn.
**Góc nhìn lãnh đạo:** một câu — "dữ liệu nhạy nhất là gì, ai được xem, có dấu vết audit không". Đây là câu CTO/pháp lý hỏi đầu tiên.

### 5. ADRs — mỗi quyết định lớn một bản ghi

```text
ADR-00x <tên quyết định>
Bối cảnh   : ràng buộc (team, domain, NFR) dẫn tới quyết định.
Quyết định : chọn gì.
Phương án đã loại : cái gì, VÌ SAO loại.
Hệ quả     : được gì, mất gì, đánh đổi gì về sau.
```
**Đủ-là-đủ:** tối thiểu ADR cho style, boundary, integration lớn, data ownership. Việc nhỏ 2–3 ADR; rủi ro cao mỗi quyết lớn một ADR. Đây cũng là chỗ trả lời open-Q còn treo từ GĐ trước.
**Góc nhìn lãnh đạo:** đọc danh sách tiêu đề ADR + "cái đã loại" là biết "vì sao hệ thống có hình này" — CTO audit được sau 6 tháng, không cần đọc code.

## Tự soi trước khi chốt (bắt buộc)

Trước khi đưa cổng, tự trả các câu — vướng câu nào sửa trước:
1. **Lãnh đạo đọc được đoạn đầu không?** Bảng quyết định + Góc nhìn lãnh đạo đứng trước mỗi artifact, ngôn ngữ nghiệp vụ, không jargon, đúng 1–3 thứ để biết on-track?
2. **Dev đủ hành động chưa?** Có style + boundary + integration + auth + ≥1 sơ đồ C4 Context để đội biết module nào sở hữu gì, nối nhau ra sao, chặn ai bằng gì, và bước sang chọn stack (GĐ7)?
3. **Đúng + đủ các phần đã liệt kê?** Đủ Architecture Brief + C4 (Context & Container) + Data Flow + Integration + Security + ADRs? Mỗi ranh giới module nối được về một bounded context GĐ5? Mỗi NFR bám PRD, không bịa? Mỗi quyết định lớn có ADR kèm phương án đã loại?
4. **Có lỡ chọn framework (việc `stack`) không?** Không tên framework nào bị chốt lén trong Brief/ADR.

## Cổng go/no-go + AI duyệt (theo A5)

Cổng chuẩn của GĐ6 (bám doc): **"Architecture đủ vững để chọn stack & dựng live slice chưa?"**

`shape` (đóng vai Kiến trúc sư/CTO theo A5) tự DUYỆT trước khi mời user quyết, kiểm 4 điều — thiếu bất kỳ điều nào → **no-go**, quay lại vá, KHÔNG bàn giao:
1. Đủ bộ artifact (Brief + C4 Context + Container + Data Flow + Integration + Security + ADRs), không bỏ cái nào — chỉ rút gọn độ sâu.
2. Module boundary bám đúng bounded context GĐ5; data ownership rõ, không mơ hồ "ai cũng đọc được".
3. Mỗi quyết định lớn có ADR + phương án đã loại; open-Q integration/reliability từ GĐ trước đã chốt hoặc ghi rõ còn treo sang GĐ7.
4. Không có tên framework nào bị chốt lén trong Brief/ADR (đó là việc `stack`).

Qua 4 điều → đưa khối cổng, chờ user:

```
═══ CỔNG GĐ6 — SHAPE: <tên hệ thống> ═══
Style / Boundary / Data / Integration / Auth / Security: đã chốt.
C4 Context: đã có · ADR: <n> bản (mỗi cái có phương án đã loại).
Open-Q còn treo → GĐ7: <liệt kê nếu có>
Câu hỏi cổng: Architecture đủ vững để chọn stack & dựng live slice chưa?
════════════════
```

AI duyệt vai **CTO/Kiến trúc sư** (Security review song song) — chỉ ra chỗ boundary lệch domain, ADR thiếu phương án loại, NFR chưa có chỗ đỡ trong architecture. KHÔNG tự bấm GO thay user. User (giữ vai CTO) mới quyết. No-go/còn băn khoăn → ghi thành open-Q, làm rõ phần thiếu, không tự trôi sang GĐ7.

## Bàn giao sang `stack` (GĐ7)

```
═══ BÀN GIAO — SHAPE → STACK: <tên hệ thống> ═══
Hình đã chốt      : <style + số module + integration chính + deployment>
Ràng buộc cho stack: <NFR/security/skill đội ép chọn tool ra sao — vd "P95<500ms", "team thạo TS", "audit bất biến">
Open-Q chuyển tiếp : <cái gì để GĐ7 chốt — vd realtime vs batch nếu còn treo>
Artifact          : <đường dẫn shape.md>
→ Chọn framework/DB/lib hiện thực hình này (GĐ7): chạy /stack
→ Muốn dựng ngay một lát cắt sống để validate shape: chạy /skeleton (live slice GĐ8) hoặc /frame
→ Cần hiểu code cũ shape sẽ đụng vào: chạy /atlas hoặc /explain
→ Cần điều phối cả pipeline: chạy /partner
════════════════
```
Chỉ liệt kê, KHÔNG tự chọn hộ user chạy skill nào tiếp.

## State

Ghi `state/current.json`:
```json
{ "project": "<project-path>", "updated_at": "<ISO 8601>" }
```

Ghi artifact vào `state/project/<project-name>/pipeline/shape.md` (Architecture Brief + C4 + Data Flow + Integration + Security + ADRs). Cập nhật `state/project/<project-name>/pipeline/shape.json`:
```json
{
  "project": "/duong/dan/project",
  "slug": "case-management",
  "giai_doan": "gd6_shape",
  "cho_duyet": false,
  "updated_at": "<ISO 8601>",
  "style": "modular_monolith",
  "modules": ["Case", "Identity-adapter", "Notification-adapter"],
  "da_chot": ["ADR-001 modular monolith (loại: microservices)", "ADR-002 batch CRM (loại: realtime)"],
  "dang_mo": ["ngưỡng retention audit log chốt ở GĐ7?"],
  "artifact_path": "state/project/<project-name>/pipeline/shape.md",
  "handoff_to": "stack"
}
```
`cho_duyet: true` = đã mở cổng, chờ user — resume không tự đi tiếp, nhắc lại khối cổng. KHÔNG ghi vào repo code trừ khi user đồng ý; greenfield mới ghi thẳng `<project>/`.

## Ví dụ Case Management (rút gọn — cùng case với doc quy trình)

```
Nhận từ idea (GĐ5): context Case Management (lõi) | Identity (ngoài) | Notification (ngoài).
Rule bất biến: "Reviewer không tự duyệt case mình tạo", "case >7 ngày → tự Escalated". Open-Q PRD: đồng bộ CRM realtime hay batch?

ARCHITECTURE BRIEF — Case Management
Góc nhìn lãnh đạo: Một khối triển khai gọn cho đội 6 người, 3 module rõ ranh giới;
  dữ liệu KH xếp "Confidential" + audit log không sửa được; rủi ro lớn nhất đã khoá bằng 2 ADR.
Style       : Modular monolith (3 module: Case · Identity-adapter · Notification-adapter).
Boundary    : module Case sở hữu toàn bộ vòng đời case; ra ngoài qua adapter (bám bounded context GĐ5).
Data        : một DB, schema-per-module, KHÔNG cross-module query trực tiếp.
Integration : REST cho UI; domain events nội bộ; CRM đồng bộ batch hằng đêm (chốt open-Q PRD).
Auth        : RBAC (Creator/Reviewer/Auditor/Admin) qua SSO công ty.
Security    : dữ liệu KH = "Confidential"; audit log append-only; threat model STRIDE cho luồng duyệt.
Reliability : retry + timeout cho CRM batch; ngoài giờ vẫn tạo case được (offline-tolerant intake).
Observability: structured log + RED metrics + trace; alert P95>500ms & error>1%.
Deployment  : cloud, 1 region, blue-green.

C4 Context : [Creator/Reviewer/Auditor] → (Case Mgmt) → [SSO] [CRM] [Email].
Data Flow  : tạo case → Case module ghi cases/attachments/status_history → phát CaseCreated
             → Notification-adapter gửi email; đêm batch đẩy sang CRM.
ADR-001 Modular monolith thay vì microservices (đội 6 người, 1 domain) — loại: microservices (quá tải vận hành).
ADR-002 Batch CRM thay vì real-time — loại: real-time (CRM rate-limit, không cần tức thời).

Cổng: Architecture đủ vững để chọn stack & dựng live slice → user (CTO) duyệt GO.
Bàn giao: chọn framework hiện thực shape này → /stack (ràng buộc: P95<500ms, team thạo TS, audit bất biến);
  hoặc build slice "tạo case" để validate → /skeleton hoặc /frame.
```

## Khi làm trong project workspace (`projects/<key>/`)

Nhận diện: user chỉ định `projects/<key>`, hoặc gói ngữ cảnh từ `resume`/`fanout` trỏ tới đó, hoặc `state/current.json` có trường `workspace`. Khi ấy:
- Bước 0 đọc thêm: `projects/<key>/constitution/` (nhất là `folders.md` + `definition-of-done.md`) và `progress/progress.json` — tìm task đang mở giao cho skill này (trường `owner`).
- Artifact người-đọc ghi vào ĐÍCH của task (trường `artifact` trong `progress.json`, đặt theo `folders.md`) — KHÔNG ghi bản chính vào `state/`. State máy riêng của skill (file json trạng thái) vẫn ở `state/project/<key>/` như cũ.
- Xong việc: báo user chạy `/checkpoint <task-id>` lấy phiếu rồi `/progress` đóng bước. Không tự lật done, không tự ghi `progress.json` — file đó một chủ (`progress`).
