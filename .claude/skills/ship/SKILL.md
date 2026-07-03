---
name: ship
description: Chốt quyết định go-live AN TOÀN cho MỘT release — biến một bản đã kiểm thử thành release có cổng, có đường lùi. Sinh Go/No-Go Checklist + Runbook + Rollback Plan + Rollout Strategy (internal alpha→pilot→beta→gradual→full), chốt bằng cổng GO/NO-GO do CTO + PO ký. Là GĐ13 (SHIP) của pipeline Idea→Operate; nhận Test & Verification Report từ `uat` (GĐ12), bàn giao vận hành sang `operate` (GĐ14). Dùng khi "chuẩn bị release", "go-live", "deploy production", "release readiness", "làm runbook", "kế hoạch rollback", "rollout dần", "quyết go/no-go", "checklist go/no-go", "sắp lên production chưa".
---

# Ship — Release Readiness & Rollout: một trang để CEO/CTO KÝ cho lên (GĐ13)

`ship` là GĐ13 (SHIP) của pipeline doanh nghiệp **Idea→Operate**. Một việc: biến "code đã pass UAT" thành một **quyết định go-live có bằng chứng an toàn** — không phải "merge xong là deploy". Sinh đúng bốn artifact ghép trên MỘT trang: **Go/No-Go Checklist** (mỗi dòng owner + trạng thái), **Runbook** (deploy / kiểm tra sau deploy / rollback từng bước), **Rollback Plan** (đã test nếu hệ quan trọng), **Rollout Strategy** (internal alpha → pilot → beta → gradual → full). Chốt bằng một cổng **GO / NO-GO** mà CTO + PO ký.

Trang này KHÔNG viết cho mình đọc. Nó viết cho đội của DOANH NGHIỆP KHÁCH HÀNG — CEO/CTO ký để cho lên, người trực sự cố cầm để hành động lúc 2 giờ sáng. Vì vậy `ship` mở bằng **Góc nhìn lãnh đạo trước** (sẵn sàng chưa · ký cái gì · hỏng thì lùi ra sao + ai trực), rồi mới tới runbook kỹ thuật.

Phân vai — mỗi skill lo một khúc, `ship` không lấn:
- `idea` = GĐ0–5, làm rõ ý tưởng tới Domain rồi dừng. `partner` = điều phối trọn pipeline 15 giai đoạn; có thể gọi `ship` như một chặng.
- `frame` / `delivery` = đóng khung + code MỘT slice — `ship` KHÔNG viết code tính năng, chỉ dàn cảnh phát hành (flag, deploy step, rollback step). `review` = đào gap/edge case sâu.
- `uat` = GĐ12 ngay trước: chứng minh hệ làm ĐÚNG, ký UAT + Security. `ship` NHẬN sign-off đó làm đầu vào, KHÔNG kiểm lại chất lượng test.
- `operate` = GĐ14 ngay sau: vận hành, đo, đóng vòng về roadmap. `ship` bàn giao sang, KHÔNG tự dựng ops dashboard dài hạn.

Ranh giới một câu: `uat` trả lời "hệ có đúng không"; `ship` trả lời "**đưa lên có an toàn không, và lên bằng cách nào để lỡ sai thì lùi được**"; `operate` trả lời "lên rồi chạy ra sao".

Nguồn template đầy đủ: `quy-trinh-idea-to-operate.md` mục "## Giai đoạn 13 —". `ship` bám ĐÚNG 8 ô của mục đó (Mục tiêu / Chủ sở hữu-Người duyệt / Chạy song song / Artifact template / Ví dụ / Đủ-là-đủ / Góc nhìn lãnh đạo / Cổng). Việc nhỏ dùng bản rút gọn dưới đây; release lớn/rủi ro cao mở file gốc.

## Luật cứng

