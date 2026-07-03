# Traceability Report — MediRemind

> Soi một phát toàn pipeline Idea→Operate (15 GĐ). `traceability` chỉ KIỂM + NHẮC, không tự làm giai đoạn, không sửa artifact.
> Nguồn: `progress/progress.json` (nguồn sự thật của workspace) + `board.md` + 20 artifact trong `problem/ idea/ docs/ codebase/ constitution/` + code thật ở `fixture/codebase/mediremind/src/`. Đọc lúc 2026-07-03.

---

⚠️ CẢNH BÁO — soi bằng đầu vào NGOÀI convention của skill (đọc trước)

- MediRemind là **project workspace kiểu mới** (`projects/<key>/` với `constitution/` + `progress/progress.json` + `board.md`), KHÔNG phải state-based `state/project/<name>/pipeline/<skill>.json` mà `traceability` được thiết kế để đọc. Theo mục *"Phạm vi với project workspace"* của `SKILL.md`, đúng ra loại project này dùng `/resume` + `progress.json` + phiếu `checkpoints/`, **KHÔNG chạy `traceability` chồng lên**. Report này vẫn được sinh vì task yêu cầu, nhưng bức tranh dựng từ `progress.json`/artifact thật (nguồn tốt), KHÔNG từ file pipeline đã-qua-cổng chuẩn của skill.
- Rủi ro: (1) mapping GĐ ↔ task là suy diễn từ trường `giai_doan` trong `progress.json`, không phải cổng pipeline gốc; (2) snapshot này KHÔNG ghi vào `state/` (đây là workspace, không phải state-based); (3) một vài artifact được trỏ trong `progress.json` KHÔNG tồn tại đúng path — đã đối chiếu file thật và ghi rõ dưới.
- Vẫn báo theo artifact + progress đọc được. Muốn chính xác theo đúng công cụ: dùng `/resume` cho workspace này.

---

## Góc nhìn lãnh đạo (đọc trong 30 giây)

**Đang ở GĐ11 (Delivery/Build).** Chuỗi giấy GĐ0→GĐ10 (Idea→Domain→Architecture→Stack→Live Slice→Backlog→Module Map+Contract) **đầy đủ và nối liền** — mọi Epic nối ngược về SM-1/SM-2, mọi NFR có số cứng. Cổng đắt **GĐ8 live slice ĐÃ PASS** (staging + E2E 5/5 xanh + log): kiến trúc + stack + boundary đã chứng minh chạy được. Cổng đắt **GĐ13 go/no-go CHƯA QUA — đang NO-GO** (0/2 chữ ký, rollback chưa diễn tập).

**Thiếu lớn nhất (chặn go-live), theo thứ tự phụ thuộc:**
1. **GĐ11 build chưa đóng** — hai module `pg-build` (Scheduling T-11a ∥ Reminders T-11b) mới `ready`, chưa `done`; chưa có bằng chứng test-pyramid/DoD cho chúng → `/fanout` chạy song song, rồi `/checkpoint` + `/progress`.
2. **GĐ12 UAT hoàn toàn trống** (never-skip: test mapping) — chưa có Test & Verification Report → **chain Requirement→AC→Test→Result ĐỨT** → chạy `/uat`.
3. **GĐ13 ship NO-GO** (never-skip: rollback + monitoring): rollback chưa test thật, cổng 0/2 chữ ký, OQ-A/OQ-B còn treo trong ship.md → chạy `/ship` sau khi UAT xong.
4. **GĐ14 Operate chưa mở.**

**2 open-question treo** (OQ-A queue-vs-cron, OQ-B retention/NFR-4) — bắt buộc đóng bằng ADR trước cổng GĐ13.

---

## 1. Artifact Dashboard (D1)

```
DASHBOARD — mediremind        Đang ở: GĐ11 · Cổng đắt: [GĐ8 live slice: ✓ PASS][GĐ13 go/no-go: ✗ NO-GO]
```

