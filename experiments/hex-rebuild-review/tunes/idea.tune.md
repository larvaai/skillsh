# Tune — skill `idea` (fixture: rebuild-hex-agent · artifact 05-idea-domain.md)

## §0 Chẩn đoán (≤6 câu)

Artifact được 14/16 nhưng **RỚT GATE ở tiêu chí 1 (BẰNG CHỨNG, xương sống)**: hằng số "15 SECRET_KEYS" (line 101) sai so code gốc (`control/redaction.py:16-33` có đúng 14), và ≥4 line-anchor trỏ lệch construct (`accept.py:52-128` cho `accept_decomposition` thực ở :186; `session.py:49-85` cho `SessionIdentity` thực ở :16-23; `state.py:35-37` cho `all_accepted()` thực ở :107-108; "327 tests" không khớp thực đếm). Cả 7 tiêu chí còn lại đều 2 — router, chuỗi GĐ0–5, domain 5 mắt xích, dừng đúng vai, đúng tầng, audit-được đều đạt trần. Điểm mấu chốt: các con số/anchor này được **kế thừa trung thực từ upstream** (`ATLAS.md`, `evidence-B/C`) — artifact không tự bịa, nó chép lại số sai của nguồn trung gian mà không đối chiếu lại code gốc. `SKILL.md` hiện tại KHÔNG có luật nào buộc verify hằng-số/anchor code trước khi neo (mục "Nguồn playbook" và `.ai-understanding/` chỉ nói ĐỌC để tránh mâu thuẫn tên, không nói KIỂM số). Đây là **lỗi-của-SKILL (thiếu luật)**, không phải agent chạy ẩu — mọi tiêu chí khác đã hoàn hảo, nên đúng một luật "verify claim code" là đòn bẩy; phần còn lại của grade thuộc chất lượng nguồn, không tune được ở `idea`.

## §1 Fixture đề xuất (cố định cả thí nghiệm)

- **project**: `rebuild-hex-agent`, đối chiếu code gốc tại `/Users/uspro/Desktop/namnson/hex_agent`.
- **input/ý tưởng**: "Rebuild sạch `hex_agent` — vòng lặp tự-điều-phối task (accept → plan → order → delegate → finish có biên)"; slug `hex-agent-rebuild`.
- **Router (cố định)**: độ rõ = **rõ ràng**, độ khả thi = **khả thi rõ** → **Nhánh C**, đi hết GĐ0→GĐ5, dừng ở Domain. (Chốt sẵn để loại biến router; mọi variant chạy đúng Nhánh C này.)
- **nguồn upstream cấp cho agent**: `00-understanding/REBUILD-BRIEF.md` + `evidence-A/-B/-C` + `ATLAS.md` — **cố tình giữ nguyên các con số sai của upstream** (15 SECRET_KEYS, 327 tests, các anchor lệch) để thử xem luật mới có bắt agent tự đối chiếu code gốc và sửa/hedge không.
- **chế độ tự-quyết**: người viết đóng vai Product/CTO tự chốt cổng GO (như artifact gốc), không hỏi user — giữ giống lần chạy đã chấm để so được.
- **output cần**: một artifact 05-idea-domain.md hoàn chỉnh GĐ0–5 + bàn giao.

## §2 Thước

- Rubric: `/Users/uspro/Desktop/skillsh/experiments/hex-rebuild-review/rubrics/05-idea.rubric.md` (8 tiêu chí 0/1/2, tối đa 16; xương sống = 1,5,6).
- **Luật xếp hạng**: loại hết bản **rớt gate** (bất kỳ tiêu chí 1/5/6 = 0) TRƯỚC; các bản còn sống mới xếp theo TỔNG; hoà tổng → bản có diff NHỎ/robust hơn thắng (ít rủi ro over-fit). Baseline hiện tại = 14/16 nhưng **rớt gate ở tiêu chí 1** → variant nào cứu được tiêu chí 1 lên ≥1 (thoát gate) đã thắng baseline bất kể tổng.

## §3 Các hướng thử (mỗi hướng nhắm ĐÚNG MỘT tiêu chí khác nhau)

### Hướng A — Luật "verify code-claim trước khi neo" (nhắm tiêu chí 1 · BẰNG CHỨNG) ⟵ đòn bẩy chính

