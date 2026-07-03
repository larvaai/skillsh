CHẤM: 07-stack · /Users/uspro/Desktop/skillsh/rebuild-hex-agent/pipeline/07-stack.md

[1] BẰNG CHỨNG — mọi claim về code gốc kiểm đúng và spike ghi trung thực "⏳ CHƯA CHẠY/TREO", NHƯNG mọi ô TỔNG được tuyên là Σ(trọng số×điểm) lại không bằng phép tính → là số không giải thích được từ đâu ra (level-1 "ô điểm không giải thích được từ đâu ra").
[2] MA TRẬN CÓ ĐIỂM — đủ 6 ma trận điểm×trọng số+TỔNG+Chọn/Lý do/Đã loại và trọng số có lý do neo ràng buộc, nhưng TỔNG sai số học ở 6/6 bảng (14/16 ô candidate lệch) — "TỔNG lệch không đổi kết luận".
[2] ADR ĐỦ MẢNH — 7 ADR đủ Bối cảnh·Quyết định·Lý do·Đã loại·Hệ quả; "Đã loại" ghi điểm mạnh thật + điều-kiện-đảo-chiều + Hệ quả nêu vendor-lock/hiring/migration, không câu phủ định cứng.
[2] SPIKE CHO ẨN SỐ — ẩn số rủi ro cao duy nhất (LangGraph resume round-trip) có SPIKE-1 đủ câu hỏi+time-box 1–2 ngày+tiêu chí (a)(b)(c) đo được+TREO có địa chỉ GĐ8+điều-kiện-đảo-chiều; hạng mục quen mỗi cái 1 dòng "không spike vì…".
[1] GÓC NHÌN LÃNH ĐẠO — mở bằng khối "Góc nhìn lãnh đạo 60 giây" đủ 4 mảnh bằng tiếng nghiệp vụ, nhưng jargon lọt dày ngay dòng "Chọn gì" ("SSE một chiều", "LLM adapter kiểu OpenAI-compatible JSON-mode", "pytest+Hypothesis property-based", "audit-test") mà người không viết code không duyệt nổi.
[2] NEO KIẾN TRÚC + ĐÚNG VAI — §0 nối từng ràng buộc GĐ6→ô tool (SQLite←ADR-005, LLM-qua-execute_tool←ADR-002, SSE←3-seam), brownfield tính stack Python gốc, không vẽ lại style/boundary, không viết code, đảo chiều spike giữ trong GĐ7.
[2] BÀN GIAO DÙNG ĐƯỢC — khối bàn giao chốt công cụ cụ thể từng hạng mục (hoặc open-Q có địa chỉ) + "ràng buộc kéo theo" (vendor-lock/migration/hiring) + ẩn số treo kèm nơi đo + điều-kiện-đảo-chiều; cổng rà đủ 4 điều kiện hợp đồng.

TỔNG: 11/14
GATE: đạt — 3 tiêu chí xương sống (1, 2, 7) đều > 0 (lần lượt 1/1/2); không tiêu chí xương sống nào = 0 nên không rớt gate, dù ma trận sai số học tràn lan.
SỬA TRƯỚC TIÊN: Cộng lại đúng TỔNG cả 6 ma trận cho khớp Σ(trọng số×điểm) đã tuyên (Python 132→134, Orchestrator 87→83, Postgres/Redis 47/40→49/43, SSE 91→94, pytest+Hyp 90→95) và xử lý minh bạch ô "—" của §5 (bỏ tuyên "none thắng" vì applicable-only 60 < Qdrant 62, chuyển hẳn sang lý do ràng-buộc-GĐ6/YAGNI) — một đòn này kéo cả tiêu chí 1 và 2 từ 1→2.

---

## Bảng tiêu chí × 3 lens + phân xử

