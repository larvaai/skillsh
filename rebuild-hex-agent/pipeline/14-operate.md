# 14 — Operate: Ops Dashboard · Incident Process · Iteration Loop — HexAgent (clean rebuild)

> Skill `operate` · Giai đoạn 14 (LEARN — Operations & Measurement). Chặng CUỐI của pipeline Idea→Operate, cũng là chỗ vòng đời **đóng lại rồi mở lại** về `backlog` (GĐ9).
> Nhận **Go/No-Go + Runbook + Rollback + Rollout GĐ13** (`pipeline/13-ship.md`: GO cho pha ALPHA nội bộ · write/delegation OFF sau flag · rollback = tắt flag `features.yaml` · incident owner đã phân công · 6 metric loop + alert cứng `false_finish_total>0` · OQ-1 ngưỡng-số NFR treo) + **Backlog GĐ9** (`pipeline/09-backlog.md`: Business Objective M1/M2/M3 để Business đối chiếu + nơi vòng lặp kế đổ item về) + **Business Case GĐ1** (`ideas/hex-agent-rebuild.md`: M1 zero-false-finish gate · M2 bounded · M3 no-escalation · OQ-1 baseline chi phí/false-finish chưa có số).
> Anchor gốc: `00-understanding/REBUILD-BRIEF.md` (7 invariant) + `evidence-A/B/C` + `ATLAS.md` (§7 observability + §12 risk O-self-score = honor-system). KHÔNG code fix (đó là `/frame`), KHÔNG viết story roadmap (đó là `/backlog`), KHÔNG đào edge case từng dòng (đó là `/review`).
> Chế độ tự-quyết: cổng go/no-go do người viết đóng vai **CEO/CTO + PO (duyệt theo nhịp)** tự quyết, ghi rõ quyết định + lý do + phương án đã loại. Không hỏi user. `operate` LÀM artifact + trình cổng + đề xuất item; KHÔNG tự quyết đầu tư vòng kế, KHÔNG tự tuyên "đạt, dừng", KHÔNG tự chọn item lên roadmap hộ.

---

## ── GÓC NHÌN LÃNH ĐẠO (đọc trước, 90 giây — không cần biết code) ──

**Một câu.** Hệ vừa lên **alpha nội bộ** (mới chạy, tải thấp, mọi hành vi nguy hiểm còn tắt sau flag) — nên đây là dashboard để **đóng vòng với lời hứa CEO đã ký ở GĐ1**, chứ chưa phải bảng đo tải-cao. Ba lời hứa đắt nhất của sản phẩm — *agent chỉ báo-xong khi thật xong · không đốt tiền vô hạn · không leo quyền* — được đo bằng đúng ba con số máy (không phải cảm tính): `false_finish_total`, `budget_tripped_total`, `delegation_rejected_total`.

**Ba điều CEO/CTO nhìn để biết on-track.**

| # | Điều lãnh đạo nhìn | Kết quả (hôm nay) |
|---|---|---|
| 1 | **Cái CEO ký ở GĐ1 có thành sự thật chưa?** (M1 zero-false-finish) | **Chưa kết luận được — và đó là trạng thái ĐÚNG, không phải tin xấu.** Mục tiêu gốc M1 = **0 lần** agent báo FINISHED mà thiếu bằng chứng thật. Ở alpha, đường-đi đo đã bật (`false_finish_total`, alert cứng khi >0) nhưng **lõi multi-agent nơi M1 sống thật (R3) CHƯA build** (GĐ12: 2 PENDING) → chưa có đủ lượt chạy thật để tuyên "đạt". Số hiện `chưa có số production` — có địa chỉ đo, không bịa "đã đạt". |
| 2 | **Đội giao hàng có nhanh & an toàn không?** (DORA) | **Đang giao đều, nhưng baseline số CHƯA chốt (OQ-1).** Trunk-based + rollback-bằng-tắt-flag → kỳ vọng deploy-thường-xuyên và MTTR-thấp; nhưng 4 số DORA (lead time · deploy freq · CFR · MTTR) mới có *cách đo*, **số baseline đo chính ở đây** (OQ-1 kế thừa từ GĐ11/GĐ13). Điều CTO chắc chắn: **0 sandbox-escape · 0 secret rò `ui_payload`** (đã test smoke offline ở GĐ13). |
| 3 | **Hỏng thì ai trực, lùi ra sao?** | **Có người trực + lùi trong vài giây.** On-call theo owner module: Team Platform (chokepoint/session/resume) · Team Safety (jail/policy) · Team Observability (secret/audit) · Team Orchestration (loop/acceptance). Đường lùi = **tắt flag `features.yaml`** (từ GĐ13), event-log bất biến → điều tra bằng replay, không mất dữ liệu. 0 incident tính tới hôm nay. |

