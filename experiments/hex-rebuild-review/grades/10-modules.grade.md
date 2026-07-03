CHẤM: 10-modules · /Users/uspro/Desktop/skillsh/rebuild-hex-agent/pipeline/10-modules.md

[1] BÁM NGUỒN — định danh/con số code khớp gốc 100% và ranh giới bám GĐ5/GĐ6, NHƯNG tiền-đề trục "09 không tồn tại" đã lỗi thời (đúng lúc viết, sai lúc chấm) + tick ✔ "E01–E21 map hết" tự-khen khi E19 vắng.
[2] SỞ HỮU SẠCH — mỗi module đúng 1 owner đặt tên, mọi contract có "Does NOT own" chỉ đích danh, đối chiếu chéo không mảnh data/event nào hai chủ (khớp GĐ5 §5.5).
[2] DÙNG ĐƯỢC THẬT — mọi module đủ ô bắt buộc; module lõi có Public API kèm request/response + error code + permission + test contract nêu cặp team đối đầu; module rìa rút gọn ĐỘ SÂU kèm lý do, không bỏ ô.
[2] ĐỌC 3 TẦNG — Map mở bằng bảng module×owner×sở-hữu/không-sở-hữu ngôn ngữ nghiệp vụ + "hai cửa công khai"; mỗi contract mở bằng dòng [Lãnh đạo] "giữ gì / hỏng hỏi ai" TRƯỚC API; jargon neo nghĩa đời thường.
[2] CHIA THEO DOMAIN — 6 module = 6 bounded context GĐ5 ánh xạ 1–1; 4 quyết định gộp/tách đều ghi tiêu chí domain (data-ownership/change-frequency) KÈM phương án đã loại + vì sao.
[1] PHỦ FEATURE — có bảng kiểm chéo + block ⚠️ đủ mẫu, nhưng E19 Test Harness (✓ 327 tests, evidence-C) không map/không park/không giải thích, và E15–E18 "gathered→E21" không nói ra → sót mục không giải thích.
[1] ĐÚNG VAI + CỔNG — đúng vai + tự-quyết GO có ủy quyền ghi rõ + phương án đã loại, NHƯNG bằng chứng cổng #3 dựa trên tiền-đề "backlog GĐ9 chưa qua cổng" đã lỗi thời + over-claim "map hết" → 1 trong 4 bằng chứng hụt.

TỔNG: 11/14

GATE: đạt (sát): 3 tiêu chí xương sống — BÁM NGUỒN=1 (không phải bịa, chỉ lỗi-thời + 1 tick tự-khen), SỞ HỮU SẠCH=2, DÙNG ĐƯỢC THẬT=2 — không cái nào =0. Rớt-điểm nằm ở criterion 6 + 7 (không phải gate).

SỬA TRƯỚC TIÊN: Đồng bộ lại với repo hiện tại — 09-backlog.md ĐÃ tồn tại & GATE:GO (dòng 331), nên bỏ ⚠️ block "09 không tồn tại", đổi bảng kiểm chéo sang map STORY→module, map/park E19 kèm lý do, rồi hạ tick ✔ "E01–E21 map hết" xuống đúng phạm vi.

---

## Phần 2 — Bảng tiêu chí × 3 lens + phân xử bất đồng

| # | Tiêu chí | ky-thuat | business | thi-cong | HỢP NHẤT | Ghi chú phân xử |
|---|---|---|---|---|---|---|
| 1 | BÁM NGUỒN (xương sống) | 0 | 1 | 2 | **1** | Bất đồng lớn nhất — quyết định gate. Phân xử bên dưới. |
| 2 | SỞ HỮU SẠCH (xương sống) | 2 | 2 | 2 | **2** | Đồng thuận. Kiểm chéo: plan tree→Orch, session→Exec-Core, event+redaction→Control-Plane, sandbox→Tools-Safety; Platform ôm 3 module vẫn mỗi module 1 owner (module≠team). |
| 3 | DÙNG ĐƯỢC THẬT (xương sống) | 2 | 2 | 2 | **2** | Đồng thuận. execute_tool→CapabilityResult (dòng 189-192), run_task_loop→Outcome (155-158), error code + test contract đối đầu đủ. |
| 4 | ĐỌC 3 TẦNG | 2 | 2 | 2 | **2** | Đồng thuận. |
| 5 | CHIA THEO DOMAIN | 2 | 2 | 2 | **2** | Đồng thuận. |
| 6 | PHỦ FEATURE | 1 | 1 | 1 | **1** | Đồng thuận cả 3 — E19 mồ côi trong artifact, E15–E18 gộp ngầm. |
| 7 | ĐÚNG VAI + CỔNG | 1 | 2 | 1 | **1** | Min=1; không nâng — bằng chứng cổng #3 thật sự hụt. Phân xử bên dưới. |
| | **TỔNG** | 10 | 12 | 12 | **11/14** | |
| | **Gate** | rớt | đạt | đạt | **đạt** | Gate lật theo criterion 1: 0→1. |

