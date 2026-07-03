---
name: pulse
description: 'Bắt nhịp một project-folder — hai chế độ: standup (read-only, "đang tới đâu, task nào ready/blocked, cổng kế là gì, nên gọi skill nào") và learn (GĐ14: vận hành, đo, rút bài học → đề xuất task vòng mới quay về plan/board). Dùng khi "đang tới đâu rồi", "resume project", "tiếp tục đi", "hôm qua làm tới đâu", "sau ship thì sao", "đo kết quả", "rút kinh nghiệm vòng này".'
---

# Pulse — standup mọi lúc + GĐ14: vận hành, đo, học

`pulse` là chỗ quay về khi lạc: mở project ra là biết đang ở đâu, tiếp gì. Sau ship, `pulse` kiêm GĐ14 — nhìn hệ thống chạy thật, đo, rút bài học, đổ vòng lặp mới về backlog. Vòng Idea→Operate khép ở đây và mở lại ở `plan`.

Phân vai: `pulse` không làm hộ việc của GĐ nào — chỉ soi và trỏ. Đề xuất task mới là đề xuất; Son gật là đổ vào board.

## Luật cứng

- **Chế độ standup là READ-ONLY tuyệt đối:** không sửa board, không journal, không chạm file nào. Chạy xong diff project = 0 byte.
- **Recap đọc từ state thật** (board, journal, artifact có mặt), không suy diễn từ trí nhớ phiên trước. Mỗi câu trong recap trỏ được về file/dòng cụ thể.
- **Chế độ learn ghi vào:** `docs/50-ops.md`, hai sổ sống (`risks.md` khi đời thật nói ngược bằng chứng cũ; `decisions.md` 1 dòng khi mở vòng mới / đổi kỳ vọng / sửa luật), và (sau khi Son gật) task mới trên board + journal.
- **Không tự đổi ưu tiên.** ≥2 hướng cạnh tranh (fix nợ vs feature mới) → nêu bằng chứng từng hướng, Son chọn — đây là chuyện hướng đi, không phải thủ tục.

## Chế độ 1 — Standup ("đang tới đâu?")

Bước 0 resume (constitution → board + journal → bức tranh), rồi trả về MỘT khối:

```
ĐANG Ở ĐÂU — <project>
Bức tranh: <1 câu từ docs/00-buc-tranh.md, version mấy>
So kỳ vọng: <khớp / đang lệch ở K nào — theo dòng "So kỳ vọng" mới nhất>
GĐ hiện tại: <n> · Điểm chốt kế: <1/4..4/4 — là gì>
Task: doing <...> · ready <...> · blocked <... + lý do>
Rủi ro mở: <N — nặng nhất: R-x, 1 câu> (từ risks.md)
Song song được ngay: <nhóm nào, hay "chưa nhóm nào — vì sao">
Phiên trước: <dòng journal cuối>
Nên gọi: /<skill> — <vì sao, 1 câu>
```

Board và artifact lệch nhau (task `done` mà artifact thiếu) → nói thẳng trong recap, đề xuất sửa board — không im.

## Chế độ 2 — Learn (GĐ14, sau ship)

1. Hỏi/thu thực tế: hệ thống có được dùng không, K nào trong kỳ vọng đã thành sự thật NGOÀI ĐỜI (không chỉ trong demo), việc chân tay trong `problem/01` đã bớt thật chưa, pain mới nào mọc ra.
2. Ghi `docs/50-ops.md`: số đo · quan sát · bài học · nợ đang gánh — mỗi mục trỏ về nguồn. Rủi ro `dong-*` mà đời thật nói ngược → mở lại trong `risks.md`.
3. Đề xuất vòng mới: mỗi bài học → 0–n task đề xuất (mô tả + vì sao + ước phụ thuộc). Son gật → đổ vào board, ý lớn → thêm `idea/<slug>.md`, quay về `plan` cắt lại. Cập nhật bức tranh (vòng mới, mờ chỗ nào).
4. Retro CÁCH LÀM, không đổ lỗi: vòng vừa rồi lệch/vòng lại ở đâu, quy trình hổng chỗ nào → đề xuất sửa `constitution/00-luat.md` của project, đáng nhân rộng → đề xuất nâng template gốc trong `seed/assets/`. Bài học thuộc về quy trình, không thuộc về ai.

## Artifact của phiên

Standup: không file nào — chỉ khối recap. Learn: `docs/50-ops.md`, task mới trên board (đã duyệt), journal, bức tranh.
