# TUNE — skill `shape` (từ chấm 06-shape trong gói rebuild-hex-agent)

Nguồn: grade `grades/06-shape.grade.md` · rubric `rubrics/06-shape.rubric.md` · SKILL `.claude/skills/shape/SKILL.md` · artifact `rebuild-hex-agent/pipeline/06-shape.md`.

---

## §0 Chẩn đoán (≤6 câu)

Bản shape ăn 14/16 nhưng **RỚT GATE** vì đúng một tiêu chí xương sống: **#1 BÁM NGUỒN = 0**, do một claim-code SAI — chuỗi middleware "cố định" `Timing→Policy→Budget→Retry→Condense→core` chèn BudgetGuard vào chuỗi kernel, trong khi `core/bootstrap.py:29-33` wire đúng `timing→policy→retry→condense` và ghi thẳng "BudgetGuard is intentionally NOT wired here" (guard per-run, ngoài chuỗi kernel). Bảy tiêu chí còn lại đều 2 — thân bài rất chắc, chỉ chết ở một mắt xích code.
Lỗi này là **lỗi-của-SKILL (thiếu luật)**, không phải agent chạy ẩu: luật "Bám nguồn" (dòng 28) và bước "Tự soi" (dòng 127-133) chỉ bắt truy vết boundary→bounded-context GĐ5 và NFR→PRD; **không có câu nào bắt kiểm-lại một claim CƠ-CHẾ-CODE với `hex_agent` khi chạy brownfield/rebuild** — nên artifact viết một thứ-tự chain "như đọc từ code" mà không ai buộc mở file đối chiếu.
Nặng thêm vì cổng 4-điều (dòng 139-143) cũng không có điều nào soi claim-code, nên artifact tự cấp "✔" và tuyên GO trên một claim sai; và claim này **load-bearing** — nó đi vào ràng buộc bàn giao (dòng 372) → GĐ7 sẽ mang một thứ-tự-chain không tồn tại làm điều kiện hiện thực. Kết: tune được, và đáng, vì một luật nhỏ (verify code-claim ở brownfield) sẽ bịt đúng lỗ làm rớt gate.

---

## §1 Fixture đề xuất (cố định cả thí nghiệm)

- **skill**: `shape` (GĐ6).
- **project / input**: gói **rebuild-hex-agent**, chạy shape bằng Domain Model GĐ5 `rebuild-hex-agent/pipeline/05-idea-domain.md` (+ anchor `00-understanding/REBUILD-BRIEF.md`, `ATLAS.md`, `evidence-A/B/C`). Đây là chế độ **brownfield/rebuild có code gốc** — đúng bối cảnh làm lộ lỗi.
- **code gốc để đối chiếu** (nguồn chân lý cho claim-code): `/Users/uspro/Desktop/namnson/hex_agent` — cụ thể `core/bootstrap.py`, `core/kernel.py`, `middleware/__init__.py`.
- **mode/level**: chế độ tự-quyết (đóng vai Kiến trúc sư/CTO, không hỏi user) — giữ y như lần chạy gốc để một-biến-duy-nhất.
- **tham số cố định**: cùng 6 bounded context + 5 rule bất biến + 6 domain event của GĐ5; cùng yêu cầu output 7 khối (Brief + C4 Context + Container + Data Flow + Integration + Security + ADRs).
- Ghi 3 hằng số (project=rebuild-hex-agent, code-anchor=hex_agent, mode=tự-quyết) ra `fixture.txt` của lượt; mọi variant đọc đúng file này, không ai đổi giữa chừng.

---

## §2 Thước

