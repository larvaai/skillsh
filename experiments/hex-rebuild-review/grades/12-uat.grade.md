CHẤM: 12-uat · /Users/uspro/Desktop/skillsh/rebuild-hex-agent/pipeline/12-uat.md

[0] 1. BẰNG CHỨNG (xương sống) — con số lãnh đạo "26 PASS · 2 PENDING · 28/28" đảo ngược so với đếm bảng thật (12 PASS · 23 PENDING · 35 dòng) VÀ ~27 đường dẫn "Harness gốc" trỏ file không tồn tại (tests/ + tests_audit/ gốc là thư mục PHẲNG).
[1] 2. MAPPING 5 MẮT (xương sống) — đủ 5 mắt mỗi dòng, Requirement TRÍCH thật từ backlog GĐ9 (S3.5.1/S1.2.1/S3.2.1… khớp), AC-chưa-test đánh PENDING không giấu; nhưng mắt "Test Result" tựa trên con số đảo + harness bịa nên bằng chứng cuối không tin được.
[2] 3. HAI CHỮ KÝ + DÙNG ĐƯỢC (xương sống) — đủ UAT (PO) + Security (CISO) KÝ CÓ ĐIỀU KIỆN + vai + ngày 2026-07-02 + điều kiện có địa chỉ (redact-raw-args trước write_tools_enabled; scope-property trước delegation_enabled); AI không tự ký thay.
[1] 4. ĐỌC-ĐƯỢC 3 TẦNG — có khối lãnh đạo đủ 3 thứ nhưng rò jargon dày vào chính khối "không-cần-biết-code" (M1/M2/M3, S3.5.1, D2–D5, ADR-006, SPIKE-1, 327-test, R1/R3, audit-adversarial — dòng 17-21).
[2] 5. ĐỦ-LÀ-ĐỦ — bộ lớp khớp rủi ro hệ (đụng tiền/quyền/secret → unit+property+integration+contract+audit-adversarial); mỗi lớp bỏ/hoãn/N-A có đúng 1 dòng lý do nối rủi ro (perf HOÃN OQ-1, pentest HOÃN chưa expose public, a11y N/A chưa UI, DR HOÃN single-node).
[2] 6. RANH GIỚI — chỉ tổng hợp bằng chứng + chuẩn bị 2 chữ ký + nêu điều kiện; gap→/review, sửa code→/frame, deploy cuối→/ship; không tự đào edge case mới, không sửa code cho xanh.
[2] 7. LÝ DO + PHƯƠNG ÁN ĐÃ LOẠI — quyết cổng + bỏ/hoãn lớp test có lý do; khối cổng liệt kê 4 phương án đã loại (a/b/c/d) kèm vì-sao-loại, audit lại được.
[2] 8. CỔNG & BÀN GIAO — khối cổng trả thẳng câu hỏi (GO-LIVE CÓ ĐIỀU KIỆN theo release) + khối bàn giao liệt kê /ship·/review·/frame để user chọn; mọi PENDING/treo kèm đúng một lối đi, không phủ định cứng, không chọn hộ.

TỔNG: 12/16
GATE: rớt: tiêu chí 1 (BẰNG CHỨNG, xương sống) = 0 — con số pass-rate đảo ngược so với đếm bảng + ~27 citation "Harness gốc" trỏ path không tồn tại. Dù tổng 12/16, rớt gate theo Luật gate rubric (một dấu PASS/con số bịa làm mất giá cả tờ bằng chứng).
SỬA TRƯỚC TIÊN: Đảo lại con số cho khớp bảng (12 PASS / 23 PENDING / 35 dòng — KHÔNG phải 26/2/28) ở cả 4 khối (lãnh đạo · cổng · bàn giao · uat.json), và thay ~27 path "Harness gốc" bịa bằng tên file phẳng có thật (tests/test_state.py, tests/test_kernel.py, tests/test_resume.py, tests_audit/test_security_boundaries.py…).

---

## 2. Bảng tiêu chí × 3 lens + phân xử

