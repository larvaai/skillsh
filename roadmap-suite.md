# Roadmap — Bộ quản lý nhiều project (bản đầy đủ, có acceptance từng skill)

> Bản này **mở rộng** `roadmap-portfolio.md` (bản gọn: 1 skill `portfolio`, 4 feature).
> Khác biệt chính: (1) tách `portfolio` thành **nhiều component** vì một skill ôm cả
> danh mục + switch + dashboard + router + phản biện là vi phạm chính nguyên tắc
> "1-skill-1-file"; (2) thêm **NỀN khoá-project** mà bản gọn bỏ sót — đây mới là dependency
> thật của mọi thứ; (3) **acceptance criteria cho CẢ 12 skill cũ**, không chỉ 4 feature mới.
> Sinh ra từ workflow 9-agent (4 khảo sát → 3 thiết kế 3 lăng kính → tổng hợp + critic).

## North star

Biến bộ **12 skill tiếng Việt** (mỗi skill sở hữu 1 file state, hiện chỉ quản **1** project
qua con trỏ `state/current.json`) thành **bộ quản lý NHIỀU project**: một *nhạc trưởng*
đọc-tổng bắc ngang `state/project/*/` để agent **hiểu repo / brainstorm / phản biện** trên
nhiều project cùng lúc — gõ một lệnh thấy bảng mỗi-dòng-một-project, chuyển ngữ cảnh an toàn,
được tiến cử skill kế và phản biện thứ tự ưu tiên **từ state thật** — trong khi giữ tuyệt đối
**mô hình sở-hữu-file** (lớp portfolio read-only trừ danh mục/con trỏ) và **kỷ luật
user-quyết-scope** (chỉ tiến cử, không auto-run).

## Chẩn đoán: 3/4 năng lực đã có skill lo

| Năng lực | Skill phủ | Trạng thái |
|---|---|---|
| Hiểu repo (1 project) | atlas · explain · trace · teen | **có đủ** |
| Brainstorm tính năng | idea · partner · frame | **có đủ** |
| Critical-thinking (1 project) | review · triage · grade · idea(Nhánh A) | **có đủ** (review cần vá) |
| Hạ tầng tự-cải-tiến | grade · tune | cần mài (mới 1/12 skill có rubric) |
| **Quản lý NHIỀU project** | — | **CÒN THIẾU (toàn bộ lớp điều phối)** |
| Cách ly dữ liệu giữa project | (mọi skill sở-hữu-state) | cần khoá lại (chưa test vì mới 1 project) |

→ Không build lại phần hiểu-repo/brainstorm/phản-biện. Chỉ dựng **lớp điều phối đa-project**
(nhạc trưởng) + **nền khoá-project** bên dưới, và **vá** vài lỗ ở skill cũ.

## Các component MỚI (giữ 1-skill-1-file)

