# TUNE — skill `frame` (từ chấm artifact slice-01-taskloop-happy-path.md, gói rebuild-hex-agent)

> Chạy đúng quy trình `tune/SKILL.md`: fixture cố định · MỘT biến duy nhất (bản sửa SKILL) · baseline trước · chấm mù bằng rubric · confirm agent mới + fixture thứ hai chống over-fit. File này CHỈ chuẩn bị thí nghiệm; chưa chạy variant nào.

## §0 — Chẩn đoán (≤6 câu)

1. Artifact được **14/16, GATE ĐẠT** (3 xương sống: MỘT SLICE=2, ACCEPTANCE=2, BÁM BẰNG CHỨNG=1 — không cái nào 0); mất điểm ở đúng **hai** tiêu chí: criterion 4 CONTRACT-TRƯỚC-CODE=1 và criterion 6 BÁM BẰNG CHỨNG=1 (xương sống).
2. Lỗi criterion 6 là **RUN, không phải SKILL**: anchor `safety/sandbox.py:38,97` sai (file gốc **56 dòng** → :97 không tồn tại — đã kiểm `wc -l`; :38 là docstring, jail thật ở `resolve_in_workspace` :46; và gán "PolicyGate fail-closed" cho file không chứa PolicyGate) — SKILL đã có luật "anchor `file:line`… chỉ đúng khi file tồn tại và đoạn code nói đúng điều được gán", agent chỉ chép ẩu một anchor trong ~15 anchor đúng-semantic còn lại.
3. Lỗi criterion 4 là **hỗn hợp nghiêng RUN**: Plan §4 bước 2 chèn `BudgetGuard` vào chuỗi middleware kernel, đúng cái `bootstrap.py:31` cố ý KHÔNG làm ("BudgetGuard is intentionally NOT wired here" — đã kiểm) VÀ tự mâu thuẫn với chính §0 non-goal + §4 bước 4 (budget enforce ở discipline/loop) — agent tự-nghịch trong cùng một artifact.
4. Điểm SKILL đáng chú ý: cả hai lỗi đều là **"claim/anchor sai code gốc" và "plan tự mâu thuẫn với constitution của chính nó"** — SKILL.md hiện KHÔNG có bước tự-soi buộc verify anchor tồn-tại/đúng-dòng, cũng KHÔNG có bước đối chiếu từng bước Plan ngược lại non_goals đã chốt; luật "Contract trước code" + rubric có nói, nhưng SKILL không cưỡng-hành một checklist bắt agent tự bắt hai lỗi này trước khi chốt cổng.
5. §7 "Tự soi trước khi chốt" của artifact TICK "5. Bám nguồn, không bịa? — CÓ" và "3. plan §4 không đụng non-goal nào — CÓ" trong khi hai lỗi trên còn nguyên → đây là tín hiệu SKILL: self-check hiện là câu hỏi Yes/No tường thuật, không buộc trỏ-bằng-chứng nên không bắt được lỗi.
6. Kết: **phần lớn điểm-rớt thuộc lần-chạy** (anchor ẩu, plan tự-nghịch — agent giỏi hơn sẽ không mắc); nhưng có đúng một lỗ SKILL thật, tái-lặp-được (self-check tường thuật không cưỡng-hành verify-anchor + reconcile-plan-vs-non_goals) khuếch đại lỗi-run thành mất điểm ở cả criterion 4 lẫn xương-sống 6 → đáng tune một vòng nhẹ.

## §1 — Fixture đề xuất (cố định cả thí nghiệm — lặp lại được)

