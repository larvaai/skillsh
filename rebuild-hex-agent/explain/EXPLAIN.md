# EXPLAIN — HexAgent (clean rebuild) · chế độ **overview** · mức **L3 (flow)**

> Skill `explain` · chế độ **overview**, kể theo thang **PHÓNG TO** (zoom): vấn đề → ý tưởng cốt lõi → luồng như một câu chuyện → module. Mỗi thuật ngữ code chỉ xuất hiện SAU khi đã được neo vào một bước trong luồng. Người nghe: đội của một khách hàng (CTO + business + dev) — không ai bị bỏ rơi.
> Nguồn: `00-understanding/ATLAS.md` (nền hiểu biết, §7 TRACE) + `REBUILD-BRIEF.md` (7 invariant) + evidence A/B/C (anchor `file:line` bản GỐC). Chỉ khẳng định điều evidence chống lưng.
> Mức L3 = dừng ở Zoom 2 kỹ + chạm Zoom 3 (điểm danh module + trách nhiệm), mỗi tên code neo vào một bước trước khi gọi tên.

---

## ── GÓC NHÌN LÃNH ĐẠO (đọc 60 giây — không cần biết code) ──

1. **Nó làm gì.** Bạn giao cho nó **một mục tiêu**, nó **tự lập kế hoạch, chia thành các bước có thứ tự, giao cho các trợ lý con làm**, và **chỉ báo "xong" khi có bằng chứng thật rằng đã xong** — không phải khi nó tự nói xong.
2. **Vì sao đáng.** Loại "AI tự chạy nhiều bước" bình thường có hai bệnh chết người: **báo-xong-khống** và **chạy mãi đốt tiền**. HexAgent chữa cả hai bằng hai chốt đối nhau — một chốt "chỉ xong khi đủ bằng chứng", một chốt "cắt cứng khi hết ngân sách". Và **mọi hành động đều ghi lại được, tua lại được** như một cuốn sổ, nên bạn dám cho nó chạy.
3. **Cho ai.** Cho **người dựng hệ agent** (dev nền tảng), không phải người dùng cuối — họ cần một cái khung *có kỷ luật* để chạy AI-làm-việc mà không mất kiểm soát.

---

## Zoom 0 — Một câu đời thường

HexAgent là **cái máy để bạn giao một việc rồi để một AI tự lo từ đầu tới cuối** — nó tự nghĩ ra các bước, tự phân công, tự kiểm tra, và **chỉ dừng khi việc thật sự xong**, cho người dựng hệ tự-động-hoá.

Chưa có tên code nào ở đây — cứ hình dung một quản đốc biết chia việc và không bao giờ nghiệm thu ẩu.

## Zoom 1 — Vấn đề + một ý tưởng thông minh cốt lõi

**Vấn đề thật.** Khi bạn để một AI tự chạy nhiều bước — gọi model để nghĩ, đọc/ghi file, chạy lệnh, nhờ agent con làm hộ — thứ đáng sợ không phải là *nó làm sai*, mà là:
- nó làm sai **ở chỗ bạn không nhìn thấy** và không tua lại được;
- nó **báo "xong" trong khi chưa xong** (vì chính nó tự chấm điểm mình);
- nó **chạy vòng vòng mãi**, đốt tiền gọi model mà không tới đích.

Người chịu ba nỗi đau này là **dev nền tảng** — người phải bảo hành cái AI đó khi nó chạy trong sản phẩm thật.

**Một ý tưởng cốt lõi (một câu).** *Bắt mọi hành động ra thế giới bên ngoài phải đi qua đúng MỘT cái cửa — không có đường tắt — nên mọi thứ đều ghi log được, chặn được, tua lại được; và tách bạch chuyện "chỉ xong khi có bằng chứng thật" khỏi chuyện "cắt cứng khi hết ngân sách", để hai điều đó cùng đúng một lúc.*

