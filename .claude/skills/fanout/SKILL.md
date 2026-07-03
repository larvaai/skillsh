---
name: fanout
description: "Bung nhiều agent chạy các task song song. Đọc progress.json, tìm một parallel_group mà MỌI task đều ready (thường là sau khi contract freeze ở gd10), gói cho mỗi task một ngữ cảnh gọn (constitution liên quan + contract + spec task + đích artifact + ranh giới KHÔNG-build), spawn mỗi task một sub-agent chạy đồng thời, thu artifact + tóm tắt về, rồi gọi checkpoint từng task và progress để đóng. Dùng khi: 'chạy song song', 'fan out', 'backend và frontend cùng lúc', 'bung agent làm mấy task này'. Không tự ghi progress.json (nhờ progress) và không tự cấp phiếu (nhờ checkpoint) — fanout chỉ điều phối chạy đồng thời."
---

# Fanout — Chạy đồng thời các nhánh độc lập sau một contract

`fanout` là lúc đồ thị task cho phép rẽ nhánh: nhiều việc chỉ phụ thuộc CÙNG một đầu vào đã sẵn và không phụ thuộc lẫn nhau, nên chạy được cùng lúc. Ví dụ kinh điển: contract API đã freeze → backend và frontend mỗi bên bám cùng contract mà build độc lập. `fanout` bung mỗi nhánh một agent, chờ tất cả về, rồi đóng từng nhánh qua đúng cổng.

Ranh giới:
- `fanout` điều phối chạy. `progress` chia nhóm (`parallel_group`) và ghi `progress.json`. `checkpoint` cấp phiếu. `fanout` không ghi hai file đó — nó gọi hai skill kia.
- Mỗi sub-agent làm phần code/việc của nó (có thể chính là `delivery`/`frame` cho slice đó); `fanout` không tự viết code, chỉ giao việc và gói ngữ cảnh.

## Quy tắc bắt buộc

- **Chỉ bung khi CẢ nhóm ready.** Mọi task trong `parallel_group` phải `ready` (mọi `depends_on` đã `done`). Còn một task `todo` → chưa bung, tiến cử làm nốt phụ thuộc.
- **Đầu vào chung phải đã chốt.** Nhánh song song điển hình chờ contract; contract phải có phiếu checkpoint `PASS` trước khi fan-out. Không bung quanh một contract chưa freeze — hai agent sẽ build lệch nhau.
- **Gói ngữ cảnh GỌN, không đổ cả repo.** Mỗi agent nhận đúng thứ cần: luật liên quan, contract, spec task của nó, đích artifact, và danh sách KHÔNG-build. Không nhét toàn bộ constitution hay task của nhánh khác.
- **Cô lập đầu ra.** Mỗi agent ghi vào đúng `artifact` path của task mình, không đụng path của nhánh khác — tránh giẫm chân khi chạy đồng thời.
- **Đóng từng nhánh qua đúng cổng.** Agent về → `checkpoint <task>` → nếu PASS thì `progress` advance. Một nhánh FAIL không chặn nhánh khác đóng; nhánh FAIL quay lại sửa rồi checkpoint lại.

## Bước 0 — Nạp ngữ cảnh, chọn nhóm

Đọc `constitution/` + `progress.json`. Tìm `parallel_group` có mọi task `ready`. Không có → in "chưa có nhóm song song sẵn sàng" + tiến cử task tuần tự kế. Nhiều nhóm → hỏi bung nhóm nào.

## Bước 1 — Kiểm điều kiện fan-out

- Mọi task trong nhóm `ready`?
- Task đầu vào chung (contract) đã `done` + có phiếu `PASS`?
Thiếu một điều → dừng, nói rõ thiếu gì.

## Bước 2 — Gói ngữ cảnh mỗi task

Với mỗi task trong nhóm, dựng một prompt gọn:
```
Bạn build: <viec>
Contract (bám đúng, không đổi): <docs/contracts/...>
Luật cần theo: <trích conventions liên quan — vd đặt artifact đúng path, .md/.json>
Đích artifact: <artifact path của task này>
KHÔNG build: <ranh giới — phần của nhánh khác, non-scope>
Xong thì: ghi artifact vào đúng đích, trả về 1 tóm tắt: đã làm gì, gắn về contract/AC nào, còn treo gì.
```

## Bước 3 — Bung agent đồng thời

Spawn mỗi task một sub-agent bằng Agent tool, TẤT CẢ trong một lượt (nhiều tool call cùng một message) để chạy song song thật. `subagent_type` thường là `general-purpose` (hoặc agent code chuyên nếu có). Ghi lại task-id ↔ agent để khớp kết quả.

```
═══ FAN-OUT — <parallel_group> ═══
Đầu vào chung: <contract path> (frozen, PASS)
Agent 1 → <T-id>: <viec>  → <artifact>
Agent 2 → <T-id>: <viec>  → <artifact>
...
(đang chạy đồng thời)
════════════════
```

## Bước 4 — Thu kết quả

Mỗi agent về: xác nhận artifact đã nằm đúng path (`ls`), giữ tóm tắt của nó.

## Bước 5 — Đóng từng nhánh

Với mỗi task: chạy `/checkpoint <task-id>` → PASS thì `/progress` advance (lật done, mở khóa hợp-nhất phía sau — vd task "tích hợp BE+FE" phụ thuộc cả hai). FAIL → giữ mở, nêu cần sửa gì.

```
═══ FAN-OUT XONG — <parallel_group> ═══
<T-id> backend  : PASS → done
<T-id> frontend : PASS → done
Mở khóa: <T-id> tích hợp (phụ thuộc cả hai) → ready
→ Kế: /progress hoặc /resume
════════════════
```

## Ví dụ (multi-lens-chat, sau khi freeze contract orchestrator↔lens)

Nhóm `pg-lens-workers`: mỗi lens (kỹ thuật/rủi ro/business/UX) là một worker độc lập chỉ bám contract "nhận task → trả insight". Freeze contract xong, bung mỗi worker một agent build song song, rồi agent chính (orchestrator) hợp nhất — đúng bài toán fan-out/tổng-hợp mà project này sinh ra để giải.