- **project**: `hex_agent` clean-rebuild — nguồn tại gói `/Users/uspro/Desktop/skillsh/rebuild-hex-agent/`; code gốc đối chiếu anchor tại `/Users/uspro/Desktop/namnson/hex_agent`.
- **Đầu vào skill nhận (đúng như lần chạy gốc, KHÔNG đổi):**
  - Live Slice Report GĐ8: `rebuild-hex-agent/pipeline/08-skeleton.md` (slice `finish-by-evidence-tối-thiểu`, E2E 9+1 chặng).
  - Backlog GĐ9: `rebuild-hex-agent/pipeline/09-backlog.md` (Story ⭐ LÕI R3 + AC S3.2/3.3/3.4/3.5, F1.5).
  - Module Map/Contract GĐ10: `rebuild-hex-agent/pipeline/10-modules.md` (6 module · 2 seam công khai).
  - Delivery Standards/DoD GĐ11: `rebuild-hex-agent/pipeline/11-delivery.md` (layout `src/…`, D1–D5, test pyramid).
  - Anchor gốc: `00-understanding/REBUILD-BRIEF.md` (7 invariant) + `evidence-A/B/C` + code gốc `/Users/uspro/Desktop/namnson/hex_agent`.
- **Nhiệm vụ (giữ nguyên):** đóng khung ĐÚNG slice-01 = happy-path GĐ8 TRỪ resume + 1 guard, ra Scope/Boundary/Acceptance + Plan/Contract, KHÔNG viết code app.
- **Chế độ (giữ nguyên để cô lập biến):** **tự-quyết** (product owner "không hỏi approval") — vì hai lỗi bị thử (anchor sai + plan tự-nghịch) chỉ lộ khi agent tự chốt cổng mà không có user chặn; đổi sang chế-độ-thường-có-cổng-chờ sẽ che mất biến đang thử.
- **level**: đọc từ `user-state.json` nếu có; không có → L6 (dev/CTO nhận slice, đọc anchor được), ghi rõ.
- **tham số chấm**: mỗi variant sinh ĐÚNG một artifact frame slice-01 trên cùng đầu vào, cùng bố cục (GÓC-NHÌN-LÃNH-ĐẠO + CHI TIẾT KỸ THUẬT §0–§9).
- Ghi 3 hằng số (project · đầu-vào-list · level · chế-độ) ra `experiments/runs/<ts>/fixture.txt`; mọi variant đọc đúng file này — không ai đổi fixture giữa chừng.

## §2 — Thước

- Rubric: `/Users/uspro/Desktop/skillsh/experiments/hex-rebuild-review/rubrics/frame.rubric.md` (8 tiêu chí 0/1/2; xương sống = 1 MỘT SLICE, 3 ACCEPTANCE ĐO ĐƯỢC, 6 BÁM BẰNG CHỨNG).
- Luật xếp hạng: **loại hết bản rớt gate trước** (bất kỳ tiêu chí 1/3/6 = 0 → loại dù tổng cao), **rồi mới xếp theo tổng**; hoà tổng → bản có **diff nhỏ/robust hơn** thắng (sửa ít, ít rủi ro over-fit vào đúng fixture này).
- Chấm mù: người/agent chấm chỉ thấy {project, đầu-vào, level, chế-độ, output}, KHÔNG thấy variant theo hướng nào.
- Đối chiếu anchor phải mở code gốc `/Users/uspro/Desktop/namnson/hex_agent` (một `file:line` chỉ đúng khi file tồn tại VÀ đoạn code nói đúng điều được gán).

## §3 — Các hướng thử (A/B/C — mỗi hướng nhắm ĐÚNG một tiêu chí khác)

> Mỗi diff là trích-đoạn thêm/sửa TỐI THIỂU vào `frame/SKILL.md`, đủ để thử — KHÔNG viết lại file.

