# TUNE — skill `backlog` (từ chấm 09-backlog · rebuild-hex-agent)

Nguồn: `grades/09-backlog.grade.md` · thước `rubrics/09-backlog.rubric.md` · skill `/.claude/skills/backlog/SKILL.md` · artifact `rebuild-hex-agent/pipeline/09-backlog.md`. Quy trình tune: `/.claude/skills/tune/SKILL.md`.

## §0 Chẩn đoán (≤6 câu)

Chỉ MỘT tiêu chí mất điểm — **tiêu chí 5 (traceability & không bịa, xương sống) = 0**, kéo bản 14/16 rớt gate; 7 tiêu chí còn lại đều 2, tức cấu trúc skill (3 tầng, ba artifact, AC dùng được, đủ-là-đủ, lý do+loại, ranh giới vai, cổng+bàn giao) chạy ĐÚNG.
Hai loại lỗi kéo về 0: (a) **trích code SAI địa chỉ** — `roles/agent.py:53` cho logic `union − forbidden` (logic thật ở `roles/spec.py:54-64`); (b) **con số tự-khai không khớp thân artifact** lặp ở khối cổng + bàn giao ("7 feature/~10 story" trong khi thân có 6 feature/7 story; "15 SECRET_KEYS" vs 14 trong code; "R3: 5 story ⭐" vs 6).
Lỗi (a) phần lớn là **lỗi-của-lần-chạy**: SKILL đã có luật "trích code khớp code thật" (Luật cứng Traceability) — agent chỉ dán nhầm dòng, không phải skill thiếu luật; các citation khác (`policy.py:25-26`, `tree.py:43-51`, `evidence.py:16-23`) đều đúng.
Lỗi (b) là **lỗi-của-SKILL bị lộ ra**: template khối Cổng và Bàn giao (`SKILL.md` mục Cổng + "Bàn giao sang modules") bắt agent GÕ LẠI con số tổng bằng tay ("<k> epic / <f> feature / <s> story") mà KHÔNG có bước tự-đếm-lại đối chiếu thân — đây là bẫy đếm-hai-lần mà mọi lần chạy đều dễ vấp, tune được.
Kết luận: chỉ (b) đáng tune (siết luật self-count/citation-check trong tự-soi + template cổng); (a) là kỷ luật lần-chạy, có thể chạm nhẹ bằng một nhắc "mỗi `path:line` phải mở file xác nhận trước khi dán" nhưng đừng kỳ vọng xoá sạch.

## §1 Fixture đề xuất (cố định cả thí nghiệm)

- **Project**: `hex_agent` (code gốc tại `/Users/uspro/Desktop/namnson/hex_agent`) — cùng codebase artifact đang chấm, để đối chiếu citation thật.
- **Đầu vào cho backlog** (giữ NGUYÊN, mọi variant đọc cùng bộ): Live Slice GĐ8 `rebuild-hex-agent/pipeline/08-skeleton.md` + PRD/Domain GĐ5 `05-idea-domain.md` + Architecture GĐ6 `06-shape.md` + Tech GĐ7 `07-stack.md` + `00-understanding/REBUILD-BRIEF.md` (epic gốc E01–E21, P0–P4).
- **Tham số**: chế độ tự-quyết (đóng vai PO + Tech-lead, không hỏi user) — y hệt lần chạy đã chấm; yêu cầu sinh đủ ba artifact (Roadmap theme×release + Backlog phân rã + Release Plan), R1 phân rã tới Story+AC.
- **Mức người đọc**: leadership-first (CEO/CTO + business + dev), scan 2–3 phút — như hợp đồng.
- Ghi 3 hằng số (project · đầu-vào-set · chế-độ) ra `experiments/runs/<ts>/fixture.txt`; không variant nào đổi.

## §2 Thước

`experiments/hex-rebuild-review/rubrics/09-backlog.rubric.md` (8 tiêu chí 0/1/2, tối đa 16; xương sống = tiêu chí 1, 3, 5). Đối chiếu code tại `/Users/uspro/Desktop/namnson/hex_agent`.
Luật xếp hạng: **loại hết bản rớt gate trước** (bất kỳ tiêu chí 1/3/5 = 0), **rồi mới xếp theo Tổng**; hoà Tổng thì bản diff NHỎ/robust hơn thắng. Chấm mù: người chấm chỉ thấy {project, input-set, chế-độ, output}, không thấy variant theo hướng nào.

