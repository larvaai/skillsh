# TUNE — skill `ship` (dựa trên chấm 13-ship.grade.md)

Nguồn: grade `experiments/hex-rebuild-review/grades/13-ship.grade.md` · rubric `rubrics/13-ship.rubric.md` · SKILL `/.claude/skills/ship/SKILL.md` · artifact `rebuild-hex-agent/pipeline/13-ship.md` · code gốc `/Users/uspro/Desktop/namnson/hex_agent`.

## §0 Chẩn đoán (≤6 câu)

Artifact **RỚT GATE**: hai xương sống C1 (BẰNG CHỨNG) = 0 và C3 (BỐN THỨ CHẶN) = 0, tổng 10/16 (C4/C5/C6 = 2, C7/C8 = 1). Cả C1 lẫn C3 rớt vì **một cơ chế duy nhất**: artifact lấy 6 tên metric loop + 3 tên flag mà GĐ11 mới ĐỀ XUẤT (thiết kế) rồi trình như **trạng thái đang chạy** — "monitoring BẬT", "rollback ĐÃ TEST trên staging" — trong khi grep code gốc = 0 hit cho cả 9 tên (tự kiểm: `event_log.py:_METRICS` thật là steps/llm_calls/policy_blocks/finish_gate_blocks…, `features.yaml` thật lại có `delegation.enabled: true` + `rag.enabled: true`, NGƯỢC claim "OFF default"). Đây là **lỗi-của-SKILL, tunable**: `ship/SKILL.md` có luật chống bịa cho ĐÚNG sign-off ("không bịa 'đã ký'", dòng 26/39) nhưng KHÔNG có luật phân biệt "tên/metric/flag do GĐ trước THIẾT KẾ chưa dựng" với "đã có thật trong code / đang chạy runtime" — nên agent tự cho phép nâng thiết-kế thành trạng-thái, và rubric C1/C3 neo thẳng đó = 0. Phần lỗi còn lại là **lần-chạy**: "6 N/A" lệch bảng (đếm lại chỉ 2) là sai số học của agent, và ký "CTO ✔ + PO ✔" không tên người (C8=1) là kỷ luật lần chạy — SKILL đã có sườn cổng đúng, chỉ chưa buộc ghi ai đóng vai. Kết: đáng tune vì gate rớt do một lỗ SKILL thật (thiếu luật phân-biệt-thiết-kế-vs-đã-dựng), phần "6 N/A" là lần-chạy nên không tune được.

## §1 Fixture đề xuất (cố định cả thí nghiệm)

- **project**: `hex_agent` rebuild — artifact ở `rebuild-hex-agent/pipeline/`, code gốc đối chiếu tại `/Users/uspro/Desktop/namnson/hex_agent` (mọi claim về metric/flag/seam kiểm bằng grep repo này).
- **Đầu vào GĐ trước** (nạp NGUYÊN cho mọi variant, không đổi): `pipeline/12-uat.md` (Test & Verification Report: 28/28 AC lõi · 26 PASS · 2 PENDING · 0 FAIL · UAT ✔ + Security ✔ ký-có-điều-kiện + 2 blocker redact-raw-args/scope-property + điều kiện đóng R1 SPIKE-1/D3) · `pipeline/11-delivery.md` (flag/rollback/migration design) · `pipeline/08-skeleton.md` (Live Slice — nói thẳng rebuild 0/9 tick, code chưa gõ, chưa staging) · `pipeline/10-modules.md` (owner on-call) · `00-understanding/REBUILD-BRIEF.md`.
- **Release cố định**: `"R1-nền + alpha nội bộ"` — chế độ tự-quyết (cổng CTO+PO do người viết đóng vai, không hỏi user). Ép cùng release + cùng đầu vào để chỉ 1 biến (bản sửa SKILL) đổi; KHÔNG cho variant tự chọn release/đầu vào khác.
- **mode/level/độ dài**: một trang SHIP 4-trong-1 (Go/No-Go + Rollback + Runbook + Rollout + cổng), người đọc = CTO/PO/business ngoài + dev trực, ~1–1.5 trang (như artifact gốc).
- **Ghi**: `experiments/runs/<ts>/fixture.txt` chép các dòng trên; mọi variant đọc đúng file này, không ai đổi giữa chừng.

