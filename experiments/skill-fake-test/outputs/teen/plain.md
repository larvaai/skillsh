# Chuỗi ngày uống thuốc đều — giải thích bằng lời thường

## Vấn đề đoạn này lo

Đoạn này lo việc: **đếm xem người dùng đã uống thuốc đủ liều liên tiếp bao nhiêu ngày, tính ngược từ hôm nay trở về.**

## Nó làm việc đó thế nào

Trong ứng dụng nhắc thuốc này, mỗi lần tới giờ uống thuốc sẽ để lại một dấu vết. Dấu vết đó nói: giờ hẹn là lúc nào, và người dùng đã "uống", đã "bỏ", hay chưa rõ.

Đoạn này gom tất cả các dấu vết đó lại rồi làm ba việc theo thứ tự:

Đầu tiên, nó xếp mọi dấu vết vào đúng ngày của chúng — tất cả những lần uống thuốc trong cùng một ngày lịch được gộp về một chỗ. Với mỗi lần trong ngày, nó ghi lại một điểm: uống thì cộng một điểm, bỏ thì trừ một điểm, còn chưa rõ thì để trống (không âm không dương).

Tiếp theo, nó xếp các ngày lại theo thứ tự mới nhất trước, cũ nhất sau — để bắt đầu đếm từ ngày gần đây nhất đi ngược về quá khứ.

Cuối cùng, nó đi qua từng ngày một, bắt đầu từ ngày mới nhất. Một ngày chỉ được tính là "ngày tốt" khi mọi lần uống trong ngày đó đều đã được uống thật — không có lần nào bỏ, và cũng không có lần nào còn để trống chưa rõ. Cứ gặp một ngày tốt thì cộng thêm một vào con số đếm và đi tiếp sang ngày trước đó. Nhưng ngay khi gặp ngày đầu tiên không đạt, nó dừng lại luôn, không đếm nữa. Con số đếm được chính là số ngày đều liên tiếp tính từ hôm nay.

## Chạy thử bằng lời

Giả sử hôm nay và hôm qua người dùng uống đủ mọi liều, còn hôm kia thì bỏ một liều.

Nó nhìn ngày mới nhất là hôm nay: mọi liều đều đã uống, không có gì bỏ hay để trống — ngày tốt, con số đếm lên thành một.

Nó lùi về hôm qua: cũng đủ cả, không sót — ngày tốt, con số đếm lên thành hai.

Nó lùi tiếp về hôm kia: có một liều bị bỏ — ngày này không đạt, nó dừng lại ngay tại đây.

Kết quả trả về là hai: người dùng đang có chuỗi hai ngày uống thuốc đều.

## Vì sao chuyện này quan trọng

Con số chuỗi ngày đều này cho người dùng thấy họ đang theo đúng lịch uống thuốc tới đâu, và chỉ cần một ngày sót là chuỗi đứt — đúng như ý nghĩa của việc uống thuốc phải đều đặn mới có tác dụng.
