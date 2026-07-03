# Định-nghĩa-Xong của một bước

Một bước (một task trong `progress.json`) chỉ được coi là XONG khi đủ cả ba, không thiếu cái nào:

```
1. ARTIFACT   — file kết quả tồn tại đúng folder theo folders.md
                (không có artifact thì bước chưa xong, dù đã "bàn xong")
2. PHIẾU ĐẠT  — checkpoint kiểm và cấp verdict PASS ở progress/checkpoints/<task-id>.md
                (đúng path + đủ mục bắt buộc của giai đoạn + qua rubric nếu có)
3. PROGRESS   — progress cập nhật: task → done, mở khóa task phụ thuộc, dời con trỏ resume
```

Thiếu 1 → không có gì để kiểm. Thiếu 2 → chưa ai xác nhận nó đủ. Thiếu 3 → đồ thị không biết bước sau được phép chạy. Cả ba mới khép được một bước.

## Mục bắt buộc tối thiểu theo giai đoạn (checkpoint kiểm)

- Problem (1–4): có ai đau + đau ở đâu (một câu cụ thể), một success metric đo được, scope in/out.
- Idea (0): input/output rõ, một plan thô đi được, ẩn số lớn nhất nêu tên.
- Domain (5): entity có identity + lifecycle, business rule bất biến, domain event chính, ranh giới context.
- Architecture (6) / Stack (7): quyết định + `rationale` + ít nhất một `rejected_alternative`.
- Contract (10): interface đủ để hai bên bám mà build độc lập (endpoint/field/kiểu, hoặc chữ ký hàm) — đây là cổng mở nhánh song song.
- Build (11): artifact code trỏ đúng path, gắn được về contract và AC.

## Vì sao siết ở đây

Yêu cầu của project: "mỗi bước xong phải có artifact và update vào folder tương ứng". Ba điều kiện trên biến câu đó thành thứ máy kiểm được, để `progress` không bao giờ đẩy nhánh sau khi bước trước mới nói miệng là xong.
