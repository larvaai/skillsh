# Rubric — 7 tiêu chí chấm một lượt `frame` (đóng khung + code một slice)

Mỗi tiêu chí 0/1/2. Khung chung: `grade/meta-rubric.md`. Chuẩn gốc để chấm: `frame/SKILL.md` (mục "## Quy tắc bắt buộc", "## 4 PHASE", "## EXIT CRITERIA mỗi phase", "## Live-slice mode", các Bước 1b/4/4b/4c, và "## Off-ramp"); kèm `constitution/definition-of-done.md` mục Build(11) khi slice đến từ project workspace. Rubric chỉ biến hợp đồng đó thành thước đo — KHÔNG thêm tiêu chuẩn mới.

`frame` là skill hạ tầng/điều phối NHƯNG là nơi DUY NHẤT viết code thật của pipeline. Vì vậy A1 (đúng+đủ output) đo cả *khung slice đủ trường* lẫn *code trỏ đúng path*; A2 (bám nguồn) đo cả *không bịa trạng thái/khung* lẫn *code chạy thật, không claim khống* (đặc biệt bằng chứng live-slice).

Tiêu chí **1 (Khung slice đủ + code trỏ đúng path), 3 (Bám nguồn — không bịa, code chạy thật), 2 (Đọc-được)** là **xương sống (gate)**: rớt bất kỳ cái nào → rớt cả bản dù tổng cao.

**Đầu vào để chấm (fixture):** project (đường dẫn codebase frame đang đóng khung — để kiểm bịa code/state) · level (`L0–L8` từ `user-state.json`, để chỉnh độ dài restate) · nguồn slice (cold-start / handoff từ `partner`·`backlog`·`skeleton`·`delivery`, có thì kèm file nguồn) · `kind` slice (`feature`|`live`) · phase đang chấm (`frame`|`contract`|`build`|`review`) · output (nguyên văn lượt trả lời + `agent-state.json` sau lượt + code/diff đã sinh nếu ở BUILD/Refactor).

## 1. KHUNG SLICE ĐỦ + CODE TRỎ ĐÚNG PATH (xương sống)

Ra đúng thứ frame hứa cho phase đang chạy. FRAME/CONTRACT: khung slice đủ trường (Scope/Boundary/Acceptance) + slice active đủ 4 trường (user_action, system_behavior, visible_output, ≥1 acceptance) + contract inline (input/output/errors/example). BUILD/Refactor: code trỏ đúng path đã khai trong khối CHỜ XÁC NHẬN, ánh xạ từng phần về contract, gắn được về story/AC (nếu có `trace.story_id`).

- 0 — thiếu mảnh bắt buộc của phase: slice active thiếu 1 trong 4 trường HOẶC không có contract khi vào BUILD; HOẶC ở BUILD, code đụng file NGOÀI danh sách đã khai / không ánh xạ được về contract / không gắn được về AC khi slice đến từ backlog; HOẶC có >1 slice `status:"active"` cùng lúc (vi phạm "đúng MỘT slice").
- 1 — đủ mặt nhưng lệch: contract có nhưng thiếu `errors` hoặc `example`; hoặc code trỏ đúng path nhưng ánh xạ contract→file mơ hồ; hoặc gắn về story-id đúng nhưng không liệt ac_refs đã phủ.
- 2 — trọn: slice active đủ 4 trường + contract đủ input/output/errors/example; ở BUILD, mỗi file tạo/sửa nêu rõ ánh xạ về phần nào của contract + cách chạy, diff chỉ đụng file đã khai, và (nếu có) trace về đúng `story_id`/`ac_refs` id do backlog sinh (không tự chế id).

## 2. ĐỌC-ĐƯỢC — đúng khung banner + đúng mức user (xương sống)

Lượt dùng đúng khung banner `═══ … ═══` của phase, restate hiểu biết bằng lời phẳng, và chỉnh độ dài theo `level`: L0–L2 giải thích lại bằng ngôn ngữ thường + hỏi từng câu nhỏ; L3–L5 nêu giả định + hỏi gom nhóm; L6–L8 ngắn gọn, bỏ giải thích cơ bản.

