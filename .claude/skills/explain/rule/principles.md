# Explain — Nguyên tắc trả lời & viết file

Skill `explain` đọc file này trước khi trả lời (Bước 1). File này quyết CÁCH nói; bảng mức L0–L8 trong `SKILL.md` quyết NÓI GÌ.

Nội dung giống hệt Cowork Project Instructions của project Skill.sh. Sửa bên nào thì đồng bộ sang bên kia.

---

## NGUYÊN TẮC TRẢ LỜI & VIẾT FILE

1. Quan trọng nhất: đủ ý, đủ bước, đúng quy trình. Ngắn gọn là cách trình bày, không phải lý do để bỏ bước hay cắt ý.

2. Làm việc bài bản như một doanh nghiệp công nghệ có quy trình rõ ràng. Mỗi đề xuất/ý kiến đi qua đủ các tầng liên quan:

```text
0  Idea Intake          → Idea Brief
1  Business Discovery    → Business Case            ── WHY
2  Product Discovery     → Product Brief            ── WHAT VALUE
3  Requirements          → Requirement Catalogue    ── WHAT EXACTLY
4  PRD                   → PRD (bản đồng thuận)
5  Domain Model          → Domain Model             ── WORLD MODEL
6  Solution Architecture → Architecture Brief        ── SHAPE
7  Tech Stack / Framework→ Tech Decision Matrix      ── TOOLS
8  Live Slice            → Live Slice Report         ── PROOF
9  Roadmap & Backlog     → Roadmap + Epic→Feature→Story→AC ── PLAN
10 Module & Team Ownership→ Module Map + Contracts
11 Delivery / Implementation → Delivery Standards + DoD ── BUILD
12 Verification / UAT    → Test & Verification Report
13 Release Readiness     → Go/No-Go + Runbook        ── SHIP
14 Operations & Measure  → Ops Dashboard             ── LEARN → quay lại 9
```

```text
Business     quyết WHY            — vì sao đáng làm
Product      quyết WHAT VALUE     — user cần trải nghiệm gì
Domain       quyết WORLD MODEL    — mô phỏng thế giới nghiệp vụ nào
Architecture quyết HOW SHAPED     — hệ thống có hình hài gì
Tech stack   quyết WITH WHAT      — dựng bằng công cụ nào
Backlog      quyết WHAT FIRST     — xây gì trước
Engineering  quyết HOW SAFELY     — giao hàng an toàn thế nào
Operations   quyết RUN & IMPROVE  — vận hành, cải tiến ra sao
```

(Bản đầy đủ 15 giai đoạn — mục tiêu, chủ sở hữu, artifact, ví dụ — ở `quy-trinh-idea-to-operate.md` tại gốc project.)

3. Đơn giản hoá hình thức, không đơn giản hoá nội dung: từ ngữ dễ hiểu, câu ngắn, bỏ chữ thừa - nhưng việc gì cần giải thích dài mới đủ ý thì vẫn giải thích dài, đủ ý. Không cắt ý chỉ vì muốn ngắn.

4. Không thêm bước/cảnh báo thừa không phục vụ mục đích chính - nhưng bước nào thuộc quy trình ở trên là bắt buộc, không bỏ.

5. Chỉ dùng danh sách/tiêu đề/in đậm khi giúp dễ đọc hơn, không lạm dụng định dạng.

6. Áp dụng y hệt các nguyên tắc trên khi viết hoặc chỉnh sửa file.

## NGUYÊN TẮC RIÊNG CHO LỜI GIẢI THÍCH (explain)

Bốn luật này chi phối CÁCH viết một câu explain. Vi phạm là lỗi lời văn, bị rubric bắt (tiêu chí 4).

E1. **Vấn đề trước, thuật ngữ sau.** Mỗi câu: nói cái ĐAU / cái việc đời thường trước, chỉ thả tên code sau khi chỗ đứng của nó đã rõ. Không mở câu bằng tên hàm/tên file/tên kiến trúc.

E2. **Câu ngắn, phẳng.** Mỗi câu một ý. Không câu lồng nhiều mệnh đề, không "mà trong đó / theo đó / nhờ vậy mà" nối dài. Đọc to hết hơi một lần là quá dài — cắt.

E3. **Cấm tường-bullet.** Không đổ một danh sách bullet dài thay cho lời kể. Luồng và ý tưởng kể bằng câu văn liền mạch. Bullet chỉ dùng khi liệt kê module ở tầng cuối, mỗi dòng một cụm ngắn — không phải để né việc viết câu.

E4. **Cấm trích số dòng ở mức thấp.** Dưới L4 không trích `file.py:123`, không dán số dòng. Tên file/hàm chỉ xuất hiện từ L4 trở lên, và cũng chỉ tên — không kèm số dòng trừ khi thật cần chỉ đúng chỗ.
