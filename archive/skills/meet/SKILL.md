---
name: meet
description: 'Buổi họp business↔tech trên một project-folder — business kể việc chân tay hàng ngày và pain, tech hỏi để lượng hoá, brainstorm mỗi pain thành ý tưởng, rồi chốt PRD + bộ kỳ vọng đo được. Chạy GĐ1–4 MỘT MẠCH (Business Case → Product Brief → Requirements → PRD), kết bằng điểm chốt 1/4. Dùng khi "họp làm rõ vấn đề", "làm rõ nghiệp vụ", "mô tả việc hàng ngày", "chốt business case", "viết PRD", "làm rõ yêu cầu", "vấn đề còn mơ hồ, hỏi tôi đi", "từ vấn đề ra ý tưởng".'
---

# Meet — GĐ1–4: làm rõ WHY → WHAT, ra ý tưởng, chốt PRD + kỳ vọng

`meet` mô phỏng buổi họp mà business mô tả vấn đề và việc hàng ngày, tech cùng bàn làm sao thay việc chân tay nhiều pain đó. Vào bằng đề bài + kỳ vọng thô (`problem/00`), ra bằng PRD + K-list đo được. Đây là mắt xích "vấn đề → ý tưởng" trong vòng đời một ý (constitution).

Chạy **một mạch, không dừng xin phép giữa chừng**: mỗi GĐ xong vẫn ghi artifact + journal ngay (để vòng lại rẻ), nhưng chỉ dừng chờ Son đúng MỘT lần — điểm chốt 1/4 ở cuối. Son nhảy vào chỉnh giữa chừng lúc nào cũng được.

Phân vai: `seed` đã nhận đề bài — không hỏi lại từ đầu. `sketch` lo domain/kiến trúc — `meet` không bàn giải pháp kỹ thuật; ý giải pháp lóe ra → ghi `idea/`, quay lại mạch họp. Khung nội dung GĐ1–4: `quy-trinh-idea-to-operate.md` mục tương ứng.

## Luật cứng

- **Bước 0 resume** theo constitution: luật → board + đuôi journal + rủi ro `mo` → `problem/00` (đề bài + kỳ vọng thô). Board cho thấy GĐ1–4 xong phần nào → làm tiếp, không làm lại.
- **Hỏi như người thật trong họp, không như form.** Mạch: một ngày diễn ra thế nào → việc nào lặp lại, mất bao lâu, mấy người → sai/đau nhất ở đâu, sai thì chuyện gì xảy ra → con số (đơn/ngày, giờ/tuần) → công cụ đang dùng. Mỗi lượt ≤3 câu cùng chủ đề. File/data Son đưa trong lúc họp → cất `problem/goc/`.
- **Không bịa số.** Số chưa có → 1 dòng `risks.md` ("chưa đo, cách kiểm rẻ nhất: X"), không chế ngưỡng.
- **Mỗi pain lớn → ít nhất 1 ý thô** vào `idea/<slug>.md` (đủ input/output/ẩn số) ở cuối GĐ1 — đây chính là chỗ vấn đề đẻ ra ý tưởng, không chờ ý "tự lóe".
- **Ẩn số lộ ra ở GĐ nào → `risks.md` ngay.** Lựa chọn phạm vi (đưa vào / để sau / loại) → `decisions.md` 1 dòng, đi tiếp.
- **Artifact 1 trang,** mở bằng 2–3 câu cho Son-sau-2-tuần đọc là nắm.

## Các bước — một mạch 4 giai đoạn

1. **GĐ1 — Nghiệp vụ + Business Case.** Hỏi theo mạch, ghi `problem/01-nghiep-vu.md`: ngày điển hình, việc chân tay lặp lại (việc → ai → bao lâu → sai kiểu gì), pain xếp theo độ đau, con số. Rồi `docs/10-business-case.md`: vì sao đáng làm, không làm thì mất gì, đo "ưng ý" bằng gì. Kết GĐ1: brainstorm pain → ý thô vào `idea/`.
2. **GĐ2 — Product Brief** → `docs/11-product-brief.md`: ai dùng, trải nghiệm cốt lõi thay việc chân tay nào, non-goals ≥3 (chống lệch scope về sau), cảm nhận "đỡ đau" trông thế nào.
3. **GĐ3 — Requirement Catalogue** → `docs/12-requirements.md`: FR đánh số bám từng việc chân tay GĐ1 (FR-x ↔ việc y, truy vết được), NFR có số, ẩn số treo → `risks.md`.
4. **GĐ4 — PRD + K-list** → `docs/13-prd.md`: phạm vi bản đầu, ưu tiên, ẩn số mang theo, và **mài kỳ vọng thô trong `problem/00` thành K1..Kn đo được** — mỗi phần phạm vi map về K nào. K nào không phần nào phục vụ, hoặc phần nào không phục vụ K nào → lộ lệch ngay tại đây.
5. **ĐIỂM CHỐT 1/4** — trình MỘT khối: vấn đề (3 câu) → phạm vi + non-goals → K1..Kn → ẩn số mang theo → ý đã gác. Son ưng → `decisions.md` 1 dòng, T02 `done`, T03 `ready`, bức tranh v1 (kèm dòng "So kỳ vọng"), bàn giao `sketch`. Son chỉnh → sửa tại chỗ, chốt lại trong cùng phiên.

## Artifact của phiên

`problem/01-nghiep-vu.md`, `docs/10..13`, `idea/*.md` từ pain, dòng mới trong `risks.md` + `decisions.md`, bức tranh v1, board + journal.