**Giả thuyết**: buộc agent tự đối chiếu MỌI hằng số/anchor về code gốc (không tin nguồn trung gian) sẽ bắt được "15→14 SECRET_KEYS" và các anchor lệch → tiêu chí 1 thoát gate.

**DIFF** — thêm vào mục "Quy tắc bắt buộc" (sau dòng "Mỗi quyết định lớn ghi lý do + phương án đã loại"):
```
- **Verify trước khi neo (claim về code).** Mọi hằng số, tên hàm/hàng số, file:line trích từ atlas/evidence/brief PHẢI mở code gốc kiểm lại trước khi đưa vào artifact — nguồn trung gian có thể đếm sai/trỏ lệch. Kiểm được & khớp → neo `file:line`. Không kiểm được (không có code, chỉ có docs) → gắn nhãn "theo <nguồn>, CHƯA đối chiếu code" và đưa thành open-Q. Cấm chép số/anchor từ nguồn trung gian như số thật mà chưa mở code.
```

**Rủi ro**: agent có thể "verify" hình thức (tuyên bố đã kiểm mà không thật mở file) — chính lỗi thi-cong-lens đã mắc; cần chấm mù bắt kỹ. Cũng có thể làm artifact dài thêm vì nhiều nhãn hedge.

### Hướng B — Nhãn nguồn phân tầng (nhắm tiêu chí 1 · BẰNG CHỨNG, cơ chế khác A)

**Giả thuyết**: thay vì buộc verify (tốn công), buộc **phân tầng độ tin của mỗi số** (đã-kiểm-code / theo-docs-chưa-kiểm / ước-lượng) sẽ khiến số sai kế thừa lộ ra dưới nhãn "chưa kiểm" thay vì trôi qua như số thật → tránh mức-0.

**DIFF** — thêm vào GĐ1 mục "Đủ-là-đủ" và NFR (một dòng luật chung, đặt cuối "Quy tắc bắt buộc"):
```
- **Mỗi con số một nhãn nguồn.** Trước mỗi số (NFR, budget, metric, hằng số code) ghi rõ 1 trong 3: `[code:file:line]` (đã mở code khớp) · `[docs:<nguồn>, chưa đối chiếu]` · `[ước lượng thô]`. Số không gắn được nhãn nào → không đưa vào artifact.
```

**Rủi ro**: nhãn "docs, chưa đối chiếu" vẫn cho số SAI lọt vào artifact (chỉ hedge, không sửa) — rubric mức-0 kích khi hằng số "sai so code gốc"; nếu grader coi số-sai-có-hedge vẫn là mức-0 thì B không cứu được gate. B nhẹ hơn A nhưng có thể không đủ để thoát gate.

### Hướng C — Checklist "đối chiếu code gốc" ở Bước 1 (nhắm tiêu chí 1 · BẰNG CHỨNG, đặt ở quy trình đọc)

**Giả thuyết**: đặt việc kiểm ngay ở **Bước 1 — Đọc trước khi hỏi** (trước khi viết) sẽ chống lỗi tận gốc hơn là một luật rải rác; agent lập sẵn "bảng số cần kiểm" rồi mới viết.

**DIFF** — sửa gạch đầu dòng `.ai-understanding/` trong "Bước 1 — Đọc trước khi hỏi":
```
- `.ai-understanding/` + code gốc (nếu brownfield) — đọc atlas/evidence để lấy domain/rule đã có. BẮT BUỘC: gom mọi hằng-số/anchor sẽ dùng thành một "bảng cần kiểm", mở code gốc đối chiếu từng cái TRƯỚC khi viết GĐ. Nguồn trung gian lệch code → dùng code làm chân lý, ghi 1 dòng "sửa X→Y theo <file:line>". Số chỉ có trong docs → nhãn "chưa đối chiếu" + open-Q.
```

**Rủi ro**: chỉ áp cho brownfield có `.ai-understanding/`; ý greenfield/không có code gốc không được bảo vệ (nhưng greenfield ít có claim-code nên rủi ro thấp). Trùng ĐÍCH tiêu chí với A/B — nếu chạy cả ba, đây là biến-thể-đặt-chỗ, giữ để so "luật ở quy tắc" vs "luật ở quy trình đọc" cái nào ăn hơn.

### Hướng D — Cấm số/anchor trong khối "đọc 60 giây" & tick tự-phong (nhắm tiêu chí 1, khía cạnh tự-khen)

