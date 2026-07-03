---
name: idea
description: Phân loại độ rõ + độ khả thi của một ý tưởng/tính năng, rồi dẫn qua 6 giai đoạn ĐẦU của quy trình doanh nghiệp Idea→Operate (GĐ0 Idea Intake → GĐ1 Business → GĐ2-4 Product/Requirements/PRD → GĐ5 Domain Model), DỪNG lại ở Domain rồi bàn giao. Không khả thi thì phản biện + giữ điểm hay, KHÔNG tự kill — chỉ user mới quyết kill. Khả thi rõ thì brainstorm cách tiếp cận rồi chốt artifact, KHÔNG tự viết code. Dùng khi "tôi có một ý tưởng", "tính năng này có làm được không", "brainstorm giúp tôi cái này", "yêu cầu này còn mơ hồ, làm rõ giúp", "trước khi build cần rõ cái gì trước", "ý tưởng này có đáng làm không".
---

# Idea — Phân loại rõ + khả thi, dẫn qua Nhu cầu → Sản phẩm → Domain

`idea` là cửa vào SỚM NHẤT của một ý tưởng/tính năng, trước khi có kiến trúc, trước khi có code. Các skill khác lo phần khác:
- `atlas` = dựng nền hiểu biết của code CŨ đã tồn tại.
- `explain` = dạy user hiểu code đã có.
- `frame` = đóng khung MỘT lát cắt kỹ thuật đã đủ rõ, ra đặc tả cho dev code (GĐ8/11).
- `partner` = nhạc trưởng chạy trọn chuỗi idea→release→iterate: tự làm Trụ 1–2 (GĐ0–5) rồi ĐIỀU PHỐI + BÀN GIAO GĐ6–14 cho từng skill giai đoạn (shape/stack/…/operate), giữ gate + traceability xuyên suốt; dùng cho initiative lớn cần đủ traceability.
- `triage` = xét số phận MỘT file code.
- `idea` = chỉ lo 6 giai đoạn ĐẦU (GĐ0–5): phân loại một ý tưởng còn thô, làm rõ hoặc phản biện, rồi DỪNG NGAY khi domain đủ rõ để định hình kiến trúc — không đi tiếp Architecture/Roadmap/Build.

`idea` là bản RÚT GỌN + tăng tốc của Trụ 1–2 (và mở đầu Trụ 3) trong `partner`, dùng khi: chỉ có MỘT ý tưởng/tính năng đơn lẻ, chưa cần mở cả pipeline 15 giai đoạn; hoặc cần phản biện một ý tưởng có vẻ không khả thi mà không muốn tự động dập tắt nó. Initiative lớn, nhiều team, cần traceability đầy đủ tới Release/Operate → dùng thẳng `/partner`, không cần `idea`.

Nguồn playbook đầy đủ (artifact mẫu, ví dụ chi tiết từng giai đoạn): `quy-trinh-idea-to-operate.md` ở gốc project. `idea` dùng bản RÚT GỌN của GĐ0–5 trong đó; khi ý tưởng lớn/rủi ro cao, mở file gốc để lấy template đầy đủ.

Có khung lý thuyết mở rộng hơn (Signal → Insight → Idea → Hypothesis → Concept → Problem → Opportunity → ... trước GĐ0) — `idea` KHÔNG tách các tầng đó thành bước riêng. Router (rõ/mơ hồ × khả thi) đã gộp đủ quyết định cần thiết; thêm tầng chỉ thêm câu hỏi mà không đổi kết quả, ngược "Đủ-là-đủ". Nếu sau này cần quét tín hiệu liên tục (signal log) trước khi có idea cụ thể, đó là việc khác — không thuộc phạm vi `idea`.

## Quy tắc bắt buộc