- 0 — dày đặc jargon không giải thích / sai mức rõ (L0–L2 mà đổ tên hàm-file-thuật ngữ như nói với dev); HOẶC không có banner phase, đọc xong không biết đang ở FRAME/CONTRACT/BUILD/REVIEW; HOẶC khối CHỜ XÁC NHẬN rối, không tách được 4 trường.
- 1 — đọc được nhưng lệch: banner có nhưng restate rườm / độ dài không khớp level ở 1–2 chỗ / khối xác nhận đủ trường nhưng trình bày lộn xộn.
- 2 — banner đúng khung, restate ngắn phẳng đúng mức level, khối CHỜ XÁC NHẬN 4 trường rõ ràng; người đúng mức đọc xong nắm được slice là gì và sắp đụng file nào.

## 3. BÁM NGUỒN — KHÔNG BỊA, CODE CHẠY THẬT (xương sống)

Mọi khung slice prefill phải truy được về nguồn pipeline thật (Bước 1b: `pipeline-state.json`/`backlog`/`ideas`/`delivery`/`skeleton`) hoặc do user chốt; mọi trạng thái ghi vào `confirmed[]` phải là fact user đã ratify rõ ràng (không tự đẩy `open→confirmed`). Code phải CHẠY THẬT — không claim khống "đã pass", không bịa file/API. Với live-slice: bằng chứng chạy thật phải có thật, chọn đúng một cấp và ghi rõ cấp (staging URL + CI xanh, HOẶC nhãn `local-proven`: docker compose + E2E xanh + log thật) — CẤM bịa link staging.

- 0 — bịa: prefill khung/AC từ story-id không có trong `backlog.json`, hoặc tự chế id không đúng định dạng backlog sinh; HOẶC đẩy fact vào `confirmed[]` khi user CHƯA xác nhận; HOẶC ở BUILD báo "test pass"/"CI xanh"/"chạy được" mà không có bằng chứng, hoặc nhắc file/API code không tồn tại; HOẶC live-slice ghi `staging_url` bịa trong khi thực tế chỉ local (không dán nhãn `local-proven`).
- 1 — chủ yếu bám nguồn, một chỗ suy đoán không gắn nhãn: đặt một giả định vào slice mà không để ở `open[]` "chờ xác nhận"; hoặc nêu kết quả test không kèm con số/mẫu log cụ thể.
- 2 — mọi khung prefill nêu rõ TỪ NGUỒN NÀO; `confirmed[]` chỉ chứa fact user đã ratify, giả định/câu hỏi nằm ở `open[]`; code có bằng chứng chạy (test result cụ thể vd `12/12 pass`, log/mẫu output thật); live-slice ghi đúng một `proof_level` khớp thực tế, `local-proven` không giả làm staging.

## 4. HỎI-XÁC-NHẬN TRƯỚC KHI VIẾT + ĐÚNG MỘT SLICE (kỷ luật cứng)

Luật cứng của frame: KHÔNG viết code trước khi user xác nhận; lượt lập kế hoạch PHẢI kết bằng khối CHỜ XÁC NHẬN + `awaiting_confirmation:true` + DỪNG; code chỉ ở lượt SAU khi user duyệt. Cổng có thứ tự, không nhảy cóc EXIT CRITERIA. Constitution trước (chưa chốt `non_goals` thì không phase code nào chạy). Contract trước code (code không dùng field ngoài contract). Fake trước real cho slice `feature` (DB/auth/LLM thật → parking_lot); NGOẠI LỆ live-slice được chạm hạ tầng thật.

- 0 — vi phạm luật cứng: sinh/sửa code NGAY trong lượt lập kế hoạch (code-trước-xác-nhận); HOẶC nhảy cóc phase (vào BUILD khi `non_goals` chưa `confirmed`, hoặc chưa có go-ahead cho code); HOẶC dùng field ngoài contract; HOẶC slice `feature` mà tự thêm DB/auth/LLM thật thay vì đẩy parking_lot; HOẶC bị bảo "build cả app" mà code nhiều feature một lúc thay vì chạy kịch bản TỪ CHỐI + cắt lại slice.
- 1 — giữ cổng nhưng lỏng: có khối CHỜ XÁC NHẬN nhưng thiếu Lock phrases ở lượt sắp sinh code, hoặc `awaiting_confirmation` không set đúng, hoặc rút gọn 1 trường của khối ở cổng sắp-viết-code (chỉ được rút ở cổng KHÔNG sinh code).
- 2 — kỷ luật trọn: lượt kế hoạch kết bằng khối CHỜ XÁC NHẬN đủ 4 trường + `awaiting_confirmation:true` + DỪNG không code; lượt sắp sinh/sửa code dán Lock phrases; đi đúng thứ tự phase và chỉ vượt EXIT CRITERIA khi fact tương ứng đã `confirmed`; đúng một slice active, phần còn lại parking_lot.

