CHẤM: 14-operate · /Users/uspro/Desktop/skillsh/rebuild-hex-agent/pipeline/14-operate.md

[0] 1. SỐ THẬT (xương sống) — "0 sandbox-escape / 0 secret / false_finish=0 trên smoke" trình như số-đã-đo & "ĐẠT ở nền" và dùng chống-lưng cổng GO, nhưng nguồn (TC-SANDBOX-ESCAPE-001, TC-REDACT-*) đều PENDING ở GĐ12 và GĐ8 = 0/9 tick-thật (chưa chạy rebuild) → số bịa; thêm "15 SECRET_KEYS" trong khi redaction.py có 14.
[2] 2. ĐÓNG VÒNG GĐ1 (xương sống) — M1/M2/M3 trong nhóm BUSINESS đối chiếu THẲNG mục tiêu gốc GĐ1 (M1 state.py:35-37 · M3 policy.py:25-26), mỗi cái có target + số hiện/`chưa có số` + trạng thái + cách lấy, dòng ĐỌC-CHO-LÃNH-ĐẠO và câu cổng dùng đúng phép so.
[2] 3. DÙNG ĐƯỢC THẬT (xương sống) — sự cố giả định đi trọn: alert false_finish>0 (ngưỡng) → owner theo vùng (4 team) → SEV → tắt flag features.yaml theo Runbook GĐ13 §3C → hậu kiểm → backlog; I-1..I-3 trỏ chỉ số cụ thể; §5 nêu rõ điều CEO/CTO phải chốt.
[2] 4. ĐỦ BỘ BA ARTIFACT — đủ 3: Dashboard 4 nhóm (DORA đủ 4) ghi SỐNG cập-nhật-mỗi-nhịp; Incident đủ 5 bước + 3 playbook; Iteration có nhịp+học+đường-backlog; độ sâu tỉ lệ rủi ro, không phình post-mortem khi 0 incident.
[2] 5. VÒNG HỌC VỀ BACKLOG — nhịp 2-tuần (ai dự rõ); 3 item, mỗi item truy về một `chưa có số`/điều-kiện-chặn và trỏ đúng địa chỉ GĐ9 (I-1→E09/E10, I-2→F1.6 S1.6.1, I-3→OQ-1), chỉ liệt kê không phân rã story.
[2] 6. KẾ THỪA GĐ13 + ĐÚNG VAI — dẫn nguồn GĐ13 rõ (alert false_finish>0, owner 4 team, rollback tắt-flag, OQ-1 treo) và chỉ NỐI thêm; mọi việc ngoài vai hand off đúng skill; metric xấu nêu số + lối đi, không phủ định cứng, không tự sunset.
[1] 7. ĐỌC-ĐƯỢC 3 TẦNG — có "GÓC NHÌN LÃNH ĐẠO" đầu bài + Dashboard có dòng ĐỌC-CHO-LÃNH-ĐẠO, NHƯNG §2 Incident và §3 Iteration nằm dưới "CHI TIẾT KỸ THUẬT" và không mở bằng góc nhìn lãnh đạo riêng — trúng điều kiện level-1 "một trong ba artifact thiếu góc nhìn lãnh đạo riêng".
[2] 8. CỔNG + BÀN GIAO + LÝ DO/PHƯƠNG ÁN ĐÃ LOẠI — cổng đúng câu "Đạt mục tiêu chưa? Làm gì tiếp?"; phân vai A5 + chế độ tự-quyết ghi tường minh; bàn giao đủ khuôn + đủ lối đi (/backlog /review /idea /partner /frame); quyết định lớn (nhịp 2-tuần, 3 số máy Business, 4 phương án cổng đã loại) có lý do + phương án loại kèm vì sao.

TỔNG: 13/16
GATE: rớt — tiêu chí 1 (SỐ THẬT, xương sống) = 0: dashboard + cổng GO trình test-chưa-chạy ("0 sandbox-escape / 0 secret / false_finish=0 trên smoke") như số-đã-đo/"ĐẠT ở nền", cộng "15 SECRET_KEYS" sai (code = 14). Đây chính là "báo-xong-khống" ở tầng quản trị — chỗ CEO quyết đầu tư vòng kế — nên rớt dù tổng 13/16.
SỬA TRƯỚC TIÊN: Hạ mọi "0 sandbox-escape / 0 secret / false_finish=0 trên smoke" từ số-đo/"ĐẠT ở nền" xuống `chưa có số` + cách lấy ("TC-SANDBOX-ESCAPE-001 + TC-REDACT-* PENDING ở GĐ12, GĐ8 0/9 tick-thật — đo trên staging khi có code"), gỡ khỏi chống-lưng cổng GO, và sửa "15 SECRET_KEYS" → 14 theo control/redaction.py.

