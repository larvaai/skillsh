CHẤM: 00-atlas · /Users/uspro/Desktop/skillsh/rebuild-hex-agent/00-understanding/ATLAS.md

1. BẰNG CHỨNG — [0] — nhiều anchor/invariant/con số SAI với code gốc và trình bày như fact: "15 SECRET_KEYS" (code=14), anchor freeze `bootstrap.py:28-53` (thực là `_install_middleware`; freeze ở `kernel.py:91`), invariant "ui/ NO imports from core" (bị `ui/server.py:21` bác), middleware order gắn [BOUNDARY] runtime nhưng sai wiring thật.
2. TRACE — [2] — §7 đi trọn vòng đời task, đủ 4 loại luồng (happy=execute_tool; failure=parse→FAILED/no-progress→BLOCKED; side-effect=event/jsonl/checkpoint; permission=scope⊆parent+redact), từng bước có nhãn STATE/SIDE-EFFECT/BOUNDARY và đi lại trên code gốc khớp mắt xích.
3. DÙNG ĐƯỢC THẬT — [2] — trả đủ 3 câu hợp đồng (bài toán §1, luồng §7, change-impact §11 "sửa X→kiểm Y+risk"), §15 chỉ đích danh stage tái dùng mục nào, §12 unknown có cách verify + priority.
4. ĐỦ BỘ MỘT LƯỢT — [2] — §1–§15 phủ đủ metadata→domain→contracts→flows→side-effects→security→test→risks + scorecard §14 + traceability §15; lệch form 20-file được khai báo mapping + lý do ở "Quyết định cổng".
5. TÁCH BIẾT / CHƯA BIẾT — [2] — nhãn độ-chắc nhất quán, §12 tách risks (có evidence) khỏi unknowns (mỗi cái có lý do+cách verify+priority), nói thẳng "chắc theo evidence ≠ re-read code gốc".
6. ĐÚNG VAI ATLAS — [2] — thuần bản đồ + bằng chứng + rủi ro; không dạy theo mức người (explain), không phán số phận file (triage), không đề xuất code sửa (frame); việc vượt vai chỉ ở open-Q/handoff §15.
7. TƯƠI & CẬP NHẬT ĐƯỢC — [1] — có built_at + scope + drift/handoff §15, NHƯNG neo phiên bản sai: header ghi "built_commit: n/a (không phải git repo)" trong khi nguồn LÀ git repo (HEAD 63d5029, 2026-06-29) và không có drift ledger/quy tắc bump.

TỔNG: 11/14
GATE: rớt: tiêu chí 1 (BẰNG CHỨNG, xương sống) = 0 — có claim sai với code gốc trình bày như fact, dù tổng 11 vẫn rớt vì atlas là NỀN mọi stage sau xây lên.
SỬA TRƯỚC TIÊN: Truy mọi con số/anchor/invariant về CODE GỐC thay vì copy từ evidence — sửa 15→14 SECRET_KEYS, neo freeze về `core/kernel.py:91` (bỏ `bootstrap.py:28-53`), thu hẹp invariant "UI ⊥ core" cho đúng (`ui/server.py:21` import `create_kernel`), đánh dấu middleware order là mô-tả-ý-định chứ không phải wiring runtime (BudgetGuard KHÔNG wire ở bootstrap), và ghi built_commit=63d5029 + thêm drift ledger.

---

## Phần 2 — Bảng tiêu chí × 3 lens + phân xử bất đồng

