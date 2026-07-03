---
name: review
description: Rà soát một tính năng, module, hoặc luồng để tìm edge case còn thiếu, error path chưa xử lý, và lỗ hổng permission. Dùng khi người dùng muốn biết "có gì tôi đang bỏ sót không". Mức L6 trở lên.
---

# Review — Rà soát gap trong implementation

Review không đọc để hiểu — review đọc để tìm lỗ hổng. Claude đóng vai người cố tình phá: đặt câu hỏi "điều gì xảy ra nếu...", tìm những case code chưa xử lý, và báo cáo trung thực những gì tìm được.

## Quy tắc
- Tái dùng `.ai-understanding/` trước: đọc artifact liên quan trước khi đọc file gốc.
- Mỗi gap tìm được phải có evidence: `file · dòng/symbol · điều thiếu · hậu quả`.
- Tách gap thực sự khỏi "có thể là gap" — gắn nhãn rõ.
- Không bỏ qua gap chỉ vì nhỏ — ghi lại, để người dùng quyết định.
- Không đề xuất fix — chỉ báo cáo những gì tìm thấy. Đóng khung fix là việc của `frame`.

## Ba chế độ review

```
edge       — Tìm input, state, hoặc sequence chưa được xử lý đúng.
             Kích bởi: "edge case nào tôi bỏ sót", "input nào có thể phá", "còn case nào chưa cover"

error      — Kiểm tra error path: có bắt đúng không, có xử lý đúng không, có propagate đúng không.
             Kích bởi: "error handling đủ chưa", "nếu X fail thì sao", "exception này đi đâu"

permission — Tìm chỗ access control có thể bị bypass hoặc thiếu.
             Kích bởi: "permission check đủ chưa", "user A có thể làm gì user B không được", "chỗ nào chưa guard"
```

Nếu không chắc chế độ: hỏi *"Bạn muốn tìm edge case, review error handling, hay kiểm tra permission?"*
Nếu người dùng nói "review tổng thể": chạy cả ba theo thứ tự edge → error → permission.

## Bước 0 — Xác định phạm vi

Hỏi hoặc suy ra:
- **Đối tượng**: tính năng, module, endpoint, hàm, hoặc luồng cụ thể.
- **Ngữ cảnh**: đang chuẩn bị ship, vừa sửa xong, hay đang thấy bug lạ?

Nếu phạm vi quá rộng ("review cả project"): hỏi thu hẹp — review cái gì trước?

## Bước 1 — Xác định project và đọc artifact

Lấy `<project-path>` từ argument, tin nhắn, hoặc `state/current.json`.

Đọc `.ai-understanding/` nếu có:
- Còn tươi: đọc artifact liên quan đến phạm vi (flows, contracts, risks).
- `99_changes.md` có pending ở phần liên quan: đọc file gốc cho phần đó.
- Chưa có: đọc thẳng từ file gốc, gợi ý chạy `atlas` sau.

## Bước 2 — Đọc implementation

Đọc code của phạm vi đã xác định. Trong khi đọc, đặt câu hỏi theo chế độ:

**edge**: Với mỗi input/state/sequence — còn case nào chưa có nhánh xử lý? Input rỗng, null, âm, overflow, quá dài, sai type, concurrent? Sequence ngoài thứ tự?

**error**: Mỗi điểm có thể fail — có được bắt không? Bắt đúng loại không? Sau khi bắt thì làm gì (log, retry, propagate, silent)? Người dùng cuối nhận được gì?

**permission**: Mỗi action — có check ai được làm không? Check đúng tầng chưa (UI, API, DB)? Có thể bypass bằng cách thay param, gọi endpoint khác, hoặc race condition không?

## Bước 3 — Báo cáo gap

```
PHẠM VI: <đối tượng>
CHẾ ĐỘ: edge / error / permission / tổng thể

GAP TÌM ĐƯỢC
  [Critical] <file · symbol> — <điều thiếu> → <hậu quả nếu xảy ra>
  [Medium]   <file · symbol> — <điều thiếu> → <hậu quả>
  [Low]      <file · symbol> — <điều thiếu> → <hậu quả>

CÓ THỂ LÀ GAP (chưa chắc)
  <file · symbol> — <nghi ngờ> · cần xác nhận thêm: <câu hỏi>

KHÔNG TÌM THẤY GAP
  <phần đã kiểm tra và thấy ổn>
```

Mức độ:
- **Critical**: có thể gây lỗi production, mất data, hoặc security breach.
- **Medium**: gây hành vi sai trong case cụ thể, không crash.
- **Low**: thiếu sót nhỏ, UX kém, hoặc inconsistency.

## Bước 4 — Gợi ý

Sau báo cáo, hỏi theo kết quả:
- Có gap Critical: *"Bạn muốn tôi đóng khung lát cắt fix theo thứ tự ưu tiên không?"* → gợi ý skill `frame`.
- Review tổng thể xong: *"Bạn muốn tôi review thêm một module khác, hay bắt đầu lên kế hoạch fix những gap vừa tìm?"*
- Có "có thể là gap" chưa rõ: *"Bạn muốn tôi đào sâu vào [X] để xác nhận đây có thực sự là gap không?"*
- Không tìm thấy gap: *"Implementation trông ổn. Bạn muốn review một phần khác, hay đóng khung tính năng tiếp theo?"* → gợi ý skill `frame`.

## Bước 5 — Cập nhật state

Ghi `state/current.json`:
```json
{ "project": "<project-path>", "updated_at": "<ISO 8601>" }
```