**Một điều CEO/CTO phải nhớ.** Dashboard này **cố tình đo lời-hứa-điểm-bán bằng số máy, không bằng lời**: M1 = `false_finish_total`, M2 = `budget_tripped_total`, M3 = `delegation_rejected_total{reason}`. Cái treo lớn nhất **không phải là hệ hỏng** mà là **hệ chưa chạy đủ thật** — R3 (multi-agent) và số NFR (OQ-1) chưa có → vòng kế đầu tư đúng vào việc *làm cho ba con số đó có dữ liệu thật* (đóng R3 + set ngưỡng NFR), không phải thêm tính năng mới. **Quyết định đầu tư vòng kế là của CEO/CTO — `operate` chỉ trình số + đề xuất, không tự chốt.**

---

## ── CHI TIẾT KỸ THUẬT (cho dev/Ops) ──

### Nhận từ GĐ13 (ship) + GĐ9 (backlog) + GĐ1 (idea) — nguồn chính (traceability đầu vào)

```
Từ 13-ship.md (đã qua cổng GĐ13 — GO cho pha ALPHA nội bộ, 2026-07-02):
  Release  : "R1-nền + alpha nội bộ" đã GO · write_tools_enabled=OFF · delegation_enabled=OFF · rag_enabled=OFF
  Monitoring: events.jsonl + summary.json + 6 metric loop; alert cứng false_finish_total>0
  Incident owner (đã phân công GĐ10): Team Platform · Team Safety · Team Observability · Team Orchestration
  Rollback : tắt flag features.yaml (<giây) → pin version (phút) → resume/replay từ SQLite; event-log bất biến
  Treo     : OQ-1 ngưỡng-số P95/error-rate/DORA-baseline chưa có → ĐO Ở ĐÂY (GĐ14); R3 (multi-agent) chưa build (2 PENDING)

Từ 09-backlog.md + ideas/hex-agent-rebuild.md (Business Objective gốc GĐ1 — Business đối chiếu THẲNG):
  M1 (gate) : zero false-finish = 0 lần FINISHED khi có AC thiếu evidence thật (all_accepted(), state.py:35-37)
  M2        : bounded = mọi task về terminal ≤ max_rounds (không runaway)
  M3        : no-escalation = 0 delegation scope con ⊄ cha (policy.py:25-26)
  OQ-1      : baseline chi phí/false-finish thực CHƯA có số → Operate đo, KHÔNG bịa
  Vòng kế đổ item về: 09-backlog.md (roadmap kế)
```
> `operate` KHÔNG dựng lại monitoring/owner/rollback — kế thừa nguyên từ GĐ13. Business metric đối chiếu THẲNG M1/M2/M3 GĐ1. Số chưa đo được → ghi `chưa có số` + cách lấy, KHÔNG bịa cho đẹp.

**Đủ-là-đủ (độ sâu theo rủi ro/ẩn số):** hệ này **đụng token/tiền · scope/quyền · secret · resume** (rủi ro cao) NHƯNG **mới alpha nội bộ, tải thấp, R3 chưa live, 0 incident** → giữ **đủ 3 artifact + 4 nhóm dashboard + đủ 4 DORA** (vì là hệ quan trọng), nhưng phần lớn con số ở trạng thái `chưa có số production` + cách lấy — đó là sự-thật, không phải thiếu sót. Incident process nêu quy trình + owner mặc định + 3 playbook cho đúng ba lỗ hổng honor-system/runaway/secret; KHÔNG phình post-mortem dài khi chưa có incident.

---

## 1) OPS DASHBOARD — 4 nhóm chỉ số, một màn hình (SỐNG, cập nhật mỗi nhịp review)

