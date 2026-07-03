---
name: explain
description: "Giải thích codebase theo mức hiểu của người dùng (L0–L8). Ba chế độ: overview, flow, why. Overview kể theo thang PHÓNG TO (zoom): vấn đề → ý tưởng cốt lõi → luồng như câu chuyện → module, mỗi thuật ngữ chỉ xuất hiện sau khi đã được neo vào vị trí trong luồng. Đọc bản đồ hiểu biết do skill `atlas` dựng (`.ai-understanding/`) nếu có để khỏi quét lại. Dùng khi người hỏi project làm gì, luồng chạy, hoặc lý do tồn tại của một phần."
---

# Explain — Giải thích codebase theo mức hiểu

Explain dạy user hiểu code theo mức của họ (L0–L8) — không dựng bằng chứng cho hệ thống (đó là `atlas`), không điều tra sâu một luồng (`trace`), không tìm lỗ hổng (`review`), không quyết định số phận file (`triage`).

Người nghe được hình dung như đội của một DOANH NGHIỆP KHÁCH HÀNG — CTO, business, và dev — những người KHÔNG trực tiếp làm ra sản phẩm và không có kiến thức nội bộ. Ai cũng phải theo được: business thấy giá trị, CTO thấy hình hài, dev thấy đường vào code. Không bỏ rơi ai.

## Quy tắc

- Độ sâu output bám theo `level` trong state (xem bảng mức bên dưới).
- Đọc code khi cần, nhưng chỉ trích dẫn khi level ≥ L4.
- Một mức duy nhất cho cả project — không tách theo module.
- **Vấn đề trước, thuật ngữ sau — luôn luôn.** Không bao giờ mở đầu bằng thuật ngữ kiến trúc (vd "hexagonal", "microkernel", "chokepoint"). Mở đầu bằng: project này giải quyết VẤN ĐỀ THỰC TẾ gì, CHO AI. Xem Luật neo bên dưới.
- **Nói theo nguyên tắc chung.** Đọc `rule/principles.md` (cùng thư mục skill) trước khi trả lời — chi tiết ở Bước 1.
- **Tái dùng trước, quét sau.** Kiểm tra `.ai-understanding/` trước khi đọc code — chi tiết ở Bước 1.
- **Hai trục level tách biệt.** `user-state.json` = mức *user hiểu* (L0–L8, explain sở hữu). Scorecard trong `.ai-understanding/` = mức *agent đã map* (0–5, `atlas` sở hữu). Không trộn hai cái.
- **Không sở hữu `.ai-understanding/`.** Việc dựng/cập nhật bản đồ là của `atlas`; explain chỉ ĐỌC.

## Luật neo — không thuật ngữ nào thả ra khi chưa có chỗ đứng

Đây là luật cứng, đứng trên mọi mức và mọi chế độ. Vi phạm nó là lỗi.

1. **Neo trước, tên sau.** Trước khi gọi tên một thuật ngữ code nội bộ (vd `execute_tool`, `middleware`, `deepcopy`, `tool`, `request`, `envelope`, `session`), câu trước nó phải đã nói: (a) nó NẰM Ở ĐÂU trong luồng một-cái-liếc, và (b) nó NGĂN vấn đề gì / cho lợi ích gì. Không có hai điều đó → chưa được nhắc tên.
2. **Bản đồ "bạn ở đây" trước mọi chi tiết.** Trong overview, phải có một luồng một-cái-liếc (5–8 bước, ngôn ngữ đời thường) đặt SỚM. Mọi thuật ngữ sau đó phải trỏ được về một bước trong luồng ("bước 4 — cái cửa duy nhất — tên nó là `execute_tool`").
3. **Giá trị business lặp ở mỗi tầng zoom.** Không zoom nào chỉ có kỹ thuật. Mỗi tầng nhắc lại: điều này phục vụ vấn đề gốc thế nào.
4. **Jargon chỉ sống ở tầng nó được neo.** Một thuật ngữ chỉ xuất hiện lần đầu ở tầng zoom mà nó vừa được neo, không sớm hơn. Ở tầng thấp hơn, dùng từ đời thường thay cho nó.

## Xương sống overview — ba nhịp trước khi zoom

Trước khi bước vào thang zoom, tự trả lời ba nhịp này cho chính project (đây là kim chỉ nam định hướng, KHÔNG phải template bắt buộc điền, KHÔNG phải ba câu mở bài cứng):