| Component | Nhiệm vụ | Sở hữu / ghi gì | Phụ thuộc |
|---|---|---|---|
| **normalizer** (canonical-key) | Quy tắc DUY NHẤT: full-path \| slug \| basename → cùng một khoá; trùng basename khác path → `basename+hash`; thống nhất shape `current.json` `{project(key),path,mode,updated_at}`; di trú greenfield→brownfield. Thay logic "cắt tên folder cuối" đang nhân bản ở explain/frame/partner/atlas. | Quy tắc dùng chung (thân là bảng path↔key trong `portfolio.json`) | — |
| **portfolio** (danh mục) | Sổ cái duy nhất liệt kê mọi project + metadata. Nguồn sự thật cho switch/dashboard/router. | **`state/portfolio.json`** (chủ MỚI) | normalizer |
| **switch** | Điểm-vào-trung-lập đổi con trỏ: đặt `current.json` chuẩn-shape + in recap, từ chối key ngoài danh mục. Gom quyền ghi con trỏ về 1 chỗ. | Ghi `state/current.json` (trong luồng switch) | normalizer, portfolio |
| **dashboard** (bảng D1) | Bảng READ-ONLY mỗi-project-một-dòng: trụ partner · #idea mở · atlas tươi/stale · user L? · slice frame · cổng go/no-go kế. | KHÔNG ghi gì | normalizer, portfolio |
| **router** | Câu ý định mơ hồ → tiến cử 1–2 skill + lý do + điểm bàn giao, định tuyến CÓ ngữ cảnh. KHÔNG auto-run. | KHÔNG ghi gì | portfolio, dashboard |
| **portfolio-critical-thinking** | ≥2 project chờ quyết định → nêu lý do đổi thứ tự dựa dữ liệu THẬT; 0–1 project → im lặng; chỉ đề xuất. | KHÔNG ghi gì | portfolio, dashboard |
| **portfolio-lifecycle** *(critic add)* | archive/unarchive + **reconcile** (folder ↔ portfolio lệch) + phát hiện **path đã biến mất/di chuyển**. Định nghĩa "project chết". | Ghi `portfolio.json` (cùng chủ portfolio) | portfolio, normalizer |
| **portfolio-testkit** (harness) | Bộ kiểm acceptance-first: fixtures đa-project + runner "input → chụp state → diff expected" + rubric mở rộng. Biến mọi AC thành falsifiable. | `experiments/acceptance/` + `rubric-<skill>.md` | normalizer |

## Roadmap theo phase (thứ tự = phụ thuộc, không nhảy cóc)

### P0 — Nền dữ liệu + harness + chuẩn-hoá format + vá tham chiếu chết
Dựng nền để MỌI thứ portfolio đứng lên. **Harness phải chạy được TRƯỚC** (nếu không, exit-criteria
P0 tự-tham-chiếu: dùng harness chưa xong để nghiệm thu harness).
- Đặc tả **canonical-key** (kèm **thuật toán hash + độ dài + chứng minh không-va-chạm trên fixture** — *critic*) + shape `current.json` thống nhất.
- Tạo `portfolio.json` + skill `portfolio`; backfill `hex_agent` suy từ `current.json`+folder, không hỏi user.
- **Chuẩn-hoá `99_changes.md` / `pipeline-state` / `ideas` thành máy-đọc-được** (JSON/front-matter cho `last_synced_commit`, `built_commit`, `scorecard`, `drift`) — *critic*: nếu không, dashboard đọc atlas-freshness đứng trên cát.
- **Chốt chính sách ghi file chung** (`current.json`, `portfolio.json`): atomic write-rename + last-write-wins, ai được chạm `last_touched_at` — *critic*: đây là điểm nhiều-người-ghi-một-file, mâu thuẫn tiềm ẩn với 1-skill-1-file.
- Dựng `experiments/acceptance/` (runner + case format) + fixtures **two-project / basename-collision / state-khuyết / greenfield-slug**.
- Viết `rubric-review.md`, `rubric-idea.md`, `rubric-portfolio-dashboard.md`; `grade` nhận tham số `skill`. **Định nghĩa schema `review.json` NGAY ở đây** (*critic*: rubric-review + pct dùng nó, không để tới P3).
- **Vá bug** `review/SKILL.md` dòng 15/86/89: `plan` → `frame` (skill `plan` không tồn tại). Grep toàn bộ `.claude/skills/*/SKILL.md` tìm tham chiếu chết khác.
- `/skill-define` xác nhận cụm portfolio không trùng 12 skill.

**Exit:** harness chạy 1 case cho PASS/FAIL rõ · backfill hex_agent đúng không hỏi user · `grep 'plan'` trong review = 0 · 2 project trùng basename → 2 khoá phân biệt · `grade` chấm được review bằng rubric mới · format state parse được bằng máy.

