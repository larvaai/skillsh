CHẤM: 13-ship · /Users/uspro/Desktop/skillsh/rebuild-hex-agent/pipeline/13-ship.md

1. BẰNG CHỨNG (xương sống): [0] — nhiều claim bịa cùng lúc: 5/6 tên metric loop + 3 tên flag KHÔNG tồn tại trong code gốc (grep = 0 hit), "rollback ĐÃ TEST trên staging" mâu thuẫn thẳng GĐ8 (rebuild 0/9 tick · code chưa gõ · chưa có staging), "6 N/A hợp lệ" lệch bảng (§1 chỉ có 2 ô N/A), "DoD S0 GĐ8" là attribution sai (0 hit trong 08).
2. ĐỦ BỘ: [2] — đủ 4 artifact ghép một trang + 12/12 ô có owner team thật + trạng thái, 2 ô N/A đều kèm lý do riêng, độ sâu bám rủi ro token/quyền/secret.
3. BỐN THỨ CHẶN (xương sống): [0] — 2/4 thứ chặn ruột rỗng khi soi: monitoring "BẬT" dựa metric không tồn tại; rollback "đã test" dựa `run_smoke.py` (không toggle flag / không đọc features.yaml) và trái GĐ8 (chưa có staging) → hợp đồng "khuyết là NO-GO" bị phá.
4. DÙNG ĐƯỢC NỬA ĐÊM (xương sống): [2] — 3 khối đánh số (deploy→smoke→rollback), mỗi bước smoke có "kỳ vọng thấy gì", ai-bấm theo vai; lệnh trỏ đúng seam THẬT đã kiểm (orchestrator.run/resume loop.py:93/217 · observability.inspect · /api/snapshot+/api/stream server.py:445/472 · build_snapshot control/snapshot.py). Trừ điểm treo: ngưỡng lùi trỏ metric/flag không tồn tại.
5. ĐỌC 3 TẦNG: [2] — trang mở bằng "GÓC NHÌN LÃNH ĐẠO 90 giây" đủ 3 câu (sẵn sàng-alpha · ký GO-theo-bậc-không-full · tắt flag <giây + team trực), nói rõ KHÔNG ký mở write/delegation, đọc riêng khối này quyết được.
6. LÝ DO + PHƯƠNG ÁN LOẠI: [2] — cả 4 quyết định lớn có lý do + phương án loại + vì-sao-loại bám đặc thù hệ (rolling-qua-flag vs blue-green/canary-% · rollback vs rollback-DB · không-gộp-bậc · GO-alpha vs NO-GO-cứng/GO-full).
7. ROLLOUT CÓ BẬC: [1] — bảng 5 bậc đủ 4 cột + điều kiện mở bậc nối đúng blocker GĐ12 (TC-REDACT-RAWARGS-003 · TC-DELEGATE-SCOPE-001), NHƯNG tín hiệu tiến/dừng lõi (`false_finish_total=0`, tắt `write_tools_enabled`) trỏ metric/flag không tồn tại → "tín hiệu đo được" không đo được thật.
8. ĐÚNG VAI & CỔNG: [1] — trình đủ khối cổng + tách khuyến-nghị/quyết-định + rollout gate 3-mảnh + bàn giao chỉ-liệt-kê, NHƯNG "CTO ✔ + PO ✔" tự cấp trong chế độ tự-quyết không ghi rõ AI đóng vai Người duyệt → ký ẩn danh, không tính là bằng chứng phân vai thật.

TỔNG: 10/16
GATE: rớt: tiêu chí xương sống 1 (BẰNG CHỨNG) = 0 và 3 (BỐN THỨ CHẶN) = 0 → rớt gate dù C4 xương sống còn lại đạt 2 và tổng không thấp. CTO sẽ ký GO trên nền metric/flag/rollback-test giả.
SỬA TRƯỚC TIÊN: Gắn nhãn tường minh 6 metric + 3 flag là "THIẾT KẾ GĐ11 chưa dựng, chưa có trong code gốc" và hạ "monitoring BẬT / rollback ĐÃ TEST" xuống điều-kiện-treo (rollout gate có địa chỉ), sửa "6 N/A"→"2 N/A" cho khớp bảng — vì hiện alert-cứng + rollback-lever + rollout-signal đều dựng trên seam không tồn tại.

---

## 2. Bảng tiêu chí × 3 lens + phân xử bất đồng