- **Hợp đồng đọc-được 3 tầng (lý do skill tồn tại — không bao giờ bỏ).** Người đọc là đội NGOÀI — CTO, business, dev — không có kiến thức nội bộ. Mọi artifact PHẢI **mở** bằng **Góc nhìn lãnh đạo** (ĐÚNG 1–3 thứ CEO/CTO nhìn để bấm GO: sẵn sàng chưa · ký cái gì · rủi ro tệ nhất + ai lo), ngôn ngữ nghiệp vụ, không jargon; **rồi mới** tới chi tiết kỹ thuật đủ để DEV bấm nút deploy/rollback theo được. Một trang, scan 2–3 phút.
- **Đủ-là-đủ.** Độ sâu tỉ lệ RỦI RO/ẨN SỐ của release, không theo vị trí trong luồng. Sửa nhỏ / đổi copy sau flag / không migration → Go/No-Go vài dòng, rollback = tắt flag, rollout có thể full ngay (ghi lý do dám). Hệ quan trọng / có data migration / lần đầu lên production / nhiều bên phụ thuộc → đầy đủ, rollback **phải test trước**, rollout đi từng nấc. KHÔNG bao giờ bỏ một trong bốn artifact hay bỏ ô nào của checklist — chỉ rút gọn độ sâu; ô không áp dụng ghi **"N/A + lý do"**, không xoá.
- **Cổng chặt: khuyết là NO-GO.** Bốn thứ không thương lượng — **rollback** (đã test nếu hệ quan trọng) · **monitoring/alert đã bật** · **incident owner đã có tên** · **UAT + Security sign-off từ GĐ12**. Thiếu một → NO-GO, ghi rõ thiếu gì, không "cho lên rồi vá sau".
- **Không lấn vai skill khác.** Không viết/sửa code tính năng (đó là `frame`/`delivery`), không kiểm lại chất lượng test (đó là `uat`), không dựng ops dashboard dài hạn (đó là `operate`). Phát hiện test còn hở → trả ngược về `uat`, không tự vá.
- **Mỗi quyết định lớn ghi LÝ DO + phương án đã loại.** Chọn blue-green thay canary, rollback bằng tắt flag chứ không rollback DB, rollout 2 tuần thay 1 ngày, "GO có điều kiện" thay "NO-GO" — đều ghi vì sao + đã cân nhắc gì. Để sau audit được vì sao dám cho lên.
- **Không tự ghi artifact vào repo code** trừ khi user đồng ý (theo `idea`). Mặc định ghi vào vùng state của skill; muốn commit runbook vào repo đích → HỎI trước.
- **`ship` KHÔNG tự bấm GO.** Cổng go/no-go là quyết định của Người duyệt (CTO + PO). `ship` (vai Release manager/Tech lead) chuẩn bị đủ để họ quyết + đưa khuyến nghị kèm lý do — không tự cho lên.
- **Cấm câu phủ định cứng khi phản biện** (kế thừa `partner`/`idea`): không "không thể", "không được deploy", "sai rồi". NO-GO luôn kèm **điều kiện để chuyển thành GO** — thiếu gì · ai làm · bao lâu.

## Đầu vào — đọc trước khi hỏi

1. **Test & Verification Report (GĐ12, từ `uat`)** — nguồn CHÍNH. Lấy: tỷ lệ pass từng lớp test, **UAT sign-off + Security sign-off** (bắt buộc có trước khi ký GO), gap/known issue còn treo, kết quả DR/rollback test nếu `uat` đã chạy. Còn Fail/gap hở → đó là NO-GO tiềm năng, nêu ra. Không có report này → chưa đủ điều kiện mở cổng GO.
2. **State** — `state/current.json` (project đang mở) + `state/project/<project-name>/pipeline/uat.md` (artifact GĐ12) và các artifact GĐ trước nếu có (PRD GĐ4 cho rollout/comms · Domain GĐ5 cho migration dữ liệu · Delivery/Modules GĐ10–11 cho flag/contract nào đụng khi rollback).
3. **`.ai-understanding/`** (atlas, nếu brownfield) — để biết hệ deploy kiểu gì, có gì downstream phụ thuộc, dữ liệu nào nhạy cảm khi migration, đường rollback thực tế không phá dữ liệu cũ.

