# REPORT — Thử nhét dữ liệu giả MediRemind vào 28 skill (pipeline Idea→Operate)

_Chạy: 2026-07-03 · Fixture: project MediRemind giữa GĐ11 · Nguồn chấm: 28 file `grades/*.json` (bản đầy đủ sau khi sửa rate-limit) · Đáp án recall: `fixture/ANSWER-KEY.md`_

---

## 1. TL;DR

- **28 skill chấm xong.** Phân bố hiệu quả: **eff=3: 23 skill** · **eff=2: 2 skill** (fanout, frame) · **eff=0–1: 3 skill** (atlas, charter, tune — đều eff=1).
- **RỚT gate: đúng 3 skill** — `atlas`, `charter`, `tune`. Cả ba rớt vì **DỪNG Ở BẢN THIẾT KẾ / BẢN SCALED, hoặc thiếu bước ghi state**, KHÔNG phải vì bịa nội dung.
- **Cả 5 skill có đáp án cứng đều ĐẠT recall**: review 7/7 (có BUG-5 IDOR trong Critical), trace 4/4 mắt xích + side-effect, triage 1/1 (verdict xoá), traceability 4/4 (có G-1), grade 3/3 (RỚT GATE bản explain bịa Kafka). Đây là tín hiệu mạnh nhất: **lõi "bắt lỗi" của bộ skill hoạt động thật.**
- **PHÁT HIỆN LỚN NHẤT:** mọi ca rớt gate là **lỗi "chưa chạy tới cùng" (dry-run / scaled / thiếu state), KHÔNG phải lỗi trung thực.** Không skill nào bịa số/PASS/sign-off; nhiều skill còn chủ động từ chối bịa (uat đánh 0/5 AC BLOCKED, ship NO-GO, operate để "chưa có số", partner giữ CASE-1 assumed). Đòn bẩy sửa nằm ở **harness test (non-interactive, không cho spawn/ghi state thật)** nhiều hơn ở SKILL.md.
- **Meta-lỗi lặp lại quen thuộc** (khớp memory các vòng trước): 2 skill tự khai sai tiền đề — tune nói "teen thiếu rubric" nhưng `teen/rubric.md` đã có; frame bịa id `STORY-dose-ownership-guard` + "backlog.json" trong khi id thật là US-3.1.1/AC-1/AC-2 (thoát gate nhờ minh bạch ghi id thật).

---

## 2. Bảng xếp hạng MỌI skill (nhóm theo cat)

### pipeline (10 skill — GĐ0→14, đều PASS/eff 3)
| skill | gate | eff | recall | top_failure | verdict |
|---|---|---|---|---|---|
| idea | pass | 3 | n/a | NONE (thiếu vòng hỏi tương tác — do fixture batch) | 6 GĐ đủ mục, số bám BIBLE, dừng đúng Domain, bàn giao /shape |
| shape | pass | 3 | n/a | NONE (worker-scheduler gọi "module 5" nhưng thân bài mô tả đúng là container) | 14/14, mọi ranh giới trace về BC GĐ5, 5 ADR đủ phương-án-loại |
| stack | pass | 3 | n/a | Spike NFR-1 chưa có p95 (đúng hợp đồng giai đoạn giấy, không bịa số) | Ma trận có điểm×trọng số, neo về BIBLE §8/NFR, ẩn số ⏳CHƯA-ĐO |
| skeleton | pass | 3 | n/a | Thiếu block ⚠️ "đầu vào ngoài pipeline" | 0/9 checklist KHÔNG tick khống (PROVE-đừng-MOCK), bám fixture từng dòng |
| backlog | pass | 3 | n/a | NONE | Đủ 3 artifact, AC dưới story, ô #5 FAIL thành story, NFR-1 60s đẩy R2 |
| modules | pass | 3 | n/a | NONE | 4 module=4 BC, contract đủ ô, F5.2 retention "chưa-có-chủ" không bịa |
| delivery | pass | 3 | n/a | Thiếu file metadata delivery.json + chạy một-lượt (do fixture non-interactive) | 12/12 mục, event snake_case + error-code khớp contract fixture |
| uat | pass | 3 | n/a | Nit: nói "code có (T-11a/b)" nhưng progress ghi ready | **Xử đúng bẫy khó nhất**: repo có code 0 test → đánh 5/5 AC BLOCKED, 2 chữ ký CHỜ |
| ship | pass | 3 | n/a | NONE | Bắt 4/4 trap answer-key (gồm G-1), NO-GO không tự bấm GO, không bịa sign-off |
| operate | pass | 3 | n/a | NONE (thêm nhánh handoff hợp lý vì hệ NO-GO) | Bắt đủ 2 planted gap, để "chưa có số", DORA 4, traceability 2 chiều |

