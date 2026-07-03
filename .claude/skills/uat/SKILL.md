---
name: uat
description: 'Chứng minh hệ chạy ĐÚNG yêu cầu bằng bảng mapping có truy vết (Requirement → Acceptance Criteria → Test Case → Test Result → Release Decision), rồi lấy UAT sign-off + Security sign-off. Sinh artifact Test & Verification Report. Là GĐ12 pipeline Idea→Operate: nhận Delivery Standards + DoD từ `delivery` (GĐ11), bàn giao sang `ship` (GĐ13). Dùng khi "đã build xong, chứng minh nó chạy đúng", "UAT", "verification", "map yêu cầu với test", "ký nghiệm thu/security để go-live", "trước khi release cần bằng chứng gì", "đã test đủ chưa", "go-live được chưa về mặt test".'
---

# uat — Verification / UAT: chứng minh hệ chạy ĐÚNG bằng mapping có truy vết (GĐ12)

`uat` là **Giai đoạn 12 (Verification / UAT — PROOF IT WORKS)** của pipeline Idea→Operate. Nó sinh MỘT artifact: **Test & Verification Report** — bảng mapping `Requirement → Acceptance Criteria → Test Case → Test Result → Release Decision`, kèm **UAT sign-off** và **Security sign-off**. Không code, không sửa hệ, không tự deploy.

Vai gọn trong một câu: `uat` lo **BẰNG CHỨNG đã test đúng + hai chữ ký**, không lo đào lỗ hổng. Đặt cạnh các skill khác để khỏi lấn:
- `delivery` (GĐ11) = định Delivery Standards + DoD; test viết CÙNG code. `uat` nhận đầu ra đó rồi chứng minh từng AC đã có test + kết quả theo DoD.
- `review` = đào gap/edge case/error path/permission còn THIẾU sâu. `uat` KHÔNG tự đào. Thấy một AC chưa có test → ghi thành hở (gap) trong bảng và trỏ `/review`, không tự moi thêm case mới rồi coi như đủ. **Ranh giới sắc:** `review` HỎI "còn hở gì chưa test?"; `uat` TRẢ LỜI "những gì đã liệt kê thì đã test đúng chưa, ai ký?".
- `ship` (GĐ13) = Go/No-Go + Runbook + rollback. `uat` bàn giao bảng mapping + hai chữ ký sang `ship`; `uat` KHÔNG tự quyết deploy.
- `idea` (GĐ0–5), `frame` (đóng khung slice để code), `partner` (điều phối cả pipeline) — `uat` không làm việc của chúng.

`uat` chạy được ĐỘC LẬP (user gọi thẳng khi cần bằng chứng test cho một release) HOẶC do `partner` gọi trong chuỗi.

Nguồn playbook đầy đủ (template + ví dụ chuẩn): `quy-trinh-idea-to-operate.md`, mục "## Giai đoạn 12". Mở khi hệ lớn/rủi ro cao cần đủ lớp test.

## Luật cứng

- **Hợp đồng đọc-được 3 tầng (lý do skill tồn tại — tuyệt đối không bỏ).** Người đọc report là đội DOANH NGHIỆP KHÁCH HÀNG — CTO, business, dev — người NGOÀI, không biết nội bộ. Report phải: (1) MỞ bằng **Góc nhìn lãnh đạo** — đúng 1–3 thứ CEO/CTO nhìn để biết có nên cho lên không (tỷ lệ pass + hai chữ ký + một dòng "còn hở gì"), ngôn ngữ nghiệp vụ, không jargon; (2) RỒI mới tới bảng mapping + số liệu test đủ để DEV hành động; (3) 1 trang, scan 2–3 phút.
- **Đủ-là-đủ.** Độ sâu tỉ lệ RỦI RO/ẨN SỐ, không theo vị trí trong luồng. Slice nhỏ, rủi ro thấp, ít AC → mapping vài dòng + lớp test tối thiểu (unit+integration+UAT) là đủ. Hệ quan trọng / đụng tiền / đụng dữ liệu nhạy cảm → đủ các lớp (perf theo NFR, security SAST/DAST/pentest, a11y, DR/rollback). KHÔNG bao giờ bỏ mapping hay bỏ chữ ký — chỉ rút gọn độ sâu. Không nhồi lớp test hệ không cần chỉ để bảng trông đầy.
- **Không lấn vai.** Không đào gap/edge case mới (đó là `review`); không sửa code cho test xanh (đó là `frame`/`delivery`); không ra quyết định Go/No-Go cuối (đó là `ship`). `uat` chỉ tổng hợp bằng chứng + chuẩn bị hai chữ ký + nêu điều kiện đủ để go-live.
- **Mỗi quyết định lớn ghi LÝ DO + phương án đã loại.** Vd Release Decision "go-live v1.4.0" ghi vì sao (mọi AC blocker pass) và phương án đã loại ("hoãn 1 sprint thêm test perf — loại vì P95 đã đạt NFR"); "chưa chạy pentest vòng này — vì slice nội bộ rủi ro thấp, ghi là gap chuyển vòng sau". Để sau audit lại được.
- **Không tự ghi artifact vào repo code** trừ khi user đồng ý (theo `idea`). Mặc định ghi vào vùng state của skill.
- **Cấm câu phủ định cứng khi phản biện.** Không "không thể", "sai rồi", "không đạt là hết", "không go được" trơ trọi. AC fail → nêu chính xác cái fail + một lối đi (fix rồi re-test / tách khỏi scope release này / go-live có điều kiện với phần đã pass / chuyển `/review`).

