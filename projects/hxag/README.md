# hxag — HexAgent (clean rebuild)

**Project là gì (một câu vấn đề):** dựng một *agent tự-điều-phối* — bạn giao một mục tiêu, nó tự lập kế hoạch, chia thành các bước có thứ tự, giao cho các sub-agent làm, và **chỉ báo "xong" khi mọi tiêu chí nghiệm thu được chứng minh bằng bằng chứng THẬT** — sao cho không **báo-xong-khống** và không **chạy-vô-hạn đốt tiền**.

## Kỳ vọng ban đầu (thô — mỏ neo để Go/No-Go GĐ13 đối chiếu)

Ghi ngày 0, trước khi agent gợi ý gì. "Ưng ý" = tận mắt thấy:
1. Một **folder project `projects/hxag/`** dựng đúng cấu trúc charter (6 folder + constitution + progress).
2. Rebuild **lần lượt qua các giai đoạn 0→14**, mỗi bước sinh một **artifact THẬT** nằm đúng folder theo `constitution/folders.md`.
3. **`progress.json` cập nhật** mỗi khi một bước xong (task → done, mở khóa bước sau), và mỗi artifact được **`checkpoint` cấp phiếu PASS/FAIL** — không có phiếu thì chưa xong.
4. Ít nhất một **nhóm chạy song song** được `fanout` bung nhiều agent đồng thời (sau khi contract freeze ở GĐ10).
5. **`resume`** in được toàn cảnh "đang ở đâu, ready cái gì" bất cứ lúc nào.
6. Mục tiêu bao trùm: **kiểm chứng cả bộ skill quản lý project (charter/progress/checkpoint/fanout/resume) có chạy hiệu quả và cho artifact có chất lượng không.**

## Meta
- **mode:** greenfield (workspace mới; codebase/ khởi đầu trống — trỏ nguồn tham chiếu).
- **Nguồn tham chiếu nội dung:** `/Users/uspro/Desktop/skillsh/rebuild-hex-agent/` (gói thiết kế 15-giai-đoạn của cùng sản phẩm, đã dựng ở vòng trước) + repo gốc `/Users/uspro/Desktop/namnson/hex_agent`.
- **Ngày dựng:** 2026-07-03.

## Điều hướng
- Toàn cảnh bất cứ lúc nào: `/resume hxag`
- Brainstorm ý đầu: `/idea`
- Sổ tiến độ người-đọc: [`progress/board.md`](progress/board.md)