```text
OPS DASHBOARD — HexAgent (clean rebuild) · sau pha ALPHA nội bộ (release R1-nền, GO 2026-07-02)
────────────────────────────────────────────────────────────────────────────────────────────
▸ ĐỌC CHO LÃNH ĐẠO (1 dòng):
  Mục tiêu gốc GĐ1 = M1 zero-false-finish (0 báo-xong-khống) · M2 bounded · M3 no-escalation.
  Hiện: false_finish=0 trên smoke (CHƯA đủ lượt thật vì R3 chưa live) → CHƯA KẾT LUẬN "đạt" ·
        0 sandbox-escape · 0 secret rò ui_payload · 0 incident. → on-track cho ALPHA, chờ R3 để tuyên M1.
────────────────────────────────────────────────────────────────────────────────────────────
BUSINESS   (đối chiếu THẲNG mục tiêu gốc GĐ1 — đây là chỗ CEO biết cái mình ký có thành sự thật)
  • M1 Zero false-finish   : target = 0 · hiện false_finish_total = 0 trên bộ smoke/nghiệm thu-R1;
                             ⚠️ chưa số production (R3 multi-agent chưa live) → "đạt R1-nền, CHƯA tuyên M1"
                             — cách lấy: đếm false_finish_total qua các loại task thật sau khi mở beta (delegation ON).
  • M2 Bounded             : target = 100% task về terminal ≤ max_rounds · hiện budget_tripped_total đo được
                             trên smoke (guard cắt đúng); production `chưa có số` — cách lấy: budget_tripped_total / tổng-run.
  • M3 No-escalation       : target = 0 child-cap ⊄ parent lọt · hiện `chưa có số production` (delegation OFF)
                             — cách lấy: delegation_rejected_total{reason=scope} sau khi mở beta; alert nếu child-cap lọt >0.
  • Baseline chi phí (OQ-1): `chưa có số` — cách lấy: token/USD trung bình/task từ llm_calls × giá model, sau ≥1 tuần beta.
    → NỐI NGƯỢC GĐ1: cả 3 con số ↑ đối chiếu THẲNG M1/M2/M3 CEO đã ký; "đạt" chỉ tuyên khi có số production (sau R3).

PRODUCT    (người ta có dùng đúng cách không · flow nào drop · điểm bán có sống không)
  • % task đạt FINISHED    : target ≥ mức baseline (chốt sau beta) · hiện `chưa có số production`
                             — cách lấy: task_finished_total / (task_finished + task_blocked + task_failed).
  • Round trung bình/task  : `chưa có số` — cách lấy: trung bình round_no lúc terminal (từ summary.json mỗi run).
  • Tỉ lệ runaway-blocked  : target thấp & mọi runaway BỊ chặn (không có runaway lọt) · hiện `chưa có số`
                             — cách lấy: task_blocked_total{reason∈max_rounds/no-progress/repeat} / tổng-run.
  • Độ sâu decompose t.b.  : theo dõi < MAX_DEPTH(6) · hiện `chưa có số` — cách lấy: max depth cây kế hoạch/run (Journal/Tree).
  • Tỉ lệ AC pass lần đầu  : `chưa có số` — cách lấy: AC passed-lần-1 / tổng-AC (đo chất lượng plan; drop thấp = plan tốt).
    → Ở ALPHA (chỉ đội build + smoke), Product metric CHƯA có người-dùng-thật → mọi số `chưa có số`, có cách lấy khi beta.

ENGINEERING (DORA — giao hàng nhanh & an toàn? — bám observability gốc + 4 DORA)
  Observability gốc (evidence-B §7 · ATLAS §7 bước 6):
  • tool_calls · llm_calls           : `chưa có số production` — nguồn: summary.json/metrics (EventLogger observability/event_log.py:102)
  • parse_errors                     : theo dõi trong parse-budget (CONSECUTIVE, reset khi parse tốt) · nguồn: metrics
  • same_tool_blocks                 : đếm lần guard max_same_tool_calls chặn · nguồn: budget_tripped_total{reason=same_tool}
  • policy_blocks                    : đếm PolicyGate fail-closed chặn (tool ∉ allow) · nguồn: tool.failed{reason=policy}
  • tool_failures                    : đếm tool.failed (không phải policy) · nguồn: metrics failures
  DORA (delivery §12 đặt móc, số baseline ĐO Ở ĐÂY — OQ-1):
  • Lead time (commit→merge-xanh staging) : `chưa có số` (OQ-1) — nguồn: CI timestamp; kỳ vọng thấp (trunk-based)
  • Deployment frequency (lần/tuần)       : `chưa có số` (OQ-1) — nguồn: CD log; kỳ vọng cao (trunk-based, single-deployable)
  • Change failure rate (%)               : `chưa có số` (OQ-1) — nguồn: CI + incident log (% PR gây rollback/hỏng-CI-sau-merge)
  • Recovery time (MTTR)                  : `chưa có số` (OQ-1) — nguồn: incident process (§2); kỳ vọng thấp (rollback = tắt flag)

OPERATIONS (uptime · latency · incident · an toàn biên)
  • Uptime                 : target ≥ 99.9% (chốt lại khi có transport public) · hiện single-node nội bộ, `chưa có số` —
                             cách lấy: health-check smoke run định kỳ; alpha chưa có SLA public.
  • Resume success rate    : target = 100% resume 0-side-effect (SPIKE-1/D3) · hiện điều-kiện-chặn ĐÓNG R1 CHƯA xanh staging
                             — cách lấy: (resume không re-emit tool.requested bước đã done ∧ round_no liên tục ∧ không checkpoint nửa-ghi) / tổng-resume.
  • Sandbox-escape attempts: target = 0 · hiện = 0 (test smoke offline GĐ13 · TC-SANDBOX-ESCAPE-001) — alert cứng nếu >0.
  • Secret rò ui_payload/jsonl : target = 0 · hiện = 0 (redact 15 SECRET_KEYS · D4) — alert cứng nếu >0 (blocker write-tool).
  • P95 latency loop       : `chưa có số` (OQ-1) — cách lấy: đo thời gian round từ event timestamp; ngưỡng chốt sau beta.
  • Incident count         : 0 (tính tới 2026-07-02) — nguồn: §2 Incident Process.
  • Support tickets        : N/A ở alpha (chưa người-dùng-ngoài) — bật khi tới pilot/beta.
────────────────────────────────────────────────────────────────────────────────────────────
```

