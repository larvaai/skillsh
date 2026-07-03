CHẤM: review · /Users/uspro/Desktop/skillsh/rebuild-hex-agent/review/REVIEW.md

[2] PHẠM VI & BA TRỤC — khai rõ phạm vi (4 artifact 05/06/08/10) + chế độ tổng thể (edge→error→permission), cả ba trục đều có kết quả kiểm được + mục "KHÔNG TÌM THẤY GAP" nêu đích danh 5 vùng đã soi sạch.
[2] BẰNG CHỨNG (xương sống) — mọi neo lấy mẫu đối chiếu code gốc đều khớp (G1 graph.py:357-382, G2 loop.py:229-235 OR-guard, G3 kernel.py:123-126 raw args + policy.py:25-26 scope `<=`, Jaccard 0.80, budget consecutive, SessionSeq in-memory), con số 12=3C/5H/4M khớp thân bài (12 header = 12 dòng bảng), không neo bịa.
[2] KỊCH BẢN PHÁ (xương sống) — mỗi Critical dựng lại được như ca test (G1 AC-2 trỏ E1 của AC-1 → all_accepted sai; G2 artifact-rác mỗi round né OR-guard; G3 Bearer sk-… vào events.jsonl vĩnh viễn), đủ input/state/sequence → vì-sao-không-chặn → hậu quả.
[2] THẬT vs NGHI — ba vùng rạch ròi: gap thật có evidence · 3 mục "CÓ THỂ LÀ GAP" kèm câu hỏi cần-xác-nhận · 5 vùng "KHÔNG TÌM THẤY GAP" đích danh; G8 tự gắn nhãn "một phần là có thể là gap".
[1] PHÂN MỨC — chèn bậc tự chế "🟠 High" giữa Critical và Med VÀ bỏ hẳn "Low", nhưng KHÔNG khai một câu ánh xạ nào cho tier "High" về thang hợp đồng Critical/Medium/Low (chỉ có suy-hậu-quả từng gap, không phải khai-ánh-xạ-tier như score-2 đòi).
[2] DÙNG ĐƯỢC NGAY (xương sống) — mỗi gap có địa chỉ đóng cụ thể (bảng "Đóng ở đâu" + slice tên riêng), thứ tự suy từ mức, Bước-4 phủ đủ nhánh (Critical→/frame · High/Med→/backlog · nghi→SPIKE-1), mọi skill trỏ tới (/frame, /backlog, /partner, /traceability) đều có thật.
[1] ĐÚNG VAI — cốt là báo cáo, nhưng gần như MỌI gap có mục "Gợi ý sửa" đi vào thiết-kế-cơ-chế-thay-thế (đặt error code WRITE_TOOL_ENABLED_WITHOUT_REDACTION / ACCEPTANCE_UNSATISFIABLE, provenance schema, per-node stuck-counter, gán owner Execution-Core) — vượt mức trỏ-việc mà SKILL.md cấm; không tới 0 vì không viết code, không lấn explain/triage.

TỔNG: 12/14
GATE: đạt — ba tiêu chí xương sống (2, 3, 6) đều = 2, không cái nào = 0.
SỬA TRƯỚC TIÊN: Cắt mục "Gợi ý sửa" (cơ chế thay thế + error code tự chế) khỏi mỗi gap để về đúng vai review thuần báo-cáo (tiêu chí 7) — đây là đòn bẩy chung của cả 3 lens; kèm theo khai một câu ánh xạ "High → biến thể đầu-nặng của Medium (hành vi sai, không mất data/breach)" để nhấc tiêu chí 5.

---

## 2. Bảng tiêu chí × 3 lens + phân xử bất đồng

| # | Tiêu chí | ky-thuat | business | thi-cong | HỢP NHẤT | Ghi chú phân xử |
|---|---|---|---|---|---|---|
| 1 | PHẠM VI & BA TRỤC | 2 | 2 | 2 | **2** | Đồng thuận. Không bất đồng. |
| 2 | BẰNG CHỨNG (xương sống) | 2 | 2 | 2 | **2** | Đồng thuận; đã tự kiểm 8 neo, tất cả khớp. |
| 3 | KỊCH BẢN PHÁ (xương sống) | 2 | 2 | 2 | **2** | Đồng thuận. |
| 4 | THẬT vs NGHI | 2 | 2 | 2 | **2** | Đồng thuận. |
| 5 | PHÂN MỨC | **1** | 2 | 2 | **1** | **BẤT ĐỒNG (1 vs 2 vs 2).** Giữ điểm THẤP NHẤT. Tự mở artifact grep toàn văn: KHÔNG có một câu legend/khai-ánh-xạ nào cho tier "High"; "Low" bị bỏ hẳn. Rubric score-2 đòi "nếu dùng bậc trung gian thì **khai rõ ánh xạ**" — artifact chỉ suy-hậu-quả TỪNG gap (thoả nửa "hậu quả biện minh mức"), KHÔNG khai-ánh-xạ-tier. Hai lens chấm 2 nhầm suy-hậu-quả-từng-gap thành khai-ánh-xạ-tier. ky-thuat (score-1) khớp đúng anchor "dùng thang tự chế mà không nêu cách ánh xạ". Không nâng được. |
| 6 | DÙNG ĐƯỢC NGAY (xương sống) | 2 | 2 | 2 | **2** | Đồng thuận. |
| 7 | ĐÚNG VAI | 1 | 1 | 1 | **1** | Đồng thuận cả 3; đã xác nhận "Gợi ý sửa" đi vào thiết-kế-cơ-chế gần như mọi gap → lấn nhẹ (score-1), chưa tới 0. |
| | **TỔNG** | **12** | **13** | **13** | **12** | Chênh nằm ĐÚNG ở tiêu chí 5. |

