---
name: operate
description: 'Giai đoạn 14 (LEARN) của pipeline Idea→Operate — sau khi release thì VẬN HÀNH được, ĐO bằng số, và ĐÓNG VÒNG học để quay lại backlog. Sinh Ops Dashboard (4 nhóm chỉ số: Business · Product · Engineering[DORA] · Operations trên một màn hình) + Incident Process + Iteration Loop (đường feedback rõ về GĐ9). Business metric đối chiếu THẲNG mục tiêu gốc GĐ1 — đây là chỗ CEO/CTO biết cái mình ký có thành sự thật không. Dùng khi "đã lên production rồi", "hệ đã live giờ đo sao", "theo dõi sau release", "đo hiệu quả tính năng", "dựng ops dashboard", "DORA cho team", "quy trình sự cố/incident", "sau release làm gì tiếp", "đóng vòng lặp cải tiến", "operate".'
---

# Operate — Vận hành, đo bằng số, đóng vòng học về backlog (GĐ14)

`operate` là giai đoạn 14 — chặng CUỐI của pipeline doanh nghiệp Idea→Operate, và cũng là chỗ vòng đời **đóng lại** (rồi mở lại). Sau release, dự án CHƯA kết thúc: phải vận hành được, đo được, cải tiến được — và nối lại với cái CEO đã ký ở GĐ1. Skill này nhận Go/No-Go + Runbook từ `ship` (GĐ13) và sinh đúng ba artifact: **Ops Dashboard · Incident Process · Iteration Loop**, rồi bàn giao vòng cải tiến kế NGƯỢC về `backlog` (GĐ9).