**Đủ-là-đủ + ngưỡng:** dashboard SỐNG (cập nhật mỗi nhịp review §3, không phải ảnh chụp một lần). Mỗi con số có **target/ngưỡng** để biết tốt-hay-xấu (không để trần); số chưa đo được ghi `chưa có số` + **cách lấy** đúng chỗ (không bỏ trống lặng lẽ). Ba nhóm đo được ngay ở alpha = **an toàn biên** (0 sandbox-escape · 0 secret) và **guard cắt đúng trên smoke**; ba nhóm treo tới beta = **Business production · Product người-dùng · DORA/NFR số** — vì hệ chưa chạy đủ thật, không phải bỏ sót.

**Lý do chọn 3 con số máy cho Business (+ phương án đã loại):**
- **Chọn** đo M1/M2/M3 bằng `false_finish_total` / `budget_tripped_total` / `delegation_rejected_total{reason}` vì ba số này **là chính điểm bán** và đo được bằng máy (evidence audit), không phải "chạy ổn" cảm tính.
- **Loại** "đo bằng khảo sát hài lòng người dùng ở alpha" — chưa có người-dùng-ngoài, số sẽ là bịa; để tới pilot/beta.
- **Loại** "tuyên M1 đạt vì smoke xanh" — smoke chỉ chứng minh nền R1, KHÔNG chứng minh M1 ở quy mô multi-agent (R3 chưa live) → tuyên đạt = báo-xong-khống ở tầng dashboard, tự phản lại điểm bán.

---

## 2) INCIDENT PROCESS — phát hiện → phân loại → owner → khắc phục → hậu kiểm

> Kế thừa NGUYÊN từ GĐ13/GĐ10: alert rule (metric loop), incident owner đã phân công, rollback = tắt flag + replay. `operate` KHÔNG dựng lại — chỉ nối thành quy trình 5 bước + 3 playbook cho ba lỗ hổng đặc thù của hệ này.

```text
INCIDENT PROCESS — HexAgent (clean rebuild)
  1. Phát hiện  : alert cứng từ metric loop (GĐ13 §9):
                  • false_finish_total > 0        → báo-xong-khống (phá M1) — P1
                  • child-cap ⊄ parent lọt / delegation_rejected bất thường → leo quyền (phá M3) — P1
                  • secret lọt ui_payload/jsonl   → rò bí mật (phá invariant #7, D4) — P1
                  • sandbox-escape attempt > 0    → thoát jail — P1
                  • guard không cắt runaway / budget_tripped bất thường → runaway (phá M2) — P1/P2
                  ⚠️ ngưỡng-số P95/error-rate = OQ-1 chưa có → alert định-tính + 5 tín-hiệu-invariant trên là trigger cứng.
                  Ai nhận đầu tiên: on-call owner module liên quan (bước 3).
  2. Phân loại  : SEV theo ảnh hưởng điểm-bán:
                  • SEV1 = chạm invariant điểm-bán (false-finish · leo-quyền · rò-secret · escape jail) — mọi cái này P1.
                  • SEV2 = runaway/budget bất thường không chạm invariant nhưng đốt token.
                  • SEV3 = lỗi vận hành cục bộ (parse-error tăng, resume lỗi 1 run) không lan.
                  Ảnh hưởng business: ai đau (đội dùng agent) · bao nhiêu run bị (đọc từ event log).
  3. Owner      : incident owner (ĐÃ phân công GĐ10/GĐ13) điều phối theo vùng:
                  • Team Platform      → chokepoint/session/resume (false-finish, checkpoint nửa-ghi, resume re-emit)
                  • Team Safety        → jail/policy (sandbox-escape, policy_blocks bất thường)
                  • Team Observability → secret/audit (secret rò ui_payload/jsonl, seq gap)
                  • Team Orchestration → loop/acceptance/delegation (leo quyền, judge honor-system, μ-proof)
                  Escalation: SEV1 → báo CTO + PO theo nhịp; SEV2/3 → owner module tự xử, ghi log.
  4. Khắc phục  : theo Runbook GĐ13 §3C — TẮT FLAG liên quan (features.yaml, <giây) trước → nếu lỗi code nền
                  thì PIN VERSION (phút). KHÔNG đụng run đang chạy (0 state bleed I2/I3). KHÔNG rollback-database
                  (phá event-log bất biến). Điều tra: build_snapshot(events) replay tới seq sự cố (deterministic).
                  MTTR đo từ phát hiện → khôi phục (feed vào DORA §1).
  5. Hậu kiểm   : post-mortem KHÔNG đổ lỗi → nguyên nhân gốc → action item VỀ Iteration Loop §3 → backlog GĐ9.
                  Chạm invariant (SEV1) = thêm audit/property-test bắt đúng ca đó vào regression TRƯỚC khi bật lại flag.
                  KHÔNG tự viết code fix ở đây — hậu kiểm ĐẺ action item cho /frame (code) hoặc /review (đào sâu).

  Incident hiện tại: 0 (tính tới 2026-07-02) — alert + owner + rollback đã SẴN SÀNG (kế thừa GĐ13, đã test smoke offline).
```

