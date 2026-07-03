# Ví dụ chấm — một bản tốt vs một bản tệ

Dùng để calibrate: hai bản explain CÙNG fixture, chấm ra hai kết quả rõ ràng khác nhau. Đọc trước khi chấm để tay chấm đều.

**Fixture**: project = bộ skill `skillsh` · level = L2 (map — hiểu nghiệp vụ, chưa hiểu code flow) · mode = overview.

---

## Bản A (tốt)

> Skill.sh là bộ công cụ bạn tự dựng để Claude Code hiểu và làm việc trên codebase theo đúng mức hiểu của từng người. Nó ra đời vì giải thích code cho người mới và cho người rành phải khác nhau — một câu trả lời không vừa cho tất cả.
>
> Cả bộ xoay quanh một ý: dựng hiểu biết một lần rồi dùng lại. Có một phần lo đọc cả dự án và ghi lại thành bản đồ; các phần còn lại đọc bản đồ đó để làm việc của mình — dạy người hiểu, đóng khung một thay đổi, soi một luồng, tìm chỗ thiếu sót, hay điều phối từ ý tưởng đến bàn giao. Mỗi phần giữ đúng một việc và một chỗ ghi trạng thái riêng, nên không giẫm chân nhau. Cả quy trình bám một tài liệu gốc mô tả 15 giai đoạn từ ý tưởng đến vận hành.
>
> Bạn đang nắm được nghiệp vụ. Muốn tôi đi qua luồng chạy chính từng bước, hay có một phần cụ thể (vd cách các skill chia việc) bạn muốn xem trước?

```
CHẤM: explain · skillsh · L2 · overview

1 Mức        [2] — nói nghiệp vụ + nhắc "phần lo đọc cả dự án" như gợi ý, không nêu tên file/hàm; đúng L2.
2 Chế độ     [2] — overview đủ: làm gì + cho ai + vì sao tồn tại.
3 Đủ ý       [2] — nắm được cốt lõi "dựng một lần, dùng lại" và "mỗi phần một việc", có nhắc tài liệu 15 giai đoạn.
4 Lời văn    [2] — câu ngắn, phẳng, không tường bullet, không trích số dòng.
5 Bám code   [2] — khớp thật: atlas dựng bản đồ, skill khác đọc lại, mỗi skill một state; không bịa.
6 Ranh giới  [2] — dạy người hiểu, không tự dựng bản đồ, không liệt gap.
7 Kết        [2] — gợi ý đúng L2 (đi qua luồng từng bước / xem một phần trước).

TỔNG: 14/14   GATE: đạt
SỬA TRƯỚC TIÊN: không có lỗi chặn; nếu tinh, có thể nêu tên 1–2 skill trọng tâm để bớt trừu tượng.
```

## Bản B (tệ) — cùng fixture

> Skill.sh implement một multi-agent orchestration layer trên Claude Code. Kiến trúc:
> - `atlas`: chạy BFS traversal qua AST của repo, emit 20 artifact (xem `atlas/SKILL.md:24`).
> - `explain`: đọc `user-state.json`, dùng finite-state machine 8 trạng thái để route (`explain/SKILL.md:22`).
> - `router.py`: bộ điều phối trung tâm gọi từng skill qua một message bus.
> - `frame`, `partner`: dùng RAG pipeline với vector embedding để chọn slice.
>
> Toàn bộ chạy trên event loop async, mỗi skill là một microservice đăng ký qua dependency injection container.

```
CHẤM: explain · skillsh · L2 · overview

1 Mức        [0] — L2 mà đầy tên code/thuật ngữ (AST, FSM, router.py, microservice, DI); dùng code name dưới L4 → 0.
2 Chế độ     [1] — đi vào cách hoạt động (how) như architecture, thiếu "cho ai / vì sao tồn tại".
3 Đủ ý       [0] — đọc xong không biết bộ này để làm gì, vì sao có; người L2 mù hơn.
4 Lời văn    [0] — tường bullet + trích số dòng + thuật ngữ dày → khó đọc.
5 Bám code   [0] — bịa: router.py, message bus, RAG/vector embedding, microservice/DI, event loop đều không có thật (bộ này là các SKILL.md + state JSON).
6 Ranh giới  [1] — sa vào mô tả kiến trúc (việc gần atlas), không dạy hiểu theo mức.
7 Kết        [0] — không có gợi ý bước tiếp.

TỔNG: 2/14   GATE: rớt: tiêu chí 1 (Mức), 4 (Lời văn), 5 (Bám code)
SỬA TRƯỚC TIÊN: bỏ hết thuật ngữ/code name và claim bịa — nói bộ này GIẢI QUYẾT gì cho ai, bằng lời thường.
```

---

Điểm rút ra: bản B nghe "kêu" nhưng bịa kiến trúc và sai mức — đúng kiểu lỗi nguy hiểm nhất (người đọc tin nhầm). Gate bắt được nó dù nó dài và tự tin. Đó là lý do gate (tiêu chí 1/4/5) quan trọng hơn tổng điểm.