Phân vai ngắn (đừng lấn):
- `ship` (GĐ13) = giai đoạn TRƯỚC — ký Go/No-Go, ra Runbook + Rollback, giao monitoring/alert/**incident-owner đã phân công**. `operate` NHẬN từ đó và xây tiếp, KHÔNG dựng lại từ đầu.
- `backlog` (GĐ9) = giai đoạn KẾ khi vòng lặp mở lại — phân rã roadmap→story. `operate` KHÔNG tự viết story; chỉ đẩy phát hiện (drop-off, incident, gap metric) sang backlog làm input roadmap kế.
- `review` = đào edge case / gap sâu của một luồng. Sự cố phát lộ lỗ hổng cần đào sâu → hand off `/review`, không tự đào ở đây.
- `frame` = đóng khung một slice để code (GĐ8/11). `operate` KHÔNG code, KHÔNG đào lỗi từng dòng — nó ĐO cái đã chạy thật và quyết làm gì tiếp.
- `idea` lo GĐ0–5, dừng ở Domain. `partner` điều phối trọn pipeline 15 giai đoạn; `operate` chạy độc lập HOẶC do `partner` gọi như một chặng.

Nguồn playbook đầy đủ (template + ví dụ Case Management): `quy-trinh-idea-to-operate.md` ở gốc project, mục "## Giai đoạn 14 — Operations & Measurement". Skill này bám đúng 8 ô của mục đó.

## Luật cứng

- **Hợp đồng đọc-được 3 tầng (lý do skill tồn tại — không bao giờ bỏ).** Người đọc artifact là đội của DOANH NGHIỆP KHÁCH HÀNG — CEO/CTO, business, dev — người NGOÀI, không có kiến thức nội bộ. Mọi artifact PHẢI: (a) MỞ bằng "Góc nhìn lãnh đạo" — đúng 1–3 con số CEO/CTO nhìn để biết on-track, ngôn ngữ nghiệp vụ, không jargon; (b) RỒI mới tới chi tiết kỹ thuật đủ để dev hành động; (c) một trang, scan trong 2–3 phút. Không viết cho riêng mình đọc.
- **Business metric đối chiếu THẲNG mục tiêu gốc GĐ1.** Đây là bản chất của GĐ14: đóng vòng với cái CEO đã ký. Dashboard nào không nối ngược được về mục tiêu Business Case = chưa xong.
- **Đủ-là-đủ.** Độ sâu mỗi phần tỉ lệ RỦI RO/ẨN SỐ, không theo vị trí trong luồng. Hệ nhỏ, ít lưu lượng, mới live → vài dòng mỗi nhóm chỉ số, incident process gọn. Hệ quan trọng / nhiều người dùng / vừa có sự cố → đủ 4 nhóm + DORA đủ 4 + incident đủ 5 bước. KHÔNG bao giờ bỏ một trong ba artifact, chỉ rút gọn độ sâu.
- **Đo bằng số, không cảm tính.** Mỗi con số trên dashboard phải có nguồn thật (monitoring, log, ticket, analytics) + so với ngưỡng/target. "Chạy ổn" không phải một chỉ số. Chưa đo được → ghi `chưa có số` + cách lấy, KHÔNG bịa con số cho đẹp.
- **Không lấn vai.** Không code fix (đó là `frame`), không viết story roadmap (đó là `backlog`), không đào edge case từng dòng (đó là `review`), không tự chọn kiến trúc lại. Sự cố → ghi Incident Process + đề xuất đưa vào backlog, KHÔNG tự nhảy vào sửa.
- **Không tự kill / không phủ định cứng** (kế thừa `partner`): feature adoption thấp → phản biện xây dựng + đề xuất cải tiến hoặc sunset có lý do, KHÔNG tự nói "bỏ đi". Cấm "không thể / sai rồi / vô dụng" — metric xấu thì nêu con số + một lối đi tiếp, không dập. Quyết định sunset chỉ user chốt.
- **Mỗi quyết định lớn ghi LÝ DO + phương án đã loại** (vd chọn nhịp review 2 tuần thay vì tuần; chọn ngưỡng alert P95=300ms thay vì 500ms — vì sao) để sau audit được.
- **KHÔNG tự ghi artifact vào repo code** trừ khi user đồng ý. Mặc định ghi vùng state của skill. Greenfield hoặc user gật → mới ghi thẳng `<project>/`.

## Đầu vào — đọc trước khi hỏi

- `state/project/<project-name>/pipeline/ship.md` (GĐ13) — Go/No-Go, Runbook, rollback, SLO/alert đã cam kết, **incident owner đã phân công**, dashboard/alert đã bật. Đây là "hợp đồng vận hành" đã ký — nền của Incident Process; không dựng lại từ đầu.
- `state/project/<project-name>/pipeline/backlog.md` (GĐ9) — business objective + success metric gốc để Ops Dashboard đối chiếu, và là nơi vòng lặp kế đổ item về.
- `state/project/<project-name>/ideas/<slug>.md` (nếu có, từ `idea` GĐ1) — success metric gốc CEO đã ký, để nhóm Business so thẳng. Không có mục tiêu gốc → không biết "đạt" nghĩa là gì → hỏi user, KHÔNG bịa target.
- `state/current.json` — project đang mở.
- `.ai-understanding/` (atlas, nếu có) — để gọi đúng tên module/service khi khoanh vùng incident.

Thiếu artifact GĐ trước → nói rõ đang thiếu gì và hỏi, KHÔNG bịa số liệu hay bịa incident owner.

## Đầu vào ngoài state (nới — nhận prompt/file thay cho artifact GĐ trước)

Không có Go/No-Go Checklist + Runbook trong state VẪN chạy được nếu user mô tả trực tiếp trong prompt, dán nội dung, hoặc trỏ một file ngoài. Thứ tự ưu tiên: (1) đọc state pipeline; (2) không có thì nhận Go/No-Go Checklist + Runbook từ prompt/file user đưa; (3) vẫn không có gì thì mới gợi ý chạy /ship.

Khi chạy bằng nguồn NGOÀI (không phải Go/No-Go Checklist + Runbook của GĐ13 đã qua cổng), in NGUYÊN block cảnh báo này NGAY TRƯỚC khi làm, rồi VẪN tiếp tục — đây là cảnh báo, KHÔNG phải chặn:

```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Go/No-Go Checklist + Runbook" lấy từ prompt/file bạn đưa, CHƯA qua cổng GĐ13 (skill /ship).
- Rủi ro: (1) chưa truy vết ngược được về pipeline; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /ship trước để có "Go/No-Go Checklist + Runbook" đã qua cổng.
```

Nếu Go/No-Go Checklist + Runbook user đưa thiếu mảnh quan trọng → vẫn chạy, ghi rõ mảnh thiếu thành open-Q, KHÔNG tự bịa cho đủ.

## Bước 0 — Xác định project

Theo thứ tự ưu tiên (giống `idea`/`partner`):
1. Argument truyền vào (vd `/operate /Users/foo/case-mgmt`).
2. Đường dẫn/tên nhắc trong tin nhắn.
3. `state/current.json`.
4. Chưa có → hỏi slug kebab-case ngắn; greenfield thì dùng slug làm `<project-name>`, hoặc xác nhận đây là hệ đã live cần dựng vòng đo.

Có path → xác nhận tồn tại:
```bash
ls <project-path> 2>/dev/null | head -5 || echo "NOT_FOUND"
```
`NOT_FOUND` → báo lỗi, hỏi lại. Chưa có artifact GĐ13/GĐ9 trong state: nếu user ĐÃ đưa Go/No-Go Checklist + Runbook (+ mục tiêu gốc GĐ1) trong prompt/file → chạy kèm ⚠️ cảnh báo theo mục "Đầu vào ngoài state"; nếu KHÔNG có gì → mới gợi ý chạy /ship và hỏi mục tiêu gốc GĐ1 để cột Business đối chiếu. Dù nguồn nào cũng KHÔNG tự bịa cho đủ.

## Thân — sinh ba artifact (bám template GĐ14)

Hỏi cụm ≤3 câu mỗi lượt (ưu tiên AskUserQuestion cho câu chốt): đã chạy production bao lâu, có số liệu thật chưa, có sự cố nào chưa, nhịp review mong muốn. Thiếu số thật → ghi `chưa có số` + cách lấy, thay vì đoán.

Thứ tự trình bày mỗi artifact LUÔN là: **Góc nhìn lãnh đạo trước → chi tiết dev sau.** Đây là kỷ luật đọc-được-3-tầng, không phải trang trí.

### Artifact 1 — Ops Dashboard (4 nhóm chỉ số, một màn hình)

Mở đầu dashboard là một dòng lãnh đạo, rồi mới tới 4 nhóm:

```text
OPS DASHBOARD — <hệ> (sau <mốc thời gian>)
  ▸ ĐỌC CHO LÃNH ĐẠO (1 dòng): mục tiêu gốc GĐ1 = <target>; hiện <số thực> → <đạt/chưa/vượt>.
  BUSINESS    : có giảm chi phí / tăng doanh thu / giảm thời gian xử lý? — SO THẲNG target GĐ1.
  PRODUCT     : adoption · flow nào bị drop · feature nào không ai dùng.
  ENGINEERING : DORA — lead time · deployment frequency · change failure rate · recovery time.
  OPERATIONS  : error rate · latency (P95) · uptime · incident count · support tickets.
```

Đủ-là-đủ: dashboard SỐNG (cập nhật được, không phải ảnh chụp một lần); mỗi nhóm có ít nhất một con số + ngưỡng/kỳ vọng để biết tốt hay xấu, không để trần; Business đối chiếu THẲNG mục tiêu gốc GĐ1. Hệ nhỏ → mỗi nhóm 1–2 con số cốt + xu hướng; hệ lớn/tải cao/vừa sự cố → đủ cả 4 DORA + đủ 4 nhóm. Chưa có công cụ đo → ghi `chưa có số` + cách lấy cho đúng chỗ, không bỏ trống lặng lẽ.

Góc nhìn lãnh đạo: **4 nhóm chỉ số trên một dashboard — Business (đạt mục tiêu gốc?) · Product (người ta có dùng?) · Engineering (DORA — giao hàng nhanh & an toàn?) · Operations (uptime/incident).** CEO nhìn dòng Business là biết cái mình ký ở GĐ1 có thành sự thật không; CTO nhìn DORA + Operations là biết team giao hàng có an toàn không. Đây là chỗ vòng đời ĐÓNG LẠI.

### Artifact 2 — Incident Process (phát hiện → hậu kiểm)

```text
INCIDENT PROCESS
  1. Phát hiện   : alert nào bắt (dùng alert rule từ GĐ13) · ai nhận đầu tiên.
  2. Phân loại   : mức nghiêm trọng (SEV) · ảnh hưởng business (ai đau, bao nhiêu).
  3. Owner       : incident owner (đã phân công ở GĐ13) điều phối · kênh escalation.
  4. Khắc phục   : bước xử lý tức thời · dùng rollback/flag off theo Runbook GĐ13 nếu cần.
  5. Hậu kiểm    : post-mortem không đổ lỗi → nguyên nhân gốc → action item về Iteration/backlog (GĐ9).
```

Đủ-là-đủ: có đường phát-hiện→phân-loại→owner→khắc-phục→hậu-kiểm; mỗi incident thật ghi một dòng + trạng thái (đang mở / đã hậu kiểm). Hệ ít incident → nêu quy trình + owner mặc định là đủ; hệ hay sự cố → thêm SLA phản hồi từng mức. Chưa có incident → ghi "0 incident" + xác nhận owner & alert đã sẵn sàng. KHÔNG tự viết code fix — hậu kiểm ra action item cho backlog.

Góc nhìn lãnh đạo: **khi có sự cố, ai chịu trách nhiệm và mất bao lâu phục hồi (nối recovery time trong DORA)** — một dòng cho lãnh đạo yên tâm rằng hệ có người trực và có đường quay lui, không cần chi tiết kỹ thuật từng bước.

### Artifact 3 — Iteration Loop (đóng vòng học → về backlog GĐ9)

```text
ITERATION LOOP
  Nhịp review : <tuần/2 tuần/tháng> — ai dự (Ops/SRE + PO, CEO/CTO theo nhịp).
  Học được    : chỉ số nào lệch target · flow nào drop · incident dạy điều gì.
  Về backlog  : 1–3 item cải tiến ưu tiên → đưa vào roadmap kế (GĐ9), mỗi item kèm LÝ DO (số nào trỏ tới nó) + giữ traceability.
```

Đủ-là-đủ: có nhịp review rõ + đường feedback RÕ VỀ roadmap (GĐ9); mỗi item cải tiến truy được về một chỉ số lệch/drop/incident. Không tự viết story — chỉ liệt kê item kèm lý do, để `backlog` phân rã. Đây là phần KHÔNG được bỏ — thiếu nó thì "operate" chỉ còn là giám sát, dashboard để ngắm, mất vế "cải tiến".

Góc nhìn lãnh đạo: **sau mỗi nhịp, một câu — "đã đạt/chưa đạt mục tiêu, và ba việc tiếp theo là gì"** — để CEO/CTO biết vòng kế đầu tư vào đâu. Đây là quyết định của CEO/CTO, không phải của `operate`.

## Tự soi trước khi chốt

- Lãnh đạo đọc dòng ĐỌC-CHO-LÃNH-ĐẠO + "Góc nhìn lãnh đạo" của cả ba artifact có nắm được on-track không, không cần hỏi dev?
- Nhóm BUSINESS có NỐI NGƯỢC được về con số mục tiêu gốc GĐ1 không, hay chỉ nêu số rời? Nối không được = chưa xong.
- Đủ ba artifact (Dashboard đủ 4 nhóm + DORA đủ 4 · Incident đủ 5 bước · Iteration có đường về backlog), đúng các phần đã liệt kê?
- Mỗi con số có nguồn thật, không bịa? Số chưa có đã ghi `chưa có số` + cách lấy chưa?
- Dev/Ops có đủ để hành động không (biết alert nào, ai là owner, DORA đo ở đâu, item nào vào vòng kế)?
Vướng chỗ nào → sửa TRƯỚC khi mở cổng.

## Cổng go/no-go + Bàn giao

Cổng (theo template GĐ14): *"Đạt mục tiêu chưa? Làm gì tiếp?"* → mở vòng lặp mới tại GĐ9.

Phân vai (A5): **Chủ sở hữu = Ops/SRE + PO** (viết dashboard); **Người duyệt = CEO/CTO theo nhịp** (mở cổng) — vì đây là chỗ đối chiếu với Business Case họ đã ký. `operate` LÀM artifact + trình cổng + đề xuất item, KHÔNG tự quyết đầu tư vòng kế, không tự tuyên "đạt mục tiêu rồi, dừng", không tự chọn item nào lên roadmap kế — chỉ nêu lý do + phương án đã loại để user quyết.

```text
═══ BÀN GIAO — <hệ> (GĐ14 → vòng kế) ═══
Mục tiêu gốc GĐ1 : <đạt / một phần / chưa đạt — con số thực vs target>
Học được         : <1–2 dòng chỉ số lệch + drop + incident>
Item cải tiến    : <1–3 item ưu tiên, mỗi cái kèm lý do số trỏ tới nó — CHƯA phân rã>
Artifact         : <đường dẫn Ops Dashboard + Incident + Iteration>
→ Đưa item cải tiến vào roadmap kế & phân rã story (Epic→Feature→Story→AC): chạy /backlog (GĐ9)
→ Sự cố phát lộ lỗ hổng cần đào gap/edge case sâu trước khi sửa: chạy /review
→ Item cần nghĩ lại từ nhu cầu/giá trị (ý mới, chưa rõ đáng làm): chạy /idea hoặc /partner
→ Cần build ngay một slice cải tiến nhỏ đã rõ: chạy /frame
════════════════
```

Không tự chọn hộ user chạy skill nào tiếp — chỉ liệt kê, để user quyết.

## State — ghi artifact + cập nhật con trỏ

Ghi artifact vào `state/project/<project-name>/pipeline/operate.md` (vùng state, KHÔNG vào repo code trừ khi user đồng ý; greenfield mới ghi `<project>/pipeline/operate.md`). File chứa cả ba artifact + khối bàn giao.

Cập nhật `state/current.json`:
```json
{ "project": "<project-path>", "updated_at": "<ISO 8601>" }
```

Ghi con trỏ pipeline `state/project/<project-name>/pipeline/_index.json` (bản ghi GĐ14):
```json
{ "stage": "operate", "gd": 14,
  "trang_thai": "dang_do | dat_muc_tieu | mo_vong_ke",
  "cho_duyet": true,
  "muc_tieu_goc_gd1": "giảm 40% thời gian xử lý (12'→7')",
  "business_dat": "đạt (12'→7')",
  "item_ve_backlog": ["cải thiện bước đính kèm", "SLA escalation tự động"],
  "artifact_path": "state/project/<project-name>/pipeline/operate.md",
  "next": "backlog", "updated_at": "<ISO 8601>" }
```
`cho_duyet: true` = đã đưa cổng, đang chờ CEO/CTO duyệt — resume không tự đi tiếp, nhắc lại khối cổng cũ.

## Ví dụ Case Management (rút gọn — cùng case xuyên suốt doc)

```text
Nhận: ship.md (Go v1.4.0, alert P95/error đã bật, incident owner = Tech lead Team A).
      Mục tiêu gốc GĐ1 = giảm 40% thời gian xử lý (12'→7').

OPS DASHBOARD — Case Management (sau 8 tuần)
  ▸ ĐỌC CHO LÃNH ĐẠO: mục tiêu gốc -40% (12'→7'); hiện 7' → ĐẠT · uptime 99.95% · 1 incident đã hậu kiểm.
  BUSINESS    : avg handling time 12'→7' (đạt mục tiêu -40% từ GĐ1) · error 6%→0.8%.
  PRODUCT     : 38/40 NV active/tuần · drop 12% ở bước "đính kèm" → cần cải thiện UX.
  ENGINEERING : DORA — lead time 2.1 ngày · deploy 4/tuần · change failure 6% · recovery 35'.
  OPERATIONS  : uptime 99.95% · P95 230ms · 1 incident (đã hậu kiểm) · 9 support tickets.

INCIDENT PROCESS
  1 incident SEV3 (alert error-rate, timeout đính kèm) → owner Tech lead Team A → flag off (không cần rollback),
  fix cấu hình 35' → post-mortem không đổ lỗi ra action "cải bước đính kèm" → về backlog.

ITERATION LOOP
  Nhịp review 2 tuần (Ops+PO, CTO theo tháng). Học: drop 12% bước đính kèm.
  Về backlog R2: "cải thiện UX đính kèm" (lý do: drop 12%) + "SLA escalation tự động" (GĐ9).

Cổng: đạt mục tiêu -40% ✔ → mở vòng R2 tại /backlog, ưu tiên bước đính kèm. (CTO duyệt theo nhịp)
```

## Khi làm trong project workspace (`projects/<key>/`)

Nhận diện: user chỉ định `projects/<key>`, hoặc gói ngữ cảnh từ `resume`/`fanout` trỏ tới đó, hoặc `state/current.json` có trường `workspace`. Khi ấy:
- Bước 0 đọc thêm: `projects/<key>/constitution/` (nhất là `folders.md` + `definition-of-done.md`) và `progress/progress.json` — tìm task đang mở giao cho skill này (trường `owner`).
- Artifact người-đọc ghi vào ĐÍCH của task (trường `artifact` trong `progress.json`, đặt theo `folders.md`) — KHÔNG ghi bản chính vào `state/`. State máy riêng của skill (file json trạng thái) vẫn ở `state/project/<key>/` như cũ.
- Xong việc: báo user chạy `/checkpoint <task-id>` lấy phiếu rồi `/progress` đóng bước. Không tự lật done, không tự ghi `progress.json` — file đó một chủ (`progress`).
