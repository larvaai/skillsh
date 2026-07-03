# Rubric — 7 tiêu chí chấm artifact GĐ8 `skeleton` (Live Slice Report)

Mỗi tiêu chí 0/1/2, tổng /14. Chuẩn gốc: `.claude/skills/skeleton/SKILL.md` (hợp đồng GĐ8 — PROOF) + template GĐ8 trong `quy-trinh-idea-to-operate.md`. Rubric chỉ biến hợp đồng đó thành thước đo được — không thêm tiêu chuẩn mới, không mượn tiêu chí của skill khác.

Chuẩn đối chiếu cho mọi claim về code: code gốc tại `/Users/uspro/Desktop/namnson/hex_agent`. Anchor `file:line`, tên hàm, hành vi được nhắc trong report phải kiểm được ở đó (hoặc ở evidence file đã anchor về đó).

## 1. MỞ ĐẦU LÃNH ĐẠO — đọc-được 3 tầng

Hợp đồng: report MỞ bằng khối "Góc nhìn lãnh đạo" — đúng 1–3 thứ (link staging hoặc trạng thái trung thực thay thế · trạng thái checklist validate · giả định đã phải đổi), ngôn ngữ nghiệp vụ, KHÔNG jargon; rồi mới tới chi tiết kỹ thuật. 1 trang, scan 2–3 phút.

- 0 — không có khối lãnh đạo đứng đầu, hoặc report mở bằng chi tiết kỹ thuật (tên framework/log tool/tên hàm/tên file), hoặc khối lãnh đạo dày jargon đến mức CTO/business NGOÀI đọc không hiểu on-track hay không.
- 1 — có khối lãnh đạo đứng đầu nhưng lệch: nhồi quá 3 thứ hoặc thiếu 1 trong 3 thứ bắt buộc; lọt vài thuật ngữ code chưa được giải nghĩa; hoặc dài vượt mức scan ~60–90 giây.
- 2 — mở đúng hợp đồng: 1–3 thứ, ngôn ngữ nghiệp vụ; nêu link staging (hoặc ghi thẳng chưa có), trạng thái checklist, giả định đã đổi; đọc RIÊNG khối này CTO biết "kiến trúc đã chứng minh chưa, có nên đổ người không" mà không cần phần kỹ thuật.

## 2. SLICE ĐÚNG DẠNG — mỏng nhất mà xuyên đủ tầng, có lý do + phương án đã loại

Hợp đồng: chọn ĐÚNG một lát cắt chạm nhiều rủi ro kiến trúc nhất bằng ít code nhất; không bao giờ bỏ tầng nào của `UI→API→Domain→DB→Auth→Log→Test→CI/CD→Staging→Monitor` — chỉ rút gọn độ sâu; ghi lý do chọn + slice đã cân nhắc & loại.

- 0 — không xác định được MỘT slice cụ thể (mô tả chung chung, nhiều feature trộn nhau); hoặc đường đi E2E bỏ hẳn một tầng của lát cắt mà không ghi lý do; hoặc hoàn toàn không có lý do chọn slice.
- 1 — có một slice rõ + đường đi, nhưng: tiêu chí chọn không nối về rủi ro kiến trúc ("feature tiêu biểu", "dễ demo"); hoặc chỉ có lý do chọn mà không có slice nào được cân nhắc & loại; hoặc một tầng bị rút/để ngoài chỉ ghi "để sau" không lý do.
- 2 — đúng dạng: một slice duy nhất, đường E2E chạm đủ các tầng (tầng nào rút độ sâu hoặc phần nào cố ý để ngoài đều có lý do ghi rõ); lý do chọn nêu bằng rủi ro/invariant slice chạm được; liệt kê ≥1 slice thay thế đã cân nhắc & loại kèm lý do loại.

## 3. BẰNG CHỨNG KIỂM ĐƯỢC — không bịa, không tự khen (xương sống)

Mọi con số và claim trong report phải có nguồn kiểm được. Claim về code đối chiếu với code gốc `/Users/uspro/Desktop/namnson/hex_agent`.

