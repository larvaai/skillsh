---
name: seed
description: 'Mở một project mới theo mô hình folder-là-project — dựng đủ 6 subfolder (problem/idea/progress/constitution/docs/codebase), chép constitution, nhận đề bài thô bằng giọng người trong nghiệp vụ, viết Bức tranh v0 và board khởi tạo. Là GĐ0 (Idea Intake) của bộ project-folder, bàn giao sang `meet` (GĐ1–4). Dùng khi "mở project mới", "có bài toán mới", "dựng khung project", "bắt đầu một dự án", "khách đưa một đề bài lớn", "setup folder project".'
---

# Seed — GĐ0: dựng khung project + nhận đề bài thô

`seed` mở màn bộ project-folder: một folder chứa TRỌN project (đề bài, ý tưởng, tiến độ, luật, tài liệu, code), để agent nào vào sau cũng đọc context từ folder và resume từ `progress/`. `seed` chỉ dựng khung + nhận đề bài — không phân tích, không đề giải pháp.

Phân vai — không lấn:
- `meet` = GĐ1–4, buổi họp làm rõ nghiệp vụ → PRD. `seed` KHÔNG hỏi sâu nghiệp vụ, chỉ ghi lại đề bài như user kể.
- Skill `idea` (bộ cũ) = phân loại một ý tưởng theo state riêng. `seed` thuộc bộ MỚI: mọi thứ nằm trong folder project, không ghi `state/project/`.
- Nội dung GĐ0 (Idea Brief): lấy khung từ `quy-trinh-idea-to-operate.md` mục GĐ0.

## Luật cứng

- **Một project = một folder dưới `projects/`.** Tên folder kebab-case, user chốt tên. Đã tồn tại → dừng, hỏi có phải resume không (nếu phải → gợi `pulse`).
- **Constitution chép nguyên từ template, không tự chế.** Template ở `assets/` của skill này. Sửa luật riêng cho project → khi Son gật, thường sau retro của `pulse`.
- **Đề bài ghi bằng lời user, không dịch sang ngôn ngữ kỹ thuật.** Được phép mơ hồ. Không ép cấu trúc, không hỏi quá 1 cụm câu hỏi để lấp chỗ trống hiển nhiên (tên project, đề bài, kỳ vọng thô).
- **Kỳ vọng thô phải nằm trên giấy NGAY ngày 0** — mục "Kỳ vọng ban đầu" trong `problem/00`: vài câu bằng lời Son, "thế nào là ưng ý / thế nào là xong". Ghi TRƯỚC khi agent kịp gợi ý gì — đây là mỏ neo mà `meet` sẽ mài thành K1..Kn và `gate` sẽ đối chiếu cuối cùng. Mơ hồ cũng ghi, không bỏ trống.
- **Bức tranh v0 mơ hồ CÓ CHỦ ĐÍCH:** chỉ viết cái đã biết + cái còn mờ. Không đoán giải pháp. Có dòng "So kỳ vọng" ngay từ v0.
- **Kết phiên đủ 4 món** theo resume protocol: artifact + board + journal + bức tranh.

## Các bước

1. **Hỏi 1 cụm:** tên project; đề bài là gì (kể tự nhiên, càng đời thường càng tốt); và **thế nào là ưng ý** — cuối cùng muốn tận mắt thấy cái gì. User đã kể sẵn trong prompt → không hỏi lại.
2. **Dựng khung** `projects/<ten>/`:
   - `constitution/00-luat.md` ← chép `assets/constitution.md`, điền tên project.
   - `problem/00-de-bai.md` ← lời kể của user, giữ nguyên giọng + mục **Kỳ vọng ban đầu** (thô); cuối file ghi nguồn (ai kể, ngày). `problem/goc/` ← file/data user đưa kèm, chỉ-thêm.
   - `progress/decisions.md` ← chép `assets/decisions-mau.md`; `progress/risks.md` ← chép `assets/risks-mau.md`; ẩn số đã lộ ngay trong đề bài → mỗi cái 1 dòng risks luôn.
   - `idea/_mau.md` ← chép `assets/idea-mau.md`. Nếu trong lời kể đã lóe ý tưởng → mỗi ý 1 file `idea/<slug>.md` trạng thái `tho`, đủ input/output/ẩn số ở mức đoán được.
   - `docs/00-buc-tranh.md` ← theo `assets/buc-tranh-mau.md`, viết v0.
   - `progress/board.md` ← chép `assets/board.md` (T01 done, T02 ready, còn lại todo theo chuỗi phụ thuộc); `progress/journal.md` ← 1 dòng đầu tiên.
   - `codebase/.gitkeep`.
3. **Đọc lại cách hiểu** — đề bài + kỳ vọng bằng lời mình (3–5 câu). Đây không phải xin duyệt: đây là lần so mỏ neo ĐẦU TIÊN — lệch ngay từ đây thì mọi thứ sau lệch theo. Son sửa gì → sửa thẳng vào `problem/00`.
4. **Bàn giao:** chỉ ra T02 đang `ready`, gợi chạy `meet`. Không tự chạy.

## Artifact của phiên

`problem/00-de-bai.md` (đề bài + kỳ vọng thô) + `constitution/00-luat.md` + `docs/00-buc-tranh.md` (v0) + `progress/board.md` + `journal.md` + `decisions.md` + `risks.md` (+ `idea/*.md`, `problem/goc/` nếu có).
