CHẤM: 06-shape · /Users/uspro/Desktop/skillsh/rebuild-hex-agent/pipeline/06-shape.md

[0] 1. BÁM NGUỒN (xương sống) — chuỗi middleware "cố định" Timing→Policy→Budget→Retry→Condense→core (C4 dòng 141, ADR-002 dòng 265, bàn giao dòng 372) SAI so với code gốc: `core/bootstrap.py:29-33` chốt chuỗi cố định là timing→policy→retry→condense và "BudgetGuard is intentionally NOT wired here" (per-run, không thuộc chuỗi kernel) — một claim cơ-chế-code không tồn tại → theo anchor tiêu chí 1 là 0.
[2] 2. ĐỦ BỘ ARTIFACT & DÙNG ĐƯỢC NGAY (xương sống) — đủ 7 khối (Brief + C4 Context + C4 Container có giao thức giữa khối dòng 161-167 + Data Flow + Integration + Security + 6 ADR); mỗi ô Brief là quyết định đọc-được hoặc "không áp dụng + lý do" (Compliance dòng 76-77); dev cầm đi chọn stack được (ràng buộc dòng 366-372).
[2] 3. ĐÚNG VAI GĐ6 (xương sống) — công nghệ chỉ nêu mức LOẠI (dòng 119); SQLite/langgraph.sqlite gắn nhãn "hiện trạng" + "chốt DB cụ thể = việc GĐ7" (dòng 305); không hỏi lại WHY/WHAT, không vẽ lại domain, không cắt slice.
[2] 4. ĐỌC-ĐƯỢC-3-TẦNG — mở bằng "Góc nhìn lãnh đạo 60 giây" đúng 3 điều CTO nhìn on-track (dòng 15), ngôn ngữ nghiệp vụ; mỗi C4 có 1 khối "Diễn giải (phẳng)" (dòng 113, 170); chi tiết dev nằm sau.
[2] 5. ADR — 6 ADR phủ style/chokepoint/delegation/acceptance/resume/redaction; mỗi ADR có Phương án đã loại kèm lý do thật (ADR-005 dòng 301) và Hệ quả có cả được lẫn mất (dòng 258-259, 303-304).
[2] 6. DATA FLOW & DATA OWNERSHIP — 7 bước Data Flow gắn đúng 6 domain event GĐ5 §5.4 (dòng 178-186) + nêu chủ dữ liệu mỗi bước; luật "cấm cross-module đọc/ghi trực tiếp, đi qua port" ghi rõ (dòng 43, 188).
[2] 7. INTEGRATION & SECURITY — bảng Integration đủ 5 ô cho từng đường LLM/tool/RAG/UI (dòng 194-201); Security có phân loại 4 lớp + auth model + audit append-only + STRIDE cho delegate+redaction (dòng 213-240), khớp code (scope `policy.py:25-26`, redaction `SECRET_KEYS` `control/redaction.py:16`).
[2] 8. CỔNG & BÀN GIAO — cổng kiểm từng-điều 4 điều + câu hỏi cổng chuẩn (dòng 333-349); bàn giao nêu hình đã chốt + 6 ràng buộc kiểm-được + open-Q chuyển tiếp có địa chỉ (dòng 366-376); các lối đi chỉ liệt kê không chọn hộ (dòng 378-381).

TỔNG: 14/16
GATE: rớt: tiêu chí xương sống 1 (BÁM NGUỒN) = 0 vì claim code sai — chuỗi middleware "cố định" chèn Budget vào chuỗi kernel trong khi `bootstrap.py:29-33` cố ý loại Budget; dù tổng 14 vẫn rớt (luật gate: backbone=0 → rớt, dù tổng cao).
SỬA TRƯỚC TIÊN: Sửa mô tả chuỗi middleware cố định ở C4 (dòng 141)/ADR-002 (dòng 265)/bàn giao (dòng 372) thành timing→policy→retry→condense, và gắn nhãn Budget = per-run guard trong loop (ngoài chuỗi kernel, `bootstrap.py:29-33`).

---

