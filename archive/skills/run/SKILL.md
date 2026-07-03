---
name: run
description: 'Executor của bộ project-folder — GĐ11: đọc progress/board.md, chọn task ready, thi công; task cùng nhóm song song đủ điều kiện (deps xong + contract locked + vùng chạm rời nhau) thì FAN-OUT mỗi task một agent chạy đồng thời, rồi merge, chạy DoD, cập nhật board. Dùng khi "build đi", "làm task tiếp theo", "chạy song song backend frontend", "fan out agent", "thi công theo board", "code theo plan".'
---

# Run — GĐ11: thi công theo board, fan-out khi được phép

`run` là skill duy nhất của bộ được phép huy động nhiều agent cùng lúc. Nó không nghĩ hộ kế hoạch — board của `plan` nói gì làm nấy; board mù mờ thì trả về `plan`, không đoán.

Phân vai: `plan` cắt task — `run` không thêm/bớt Story, không sửa contract. `gate` nghiệm thu tổng — `run` chỉ check DoD từng task. Chuẩn delivery chi tiết: `quy-trinh-idea-to-operate.md` mục GĐ11.

## Luật cứng

- **Bước 0 resume:** constitution → board + journal → task `doing` dở (ưu tiên làm nốt) rồi mới tới `ready`. Đọc AC của Story tương ứng + contract liên quan trước khi gõ code.
- **Điều kiện fan-out — đủ 3, thiếu 1 là chạy tuần tự:** (1) mọi Phụ thuộc của cả nhóm `done`; (2) contract giữa chúng `locked`; (3) Vùng chạm rời nhau. Kiểm cả 3 và nói rõ kết quả kiểm trước khi fan-out.
- **Chỉ agent điều phối ghi `progress/`.** Agent con không chạm board/journal — tránh 2 agent ghi 1 file. Agent con cũng không sửa ngoài Vùng chạm của mình; cần sửa ngoài vùng → dừng, báo về, điều phối quyết.
- **Task xong không tự `done`:** agent con trả kết quả → điều phối review theo AC + DoD (build/test pass, README còn đúng) → `review` → `done`. Fail → trả lại kèm lý do, hoặc `blocked` + ghi chú.
- **Đụng chuyện đổi thiết kế/contract đã locked → dừng task, chốt lại với Son.** Đây là chỗ DUY NHẤT `run` dừng chờ — mọi lựa chọn nhỏ khác: tự quyết, đáng nhớ thì 1 dòng `decisions.md`, đi tiếp.
- **Điều chưa chắc mới lộ khi code → 1 dòng `risks.md`.** Secrets không ghi vào folder — chỉ pointer, `codebase/` chỉ chứa `.env.example`.
- **Kết phiên:** board + journal; xong trọn một Feature/GĐ → cập nhật bức tranh (kèm dòng "So kỳ vọng").

## Các bước

1. **Chọn việc, không chờ lệnh:** theo thứ tự roadmap, ưu tiên đường ngắn nhất tới K gần nhất; nhóm song song đủ 3 điều kiện → fan-out luôn. Nói rõ đang làm gì rồi làm — Son đổi nhịp bất cứ lúc nào.
2. **Tuần tự:** đánh dấu `doing` → code trong Vùng chạm, bám AC + contract → check DoD → `review` → tự review theo AC → `done` + journal.
3. **Fan-out:** đánh dấu cả nhóm `doing`, mỗi task một agent (Task tool) với prompt chuẩn dưới; đợi tất cả về → review từng cái theo AC → merge/chạy test chung → `done` từng task + journal từng dòng.
4. **Prompt chuẩn cho agent con** (điền đủ, không rút gọn):

```
Bạn thi công task <ID> của project <đường dẫn projects/<ten>>.
1. Đọc constitution/00-luat.md và làm đúng phần "Agent con" trong Luật fan-out.
2. Task (dòng board): <chép nguyên dòng>. AC: <chép AC từ docs/30-roadmap.md>.
   Contract phải theo: <docs/contracts/... — không được sửa file này>.
3. Chỉ sửa trong Vùng chạm: <vùng>. KHÔNG chạm progress/. Cần ra ngoài vùng → dừng, báo về.
4. Xong: chạy check theo DoD, trả về ≤10 dòng: đã làm gì · file tạo/sửa · kết quả check · điều còn treo.
```

5. **Sau mỗi vòng:** nhìn lại board — task nào vừa thành `ready`, còn nhóm nào fan-out được — báo user nhịp kế. Hết task GĐ11 → gợi `gate`.

## Artifact của phiên

Code trong `codebase/` từng task, board cập nhật đúng vòng đời trạng thái, journal mỗi task 1 dòng, bức tranh nếu xong Feature/GĐ.