- Dùng nguyên **`rubrics/06-shape.rubric.md`** (8 tiêu chí 0/1/2; xương sống = #1 BÁM NGUỒN, #2 ĐỦ BỘ ARTIFACT, #3 ĐÚNG VAI GĐ6).
- Luật xếp hạng: **loại hết bản RỚT GATE trước** (bất kỳ tiêu chí xương sống = 0 → loại, dù tổng cao), rồi mới **xếp theo Tổng/16**; hoà Tổng thì bản có **diff NHỎ/robust hơn** thắng (ít rủi ro over-fit).
- Chấm mù: người chấm chỉ thấy {project, mode, output}, KHÔNG thấy variant theo hướng nào.

---

## §3 Các hướng thử (A/B/C/D — mỗi hướng nhắm MỘT tiêu chí khác nhau)

> Tất cả là DIFF trích-đoạn vào `.claude/skills/shape/SKILL.md` — sửa tối thiểu đủ thử, không viết lại file.

### Hướng A — Luật "verify claim-code ở brownfield" (nhắm tiêu chí #1 BÁM NGUỒN) ← lỗi làm rớt gate
**Giả thuyết:** thêm một luật cứng bắt MỌI claim về cơ-chế/tên/thứ-tự trong code gốc phải mở file đối chiếu và ghi địa chỉ nguồn (`path:line`), thì claim middleware-chain sai bị bắt trước gate → #1 lên 2.
**DIFF** — thêm vào mục "## Luật cứng", ngay sau bullet "Bám nguồn" (dòng 28):
```
- **Verify claim-code (brownfield/rebuild).** Khi artifact khẳng định một CƠ-CHẾ / TÊN / THỨ-TỰ có trong code gốc (vd "chuỗi middleware cố định X→Y→Z", "kernel giữ state", "gọi trực tiếp"), PHẢI mở đúng file nguồn đối chiếu và gắn địa chỉ `path:line` NGAY CẠNH claim. Chưa mở được file → viết "chưa kiểm" / open-Q, KHÔNG viết như sự thật. Một claim-code sai = rớt tiêu chí Bám nguồn, dù mọi thứ khác đúng.
```
**Rủi ro:** artifact có thể phình ghi chú `path:line` ở mọi câu → giảm điểm #4 (đọc-được-3-tầng) nếu nhét địa chỉ code vào phần Góc nhìn lãnh đạo; phải giới hạn địa chỉ nguồn ở phần chi-tiết-dev.

### Hướng B — Cổng có điều "soi claim-code" (nhắm tiêu chí #8 CỔNG & BÀN GIAO, chặn self-grant "✔")
**Giả thuyết:** thêm điều thứ 5 vào cổng 4-điều — "mọi claim-code trong artifact đã đối chiếu file gốc" — thì gate không thể tuyên GO khi còn claim-code chưa kiểm; cổng thành lưới bắt thứ mà #1 lọt.
**DIFF** — trong mục "## Cổng go/no-go + AI duyệt", thêm điều 5 (sau dòng 143):
```
5. Mọi claim về code gốc (cơ chế/tên/thứ-tự/known-gap) đã đối chiếu file nguồn và gắn `path:line`; không claim-code nào "viết như đã đọc" mà chưa mở file. Còn một claim chưa kiểm → no-go.
```
Và sửa khối cổng mẫu (dòng 148-154) thêm một dòng: `Claim-code: đã đối chiếu file gốc (path:line) · <n> claim, 0 chưa kiểm.`
**Rủi ro:** cổng dài thêm một điều nhưng không tự BẮT lỗi nếu agent vẫn tick "✔" hình thức — B chỉ mạnh khi đi kèm A (A tạo dữ liệu `path:line`, B kiểm sự có mặt). Thử B đơn lẻ để đo cổng-một-mình có đủ không.

### Hướng C — Sửa "Tự soi" thành có bằng chứng, cấm tick trần (nhắm tiêu chí #1 qua đường tự-kiểm)
**Giả thuyết:** bước "Tự soi trước khi chốt" hiện cho phép trả lời "CÓ/KHÔNG" trần (artifact gốc tick "— CÓ", "— KHÔNG"); nếu bắt mỗi câu tự-soi phải kèm 1 bằng chứng truy được, agent buộc phải mở file khi khẳng định code → bắt lỗi chain sớm.
**DIFF** — thêm một câu vào đầu mục "## Tự soi trước khi chốt (bắt buộc)" (dòng 127-128):
```
Mỗi câu trả lời PHẢI kèm bằng chứng truy được (đường dẫn GĐ5 / PRD / `path:line` code gốc), KHÔNG tick "CÓ/KHÔNG" trần. Câu nào không dẫn được bằng chứng = coi như CHƯA ĐẠT, sửa trước khi ra cổng.
```
Và thêm một câu tự-soi #5: `5. **Mọi claim-code đã mở file đối chiếu chưa?** Không có claim cơ-chế/thứ-tự nào viết theo trí nhớ.`
**Rủi ro:** trùng mục tiêu với A (cùng nhắm #1) — nếu cả A và C cùng thắng thì tốn một agent; giữ C như biến thể "sửa chỗ tự-soi thay vì thêm luật cứng" để so cách đặt luật nào robust hơn, KHÔNG chạy C nếu đã quá tải agent.

### Hướng D — Nhãn "hiện trạng-code vs quyết-định" cho claim brownfield (nhắm tiêu chí #3 ĐÚNG VAI GĐ6)
**Giả thuyết:** lỗi chain một phần vì artifact trộn "mô tả hiện trạng code gốc" với "quyết định kiến trúc" — bắt tách bạch hai loại (claim mô-tả-hiện-trạng phải gắn nhãn + nguồn; claim quyết-định là của shape) giúp lộ ngay chỗ nào là "đọc từ code" cần kiểm.
**DIFF** — thêm vào mục "## Luật cứng" một bullet:
```
- **Tách "hiện trạng code cũ" khỏi "quyết định của shape".** Ở brownfield, mọi câu MÔ TẢ code hiện có phải gắn nhãn `[hiện trạng: path:line]`; mọi câu là QUYẾT ĐỊNH kiến trúc mới của GĐ6 để trần. Không trộn hai loại trong một câu (vd "chuỗi cố định X→Y→Z" — là mô tả code thì phải có nguồn, là quyết định thì phải nói rõ đang CHỐT lại).
```
**Rủi ro:** nhắm #3 nhưng lỗi gốc thực chất ở #1 (claim SAI, không phải lẫn-vai) — D có thể cải thiện độ rõ mà vẫn để lọt claim sai nếu agent gắn nhãn `[hiện trạng]` cho một thứ tự vẫn bịa; D yếu hơn A/B về đúng-lỗi, giữ để kiểm giả thuyết "lỗi là do lẫn mô-tả/quyết-định" có đúng không.

**Không trùng tiêu chí:** A→#1 (thêm luật), B→#8 (cổng lọc), C→#1 (đường tự-soi — biến thể của A, chỉ chạy nếu còn agent), D→#3 (tách nhãn hiện-trạng). Nếu chỉ chạy 3 agent: **A, B, D** (ba tiêu chí khác nhau); C là dự bị.

---

## §4 Ưu tiên

**TUNE NGAY.** Lý do: đây là lỗi làm **RỚT GATE** (tiêu chí xương sống #1 = 0) chứ không phải mất điểm lặt vặt, và nó **load-bearing** — claim sai chảy vào ràng buộc bàn giao GĐ7. Lỗi thuộc **SKILL (thiếu luật verify code-claim ở brownfield)**, đúng loại tune sửa được; bảy tiêu chí còn lại đã 2 nên một luật nhỏ, đúng chỗ, có thể nâng thẳng từ RỚT GATE lên 16/16 mà không phải viết lại skill.

---

## §5 Nhắc luật thí nghiệm

- **Chấm mù:** đưa người/agent chấm chỉ {project=rebuild-hex-agent, mode=tự-quyết, output.md}, KHÔNG lộ variant theo hướng nào — tránh thiên vị hướng A vì "đúng lỗi đã biết".
- **Baseline trước:** chấm lại artifact gốc `pipeline/06-shape.md` bằng rubric = mốc 14/16-rớt-gate; mọi variant phải **qua gate + ≥ mốc** mới tính là tiến.
- **Confirm bản thắng bằng agent MỚI + fixture thứ hai:** chạy `proposed-SKILL.md` của bản thắng bằng agent chưa từng thấy lỗi này trên (a) đúng fixture rebuild-hex-agent, và (b) **một shape brownfield thứ hai có code gốc khác** (để chắc luật verify-code-claim không chỉ khớp riêng vụ middleware-chain). Chỉ hơn ở fixture gốc → có mùi over-fit, xem lại diff.
- **Một biến duy nhất:** mọi variant cùng GĐ5-input, cùng code-anchor `hex_agent`, cùng mode tự-quyết — chỉ khác ở diff SKILL.