## 2. Bảng tiêu chí × 3 lens + phân xử bất đồng

| # | Tiêu chí (xương sống?) | ky-thuat | business | thi-cong | HỢP NHẤT | Ghi chú phân xử |
|---|---|---|---|---|---|---|
| 1 | BÁM NGUỒN (XS) | 0 | 1 | 1 | **0** | Bất đồng chính — xem dưới |
| 2 | ĐỦ BỘ ARTIFACT (XS) | 2 | 2 | 2 | **2** | Đồng thuận |
| 3 | ĐÚNG VAI GĐ6 (XS) | 2 | 2 | 2 | **2** | Đồng thuận |
| 4 | ĐỌC-ĐƯỢC-3-TẦNG | 2 | 2 | 2 | **2** | Đồng thuận |
| 5 | ADR | 2 | 2 | 2 | **2** | Đồng thuận |
| 6 | DATA FLOW & OWNERSHIP | 2 | 2 | 2 | **2** | Đồng thuận |
| 7 | INTEGRATION & SECURITY | 2 | 2 | 2 | **2** | Đồng thuận |
| 8 | CỔNG & BÀN GIAO | 2 | 2 | 2 | **2** | Đồng thuận |
| | **TỔNG** | **14** | **15** | **15** | **14** | |
| | **GATE** | rớt | đạt | đạt | **rớt** | Theo luật gate + tiêu chí 1 |

**Bất đồng đáng chú ý duy nhất — tiêu chí 1 (0 vs 1 vs 1):**

- **Bằng chứng đã tự kiểm:** mở `/Users/uspro/Desktop/namnson/hex_agent/core/bootstrap.py`. Hàm `_install_middleware` (dòng 28-53) wire theo đúng thứ tự `timing → policy → retry → condense`, và docstring dòng 29-33 ghi nguyên văn: *"Order = outer -> inner: timing, policy, retry, condense. ... BudgetGuard is intentionally NOT wired here: its same-tool counter is per-run, so a kernel-lifetime instance would leak across runs — wire it per run instead."* Grep xác nhận `middleware/__init__.py` export BudgetGuard nhưng KHÔNG có `kernel.use(BudgetGuard)` nào ở prod. Bốn nguồn phụ trong repo cùng khẳng định: `MAP.md:87`, `CHANGELOG.md:65` ("cố ý KHÔNG wire ở bootstrap"), `plans/reports/architecture-map-...:43` ("BudgetGuard deliberately excluded — per-run state"), `phase-3-toolbox-safety.md:130` ("thứ tự timing→policy→retry→condense ... BudgetGuard cố tình KHÔNG wire").

- **Artifact nói gì:** dòng 170 gọi đây là "một chuỗi middleware **cố định** (Timing→Policy→Budget→Retry→Condense→core)"; ADR-002 dòng 265 lặp lại trong ô Quyết định; bàn giao dòng 372 chốt thành ràng buộc cho stack: "Middleware chain có thứ tự cố định (Timing→Policy→Budget→Retry→Condense→core)". Cả ba đều khẳng định Budget nằm TRONG chuỗi kernel cố định — trái với code.

- **Vì sao lấy 0, không phải 1:** rubric tiêu chí 1, anchor điểm 0 liệt kê thẳng "claim về code gốc SAI khi đối chiếu `hex_agent` (cơ chế/tên/hành vi không tồn tại)" và chốt "Bất kỳ claim bịa nào → tiêu chí này 0". Đây đúng là một claim cơ-chế-code sai (Budget không ở chuỗi kernel), không phải "boundary trace lỏng" hay "một suy đoán không gắn nhãn" (những cái đó mới là anchor điểm 1). business/thi-cong hạ xuống 1 với lý do "chỉ một mắt xích sai / suy đoán viết như sự thật" — nhưng rubric KHÔNG cho phép du di đó với claim-code: anchor là phân loại (categorical), không phải cân theo mức độ. Theo luật hợp nhất "lấy điểm THẤP NHẤT trừ khi chứng minh lens thấp chấm sai": ở đây lens thấp (ky-thuat=0) chấm ĐÚNG theo anchor, nên KHÔNG nâng. Thêm nữa, claim này load-bearing: nó đi vào ràng buộc bàn giao (dòng 372) → GĐ7 sẽ mang một thứ-tự-chain không tồn tại làm điều kiện hiện thực.

