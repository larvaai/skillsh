```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Test & Verification Report" lấy từ prompt/file bạn đưa, CHƯA qua cổng GĐ12 (skill /uat).
- Rủi ro: (1) chưa truy vết ngược được về pipeline; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /uat trước để có "Test & Verification Report" đã qua cổng.
```

Project: `hex_agent` (multi-agent microkernel — mọi call qua `execute_tool`, delegation cửa riêng, SQLite là checkpoint-truth, chạy trên LangGraph). Release: **hex_agent rebuild (đề xuất tag `v2.0.0-rebuild`)**. Đây là hệ quan trọng — có **SQLite checkpoint mang state resume thật** (`orchestrator/checkpoint.py`, `supervisor/checkpoint.py`), nên rollback **phải test trước** và rollout **đi từng nấc**, không full một phát.

---

## GÓC NHÌN LÃNH ĐẠO — hex_agent rebuild v2.0.0

- **Sẵn sàng lên?** UAT đã qua (bạn xác nhận). Nhưng có **2 dòng chặn chưa ký**: UAT + Security sign-off của GĐ12 mình chưa cầm được bản chính (bạn mô tả "đã qua UAT", chưa có chữ ký CISO/PO trong state) → hiện là **NO-GO có điều kiện**, đủ điều kiện GO ngay khi 2 chữ ký về.
- **Ký cái gì?** Cho phép cắt traffic sang runtime rebuild theo pha, bắt đầu ở nội bộ, không mở 100% cho tới khi checkpoint-resume chạy sạch trên dữ liệu thật.
- **Hỏng thì sao + ai trực?** Tắt cờ trong `config/features.yaml`, trỏ lại binary/checkpoint cũ — **hệ cũ chạy song song nên lùi trong vài phút**. Điểm cần canh: **schema của SQLite checkpoint** (nếu rebuild đổi shape → đây là chỗ có thể "không lùi được", cần backward-decode). Trực sự cố: **Tech lead runtime (cần điền tên)**.

---

## 1) GO/NO-GO CHECKLIST (hạng mục · owner · trạng thái)

```
[x] Release note v2.0.0 (CHANGELOG.md đã có)          — owner: Release mgr
[x] Deployment plan (blue-green, xem Runbook)          — owner: Tech lead runtime
[ ] Rollback ĐÃ TEST trên staging                       — owner: Tech lead · CHẶN: chưa có bằng chứng test
[ ] Data migration plan — SQLite checkpoint schema      — owner: Tech lead · CHẶN nếu schema đổi (xác nhận forward+backward)
[x] Feature flag plan (config/features.yaml + delegation.enabled)  — owner: Tech lead
[N/A] User communication — N/A: hệ nội bộ/infra, không có end-user ngoài
[N/A] Training material — N/A: đội vận hành nội bộ, dùng docs/getting-started.md
[x] Support playbook (docs/reference/known-risks.md + runbook dưới)  — owner: Ops
[ ] Monitoring dashboard + alert — event_log/summary.json đã có; ALERT RULE chưa bật — owner: Ops · CHẶN
[ ] Incident owner đã phân công — CHƯA có tên · CHẶN
[ ] UAT sign-off — bạn nói "đã qua UAT" nhưng CHƯA có bản ký GĐ12 · CHẶN (kéo từ GĐ12)
[ ] Security sign-off — CHƯA CÓ (path-jail `safety/sandbox.py` + no-shell argv là điểm phải review) · CHẶN
```
Dòng đỏ = chưa được ký. CTO nhìn 10 giây: còn **5 dòng chặn thật** (rollback-test, monitoring-alert, incident owner, UAT, Security) + 1 dòng có điều kiện (migration).

---

## 2) ROLLBACK PLAN (viết TRƯỚC khi lên)

- **Tín hiệu lùi:** error rate > 2% hoặc P95 loop-latency vượt ngưỡng thường trong 10'; HOẶC **bất kỳ lỗi resume nào** từ checkpoint (đây là ngưỡng cứng — checkpoint là data-truth).
- **Lùi bằng cách nào:** tắt cờ trong `config/features.yaml` (và `delegation.enabled: false` nếu sự cố ở multi-agent) → redeploy binary "blue" cũ đang chạy song song. Vì mọi call qua `execute_tool` và delegation có chokepoint riêng, có thể **cắt riêng delegation** mà không hạ cả runtime.
- **Dữ liệu sinh ra lúc lỗi:** run mới ghi vào `var/agent_runs/<run_id>/` + `langgraph.sqlite`. Nếu rebuild **giữ nguyên schema checkpoint** → không mất gì, chỉ bỏ run dở. Nếu rebuild **đổi schema** → cần backward-decode script để đọc checkpoint mới bằng runtime cũ; **nếu không có script này thì đây là point-of-no-return** — phải xác nhận trước GO.
- *Lý do chọn tắt-flag thay rollback-DB:* checkpoint SQLite là truth cho resume, rollback DB thô rủi ro mất run đang chạy; tắt flag + blue-green giữ dữ liệu, nên loại phương án drop/recreate.
- **CHẶN:** cần dòng "đã test rollback trên staging ngày __ — PASS" (gồm test **resume một run từ checkpoint sau khi lùi**). Chưa có = NO-GO.

---

## 3) RUNBOOK (cho dev trực, thao tác được lúc nửa đêm)

**A. Deploy (blue-green — chọn vì cần zero-downtime cho run đang chạy; loại canary vì hệ chạy theo run/session rời rạc, blue-green sạch hơn):**
1. Dựng "green" song song "blue", `var/` riêng, trỏ cùng checkpoint store (hoặc bản sao read-only để test resume).
2. Bật cờ green ở `config/features.yaml`, giữ `blue` sống.