### P1 — Cách ly dữ liệu + di trú shape + sửa nhãn tier
Chứng minh chạy project B **không đụng** state A — điều kiện tiên quyết của mọi aggregation
(gap đa-project chỉ lộ khi có project thứ hai).
- Hiện thực `normalizer` thành code kiểm được; cập nhật explain/frame/partner/atlas/idea tham chiếu quy tắc chung.
- Hook Bước-0: chạy skill trên project mới → `portfolio.json` tự thêm entry.
- **Runner di trú greenfield→brownfield đa-file + rollback** (*critic*): đổi folder + rewrite mọi `ideas/*.json.project` + `_index` + `review/triage/pipeline` — xử trạng thái đứt-gãy giữa chừng, không để lệch.
- **Task có-gate "di trú 10 skill về shape `current.json` chuẩn"** (*critic*): grep mọi nơi ghi con trỏ, sửa về 1 schema, test sau khi chạy từng skill con trỏ luôn đúng 1 shape.
- AC cách-ly cho từng skill sở-hữu-state (diff state A = 0 byte khi thao tác B).
- Kiểm cảnh báo lệch: `current.json` trỏ A + thao tác đối tượng B → skill HỎI, không ghi nhầm A.
- **Sửa nhãn tier** (*critic*): `idea-2`, `triage-5`, `explain-4`, `frame-4/5` là hành vi MỚI phụ thuộc P0+P1 — không được coi "có-sẵn".

**Exit:** thao tác B không sửa 1 byte state A · basename-collision không ghi đè nhau · di trú đứt-gãy rollback được · mọi ghi con trỏ đi qua shape chuẩn.

### P2 — Nhạc trưởng lõi: switch + dashboard
- `switch`: đổi con trỏ chuẩn-shape, từ chối ngoài danh mục, recap đọc thuần state.
- **Bảng ánh xạ 3 thang** (idea gd0-5 · partner pillar 1-5 · atlas 0-5) → trục 15 GĐ của doc; **chốt bằng ví dụ hex_agent trước** khi render diện rộng (*top-risk*: lệch một nấc → cột "cổng kế" sai âm thầm).
- `dashboard` read-only khớp cột D1 (dòng 941-963 của `quy-trinh-idea-to-operate.md`), nhấn 2 cổng đắt GĐ8 Live Slice & GĐ13 Go/No-Go, state khuyết → `—`, project chờ go/no-go nổi đầu.
- Atlas freshness: so `last_synced_commit` với `git HEAD`; **phân biệt "path không tồn tại" vs "tồn tại nhưng không git"** (*critic*), không crash.

**Exit:** `/dashboard` ≥2 project in đúng số dòng = số folder · diff state trước-sau = rỗng · `/switch A↔B` đúng con trỏ + recap.

### P3 — Trí tuệ điều phối: router + phản biện ưu tiên + cầu dashboard→hành động
- `router` read-only: ý định mơ hồ → 1–2 skill + lý do; định tuyến có ngữ cảnh (chưa `.ai-understanding/` mà hỏi overview → gợi `/atlas` trước). Phủ đủ 12 skill.
- `portfolio-critical-thinking`: ≥2 project chờ → ≥1 lý do đổi thứ tự bám ô state cụ thể.
- **Bắc cầu dashboard→router** (*critic*): mỗi dòng project → "gõ gì để hành động", không để user tự dịch.

**Exit:** router gợi atlas trước trên project chưa map, không tự chạy · phản biện trích số cụ thể truy được về field · 6 component mới + 12 skill cũ có ≥1 gate-case PASS.

### P4 — Vá tích luỹ & trung thành doc (thin, không missing)
- Traceability **idea→frame** (bịt `redact-tool-args` done_handoff mà không có `agent-state.json`).
- trace/teen đọc `user-state.level` đúng project đang thao tác.
- Nâng partner Trụ 5 (GĐ12-14) từ checklist lên artifact thật (Verification Report / Go-No-Go Runbook / Ops Dashboard) → đóng vòng LEARN.
- Mở rộng rubric cho triage + portfolio-skill để `tune` chạy ngoài explain.

## Acceptance criteria — từng skill