### Hướng A — Verify-anchor trước khi chốt (nhắm criterion 6 BÁM BẰNG CHỨNG, xương sống)
- **Giả thuyết:** nếu SKILL buộc mỗi anchor `file:line` viện dẫn phải được VERIFY (file tồn tại + số dòng nằm trong file + đoạn code nói đúng điều được gán) TRƯỚC khi đưa vào artifact, agent sẽ tự bắt `sandbox.py:97` (không tồn tại) và gán-sai-PolicyGate → criterion 6 lên 2.
- **DIFF** — thêm 1 gạch đầu dòng vào §"Quy tắc bắt buộc" (sau dòng "Contract trước code…"):
  ```
  - **Anchor phải verify được, không chép trí nhớ.** Mọi anchor `file:line` viện dẫn code gốc phải được KIỂM trước khi đưa vào artifact: file tồn tại · số dòng ≤ số dòng thật của file · đoạn ở dòng đó THẬT nói điều được gán (không phải docstring/dòng lân cận, không gán cấu phần ở file khác). Không kiểm được → hạ thành tên-file + nhãn "chưa định vị dòng", KHÔNG ghi số dòng đoán. Một anchor sai kéo cả chuỗi stage sau xây trên claim sai.
  ```
- **Rủi ro:** agent có thể lười, hạ nhiều anchor đúng xuống "chưa định vị dòng" cho an toàn → artifact loãng bằng chứng, criterion 6 không lên mà còn nhạt. Chấm phải phạt cả "né anchor" lẫn "anchor sai".

### Hướng B — Reconcile Plan ngược non_goals + wiring code gốc (nhắm criterion 4 CONTRACT-TRƯỚC-CODE)
- **Giả thuyết:** nếu SKILL buộc mỗi bước Plan phải đối chiếu ngược (a) chính non_goals/constitution đã chốt và (b) wiring code gốc mà nó viện dẫn, agent sẽ bắt được `BudgetGuard`-in-kernel-chain (mâu thuẫn §0 + trái `bootstrap.py:31`) → criterion 4 lên 2.
- **DIFF** — thêm 1 gạch đầu dòng vào §"Quy tắc bắt buộc" (ngay sau dòng "Contract trước code…"), hoặc 1 dòng vào EXIT CRITERIA của phase CONTRACT:
  ```
  - **Plan phải nhất quán với constitution của chính nó và với wiring code gốc.** Trước khi chốt Plan: đọc lại từng bước, đối chiếu (a) không bước nào chạm/mâu thuẫn một non_goal đã liệt, (b) nếu bước mô tả cách gắn/wire một cấu phần, nó khớp cách code gốc thật sự wire (không "gắn" thứ code gốc CỐ Ý không wire). Bước nào lệch → sửa Plan hoặc ghi rõ là chủ-ý-khác-gốc kèm lý do; KHÔNG để Plan tự mâu thuẫn với §Constitution.
  ```
- **Rủi ro:** trùng một phần với luật "Contract trước code" đã có; nếu chỉ thêm lời-nhắc mà không có checklist cưỡng-hành thì delta đo được có thể nhỏ. Chấm so với baseline xem lời-nhắc-suông có đủ đổi hành vi không.

### Hướng C — Tự-soi phải TRỎ bằng chứng, không tick Yes/No (nhắm criterion 6 BÁM BẰNG CHỨNG, cách khác A — sửa ở tầng self-check thay vì tầng viết-anchor)
- **Giả thuyết:** artifact có §7 "Tự soi" tick "Bám nguồn — CÓ" và "plan không đụng non-goal — CÓ" trong khi hai lỗi còn nguyên; nếu SKILL buộc mỗi mục tự-soi phải TRỎ tới một bằng chứng cụ thể (một anchor đã-verify / một hàng bảng) thay vì trả lời CÓ/KHÔNG, agent phải mở file khi tự-soi và sẽ vấp `sandbox.py:97` + `BudgetGuard` → criterion 6 (và kèm 4) lên.
- **DIFF** — thêm vào §"Vòng lặp lõi của MỌI cổng" (hoặc tạo mục "Tự soi trước khi chốt cổng"), 1 câu:
  ```
  - **Tự-soi phải TRỎ bằng chứng, không tick suông.** Mỗi câu tự-soi ("bám nguồn?", "plan không đụng non-goal?") chỉ được đánh CÓ khi trỏ được tới bằng chứng cụ thể vừa kiểm (anchor đã verify tồn-tại/đúng-dòng; số hàng Plan đã đối chiếu non_goals). Không trỏ được = chưa CÓ: ghi "còn phải kiểm X" thay vì tick. Tick CÓ mà không trỏ được bằng chứng = tự-khen suông, làm hỏng cổng.
  ```
