---
name: sketch
description: 'Vẽ lời giải cho một project-folder từ mờ đến rõ — GĐ5–8 MỘT MẠCH: Domain Model → Architecture Brief → Tech Decision Matrix → Live Slice chạy được. Slice nhắm thẳng vào rủi ro nặng nhất đang mở trong risks.md để đóng nó bằng bằng chứng — đây là chỗ đo ĐỘ KHẢ THI. Kết bằng điểm chốt 2/4. Dùng khi "chốt giải pháp", "vẽ domain", "bàn kiến trúc", "chọn framework/stack", "làm live slice", "PRD xong rồi, thiết kế thế nào", "ý này khả thi không, chứng minh đi".'
---

# Sketch — GĐ5–8: domain → hình hài → công cụ → bằng chứng khả thi

`sketch` biến PRD thành lời giải có hình: mô hình nghiệp vụ (WORLD MODEL) → hình hài hệ thống (SHAPE) → công cụ (WITH WHAT) → một lát cắt sống chứng minh (PROOF). Đây là mắt xích "ý tưởng → cách triển khai + độ khả thi": ẩn số nặng nhất của ý phải được đóng bằng bằng chứng ở đây, không phải bằng lời hứa.

Chạy **một mạch GĐ5→8**, mỗi GĐ xong ghi artifact + journal ngay; dừng chờ Son đúng một lần — điểm chốt 2/4 sau slice (đoán sai kiến trúc là chỗ đắt nhất để sai).

Phân vai: `meet` đã chốt WHY/WHAT — không hỏi lại, không mở lại scope. `plan` lo thứ tự — `sketch` không cắt task. Khung nội dung + luật "Architecture trước, framework sau" + ADR có phương-án-đã-loại: `quy-trinh-idea-to-operate.md` mục GĐ5–8.

## Luật cứng

- **Bước 0 resume:** constitution → board + journal + rủi ro `mo` trong `risks.md` → `docs/13-prd.md` + `problem/01`. Thiếu PRD → dừng, gợi `meet`, không bịa.
- **Đúng thứ tự 5→6→7→8.** Đang bàn kiến trúc mà buột chọn framework → ghi thành đề mục GĐ7, không chốt non.
- **Domain bám nghiệp vụ:** mỗi khái niệm/rule truy về `problem/01` hoặc FR trong `docs/12`. Không đẻ khái niệm không ai kể.
- **ADR đủ 5 ô** (Quyết định · Bối cảnh · Lựa chọn · Đã loại vì sao · Hệ quả); mỗi ADR chốt xong → 1 dòng `decisions.md` trỏ tới. Không có phương án đã loại → chưa phải quyết định.
- **Slice nhắm vào rủi ro:** chọn lát cắt theo rủi ro `mo` nặng nhất trong `risks.md` (không phải lát dễ nhất). Code thật trong `codebase/` (spike nháp ở `codebase/spikes/`), time-box. Chạy xong → cập nhật dòng rủi ro: `dong-dung` hay `dong-sai` + kết quả. `dong-sai` → quay lại sửa GĐ5–7 trước khi sang `plan` — đó là vòng lại rẻ, đúng mục đích slice.
- **Open question mới lộ → `risks.md` ngay.** Đủ-là-đủ: domain nhỏ/quen → mỗi artifact vài dòng một mục vẫn đạt; không bỏ artifact nào.

## Các bước — một mạch 4 giai đoạn

1. **GĐ5 — Domain Model** → `docs/20-domain-model.md`: khái niệm bằng lời người trong nghề, quan hệ, rule bất biến, sự kiện, ai sở hữu dữ liệu nào.
2. **GĐ6 — Architecture Brief** → `docs/21-architecture-brief.md`: style + ranh giới module bám domain, dữ liệu chảy thế nào, nối ngoài gì, chặn ai bằng gì, ADR 2–5 cái.
3. **GĐ7 — Tech Decision Matrix** → `docs/22-tech-matrix.md`: từng lớp chọn gì / đã loại gì / vì sao, khớp ràng buộc thật của Son (máy, công cụ có sẵn, thứ muốn học).
4. **GĐ8 — Live Slice** → code + `docs/23-live-slice-report.md`: slice chứng minh gì, chạy thế nào, giả định nào đứng/đổ, ảnh hưởng gì tới thiết kế; cập nhật `risks.md`.
5. **ĐIỂM CHỐT 2/4** — trình MỘT khối: hình hài (3 câu) → stack + vì sao → bằng chứng slice (rủi ro nào vừa đóng, đóng đúng hay sai) → dòng "So kỳ vọng". Son ưng → `decisions.md`, T03 `done`, T04 `ready`, bức tranh v2, bàn giao `plan`. Slice đổ giả định → đề xuất vòng lại cụ thể.

## Artifact của phiên

`docs/20..23`, code slice trong `codebase/`, rủi ro đóng/mở cập nhật trong `risks.md`, ADR → `decisions.md`, bức tranh v2, board + journal.
