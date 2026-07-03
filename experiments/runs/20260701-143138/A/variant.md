# A · Ví dụ mẫu

## editSummary
Sửa ở explain/SKILL.md, ngay sau khối "Tự soi trước khi gửi" trong Bước 2, thêm một mục mới "Ví dụ mẫu — một overview TỐT ở L3 (calibrate theo đây)". Vì sao ở đó: đó là điểm cuối của phần overview, ngay trước khi model đi soạn câu trả lời — chèn ví dụ mẫu ngay sau checklist tự soi giúp model calibrate bằng ví dụ cụ thể chứ không chỉ theo luật trừu tượng (Luật neo + thang zoom). Mục gồm 3 phần: (1) một câu mở SAI ngắn để tương phản (mở bằng thuật ngữ kiến trúc + tên code), (2) một overview TỐT đầy đủ cho L3 đúng thứ tự vấn đề+cho ai → luồng "bạn ở đây" 8 bước → module map, mỗi tên code chỉ gọi sau khi đã neo, (3) một đoạn giải thích vì sao mẫu này đúng L3 và người thấp/cao hơn khác ra sao. Sửa tối thiểu: không đụng luật, bảng mức, hay thang zoom sẵn có.

## changedSections
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

## output (nguyên văn)
Bạn đang ở L3 (flow), nên mình đi kỹ tới bản đồ luồng rồi chạm vào các module. Ba tầng, phóng to dần.

**Nó giải quyết gì, cho ai.** Khi bạn để một AI tự chạy nhiều bước — gọi model, đọc/ghi file, chạy lệnh, nhờ agent con làm hộ — thứ đáng sợ không phải nó làm sai một lần, mà là nó làm sai ở chỗ *bạn không nhìn thấy* và không tua lại được. Đây là bộ khung để chạy loại AI-làm-việc đó một cách *có kỷ luật và tua lại được*, dành cho người dựng hệ agent (dev nền tảng), không phải người dùng cuối.

**Ý tưởng cốt lõi (một câu).** Mọi hành động ra thế giới bên ngoài phải đi qua đúng một cái cửa — không có đường tắt — nên mọi thứ đều log được, chặn được, và tua lại được từ một nguồn sự thật duy nhất.

**Luồng "bạn ở đây" — một task chạy từ input tới output:**
1. Một caller (UI, script, hay smoke test) gọi facade `run/resume` — cửa vào công khai, ổn định duy nhất.
2. Facade chạy một *sơ đồ bước* biên dịch sẵn, dùng chung (đây là "graph"; LangGraph chỉ lo điều phối, `core/` không hề import nó).
3. Trước mỗi lượt nghĩ, chốt **guard** kiểm ngân sách bước — hết bước thì dừng sạch (fail), không treo vô hạn.
4. Ô **agent** gọi model hỏi "làm gì tiếp", rồi ép câu trả lời về đúng *một* hành động JSON (một cổng parse có sửa lỗi; parse hỏng quá ngưỡng mới bỏ cuộc).
5. Nếu hành động đó là gọi tool hoặc gọi model, nó chui qua *cái cửa duy nhất* — code gọi là `execute_tool`: chỗ này phát event, kiểm phạm vi (tool ngoài scope bị chặn), rồi chạy qua một chuỗi middleware. LLM cũng là một "tool" (`llm.chat`) đi qua đây, không có ngoại lệ.
6. Nếu hành động là nhờ agent con làm hộ, nó đi *một cửa khác* — node `delegate` gọi `delegate` bên `delegation/` — cố tình tách riêng, không phải method của kernel, để việc giao-việc không lẫn với việc gọi-tool.
7. Khi model báo "xong", chốt **finish** chặn lại nếu đã đổi code mà chưa validate; đạt thì mới `complete_task` và kết thúc.
8. Mỗi lần chuyển bước, trạng thái ghi xuống SQLite (`var/agent_runs/<run_id>/langgraph.sqlite`) — đó là *nguồn sự thật* để `resume` tua lại đúng chỗ đang dở.

**Module map — mỗi cái là một chỗ trong luồng trên:**
- `core/` — cái cửa duy nhất ở bước 5 (`kernel.execute_tool`, session gọi vào) + bộ khung dùng chung. Điểm cần nắm ở mức bạn: phần *dùng chung, đóng băng* (`AgentKernel`, frozen) tách khỏi phần *trạng thái của một lần chạy* (`KernelSession`) — nên nhiều run không giẫm lên nhau, và mỗi session mang theo `allowed_capabilities` để giới hạn phạm vi.
- `graph/` + `orchestrator/` — bước 1–2: `orchestrator/loop.py` là facade `run/resume`, `graph/runtime.py` biên dịch sơ đồ bước, `graph/nodes.py` là từng ô (guard/agent/tool/delegate/finish/fail). Checkpoint SQLite mở ở `orchestrator/checkpoint.py`.
- `delegation/` — cửa riêng ở bước 6: `manager.py` là chokepoint tuần tự, `policy.py` chặn độ sâu/ngân sách/phạm vi khi giao việc cho agent con.
- `discipline/` — các chốt kỷ luật ở bước 3, 4, 7: budget (đếm bước), json_gate (ép + sửa JSON), finish_gate. Dùng chung, không nhân bản — middleware và graph đều tái dùng.
- `control/` — lớp realtime để người ngồi ngoài *nhìn và can thiệp* lúc đang chạy. Đang làm dở: mới có phần hợp đồng (events/commands/permission) + một EventEmitter, chưa có transport/UI.

**Vì sao đáng (nhắc lại giá trị).** Một cửa cho mọi hành động = mọi thứ audit/chặn/tua được; SQLite là một nguồn sự thật = resume không đoán mò; giao-việc đi cửa riêng = phân quyền agent con không rò rỉ vào lời gọi tool thường. Đó là cái làm một hệ agent tự-chạy *dám tin để cho chạy*.

Bước tiếp theo tùy bạn: muốn mình đi sâu trách nhiệm của một module cụ thể (vd `core/session.py` với chuyện frozen kernel vs per-run state), hay có một chỗ trong 8 bước trên bạn đang thắc mắc? Nếu bạn muốn *theo dấu* một giá trị đi xuyên các bước (vd envelope của tool đi tới đâu, state đổi ở đâu) thì đó là mức L5 — lúc đó dùng skill `trace` sẽ đúng đồ nghề hơn.