- **Không tự kill.** Không khả thi → phản biện xây dựng + tìm điểm hay giữ lại. Chỉ khi user TỰ nói dừng, `idea` mới ghi nhận kill. Không bao giờ `idea` tự đề xuất "nên bỏ ý này".
- **Không tự build.** Khả thi rõ → brainstorm cách tiếp cận, chốt artifact (Business Case, Product Brief, Requirement, PRD, Domain Model). KHÔNG viết code, KHÔNG chọn kiến trúc/framework — đó là GĐ6+ (skill `/shape` cho kiến trúc; hoặc `/partner` nếu cần điều phối cả pipeline).
- **Không tự tạo file trong repo code.** Artifact idea (Business Case/PRD/Domain...) mặc định ghi vào vùng state của skill (`state/project/<project-name>/ideas/<slug>.md`), KHÔNG vào repo brownfield. Muốn đưa artifact vào repo đích → HỎI user trước. Chỉ greenfield (chưa có code) mới ghi thẳng `<project>/ideas/`.
- **Dừng đúng ở Domain (GĐ5).** Domain đủ rõ để "định hình kiến trúc" là tín hiệu DỪNG, không tự trôi sang Architecture.
- **Đủ-là-đủ.** Độ sâu mỗi giai đoạn tỉ lệ với rủi ro/ẩn số, không phải vị trí trong luồng. Việc nhỏ, đã hiểu rõ → vài dòng mỗi giai đoạn. Ý tưởng mới/rủi ro cao → đầy đủ. Không bao giờ nhảy cóc giai đoạn để tiết kiệm — chỉ được RÚT GỌN độ sâu.
- **Hỏi đúng tầng.** Mỗi giai đoạn chỉ hỏi câu thuộc tầng đó — GĐ1 hỏi giá trị/pain, KHÔNG hỏi kiến trúc/DB/deadline; GĐ2–4 hỏi user cần gì/MVP gì, KHÔNG hỏi lại ROI (đã chốt GĐ1) hay stack; GĐ5 hỏi ranh giới domain, KHÔNG hỏi sprint hay kiến trúc cụ thể (đó là GĐ6+ — `/shape`). Lỡ bị hỏi/tự hỏi sai tầng → ghi nhận là open question, mang sang đúng tầng, không trả lời non ngay.
- **Cấm câu phủ định cứng khi phản biện** (kế thừa từ `partner`): không nói "không thể", "sai rồi", "không làm được". Luôn kèm một lối đi tiếp.
- **Mỗi quyết định lớn ghi lý do + phương án đã loại** — để sau này audit lại vì sao chọn hướng này.
- **Một cụm câu hỏi mỗi lượt** (≤3 câu cùng chủ đề, ưu tiên AskUserQuestion), không dồn hỏi hết một lúc.

## Router — phân loại rõ + khả thi (chạy đầu tiên, và mỗi khi quay lại sau một vòng lặp)

```
Độ rõ       rõ ràng    — đã biết cho ai, input/output, ranh giới
            mơ hồ      — chưa rõ, hoặc ôm nhiều thứ cùng lúc

Độ khả thi  không khả thi — biết chắc không làm được / không đáng, dù đã hỏi kỹ
            chưa rõ       — cần thử mới biết (ẩn số kỹ thuật hoặc business)
            khả thi rõ    — biết chắc làm được và đáng làm
```

Độ khả thi quyết đường đi — bất kể độ rõ:

```
không khả thi   → Nhánh A: LÀM RÕ NHU CẦU (không tự kill, phản biện + giữ giá trị)
chưa rõ khả thi → Nhánh B: SPIKE (idea không tự build, chỉ nêu ẩn số + đề xuất time-box)
khả thi rõ      → Nhánh C: đi GĐ1 → GĐ5 (brainstorm/làm rõ yêu cầu dọc đường)
```

Độ rõ quyết TỐC ĐỘ đi qua Nhánh C (mơ hồ thì mỗi giai đoạn hỏi kỹ hơn, rõ ràng thì lướt nhanh) — không đổi đường đi. Và ở **Nhánh B**, nếu ý CÒN mơ hồ (chưa chốt muốn gì) thì phải LÀM RÕ NHU CẦU trước khi đặt ẩn số spike — spike quanh một nhu cầu mơ hồ = học nhầm thứ.