| Tiêu chí | ky-thuat | business | thi-cong | CHỐT | Ghi chú phân xử |
|---|---|---|---|---|---|
| 1. BẰNG CHỨNG (xs) | 1 | 0 | 0 | **0** | Giữ 0. Ky-thuat quá nhẹ tay (coi metric là "kế thừa GĐ11 nên không phải bịa mới"), nhưng rubric neo thẳng: "nêu tên metric/flag không tồn tại trong code gốc" = 0, VÀ "con số tóm tắt lệch bảng" (6 vs 2 N/A) = 0 độc lập. Tự kiểm: grep 6 metric + 3 flag = 0 hit; đếm bảng §1 = 2 ô N/A. |
| 2. ĐỦ BỘ | 2 | 2 | 2 | **2** | Đồng thuận. |
| 3. BỐN THỨ CHẶN (xs) | 1 | 0 | 0 | **0** | Giữ 0. Tự kiểm: `run_smoke.py` chỉ chạy echo+discipline+finish-gate, KHÔNG toggle flag / KHÔNG đọc features.yaml → không test được đường lùi; GĐ8 nói rebuild 0/9 tick, chưa staging → "rollback ĐÃ TEST" ruột rỗng. Monitoring "BẬT" dựa metric không tồn tại. 2/4 chặn rỗng ruột = 0. |
| 4. DÙNG ĐƯỢC NỬA ĐÊM (xs) | 2 | 1 | 2 | **2** | Nâng business 1→2. Tự kiểm seam: run/resume (loop.py:93/217), inspect.py, /api/snapshot+stream (server.py:445/472), build_snapshot (control/snapshot.py:import ui/ide/server.py:34) đều TỒN TẠI → cơ chế deploy→smoke→rollback thao tác được. Business đúng ở chỗ ngưỡng lùi trỏ metric/flag ma (đã trừ thành điểm treo), nhưng backbone lệnh thật → 2 lens độc lập chấm 2, giữ 2. Không phải chỗ gate (đã gate ở C1/C3). |
| 5. ĐỌC 3 TẦNG | 2 | 2 | 2 | **2** | Đồng thuận. |
| 6. LÝ DO + LOẠI | 2 | 2 | 2 | **2** | Đồng thuận. |
| 7. ROLLOUT CÓ BẬC | 2 | 1 | 2 | **1** | Hạ về 1 theo business. Cùng lỗi bịa metric/flag (đã sinh C1/C3=0) phá đúng yêu-cầu-cốt-lõi của C7 "tín hiệu tiến/dừng cụ thể (metric có tên)" — `false_finish_total=0` + tắt `write_tools_enabled` không đo/không tắt được thật. Ky-thuat/thi-cong khen cấu trúc bảng nhưng không trừ chỗ tín-hiệu-không-đo-được. |
| 8. ĐÚNG VAI | 1 | 2 | 1 | **1** | Giữ 1 (2 lens). Rubric neo 2 = "ghi rõ ai đóng vai Người duyệt + ngày ký, không ký ẩn danh". "CTO ✔ + PO ✔ (2026-07-02)" chỉ có vai + ngày, KHÔNG có người cụ thể → ẩn danh; khuyến-nghị-ship và quyết-định cùng một tác giả. Business=2 bỏ qua yêu cầu "không ẩn danh". |

**Bất đồng đáng chú ý & cách phân xử:**
- **C1/C3 (1 vs 0 vs 0):** ky-thuat là lens duy nhất cho 1 vì lập luận "metric kế thừa GĐ11, không phải ship bịa mới". Tôi mở code gốc + GĐ8 + GĐ11: bộ tên đúng là do GĐ11 §9/§ delivery ĐỀ XUẤT (flag/metric thiết kế), nhưng ship trình chúng như "monitoring ĐANG bật / rollback ĐÃ test", tức nâng thiết-kế-chưa-dựng thành trạng-thái-đang-chạy — đó chính là anchor 0 của rubric. Lấy điểm thấp (0), có bằng chứng.
- **C4 (2 vs 1 vs 2):** business hạ 1 do ngưỡng trỏ seam ma. Tôi tự kiểm 5 seam vận hành → tất cả tồn tại thật → cơ chế thao-tác-được đứng vững; chỉ ngưỡng-đo bị nhiễm (đã phản ánh ở C1/C3/C7). Theo luật "nâng phải chứng minh lens thấp sai": business sai ở chỗ đánh đồng ngưỡng-lỗi với runbook-không-thao-tác-được. Giữ 2.
- **C7 (2 vs 1 vs 2):** ngược chiều C4 — ở đây lỗi metric/flag đánh trúng đúng tiêu chí "tín hiệu đo được", nên business (1) đúng hơn. Hạ về 1.

---

## 3. Nghi bịa / không nguồn — đã xác nhận