## §2 Thước

- Rubric: `/Users/uspro/Desktop/skillsh/experiments/hex-rebuild-review/rubrics/13-ship.rubric.md` (8 tiêu chí × 0/1/2, /16; xương sống = C1, C3, C4).
- **Luật xếp: loại hết bản RỚT GATE trước (C1/C3/C4 bất kỳ = 0), rồi mới xếp theo Tổng.** Hoà Tổng → bản diff NHỎ/robust hơn thắng (ít rủi ro over-fit vào đúng fixture hex này).
- Baseline = artifact hiện tại `13-ship.md` đã chấm **10/16, RỚT GATE (C1=0, C3=0)**. Mọi variant phải kéo C1 **và** C3 lên ≥1 (thoát gate) mà KHÔNG làm tụt tiêu chí nào khác mới đáng — kéo được cả hai lên 2 là mục tiêu.
- **Chấm mù**: agent chấm chỉ thấy {project, release, level, mode, output.txt}, không biết variant theo hướng nào; đặt tên A/B/C/D trung tính.

## §3 Hướng thử A/B/C/D (mỗi hướng nhắm tiêu chí KHÁC — A/B đánh trực tiếp gate C1+C3 bằng 2 cơ chế; C nhắm C8; D đối chứng nhắm C1 riêng lẻ)

### Hướng A — Luật cứng "phân biệt THIẾT-KẾ-GĐ-trước vs ĐÃ-DỰNG-trong-code" (nhắm C1 BẰNG CHỨNG + kéo theo C3)
**Giả thuyết:** Nếu Luật cứng buộc gắn nhãn mọi tên metric/flag/endpoint/monitoring/rollback theo NGUỒN — "đã có trong code gốc (kiểm được)" vs "GĐ trước ĐỀ XUẤT, chưa dựng" — và cấm trình cái-chưa-dựng như trạng-thái-đang-chạy, agent sẽ không nâng 6 metric/3 flag GĐ11 thành "monitoring BẬT/rollback ĐÃ TEST" → C1 thoát 0, và "bốn thứ chặn" không còn ruột rỗng → C3 thoát 0.
**Diff (thêm 1 gạch đầu dòng vào mục "## Luật cứng", ngay sau luật "Cổng chặt: khuyết là NO-GO", dòng 26):**
> - **Phân biệt "đã DỰNG" với "GĐ trước THIẾT KẾ".** Mọi tên metric · flag · endpoint · alert · dòng "monitoring bật" · "rollback đã test" phải gắn nguồn: (a) **đã có trong code gốc / artifact GĐ trước — kiểm được** (ghi địa chỉ file:line hoặc mục nguồn), hay (b) **GĐ trước ĐỀ XUẤT nhưng CHƯA dựng** (đánh dấu "THIẾT KẾ GĐn — chưa có trong code"). CẤM trình cái loại (b) như trạng-thái-đang-chạy: "monitoring bật" chỉ được viết khi metric/alert đó tồn tại thật; "rollback đã test" chỉ khi trỏ được test nào chạy ở đâu ngày nào (nếu GĐ8 nói chưa có staging → rollback là **điều-kiện-treo/rollout-gate**, KHÔNG phải "đã test"). Kiểm: mỗi tên kỹ thuật trong "bốn thứ chặn" phải trả lời được "có thật trong code chưa?" — chưa thì hạ xuống dòng chặn, không tô xanh.
**Rủi ro:** buộc gắn địa chỉ cho MỌI tên có thể làm agent quá tải và bỏ sót ở việc-nhỏ (release đơn giản không cần grep code) — cần giữ mệnh đề "kiểm được" nhẹ để không biến ship thành audit lại code (lấn vai `uat`).