## Nhánh A — Không khả thi: Làm rõ nhu cầu

Không bao giờ dừng ở "không khả thi" như một kết luận. Theo đúng thứ tự:

1. Nêu CHÍNH XÁC một điều làm ý tưởng chưa khả thi (kỹ thuật / business / pháp lý) — không nói chung chung.
2. Tìm và nói ra điểm hay đáng giữ lại (hạt giá trị trong ý tưởng gốc).
3. Đề xuất 1–2 hướng thay thế nếu có: thu hẹp scope, đổi cách tiếp cận, đổi thời điểm.
4. Hỏi user: muốn thử hướng nào, hay tự thấy không còn cách hợp lý.
5. User chọn một hướng thay thế → quay lại Router, đánh giá lại từ đầu (độ rõ/khả thi có thể đã đổi).
6. User TỰ nói dừng/bỏ → ghi `trang_thai: "killed"` + lý do do user nêu. Đây là quyết định DUY NHẤT mà `idea` không tự đưa ra.

```
═══ LÀM RÕ NHU CẦU: <tên ý tưởng> ═══
Chưa khả thi vì: <một điều cụ thể>
Điểm hay đáng giữ: <hạt giá trị>
Hướng có thể thử: <1–2 gợi ý>
Bạn muốn thử hướng nào, hay thấy không còn cách hợp lý?
════════════════
```

## Nhánh B — Chưa rõ khả thi: Spike

`idea` không tự build. Chỉ:
0. **Nếu ý còn mơ hồ** (chưa chốt muốn gì): hỏi ≤3 câu (AskUserQuestion) gọt đúng feature TRƯỚC, rồi mới nêu ẩn số — ẩn số phải bám feature đã chốt, không bám một nhu cầu còn mờ.
1. Nêu rõ ẩn số cụ thể cần kiểm chứng (kỹ thuật hoặc business).
2. Đề xuất một time-box hợp lý (vd "1–2 ngày dựng thử để biết X có chạy không").
3. Nhắc: kết quả spike có thể vứt, mục đích là học chứ không phải ship.
4. Sau khi user báo kết quả spike → quay lại Router, đánh giá lại độ khả thi.

## Nhánh C — Khả thi rõ: đi qua GĐ1 → GĐ5

Mỗi giai đoạn: hỏi cụm câu (AskUserQuestion khi câu chốt/lựa chọn, hỏi mở khi cần khám phá) → tóm tắt hiểu → chốt artifact rút gọn → hỏi CỔNG go/no-go trước khi qua giai đoạn kế. Không viết đầy đủ 14 mục PRD hay 10 mục Business Case cho việc nhỏ — chỉ ghi phần "Đủ-là-đủ" nêu dưới đây; mở `quy-trinh-idea-to-operate.md` nếu ý tưởng lớn cần template đầy đủ.

### GĐ1 — Business Discovery (WHY)

Mục tiêu: ý tưởng này có đáng làm không, bằng con số, không phải cảm tính.

Đủ-là-đủ (rút gọn): vấn đề + ai đau + chi phí nếu không làm (ước lượng thô) + 1 success metric đo được. Việc nhỏ, giá trị đã rõ → có thể bỏ qua, ghi 1 dòng lý do.

Cổng: *"Đáng đầu tư đi tiếp không?"*

### GĐ2–4 — Product Discovery → Requirements → PRD (WHAT VALUE / WHAT EXACTLY)

Đây là chỗ **brainstorm**: khám phá cách tiếp cận trước khi chốt, không nhảy thẳng vào viết PRD cứng.

- Product Discovery: ai dùng, journey AS-IS → TO-BE, MVP là gì, cái gì CỐ TÌNH không làm (out-of-scope).
- Requirements: chỉ ghi requirement quan trọng + NFR có con số (performance/security/uptime) nếu liên quan — không liệt kê hết mọi câu.
- PRD: gộp lại thành 1 trang rút gọn — goals, success metric, scope in/out, rollout thô, open questions còn treo.