| # | Tiêu chí | ky-thuat | business | thi-cong | Hợp nhất | Ghi chú phân xử |
|---|---|---|---|---|---|---|
| 1 | BẰNG CHỨNG (xương sống) | 0 | 1 | 1 | **0** | Lấy điểm thấp nhất; TỰ KIỂM khẳng định lens 0 đúng (xem dưới). |
| 2 | TRACE (xương sống) | 2 | 2 | 2 | **2** | Đồng thuận; đi lại trace trên code gốc khớp. |
| 3 | DÙNG ĐƯỢC THẬT (xương sống) | 2 | 2 | 2 | **2** | Đồng thuận. |
| 4 | ĐỦ BỘ MỘT LƯỢT | 2 | 2 | 2 | **2** | Đồng thuận. |
| 5 | TÁCH BIẾT/CHƯA BIẾT | 2 | 2 | 2 | **2** | Đồng thuận. |
| 6 | ĐÚNG VAI ATLAS | 2 | 2 | 2 | **2** | Đồng thuận. |
| 7 | TƯƠI & CẬP NHẬT | 1 | 1 | 1 | **1** | Đồng thuận; neo commit sai + thiếu drift ledger. |
| | **TỔNG** | 11 | 12 | 12 | **11** | |
| | **GATE** | rớt | đạt | đạt | **rớt** | |

**Bất đồng đáng chú ý #1 — tiêu chí 1 (0 vs 1) → quyết định gate.**
- ky-thuat chấm 0 theo luật rubric "một claim bịa là đủ → 0". business/thi-cong chấm 1, lý luận rằng con số "15" và "327" truy được về evidence file (nguồn thứ cấp) nên không tính "bịa" mà chỉ là "chỗ suy đoán trình bày như fact".
- Phân xử: GIỮ điểm thấp nhất (0). Rubric §1 chốt chuẩn đối chiếu là **code gốc**, không phải evidence. Mức 0 định nghĩa: "file/symbol/dòng/hành vi không tồn tại hoặc **sai bản chất khi đối chiếu code gốc**". Đây KHÔNG chỉ là con số sai; có anchor trỏ code không chứa hành vi (`bootstrap.py:28-53`→_install_middleware, không phải freeze) và invariant kiến trúc SAI (`ui/ NO imports from core` bị `ui/server.py:21` bác). Đó là "sai bản chất", không phải "khái quát ~N". Mức 1 chỉ dành cho "còn 1–2 chỗ suy đoán/khái quát" — không phủ trường hợp anchor + invariant + số đều sai. Vậy 0 đúng.
- Việc con số truy về evidence-B (nói 15) không cứu được: rubric mức 2 đòi "dùng nguồn thứ cấp thì khai báo rõ là thứ cấp và hạ độ chắc"; ATLAS §4/§6/§9 in "15" như fact chắc chắn, không hạ độ chắc riêng cho con số → không đạt cả mức 2 lẫn mức 1 khi kèm 3 anchor/invariant sai bản chất khác.

**Bất đồng #2 — GATE tổng (rớt vs đạt).** business/thi-cong tuyên "đạt" vì chấm tiêu chí 1 = 1. Vì hợp nhất kéo tiêu chí 1 về 0 (xương sống), gate = **rớt** theo luật rubric ("bất kỳ xương sống = 0 → rớt gate dù tổng cao").

---

## Phần 3 — Nghi bịa / không nguồn — đã xác nhận

