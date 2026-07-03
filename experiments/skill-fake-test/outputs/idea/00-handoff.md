# Bàn giao — MediRemind (sau GĐ5 Domain)

```
═══ BÀN GIAO — MediRemind ═══
Domain đã chốt:
  4 bounded context (Identity&Access · Scheduling · Reminders · Adherence);
  entity trung tâm DoseEvent với state machine pending→taken/skipped/missed;
  rule chính: caregiver chỉ-xem (BR-1), phải có CaregiverLink active + audit mọi truy cập (BR-2/3),
  cửa sổ on-time quyết taken/missed (BR-4).
Artifact:
  - outputs/idea/01-idea-brief.md      (GĐ0 Idea Brief + Router)
  - outputs/idea/02-business-case.md   (GĐ1 Business Case)
  - outputs/idea/03-prd.md             (GĐ2–4 Product/Requirements/PRD)
  - outputs/idea/04-domain-model.md    (GĐ5 Domain Model — điểm DỪNG)
→ Bước kế mặc định — định hình kiến trúc (GĐ6): chạy /shape (rồi /stack → /skeleton…)
→ Initiative lớn, nhiều team, cần điều phối + traceability đủ: chạy /partner
→ Chỉ cần build ngay một lát cắt nhỏ: chạy /frame
→ Cần hiểu code cũ trước khi domain đụng vào: chạy /atlas hoặc /explain
════════════════
```

Open questions mang sang GĐ6+ (không giải ở idea): ngưỡng số cứng NFR (OQ-2), realtime vs
batch cho sinh DoseEvent + dispatch reminder (OQ-3), retention dữ liệu sức khoẻ (OQ-4), ranh giới
ghi DoseEvent giữa Scheduling↔Adherence, độ rộng cửa sổ on-time (BR-4).

Không tự chọn hộ skill kế — user quyết.
