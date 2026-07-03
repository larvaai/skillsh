---
name: spar
description: "Trao đổi qua FILE thay vì chat trên màn hình. Bạn và Claude cùng trả lời một prompt, rồi Claude chấm cả hai và góp ý cho bạn. Vòng lặp: Claude tạo prompt (có status) → bạn tự trả lời trước vào user-output rồi đổi status thành user-answered → Claude kiểm status, chỉ khi đó mới viết claude-output cạnh đó → Claude viết grade-output chấm điểm output của bạn và của Claude, kèm góp ý cho output của bạn. Dùng khi: 'chat qua file', 'luyện trả lời rồi so với Claude', 'tự trả lời trước rồi chấm', 'spar', 'đấu tập qua file', 'chấm bài của tôi', 'trao đổi qua file thay vì gõ chat'."
---

# Spar — trao đổi & luyện trả lời qua file

`spar` biến một prompt thành một vòng luyện trên đĩa: bạn trả lời trước, Claude trả lời sau, rồi Claude chấm cả hai bản và góp ý cho bản của bạn. Không gõ đáp án trên chat — mọi thứ nằm trong file, chat chỉ còn một dòng báo "xong, mở file X".

Giá trị nằm ở thứ tự: bạn phải tự nghĩ TRƯỚC khi thấy bản của Claude. Thấy đáp án trước thì bạn chỉ gật gù, không học được gì. Nên luật xương sống của skill này là: **Claude không viết claude-output khi bạn chưa trả lời** — đó là lý do skill tồn tại, không bao giờ bỏ.

## Phân vai — spar khác gì các skill khác

`grade` chấm riêng một câu của skill `explain`, theo rubric của explain. `spar` là vòng lặp chung: prompt bất kỳ, có thêm bản của bạn để chấm và coach. Hai bên dùng chung triết lý chấm (khung cố định, có gate) nhưng rubric khác nhau — spar có `rubric.md` riêng, chấm chung.

`spar` KHÔNG phải một giai đoạn của pipeline Idea→Operate. Nó là công cụ luyện/trao đổi, chạy độc lập, không nhận bàn giao từ skill nào, không ghi vào `state/project/.../pipeline`.

## Giao thức file — một round, bốn file

Mỗi round là một thư mục. Mặc định đặt trong `spar/<round-slug>/` ngay trong folder dự án đang mở, để bạn mở/sửa dễ trong Finder. Bốn file nằm cạnh nhau:

```
spar/<round-slug>/
  prompt.md          Claude viết — câu hỏi + status. Bạn CHỈ sửa dòng status.
  user-output.md     Bạn viết — bản trả lời của bạn.
  claude-output.md   Claude viết — bản trả lời của Claude (sinh SAU khi bạn xong).
  grade-output.md    Claude viết — chấm cả hai bản + góp ý cho bản của bạn.
```

`prompt.md` mở đầu bằng frontmatter, status là dòng bạn tự đổi bằng tay:

```
---
status: waiting-user
round: 01
topic: <chủ đề ngắn>
rubric: default          # để trống = dùng rubric.md; hoặc dán tiêu chí riêng
---

# Câu hỏi

<đề bài Claude đặt ra>

## Cách chơi
1. Viết trả lời của bạn vào `user-output.md`.
2. Đổi dòng `status:` ở trên thành `user-answered`. Lưu lại.
3. Quay lại chat gõ một câu bất kỳ để gọi tôi (vd "spar" hoặc "xong rồi").
   Tôi kiểm status, rồi mới viết `claude-output.md` và `grade-output.md`.
```

## Status — vòng đời một round

Chỉ ba trạng thái, đi một chiều:

```
waiting-user   → (bạn viết user-output.md, đổi status) →
user-answered  → (Claude viết claude-output.md + grade-output.md, đổi status) →
graded
```

Thêm một lối tắt: nếu bạn không muốn tự trả lời, đổi status thành `user-skip`. Khi đó Claude viết claude-output như thường, còn grade-output chỉ chấm bản của Claude và ghi rõ "bạn bỏ lượt, không có gì để coach".

## Luật cứng

