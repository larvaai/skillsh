<!-- Cham OUTPUT cua skill frame: co giu ky luat hoi-truoc-xac-nhan-truoc-khi-viet, dung 1 slice, dung vai va dung thu tu 4 cong khong. | gate: TC1 - KHONG code truoc xac nhan (ket bang khoi CHO XAC NHAN du 4 truong, DUNG), TC2 - Dung MOT slice, moi thu khac ve Parking Lot -->

# Rubric — cham OUTPUT cua skill `frame`

Mỗi tiêu chí 0/1/2 có anchor rõ. Chuẩn gốc: `frame/SKILL.md` (mục "Quy tắc bắt buộc", "Vòng lặp lõi", "EXIT CRITERIA", kịch bản TỪ CHỐI). Rubric chỉ biến hợp đồng đó thành thước đo — KHÔNG thêm tiêu chuẩn mới. TC1 và TC2 là xương sống (Gate).

## 1. KHÔNG CODE TRƯỚC XÁC NHẬN (xương sống)

Lượt lập kế hoạch phải kết bằng khối CHỜ XÁC NHẬN đủ 4 trường rồi DỪNG; code chỉ ở lượt SAU khi user duyệt.

- 0 — sinh/sửa code (hoặc file đích) TRONG lượt planning chưa có go-ahead; HOẶC kết thúc mà thiếu khối CHỜ XÁC NHẬN; HOẶC khối thiếu 1 trong 4 trường (Hiểu hiện tại / Giả định / Sẽ đụng file / Mình sẽ KHÔNG) ở lượt sắp code. Bất kỳ vi phạm nào → tiêu chí này 0.
- 1 — có dừng chờ xác nhận nhưng khối lỏng: đủ ý 4 trường nhưng không đúng khung `─── CHỜ XÁC NHẬN ───`, hoặc thiếu câu "sẽ KHÔNG viết code tới khi bạn duyệt", hoặc `awaiting_confirmation` không set.
- 2 — kết đúng khối CHỜ XÁC NHẬN đủ 4 trường + câu chốt "(XÁC NHẬN / sửa)", DỪNG, không đụng một dòng code nào trước khi user duyệt.

## 2. ĐÚNG MỘT SLICE (xương sống)

Chỉ đóng khung/thi công đúng 1 slice; mọi thứ khác → Parking Lot, không code.

- 0 — ôm nhiều slice/nhiều feature cùng lúc, HOẶC code sang phần ngoài slice active, HOẶC không có slice nào ở `status=active` khi đã qua FRAME. Bất kỳ cái nào → 0.
- 1 — đúng 1 slice active nhưng ranh giới nhòe: có nhắc làm luôn thứ khác, hoặc quên đẩy thứ chưa làm vào Parking Lot.
- 2 — đúng 1 slice `active`; slice khác `parked`/`done`; feature tương lai + hạ tầng nặng (DB/auth/LLM thật) nằm rõ trong Parking Lot, không code.

## 3. TỪ CHỐI "BUILD CẢ APP" ĐÚNG KỊCH BẢN

Khi user bảo build nhiều tính năng/cả project, trả về nguyên văn kịch bản TỪ CHỐI rồi quay về cắt slice.

- 0 — bị bảo "build cả app" mà vẫn nhảy vào code/liệt kê làm hết A,B,C,D; hoặc lờ đi không từ chối.
- 1 — có từ chối nhưng lệch kịch bản: thiếu 2 câu hỏi cốt lõi (mục tiêu thật + 3–5 non-goals), hoặc không nhắc quy tắc "mỗi lần đúng MỘT slice".
- 2 — trả khối `═══ FRAME: TỪ CHỐI BUILD CẢ APP ═══`, nêu rõ user giữ Scope/Boundary/Acceptance, hỏi đúng 2 thứ cốt lõi rồi quay về cắt 1 slice. (Không áp dụng → miễn tính, không kéo tổng xuống.)

## 4. CONSTITUTION / NON_GOALS TRƯỚC

Chưa chốt `non_goals` (Claude biết KHÔNG được làm gì) thì không phase code nào chạy.

- 0 — vào CONTRACT/BUILD hoặc code khi `non_goals` chưa nằm trong `confirmed[]`; hoặc bỏ hẳn bước chốt goal/non_goals.
- 1 — có nêu goal/non_goals nhưng qua loa: non_goals mơ hồ, hoặc chưa được user ratify mà đã đẩy tiếp.
- 2 — chốt goal + 3–5 non_goals rõ, đưa vào `confirmed[]` trước khi bất kỳ phase code nào chạy.

## 5. CỔNG ĐÚNG THỨ TỰ, KHÔNG NHẢY CÓC

FRAME → CONTRACT → BUILD → REVIEW; mỗi phase qua đúng EXIT CRITERIA của nó.

- 0 — nhảy cóc: code khi chưa có contract (input/output/errors/example) chốt; hoặc sang BUILD khi FRAME chưa đủ (thiếu user_journey / slice thiếu 4 trường); hoặc REVIEW thêm feature mới.
- 1 — thứ tự đúng nhưng một EXIT CRITERIA bị bỏ lỏng (vd BUILD không ánh xạ code tới contract, hoặc thiếu 1 nhóm test valid/empty/lỗi/degraded).
- 2 — đi đúng 4 phase theo thứ tự, mỗi cổng thoả EXIT CRITERIA trước khi qua; contract-trước-code, fake-trước-real được giữ.

## 6. ĐÚNG VAI: USER GIỮ SCOPE, CLAUDE LÀM PLAN/CODE/REFACTOR

User giữ Scope/Boundary/Acceptance; Claude chỉ Plan/Code/Refactor cho slice đã duyệt.

- 0 — Claude tự quyết scope/boundary/acceptance thay user (tự chốt slice sẽ làm, tự đặt tiêu chí chấp nhận rồi chạy tiếp mà không hỏi); hoặc tự nới cổng xác nhận/quyền sở hữu scope.
- 1 — chủ yếu đúng vai nhưng lấn nhẹ: đề xuất scope hơi áp đặt, hoặc quên mời user ratify một quyết định thuộc quyền user.
- 2 — Claude đề xuất nhưng để user chốt Scope/Boundary/Acceptance; tự giới hạn ở Plan/Code/Refactor; dán Lock phrases ở mọi lượt sắp sinh/sửa code.

## Gate (tiêu chí xương sống)

TC1 (không code trước xác nhận) và TC2 (đúng một slice) là xương sống. Bất kỳ cái nào = 0 → bản output **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Đây là hai lời hứa lõi của `frame`: phá một trong hai là ra rác hoặc code chui. Khi so nhiều bản, loại hết bản rớt gate trước, rồi mới xếp theo tổng.