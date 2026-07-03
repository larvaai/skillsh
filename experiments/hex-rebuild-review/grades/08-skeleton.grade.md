CHẤM: 08-skeleton · /Users/uspro/Desktop/skillsh/rebuild-hex-agent/pipeline/08-skeleton.md

[1] Tiêu chí 1 — MỞ ĐẦU LÃNH ĐẠO: khối "Góc nhìn lãnh đạo" đứng đầu có đủ 3 thứ bắt buộc (staging ⏳ CHƯA CÓ · 0/9 tick · giả định SPIKE-1) NHƯNG lọt file:line + tên hàm chưa giải nghĩa (dòng 13: `supervisor/loop.py:_drive`, `delegation/manager.py:63`, `judge_acceptance`; dòng 15: Python 3.11+LangGraph+SQLite, SPIKE-1) → CTO/CEO ngoài đọc riêng vẫn vấp jargon.
[2] Tiêu chí 2 — SLICE ĐÚNG DẠNG: một slice `finish-by-evidence-tối-thiểu`, E2E 9+1 chặng xuyên đủ tầng (control-plane cố ý để ngoài + lý do ADR-006), lý do chọn nối về 6/7 invariant lõi, ≥3 slice đã cân nhắc & loại kèm lý do.
[2] Tiêu chí 3 — BẰNG CHỨNG KIỂM ĐƯỢC (xương sống): ~15 anchor kiểm được đều khớp code gốc; chỗ chưa chắc gắn nhãn (SPIKE-1 CHƯA ĐO, NFR không bịa); không câu tự khen vô căn — chỉ 2-3 khung phạm vi lệch nhẹ (finished, accept.py range), là imprecision không phải bịa.
[2] Tiêu chí 4 — CHẠY THẬT, KHÔNG MOCKUP (xương sống): 0/9 tick, không một ô khống; mỗi ô trống ghi thành rủi ro + nơi kiểm (tách G-gốc/R-rebuild); staging "CHƯA CÓ — chặn pass"; cổng TRÌNH NO-GO, loại thẳng phương án "tick theo gốc = tick khống".
[2] Tiêu chí 5 — DÙNG ĐƯỢC NGAY (xương sống): bảng E2E chỉ rõ thành phần + điều phải chứng minh mỗi chặng; mỗi ô checklist có tiêu chí tick đo được (DoD/property-test); khối bàn giao đích danh việc + skill (/frame, /backlog, /delivery, /partner); CTO đủ dữ kiện quyết.
[2] Tiêu chí 6 — BÁM ĐẦU VÀO GĐ7 + FEED NGƯỢC: dùng đúng stack GĐ7, không chọn lại; 4 giả-định-đổi mỗi cái chỉ artifact feed ngược đã kiểm là thật (OQ-3 khớp `06-shape.md:205`, redact khớp `06-shape.md:238`/ADR-006, max_steps-ở-discipline khớp `discipline/budget.py`); mỗi rủi ro có địa chỉ kiểm.
[2] Tiêu chí 7 — RANH GIỚI VAI + LỐI ĐI TIẾP: chỉ định-slice+checklist+báo-cáo, code giao /frame, phân rã giao /backlog, không mở lại stack; không phủ định cứng ("chưa dựng nên chưa chứng minh", dòng 159); mọi chỗ chưa proven kèm lối đi tiếp.

TỔNG: 13/14
GATE: đạt — cả 3 tiêu chí xương sống (3, 4, 5) đều = 2, không cái nào = 0.
SỬA TRƯỚC TIÊN: Dọn sạch file:line + tên-hàm (`supervisor/loop.py:_drive`, `delegation/manager.py:63`, `judge_acceptance`) và jargon stack (Python/LangGraph/SQLite/SPIKE-1) ra khỏi khối "Góc nhìn lãnh đạo", đẩy xuống phần kỹ thuật — đòn bẩy duy nhất kéo tiêu chí 1 từ 1→2 và tổng lên 14/14.

---

## 2. Bảng tiêu chí × 3 lens + phân xử bất đồng