### Ba playbook cho ba lỗ hổng đặc thù (bám điểm bán + rủi ro honor-system GĐ atlas §12)

```text
PLAYBOOK A — "AC passed nhưng kết quả sai" (honor-system gap — rủi ro cao gốc, ATLAS §12)
  Triệu chứng : agent tuyên FINISHED, AC status=passed, nhưng kết quả thực SAI (O tự-chấm = honor-system,
                judge≠doer chưa tách hoàn toàn — evidence-C §4, A §4).
  Phát hiện   : false_finish_total > 0 KHÔNG bắt được ca này (evidence có mặt nhưng SAI, không phải THIẾU)
                → phát hiện qua reviewer/người-dùng báo "xong mà sai" HOẶC audit mẫu định kỳ trên evidence thật.
  Owner       : Team Orchestration (judge_acceptance/evidence) + Team Observability (audit evidence-type).
  Khắc phục   : KHÔNG rollback-DB. Đánh dấu run BLOCKED, giữ evidence để điều tra; nếu lan → tắt delegation_enabled
                về single-agent (giảm bề mặt honor-system).
  Hậu kiểm    : nguyên nhân gốc = evidence-type quá lỏng HOẶC thiếu verifier tách khỏi doer →
                action item VỀ backlog: "siết evidence types + thêm verifier độc lập" (E15 merged→E21, evidence-C §4).
                Đây là rủi ro ĐÃ ghi từ GĐ8/GĐ9 (R3 judge = honor-system một phần) — Operate chỉ ĐO + đẩy về backlog,
                KHÔNG tự sửa. (Không phủ định cứng: không nói "bỏ acceptance" — đề xuất SIẾT + thêm verifier.)

PLAYBOOK B — "runaway không bị chặn" (phá M2 bounded)
  Triệu chứng : một task chạy quá max_rounds mà không về BLOCKED, HOẶC budget_tripped không kích hoạt khi đáng lẽ phải.
  Phát hiện   : budget_tripped_total bất thường / task chạy lâu bất thường (thời gian round tăng vô biên) /
                same_tool_blocks không tăng dù lặp tool.
  Owner       : Team Platform (budget/guard ở discipline) + Team Orchestration (no-progress/repeat-decision guard).
  Khắc phục   : tắt flag loại-task gây runaway (nếu cô lập được) hoặc dừng run (StopAgentTurn) → về an toàn.
                Điều tra: replay event log tìm vòng lặp không-tiến-triển (artifacts không tăng ∧ acceptance không đổi).
  Hậu kiểm    : nguyên nhân gốc = guard nào KHÔNG cắt (max_steps enforce ở discipline chưa đúng — giả định GĐ8 đã đổi,
                F1.2-AC3) → action item VỀ backlog: "vá guard đúng tầng + thêm property-test cắt-đúng". 

PLAYBOOK C — "secret rò trong log" (phá invariant #7 redact-tại-biên · D4)
  Triệu chứng : SECRET_KEYS xuất hiện trong events.jsonl (raw args tool.requested, kernel.py:125) HOẶC ui_payload.
  Phát hiện   : alert cứng grep SECRET_KEYS ≠ [REDACTED] trên jsonl/ui_payload (test 0-secret — D4 · TC-REDACT-RAWARGS-003).
  Owner       : Team Observability (redact biên) + Team Safety (nếu qua write-tool).
  Khắc phục   : P1 — tắt write_tools_enabled NGAY (chặn thêm raw-args ghi ra); KHÔNG xoá jsonl đã ghi
                (event-log bất biến) nhưng cô lập file chứa secret + xoay khoá bị lộ theo quy trình secret.
  Hậu kiểm    : nguyên nhân gốc = redact-raw-args chưa bật TRƯỚC khi enable write-tool (điều kiện chặn GĐ11/GĐ13) →
                action item VỀ backlog: "bật redact-raw-args + test 0-secret-in-jsonl xanh làm rollout-gate pilot".
                Đây chính là Security blocker GĐ12 → Operate ĐO việc nó đã xanh chưa, không tự code.
```

**Đủ-là-đủ (Incident):** hệ quan trọng NHƯNG 0 incident + alpha → nêu quy trình 5 bước + owner mặc định + 3 playbook cho đúng ba lỗ hổng điểm-bán/honor-system (không phình SLA-từng-mức khi chưa có incident). SLA-phản-hồi-từng-SEV = `chưa cần` ở alpha, bật khi tới beta (nhiều loại task, delegation ON).

---

## 3) ITERATION LOOP — đóng vòng học → về backlog (GĐ9)