### Bất đồng #1 (quyết định gate) — Criterion 1: ky-thuat=0 vs business=1 vs thi-cong=2

Luật hợp nhất: lấy THẤP NHẤT (=0) TRỪ KHI chứng minh được lens thấp chấm sai. Tôi mở repo và chứng minh được — nên nâng 0→1, không giữ 0, cũng không lên 2:

- **Vì sao KHÔNG giữ 0 (ky-thuat sai chỗ gọi "BỊA"):** Rubric criterion-1=0 đòi "có ít nhất một claim BỊA" (định danh/hành vi không tồn tại, hoặc trích GĐ trước mở ra không có). Claim "pipeline/09-*.md không tồn tại" (dòng 9) KHÔNG phải bịa: `stat` cho thấy `10-modules.md` mtime = **02:30:51**, `09-backlog.md` mtime = **02:32:03**. Tức đúng thời điểm 10-modules được viết, 09-backlog CHƯA tồn tại — claim ĐÚNG lúc viết, chỉ LỖI-THỜI sau đó ~2 phút. Lỗi-thời ≠ bịa. (Chính lens thi-cong bắt được mtime này; ky-thuat gọi "BỊA" là định danh sai kiểu lỗi.) Mọi định danh code còn lại đều khớp gốc đã kiểm tay: `JACCARD_MAX=0.80` (accept.py:22), `K=3/K_LEAF=5/MAX_DEPTH=6` (solve.py:32-34), `max_steps=100/max_depth=8` (policy.py), `execute_tool` (core/kernel.py:106), `SessionIdentity` 7-field (session.py:16-23). Không có định danh nào bịa → không đủ điều kiện =0.
- **Vì sao KHÔNG lên 2 (business/thi-cong quá rộng lượng):** Rubric-1 ghi rõ "Tự khen (✔) ở Tự-soi/Cổng mà không trỏ được bằng chứng cụ thể → cũng tính trừ". Tick ✔ #3 (dòng 308 Tự-soi + dòng 325 Cổng) "Epic E01–E21 map hết vào đúng một module" là claim quá lời: E19 Test Harness (evidence-C dòng 25: ✓ 327 tests) KHÔNG xuất hiện ở đâu trong artifact (grep 0 hit). Đây là ✔ tự-khen không trỏ được bằng chứng. Cộng với tiền-đề trục lỗi-thời chống đỡ cả ⚠️ block → nhiều hơn "1–2 claim mơ hồ" nhưng chưa tới mức bịa. Đúng khung "1 — bám nguồn phần lớn, còn claim không gắn nguồn/không chuẩn".
- **Kết:** **1.** Gate LẬT từ rớt→đạt vì backbone không còn =0.

### Bất đồng #2 — Criterion 7: business=2 vs (ky-thuat, thi-cong)=1

Min=1. Xét có nên nâng lên 2 (theo business) không — KHÔNG:
- Lý do hạ điểm của **thi-cong** ("GO tự-cấp + tick ✔ tự-phong không tính bằng chứng độc lập") — TRÁI rubric: criterion-7=2 CHO PHÉP tự-quyết GO "nếu có ủy quyền ghi rõ + lý do + phương án đã loại". Artifact có đủ (header dòng 5, cổng dòng 342 "product owner: không hỏi approval", phương án đã loại dòng 344). Nên riêng lý do này KHÔNG hạ được điểm.
- NHƯNG lý do của **ky-thuat** đứng vững: bằng chứng cổng #3 (dòng 325) vừa dựa trên tiền-đề lỗi-thời "backlog GĐ9 chưa qua cổng" (nay sai) VỪA over-claim "map hết" khi E19 vắng → đúng 1 trong 4 bằng chứng cổng bị hụt. Rubric-7=1 = "có cổng nhưng bằng chứng thiếu/hụt 1 trong 4 mục". Vậy giữ **1**, không nâng lên 2.