Nếu KHÔNG có report GĐ12 trong state VÀ user cũng không đưa nguồn nào ngoài → gợi ý chạy `/uat` trước để có Test & Verification Report đã qua cổng; nếu user ĐÃ đưa report qua prompt/file → chạy kèm ⚠️ cảnh báo theo mục "Đầu vào ngoài state" dưới đây. Dù nguồn nào, mảnh nào chưa có thì ghi thành **giả định**/open-Q (dòng "UAT + Security sign-off = CHƯA CÓ — chặn GO"), KHÔNG bịa là đã ký cho đủ.

## Đầu vào ngoài state (nới — nhận prompt/file thay cho artifact GĐ trước)

Không có Test & Verification Report trong state VẪN chạy được nếu user mô tả trực tiếp trong prompt, dán nội dung, hoặc trỏ một file ngoài. Thứ tự ưu tiên: (1) đọc state pipeline; (2) không có thì nhận Test & Verification Report từ prompt/file user đưa; (3) vẫn không có gì thì mới gợi ý chạy /uat.

Khi chạy bằng nguồn NGOÀI (không phải Test & Verification Report của GĐ12 đã qua cổng), in NGUYÊN block cảnh báo này NGAY TRƯỚC khi làm, rồi VẪN tiếp tục — đây là cảnh báo, KHÔNG phải chặn:

```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Test & Verification Report" lấy từ prompt/file bạn đưa, CHƯA qua cổng GĐ12 (skill /uat).
- Rủi ro: (1) chưa truy vết ngược được về pipeline; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /uat trước để có "Test & Verification Report" đã qua cổng.
```

Nếu Test & Verification Report user đưa thiếu mảnh quan trọng → vẫn chạy, ghi rõ mảnh thiếu thành open-Q, KHÔNG tự bịa cho đủ.

## Bước 0 — Xác định project + release

Theo thứ tự (giống `idea`/`partner`): (1) argument truyền vào (vd `/ship /Users/foo/my-app`) → (2) path/tên nhắc trong tin nhắn → (3) `state/current.json` → (4) chưa có → hỏi một slug kebab-case ngắn (vd `case-mgmt`) làm `<project-name>` (greenfield); hoặc hỏi thẳng path.

Có path thì xác nhận tồn tại:
```bash
ls <project-path> 2>/dev/null | head -5 || echo "NOT_FOUND"
```
`NOT_FOUND` → báo lỗi, hỏi lại. Xác định **release đang chuẩn bị** (vd `v1.4.0`) — một project có thể ship nhiều release, mỗi release một artifact riêng. Không có Test Report GĐ12 → nói rõ `ship` cần nó trước; hỏi user muốn nhập tay tình trạng test hay chạy `/uat` trước.

## Thân — dựng MỘT trang SHIP (4 artifact ghép, lãnh đạo đọc trước)

Trước tiên hỏi một cụm (≤3 câu, AskUserQuestion khi chốt): **hệ này có quan trọng / có migration dữ liệu không** (quyết rollback phải-test hay không) · **rollout muốn chia pha hay full ngay** · **ai là incident owner khi lên**. Câu trả lời quyết độ sâu (Đủ-là-đủ). Rồi dựng trang theo đúng thứ tự đọc; mỗi artifact mở bằng **Góc nhìn lãnh đạo** rồi tới chi tiết dev.

**0) Góc nhìn lãnh đạo (MỞ ĐẦU — 1–3 dòng, đọc trước mọi thứ).** Sẵn sàng lên chưa (tóm tắt) · CEO/CTO ký cái gì · nếu hỏng thì rollback thế nào + ai trực. Đây là tài liệu **ký để cho lên**, không jargon.
- *Đủ-là-đủ:* việc nhỏ → 1 dòng "vá nhỏ, có flag, rollback tức thì, không cần ký cấp cao". Release lớn → 3 dòng đủ để lãnh đạo quyết mà không cần đọc runbook.