### Hướng B — Thêm bước Tự-soi "grep-thử tên kỹ thuật" (nhắm C1 + C3 bằng kỷ-luật-kiểm, diff nhỏ nhất)
**Giả thuyết:** Lỗi là agent không đối chiếu tên với code trước khi tô "xanh/đã test". Thêm một câu tự-soi BẮT rà mọi tên metric/flag/endpoint trong "bốn thứ chặn" so với nguồn TRƯỚC khi trình cổng sẽ chặn bịa mà không đụng Luật cứng — robust hơn A, ít rủi ro over-fit.
**Diff (thêm 1 gạch đầu dòng vào mục "## Tự soi trước khi chốt", ngay sau gạch "Bốn thứ chặn có mặt chưa?", dòng 102):**
> - **Mọi tên có kiểm được không?** Với mỗi metric/flag/endpoint/alert nêu trong "bốn thứ chặn" + Runbook + Rollout: nó CÓ THẬT trong code gốc / artifact GĐ trước không (grep-thử tên + nhãn `{...}` nếu có)? Có → giữ + ghi địa chỉ. Không (là tên GĐ trước ĐỀ XUẤT) → gắn nhãn "THIẾT KẾ GĐn, chưa dựng" và hạ "đã bật/đã test" xuống điều-kiện-treo. Đừng viết "monitoring bật / rollback đã test" khi cái đó chỉ mới được đề xuất trên giấy.
**Rủi ro:** tự-soi là lời-nhắc-mềm — agent "chạy ẩu" vẫn có thể bỏ qua mục này (đúng cái đã xảy ra ở baseline dù §5 tự-soi hiện có đã bảo "không bịa"); hiệu lực có thể yếu hơn luật cứng A nếu nguyên nhân thật là agent không đọc kỹ mục tự-soi.

### Hướng C — Buộc ghi TÊN người đóng vai Người-duyệt trong chế độ tự-quyết (nhắm C8 ĐÚNG VAI)
**Giả thuyết:** C8 = 1 vì "CTO ✔ + PO ✔ (2026-07-02)" ký ẩn danh (chỉ vai + ngày, không người). SKILL bảo "đóng vai CTO+PO tự quyết, ghi rõ" (dòng 30/172-hàm-ý) nhưng KHÔNG buộc ghi AI/người-nào đóng vai — nếu luật cổng buộc ghi tên/định danh người đóng vai Người-duyệt + tách rõ khuyến-nghị (ship) khỏi quyết-định (Người-duyệt), C8 lên 2.
**Diff (sửa luật "`ship` KHÔNG tự bấm GO", dòng 30 — thêm 1 câu vào cuối):**
> … không tự cho lên. **Chế độ tự-quyết (user nói "không hỏi approval"): ship VẪN tách khuyến-nghị (của ship) khỏi quyết-định (của Người-duyệt), và PHẢI ghi rõ AI/người-cụ-thể đang đóng vai CTO + PO ký + ngày — không ký bằng vai trơn ("CTO ✔") ẩn danh. Khuyến-nghị-ship và chữ-ký-Người-duyệt không được cùng một dòng vô-danh.**
**Rủi ro:** C8 chỉ mất 1 điểm và KHÔNG phải gate — kéo nó không giúp thoát gate; nếu chỉ chạy được ít agent thì C nên nhường chỗ cho A/B (thứ thật sự mở gate). Chạy C như hướng phụ để xem có kéo tổng mà không đụng gate không.