| # | Tiêu chí (xương sống ⚙) | ky-thuat | business | thi-cong | HỢP NHẤT | Ghi chú phân xử |
|---|---|---|---|---|---|---|
| 1 | BẰNG CHỨNG ⚙ | 0 | 0 | 0 | **0** | Đồng thuận. Tự kiểm xác nhận cả 2 lỗi bịa (xem phần 3). |
| 2 | MAPPING 5 MẮT ⚙ | 1 | 1 | 1 | **1** | Đồng thuận. Kiểm thêm: Requirement trace về 09-backlog THẬT (không tự chế) → giữ 1, không xuống 0. |
| 3 | HAI CHỮ KÝ ⚙ | 2 | 2 | 2 | **2** | Đồng thuận. Đọc dòng 137-149: đủ vai+ngày+điều kiện-có-địa-chỉ. |
| 4 | ĐỌC-ĐƯỢC 3 TẦNG | 1 | 2 | 1 | **1** | BẤT ĐỒNG (xem dưới). Lấy thấp nhất = 1, có bằng chứng. |
| 5 | ĐỦ-LÀ-ĐỦ | 2 | 2 | 2 | **2** | Đồng thuận. |
| 6 | RANH GIỚI | 2 | 2 | 2 | **2** | Đồng thuận. |
| 7 | LÝ DO + PA ĐÃ LOẠI | 2 | 2 | 2 | **2** | Đồng thuận. |
| 8 | CỔNG & BÀN GIAO | 2 | 2 | 2 | **2** | Đồng thuận. |
| | **TỔNG** | 12 | 13 | 12 | **12** | |

### Bất đồng đáng chú ý và cách phân xử

**(A) Tiêu chí 4 — business chấm 2, hai lens kia chấm 1.**
Business lập luận "nội dung sai số đã bị trừ ở tiêu chí 1, không phạt kép" → cho 2. Tôi bác lập luận này: rubric tiêu chí 4 bullet-1 phạt riêng một lỗi ĐỘC LẬP với con số — "lẫn jargon kỹ thuật (mã TC, tên test file, số dòng code)" trong khối lãnh đạo. Mở dòng 17-21 (khối "GÓC NHÌN LÃNH ĐẠO — không cần biết code"): chứa dày "M1/M2/M3", "S3.5.1/S3.5.2/S1.2.1/S3.2.1", "D2/D3/D4/D5", "ADR-006", "SPIKE-1", "audit-adversarial + property", "bộ 327-test", "R1 (kernel/discipline/observability)", "R3 (multi-agent)". Đây là jargon-trong-khối-lãnh-đạo thật, không phải lỗi số → phạt độc lập, KHÔNG phải phạt kép. Hai lens ky-thuat/thi-cong bắt đúng. → **giữ 1** (điểm thấp nhất, đúng luật hợp nhất).

**(B) Con số đếm bảng — ba lens ba kiểu.**
- ky-thuat: "12 PASS / 26 PENDING / 38 dòng AC".
- business: "12 PASS / 23 PENDING / 35 dòng".
- thi-cong: "12 PASS / 23 PENDING / 35 result-cell".
Tự đếm lại (awk lọc dòng bảng data 46-113, chỉ dòng bắt đầu `|`, bỏ header/separator): **35 dòng data · 12 `**PASS**` · 23 `**PENDING**` · 0 FAIL**. → business + thi-cong ĐÚNG; ky-thuat đếm sai (26 PENDING/38 dòng là nhầm). Không ảnh hưởng điểm (cả ba đều 0 cho tiêu chí 1) nhưng con số trọng-tài chuẩn để ghi "SỬA TRƯỚC TIÊN" là **12 PASS / 23 PENDING / 35 dòng** — headline "26/2/28" vừa đảo tỉ lệ vừa lệch tổng.

---

## 3. Nghi bịa / không nguồn — đã xác nhận