| # | Tiêu chí (xương sống*) | ky-thuat | business | thi-cong | CHỐT | Ghi chú phân xử |
|---|---|---|---|---|---|---|
| 1 | BẰNG CHỨNG* | 1 | 1 | 2 | **1** | Lấy thấp nhất. thi-cong=2 không đứng vững: artifact tự tuyên "TỔNG = Σ(trọng số × điểm)" (§35) nhưng 14/16 ô TỔNG không bằng phép tính đó → đúng level-1 "ô điểm không giải thích được từ đâu ra". Không phải chỉ lỗi số học của tiêu chí 2 — con số hiển thị mâu thuẫn công thức đã tuyên là claim không truy về nguồn. Không hạ 0 vì mọi claim code gốc kiểm đúng, spike ghi trung thực. |
| 2 | MA TRẬN CÓ ĐIỂM* | 1 | 1 | 1 | **2** | ĐỒNG THUẬN cả 3 = 1. Tự kiểm lại: đủ ma trận + trọng số (có lý do) + TỔNG + Chọn/Lý do/Đã loại; TỔNG lệch nhưng KHÔNG ô nào đổi thứ hạng candidate (winner mọi bảng giữ nguyên) → đúng mô tả level-1 "TỔNG lệch nhỏ không đổi kết luận". Giữ đúng đồng thuận: **1**. |
| 3 | ADR ĐỦ MẢNH | 2 | 2 | 2 | **2** | Đồng thuận. |
| 4 | SPIKE CHO ẨN SỐ | 2 | 2 | 2 | **2** | Đồng thuận. |
| 5 | GÓC NHÌN LÃNH ĐẠO | 1 | 2 | 2 | **1** | Lấy thấp nhất; KHÔNG nâng. Kiểm dòng "Chọn gì" (§11): chứa "OpenAI-compatible JSON-mode adapter", "property-based", "audit-test", "SSE một chiều" — jargon thật, người không viết code không parse nổi, dù header §9 tự hứa "không cần biết code". Hai lens đọc rộng lượng nhưng charge của ky-thuat đúng sự thật nên không thể chứng minh sai. Phần "vì sao"/"rủi ro" (§13,15) sạch hơn (P95/spike có gloss), nhưng riêng khối mở đã lọt jargon = level-1. |
| 6 | NEO KIẾN TRÚC + ĐÚNG VAI | 2 | 2 | 2 | **2** | Đồng thuận. |
| 7 | BÀN GIAO DÙNG ĐƯỢC* | 2 | 2 | 2 | **2** | Đồng thuận. |
| | **TỔNG** | 11/14 | 12/14 | 13/14 | **11/14** | |
| | **GATE** | đạt | đạt | đạt | **đạt** | Xương sống 1,2,7 = 1/1/2, không cái nào 0. |

### Bất đồng đáng chú ý và cách phân xử

1. **Tiêu chí 1 (1 vs 1 vs 2).** thi-cong tách bạch "sai số học là lỗi tiêu chí 2, không phải tiêu chí 1" và giữ 1 ở tiêu chí 1. Nhưng artifact TUYÊN công thức "TỔNG = Σ(trọng số × điểm)" (§35) rồi hiển thị số không bằng công thức → đây không chỉ là cộng sai (tiêu chí 2) mà là con số không truy về được nguồn/công thức đã khai (tiêu chí 1, level-1 "ô điểm không giải thích được từ đâu ra"). Cả ky-thuat lẫn business đều bắt đúng chỗ này. Chốt **1**.
2. **Tiêu chí 2 (đồng thuận 1).** Tôi tự tính lại toàn bộ: 6/6 ma trận có ≥1 ô sai; 14/16 ô candidate lệch (M1 Python 132/134, Go 82/83, TS 108/109; M2 Orchestrator 87/83; M3 Postgres 47/49, Redis 40/43; M5 none-applicable 70/60, Qdrant 61/62, pgvector 57/56; M6 SSE 91/94, WS 56/55; M7 90/95, 62/68, 40/41). Winner mỗi bảng KHÔNG đổi → không tới mức "đổi thứ hạng candidate" (level-0). Đúng level-1. Giữ **1**, không nâng 2 (số sai quá nhiều), không hạ 0 (không đổi kết luận).
3. **Tiêu chí 5 (1 vs 2 vs 2).** Phân xử ở bảng: charge jargon của ky-thuat kiểm được là thật, không chứng minh sai được → lấy thấp = **1**.
4. **Chi tiết đáng lưu cho GĐ8 — M5 "none" là ranking-flip cục bộ:** ô "none" §142 ghi TỔNG=70* nhưng cộng chỉ 3 tiêu chí áp-dụng-được (5×5+5×4+5×3) = 60, mà Qdrant tính lại = 62 → trên "tiêu chí áp dụng được" none THUA Qdrant. Footnote tự tuyên "none thắng trên tiêu chí áp dụng được" là SAI về số. Quyết định NONE-cho-MVP vẫn đúng nhưng do ràng buộc GĐ6/YAGNI, KHÔNG do điểm — cần bỏ tuyên "thắng bằng điểm". Đây là chỗ số bị thổi để đỡ lựa chọn; không rớt gate vì quyết định vẫn có neo ràng buộc, nhưng là lỗi số học tệ nhất trong 6 bảng.