### pm (7 skill)
| skill | gate | eff | recall | top_failure | verdict |
|---|---|---|---|---|---|
| resume | pass | 3 | n/a | Vài dòng hơi dài, thêm block "ghi chú tiến cử" | Khối 6 mục đủ, tính đúng parallel_group, read-only, tiến cử /fanout đúng |
| progress | pass | 3 | n/a | NONE | **Đòn hiểm nhất bị chặn đúng**: báo-xong-thiếu-phiếu → giữ in_progress, không mở T-12 |
| checkpoint | pass | 3 | n/a | Lệch path: `outputs/checkpoint/delivery.md` thay vì `progress/checkpoints/T-11.md` | Phiếu PASS T-11 mọi ✓ truy về artifact thật, đúng checklist GĐ11 |
| partner | pass | 3 | n/a | Trình handoff /idea khi Trụ 1 chưa đóng (ding nhẹ) | Cold-start Trụ 1, feasibility bám BIBLE 100%, CASE-1 giữ assumed |
| frame | pass | 2 | n/a | **Bịa id**: tự chế `STORY-dose-ownership-guard` + "backlog.json" (id thật US-3.1.1/AC-1/AC-2) | Đúng-trước-code, khung+contract đủ, code-claim kiểm thật; thoát gate nhờ minh bạch |
| fanout | pass | 2 | n/a | **DRY-RUN**: không spawn sub-agent thật, không /checkpoint→/progress đóng nhánh | Kế-hoạch trung thực (10/12) nhưng lõi "bung song song" chưa chạy |
| charter | **fail** | 1 | n/a | **Thiếu `state/current.json`** (rubric A1=gate) + thiếu memory project | Khung 6 folder + constitution bám seed đẹp, nhưng bỏ Bước 6+7 → resume không thấy project |

### code (6 skill)
| skill | gate | eff | recall | top_failure | verdict |
|---|---|---|---|---|---|
| review | pass | 3 | **7/7** (BUG-5 IDOR đúng Critical) | Nit: BUG-1/2/7 xếp Medium (đúng thang) | Recall đủ 7 khuyết tật, mọi gap bám code thật, không lấn fix |
| trace | pass | 3 | **4/4** mắt xích B + side-effect | NONE | Đường status khớp 100% đáp án B, bắt 2 write-point + mutate in-place shared db |
| triage | pass | 3 | **1/1** (verdict xoá) | Thiếu cổng-3-lối AskUserQuestion (Bước 4) | Verdict xoá đúng, grep 0 caller thật, trích atlas có thật |
| explain | pass | 3 | n/a | 2 suy diễn wiring không gắn nhãn "chưa chắc" (setInterval/streak) | Overview L3 mở bằng vấn đề, bắt đúng "không Kafka" (ngược flawed-explain) |
| teen | pass | 3 | n/a | Thiếu Bước-6 (gợi ý bước tiếp) → tc6=1/2 | Feynman sạch, 0 jargon, 0 analogy, bám code streak.ts từng dòng |
| atlas | **fail** | 1 | n/a | **Chỉ 12/20 artifact** ("bản scaled đại diện") → A1=0 | Nội dung bám evidence từng dòng nhưng khuyết 8 mảnh xương → chưa làm nền chung được |