| GĐ | Artifact | Trạng thái | Owner | Skill bổ sung | Cổng kế |
|---|---|---|---|---|---|
| 0 | Idea Brief (`idea/mediremind.md`) | ✓ | idea | /idea | — |
| 1 | Business Case + SM-1/SM-2 (`problem/business-case.md`) | ✓ | idea | /idea | — |
| 2–4 | Product Brief + Requirements + PRD, NFR-1..5 (`problem/product-brief.md`, `requirements.md`, `prd.md`) | ✓ | idea | /idea | — |
| 5 | Domain Model, 7 entity + 4 bounded context (`docs/domain-model.md`) | ✓ | idea | /idea | Domain xong? ✓ |
| 6 | Architecture Brief + C4 + 2 ADR (`docs/architecture.md`) | ✓ | shape | /shape | Đủ vững chọn stack? ✓ |
| 7 | Tech Decision Matrix + ADR-007 (`docs/tech-decision.md`) | ✓ | stack | /stack | Stack chốt? ✓ |
| 8 | Live Slice Report **(đắt)** (`docs/skeleton-live-slice.md`) | ✓ | skeleton | /skeleton | Live slice pass? ✓ PASS |
| 9 | Roadmap+Backlog (Epic→Feature→Story→AC*) (`docs/backlog.md`) | ✓ | backlog | /backlog | Đủ để plan? ✓ |
| 10 | Module Map + Contracts (`docs/module-map.md` + `docs/contracts/scheduling-v1.md`, `adherence-v1.md`) | ✓ | modules | /modules | Ownership rõ? ✓ |
| 11 | Delivery Std + DoD* + PR Checklist (`codebase/delivery-standards.md`) — **NHƯNG 2 module build chưa done** | ~ | delivery | /delivery, /fanout | Đạt DoD? CHƯA |
| 12 | Test & Verification (mapping Req→AC→Test*) | ✗ | uat | /uat | Đủ go-live? CHƯA |
| 13 | Go/No-Go + Runbook + Rollback* + Rollout **(đắt)** (`codebase/ship.md`) — **NO-GO** | ~→✗ | ship | /ship | GO/NO-GO? **NO-GO** |
| 14 | Ops Dashboard + Metric + Incident + Iteration Loop | ✗ | operate | /operate | Đạt mục tiêu? — |

`✓`=đủ · `~`=có nhưng chưa đóng cổng / rút gọn · `✗`=thiếu · `*`=never-skip.

**Ghi chú trạng thái (bám nguồn, không đoán):**
- **GĐ11 = `~`, KHÔNG phải `✓`:** Delivery Standards + DoD + PR Checklist đã đủ (never-skip DoD có mặt — `delivery-standards.md §DoD`). NHƯNG hai task build `T-11a` (Scheduling) và `T-11b` (Reminders) trong `progress.json` đang **`ready`**, chưa `done` → GĐ11 chưa đóng. Code `src/scheduling/dose-generator.service.ts`, `src/reminders/reminder.worker.ts`, `reminder.service.ts` CÓ tồn tại trên đĩa, nhưng progress chưa lật done và **không có bằng chứng test-pyramid/phiếu checkpoint** cho hai module → theo Định-nghĩa-Xong của project (artifact + phiếu PASS + progress) thì chưa xong. **Không rõ** hai module đã đạt DoD hay chưa — progress nói chưa.
- **GĐ13 `ship.md` CÓ tồn tại nhưng KHÔNG nằm trong `progress.json`** (task list dừng ở T-12). Tự bản thân ship.md tuyên bố **NO-GO** với 2 gap cài sẵn (rollback chưa test, cổng 0/2 chữ ký). Vẽ `~→✗`: có bản nháp ship nhưng cổng chưa qua và phụ thuộc GĐ12 (chưa có) → thực chất chưa tới lượt đóng.

**⚠️ Lệch giữa `progress.json` và file thật trên đĩa (đã đối chiếu):**