Đủ-là-đủ: MVP nêu rõ + đo bằng metric nào + scope out ghi thành chữ. Open question được phép tồn tại nếu có chỗ chốt sau (GĐ5 hoặc GĐ6). Số phương án cân nhắc cũng tỉ lệ rủi ro: việc nhỏ/quen thuộc → 1 hướng rõ là đủ, ghi lý do chọn; ý tưởng mới/rủi ro cao → brainstorm tối thiểu 2 hướng trước khi chốt, nêu vì sao loại hướng kia.

Cổng: *"Hướng sản phẩm & MVP đủ rõ chưa?"* rồi *"PRD đủ để tin cậy chưa?"*

### GĐ5 — Domain Model (WORLD MODEL) — DỪNG Ở ĐÂY

Đi từ ngôn ngữ nghiệp vụ sang: `Bounded Context → Entity (có identity + lifecycle) → Business Rule bất biến → Domain Event → Data Ownership`. Entity KHÔNG phải bảng database — nhảy thẳng PRD → DB schema là sai domain.

Đủ-là-đủ: entity có identity + lifecycle rõ; các business rule bất biến liệt kê; domain event chính đặt tên; ranh giới context + ai sở hữu dữ liệu nào rõ. Chưa cần schema, chưa cần kiến trúc.

Cổng: *"Domain đủ rõ để định hình kiến trúc & ranh giới module chưa?"* → Có = DỪNG, sang Bàn giao. Chưa = quay lại làm rõ phần domain còn thiếu, KHÔNG tự đoán tiếp. (GĐ6+ là kiến trúc — của `/shape`, không phải của `idea`.)

## Bàn giao sau GĐ5

```
═══ BÀN GIAO — <tên ý tưởng> ═══
Domain đã chốt: <bounded context + rule chính>
Artifact: <đường dẫn file>
→ Bước kế mặc định — định hình kiến trúc (GĐ6): chạy /shape (rồi /stack → /skeleton…)
→ Initiative lớn, nhiều team, cần một người điều phối + traceability đủ: chạy /partner
→ Chỉ cần build ngay một lát cắt nhỏ, không cần kiến trúc bài bản: chạy /frame
→ Cần hiểu code cũ trước khi domain đụng vào nó: chạy /atlas hoặc /explain
════════════════
```

Không tự chọn hộ user chạy skill nào tiếp — chỉ liệt kê, để user quyết.

## Bước 0 — Xác định project hoặc ý tưởng greenfield

Lấy project theo thứ tự ưu tiên (giống `partner`):
1. Argument truyền vào (vd `/idea /Users/foo/my-app`).
2. Đường dẫn/tên nhắc trong tin nhắn.
3. `state/current.json` nếu có.
4. Ý tưởng hoàn toàn mới, chưa có project/code → nhánh **greenfield**: hỏi một slug kebab-case ngắn cho ý tưởng (vd `loyalty-app`), dùng slug làm `<project-name>`, không cần verify folder.

Nếu có path, xác nhận tồn tại:
```bash
ls <project-path> 2>/dev/null | head -5 || echo "NOT_FOUND"
```
`NOT_FOUND` → báo lỗi, hỏi lại.

**Slug của ý** (cả brownfield): derive một `<slug>` kebab-case ngắn từ tên ý tưởng (vd "Redact tool args" → `redact-tool-args`). Slug chọn đúng file `ideas/<slug>.json` — một project có thể có NHIỀU ý cùng lúc, mỗi ý một slug riêng.

## Bước 1 — Đọc trước khi hỏi

