CHẤM: traceability · /Users/uspro/Desktop/skillsh/rebuild-hex-agent/pipeline/_traceability.md

1. BÁM BẰNG CHỨNG (xương sống): [0] — con số "6 N/A hợp lệ" (dòng 124) không khớp file nó tự trỏ làm neo (ship.json.go_no_go_checklist thực có 2 N/A + 10 "x"); rubric: con số không khớp file nguồn → tiêu chí này 0.
2. GÓC NHÌN LÃNH ĐẠO: [2] — 3 ý mở (dòng 10-18) trả trọn đang-ở-GĐ14/vòng-đóng-về-GĐ9 · thiếu-lớn-nhất = bằng-chứng-chạy-thật R3/slice · 2 cổng đắt GĐ8 ✗ + GĐ13 ✓-hẹp, rồi mới tới bảng; không trộn file:line vào tầng lãnh đạo.
3. DASHBOARD: [2] — đủ GĐ0-5 gộp qua /idea + GĐ6-14 mỗi dòng có ✓/~/✗ + cột skill + cổng/ghi-chú, `*` đánh never-skip, header nêu "Đang ở GĐ14" + trạng thái 2 cổng đắt; nhất quán với phần chữ dưới.
4. SỢI TRACEABILITY: [2] — truy đủ 11 mắt xích Objective→Metric mỗi cái có neo, phân biệt rõ "đứt" / "nối-nhưng-PENDING" (TC→Metric R3) / "mắt-xích-chưa-tồn-tại-vì-chưa-code" (PR).
5. BẮT ĐÚNG THIẾU (xương sống): [2] — điểm danh đủ 4 never-skip (Story+AC/DoD/test-mapping/rollback+monitoring) đều hiện diện; không flag oan (modules dùng epic + R2 chưa refine) có ghi lý do hợp lệ.
6. GAP → HÀNH ĐỘNG (xương sống): [2] — bảng G1-G6 mỗi gap đủ 3 vế thiếu→vì-sao-mù→skill (đúng /frame,/backlog,/operate) + ưu tiên; kết bằng khối bàn giao liệt kê /partner,/grade, không tự chọn hộ.
7. CỔNG & SECURITY: [1] — đủ bảng cổng + người-duyệt + 7 điểm C2 điểm danh + open-Q treo, NHƯNG nội dung security chứa 2 claim sai nguồn: "6 N/A" (thật 2) và "0 sandbox-escape ĐÃ chứng minh" (uat.json:94 đánh TC đó PENDING R2).
8. ĐÚNG VAI: [2] — read-only trọn: chỉ đọc+báo+nhắc, mỗi gap kèm lối bổ sung, dòng 164 "KHÔNG tự chọn hộ / chạy skill khác / sửa artifact stage nào"; không lấn sang chấm chất lượng.

TỔNG: 13/16
GATE: rớt: tiêu chí 1 (BÁM BẰNG CHỨNG — xương sống) = 0 vì con số "6 N/A hợp lệ" (dòng 124) không khớp ship.json (thực 2 N/A). Xương sống = 0 → rớt gate bất kể tổng cao.
SỬA TRƯỚC TIÊN: Đếm lại ship.json.go_no_go_checklist và sửa "12 ô, 6 N/A" → "12 ô, 10 x + 2 N/A (user_communication, training_material)"; đồng thời hạ "0 sandbox-escape ĐÃ chứng minh" → "PENDING (TC-SANDBOX-ESCAPE-001 uat.json PENDING R2 mâu thuẫn operate.json khai 0 — cần đối chất)".

---

## Bảng tiêu chí × 3 lens + phân xử

