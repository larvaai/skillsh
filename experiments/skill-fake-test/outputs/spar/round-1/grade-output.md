CHẤM: round 01 · reminder gửi lặp

— BẠN —
1 Đúng       [2] — không claim nào sai: retry mù, đa server, khoá theo user+thuốc+giờ, snooze là nhắc cố ý — đều đúng.
2 Đủ ý       [1] — nêu được nguyên nhân + cơ chế khoá + một đánh đổi + một ngoại lệ, nhưng thiếu ba mảnh: (a) chuẩn hoá khung giờ về mốc tất định để mọi worker sinh cùng khoá, (b) dùng ràng buộc UNIQUE của DB thay vì "tra rồi mới ghi" (tra-rồi-ghi vẫn race), (c) rủi ro claim xong worker chết làm KẸT liều — với app thuốc là rủi ro nặng.
3 Lập luận   [1] — có nêu vì sao khoá chặn được retry, nhưng "kiểm tra DB xem đã gửi chưa, gửi rồi thì bỏ" là chỗ hở: hai worker cùng đọc "chưa gửi" rồi cùng ghi — chưa dẫn tới vì sao cần cưỡng chế duy nhất ở tầng DB.
4 Rõ         [2] — câu ngắn, phẳng, dễ theo.
5 Trọng tâm  [2] — bám đúng cả ba ý câu hỏi, không lan man.
TỔNG: 8/10   GATE: đạt

— CLAUDE —
1 Đúng       [2] — mọi claim khớp thực tế: at-least-once vs exactly-once, INSERT ON CONFLICT, timeout cho bản ghi kẹt.
2 Đủ ý       [2] — đủ ba câu hỏi: 3 nguồn lặp + cơ chế khoá tất định có UNIQUE + đánh đổi + hai ngoại lệ (snooze, escalation) kèm ranh giới phân biệt.
3 Lập luận   [2] — chỉ ra được chỗ "tra rồi ghi" hở race và vì sao phải để DB cưỡng chế; mỗi đánh đổi gắn hệ quả (kẹt liều → nghiêng về thà-lặp-hiếm vì app y tế).
4 Rõ         [2] — chia mục, câu phẳng, list chỉ dùng chỗ giúp.
5 Trọng tâm  [2] — bám đúng câu hỏi từ đầu đến cuối.
TỔNG: 10/10  GATE: đạt

GÓP Ý CHO BẠN
- Bạn làm tốt hơn: gọi thẳng "snooze" là ngoại lệ hợp lệ ngay từ đầu — đúng và gọn, không vòng vo.
- Bạn thiếu: (1) cơ chế "tra DB xem đã gửi chưa rồi mới ghi" của bạn vẫn dính race hai worker cùng đọc "chưa" — cái chặn thật là ràng buộc UNIQUE để CHÍNH DB từ chối bản thứ hai; (2) khung giờ phải chuẩn hoá về một mốc tất định thì mọi worker mới sinh trùng khoá; (3) chưa chạm rủi ro claim-xong-mà-chết làm bỏ liều — với app thuốc đây là hỏng nặng hơn cả lặp.
- SỬA TRƯỚC TIÊN: khi thiết kế chống-trùng, đừng dừng ở "kiểm tra rồi mới làm" — hỏi tiếp "nếu hai bên cùng kiểm tra đúng lúc thì sao?". Đẩy tính duy nhất xuống chỗ cưỡng chế được (UNIQUE của DB), đừng để nó nằm trong trí nhớ của code.