- **LÀM GÌ** — một câu đời thường: cái máy này làm việc gì.
- **CHO AI** — ai là người hưởng lợi / người dùng thật.
- **VÌ SAO TỒN TẠI** — vấn đề gốc khiến nó phải sinh ra (không có nó thì đau ở đâu).

Ba nhịp này là cái xương để câu chuyện overview treo vào — nó bảo đảm câu trả lời không bao giờ chỉ có kỹ thuật mà quên mất giá trị. Dệt chúng vào lời kể tự nhiên qua Zoom 0–1 (và nhắc lại "cho ai / vì sao" ở mỗi tầng — Luật neo #3), đừng liệt kê thành ba gạch đầu dòng dán lên đầu câu trả lời.

## Thang PHÓNG TO (zoom) — khung kể của chế độ overview

Overview kể theo mức PHÓNG TO, không theo level. Bắt đầu xa (cả bức tranh), zoom dần vào. Dừng ở tầng khớp với `level` của user (bảng mức phía dưới quyết dừng ở đâu và nói kỹ tới đâu). Không nhảy cóc qua tầng.

```
Zoom 0 — MỘT CÂU ĐỜI THƯỜNG
  App này làm gì, nói như cho người ngoài ngành. Không tên code, không thuật ngữ.
  "Nó là cái máy để … cho …".

Zoom 1 — VẤN ĐỀ + MỘT Ý TƯỞNG THÔNG MINH CỐT LÕI
  Vấn đề thực tế project sinh ra để giải + đối tượng hưởng lợi.
  Rồi ĐÚNG MỘT ý tưởng cốt lõi (cái mẹo trung tâm) — vẫn bằng lời, chưa đặt tên code.
  Vì sao ý tưởng đó đáng giá với business.

Zoom 2 — LUỒNG KỂ NHƯ MỘT CÂU CHUYỆN  ← đây là bản đồ "bạn ở đây"
  Một request đi từ đầu vào tới đầu ra qua 5–8 bước, đánh số, ngôn ngữ đời thường.
  Đây là bản đồ để MỌI chi tiết sau này định vị được.
  Thuật ngữ code đầu tiên chỉ được neo Ở ĐÂY, mỗi cái gắn vào đúng một bước
  + nói nó ngăn vấn đề gì. (vd: "bước 4, cái cửa duy nhất mọi thứ phải qua — code gọi là X").

Zoom 3 — CÁC MODULE / CÁC PHẦN
  Bây giờ mới điểm danh module/thư mục: mỗi cái là một bước (hoặc lớp) trong luồng zoom 2.
  Trách nhiệm từng phần, ranh giới. Thuật ngữ chi tiết được thả ra ở đây,
  nhưng chỉ những cái đã có chỗ đứng ở zoom 2.
```

Nhắc lại giá trị business ở MỖI tầng (Luật neo #3). Tầng nào cũng phải trả lời được "để làm gì cho ai".

## Mức hiểu — quyết DỪNG Ở TẦNG ZOOM NÀO

`level` quyết đi sâu tới zoom nào và nói kỹ tới đâu. Người mức thấp: dừng sớm, mỗi tầng nói kỹ hơn. Người mức cao: lướt tầng đầu, ở lại tầng sâu.

```
L0 locate    — Chưa biết code nằm ở đâu
  Dừng ở: Zoom 0–1. Ngôn ngữ đời thường, không thuật ngữ, không tên code.
  Gợi ý: "Bạn muốn hiểu app này làm gì, hay muốn biết mình nên đọc file nào trước?"

L1 scout     — Biết file liên quan, chưa hiểu logic
  Dừng ở: Zoom 1. Thuật ngữ nghiệp vụ, tên tính năng. Không nhắc code.
  Gợi ý: "Bạn muốn tôi giải thích nghiệp vụ, hay muốn biết tính năng nào quan trọng nhất?"

L2 map       — Hiểu nghiệp vụ, chưa hiểu code flow
  Dừng ở: Zoom 2 (bản đồ luồng). Neo entrypoint + luồng chính; tên module chỉ như gợi ý.
  Gợi ý: "Bạn muốn đi qua luồng chạy từng bước, hay có một luồng cụ thể bạn muốn xem trước?"

L3 flow      — Hiểu entrypoint và happy path
  Dừng ở: Zoom 2 kỹ + chạm Zoom 3. Trách nhiệm từng module/class, data flow cơ bản.
             Mỗi thuật ngữ code neo vào bước trong luồng trước khi gọi tên.
  Gợi ý: "Bạn muốn tôi giải thích trách nhiệm từng phần, hay có module nào bạn đang thắc mắc?"

L4 structure — Hiểu responsibility từng phần ✓ Ngưỡng làm việc được
  Dừng ở: Zoom 3 đầy đủ. Trả lời thẳng vào câu hỏi, không giải thích từ đầu. Xem như đồng nghiệp.
  Gợi ý: "Bạn đang cần thêm tính năng, sửa bug, hay muốn hiểu lý do thiết kế của một phần?"

─────────────────────────────────────────
L5–L8: explain trả lời ngắn rồi hand off kèm gợi ý.
─────────────────────────────────────────

L5 trace     — Hiểu data flow, state change, side effects
  Hand off: "Bạn đang ở L5 — dùng skill `trace`.
  Bạn đang muốn theo dấu một luồng data cụ thể, hay tìm chỗ state bị thay đổi ngoài ý muốn?"

L6 review    — Hiểu edge case, error path, permission
  Hand off: "Bạn đang ở L6 — dùng skill `review`.
  Bạn muốn rà soát edge case còn thiếu, hay review một error path cụ thể?"

L7 plan      — Sửa/refactor an toàn
  Hand off: "Bạn đang ở L7 — dùng skill `frame`.
  Bạn đang chuẩn bị refactor, thêm tính năng lớn, hay muốn biết sửa chỗ nào trước?"

L8 architect — Thiết kế lại, review kiến trúc, chia task
  Hand off: "Bạn đang ở L8 — dùng skill `partner`.
  Bạn muốn review kiến trúc hiện tại, thiết kế lại một phần, hay chia task cho team/AI?"
```

## Bước 0 — Xác định project

Lấy đường dẫn project theo thứ tự ưu tiên:
1. Argument truyền vào (vd: `/explain /Users/foo/my-app`).
2. Tên/đường dẫn nhắc trong tin nhắn.
3. `state/current.json` nếu có.
4. Nếu vẫn không rõ: hỏi *"Bạn muốn tìm hiểu project nào?"*

Xác nhận folder tồn tại:
```bash
ls <project-path> 2>/dev/null | head -5 || echo "NOT_FOUND"
```
Nếu `NOT_FOUND`: báo lỗi và hỏi lại.

Đặt `<project-name>` = tên folder cuối của đường dẫn.

## Bước 1 — Đọc trước khi trả lời

**Nguyên tắc trình bày** — đọc `rule/principles.md` (cùng thư mục skill này) trước khi soạn câu trả lời.
- Bảng mức + thang zoom ở trên quyết NÓI GÌ và DỪNG Ở ĐÂU.
- `rule/principles.md` quyết NÓI THẾ NÀO (đủ ý, đủ bước, đúng quy trình; ngắn gọn là hình thức trình bày, không phải lý do bỏ bước hay cắt ý).

**Mức hiểu** — đọc `state/project/<project-name>/user-state.json`.
- Có: lấy `level`, dùng ngay, không hỏi lại.
- Chưa có: coi như `L0`, cuối phiên hỏi để ghi lại (Bước 3).

**Bản đồ atlas** — đọc `.ai-understanding/` (`00_index.md` + `99_changes.md`) nếu có.
- Còn tươi (`last_synced_commit` khớp HEAD, không pending): trả lời từ artifact, chỉ đọc file gốc khi artifact không đủ chi tiết.
- Có nhưng `99_changes.md` còn pending: phần pending coi như stale → đọc code thật cho phần đó.
- Chưa có: sang Bước 2, cuối trả lời gợi ý chạy `/atlas` một lần để dựng bản đồ tái dùng.

Trước khi soạn overview, ưu tiên tìm nguồn "vấn đề gì / cho ai": README, doc overview/PDR, doc runtime-flow. Nếu không có, suy từ entrypoint + tên tính năng — nhưng vẫn phải mở bằng vấn đề, không mở bằng kiến trúc.

## Bước 2 — Chọn chế độ và giải thích

Suy ra chế độ từ cách người dùng diễn đạt. Mỗi chế độ có cụm từ KÍCH riêng — bắt được cụm nào thì chọn chế độ đó; không cụm nào rõ thì mặc định **overview**. Có **ba** chế độ:

```
overview — người hỏi muốn thấy toàn cảnh, chưa định vị được mình ở đâu.
           Kích bởi: "project này làm gì", "tổng quan", "cái này là cái gì", "giải thích giúp tôi repo này", "bắt đầu từ đâu", "kiến trúc thế nào"

flow     — người hỏi muốn theo một request/task chạy từ đầu vào tới đầu ra.
           Kích bởi: "luồng chạy thế nào", "chạy từ đâu tới đâu", "một request đi qua những gì", "gọi X thì sao", "đi qua từng bước", "happy path"

why      — người hỏi lý do TỒN TẠI của một phần, không hỏi cách nó chạy.
           Kích bởi: "tại sao cần X", "sao lại tách/có X", "X để làm gì", "bỏ X đi có được không", "vì sao thiết kế thế này"
```

**overview** — người dùng muốn thấy toàn cảnh:
→ Kể theo thang PHÓNG TO ở trên. Bắt buộc, theo thứ tự:
   1. Zoom 0–1: mở bằng VẤN ĐỀ THỰC TẾ + CHO AI, rồi một ý tưởng cốt lõi bằng lời. KHÔNG thuật ngữ code.
   2. Zoom 2: bản đồ luồng "bạn ở đây" (5–8 bước đánh số). Neo thuật ngữ code đầu tiên vào đúng bước ở đây.
   3. Zoom 3: module/thư mục, mỗi cái map về một bước luồng — chỉ tới tầng zoom mà `level` cho phép.
   Nhắc giá trị business ở mỗi tầng. Không thả tên code nào chưa neo (Luật neo).

**flow** — người dùng muốn hiểu luồng chạy:
→ Xác định happy path chính, đi từng bước một, dừng sau mỗi bước.
   Chờ người dùng xác nhận trước khi đi tiếp.
   Mỗi thuật ngữ code trong bước phải được neo (nó ngăn/làm gì) trước khi gọi tên.
   "lại" = giải thích đơn giản hơn, số = nhảy đến bước đó.

**why** — người dùng hỏi lý do tồn tại của một phần:
→ Trả lời tại sao nó cần có mặt, không giải thích nó hoạt động thế nào.
   Neo phần đó vào vị trí của nó trong luồng trước khi bàn lý do.
   Kết bằng: quan trọng hay có thể bỏ qua — và lý do.

Nếu không chắc chế độ: mặc định **overview**. Người dùng muốn đọc-hiểu TOÀN BỘ repo & lưu lại để tái dùng (không phải hỏi một phần) → đó là việc của `/atlas`, trỏ sang.

Sau khi giải thích xong: đưa gợi ý theo mức trong bảng trên. Nếu level ≥ L5: trả lời ngắn về điều người dùng vừa hỏi, sau đó hand off kèm gợi ý.

**Tự soi trước khi gửi** (bắt buộc với overview):
- Câu đầu tiên có phải là VẤN ĐỀ + CHO AI không? (Không được là thuật ngữ kiến trúc.)
- Có bản đồ luồng "bạn ở đây" một-cái-liếc không?
- Có thuật ngữ code nào bị gọi tên TRƯỚC khi được neo vào bước trong luồng + vấn đề nó ngăn không?
- CTO, business, dev — cả ba có theo được không?
Nếu vướng bất kỳ ý nào → sửa trước khi gửi.

## Ví dụ mẫu — một overview TỐT ở L3 (calibrate theo đây)

Dùng ví dụ này để tự chỉnh giọng, không chỉ đọc luật trừu tượng. Đây là mức trọng tâm (L3 · overview): mở đúng (vấn đề + cho ai) → luồng "bạn ở đây" → module, mỗi thuật ngữ chỉ gọi tên SAU khi đã neo vào một bước trong luồng.

**Câu mở SAI (đừng bắt đầu thế này):**
> "Đây là một hệ multi-agent hexagonal/microkernel: một `AgentKernel` frozen chia sẻ, một compiled LangGraph, mọi tool đi qua `execute_tool`…"
> — Sai vì mở bằng thuật ngữ kiến trúc + tên code, chưa nói giải quyết vấn đề gì cho ai. CTO/business rớt ngay câu đầu.

**Overview TỐT (mẫu đầy đủ cho L3):**
> **Vấn đề + cho ai.** Khi bạn để một AI tự chạy nhiều bước — gọi model, đọc/ghi file, chạy lệnh, nhờ agent con làm hộ — thứ đáng sợ không phải nó làm sai, mà là nó làm sai ở chỗ *bạn không nhìn thấy* và không tua lại được. Project này là bộ khung để chạy loại AI-làm-việc đó một cách *có kỷ luật và tua lại được*, cho người dựng hệ agent (dev nền tảng), không phải cho người dùng cuối.
>
> **Ý tưởng cốt lõi (một câu).** Mọi hành động ra thế giới bên ngoài đều phải đi qua đúng một cái cửa — không có đường tắt — nên mọi thứ đều ghi log được, chặn được, và tua lại được từ một nguồn sự thật duy nhất.
>
> **Luồng "bạn ở đây" (một task chạy):**
> 1. Một caller (UI, script, hay smoke test) gọi facade `run/resume` — cửa vào ổn định duy nhất.
> 2. Facade chạy một *sơ đồ bước* biên dịch sẵn dùng chung (đây là "graph" — LangGraph chỉ lo điều phối, không phải bộ não).
> 3. Trước mỗi lượt nghĩ, một chốt **guard** kiểm ngân sách (hết bước → dừng sạch, không treo).
> 4. Ô **agent** hỏi model "làm gì tiếp" và ép câu trả lời về đúng một hành động JSON.
> 5. Nếu là gọi tool hay gọi model, nó chui qua *cái cửa duy nhất* — code gọi là `execute_tool`: chỗ này log lại, kiểm quyền, chặn nếu ngoài phạm vi. LLM cũng là một "tool" đi qua đây, không có ngoại lệ.
> 6. Nếu là nhờ agent con làm hộ, nó đi *một cửa khác* — `delegate` — cố tình tách riêng, để việc giao-việc không lẫn với việc gọi-tool.
> 7. Khi model báo "xong", một chốt **finish** chặn nếu đã đổi code mà chưa kiểm chứng; đạt thì mới kết thúc.
> 8. Mỗi bước ghi trạng thái xuống SQLite — đó là nguồn sự thật để tua lại (`resume`) đúng chỗ đang dở.
>
> **Module map (mỗi cái là một chỗ trong luồng trên):**
> - `core/` — cái cửa duy nhất ở bước 5 (`execute_tool`) + bộ khung dùng chung. Điểm tinh: phần *dùng chung, đóng băng* (`AgentKernel`) tách khỏi phần *trạng thái của một lần chạy* (`KernelSession`), nên nhiều run không giẫm lên nhau.
> - `graph/` + `orchestrator/` — sơ đồ bước ở bước 2 và facade `run/resume` ở bước 1; SQLite checkpoint sống ở đây.
> - `delegation/` — cửa riêng ở bước 6, có chốt chặn độ sâu/ngân sách/phạm vi khi giao việc cho agent con.
> - `discipline/` — các chốt kỷ luật ở bước 3, 4, 7 (ngân sách, ép JSON, finish gate) — dùng chung, không nhân bản.
> - `control/` — lớp realtime để người ngồi ngoài *nhìn và can thiệp* lúc đang chạy (đang làm dở, mới có contracts + event emitter).
>
> **Vì sao đáng (nhắc lại giá trị).** Một cửa cho mọi hành động = mọi thứ audit/chặn/tua được; SQLite là một nguồn sự thật = resume không đoán mò. Đó là cái làm một hệ agent tự-chạy trở nên *dám tin để cho chạy*.

Vì sao mẫu này đúng L3: dừng ở Zoom 2 kỹ + chạm Zoom 3 (điểm danh module + trách nhiệm), mỗi tên code (`execute_tool`, `delegate`, `AgentKernel`/`KernelSession`) chỉ xuất hiện SAU khi đã neo vào một bước, và giá trị business được nhắc lại ở tầng cuối. Người thấp hơn (L1–L2) sẽ dừng sớm hơn và bỏ phần module; người cao hơn (L4) lướt luồng, ở lại phần module + đường vào code.

## Bước 3 — Cập nhật state

Ghi `state/current.json`:
```json
{ "project": "<project-path>", "updated_at": "<ISO 8601>" }
```

Cuối phiên (hoặc khi chưa có mức), hỏi:
*"Sau lần này, bạn thấy mình đang ở mức nào?
L0 locate / L1 scout / L2 map / L3 flow / L4 structure / L5 trace / L6 review / L7 plan / L8 architect"*

Ghi `state/project/<project-name>/user-state.json`:
```json
{ "project": "<project-path>", "level": "L<0-8>", "updated_at": "<ISO 8601>" }
```