- **Rủi ro:** chồng lấn với A (cùng criterion 6) và B (cùng đụng "plan vs non_goal"). Giữ C tách riêng để đo đòn bẩy nằm ở tầng VIẾT (A/B: cưỡng-hành lúc sinh) hay tầng SOI (C: cưỡng-hành lúc kiểm-lại) — nếu C thắng thì gốc là "self-check quá lỏng", nếu A/B thắng thì gốc là "thiếu luật lúc viết". KHÔNG chạy cả ba nếu chỉ có 3 slot; ưu tiên A + B (hai criterion khác nhau), thêm C nếu muốn tách tầng của criterion 6.

> Ghép chạy đề xuất: **A (criterion 6) + B (criterion 4)** là cặp tối thiểu (hai tiêu chí khác nhau, hai lỗi khác nhau). Thêm **C** nếu muốn biết criterion 6 sửa tốt hơn ở tầng viết-anchor (A) hay tầng tự-soi (C) — chọn một trong A/C để merge, không cả hai (thừa).

## §4 — Ưu tiên

**KHÔNG ĐÁNG TUNE (ngay lúc này) — nghiêng về "để sau" nếu có slot.** Grade 14/16 là cao và GATE đã ĐẠT; **cả hai lỗi mất điểm về bản chất là lỗi-của-lần-chạy** (anchor `sandbox.py:97` chép ẩu; Plan tự mâu thuẫn với chính §0 của nó) — một agent chạy cẩn thận trên đúng SKILL này sẽ không mắc, nên phần lớn không tune được. Lỗ SKILL thật (self-check tường thuật không cưỡng-hành verify-anchor + reconcile-plan-vs-non_goals) là có, rẻ để thử (2–3 diff nhỏ) và chạm đúng một xương sống — nên nếu vẫn muốn nâng độ chống-ẩu thì xếp "để sau, một vòng ngắn", không chặn việc khác. Không "tune ngay" vì tỉ lệ lỗi-run:lỗi-skill nghiêng mạnh về run.

## §5 — Nhắc luật thí nghiệm (bắt buộc khi chạy)

- **Baseline trước:** chạy `frame` HIỆN TẠI trên fixture §1 → `runs/<ts>/baseline/output.md`, chấm bằng rubric §2 → `baseline/grade.md`. Mọi variant phải hơn 14/16 (và giữ gate) mới đáng theo.
- **Một biến duy nhất:** mọi variant cùng fixture §1 (cùng project, cùng đầu-vào, cùng level, cùng chế-độ tự-quyết). Chỉ khác đúng bản sửa SKILL. Đổi fixture/chế-độ giữa chừng → làm lại.
- **Chấm mù:** người/agent chấm chỉ thấy {project, đầu-vào, level, chế-độ, output}, không thấy hướng; phải mở code gốc để verify anchor.
- **Confirm bản thắng bằng agent MỚI + fixture thứ hai:** lấy `proposed-SKILL.md` bản thắng, chạy agent mới trên (a) đúng fixture hex_agent slice-01, và (b) một project thứ hai KHÁC (một codebase có anchor code thật để bẫy lại lỗi verify-anchor + có non_goals để bẫy plan-vs-constitution). Vẫn hơn baseline ở CẢ HAI → điểm đến từ SỬA, đáng merge; chỉ hơn ở fixture gốc → mùi over-fit (có thể chỉ vá đúng `sandbox.py`/`BudgetGuard` của lần này), xem lại diff.
- **Không đụng `frame/SKILL.md` thật** cho tới khi có bản thắng đã qua confirm; mỗi variant nằm trong `experiments/runs/<ts>/<variant>/proposed-SKILL.md`.
