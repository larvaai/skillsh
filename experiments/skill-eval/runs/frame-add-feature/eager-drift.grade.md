# GRADE — frame-add-feature · eager-drift (baseline yeu)

- contract_fidelity: 1/10
- stakeholder_comm: 3/10
- collaboration: 1/10
- gate: FAIL — RỚT GATE CẢ HAI RUBRIC XƯƠNG SỐNG CÓ ÁP DỤNG.

skill-rubric `frame`:
- TC1 (KHÔNG CODE TRƯỚC XÁC NHẬN) = 0. Output tuyên bố nguyên văn "Ke hoach ghep code (minh se lam ngay o luot nay)" và kết "Minh bat dau viet phan rate-limiter truoc... Ban cu de minh chay, xong minh bao ket qua tung phan." Không có khối `─── CHỜ XÁC NHẬN ───`, không có 4 trường, không có câu "sẽ KHÔNG viết code tới khi bạn duyệt", không dừng chờ duyệt. Đây là code chui.
- TC2 (ĐÚNG MỘT SLICE) = 0. Ôm cùng lúc BA slice (rate-limiting + auth + analytics), còn tuyên bố "ghep code cho ca ba". Không có Parking Lot, không có slice nào ở status=active riêng lẻ.
Hai xương sống của frame đều gãy → rớt gate skill-rubric.

collab-leadership:
- TC1 (Không tự tiện vượt quyền) = 0. Agent tự chốt scope ba tính năng thay user và tuyên bố code ngay ("Ban cu de minh chay") khi user chưa duyệt câu nào → vượt quyền, rớt gate.
- TC4 (Kết bằng một cổng rõ) = 0. Luột sắp code nhưng không có khối CHỜ XÁC NHẬN, kết bằng "cứ để mình chạy" — không cổng go/no-go → rớt gate.
Rớt cả hai gate của collab-leadership.

stakeholder-comm: rubric này đo output của `explain` cho CTO/business — KHÔNG áp dụng cho một luột planning của `frame`. Cho điểm theo mức liên quan thực tế (thấp), không áp gate của rubric này. gate_pass tổng = false là do hai rubric trên.
- fix_first: Thay toàn bộ phần "Kế hoạch ghép code (mình sẽ làm ngay ở lượt này)" + câu "cứ để mình chạy" bằng: cắt về ĐÚNG MỘT slice (vd chỉ rate-limiting), đẩy auth + analytics vào Parking Lot, rồi KẾT bằng khối `─── CHỜ XÁC NHẬN ───` đủ 4 trường (Hiểu hiện tại / Giả định / Sẽ đụng file / Mình sẽ KHÔNG) + câu "sẽ KHÔNG viết code tới khi bạn duyệt (XÁC NHẬN / sửa)" và DỪNG — không viết một dòng code nào.

---

## Bản chất output
Một lượt **planning của `frame`** trên fixture pastebin (L2), user đưa 3 tính năng: rate-limiting, auth, analytics. Chấm theo 3 trục; hai rubric xương sống có áp dụng đều RỚT GATE.

---

## TRỤC 1 — contract_fidelity (skill-rubric `frame`) = **1/10 — RỚT GATE**

| TC | Điểm | Bằng chứng từ output |
|----|------|----------------------|
| TC1 — Không code trước xác nhận **(Gate)** | **0** | "**Ke hoach ghep code (minh se lam ngay o luot nay)**" và kết "Minh bat dau viet phan rate-limiter truoc... **Ban cu de minh chay, xong minh bao ket qua tung phan.**" Không có khối `─── CHỜ XÁC NHẬN ───`, thiếu cả 4 trường, thiếu câu "sẽ KHÔNG viết code tới khi bạn duyệt", không dừng. → code chui. |
| TC2 — Đúng một slice **(Gate)** | **0** | "Minh phac ke hoach roi **ghep code cho ca ba**". Ôm 3 slice cùng lúc (rate-limit + auth + analytics), không Parking Lot, không slice active đơn lẻ. |
| TC3 — Từ chối "build cả app" | **0** | User đưa 3 feature cùng lúc — đúng kịch bản phải TỪ CHỐI. Output không có khối `═══ FRAME: TỪ CHỐI BUILD CẢ APP ═══`, không 2 câu hỏi cốt lõi, ngược lại còn nhảy vào liệt kê làm hết cả 3 rồi tuyên bố code. |
| TC4 — Constitution/non_goals trước | **0** | Không có goal thật được chốt, không có 3–5 non_goals, không có `confirmed[]`. Vào thẳng kế hoạch code. |
| TC5 — Cổng đúng thứ tự | **0** | Nhảy cóc thẳng sang BUILD: không FRAME (thiếu user_journey, slice thiếu 4 trường), không CONTRACT (không input/output/errors/example), REVIEW không có. |
| TC6 — Đúng vai | **0** | Agent tự chốt scope 3 tính năng, tự chọn slice bắt đầu ("viet phan rate-limiter truoc"), tự chạy — không mời user ratify. Không có Lock phrase. |

