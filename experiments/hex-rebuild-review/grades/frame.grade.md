CHẤM: frame · /Users/uspro/Desktop/skillsh/rebuild-hex-agent/frame/slice-01-taskloop-happy-path.md

[2] — Đúng MỘT lát happy-path E2E + 1 guard; §2 Boundary liệt 7 nhóm OUT, mỗi cái có LÝ DO lẫn ĐỊA CHỈ (resume→slice-02, RAG→E08/R2, control-plane→E21/R4…) và cố ý bỏ hạ tầng nặng (DB/auth/LLM thật) đúng luật.
[2] — §0 đặt 7 non-goals là hành-vi-cấm-cụ-thể ("KHÔNG resume", "KHÔNG gọi LLM thật", "KHÔNG terminal_run") TRƯỚC plan §4 + coding_rules override; rà lại plan §4 không bước nào chạm non-goal.
[2] — 8 AC dạng Given/When/Then có oracle PASS/FAIL rõ và mỗi AC chỉ nơi kiểm (integration/property Hypothesis/audit); slice đủ 4 trường (user_action/system_behavior/visible_output/acceptance).
[1] — Không một dòng code app và dùng đúng 2 seam công khai GĐ10, NHƯNG Plan §4 bước 2 kê middleware chain "Timing→PolicyGate→BudgetGuard→Retry→Condense→core" trong khi bootstrap.py:31 ghi rõ "BudgetGuard is intentionally NOT wired here" — bước này lệch wiring code gốc VÀ tự mâu thuẫn với chính §0/§4-bước-4 (budget enforce ở discipline/loop).
[2] — Ghi tường minh cái gì fake (LLM-plan=simulator tất định) và cái gì THẬT có lý do (fs_write/fs_read thật để sinh evidence thật cho judge) + điều kiện chuyển real (bật LLM/write-tool thật phải bật redact-raw-args TRƯỚC, RS-7/D4).
[1] — Đa số ~15 anchor resolve đúng, NHƯNG anchor `safety/sandbox.py:38,97` (dùng ở §1 chặng 6 + Plan bước 5 + bảng files) lệch xa: file chỉ 56 dòng nên dòng 97 KHÔNG tồn tại, dòng 38 là docstring chứ không phải jail-logic (thật ở :46), và cụm còn gán "PolicyGate fail-closed" cho file này trong khi PolicyGate không nằm ở sandbox.py.
[2] — §6 liệt 7 rủi ro, mỗi cái có *Kiểm* trỏ AC cụ thể (RS-1→AC-5/AC-1, RS-3→AC-4 property) + *Giảm*; rủi ro mang từ boundary (RS-6 resume) ghi rõ "KHÔNG gỡ trong slice này"→slice-02.
[2] — §8 chế-độ-tự-quyết có quyết định GO + lý do 4 điểm + 4 phương án đã loại kèm vì-sao-loại; §9 bàn giao trỏ đích cụ thể (BUILD theo Plan §4 · slice-02 resume · /uat GĐ12) mang theo open-Q RS-6/RS-7.

TỔNG: 14/16
GATE: đạt (xương sống: tiêu chí 1=2, tiêu chí 3=2, tiêu chí 6=1 — không cái nào =0; anchor sandbox.py lệch dòng-far + một cấu phần sai-file là lỗi mức-1 vì cơ chế jail có thật ở :46, không phải bịa claim ra khỏi hư không, nên không kéo tiêu chí 6 về 0)
SỬA TRƯỚC TIÊN: Sửa Plan §4 bước 2 — bỏ BudgetGuard khỏi chuỗi middleware kernel (bootstrap.py:31 nói rõ nó KHÔNG wired ở đây; budget enforce ở discipline/loop) VÀ sửa anchor `safety/sandbox.py:38,97` về đúng `:46` (`resolve_in_workspace`), tách PolicyGate về đúng file của nó.

---

## Bảng tiêu chí × 3 lens + phân xử bất đồng

| # | Tiêu chí | ky-thuat | business | thi-cong | Hợp nhất | Ghi chú phân xử |
|---|---|---|---|---|---|---|
| 1 | MỘT SLICE (xương sống) | 2 | 2 | 2 | **2** | Đồng thuận. |
| 2 | CONSTITUTION | 2 | 2 | 2 | **2** | Đồng thuận. |
| 3 | ACCEPTANCE ĐO ĐƯỢC (xương sống) | 2 | 2 | 2 | **2** | Đồng thuận. |
| 4 | CONTRACT-TRƯỚC-CODE | **1** | 2 | 2 | **1** | Bất đồng. Lấy THẤP NHẤT (ky-thuat=1) — đã KIỂM và xác nhận đúng, không nâng. |
| 5 | FAKE-TRƯỚC-REAL | 2 | 2 | 2 | **2** | Đồng thuận. |
| 6 | BÁM BẰNG CHỨNG (xương sống) | 2 | **1** | 2 | **1** | Bất đồng. Lấy THẤP NHẤT (business=1) — đã KIỂM và xác nhận đúng, không nâng, không hạ về 0. |
| 7 | GIẢ ĐỊNH & RỦI RO | 2 | 2 | 2 | **2** | Đồng thuận. |
| 8 | CỔNG & BÀN GIAO | 2 | 2 | 2 | **2** | Đồng thuận. |
| | **TỔNG** | 15 | 15 | 16 | **14** | Hợp nhất thấp hơn cả 3 vì nuốt lỗi mức-1 của cả hai lens (crit 4 từ ky-thuat, crit 6 từ business) vào cùng một bản. |