| Task | Path progress.json khai | File THẬT trên đĩa | Kết luận |
|---|---|---|---|
| T-06 (GĐ8) | `codebase/live-slice-report.md` | `docs/skeleton-live-slice.md` | Artifact CÓ, nhưng path trong progress **sai** |
| T-07 (GĐ9) | `docs/roadmap.md` | `docs/backlog.md` (chứa cả Roadmap) | Artifact CÓ, path progress **sai** |
| T-08 (GĐ10) | `docs/contracts/module-contract-v1.md` | `docs/module-map.md` + `contracts/scheduling-v1.md` + `adherence-v1.md` | Artifact CÓ (tách 3 file), path progress **sai** |
| T-12 (GĐ12) | `codebase/uat-report.md` | (không tồn tại) | Đúng — GĐ12 chưa làm, T-12=todo |
| — (GĐ13) | (không có task) | `codebase/ship.md` tồn tại | ship.md có mặt nhưng **progress không track** |

Đây là gap **traceability nội bộ**: sổ tiến độ trỏ tới path không khớp file thật. Không chặn nội dung, nhưng làm tự-động-kiểm (checkpoint/resume) trỏ nhầm. → Nhắc: `/progress` cập nhật lại `artifact` path cho T-06/T-07/T-08 và thêm task GĐ13 cho ship.md.

---

## 2. Kiểm Sợi traceability (C1)

Chuỗi bắt buộc: **Business Objective → Product Goal → Requirement → PRD → Epic → Feature → Story → AC → Test Case → PR → Release → Metric**

**Nối liền tới AC (GĐ0–9):**
- **SM-1** (on-time dose +≥15đpt) → Product Brief (vòng giá trị lõi) → NFR-1/NFR-2 → PRD §1 → **E1/E2/E3** → F1.1..F3.2 → US-1.1.1..US-3.2.1 → **AC Given/When/Then đầy đủ**. ✓ liền.
- **SM-2** (≥60% caregiver-link) → PRD §3 → **E4** → F4.1/F4.2 → US-4.1.1/US-4.2.1 → AC (gồm audit-log NFR-4). ✓ liền.
- **NFR-4** (nhạy cảm/audit) → **E5** → F5.1/F5.2 → US-5.1.1/US-5.2.1 → AC. ✓ liền (F5.2 cố tình để hở OQ-B, ghi rõ trong story — hợp lệ, không tính đứt).
- Mỗi Feature nối được về một business objective (backlog §3 "Truy vết Epic → business value" liệt kê tường minh). ✓ Không có feature mồ côi.

**Mắt xích ĐỨT (cụ thể):**
- 🔴 **AC → Test Case ĐỨT toàn bộ:** GĐ12 chưa có Test & Verification Report. Mọi AC ở `backlog.md` (AC-1..AC-2 của F1.1→F5.2) **chưa có Test Case nào map tới**. Ví dụ cụ thể: AC-2 của **US-3.1.1** ("liều của user khác → 403") — đây chính là khiếm khuyết authorization ô #5 của Live Slice Report — **chưa có Test Case chứng minh đã đóng**. → chuỗi Req→AC→**Test**→Result đứt ở nhịp Test. (never-skip)
- 🔴 **AC → PR → Release ĐỨT:** hai module build (T-11a/T-11b) chưa done, chưa có PR/Release nào link về Story. Ví dụ: **US-3.1.1** (xác nhận liều an toàn quyền) chưa nối được tới PR nào đóng nó; **US-2.1.1** (dedupe reminder, chặn lỗi gửi lặp thấy ở slice) chưa có PR.
- 🟡 **Metric (SM-1/SM-2) chưa có đường đo runtime:** cột cuối của sợi (Release→Metric) chỉ tồn tại ở mức kế hoạch (`ship.md` Rollout theo dõi SM-1/SM-2, `delivery-standards.md §8` liệt kê metric NFR). Chưa có Ops Dashboard (GĐ14) để SM-1/SM-2 được ĐO thật → đuôi sợi treo cho tới GĐ14.

**Luật tối thiểu C1:** mỗi story thuộc feature ✓ · mỗi feature phục vụ một objective ✓ · mỗi PR link story → **chưa kiểm được vì chưa có PR** (build chưa đóng).

---

## 3. Phần còn thiếu + nhắc skill (theo thứ tự phụ thuộc)

