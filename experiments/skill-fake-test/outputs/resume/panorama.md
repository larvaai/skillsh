```
═══ ĐANG Ở ĐÂU — mediremind ═══
Bức tranh: Nhắc uống thuốc + đo tuân thủ cho người mạn tính/người già (patient xác nhận liều một chạm) và caregiver theo dõi từ xa (chỉ-xem); thành công đo bằng SM-1 (on-time dose rate +≥15 điểm % sau 30 ngày) và SM-2 (≥60% caregiver-link kích hoạt).
Con trỏ: gd11_delivery — Delivery Standards vừa xong (T-11 done); nhóm pg-build (T-11a Scheduling ∥ T-11b Reminders) READY, chạy /fanout; GĐ12 UAT còn todo. 2 open-Q chưa đóng (OQ-A, OQ-B).
Đã chốt gần nhất: T-11 · Delivery Standards + DoD + PR Checklist (codebase/delivery-standards.md) — trước đó T-08 freeze Module Map + Contracts (docs/contracts/module-contract-v1.md) mở cổng chạy song song.
Sẵn sàng chạy: T-11a · Sinh Scheduling module theo contract (owner: delivery) · T-11b · Sinh Reminders module theo contract (owner: delivery) — cả hai trong nhóm pg-build.
Chạy song song được: pg-build (T-11a ∥ T-11b) — MỞ: cả hai depends_on T-08 (contract freeze GĐ10) + T-11 (Delivery Standards) đã done; mỗi agent bám cùng Module Contract.
Còn treo: OQ-A (managed job-queue vs tự cron cho Reminder Worker — liên quan src/legacy/old_reminder_cron.ts) · OQ-B (retention dữ liệu liều/thuốc cho NFR-4) — chưa artifact nào đóng, phải đóng bằng ADR trước cổng GĐ13.
→ Tiến cử: /fanout   (bung pg-build: T-11a ∥ T-11b, mỗi agent bám Module Contract v1)
════════════════
```

## Ghi chú tiến cử (đọc thêm)

- Sau khi `/fanout` sinh xong T-11a + T-11b: mỗi task cần `/checkpoint` cấp phiếu PASS rồi `/progress` lật `done`; khi cả hai done, T-12 (UAT) hết bị chặn.
- OQ-A và OQ-B **chưa** đóng và **không** chặn nhóm pg-build, nhưng phải đóng bằng ADR **trước cổng GĐ13 (ship)**. Nhắc để không quên khi tới cổng go-live.
- Con trỏ đang ở gd11_delivery — **không** phải cổng chờ ký GO/NO-GO, nên tiến cử đi tiếp bình thường (không dừng chờ ký).
