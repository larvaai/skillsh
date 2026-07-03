# 04 — Architecture Map

> built_at: 2026-07-03T10:26:11Z · built_commit: n/a · scope: partial (bản scaled)

## Observed style
**Feature-based + layered nhẹ** (modular slice). Code tách theo tính năng-domain (scheduling / reminders / adherence / identity) với hạ tầng chung (common). Trong mỗi feature có tách entity ↔ service ↔ controller/worker.

Evidence:
- File path: cây thư mục src/{scheduling,reminders,adherence,identity,common,legacy}
- Symbol: mỗi feature có *.service.ts; adherence có dose.controller.ts; reminders có reminder.worker.ts; scheduling có *.entity.ts
- Suy luận: phân theo domain feature, không phân theo tầng kỹ thuật thuần (không có thư mục controllers/ services/ toàn cục)
- Mức chắc chắn: chắc chắn

## Layers (quan sát được)
| Layer | Responsibility | Example files | Allowed to depend on |
|---|---|---|---|
| Entry (controller/worker) | nhận HTTP/cron, điều phối | dose.controller.ts, reminder.worker.ts | service, db |
| Service (use case) | logic nghiệp vụ | dose-generator.service.ts, reminder.service.ts, adherence.service.ts | entity, db, providers |
| Entity (model) | kiểu dữ liệu domain | schedule.entity.ts, dose-event.entity.ts | (không phụ thuộc gì) |
| Infra (common) | db in-memory, provider ngoài | common/db.ts, common/providers.ts | entity |
| Guard | phân quyền | identity/caregiver.guard.ts | db |

Evidence:
- File path/Symbol: DoseGeneratorService import Schedule/DoseEvent/db; ReminderService import db + pushProvider; controller import service + db
- Mức chắc chắn: chắc chắn

## Dependency direction
`worker → service → {entity, db, providers}` và `controller → service + db`. Entity là lá (không import gì). Chiều phụ thuộc hướng vào trong (entry → service → infra), khá sạch cho một slice.

## Architecture violations (observed)
1. **Service chạm thẳng db toàn cục** (không qua repository). `DoseGeneratorService` vừa build event vừa `db.doseEvents.push`; `ReminderService` filter + push trực tiếp; `AdherenceService` filter trực tiếp. => trộn logic domain với persistence.
   - Evidence: dose-generator.service.ts:39 `db.doseEvents.push(...events)`; reminder.service.ts:11 `db.doseEvents.filter`; adherence.service.ts:9 `db.doseEvents.filter`. Mức: chắc chắn.
2. **Controller chạm thẳng db** — `confirmDose` tự `db.doseEvents.find` + mutate `dose.status` thay vì qua service.
   - Evidence: dose.controller.ts:11,16-17. Mức: chắc chắn.
   - Hệ quả: check permission (nếu có) sẽ nằm rải rác ở controller, dễ sót — đúng là chỗ BUG-5 IDOR xảy ra.

## Ghi chú
Vì db là in-memory global mutable, mọi module chia sẻ cùng một state — không có ranh giới transaction/isolation. Chấp nhận được cho slice demo, nhưng là nợ kiến trúc lớn khi lên Postgres (đẩy risk xuống 18).