## Đầu vào — đọc trước khi hỏi

- **Artifact GĐ11 (`delivery`)** — `state/project/<project-name>/pipeline/delivery.md`: Delivery Standards + Definition of Done + PR checklist đã link requirement/story. Đây là GỐC của sợi traceability và là chuẩn "một AC coi là đã verify" (test pass unit+integration, contract giữ, observability có…). Nối tiếp, không dựng lại.
- **`state/current.json`** — project đang mở.
- Ngược lên GĐ3–5 nếu cần đối chiếu Requirement/AC gốc: PRD/Requirement Catalogue (GĐ3–4), Domain (GĐ5) trong `state/project/<project-name>/pipeline/*.md` hoặc `ideas/`.
- **`.ai-understanding/`** (atlas, nếu có, brownfield) — để đối chiếu tên requirement/entity với code thật, gọi đúng tên test suite/contract, khỏi map nhầm.

Bám nguồn tuyệt đối: Requirement và AC trong bảng phải TRÍCH từ artifact GĐ trước, không tự chế yêu cầu mới. Không thấy `delivery.md`: nếu user ĐÃ đưa Delivery Standards + Definition of Done trong prompt/file → chạy kèm ⚠️ cảnh báo (theo mục "Đầu vào ngoài state" ngay dưới); nếu KHÔNG có gì → mới gợi ý chạy /delivery. Dù nguồn nào cũng KHÔNG bịa DoD hay yêu cầu user không đưa; ghi rõ đang thiếu mắt xích nào trong report.

## Đầu vào ngoài state (nới — nhận prompt/file thay cho artifact GĐ trước)

Không có Delivery Standards + Definition of Done trong state VẪN chạy được nếu user mô tả trực tiếp trong prompt, dán nội dung, hoặc trỏ một file ngoài. Thứ tự ưu tiên: (1) đọc state pipeline; (2) không có thì nhận Delivery Standards + Definition of Done từ prompt/file user đưa; (3) vẫn không có gì thì mới gợi ý chạy /delivery.

Khi chạy bằng nguồn NGOÀI (không phải Delivery Standards + Definition of Done của GĐ11 đã qua cổng), in NGUYÊN block cảnh báo này NGAY TRƯỚC khi làm, rồi VẪN tiếp tục — đây là cảnh báo, KHÔNG phải chặn:

```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Delivery Standards + Definition of Done" lấy từ prompt/file bạn đưa, CHƯA qua cổng GĐ11 (skill /delivery).
- Rủi ro: (1) chưa truy vết ngược được về pipeline; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /delivery trước để có "Delivery Standards + Definition of Done" đã qua cổng.
```

Nếu Delivery Standards + Definition of Done user đưa thiếu mảnh quan trọng → vẫn chạy, ghi rõ mảnh thiếu thành open-Q, KHÔNG tự bịa cho đủ.

## Bước 0 — Xác định project (giống `idea`/`partner`)

Lấy project theo thứ tự ưu tiên:
1. Argument truyền vào (vd `/uat /Users/foo/my-app`).
2. Đường dẫn/tên nhắc trong tin nhắn.
3. `state/current.json`.
4. Chưa có → hỏi một slug kebab-case ngắn làm `<project-name>` (greenfield, mới ghi thẳng repo được).

Có path thì xác nhận tồn tại:
```bash
ls <project-path> 2>/dev/null | head -5 || echo "NOT_FOUND"
```
`NOT_FOUND` → báo lỗi, hỏi lại. Không có artifact GĐ11 trong state → nhắc user rằng `uat` bình thường chạy sau `delivery`, hỏi có muốn tiếp tục từ AC/PRD không.

