# Ví dụ — một round hoàn chỉnh trông ra sao

Bốn file của round `spar/07-cache-invalidation/`. Đọc để thấy đầu vào/đầu ra khớp nhau thế nào và grade-output coach ra sao.

## prompt.md (sau khi user đã trả lời)

```
---
status: user-answered
round: 07
topic: cache invalidation
rubric: default
---

# Câu hỏi
Vì sao "cache invalidation" nổi tiếng là một trong hai thứ khó nhất trong lập
trình? Nêu bản chất cái khó, một ví dụ hỏng thực tế, và một cách giảm đau.
```

## user-output.md (bản của người dùng)

```
Cache khó vì dữ liệu gốc đổi mà cache không biết, nên trả ra bản cũ.
Ví dụ: đổi giá sản phẩm nhưng trang vẫn hiện giá cũ vì còn cache.
Cách giảm: đặt thời gian hết hạn cho cache.
```

## claude-output.md (bản của Claude, viết sau, không nhại bản user)

```
Cái khó không nằm ở việc lưu bản sao — mà ở việc biết CHÍNH XÁC lúc nào bản sao
đã sai. Nguồn sự thật (database) và bản sao (cache) là hai nơi; mỗi khi nguồn
đổi, mọi bản sao liên quan phải được đánh dấu cũ. Khó ở ba chỗ: (1) một thay đổi
có thể ảnh hưởng nhiều key cache khó liệt hết; (2) nhiều máy chủ giữ cache riêng,
xoá nơi này còn sót nơi khác; (3) đúng lúc xoá xong lại có request nạp lại bản cũ
(race).

Ví dụ hỏng: sàn thương mại đổi giá về 0 để test, invalidation sót một tầng CDN,
khách mua được hàng giá 0 trong nhiều phút.

Giảm đau, theo thứ tự nên thử: đặt TTL ngắn để cái sai tự hết hạn (đơn giản nhất,
chấp nhận trễ); hoặc chủ động xoá key khi ghi (đúng hơn, phức tạp hơn); hoặc gắn
version vào key để bản mới không đụng bản cũ. Chọn theo mức chịu-được-dữ-liệu-cũ.
```

## grade-output.md

```
CHẤM: round 07 · cache invalidation

— BẠN —
1 Đúng       [2] — không sai chỗ nào.
2 Đủ ý       [1] — nêu được bản chất + ví dụ, nhưng chỉ một cách giảm (TTL), thiếu chủ động xoá / version.
3 Lập luận   [1] — có nêu vì sao khó nhưng dừng ở một tầng, chưa chạm race/nhiều máy chủ.
4 Rõ         [2] — câu ngắn, dễ đọc.
5 Trọng tâm  [2] — bám đúng câu hỏi.
TỔNG: 8/10   GATE: đạt

— CLAUDE —
1 Đúng       [2] — khớp thực tế.
2 Đủ ý       [2] — bản chất + 3 tầng khó + ví dụ + 3 cách giảm.
3 Lập luận   [2] — mỗi cách giảm gắn với đánh đổi.
4 Rõ         [2] — phẳng, đủ ý.
5 Trọng tâm  [2] — không lan man.
TỔNG: 10/10  GATE: đạt

GÓP Ý CHO BẠN
- Bạn làm tốt hơn: ví dụ giá của bạn cụ thể và đời thường, dễ hình dung.
- Bạn thiếu: cái khó thật nằm ở "nhiều bản sao trên nhiều máy" và "race lúc nạp lại" — bạn mới chạm một tầng. Và mới một cách giảm.
- SỬA TRƯỚC TIÊN: khi câu hỏi xin "một cách", vẫn nên nêu 2–3 lựa chọn kèm đánh đổi — người đọc cần biết chọn cái nào khi nào, không chỉ một đáp án.
```

Chú ý: bản của Claude 10/10, bản của bạn 8/10 — nhưng grade-output không dừng ở đó, phần coach chỉ đúng một đòn bẩy để lần sau bạn kéo điểm "đủ ý" và "lập luận" lên.