**B. Kiểm tra sau deploy (phải XANH trước khi mở rộng):**
3. `python run_smoke.py` → phải in `CORE_AGENT_SMOKE_OK`.
4. `python -m pytest` (offline) + suite `tests_audit/` → pass.
5. Chạy 1 task thật → `python -m observability.inspect summary latest` phải xanh; **kill giữa chừng rồi resume từ checkpoint** → run hoàn tất đúng (đây là smoke quan trọng nhất của hệ này).
6. Kiểm E21 control plane: transport/Control-Tower UI **vẫn pending** (known issue từ README) → xác nhận không chặn core runtime.

**C. Rollback (khớp Rollback Plan, ai bấm = Tech lead trực):**
7. Ngưỡng: error>2% / P95 vượt 10' / bất kỳ lỗi resume → tắt cờ green trong `features.yaml`, trỏ về blue.
8. Nếu schema đổi: chạy backward-decode trước khi blue đọc checkpoint mới.

---

## 4) ROLLOUT STRATEGY (lên dần, mỗi bậc một cổng)

Chọn **4 bậc** (bỏ pilot-group vì hệ nội bộ, gộp vào internal → beta):
- **Internal alpha** — đội runtime, vài run/ngày, 3–5 ngày. Tiến khi: smoke+resume sạch, 0 lỗi checkpoint. Lùi: tắt cờ.
- **Beta (một luồng workload thật, ~25%)** — 1 tuần. Tiến khi: error<1% + resume/checkpoint 0 lỗi + delegation chạy đúng depth/budget. Lùi: tắt cờ (+`delegation.enabled:false` nếu lỗi ở multi-agent).
- **Gradual (50%)** — vài ngày, canh P95 + tỉ lệ resume thành công.
- **Full (100%)** — khi gradual sạch một chu kỳ; blue giữ sống thêm 1 tuần rồi mới rút.
*Lý do có bậc, không full ngay:* đây là **lần đầu lên rebuild + đụng checkpoint mang state resume thật** → rủi ro dữ liệu, chia nhỏ.

---

## Tự soi (trước cổng)
- Lãnh đạo đọc đoạn đầu biết ký gì / hỏng lùi sao / ai trực — ✔ (trừ tên incident owner đang trống, đã ghi rõ là dòng chặn).
- Người trực cầm Runbook+Rollback thao tác được — ✔ có bước + ngưỡng cụ thể.
- Đủ 4 artifact + 12 ô — ✔ (2 ô N/A có lý do, không xoá).
- 4 thứ chặn: rollback-test ❌, monitoring/alert ❌, incident owner ❌, UAT+Security ❌ — **thiếu, không bịa "đã ký"**.
- ship có tự bấm GO không — không, chỉ khuyến nghị.

---

```
═══ CỔNG GO / NO-GO — hex_agent v2.0.0-rebuild ═══
Sẵn sàng: 5/12 dòng xong · rollback CHƯA test · monitoring alert CHƯA bật · trực sự cố CHƯA có tên
Còn chặn: rollback-test · monitoring/alert · incident owner · UAT sign-off · Security sign-off · (migration: xác nhận schema checkpoint có đổi không)
Rollout: internal alpha trước (chưa mở beta)
Khuyến nghị của ship: NO-GO (tạm) — vì thiếu 4 thứ chặn cứng; chọn NO-GO thay "GO vá sau" vì hệ có checkpoint mang state resume — lên mà chưa test lùi được thì rủi ro mất run thật, không audit ngược được.
  Để chuyển thành GO còn thiếu:
   · rollback-test (gồm resume-từ-checkpoint sau khi lùi) — ai: Tech lead runtime — xong khi: PASS trên staging
   · alert rule P95/error/lỗi-resume bật trên event_log — ai: Ops — xong khi: alert fire thử được
   · incident owner: điền tên Tech lead trực — ai: Eng mgr — xong khi: có tên + lịch trực
   · UAT + Security sign-off bản chính từ GĐ12 — ai: PO + CISO (path-jail + no-shell argv) — xong khi: có chữ ký
   · xác nhận SQLite checkpoint schema có đổi không; nếu đổi → backward-decode script — ai: Tech lead — xong khi: forward+backward chạy được
  → Đủ 5 mục trên thì GO internal alpha ngay.
→ Người duyệt (CTO + PO) quyết: GO / NO-GO?
════════════════
```

Khi 5 mục về đủ và CTO+PO ký GO, mình chốt ngày ký vào checklist rồi bàn giao:

```
═══ BÀN GIAO — hex_agent v2.0.0-rebuild đã lên ═══
Đã lên: internal alpha bắt đầu <ngày>   Runbook + Rollback: state/project/hex_agent/pipeline/ship.md
Đang trực sự cố: <owner>   Monitoring/alert: event_log/summary.json — theo dõi error<1%, P95 loop-latency, TỈ LỆ RESUME THÀNH CÔNG (ngưỡng: bất kỳ lỗi checkpoint = alert đỏ)
→ Vận hành, đo metric sau release, đóng vòng với Business Case (GĐ1): chạy /operate
→ Rollout còn beta/gradual/full chưa mở: quay lại /ship khi tới mốc mở pha kế
→ Gặp sự cố cần lùi: theo Rollback Plan (tắt cờ features.yaml → blue); sự cố lớn → /operate xử incident
→ Phát hiện gap chất lượng (vd E21 control plane còn pending gây lỗi): quay về /uat (hoặc /review đào sâu)
════════════════
```

Trước khi mình đưa ra khuyến nghị cuối cho CTO+PO: **SQLite checkpoint schema ở bản rebuild có đổi so với bản cũ không?** Câu này quyết migration là "N/A" hay là dòng chặn cứng cần backward-decode — nó là rủi ro lớn nhất của release này.