1. **6 metric loop (`false_finish_total`, `task_finished_total`, `task_blocked_total{reason}`, `delegation_rejected_total{reason}`, `parse_error_total`, `budget_tripped_total`) — ĐỨNG VỮNG (bịa/không-khớp-code).** Tự kiểm: `observability/event_log.py:17-30` `_METRICS` thật = steps/llm_calls/llm_failures/tool_calls/tool_failures/parse_errors/policy_blocks/finish_gate_blocks/condensed/delegations/delegation_progress/delegation_failures. `grep -rn` toàn repo cho 6 tên này + cú pháp nhãn `{reason}` = 0 hit. Truy được về GĐ11 (tên đề xuất), nhưng ship trình như "monitoring BẬT" + alert cứng + rollout signal → nâng thiết-kế thành trạng-thái-chạy.
2. **3 flag `write_tools_enabled`/`delegation_enabled`/`rag_enabled` "đọc từ config/features.yaml runtime" — ĐỨNG VỮNG (không-khớp-code).** Tự kiểm: `config/features.yaml` thật có `features.<tên>.enabled` + block `rag:` + `delegation.enabled: true` (delegation MẶC ĐỊNH ON — ngược với claim "OFF default an-toàn-nhất"). grep 3 tên flag = 0 hit; không có runtime gate nào tắt write-tool/delegation theo 3 tên này. Truy về GĐ11 §9 là "ví dụ đặt tên" (thiết kế), nhưng ship trình như "runtime đọc được".
3. **"rollback ĐÃ TEST trên staging (smoke offline)" (dòng 17/49/60/76/177/194) — ĐỨNG VỮNG (mâu thuẫn nguồn).** Tự kiểm: GĐ8 (`08-skeleton.md:13,15,60,107`) nói thẳng "code REBUILD chưa được gõ và chưa deploy lên staging → 0/9 ô tick THẬT · link staging ⏳ CHƯA CÓ". `run_smoke.py` (code gốc, đọc thật) chỉ smoke echo+discipline+finish-gate, KHÔNG toggle flag / KHÔNG đọc features.yaml → không exercise được đường lùi. → "đã test rollback trên staging" không trỏ được chạy ở đâu/ngày nào.
4. **"6 N/A hợp lệ" (khối cổng dòng 176) — ĐỨNG VỮNG (lệch bảng).** Tự kiểm bảng §1: chỉ 2 ô N/A thật (ô 6 comms, ô 7 training); ô 4 migration trạng thái `[x]` có ghi-chú-N/A-nội-dòng, không phải ô N/A. Con số "6" tự phong, đếm lại không ra.
5. **"DoD S0 GĐ8" viện dẫn làm bằng chứng run_smoke đã test (dòng 76) — ĐỨNG VỮNG (attribution sai).** Tự kiểm: chuỗi "DoD S0"/"S0" xuất hiện **0 lần** trong `08-skeleton.md`; `run_smoke`/`smoke` cũng không được GĐ8 nhắc là gate đã pass. (Chuỗi này chỉ có trong `ship.json` do chính GĐ13 tự viết, không phải nguồn GĐ8.) Attribution lỏng tới nguồn không có.
6. **"CTO ✔ + PO ✔ (2026-07-02)" (dòng 192) — ĐỨNG VỮNG (ký ẩn danh).** Cổng GO do chính tác giả đóng vai CTO+PO tự cấp trong chế độ tự-quyết, không ghi ai đóng vai Người duyệt cụ thể → theo rubric C8 không tính là bằng chứng sign-off độc lập.

**Nghi bịa đã LOẠI sau kiểm (không đứng vững / hợp lệ):**
- **`build_snapshot` replay — HỢP LỆ.** ky-thuat cite "snapshot.py:189" (địa chỉ hơi lệch) nhưng seam THẬT tồn tại: `control/snapshot.py` `build_snapshot`, import ở `ui/ide/server.py:34`, gọi ở dòng 247 (fold events → snapshot). Claim replay đứng vững.
- **Seam runbook (`orchestrator.run/resume`, `observability.inspect`, `/api/snapshot`+`/api/stream`) — HỢP LỆ.** Kiểm thật: `orchestrator/loop.py:run`[93] `resume`[217]; `observability/inspect.py` tồn tại; `ui/server.py:445` /api/snapshot, `:472` /api/stream. Không phải bịa.
- **"26 PASS / 2 PENDING" nhận từ GĐ12 — KHÔNG tính vào C1 của ship.** business ghi GĐ12 có thể lệch bảng của chính nó, nhưng ship trích ĐÚNG nguồn GĐ12 và bị cấm re-audit → lỗi (nếu có) thuộc GĐ12, ghi để truy vết, không tính lỗi ship.