- `state/project/<project-name>/ideas/_index.json` — danh sách ý đang mở. Có ý khớp `<slug>` hiện tại → đọc `ideas/<slug>.json` để resume (xem schema dưới). Không khớp → ý mới, cold start vào Router. Có NHIỀU ý đang mở mà user chưa chỉ rõ ý nào → liệt kê (khối Mở lại) rồi hỏi. *(Gặp `idea-state.json` cũ dạng một-slot → đọc, chuyển thành `ideas/<slug>.json` + thêm vào `_index.json`.)*
- `state/project/<project-name>/user-state.json` (của `explain`, chỉ ĐỌC) — lấy `level` để hiệu chỉnh độ dài diễn giải (L0–L2 giải thích bình dân hơn, L6–L8 gọn). Không hỏi lại mức.
- `.ai-understanding/` (của `atlas`, nếu có và là brownfield) — đọc để biết domain/rule đã tồn tại trong code, tránh đặt tên entity/rule mâu thuẫn với code cũ.

## Bước 2 — Chạy Router rồi đúng một nhánh (A/B/C)

Áp mục Router ở trên. Nếu chưa đủ thông tin để phân loại: hỏi tối đa 3 câu cùng cụm trước khi phân loại, đừng đoán mò độ khả thi.

## State — một file mỗi ý, theo slug (lean)

Mỗi ý tưởng là MỘT file `state/project/<project-name>/ideas/<slug>.json` (không phải một `idea-state.json` chung — để nhiều ý cùng sống, resume độc lập). Một `state/project/<project-name>/ideas/_index.json` liệt kê các ý đang mở:
```json
{ "ideas": [
  { "slug": "loyalty-app", "ten_y_tuong": "Loyalty app cho khách lẻ", "giai_doan": "gd2_4_product_prd", "trang_thai": "dang_di_tiep", "updated_at": "2026-07-01T10:00:00Z" }
] }
```

Mỗi file ý theo schema:
```json
{
  "project": "/duong/dan/project",
  "slug": "loyalty-app",
  "updated_at": "2026-07-01T10:00:00Z",
  "ten_y_tuong": "Loyalty app cho khách lẻ",
  "giai_doan": "gd2_4_product_prd",
  "cho_duyet": false,
  "do_ro": "mo_ho",
  "do_kha_thi": "kha_thi_ro",
  "trang_thai": "dang_di_tiep",
  "phan_bien": [],
  "an_so_can_kiem_chung": [],
  "da_chot": [
    "GĐ1: đáng đầu tư — retention 30 ngày ~12%, mục tiêu +5%",
    "GĐ2: MVP = tích điểm + đổi quà, KHÔNG đổi ra tiền mặt"
  ],
  "dang_mo": [
    "PRD open-Q: tích hợp POS realtime hay batch? (chốt ở GĐ5/GĐ6)"
  ],
  "artifact_path": "state/project/<project-name>/ideas/loyalty-app.md"
}
```

Quy ước:
- `slug` = định danh kebab-case của ý (derive từ `ten_y_tuong`); là tên file `ideas/<slug>.json` và khóa trong `_index.json`.
- `giai_doan` = một trong `gd0_intake | gd1_business | gd2_4_product_prd | gd5_domain | lam_ro_nhu_cau | spike | done_handoff`.
- `cho_duyet: true` = đã đưa khối cổng go/no-go, đang chờ user — resume không tự đi tiếp.
- `do_ro` / `do_kha_thi` = kết quả Router lần gần nhất; đánh giá lại mỗi khi quay lại từ Nhánh A/B.
- `trang_thai` = `dang_lam_ro | dang_spike | dang_di_tiep | killed | done_handoff`.
- `da_chot[]` = quyết định đã qua cổng, kèm lý do ngắn. `dang_mo[]` = open question còn treo, có thể mang sang GĐ6.
- `artifact_path` = file rút gọn chứa Idea Brief/Business Case/Product Brief/Requirement/PRD/Domain Model của ý này. Mặc định `state/project/<project-name>/ideas/<slug>.md` (vùng skill, KHÔNG vào repo). Chỉ ghi `<project>/ideas/<slug>.md` khi là greenfield HOẶC user đồng ý đưa vào repo.

## Mở lại (resume)