| Tiêu chí | ky-thuat | business | thi-cong | HỢP NHẤT | Ghi chú phân xử |
|---|---|---|---|---|---|
| 1. Mở đầu lãnh đạo | 2 | 1 | 1 | **1** | Bất đồng chính. Xem phân xử #1 dưới. |
| 2. Slice đúng dạng | 2 | 2 | 2 | **2** | Đồng thuận. |
| 3. Bằng chứng kiểm được (xương sống) | 2 | 2 | 2 | **2** | Đồng thuận; đã tự kiểm ~15 anchor. |
| 4. Chạy thật, không mockup (xương sống) | 2 | 2 | 2 | **2** | Đồng thuận; 0/9 tick khớp `skeleton.json:validate_tick "0/9"`. |
| 5. Dùng được ngay (xương sống) | 2 | 2 | 2 | **2** | Đồng thuận. |
| 6. Bám GĐ7 + feed ngược | 2 | 2 | 2 | **2** | Đồng thuận. |
| 7. Ranh giới vai + lối đi tiếp | 2 | 2 | 2 | **2** | Đồng thuận. |
| **TỔNG** | 14/14 | 13/14 | 13/14 | **13/14** | |

### Bất đồng đáng chú ý và cách phân xử

**#1 — Tiêu chí 1 (2 vs 1 vs 1): giữ 1.**
Luật hợp nhất = lấy điểm THẤP NHẤT trừ khi chứng minh được lens thấp chấm sai. Ở đây tôi tự mở khối "Góc nhìn lãnh đạo" (dòng 9-17) và XÁC NHẬN lens thấp (business + thi-cong) chấm ĐÚNG:
- Dòng 13 nhồi thẳng anchor code vào khối lãnh đạo: *"vòng lặp `supervisor/loop.py:_drive`, cửa giao-việc `delegation/manager.py:63`, resume `orchestrator/loop.py:resume`, nghiệm-thu-bằng-bằng-chứng `judge_acceptance`"* — đây là file:line + tên hàm, đúng loại "thuật ngữ code chưa được giải nghĩa" mà rubric mức-1 mô tả.
- Dòng 15 nêu trần "Python 3.11 + LangGraph + SQLite", "LangGraph resume một-lần-đúng", "SPIKE-1" — jargon stack chưa dịch cho người không-code.
Rubric mức 2 đòi "ngôn ngữ nghiệp vụ, KHÔNG jargon" và "đọc RIÊNG khối này CTO/business ngoài hiểu on-track". Có file:line trong khối lãnh đạo là vi phạm trực tiếp. Lens ky-thuat cho 2 vì bản thân người kỹ thuật đọc-qua-được jargon — nhưng tiêu chí này đo cho người NGOÀI code, nên góc nhìn ky-thuat không phải chuẩn. → Giữ 1.

**#2 — Đủ 3 thứ bắt buộc (không tụt xuống 0):** Cả 3 lens đồng thuận khối lãnh đạo CÓ đủ 3 thứ (staging trung thực · trạng thái checklist · giả định đổi) và đứng đầu report, nên không rơi mức 0. Điểm 1 là đúng "có khối nhưng lọt jargon", không phải "không có khối / mở bằng kỹ thuật".

**#3 — Gate:** Cả 3 lens đều chấm 3 tiêu chí xương sống = 2. Không có cái nào = 0 → GATE ĐẠT. Tổng 13/14 không ảnh hưởng gate.

---

## 3. Nghi bịa / không nguồn — đã xác nhận

Gom nghi_bia của cả 3 lens, tự mở file/code kiểm lại từng cái:

1. **"327 test"** — ĐỨNG VỮNG, KHÔNG bịa. Kiểm `docs/roadmap/project-roadmap.md:159` ghi nguyên văn "198 test functions (tests/) + 129 test audit (tests_audit/) = 327 functions"; cũng có ở `:41`, `:61`, `:169` và `docs/explanation/overview-pdr.md:172`. Report còn tự caveat "CI cụ thể chưa neo được cho bản rebuild" (dòng 89) và KHÔNG dùng số này để tick ô 6 (ô 6 trống). Không tự phong.