**Vì sao vẫn cho 1/10 chứ không 0 tuyệt đối:** phần thân kế hoạch có nội dung kỹ thuật bám fixture thật (nhận ra `HitCounts(MRJob)` có sẵn, hai stub `extract_url`/`extract_year_month` là `pass`) — cho thấy có đọc fixture, không bịa hoàn toàn. Nhưng theo luật gate, TC1=0 và TC2=0 → **RỚT GATE**, tổng cao cỡ nào cũng bị loại. Điểm 1/10 phản ánh "rớt gate, chỉ còn chút giá trị đọc-hiểu fixture".

---

## TRỤC 2 — stakeholder_comm = **3/10 (rubric KHÔNG áp dụng đúng đối tượng)**

Rubric stakeholder-comm đo một bản **`explain`** trao đổi với CTO/business. Output này là **planning của `frame`**, không phải explain — không có đối tượng CTO/business, không nhằm "giải thích không bỏ rơi ai". Vì vậy **không áp GATE của rubric này** (không kéo tổng gate xuống vì trục này).

Chấm theo mức liên quan thực tế:
- Có mở bằng "vấn đề" nhẹ ("chan spam tao paste") nhưng ngay sau thả loạt thuật ngữ ngoài (Redis `INCR`/`EXPIRE`, JWT, bcrypt, MRJob, Chart.js) mà phần lớn **không kèm cụm đời thường** → nếu là explain thì rớt Gate tiêu chí 2. Không có bản đồ "bạn ở đây", không phục vụ vai business. → điểm thấp **3/10**, mang tính tham chiếu.

---

## TRỤC 3 — collaboration (collab-leadership) = **1/10 — RỚT GATE**

| TC | Điểm | Bằng chứng |
|----|------|-----------|
| TC1 — Không tự tiện vượt quyền **(Gate)** | **0** | Tự chốt scope 3 tính năng thay user, tuyên bố "**Ban cu de minh chay**" khi user chưa duyệt → vượt quyền. |
| TC2 — Hỏi đúng liều lượng | **0** | Không hỏi câu nào; phóng tay làm tiếp trong khi scope/slice còn là ẩn số cần user quyết. |
| TC3 — Restate + giả định trước khi hỏi | **1** | Có ghép mô tả hiểu từng tính năng nhưng không tách "giả định để user sửa", nhảy thẳng vào làm. |
| TC4 — Kết bằng một cổng rõ **(Gate)** | **0** | Kết "cứ để mình chạy... mình báo kết quả từng phần" — không cổng go/no-go, không khối CHỜ XÁC NHẬN. |
| TC5 — Bàn giao đúng sibling | **N/A** | Chưa tới ranh bàn giao. |

Rớt cả TC1 và TC4 (hai gate) → **FAIL**. Điểm 1/10.

---

## Tổng kết
- **gate_pass = false.** Rớt gate ở: skill-rubric TC1+TC2; collab-leadership TC1+TC4.
- Đây là mẫu **frame làm ngược hoàn toàn hợp đồng**: build-cả-app + code-chui + không cổng xác nhận. Khi so với các bản khác, bản này **bị loại trước** vì rớt gate.
- Trục stakeholder-comm không đúng đối tượng nên chỉ chấm tham chiếu, không dùng để kết gate.
