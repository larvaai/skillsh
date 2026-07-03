# MediRemind — Ship (GĐ13) [CHƯA KÝ — cổng chưa qua]

> Bám BIBLE §6 (NFR), §9 (live slice), §11 (trạng thái). Release: đưa bản đã build lên production AN TOÀN.
> TRẠNG THÁI: cổng GO/NO-GO **CHƯA đủ chữ ký** (planted gap G-2); rollback **CHƯA chạy thử** (planted gap G-4).

## Go/No-Go Checklist

| # | Mục | Trạng thái |
|---|---|---|
| 1 | Smoke E2E slice "Patient xác nhận một liều" (§9) xanh trên staging | ✅ |
| 2 | Metric NFR-1 reminder ≤ 60s kiểm ở staging | ✅ |
| 3 | Metric NFR-2 confirm-write ≤ 300ms p95 kiểm ở staging | ✅ |
| 4 | Audit-log truy cập caregiver bật (NFR-4) | ✅ |
| 5 | Migration chạy sạch ở staging | ✅ |
| 6 | **UAT / Test & Verification Report (GĐ12)** | ❌ CHƯA CÓ (chain Req→Test đứt) |
| 7 | Rollback plan đã chạy thử | ❌ CHƯA (xem dưới) |
| 8 | Open-question đã đóng: OQ-A (queue vs cron), OQ-B (retention) | ❌ CÒN TREO |

### Cổng GO/NO-GO
| Vai | Người | Chữ ký | Ngày |
|---|---|---|---|
| CTO | — | ☐ CHƯA KÝ | — |
| PO  | — | ☐ CHƯA KÝ | — |

> Cổng yêu cầu ĐỦ 2 chữ ký (CTO + PO) mới GO. Hiện **0/2** → **NO-GO**.

## Runbook (deploy production)
1. Freeze `main`, tag release.
2. Chạy migration production (forward-only).
3. Deploy Web/API + Reminder Worker.
4. Smoke: tạo Schedule test → chờ reminder (NFR-1) → confirm liều (NFR-2) → xem adherence.
5. Theo dõi metric NFR-1/NFR-2/availability 30 phút.

## Rollback Plan  [G-4]
- Bước lùi: redeploy tag trước; migration reversible → chạy down-migration; nếu không reversible thì restore snapshot Postgres.
- Reminder Worker: dừng cron, drain Redis queue trước khi lùi.
- **TRẠNG THÁI: CHƯA chạy thử.** Rollback plan này chưa được diễn tập trên staging → rủi ro chưa đo được. Phải chạy thử trước khi GO.

## Rollout Strategy
internal alpha → pilot (nhóm nhỏ patient + caregiver) → beta → gradual (theo % user) → full.
Mỗi nấc theo dõi on-time dose rate (SM-1) và tỉ lệ caregiver-link kích hoạt (SM-2) trước khi mở rộng.

---
**KẾT: NO-GO.** Chặn bởi: (6) thiếu UAT report, (7) rollback chưa chạy thử, cổng 0/2 chữ ký, OQ-A/OQ-B còn treo.
