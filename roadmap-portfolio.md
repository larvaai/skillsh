# Roadmap — Quản lý nhiều project (portfolio)

## Hiện trạng: 3/4 nhu cầu đã có skill lo, chỉ thiếu 1

- **Hiểu repo** → `atlas` (dựng bản đồ hiểu biết) + `explain` (dạy hiểu theo mức L0-L8) + `teen` (giải thích đơn giản). Đã có, không cần build thêm.
- **Brainstorm tính năng** → `idea` (GĐ2-4, brainstorm cách tiếp cận trước khi chốt PRD) + `partner` (brainstorm cả pipeline 15 giai đoạn). Đã có.
- **Critical thinking** → `idea` Nhánh A (phản biện ý tưởng không khả thi, không tự kill) + `review` (tìm edge case/lỗ hổng trong 1 tính năng) + `trace` (theo dấu side effect). Đã có, nhưng chỉ ở mức 1 tính năng/1 project tại 1 thời điểm.
- **Quản lý NHIỀU project cùng lúc** → CHƯA CÓ. Mọi skill hiện tại (atlas/explain/idea/frame/partner/triage/trace/review) chỉ thao tác trên 1 project, `state/current.json` chỉ giữ đúng 1 project đang mở. Không có chỗ xem tổng toàn bộ project đang track, project nào đang chờ quyết định, project nào bị bỏ quên. Hiện `state/project/` mới có 1 project (`hex_agent`) nên gap này chưa lộ rõ, nhưng cứ thêm project là sẽ thiếu ngay.

→ Chỉ cần build **1 skill mới**, tạm gọi `portfolio`. Không build lại phần hiểu-repo/brainstorm/critical-thinking vì đã có — `portfolio` chỉ TRỎ tới các skill đó, không thay thế, tránh trùng lặp phải bảo trì 2 chỗ.

## Epic: Portfolio — quản lý nhiều project cùng lúc

### Feature 1 — Bảng tổng hợp toàn bộ project

Story: xem tất cả project đang track, biết ngay project nào đang ở giai đoạn gì, project nào đang chờ quyết định.

AC:
- Chạy `/portfolio` không tham số → liệt kê đúng số project có thư mục trong `state/project/`, mỗi dòng gồm tên, giai đoạn hiện tại (đọc từ state file tương ứng), lần cập nhật cuối.
- Project có `cho_duyet: true` (đang chờ go/no-go) → luôn hiện đầu danh sách.
- Test giả: thêm/xoá 1 thư mục trong `state/project/` → chạy lại `/portfolio`, danh sách phải đổi đúng theo, không có project ảo hoặc thiếu.

### Feature 2 — Điều hướng vào đúng project, đúng skill

Story: từ bảng tổng hợp, chọn 1 project, được đưa thẳng vào chỗ đang dở (idea/atlas/frame), không phải tự gõ lại path.

AC:
- Chọn project X → `state/current.json` được ghi đúng path của X.
- X đang dở ở `idea` (có `idea-state.json` chưa `done_handoff`) → gợi ý chạy `/idea`, không tự chạy hộ.
- X đã qua Domain (`done_handoff`) và có atlas map → gợi ý `/atlas` hoặc `/explain`.
- `portfolio` không tự chọn skill nào để chạy — chỉ liệt kê lựa chọn, giữ đúng nguyên tắc "không tự quyết hộ" mà `idea` đang theo ở bước bàn giao GĐ5.

### Feature 3 — Phản biện thứ tự ưu tiên (critical thinking ở mức portfolio)

Story: khi nhiều project cùng chờ quyết định, được nhắc nếu thứ tự đang ưu tiên có vẻ bất hợp lý.

AC:
- Có ≥2 project cùng `cho_duyet: true` → phải nêu ít nhất 1 lý do nên cân nhắc đổi thứ tự, dựa trên dữ liệu thật trong state (số ẩn số còn mở, số ngày không cập nhật) — không được chung chung kiểu "nên ưu tiên cái quan trọng hơn".
- Không tự đổi thứ tự build của user, chỉ đề xuất — tự đổi là bug.

### Feature 4 — Cách ly dữ liệu giữa các project (điều kiện nền, không phải tính năng mới)

Story: đảm bảo dữ liệu project A không lẫn sang B khi có nhiều project cùng lúc — thiếu cái này thì cả 3 feature trên xây trên nền sai.

AC:
- `atlas` chạy trên project A không đọc/ghi nhầm `.ai-understanding/` của B.
- `idea`, `frame` mỗi project có state riêng dưới `state/project/<ten>/`, không có file state dùng chung giữa 2 project.

## Thứ tự làm

1. Feature 4 (cách ly dữ liệu) — kiểm tra/khoá nền trước, vì nếu sai thì mọi thứ phía trên vô nghĩa.
2. Feature 1 (bảng tổng hợp) — dùng được ngay, không phụ thuộc Feature 2/3.
3. Feature 2 (điều hướng) — nối tiếp ngay sau khi có bảng.
4. Feature 3 (phản biện ưu tiên) — thêm sau cùng, không chặn 3 feature đầu.

## Không làm (out of scope)

- Không build lại hiểu-repo/brainstorm/critical-thinking — đã có atlas/idea/review/trace, `portfolio` chỉ trỏ tới.
- Không tự động hoá quyết định ưu tiên — Feature 3 chỉ đề xuất, quyền quyết vẫn ở bạn.

## Bước kế tiếp

Đây là roadmap (GĐ9), chưa phải lúc viết SKILL.md thật (GĐ11). Trước khi build: chạy `/skill-define` để xác nhận `portfolio` không trùng gì thêm với 12 skill hiện có, rồi `/frame` để đóng khung Feature 4 làm trước.