### meta (5 skill)
| skill | gate | eff | recall | top_failure | verdict |
|---|---|---|---|---|---|
| grade | pass | 3 | **3/3** (RỚT GATE bản bịa) | Nit: thêm 2 mục phụ ngoài khung phẳng | Dùng rubric thật của explain, RỚT GATE chính xác, phần bịa Kafka truy về code |
| traceability | pass | 3 | **4/4** (có G-1) | Nit: ~150 dòng hơi dài | Recall 4/4, còn bắt thêm mâu thuẫn state OQ-A (đã đóng ở ADR-007) không bịa |
| spar | pass | 3 | n/a | NONE | Đủ 4 file, giữ luật không-nhìn-trước, chấm cùng thước, bắt đúng race của user |
| skill-define | pass | 3 | n/a | Format "Trường hợp X:" thay vì "X -> làm gì" | 5 case bám nhu cầu, kết luận CHƯA-đáng ngả rõ, đối chiếu skill đã có |
| tune | **fail** | 1 | n/a | **DRY-RUN thiết kế**: 0 baseline, 0 variant, 0 grade.txt → rớt cả 3 gate | Thiết kế bám 7 bước nhưng dừng ở giấy; + khai sai "teen thiếu rubric" |

---

## 3. Bảng RECALL đáp án (5 skill có đáp án — MỤC QUAN TRỌNG NHẤT)

| # | skill | mục AK | BẮT được gì | THIẾU gì | Kết luận |
|---|---|---|---|---|---|
| A | **review** | 7 bug, buộc có BUG-5 | **7/7**: BUG-5 IDOR@dose.controller.ts:14 **Critical** ✓, BUG-4 error-path & BUG-3 dedupe & BUG-6 chia-0 → Critical; BUG-1 tz / BUG-2 endDate / BUG-7 mẫu-số → Medium. Grep xác minh canCaregiverView 0 caller. | Không thiếu bug nào. (BUG-1/2/7 để Medium — đúng thang, không phải miss) | **ĐẠT** — chuẩn "≥5/7 + buộc BUG-5" vượt xa; recall hoàn hảo. |
| B | **trace** | đường `status` + side-effect | **4/4 mắt xích**: pending@dose-generator → read due@reminder.service → taken@confirmDose → read@rateFor. Nêu đúng **mutate in-place trên shared in-memory db + db.reminders.push**. Bonus: phát hiện 'missed'/'skipped' khai báo mà 0 hàm ghi → streak chết. | Không thiếu (không bắt BUG-1/2/3/4 nhưng đúng — ngoài phạm vi trace state). | **ĐẠT** — khớp 100% đáp án B, có cả điểm side-effect bắt buộc. |
| C | **triage** | file legacy → xoá/archive | **1/1**: verdict "xoá (có kiểm soát)" + plan B "archive". Grep thật `old_reminder_cron\|OldCron` = 0 caller (chỉ 2 dòng định nghĩa trong chính file). Xác nhận reminder.worker.ts đã thay. | Thiếu **cổng-3-lối AskUserQuestion** (Bước 4 SKILL.md) — quy trình, không phải recall. | **ĐẠT** — verdict đúng đáp án C, có grep-verify caller như chuẩn đòi. |
| D | **traceability** | 4 gap, buộc có G-1 | **4/4**: G-1 thiếu uat.md/GĐ12 ✓ (verify find), G-2 ship 0/2 chữ ký ✓, G-3 hai open-Q OQ-A+OQ-B ✓, G-4 rollback chưa test ✓. Bonus: bắt OQ-A **thực ra đã đóng** ở tech-decision ADR-007 §5 trong khi ship/progress còn ghi treo → mâu thuẫn state thật. | Không thiếu. | **ĐẠT** — recall 4/4 buộc-có-G-1, còn vượt key bằng phát hiện mâu thuẫn state không bịa. |
| E | **grade** | bản explain cố ý lỗi | **3/3**: (1) **RỚT GATE** đúng như đòi (1/14); (2) rớt Bám-code do **bịa Kafka/microservice** — grep codebase kafka/microservice = 0 hit; (3) rớt Lời-văn/3-tầng do nhảy thẳng jargon. Bonus: bắt sai-mức (tên hàm ở L3) + thiếu "vấn đề trước/cho ai". | Không thiếu. | **ĐẠT** — dùng `explain/rubric.md` thật, RỚT GATE chính xác, mọi verdict "BỊA" truy về code. |

