# Traceability Report — hex-agent-rebuild (Tháp kiểm soát Idea→Operate)

> Skill `traceability` · GĐ control (panel CEO/CTO). READ-ONLY: chỉ đọc artifact + state của 15 giai đoạn rồi báo thiếu/đứt/cổng, KHÔNG sửa artifact stage nào. Snapshot tại 2026-07-02.
> Nguồn: `rebuild-hex-agent/00-understanding/*` (ATLAS + REBUILD-BRIEF + evidence A/B/C) · `rebuild-hex-agent/pipeline/*.md` + `pipeline/*.json` (state đã qua cổng của từng stage). Không đọc được từ file → ghi "không rõ", không đoán.

---

## Góc nhìn lãnh đạo (đọc 60 giây)

1. **Đang ở đâu.** Pipeline đã CHẠY HẾT trọn vòng GĐ0→GĐ14: từ Idea/Domain tới Operate, mọi giai đoạn đều có artifact + state + cổng tự-quyết GO. Hiện đang **ở GĐ14 (Operate)**, cổng GĐ14 đã GO và **đóng vòng quay lại GĐ9 (/backlog)** cho vòng lặp kế. Đây là một pipeline HOÀN CHỈNH-VỀ-HÌNH nhưng **CHƯA HOÀN CHỈNH-VỀ-BẰNG-CHỨNG-CHẠY-THẬT**.

