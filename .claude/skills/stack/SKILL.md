---
name: stack
description: Chọn framework/ngôn ngữ/infra bằng TIÊU CHÍ có điểm (fit domain/team/scale/NFR/enterprise/hiring/maintainability), kèm lý do + phương án đã loại — chỉ SAU khi kiến trúc đã chốt. Sinh Tech Decision Matrix + ADR chọn framework (+ Spike Result nếu có ẩn số). Là GĐ7 của pipeline Idea→Operate, nhận Architecture Brief từ `shape` (GĐ6), bàn giao skeleton cho `skeleton` (GĐ8). Dùng khi "chọn stack", "dùng framework nào", "so sánh NestJS vs Spring", "React hay Vue", "ngôn ngữ/DB nào cho cái này", "chốt tech stack", "đã có kiến trúc rồi, giờ chọn công cụ gì".
---

# Stack — Chọn công cụ hiện thực cái shape đã chốt (GĐ7 · TOOLS)

`stack` là **Giai đoạn 7** của pipeline Idea→Operate. Nó nhận **hình hài hệ thống** đã chốt và trả lời đúng một câu: *dựng cái shape này bằng CÔNG CỤ nào* — framework, ngôn ngữ, DB, hạ tầng. Chọn bằng ma trận tiêu chí **có điểm**, không theo "đang hot". Sinh ra **Tech Decision Matrix + ADR chọn framework** (+ **Spike Result** nếu có ẩn số cần đo). Framework chỉ là tool hiện thực cái **shape** kiến trúc đã chốt ở GĐ6 — nên `stack` KHÔNG chạy trước khi có kiến trúc.

Phân vai với các skill khác — không lấn sân ai:
- `idea` = GĐ0–5, làm rõ nhu cầu → Domain Model, DỪNG trước kiến trúc. Không bàn lại giá trị/scope, không chọn công cụ.
- `shape` = GĐ6, chốt **hình hài** hệ thống (Architecture Brief: style, boundary, integration, auth, deployment). Là đầu vào BẮT BUỘC của `stack`.
- `stack` = GĐ7 (skill này). Nhận Architecture Brief, chọn stack **bằng tiêu chí**, KHÔNG vẽ lại kiến trúc, bàn giao sang `skeleton`.
- `skeleton` = GĐ8, dựng lát cắt sống end-to-end bằng đúng stack `stack` chốt, chứng minh stack + kiến trúc đúng. `stack` KHÔNG viết code sản phẩm — chỉ spike ném-đi để đo ẩn số.
- `frame` = đóng khung + code một slice (GĐ8/11). `partner` = điều phối trọn pipeline 15 giai đoạn, có thể gọi `stack` như một bước. `review` = đào gap sâu.

`stack` chạy được độc lập (user đã có Architecture Brief) HOẶC do `partner` gọi.

Playbook gốc (template + ví dụ đầy đủ GĐ7): `quy-trinh-idea-to-operate.md` ở gốc project, mục "## Giai đoạn 7 —". Việc lớn/rủi ro cao thì mở file gốc lấy template đầy đủ.

## Luật cứng

