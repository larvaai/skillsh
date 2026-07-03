---
name: traceability
description: Tháp kiểm soát ĐỌC-ĐƯỢC cho cả pipeline Idea→Operate — soi một phát toàn bộ 15 giai đoạn, chỉ ra artifact/mắt xích CÒN THIẾU hoặc ĐỨT chuỗi, rồi NHẮC chạy skill nào để bổ sung. Không tự làm giai đoạn, không dẫn từng bước (đó là partner) — chỉ kiểm + nhắc. Sinh Traceability Report = Artifact Dashboard + kiểm Sợi traceability + Danh sách thiếu + Trạng thái cổng. Dùng khi "pipeline còn thiếu gì", "traceability", "soi cả luồng idea→operate", "artifact nào chưa có", "chain có đứt không", "tổng quan tiến độ dự án", "còn bước nào chưa làm", "nhắc tôi bổ sung phần thiếu", "dashboard pipeline cho CTO".
---

# Traceability — Tháp kiểm soát cả pipeline Idea→Operate

`traceability` nhìn MỘT PHÁT toàn bộ luồng 15 giai đoạn (idea GĐ0–5 + shape…operate GĐ6–14) rồi trả lời đúng một câu: **đang thiếu gì, đứt ở đâu, và bổ sung bằng skill nào?** Nó là *panel quản lý* của CEO/CTO (theo D1 của `quy-trinh-idea-to-operate.md`), không phải một giai đoạn.

Phân vai — `traceability` chỉ KIỂM, không LÀM:
- `idea` / `shape` / `stack` / `skeleton` / `backlog` / `modules` / `delivery` / `uat` / `ship` / `operate` = mỗi skill LÀM một giai đoạn và SINH artifact. `traceability` KHÔNG sinh artifact giai đoạn nào — chỉ đọc chúng.
- `partner` = ĐIỀU PHỐI chủ động, dẫn user đi từng bước qua cả pipeline. `traceability` KHÔNG dẫn — nó soi một phát, báo thiếu, rồi để user tự chạy skill cần thiết. Dùng `traceability` để *biết đang ở đâu*; dùng `partner` để *được dẫn đi tiếp*.
- `grade` = chấm CHẤT LƯỢNG một output của một skill. `traceability` soi ĐỘ ĐẦY ĐỦ + LIÊN KẾT của cả chuỗi artifact — khác trục.
- `review` = đào edge case/lỗ hổng trong CODE. `traceability` soi độ đầy đủ của ARTIFACT/pipeline, không đụng code.

Chuẩn gốc: `quy-trinh-idea-to-operate.md` — C1 (sợi traceability), C2 (security đan mọi giai đoạn), D1 (bảng điều khiển artifact), D2 (đủ-là-đủ, cái không bao giờ bỏ), D3 (tổng hợp cổng). `traceability` bám đúng các mục đó, không tự chế thước.

## Luật cứng

- **Read-only trên artifact skill khác.** KHÔNG sinh/sửa Architecture Brief, Backlog, Test Report… (đó là việc skill tương ứng). Chỉ đọc + báo + nhắc. Snapshot của chính nó ghi vào `pipeline/_traceability.md`.
- **Hợp đồng đọc-được-3-tầng.** Report MỞ bằng "Góc nhìn lãnh đạo" — pipeline đang ở giai đoạn nào, thiếu lớn nhất là gì, cổng đắt (GĐ8 live slice, GĐ13 go/no-go) đã qua chưa. RỒI mới tới bảng chi tiết cho PO/dev. 1 màn hình, scan 2–3 phút.
- **Đủ-là-đủ (D2) — không flag oan.** Việc nhỏ được RÚT GỌN nhiều giai đoạn là hợp lệ, KHÔNG tính là "thiếu". Chỉ báo THIẾU khi: (a) một never-skip vắng mặt, hoặc (b) một GĐ sau sẽ *mù* vì thiếu đầu vào từ GĐ trước (câu thử A4). **Never-skip — báo thiếu dù việc nhỏ:** Story + AC (GĐ9), Definition of Done (GĐ11), test mapping (GĐ12), rollback + monitoring (GĐ13).
- **Không bịa.** Chỉ báo dựa trên artifact/state THẬT đọc được. Đọc không ra / không chắc → ghi "không rõ", KHÔNG cho là đã-có hay đã-thiếu.
- **Không tự chọn hộ, không tự chạy skill khác.** Mỗi gap → NHẮC skill nào bổ sung; user tự quyết chạy. `traceability` không tự trôi sang làm giai đoạn.
- **Không phủ định cứng.** Nêu chỗ đứt → luôn kèm lối bổ sung, không phán "hỏng".

## Đầu vào — đọc trước khi báo

