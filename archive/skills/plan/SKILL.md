---
name: plan
description: 'Biến thiết kế của một project-folder thành kế hoạch thi công — GĐ9–10: Roadmap, backlog Epic→Feature→Story→AC, Module Map, CONTRACT giữa các module, rồi đổ task vào progress/board.md kèm phụ thuộc + nhóm song song + vùng chạm để `run` fan-out được. Dùng khi "lên roadmap", "cắt backlog", "chia task", "task nào song song được", "chốt contract", "xếp thứ tự làm", "thiết kế xong rồi, làm gì trước".'
---

# Plan — GĐ9–10: roadmap, backlog, contract, board DAG

`plan` quyết WHAT FIRST: cắt lời giải thành task có thứ tự, đánh dấu cái nào phụ thuộc cái nào, cái nào chạy song song được — để `run` nhìn board là thi công, kể cả fan-out nhiều agent. Chất lượng board của `plan` quyết định độ an toàn của `run`.

Phân vai: `sketch` đã chốt hình hài — không mở lại kiến trúc. `run` thi công — `plan` không viết code. Bộ cũ có `backlog`/`modules` làm GĐ9–10 trên `state/` — `plan` là bản project-folder, khung nội dung lấy từ `quy-trinh-idea-to-operate.md` mục GĐ9–10.

## Luật cứng

- **Bước 0 resume:** constitution → board + journal → `docs/13-prd.md` + `docs/20..23`. Thiếu GĐ5–7 → dừng, gợi `sketch` (GĐ8 thiếu thì cảnh báo rủi ro, user quyết đi tiếp hay quay lại).
- **Mọi Story truy vết được:** Story → Feature → Epic → FR trong `docs/12` → pain trong `problem/01`, và mỗi Feature trỏ về K nào trong kỳ vọng. Story mồ côi → gắn cờ trong roadmap + 1 dòng `risks.md`, không lặng lẽ giữ.
- **AC kiểm được bằng máy hoặc mắt,** không AC kiểu "hoạt động tốt". Mỗi Story 2–5 AC.
- **Contract trước, song song sau.** Hai task chỉ được cùng nhóm Song song khi giao diện giữa chúng đã thành file trong `docs/contracts/` (API/schema/event — có version + dòng `Trạng thái: draft|locked`). Contract còn `draft` → nhóm đó chưa được fan-out. Đổi contract đã `locked` → dừng, chốt lại với Son + version mới + 1 dòng `decisions.md`.
- **Mỗi task trên board đủ 8 cột,** đặc biệt Vùng chạm (file/folder được sửa) — hai task song song mà vùng chạm giao nhau là board sai, phải cắt lại.
- **Thứ tự không cần duyệt:** đề xuất theo giá-trị-trước-rủi-ro-sớm, ghi 1 dòng `decisions.md` rồi chạy — Son đổi lúc nào cũng được, làm lại rẻ. Điểm dừng duy nhất của `plan` là khoá contract (điểm chốt 3/4), vì agent song song chạy trên contract sai là công cốc.

## Các bước

1. **GĐ9 — Roadmap + Backlog** → `docs/30-roadmap.md`: Epic → Feature → Story → AC, mỗi Feature → K nào; thứ tự đề xuất + vì sao (giá trị, rủi ro, phụ thuộc), phạm vi bản đầu vs sau; ghi thứ tự vào `decisions.md` rồi đi tiếp.
2. **GĐ10 — Module Map + Contracts** → `docs/31-module-map.md` (module nào lo gì, bám ranh giới GĐ6) + `docs/contracts/<ten>.md` cho mọi đường biên giữa 2 module sẽ làm song song.
3. **ĐIỂM CHỐT 3/4** — trình contract của nhóm song song đầu tiên (1 khối: 2 bên nói chuyện qua gì, dữ liệu hình gì, ví dụ 1 request/response). Son gật → đóng dấu `Trạng thái: locked` + 1 dòng `decisions.md`. Đây là chỗ duy nhất `plan` dừng chờ.
4. **Đổ board:** thay các task khung (T05...) bằng task thật — mỗi Story ≥1 task, đủ Phụ thuộc / Song song / Vùng chạm / Artifact. Ví dụ chuẩn: `T12 chốt contract API (done) ← T13 backend (xay-1, codebase/be/) + T14 frontend (xay-1, codebase/fe/)` — T13, T14 `ready` cùng lúc và fan-out được.
5. **Kết phiên:** T04 `done`, task build đầu tiên `ready`, journal, bức tranh v3 (giờ thấy cả kế hoạch + dòng "So kỳ vọng"), bàn giao `run`.

## Artifact của phiên

`docs/30-roadmap.md`, `docs/31-module-map.md`, `docs/contracts/*.md`, `progress/board.md` bản DAG đầy đủ, bức tranh v3, journal.