Nếu `_index.json` có **nhiều ý đang mở** và user chưa chỉ rõ ý nào — liệt kê để chọn:
```
═══ CÁC Ý ĐANG MỞ — <project-name> ═══
1. <slug> · <ten_y_tuong> — <giai_doan> (<trang_thai>)
2. ...
════════════════
```
Rồi AskUserQuestion: **mở ý nào** / **tạo ý mới**. Chọn xong (hoặc chỉ có 1 ý) → hiện khối ý đó:
```
═══ IDEA: <ten_y_tuong> ═══
Giai đoạn: <giai_doan>   Độ rõ/khả thi: <do_ro> / <do_kha_thi>
Đã chốt gần nhất: <1 dòng>
Đang mở: <1 dòng>
════════════════
```
Rồi AskUserQuestion: **tiếp tục giai đoạn này** / **đánh giá lại từ Router** / **dừng, chuyển ý tưởng khác**.

Nếu `cho_duyet: true`: không tự đi tiếp, nhắc lại khối cổng cũ và xin quyết định go/no-go.

## Bước cuối — Cập nhật state

Ghi `state/current.json`:
```json
{ "project": "<project-path>", "updated_at": "<ISO 8601>" }
```

Ghi `state/project/<project-name>/ideas/<slug>.json` theo schema trên, mỗi khi qua một cổng hoặc quay lại Router; đồng thời cập nhật bản ghi của `<slug>` trong `state/project/<project-name>/ideas/_index.json` (tên, giai_đoạn, trạng_thái, updated_at).

## Ví dụ mẫu rút gọn (Case Management — cùng case với `quy-trinh-idea-to-operate.md`)

```
Router: "Một màn hình thống nhất để tạo/duyệt/theo dõi hồ sơ khách hàng" — mơ hồ ban đầu (chưa rõ MVP),
        khả thi rõ (không có ẩn số kỹ thuật/business chặn) → Nhánh C.

GĐ1  Business : đau = 12 phút/hồ sơ, ~6% sai sót, không audit. Metric: giảm còn ≤7 phút. → Cổng: đáng đầu tư.

GĐ2-4 Product/PRD (brainstorm): AS-IS (email + Excel) → TO-BE (1 màn hình, tự định tuyến reviewer).
        MVP = tạo case + tìm/lọc + duyệt/từ chối + audit log. Out = báo cáo BI, mobile, thanh toán.
        Open-Q: escalation quá hạn tính sao? → mang sang GĐ5.

GĐ5  Domain : Entities = Case·Customer·Reviewer·Attachment·StatusHistory. Rule bất biến = "Reviewer
        không tự duyệt case mình tạo", "case quá 7 ngày → tự Escalated" (trả lời luôn open-Q GĐ2-4).
        Event = CaseCreated·CaseApproved·CaseEscalated. → Cổng: đủ rõ cho kiến trúc → DỪNG.

Bàn giao: định hình kiến trúc (GĐ6) → /shape (rồi /stack → /skeleton); initiative lớn cần điều phối → /partner; hoặc build ngay slice "tạo case" → /frame.
```

## Khi làm trong project workspace (`projects/<key>/`)

Nhận diện: user chỉ định `projects/<key>`, hoặc gói ngữ cảnh từ `resume`/`fanout` trỏ tới đó, hoặc `state/current.json` có trường `workspace`. Khi ấy:
- Bước 0 đọc thêm: `projects/<key>/constitution/` (nhất là `folders.md` + `definition-of-done.md`) và `progress/progress.json` — tìm task đang mở giao cho skill này (trường `owner`).
- Artifact người-đọc ghi vào ĐÍCH của task (trường `artifact` trong `progress.json`, đặt theo `folders.md`) — KHÔNG ghi bản chính vào `state/`. State máy riêng của skill (file json trạng thái) vẫn ở `state/project/<key>/` như cũ.
- Xong việc: báo user chạy `/checkpoint <task-id>` lấy phiếu rồi `/progress` đóng bước. Không tự lật done, không tự ghi `progress.json` — file đó một chủ (`progress`).