- **Hợp đồng đọc-được 3 tầng (lý do skill tồn tại).** Người đọc Tech Decision Matrix là đội của DOANH NGHIỆP KHÁCH HÀNG — CTO, business, dev — người NGOÀI, không có kiến thức nội bộ. Mọi artifact PHẢI: MỞ bằng **Góc nhìn lãnh đạo** (đúng 1–3 thứ CEO/CTO nhìn để duyệt trên NIỀM TIN: chọn gì · vì sao · loại gì · rủi ro/chi phí — ngôn ngữ nghiệp vụ, không jargon), RỒI mới tới ma trận điểm + ADR đủ để DEV hành động. 1 trang, scan 2–3 phút. Không viết cho riêng mình đọc.
- **Chọn bằng tiêu chí có điểm, không theo "đang hot".** Mỗi hạng mục là một ma trận: tiêu chí × trọng số × điểm từng candidate. Không có điểm số thì không phải quyết định, chỉ là ý thích. Mọi ô điểm truy vết được — "đang hot"/"quen tay" KHÔNG phải lý do, phải neo vào một tiêu chí.
- **Mỗi quyết định lớn ghi LÝ DO + phương án đã loại.** ADR bắt buộc cho mỗi lựa chọn lớn: Quyết định · Bối cảnh · Đã loại & vì sao · Hệ quả. Không ghi cái đã loại = không audit lại được vì sao không chọn nó.
- **Còn ẩn số → spike thực đo, không đoán.** Rủi ro cao (NFR chưa chắc đạt, công nghệ mới với đội) → đề xuất spike time-box, ghi **kết quả đo thật** vào matrix. `stack` không tự dựng thay dev; nêu ẩn số + đề xuất time-box, dev/user chạy rồi báo số. Không có số đo thật cho ẩn số rủi ro cao = ma trận chưa đủ tin.
- **Đủ-là-đủ.** Độ sâu tỉ lệ RỦI RO/ẨN SỐ, không theo vị trí trong luồng. Hạng mục quen thuộc / ràng buộc đã ép sẵn 1 lựa chọn → ma trận vài dòng + 1 ADR ngắn, ghi lý do. Hạng mục mới / rủi ro cao / đắt-khó-đổi → ma trận đầy đủ + spike thực đo. KHÔNG bao giờ bỏ bước (vẫn có matrix + ADR), chỉ rút gọn độ sâu.
- **Kiến trúc trước, framework sau.** Chưa có Architecture Brief (GĐ6) → KHÔNG chọn stack. Chọn công cụ trước khi biết hình hài là chọn mù (ngược thứ tự A3-#2). Thiếu → dừng, chỉ user sang `/shape` trước. Không tự đoán kiến trúc để chọn tool.
- **Không lấn vai.** Không sửa lại kiến trúc/boundary (việc của `shape`); không viết code slice (việc của `skeleton`/`frame`); không phân rã backlog/sprint (GĐ9). Nếu chọn stack lộ ra kiến trúc sai → ghi làm open question, trả ngược `shape`, không tự vá.
- **Cấm câu phủ định cứng khi phản biện một candidate** (kế thừa `partner`): không "framework này sai", "không dùng được". Loại một candidate thì nêu điểm nó thua theo tiêu chí + vẫn ghi nhận điểm mạnh + kèm điều kiện/ngưỡng ("candidate B lệ thuộc vendor X; hợp nếu chấp nhận khoá vào cloud đó").
- **Không tự ghi artifact vào repo code** trừ khi user đồng ý (theo `idea`). Mặc định ghi vùng state của skill; greenfield thì ghi thẳng vùng project của skill. Muốn đưa ADR vào repo đích (vd `docs/adr/`) → HỎI trước.

## Đầu vào — đọc trước khi chọn

- **Architecture Brief (GĐ6, `shape`)** — bắt buộc. Đọc: architecture style + module boundary + data ownership + integration + auth + security + reliability + performance + observability + deployment + compliance. Đây là RÀNG BUỘC ép danh sách candidate và trọng số tiêu chí. Không có → dừng (xem Bước 0).
- **Domain Model + PRD/NFR (GĐ5, GĐ2–4)** nếu có trong state — lấy domain complexity (module rõ hay logic rối) + con số NFR (P95, uptime, tải) để chấm "Fit domain" và "Fit scale".
- `state/project/<project-name>/pipeline/shape.md` + `pipeline/_index.json` + `state/current.json` — biết đang ở đâu, đã chốt gì, nối mạch, không bịa lại.
- `.ai-understanding/` (của `atlas`, nếu brownfield) — stack đang tồn tại trong code cũ (ngôn ngữ, framework, DB, hạ tầng). Brownfield thì "Fit team đã biết" và "Fit maintainability" phải tính cả stack hiện có; một stack mới phải sống chung được, tránh chọn cái xé lẻ hệ thống.
- `state/project/<project-name>/user-state.json` (của `explain`, chỉ ĐỌC) — lấy `level` để hiệu chỉnh độ dài diễn giải, không hỏi lại mức.

## Đầu vào ngoài state (nới — nhận prompt/file thay cho artifact GĐ trước)

Không có Architecture Brief trong state VẪN chạy được nếu user mô tả trực tiếp trong prompt, dán nội dung, hoặc trỏ một file ngoài. Thứ tự ưu tiên: (1) đọc state pipeline; (2) không có thì nhận Architecture Brief từ prompt/file user đưa; (3) vẫn không có gì thì mới gợi ý chạy /shape.

Khi chạy bằng nguồn NGOÀI (không phải Architecture Brief của GĐ6 đã qua cổng), in NGUYÊN block cảnh báo này NGAY TRƯỚC khi làm, rồi VẪN tiếp tục — đây là cảnh báo, KHÔNG phải chặn:

```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Architecture Brief" lấy từ prompt/file bạn đưa, CHƯA qua cổng GĐ6 (skill /shape).
- Rủi ro: (1) chưa truy vết ngược được về pipeline; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /shape trước để có "Architecture Brief" đã qua cổng.
```

Nếu Architecture Brief user đưa thiếu mảnh quan trọng → vẫn chạy, ghi rõ mảnh thiếu thành open-Q, KHÔNG tự bịa cho đủ.

## Bước 0 — Xác định project

Lấy project theo thứ tự (giống `idea`/`partner`):
1. Argument truyền vào (vd `/stack /Users/foo/case-app`).
2. Đường dẫn/tên nhắc trong tin nhắn.
3. `state/current.json`.
4. Greenfield tiếp nối từ `idea`/`shape` → dùng `<project-name>` = slug đã có ở GĐ trước; không cần verify folder.

Có path thì xác nhận tồn tại:
```bash
ls <project-path> 2>/dev/null | head -5 || echo "NOT_FOUND"
```
`NOT_FOUND` → báo lỗi, hỏi lại.

**Cổng đầu vào:** tìm Architecture Brief GĐ6 theo thứ tự ưu tiên ở mục "Đầu vào ngoài state": (1) state `pipeline/shape.md`; (2) user đã đưa trong prompt/file → chạy KÈM ⚠️ block cảnh báo rồi tiếp tục; (3) vẫn không có gì → gợi ý một dòng: *"Chưa có Architecture Brief (GĐ6). `stack` chọn tool cho một shape đã chốt. Chạy `/shape` trước, hoặc dán/trỏ Architecture Brief để chạy kèm cảnh báo."* Không tự chế kiến trúc để chọn tool.

## Thân — sinh Tech Decision Matrix + ADR (+ Spike)

Bám đúng template GĐ7 của `quy-trinh-idea-to-operate.md` (8 ô: Mục tiêu / Chủ sở hữu-Người duyệt / Chạy song song / Artifact / Ví dụ / Đủ-là-đủ / Góc nhìn lãnh đạo / Cổng). Chủ sở hữu = **Kiến trúc sư / Tech lead** · Người duyệt = **CTO**. Chạy song song với: lập kế hoạch live slice (GĐ8).

### 1. Liệt kê hạng mục cần chọn (từ Architecture Brief)

Từ bảng quyết định GĐ6 rút ra các "ô còn để mở tool": integration REST → chọn web framework; data ownership → chọn DB + ORM; auth RBAC/SSO → chọn auth provider; deployment cloud → chọn nền tảng; queue/cache nếu shape có. Ràng buộc đã ép sẵn (vd doanh nghiệp bắt buộc on-prem Java, hoặc DB đã ép bởi shape/code cũ) → ghi thẳng 1 dòng "chọn X vì Y", KHÔNG mở ma trận giả.

### 2. Tech Decision Matrix — mỗi hạng mục rủi ro cao một bảng có điểm

Tiêu chí lấy từ template GĐ7 — **có trọng số, có điểm từng candidate**:
```text
TECH DECISION MATRIX — <hạng mục, vd: Backend framework>
Tiêu chí                                     | Trọng số | Cand A | Cand B | Cand C
Fit domain (bám bounded context GĐ5/6)       |   ...    |  điểm  |  ...   |  ...
Fit team (đã biết chưa? learning curve)      |          |
Fit scale / NFR (P95, uptime, tải — số GĐ2–4)|          |
Fit enterprise (auth · audit · log · monitor)|          |
Fit testing (unit · integration · e2e · contract) |
Fit hiring (thị trường tuyển)                |          |
Fit ecosystem / vendor / cloud               |          |
Fit maintainability (2 năm nữa còn dễ nuôi?) |          |
TỔNG (có trọng số)                           |          |
=> Chọn: ___ · Lý do: ___ · Đã loại & vì sao: ___
```
Trọng số do RÀNG BUỘC kiến trúc + NFR quyết, không đều nhau. NFR P95 gắt → "Fit scale" nặng; đội nhỏ giao gấp → "Fit team" nặng. Ghi trọng số ra để truy vết được. Chọn 5–8 tiêu chí liên quan nhất; rủi ro thấp → cắt bớt tiêu chí ít liên quan, giữ tối thiểu domain/team/NFR/maintainability + có điểm. Không bịa candidate cho đủ 3 cột.

**Đủ-là-đủ:** ma trận **có điểm** (không để trống) + TỔNG có trọng số + dòng "Chọn/Lý do/Đã loại". Hạng mục nhỏ/đã bị ràng buộc ép → 3–4 tiêu chí liên quan là đủ, ghi rõ ràng buộc. Hạng mục lớn/rủi ro → đủ 8 tiêu chí + spike.

### 3. ADR cho mỗi quyết định lớn

```text
ADR-00x — Chọn <công cụ> cho <hạng mục>
Bối cảnh   : ràng buộc từ Architecture Brief + NFR liên quan.
Quyết định : chọn gì (stack cụ thể, vd NestJS + PostgreSQL + Prisma).
Lý do      : neo vào tiêu chí thắng điểm.
Đã loại    : candidate nào, thua ở tiêu chí nào (ghi nhận cả điểm mạnh của nó).
Hệ quả     : ràng buộc kéo theo (hiring, license, vendor lock, migration path).
```
ADR là thứ CTO đọc để biết "vì sao stack có mặt này" mà không cần đọc code.

### 4. Spike Result — chỉ khi có ẩn số / rủi ro cao

Ẩn số kỹ thuật chưa chắc (NFR có đạt không? tích hợp có chạy không? giới hạn vendor?) mà bảng điểm không trả lời chắc → đề xuất time-box, dựng thử, **đo thật**, ghi kết quả. `stack` không tự build sản phẩm — spike là code ném-đi để HỌC, kết quả có thể vứt. Không có ẩn số → bỏ, ghi 1 dòng "không spike vì stack quen, NFR dư biên".
```text
SPIKE RESULT — <ẩn số>
Câu hỏi   : cần chứng minh điều gì (vd "GET /cases 10k bản ghi có đạt P95<500ms?").
Time-box  : vd 1–2 ngày.
Đo được   : số thật (vd P95 ~210ms → đạt).
Kết luận  : chốt / đổi lựa chọn / cần thêm.
```

### Góc nhìn lãnh đạo — VIẾT ĐẦU artifact (đọc trước, 30 giây)

Mở artifact bằng đúng thứ CEO/CTO cần, TRƯỚC ma trận điểm:
```text
─── GÓC NHÌN LÃNH ĐẠO (đọc trước, 30 giây) ───
Chọn         : <công cụ> cho <hạng mục>.
Vì sao       : <1 câu nghiệp vụ — hợp đội / đủ tốc độ yêu cầu / nuôi được lâu>.
Đã loại      : <candidate> — <lý do ngắn, không jargon>.
Rủi ro/chi phí: <đã hết bằng spike? còn treo gì? khoá vendor? tốn kém gì khi sai>.
```
Ngôn ngữ nghiệp vụ: "chọn NestJS vì đội đã thạo nên lên nhanh & rẻ, đủ tốc độ yêu cầu; loại Spring vì đội chưa quen, lên chậm; loại Django vì mô hình module kém rõ cho case này." CTO đọc băng đầu là duyệt được công cụ trên niềm tin, không cần đọc điểm từng ô — quyết định **truy vết được, không cảm tính**, quản được rủi ro & chi phí mà không cần đọc code.

## Tự soi trước khi chốt

Trước khi ghi artifact, trả lời được cả ba mới chốt; vướng cái nào thì sửa trước:
- **Lãnh đạo đọc được băng đầu không?** Người không viết code, đọc "Góc nhìn lãnh đạo" 30 giây, có duyệt được lựa chọn công cụ này không — chọn gì + đã loại gì + vì sao, không bắt CEO đọc điểm số? Còn jargon lọt lên đầu → hạ xuống phần kỹ thuật.
- **Dev đủ để hành động không?** Có đủ ma trận có điểm + ADR (stack cụ thể + hệ quả) + (nếu rủi ro) số spike thực đo để đội bắt tay dựng skeleton mà không phải chọn lại?
- **Artifact đúng + đủ chưa?** Có đủ Tech Decision Matrix (có điểm) + ADR (có phương án đã loại) (+ Spike nếu có ẩn số rủi ro cao)? Mọi ô điểm truy về được Architecture Brief GĐ6 / NFR / team, không bịa ràng buộc, không "đang hot"?

## Cổng go/no-go + Bàn giao sang skeleton

**Cổng (bám doc GĐ7):** *"Stack đã chốt, sẵn sàng dựng live slice chưa?"*

**AI DUYỆT theo phân vai A5:** chủ sở hữu = Kiến trúc sư / Tech lead, **người duyệt = CTO**. Theo A5, người giữ vai chủ chốt (CTO) giữ quyết định GO; `stack` đóng vai người duyệt để rà — chỉ được cho qua cổng khi ĐỦ CẢ: (1) mỗi hạng mục rủi ro cao có ma trận **có điểm**; (2) mỗi lựa chọn lớn có ADR kèm phương án đã loại; (3) ẩn số rủi ro cao đã có spike thực đo (hoặc ghi rõ vì sao không cần); (4) mọi lựa chọn nằm trong ràng buộc của Architecture Brief. Thiếu một → chưa qua cổng, nêu ĐÚNG chỗ thiếu, KHÔNG tự đoán lấp. `stack` chuẩn bị matrix + ADR + spike, không tự tuyên "chốt" thay CTO — đủ thì hỏi user câu cổng, chờ quyết.

Qua cổng → khối bàn giao (chỉ liệt kê, KHÔNG tự chọn hộ):
```text
═══ BÀN GIAO — <project> · Tech Stack (GĐ7) ═══
Stack đã chốt     : <hạng mục → công cụ, vd Backend=NestJS · DB=PostgreSQL+Prisma · Deploy=cloud blue-green>
Ràng buộc kéo theo : <hiring / license / vendor / migration path>
Ẩn số còn treo    : <nếu còn — spike tiếp ở đâu, hoặc NFR cần live slice chứng minh>
Artifact          : <đường dẫn pipeline/stack.md>
→ Dựng live slice / walking skeleton end-to-end (GĐ8) để chứng minh stack + kiến trúc: chạy /skeleton
→ Cần điều phối tiếp trọn pipeline tới release: chạy /partner
→ Muốn code ngay một slice nhỏ để thử stack: chạy /frame
→ Kiến trúc lộ ra vấn đề khi chọn tool: quay lại /shape
════════════════
```

## State — ghi artifact vào vùng skill

- Artifact: `state/project/<project-name>/pipeline/stack.md` (Góc nhìn lãnh đạo + Tech Decision Matrix + ADR + Spike). KHÔNG ghi vào repo code trừ khi user đồng ý (theo `idea`); greenfield thì ghi thẳng vùng project của skill.
- Cập nhật `state/current.json`:
```json
{ "project": "<project-path>", "updated_at": "<ISO 8601>" }
```
- Ghi/cập nhật `state/project/<project-name>/pipeline/_index.json` (bản ghi GĐ7):
```json
{ "giai_doan": "gd7_stack",
  "artifact_path": "state/project/<project-name>/pipeline/stack.md",
  "nhan_tu": "shape",
  "ban_giao": "skeleton",
  "cho_duyet": false,
  "chot": ["Backend: NestJS (team thạo TS, module/DI rõ, đủ NFR)"],
  "an_so": ["Perf đồng thời nhiều reviewer — kiểm ở live slice"],
  "updated_at": "<ISO 8601>" }
```
`cho_duyet: true` = đã đưa khối cổng, đang chờ CTO/user — resume KHÔNG tự đi tiếp, nhắc lại cổng. Trạng thái: `cho_duyet` hoặc `done_handoff`.

## Ví dụ Case Management (rút gọn — cùng case với doc GĐ7)

```text
Nhận từ shape (GĐ6): modular monolith 3 module · REST cho UI + domain events · RBAC qua SSO ·
  1 DB schema-per-module (đã ép PostgreSQL) · auth ép SSO công ty · deploy cloud blue-green ·
  NFR P95<500ms, error<1%.

Hạng mục cần chọn : Backend framework (mở, mở ma trận); DB đã ép PostgreSQL (ghi 1 dòng);
  auth ép SSO công ty (ghi 1 dòng).

─── GÓC NHÌN LÃNH ĐẠO ───
Chọn : NestJS + PostgreSQL + Prisma cho backend.
Vì sao: đội đã thạo TypeScript nên lên nhanh & rẻ; mô hình module/DI khớp 3 module đã chốt;
        test tốt; đủ mốc tốc độ yêu cầu.
Đã loại: Spring Boot (mạnh enterprise nhưng đội chưa thạo, lên chậm); Django (module kém rõ cho case này).
Rủi ro: đã dựng thử — 10k bản ghi cho P95 ~210ms, đạt mốc <500ms. Không khoá vendor, tuyển TS dồi dào.

TECH DECISION MATRIX — Backend framework
Tiêu chí (trọng số)          | NestJS | Spring Boot | Django
Fit domain (module rõ)       |   5    |     5       |   3
Fit team (đã biết)           |   5    |     2       |   3
Fit NFR (P95<500ms)          |   4    |     5       |   4
Fit enterprise (auth/audit)  |   4    |     5       |   4
Fit testing                  |   5    |     4       |   4
Fit hiring (thị trường)      |   4    |     4       |   4
TỔNG (có trọng số)           |  27    |    25       |  22
=> Chọn: NestJS · Lý do: đội thạo TS, module/DI rõ, test tốt, đủ NFR.
   Đã loại: Spring (mạnh enterprise nhưng đội chưa thạo, lên chậm); Django (module kém rõ cho case này).

ADR-003 : Chọn NestJS + PostgreSQL + Prisma. Bối cảnh: modular monolith 3 module, đội 6 người TS.
          Đã loại: Spring, Django (lý do trên). Hệ quả: chuẩn hoá DI + test theo module; cần guard RBAC;
          hiring TS dễ, không vendor lock.
SPIKE   : ẩn số P95 → 1 ngày dựng GET /cases với 10k bản ghi → đo P95 ~210ms (đạt <500ms, dư biên).

Cổng "Stack đã chốt, sẵn sàng dựng live slice?" → đủ (ma trận có điểm + ADR + spike đạt) → CTO duyệt GO.
Bàn giao: dựng lát cắt sống "tạo case → duyệt → audit" xuyên UI→API→DB→auth→CI → /skeleton (GĐ8).
```

## Khi làm trong project workspace (`projects/<key>/`)

Nhận diện: user chỉ định `projects/<key>`, hoặc gói ngữ cảnh từ `resume`/`fanout` trỏ tới đó, hoặc `state/current.json` có trường `workspace`. Khi ấy:
- Bước 0 đọc thêm: `projects/<key>/constitution/` (nhất là `folders.md` + `definition-of-done.md`) và `progress/progress.json` — tìm task đang mở giao cho skill này (trường `owner`).
- Artifact người-đọc ghi vào ĐÍCH của task (trường `artifact` trong `progress.json`, đặt theo `folders.md`) — KHÔNG ghi bản chính vào `state/`. State máy riêng của skill (file json trạng thái) vẫn ở `state/project/<key>/` như cũ.
- Xong việc: báo user chạy `/checkpoint <task-id>` lấy phiếu rồi `/progress` đóng bước. Không tự lật done, không tự ghi `progress.json` — file đó một chủ (`progress`).
