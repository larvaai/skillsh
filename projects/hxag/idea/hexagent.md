# Idea Brief — HexAgent (GĐ0 Idea Intake)

> Hộp brainstorm ý đầu. Đủ-là-đủ cho GĐ0: input/output rõ, một plan thô đi được, ẩn số lớn nhất nêu tên. Nguồn tham chiếu: `rebuild-hex-agent/pipeline/05-idea-domain.md`.

## Ý một câu
Một **agent tự-điều-phối**: người dùng giao một *mục tiêu*, agent tự lập kế hoạch, chia thành các bước có thứ tự, giao cho sub-agent làm, và **chỉ báo "xong" khi mọi tiêu chí nghiệm thu có bằng chứng THẬT** — có ngân sách/guard chặn chạy vô hạn.

## Cho ai + đau ở đâu
- **Cho:** dev/đội xây hệ agent tự chạy nhiều bước (gọi model, đọc/ghi file, nhờ agent con).
- **Đau:** khi để AI tự chạy chuỗi bước, hai bệnh chết người — (1) **báo-xong-khống** (agent tự nói "xong" mà chưa xong), (2) **chạy-vô-hạn đốt tiền**; và cả hai thường xảy ra ở chỗ *không nhìn thấy, không tua lại được*.

## Input → Output (ranh giới rõ)
- **Input:** một `Task` = mục tiêu ngôn ngữ tự nhiên + (tuỳ chọn) danh sách `AcceptanceCriterion` + ngân sách (max bước/độ sâu).
- **Output:** trạng thái terminal `FINISHED | BLOCKED | FAILED` + tập `Evidence` chứng minh từng AC + `events.jsonl` (nhật ký tua-lại-được).
- **Không thuộc phạm vi:** UI điều khiển realtime, RAG, catalog role phức tạp — để pha sau.

## Plan thô đi được (một luồng chạy được)
1. Nhận Task → lập **plan** = cây bước (forest theo cha + DAG theo `depends_on`), mỗi bước có `done_when`.
2. Cổng-cấu-trúc kiểm plan có **chứng minh dừng** (μ co ngặt) trước khi đổi cây.
3. Chọn bước sẵn-sàng-nhất (deps đã xong) → **delegate** cho sub-agent với scope con ⊆ cha.
4. Sub-agent chạy qua **một chokepoint** (mọi hành động đi một cửa → trace + scope-check).
5. **Nghiệm thu**: mỗi AC "đạt" phải trỏ ≥1 evidence THẬT (không phải scaffolding); worker không tự ghi verdict.
6. `all_accepted()` → **FINISHED**; guard (max bước/no-progress/repeat/depth) chặn runaway.

## Ẩn số lớn nhất (nêu tên, chưa giải)
- **U1 (cao):** resume một-lần-đúng sau crash — checkpoint atomic + không re-emit side-effect. → đo ở GĐ8 live-slice (SPIKE).
- **U2 (trung):** "đáng nới ngân sách" theo tiêu chí nào khi để LLM tự quyết — giữ META-cap cứng.
- **U3 (trung):** honor-system nghiệm thu (Agent-O tự chấm) — khe hở evidence-của-node-khác. → soi ở review.

## Độ rõ / khả thi (router)
- **Rõ:** input/output/ranh giới rõ. **Khả thi:** cao — có tiền lệ chạy thật ở repo gốc `hex_agent` (anchor `supervisor/loop.py`, `delegation/manager.py`, `judge_acceptance`). → đi tiếp GĐ1→5.