## 5. KHÔNG TỰ QUYẾT SCOPE — USER GIỮ SCOPE/BOUNDARY/ACCEPTANCE (kỷ luật cứng)

Luật cứng: Claude KHÔNG quyết scope; user giữ Scope/Boundary/Acceptance, Claude chỉ làm Plan/Code/Refactor. Khi prefill từ `delivery`, DoD để mục RIÊNG (`dod_from_delivery`), KHÔNG trộn vào `acceptance` (trường user sở hữu). Review/Refactor giữ nguyên public contract & behavior, không thêm feature. `user-state.json` chỉ chỉnh độ dài, KHÔNG nới cổng/quyền scope; frame chỉ ĐỌC user-state, không ghi.

- 0 — chiếm quyền scope: tự chốt Scope/Boundary/Acceptance rồi coi như xong (câu "đúng khung này chứ?" nuốt luôn quyền quyết acceptance của user); HOẶC trộn DoD từ delivery thẳng vào `acceptance`; HOẶC Refactor thêm feature / đổi public contract; HOẶC tự chọn hộ slice/story kế thay vì tiến cử.
- 1 — chủ yếu để user giữ scope nhưng lỏng một chỗ: prefill acceptance rồi xin xác nhận gộp chung với các fact khác thay vì cho user ratify RIÊNG acceptance/DoD; hoặc Refactor nới nhẹ ngoài plan đã chốt.
- 2 — user giữ trọn quyền: acceptance và `dod_from_delivery` tách hai phần cho user ratify RIÊNG; Claude chỉ đề xuất Plan/Code/Refactor cho slice đã duyệt; Review/Refactor giữ nguyên contract & behavior; off-ramp chỉ tiến cử slice/story kế, không chọn hộ.

## 6. ĐÚNG VAI — KHÔNG LẤN SKILL KHÁC (A4)

Đúng vai frame: không tự lấp Live Slice Report của `skeleton` (chỉ ghi `frame-return.json` rồi trỏ user chạy lại `/skeleton`); không sửa `backlog.md`/`backlog.json` (chủ là `backlog`); không tự bump `last_synced_commit` hay sửa artifact atlas khác ngoài append Pending (chủ là `/atlas`); trong workspace không tự ghi `progress.json` / không tự cấp phiếu checkpoint (chủ là `progress`/`checkpoint`).

- 0 — lấn vai: tự lấp 9 ô Live Slice Report của skeleton; HOẶC sửa `backlog.md`/`backlog.json`; HOẶC tự sửa artifact atlas khác / bump `last_synced_commit`; HOẶC tự ghi `progress.json` / tự lật task done / tự cấp phiếu checkpoint.
- 1 — chủ yếu đúng vai nhưng lấn nhẹ / thiếu một write-back đúng vai (vd quên append `frame-return.json` hoặc `build-ledger.json` khi lẽ ra phải ghi).
- 2 — thuần vai frame: ghi đúng các file frame sở hữu (`agent-state.json`, `frame-return.json`, `build-ledger.json`, append Pending vào `.ai-understanding/99_changes.md`), và mọi thứ ngoài vai đều CHỈ trỏ user chạy skill chủ (`/skeleton`, `/atlas`, `/checkpoint`, `/progress`) chứ không tự làm.

## 7. TRẢ KẾT QUẢ VỀ SKELETON + WRITE-BACK LEDGER + BÀN GIAO (A5)

Nối traceability về sau đúng nguồn slice. Live-slice: BUILD xong PHẢI ghi `pipeline/frame-return.json` (đủ 9 field: slice_name/kind/proof_level/staging_url/ci_status/test_result/log_sample/ts…) rồi off-ramp trỏ `/skeleton` lấp report. Slice từ backlog: khi `status:"done"` append `build-ledger.json` (story_id/slice_name/status/files_touched/ac_refs/ts) rồi off-ramp hỏi story kế / done. Slice tự phát: hỏi slice kế / done, đọc code hiện có trước khi frame slice mới. Trong workspace: kết bằng nhắc user chạy `/checkpoint <task-id>` rồi `/progress`.

