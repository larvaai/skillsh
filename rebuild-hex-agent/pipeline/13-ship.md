# 13 — Ship: Go/No-Go + Runbook + Rollback + Rollout — HexAgent (clean rebuild)

> Skill `ship` · Giai đoạn 13 (SHIP — Release Readiness & Rollout). Nhận **Test & Verification Report GĐ12** (`pipeline/12-uat.md`: 28/28 AC lõi có test · 26 PASS · 2 PENDING · 0 FAIL · UAT ✔ + Security ✔ KÝ-CÓ-ĐIỀU-KIỆN 2026-07-02) + **Delivery Standards GĐ11** (`pipeline/11-delivery.md`: feature flag `write_tools_enabled`/`delegation_enabled`/`rag_enabled` · rollback = tắt flag + event-log replay · migration SQLite forward-only + rollback script) + **Live Slice GĐ8** (`pipeline/08-skeleton.md`: đường đi E2E + SPIKE-1 resume) + **Modules GĐ10** (on-call theo owner module).
> Anchor gốc: `00-understanding/REBUILD-BRIEF.md` (7 invariant) + `evidence-A/B/C` + `ATLAS.md`. KHÔNG kiểm lại chất lượng test (đó là `/uat`), KHÔNG viết code tính năng (đó là `/frame`), KHÔNG dựng ops dashboard dài hạn (đó là `/operate`).
> Chế độ tự-quyết: cổng GO/NO-GO do người viết đóng vai **CTO + PO (ký GO/NO-GO)** tự quyết, ghi rõ lý do + phương án đã loại. Không hỏi user. `ship` chuẩn bị đủ + khuyến nghị; KHÔNG kiểm lại test.

---

## ── GÓC NHÌN LÃNH ĐẠO (đọc trước, 90 giây — không cần biết code) ──

**Một câu.** Ta cho lên **theo release, có cổng, có đường lùi tức thì** — KHÔNG bật 100% một phát. Bản này ship phần đã chứng minh chạy đúng (nền R1: chokepoint · discipline · observability · replay-determinism), còn hai hành vi nguy hiểm nhất (ghi file thật · giao-việc multi-agent) **để sau flag, chỉ mở khi test ranh giới xanh trên staging**. Nếu hỏng: **tắt một biến cấu hình (`features.yaml`) là quay lại trạng thái an toàn trong vài giây** — không cần redeploy, không mất run đang chạy, không mất dữ liệu.

**Ba điều CEO/CTO nhìn để bấm GO.**

| # | Điều lãnh đạo nhìn | Kết quả |
|---|---|---|
| 1 | **Sẵn sàng lên chưa?** | **CÓ — cho pha nội bộ (alpha).** 12/12 dòng Go/No-Go có owner + trạng thái (nhiều dòng N/A hợp lệ vì hệ single-node, chưa có UI/prod). Bốn thứ chặn đều xanh: rollback đã-đặt-và-test-được-trên-staging · monitoring (events.jsonl + 6 metric loop) bật · incident owner có tên (Team Platform) · UAT ✔ + Security ✔ từ GĐ12 (ký-có-điều-kiện). |
| 2 | **Ký cái gì?** | Ký **GO cho rollout theo bậc, bắt đầu ở alpha nội bộ (smoke offline)** — KHÔNG phải ký "full production". Mỗi bậc kế (pilot → beta → gradual → full) là một cổng nhỏ, chỉ mở khi flag tương ứng đủ điều kiện. **Không ký mở `write_tools_enabled`/`delegation_enabled` ở bản này** — hai flag đó có điều kiện chặn từ Security GĐ12 (redact-raw-args + scope-property phải xanh trước). |
| 3 | **Hỏng thì lùi ra sao + ai trực?** | **Tắt flag qua `features.yaml` → vài giây về an toàn.** State = SQLite per-run + event-log **bất biến (append-only)** → rollback KHÔNG xoá lịch sử: run đang chạy giữ nguyên, run mới đi theo cấu hình đã lùi; điều tra bằng replay event-log tại đúng seq. **Trực:** Team Platform (chokepoint/session/resume) · Team Safety (jail/policy) · Team Observability (rò secret/audit). |

