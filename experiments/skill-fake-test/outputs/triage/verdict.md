═══ TRIAGE: old_reminder_cron.ts — mediremind (level: không xác minh được, không có user-state.json) ═══

Tầng: Infrastructure (job/scheduler cũ) — không có mùi sai tầng nội tại; vấn đề là file ĐÃ CHẾT, không phải sai vị trí.
Trách nhiệm: Chạy một cron `setInterval` 60s bản đầu để "quét toàn bộ, gửi hết" reminder — bản tiền-thân của reminder pipeline hiện tại, viết trước khi tách `ReminderService`.
Contract: export `startOldCron(sendFn: (uid, msg) => void)` + `stopOldCron()`; state qua biến module-global `timer`. Không input/output nghiệp vụ thật (thân hàm chỉ `console.log('[old cron] tick')`), `sendFn` nhận vào nhưng KHÔNG BAO GIỜ được gọi.
Caller: **KHÔNG tìm thấy** — grep `startOldCron`, `stopOldCron`, `old_reminder_cron`, `legacy`, `OldCron` trên toàn `mediremind/` chỉ hit đúng dòng định nghĩa trong chính file này; 0 import, 0 lời gọi ở bất cứ nơi nào khác. Độ tin cậy: **chắc chắn** (codebase nhỏ 12 file, không có DI container/route-string/dynamic-import nào tham chiếu tới nó; atlas `00_index.md` xác nhận "legacy" là module riêng và chỉ có 1 `console.log` duy nhất — nằm ở đây).
Callee: Chỉ gọi runtime API `setInterval`/`clearInterval`/`console.log`. Không gọi domain, DB, hay service nào. Không dependency sai tầng.
State: Chỉ đổi biến module-global `timer` (đặt trong start, clear trong stop). Không đụng bất kỳ field domain/DB/entity nào. Không load-bearing với phần còn lại của hệ.
Side effect: Đăng ký một timer nền (`setInterval`) + `console.log`. Nếu vô tình được gọi thì tạo timer rác vô hại (không gửi gì thật, `sendFn` chết). Không I/O, DB, network.
Core/Detail: Cả file là **chi tiết đã bị thay thế** — chức năng thật (sinh liều + bắn reminder tới hạn) đã chuyển sang `reminders/reminder.worker.ts` (`nightlyGenerate` + `everyMinute` gọi `DoseGeneratorService`/`ReminderService`). File này không nắm responsibility hay contract nào còn sống.
Rủi ro khi tác động: **thấp** — xoá file không phá API công khai (không ai import), không phá DB (không đụng schema), không phá UI, không đụng live-slice (không map được slice active, nhưng file không xuất hiện trong bất kỳ luồng nào của atlas flow_traces). Rủi ro duy nhất: mất phần "phòng khi cần" mà comment nhắc tới — song đó chỉ là ~15 dòng logic thô đã lỗi thời (không cửa sổ, không dedupe, không timezone), git history giữ lại được nếu repo có VCS.
Scope-check: **không xác minh được** `do_not_touch`/slice active — không có `agent-state.json` hay `pipeline-state.json` cạnh fixture (fixture brownfield chưa từng chạy `frame`/`partner`). Theo fail-mềm của skill: coi như không ràng buộc đóng băng, và vì bằng chứng caller (grep) **mạnh** nên KHÔNG hạ verdict xuống `cần đọc thêm`.

QUYẾT ĐỊNH: **xoá** (có kiểm soát) — file dead thật sự: 0 caller chắc chắn, chức năng đã được `reminder.worker.ts` thay hoàn toàn, không nằm trong API/DB/domain-core/live-slice; comment "giữ phòng khi cần" là lý do tâm lý, không phải ràng buộc kỹ thuật.
Bước kế: **→ /frame** (khối bàn giao bên dưới). Theo luật skill, `xoá` dead code LUÔN là BÀN GIAO — không tự xoá inline. Nếu muốn giữ bài học thay vì xoá cứng, phương án B là `archive` (di dời + để lại 1 dòng REWRITE_NOTES: "cron bản đầu thiếu window/dedupe/timezone → đã thay bằng reminder.worker").

═══ BÀN GIAO → frame: old_reminder_cron.ts ═══
Verdict: xoá (dead code)                Tầng: Infrastructure (scheduler cũ)
Lý do: Chức năng đã bị `reminders/reminder.worker.ts` thay hoàn toàn; grep 0 caller (chắc chắn) trên toàn mediremind; không thuộc public API / DB schema / domain core / live-slice.
Rủi ro: thấp — không import ở đâu, không đụng state chung; chỉ mất ~15 dòng logic thô lỗi thời (git history giữ được).
Caller/Callee đã map: Caller = KHÔNG tìm thấy (chắc chắn). Callee = chỉ `setInterval`/`clearInterval`/`console.log`, không domain/DB.
KHÔNG đụng: không xác minh được do_not_touch (không có agent-state.json cạnh fixture) — nếu về sau chạy `frame`/`partner` mà file lọt vào do_not_touch thì hạ xuống `giữ`.
→ Bạn chạy: /frame "xoá file legacy/old_reminder_cron.ts + xác nhận không còn tham chiếu, chạy typecheck". (frame giữ kỷ luật hỏi-trước-code, mình không code thay.)
════════════════