**1) Go/No-Go Checklist — trái tim của trang.** Mỗi dòng: **hạng mục + owner + trạng thái** (`[x]` xong / `[ ]` chưa / `N/A + lý do`). Đủ 12 ô của template GĐ13, không bỏ ô nào:
```
Release note · Deployment plan · Rollback plan (đã test nếu hệ quan trọng) · Data migration plan ·
Feature flag plan · User communication · Training material · Support playbook ·
Monitoring dashboard + alert rule · Incident owner đã phân công · UAT sign-off · Security sign-off
                                                              (2 cái cuối kéo từ GĐ12)
```
- *Đủ-là-đủ:* việc nhỏ → nhiều ô "N/A + lý do" (vd không migration → "N/A: không đổi schema"), vẫn giữ 4 thứ chặn. Hệ quan trọng → mọi ô có owner thật + trạng thái thật.
- *Góc nhìn lãnh đạo:* một bảng — mỗi dòng ai chịu, xanh hay đỏ, CTO nhìn 10 giây biết còn vướng gì. Dòng đỏ = chưa được ký.

**2) Rollback Plan — đường lùi (viết TRƯỚC khi lên).** Trả lời 3 câu: **tín hiệu nào thì lùi** (ngưỡng error/P95 vượt bao nhiêu, trong bao lâu) · **lùi bằng cách nào** (tắt flag / redeploy bản cũ / chạy script backward) · **dữ liệu sinh ra trong lúc lỗi xử lý sao** (giữ / migrate ngược / bỏ). Ghi lý do + phương án loại nếu chọn cách này thay cách khác.
- *Đủ-là-đủ:* có flag → "tắt flag `x`, tức thì". Có schema change → forward + backward script, nêu điểm không lùi được (point of no return) nếu có; hệ quan trọng → ghi rõ "đã test rollback trên staging ngày __" (chưa test → đây là dòng chặn GO).
- *Góc nhìn lãnh đạo:* "Nếu hỏng, X phút quay lại trạng thái an toàn, mất dữ liệu gì không, người trực là <ai>."

**3) Runbook — cẩm nang thao tác cho dev trực.** Ba khối đánh số bước rõ: **các bước deploy** → **kiểm tra sau deploy** (smoke check, endpoint/health/metric nào phải xanh trước khi mở rộng) → **các bước rollback** (khớp Rollback Plan, ai bấm). Cụ thể tới mức người KHÁC (không phải tác giả) làm theo được lúc nửa đêm.
- Deploy: kiểu triển khai (blue-green/canary/rolling — ghi **lý do chọn** + phương án loại), lệnh/nút, thứ tự bật flag. Ghi rõ ngưỡng alert nào là "hỏng, rollback ngay".
- *Đủ-là-đủ:* deploy quen (một lệnh CI) → checklist ngắn. Blue-green / migration nhiều bước → đánh số đầy đủ, mỗi bước có "kỳ vọng thấy gì".
- *Góc nhìn lãnh đạo:* không cần đọc chi tiết — chỉ cần biết "có runbook, người trực theo được mà không cần tác giả". Nhưng phải CÓ, để không ai deploy bằng trí nhớ.

**4) Rollout Strategy — lên DẦN, mỗi bậc một cổng nhỏ.** Bậc thang chuẩn: **internal alpha → pilot group → beta → gradual rollout → full.** Mỗi bậc ghi: **ai / bao nhiêu %** · **quan sát bao lâu** · **tín hiệu để tiến bậc kế / dừng lại** (error rate, P95, phản hồi user) · **đường lùi ở bậc đó** (thường: tắt flag, quay lại quy trình cũ song song).
- Chọn số bậc theo rủi ro: sửa nhỏ có flag → gộp ("pilot 1 tổ 1 tuần → full", ghi lý do dám bỏ bậc). Hệ mới / đụng dữ liệu người dùng → đủ 5 bậc, mỗi bậc một cổng có ngưỡng số.
- *Góc nhìn lãnh đạo:* "Lên theo <n> bậc, mỗi bậc có tín hiệu tiến/lùi, không bật 100% một phát." Lãnh đạo yên tâm vì rủi ro chia nhỏ.

