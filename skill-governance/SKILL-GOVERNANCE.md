# Quyết định skill từ log harness — giữ / bỏ / sửa

> Viết 2026-07-03, dựa trên log thật trong `namnson/hex_agent/harness/state/telemetry/`. Số liệu là ảnh chụp; chạy lại `skill_decision_report.py` để có số mới.

## Kết luận trước

Log skill của bạn **đã tồn tại và chạy đúng** — không cần dựng lại từ đầu. Hook `track_skill_invocation.py` ghi mọi lần gọi skill vào `invocations.jsonl`, và `analyze_telemetry.py` đã có sẵn 6 lăng kính, trong đó `skill_usage` trả lời thẳng câu "skill nào được gọi, skill nào chưa".

Nhưng **chưa được cắt bất kỳ skill nào lúc này**, và điều đó không phải do bạn thiếu quyết đoán — chính cổng-trung-thực trong code của harness từ chối tín hiệu cắt khi dữ liệu còn mỏng. Hiện có 49 lần gọi trong 4 ngày (26–29/06), 30 phiên. 16/97 skill từng chạy; 81 skill chưa xuất hiện. Với 49 lần gọi mà mẫu số là 97 skill, "chưa dùng" gần như chắc chắn là "chưa có dịp chạy", không phải "vô dụng".

Việc đáng làm không nằm ở cắt skill, mà ở **vá ba lỗ đo** đang chặn chính quyết định đó. Vá xong, để log chạy thật vài tuần, thì danh sách "chưa dùng" mới đủ tin để thành danh sách cắt.

## Log đang đo gì, ở đâu

Ba tầng, đều là file JSONL trong `harness/state/telemetry/`:

`invocations.jsonl` — mỗi lần gọi skill một dòng `{ts, skill, session, via, actor}`. Bắt hai đường: model gọi qua Skill-tool (`PreToolUse:Skill`) và bạn gõ slash `/hs:*` (`UserPromptExpansion`). Dedup theo phút. Đây là nguồn chính cho "được gọi hay không".

`subagent-outcomes.jsonl` — kết cục mỗi subagent `{agent_type, outcome, transcript}`. Đây là tín hiệu hiệu quả gần nhất bạn có.

`sessions.jsonl` — tóm tắt mỗi phiên: `skills[]`, `tools{}`, `files_modified`, `duration_s`. Nguồn phụ cho usage.

Đọc chúng bằng `analyze_telemetry.py --lens all`, hoặc bằng script kèm báo cáo này (áp thẳng quy tắc quyết định).

## Skill nào ĐƯỢC GỌI — phần đáng tin

Đây là phần log nói chắc. Bảy skill bạn thật sự với tới, xếp theo lần gọi:

| skill | plugin | lần gọi | phiên | lần cuối |
|---|---|--:|--:|---|
| discover | hs-research | 9 | 9 | 29/06 |
| plan | hs | 7 | 7 | 27/06 |
| cook | hs | 6 | 5 | 27/06 |
| brainstorm | hs-think | 5 | 4 | 27/06 |
| loop | hs-flow | 4 | 1 | 26/06 |
| fix | hs | 3 | 1 | 26/06 |
| understand | hs | 3 | 3 | 26/06 |

Còn lại (find-skills, bakeoff, explain, ship, skill-creator, afk, setup, critique, frontend-design) mỗi cái 1–2 lần. Đọc theo plugin: lõi `hs` được dùng nhiều nhất (7/14 skill, 23 lần gọi), rồi `hs-research`, `hs-think`, `hs-flow`. Bảy plugin chuyên đề — `hs-ai`, `hs-devops`, `hs-extra`, `hs-integrations`, `hs-mem`, `hs-stack`, `hs-viz` — **không có lần gọi nào**.

Đây đúng là "xương sống SDLC chạy, đồ chuyên biệt chưa đụng" — hợp lý với 4 ngày mang máy lên.

## Skill nào CHƯA DÙNG — và vì sao CHƯA cắt

81 skill có 0 lần gọi trong log. Script gắn nhãn chúng **THEO DÕI, không phải CẮT**. Ba lý do, đều là kỷ luật của chính harness chứ không phải tôi nương tay:

Thứ nhất, mỏng. Cổng-trung-thực chỉ bật tín hiệu cắt khi số-lần-gọi-skill-nhà ≥ số-skill-nhà — tức mỗi skill trung bình có cơ hội chạy ít nhất một lần. Hiện là 49 ≥ 97: chưa đạt. Dưới ngưỡng, "chưa thấy" lẫn với "vô dụng".

Thứ hai, có loại gọi log không thấy. Hook chỉ bắt Skill-tool và slash. Nếu bạn mở `SKILL.md` đọc tay thì không có bản ghi nào — skill đó "chưa dùng" trên giấy nhưng thực ra đã dùng.

Thứ ba — và đây là điểm dễ bị bỏ qua — **phần lớn 81 skill này thuộc plugin opt-in**. Cài mới chỉ bật lõi `hs`; sáu nhóm chuyên đề và các sibling ck-port phải bật tay qua `enabledPlugins`. Một skill trong `hs-ai` báo 0 lần gọi rất có thể vì `hs-ai` chưa bao giờ được bật, chứ không phải bị ngó lơ. Mà log lại **không ghi phiên đó bật plugin nào** — nên ngay cả khi muốn, hiện chưa tách được "tắt nên không có cửa chạy" khỏi "bật mà không ai gọi". Đó tự nó là một lỗ đo.

