# TUNE — skill `stack` (từ chấm 07-stack, gói rebuild-hex-agent)

> Thước: `/Users/uspro/Desktop/skillsh/experiments/hex-rebuild-review/rubrics/07-stack.rubric.md`
> Grade nguồn: `/Users/uspro/Desktop/skillsh/experiments/hex-rebuild-review/grades/07-stack.grade.md` (11/14, GATE đạt)
> SKILL đang sửa: `/Users/uspro/Desktop/skillsh/.claude/skills/stack/SKILL.md`

## §0 Chẩn đoán (≤6 câu)

Artifact được 11/14, mất điểm ở 3 tiêu chí: **1 BẰNG CHỨNG (1)**, **2 MA TRẬN CÓ ĐIỂM (1)**, **5 GÓC NHÌN LÃNH ĐẠO (1)**; hai cái đầu bị đúng MỘT gốc lỗi — 6/6 ma trận có TỔNG lệch Σ(trọng số×điểm) (14/16 ô candidate sai) cộng footnote §5 "none thắng trên tiêu chí áp dụng được" là SAI số (60 < Qdrant 62).
Lỗi số học **thuộc SKILL.md**: template ghi "TỔNG (có trọng số)" và mục 0 tuyên "TỔNG = Σ(trọng số × điểm)" nhưng KHÔNG có luật/bước nào buộc agent CỘNG LẠI để tự kiểm — skill để trần một phép tính rồi tin agent làm đúng bằng tay (một agent cẩn thận vẫn dễ lệch khi có 6 bảng × 8 dòng).
Footnote §5 cũng thuộc SKILL: skill có luật "không bịa candidate" và "ràng buộc ép → 1 dòng" nhưng THIẾU luật xử lý ô "—" (tiêu chí không áp dụng cho candidate này) — agent bịa ra một TỔNG "applicable-only" rồi tuyên thắng bằng điểm, trong khi lẽ ra phải chốt bằng lý do YAGNI/ràng-buộc.
Lỗi jargon ở tiêu chí 5 **nửa-SKILL nửa-run**: SKILL có luật "Góc nhìn lãnh đạo… ngôn ngữ nghiệp vụ, không jargon" và ví dụ tốt, nhưng luật nằm ở tầng nguyên tắc, KHÔNG có checklist "cấm tên công nghệ trong dòng Chọn gì" nên agent vẫn nhét "SSE một chiều / OpenAI-compatible JSON-mode / property-based / audit-test" vào ngay khối mở.
Kết luận: **phần lớn lỗi mất điểm là lỗi-của-SKILL** (thiếu luật tự-kiểm số học, thiếu luật ô "—", luật chống-jargon quá mềm) → tune được; không phải agent chạy ẩu cá biệt.

## §1 Fixture đề xuất (cố định cả thí nghiệm)

- **Skill tune**: `stack` (GĐ7).
- **Project/fixture chính**: `rebuild-hex-agent` — chạy `stack` với đầu vào Architecture Brief GĐ6 = `rebuild-hex-agent/pipeline/06-shape.md` + anchor `00-understanding/REBUILD-BRIEF.md`, `evidence-A/B/C`, `ATLAS.md`. Đây là brownfield-informed rebuild của repo `/Users/uspro/Desktop/namnson/hex_agent`.
- **Tham số cố định (một biến duy nhất = bản sửa SKILL)**:
  - chế độ: tự-quyết (đóng vai Kiến trúc sư/Tech-lead + CTO duyệt, không hỏi user) — GIỮ NGUYÊN như artifact gốc.
  - hạng mục phải chốt: đúng 7 ô như artifact gốc (lang · graph · checkpoint · LLM adapter · vector · transport · test) để mọi bản sinh cùng số bảng, so được.
  - thang điểm: 1–5, trọng số không đều, TỔNG = Σ(trọng số×điểm) — giữ y hệt để lỗi số học lộ ra chỗ cũ.
  - level diễn giải: lấy từ user-state nếu có; không có → L4, ghi rõ.
- **Fixture thứ hai (cho Bước 5 confirm, chống over-fit)**: một case greenfield KHÁC hẳn brownfield — ví dụ Case Management ở §ví-dụ của SKILL (modular monolith, NestJS/PostgreSQL, NFR P95<500ms). Chọn nó vì có ma trận nhiều cột + có NFR-số thật → kiểm được luật tự-kiểm-số-học VÀ luật chống-jargon trên bối cảnh không-brownfield.
- Ghi 3 hằng số (project, level, chế độ tự-quyết) ra `experiments/runs/<ts>/fixture.txt`; mọi variant đọc đúng file này.

## §2 Thước

