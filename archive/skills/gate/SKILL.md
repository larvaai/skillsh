---
name: gate
description: 'Cổng chất lượng cuối của bộ project-folder — GĐ12–13: Verification (test theo AC, thứ tự edge → error → permission) rồi ĐỐI CHIẾU ƯNG Ý: so sản phẩm với từng kỳ vọng K1..Kn và phạm vi PRD, ra khuyến nghị ship hay vòng lại. Chưa ưng không phải thất bại — là quy trình bắt được lệch trước khi ship. Điểm chốt 4/4. Dùng khi "nghiệm thu", "UAT", "verify trước khi ship", "ưng ý chưa", "so với kỳ vọng ban đầu", "go no go", "code xong rồi, ship được chưa".'
---

# Gate — GĐ12–13: nghiệm thu → đối chiếu ƯNG Ý → runbook

`gate` đứng giữa "code xong" và "dùng thật". Nó trả lời đúng câu hỏi mà cả quy trình tồn tại để trả lời: **sản phẩm có khớp kỳ vọng ban đầu không?** Vào bằng code + AC trên board + K-list trong `problem/00`, ra bằng bằng chứng nghiệm thu và một bản đối chiếu từng-K-một.

Phân vai: `run` check DoD từng task — `gate` nghiệm tổng thể, tìm cái từng-task-pass-nhưng-ghép-lại-gãy. Khung nội dung: `quy-trinh-idea-to-operate.md` mục GĐ12–13.

## Luật cứng

- **Bước 0 resume:** constitution → board + journal + rủi ro `mo` trong `risks.md` → `docs/30-roadmap.md` (AC), `docs/13-prd.md` (phạm vi + map phần→K), `problem/00` (K-list). Còn task GĐ11 dở → nói rõ, nghiệm phần đã xong hay đợi là lựa chọn ghi 1 dòng rồi làm. Rủi ro `mo` dính phạm vi ship → phải hiện trong bản đối chiếu, không im; điều chưa chắc mới lộ khi nghiệm → thêm dòng `risks.md`.
- **Nghiệm theo AC, đúng thứ tự nhà: edge → error → permission.** Mỗi phát hiện đủ: tái hiện thế nào · kỳ vọng gì · thực tế gì · mức Critical/Medium/Low. Không phát hiện nào thiếu bằng chứng.
- **Đối chiếu hai chiều:** (1) ngược PRD — cái đã hứa trong phạm vi mà vắng mặt → gap, kể cả khi mọi test pass; (2) ngược K-list — từng K một, Son có TỰ THẤY bằng mắt như K mô tả không, không tính "về mặt kỹ thuật là có".
- **Fix nhỏ → task mới cho `run`,** không tiện tay sửa trong lúc nghiệm — trộn vai là mất dấu.
- **Chưa ưng = vòng lại, không phải thất bại.** Critical mở hoặc K không đạt → khuyến nghị vòng lại (về điểm chốt nào, sửa gì). Son vẫn có thể ship kèm lệch — khi đó `decisions.md` ghi "ship, chấp nhận lệch X". `gate` không bao giờ tự ship.
- **Runbook viết cho Son-3-tháng-sau:** chạy sao, biết nó sống bằng gì, hỏng thường gặp xử sao, rollback; kèm mục **Hiện trạng triển khai** (đang chạy ở đâu · bản nào · từ ngày nào) — cập nhật mỗi lần ship.

## Các bước

1. **GĐ12 — Verification** → `docs/40-verification.md`: bảng Story × AC × kết quả, phát hiện xếp Critical/Medium/Low kèm bằng chứng, mục "đã hứa mà thiếu".
2. **GĐ13 — Đối chiếu ưng ý** → `docs/41-ung-y.md`: bảng K1..Kn — mỗi K: `đạt / lệch-chấp-nhận-được / chưa đạt` + nhìn thấy ở đâu; tổng hợp gap từ GĐ12; khuyến nghị: ship, hay vòng lại về đâu.
3. **Runbook** → `docs/42-runbook.md` + hiện trạng triển khai.
4. **ĐIỂM CHỐT 4/4** — trình bảng đối chiếu. Son nói **ưng** → ship: `decisions.md` 1 dòng, T06 `done`, T07 `ready`, bức tranh v4 ("đã thành sự thật cái gì"), bàn giao `pulse`. Son **chưa ưng** → chốt vòng lại: về điểm chốt nào, task nào mở lại, `decisions.md` ghi "vòng lại vì X, học được Y" — rồi chạy tiếp, không đổ lỗi cho vòng trước.

## Artifact của phiên

`docs/40-verification.md`, `docs/41-ung-y.md`, `docs/42-runbook.md`, dòng decisions (ship hoặc vòng lại), board + journal, bức tranh v4 khi ship.