Vì vậy danh sách 81 skill này là **danh sách theo dõi**: cứ để đó, mỗi kỳ chạy lại report xem cái nào vẫn im.

## Skill nào KÉM HIỆU QUẢ — chưa trả lời được, và phải trung thực về điều đó

Câu này log **chưa đủ sức trả lời**. Lăng kính `subagent_outcomes` cho thấy chỉ 12% số run subagent có kết cục rõ (success/timeout/blocked); 88% là `unknown`. Không phải harness dò sai — hook ghi lúc `SubagentStop` khi transcript chưa kịp flush, nên để `unknown` + đường dẫn transcript rồi phân loại lại lúc đọc; bản ghi cũ mất đường dẫn thì kẹt `unknown`.

Quan trọng hơn, harness **cố tình không đo** ba thứ mà "hiệu quả" cần: chi phí token/tiền mỗi skill, tính đúng và chất lượng ngữ nghĩa mỗi run, và độ sâu review của người. Lăng kính nào cũng in ra mục "NOT measured" để không ai đọc nhầm log một phần thành phủ đủ.

Kết: đừng xếp skill "kém hiệu quả" từ dữ liệu này. Muốn xếp được, phải thêm một tín hiệu chất lượng (mục vá logging bên dưới).

## Quyết định bây giờ

Giữ cả 97 skill. Không cắt cái nào — chưa có bằng chứng nào chịu nổi sức nặng của một quyết định cắt.

Đổi trọng tâm từ "cắt skill" sang "vá đo". Đây mới là nút thắt thật.

Ngưỡng để sau này ĐƯỢC cắt (khi cả bốn cùng đúng): (1) số-lần-gọi-skill-nhà ≥ 97 để cổng `never_used_reliable` bật TRUE; (2) đã qua ≥ 2–3 tuần usage thật, nhiều loại việc, không phải smoke/dev; (3) log có ghi `enabledPlugins` mỗi phiên, để tách "tắt" khỏi "bị lơ" — chỉ cắt skill ở nhóm ĐÃ bật mà vẫn 0 gọi; (4) không có tín hiệu chất lượng dương nào cho skill đó. Đạt đủ, "chưa dùng" mới chuyển thành "ứng viên cắt" — vẫn là đề cử, bạn ký.

## Vá logging — dựng phần còn thiếu

Bốn lỗ, theo thứ tự đáng vá:

**1. Ghi `enabledPlugins` mỗi phiên.** Đây là lỗ chặn nặng nhất, vì thiếu nó thì "chưa dùng" luôn nhập nhằng. `session_init.py` / `emit_session_summary.py` đã ghi `sessions.jsonl` — thêm một trường `enabled_plugins` lấy từ context phiên. Có nó, report tách được "0 gọi vì tắt" khỏi "0 gọi dù bật".

**2. Nâng tỷ lệ outcome rõ.** 88% `unknown` khiến hiệu quả gần như mù. Đảm bảo `track_subagent_outcome.py` luôn lưu đường dẫn transcript, và chạy một lượt phân loại-lại trên bản ghi cũ còn transcript. Mục tiêu kéo definite% từ 12% lên đủ để so sánh giữa các skill.

**3. Vá `skills[]` trong session summary.** 138/174 phiên có `skills[]` rỗng — nguồn usage phụ đang thủng. Kiểm `emit_session_summary.py` xem vì sao không gom được skill của phiên; vá xong có nguồn thứ hai đối chiếu với `invocations.jsonl`.

**4. Nếu muốn quyết theo hiệu quả, thêm một tín hiệu chất lượng.** Telemetry cố tình không đo chất lượng, nên phải chủ động gắn vào — ví dụ cho skill `review`/`critique` ghi một điểm/verdict vào một dòng telemetry gắn `session` + `skill`. Đây là thứ duy nhất trong danh sách này là "dựng mới" thật; ba cái trên là vá cái đã có.

Skill chạy tay không log thì để nguyên — đó là blind spot nội tại harness đã tự khai. Cách gọn nhất: kỷ luật luôn gọi skill qua `/hs:*` hoặc Skill-tool, để mọi lần dùng đều rơi vào log.

## Nhịp kiểm soát skill

Đừng canh log thủ công. Mỗi 1–2 tuần chạy:

```bash
python3 skill-governance/skill_decision_report.py \
  --harness ~/Desktop/namnson/hex_agent --days 30 --format md
```

Đọc ba thứ: skill nào lên top (đầu tư vào đó), skill nào rớt khỏi danh sách theo dõi (đã có người dùng), skill nào vẫn im qua nhiều kỳ (ứng viên cắt tương lai). Khi `never_used_reliable` bật TRUE, report tự đổi nhãn từ THEO DÕI sang CẮT (ứng viên) — đó là lúc bàn chuyện cắt, không phải bây giờ.

Muốn tự động, đặt scheduled task chạy report mỗi sáng thứ Hai và gửi bạn bản md.

## File kèm

`skill_decision_report.py` — bộ sinh báo cáo, read-only, khớp đúng số của `analyze_telemetry.py` (đã đối chiếu: 49 gọi · 16 dùng · 97 skill-nhà · reliable=false · 301 outcome/12% rõ). Áp sẵn cổng-trung-thực và quy tắc giữ/bỏ/sửa. Có thể chép vào `harness/scripts/` để sống cạnh các lăng kính khác.

`SKILL-DECISION.generated.md` — bản báo cáo máy sinh của ảnh chụp hôm nay.
