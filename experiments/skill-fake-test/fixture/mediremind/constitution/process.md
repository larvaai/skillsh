# Quy trình 0–14 — Idea đến Operate (MediRemind)

Đây là luật chơi về THỨ TỰ. Mỗi đề xuất đi qua đủ các tầng, không nhảy cóc. Được rút gọn độ sâu theo rủi ro, không được bỏ bước.

## 15 giai đoạn

```
0  Idea Intake           → Idea Brief
1  Business Discovery     → Business Case            ── WHY
2  Product Discovery      → Product Brief            ── WHAT VALUE
3  Requirements           → Requirement Catalogue    ── WHAT EXACTLY
4  PRD                    → PRD (bản đồng thuận)
5  Domain Model           → Domain Model             ── WORLD MODEL
6  Solution Architecture  → Architecture Brief       ── SHAPE
7  Tech Stack / Framework → Tech Decision Matrix      ── TOOLS
8  Live Slice             → Live Slice Report         ── PROOF
9  Roadmap & Backlog      → Roadmap + Epic→Feature→Story→AC ── PLAN
10 Module & Team Ownership→ Module Map + Contracts
11 Delivery / Build       → Delivery Standards + DoD  ── BUILD   ◄── con trỏ ĐANG Ở ĐÂY
12 Verification / UAT     → Test & Verification Report
13 Release Readiness      → Go/No-Go + Runbook        ── SHIP
14 Operations & Measure   → Ops Dashboard             ── LEARN → quay lại 9
```

## Ai quyết gì

```
Business     quyết WHY            — vì sao đáng làm
Product      quyết WHAT VALUE     — user cần trải nghiệm gì
Domain       quyết WORLD MODEL    — mô phỏng thế giới nghiệp vụ nào
Architecture quyết HOW SHAPED     — hệ thống có hình hài gì
Tech stack   quyết WITH WHAT      — dựng bằng công cụ nào
Backlog      quyết WHAT FIRST     — xây gì trước
Engineering  quyết HOW SAFELY     — giao hàng an toàn thế nào
Operations   quyết RUN & IMPROVE  — vận hành, cải tiến ra sao
```

## Điểm rẽ nhánh song song

Từ GĐ10, khi Module Map + Contract đã freeze, các module không phụ thuộc nhau có thể build song song. Với MediRemind: 4 bounded context (Scheduling · Reminders · Adherence · Identity & Access) đã có contract freeze ở GĐ10, nên trong GĐ11 các module không đụng nhau build cùng lúc — ví dụ Scheduling và Reminders (nhóm `pg-build`). Đây là chỗ `fanout` bung nhiều agent, mỗi agent bám cùng một Module Contract. Trước GĐ10 gần như luôn tuần tự vì mỗi bước là đầu vào của bước sau.

## Đủ-là-đủ

Độ sâu mỗi giai đoạn tỉ lệ với rủi ro và ẩn số, không tỉ lệ với vị trí trong luồng. MediRemind là modular monolith, đội 3 dev — rút gọn độ sâu ở chỗ đã rõ (vd ranh giới module theo đúng 4 bounded context), làm đầy ở chỗ rủi ro (dữ liệu sức khoẻ nhạy cảm → NFR-4, timeliness reminder → NFR-1). Không bao giờ nhảy cóc giai đoạn để tiết kiệm — chỉ được rút gọn độ sâu.
