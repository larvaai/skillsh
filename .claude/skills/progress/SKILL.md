---
name: progress
description: "Sổ tiến độ và đồ thị task của một project — sở hữu duy nhất progress/progress.json + board.md. Hai việc: PLAN (chia chunk kế tiếp thành task, gắn depends_on + parallel_group + owner + đích artifact, tính task nào ready, đánh dấu nhóm chạy song song được) và ADVANCE (một bước báo xong → kiểm có phiếu checkpoint PASS chưa → lật task done, mở khóa task phụ thuộc, dời con trỏ resume). Dùng khi: 'chia task', 'cập nhật tiến độ', 'task này xong rồi', 'cái gì làm được song song', 'đánh dấu done'. Chỉ progress được ghi progress.json; checkpoint cấp phiếu, fanout đọc nhóm song song, resume đọc để in toàn cảnh."
---

# Progress — Đồ thị task, con trỏ resume, cổng mở nhánh song song

`progress` giữ tấm bản đồ thực thi: mọi việc cần làm, cái nào chặn cái nào, cái nào chạy song song được, và đang đứng ở đâu. Nó là chủ DUY NHẤT của `progress.json`. Nó KHÔNG kiểm chất lượng artifact (việc của `checkpoint`) và KHÔNG tự bung agent (việc của `fanout`) — nó chỉ ghi sự thật về đồ thị.

Ranh giới:
- `progress` ghi `progress.json`. `checkpoint` ghi phiếu đạt. `progress` ĐỌC phiếu để quyết có được lật `done` không.
- `backlog` (GĐ9) chia Epic→Feature→Story→AC ở tầng sản phẩm. `progress` là tầng thực thi mỏng hơn: task nào chạy được bây giờ, theo thứ tự phụ thuộc nào. Không lặp backlog; task của `progress` có thể trỏ về story của `backlog`.

## Quy tắc bắt buộc

- **Một chủ.** Chỉ `progress` ghi `progress.json` + `board.md`. Không skill nào khác ghi hai file này.
- **Không lật `done` khi thiếu phiếu.** Một task chỉ lên `done` khi `progress/checkpoints/<task-id>.md` tồn tại và verdict là `PASS`. Chưa có → giữ `in_progress`, bảo user chạy `/checkpoint <task-id>`. Đây là cách ép Định-nghĩa-Xong.
- **depends_on/parallel_group là dữ liệu, không phải lời kể.** Muốn hai việc chạy song song thì cho chúng cùng `parallel_group` và `depends_on` giống nhau (thường cùng trỏ về task contract). Không "song song" bằng miệng.
- **Append, không xoá.** Sửa `trang_thai` tại chỗ; không xoá task cũ. Đồ thị là lịch sử.
- **Con trỏ luôn khớp task ready đầu tiên.** Sau mỗi lần advance, `con_tro.giai_doan` trỏ tới giai đoạn của task ready kế.

## Trạng thái task

```
todo         chưa tới lượt (còn depends_on chưa done)
ready        hết phụ thuộc, chờ chạy
in_progress  đang làm (artifact chưa xong hoặc chưa có phiếu PASS)
done         artifact có + phiếu checkpoint PASS + đã mở khóa phụ thuộc
blocked      bị chặn bởi open question/quyết định treo (ghi lý do ở ghi_chu)
```

## Bước 0 — Nạp ngữ cảnh

Đọc `constitution/` (luật) + `progress.json` hiện tại. Không có `progress.json` → project chưa charter, tiến cử `/charter` trước.

## Chế độ PLAN — chia chunk kế thành task

Khi con trỏ vừa qua một cổng và cần vạch việc kế (vd domain xong → cần shape, stack; hoặc contract xong → cần BE + FE):

1. Chia thành các task NHỎ ĐỦ để một skill/agent làm gọn, mỗi task một artifact rõ.
2. Mỗi task gắn: `depends_on[]` (task phải done trước), `parallel_group` (null nếu tuần tự; cùng nhãn nếu chạy song song được), `owner` (skill sẽ làm), `artifact` (đích path theo `folders.md`).
3. **Nhận diện điểm fan-out:** nếu hai+ task chỉ phụ thuộc CÙNG một đầu vào đã sẵn (điển hình: contract đã freeze) và không phụ thuộc lẫn nhau → cho chung `parallel_group`. Đây là chỗ sau này `fanout` bung agent.
4. Ghi tasks vào `progress.json`, cập nhật `board.md`, dời con trỏ nếu cần.

In lại nhánh vừa chia:
```
═══ ĐÃ CHIA TASK — sau <cổng vừa qua> ═══
Tuần tự: <T-id việc → T-id việc>
Song song (<parallel_group>): <T-id> ∥ <T-id>  — cùng chờ <task đầu vào>
Ready ngay: <T-id...>
════════════════
```

## Chế độ ADVANCE — đóng một bước

Khi user báo một task xong:
1. Kiểm `progress/checkpoints/<task-id>.md`. Không có / verdict `FAIL` → dừng: "Chưa có phiếu đạt. Chạy `/checkpoint <task-id>` trước." (nếu FAIL, nêu lý do trong phiếu).
2. Verdict `PASS` → set task `done`.
3. Mở khóa: mọi task `todo` mà toàn bộ `depends_on` giờ đã `done` → chuyển `ready`.
4. Dời `con_tro` tới giai đoạn của task ready kế; nếu một `parallel_group` vừa đủ ready → ghi chú "mở nhánh song song, chạy /fanout".
5. Cập nhật `board.md`, `updated_at`.

```
═══ ĐÓNG BƯỚC — <T-id> ✓ ═══
Artifact: <path>   Phiếu: PASS
Mở khóa: <T-id...> → ready
Con trỏ: <giai_doan mới>
→ Kế: /<skill owner task ready>   (hoặc /fanout nếu nhóm song song đã đủ)
════════════════
```

## Schema — progress.json

```json
{
  "schema_version": 1,
  "project": "<key>",
  "mode": "greenfield|brownfield",
  "con_tro": { "giai_doan": "gd<n>_<tên>", "ghi_chu": "<1 dòng>" },
  "tasks": [
    { "id": "T-05", "viec": "Build backend theo contract", "giai_doan": "gd11_delivery",
      "trang_thai": "ready", "depends_on": ["T-04"], "parallel_group": "pg-be-fe",
      "owner": "delivery", "artifact": "codebase/backend/", "traces_to": ["STORY-3"] }
  ],
  "updated_at": "<ISO 8601>"
}
```

`traces_to` (tùy chọn) nối task về story/AC của `backlog` để giữ traceability. `giai_doan` dùng bộ `gd0_intake … gd14_operate`.

## board.md — bản người đọc

Một bảng: cột `id · việc · giai đoạn · trạng thái · phụ thuộc · nhóm song song · owner · artifact`. Thêm một khối "Đang ready" và "Song song sẵn sàng" ở đầu để đọc nhanh. `board.md` không chứa dữ liệu mới — chỉ là ảnh của `progress.json`.