## Tự soi trước khi chốt

Trước khi trình cổng, tự hỏi:
- **Lãnh đạo đọc đoạn đầu có biết "cho lên an toàn không, ký gì, hỏng thì lùi ra sao"** — mà không cần đọc runbook hay hỏi dev?
- **Người trực sự cố cầm Runbook + Rollback có thao tác được không cần đoán** lúc nửa đêm (bước cụ thể, ngưỡng rõ)?
- **Đúng + đủ bốn artifact chưa?** Go/No-Go, Runbook, Rollback, Rollout — có mặt cả bốn + đủ 12 ô (ô không dùng ghi N/A, không xoá)?
- **Bốn thứ chặn có mặt chưa?** rollback (đã test nếu hệ quan trọng) · monitoring/alert bật · incident owner có tên · UAT+Security sign-off KÉO từ GĐ12 (không bịa "đã ký"). Thiếu → NO-GO.
- **Có tự bấm GO không?** (không được — chỉ khuyến nghị, CTO+PO quyết.)
Vướng ô nào → sửa TRƯỚC khi trình cổng.

## Cổng GO / NO-GO (phân vai A5) + Bàn giao sang `operate`

Cổng là câu hỏi cho **Người duyệt = CTO + PO** (không phải AI tự quyết go-live). `ship` trình đủ bốn artifact + nêu rõ các dòng còn chặn + đưa khuyến nghị kèm lý do + phương án đã loại, rồi hỏi:
```
═══ CỔNG GO / NO-GO — <project> <release> ═══
Sẵn sàng: <n>/<m> dòng checklist xong · rollback <đã test / chưa> · monitoring <bật / chưa> · trực sự cố <ai>
Còn chặn: <liệt kê dòng [ ] + lý do — vd "UAT sign-off chưa có">  | (không có → "sạch")
Rollout: <full / pha nào trước>
Khuyến nghị của ship: GO / NO-GO / GO-có-điều-kiện — vì <lý do + phương án đã loại>
  (NO-GO → còn thiếu: <việc> · ai: <owner> · xong khi: <mốc> → rồi GO lại)
→ Người duyệt (CTO + PO) quyết: GO / NO-GO?
════════════════
```
NO-GO không phải điểm chết: luôn kèm **thiếu gì · ai làm · bao lâu** để chuyển thành GO. GO được ký → ghi người ký + ngày vào Go/No-Go, rồi bàn giao (chỉ liệt kê, không tự chọn hộ):
```
═══ BÀN GIAO — <project> <release> đã lên ═══
Đã lên: <pha rollout hiện tại> bắt đầu <ngày>   Runbook + Rollback: <đường dẫn file>
Đang trực sự cố: <owner>   Monitoring/alert: <đã bật, metric cần theo dõi + ngưỡng>
→ Vận hành, đo metric sau release, đóng vòng với Business Case (GĐ1) và nạp roadmap kế (GĐ14): chạy /operate
→ Rollout còn pha sau chưa mở: quay lại /ship khi tới mốc mở pha kế
→ Rollout gặp sự cố cần lùi: theo Rollback Plan trong artifact; sự cố lớn → /operate xử incident
→ Phát hiện gap chất lượng phải kiểm lại: quay về /uat (hoặc /review để đào lỗi sâu)
════════════════
```

## State — ghi vào vùng skill, KHÔNG vào repo code

