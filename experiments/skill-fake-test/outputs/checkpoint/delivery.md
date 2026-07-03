# Phiếu checkpoint — T-11

- Task: Delivery Standards + DoD + PR Checklist
- Giai đoạn: gd11_delivery (Build / Delivery)
- Owner: delivery
- Artifact: codebase/delivery-standards.md
- Chuẩn đối chiếu: constitution/definition-of-done.md (checklist GĐ11 + Luật cổng GĐ11 của MediRemind)
- Kiểm lúc: 2026-07-03T00:00:00Z

## Bước 1 — Artifact tồn tại đúng chỗ
- [x] File tồn tại: `codebase/delivery-standards.md` (khớp `artifact` của T-11 trong progress.json).
- [x] Đúng folder theo folders.md: artifact GĐ11 thuộc `codebase/` — đúng chỗ.

## Checklist (GĐ11 — Build / Delivery)
Từ definition-of-done.md: "Delivery Standards + DoD + PR Checklist; artifact code trỏ đúng path, gắn được về contract và AC; mỗi module build xong có test theo test-pyramid."

- [x] **Có Delivery Standards** — đủ 9 mục chuẩn giao hàng: Repo & branch (§1), Coding standard (§2), CI/CD (§3), Test pyramid (§4), Environments (§5), Secret & data (§6), Migration (§7), Observability (§8), Incident (§9).
- [x] **Có Definition of Done (DoD)** — mục "Definition of Done (DoD)" (7 điều kiện: code đúng module, test xanh, lint/CI xanh, NFR có metric, audit-log caregiver, migration staging, contract không đổi/bump). Kèm cả Definition of Ready (DoR).
- [x] **Có PR Checklist** — mục "PR Checklist" (7 mục: 1 module/review chéo, có test, lint+build xanh, không commit secret, không ghi entity module khác, error code theo contract, audit-log + at-rest cho dữ liệu nhạy cảm).
- [x] **Gắn được về contract** — §2 chốt "Contract (scheduling-v1, adherence-v1) là nguồn sự thật cho API/event; đổi contract phải bump version"; §4 map integration test tới từng contract endpoint + domain event; contracts thật tồn tại trong `docs/contracts/`.
- [x] **Gắn được về AC/NFR** — DoR "AC viết được, map tới NFR liên quan"; §8 buộc metric NFR-1 (reminder-latency ≤60s), NFR-2 (confirm-write p95 ≤300ms), NFR-5 (availability 99.5%); §6/§8/DoD/PR ràng NFR-4 (dữ liệu nhạy cảm).
- [x] **Đặt chuẩn test theo test-pyramid** — §4 định nghĩa 3 tầng: Unit (sinh DoseEvent, chuyển trạng thái, adherence rate), Integration (mỗi contract endpoint + domain event), E2E (smoke slice xác-nhận-liều). Đây là CHUẨN cho các module build; đúng vai delivery "đặt chuẩn, không code hộ".

## Luật cổng GĐ11 riêng của MediRemind (definition-of-done.md)
"Module GĐ11 chỉ done khi code trỏ đúng path repo (pointer.md) + có test theo test-pyramid + không nới NFR-4 (kiểm quyền caregiver + audit-log)."

- [x] **Con trỏ code repo (pointer.md)** — `codebase/pointer.md` tồn tại, trỏ repo thật + ánh xạ module↔bounded context↔nhánh build; §1 Delivery Standards khớp (monorepo modular monolith, 4 module trong `codebase/`).
- [x] **Test theo test-pyramid** — thoả qua §4 (xem trên).
- [x] **Không nới NFR-4** — §6 "mã hoá at-rest; kiểm soát truy cập; audit-log mọi truy cập caregiver"; §8 "audit-log riêng cho truy cập caregiver (NFR-4)"; DoD "Audit-log áp cho mọi path truy cập caregiver"; PR "audit-log + at-rest encryption còn nguyên". NFR-4 được siết chặt, không nới.

## Ghi chú (không phải điều kiện của artifact GĐ11 này — chỉ nêu để không bỏ sót)
- "Mỗi module build xong có test xanh" và "code trỏ đúng path" ở mức KẾT QUẢ BUILD là điều kiện của T-11a (Scheduling) và T-11b (Reminders), không phải của T-11. T-11 là artifact ĐẶT CHUẨN; checklist GĐ11 áp cho T-11 được thoả ở mức chuẩn. Hai task build còn `ready`, sẽ checkpoint riêng.
- OQ-A (managed queue vs cron) và OQ-B (retention NFR-4) còn `open` trong progress.json. Delivery Standards đã xử lý đúng: §6 ghi "OQ-B retention chưa chốt → chưa xoá dữ liệu tự động cho tới khi có quyết định" (không giả vờ đã đóng). Hai OQ này là cổng GĐ13, KHÔNG chặn phiếu GĐ11.

## Verdict: PASS
Lý do: Artifact nằm đúng `codebase/`, có đủ ba khối bắt buộc GĐ11 (Delivery Standards + DoD + PR Checklist), gắn được về contract (scheduling-v1/adherence-v1) và về NFR/AC, đặt chuẩn test theo test-pyramid, và thoả trọn Luật cổng GĐ11 (pointer.md có, test-pyramid có, NFR-4 không nới).
Nếu FAIL, cần bổ sung: — (không có; phiếu PASS)

═══ CHECKPOINT — T-11: PASS ═══
Artifact: codebase/delivery-standards.md
Đạt: 9/9 mục (6 checklist GĐ11 + 3 luật cổng GĐ11)   |   Thiếu: —
→ PASS: chạy /progress để lật done (T-11 đã done) + mở nhánh pg-build (T-11a ∥ T-11b) chạy /fanout
→ FAIL: —
════════════════
