## Các bước hiện thực

1. **Chuẩn hóa task đầu vào**
   - Mỗi task có: mục tiêu, dữ liệu đầu vào, kết quả mong đợi, tiêu chí hoàn thành và ràng buộc.
   - Gán mã phân cấp: `1.0`, `1.0.0`, `1.0.1`...

2. **Cho agent đánh giá task**
   Agent phải trả về dữ liệu có cấu trúc:
   - Mức độ khó và độ tin cậy.
   - Task có thể thực hiện trực tiếp hay cần chia nhỏ.
   - Lý do.
   - Danh sách step con nếu cần.

3. **Đặt tiêu chí chia nhỏ**
   Task được xem là khó khi:
   - Có nhiều kết quả trung gian phụ thuộc nhau.
   - Thiếu thông tin hoặc cần khám phá.
   - Không thể kiểm chứng bằng một tiêu chí rõ ràng.
   - Ước lượng vượt giới hạn thời gian, token hoặc công cụ.
   - Agent có độ tin cậy thấp.

4. **Xây dựng bộ điều phối đệ quy**
   ```text
   process(task):
       assessment = agent.assess(task)

       if assessment.can_execute:
           result = agent.execute(task)
           return verify(task, result)

       children = create_subtasks(task, assessment.steps)

       for child in dependency_order(children):
           process(child)

       return aggregate_and_verify(task, children)
   ```

5. **Biểu diễn dưới dạng cây task**
   - `1.0`: task gốc.
   - `1.0.0`, `1.0.1`: các task con.
   - Mỗi node lưu `pending`, `running`, `completed`, `failed` hoặc `blocked`.
   - Lưu cả quan hệ phụ thuộc, kết quả, lỗi và số lần thử.

6. **Đánh giá lại tại mọi node**
   Khi agent bắt đầu `1.0.0`, nó phải chạy lại cùng quy trình đánh giá. Nếu vẫn khó, tiếp tục sinh `1.0.0.0`, `1.0.0.1`... Không mặc định rằng task con luôn đủ nhỏ.

7. **Đặt điều kiện dừng**
   - Giới hạn độ sâu.
   - Giới hạn tổng số task con.
   - Giới hạn thời gian, token và chi phí.
   - Không chia nếu task con không nhỏ hơn task cha.
   - Nếu vẫn không thực hiện được ở giới hạn cuối, chuyển sang `blocked` và nêu rõ thông tin cần bổ sung.

8. **Kiểm chứng và tổng hợp**
   - Mỗi task con phải có tiêu chí nghiệm thu riêng.
   - Chỉ hoàn thành task cha khi các task con bắt buộc đã đạt yêu cầu.
   - Agent tổng hợp kết quả con và kiểm tra lại theo tiêu chí của task cha.

9. **Bổ sung cơ chế phục hồi**
   - Retry có giới hạn.
   - Cho phép lập kế hoạch lại khi một nhánh thất bại.
   - Tránh tạo task trùng lặp.
   - Ghi lại toàn bộ quyết định để theo dõi và gỡ lỗi.

Điểm quan trọng là không để agent tự do chia task vô hạn. Việc phân rã phải tạo ra các task nhỏ hơn, có đầu ra kiểm chứng được và chịu giới hạn tài nguyên rõ ràng.