### Hướng D — Đối chứng: siết riêng "rollback đã-test" thành trạng-thái-3-mức (nhắm C3 BỐN THỨ CHẶN, tách khỏi A)
**Giả thuyết (đối chứng, nhắm đúng một trong bốn-thứ-chặn):** Nếu chỉ siết RIÊNG ô "rollback đã test" — buộc phân 3 trạng thái rõ (đã-test-có-địa-chỉ / test-được-nhưng-chưa-chạy / chưa-test → dòng chặn) — có kéo C3 thoát 0 mà không cần luật phân-biệt-nguồn rộng như A không? Dùng để biết gate rớt vì rollback-giả hay vì cả cụm metric+flag+rollback.
**Diff (thêm 1 câu vào artifact "2) Rollback Plan", mục Đủ-là-đủ, dòng 84 — sau "chưa test → đây là dòng chặn GO"):**
> … (chưa test → đây là dòng chặn GO). **Ghi trạng thái rollback bằng đúng MỘT trong ba nhãn, không nhập nhèm: (i) "ĐÃ TEST" — chỉ khi trỏ được chạy ở đâu/ngày/phạm vi nào; (ii) "TEST-ĐƯỢC, CHƯA CHẠY" — cơ chế lùi có nhưng chưa exercise (vd chưa có staging theo GĐ8); (iii) "CHƯA TEST" — thành dòng chặn GO. CẤM viết "đã test" cho loại (ii)/(iii).**
**Rủi ro:** D chỉ chạm 1/4 thứ chặn (rollback) — nếu C3 rớt còn vì "monitoring BẬT" dựa metric ma thì D một mình không kéo C3 lên 2 (chỉ lên 1); đáng chạy như đối chứng để định vị, không kỳ vọng thắng đơn lẻ.

> Ghi chú xếp hướng: **A và B cùng đánh cụm gate C1+C3** nhưng bằng 2 cơ chế khác (luật-cứng-phân-biệt-nguồn vs tự-soi-grep) — không trùng, để đo cách nào mở gate rẻ + ít over-fit hơn. **C nhắm C8** (điểm mất ngoài gate). **D nhắm riêng C3 qua ô rollback** để định vị gate rớt do cụm hay do rollback. C7 (=1) KHÔNG cấp hướng riêng vì grade ghi rõ nó tụt do CÙNG lỗi metric/flag ma — sửa A/B là C7 tự lên. Muốn 3 agent: bỏ D. Muốn tối thiểu 2: chạy A + B.

## §4 Ưu tiên

**"tune ngay".** Lý do: artifact **RỚT GATE ở hai xương sống** (C1=0, C3=0) — CTO sẽ ký GO trên nền metric/flag/rollback-test GIẢ, đúng loại lỗi nguy hiểm nhất mà GĐ13 tồn tại để chặn; và nguyên nhân là **một lỗ SKILL thật, tunable** (thiếu luật phân-biệt "GĐ-trước-thiết-kế" vs "đã-dựng-trong-code"), không phải chỉ lần-chạy. Đây là gate-fail do SKILL → ưu tiên cao hơn skeleton (13/14, gate đạt, "để sau").

## §5 Nhắc luật thí nghiệm

- **Chấm mù**: agent chấm chỉ nhận {project, release, level, mode, output.txt}, không biết variant theo hướng nào; tên A/B/C/D trung tính.
- **Baseline trước**: chấm lại artifact hiện tại `13-ship.md` bằng rubric trong CÙNG lượt để chốt mốc **10/16, RỚT GATE (C1=0, C3=0)**; mọi variant phải thoát gate (C1 và C3 ≥1) mới tính là hơn — tổng cao mà vẫn rớt gate thì vẫn loại trước.
- **Một biến duy nhất**: mọi variant cùng fixture §1 (cùng release, cùng đầu vào GĐ12/11/10/8), chỉ khác bản sửa SKILL; variant KHÔNG được đổi đầu vào hay release.
- **Confirm bản thắng bằng agent MỚI + fixture thứ hai**: chạy `proposed-SKILL.md` bản thắng bằng agent mới trên (a) đúng fixture hex-agent, VÀ (b) **fixture thứ hai khác** — vd một release greenfield case-mgmt có Test Report GĐ12 sạch (mọi metric/flag ĐỀU có thật, không có "tên GĐ-trước-chưa-dựng") — để chắc luật phân-biệt-nguồn không làm hỏng case mà mọi thứ vốn đã có thật (không đẻ nhãn thừa, không tụt điểm ở case sạch). Vẫn hơn baseline ở CẢ HAI → mới merge; chỉ hơn ở fixture hex → nghi over-fit, xem lại diff.
- **Không đụng SKILL thật khi đang thử**: mỗi bản sửa nằm trong `experiments/runs/<ts>/<variant>/proposed-SKILL.md`; `ship/SKILL.md` chỉ đổi sau khi có bản thắng qua confirm và Son chốt.