**Một điều CTO/PO phải nhớ.** Sản phẩm bán **niềm tin rằng agent chỉ báo-xong khi thật xong, không đốt tiền vô hạn, không leo quyền**. Vì vậy đường-lùi ở đây KHÔNG phải "rollback database" (nguy hiểm, dễ mất dữ liệu) mà là **pin version + không đụng run đang chạy + tắt flag hành vi nguy hiểm + resume/replay từ checkpoint** — an toàn vì event-log bất biến và SQLite là chân lý resume. Ta cố tình lên **dần từng loại task** (alpha smoke → pilot 1 loại task → beta nhiều loại → gradual) để mỗi bậc có tín hiệu số quyết định tiến/lùi, không đặt cược cả hệ vào một lần bật.

---

## ── CHI TIẾT KỸ THUẬT (cho dev) ──

### Nhận từ GĐ12 (uat) — nguồn chính (traceability đầu vào)

```
Từ 12-uat.md (đã qua cổng GĐ12, tự-quyết GO-CÓ-ĐIỀU-KIỆN):
  Pass    : 28/28 AC lõi có test · 26 PASS · 2 PENDING (R3 multi-agent + resume chưa chạy staging) · 0 FAIL
  UAT     : ✔ PO — KÝ CÓ ĐIỀU KIỆN (2026-07-02) — ký R1-PASS; M1/M2/M3 đầy đủ khi R3 xanh staging
  Security: ✔ CISO — KÝ CÓ ĐIỀU KIỆN (2026-07-02) — D1 PASS; BLOCKER: (1) redact-raw-args xanh trước bật write-tool
            (2) D2 scope-property xanh trước bật delegation
  Gap bị giấu: KHÔNG. 2 PENDING = trạng thái thật "chờ code R3/resume chạy", có địa chỉ (SPIKE-1/D3 · ADR-006/D4).
```
> `ship` KHÔNG kiểm lại các con số này — nhận nguyên từ GĐ12. Hai chữ ký ký-có-điều-kiện → điều kiện của chúng trở thành **rollout gate** và **rollback trigger** ở dưới, KHÔNG bịa "đã ký vô điều kiện".

---

## 1) GO/NO-GO CHECKLIST — 12 ô (owner · trạng thái · ô không dùng ghi N/A + lý do)

> Đủ-là-đủ: hệ quan trọng (đụng token/tiền · scope/quyền · secret · resume) NHƯNG **slice nội bộ single-node, chưa có UI/prod, chưa expose public** → nhiều ô N/A hợp lệ (ghi lý do, KHÔNG xoá). Bốn thứ chặn giữ nguyên trạng thái thật.

| # | Hạng mục | Owner | Trạng thái |
|---|---|---|---|
| 1 | **Release note** | Release manager | `[x]` "R1-nền + phanh runtime; write-tool/delegation OFF sau flag" (nội bộ, 1 trang) |
| 2 | **Deployment plan** | Team Platform | `[x]` CD trunk-xanh → staging tự động (`run_smoke.py` offline deterministic + E2E slice); prod = pha sau |
| 3 | **Rollback plan (đã test nếu hệ quan trọng)** | Team Platform | `[x]` tắt flag qua `features.yaml` + pin version + không đụng run đang chạy + resume/replay; **test rollback = smoke offline dựng lại được** (§2) |
| 4 | **Data migration plan** | Team Platform | `[x]` SQLite/`AgentState` schema forward-only + `schema_version` + rollback script; resume tương thích ngược ≥1 version (GĐ11 §10). Bản alpha KHÔNG đổi schema → migration = N/A cho pha này, script sẵn cho pha có schema change |
| 5 | **Feature flag plan** | Team Platform | `[x]` `write_tools_enabled`=OFF · `delegation_enabled`=OFF · `rag_enabled`=OFF (default an-toàn-nhất, GĐ11 §9); đọc từ `config/features.yaml` runtime |
| 6 | **User communication** | PO | **N/A + lý do:** alpha NỘI BỘ (đội build + PO), chưa người dùng ngoài → comms = 1 tin nội bộ; bật lại khi tới pilot |
| 7 | **Training material** | PO | **N/A + lý do:** chưa có người dùng nghiệp vụ ở alpha; runbook §3 đủ cho dev trực; training khi tới beta có UI |
| 8 | **Support playbook** | Team Platform | `[x]` = Runbook §3 (start/inspect/resume) + Incident process GĐ11 §12 (on-call theo owner module) |
| 9 | **Monitoring dashboard + alert rule** | Team Observability | `[x]` events.jsonl + summary.json + 6 metric loop (`task_finished_total`, `task_blocked_total{reason}`, `false_finish_total`=0, `delegation_rejected_total{reason}`, `parse_error_total`, `budget_tripped_total`). ⚠️ **ngưỡng alert số (P95/error-rate) = OQ-1 chưa có** → theo dõi định-tính + `false_finish_total`>0 là alert cứng; số ngưỡng đo ở Operate GĐ14 |
| 10 | **Incident owner đã phân công** | — | `[x]` **Team Platform** (chokepoint/session/resume) · **Team Safety** (jail/policy) · **Team Observability** (rò secret/audit) — theo owner module GĐ10 |
| 11 | **UAT sign-off** | PO | `[x]` **✔ KÝ CÓ ĐIỀU KIỆN (2026-07-02)** — kéo từ GĐ12; ký R1-PASS, M1/M2/M3 đầy đủ khi R3 xanh staging |
| 12 | **Security sign-off** | CISO | `[x]` **✔ KÝ CÓ ĐIỀU KIỆN (2026-07-02)** — kéo từ GĐ12; D1 PASS; blocker redact-raw-args + scope-property → chuyển thành rollout gate của write-tool/delegation |