**Kết luận mục 3:** 5/5 skill có đáp án đều ĐẠT, không skill nào bỏ sót khuyết tật cài sẵn hay bịa phát hiện. Lõi phát hiện-lỗi (review/trace/triage) và lõi kiểm-soát (traceability/grade) là phần **chắc nhất** của bộ skill.

---

## 4. Skill RỚT gate / friction cao — chẩn đoán nguyên nhân

### RỚT GATE (3)

**`atlas` (code, fail, eff 1) — chẩn đoán: hành vi "scaled" tự chọn, NGHI lỗi SKILL.md.**
- Triệu chứng: chỉ sinh 12/20 artifact, `00_index.md:7` tự thú "chỉ sinh mẫu đại diện" → vi phạm thẳng luật cứng "Một lần, đầy đủ" → rubric A1=0 → rớt.
- Nguyên nhân **không phải thiếu input** (đã đọc 12/12 file source, bám evidence sạch) và **không phải mâu thuẫn convention** (ghi đúng `.ai-understanding/`). Đây là **agent tự quyết cắt scope** — hoặc SKILL.md không đủ cứng ở chỗ "20 artifact bất khả thương lượng kể cả repo nhỏ", hoặc fixture repo quá nhỏ (12 file) khiến 20 artifact cảm thấy thừa. **Cần soi SKILL.md**: có chỗ nào cho phép "scale theo repo" không? Có → mâu thuẫn nội tại; không → lỗi tuân thủ của agent.
- Phụ: thiếu ghi `state/current.json` (Bước 3) — cùng họ lỗi với charter.

