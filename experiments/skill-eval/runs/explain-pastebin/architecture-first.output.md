# explain-pastebin · architecture-first (baseline yeu) — OUTPUT (skill: explain)

# Pastebin — tổng quan kiến trúc (mức L2)

Hệ thống này là một kiến trúc **web-tier tách write-path / read-path**, đặt sau một **reverse proxy Web Server**, với một **SQL Database** làm hash table tra cứu và một **Object Store** (kiểu Amazon S3) làm nơi chứa nội dung. Trước một **CDN** và một **Memory Cache** để phục vụ đọc, phía sau là **SQL Master-Slave** có read-replica. Một job **MapReduce** chạy offline trên log của Web Server để ra số liệu analytics.

Cụ thể các thành phần:

- **Web Server (reverse proxy)** — điểm nhận mọi request từ Client, rồi định tuyến sang API tương ứng.
- **Write API server** — xử lý đường ghi: sinh URL duy nhất bằng cách lấy **MD5 hash** của `ip_address + timestamp`, rồi **Base 62 encode** và cắt lấy 7 ký tự đầu (không gian 62^7 giá trị). Ghi bản ghi vào bảng `pastes` của **SQL Database** và ghi nội dung vào **Object Store**.
- **Read API server** — xử lý đường đọc: tra `shortlink` trong **SQL Database**, nếu có thì fetch nội dung từ **Object Store**, không có thì trả lỗi.
- **SQL Database** — bảng `pastes` với các cột `shortlink char(7)`, `expiration_length_in_minutes`, `created_at`, `paste_path`, `PRIMARY KEY(shortlink)`. Có thêm index trên `created_at` để tra cứu log-time và giữ dữ liệu trong bộ nhớ.
- **Object Store (S3)** — chứa nội dung paste (text, ~1 KB/paste), tách khỏi metadata trong SQL.
- **Memory Cache + SQL Read Replicas + CDN** — tầng phục vụ đọc, hấp thụ traffic nóng và traffic không đều.
- **MapReduce (`HitCounts`)** — job offline gồm `mapper` phát cặp `(period, url) → 1` và `reducer` cộng tổng, cho ra số lượt truy cập theo tháng.

## API bề mặt

Giao tiếp ngoài dùng **REST**, giao tiếp nội bộ dùng **RPC**.

Ghi paste:
```
POST https://pastebin.com/api/v1/paste
{ "expiration_length_in_minutes": "60", "paste_contents": "Hello World!" }
→ { "shortlink": "foobar" }
```

Đọc paste:
```
GET https://pastebin.com/api/v1/paste?shortlink=foobar
→ { "paste_contents": "...", "created_at": "...", "expiration_length_in_minutes": "60" }
```

---

Bây giờ mới nói công dụng: đây là bản thiết kế của một dịch vụ kiểu **Pastebin.com / Bit.ly** — người dùng dán một khối văn bản vào và nhận về một đường link ngắn ngẫu nhiên; ai có link thì mở ra xem lại nội dung. Người dùng ẩn danh, không cần đăng ký. Paste mặc định không hết hạn, nhưng có thể đặt thời hạn; dịch vụ tự xóa paste hết hạn và thống kê lượt xem theo tháng.

Bài toán quy mô mà thiết kế nhắm tới: 10 triệu người dùng, 10 triệu lượt ghi paste/tháng, 100 triệu lượt đọc/tháng — tỷ lệ đọc:ghi khoảng 10:1 (~4 ghi/giây và ~40 đọc/giây trung bình). Trong 3 năm sinh ra ~450 GB nội dung và ~360 triệu shortlink. Chính vì đọc nhiều hơn ghi 10 lần và traffic không phân bố đều, kiến trúc mới tách hẳn đường đọc ra để cache/replica gánh, còn đường ghi giữ đơn giản trên một SQL master.

## Luồng chạy (map "bạn ở đây")

Đường ghi — người dùng tạo paste:
1. Client gửi request tạo paste tới **Web Server**.
2. Web Server chuyển tiếp sang **Write API server**.
3. Write API sinh một URL ngắn: MD5(`ip_address + timestamp`) → Base 62 → lấy 7 ký tự đầu.
4. Kiểm tra `shortlink` đó đã tồn tại trong **SQL Database** chưa; trùng thì sinh lại.
5. Ghi bản ghi (metadata) vào bảng `pastes` của SQL; ghi nội dung vào **Object Store**.
6. Trả `shortlink` về cho Client.

Đường đọc — người dùng mở link:
1. Client gửi request đọc tới **Web Server**.
2. Web Server chuyển tiếp sang **Read API server**.
3. Read API tra `shortlink` trong **SQL Database** (trước đó thường trúng **Memory Cache**).
4. Có thì fetch nội dung từ **Object Store** và trả về (kèm `created_at`, `expiration_length_in_minutes`); không có thì trả lỗi.

Hai đường phụ chạy nền: một tiến trình quét **SQL Database** tìm bản ghi quá hạn để xóa/đánh dấu hết hạn; một job **MapReduce** chạy trên log Web Server để đếm lượt xem theo tháng (analytics không cần realtime nên để offline).

## Vì sao hình hài này (nhắc lại giá trị)

Tách metadata (SQL) khỏi nội dung (Object Store) để SQL nhẹ, tra `shortlink` nhanh, còn khối text nặng đẩy sang S3 rẻ và co giãn được. Tách write-path khỏi read-path để bên đọc gấp 10 lần bên ghi được cache và read-replica gánh riêng, không đụng tới master ghi. Sinh link bằng hash + Base 62 để ra chuỗi 7 ký tự chỉ gồm `[a-zA-Z0-9]`, hợp với URL và đủ 62^7 tổ hợp cho 360 triệu link trong 3 năm.

---

Bạn muốn tôi đi qua luồng chạy từng bước (ví dụ soi kỹ đường ghi tạo shortlink), hay có một luồng cụ thể — như xử lý hết hạn hoặc analytics — bạn muốn xem trước?

(Bạn đang ở L2 — map. Sau lần này, bạn thấy mình đang ở mức nào? L0 locate / L1 scout / L2 map / L3 flow / L4 structure / L5 trace / L6 review / L7 plan / L8 architect)