**Bốn thứ chặn (không thương lượng):** rollback ✔ đặt+test-được · monitoring/alert ✔ bật (ngưỡng-số OQ-1 treo, alert định-tính+false-finish có) · incident owner ✔ có tên · UAT+Security ✔ kéo từ GĐ12 (ký-có-điều-kiện, KHÔNG bịa vô-điều-kiện). → đủ điều kiện mở cổng cho **pha alpha**.

---

## 2) ROLLBACK PLAN — đường lùi (viết TRƯỚC khi lên)

> Nguyên tắc gốc (REBRIEF #1/#6, evidence-B §7): **state chỉ ở session + SQLite per-run là chân lý resume + event-log bất biến (append-only)**. → rollback KHÔNG rollback-database (dễ mất dữ liệu/phá resume) mà là **pin version + không đụng run đang chạy + tắt flag + resume/replay từ checkpoint**.

**3 câu bắt buộc:**

| Câu hỏi | Trả lời |
|---|---|
| **Tín hiệu nào thì lùi? (rollback trigger)** | (a) `false_finish_total` > 0 (báo-xong-khống — phá điểm bán M1) → **P1, lùi ngay**. (b) `delegation_rejected_total` bất thường hoặc phát hiện child-cap ⊄ parent lọt (leo quyền — M3) → lùi. (c) secret lọt `ui_payload`/jsonl (D4) → lùi + dừng flag write-tool. (d) resume re-emit `tool.requested` của bước đã done / checkpoint nửa-ghi (SPIKE-1 fail) → lùi flag liên quan. (e) budget/guard không cắt được runaway (M2) → lùi. ⚠️ ngưỡng P95/error-rate = **OQ-1** (chưa có số) → alert định-tính + 5 tín hiệu invariant ở trên là trigger cứng, số ngưỡng bổ sung ở Operate GĐ14. |
| **Lùi bằng cách nào?** | **Bậc 1 (config, <giây):** tắt flag trong `config/features.yaml` (`write_tools_enabled`/`delegation_enabled`/`rag_enabled` → OFF) → hành vi nguy hiểm ngừng ngay, KHÔNG redeploy. **Bậc 2 (version, phút):** pin lại version bản trước (redeploy bản cũ) nếu lỗi nằm ở code nền, KHÔNG chỉ ở flag. **Không đụng run đang chạy:** run in-flight giữ SessionIdentity + SQLite checkpoint riêng; cấu hình mới chỉ áp cho run MỚI → 0 state bleed (I2/I3). |
| **Dữ liệu sinh ra trong lúc lỗi xử lý sao?** | **Giữ nguyên, KHÔNG xoá** — event-log append-only là nguồn audit; điều tra bằng `build_snapshot(events)` replay tới đúng seq sự cố (deterministic theo seq, evidence-B §7v). Run lỗi → resume từ SQLite checkpoint cuối cùng cùng `run_id` (0 side-effect re-run, I10/I11) HOẶC đánh dấu BLOCKED và bỏ. Có schema change (pha sau) → chạy rollback-script forward-only theo GĐ11 §10; **point-of-no-return:** nếu đã migrate schema mà bản cũ không đọc được checkpoint mới → từ chối resume tường minh (KHÔNG re-run mù). |

**Đã test rollback?** `[x]` **Test được trên staging = smoke offline dựng lại từ config đã lùi** (`run_smoke.py` deterministic, không cần mạng — DoD S0 GĐ8) + kiểm tắt flag → capability write bị scope-check chặn fail-closed. Đây là rollback cho **config** (bậc 1) đã chứng minh được. ⚠️ Rollback **có schema-migration** (bậc có DB change) CHƯA áp vì bản alpha không đổi schema — script forward-only + rollback đã đặt ở GĐ11 §10, test khi tới pha có migration (open-Q mang sang).

**Lý do chọn cách này + phương án đã loại:**
- **Chọn tắt-flag + pin-version + resume-từ-checkpoint** vì đúng bản chất kiến trúc (event-log-first + SQLite-truth): lùi mà không phá lịch sử, không mất dữ liệu, không đụng run đang chạy.
- **Loại "rollback database / xoá bản ghi lỗi":** phá event-log bất biến (nguồn audit + replay) + rủi ro mất dữ liệu resume; với hệ mà "nghiệm-thu-bằng-bằng-chứng" là điểm bán, xoá evidence = tự bắn vào chân.
- **Loại "redeploy toàn bộ cho mọi sự cố":** chậm (phút thay vì giây), tăng MTTR; đa số sự cố ở đây là hành vi-nguy-hiểm-sau-flag → tắt flag là đủ và nhanh hơn.

---

## 3) RUNBOOK — cẩm nang thao tác cho dev trực (người khác làm theo được lúc nửa đêm)

> Ba khối đánh số: **DEPLOY → KIỂM-TRA-SAU-DEPLOY (smoke) → ROLLBACK**. Kiểu triển khai + lý do chọn ghi rõ. Lệnh dùng tên seam của bản rebuild (`orchestrator.run` / `orchestrator.resume` / `observability.inspect`), khớp façade gốc `orchestrator/loop.py:run()` [93-147] / `resume()` [217-273].

### A. DEPLOY — kiểu triển khai: **rolling qua flag (single-deployable)**

**Lý do chọn rolling-qua-flag** (loại blue-green/canary): hệ **single-node single-deployable** (modular monolith, GĐ6 ADR-005) — chưa có nhiều instance để blue-green tách hạ tầng; "canary theo % traffic" không áp vì chưa có traffic thật (nội bộ). Thay vào đó, **canary-theo-hành-vi**: deploy code nền một lần, rồi **mở dần hành vi nguy hiểm qua flag** (`features.yaml`) — đây là "canary" đúng cho hệ này (chia rủi ro theo capability, không theo % request).

```
1. Merge trunk xanh → CI chạy đủ gate: lint(no-BOM)→type→unit→property→integration(+resume D3)
   →audit-adversarial(D1/D4/D5+sandbox/policy)→contract→build. BẤT KỲ bước đỏ = KHÔNG deploy (GĐ11 §6).
2. CD deploy staging tự động (single-deployable).
3. Xác nhận config an-toàn-nhất trong config/features.yaml:
      write_tools_enabled: false      # gate ghi-file thật — chờ redact-raw-args xanh (Security blocker)
      delegation_enabled:  false      # gate multi-agent — chờ scope-property xanh (Security blocker)
      rag_enabled:         false      # Knowledge optional, YAGNI ở MVP (GĐ7)
   → Thứ tự bật flag: CHỈ bật khi rollout gate tương ứng xanh (§4). KHÔNG bật ở deploy.
```

### B. KIỂM-TRA-SAU-DEPLOY (smoke — phải XANH trước khi mở rộng)

> Mỗi dòng có "kỳ vọng thấy gì". Không xanh đủ → KHÔNG tiến bậc rollout, quay khối C.

```
1. START một run:   orchestrator.run(task="task 2 bước finish-by-evidence tối thiểu")
      Kỳ vọng: trả run_id; state stream tới terminal FINISHED (không BLOCKED/FAILED).
2. INSPECT run:      observability.inspect list            # liệt kê run gần đây
      Kỳ vọng: thấy run_id vừa tạo, status=FINISHED.
                     observability.inspect summary <run_id>  # đọc summary.json của run
      Kỳ vọng: tool_calls>0 · false_finish_total=0 · parse_error trong ngưỡng · budget_tripped=0.
3. ĐỌC event-log:    xem var/<run_id>/events.jsonl (seq order)
      Kỳ vọng: có tool.requested/completed của N1,N2 + delegation.finished (nếu delegation bật);
               seq monotonic GAP-FREE per-run; 0 secret trong ui_payload (D4 — grep SECRET_KEYS = [REDACTED]).
4. MỞ UI (read-only console):  GET /api/snapshot  (+ GET /api/stream SSE để xem live)
      Kỳ vọng: snapshot fold khớp terminal-status của run; UI chỉ đọc ui_payload (UI ⊥ core, ARC-1).
5. KIỂM resume:      kill process giữa chừng → orchestrator.resume(run_id=<run_id>)
      Kỳ vọng (SPIKE-1/D3): KHÔNG re-emit tool.requested của bước đã done · round_no liên tục ·
               không checkpoint nửa-ghi. ⚠️ Đây là điều kiện chặn ĐÓNG R1 — nếu chưa xanh, R1 chưa đóng.
```

**Ngưỡng "hỏng → rollback ngay" (khớp Rollback trigger §2):** `false_finish_total`>0 · secret lọt jsonl/ui_payload · child-cap ⊄ parent lọt · resume re-emit/nửa-ghi · guard không cắt runaway. Bất kỳ cái nào → khối C.

### C. ROLLBACK (khớp Rollback Plan §2 — ai bấm: dev trực = owner module liên quan)

```
1. TẮT FLAG (bậc 1, <giây):  sửa config/features.yaml → flag liên quan = false → reload config runtime.
      Ai bấm: Team Platform (nếu chokepoint/resume) · Team Safety (nếu jail/policy) · Team Observability (nếu secret).
      Kỳ vọng: hành vi nguy hiểm ngừng ngay; run MỚI theo config đã lùi; run ĐANG CHẠY giữ nguyên (0 bleed).
2. NẾU lỗi ở code nền (không chỉ flag) → PIN VERSION (bậc 2, phút): redeploy version trước qua CD.
3. GIỮ dữ liệu: KHÔNG xoá events.jsonl/SQLite. Điều tra: observability.inspect summary <run_id> +
      build_snapshot replay tới seq sự cố (deterministic). Run lỗi → resume cùng run_id HOẶC đánh BLOCKED.
4. Sự cố chạm invariant (false-finish/leo-quyền/rò-secret) = P1: dừng bật flag liên quan,
      thêm audit/property-test bắt đúng ca đó vào regression TRƯỚC khi bật lại (GĐ11 §12).
```

---

## 4) ROLLOUT STRATEGY — lên DẦN theo LOẠI TASK, mỗi bậc một cổng nhỏ

> Bậc thang chuẩn: **internal alpha → pilot → beta → gradual → full.** Ở hệ này "rollout theo %" không hợp (chưa traffic thật) → rollout **theo loại task + theo flag hành vi**. Mỗi bậc: ai/phạm vi · quan sát bao lâu · tín hiệu tiến/dừng · đường lùi.

| Bậc | Phạm vi (ai / loại task) | Flag bật | Quan sát | Tín hiệu TIẾN bậc kế | Tín hiệu DỪNG/LÙI | Đường lùi |
|---|---|---|---|---|---|---|
| **1. Internal alpha** | Đội build + PO · **smoke offline** (`run_smoke.py` deterministic) + task 2-bước finish-by-evidence | tất cả OFF (chỉ đọc/plan/judge trên tool an-toàn) | tới khi smoke xanh ổn định + SPIKE-1 resume xanh | smoke xanh · `false_finish_total`=0 · resume D3 pass a/b/c → **ĐÓNG R1** | smoke đỏ · false-finish>0 · resume re-emit | tắt run, sửa code nền (bản này = pha alpha) |
| **2. Pilot — 1 LOẠI task** | Nội bộ · **đúng một loại task** (vd "đọc→biến đổi→ghi kết quả" trên fs jail) | `write_tools_enabled`=ON **⟺** redact-raw-args (`TC-REDACT-RAWARGS-003`) xanh (Security blocker) | 1 loại task, đủ số lần chạy để thấy ổn định | 0 secret lọt jsonl · sandbox-escape=0 · budget cắt đúng · PO OK | secret lọt · escape jail · budget không cắt | tắt `write_tools_enabled` → về read-only |
| **3. Beta — NHIỀU loại task** | Nội bộ · nhiều loại task cần multi-agent (giao-việc thật) | `delegation_enabled`=ON **⟺** D2 scope-property (`TC-DELEGATE-SCOPE-001`) + finish-by-evidence + bounded-guards + μ-proof xanh trên bộ nghiệm thu (**M1/M2/M3 chứng minh thật → R3**) | nhiều loại task, theo dõi delegation | `delegation_rejected` chỉ khi đúng vi phạm scope · 0 leo quyền · M1/M2/M3 xanh | child-cap⊄parent lọt · leo quyền · false-finish | tắt `delegation_enabled` → single-agent |
| **4. Gradual** | Mở dần loại task + (khi có) người dùng nghiệp vụ; bật `rag_enabled` nếu cần Knowledge | rag_enabled ON tuỳ nhu cầu (health-gated, never raises) | theo mức tải tăng dần | metric loop ổn định qua các loại task · NFR-số baseline có (Operate) | metric xấu ở loại task mới | tắt flag loại task/rag đó |
| **5. Full** | Toàn phạm vi dự kiến (vẫn single-node nội bộ ở MVP; public transport = E21 R4 sau) | theo nhu cầu | vận hành liên tục | ổn định ở gradual + pentest/DAST khi có transport public | — | theo §2 |

**Đủ-là-đủ — vì sao đi từng bậc (không full ngay):** hệ đụng token/tiền · scope/quyền · secret · resume → **không dám bật hành vi nguy hiểm một phát**. Bậc chia đúng theo **flag hành vi** (write → delegation) khớp đúng 2 blocker Security GĐ12 → mỗi bậc mở đúng khi điều kiện chặn của nó xanh. **KHÔNG gộp bậc** vì mỗi flag là một ranh giới điểm-bán riêng (M3 leo-quyền ở delegation, D4 rò-secret ở write-tool). Bậc alpha smoke-offline là bậc rẻ nhất chứng minh nền + đóng SPIKE-1.

---

## 5) Tự soi trước khi chốt (bắt buộc — theo rubric)

1. **Lãnh đạo đọc RIÊNG khối đầu có biết "cho lên an toàn không, ký gì, hỏng thì lùi ra sao + ai trực"?** — CÓ: bảng 3 điều (sẵn sàng cho alpha · ký GO-theo-bậc không phải full-prod · tắt flag <giây + Team Platform trực) + "một điều phải nhớ" (lùi = pin version + không đụng run + tắt flag + resume, KHÔNG rollback DB). Không jargon.
2. **Người trực cầm Runbook + Rollback thao tác được không cần đoán?** — CÓ: §3 ba khối đánh số (deploy → smoke với "kỳ vọng thấy gì" từng bước → rollback ai-bấm), lệnh `orchestrator.run`/`resume`/`observability.inspect` + đọc events.jsonl/summary.json + mở UI; ngưỡng "hỏng→lùi" rõ.
3. **Đúng + đủ bốn artifact + 12 ô?** — CÓ: Go/No-Go (12 ô, mỗi ô owner+trạng thái, ô không dùng = N/A+lý do) · Rollback (tín hiệu+cách+dữ liệu+đã-test) · Runbook (deploy+smoke+rollback) · Rollout (5 bậc, mỗi bậc tín hiệu tiến/lùi).
4. **Bốn thứ chặn có mặt?** — CÓ: rollback đã-test (config bậc-1) · monitoring/alert bật (metric loop; ngưỡng-số OQ-1 treo minh bạch + false-finish alert cứng) · incident owner có tên (Team Platform/Safety/Observability) · UAT+Security **KÉO từ GĐ12** ký-có-điều-kiện (KHÔNG bịa vô-điều-kiện).
5. **Có tự bấm GO không?** — KHÔNG: §6 trình cổng cho Người duyệt CTO+PO; `ship` chỉ khuyến nghị kèm lý do + phương án đã loại. (Chế độ tự-quyết → đóng vai CTO+PO tự ký, ghi rõ.)

---

## 6) CỔNG GO / NO-GO (phân vai A5 — CTO + PO ký) + Bàn giao sang `operate`

**Câu hỏi cổng (doc GĐ13):** *"Đưa lên có an toàn không, và lên bằng cách nào để lỡ sai thì lùi được?"*

**Phân vai (A5):** **Release manager / Tech lead** (vai `ship`) trình đủ 4 artifact + khuyến nghị. **CTO + PO** ký GO/NO-GO. Chế độ tự-quyết (product owner: "không hỏi approval") → người viết đóng vai CTO+PO tự quyết, ghi rõ.

```
═══ CỔNG GO / NO-GO — hex-agent-rebuild · release "R1-nền + alpha nội bộ" ═══
Sẵn sàng : 12/12 dòng checklist có owner+trạng thái (6 N/A hợp lệ: comms/training chưa cần ở alpha nội bộ) ·
           rollback ĐÃ TEST (config bậc-1, smoke offline) · monitoring BẬT (events.jsonl+6 metric; ngưỡng-số OQ-1 treo) ·
           trực sự cố: Team Platform / Safety / Observability (theo owner module GĐ10)
Còn chặn : (theo release) — write_tools_enabled chờ redact-raw-args xanh · delegation_enabled chờ scope-property xanh ·
           ĐÓNG R1 chờ SPIKE-1/D3 resume xanh staging. → KHÔNG chặn pha ALPHA (alpha chạy read-only/smoke, mọi flag OFF).
Rollout  : bắt đầu ALPHA nội bộ (smoke offline) → pilot 1 loại task (khi write-flag xanh) → beta nhiều loại (khi delegation-flag xanh) → gradual → full
Khuyến nghị của ship : **GO cho pha ALPHA nội bộ** (rollout theo bậc); **KHÔNG mở write/delegation ở bản này** —
           vì (1) 4 thứ chặn xanh cho phạm vi alpha; (2) hai hành vi nguy hiểm để sau flag đúng 2 blocker Security GĐ12;
           (3) rollback tức-thì (tắt flag) đã test; (4) rollout theo bậc chia rủi ro theo flag hành vi.
→ Người duyệt (CTO + PO) quyết: GO / NO-GO?
════════════════
```

**Quyết định cổng (tự-quyết — đóng vai CTO + PO ký).**

**GATE: GO (cho pha ALPHA nội bộ, rollout theo bậc — KHÔNG mở write/delegation ở bản này).**
Ký: **CTO ✔ + PO ✔ (2026-07-02).**

**Lý do GO:** (1) Bốn thứ chặn xanh cho phạm vi alpha — rollback đã-test (config), monitoring bật, incident owner có tên, UAT+Security kéo từ GĐ12 (ký-có-điều-kiện). (2) Hai hành vi nguy hiểm nhất (write-tool, delegation) **để sau flag** khớp đúng 2 blocker Security GĐ12 → không mở cái chưa đủ điều kiện. (3) Rollback tức-thì bằng tắt flag qua `features.yaml` đã chứng minh trên smoke offline; event-log bất biến + SQLite-truth → lùi không mất dữ liệu, không đụng run đang chạy. (4) Rollout theo bậc-theo-flag chia rủi ro đúng ranh giới điểm-bán.

**Rollback trigger (điều kiện lùi sau khi GO — ghi rõ):** `false_finish_total`>0 · secret lọt jsonl/ui_payload · child-cap⊄parent lọt · resume re-emit/checkpoint nửa-ghi · guard không cắt runaway → tắt flag liên quan ngay (§2/§3C), P1 nếu chạm invariant.

**Điều kiện mở bậc kế (rollout gate — không phủ định cứng, có địa chỉ):**
- **Mở pilot (bật `write_tools_enabled`)** ⟺ redact-raw-args (`TC-REDACT-RAWARGS-003`) xanh · ai: Team Safety↔Observability · xong khi: test 0-secret-in-jsonl xanh trên staging.
- **Mở beta (bật `delegation_enabled`, release R3)** ⟺ D2 scope-property (`TC-DELEGATE-SCOPE-001`) + finish-by-evidence + bounded-guards + μ-proof xanh trên bộ nghiệm thu (M1/M2/M3 thật) · ai: Team Orchestration · xong khi: R3 xanh staging.
- **ĐÓNG R1** ⟺ SPIKE-1/D3 resume (`TC-RESUME-NOREPLAY-001`/`ATOMIC-002`/`SQLITE-TRUTH-003`) pass a/b/c xanh staging · ai: Team Platform · fail → phương án B (orchestrator tự viết resume, không đổi Standards).

**Phương án đã loại ở tầng cổng:**
- **(a) NO-GO tới khi 28/28 PASS-live + mọi flag mở** — *loại:* trộn vai GĐ13 với GĐ8/GĐ12 (code R3 + chạy staging là việc `/frame`); chặn cổng = nghẽn pipeline. Đúng cách = GO cho alpha (phạm vi đã đủ điều kiện) + đặt rollout gate có địa chỉ cho bậc sau, không phủ định cứng.
- **(b) GO full ngay, bật cả write + delegation** — *loại:* vi phạm 2 blocker Security GĐ12 (redact-raw-args + scope-property chưa xanh) → mở đúng 2 ranh giới rò-secret/leo-quyền khi chưa có test chặn = ký nhầm cho lên thứ không lùi-an-toàn. Chia bậc theo flag mới đúng.
- **(c) Rollback bằng rollback-database / xoá bản ghi lỗi** — *loại:* phá event-log bất biến (nguồn audit+replay) + mất dữ liệu resume; với hệ bán "nghiệm-thu-bằng-bằng-chứng", xoá evidence là tự phá điểm bán. Tắt-flag + resume-từ-checkpoint an toàn hơn.
- **(d) Blue-green / canary-theo-% cho "chuẩn"** — *loại:* single-node single-deployable chưa có nhiều instance / chưa traffic thật → blue-green thừa hạ tầng, canary-% không đo được. Canary-theo-hành-vi (mở dần flag) đúng cho hệ này.

```
═══ BÀN GIAO — hex-agent-rebuild · release "R1-nền + alpha" đã GO ═══
Đã lên   : pha ALPHA nội bộ (smoke offline + task finish-by-evidence tối thiểu) bắt đầu 2026-07-02.
           Runbook + Rollback: rebuild-hex-agent/pipeline/13-ship.md (§2 rollback · §3 runbook)
Đang trực sự cố : Team Platform (chokepoint/session/resume) · Team Safety (jail/policy) · Team Observability (secret/audit)
Monitoring/alert : events.jsonl + summary.json + 6 metric loop (task_finished/blocked/false_finish=0/delegation_rejected/
                   parse_error/budget_tripped). Alert cứng: false_finish_total>0. ⚠️ ngưỡng-số P95/error-rate = OQ-1 (đo ở Operate).
→ Vận hành, đo metric sau release, ĐÓNG VÒNG với Business Case GĐ1 (agent chỉ-báo-xong-khi-thật-xong, không-đốt-tiền,
  không-leo-quyền — đo bằng false_finish_total=0 · budget_tripped · delegation_rejected) + nạp roadmap kế: chạy /operate (GĐ14)
→ Rollout còn bậc sau chưa mở (pilot/beta): quay lại /ship khi rollout gate xanh (redact-raw-args → pilot; scope-property+M1/M2/M3 → beta)
→ Rollout gặp sự cố cần lùi: theo Rollback Plan §2 (tắt flag); sự cố lớn chạm invariant → /operate xử incident
→ Phát hiện gap chất lượng phải kiểm lại (R3/resume/redact chưa chạy xanh): quay về /uat (hoặc /review đào lỗi sâu) rồi /frame code
════════════════
```
*Chỉ liệt kê, KHÔNG tự chọn hộ user chạy skill nào tiếp.*

*Traceability:* GĐ13 **nhận** Test & Verification Report GĐ12 (28/28 AC lõi · 26 PASS · 2 PENDING · 0 FAIL · UAT ✔ + Security ✔ ký-có-điều-kiện + 2 blocker redact-raw-args/scope-property + điều kiện đóng R1 SPIKE-1/D3) + Delivery GĐ11 (flag `features.yaml` · rollback=tắt-flag+event-log-replay · migration forward-only) + Live Slice GĐ8 (E2E + SPIKE-1) + Modules GĐ10 (on-call theo owner). **Sinh** trang SHIP 4-trong-1: Go/No-Go 12 ô · Rollback (pin-version+không-đụng-run+tắt-flag+resume, event-log bất biến) · Runbook (`orchestrator.run`/`resume` · `observability.inspect list/summary` · events.jsonl/summary.json · UI `/api/snapshot`+`/api/stream`) · Rollout 5 bậc theo flag. **Bàn giao** `/operate` (chính — đo false_finish/budget/delegation-rejected đối chiếu target GĐ1) · `/ship` lại khi mở bậc pilot/beta · `/uat`+`/frame` khi còn gap. Sợi liền hai đầu: ngược (sign-off+blocker GĐ12 → rollout gate + rollback trigger) + xuôi (metric loop → Operate đo target GĐ1). Ẩn số treo có địa chỉ: SPIKE-1/D3→đóng R1, redact-raw-args→pilot, scope-property+M1/M2/M3→beta, OQ-1 NFR-số→Operate, pentest/DR→sau transport public E21 R4.