---

## 2. Bảng tiêu chí × 3 lens + phân xử bất đồng

| # | Tiêu chí | ky-thuat | business | thi-cong | Hợp nhất | Ghi chú phân xử |
|---|----------|:--------:|:--------:|:--------:|:--------:|-----------------|
| 1 | SỐ THẬT (xương sống) | 0 | 0 | 0 | **0** | Ba lens đồng thuận; tự kiểm xác nhận (dưới). |
| 2 | ĐÓNG VÒNG GĐ1 (xương sống) | 2 | 2 | 2 | **2** | Đồng thuận; khớp ideas/hex-agent-rebuild.md §M1-M3. |
| 3 | DÙNG ĐƯỢC THẬT (xương sống) | 2 | 2 | 2 | **2** | Đồng thuận; sự cố giả định đi trọn đường. |
| 4 | ĐỦ BỘ BA ARTIFACT | 2 | 2 | 2 | **2** | Đồng thuận. |
| 5 | VÒNG HỌC VỀ BACKLOG | 2 | 2 | 2 | **2** | Đồng thuận. |
| 6 | KẾ THỪA GĐ13 + ĐÚNG VAI | 2 | 2 | 2 | **2** | Đồng thuận. |
| 7 | ĐỌC-ĐƯỢC 3 TẦNG | 2 | 2 | **1** | **1** | BẤT ĐỒNG — giữ điểm thấp (thi-cong). Xem dưới. |
| 8 | CỔNG + BÀN GIAO + LÝ DO/LOẠI | 2 | 2 | 2 | **2** | Đồng thuận. |
| | **TỔNG** | 14 | 14 | 11 | **13** | |

### Bất đồng đáng chú ý & cách phân xử

**Tiêu chí 7 (ky-thuat/business = 2 vs thi-cong = 1) — giữ 1.**
Tôi tự mở artifact kiểm cấu trúc tầng lãnh đạo:
- Có "── GÓC NHÌN LÃNH ĐẠO ──" ở đầu bài (dòng 10-22) bao cả 3 artifact chung một chỗ.
- Dashboard (§1) có dòng riêng "▸ ĐỌC CHO LÃNH ĐẠO (1 dòng)" (dòng 56).
- Incident (§2, dòng 117-119) MỞ bằng ghi chú `>` kỹ thuật ("Kế thừa NGUYÊN từ GĐ13/GĐ10... alert rule, incident owner") — không phải góc nhìn lãnh đạo, không 1-3 con số nghiệp vụ.
- Iteration (§3, dòng 194-198) MỞ thẳng vào code block "Nhịp review : 2 TUẦN..." — không có dòng lãnh đạo riêng.

Rubric tiêu chí 7 level-1 nêu đúng điều kiện "**một trong ba artifact thiếu góc nhìn lãnh đạo riêng**"; ở đây có tới HAI artifact (§2, §3) thiếu góc nhìn lãnh đạo riêng — chỉ Dashboard có. Self-check của chính artifact (dòng 229) tuyên mỗi artifact có dòng lãnh đạo, nhưng "1 dòng 0 incident" và "1 câu iteration" mà nó viện thực ra nằm ở KHỐI LÃNH ĐẠO TỔNG đầu bài (dòng 20-22), không phải mở đầu §2/§3. Luật cứng hợp đồng là "mỗi artifact MỞ bằng Góc nhìn lãnh đạo". Không chứng minh được thi-cong sai — ngược lại đọc kỹ thì thi-cong đúng hơn → giữ **1** theo luật lấy-điểm-thấp.

**Tổng lệch giữa các lens (14/14/11):** chênh 3 điểm chỉ do một tiêu chí 7 (thi-cong bắt được lỗi cấu trúc tầng mà 2 lens kia bỏ qua). Ba tiêu chí xương sống ba lens đều đồng thuận, và cái = 0 (tiêu chí 1) mới là cái quyết định gate — nên dù ky-thuat/business để tổng 14, kết cục vẫn RỚT như cả ba lens kết luận.

---

## 3. Nghi bịa / không nguồn — đã xác nhận

