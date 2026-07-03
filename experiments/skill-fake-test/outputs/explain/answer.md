# MediRemind — overview (mức L3)

## Nó là cái máy để làm gì

Người phải uống thuốc đúng giờ, đúng ngày, thường quên. Người già uống nhiều loại một lúc còn dễ quên hơn, và người nhà thì lo không biết hôm nay họ đã uống chưa. MediRemind là cái máy nhắc uống thuốc và theo dõi có uống đủ không. Nó nhắc đúng giờ, cho người bệnh bấm "đã uống", rồi tính ra tỉ lệ tuân thủ để cả bệnh nhân lẫn người chăm (caregiver) nhìn vào biết tình hình.

Người hưởng lợi có hai nhóm. Một là bệnh nhân — được nhắc và tự xác nhận. Hai là người chăm sóc — được xem báo cáo tuân thủ của người mình lo, nhưng chỉ được xem, không sửa. Bản trong repo là một bản demo dựng để chứng minh luồng chạy: kho dữ liệu còn để tạm trong bộ nhớ, cổng gửi tin nhắn còn là hàng giả, comment trong code ghi rõ "thật sẽ là Postgres / thật sẽ gọi HTTP tới provider".

## Ý tưởng cốt lõi (một câu)

Thay vì canh từng phút xem tới giờ ai chưa, hệ tách làm hai nhịp: mỗi sáng dựng sẵn danh sách "hôm nay ai phải uống liều gì lúc mấy giờ", rồi trong ngày chỉ việc quét danh sách đó và bắn nhắc cái nào sắp tới hạn. Dựng trước một lần, nhắc nhiều lần trong ngày. Nhờ tách vậy nên việc "tính lịch" và việc "gửi nhắc" không dẫm lên nhau, và mỗi lần uống trở thành một mẩu dữ liệu rõ ràng để sau này tính ra tỉ lệ tuân thủ.

Điều này đáng với business vì giá trị của sản phẩm nằm ở con số "có uống đủ không". Muốn có con số đó thì mỗi liều phải là một bản ghi có trạng thái — chưa tới giờ, đã uống, bỏ lỡ, hay chủ động bỏ. Cái danh sách dựng mỗi sáng chính là chỗ những bản ghi đó ra đời.

## Luồng "bạn ở đây" — một liều thuốc đi từ lịch tới báo cáo

Đây là bản đồ để mọi chi tiết sau này định vị. Đọc từ trên xuống là đi hết vòng đời một liều thuốc.

1. Bệnh nhân có sẵn một **lịch uống** (schedule): thuốc này, những giờ nào trong ngày, những thứ mấy trong tuần, từ ngày nào tới ngày nào.
2. Mỗi sáng lúc 00:05, một tác vụ chạy nền tự bật (cron trong tiến trình) gọi bộ **sinh liều** (dose generator). Nó đọc các lịch đang hoạt động và đẻ ra danh sách **liều trong ngày** (dose event) — mỗi liều gắn một giờ cụ thể và bắt đầu ở trạng thái "chưa tới giờ".
3. Cũng tác vụ nền đó, nhưng nhịp mỗi phút, gọi bộ **gửi nhắc** (reminder service). Nó quét các liều sắp tới hạn trong cửa sổ vài phút tới và bắn thông báo qua **cổng gửi tin** (push provider) — chỗ này về sau nối ra Expo/Twilio, hiện là hàng giả.
4. Bệnh nhân nhận nhắc, uống thuốc, rồi bấm "Đã uống". Cú bấm đó vào **cửa xác nhận liều** (dose controller) — một endpoint HTTP; danh tính người bấm đã được lớp auth gắn sẵn trước khi tới đây.
5. Cửa đó đổi trạng thái liều thành "đã uống" và ghi giờ uống.
6. Ngay sau khi đổi, hệ gọi bộ **tính tuân thủ** (adherence service) để ra tỉ lệ đã-uống trên tổng, trả về cho màn hình. Cạnh đó có bộ tính **chuỗi ngày liên tiếp** (streak) để khích lệ.
7. Người chăm sóc muốn xem báo cáo của bệnh nhân thì phải qua một **chốt quyền** (caregiver guard): chỉ ai có liên kết chăm-sóc đúng phạm vi "chỉ-xem" mới được nhìn.