- Dùng nguyên `/Users/uspro/Desktop/skillsh/experiments/hex-rebuild-review/rubrics/07-stack.rubric.md` (7 tiêu chí 0/1/2; xương sống = 1, 2, 7).
- **Luật xếp hạng**: (1) LOẠI hết bản rớt gate trước (bất kỳ tiêu chí 1/2/7 = 0); (2) còn lại xếp theo TỔNG /14; (3) hoà TỔNG → bản có diff NHỎ/robust hơn thắng (sửa ít, ít over-fit vào đúng fixture này).
- Chấm mù: người chấm chỉ thấy {project, level, chế độ, output.txt}, KHÔNG thấy variant theo hướng nào.

## §3 Các hướng thử A/B/C/D (mỗi hướng nhắm MỘT tiêu chí khác nhau)

### Hướng A — Bước tự-kiểm số học TỔNG (nhắm tiêu chí 2 MA TRẬN CÓ ĐIỂM, chạm 1)

**Giả thuyết**: nếu skill buộc agent cộng lại từng TỔNG = Σ(trọng số×điểm) và sửa trước khi ghi, 14/16 ô lệch biến mất → tiêu chí 2 từ 1→2 và tiêu chí 1 hết chỗ "số không khớp công thức đã tuyên".

**DIFF** — thêm vào cuối mục "### 2. Tech Decision Matrix" (sau đoạn "Không bịa candidate cho đủ 3 cột."):
```
**Kiểm số học TỔNG (bắt buộc trước khi ghi).** Với MỖI bảng, tính lại TỔNG = Σ(trọng số × điểm) cho TỪNG candidate, đối chiếu con số bạn định ghi. Lệch một ô = phải sửa con số, KHÔNG ghi ra bảng có TỔNG không bằng công thức đã tuyên — đó là con số không truy về nguồn (rớt tiêu chí BẰNG CHỨNG), dù không đổi thứ hạng. Sau khi khớp, kiểm lần cuối: winner mỗi bảng có đúng là candidate TỔNG cao nhất không.
```

**Rủi ro**: agent có thể "kiểm cho có" rồi vẫn cộng sai — phải kiểm output thật ở Bước 4 bằng cách tự cộng lại 1-2 bảng bất kỳ, không tin lời agent tuyên "đã kiểm".

### Hướng B — Luật xử lý ô "—" (không-áp-dụng) & cấm tuyên thắng-bằng-điểm cho candidate ràng-buộc-ép (nhắm tiêu chí 1 BẰNG CHỨNG)

**Giả thuyết**: nếu skill cấm bịa "TỔNG applicable-only" rồi tuyên thắng bằng điểm cho ô có tiêu chí "—", footnote §5 sai số biến mất → tiêu chí 1 từ 1→2 (đây là lỗi số học nặng nhất trong grade).

**DIFF** — thêm một gạch đầu dòng vào "## Luật cứng" (ngay dưới luật "Chọn bằng tiêu chí có điểm"):
```
- **Candidate có tiêu chí KHÔNG áp dụng (ô "—") → KHÔNG được cộng "TỔNG áp-dụng-được" rồi tuyên thắng bằng điểm.** TỔNG chỉ so được giữa các candidate cùng bộ tiêu chí. Khi một lựa chọn thắng vì YAGNI/ràng-buộc-GĐ6 (vd "none cho MVP") → ghi thẳng lý do RÀNG BUỘC, để TỔNG của nó là "n/a" hoặc bỏ trống, tuyệt đối không thổi số để đỡ lựa chọn. Con số bịa để biện minh = claim không truy về nguồn (rớt BẰNG CHỨNG).
```

**Rủi ro**: chạm nhẹ cách trình bày bảng vector (§5) — agent có thể chuyển thành bỏ hẳn candidate "none" khỏi ma trận; cần nhắc: vẫn liệt kê "none" như một lựa-chọn-mặc-định, chỉ đổi phần TỔNG+footnote.

### Hướng C — Checklist chống-jargon cho dòng "Chọn gì" của Góc nhìn lãnh đạo (nhắm tiêu chí 5)

**Giả thuyết**: nếu skill nêu rõ "dòng Chọn gì cấm tên công nghệ trần — dịch sang chức năng nghiệp vụ, tên kỹ thuật để trong ngoặc/hạ xuống ma trận", jargon ("SSE một chiều", "OpenAI-compatible JSON-mode", "property-based") không lọt khối mở → tiêu chí 5 từ 1→2.

**DIFF** — thêm vào khối "### Góc nhìn lãnh đạo — VIẾT ĐẦU artifact", ngay dưới template ```Chọn/Vì sao/Đã loại/Rủi ro```:
```
Luật viết dòng "Chọn": nói CHỨC NĂNG nghiệp vụ trước, tên công nghệ chỉ để trong ngoặc và tối đa 1 lần. CẤM trong 4 dòng này các cụm chỉ dev hiểu: tên giao thức/thư viện đứng trần (SSE, WebSocket, JSON-mode), tên kỹ thuật test (property-based, fuzz), thuật ngữ kiến trúc nội bộ (adapter, seam, checkpointer). Vd ĐÚNG: "kênh cập nhật realtime một chiều (SSE)"; SAI: "SSE một chiều". Nếu buộc phải nêu tên → thêm 3–5 chữ giải nghĩa nghiệp vụ liền sau.
```