**[ĐỨNG VỮNG] "0 sandbox-escape" trình như số-đã-đo / "ĐẠT ở nền"** (operate dòng 19, 100, 247, 262).
Kiểm: 12-uat.md:112 ghi TC-SANDBOX-ESCAPE-001 = **PENDING (R2)**; 13-ship.md:76 chỉ test rollback-config + flag-off scope-check fail-closed, KHÔNG chạy sandbox-escape; 08-skeleton.md:107 = **0/9 tick THẬT** (code rebuild chưa chạy staging). → số 0 là kết quả một test chưa chạy = bịa. ĐỨNG.

**[ĐỨNG VỮNG] "0 secret rò ui_payload" trình như đo-được / "ĐẠT ở nền"** (dòng 19, 101, 247).
Kiểm: 12-uat.md:80 TC-REDACT-RAWARGS-003 = PENDING ⚠️ ("chưa chạy write-tool"); 12-uat.md:81 TC-REDACT-UIPAYLOAD-004 = PENDING. → tuyên 0-secret-đạt trước khi test chạy = bịa. ĐỨNG.

**[ĐỨNG VỮNG] "15 SECRET_KEYS"** (dòng 101).
Kiểm: /Users/uspro/Desktop/namnson/hex_agent/control/redaction.py:16-33 có ĐÚNG **14** key (api_key, apikey, authorization, password, passwd, secret, secret_key, client_secret, token, access_token, refresh_token, private_key, set-cookie, cookie). 12-uat.md:81 còn ghi "~15" (xấp xỉ, có dấu ~); operate bỏ dấu ~ biến ước-lượng thành số cứng SAI. ĐỨNG.

**[ĐỨNG VỮNG] "false_finish_total=0 trên smoke" trình như số đo-được** (dòng 58, 62, 65 "guard cắt đúng trên smoke").
Kiểm: 13-ship.md:114 ghi `false_finish_total=0` là "**Kỳ vọng**" của bước smoke; 13-ship.md:148 để `false_finish_total=0` ở cột tiêu-chí-ĐÓNG-R1 (mục tiêu cần đạt), chưa đạt; 08-skeleton.md:107 = 0/9 tick THẬT → chưa có lượt smoke nào thực chạy trên rebuild. Artifact có hedge "CHƯA đủ lượt thật" nhưng vẫn nêu 0 như số đo → ĐỨNG.

**[ĐỨNG VỮNG] "Nền R1 an toàn đã chứng minh BẰNG SỐ" làm lý do GO** (dòng 262; cũng "nền R1 an toàn ĐẠT" dòng 274).
Kiểm: dựa trên chính ba số chưa đo ở trên → chống-lưng cổng GO bằng số ma, mâu thuẫn lời tự-thú "hệ chưa chạy đủ thật" (dòng 22) + GĐ8 0/9. ĐỨNG.

**[DEMOTE — KHÔNG tính là bịa] "CTO ✔ + PO ✔ (2026-07-02)"** (dòng 260) — cả 3 lens flag.
Kiểm: đây là dấu tự-cấp trong chế độ tự-quyết, ĐƯỢC ghi tường minh (dòng 6, 241, 257: "người viết đóng vai CEO/CTO+PO tự quyết, ghi rõ"). Rubric tiêu chí 8 cho phép "tự-quyết ghi tường minh: ai ủy quyền, đóng vai gì, quyết định vẫn audit được". Dấu ✔ KHÔNG chống-lưng bất kỳ con số nào (các số ma đã tính riêng ở tiêu chí 1). → là role-play được công bố hợp lệ, KHÔNG phải claim bịa. Loại khỏi danh sách bịa (không đổi điểm — tiêu chí 1 đã = 0 vì các số khác).

**[DEMOTE — KHÔNG phải operate bịa] "GĐ12: 2 PENDING / 26 PASS"** (dòng 4, 18, 201) — thi-cong flag mềm.
Kiểm: 12-uat.md:11 chính là headline "26 PASS, 2 PENDING, 0 FAIL"; operate trích đúng, không tự chế. Đây là số MỀM kế thừa từ GĐ12 (bảng AC của uat có nhiều dòng PENDING hơn nhưng đó là con số của uat, không phải operate); operate nối một con số đáng ngờ mà không cảnh báo — điểm yếu nhẹ về kế thừa, KHÔNG phải bịa của operate. Loại khỏi danh sách bịa-của-operate.

**Kết:** sau tự kiểm, còn **5 claim bịa đứng vững** (3 số an-toàn-biên trình như đo-được + "15 key" sai + "chứng minh bằng số" làm lý do GO), tất cả trỏ vào cùng một lỗi gốc: trình test-chưa-chạy như số-đã-đạt ở tầng dashboard + cổng GO. Đủ để tiêu chí 1 = 0 → rớt gate.