**Vì sao đáng với business.** Một cửa cho mọi hành động = mọi thứ **audit được** (biết chuyện gì đã xảy ra), **chặn được** (dừng hành động nguy hiểm), **tua lại được** (chạy tiếp từ chỗ dở, không làm lại từ đầu). Còn "xong-phải-có-bằng-chứng" chính là thứ khiến bạn **dám tin để cho nó chạy tự động** — đúng cái mà một AI-tự-chạy bình thường không cho bạn.

## Zoom 2 — Luồng kể như một câu chuyện  ← bản đồ "bạn ở đây"

Đây là một task đi từ lúc bạn giao tới lúc máy báo xong. Tám bước, đánh số — mọi thuật ngữ code phía sau sẽ trỏ về đúng một bước ở đây.

1. **Bạn giao một việc.** Một người gọi (UI, script, hay bài test) đưa vào **một mục tiêu** — cửa vào ổn định duy nhất là một hàm `run`. Từ đây một *phiên làm việc* được tạo ra để giữ mọi trạng thái của lần chạy này (không lẫn với lần chạy khác).

2. **AI lập kế hoạch — và phải chứng minh kế hoạch sẽ dừng.** AI đọc mục tiêu rồi đề xuất chia nó thành các bước con. Nhưng trước khi kế hoạch được nhận, có một **chốt cấu trúc** kiểm: mỗi lần chia nhỏ phải làm việc-còn-lại *ngắn đi thật sự* (không chia giả, không đổi-tên-cho-có). Đây là chỗ code gọi là **decompose gate** (`accept_decomposition`) — nó ngăn cây kế hoạch phình vô hạn, bằng một chứng minh toán học đơn giản: mỗi lần chia, "khối việc cần làm" của một nút co ngặt lại.

3. **Sắp thứ tự — không leo sớm.** Trong đám bước con, máy luôn chọn **bước sẵn-sàng-nhất**: bước ngoài-cùng-trái mà *mọi thứ nó phụ thuộc đã xong*. Nhờ vậy một bước cần kết quả của bước khác sẽ không bao giờ chạy trước — "không leo sớm" là miễn phí, không cần luật riêng.

4. **Giao việc cho trợ lý con — qua một cửa RIÊNG.** Khi cần nhờ một agent con làm một bước, việc đó đi qua **một cửa tách bạch** — code gọi là **delegation** (`DelegationManager.delegate`). Cửa này *cố tình khác* cửa gọi-tool ở bước sau, và nó kiểm một luật cứng: **quyền của con phải ⊆ quyền của cha** (con không bao giờ có quyền rộng hơn cha). Nhờ tách riêng, việc "giao-việc" luôn *audit được và không leo thang quyền*, không lẫn vào việc "gọi-công-cụ".

5. **Trợ lý con làm việc — qua CÁI CỬA DUY NHẤT.** Mọi hành động thật ra thế giới (ghi file, đọc file, và cả *gọi model để nghĩ*) đều chui qua đúng **một cửa** — code gọi là **chokepoint `execute_tool`**. Tại đây: ghi lại hành động, kiểm quyền (hành động này có nằm trong phạm vi cho phép không?), rồi mới cho chạy. **LLM cũng chỉ là một "tool" đi qua cửa này**, không có ngoại lệ — đó là mẹo khiến *mọi thứ* đều audit được từ một chỗ.

6. **Mỗi hành động đẻ ra một dòng nhật ký.** Đi qua cửa ở bước 5, mỗi hành động phát ra một **sự kiện** (`tool.requested` / `tool.completed`) được ghi xuống một cuốn sổ (`events.jsonl`). Cuốn sổ này — code gọi là **event log** — là *nguồn sự thật* để sau này xem lại và tua lại. Trước khi sổ này lộ ra ngoài (ra UI), bí mật (API key…) bị **che (redact) ngay tại biên**.