---

## Phần 3 — Nghi bịa / không nguồn — đã xác nhận

Gom nghi_bia của cả 3 lens, tự mở file/code kiểm lại từng cái:

1. **"pipeline/09-*.md không tồn tại" (dòng 9)** — KHÔNG phải bịa, là **claim lỗi-thời**. Bằng chứng: `stat` → 10-modules.md mtime 02:30:51, 09-backlog.md mtime 02:32:03; 09 sinh SAU 10 đúng ~72 giây. Đúng lúc viết 10-modules, 09-backlog chưa tồn tại → claim đúng-tại-thời-điểm-viết. Hiện 09-backlog.md tồn tại (46KB) và mang **GATE: GO** (dòng 331: "Backlog đủ để phân module (GĐ10)..."). Kết luận: lỗi-thời phải sửa (đồng bộ repo), KHÔNG tính là bịa để đánh gate =0. → Đây là mắt xích khiến ky-thuat chấm 0 nhầm.

2. **Tick ✔ #3 "Epic E01–E21 map hết vào đúng một module" (dòng 308 + 325)** — **đứng vững là over-claim**. grep E19/E15/E16/E17/E18/"Test Harness" trong 10-modules.md = **0 hit**. Evidence-C dòng 25: E19 Test Harness ✓ (327 tests, `tests/`,`tests_audit/`). E19 KHÔNG map vào module nào, KHÔNG nằm trong danh sách park (chỉ park E11–E14/E20 dòng 123). Vậy "map hết" sai phạm vi thật → ✔ tự-khen không trỏ được bằng chứng (rubric-1 trừ điểm). Đây là lý do chốt criterion-1 ở 1 chứ không lên 2, và làm hụt bằng chứng cổng #3 (criterion-7).

3. **E15–E18 "gathered→E21" không nói ra trong artifact** — **đứng vững là sợi-trace-đứt-ngầm, KHÔNG phải bịa**. Evidence-C dòng 6: "P4 Realtime Control (E21, gathers E15/E16/E17/E18)"; dòng 24: E15 "⚠ merged→E21". Artifact CÓ map E21 (dòng 121) nên E21 không mồ côi; nhưng việc E15–E18 gộp vào E21 bị bỏ ngầm, không ghi. Là điểm trừ criterion-6 (sót mục không giải thích), không phải claim bịa.

4. **GATE: GO tự cấp + 4 tick ✔ ở cổng (dòng 323–326, 343)** — **KHÔNG phải bịa**. Kiểm 4 evidence item: #1 (mỗi module 1 owner), #2 (không data/event hai chủ), #4 (mọi phụ thuộc qua seam) TỰ chúng trỏ được vào nội dung artifact và khớp GĐ5 §5.5. Chế độ tự-quyết có ủy quyền ghi rõ (dòng 5, 342) → rubric-7 cho phép GO tự cấp. Chỉ riêng evidence #3 hụt (mục 2 trên). Vậy "GO tự cấp" tự nó hợp lệ, không tính bịa (bác lý do hạ điểm của thi-cong).

5. **Error code công khai (CAPABILITY_NOT_IN_SCOPE, SANDBOX_PATH_ESCAPE, EVENT_SEQ_GAP…)** — **KHÔNG bịa**. Không tồn tại verbatim trong code gốc (0 hit) nhưng là code MỚI do contract GĐ10 ĐẶT (đúng vai — đặt error code là việc của contract), và HÀNH VI chúng đặt tên đều bám code thật (scope-check fail-closed tại execute_tool, jail escape ở safety/sandbox, seq gap ở EventEmitter). Hợp lệ.

6. **P95 latency / ngưỡng alert** — **KHÔNG bịa, khai đúng chuẩn**. Dòng 167 + 254: "chưa có số → OQ-1 → Operate, KHÔNG bịa". Đúng rubric-1 (chỗ chưa có số ghi thành open-Q chuyển đúng giai đoạn).

**Còn lại sau kiểm:** 1 claim LỖI-THỜI cần sửa (#1) + 1 tick OVER-CLAIM đứng vững (#2) + 1 sợi-trace đứt ngầm (#3). Không claim nào là BỊA-định-danh/bịa-số → criterion-1 không đủ điều kiện =0; gate ĐẠT nhưng sát mép, sửa-trước-tiên chính là đồng bộ lại với 09-backlog.md đã GATE:GO.