| # | Thiếu gì | Vì sao GĐ sau sẽ mù | Chạy skill | Bắt buộc? |
|---|---|---|---|---|
| 1 | **GĐ11 build 2 module chưa done** (T-11a Scheduling ∥ T-11b Reminders còn `ready`, chưa có test-pyramid/phiếu) | Không có code đã-đạt-DoD thì UAT không có gì để verify; chain AC→PR đứt | `/fanout` (chạy pg-build song song) → `/checkpoint` từng task → `/progress` lật done | — (DoD chuẩn ĐÃ có) |
| 2 | **GĐ12 Test & Verification Report** — mapping Requirement→AC→Test→Result→Decision + UAT sign-off + Security sign-off | Không có test mapping thì cổng go-live mù; chain Req→Test đứt hoàn toàn | `/uat` (sau khi #1 done) | **BẮT BUỘC** (never-skip: test mapping) |
| 3 | **GĐ13 rollback CHƯA diễn tập + cổng 0/2 chữ ký** (ship.md đang NO-GO) | Release không có đường lùi đã-thử = rủi ro không đo được; go-live không an toàn | `/ship` (sau khi #2 xong; cần CTO+PO ký) | **BẮT BUỘC** (never-skip: rollback + monitoring) |
| 4 | **GĐ14 Ops Dashboard + Incident + Iteration Loop** — chưa mở | SM-1/SM-2 không được ĐO thật; không đóng được vòng học về GĐ9; monitoring never-skip trống | `/operate` (sau go-live) | **BẮT BUỘC** (never-skip: monitoring) |
| 5 | **OQ-A** (managed queue vs cron) — progress nói `open`, NHƯNG `tech-decision.md §5` đã **ĐÓNG** bằng ADR-007 (BullMQ/Redis) | Không mù GĐ sau; đây là **lệch state**: ADR đã đóng mà progress/ship.md vẫn ghi treo | `/progress` cập nhật OQ-A → closed (trỏ ADR-007); hoặc `/ship` đọc lại ADR | — |
| 6 | **OQ-B** (retention/NFR-4) — thật sự CÒN TREO (tech-decision, delivery-standards, backlog F5.2 đều xác nhận chưa chốt) | Cổng GĐ13 yêu cầu đóng OQ-B bằng ADR trước release; chưa đóng → chặn ship | Đóng bằng ADR (thuộc `/shape` hoặc quyết định retention của team) trước `/ship` | — (nhưng chặn cổng 13) |
| 7 | **Đồng bộ path trong `progress.json`** (T-06/T-07/T-08 trỏ sai file; ship.md không được track) | checkpoint/resume tự-động trỏ nhầm path → báo thiếu sai | `/progress` sửa trường `artifact` + thêm task GĐ13 | — |

**Đủ-là-đủ (D2):** KHÔNG flag oan — GĐ0–10 rút gọn hợp lệ đều đã có đủ. 4 never-skip đối chiếu: Story+AC (GĐ9) ✓ CÓ · DoD (GĐ11) ✓ CÓ · test mapping (GĐ12) ✗ THIẾU (báo) · rollback+monitoring (GĐ13/14) ✗ THIẾU (báo).

---

## 4. Cổng & Security chưa đủ (D3 + C2)

**Cổng chưa qua (kèm ai duyệt):**
- **GĐ11 → GĐ12:** module chỉ done khi code trỏ đúng path + test-pyramid + không nới NFR-4. T-11a/T-11b chưa done → **cổng CHƯA qua** (duyệt: checkpoint + delivery owner).
- **GĐ12:** thiếu Test & Verification Report → chain Req→Test đứt → **chưa đủ điều kiện xét go-live** (duyệt: UAT sign-off + Security sign-off).
- **GĐ13 GO/NO-GO:** hiện **0/2 chữ ký** (CTO ☐ · PO ☐), rollback chưa test, OQ-A/OQ-B ghi treo trong ship.md → **NO-GO** (duyệt: CTO + PO). *Lưu ý: ship.md ghi OQ-A còn treo, nhưng ADR-007 đã đóng OQ-A — cần đồng bộ trước khi ký.*

**Security đan giai đoạn (C2) — soi từng mốc:**
- **Data classification (GĐ1):** ✓ có — business-case.md §5 phân loại "dữ liệu sức khoẻ nhạy cảm", NFR-4 mã hoá at-rest + audit-log.
- **Threat/Security model (GĐ6):** ✓ có — architecture.md §6 Security Model (at-rest, access control theo role, audit-log caregiver, Identity là điểm chốt quyền).
- **Secret (GĐ8/11):** ✓ có chuẩn — delivery-standards.md §6 (secret manager, không commit). Live slice dùng in-memory db, chưa chạm secret thật (hợp lệ cho slice).
- **Scan/SAST/DAST (GĐ11/12):** 🟡 **không rõ** — delivery-standards.md §3 CI liệt kê lint→unit→integration→build, KHÔNG nêu SAST/DAST/dependency-scan. GĐ12 UAT (nơi Security sign-off sống) chưa có → security scan chưa có bằng chứng. → `/delivery` bổ sung bước scan vào CI; `/uat` cấp Security sign-off.
- **Checklist go-live (GĐ13):** ~ có bản nháp trong ship.md nhưng cổng chưa ký.
- **Monitoring (GĐ14):** ✗ trống — chưa có Ops Dashboard; audit-log NFR-4 mới ở mức chuẩn (delivery §8), chưa có dashboard đo thật.

**Open-Q còn treo:** OQ-A (đã đóng ở ADR-007 nhưng progress/ship chưa cập nhật — **lệch state**) · OQ-B (thật sự treo, chặn cổng 13).

---

## Tự soi trước khi chốt

1. Lãnh đạo đọc 3 câu đầu biết đang ở GĐ11, thiếu lớn nhất (build→UAT→ship), cổng đắt (GĐ8 ✓ / GĐ13 ✗ NO-GO)? ✓
2. Mỗi `✗/~` bám artifact thật? ✓ — GĐ11 `~` vì progress nói T-11a/b `ready`; GĐ12 `✗` vì không có file; GĐ13 `~→✗` vì ship.md tự tuyên NO-GO. Cái "không rõ" (2 module đạt DoD chưa, SAST/DAST) đã ghi "không rõ". ✓
3. Không flag oan GĐ0–10 rút gọn; bắt đủ 4 never-skip (Story/AC ✓có · DoD ✓có · test mapping ✗báo · rollback+monitoring ✗báo)? ✓
4. Mỗi gap trỏ đúng skill theo thứ tự phụ thuộc; KHÔNG tự làm giai đoạn nào? ✓ (chỉ nhắc `/fanout /uat /ship /operate /progress`, không tự sinh artifact).

---

```
═══ TRACEABILITY — mediremind ═══
Đang ở: GĐ11 (Build)   Cổng đắt: live slice ✓ PASS · go/no-go ✗ NO-GO
Thiếu ưu tiên:
  1. GĐ11 build 2 module chưa done (T-11a ∥ T-11b) → /fanout rồi /checkpoint + /progress
  2. GĐ12 UAT trống — chain Req→Test đứt (never-skip) → /uat
  3. GĐ13 rollback chưa test + cổng 0/2 chữ ký (never-skip) → /ship
  4. GĐ14 Operate/monitoring trống (never-skip) → /operate
  + Lệch state: OQ-A đã đóng ở ADR-007 mà progress/ship ghi treo; path T-06/07/08 sai → /progress
→ Bổ sung build:   chạy /fanout (pg-build) → /checkpoint → /progress
→ Bổ sung UAT:     chạy /uat
→ Bổ sung ship:    chạy /ship (cần CTO + PO ký; đóng OQ-B bằng ADR trước)
→ Bổ sung operate: chạy /operate
→ Muốn được dẫn đi tiếp cả pipeline: chạy /partner
→ Muốn chấm chất lượng một artifact đã có: chạy /grade
────────────────
(Lưu ý phạm vi: đây là project workspace — công cụ đúng để "đang ở đâu" là /resume + progress.json, không phải traceability. Xem cảnh báo đầu report.)
```
