# TUNE — skill `review` (fixture: gói rebuild-hex-agent, artifact REVIEW.md)

Bản chấm cuối: 12/14, GATE ĐẠT (xương sống 2·3·6 đều = 2). Chỉ rớt điểm ở **tiêu chí 5 (PHÂN MỨC = 1)** và **tiêu chí 7 (ĐÚNG VAI = 1)**. Cả hai đều là lỗi-của-SKILL, tune được.

---

## §0 Chẩn đoán (≤6 câu)

Artifact mất điểm ở đúng hai tiêu chí: **5 (PHÂN MỨC)** vì chèn tier tự chế "🟠 High" giữa Critical/Med, bỏ hẳn "Low", và không khai một câu ánh xạ "High → thang hợp đồng"; **7 (ĐÚNG VAI)** vì gần như MỌI gap có mục "Gợi ý sửa" đi vào thiết-kế-cơ-chế-thay-thế (đặt error code `WRITE_TOOL_ENABLED_WITHOUT_REDACTION`, provenance schema, per-node stuck-counter, gán owner Execution-Core) — vượt mức trỏ-việc.
Cả hai là **lỗi-của-SKILL**, không phải lần-chạy ẩu: (5) SKILL.md chỉ định nghĩa Critical/Medium/Low (dòng 78-81), KHÔNG có luật cấm tier tự chế hay buộc khai ánh xạ → agent tự bịa "High" trong khoảng trống luật; (7) luật "Không đề xuất fix" chỉ một dòng mờ (dòng 15), lại còn trỏ skill `plan` KHÔNG tồn tại trong hệ, và format báo cáo Bước 3 không vẽ ranh giới đâu-là-báo-cáo-đâu-là-fix → agent đọc `<điều thiếu> → <hậu quả>` như giấy phép thêm "gợi ý sửa" mỗi gap.
Lỗi lần-chạy CÓ nhưng nhỏ và không mất điểm rubric (cổng tự-phong GO/NO-GO ở chế độ tự-quyết đã bị grade loại đúng, không tính là bằng chứng) — phần lớn điểm mất thuộc SKILL, nên đáng tune.

## §1 Fixture đề xuất (cố định cả thí nghiệm)

- **project**: `/Users/uspro/Desktop/namnson/hex_agent` (code gốc để đối chiếu neo) + gói thiết kế rebuild `/Users/uspro/Desktop/skillsh/rebuild-hex-agent/` (artifact `05-idea-domain`, `06-shape`, `08-skeleton`, `10-modules` + `00-understanding/REBUILD-BRIEF.md` + `evidence-A/B/C`).
- **đối tượng review**: vòng lặp plan→order→delegate→judge→finish + budget/resume/redaction, qua đúng 4 artifact 05/06/08/10 (y hệt lần chạy đã chấm).
- **level**: L6+ (theo description skill).
- **mode**: tổng thể (edge → error → permission, chạy đủ ba trục theo thứ tự).
- **chế độ chạy**: tự-quyết, KHÔNG hỏi user (như lần gốc, để so cùng điều kiện).
- Ghi 3 hằng số (project, level=L6+, mode=tổng thể) ra `experiments/runs/<ts>/fixture.txt`. Mọi variant đọc đúng file này; không đổi giữa chừng.

## §2 Thước

- Rubric: `/Users/uspro/Desktop/skillsh/experiments/hex-rebuild-review/rubrics/review.rubric.md` (7 tiêu chí 0/1/2; xương sống = 2·3·6).
- Luật xếp hạng: **loại hết bản rớt gate (bất kỳ tiêu chí 2/3/6 = 0) TRƯỚC, rồi mới xếp phần còn lại theo TỔNG**; hoà tổng → bản có diff nhỏ/robust hơn thắng (ít rủi ro over-fit).
- Baseline = REVIEW.md hiện tại = 12/14, gate đạt. Variant phải ≥ 12 và KHÔNG được kéo tụt tiêu chí xương sống mới đáng theo.

## §3 Hướng thử A/B/C/D (mỗi hướng nhắm ĐÚNG MỘT tiêu chí khác nhau)

### Hướng A — Khoá thang mức, cấm tier tự chế (nhắm tiêu chí 5)
**Giả thuyết:** nếu SKILL.md nêu rõ chỉ dùng đúng 3 mức và buộc khai ánh xạ khi muốn bậc trung gian, agent sẽ không bịa "High" trần → tiêu chí 5 lên 2.
**DIFF (thêm vào mục "Mức độ" cuối Bước 3, sau dòng 81):**
```
Chỉ dùng ĐÚNG ba mức Critical / Medium / Low — không tự chế bậc mới (High, P0…).
Nếu buộc phải tách trong một mức, KHÔNG thêm tier: dùng thứ tự liệt kê + một câu
"[Medium — đầu-nặng]" và khai ánh xạ về ba mức gốc. Mỗi gap đọc mức là đoán được
loại hậu quả (Critical = mất data / breach / lỗi prod; Medium = hành vi sai không crash;
Low = thiếu sót nhỏ / UX / inconsistency). Không bỏ trống mức Low: gap nhỏ vẫn xếp Low.
```
**Rủi ro:** ép về 3 mức có thể làm 5 gap "High" gốc dồn hết vào Medium, mất sắc thái ưu tiên → tiêu chí 6 (thứ tự làm) hơi mờ; theo dõi 6 không tụt.