Quy ước: **[GATE]** = trượt thì skill coi như CHƯA xong. `proof` = cách chứng minh (chạy fixture,
diff state, quét cơ học). *Nguyên tắc từ critic:* thay phán-đoán-chủ-quan bằng **oracle cơ học**
(regex từ-cấm đóng, tập câu-vàng, `grade` chấm k-lần lấy trung vị + báo phương sai).

### Skill CŨ

**explain** *(có-sẵn)*
- [GATE] `current.json` trỏ A + user-state A=L1: overview không-arg mở bằng VẤN ĐỀ+CHO-AI (không thuật ngữ kiến trúc), dừng đúng Zoom-1, không rò rỉ project B. *proof:* fixture two-project + regex từ-cấm.
- [GATE] Overview L3 qua `grade` ≥8/14 (chấm 3 lần lấy trung vị, báo phương sai) và 3 gate xương sống không rớt.
- Có `.ai-understanding/` tươi → trả lời từ artifact, không re-scan hàng loạt. *proof:* log đọc file.
- Arg project B ≠ current → đọc user-state B, ghi con trỏ B chuẩn-shape, không lẫn A *(tier: mài-cứng — hành vi mới)*.
- Chưa có user-state → coi L0; cuối phiên hỏi mức và ghi `user-state.json` đúng schema.

**trace** *(mài-cứng)*
- [GATE] Mỗi bước đủ 4 trường evidence; mọi [STATE CHANGE]/[SIDE EFFECT] đánh dấu; gặp DB/external → ghi "boundary" và DỪNG.
- [GATE] Khối TÌNH HUỐNG đời thường + bảng ánh xạ xuất hiện TRƯỚC tên kỹ thuật.
- Tổng hợp (Bước 3) lên trước bằng chứng; chi tiết Bước 2 chỉ khi user chỉ định.
- Đọc `user-state.level` đúng project để canh độ sâu (hiện KHÔNG đọc dù tuyên bố L5+).
- Trace project B khi con trỏ trỏ A → resolve đúng, không trace nhầm code A.

**teen** *(mài-cứng)*
- [GATE] Lời giải không chứa `function/loop/variable/class/method/array` (regex từ-cấm đóng); buộc nhắc thì giải nghĩa trước, đúng 1 lần.
- [GATE] Không analogy/câu chuyện ngoài project.
- Đúng 5 nhịp: VẤN ĐỀ (1 câu) → giải thẳng bằng context → chạy bằng lời → 1 câu kết ý nghĩa.
- Code dài → HỎI muốn hiểu phần nào trước.
- User hỏi "đoạn này nằm đâu" → gợi explain/trace, kèm neo project.

**idea** *(có-sẵn)*
- [GATE] Ý "chưa rõ khả thi" → đúng Nhánh B (spike), ghi `an_so_can_kiem_chung[]` + time-box, không code, không tự kill. *proof:* `budget-exhaustion-backoff` dừng đúng ở spike.
- [GATE] Con trỏ A + ý thuộc B → HỎI/cảnh báo lệch, không ghi `ideas/` vào A *(tier: mài-cứng — hành vi mới)*.
- Resume không rõ slug → liệt kê "CÁC Ý ĐANG MỞ" đủ, không tự chọn hộ. *proof:* hex_agent có 2 ý → liệt kê đủ 2.
- `cho_duyet:true` phản ánh đúng để dashboard liệt kê "đang chờ quyết định" không cần mở từng `.json`.
- Ghi `ideas/<slug>.json` → cùng lượt cập nhật `_index.json` + chạm `portfolio.json`.

**review** *(mài-cứng)*
- [GATE] Bàn giao khi có gap Critical trỏ skill CÓ THẬT (`frame`), không trỏ `plan`. *proof:* `grep 'plan'`=0.
- Mỗi gap đủ evidence + nhãn Critical/Medium/Low; không gap nào thiếu evidence.
- Có `agent-state.json` với do_not_touch → không báo gap vùng out-of-scope.
- Review tổng thể → đúng thứ tự edge → error → permission.
- User ghi-nhận → append 1 dòng `review.json` đúng project; thêm/xoá project không lẫn gap.