## Thân — dựng Test & Verification Report (đúng template GĐ12)

Đây là artifact duy nhất. Dựng theo thứ tự đọc-được-3-tầng: lãnh đạo trước, dev sau. Ba khối.

### 1) Góc nhìn lãnh đạo (mở đầu — viết TRƯỚC cả bảng)
Đúng những gì exec cần để tin "cho lên được", ngôn ngữ nghiệp vụ:
- **Tỷ lệ pass** trên tổng AC/test trong phạm vi (vd "18/18 AC có test, 17 PASS, 1 chặn release phần X").
- **Hai chữ ký**: **UAT sign-off** (PO) + **Security sign-off** (Sec/CISO) — có/chưa, ngày.
- **Còn hở gì**: một dòng — "không hở trong phạm vi", hoặc "AC-07 chưa có test → chuyển `/review`", hoặc điều kiện go-live. Không jargon, không số dòng code.

### 2) Bảng MAPPING (xương của artifact — không có là sau khó audit)
Mỗi AC trong phạm vi một dòng, nối nguyên sợi:
```text
Requirement → Acceptance Criteria → Test Case → Test Result → Release Decision
```
- **Requirement** — TRÍCH từ PRD/Requirement Catalogue (GĐ3–4).
- **AC** — điều kiện chấp nhận cụ thể, đo được.
- **Test Case** — mã TC ánh xạ (vd `TC-CASE-SEARCH-001`).
- **Test Result** — PASS / FAIL / BLOCKED (fail → kèm lối đi tiếp, không phán chết).
- **Release Decision** — đủ / chưa đủ điều kiện vào version nào.

Nối ngược lên PR/story của GĐ11 (Delivery) và requirement/PRD (GĐ3–4) — đây là chỗ traceability sống. AC nào **không tìm thấy test** → không im lặng: để trống Test Case + đánh dấu dòng đó là **hở (gap)**, và trong khối bàn giao trỏ `/review` để đào cho đủ. Đây là ranh giới: `uat` phát hiện hở, `review` lấp hở.

### 3) TEST & VERIFICATION REPORT (lớp test + hai chữ ký — chi tiết cho dev)
Bảng lớp test — Đủ-là-đủ chọn lớp theo rủi ro:
```text
Lớp test | Phạm vi | Pass/Fail | Ghi chú
unit · integration · contract · e2e · regression · perf · security(SAST/DAST/pentest) · a11y · UAT · operational readiness · DR/rollback (nếu hệ quan trọng)
UAT sign-off      : <PO> ngày __
Security sign-off : <Sec/CISO> ngày __
```
Lớp nào bỏ → ghi 1 dòng lý do (Đủ-là-đủ), không im lặng bỏ. Slice nhỏ nội bộ: unit+integration+UAT là đủ. Hệ quan trọng: đủ perf (gate theo NFR), DAST/pentest, a11y, DR/rollback với con số thật.

**Đủ-là-đủ cho artifact này:** mỗi AC có **test + kết quả**; có **UAT sign-off + Security sign-off** cho release. Không đủ hai chữ ký → chưa phải report hoàn chỉnh; ghi rõ đang chờ ai ký.

## Tự soi trước khi chốt

Trước khi đóng artifact, tự hỏi, vướng câu nào sửa câu đó:
- Lãnh đạo đọc RIÊNG khối đầu (Góc nhìn lãnh đạo) có biết on-track không (pass rate + 2 chữ ký + hở), không cần lội qua jargon test?
- Dev đọc bảng mapping + lớp test có đủ để hành động (biết TC nào fail, hở ở đâu) không?
- Artifact có ĐÚNG + ĐỦ các phần đã liệt kê (Góc nhìn lãnh đạo · Mapping 5 mắt · Report lớp test · 2 sign-off) không? Requirement/AC có TRÍCH từ GĐ trước (không bịa), lớp test bỏ có ghi lý do?
- Có lỡ lấn sang đào edge case mới (việc `review`) hay quyết Go/No-Go (việc `ship`) không?

## Cổng go/no-go + AI DUYỆT (theo phân vai GĐ12)

Cổng của GĐ12: **"Pass đủ điều kiện để go-live chưa?"**