**Giả thuyết**: một phần điểm-trừ tiêu chí 1 đến từ số/tick trưng ở "Góc nhìn lãnh đạo" và GĐ0 ("327 tests, E01–E10 ✓, E19 ✓") — dấu ✓ tự-phong không phải log chạy. Cấm đưa số cứng + tick "đã pass" vào khối tóm tắt/intake, đẩy xuống bảng NFR có nhãn nguồn, sẽ giảm bề mặt số-sai chưa-kiểm.

**DIFF** — thêm một dòng vào GĐ1/GĐ0 (đặt trong "Quy tắc bắt buộc" hoặc mô tả GĐ0):
```
- **Khối tóm tắt lãnh đạo & Idea Intake không mang số kỹ thuật/tick pass.** Con số đo-được và trạng thái "đã pass/✓" chỉ xuất hiện ở GĐ1 metric hoặc bảng NFR, kèm nhãn nguồn. Cấm dấu ✓ tự-phong (không phải log chạy độc lập) ở mọi khối.
```

**Rủi ro**: nhắm phần hẹp của tiêu chí 1 (tick tự-phong), có thể KHÔNG chạm được lỗi lõi "15 SECRET_KEYS" nằm ở bảng NFR — nếu vậy D một mình không thoát gate; giá trị chính là bổ trợ cho A/C, không đứng một mình.

> Ghi chú phủ đè: **A, B, C, D đều nhắm tiêu chí 1** — đây là ngoại lệ có chủ đích vì baseline chỉ mất điểm duy nhất ở tiêu chí 1 (7 tiêu chí kia đã 2/2, không còn gì để tune). Bốn hướng khác nhau ở CƠ CHẾ (verify-bắt-buộc / nhãn-phân-tầng / checklist-ở-bước-đọc / cấm-số-ở-khối-tóm-tắt) chứ không trùng cách. Nếu chỉ chạy 3 agent: lấy **A, B, C** (bỏ D vì hẹp nhất); D chỉ đáng khi muốn tách riêng lỗi tick-tự-phong.

## §4 Ưu tiên

**Để sau (đáng tune nhưng không gấp).** Lý do: (1) lỗi là lỗi-của-SKILL thật (thiếu luật verify claim-code) nên tune CÓ tác dụng — không phải "grade cao + lỗi-lần-chạy → bỏ"; (2) nhưng gốc rễ con số sai nằm ở **upstream atlas/evidence** ("15 SECRET_KEYS" lan từ `ATLAS.md`/`evidence-B`), nên sửa nguồn (một lần) chặn lỗi cho MỌI skill hạ nguồn hiệu quả hơn thêm luật vào riêng `idea`; ưu tiên fix upstream trước, rồi tune `idea` để có lớp verify độc lập (defense-in-depth). Nếu buộc chọn tune ngay một hướng: chạy A.

## §5 Nhắc luật thí nghiệm (bắt buộc khi chạy)

- **Chấm mù**: grader chỉ thấy {project=rebuild-hex-agent, Nhánh C, output.md}, KHÔNG thấy variant theo hướng nào. Đặc biệt với tiêu chí 1: grader phải **tự mở code gốc** (`len(SECRET_KEYS)`, `accept.py`, `session.py`, `state.py`) kiểm lại — KHÔNG tin lời agent tuyên bố "đã verify" (thi-cong-lens từng chấm 2 vì tin lời "15 đếm đúng" mà không thật đếm).
- **Baseline trước**: chốt baseline = artifact 05-idea-domain.md hiện tại = 14/16, **rớt gate tiêu chí 1**. Mọi variant so với mốc này; thoát gate (tiêu chí 1 ≥ 1) là điều kiện cần để coi là "thắng".
- **Confirm bằng agent MỚI + fixture thứ hai**: bản thắng chạy lại bằng agent mới trên (a) đúng fixture hex-agent-rebuild, và (b) **một ý greenfield/brownfield khác có claim-code** (vd một artifact idea trên codebase khác, hoặc case Case-Management trong ví dụ mẫu). Chỉ hơn baseline ở fixture gốc → nghi over-fit (luật verify chỉ hợp cảnh hex_agent); hơn ở cả hai → luật thật, đáng merge vào `idea/SKILL.md`.