- Artifact (trang SHIP 4-trong-1) → `state/project/<project-name>/pipeline/ship.md` (một file/release; nhiều release thì `ship-<release>.md`). Chỉ ghi vào repo đích khi greenfield HOẶC user đồng ý.
- Cập nhật `state/current.json`:
```json
{ "project": "<project-path>", "release": "<vd v1.4.0>", "giai_doan": "gd13_ship",
  "quyet_dinh": "go | no_go | go_co_dieu_kien | cho_duyet", "updated_at": "<ISO 8601>" }
```
- Ghi con trỏ pipeline (giai đoạn, quyết định GO/NO-GO, rollout đang ở pha nào) để `operate` resume được. `quyet_dinh: "cho_duyet"` = đã đưa cổng, đang chờ CTO+PO — resume thì nhắc lại khối cổng, KHÔNG tự đi tiếp.

## Ví dụ Case Management (rút gọn — cùng case với doc)

```
Nhận từ GĐ12 (uat): unit 312/312 · perf P95 210ms (đạt <500ms) · security 0 high ·
                     UAT ✔ PO (15/09) · Security ✔ CISO (16/09). Gap: 0.

GÓC NHÌN LÃNH ĐẠO — Case Management v1.4.0
  Sẵn sàng lên: 12/12 dòng xanh, UAT ✔ + Security ✔ từ GĐ12. Ký để cho lên.
  Nếu hỏng: tắt flag `case_create`/`case_search`, quay lại Excel song song — trong vài phút. Trực: Tech lead Team A.

GO/NO-GO CHECKLIST (owner · trạng thái)
  [x] Release note (COO)  [x] Deploy plan blue-green (chọn vì zero-downtime, loại canary do đội nhỏ)
  [x] Rollback ĐÃ TEST trên staging (18/09, PASS)  [x] Migration cases/status_history — forward + backward
  [x] Flag `case_create`,`case_search`  [x] Comms gửi 40 NV (PO)  [x] Training 2 buổi  [x] Support playbook
  [x] Dashboard + alert P95/error  [x] Incident owner: Tech lead Team A
  [x] UAT ✔ (PO 15/09) · Security ✔ (CISO 16/09) — kéo từ GĐ12

ROLLBACK: tắt 2 flag → quay lại Excel song song (<5 phút, không mất dữ liệu); bản ghi mới migrate ngược bằng
          backward script. Đã test staging 18/09.
RUNBOOK : deploy blue-green → smoke (health + tạo 1 case + tìm theo trạng thái phải xanh) → bật flag 100% pilot.
          Alert P95>500ms hoặc error>2% trong 10' → switch về blue + tắt flag.
ROLLOUT : pilot Tổ 1 (2 tuần, tín hiệu tiến: error<1% + PO OK) → beta 50% → full. Rollback mỗi bậc = tắt flag.
          (Lý do có pilot: lần đầu đụng dữ liệu hồ sơ thật → không full ngay.)

CỔNG: sẵn sàng 12/12, rollback đã test, monitoring bật, không dòng chặn → khuyến nghị GO.
QUYẾT ĐỊNH: GO ✔ — Người duyệt CTO + COO quyết (20/09).
Bàn giao: rollout pilot bắt đầu 21/09 → /operate đo metric, đóng vòng target GĐ1 (12'→7'); mở beta khi tới mốc.
```

## Khi làm trong project workspace (`projects/<key>/`)

Nhận diện: user chỉ định `projects/<key>`, hoặc gói ngữ cảnh từ `resume`/`fanout` trỏ tới đó, hoặc `state/current.json` có trường `workspace`. Khi ấy:
- Bước 0 đọc thêm: `projects/<key>/constitution/` (nhất là `folders.md` + `definition-of-done.md`) và `progress/progress.json` — tìm task đang mở giao cho skill này (trường `owner`).
- Artifact người-đọc ghi vào ĐÍCH của task (trường `artifact` trong `progress.json`, đặt theo `folders.md`) — KHÔNG ghi bản chính vào `state/`. State máy riêng của skill (file json trạng thái) vẫn ở `state/project/<key>/` như cũ.
- Xong việc: báo user chạy `/checkpoint <task-id>` lấy phiếu rồi `/progress` đóng bước. Không tự lật done, không tự ghi `progress.json` — file đó một chủ (`progress`).