7. **Nghiệm thu — bằng bằng chứng THẬT.** Khi AI báo "xong", một **chốt nghiệm thu** (`judge_acceptance`) chặn lại và kiểm: mỗi tiêu chí "đạt" phải trỏ tới ít nhất **một bằng chứng thật** — là kết quả một hành động có thật (file đã ghi, tool đã chạy), *không* phải bản-kế-hoạch hay bản-tóm-tắt do chính AI viết ra. Chỉ khi **mọi tiêu chí đều có bằng chứng thật** thì mới sang bước 8. Quan trọng: **agent làm việc không được tự ghi điểm "đạt" — chỉ chốt này mới ghi**.

8. **Kết thúc — hoặc bị phanh.** Đủ bằng chứng → trạng thái **FINISHED**, mọi bước ghi xuống một file SQLite làm *chân lý để tua lại* (`resume` đúng chỗ đang dở). Song song, luôn có các **guard** chạy cùng vòng lặp: hết ngân sách (`max_steps`), không tiến triển, hay lặp lại một quyết định N lần → **BLOCKED** — cắt cứng, không treo. Đây là chốt thứ hai, đối lại chốt nghiệm thu ở bước 7.

> **Hai chốt đối nhau chính là điểm thiết kế cốt lõi:** bước 7 giữ cho "chỉ xong khi thật sự xong"; bước 8 (guards) giữ cho "không chạy vô hạn". Cả hai cùng đúng — đó là lý do một AI-tự-chạy trở nên *dám tin để cho chạy*.

## Zoom 3 — Các module (mỗi cái là một chỗ trong luồng trên)

Giờ mới điểm danh các phần — mỗi phần là một khúc của luồng Zoom 2, chia theo **ranh giới nghiệp vụ (bounded context)**, không theo màn hình:

- **Execution Core** (`core/`) — **cái cửa duy nhất ở bước 5** (`execute_tool`) + bộ khung dùng chung. Điểm tinh: phần *dùng chung, đóng băng trước khi chạy* (`AgentKernel` — "nhân đông cứng") tách khỏi phần *trạng thái của một lần chạy* (`KernelSession` — "session sống"), nên nhiều lần chạy **không giẫm lên nhau** (0 rò state). Đây là chỗ enforce luật "quyền con ⊆ cha" khi tạo session con.

- **Orchestration** (`orchestrator/` + `graph/` + `supervisor/` + `delegation/` + `roles/`) — **bộ não điều phối**: cửa vào `run/resume` ở **bước 1**, kế hoạch + **decompose gate** ở **bước 2**, sắp thứ tự `next_node()` ở **bước 3**, **cửa giao-việc RIÊNG** `DelegationManager.delegate` ở **bước 4**, và **chốt nghiệm thu** `judge_acceptance` ở **bước 7**. Lưu ý: LangGraph ở đây chỉ *lo điều phối*, không phải bộ não; SQLite checkpoint (chân lý tua-lại của bước 8) sống ở khúc `orchestrator/`.

- **Discipline** (`discipline/`) — **các chốt kỷ luật dùng chung**: ép câu trả lời model về đúng JSON (`json_gate`), đếm ngân sách và **phanh** ở bước 8 (`budget`), chặn báo-xong-khi-chưa-kiểm (`finish_gate`). Là logic thuần, không đẻ side effect — không nhân bản ở mỗi nơi.

- **Tools & Safety** (`toolbox/` + `safety/` + `middleware/`) — **hàng thật mà bước 5 gọi tới**: đọc/ghi file, chạy lệnh — nhưng nhốt trong một **hộp cát (sandbox jail)**: mọi đường dẫn phải nằm trong `var/workspace/`, và một `PolicyGate` *đóng-mặc-định* (fail-closed) chặn thứ ngoài danh sách.