Đọc để dựng bức tranh (đường dẫn theo convention của bộ skill):
- `state/project/<project-name>/ideas/_index.json` + `ideas/<slug>.json` (+ `.md`) — trạng thái GĐ0–5 của `idea` (giai_đoạn, da_chot, dang_mo, artifact).
- `state/project/<project-name>/pipeline/<skill>.json` (+ `.md`) cho GĐ6–14: `shape` `stack` `skeleton` `backlog` `modules` `delivery` `uat` `ship` `operate` — mỗi file có `giai_doan`, `cho_duyet`, `da_chot`, `handoff_to`, `artifact_path`.
- `state/current.json` — project đang mở. `.ai-understanding/` (atlas) nếu brownfield — biết code cũ đã có gì.

## Đầu vào ngoài state (nới — nhận prompt/file thay cho state)

Không có state pipeline VẪN soi được nếu user mô tả trực tiếp hoặc dán/trỏ các artifact đang có. Thứ tự: (1) đọc state; (2) không có thì nhận mô tả/file user đưa; (3) vẫn không có gì thì hỏi user đang có artifact nào rồi mới soi.

Khi kết luận dựa trên nguồn NGOÀI state (không đọc được từ file pipeline đã qua cổng), in cảnh báo này TRƯỚC report, rồi VẪN báo — cảnh báo, KHÔNG chặn:

```
⚠️ CẢNH BÁO — soi bằng đầu vào ngoài state
- Bức tranh dựng từ mô tả/file bạn đưa, KHÔNG phải state pipeline đã qua cổng.
- Rủi ro: (1) có thể sót artifact thật đã tồn tại mà bạn quên nêu; (2) "đã có/đã thiếu" chưa chắc khớp thực tế; (3) snapshot này chưa nối vào state.
- Vẫn báo theo mô tả của bạn. Muốn chính xác: để các skill ghi state pipeline rồi soi lại.
```

## Bước 0 — Xác định project

Theo thứ tự (giống `idea`/`partner`): argument (`/traceability /path` hoặc slug) → tên/đường dẫn trong tin nhắn → `state/current.json` → chưa rõ thì hỏi. Nhiều `<slug>` trong `ideas/_index.json` → hỏi soi cho ý nào (hoặc cả project).

## Thân — sinh Traceability Report

### 1. Artifact Dashboard (theo D1) — mở bằng góc nhìn lãnh đạo

Một dòng mỗi giai đoạn: có/thiếu/rút-gọn · chủ sở hữu · cổng kế. Đứng đầu là 2–3 câu lãnh đạo: *đang ở GĐ mấy, thiếu lớn nhất, cổng đắt đã qua chưa*.

```
DASHBOARD — <project/slug>          Đang ở: GĐ<n> · Cổng đắt: [GĐ8 live slice: ? ][GĐ13 go/no-go: ? ]
GĐ  Artifact                     Trạng thái     Skill bổ sung   Cổng kế
0-5 Idea→Domain (idea)           ✓ / ~ / ✗      /idea           <cổng GĐ đang mở>
6   Architecture Brief+ADR       ✓ / ~ / ✗      /shape          Đủ vững chọn stack?
7   Tech Decision Matrix         ...            /stack          Stack chốt?
8   Live Slice Report (đắt)      ...            /skeleton       Live slice pass?
9   Roadmap+Backlog(Story/AC*)   ...            /backlog        Đủ để plan?
10  Module Map+Contract          ...            /modules        Ownership rõ?
11  Delivery Std+DoD*            ...            /delivery        Đạt DoD?
12  Test&Verification(mapping*)  ...            /uat            Đủ go-live?
13  Go/No-Go+Runbook+Rollback*(đắt) ...         /ship           GO/NO-GO?
14  Ops Dashboard+Metric         ...            /operate        Đạt mục tiêu?
```
`✓`=đủ · `~`=rút gọn hợp lệ (đủ-là-đủ) · `✗`=thiếu. `*`=never-skip (thiếu là báo dù việc nhỏ).

### 2. Kiểm Sợi traceability (theo C1)

Truy chuỗi bắt buộc cho từng item đang sống, chỉ ra mắt xích ĐỨT (cụ thể, không chỉ liệt kê):
```
Business Objective → Product Goal → Requirement → PRD → Epic → Feature
→ Story → AC → Test Case → PR → Release → Metric
```
Ví dụ báo đứt: "Feature *Case Search* không nối được về Business Objective nào" · "Story *Search by status* thiếu AC" · "Requirement *tìm theo trạng thái* chưa có Test Case". Luật tối thiểu (C1): mỗi PR link story · mỗi story thuộc feature · mỗi feature phục vụ một business objective.

### 3. Phần còn thiếu + nhắc skill

Mỗi gap một dòng: *thiếu gì → vì sao GĐ sau sẽ mù → chạy skill nào*. Bám Đủ-là-đủ (đừng đòi làm thừa); never-skip thì đánh dấu **bắt buộc**.

