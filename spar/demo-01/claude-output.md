# Các bước hiện thực: agent tự chia task theo độ khó, đệ quy nhiều tầng

Ý tưởng gọn lại: đưa agent một task; nó tự chấm khó hay dễ; dễ thì làm thẳng, khó thì chẻ thành các step con; bước vào từng step con, nếu vẫn khó lại chẻ tiếp. Cây task lớn dần theo id: `1.0` → `1.0.0`, `1.0.1` → `1.0.0.0`… Đây là đệ quy chia-để-trị, và chỗ khó không phải "chia thế nào" mà là "khi nào NGỪNG chia" và "gom kết quả ngược lên ra sao".

Dưới đây là các bước để dựng nó, xếp theo thứ tự nên làm.

## Bước 1 — Chốt một "task" là gì

Trước khi chia, phải có khuôn cho một task. Mỗi task là một nút, tối thiểu có: `id` (1.0, 1.0.0…), mô tả việc, **tiêu chí xong** (làm sao biết task này đã đạt — thứ này bắt buộc, thiếu nó thì không kiểm được và không biết lúc nào dừng), trạng thái (chờ / đang làm / xong / kẹt), và con trỏ tới task cha + danh sách con. Cả cây task lưu ra một file (JSON), để theo dõi được và chạy lại được khi đứt.

## Bước 2 — Một hàm xử-lý-một-task, gọi lại chính nó

Trái tim là một hàm nhận một task và làm đúng ba việc, theo thứ tự:

1. **Chấm độ khó** task này (Bước 3).
2. **Quyết**: đủ nhỏ để làm thẳng → sang Bước 5 làm thật. Còn khó → sang Bước 4 chẻ nhỏ.
3. Nếu chẻ: sinh các task con, rồi **gọi lại chính hàm này** cho từng con. Đó là chỗ đệ quy sinh ra tầng `1.0.0`, `1.0.0.0`…

## Bước 3 — Chấm khó/dễ bằng tiêu chí rõ, không cảm tính

"Khó hay dễ" phải quy về câu hỏi kiểm được, nếu không mỗi lần chấm một kiểu. Dùng vài mốc cụ thể: task này có làm gọn trong **một bước đáng tin** không (một lần gọi, một thay đổi, kiểm được ngay)? Mô tả còn mơ hồ tới mức chưa biết bắt đầu từ đâu không? Nó có đụng nhiều phần tách rời nhau không? "Khó" = một trong các dấu đó đúng. "Dễ" = làm thẳng được và nghiệm thu được ngay.

## Bước 4 — Chẻ task cha thành các con, đánh id nối tiếp

Khi quyết chẻ: sinh danh sách step con có thứ tự, mỗi con là một task mới với id nối từ cha (`1.0` → `1.0.0`, `1.0.1`…). Hai điều kiện cho một lần chẻ tốt: các con **cộng lại đúng bằng** task cha (đủ, không thiếu việc), và **không chồng lấn** nhau. Ghi luôn thứ tự phụ thuộc — con nào phải xong trước con nào — vì lát nữa thực thi theo thứ tự đó.

## Bước 5 — Ngưỡng dừng đệ quy (chỗ dễ hỏng nhất)

Không có ngưỡng thì agent hoặc chia mãi, hoặc chẻ ra con to gần bằng cha rồi chẻ tiếp vô nghĩa. Cần ba chốt chặn, đụng cái nào thì DỪNG chẻ:

- **Đủ nhỏ**: task đã "dễ" theo Bước 3 → làm thẳng, không chẻ nữa.
- **Chạm đáy độ sâu**: đặt giới hạn tầng tối đa (vd 4–5 tầng). Tới đáy mà vẫn khó → không chẻ tiếp, đánh dấu kẹt, đẩy lên người.
- **Chẻ không tiến triển**: nếu các con sinh ra gần bằng cha (chia mà không nhỏ đi), coi như chia hỏng → dừng, báo, đừng lặp.

## Bước 6 — Làm thật ở lá, rồi gom kết quả ngược lên

Duyệt cây theo chiều sâu và đúng thứ tự phụ thuộc. Chỉ **lá** (task đã "dễ") mới được làm thật. Khi mọi con của một task cha đã xong, **tổng hợp** kết quả các con thành kết quả của cha, rồi kiểm tiêu chí xong của cha — đạt thì cha mới tính xong. Cứ thế gom lên tới gốc. Bước gom này quan trọng ngang bước chẻ: chia mà không ráp lại thì chỉ có mảnh vụn.

## Bước 7 — Chặn chi phí và xử lý kẹt

Đặt trần tổng: số task tối đa và ngân sách (thời gian/lượt gọi) cho cả cây, để một nhánh xấu không nuốt hết tài nguyên. Một lá không làm được thì **không im lặng**: đánh dấu `kẹt`, ghi lý do, thử hướng khác hoặc đẩy lên người quyết. Task cha có con kẹt thì cha cũng chưa xong — trạng thái kẹt phải nổi lên tới nơi có người nhìn.

## Bước 8 — Dựng lát nhỏ nhất trước, rồi mới mở đệ quy

Đừng dựng full đệ quy ngay. Làm bản một tầng trước: nhận task → chẻ đúng một lần → làm các con → gom lên. Chạy đúng đã, rồi mới cho hàm gọi lại chính nó để lên tầng `1.0.0`. Có bản một tầng chạy được làm mốc, việc mở lên nhiều tầng chỉ là bật đệ quy + bật ba chốt chặn ở Bước 5, không phải viết lại.

## Tóm một câu

Một khuôn task có tiêu chí xong, một hàm đệ quy chấm-rồi-quyết (làm thẳng hay chẻ), ba chốt chặn để biết lúc nào ngừng chẻ, và một bước gom kết quả ngược lên gốc — đó là bộ xương. Chẻ là nửa dễ; ngưỡng dừng và gom ngược lên mới là nửa quyết định nó có chạy thật hay không.