**triage** *(có-sẵn)*
- [GATE] Verdict luôn ĐÚNG MỘT trong 7 giá trị + 1 câu lý do + 1 câu rủi ro; không bao giờ "kết quả mở".
- [GATE] File ∈ do_not_touch → chỉ verdict giữ/cần-đọc-thêm, không fix inline dù typo.
- Verdict xoá field chỉ khi grep caller = không-thấy VÀ không thuộc API/DB/domain/live-slice.
- Verdict giữ (đường nhanh) → không grep, không đọc state, không ghi `triage.json`.
- Ghi-nhận verdict xoá/chuyển/rewrite → append `triage.json` đúng project của FILE; file chưa track → cảnh báo lệch *(tier: mài-cứng — hành vi mới)*.

**grade** *(mài-cứng)*
- [GATE] Report đúng khung 7 dòng + TỔNG/14 + GATE + "SỬA TRƯỚC TIÊN".
- [GATE] Tiêu chí 1/4/5 = 0 → GATE "rớt" dù TỔNG cao.
- Claim nhắc file/API/hành vi không có trong code → tiêu chí 5 = 0.
- Chạy trong `tune` → ghi `grade.txt` đúng chỗ, không đụng state skill khác.
- Nhận tham số `skill` → đọc `rubric-<skill>.md` (mở trần chấm ngoài explain).

**frame** *(có-sẵn)*
- [GATE] Lượt lập kế hoạch kết bằng khối CHỜ XÁC NHẬN đủ 4 trường + `awaiting_confirmation=true`; không dòng code nào trước câu duyệt.
- [GATE] "Build cả app" → phát đúng kịch bản TỪ CHỐI (kiểm bằng marker `awaiting_confirmation`, không "nguyên văn"), quay về hỏi goal + 3-5 non_goals.
- Không sang CONTRACT tới khi non_goals confirmed + đúng 1 slice active đủ 4 trường.
- Sau BUILD đụng code + có `.ai-understanding/99_changes.md` → append 1 dòng Pending, không bump `last_synced_commit`; không ghi drift sang project B *(tier: mài-cứng)*.
- Thêm ô "đến từ idea slug X" (traceability idea→frame) *(tier: làm-mới — P4)*.

**skill-define** *(mài-cứng)*
- [GATE] Nhu cầu độc hại → dừng ngay, không liệt case.
- [GATE] Nhu cầu giống skill đã có (đọc/grep `.claude/skills/` thật) → nói thẳng có thể không cần skill mới.
- Output đúng format: 3-5 dòng "Trường hợp → làm gì" + 1 dòng "không có skill thì làm sao" + (nếu đáng) trỏ skill-creator.
- Chạy cho cụm portfolio → xác nhận không trùng 12 skill, không tự viết SKILL.md.

**tune** *(mài-cứng)*
- [GATE] Mọi variant + baseline chạy CÙNG fixture; đổi fixture giữa chừng → loại thí nghiệm.
- [GATE] Tune skill chưa có rubric → DỪNG, yêu cầu làm rubric trước.
- Chấm mù: agent chấm chỉ nhận `{project,level,mode,output.txt}`.
- Bản thắng qua Bước-5 (fixture gốc + project thứ hai) trước khi đề xuất merge; chỉ hơn ở fixture gốc → nhãn over-fit.
- Tune không ghi `current.json`, không đụng state skill khác.

**atlas** *(mài-cứng)*
- [GATE] Chạy repo A ghi `.ai-understanding/` dưới A, không đụng của B.
- Dựng đủ 20 artifact + index + scorecard + `99_changes`.
- Portfolio reader thu scorecard + `built_commit` + drift **không re-scan** (nhờ format máy-đọc P0).
- Chạy lại trên repo đã map → chỉ cập nhật phần đổi.
- Ghi con trỏ 1 lần/phiên chuẩn-shape; không ghi state skill khác.