2. **"finished [186]" (bảng §2 chặng 9)** — imprecision NHỎ, KHÔNG bịa. Kiểm `supervisor/loop.py`: nhánh `if decision.decision == "finished"` ở dòng 184, `_terminate(... FINISHED ...)` ở dòng 189 — không phải 186. Drift ~2 dòng, vẫn nằm trong hàm `_drive` [157-241]; nội dung/hành vi có thật. Xếp mức 1-issue của tiêu chí 3, không đủ để hạ điểm (mọi anchor khác khớp).

3. **"accept.py:52-128 (μ proof, coverage [101-127])" gán tên `accept_decomposition`** — imprecision NHỎ, KHÔNG bịa. Kiểm `decompose_agent/accept.py`: `def accept_decomposition` thực ở dòng 186, không trong 52-128. Nhưng `def mu` @52 và `def _implies` (coverage-by-implication) @101 ĐÚNG là các mảnh được trích trong khoảng đó. Anchor có thật, chỉ ghép tên-hàm-cổng với range của helper hơi lệch.

4. **OQ-3 event mismatch (`tool.requested/completed` vs `tool.call_requested/before_call/after_call`)** — ĐỨNG VỮNG, có nguồn thượng nguồn. Kiểm `06-shape.md:205` ghi ĐÚNG NGUYÊN VĂN mismatch này và quyết "reconcile về `tool.requested/completed/failed`". Trong code gốc: `core/kernel.py:124` emit `tool.requested`, `:216` emit `tool.completed/failed`; còn `tool.call_requested/before_call/after_call` xuất hiện ở control-plane/design-pattern files và `ui/ide/bridge.py`. Mismatch là thật, được nêu như "known gap phải reconcile", không tự phong là đã xong.

5. **"atomic txn loop.py:208-218" (bảng §2 chặng ✚)** — imprecision NHỎ, KHÔNG bịa. Kiểm `orchestrator/loop.py`: `def resume` bắt đầu @217; 208-218 là đuôi một helper restore-session + đầu resume. Cơ chế atomic/checkpointer có thật (`open_checkpointer` trong resume, resume-from-`snapshot.next`), chỉ khung dòng hơi lệch. Cùng loại với #2/#3.

6. **Gate "NO-GO/GO dựng-slice" tự-cấp** — KHÔNG tính là bằng chứng pass, đúng luật. Report giữ NO-GO cho pass/build-full, chỉ mở GO cho việc bàn-giao /frame; KHÔNG mượn nó để tick ô nào (0/9). Không thành tick khống → tiêu chí 4 vẫn = 2.

7. **"9/9 có bằng-chứng-đường-đi gốc anchored"** — ĐỨNG VỮNG. Tự kiểm các anchor lõi đều khớp code gốc: `core/kernel.py:106` execute_tool, `delegation/manager.py:63` delegate, `delegation/policy.py:25-26` scope⊆parent, `core/session.py:163` scope-shrink, `supervisor/graph.py:357` judge_acceptance, `supervisor/evidence.py:16` EVIDENCE_TYPES (đúng 5 loại), `decompose_agent/tree.py:43` next_node, `orchestrator/loop.py:217` resume, `observability/event_log.py:102` attach_to_bus, `discipline/budget.py:10-67` Budget (`max_steps` @20, enforce @42). Claim đúng, không tự phong.

**Kết luận:** Không còn claim BỊA nào sau kiểm. 3-4 anchor có khung dòng lệch nhẹ (finished, accept range, atomic txn) là imprecision file:line trong-hàm — đủ để nêu là "sửa trước tiên về kỷ luật anchor" nhưng KHÔNG đủ hạ tiêu chí 3 xuống 1 (rubric mức-1 = "1-2 chỗ mơ hồ không gắn nhãn"; đây là anchor có thật, chỉ lệch offset nhỏ trong cùng hàm, không phải claim không kiểm được).