## §3 Các hướng thử (mỗi hướng nhắm ĐÚNG MỘT tiêu chí đang/dễ mất điểm)

> Baseline (Bước 1): chạy `backlog` HIỆN TẠI trên fixture → chấm → kỳ vọng tái hiện gate rớt ở tiêu chí 5 (hoặc gần đó). Mọi hướng dưới nhắm **tiêu chí 5** ở các mặt KHÁC nhau (đây là tiêu chí duy nhất fail — nên các hướng chia theo *loại lỗi trong 5*, không trùng nhau). Thêm 1 hướng đối-chứng nhắm tiêu chí 8 vì con số cổng cũng chạm cổng+bàn giao.

### Hướng A — Bước "đếm-lại-tổng từ thân" trước khi viết cổng/bàn giao (nhắm tiêu chí 5, mặt con-số-tự-khai)
**Giả thuyết**: nếu bắt agent ĐẾM lại số epic/feature/story TỪ thân artifact rồi mới điền vào khối Cổng + Bàn giao, con số "7 feature/~10 story" sẽ khớp thân → hết lỗi tự-khen-đếm-không-khớp.
**DIFF** — thêm vào cuối mục "Tự soi trước khi chốt" (`SKILL.md`) một gạch đầu dòng:
```
- **Đếm-lại-từ-thân (chống tự-khai lệch).** Trước khi viết khối Cổng và Bàn giao: ĐẾM số epic/feature/story CÓ-AC trực tiếp trong thân Backlog (không lấy từ trí nhớ), rồi dán ĐÚNG con số đó. Nếu dùng "~" cho số xấp xỉ thì con số nền vẫn phải là số đếm được. Con số ở Cổng/Bàn giao KHÔNG khớp thân = tự-khai lệch → rớt traceability, sửa trước khi chốt.
```
**Rủi ro**: agent đếm cho có rồi vẫn dán số cũ — cần chấm mù kiểm con số thật, không tin lời "đã đếm".

### Hướng B — Bắt xác nhận từng `path:line` trước khi dán (nhắm tiêu chí 5, mặt trích-code-sai)
**Giả thuyết**: nếu mỗi trích code phải "mở file, đọc đúng dòng, dán nguyên câu code" thì citation sai kiểu `agent.py:53` (thật ra `spec.py:54-64`) sẽ bị bắt tại chỗ.
**DIFF** — sửa gạch "Traceability là bắt buộc" trong Luật cứng, thêm câu cuối:
```
Mỗi trích code (`path:line` hoặc mô tả hành vi) phải MỞ đúng file+dòng đó và dán KÈM nguyên câu code minh chứng (vd `return frozenset(union - forbidden)`); không dán được câu code khớp = chưa xác minh → ghi open-Q, KHÔNG đoán địa chỉ.
```
**Rủi ro**: phần lớn là kỷ luật lần-chạy; luật này có thể chỉ giảm tần suất chứ không xoá — và làm artifact dài thêm vì kèm câu code.

### Hướng C — Nhãn nguồn bắt buộc cho MỖI con số/metric (nhắm tiêu chí 5, mặt con-số-không-nguồn)
**Giả thuyết**: nếu MỖI con số định lượng (max_depth=8, 15/14 SECRET_KEYS, N story) phải kèm `[nguồn: file:line hoặc artifact §]`, các số kế thừa-lỗi (15 SECRET_KEYS từ GĐ5) sẽ bị soi và sửa về đúng code.
**DIFF** — thêm vào Luật cứng, ngay dưới gạch Traceability:
```
- **Số phải có nhãn nguồn.** Mọi con số định lượng trong artifact (ngưỡng, đếm khoá/depth/round, số epic/feature/story) kèm nhãn nguồn ngắn — `[code path:line]` hoặc `[artifact GĐx §y]`. Số kế thừa từ GĐ trước phải đối chiếu lại code gốc nếu code là chân lý (vd đếm SECRET_KEYS mở đúng file, không chép số cũ).
```
**Rủi ro**: có thể phình nhãn ở Tasks/AC làm loãng lớp dev; cần giới hạn nhãn cho số load-bearing.