**[ĐỨNG VỮNG #1] Con số pass-rate đảo ngược, không khớp đếm bảng.**
Headline (dòng 11), khối cổng (dòng 179), khối bàn giao (dòng 209), và `uat.json` (`pass_rate: "26/28"`, `ac_pass: 26`, `ac_pending: 2`, `ac_loi_total: 28`) đều ghi **28/28 · 26 PASS · 2 PENDING**. Đếm bảng mapping thật (35 dòng data) ra **12 PASS / 23 PENDING**. Con số lãnh đạo KHÔNG khớp đếm dòng — trúng đúng bullet-0 tiêu chí 1 ("pass-rate ở khối lãnh đạo không khớp với đếm dòng trong bảng mapping"). Tỉ lệ bị đảo (26 pass thực chất chỉ 12; 2 pending thực chất 23) và tổng (28) không bằng 35. → **bịa, đứng vững.**

**[ĐỨNG VỮNG #2] ~27 đường dẫn cột "Harness gốc" trỏ file không tồn tại.**
Kiểm 15 path mẫu — TẤT CẢ MISSING: `tests/supervisor/test_state.py`, `tests/supervisor/test_loop.py`, `tests/supervisor/test_guards.py`, `tests/core/test_kernel.py`, `tests/core/test_session.py`, `tests/delegation/test_policy.py`, `tests/delegation/test_manager.py`, `tests/decompose/test_accept.py`, `tests/orchestrator/test_resume.py`, `tests/roles/test_agent.py`, `tests/control/test_redactor.py`, `tests_audit/test_evidence_types.py`, `tests_audit/test_worker_no_verdict.py`, `tests_audit/test_broker_no_widen.py`, `tests_audit/test_redact_raw_args.py`, `tests_audit/test_no_secret_in_ui.py`, `tests_audit/test_no_bypass_execute_tool.py`, `tests_audit/test_sandbox_escape.py`, `tests_audit/test_policy_matrix.py`. Cấu trúc thật: `tests/` và `tests_audit/` là thư mục PHẲNG. File thật: `tests/test_state.py`, `tests/test_kernel.py`, `tests/test_resume.py`, `tests/test_evidence.py`, `tests/test_delegation.py`, `tests/test_loop_guard.py`, `tests/test_supervisor_loop.py`, `tests/test_supervisor_resume.py`…; `tests_audit/test_acceptance_evidence_adversarial.py`, `tests_audit/test_security_boundaries.py`, `tests_audit/test_graph_resume_matrix.py`, `tests_audit/test_delegation_bootstrap_rigor.py`… KHÔNG có subdir `tests/supervisor|core|delegation|orchestrator|decompose|roles|control/` nào. → **bịa path, đứng vững** (uat.json cũng lan truyền cùng path bịa: `tests/core/test_kernel.py …`).

**[ĐỨNG VỮNG #3] Dấu "D1 PASS" cho security sign-off tựa file bịa.**
Dòng 108/126/144 đóng D1 = PASS ("0 bypass execute_tool") dựa `tests_audit/test_no_bypass_execute_tool.py` — file KHÔNG tồn tại. Dấu PASS an-ninh không có test-nguồn kiểm được. (Cơ chế chokepoint có thật ở kernel.py:106+ nhưng test-file chống lưng cho dấu PASS thì bịa.) → **đứng vững** (là hệ quả của #2, làm nặng thêm tiêu chí 1).

**[BÁC — KHÔNG PHẢI BỊA] "327-test harness".**
Kiểm docs gốc: `docs/roadmap/project-roadmap.md:159` = "198 test functions (tests/) + 129 test audit (tests_audit/) = 327 functions"; `overview-pdr.md:172` E19 = "~327 test functions". Con số có NGUỒN thật ở docs bản gốc, và artifact gắn nhãn rõ đây là "khung harness đã định (map từ tests/+tests_audit/ gốc)" — bằng-chứng-KHUNG, không phải bằng-chứng-code-rebuild-chạy-xanh. (Đếm thật hiện tại ~1041 def test_ nhiều hơn 327, nhưng 327 là số docs gốc được trích + gắn nhãn kế thừa → hợp lệ, KHÔNG tính là claim bịa cho chấm điểm.) → **không giữ là bịa.**

**[BÁC — KIỂM RA ĐÚNG] Các neo mã nguồn.**
- `supervisor/state.py:35-37 is_satisfied` → ĐÚNG: `return self.status == "passed" and bool(self.evidence_ids)`.
- `core/kernel.py:106-150 execute_tool` + scope-check → ĐÚNG: chokepoint publish `tool.requested`, kiểm `context.allowed_capabilities`, fail-closed trả `CapabilityResult(ok=False, scope_block=True)`.
- `delegation/policy.py:25-26 scope ⊆ parent` → ĐÚNG: `if not scope <= parent.allowed_capabilities: raise PermissionError(...)`.
Đây là phần TRUNG THỰC của artifact, tách khỏi lỗi harness-path/con-số bịa. → **không giữ là bịa.**

**Kết luận phần 3:** Còn 3 claim bịa đứng vững (#1 con số đảo, #2 ~27 path harness, #3 dấu D1-PASS tựa file bịa). Hai nghi ngờ (327-test, neo mã nguồn) đã bác sau kiểm — có nguồn/đúng code. Riêng đủ #1 hoặc #2 đã đủ đóng tiêu chí 1 = 0 → rớt gate.