**Bất đồng đáng chú ý duy nhất — tiêu chí 5 (PHÂN MỨC).**
- business & thi-cong lập luận: mỗi gap tự-biện-minh mức bằng hậu quả (G3 breach→Critical; G4/G7 "không mất data/không crash"→High; G9/G11 "không phá invariant"→Med), "đọc mức đoán được hậu quả" → cho 2.
- ky-thuat lập luận: artifact chèn "🟠 High" (thang tự chế) giữa Critical/Med mà không khai cách ánh xạ về thang hợp đồng → đúng anchor score-1.
- **Phân xử:** giữ 1. Đã grep toàn văn REVIEW.md (dòng 137, 183 là chỗ duy nhất chứa "thang/bậc/ánh xạ" nhưng đều nói về scope, không phải mapping tier). Không tồn tại câu nào khai "High = …" theo thang hợp đồng, và tier "Low" biến mất hoàn toàn khỏi thang. Rubric phân biệt rõ hai điều ở score-2: (a) hậu-quả-biện-minh-mức VÀ (b) khai-rõ-ánh-xạ-bậc-trung-gian. Artifact có (a) nhưng thiếu (b). Đúng chữ rubric score-1. business/thi-cong đã trộn (a) vào chỗ của (b) → chấm cao sai; không có bằng chứng nào nâng lại được.

Không có bất đồng nào khác: 6 tiêu chí còn lại cả 3 lens trùng điểm.

---

## 3. Nghi bịa / không nguồn — đã xác nhận

Gom nghi_bia của cả 3 lens rồi tự mở đúng file/code kiểm lại. Kết quả: **không còn claim bịa nào đứng lại — mọi neo trọng yếu khớp code gốc; các cổng tự-phong đã loại đúng, không dùng làm bằng chứng.**

- **8 neo file:line lấy mẫu — TẤT CẢ khớp `/Users/uspro/Desktop/namnson/hex_agent`:**
  - G1 `judge_acceptance` (supervisor/graph.py:357-382): honor "passed" khi evidence resolve trên Blackboard (`e in state.artifacts`) ∧ ≥1 kiểu real — KHÔNG kiểm evidence thuộc AC đang chấm. Cross-AC reuse gap CÓ THẬT, neo chính xác.
  - G2 no-progress (supervisor/loop.py:229-235): `progressed = artifacts>before OR acceptance≠before OR applied>0` — đúng OR-guard; artifact-rác +1 mỗi round làm nhánh đầu true → guard không trip. Mô tả khớp.
  - G3 raw args (core/kernel.py:123-126): `publish("tool.requested", {..., "args": request.args})` phát RAW args; redact ở control/emitter+redaction (biên), "redact-trước-write" chỉ là ràng buộc điều-phối (ADR-006 + 10-modules Tools-Safety SLA dòng 222-223), KHÔNG có cơ chế enforce. Gap CÓ THẬT.
  - policy.py:25-26 + core/session.py:163: cả hai dùng `scope <= parent.allowed_capabilities` (⊆ cho phép ==) — nền cho G9 "không-thu-hẹp". Khớp.
  - decompose_agent/accept.py:22,224-225: `JACCARD_MAX = 0.80`, RENAME khi `_jaccard > JACCARD_MAX` — lexical token-overlap. Khớp G8.
  - discipline/budget.py:13-45: `consecutive_parse_errors` reset on good parse, `max_parse_errors=8` CONSECUTIVE, `parse_errors` chỉ telemetry. Khớp G10.
  - control/events.py:193-208 `SessionSeq`: counter thuần in-memory (`self._counters: dict[str,int]={}`, mỗi session 0+1=1), KHÔNG persist → tiến-trình-mới reset. G11 (nguồn seq khi restore chưa nêu) là câu-hỏi-thiết-kế hợp lý, artifact khai đúng là nghi-ngờ Med, không overclaim.
- **Con số "12 gap (3 Critical/5 High/4 Med)":** đếm thực — 12 header `[Critical|High|Med] Gn` = 12 dòng bảng scan; 3+5+4=12; nhất quán summary↔bảng↔cổng↔bàn giao. KHÔNG tự phong lệch.
- **"skeleton 0/9 tick":** truy về 08-skeleton.md ("Tổng tick THẬT rebuild: 0/9") — tự-thú trung thực, có nguồn, KHÔNG bịa; nhưng không miễn trừ tiêu chí nội dung.
- **Cổng "GATE: NO-GO/GO" (dòng 226) + "Xương sống 7-invariant KHÔNG gãy":** AI tự cấp trong chế độ tự-quyết ("đóng vai Reviewer, KHÔNG tự duyệt phần mình viết") — theo luật khắt khe KHÔNG tính là bằng chứng ngoài. Đã loại đúng: điểm tiêu chí 6 dựa trên địa-chỉ-đóng từng gap, không dựa cổng tự-phong. Artifact tự khai rõ vai nên không nguỵ trang thành đã-duyệt-ngoài.
- **"detects STUCK" thừa hưởng từ evidence-A:** decompose_agent/accept.py:27 `STUCK_DECOMP` chỉ là chuỗi error-code, không có logic detect đầy đủ; artifact xử lý trung thực bằng cách để STUCK ở "CÓ THỂ LÀ GAP" (G8-phụ) thay vì khẳng định → không thành claim bịa của REVIEW.