2. **Cổng đắt qua chưa.** Đây là chỗ lãnh đạo phải tỉnh táo:
   - **GĐ8 live slice (cổng đắt #1): CHƯA PASS.** Skeleton tick **0/9** ô — chưa có staging chạy thật trên bản rebuild; slice chưa được `/frame` dựng & deploy; `link_staging = null`. Cổng GĐ8 ghi rõ **"NO-GO cho pass / đổ-người-build-full"** (chỉ GO cho "dựng-slice-ngay"). Nghĩa là **kiến trúc CHƯA được chứng minh chạy được ở bản rebuild** — mới chỉ chứng minh ở bản GỐC (anchor file:line).
   - **GĐ13 go/no-go (cổng đắt #2): ĐÃ GO — nhưng CÓ ĐIỀU KIỆN, phạm vi hẹp.** CTO+PO ký GO cho **ALPHA nội bộ**, write-tool + delegation **TẮT (OFF)**. Đây là GO cho "nền R1 an toàn", KHÔNG phải GO cho lõi bán hàng (R3 multi-agent).

3. **Thiếu lớn nhất (một câu).** Không phải thiếu artifact — mà thiếu **BẰNG CHỨNG CHẠY THẬT cho lõi sản phẩm**: (a) live slice GĐ8 chưa dựng (0/9), (b) **R3 multi-agent chưa build** nên **M1/M2/M3 — ba lời hứa điểm bán — chưa tuyên được** (GĐ12: 2 AC PENDING, GĐ14: business "đạt MỘT PHẦN"), (c) **SPIKE-1/D3 resume chưa xanh staging** (điều kiện chặn ĐÓNG R1). Cả ba đã được các stage ghi minh bạch và **cùng đổ về /backlog GĐ9** (item I-1/I-2/I-3). Không có mắt xích traceability nào ĐỨT; vấn đề là **độ chín thực thi**, không phải lỗ hổng thiết kế.

**Kết một câu cho CEO/CTO:** *Bản thiết kế và kế hoạch đã đủ và nối liền từ mục tiêu M1 tới metric Operate; nhưng "đã GO" ở GĐ13 chỉ là GO-alpha-nền — muốn tuyên đạt mục tiêu sản phẩm (M1/M2/M3) thì phải quay lại xây R3 + đóng live-slice GĐ8 + SPIKE-1, rồi mới go-live pilot/beta.*

---

## 1. Artifact Dashboard (D1)

```
DASHBOARD — hex-agent-rebuild     Đang ở: GĐ14 Operate (vòng đóng về GĐ9)
                                  Cổng đắt: [GĐ8 live slice: ✗ CHƯA PASS 0/9] [GĐ13 go/no-go: ✓ GO-alpha có điều kiện]
GĐ   Artifact                              TT   Skill      Cổng / ghi chú
00   ATLAS (nền hiểu biết, 7 invariant)    ✓    /atlas     GO — understanding L4, scope partial
0-5  Idea→Domain (Business/PRD/Domain)     ✓    /idea      GO×3 (GĐ1·GATE1·GATE2·GĐ5) — done_handoff
6    Architecture Brief + C4 + 6 ADR       ✓    /shape     GO — có Security Model + STRIDE
7    Tech Decision Matrix + 7 ADR + SPIKE  ✓    /stack     GO — Python3.11·LangGraph·SQLite; SPIKE-1 TREO
8    Live Slice Report (đắt)               ✗    /skeleton  NO-GO pass · 0/9 tick · staging=null · SPIKE-1 chưa đo
9    Roadmap + Backlog (Story/AC*)         ✓    /backlog   GO — R1 tới Story+AC; R3 lõi có AC (M1/M2/M3)
10   Module Map + Contract                 ✓    /modules   GO — 6 module·6 owner·2 seam (⚠ map-feature dùng epic)
11   Delivery Std + DoD*                    ✓    /delivery  GO — DoD 9 dòng + D1–D5 invariant-test
12   Test & Verification (mapping*)         ~    /uat       GO-có-ĐK — 26/28 PASS · 2 PENDING R3 · sign-off có-ĐK
13   Go/No-Go + Runbook + Rollback* (đắt)   ✓    /ship      GO alpha nội bộ (write/delegation OFF) · CTO+PO ✔
14   Ops Dashboard + Metric                 ~    /operate   GO — business "đạt MỘT PHẦN"; nhiều ô "chưa có số"
```
`✓`=đủ · `~`=đủ-artifact-nhưng-điều-kiện-treo (hợp lệ, không phải thiếu) · `✗`=cổng chưa pass · `*`=never-skip.

**Never-skip — kiểm hết, KHÔNG cái nào vắng:**
- Story + AC (GĐ9): ✓ có (15 story R1 có AC + 6 story lõi R3 có AC; AC nằm dưới story; DoD tách khỏi AC).
- Definition of Done (GĐ11): ✓ có (DoD 9 dòng + 5 invariant-kiểm-được D1–D5, "không cắt dòng").
- Test mapping (GĐ12): ✓ có (Requirement→AC→Test Case→Result; 28 AC lõi ánh xạ TC, 26 PASS / 2 PENDING).
- Rollback + Monitoring (GĐ13): ✓ có (rollback = tắt flag features.yaml + resume/replay, đã test smoke offline; monitoring = events.jsonl + 6 metric + alert cứng false_finish>0).

→ **0 never-skip vắng mặt.** Trạng thái `✗`/`~` ở GĐ8/12/14 là **cổng/điều-kiện treo có địa chỉ**, không phải artifact bị bỏ.

---

## 2. Kiểm Sợi traceability (C1)

Chuỗi bắt buộc, truy từng mắt xích cho các item ĐANG SỐNG:

```
Business Objective → Product Goal → Requirement → PRD → Epic → Feature → Story → AC → Test Case → Release → Metric
```

| Mắt xích | Có nối? | Neo |
|---|---|---|
| **Business Objective** M1 zero-false-finish (phụ M2 bounded, M3 no-escalation) | ✓ | 05-idea-domain.md:44 (oracle `state.py:35-37`) |
| → **Product Goal** agent tự-điều-phối, FINISHED chỉ khi mọi AC có evidence thật | ✓ | backlog.json roadmap.product_goal |
| → **Requirement / PRD** (Success metric M1/M2/M3, NFR neo file:line) | ✓ | 05-idea-domain.md:106-116 (PRD 1 trang) |
| → **Epic** E01–E21 (P0 Foundation → P3 Multi-agent lõi → P4 Control Plane) | ✓ | REBUILD-BRIEF §Roadmap; backlog.json releases R1–R4 |
| → **Feature** F1.1–F1.6 (R1) · F3.2–F3.5 (R3 lõi) | ✓ | backlog.json features(15); E10 cắt 4 feature |
| → **Story** S1.1.1…S1.6.1 (R1) · S3.5.1/S3.5.2/S3.2.1/S3.3.1/S3.4.1 (R3 lõi) | ✓ | backlog.json stories_co_ac / stories_loi_R3 |
| → **AC** (nối thẳng 5 domain-rule: finish-evidence · gate-verdict · scope⊆parent · μ-proof · execute_tool) | ✓ | backlog.json traceability.ac_noi_domain_rule |
| → **Test Case** TC-… (28 AC lõi ↦ TC property/audit/integration) | ✓ | uat.json ac_loi_6_nhom + ac_bo_tro_chokepoint_D1 |
| → **Release** R1 (GO alpha) · pilot⟺write · beta⟺delegation (R3) | ✓ | ship.json rollout_strategy (bậc 1–5) |
| → **Metric** M1 false_finish_total · M2 budget_tripped · M3 delegation_rejected{scope} | ✓ | operate.json dashboard.business ↔ muc_tieu_goc_gd1 (vòng khép về GĐ1) |

**Kết luận sợi: KHÔNG có mắt xích ĐỨT.** Chuỗi khép kín cả hai chiều — xuôi (Objective→Metric) và ngược (Operate metric đối chiếu thẳng target GĐ1). Điểm cần lãnh đạo nắm, **không phải đứt mà là "chưa có số"**:
- Mắt xích **Test Case → Metric của R3** tồn tại về ĐỊNH NGHĨA nhưng **giá trị là PENDING/"chưa có số production"**: TC-FINISH-EVIDENCE-001, TC-DELEGATE-SCOPE-001, TC-BOUNDED-* … đã map nhưng chưa chạy xanh (R3 chưa build). Đây là **liên kết-có-nhưng-chưa-kích-hoạt**, đã ghi PENDING minh bạch ở GĐ12 — không tính là đứt (đúng luật "không bịa PASS").
- **PR** (mắt xích Story→PR→Release) **chưa tồn tại**: chưa có code slice nào được `/frame` build → chưa có PR link story. Không tính đứt chuỗi thiết kế, nhưng là **bằng chứng cho thấy chưa bước sang thực thi**.

---

## 3. Phần còn thiếu + nhắc skill

Không có never-skip vắng mặt. "Thiếu" ở đây = **điều kiện treo chặn tuyên-đạt-mục-tiêu**, mỗi cái có địa chỉ và skill bổ sung rõ (đúng như 3 item Operate đã đẩy về backlog):

| # | Thiếu / treo | Vì sao GĐ sau/mục-tiêu sẽ MÙ | Chạy skill | Ưu tiên |
|---|---|---|---|---|
| G1 | **Live slice GĐ8 chưa dựng (0/9), staging=null** | Cổng đắt #1 chưa pass → "kiến trúc chạy được ở rebuild" chưa chứng minh; mọi tuyên PASS sau đứng trên bằng-chứng-gốc chứ không phải rebuild | **/frame** (dựng slice finish-by-evidence + đo SPIKE-1) → rồi cập nhật /skeleton | **cao** |
| G2 | **R3 multi-agent chưa build → M1/M2/M3 chưa tuyên** | Đây là LÕI ĐIỂM BÁN. GĐ12 2 AC PENDING, GĐ14 business "đạt MỘT PHẦN". Không có R3 = không có số chứng minh sản phẩm làm đúng lời hứa | **/backlog** (đã có story R3 AC → refine) → **/frame** (build S3.5.1/S3.2.1/S3.3.1) | **cao** (I-1) |
| G3 | **SPIKE-1/D3 resume chưa xanh staging** (điều kiện chặn ĐÓNG R1) | Không xanh → uptime/resume-success chưa chốt; nếu fail phải đảo sang phương án B (orchestrator tự viết) | **/frame** (đo resume round-trip a/b/c trong slice) | **cao** (I-2) |
| G4 | **redact-raw-args (D4) chưa xanh** — blocker CISO bật write-tool | Không xanh → không mở được pilot (write_tools_enabled); rò secret raw args trong jsonl (known-gap ADR-006) | **/frame** (bật redact + test 0-secret) → /uat verify | trung |
| G5 | **OQ-1: baseline DORA + NFR-số (P95 loop, ngưỡng alert/error-rate)** chưa có số | DORA + nhiều ô Operations "chưa có số"; alert hiện chỉ định-tính (false_finish>0 + 5 tín hiệu invariant) | **/operate** (đo qua các nhịp, ≥1 tuần beta) — KHÔNG bịa | trung (I-3) |
| G6 | **pentest / DAST public / DR đa-region** hoãn tới khi có transport public (E21 R4) | Chưa expose public transport → chưa cần; nhưng phải mở lại khi bật Control Plane | (park-with-trigger) — mở khi tới E21 R4 | thấp |

**Lưu ý ĐỦ-LÀ-ĐỦ (không flag oan):** GĐ10 (modules) map-feature bằng EPIC thay story vì chạy TRƯỚC khi backlog qua cổng — modules.json đã tự in ⚠ cảnh báo và ranh giới vẫn bám domain GĐ5 (đã qua cổng). **Không tính là thiếu** — đây là rút-gọn-hợp-lệ có ghi chú. Việc R2 (E06–E08) chưa phân rã tới Story+AC cũng **không flag oan**: backlog cố ý refine theo release tới (chống cầu toàn), R2 chưa tới lượt.

---

## 4. Cổng & Security (D3 + C2)

### Cổng tổng hợp

| GĐ | Cổng | Trạng thái | Người duyệt (tự-quyết) |
|---|---|---|---|
| 0–5 | Idea/PRD/Domain đủ rõ? | ✓ GO×4 | PO/CTO |
| 6 | Đủ vững chọn stack? | ✓ GO | Kiến trúc sư/CTO + Security |
| 7 | Stack chốt? | ✓ GO | CTO |
| **8** | **Live slice pass?** | **✗ NO-GO-pass (GO chỉ cho dựng-slice)** | CTO + Tech-lead |
| 9 | Backlog đủ để plan? | ✓ GO | PO + Tech-lead |
| 10 | Ownership rõ? | ✓ GO | Kiến trúc sư + Eng-mgr + CTO |
| 11 | Đạt DoD / chuẩn đủ? | ✓ GO | CTO/Kiến trúc sư + Eng-mgr |
| 12 | Đủ go-live? | ~ **GO-CÓ-ĐIỀU-KIỆN** (2 sign-off ký-có-điều-kiện) | QA-lead + PO + CISO |
| **13** | **GO/NO-GO?** | **✓ GO alpha nội bộ (write/delegation OFF)** | CTO + PO ✔ |
| 14 | Đạt mục tiêu? | ~ GO mở vòng kế — đạt **MỘT PHẦN**, chưa tuyên M1/M2/M3 | CTO + PO |

**Đọc cổng cho lãnh đạo:** cổng đắt #1 (GĐ8) **chưa qua** — đây là cái chuông cảnh báo lớn nhất: mọi GO ở GĐ9→14 đều dựng trên "kiến trúc đã chạy ở GỐC + kế hoạch tốt", chứ chưa trên "slice rebuild chạy thật trên staging". Cổng đắt #2 (GĐ13) **đã GO nhưng phạm vi hẹp** (alpha, hành vi nguy hiểm TẮT). Cả hai điều này các stage đã ghi trung thực, không giấu.

### Security đan giai đoạn (C2) — 7 điểm

| Điểm chốt | GĐ | Trạng thái | Neo |
|---|---|---|---|
| **Data classification** (Public/Internal/Confidential/Secret) | 1/6 | ✓ có | 06-shape.md:58 §6; chống-rò-secret 05-idea-domain.md:101 |
| **Threat model STRIDE** (luồng delegate + redaction) | 6 | ✓ có | 06-shape.md:231 §6.4 |
| **Secret / redact tại biên** | 8/11 | ~ đặt luật, **redact-raw-args CHƯA xanh** (blocker) | skeleton ô#8; delivery secret-mgmt; ADR-006 |
| **Scan (lint/type/audit trong CI)** | 11 | ✓ có (audit-adversarial thay scan generic) | delivery.json ci_pipeline |
| **SAST/DAST** | 12 | ~ audit-adversarial thay DAST (mạnh hơn cho hệ này) PASS-1phần; **pentest/DAST public HOÃN** (chưa transport public) | uat.json lop_test.security_sast_dast_pentest |
| **Checklist go/no-go** | 13 | ✓ có (12 ô, 6 N/A hợp lệ cho alpha nội bộ) | ship.json go_no_go_checklist |
| **Monitoring** | 14 | ~ có (events.jsonl + 6 metric + alert cứng); **ngưỡng-số P95/error-rate = OQ-1 chưa có** | operate.json dashboard + incident_process |

**Security tổng:** nền an toàn ĐÃ chứng minh trên smoke (0 sandbox-escape · 0 secret rò ui_payload). Hai blocker security **có địa chỉ, đúng vai rollout-gate**: (1) redact-raw-args ⟺ mở pilot (write-tool), (2) scope-property D2 ⟺ mở beta (delegation). CISO ký-có-điều-kiện là ĐÚNG (AI chuẩn bị, người thật ký). Không có điểm security nào bị bỏ trống-không-ghi.

### Open-Q còn treo (mang xuyên stage, KHÔNG bịa số)
- **OQ-1** baseline chi phí + false-finish thực + NFR-số (P95/alert) → đo ở Operate.
- **SPIKE-1/D3** resume round-trip a/b/c → điều kiện chặn ĐÓNG R1; fail → phương án B.
- **M1/M2/M3 R3** → chặn release beta.
- **OQ-M1** Skills (E07) nếu phình có state → tách khỏi Discipline.
- **honor-system gap** (O tự-chấm judge, judge≠doer) → /review + verifier độc lập (E15→E21).

---

## Tự soi trước khi chốt

1. Lãnh đạo đọc 3 câu đầu có biết đang-ở-đâu (GĐ14, vòng đóng về GĐ9) + thiếu-lớn-nhất (bằng-chứng-chạy-R3/slice, không phải artifact) + cổng-đắt (GĐ8 ✗, GĐ13 ✓-hẹp) không? — **Có.**
2. Mỗi ✗/~ bám artifact/state thật? Cái chưa chắc ghi rõ? — **Có** (GĐ8 0/9 từ skeleton.json; PENDING từ uat.json; "chưa có số" từ operate.json). Không đoán.
3. Không flag oan (modules dùng epic; R2 chưa refine) + bắt đủ 4 never-skip? — **Có**: 4 never-skip đều hiện diện; 2 chỗ rút-gọn-hợp-lệ được nêu là hợp lệ, không tính thiếu.
4. Mỗi gap trỏ đúng skill, KHÔNG tự làm giai đoạn? — **Có** (G1/G3/G4→/frame, G2→/backlog+/frame, G5→/operate). Read-only, không sửa artifact stage nào.

---

## Bàn giao — nhắc, không làm hộ

```
═══ TRACEABILITY — hex-agent-rebuild ═══
Đang ở: GĐ14 Operate (vòng đóng về GĐ9)
Cổng đắt: live slice GĐ8 ✗ CHƯA PASS (0/9) · go/no-go GĐ13 ✓ GO-alpha-có-điều-kiện (write/delegation OFF)
Thiếu ưu tiên (không phải artifact — mà bằng-chứng-chạy-thật cho lõi):
  1. Live slice GĐ8 chưa dựng (0/9) + SPIKE-1 resume chưa đo → /frame
  2. R3 multi-agent chưa build → M1/M2/M3 chưa tuyên (điểm bán) → /backlog refine → /frame
  3. redact-raw-args (D4) chưa xanh — blocker mở pilot → /frame → /uat
→ Bổ sung live slice + SPIKE-1 + R3 code: chạy /frame (build story R1/R3 có AC)
→ Bổ sung/refine backlog R3: chạy /backlog
→ Set baseline OQ-1 (DORA + NFR-số): chạy /operate qua các nhịp (không bịa số)
→ Muốn được dẫn đi tiếp cả pipeline: chạy /partner
→ Muốn chấm chất lượng một artifact đã có: chạy /grade (vd /grade cho explain)
════════════════
```
Chỉ liệt kê — KHÔNG tự chọn hộ, KHÔNG tự chạy skill khác, KHÔNG sửa artifact stage nào.
