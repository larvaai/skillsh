# TUNE — skill `modules` (từ chấm artifact 10-modules.md, gói rebuild-hex-agent)

> Chạy đúng quy trình `tune/SKILL.md`: fixture cố định · MỘT biến duy nhất (bản sửa SKILL) · baseline trước · chấm mù bằng rubric · confirm agent mới + fixture thứ hai chống over-fit. File này CHỈ chuẩn bị thí nghiệm; chưa chạy variant nào.

## §0 — Chẩn đoán (≤6 câu)

1. Artifact được 11/14, GATE ĐẠT (3 xương sống: BÁM NGUỒN=1, SỞ HỮU SẠCH=2, DÙNG ĐƯỢC THẬT=2); mất điểm ở criterion 1 (BÁM NGUỒN, do 1 tick tự-khen over-claim), criterion 6 (PHỦ FEATURE, E19 mồ côi + E15–E18 gộp ngầm), criterion 7 (ĐÚNG VAI + CỔNG, bằng chứng cổng #3 dựa trên over-claim).
2. Lỗi criterion 6 GỐC là RUN: agent bỏ sót hàng E19 Test Harness (có thật ở evidence-C dòng 25, ✓ 327 tests) và nuốt ngầm việc E21 "gathers E15/E16/E17/E18" (evidence-C dòng 6, 24) khi liệt kê bảng kiểm chéo — không phải SKILL thiếu luật kiểm chéo.
3. NHƯNG chỗ khuếch đại lỗi thành criterion 1 + 7 là LỖI-CỦA-SKILL: `modules/SKILL.md` §Tự soi + §Cổng bảo writer "trình bằng chứng" và tick ✔ nhưng KHÔNG cấm tick tự-khen không-trỏ-được-hàng, và KHÔNG buộc liệt kê cạn danh sách epic/feature nguồn trước khi tuyên "map hết" → writer viết "Epic E01–E21 map hết" (dòng 308, 325) trong khi E19 vắng.
4. Claim "pipeline/09-*.md không tồn tại" (dòng 9) là LỖI-THỜI thuần RUN (10-modules viết 02:30, 09-backlog sinh 02:32) — KHÔNG tune được, và luật SKILL hiện tại ("không có gì → mới gợi ý /backlog") vốn đúng.
5. Kết: phần lớn điểm-rớt criterion 6 là run-ẩu; nhưng có ĐÚNG MỘT lỗ SKILL thật, tái lặp được (không có anti-self-praise + không có "enumerate-rồi-mới-tick"), và nó chính là mắt xích kéo tụt cả criterion 1 lẫn 7 → đáng tune một vòng nhẹ.
6. Các tiêu chí 2/3/4/5 đều 2 điểm và không có tín hiệu lỗi SKILL → không đụng.

## §1 — Fixture đề xuất (cố định cả thí nghiệm — lặp lại được)

- **project**: `hex_agent` clean-rebuild — nguồn tại gói `/Users/uspro/Desktop/skillsh/rebuild-hex-agent/`.
- **Đầu vào skill nhận (đúng như lần chạy gốc, KHÔNG đổi):**
  - Domain Model GĐ5: `rebuild-hex-agent/pipeline/05-idea-domain.md` (6 bounded context, 6 domain event §5.4, data ownership §5.5, 5 rule bất biến).
  - Architecture Brief GĐ6: `rebuild-hex-agent/pipeline/06-shape.md` (6 module = 6 context 1–1, 6 ADR, 2 chokepoint).
  - Roadmap epic NGOÀI pipeline (chưa qua cổng GĐ9): `00-understanding/REBUILD-BRIEF.md` §Roadmap + `00-understanding/evidence-C-roadmap.md` (epic E01–E21, gồm E19 Test Harness ✓ và E15–E18 merged→E21).
- **Ràng buộc fixture để cô lập biến:** cố tình GIỮ nguyên tình huống "chưa có backlog GĐ9 trong prompt" (nguồn ngoài = epic) — vì criterion 6 chỉ thật sự bị thử khi feature vào bằng epic thô. Nếu đưa backlog GĐ9 vào thì lỗi E19/E15–E18 biến mất và ta không đo được hướng sửa. (Bỏ qua sự thật 09-backlog.md đã sinh sau — đó là lỗi-thời của lần chạy, không thuộc biến đang thử.)
- **level**: đọc từ `user-state.json` nếu có; không có → L4 (CTO/eng-manager đọc), ghi rõ.
- **tham số chấm**: mỗi variant sinh ĐÚNG hai artifact (Module Map + 6 Module Contract) trên cùng đầu vào trên, cùng độ dài ~1 trang lãnh đạo + chi tiết dev.
- Ghi 3 hằng số (project · đầu-vào-list · level) ra `experiments/runs/<ts>/fixture.txt`; mọi variant đọc đúng file này.

## §2 — Thước

- Rubric: `/Users/uspro/Desktop/skillsh/experiments/hex-rebuild-review/rubrics/10-modules.rubric.md` (7 tiêu chí 0/1/2; xương sống = 1 BÁM NGUỒN, 2 SỞ HỮU SẠCH, 3 DÙNG ĐƯỢC THẬT).
- Luật xếp hạng: **loại hết bản rớt gate trước** (bất kỳ tiêu chí 1/2/3 = 0 → loại dù tổng cao), **rồi mới xếp theo tổng**; hoà tổng → bản có **diff nhỏ/robust hơn** thắng (ít rủi ro over-fit vào đúng fixture này).
- Chấm mù: người chấm chỉ thấy {project, đầu-vào, level, output}, KHÔNG thấy variant theo hướng nào.

## §3 — Các hướng thử (A/B/C/D — mỗi hướng nhắm ĐÚNG một tiêu chí khác)

> Mỗi diff là trích-đoạn thêm/sửa TỐI THIỂU vào `modules/SKILL.md`, đủ để thử — KHÔNG viết lại file.

### Hướng A — Anti-self-praise tick (nhắm criterion 1 BÁM NGUỒN)
- **Giả thuyết:** nếu cấm tick ✔ tự-khen không-trỏ-được-bằng-chứng và buộc mỗi ✔ ở Tự-soi/Cổng phải kèm con-trỏ (dòng/hàng bảng), writer sẽ không viết "E01–E21 map hết" khi E19 vắng → criterion 1 lên 2.
- **DIFF** — thêm 1 gạch đầu dòng vào §"Luật cứng" (sau dòng "Mỗi quyết định lớn ghi LÝ DO..."):
  ```
  - **Mỗi dấu ✔ / mỗi câu "đầy đủ/sạch/map hết" ở Tự-soi và Cổng phải TRỎ được tới bằng chứng cụ thể trong chính artifact** (số hàng bảng / tên module / dòng). Không trỏ được thì KHÔNG tick — viết thành open-Q hoặc "còn X chưa map". Tick tự-khen suông = claim bịa, làm hỏng cả cổng.
  ```
- **Rủi ro:** writer có thể trở nên rụt rè, hạ mọi ✔ xuống open-Q kể cả khi đủ bằng chứng → cổng loãng, criterion 7 tụt nhẹ. Theo dõi criterion 7 khi chấm.

### Hướng B — Enumerate-rồi-mới-tick coverage (nhắm criterion 6 PHỦ FEATURE)
- **Giả thuyết:** nếu buộc bảng kiểm chéo liệt kê CẠN từng epic/feature/story nguồn (một hàng cho MỖI mục, kể cả mục cross-cutting như test harness, và ghi rõ mục nào merge/park), sẽ không còn mục mồ côi/gộp-ngầm → criterion 6 lên 2.
- **DIFF** — thay câu kiểm-chéo ở §"Artifact 1 — Module Map" (dòng "Kiểm chéo backlog: mọi feature GĐ9 rơi vào đúng một module — không feature mồ côi, không feature thuộc hai module."):
  ```
  Kiểm chéo backlog: LIỆT KÊ CẠN từng epic/feature/story nguồn — mỗi mục MỘT hàng, kể cả mục cross-cutting (test harness, governance) và mục "gathered/merged vào mục khác". Mỗi hàng ghi: rơi vào module nào, HOẶC nhãn rõ [park / merged→X / YAGNI + khi nào cấp lại]. Không mục nào được biến mất khỏi bảng: mồ côi = rớt criterion. Chỉ được tuyên "map hết" sau khi số hàng = số mục nguồn.
  ```
- **Rủi ro:** với backlog lớn, "một hàng mỗi story" phình bảng rất dài, đụng luật 1-trang → phải cho phép gộp story cùng epic nhưng vẫn giữ mọi epic + mọi cross-cutting item. Chấm cân giữa "cạn" và "scan 2–3 phút".

### Hướng C — Cổng: bằng chứng phải trỏ hàng, không suy từ tick (nhắm criterion 7 ĐÚNG VAI + CỔNG)
- **Giả thuyết:** nếu 4 bằng chứng cổng buộc trỏ THẲNG vào nội dung artifact (không dùng lại tick tự-khen của Tự-soi làm bằng chứng), bằng chứng #3 sẽ tự lộ E19 thiếu và writer sửa trước khi mở cổng → criterion 7 lên 2.
- **DIFF** — thêm 1 câu vào §"Cổng go/no-go", ngay sau "TRÌNH BẰNG CHỨNG (mỗi module đúng một owner; ...; mọi phụ thuộc đi qua contract)":
  ```
  Mỗi trong 4 bằng chứng phải TRỎ vào một mục cụ thể của artifact vừa dựng (số hàng bảng kiểm chéo, tên contract), KHÔNG được viện dẫn lại dấu ✔ ở Tự-soi. Bằng chứng "không feature mồ côi" chỉ hợp lệ khi bảng kiểm chéo đã liệt kê cạn (số hàng = số mục nguồn); còn mục chưa map → cổng ghi "hụt bằng chứng #3", không GO cho tới khi vá.
  ```
- **Rủi ro:** chồng lấn với A và B (cùng động tới "tick phải trỏ bằng chứng"). Nếu chạy cả A+B+C thì C có thể không thêm delta đo được — giữ C để tách xem đòn bẩy nằm ở tầng Tự-soi (A) hay tầng Cổng (C).

### Hướng D — Chốt danh sách nguồn epic ở Đầu vào (nhắm criterion 6, cách khác B — phòng thủ đầu-vào thay vì đầu-ra)
- **Giả thuyết:** nếu §Đầu vào buộc writer TRÍCH nguyên danh sách epic/feature từ nguồn (dán ID + tên) vào một chỗ trước khi map, thì lúc map sẽ đối chiếu 1-1 và không rơi mục nào — sửa nguyên-nhân-gốc (bỏ sót khi đọc nguồn) thay vì triệu chứng (bảng thiếu hàng).
- **DIFF** — thêm 1 câu cuối §"Đầu vào — đọc trước khi vẽ":
  ```
  TRƯỚC khi map, TRÍCH nguyên danh sách mục nguồn (epic/feature ID + tên, kể cả mục ✓ cross-cutting và mục merged/park) ra một danh sách đối chiếu; map từng mục theo danh sách này. Số mục map + số mục park/merge (có nhãn) phải BẰNG tổng mục nguồn — lệch = còn sót, chưa được tuyên phủ hết.
  ```
- **Rủi ro:** trùng đích với B (cùng criterion 6). Chạy B và D song song để xem sửa ở đầu-ra (bảng) hay đầu-vào (danh sách trích) hiệu quả hơn; nếu D thắng thì gốc lỗi là "đọc nguồn ẩu", nếu B thắng thì gốc là "trình bày bảng ẩu". KHÔNG merge cả hai (thừa).

> Ghép chạy đề xuất: A (criterion 1) + (B **hoặc** D, không cả hai) (criterion 6) + C (criterion 7). A và C khác tầng (Tự-soi vs Cổng) nên không trùng; B/D là hai cách cho cùng criterion 6, chọn một để không phí agent.

## §4 — Ưu tiên

**ĐỂ SAU (tune nhẹ, một vòng ngắn).** Grade 11/14 và GATE đã ĐẠT; hai trong ba điểm-rớt (stale-09, và phần lớn E19/E15–E18) là lỗi-của-lần-chạy, không tune được. Chỉ có đúng một lỗ SKILL thật (thiếu anti-self-praise + thiếu enumerate-trước-khi-tick) đáng vá — nhưng vì nó kéo tụt cả 3 tiêu chí cùng lúc và rẻ để thử (4 diff nhỏ), nên xếp "để sau" chứ không "không đáng tune": làm khi có slot, không chặn việc khác.

## §5 — Nhắc luật thí nghiệm (bắt buộc khi chạy)

- **Baseline trước:** chạy `modules` HIỆN TẠI trên fixture §1 → `runs/<ts>/baseline/output.md`, chấm bằng rubric §2 → `baseline/grade.md`. Mọi variant phải hơn 11/14 mới đáng theo.
- **Một biến duy nhất:** mọi variant cùng fixture §1 (cùng project, cùng đầu-vào, cùng level, cùng nguồn-ngoài-epic). Chỉ khác đúng bản sửa SKILL. Đổi fixture giữa chừng → làm lại.
- **Chấm mù:** người/agent chấm chỉ thấy {project, đầu-vào, level, output}, không thấy hướng.
- **Confirm bản thắng bằng agent MỚI + fixture thứ hai:** lấy `proposed-SKILL.md` bản thắng, chạy agent mới trên (a) đúng fixture hex_agent, và (b) một project thứ hai KHÁC domain (vd một hệ có backlog GĐ9 thật + có mục cross-cutting kiểu test/governance để bẫy lại lỗi E19). Vẫn hơn baseline ở CẢ HAI → điểm đến từ SỬA, đáng merge; chỉ hơn ở fixture gốc → mùi over-fit, xem lại diff.
- **Không đụng `modules/SKILL.md` thật** cho tới khi có bản thắng đã qua confirm; mỗi variant nằm trong `experiments/runs/<ts>/<variant>/proposed-SKILL.md`.