---

## Nghi bịa / không nguồn — đã xác nhận

Gom nghi_bia của cả 3 lens, tự mở file/code kiểm lại từng cái:

1. **TỔNG ma trận sai số học ở 6/6 bảng (14/16 ô) — ĐỨNG VỮNG, nhưng KHÔNG phải "bịa nguồn" mà là cộng-sai/không-khớp-công-thức.** Tự tính lại bằng Σ(trọng số×điểm): Python 132→134, Go 82→83, TS 108→109, Orchestrator 87→83, Postgres 47→49, Redis 40→43, none-applicable 70→60, Qdrant 61→62, pgvector 57→56, SSE 91→94, WebSocket 56→55, pytest+Hyp 90→95, pytest-only 62→68, unittest 40→41. Kiểm thứ hạng: KHÔNG bảng nào đổi winner. → Hạ tiêu chí 2 xuống 1 và chạm tiêu chí 1 (số không khớp công thức đã tuyên), KHÔNG rớt gate.

2. **§5 Vector "none" TỔNG=70 không suy được từ ô hiển thị — ĐỨNG VỮNG.** Cộng các tiêu chí áp-dụng-được (domain 5×5 + deploy 5×4 + maint 5×3) = 60, không phải 70; và footnote "none thắng trên tiêu chí áp dụng được" SAI vì 60 < Qdrant 62. Con số bị thổi để đỡ lựa chọn; quyết định thực ra do ràng buộc GĐ6/YAGNI. Là lỗi số học nặng nhất, nhưng quyết định có neo ràng buộc nên không rớt gate.

3. **"gốc có 327 test" (§182, ADR-007) — KHÔNG còn là nghi bịa sau kiểm.** Mở evidence-C-roadmap.md:25: dòng E19 ghi nguyên văn "`tests/`,`tests_audit/` (327 tests)". Artifact trích ĐÚNG anchor evidence-C:25 → theo rubric tiêu chí 1 (cho phép neo về evidence file:line), đây là claim có nguồn hợp lệ, KHÔNG trừ. Lưu ý cho GĐ8: repo hex_agent thực có ~7061 (đếm mọi thư mục) / ~1041 (tính hẹp qua tests/+tests_audit/) `def test_` — số 327 trong evidence đã lỗi thời so với hiện trạng code; GĐ8 nên dùng con số thật khi đo, nhưng lỗi này thuộc evidence GĐ0, không phải bịa của 07-stack.

4. **Dấu ✔ ở cổng §10 + "GATE: GO" là AI tự cấp (vai CTO tự-quyết) — ĐÚNG là không tính làm bằng chứng, nhưng KHÔNG che lỗ hổng.** Kiểm nội dung 4 tick: (1) 6 ma trận + 1 dòng ràng-buộc-ép — có thật trong §1-7; (2) 7 ADR có phương án đã loại — có thật §8; (3) SPIKE-1 time-box + NFR open-Q — có thật §7b; (4) mọi lựa chọn trong ràng buộc GĐ6 — kiểm §0 nối mạch đúng. Tick tự-cấp nhưng nội dung bên dưới truy vết được → không giấu lỗ hổng nội dung.

5. **Claim về code gốc — ĐÃ KIỂM TRỰC TIẾP TRÊN hex_agent, ĐÚNG HẾT (củng cố tiêu chí 1 không rớt 0):** `pyproject.toml:5` requires-python ">=3.11"; `orchestrator/checkpoint.py:13` `from langgraph.checkpoint.sqlite import SqliteSaver`, dòng 32 `langgraph.sqlite`, dòng 139 nguyên văn "Read the UI projection. Resume intentionally does not call this function."; `rag/stores_qdrant.py:29` `uuid.uuid5(...)` deterministic ids; `llm/adapter.py:1` "OpenAI-compatible LLM adapter — JSON-mode, lazy client, retry/backoff…"; `ui/server.py:472` `/api/stream` + dòng 524 `Content-Type: text/event-stream`. Không claim code gốc nào sai → tiêu chí 1 không có căn cứ rớt 0.

**Kết:** sau kiểm, nghi bịa thực sự đứng vững = (1) và (2) — đều là lỗi SỐ HỌC/không-khớp-công-thức, không phải bịa nguồn hay bịa kết quả spike. "327 test" và các claim code gốc đã được minh oan. Gate ĐẠT.