**partner** *(mài-cứng)*
- [GATE] ≥2 project cùng chạy partner: chạy B không sửa `decisions[]` của A.
- [GATE] Không nhảy idea→code: mọi bàn giao build qua `frame`; recap "ĐANG Ở ĐÂU" đúng trụ/stage.
- Dashboard render dòng D1 từ `pipeline-state`: pillar/stage + cổng go/no-go + ai duyệt.
- Gate chưa đóng vì `status:assumed` → hiện "đang chờ chốt", không coi đã qua cổng.
- (P4) GĐ12-14 xuất artifact thật thay checklist.

### Component MỚI

**normalizer / canonical-key** *(làm-mới)*
- [GATE] full-path / slug / basename → CÙNG khoá; skill cũ tham chiếu quy tắc này thay tự cắt tên folder.
- [GATE] Trùng basename khác path → khoá phân biệt (`basename+hash`, **hash có đặc tả độ dài + xử va-chạm thật, không ghi đè im lặng** — *critic*).
- Di trú greenfield slug→canonical khi có code: đổi folder + cập nhật `current.json`+entry trong 1 thao tác kiểm được, không mồ côi.
- Shape `current.json` = 1 schema `{project(key),path,mode,updated_at}` cho cả 2 mode.
- Không còn logic "cắt tên folder cuối" nhân bản ở >1 nơi.

**portfolio (danh mục)** *(làm-mới)*
- [GATE] Tồn tại `portfolio.json` `projects[]{key,path,mode,created_at,last_touched_at,last_skill,archived?}`; mỗi entry khớp 1-1 folder `state/project/<key>/` (không mồ côi 2 chiều).
- [GATE] CHỦ ghi là skill danh mục MỚI (không phải partner/atlas).
- Chạy skill trên project mới → tự thêm entry đúng key+path+mode.
- Backfill hex_agent từ `current.json`+folder, không hỏi user.
- Basename-collision → 2 khoá, không ghi đè.

**switch** *(làm-mới)*
- [GATE] `/switch <key|path>` → con trỏ chuẩn-shape; ngoài danh mục → TỪ CHỐI + gợi ý gần đúng, không ghi.
- [GATE] Chỉ switch được ghi con trỏ trong luồng đổi-project; skill khác có arg chỉ ĐỌC.
- Recap 1 khối đọc thuần state, không quét repo.
- Switch greenfield (slug) hoạt động không đòi verify folder.
- A→B→A đúng con trỏ + recap mỗi lần.

**dashboard (bảng D1)** *(làm-mới)*
- [GATE] READ-ONLY tuyệt đối: chạy xong diff **toàn state** = rỗng (**định nghĩa rõ phạm vi diff + bỏ mtime** — *critic*).
- [GATE] Không tham số → đúng số project = số folder; thêm/xoá folder → bảng đổi đúng.
- Cột khớp D1 (chủ/duyệt/góc-nhìn/cổng), nhấn GĐ8 & GĐ13, không bịa cột ngoài doc.
- atlas tươi/stale = so `last_synced_commit` vs HEAD; path biến mất vs non-git phân biệt; state khuyết → `—`.
- Project chờ go/no-go nổi đầu.
- *(AC theo QUY TẮC ánh xạ trên fixture cố định, KHÔNG đóng đinh vào snapshot hex_agent sống — critic: tránh test giòn.)*

**router** *(làm-mới)*
- [GATE] KHÔNG tự CHẠY skill — chỉ tiến cử; không ghi state.
- [GATE] Định tuyến CÓ ngữ cảnh: chưa `.ai-understanding/` + hỏi "làm gì" → gợi `/atlas` trước, giải thích vì sao.
- Ý định mơ hồ → 1–2 skill + lý do + điểm bàn giao.
- **Đo bằng TẬP CÂU-VÀNG** (golden intents có skill kỳ vọng), không phải "đếm đủ 12" (*critic*).
- Câu đa-nghĩa ("review feasibility" → partner+review) → phân giải rõ.