### 4. Cổng & security chưa đủ

Cổng nào chưa qua (D3, kèm ai duyệt); security đan giai đoạn nào còn trống (C2: data classification GĐ1, threat model GĐ6, secret GĐ8, scan GĐ11, SAST/DAST GĐ12, checklist GĐ13, monitoring GĐ14); open-Q còn treo.

### Tự soi trước khi chốt (bắt buộc)

1. Lãnh đạo đọc 3 câu đầu có biết *đang ở đâu + thiếu lớn nhất + cổng đắt qua chưa* không?
2. Mỗi "✗/thiếu" có bám artifact thật (hoặc mô tả user đưa), không đoán? Cái "không rõ" đã ghi rõ là không rõ chưa?
3. Không flag oan giai đoạn rút gọn hợp lệ; đã bắt đủ never-skip (Story/AC · DoD · test mapping · rollback+monitoring)?
4. Mỗi gap có trỏ ĐÚNG skill để bổ sung, và mình KHÔNG tự làm giai đoạn nào chứ?

## Bàn giao — nhắc, không làm hộ

```
═══ TRACEABILITY — <project/slug> ═══
Đang ở: GĐ<n>   Cổng đắt: live slice <?> · go/no-go <?>
Thiếu ưu tiên: <1–3 gap lớn nhất, kèm skill>
→ Bổ sung <artifact>: chạy /<skill>   (lặp cho từng gap)
→ Muốn được dẫn đi tiếp cả pipeline: chạy /partner
→ Muốn chấm chất lượng một artifact đã có: chạy /grade
════════════════
```
Chỉ liệt kê, KHÔNG tự chọn hộ hay tự chạy skill.

## State

Ghi `state/current.json` (`{ "project", "updated_at" }`). Ghi snapshot `state/project/<project-name>/pipeline/_traceability.md` (dashboard + gap tại thời điểm soi) + `_traceability.json`:
```json
{ "project": "/duong/dan", "slug": "case-management", "updated_at": "<ISO>",
  "dang_o_gd": 9,
  "co": ["gd0_5_idea","gd6_shape","gd7_stack","gd8_skeleton"],
  "thieu": ["gd9_backlog: Story/AC (bắt buộc)","gd11_delivery: DoD (bắt buộc)"],
  "chain_dut": ["Feature 'Case Search' chưa nối Business Objective"],
  "cong_dat": ["gd8_live_slice_pass"] }
```
KHÔNG đụng file state/artifact của skill khác (read-only).

## Ví dụ Case Management (rút gọn)

```
Góc nhìn lãnh đạo: Pipeline đang ở GĐ9. Cổng đắt GĐ8 (live slice) ĐÃ pass — kiến trúc chứng minh chạy.
  Thiếu lớn nhất: Backlog chưa có AC cho 2 feature (never-skip) → chưa thể lập kế hoạch tin cậy.

DASHBOARD:
GĐ0-5 Idea→Domain      ✓   (idea: rule "reviewer không tự duyệt" đã chốt)
GĐ6   Architecture+ADR ✓   (modular monolith, 2 ADR có phương án loại)
GĐ7   Tech Decision    ✓   (NestJS+Postgres, matrix có điểm)
GĐ8   Live Slice       ✓   (staging chạy "tạo case" E2E — cổng đắt qua)
GĐ9   Roadmap+Backlog  ~→✗ Roadmap có, nhưng Feature "Case Search" & "Approve" THIẾU AC (*bắt buộc)
GĐ10+ Module…Operate   ✗   chưa mở

Sợi đứt: Feature "Case Search" chưa nối được về Business Objective "giảm 40% thời gian".
Thiếu (ưu tiên):
- AC cho 2 feature (never-skip) → chạy /backlog.  [chặn lập kế hoạch]
- Module Map + owner → chạy /modules (sau khi backlog xong).
Cổng chưa qua: GĐ9 "Backlog đủ để plan?" (PO+Tech). Security: threat model GĐ6 đã có; secret GĐ8 ok.

→ Bổ sung AC: /backlog · Muốn được dẫn tiếp: /partner
```

## Phạm vi với project workspace (`projects/<key>/`)

Project quản bằng workspace đã có tháp kiểm soát riêng: `/resume` (toàn cảnh + tiến cử), `progress/progress.json` (đồ thị task), phiếu `progress/checkpoints/` (từng bước) — dùng chúng, KHÔNG chạy `traceability` chồng lên (sẽ báo thiếu sai vì nó đọc `state/pipeline/`). `traceability` phục vụ project quản kiểu cũ qua `state/project/<key>/pipeline/` (vd `hex-agent-rebuild`). Khi project state-based cuối cùng migrate sang workspace → cân nhắc cất skill này vào `archive/skills/`.