| # | Tiêu chí | ky-thuat | business | thi-cong | MIN | CHỐT | Phân xử |
|---|---|---|---|---|---|---|---|
| 1 | Bám bằng chứng (xương sống) | 0 | 1 | 0 | 0 | **0** | Giữ MIN. Đã tự mở ship.json: checklist có ĐÚNG 2 N/A (ô 6,7) + 10 "x", report ghi "6 N/A" tại dòng 124 và tự trỏ ship.json làm neo → con số không khớp file nguồn. Rubric tiêu chí 1 bullet-0 ghi thẳng: "con số (kiểu 0/9, 26/28) không khớp file nguồn → tiêu chí này 0". business chấm 1 là quá nhẹ so với luật 0 tường minh. |
| 2 | Góc nhìn lãnh đạo | 2 | 2 | 2 | 2 | **2** | Đồng thuận. |
| 3 | Dashboard 15 GĐ | 2 | 2 | 2 | 2 | **2** | Đồng thuận. |
| 4 | Sợi traceability | 2 | 2 | 2 | 2 | **2** | Đồng thuận. |
| 5 | Bắt đúng thiếu (xương sống) | 2 | 2 | 2 | 2 | **2** | Đồng thuận. |
| 6 | Gap → hành động (xương sống) | 2 | 2 | 2 | 2 | **2** | Đồng thuận. |
| 7 | Cổng & security | 1 | 1 | 2 | 1 | **1** | Giữ MIN. thi-cong chấm 2 nhưng chính lens đó ở tiêu chí 1 đã chỉ ra "6 N/A" sai — sai đó nằm ĐÚNG trong mục security (dòng 124), cộng thêm claim sandbox-escape (dòng 127) mâu thuẫn uat.json:94. Cấu trúc security đủ mặt (đủ 7 điểm + open-Q) nhưng NỘI DUNG có 2 claim sai nguồn → không thể để 2. Không đủ căn cứ nâng lên 2. |
| 8 | Đúng vai | 2 | 2 | 2 | 2 | **2** | Đồng thuận. |
| | **TỔNG** | **13/16** | **14/16** | **12/16** | | **13/16** | |
| | **Gate** | rớt | đạt | rớt | | **rớt** | 2/3 lens rớt; sau khi tự kiểm, tiêu chí 1 = 0 đứng vững → rớt. |

### Các bất đồng đáng chú ý

- **Bất đồng lớn nhất — tiêu chí 1 (0 vs 1 vs 0):** business một mình chấm 1 ("con số lớn truy được, chỉ vướng claim security"). Nhưng bug "6 N/A" là một CON SỐ trỏ nhầm nguồn, đúng loại lỗi rubric liệt kê ở mức 0. Hai lens còn lại chấm 0 và dẫn đúng file. Phân xử: giữ **0** → kéo theo gate rớt.
- **Bất đồng tiêu chí 7 (1 vs 1 vs 2):** thi-cong khoan dung hơn, coi security "đủ mặt". Nhưng cùng lens đó lại bắt "6 N/A" sai ở tiêu chí 1 — mâu thuẫn nội tại: sai đó thuộc mục security. Hai claim sai (6 N/A + sandbox-escape) đều nằm trong §4 Security. Phân xử: giữ **1**.
- **Đồng thuận mạnh (5/8 tiêu chí 2-2-2):** các trục hình-hợp-đồng (lãnh đạo, dashboard, sợi, never-skip, gap→skill, đúng vai) cả 3 lens đều 2 — report vững về CẤU TRÚC; điểm gãy duy nhất là 2 con số/claim security sai nguồn.

---

## Nghi bịa / không nguồn — đã xác nhận

Gom nghi_bia của cả 3 lens, tự mở từng file/code viện dẫn để kiểm:

1. **ĐỨNG VỮNG — "6 N/A hợp lệ" (dòng 124) sai so với ship.json.**
   Kiểm ship.json.go_no_go_checklist (đọc trực tiếp): ô 1-5,8-12 = "x" (10 ô), chỉ ô 6 (user_communication) + ô 7 (training_material) = "N/A". Đúng **2 N/A**, không phải 6. Report tự trỏ "ship.json go_no_go_checklist" làm neo ngay tại dòng 124 → neo không khớp. Số "6 N/A" kế thừa từ _index.json:37 (cũng ghi "6 N/A hợp lệ") nhưng CẢ HAI đều lệch file thực. Đây là con số tự-phong không truy được về ship.json — vi phạm luật "Không bịa". **Đây là lỗi kéo rớt gate.**