Phân vai người duyệt (A5): **QA lead** chủ sở hữu, duyệt bởi **PO (UAT sign-off)** + **Security (security sign-off)**. `uat` KHÔNG tự đóng hai chữ ký hộ người thật — nó CHUẨN BỊ report đủ để hai vai đó ký, kiểm điều kiện đủ để trình ký, và ghi rõ chữ ký nào còn treo. Đưa cổng cho user quyết:
```text
═══ CỔNG GO/NO-GO (GĐ12 UAT) — <project> ═══
Pass: <n/m AC có test> · <k PASS>        Gap chưa test: <số / "không">
UAT sign-off: <PO — ngày / CHỜ>          Security sign-off: <Sec — ngày / CHỜ>
Đủ điều kiện go-live? (đủ / go-live có điều kiện / chưa — cần <gì>)
═══════════════
```
Chưa đủ → nêu đúng cái thiếu + một lối đi tiếp (bổ test, chuyển `/review` cho gap, hoặc go-live có điều kiện với phần đã pass). Không phủ định cứng, không tự phán "không release".

## Bàn giao sang `ship` (GĐ13)

```text
═══ BÀN GIAO — <project> (GĐ12 → GĐ13) ═══
Đã chứng minh: <n/m AC PASS> · UAT <✔ ngày / chờ> · Security <✔ ngày / chờ>
Điều kiện/hở còn treo: <1 dòng — hoặc "không hở trong phạm vi">
Artifact: state/project/<project-name>/pipeline/uat.md
→ Đủ điều kiện go-live, làm Go/No-Go + Runbook + rollback: chạy /ship (GĐ13)
→ Còn nghi gap/edge case/permission chưa test hết: chạy /review trước khi ship
→ Có AC fail cần sửa code rồi re-test: chạy /frame cho slice fix (hoặc /delivery)
═══════════════
```
Chỉ liệt kê, không tự chọn hộ user chạy skill nào tiếp.

## State — ghi ở đâu

Ghi report vào `state/project/<project-name>/pipeline/uat.md` (vùng skill, KHÔNG vào repo code trừ khi user đồng ý). Cập nhật `state/current.json`:
```json
{ "project": "<project-path>", "updated_at": "<ISO 8601>" }
```
Và một dòng trạng thái GĐ12 trong `state/project/<project-name>/pipeline/_index.json` để `ship` đọc tiếp:
```json
{ "stage": "gd12_uat", "trang_thai": "<dang_verify|cho_ky|done_handoff>",
  "pass_rate": "24/24", "uat_signoff": false, "security_signoff": false,
  "updated_at": "<ISO 8601>" }
```
`cho_ky: true` = bảng xong, đang chờ PO/Security ký — resume thì nhắc lại chỗ chờ, KHÔNG tự đi tiếp sang `ship`.

## Ví dụ Case Management (rút gọn — cùng case với doc)

```text
GÓC NHÌN LÃNH ĐẠO
  Mọi yêu cầu chặn-release đã có test và pass: 24/24 AC pass.
  PO đã ký UAT (15/09), CISO đã ký bảo mật (16/09). Không còn hở chặn-release
  trong phạm vi v1.4.0 → đủ điều kiện trình go-live.

MAPPING
  R: "User tìm hồ sơ theo trạng thái"
  → AC: chỉ thấy hồ sơ Pending user có quyền xem
  → TC-CASE-SEARCH-001 → Result: PASS
  → Release: đủ điều kiện đưa vào v1.4.0

REPORT
  unit 312/312 · integration 48/48 · contract (Case↔Notification) PASS
  perf: P95 210ms @10k (đạt NFR<500ms) · security: SAST 0 high, DAST 0 high · a11y: WCAG AA pass
  UAT sign-off: PO ✔ (15/09) · Security sign-off: CISO ✔ (16/09)

Cổng: pass đủ điều kiện go-live → GO. Bàn giao sang /ship (Go/No-Go + Runbook + rollback).
```

## Khi làm trong project workspace (`projects/<key>/`)

Nhận diện: user chỉ định `projects/<key>`, hoặc gói ngữ cảnh từ `resume`/`fanout` trỏ tới đó, hoặc `state/current.json` có trường `workspace`. Khi ấy:
- Bước 0 đọc thêm: `projects/<key>/constitution/` (nhất là `folders.md` + `definition-of-done.md`) và `progress/progress.json` — tìm task đang mở giao cho skill này (trường `owner`).
- Artifact người-đọc ghi vào ĐÍCH của task (trường `artifact` trong `progress.json`, đặt theo `folders.md`) — KHÔNG ghi bản chính vào `state/`. State máy riêng của skill (file json trạng thái) vẫn ở `state/project/<key>/` như cũ.
- Xong việc: báo user chạy `/checkpoint <task-id>` lấy phiếu rồi `/progress` đóng bước. Không tự lật done, không tự ghi `progress.json` — file đó một chủ (`progress`).