```text
ITERATION LOOP — HexAgent (clean rebuild)
  Nhịp review : 2 TUẦN (Ops/SRE + PO dự mỗi nhịp · CTO/CEO theo THÁNG hoặc khi có SEV1).
                Lý do 2-tuần (không tuần/không tháng — xem dưới).
  Học được (từ dashboard §1 + incident §2):
    • M1/M2/M3 CHƯA có số production vì R3 (multi-agent) chưa build (GĐ12: 2 PENDING) → không thể tuyên "đạt mục tiêu GĐ1".
    • Resume (SPIKE-1/D3) là điều-kiện-chặn ĐÓNG R1 CHƯA xanh staging → uptime/resume-success chưa chốt được.
    • OQ-1: baseline DORA + ngưỡng NFR-số (P95/error-rate) chưa có → dashboard nhiều ô `chưa có số`.
    • An toàn biên đã chứng minh (0 sandbox-escape · 0 secret) → nền vững để mở bậc pilot khi redact-raw-args xanh.
  Về backlog (1–3 item ưu tiên → roadmap kế GĐ9, mỗi item kèm LÝ DO = số/incident trỏ tới nó — CHƯA phân rã):
    [I-1] ĐÓNG R3 (multi-agent TaskLoop + Delegation + Acceptance) để có số M1/M2/M3 THẬT.
          Lý do: Business dashboard §1 — cả M1/M2/M3 `chưa có số production` vì R3 chưa live; đây là chỗ điểm-bán sống.
          Trỏ tới: backlog R3 (E09/E10, story ⭐ LÕI đã có AC) — traceability về GĐ9 sẵn.
    [I-2] ĐÓNG SPIKE-1/D3 resume (0 side-effect) để chốt uptime/resume-success rate.
          Lý do: Operations §1 resume-success = điều-kiện-chặn ĐÓNG R1 chưa xanh staging; fail → phương án B (GĐ7).
          Trỏ tới: backlog R1 F1.6 (story S1.6.1, 4 AC SPIKE-1) — không đổi cấu trúc backlog, chỉ task nội bộ.
    [I-3] SET baseline OQ-1 (4 DORA + ngưỡng NFR P95/error-rate) + bật redact-raw-args làm rollout-gate pilot.
          Lý do: DORA §1 + Operations §1 nhiều ô `chưa có số` = OQ-1 kế thừa GĐ11/GĐ13; playbook C cần redact xanh.
          Trỏ tới: đo tại Operate + đưa "bật redact-raw-args + test 0-secret" vào backlog như rollout-gate.
    (Ưu tiên gợi ý: I-1 ≈ I-2 (cùng chặn "tuyên đạt mục tiêu") > I-3 (đo/hạ-tầng). — CEO/CTO chốt thứ tự đầu tư.)
```

**Đủ-là-đủ + đường về backlog RÕ:** mỗi item [I-1..I-3] truy được về **một chỉ số `chưa có số`/điều-kiện-chặn cụ thể** trong dashboard, và trỏ thẳng vào **backlog GĐ9** (R3 story ⭐ đã có AC / R1 F1.6 / OQ-1). `operate` KHÔNG viết story (đó là `/backlog`) — chỉ liệt kê item + lý do. Đây là vế "cải tiến" KHÔNG được bỏ: thiếu nó thì dashboard chỉ để ngắm.

**Lý do chọn nhịp review 2 tuần (+ phương án đã loại):**
- **Chọn 2 tuần** vì hệ mới alpha, thay đổi nhanh (đang đóng R1/R3), có metric mới liên tục → nhịp 2-tuần đủ dày để bắt drift sớm mà không họp-quá-nhiều khi chưa có tải-thật.
- **Loại nhịp tuần** — quá dày cho hệ tải-thấp 0-incident, tốn thời gian đội build đang code R3; để dành khi beta có tải thật.
- **Loại nhịp tháng** — quá thưa khi đang đóng R1/R3 và số production còn trống; drift (vd resume fail, secret rò) sẽ phát hiện muộn.

---

## 4) Tự soi trước khi chốt (bắt buộc — theo rubric)

1. **Lãnh đạo đọc dòng ĐỌC-CHO-LÃNH-ĐẠO + "Góc nhìn lãnh đạo" của cả 3 artifact có nắm on-track không, không cần hỏi dev?** — CÓ: 3 điều (M1 chưa-tuyên-được-vì-R3-chưa-live nhưng đúng trạng thái · DORA baseline OQ-1 nhưng 0-escape/0-secret chắc · có người trực + lùi vài giây); Incident 1 dòng "0 incident, alert+owner+rollback sẵn"; Iteration 1 câu "chưa đạt vì R3/resume/NFR treo, 3 việc kế". Không jargon ở tầng lãnh đạo.
2. **Nhóm BUSINESS NỐI NGƯỢC được về con số mục tiêu gốc GĐ1 không?** — CÓ: M1/M2/M3 trong Business đối chiếu THẲNG M1/M2/M3 GĐ1 (`ideas/hex-agent-rebuild.md`), mỗi cái có target + số hiện + cách lấy; "đạt" chỉ tuyên khi có số production — không đo lơ lửng.
3. **Đủ 3 artifact (Dashboard 4 nhóm + DORA đủ 4 · Incident đủ 5 bước · Iteration có đường về backlog)?** — CÓ: Dashboard Business/Product/Engineering[DORA 4]/Operations; Incident phát-hiện→phân-loại→owner→khắc-phục→hậu-kiểm + 3 playbook; Iteration nhịp 2-tuần + 3 item trỏ backlog GĐ9.
4. **Mỗi con số có nguồn thật, không bịa? Số chưa có đã ghi `chưa có số` + cách lấy?** — CÓ: số đo-được (0 sandbox-escape, 0 secret, false_finish=0-trên-smoke) gắn nguồn (test GĐ13/summary.json); số chưa có (M1 production, DORA, P95, %FINISHED…) ghi `chưa có số` + cách lấy + OQ-1. KHÔNG bịa "đã đạt M1".
5. **Dev/Ops có đủ để hành động?** — CÓ: biết alert nào (metric loop), ai owner (4 team theo vùng), DORA đo ở đâu (CI/CD/incident), item nào vào vòng kế (I-1..I-3 trỏ backlog), playbook cho 3 lỗ hổng.