- 0 — có ≥1 claim bịa hoặc không thể kiểm: anchor `file:line`/tên hàm/hành vi không khớp code gốc; con số (số test, tỉ lệ tick, kết quả spike) không có nguồn; link staging không tồn tại nhưng viết như đang chạy; hoặc câu tự khen ("kiến trúc đã được chứng minh", "sẵn sàng scale") không kèm bằng chứng. Bất kỳ claim bịa nào → tiêu chí này 0.
- 1 — đúng phần lớn nhưng 1–2 chỗ mơ hồ không gắn nhãn: anchor thiếu vị trí kiểm được ("đâu đó trong kernel"); số liệu ước lượng không ghi là ước lượng; một claim hành vi chỉ suy diễn từ tên hàm.
- 2 — mọi con số & claim truy được nguồn: claim code trỏ đúng `file:line` trong code gốc (hoặc evidence file đã anchor); chỗ chưa chắc được gắn nhãn rõ (open-Q / chưa đo / giả định); không một câu tự khen vô căn.

## 4. CHẠY THẬT, KHÔNG MOCKUP — tick chỉ khi có bằng chứng, không tuyên pass hộ (xương sống)

Luật sống còn của GĐ8: ô "đã validate" chỉ được tick khi có bằng chứng chạy THẬT trên chính bản đang được chứng minh (staging mở được / CI xanh / test pass / log-metric-trace). "Chạy trên máy tôi", happy-path giả, hay bằng chứng của một hệ KHÁC (vd bản gốc khi đang chứng minh bản rebuild) đều không được tính là tick.

- 0 — có ≥1 ô tick không kèm bằng chứng chạy thật trên bản được chứng minh; hoặc mượn bằng chứng của hệ khác/bản cũ để tick cho bản đang proof; hoặc artifact tự tuyên "pass" cổng thay người duyệt (CTO). Một tick khống → tiêu chí này 0.
- 1 — không tick khống, nhưng kỷ luật bằng chứng mờ ở 1–2 chỗ: ô để trống nhưng không được ghi thành rủi ro còn lại + nơi kiểm; trạng thái staging/CI nói nước đôi khiến người đọc có thể hiểu nhầm là đã chạy.
- 2 — kỷ luật trọn: mỗi ô `[x]` kèm bằng chứng chạy chỉ-được-trỏ; ô chưa chạy để trống + ghi thẳng là rủi ro + nơi kiểm; link staging thật hoặc ghi rõ "chưa có — chặn pass"; cổng được TRÌNH cho người giữ vai CTO quyết, report không tự phán pass.

## 5. DÙNG ĐƯỢC NGAY — người nhận cầm đi làm được (xương sống)

Report có 3 người nhận: CTO quyết go/no-go; dev chạy lại / dựng slice; `/frame` nhận khung slice (scope + đường đi + tiêu chí nghiệm thu) để viết code thật.

- 0 — đọc xong không hành động được: đường đi E2E chỉ liệt kê tên tầng, không chỉ thành phần đảm nhận từng chặng; checklist không có tiêu chí "khi nào được tick"; `/frame` không nhận được khung slice (thiếu scope hoặc tiêu chí nghiệm thu); CTO không có căn cứ để quyết.
- 1 — dùng được nhưng phải quay lại hỏi 1–2 chỗ: một chặng E2E không rõ thành phần nào lo; một ô checklist thiếu tiêu chí tick đo được; bước kế tiếp nêu chung chung không chỉ đích danh việc + skill nhận.
- 2 — cầm đi làm được ngay: mỗi chặng E2E chỉ rõ thành phần + điều phải chứng minh; mỗi ô checklist có tiêu chí tick đo được; khối bàn giao chỉ đích danh việc kế + skill nhận (`/frame`, `/backlog`, …); CTO có đủ dữ kiện (staging · checklist · giả định đổi · rủi ro) để quyết go/no-go.

## 6. BÁM ĐẦU VÀO GĐ7 + FEED NGƯỢC