**portfolio-critical-thinking** *(làm-mới)*
- [GATE] ≥2 project chờ → ≥1 lý do dựa dữ liệu THẬT (ẩn số mở / kẹt GĐ8|GĐ13 / gap Critical treo), không chung chung. *(updated_at là thời-điểm-GHI-STATE, không phải hoạt-động-thật — dùng thận trọng, critic.)*
- [GATE] KHÔNG tự đổi thứ tự build — chỉ đề xuất.
- 0–1 project chờ → im lặng.
- Mỗi lý do truy được về ô state (project X, field Y).
- READ-ONLY: diff state = rỗng.

**portfolio-lifecycle** *(làm-mới — critic)*
- [GATE] Project `archived` → biến khỏi dashboard/router/pct nhưng `state/project/<key>/` vẫn còn.
- Entry mồ côi 1 chiều (folder có, portfolio thiếu / ngược lại) → **reconcile** sửa (nguồn sự thật = quét folder, portfolio là cache), không crash.
- Path trỏ folder đã xoá/di chuyển → cảnh báo, `n/a`, không chết cả bảng.
- Định nghĩa "project chết" (ngưỡng ngày `last_touched_at`) + ai được set `archived`.

**portfolio-testkit (harness)** *(làm-mới)*
- [GATE] `experiments/acceptance/` chạy 1 case end-to-end PASS/FAIL: `{input, expected_state_delta, expected_output_contains, gate?}`.
- Fixtures đủ: two-project + basename-collision + state-khuyết + greenfield-slug.
- `rubric-review/idea/portfolio-dashboard.md` tồn tại; `grade` đọc rubric theo tham số.
- Runner tái dùng cấu trúc `experiments/runs/` của tune, không đụng cây state thật.

## Top risks

1. **Phụ thuộc dây chuyền cứng** — dashboard/switch/router đều cần path thật. Build trước normalizer+portfolio (P0) → cả nhà xây trên nền lệch. Không nhảy cóc P0.
2. **Trùng basename ghi đè state im lặng** (`.../a/api` vs `.../b/api`) — mất dữ liệu. Phải phát hiện xung đột + khoá phân biệt NGAY ở normalizer (hash có đặc tả).
3. **Gap đa-project chưa lộ** vì state thật chỉ có 1 project. Bỏ P1 (fixture 2+ project) → bug lẫn-state chỉ lộ ở production, khó truy.
4. **Vi phạm read-only** — dashboard/router/pct "tiện tay" chạm `last_touched` = đổi project đang-mở ngoài ý muốn. Gate "diff state = rỗng" là bất di.
5. **Con trỏ nhiều shape** — chuẩn-hoá mà không sửa TẤT CẢ nơi ghi (10 skill) → suy sai `mode` giữa phiên. (P1 có task-gate riêng.)
6. **Ánh xạ 3 thang → 15 GĐ** là điểm dễ sai nhất của dashboard; chốt bằng ví dụ hex_agent trước.
7. **Nhiều-người-ghi-một-file** (`portfolio.json`, `current.json`) — cần chính sách atomic-write/last-write-wins (P0).
8. **Kỷ luật user-quyết-scope** dễ bị router/pct ăn mòn (tự quyết hộ / tự đổi thứ tự). Test bằng case cố tình mơ hồ.

## Bước kế tiếp
Đây là roadmap (GĐ9), chưa phải lúc viết SKILL.md (GĐ11). Trước khi build:
1. `/skill-define` cụm portfolio (xác nhận không trùng, có nên tách 8 component hay gộp bớt).
2. `/frame` đóng khung **P0 workstream đầu tiên** (canonical-key + harness) làm slice đầu.