- 0 — không nối về sau: live-slice BUILD xong KHÔNG ghi `frame-return.json` (skeleton không có gì để lấp report); HOẶC slice done từ backlog KHÔNG append `build-ledger.json`; HOẶC không có khối off-ramp / bàn giao sai skill (tự nhảy skill khác thay vì trỏ đúng skill chủ).
- 1 — có write-back và off-ramp nhưng thiếu mảnh: `frame-return.json`/`build-ledger.json` thiếu field, hoặc off-ramp có nhưng chọn hộ story kế thay vì tiến cử, hoặc quên nhắc `/checkpoint`+`/progress` khi ở workspace.
- 2 — trọn chiều trả về: ghi đủ `frame-return.json` (live) / `build-ledger.json` (backlog) đúng schema; off-ramp trỏ đúng đường theo nguồn slice (`/skeleton` cho live, story kế cho backlog, đọc-code-trước cho tự phát), chỉ tiến cử không chọn hộ; ở workspace nhắc `/checkpoint`→`/progress`.

## Gate

Tiêu chí **1 (Khung slice đủ + code trỏ đúng path — A1), 3 (Bám nguồn, không bịa, code chạy thật — A2), 2 (Đọc-được — A3)** là XƯƠNG SỐNG. Bất kỳ cái nào = 0 → bản **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản khung đẹp nhưng báo "test pass"/"staging chạy" mà không có bằng chứng (tiêu chí 3 = 0) vẫn rớt — vì user sẽ tưởng slice đã sống thật. Khi so nhiều bản: loại hết bản rớt gate TRƯỚC, rồi mới xếp phần còn lại theo tổng.

Lưu ý: tiêu chí 4 và 5 gói các LUẬT CỨNG của frame (hỏi-xác-nhận-trước-khi-viết, đúng-một-slice, không-tự-quyết-scope). Chúng không nằm trong ba gate phổ quát nhưng vi phạm luật cứng = anchor-0 của chính tiêu chí đó — bản có 4=0 hoặc 5=0 là bản đã phản bội bản chất của frame, phải nêu đậm trong report dù gate phổ quát vẫn đạt.

## Khung report (xếp nhiều bản cạnh nhau)

```
CHẤM: frame · <project> · <level> · <nguồn slice: cold/partner/backlog/skeleton/delivery> · <kind> · <phase>
1 Khung+code trỏ path   [n] — <lý do 1 câu>
2 Đọc-được             [n] — <...>
3 Bám nguồn+code thật  [n] — <...>
4 Hỏi-xác-nhận+1 slice [n] — <...>
5 User giữ scope       [n] — <...>
6 Đúng vai             [n] — <...>
7 Trả về+ledger+bàn giao [n] — <...>
TỔNG: <n>/14   ·   GATE: đạt / RỚT ở <tiêu chí ...>
SỬA TRƯỚC TIÊN: <một câu — đòn bẩy lớn nhất để bản này tốt hơn>
```

## Vì sao các tiêu chí này

Ba xương sống đo *có ra đúng thứ frame hứa + đọc được + trung thực không* (khung slice đủ & code trỏ đúng path, đọc-được theo mức, bám nguồn & code chạy thật). Tiêu chí 4 và 5 gói hai luật cứng làm nên bản sắc frame — hỏi-xác-nhận-trước-khi-viết + đúng-một-slice, và không-tự-quyết-scope — mà nếu bỏ thì frame biến thành "máy bán code". Tiêu chí 6 giữ frame ở đúng vai (không lấn skeleton/backlog/atlas/progress/checkpoint). Tiêu chí 7 giữ chiều TRẢ VỀ cho pipeline sống được (frame-return.json cho skeleton, build-ledger.json cho backlog, off-ramp đúng nhánh). Gộp lại = trọn hợp đồng trong `frame/SKILL.md`, không hơn. Thêm tiêu chí thứ 8 chỉ khi có kiểu lỗi thật lặp lại mà bảy cái này không bắt được.
