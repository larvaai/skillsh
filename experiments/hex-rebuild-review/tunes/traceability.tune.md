# TUNE — traceability (dựa trên chấm artifact `pipeline/_traceability.md`)

> Vòng tune cho skill `traceability`. Bám quy trình `tune/SKILL.md`: fixture cố định · MỘT biến duy nhất (bản sửa SKILL) · chấm mù · baseline trước · confirm bằng agent mới chống over-fit.
> Nguồn chấm: `experiments/hex-rebuild-review/grades/traceability.grade.md` (rớt gate, 13/16).

---

## §0 Chẩn đoán (≤6 câu)

Report rớt gate DUY NHẤT ở tiêu chí 1 (BÁM BẰNG CHỨNG — xương sống) = 0: con số "6 N/A hợp lệ" (dòng 124) không khớp `ship.json.go_no_go_checklist` (thực có 2 N/A: ô 6 user_communication + ô 7 training_material, còn lại 10 "x"); kéo theo tiêu chí 7 (Cổng & Security) bị hạ xuống 1 vì cùng claim sai đó nằm trong §4 Security, cộng claim "0 sandbox-escape ĐÃ chứng minh" (dòng 127) mâu thuẫn `uat.json:94` (TC-SANDBOX-ESCAPE-001 PENDING). 6 tiêu chí còn lại đều 2/2 — report VỮNG về hình hợp đồng, gãy đúng chỗ số/claim.
Lỗi này thuộc SKILL, không chỉ lần chạy: `_index.json:37` cũng ghi "6 N/A hợp lệ" — agent kế thừa con số từ bản tóm tắt tầng trên thay vì tự đếm file nguồn, mà SKILL.md HIỆN KHÔNG có luật nào buộc "số phải đếm lại ở artifact gốc, không tin summary upstream" (luật "Không bịa" và self-check #2 chỉ nói "bám artifact thật", đủ mơ hồ để agent tưởng trỏ đúng tên file là đủ, dù chưa đếm).
Claim sandbox-escape cũng cùng gốc: SKILL không có luật buộc cross-check một claim security-PASS chéo qua `uat.json` trước khi tuyên "ĐÃ chứng minh". Kết: đây là lỗi-của-SKILL (luật mơ hồ + thiếu luật xác minh số/claim), TUNE ĐƯỢC.

## §1 Fixture đề xuất (cố định cả thí nghiệm)

- **project**: `rebuild-hex-agent` (gói hex-agent-rebuild) — state pipeline đầy đủ tại `/Users/uspro/Desktop/skillsh/rebuild-hex-agent/pipeline/*.json|*.md`.
- **slug**: hex-agent-rebuild (pipeline đã chạy hết GĐ0→GĐ14, đang ở GĐ14 Operate).
- **mode/tham số**: soi CẢ pipeline (không chỉ 1 slug), y hệt lần chạy đã bị chấm. Không dùng đường "đầu vào ngoài state" — state đọc được đầy đủ.
- **Bẫy cố ý trong fixture (giữ nguyên, ĐỪNG sửa state)**: `_index.json:37` ghi sai "6 N/A" trong khi `ship.json.go_no_go_checklist` thực 2 N/A + 10 "x"; `uat.json:94` để TC-SANDBOX-ESCAPE-001 PENDING trong khi `operate.json:58` khai 0. Chính hai bẫy này là thứ phân biệt các variant — variant tốt phải đếm/cross-check ra đúng.
- **Lặp lại được**: mọi variant đọc đúng cây `rebuild-hex-agent/pipeline/`, cùng ghi output ra `experiments/runs/<ts>/<variant>/output.md`, không ai được đụng/sửa state nguồn.

## §2 Thước

- Dùng `experiments/hex-rebuild-review/rubrics/traceability.rubric.md` (8 tiêu chí 0/1/2, tối đa 16; xương sống = 1,5,6).
- Luật xếp hạng: **loại hết bản rớt gate trước** (bất kỳ tiêu chí 1/5/6 = 0), **rồi mới xếp theo tổng**. Hoà tổng → bản diff NHỎ/ROBUST hơn thắng (ít rủi ro over-fit vào đúng fixture này).
- Đối chiếu ngoài khi có claim code: `/Users/uspro/Desktop/namnson/hex_agent` (rubric đã ghi). Claim số đối chiếu file `pipeline/*.json` nguồn.

## §3 Các hướng thử (mỗi hướng nhắm ĐÚNG MỘT tiêu chí đang mất điểm)

Hai tiêu chí mất điểm: **#1 Bám bằng chứng (gate, kéo rớt)** và **#7 Cổng & Security**. Các hướng nhắm khác nhau; A/B/C dồn vào #1 (gate — quan trọng nhất) nhưng qua CƠ CHẾ khác nhau, D nhắm #7.

### Hướng A — Luật "đếm-lại-ở-nguồn, không tin summary" (nhắm tiêu chí 1)

**Giả thuyết:** Buộc mọi con số đếm được phải RE-COUNT ở artifact gốc và cấm kế thừa số từ bản tóm tắt tầng trên (`_index.json`) sẽ chặn đúng bug "6 N/A".

**Diff (thêm vào mục "## Luật cứng", sau bullet "Không bịa"):**
```
- **Số phải đếm lại ở NGUỒN GỐC.** Mọi con số đếm được (x/y ô, n N/A, k PASS/PENDING, m ADR) phải
  đếm trực tiếp trên artifact gốc của giai đoạn đó (vd `ship.json.go_no_go_checklist`), KHÔNG kế thừa
  con số từ bản tóm tắt tầng trên (`_index.json`, header, hay report giai đoạn khác). Nếu số ở summary
  khác số đếm được ở nguồn → báo con số ĐÚNG (đếm được) + cờ một dòng "summary lệch nguồn".
```

**Rủi ro:** Có thể làm report dài/chậm hơn nếu agent liệt kê thao tác đếm; cần dặn "đếm nhưng chỉ in con số cuối + neo", không in phần trung gian, kẻo va tiêu chí 2 (gọn 1 màn hình).

### Hướng B — Thêm bước "Kiểm số" vào block "Tự soi trước khi chốt" (nhắm tiêu chí 1)

**Giả thuyết:** Đặt câu tự-soi CHUYÊN cho con số (thay vì self-check #2 chung chung "bám artifact thật") sẽ bắt agent dừng lại đối chiếu trước khi chốt.

**Diff (thêm 1 mục vào "### Tự soi trước khi chốt (bắt buộc)", chèn thành mục 2b hoặc sau #2):**
```
2b. Mọi CON SỐ trong report (x/y ô, n N/A, số PASS/PENDING/ADR) mình đã đếm lại ở artifact gốc chưa,
    hay chép từ summary? Con số cuối có KHỚP đúng file:mục nó trỏ làm neo không? Lệch → sửa theo NGUỒN.
```

**Rủi ro:** Self-check là "nhắc" chứ không "cấm" — agent vẫn có thể lướt qua như đã lướt self-check #2 lần này; hiệu lực yếu hơn A (khác vị trí: A là luật-cứng, B là check-list cuối).

### Hướng C — Ví dụ mẫu một dòng dashboard "số-khớp-neo" (nhắm tiêu chí 1)

**Giả thuyết:** Cho một ví dụ MẪU cách viết một ô có số kèm neo đã-đếm (calibrate bằng example, như hướng A của `tune explain`) sẽ khiến agent bắt chước format "số + neo đã kiểm".

**Diff (thêm vào "## Ví dụ Case Management (rút gọn)", một dòng mẫu minh hoạ số-khớp-neo):**
```
Ví dụ ô số ĐÚNG (số đã đếm lại ở nguồn, không chép summary):
  "checklist 12 ô: 10 x + 2 N/A (user_communication, training_material)  [đếm ship.json.go_no_go_checklist]"
  — KHÔNG viết "6 N/A" vì đó là số ở _index.json summary, đếm nguồn ra 2.
```

**Rủi ro:** Ví dụ lấy đúng con số của fixture này → mùi over-fit; agent có thể học "case này = 2 N/A" thay vì học nguyên tắc đếm-lại. Bước 5 confirm trên fixture thứ hai là bắt buộc để lộ over-fit.

### Hướng D — Luật cross-check claim security-PASS chéo qua uat/gate (nhắm tiêu chí 7)

**Giả thuyết:** Buộc mọi claim "đã chứng minh / PASS" về security phải đối chiếu chéo `uat.json` (và cổng liên quan) trước khi tuyên, sẽ chặn claim "0 sandbox-escape ĐÃ chứng minh" mâu thuẫn PENDING.

**Diff (thêm vào mục "### Security đan giai đoạn (C2)" của thân report, hoặc thành 1 bullet luật cứng riêng cho security):**
```
- **Claim security-PASS phải chéo với uat + cổng.** Trước khi ghi một điểm security là "đã chứng minh/
  PASS/0 sự cố", đối chiếu `uat.json` (trạng thái TC tương ứng) và cổng GĐ12/13. Nếu TC còn PENDING/FAIL
  hoặc hai nguồn mâu thuẫn (vd operate khai 0 nhưng uat để PENDING) → ghi "PENDING/mâu thuẫn (neo cả hai)",
  KHÔNG lấy số lạc quan của một nguồn tuyên PASS.
```

**Rủi ro:** Chỉ chữa tiêu chí 7, KHÔNG gỡ gate (gate rớt vì tiêu chí 1). Nếu chạy một mình, report vẫn rớt gate — D phải ghép cùng một hướng gỡ #1 (A/B/C) mới lên điểm thật; giữ D làm hướng riêng để đo phần đóng góp của nó vào #7.

**Ghi chú ghép:** A (hoặc B) gỡ gate #1 + D nâng #7 là cặp có khả năng lên 15–16/16. Bước 6 cân nhắc merge A+D nếu cả hai qua confirm.

## §4 Ưu tiên

**TUNE NGAY.** Report rớt GATE (tiêu chí xương sống #1 = 0) — đây là loại lỗi nặng nhất theo rubric (CEO/CTO ra quyết định trên số sai), và nó thuộc lỗi-của-SKILL (thiếu luật đếm-lại-ở-nguồn + thiếu luật cross-check claim security), tune được. 6/8 tiêu chí đã 2/2 nên đòn bẩy rõ và hẹp: chỉ cần một luật xác minh số là gỡ được gate, chi phí sửa nhỏ.

## §5 Nhắc luật thí nghiệm (bắt buộc theo tune/SKILL.md)

- **Baseline trước:** chạy lại `traceability` HIỆN TẠI trên fixture §1 → `runs/<ts>/baseline/output.md`, chấm bằng thước §2. Bản đã có (`_traceability.md`, 13/16 RỚT GATE) dùng làm mốc — mọi variant phải hơn mốc này (tối thiểu: gỡ gate).
- **Một biến duy nhất:** mọi variant cùng fixture §1, chỉ khác bản sửa SKILL. Không ai đổi state nguồn hay fixture giữa chừng.
- **Chấm mù:** agent chấm chỉ thấy {project, "soi cả pipeline", output.md}, KHÔNG thấy variant theo hướng nào (đặt tên A/B/C/D trung tính).
- **Confirm agent mới + fixture thứ hai:** bản thắng chạy lại bằng agent MỚI trên (a) fixture §1 và (b) một project pipeline thứ hai (vd một slug/project khác có state đầy đủ, hoặc chèn một bẫy-số khác chỗ khác). Chỉ hơn ở fixture gốc → mùi over-fit (nhất là hướng C), xem lại diff. Hơn ở cả hai → điểm đến từ SỬA, đáng merge.