---

## 5) CỔNG GO/NO-GO (phân vai A5 — CEO/CTO + PO duyệt theo nhịp) + Bàn giao sang `backlog`

**Câu hỏi cổng (doc GĐ14):** *"Đạt mục tiêu chưa? Làm gì tiếp?"* → mở vòng lặp mới tại GĐ9.

**Phân vai (A5):** **Chủ sở hữu = Ops/SRE + PO** (viết dashboard). **Người duyệt = CEO/CTO theo nhịp** (mở cổng) — vì đây là chỗ đối chiếu với Business Case họ ký ở GĐ1. `operate` LÀM artifact + trình cổng + đề xuất item; KHÔNG tự quyết đầu tư vòng kế, KHÔNG tự tuyên "đạt, dừng", KHÔNG tự chọn item lên roadmap hộ. Chế độ tự-quyết → người viết đóng vai CEO/CTO+PO tự quyết, ghi rõ.

```text
═══ CỔNG GĐ14 — OPERATE: HexAgent (clean rebuild) · sau pha ALPHA nội bộ ═══
Đạt mục tiêu GĐ1? : MỘT PHẦN (nền R1) — CHƯA TUYÊN được M1/M2/M3.
                    Con số thực vs target: false_finish=0 trên smoke (target 0) NHƯNG chưa số production vì R3 chưa live;
                    0 sandbox-escape / 0 secret (target 0, ĐẠT ở nền); DORA/NFR = OQ-1 chưa có số.
Học được          : (1) M1/M2/M3 chưa có số production vì R3 (multi-agent) chưa build (GĐ12 2 PENDING);
                    (2) resume SPIKE-1/D3 điều-kiện-chặn ĐÓNG R1 chưa xanh staging; (3) OQ-1 DORA+NFR chưa set.
Item cải tiến     : [I-1] đóng R3 để có số M1/M2/M3 thật · [I-2] đóng SPIKE-1/D3 resume · [I-3] set OQ-1 DORA/NFR + redact-raw-args.
                    (mỗi item kèm lý do số/điều-kiện-chặn trỏ tới nó — CHƯA phân rã story)
Artifact          : rebuild-hex-agent/pipeline/14-operate.md (Ops Dashboard §1 · Incident §2 · Iteration §3)
Câu hỏi cổng      : Đạt mục tiêu chưa? Làm gì tiếp? → CEO/CTO + PO quyết đầu tư vòng kế.
════════════════
```

**Quyết định cổng (tự-quyết — đóng vai CEO/CTO + PO duyệt theo nhịp).**

**GATE: GO — mở vòng lặp kế (R3-first) tại `/backlog` GĐ9; alpha TIẾP TỤC vận hành, CHƯA tuyên "đạt mục tiêu".**
Duyệt: **CTO ✔ + PO ✔ (2026-07-02, nhịp đầu).**

**Lý do GO (mở vòng kế, không dừng):** (1) Nền R1 an toàn đã chứng minh bằng số (0 sandbox-escape · 0 secret · guard cắt đúng trên smoke) → đủ để vận hành alpha tiếp và mở bậc pilot khi redact-raw-args xanh. (2) Ba lời hứa điểm-bán (M1/M2/M3) **chưa có số production** — không phải vì hỏng mà vì **R3 chưa live** → việc đúng của vòng kế là *đóng R3 + SPIKE-1 + set OQ-1*, không phải thêm tính năng mới. (3) Có người trực + đường lùi vài-giây + 0 incident → rủi ro vận hành thấp, cổng mở an toàn. (4) Mọi số treo có **địa chỉ đo** rõ (I-1..I-3 trỏ backlog/Operate), không bịa nối.

**Điều CEO/CTO phải chốt (Operate KHÔNG tự quyết):** thứ tự đầu tư vòng kế (I-1 R3 vs I-2 resume vs I-3 OQ-1), và mốc "coi như đạt M1" (Operate đề xuất: sau ≥1 tuần beta với delegation ON và `false_finish_total`=0 trên nhiều loại task — nhưng **CEO/CTO chốt**, không phải `operate`).