- Không có tiêu chí nào bị lens thấp chấm oan để cần nâng: 7 tiêu chí còn lại đồng thuận 2, tôi đã đối chiếu mẫu (scope `policy.py:25-26`, event-name mismatch `config/runtime_event_types.yaml:43-49`, redaction `redaction.py:16`, 6 domain event `05 §5.4`) — tất cả khớp.

---

## 3. Nghi bịa / không nguồn — đã xác nhận

**[ĐỨNG VỮNG] Chuỗi middleware "cố định" Timing→Policy→Budget→Retry→Condense→core (C4 dòng 141 · ADR-002 dòng 265 · bàn giao dòng 372).**
Bằng chứng: `core/bootstrap.py:29-33` — chuỗi cố định thật là timing→policy→retry→condense; "BudgetGuard is intentionally NOT wired here" (counter per-run rò giữa run). Corroborate: `MAP.md:87`, `CHANGELOG.md:65`, `architecture-map-...report.md:43` ("BudgetGuard tests-only"), `phase-3-toolbox-safety.md:130`. Budget là mechanism CÓ THẬT nhưng là guard per-run trong loop, KHÔNG thuộc chuỗi kernel cố định → claim "cố định + có Budget" sai. Đây là claim làm rớt gate.

**[GHI NHẬN, KHÔNG TRỪ ĐIỂM RIÊNG] Cổng tự cấp "✔" 4 điều + "GATE: GO" (dòng 334-354).**
Do AI tự duyệt trong chế độ tự-quyết. Theo luật khắt khe không tính là bằng chứng. Rubric không có tiêu chí "gate-self-grant" nên không trừ riêng; nhưng self-certification này KHÔNG miễn trừ lỗi tiêu chí 1 — cổng tự tuyên GO trên một artifact có claim-code sai. (Cả 3 lens cùng ghi nhận.)

**[GHI NHẬN, KHÔNG TRỪ TIÊU CHÍ KIẾN TRÚC] "Hai bệnh chết người mà thị trường đều dính" (dòng 13).**
Claim thị trường không có nguồn ngoài; là suy đoán nghiệp vụ, không phải dữ kiện đo được (business lens nêu). Không thuộc phạm vi tiêu chí kiến trúc nào có điểm; là claim-value tự-tham-chiếu, đã có OQ-1 (baseline chi phí/false-finish → Operate) làm chỗ trú. Không trừ.

**[KHÔNG ĐỨNG — đã kiểm, KHỚP code] Các số nền & tên cơ chế khác.**
max_depth=8/max_steps=100, SessionIdentity 7-field, scope con⊆cha (`policy.py:25-26`: `if not scope <= parent.allowed_capabilities: raise PermissionError`), OQ-3 event-name mismatch (`config/runtime_event_types.yaml:43-49` khai `tool.call_requested/before_call/after_call` vs `kernel.py:124,216` phát `tool.requested/completed/failed` — mismatch THẬT, artifact chốt reconcile về registry allowlist là hợp lý), redaction SECRET_KEYS (`control/redaction.py:16,34,56`), 6 domain event (`05 §5.4`) — tất cả truy về code/GĐ5 và khớp. Đây là những claim ĐÚNG, không phải bịa. Self-praise "0 rò state / 0 secret" là mục-tiêu-kiến-trúc có cơ chế đỡ truy được (freeze kernel, redact-tại-biên) chứ chưa có test-run trong artifact — chấp nhận mức claim-có-cơ-chế, không trừ.

**Kết:** sau khi tự kiểm, còn ĐÚNG MỘT claim đứng vững làm rớt gate — chuỗi middleware "cố định" chèn Budget. Các nghi ngờ khác hoặc là ghi-nhận-không-trừ (self-gate, claim thị trường) hoặc đã kiểm và khớp code (không còn là nghi bịa).