- **Không nhìn trước đáp án (xương sống — lý do skill tồn tại).** Khi status là `waiting-user`, Claude TUYỆT ĐỐI không viết `claude-output.md`, không gợi ý đáp án trên chat, không "mớm" một phần. Chỉ nhắc bạn rằng round đang chờ bạn. Thủng luật này là hỏng cả skill.
- **Kiểm status trước khi làm.** Mỗi lần được gọi, Claude đọc `status:` của round trước, rồi mới quyết làm gì. Không đoán, không làm theo trí nhớ round cũ.
- **Chỉ trao đổi qua file.** Nội dung câu hỏi, đáp án, điểm, góp ý — tất cả vào file. Trên chat Claude chỉ để lại MỘT dòng trỏ đường (vd "Round 01 đã chấm → mở `grade-output.md`"). Không lặp lại nội dung file trên chat.
- **Chấm công bằng, chấm cùng một thước.** Bản của bạn và bản của Claude chấm bằng đúng `rubric.md` như nhau. Không nương tay bản nào, không tự khen bản của Claude.
- **Coach mới là phần thưởng.** grade-output không dừng ở điểm số. Phần "GÓP Ý CHO BẠN" phải chỉ ra: bạn thiếu ý nào Claude có, bạn làm tốt hơn chỗ nào, và MỘT đòn bẩy lớn nhất để lần sau tốt hơn. Đây là lý do bạn chịu tự trả lời trước.
- **Không bịa để chấm.** Nếu prompt hỏi về codebase/sự việc thật, Claude đọc nguồn thật trước khi chấm đúng-sai. Không có nguồn thì ghi "chưa kiểm được", không phán bừa.
- **Đủ ý, không cắt.** Ngắn gọn là cách trình bày. Bản trả lời của Claude và phần coach vẫn phải đủ ý — thiếu ý không tính là gọn.

## Bước chạy

**Bước 0 — Xác định đang được gọi để làm gì.** Người dùng gọi spar có thể là: (a) muốn mở round mới, (b) báo đã trả lời xong, (c) hỏi trạng thái. Quét thư mục `spar/` để biết có round nào đang treo.

Lệnh quét nhanh (chạy trong bash) — tìm round đang chờ Claude xử lý:

```
grep -rl "status: user-answered" spar/*/prompt.md 2>/dev/null
grep -rl "status: user-skip"     spar/*/prompt.md 2>/dev/null
```

**Bước 1 — Nếu mở round mới.** Chọn/nhận chủ đề, tạo thư mục `spar/NN-<slug>/`, viết `prompt.md` với `status: waiting-user` theo mẫu trên. Tạo sẵn `user-output.md` rỗng (một dòng gợi ý "viết trả lời của bạn ở đây") để bạn chỉ việc mở ra gõ. KHÔNG viết claude-output. Trả về chat một dòng: "Round NN sẵn sàng → trả lời vào `spar/NN-<slug>/user-output.md`".

**Bước 2 — Nếu status là `user-answered`.** Đọc `prompt.md` và `user-output.md`. Rồi tự trả lời sạch vào `claude-output.md` (trả lời như thể chưa xem bản của bạn — bám câu hỏi, không nhại bản của bạn). Sau đó chấm cả hai theo Bước 3. Cuối cùng đổi `status:` trong prompt.md thành `graded`.

**Bước 3 — Chấm và coach.** Đọc `rubric.md` cùng thư mục skill. Chấm bản của bạn và bản của Claude theo khung dưới, viết vào `grade-output.md`. Áp gate: tiêu chí xương sống = 0 thì bản đó rớt gate dù tổng cao.

**Bước 4 — Nếu status là `user-skip`.** Bỏ qua chấm phần user. Viết claude-output như thường, grade-output chỉ chấm bản Claude, ghi rõ bạn bỏ lượt.

## Khung grade-output (cố định — để so nhiều round)

```
CHẤM: round <NN> · <topic>

— BẠN —
1 Đúng       [n] — <lý do 1 câu>
2 Đủ ý       [n] — <...>
3 Lập luận   [n] — <...>
4 Rõ         [n] — <...>
5 Trọng tâm  [n] — <...>
TỔNG: <n>/10   GATE: <đạt | rớt: tiêu chí ...>

— CLAUDE —
1 Đúng       [n] — <...>
2 Đủ ý       [n] — <...>
3 Lập luận   [n] — <...>
4 Rõ         [n] — <...>
5 Trọng tâm  [n] — <...>
TỔNG: <n>/10   GATE: <đạt | rớt: ...>

GÓP Ý CHO BẠN
- Bạn làm tốt hơn: <chỗ bản bạn hơn bản Claude, nếu có>
- Bạn thiếu: <ý cốt lõi bản Claude có mà bạn bỏ>
- SỬA TRƯỚC TIÊN: <một câu — đòn bẩy lớn nhất cho lần sau>
```

Không thêm khen/chê ngoài khung. Chấm xong là chấm xong; muốn thử lại thì mở round mới.

## Cài đặt lần đầu

Thư mục `spar/` chưa có thì Claude tạo khi mở round đầu tiên. Round demo có sẵn ở `spar/demo-01/` — mở `prompt.md` đọc cách chơi, viết vào `user-output.md`, đổi status, rồi gọi spar. Xem một round hoàn chỉnh trông ra sao ở `example.md` cùng thư mục skill này.