### Hướng D — Bảng "mỗi giả-định-GĐ8 → Story/AC nào" (nhắm tiêu chí 5, mặt mắt-xích-truy-vết)
**Giả thuyết**: rubric 5 mức-2 đòi "từng giả định đã đổi GĐ8 chỉ ra thành story/AC nào"; một bảng ánh xạ hiện tại đang nằm rải trong tự-soi — làm nó thành khối bắt buộc sẽ khoá mắt xích và lộ luôn citation lệch khi map.
**DIFF** — thêm vào cuối phần "3) Release Plan" (mục Traceability):
```
**Bảng khoá mắt xích (bắt buộc, mỏng):** một bảng | Giả-định-GĐ8 / rule Domain | → Story | → AC | → path:line code |. Mỗi hàng phải điền đủ 4 cột; cột code mở file xác nhận. Ô không nối được = ghi open-Q, không bỏ trống, không bịa.
```
**Rủi ro**: trùng phần một phần với Hướng B (đều chạm citation); nếu chạy cùng lượt phải chấm để tách đóng góp — nhưng D nhắm *mắt xích truy vết đầy đủ*, B nhắm *đúng địa chỉ*, khác mặt.

### Hướng E (đối-chứng) — Cổng/bàn giao TRỎ tổng thay vì gõ lại (nhắm tiêu chí 8, phòng số-lệch nhân đôi)
**Giả thuyết**: nếu template Cổng + Bàn giao KHÔNG bắt gõ lại con số mà chỉ "trỏ về mục Backlog phân rã", nguồn lệch số-nhân-đôi biến mất → cổng sạch mà không đụng thân.
**DIFF** — sửa dòng "Đã chốt : Roadmap (<n> theme × <m> release) · Backlog release gần nhất (<k> epic / <f> feature / <s> story có AC)" trong khối Bàn giao thành:
```
Đã chốt : Roadmap · Backlog release gần nhất (số epic/feature/story: xem mục "2) Backlog phân rã") · Release Plan R1.
```
và tương tự bỏ con số cứng trong khối Cổng, thay bằng "trình đủ ba artifact (chi tiết ở thân)".
**Rủi ro**: mất tính "tự-đứng" của khối cổng cho người chỉ đọc cổng — có thể bị chấm nhẹ ở tiêu chí 1/8 vì kém scan-nhanh; là đối-chứng để so với A (đếm-lại vs bỏ-số).

## §4 Ưu tiên

**Để sau** (không phải "tune ngay", không phải "không đáng").
Lý do: grade cao (14/16, 7/8 tiêu chí đạt trần) và phần lớn cái kéo gate về 0 là **lỗi-của-lần-chạy** (dán nhầm `path:line`) — thứ không tune được bằng sửa prompt. Chỉ có mặt **con-số-tự-khai-lệch** ở khối cổng/bàn giao là lỗi-của-SKILL đáng sửa (template bắt gõ lại số không kèm bước đếm-lại); đáng gộp vào vòng tune chung của cả suite chứ chưa cần vòng riêng khẩn.

## §5 Nhắc luật thí nghiệm

- **Chấm mù**: người chấm chỉ thấy {project, input-set, chế-độ, output.txt}, không thấy variant thuộc hướng nào (đặt tên A/B/C/D/E ngẫu nhiên khi chấm).
- **Baseline trước**: chạy `backlog` hiện tại trên fixture, chấm bằng rubric — phải tái hiện gate rớt ở tiêu chí 5 rồi mới so; không có baseline thì "13/16 qua-gate" không biết là tiến hay lùi.
- **Một biến duy nhất**: mọi variant cùng fixture (§1), chỉ khác đúng đoạn DIFF của nó; không sửa thêm chỗ khác.
- **Confirm bản thắng bằng agent MỚI + fixture thứ hai**: chạy `proposed-SKILL.md` bản thắng bằng agent mới trên (a) fixture gốc và (b) một project thứ hai (vd một live-slice khác không phải hex_agent). Chỉ hơn baseline ở CẢ HAI mới đáng merge; chỉ hơn ở fixture gốc = mùi over-fit vào đúng con số hex_agent.
- **Không đụng bản thật khi thử**: variant nằm trong `experiments/runs/<ts>/<variant>/`, `backlog/SKILL.md` thật chỉ đổi sau khi có bản thắng qua confirm và Son chốt.