### Hướng B — Vẽ ranh giới báo-cáo vs fix, bỏ "Gợi ý sửa" (nhắm tiêu chí 7)
**Giả thuyết:** nếu SKILL.md cấm rõ mục "gợi ý sửa/cơ chế thay thế" và chỉ cho trỏ-skill, agent thôi thiết-kế-hộ → tiêu chí 7 lên 2.
**DIFF (thay dòng 15 + thêm ngay dưới):**
```
- Không đề xuất fix — chỉ báo cáo những gì tìm thấy. Fix là việc của skill build (`/frame`).
  CẤM mục "Gợi ý sửa" / cơ chế thay thế / error code tự đặt / schema / gán owner trong mỗi gap.
  Được phép: một dòng "Đóng ở đâu → /frame slice <tên>" (trỏ VIỆC, không thiết kế cách làm).
  Ranh giới: mô tả ĐIỀU THIẾU + HẬU QUẢ là báo cáo; mô tả CÁCH SỬA (thêm counter/field/gate cụ thể)
  là lấn vai build → bỏ.
```
**Rủi ro:** cắt "gợi ý sửa" có thể làm vài gap mất một phần lý-do-là-Critical đang nằm trong đó → theo dõi tiêu chí 3 (kịch bản phá) và 5 không tụt; nếu tụt, chuyển lý-do đó lên phần "điều thiếu/hậu quả".

### Hướng C — Sửa handoff sai skill (nhắm tiêu chí 7, trục khác B)
**Giả thuyết:** dòng 15 + Bước 4 trỏ skill `plan` KHÔNG tồn tại; sửa mọi handoff về skill CÓ THẬT (`/frame`, `/backlog`) giữ tiêu chí 6/7 không rớt vì "trỏ nơi xử lý không tồn tại" (rubric 6 score-0) và củng cố vai.
**DIFF (Bước 4, dòng 86 & 89, và dòng 15):** đổi mọi `plan` → `/frame` (Critical → build) và thêm nhánh `/backlog` cho High/Med:
```
- Có gap Critical: "Lên kế hoạch fix theo ưu tiên?" → gợi ý `/frame` (từng slice).
- High/Medium/Low còn lại: "Mang vào backlog vòng kế?" → gợi ý `/backlog`.
- Không tìm thấy gap: … → gợi ý review phần khác (KHÔNG trỏ `plan`).
```
**Rủi ro:** C trùng-vùng tiêu chí 7 với B; chạy song song để tách ĐÓNG-GÓP của "bỏ gợi-ý-sửa" (B) khỏi "sửa handoff" (C) — nếu cả hai đều nâng 7 thì merge cả hai, đừng coi là trùng phí.

### Hướng D — Chốt format báo cáo Bước 3 làm khuôn cứng (nhắm tiêu chí 5+7 qua CẤU TRÚC, không qua luật)
**Giả thuyết:** nếu khối format Bước 3 in sẵn đúng ba nhãn mức và KHÔNG có ô "gợi ý sửa", agent điền theo khuôn thay vì tự bịa → nhấc cả 5 và 7 bằng đòn bẩy cấu-trúc thay vì văn-luật.
**DIFF (thay khối template dòng 62-76):** template mỗi gap cố định đúng bốn ô `[Critical|Medium|Low] <file · dòng/symbol> — <điều thiếu> → <hậu quả>` + một ô cuối `Đóng ở đâu: /frame slice <tên>`; bỏ hoàn toàn chỗ cho "gợi ý sửa"; ba khối mức in sẵn nhãn Critical/Medium/Low (không có High).
**Rủi ro:** đòn bẩy cấu-trúc mạnh nhưng có thể over-fit khuôn cho fixture này; ở Bước 5 phải confirm trên fixture thứ hai (project khác) xem khuôn còn hợp không.

*Ghi chú phân vai hướng:* A nhắm 5; B & C nhắm 7 (hai cơ chế khác nhau — B cắt nội-dung-lấn, C sửa-trỏ-sai); D là cách khác (cấu-trúc) tấn công cùng 5+7 để so văn-luật vs khuôn-cứng. Không hướng nào trùng-cơ-chế; nếu muốn tiết kiệm agent, gộp thành 3 (A, B+C, D).

## §4 Ưu tiên

**Tune ngay** — nhưng nhẹ, ưu tiên B+C rồi A. Grade đã cao (12/14) và gate đạt, nên đây là mài đỉnh chứ không cứu skill; hai điểm mất đều là lỗi-của-SKILL rẻ để đóng (một luật cấm tier tự chế + một luật cấm "gợi ý sửa" và sửa handoff `plan`→`/frame`), nên đáng làm một vòng ngắn để lên 14/14, không đáng làm nhiều vòng.

## §5 Nhắc luật thí nghiệm

- **Chấm mù:** người/agent chấm chỉ thấy {project, level=L6+, mode=tổng thể, output.md}, KHÔNG thấy variant theo hướng nào.
- **Baseline trước:** REVIEW.md hiện tại = 12/14 (gate đạt) là mốc; mọi variant phải ≥ 12 VÀ không kéo tụt tiêu chí xương sống mới đáng theo.
- **Một biến duy nhất:** mọi variant chạy trên cùng fixture §1, chỉ khác ở diff SKILL.md của nó; không đụng `review/SKILL.md` thật cho tới khi có bản thắng qua confirm.
- **Confirm bản thắng bằng agent MỚI + fixture thứ hai:** chạy lại proposed-SKILL.md bản thắng trên (a) fixture gốc và (b) một artifact review khác (project thứ hai). Chỉ hơn ở fixture gốc = mùi over-fit (đặc biệt cảnh giác hướng D khuôn-cứng) → xem lại diff trước khi merge.