**Rủi ro**: over-correct → khối mở loãng, dài quá khung scan 30–60s (rơi vào level-1 vế "dài vượt khung"). Chấm phải kiểm cả độ dài, không chỉ độ sạch jargon.

### Hướng D — Bảng "self-audit số + jargon" ở mục "Tự soi trước khi chốt" (nhắm tiêu chí 1, gộp phòng-thủ cả 2 lỗi số học)

**Giả thuyết**: thêm một câu tự-soi thứ 4 buộc agent đối chiếu MỌI con số hiển thị với nguồn/công thức trước khi chốt sẽ chặn CẢ lỗi TỔNG lệch (A) LẪN footnote §5 (B) bằng một điểm kiểm duy nhất → tiêu chí 1 từ 1→2, có thể kéo theo 2.

**DIFF** — thêm gạch đầu dòng thứ 4 vào "## Tự soi trước khi chốt":
```
- **Mọi CON SỐ hiển thị có khớp nguồn/công thức không?** Cộng lại từng TỔNG = Σ(trọng số×điểm); mọi số "áp-dụng-được"/"thắng bằng điểm" cho ô có tiêu chí "—" phải bỏ (chuyển sang lý do ràng-buộc); mọi con số NFR/số-test phải có anchor file:line hoặc gắn nhãn open-Q. Còn một số không truy về được → sửa trước khi ghi, đừng để GĐ8 dựng skeleton trên số ma.
```

**Rủi ro**: TRÙNG phạm vi với A + B (cùng nhắm lỗi số học) — nếu chạy cả A, B, D thì D là biến-thể "gộp một điểm kiểm" so với "hai luật rời"; chỉ đáng giữ D nếu muốn so *đặt-luật-ở-đâu* (thân template vs mục tự-soi) hiệu quả hơn. Nếu muốn 4 hướng tiêu chí KHÁC nhau hoàn toàn thì bỏ D, giữ A/B/C.

> Gợi ý ghép ở Bước 6: A (số học ma trận) + B (ô "—") + C (jargon) nhắm ĐỦ 3 tiêu chí mất điểm mà không chồng lấn; D chỉ để trả lời câu phụ "gộp vào tự-soi có gọn hơn hai luật rời không".

## §4 Ưu tiên

**TUNE NGAY.** Lý do: (1) 2/3 tiêu chí mất điểm (1 và 2, đều XƯƠNG SỐNG) do đúng một gốc lỗi-của-SKILL là để-trần phép tính TỔNG mà không có bước tự-kiểm — fix rẻ, một luật ngắn, tác động lên chính hai tiêu chí gate; (2) footnote §5 "thắng bằng điểm" là kiểu lỗi số-bị-thổi-để-đỡ-lựa-chọn có thể tái diễn ở mọi artifact có ô "—", đáng đóng luật lại; (3) grade tuy 11/14 nhưng lỗi lặp-được (mọi lần chạy có nhiều ma trận đều dễ dính) chứ không phải run-ẩu cá biệt → sửa SKILL có đòn bẩy.

## §5 Nhắc luật thí nghiệm

- **Chấm mù**: mọi output.txt chấm chỉ với {project, level, chế độ, output}, giấu nhãn hướng A/B/C/D — tránh thiên vị hướng mình kỳ vọng.
- **Baseline trước**: chạy `stack` HIỆN TẠI trên fixture chính → `runs/<ts>/baseline/output.txt`, chấm bằng rubric → `baseline/grade.txt` (kỳ vọng tái hiện ~11/14). Không có baseline thì không biết "12/14" là tiến hay lùi.
- **Một biến duy nhất**: mọi variant cùng fixture (§1), chỉ khác bản sửa SKILL; mỗi agent đóng vai đúng `proposed-SKILL.md` của mình, KHÔNG bản gốc.
- **Confirm bản thắng bằng agent MỚI + fixture thứ hai**: lấy `proposed-SKILL.md` bản thắng, agent mới chạy trên (a) fixture chính rebuild-hex-agent VÀ (b) fixture greenfield Case Management (§1). Hơn baseline ở CẢ HAI → điểm đến từ SỬA, đáng merge; chỉ hơn ở fixture gốc → mùi over-fit (vd luật số học chỉ giúp khi có sẵn 6 bảng), xem lại diff.
- **Tự kiểm khi chấm A/D**: đừng tin agent tuyên "đã cộng lại"; người chấm tự cộng lại 1–2 TỔNG bất kỳ trong output để xác nhận số học thật khớp.