**1. "15 SECRET_KEYS" (§4 bất biến #7, §6 Bước 6, §9) — SAI, giữ vững.**
Code gốc `control/redaction.py:16-33` (HEAD 63d5029) đếm đúng **14 key**: api_key, apikey, authorization, password, passwd, secret, secret_key, client_secret, token, access_token, refresh_token, private_key, set-cookie, cookie. Evidence-B nói "15 SECRET_KEYS", evidence-C:47 nói "Redactor 14-key mask" (hai nguồn thứ cấp mâu thuẫn); ATLAS chọn con số SAI và in như fact 3 lần không hedge.

**2. Anchor freeze `core/bootstrap.py:28-53` (§1 evidence, §4 invariant #1, §7 Bước 0) — SAI VỊ TRÍ, giữ vững.**
`bootstrap.py:28-53` thực chất là hàm `_install_middleware` (docstring ghi rõ). `freeze()` định nghĩa ở `core/kernel.py:91`, gọi ở `core/session.py:141` và `:195`. Hành vi freeze CÓ THẬT nhưng anchor trỏ nhầm đoạn code, lặp 3 lần → "dòng không chứa hành vi được claim" = sai bản chất theo rubric §1.

**3. Invariant "UI ⊥ core/, ui/ NO imports from core" (§2 ARC-1, §3 module UI) — SAI, giữ vững.**
`ui/server.py:21` làm `from core.bootstrap import create_kernel`; `ui/ide/runner.py:126` cũng `from core.bootstrap import create_kernel`. Invariant kiến trúc "chống lưng lãnh đạo" bị chính nguồn bác. Chỉ đúng nếu giới hạn ở front-end/read-model, không phải cả thư mục ui/.

**4. Middleware order "Timing→PolicyGate→BudgetGuard→Retry→Condense→core" gắn [BOUNDARY] runtime (§7 Bước 5) — SAI, giữ vững.**
`bootstrap.py:28-53` wire thực tế = timing→policy→retry→condense (4 món) và GHI RÕ "BudgetGuard is intentionally NOT wired here: its same-tool counter is per-run… wire it per run instead." ATLAS thêm BudgetGuard vào chuỗi kernel-lifetime và trình bày như thứ tự runtime thật → sai wiring.

**5. "built_commit: n/a (không phải git repo)" (header) — SAI, giữ vững (rơi vào tiêu chí 7, không đủ để bịa tiêu chí 1 nhưng vẫn là claim sai sự thật).**
`/Users/uspro/Desktop/namnson/hex_agent/.git` tồn tại; HEAD = `63d5029e4acf120d947d50353e00d4c782b71fae` (2026-06-29 23:11:45 +0700). Lý do bỏ neo phiên bản là sai sự thật; có hash truy được nhưng artifact tự phong "không có".

**6. "~327 tests" (§10) — KHÔNG tính bịa (truy được nguồn), nhưng lệch nặng — ghi nhận.**
Truy về evidence-C:25 "(327 tests)" nên không phải bịa. Nhưng code gốc có **1041** `def test_` trên **88** file test/tests_audit — lệch ~3×. ATLAS bê số stale từ nguồn thứ cấp, chỉ hạ độ-chắc "một phần" cho *nội dung* test chứ không cho *con số*.

**7. "~50 event / 16 command" (§6, §12) — TRUNG THỰC, không tính bịa.**
`config/runtime_event_types.yaml` có **57** event type (ATLAS hedge "~50" và đưa vào §12 unknowns cần mở YAML để verify → dưới thực tế nhưng trung thực). `config/runtime_command_types.yaml` có đúng **16** command → khớp.

**8. Các tick ✓ / DoD gate (§10: E19 ✓, "0 secret in ui_payload", "no privilege escalation") — HỢP LỆ.**
Là ĐỊNH NGHĨA DoD bê từ evidence-C, ATLAS ghi "DoD gates" chứ không tuyên "đã PASS" → không phải kết-quả AI tự phong.

**9. GATE: GO của ATLAS (§Quyết-định-cổng) — ghi nhận, không nâng.**
Là quyết-định-nội-bộ AI tự đóng vai "Kiến trúc sư" tự cấp; không tính là bằng chứng giá trị/độ-tin (business lens nêu đúng). Không ảnh hưởng điểm ngoài việc củng cố rằng self-decide không thay được kiểm chứng anchor.

**Anchor spot-check ĐÚNG (để cân bằng — atlas KHÔNG bịa toàn bộ):** `core/kernel.py:106` execute_tool ✓; `delegation/policy.py:25-27` scope⊆parent ✓ (đúng cả line); `decompose_agent/node.py` FORBIDDEN_VERDICT_KEYS ✓; supervisor trace anchors `_drive:157/163/164`, `run_round:218`, checkpoint-after-turn `graph.py:332`, `judge_acceptance:357` ✓; 16 command ✓. Nền trace vững — vấn đề nằm ở các con số/anchor/invariant copy-từ-evidence chưa truy về code.