Hai nhịp ở bước 2 và 3 chạy trong CÙNG một tiến trình, bằng hàm hẹn giờ (`setInterval`/cron nội bộ), không có hàng đợi tin nhắn, không có Kafka, không có service tách rời. Đây là một khối đơn (monolith) chia theo domain, không phải hệ microservice.

## Các phần (module) — mỗi cái là một chỗ trong luồng trên

Code chia thư mục theo lĩnh vực nghiệp vụ, mỗi thư mục lo một khúc của luồng.

- **`scheduling/`** — khúc lịch và sinh liều ở bước 1–2. Đây định nghĩa "lịch uống" và "liều trong ngày" là gì, và bộ sinh liều dựng danh sách mỗi sáng. Đáng chú ý: lịch có ghi múi giờ của người dùng nhưng bộ sinh liều hiện chưa dùng tới — nó tính theo giờ máy chủ (comment trong code tự đánh dấu đây là chỗ chưa xong).
- **`reminders/`** — khúc gửi nhắc ở bước 3, cùng hai cái đồng hồ hẹn giờ. Một hàm chạy nhịp-mỗi-sáng để gọi sinh liều, một hàm chạy nhịp-mỗi-phút để gọi gửi nhắc. Đây là "trái tim chạy nền" của hệ, nhưng chỉ là hàm hẹn giờ trong tiến trình chứ không phải worker riêng.
- **`adherence/`** — khúc xác nhận và đo lường ở bước 4–6. Gồm cửa xác nhận liều (endpoint bấm "đã uống"), bộ tính tỉ lệ tuân thủ, và bộ tính chuỗi ngày liên tiếp. Đây là chỗ dữ liệu biến thành con số mà sản phẩm bán.
- **`identity/`** — chốt quyền của người chăm sóc ở bước 7. Nhỏ nhưng là ranh giới ai được xem của ai.
- **`common/`** — hạ tầng dùng chung: kho dữ liệu (hiện để tạm trong bộ nhớ, mô phỏng Postgres) và cổng gửi tin ra ngoài (hiện là hàng giả). Mọi module đọc/ghi qua kho này.
- **`legacy/`** — bản nhắc thuốc đời đầu, viết trước khi tách bộ gửi nhắc riêng. Không còn được gọi ở đâu, giữ lại "phòng khi cần". Không nằm trong luồng chạy hiện tại.

## Vì sao cách này đáng (nhắc lại giá trị)

Tách "dựng lịch mỗi sáng" khỏi "gửi nhắc mỗi phút" giúp mỗi liều thành một bản ghi có trạng thái — và đó chính là nguyên liệu để tính ra tỉ lệ tuân thủ, thứ giá trị nhất với bệnh nhân lẫn người chăm. Chia theo domain (lịch / nhắc / tuân thủ / danh tính) giúp mỗi khúc sửa riêng được mà không đụng khúc khác. Đây là một khối đơn chạy gọn trong một tiến trình — đủ để chứng minh luồng, chưa phải hệ phân tán.

## Gợi ý bước tiếp (mức L3)

Bạn muốn tôi đi sâu trách nhiệm từng phần, hay có module nào bạn đang thắc mắc? Nếu muốn theo một liều chạy qua từng bước và dừng lại xem kỹ ở mỗi chặng, đó là chế độ *flow*. Nếu bạn đã nắm hình hài và muốn soi những chỗ code tự đánh dấu là chưa xong (múi giờ, gửi trùng, quyền xác nhận), đó là việc của skill `review`.
