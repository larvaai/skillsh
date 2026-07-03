---
name: charter
description: "Dựng một project mới để làm việc bài bản: tạo folder projects/<key>/ với 6 thư mục (problem, idea, progress, constitution, docs, codebase), gieo constitution (luật chơi + quy trình 0–14), khởi tạo progress.json rỗng + board.md, ghi memory về project, trỏ current.json. Chạy MỘT LẦN cho mỗi project. Dùng khi: 'bắt đầu project mới', 'dựng workspace cho X', 'khởi tạo dự án', 'tạo folder project', 'charter cho ý tưởng này'. Sau khi dựng xong thì bàn giao sang idea (brainstorm) hoặc resume (xem toàn cảnh). KHÔNG dùng để tiếp tục project đã có — đó là việc của resume."
---

# Charter — Dựng project mới, gieo luật, khởi tạo tiến độ

`charter` là điểm khởi sinh của một project. Nó KHÔNG brainstorm, KHÔNG viết PRD, KHÔNG code — nó chỉ dựng cái khung để mọi skill khác vào làm việc: 6 folder, bản hiến pháp (constitution), và một `progress.json` rỗng biết con trỏ đang ở GĐ0.

Ranh giới với skill khác:
- `charter` = dựng khung một lần. `resume` = mỗi lần quay lại, đọc khung đó rồi nói đang ở đâu.
- `idea` = brainstorm một ý trong `idea/`. `charter` chỉ tạo folder trống cho nó.
- `progress` = sở hữu và cập nhật `progress.json` suốt vòng đời. `charter` chỉ khởi tạo file đó lần đầu, rồi buông.

## Quy tắc bắt buộc

- **Chạy một lần.** Nếu `projects/<key>/` đã tồn tại → KHÔNG tạo đè, KHÔNG xoá. Báo "project đã có" và bảo user chạy `/resume <key>`.
- **Không đụng project khác.** Chỉ tạo đúng folder của key này. Không migrate, không sửa project cũ.
- **Gieo constitution y bản seed.** Copy nguyên 4 file từ `assets/constitution/` sang `projects/<key>/constitution/`. Không tự chế lại luật; muốn sửa luật thì sửa ở seed, không sửa lẻ trong một project.
- **progress.json khởi tạo tối thiểu.** Chỉ một task seed GĐ0 + con trỏ ở `gd0_intake`. Không bịa task tương lai — `progress` sẽ chia task khi tới lúc.
- **Slug ổn định.** `<key>` là một slug kebab-case, dùng thống nhất cho folder + memory + `state/current.json`. Một project một khoá.

## Bước 0 — Lấy tên và một dòng vấn đề

Lấy theo thứ tự ưu tiên:
1. Argument truyền vào (vd `/charter loyalty-app`).
2. Tên/mô tả nhắc trong tin nhắn → derive slug kebab-case ngắn (vd "App tích điểm khách lẻ" → `loyalty-app`).
3. Chưa rõ → hỏi đúng 1 cụm: (a) đặt slug gì, (b) một câu vấn đề định giải, (c) kỳ vọng thô — cuối cùng muốn tận mắt thấy gì thì gọi là "ưng ý". Kỳ vọng ghi NGAY ngày 0, trước khi agent kịp gợi ý gì — mơ hồ cũng ghi.

Xác định `mode`: có repo code sẵn (brownfield) hay ý tưởng mới chưa có code (greenfield). Không có path code → `greenfield`.

## Bước 1 — Kiểm tồn tại

```bash
ls projects/<key> 2>/dev/null | head -1 && echo "ĐÃ CÓ" || echo "CHƯA CÓ"
```
`ĐÃ CÓ` → dừng, tiến cử `/resume <key>`. `CHƯA CÓ` → đi tiếp.

## Bước 2 — Tạo 6 folder

```bash
cd projects/<key> 2>/dev/null || mkdir -p projects/<key>
cd projects/<key>
mkdir -p problem idea docs codebase constitution progress/checkpoints
```

## Bước 3 — Gieo constitution

Copy 4 file seed (không sửa nội dung):
```bash
cp .claude/skills/charter/assets/constitution/*.md projects/<key>/constitution/
```
Bốn file: `process.md` (quy trình 0–14), `conventions.md` (luật bất biến), `folders.md` (bản đồ artifact), `definition-of-done.md` (một bước xong là gì).

## Bước 4 — Khởi tạo progress + board

`projects/<key>/progress/progress.json`:
```json
{
  "schema_version": 1,
  "project": "<key>",
  "mode": "greenfield",
  "con_tro": { "giai_doan": "gd0_intake", "ghi_chu": "vừa dựng project, chưa có ý nào" },
  "tasks": [
    { "id": "T-01", "viec": "Brainstorm ý đầu tiên → plan có input/output", "giai_doan": "gd0_intake",
      "trang_thai": "todo", "depends_on": [], "parallel_group": null, "owner": "idea", "artifact": "idea/<slug>.md" }
  ],
  "updated_at": "<ISO 8601>"
}
```

`projects/<key>/progress/board.md`: một trang người-đọc — tên project, một dòng vấn đề, con trỏ hiện tại, bảng task (rỗng lúc đầu trừ T-01). `board.md` diễn giải; `progress.json` là nguồn.

## Bước 5 — README project

`projects/<key>/README.md`: một trang — project là gì (một câu vấn đề), **Kỳ vọng ban đầu** (thô, vài dòng "thế nào là ưng ý" — mỏ neo để Go/No-Go GĐ13 đối chiếu, xem `definition-of-done.md`), `mode`, ngày dựng, link tới `board.md`, và nhắc "vào bằng `/resume <key>`, brainstorm bằng `/idea`".

## Bước 6 — Ghi memory

Viết một memory `project`: project mới tên gì, giải bài toán gì, ở `projects/<key>/`, đang GĐ0. Thêm một dòng trỏ trong `MEMORY.md`. Không lặp lại thứ đã nằm trong README.

## Bước 7 — Trỏ current.json

`state/current.json`:
```json
{ "project": "<key>", "workspace": "projects/<key>", "updated_at": "<ISO 8601>" }
```

## Bàn giao

```
═══ ĐÃ DỰNG — <key> ═══
6 folder + constitution + progress.json (con trỏ: gd0_intake)
Bài toán: <một câu>
→ Bắt đầu brainstorm ý đầu: /idea
→ Xem toàn cảnh bất cứ lúc nào: /resume <key>
════════════════
```

Không tự chạy tiếp `idea` — chỉ tiến cử, để user quyết.