- **Control Plane / Observability** (`control/` + `observability/`) — **cuốn sổ ở bước 6** và lớp cho người ngoài *nhìn và can thiệp* lúc đang chạy. Đây là nơi **che secret trước khi ra UI** (redact tại biên) và giữ 3 "seam" (khe nối) đóng kín giữa back-end và UI: luồng sự kiện, ảnh-chụp-trạng-thái, và kênh lệnh. Bất biến: **UI không được import `core/`** — UI chỉ đọc, không có logic nghiệp vụ.

- **Knowledge** (`rag/`, tuỳ chọn) — kho tri thức vector (Qdrant), *health-gated* (hỏng thì im lặng bỏ qua, không làm sập luồng chính). Nằm ngoài đường tới FINISHED — có cũng được, không có cũng chạy.

> **Vì sao đáng (nhắc lại giá trị ở tầng module).** Một cửa cho mọi hành động (Execution Core, bước 5) = **audit/chặn/tua được**. Nghiệm-thu-bằng-bằng-chứng (Orchestration, bước 7) + **phanh** (Discipline, bước 8) = **không báo-xong-khống, không chạy-vô-hạn**. Che-secret-tại-biên (Control Plane, bước 6) = **dùng được realtime mà không rò bí mật**. Ba điều đó là cái làm một hệ agent tự-chạy trở nên *dám tin để cho chạy* — đúng vấn đề ở Zoom 1.

---

## Neo về gói rebuild (để đọc tiếp)

- Muốn thấy **7 bất biến** ở dạng luật: `00-understanding/REBUILD-BRIEF.md` §"7 invariant".
- Muốn **trace một task end-to-end với anchor `file:line`**: `00-understanding/ATLAS.md` §7 (đây là bản dài của Zoom 2 ở trên).
- Muốn thấy **các lỗ hổng thiết kế còn hở** (chỗ báo-xong-khống tinh vi, chỗ kẹt-vòng đốt tiền, chỗ rò secret): `review/REVIEW.md` (12 gap, 3 Critical).
- Muốn thấy **slice đầu tiên sẽ code**: `frame/slice-01-taskloop-happy-path.md` (chính là Zoom 2 TRỪ resume + 1 guard).

## Gợi ý bước tiếp (theo mức L3)

Bạn đang ở **L3 (flow)** — hiểu entrypoint và happy path. Bạn muốn tôi giải thích **trách nhiệm từng module kỹ hơn** (đi sâu Zoom 3, lên L4), hay có **một luồng cụ thể** bạn muốn xem từng bước (vd luồng *nghiệm thu* hay luồng *giao-việc*, dùng chế độ `flow`)?

---

## Tự soi trước khi gửi (bắt buộc với overview)

1. **Câu đầu là VẤN ĐỀ + CHO AI, không phải thuật ngữ kiến trúc?** — CÓ: mở bằng "cái máy để giao một việc rồi để AI tự lo", chưa có tên code; "hexagonal/microkernel/chokepoint" không xuất hiện ở Zoom 0–1.
2. **Có bản đồ luồng "bạn ở đây" một-cái-liếc?** — CÓ: Zoom 2, 8 bước đánh số, ngôn ngữ đời thường.
3. **Thuật ngữ code nào bị gọi tên TRƯỚC khi neo?** — KHÔNG: `execute_tool` neo ở bước 5, `delegation` bước 4, `decompose gate` bước 2, `judge_acceptance`/acceptance bước 7, `event log` bước 6, `AgentKernel/KernelSession` chỉ tới Zoom 3. Mỗi cái đã nói *ở đâu trong luồng* + *ngăn vấn đề gì* trước khi gọi tên.
4. **CTO, business, dev — cả ba theo được?** — CÓ: business đọc Zoom 0–1 + Góc nhìn lãnh đạo; CTO thấy hình hài ở Zoom 2 + module; dev thấy đường vào code ở Zoom 3 + neo file/anchor.
5. **Giá trị business nhắc lại ở mỗi tầng?** — CÓ: Zoom 1 ("dám tin để cho chạy"), Zoom 2 (hộp "hai chốt đối nhau"), Zoom 3 (đoạn "Vì sao đáng").