**`charter` (pm, fail, eff 1) — chẩn đoán: bỏ Bước 6+7 (state plumbing), lệch convention đích.**
- Triệu chứng: 6 folder + constitution seed IDENTICAL (đẹp), nhưng `find current.json` = rỗng + không dòng trỏ MEMORY.md → rubric A1 (liệt `state/current.json` là mục gate) = 0.
- Nguyên nhân **lệch convention đích**: harness ghi `outputs/charter/mediremind2/` (sandbox), agent không ghi `state/current.json` vì **state là artifact toàn-cục NẰM NGOÀI outputs/<skill>/** — harness non-interactive không dựng sẵn `state/`. **Nửa lỗi harness** (không có `state/` để ghi), **nửa lỗi skill** (nên tạo `state/` nếu thiếu). Slug lệch (`mediremind2` vs `mediremind`) là dấu hiệu harness chạy lặp.

**`tune` (meta, fail, eff 1) — chẩn đoán: dry-run + tiền đề sai.**
- Triệu chứng: chỉ 1 file `design.md` tự khai "bản THIẾT KẾ (chưa chạy 5 variant)" → 0 baseline, 0 grade.txt → rớt cả 3 gate xương sống.
- Nguyên nhân kép: (1) **thiếu môi trường chạy thật** — tune cần spawn nhiều agent + gọi `grade` thật, harness single-shot không cho → lỗi HARNESS. (2) **tiền đề sai TRONG output**: "CẢNH BÁO CHẶN teen KHÔNG có rubric.md" trong khi `teen/rubric.md` đã tồn tại (9238 bytes) → **lỗi THẬT của agent** (không grep kiểm trước khi tuyên chặn), không đổ cho harness.

### FRICTION CAO nhưng PASS (2)

**`fanout` (pm, pass, eff 2) — DRY-RUN.** Bước 0-2 (lập kế-hoạch bundle) chạy sạch, nhưng Bước 3-5 (bung sub-agent song song THẬT + thu artifact + /checkpoint→/progress) chỉ mô tả template. **Lỗi HARNESS**: fanout tồn tại để điều phối chạy đồng thời — môi trường test single-agent không cho spawn thật. Nội dung trung thực, không bịa.

**`frame` (pm, pass, eff 2) — bịa id nguồn.** Đúng-trước-code + code-claim kiểm thật, nhưng **tự chế** `STORY-dose-ownership-guard`/`AC-dose-ownership-guard-1/2` và khai prefill từ "backlog.json GĐ9" — file không tồn tại; id thật là US-3.1.1/AC-1/AC-2. Thoát gate CHỈ nhờ dòng 36 minh bạch nêu id thật. **Lỗi THẬT của skill/agent** (Bước 1b cấm tự chế id) — không đổ cho harness.

---

## 5. Meta-findings xuyên skill

### Pattern lỗi do FIXTURE / MÔI TRƯỜNG TEST (không phải lỗi SKILL.md)
1. **Non-interactive nuốt vòng hỏi.** idea/delivery/triage/partner đều "tự trả CÓ" hoặc chạy một-lượt vì fixture batch, không có AskUserQuestion thật. Không skill nào lấn vai vì lý do này — nhưng làm mờ kỷ luật hỏi-trước.
2. **Single-agent chặn skill điều-phối.** fanout & tune rớt/friction vì cần spawn nhiều agent + gọi skill khác THẬT; harness single-shot không cho. Đây là **giới hạn cấu trúc của mô phỏng**, không phải khuyết SKILL.md.
3. **Không có `state/` toàn-cục.** charter (& phụ ở atlas) không ghi được `state/current.json` vì harness chỉ dựng `outputs/<skill>/`, không dựng `state/`. Nửa lỗi harness.
4. **Convention đích `outputs/<skill>/` vs path hợp đồng.** checkpoint ghi `outputs/checkpoint/delivery.md` thay vì `progress/checkpoints/T-11.md` — lệch path do sandbox, không phải bịa (nội dung tự nhận đúng là T-11).

### Pattern lỗi THẬT trong hành vi skill/agent (đáng sửa)
5. **Tự cắt scope / dry-run rồi tự khai.** atlas ("scaled 12/20") + tune ("thiết kế chưa chạy") — agent chọn làm bản rút gọn rồi thú nhận, thay vì làm đủ. Trung thực nhưng KHÔNG hoàn thành hợp đồng. **Đây là meta-lỗi trung tâm của vòng này.**
6. **Tự chế id / tiền đề sai không grep-verify.** frame bịa STORY-id + "backlog.json"; tune tuyên "teen thiếu rubric" khi rubric đã có. Cùng họ với meta-lỗi các vòng trước ("báo số từ run không tồn tại"). **Cần luật cứng: grep-verify tên file/id trước khi trích.**
7. **Suy diễn wiring không gắn nhãn "chưa chắc".** explain gán setInterval/streak "đã nối" khi call-site = 0. Không bịa file nhưng thổi phồng mức nối. Nhẹ.

### Điểm SÁNG xuyên skill (ngược với meta-lỗi cũ)
8. **Từ chối bịa khi thiếu bằng chứng — nhất quán.** uat (0/5 AC BLOCKED), ship (NO-GO), operate ("chưa có số"), skeleton (0/9 không tick khống), progress (giữ in_progress vì thiếu phiếu), partner (CASE-1 assumed). Đây là **hành vi fail-closed** mà các vòng review trước mong muốn — giờ đã có mặt.

---

## 6. TOP việc nên sửa (theo đòn bẩy) — tách harness khỏi skill

### A. SỬA HARNESS TEST (đòn bẩy cao nhất — mở khoá đánh giá đúng)
1. **Cho fanout & tune chạy đa-agent thật** (hoặc đánh dấu N/A "không đo được trong single-shot" thay vì FAIL). Hiện 2 rớt/friction này **không phản ánh chất lượng skill** mà phản ánh giới hạn mô phỏng.
2. **Dựng sẵn `state/` toàn-cục** trong sandbox để charter/atlas ghi `state/current.json` được → tách "lỗi state-plumbing thật" khỏi "không có chỗ để ghi".
3. **Cho vòng hỏi tương tác tối thiểu** (hoặc script sẵn câu trả lời) để đo đúng kỷ luật hỏi-trước của idea/frame/partner/triage, thay vì để chúng chạy một-lượt.
4. **Thống nhất path đích**: hoặc chấp nhận `outputs/<skill>/`, hoặc dựng cây path hợp đồng thật (`progress/checkpoints/…`) — để checkpoint không bị dock oan.

### B. SỬA SKILL (đòn bẩy thật, độc lập với test)
5. **atlas — siết luật "20 artifact bất khả thương lượng":** soi SKILL.md xem có chỗ nào cho phép "scale theo repo"; nếu có, xoá; thêm câu cứng "repo nhỏ vẫn phải đủ 20 file, mỗi file có thể ngắn nhưng KHÔNG bỏ". Đây là ca rớt gate DUY NHẤT có thể là mâu thuẫn SKILL.md.
6. **frame — luật cứng grep-verify id nguồn:** trước khi trích/tự chế id story/AC, PHẢI grep fixture; không thấy id → dùng id thật đã grep, cấm tự chế. (Bước 1b đã có, cần nâng thành gate.)
7. **tune — thêm bước grep-verify tiền đề "skill X thiếu rubric":** trước khi tuyên CHẶN, phải `ls <skill>/rubric.md`. Lỗi "khai sai rubric không tồn tại" là lỗi sự thật thuần.
8. **triage — nâng cổng-3-lối thành bắt buộc cho verdict non-trivial** (Bước 4 đang bị bỏ khi chạy batch).
9. **teen — thêm Bước-6 (gợi ý bước tiếp)** nếu muốn tc6 đạt 2/2; hiện luôn hụt.
10. **explain — luật gắn nhãn "(chưa chắc/suy diễn)" cho claim wiring không có call-site** (chống thổi phồng mức-nối).

**Ưu tiên:** A1–A2 (mở khoá fanout/tune/charter) trước, vì đang làm 3/3 ca "rớt gate" trông tệ hơn thực tế. Sau đó B5 (atlas — ca skill-thật khả nghi nhất), rồi B6–B7 (chống bịa id/tiền đề — meta-lỗi lặp qua nhiều vòng).

---

## 7. Giới hạn của cuộc thử (trung thực)

- **Đây là chạy MÔ PHỎNG, KHÔNG phải invoke skill thật.** Mỗi "skill" là một agent được đưa prompt trỏ vào `SKILL.md` tương ứng rồi làm theo, ghi ra `outputs/<skill>/`. Không có runtime skill thật, không có AskUserQuestion thật, không spawn sub-agent thật.
- **Hệ quả trực tiếp:** 3 skill vốn cần môi trường "sống" (fanout: spawn song song · tune: đa-variant + grade thật · charter: ghi state toàn-cục) bị đánh giá thấp KHÔNG hẳn vì SKILL.md kém, mà vì mô phỏng single-shot không tái tạo được điều kiện chạy của chúng. Đọc 3 verdict đó kèm ngữ cảnh này.
- **Recall (mục 3) đáng tin nhất** vì đo khách quan bằng đáp án cứng (bug/gap có file:line). Các eff=3 còn lại của pipeline dựa trên đối chiếu file:line với fixture — cũng vững — nhưng "hiệu quả" của skill điều-phối/hỏi-đáp chỉ đo được một phần.
- Chấm do một agent-grader đọc output + đối chiếu source; không có vòng review đối kháng thứ hai trên chính bảng chấm này.

---

_Đường dẫn: `/Users/uspro/Desktop/skillsh/experiments/skill-fake-test/REPORT.md`_