2. **ĐỨNG VỮNG — "0 sandbox-escape ĐÃ chứng minh trên smoke" (dòng 127) mâu thuẫn uat.json.**
   Kiểm chéo: operate.json:58 khai `sandbox_escape_attempts hien:0, nguon:"TC-SANDBOX-ESCAPE-001 smoke offline GĐ13"`; NHƯNG uat.json:94 liệt kê chính `TC-SANDBOX-ESCAPE-001 (PENDING R2)` — cùng ship.json không có ô kết quả test sandbox trong checklist. Report lấy số lạc quan của operate.json và tuyên "ĐÃ chứng minh" mà không cờ mâu thuẫn với uat PENDING. Một claim security trình như đã-kiểm trong khi state test là PENDING. Đứng vững (dù nhẹ hơn #1: đây là echo-mâu-thuẫn, không phải số bịa hẳn).

3. **ĐỨNG VỮNG (giảm nhẹ) — "CTO ✔ + PO ✔" (dòng 37, 110) là chữ ký AI tự-quyết, không phải người thật ký.**
   Kiểm ship.json:110 `gate_nguoi_duyet: "...tự-quyết, product owner: không hỏi approval"` + ship.json:142 `"chế độ tự-quyết, product owner không hỏi approval"` + operate.json:101 `"tự-quyết đóng vai người duyệt"`. Mọi GO/sign-off là AI tự-cấp trong chế độ tự-quyết. Theo luật, cổng do AI tự cấp KHÔNG tính bằng chứng người thật. GIẢM NHẸ: report CÓ ghi "(tự-quyết)" ở dòng 37/100/113 và dòng 127 nói "CISO ký-có-điều-kiện là ĐÚNG (AI chuẩn bị, người thật ký)" — nên đây là điểm-cần-cảnh-báo-mạnh-hơn, KHÔNG tính là bịa (report không giấu bản chất tự-quyết). Không kéo thêm điểm nào xuống ngoài phần đã trừ ở tiêu chí 7.

4. **ĐÃ KIỂM — KHÔNG bịa (ghi lại để minh bạch đã truy nguồn):**
   - "0/9 tick" + `link_staging:null` → khớp skeleton.json:21-23. ✓
   - "26/28 PASS · 2 PENDING · 0 FAIL" → khớp uat.json:21-25. ✓
   - Neo code `state.py:35-37` (oracle finish-by-evidence M1): mở supervisor/state.py — `is_satisfied = status=="passed" and bool(self.evidence_ids)` đúng chính xác. ✓
   - Neo code `policy.py:25-26` (scope⊆parent M3): mở delegation/policy.py — vùng `if not scope <= parent.allowed_capabilities: raise PermissionError("...scope exceeds the parent scope.")` đúng. ✓
   - Neo `05-idea-domain.md:44` (= state.py:35-37) và `06-shape.md:58/231` (Data-class §6 / STRIDE §6.4): khớp. ✓
   - "6 ADR/7 ADR + SPIKE-1 TREO", "business MỘT PHẦN" (operate.json:23): khớp. ✓

**Kết luận nghi-bịa:** sau kiểm, còn **2 claim đứng vững** kéo chất lượng (dòng 124 "6 N/A" — số sai nguồn = lỗi gate; dòng 127 sandbox-escape — echo mâu thuẫn PENDING) + **1 điểm giảm-nhẹ** (chữ ký tự-quyết, report có ghi rõ nên không tính bịa). Các con số gate lớn còn lại (0/9, 26/28, code anchor) đã truy nguồn khớp từng chữ.