### Bất đồng #1 — Tiêu chí 4 (ky-thuat=1 vs business/thi-cong=2)

Phân xử: **giữ 1**. Luật hợp nhất buộc lấy điểm thấp nhất trừ khi chứng minh lens thấp chấm sai. Tôi mở `core/bootstrap.py`:
- Dòng 28–32: `_install_middleware` docstring ghi "Order = outer -> inner: timing, policy, retry, condense" và dòng 31 "BudgetGuard is intentionally NOT wired here: its same-tool counter is per-run… wire it per run instead."
- `middleware/budget.py:10` có `class BudgetGuard` thật → không phải bịa, mà là **lệch wiring**: Plan §4 bước 2 chèn BudgetGuard vào chuỗi kernel, đúng cái mà code gốc CỐ Ý không làm.
- Nặng hơn: bước 2 tự mâu thuẫn với chính artifact — §0 non-goal + §1 ô G + §4 bước 4 đều nói budget enforce ở tầng **discipline/loop, KHÔNG phải core**.

business/thi-cong cho 2 vì "mỗi bước gắn file đích, chỉ 2 seam" — đúng phần lớn, nhưng bỏ sót bước lệch-wiring này. ky-thuat bắt đúng → 1 là mức công bằng (rubric 4: "plan đúng ranh giới nhưng còn 1–2 bước… thừa/mơ hồ" = mức 1). Không tụt xuống 0 vì không có code app và không đẻ API ngoài contract.

### Bất đồng #2 — Tiêu chí 6, xương sống (business=1 vs ky-thuat/thi-cong=2)

Phân xử: **giữ 1** (không lên 2, không xuống 0). Tôi mở `safety/sandbox.py`:
- `wc -l` = **56 dòng** → anchor `:97` trỏ **quá cuối file, không tồn tại**.
- Dòng 38 nằm trong docstring của `_reject_foreign_path_syntax` ("treat every jail rejection uniformly"), KHÔNG phải jail-logic. Hàm thật `resolve_in_workspace` ở **:46**.
- Cụm gán ở §1 chặng 6 còn ghép "sandbox jail resolve_in_workspace → PolicyGate fail-closed" vào cùng anchor này, nhưng `grep` cả file: **không có PolicyGate trong sandbox.py** (chỉ có path-jail). PolicyGate/scope-check nằm chỗ khác.

→ business đúng: đây là anchor lệch-dòng-xa + một cấu phần (PolicyGate) gán sai file. ky-thuat/thi-cong cho 2 vì "sample ~15 anchor resolve đúng" — đúng cho 14 cái còn lại, nhưng cả hai KHÔNG kiểm riêng `sandbox.py` (ky-thuat thậm chí liệt nó trong nghi_bia nhưng vẫn để crit 6 = 2, tự-mâu-thuẫn nhẹ).

Vì sao KHÔNG kéo xương sống về 0 (rớt gate): rubric 6 phân mức 0 cho "claim bịa — anchor không tồn tại HOẶC code không nói điều được gán" và mức 1 cho "anchor mơ hồ / số dòng lệch xa". Ở đây cơ chế được mô tả (path-jail `resolve_in_workspace`) CÓ THẬT ở :46 ngay cạnh :38 — tức là lỗi định-vị-dòng + gộp-sai-file cho một cấu phần, không phải dựng một claim từ hư không. Đây đúng mô tả mức 1 ("số dòng lệch xa"). Một anchor lệch trong ~15 anchor đúng-semantic → 1, không 0. Gate: xương sống 1/3/6 = 2/2/1, không cái nào 0 → **đạt**.

---

## Nghi bịa / không nguồn — đã xác nhận

Gom nghi_bia của cả 3 lens, tự kiểm lại từng cái (mở đúng file/code viện dẫn). Kết quả:

1. **[ĐỨNG VỮNG — nhưng là LỖI mức-1, không phải bịa] Plan §4 bước 2 kê middleware chain có "BudgetGuard".**
   KIỂM: `bootstrap.py:28-32` — order thật timing→policy→retry→condense; dòng 31 "BudgetGuard is intentionally NOT wired here". `middleware/budget.py:10` có `class BudgetGuard` thật. → Là **lệch-wiring** (class có thật, đặt sai chỗ + tự mâu thuẫn §0/§4-bước-4), không bịa hoàn toàn. Đã phản ánh vào tiêu chí 4 = 1.

2. **[ĐỨNG VỮNG — LỖI mức-1] anchor `safety/sandbox.py:38,97`.**
   KIỂM: file 56 dòng → `:97` không tồn tại; `:38` là docstring; hàm thật `resolve_in_workspace` ở `:46`; PolicyGate không có trong file này. Dùng ở §1 chặng 6 + Plan bước 5 + bảng files §5. → Anchor lệch-dòng-xa + gộp-sai-file. Đã phản ánh vào tiêu chí 6 = 1.

3. **[ĐỨNG VỮNG — cảnh báo cho người đọc, KHÔNG hạ điểm] "GATE: GO" (§8) do chính AI tự cấp trong chế-độ-tự-quyết.**
   KIỂM: rubric 8 CHO PHÉP cổng tự-quyết = quyết định + lý do + phương án đã loại (không cần chữ ký ngoài). Artifact trung thực gắn nhãn "đóng vai Dev nhận slice". → Hợp lệ ở tầng frame; KHÔNG phải bằng chứng phê duyệt độc lập cho nhà đầu tư, nhưng cũng không bị tính là bịa. Không hạ tiêu chí 8.

4. **[ĐỨNG VỮNG một phần — chủ quan, KHÔNG hạ điểm] "chạm 6/7 lời hứa đắt nhất" + "rủi ro thấp".**
   KIỂM: "7 invariant" có nguồn thật (`REBUILD-BRIEF.md:28` "The 7 load-bearing invariants"). Con số "6/7 đắt nhất" và xếp hạng "đắt nhất" là phán đoán nội bộ không có tiêu chí đo. "Rủi ro thấp / mọi chặng có tiền lệ chạy ở gốc" ĐÚNG cho code gốc (anchor kiểm được) nhưng bản REBUILD chưa chạy dòng nào (`09-backlog.md:21` "Chưa dòng code rebuild nào chạy trên staging"; `08-skeleton.md:13,15` "0/9 ô tick THẬT trên bản rebuild"). → Đây là nhận định GÓC-NHÌN-LÃNH-ĐẠO có gắn ngữ cảnh ("đường đi đã chạy ở gốc"), không tick khống ô rebuild → không đủ để hạ tiêu chí 6 thêm (đã 1 vì anchor sandbox), nhưng ghi để CEO không đọc "rủi ro thấp" như đo-trên-bản-dựng-lại.

5. **[LOẠI — không đứng vững] "AC-5 anchor accept.py:52-128 là bịa".**
   KIỂM: `accept.py:52` = `def mu()`, `:101` = `def _implies()` (coverage), `:186` = `accept_decomposition`, `JACCARD_MAX=0.80` ở `:22`. Dải 52-128 trỏ đúng vùng μ+coverage; hàm cổng thật ở :186 (ngoài dải) → anchor **hơi lỏng nhưng KHÔNG bịa** (thi-cong tự đánh giá đúng: kế thừa từ backlog GĐ9). Không tính là lỗi hạ điểm.

6. **[LOẠI — không đứng vững] "SessionFactory.create / .restore lệch".**
   KIỂM: `session.py` có `create_root` (:119), `create_child` (:148), `restore` (:188). Artifact §1/Plan §2 viết "SessionFactory.create/.restore" — `create` là rút gọn của create_root/create_child, `restore` KHỚP tên thật. Cơ chế (scope-shrink child ⊆ parent, PermissionError ở :163) đúng. → Tên method rút-gọn nhẹ, không bịa; không đủ để thành lỗi riêng.

7. **[LOẠI — không đứng vững] "EventEmitter.emit / event_log.py:102".**
   KIỂM: `event_log.py:102` = `def attach_to_bus` (mirror kernel events vào log), `events.jsonl` set ở `:55`. Semantic emit-gate→seq→redact→fan-out + append jsonl đúng khớp; tên/dòng lệch nhẹ nhưng trỏ đúng vùng logger. → Không bịa.

Kết: sau kiểm, **2 lỗi thật đứng vững** (BudgetGuard-in-chain → tiêu chí 4; anchor sandbox.py:38,97 → tiêu chí 6), đã phản ánh vào điểm. Các nghi_bia còn lại là anchor-lỏng-nhưng-đúng-vùng hoặc nhận-định-chủ-quan-có-ngữ-cảnh — không phải claim bịa, không kéo tiêu chí xương sống về 0.