Hợp đồng: `skeleton` CHỨNG MINH cái đã chốt, không chọn lại — đúng stack GĐ7, đúng boundary GĐ6; giả định phải đổi sau khi va thực tế được ghi + feed ngược về artifact nguồn; rủi ro chưa gỡ có địa chỉ kiểm.

- 0 — đổi/chọn lại stack hoặc kiến trúc so với GĐ7/GĐ6 mà không khai báo; hoặc thiếu đầu vào GĐ7 mà tự bịa stack (không có block ⚠️ đầu-vào-ngoài); hoặc report không có mục "giả định đã đổi".
- 1 — đúng stack/kiến trúc đã chốt, nhưng feed ngược mỏng: giả định đã đổi nêu chung chung, không chỉ artifact nào (PRD/Architecture/stack) phải cập nhật; hoặc có rủi ro còn lại không ghi nơi kiểm.
- 2 — chứng minh đúng cái đã chốt; mỗi giả định đã đổi chỉ rõ feed ngược về đâu; mỗi rủi ro còn lại có địa chỉ kiểm cụ thể (GĐ nào / skill nào / slice nào); mắt xích GĐ7→GĐ8→GĐ9 truy vết được.

## 7. RANH GIỚI VAI + LỐI ĐI TIẾP

Hợp đồng: `skeleton` chỉ *định slice + validate + báo cáo*. Code thật giao `/frame`; phân rã Epic/Story/AC là `/backlog`; chọn kiến trúc là `/shape`, stack là `/stack`. Cấm phủ định cứng — chỗ chưa proven phải kèm lối đi tiếp.

- 0 — lấn vai: tự viết code slice trong artifact, phân rã story/AC, hoặc mở lại quyết định kiến trúc/stack; hoặc dùng phủ định cứng ("không chạy được", "sai kiến trúc") mà không kèm lối đi tiếp.
- 1 — đúng vai chính nhưng lấn nhẹ (vd đặc tả chi tiết mức pseudo-code lẽ ra của `/frame`, hay đẻ vài story lẻ), hoặc 1 chỗ chưa proven được nêu mà không có lối đi tiếp.
- 2 — đúng vai trọn: định slice + checklist + báo cáo, code bàn giao `/frame`, phân rã bàn giao `/backlog`; mọi chỗ chưa proven đều kèm ít nhất một lối đi tiếp cụ thể (dựng nốt tầng thiếu / spike bổ sung / thu hẹp slice / kiểm ở GĐ sau).

## Luật gate

Tiêu chí **3, 4, 5** là xương sống. Bất kỳ cái nào = 0 → artifact **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một report 12/14 nhưng có một ô tick khống (tiêu chí 4 = 0) vẫn rớt — vì GĐ8 là cổng bằng chứng cuối trước khi đổ ngân sách: lãnh đạo sẽ tin nhầm "kiến trúc đã chứng minh" và quyết sai trên nền chưa chạy. Gate quan trọng hơn tổng: khi so nhiều bản, loại hết bản rớt gate trước, rồi mới xếp theo tổng.

## Vì sao 7 tiêu chí này

Hai cái đầu đo *report có đúng hình cái skeleton hứa không* (mở bằng góc nhìn lãnh đạo đọc-được 3 tầng; một slice mỏng nhất xuyên đủ tầng có lý do). Ba cái giữa — ba gate — đo *có trung thực và dùng được không*: bằng chứng kiểm được (không bịa), chạy thật không mockup (luật sống còn khiến GĐ8 tồn tại), và người nhận cầm đi làm được ngay (report vô dụng thì proof cũng vô nghĩa). Hai cái cuối đo *có nằm đúng chỗ trong pipeline không* (bám GĐ7 + feed ngược; đúng vai + lối đi tiếp). Gộp lại = toàn bộ hợp đồng của `skeleton`, không hơn. Thêm tiêu chí thứ 8 chỉ khi có một kiểu lỗi thật lặp lại mà 7 cái này không bắt được.
