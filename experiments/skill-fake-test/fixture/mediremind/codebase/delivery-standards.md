# MediRemind — Delivery Standards (GĐ11)

> Bám BIBLE §6 (NFR), §7 (kiến trúc modular monolith), §8 (đội 3 dev, mạnh TS).
> Áp cho toàn dự án. Đặt CHUẨN cách giao hàng an toàn, không code hộ.

## 1. Repo & branch
- Monorepo (modular monolith §7): 4 module theo bounded context §5 trong `codebase/`.
- Branch: `main` protected; feature branch `feat/<module>-<slice>`; squash-merge.
- Mỗi PR chỉ đụng 1 module trừ khi đổi contract (cần review chéo owner).

## 2. Coding standard
- TypeScript (§8: đội mạnh TS), style NestJS thu nhỏ như codebase thật (§10).
- Lint + format bắt buộc trong CI; không merge nếu lint fail.
- Contract (scheduling-v1, adherence-v1) là nguồn sự thật cho API/event; đổi contract phải bump version.

## 3. CI/CD
- CI chạy: lint → unit → integration → build. Fail bất kỳ bước → chặn merge.
- CD: deploy staging tự động sau merge `main`; production thủ công (có cổng ship GĐ13).

## 4. Test pyramid
- Unit: logic sinh DoseEvent, chuyển trạng thái, tính adherence rate.
- Integration: mỗi contract endpoint + domain event.
- E2E: slice "Patient xác nhận một liều" (đã chứng minh ở live slice §9) là smoke E2E bắt buộc.

## 5. Environments
- `local` (docker compose) · `staging` · `production`.
- Container theo §7: Web/API · Reminder Worker · Postgres · Redis · Push/SMS provider (ngoài, dùng sandbox ở staging).

## 6. Secret & data
- Secret qua secret manager, KHÔNG commit.
- Dữ liệu thuốc nhạy cảm (NFR-4): mã hoá at-rest; kiểm soát truy cập; audit-log mọi truy cập caregiver.
- OQ-B retention chưa chốt → chưa xoá dữ liệu tự động cho tới khi có quyết định.

## 7. Migration
- Migration versioned, forward-only ưu tiên; mỗi migration phải reversible hoặc ghi rõ không reversible.
- Chạy migration ở staging trước, có smoke check.

## 8. Observability
- Log có request-id; audit-log riêng cho truy cập caregiver (NFR-4).
- Metric NFR: reminder-latency (NFR-1 ≤ 60s), confirm-write p95 (NFR-2 ≤ 300ms), availability (NFR-5 99.5%).

## 9. Incident (khung)
- Sev theo ảnh hưởng liều bị bỏ lỡ; app không dùng cho cấp cứu (§NFR-5) → không life-critical.

---

## Definition of Ready (DoR)
Một slice READY khi:
- [ ] Thuộc đúng 1 module (contract owner rõ).
- [ ] AC viết được, map tới NFR liên quan (nếu có).
- [ ] Contract phụ thuộc đã freeze (scheduling-v1 / adherence-v1).
- [ ] Không phụ thuộc open-question đang treo (OQ-A queue, OQ-B retention).

## Definition of Done (DoD)
Một slice DONE khi:
- [ ] Code trong đúng module, không rò trách nhiệm sang module khác (theo module-map "Does NOT own").
- [ ] Unit + integration test xanh; smoke E2E slice xác-nhận-liều xanh.
- [ ] Lint/format xanh; CI toàn xanh.
- [ ] NFR liên quan có metric/kiểm chứng (VD confirm-write đo p95).
- [ ] Audit-log áp cho mọi path truy cập caregiver.
- [ ] Migration (nếu có) chạy được ở staging.
- [ ] Contract không đổi, hoặc đã bump version + review chéo owner.

## PR Checklist
- [ ] PR chỉ đụng 1 module (hoặc có review chéo nếu đổi contract).
- [ ] Có test cho code mới (unit/integration).
- [ ] Lint + build xanh trong CI.
- [ ] Không commit secret.
- [ ] Không ghi entity của module khác (chiếu module-map "Does NOT own").
- [ ] Error code dùng đúng bảng contract.
- [ ] Nếu chạm dữ liệu nhạy cảm: audit-log + at-rest encryption còn nguyên.