**Phương án đã loại ở tầng cổng:**
- **(a) Tuyên "ĐÃ ĐẠT M1, đóng dự án"** — *loại:* false_finish=0 trên smoke KHÔNG chứng minh M1 ở quy mô multi-agent (R3 chưa live); tuyên đạt = báo-xong-khống ở tầng operate, tự phản điểm bán. `operate` không tự tuyên "đạt, dừng" (luật A5).
- **(b) NO-GO / dừng vận hành tới khi R3 xong** — *loại:* nền R1 đã an toàn (0 escape/secret) + 0 incident → dừng alpha là lãng phí; đúng cách = vận hành tiếp + đẩy R3 vào vòng kế. Không phủ định cứng.
- **(c) Đưa "thêm feature mới / E11-E14" vào vòng kế cho hoành tráng** — *loại:* các epic đó park-with-trigger (YAGNI, evidence-C §4), chưa chạm metric-threshold + chưa có consumer; vòng kế phải đóng cái ĐANG treo (R3/resume/NFR) trước, không mở scope mới. (Và `operate` không đề xuất tính năng mới — đó là `/idea`.)
- **(d) `operate` tự chọn I-1 lên roadmap và tự viết story R3** — *loại:* lấn vai `/backlog` (viết story) + lấn quyền CEO/CTO (chọn đầu tư). `operate` chỉ liệt kê item + lý do, để user quyết + `/backlog` phân rã.

```text
═══ BÀN GIAO — HexAgent (clean rebuild) · GĐ14 → vòng kế ═══
Mục tiêu gốc GĐ1 : MỘT PHẦN — M1/M2/M3 CHƯA tuyên được (chưa số production vì R3 chưa live); nền R1 an toàn ĐẠT (0 escape/secret).
Học được         : R3 chưa build → không có số điểm-bán · SPIKE-1/D3 resume chưa xanh staging · OQ-1 DORA/NFR chưa set.
Item cải tiến    : [I-1] đóng R3 multi-agent (có số M1/M2/M3) · [I-2] đóng SPIKE-1/D3 resume · [I-3] set OQ-1 DORA/NFR + redact-raw-args
                   (mỗi item trỏ chỉ số/điều-kiện-chặn cụ thể ở §1 — CHƯA phân rã story)
Artifact         : rebuild-hex-agent/pipeline/14-operate.md (§1 Dashboard · §2 Incident+3 playbook · §3 Iteration)
→ Đưa item cải tiến vào roadmap kế & phân rã story (Epic→Feature→Story→AC): chạy /backlog (GĐ9)  [ĐƯỜNG CHÍNH đóng vòng]
   (gợi ý: I-1 ráp thẳng backlog R3 E09/E10 story ⭐ LÕI đã có AC; I-2 = R1 F1.6 SPIKE-1)
→ Sự cố phát lộ lỗ hổng cần đào gap/edge case sâu (vd honor-system Playbook A) trước khi sửa: chạy /review
→ Item cần nghĩ lại từ nhu cầu/giá trị (verifier độc lập tách judge — ý mới, chưa rõ đáng làm): chạy /idea hoặc /partner
→ Cần build ngay một slice cải tiến nhỏ đã rõ (vd bật redact-raw-args + test 0-secret): chạy /frame
════════════════
```
*Chỉ liệt kê, KHÔNG tự chọn hộ user chạy skill nào tiếp.*

*Traceability:* GĐ14 **nhận** Go/No-Go + Runbook + Rollback GĐ13 (`13-ship.md`: GO alpha · 6 metric loop + alert false_finish>0 · incident owner 4 team · rollback tắt-flag · OQ-1 treo) + Backlog GĐ9 (`09-backlog.md`: M1/M2/M3 + nơi vòng lặp kế đổ về) + Business Case GĐ1 (`ideas/hex-agent-rebuild.md`: M1 gate/M2/M3 · OQ-1). **Sinh** trang OPERATE 3-trong-1: Ops Dashboard 4 nhóm (Business đối chiếu THẲNG M1/M2/M3 · Product · Engineering[observability gốc tool_calls/llm_calls/parse_errors/same_tool_blocks/policy_blocks/tool_failures + DORA 4] · Operations[uptime/resume-success/sandbox-escape=0/secret=0]) · Incident 5-bước + 3 playbook (honor-system/runaway/secret) · Iteration nhịp-2-tuần + 3 item về backlog. **Bàn giao** `/backlog` (chính — đóng vòng: I-1 R3 · I-2 resume · I-3 OQ-1) · `/review` (đào honor-system) · `/idea`·`/partner` (verifier độc lập) · `/frame` (redact-raw-args). Sợi liền hai đầu: ngược (Business ↔ M1/M2/M3 GĐ1 · Incident ↔ owner/rollback/alert GĐ13 · mỗi item ↔ một chỉ số `chưa có số`/điều-kiện-chặn) + xuôi (item cải tiến → roadmap kế GĐ9). Ẩn số treo có địa chỉ: R3→backlog R3, SPIKE-1/D3→R1 F1.6, OQ-1 DORA/NFR→đo tại Operate qua các nhịp, honor-system→/review+/idea.
