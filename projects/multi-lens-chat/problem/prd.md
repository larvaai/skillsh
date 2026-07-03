# PRD (bản nháp) — multi-lens-chat (GĐ2–4)

Trạng thái: ĐANG CHỐT. Còn 3 open question đòn-bẩy-cao chặn việc qua Domain (GĐ5).

## Ý tưởng lõi (đã rõ)
Một agent chính hội thoại với người dùng. Song song, N trợ lý nền — mỗi trợ lý một "lens" (góc nhìn) — cùng xử lý input rồi trả insight. Agent chính (hoặc giao diện) tổng hợp/hiển thị các insight đó.

## MVP (đề xuất, chờ chốt)
Nhận một input (câu hỏi / đoạn code / mô tả thiết kế) → fan-out tới một bộ lens cố định (kỹ thuật, rủi ro, business, UX) → mỗi lens trả một insight ngắn → hiển thị gộp cho người đọc. Ca dùng đầu: review một đoạn code.

## Success metric (đề xuất, chờ chốt)
Mỗi phiên review lộ ít nhất một insight mà một-lens-đơn (chỉ kỹ thuật) sẽ bỏ sót — đo bằng đối chiếu thủ công vài phiên đầu.

## Scope
Trong: orchestrator, ≥2 lens worker chạy song song, tổng hợp insight, một ca review code.
Ngoài (V1): giao diện đẹp, lưu lịch sử dài hạn, cho user tự định nghĩa lens runtime, đa người dùng.

## Open questions (đang chặn — OQ đòn-bẩy-cao)
- **OQ-4:** Lens cố định (vd 4 lens) hay để user tự định nghĩa lúc chạy?
- **OQ-5:** Insight hiển thị real-time (streaming từng lens về) hay đợi tất cả xong mới show gộp?
- **OQ-6:** Agent chính tự lọc/tổng hợp trước khi trả lời, hay show riêng từng lens để người tự đọc?

Ba câu này quyết hình hài Domain + Architecture (streaming vs batch, orchestrator chủ động vs thụ động), nên phải chốt trước khi qua GĐ5. → chạy `/idea` để chốt.
