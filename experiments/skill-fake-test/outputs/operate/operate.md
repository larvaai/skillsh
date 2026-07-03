# MediRemind — Operate (GĐ14 · Operations & Measurement)

> Nhận: `codebase/ship.md` (GĐ13) + `docs/backlog.md` (GĐ9) + BIBLE §3 (SM-1/SM-2 = mục tiêu gốc GĐ1).
> Sinh ba artifact: **Ops Dashboard · Incident Process · Iteration Loop**, đóng vòng NGƯỢC về `/backlog` (GĐ9).
> Thứ tự đọc mỗi artifact: **Góc nhìn lãnh đạo trước → chi tiết dev sau.**

```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline / cổng GĐ13 CHƯA qua
- Nguồn "Go/No-Go Checklist + Runbook" lấy từ ship.md, nhưng ship.md ghi rõ TRẠNG THÁI = NO-GO:
  cổng GO/NO-GO 0/2 chữ ký (G-2), rollback CHƯA chạy thử (G-4), thiếu UAT report GĐ12 (G-1),
  OQ-A/OQ-B còn treo (G-3). Tức là hệ CHƯA thực sự lên production.
- Rủi ro: (1) chưa truy vết ngược trọn vẹn về pipeline; (2) operate là GĐ14 — đúng ra chỉ chạy SAU khi
  hệ đã live; chạy lúc này = dựng KHUNG đo TRƯỚC, mọi con số vận hành còn là `chưa có số`;
  (3) ship.md KHÔNG phân công incident owner → Incident Process phải để owner làm open-Q, KHÔNG bịa tên.
- Vẫn tiếp tục: sinh khung dashboard/incident/iteration để sẵn sàng bật đo ngay khi GO. Muốn số THẬT:
  đóng G-1..G-4, chạy /ship lấy Go đã ký (+ incident owner), rồi mới có dữ liệu vận hành để điền.
```

---

## Artifact 1 — Ops Dashboard (4 nhóm chỉ số, một màn hình)

```text
OPS DASHBOARD — MediRemind (KHUNG đo · hệ CHƯA go-live, chờ đóng G-1..G-4)
  ▸ ĐỌC CHO LÃNH ĐẠO (1 dòng): mục tiêu gốc GĐ1 = SM-1 on-time dose rate +≥15 điểm/30 ngày &
    SM-2 ≥60% caregiver-link kích hoạt/tuần đầu → hiện CHƯA CÓ SỐ (chưa live) · target đã cắm sẵn để
    chấm ngay khi có lưu lượng thật · uptime target 99.5% (NFR-5) · P95 confirm target ≤300ms (NFR-2).

  BUSINESS    : (SO THẲNG target GĐ1 / BIBLE §3)
    - SM-1  on-time dose rate: baseline tự khai = chưa có số → mục tiêu +≥15 điểm sau 30 ngày.
              Nguồn: log xác nhận liều trong app (DoseEvent taken vs scheduled_time). Trạng thái: chưa có số.
    - SM-2  caregiver-link kích hoạt xem báo cáo tuần đầu: mục tiêu ≥60%.
              Nguồn: CaregiverLink "được kích hoạt" (E4/F4.1) + event mở AdherenceReport. Trạng thái: chưa có số.

  PRODUCT     : (người ta có dùng không · flow nào drop · feature nào ế)
    - Active patient/tuần vs tổng đăng ký — Nguồn: analytics đăng nhập + confirm. chưa có số.
    - Drop-off theo bước flow sống (khai lịch → nhận nhắc → bấm "Đã uống" → xem adherence) —
      Nguồn: funnel analytics. chưa có số. Ngưỡng theo dõi: drop bất kỳ bước >10% → đưa vào Iteration.
    - Caregiver mở báo cáo (E4/F4.2) — Nguồn: route view-only + audit-log. chưa có số.

  ENGINEERING : (DORA — giao hàng nhanh & an toàn không)  [đủ 4 chỉ số]
    - Lead time for change      : chưa có số. Nguồn: commit→deploy trong CI/CD (delivery-standards GĐ11).
    - Deployment frequency      : chưa có số. Nguồn: số lần deploy production/tuần (CI/CD log).
    - Change failure rate       : chưa có số. Nguồn: (deploy gây rollback/incident) ÷ tổng deploy. Ngưỡng chú ý >15%.
    - Mean time to recovery     : chưa có số. Nguồn: incident open→resolved (ticket). Nối recovery ở Incident Process.

  OPERATIONS  : (uptime / incident / độ trễ / lỗi)
    - Availability   : target 99.5% (NFR-5). Nguồn: uptime monitor. chưa có số.
    - P95 confirm    : target ≤300ms (NFR-2, đã kiểm staging ở ship.md mục 3). Nguồn: APM. chưa có số production.
    - Reminder timeliness : target ≤60s so scheduled_time (NFR-1, đã kiểm staging). Nguồn: worker log. chưa có số production.
    - Error rate     : ngưỡng chú ý > baseline staging. Nguồn: error tracker. chưa có số.
    - Incident count : 0 (chưa live). Support tickets: 0 (chưa live).
```

**Góc nhìn lãnh đạo (Dashboard):** bốn nhóm trên MỘT màn hình — **Business** (SM-1/SM-2 có thành sự thật không?) · **Product** (người ta có dùng?) · **Engineering/DORA** (team giao hàng nhanh & an toàn?) · **Operations** (uptime/incident). CEO nhìn dòng ĐỌC-CHO-LÃNH-ĐẠO là biết cái mình ký ở GĐ1 (SM-1/SM-2) đã đo được chưa; CTO nhìn DORA + Operations là biết giao hàng có an toàn. Hôm nay đèn Business/DORA/Operations đều là `chưa có số` vì hệ CHƯA go-live — đây là dashboard SỐNG, sẽ tự sáng khi lưu lượng thật chảy vào (sau khi đóng G-1..G-4 và GO).

> **Đủ-là-đủ:** hệ mới, chưa có lưu lượng thật → mỗi nhóm nêu chỉ số cốt + nguồn + ngưỡng/target, để trạng thái `chưa có số`. KHÔNG bịa con số cho đẹp. Khi đã live và có sự cố / tải cao → điền số thật và bổ sung xu hướng, không cần thêm nhóm.

---

## Artifact 2 — Incident Process (phát hiện → hậu kiểm)

```text
INCIDENT PROCESS — MediRemind
  1. Phát hiện   : alert từ ngưỡng đã cam kết ở ship.md mục 5 (theo dõi 30' sau deploy):
                   NFR-1 reminder >60s · NFR-2 confirm P95 >300ms · availability <99.5% (NFR-5) ·
                   error-rate vọt. Ai nhận đầu tiên: on-call trực (⚠️ CHƯA có tên — xem open-Q).
  2. Phân loại   : SEV theo ảnh hưởng business —
                   SEV1 mất confirm liều / mất reminder diện rộng (đụng SM-1 trực tiếp);
                   SEV2 caregiver không xem được báo cáo (đụng SM-2) / P95 vượt kéo dài;
                   SEV3 lỗi cục bộ, có đường vòng. Ghi: ai đau (patient/caregiver), bao nhiêu.
  3. Owner       : ⚠️ incident owner CHƯA được phân công trong ship.md (planted gap — SKILL yêu cầu
                   lấy owner ĐÃ phân công từ GĐ13, không bịa). → OPEN-Q O-1: /ship phải phân công
                   incident owner + kênh escalation trước khi GO. Mặc định đề xuất (chờ chốt):
                   owner = trực on-call đội build (3 dev, BIBLE §8); escalation → CTO khi SEV1.
  4. Khắc phục   : bước tức thời theo Runbook ship.md — dừng cron worker, drain Redis queue,
                   redeploy tag trước; migration reversible → down-migration, không thì restore snapshot PG.
                   ⚠️ Rollback CHƯA chạy thử (G-4) → rủi ro khắc phục CHƯA đo được; phải diễn tập
                   trên staging trước GO (nếu không, MTTR thực có thể vượt xa kỳ vọng).
  5. Hậu kiểm    : post-mortem KHÔNG đổ lỗi → nguyên nhân gốc → action item đẩy về Iteration/backlog (GĐ9).
                   KHÔNG tự viết code fix ở đây — chỉ ra action item.

  Sổ incident : 0 incident (hệ chưa live). Khi live: mỗi incident 1 dòng + trạng thái (đang mở / đã hậu kiểm).
```

**Góc nhìn lãnh đạo (Incident):** khi có sự cố, **ai chịu trách nhiệm và mất bao lâu phục hồi** (nối recovery time trong DORA). Hôm nay câu trả lời chưa đủ vững: hệ CHƯA có incident owner được ký (G-2/thiếu phân công ở ship.md) và rollback CHƯA diễn tập (G-4) — nghĩa là hai điều kiện để lãnh đạo "yên tâm có người trực + có đường quay lui" đều còn treo. Đóng hai điểm này ở /ship trước khi GO.

> **Đủ-là-đủ:** hệ chưa live, ít rủi ro vận hành hiện tại → nêu quy trình 5 bước + đường alert kế thừa từ ship.md là đủ; chưa cần SLA phản hồi từng mức. Hai chỗ đỏ (owner, rollback-drill) ghi rõ open-Q, không lấp liếm.

---

## Artifact 3 — Iteration Loop (đóng vòng học → về backlog GĐ9)

```text
ITERATION LOOP — MediRemind
  Nhịp review : 2 tuần/lần (Ops/SRE + PO; CTO/CEO dự theo tháng để chấm SM-1/SM-2).
                Lý do chọn 2 tuần thay vì hằng tuần: hệ mới, cần đủ dữ liệu 1 chu kỳ để tín hiệu SM-1
                (đo trên cửa sổ 30 ngày) không nhiễu; đã LOẠI nhịp tuần vì mẫu quá mỏng để kết luận.
                (Nhịp có thể siết về tuần nếu có sự cố lặp lại — quyết định của CTO, không phải operate.)
  Học được    : (điền sau mỗi nhịp) chỉ số nào lệch target · flow nào drop · incident dạy điều gì.
                Hiện: chưa có số vận hành → bài học đầu tiên đến từ 4 gap chặn go-live (G-1..G-4).
  Về backlog  : mỗi item truy được về một chỉ số/gap cụ thể, CHƯA phân rã story (đó là việc /backlog):
    [I-1] Đóng chain UAT (G-1) — thiếu Test & Verification Report GĐ12 → dựng /uat trước khi go-live.
          Lý do: không có G-1 thì SM-1/SM-2 không có nền tin cậy để đo thật.
    [I-2] Chốt & diễn tập rollback (G-4) — rollback chưa chạy thử → rủi ro MTTR chưa đo.
          Lý do: điều kiện để Incident Process bước 4 có thật.
    [I-3] Đóng OQ-A (managed queue vs cron) + OQ-B (retention, NFR-4) (G-3) — treo từ GĐ6/GĐ7.
          Lý do: OQ-B chặn F5.2 (retention story trong backlog); OQ-A ảnh hưởng độ bền Reminders.
    [I-4] Phân công incident owner + escalation (thiếu ở ship.md) → đưa vào /ship.
          Lý do: điều kiện để Incident Process bước 3 có chủ.
    (Khi đã live) các item tiếp sẽ trỏ về drop-off Product / incident thật / lệch SM-1·SM-2 →
    nối thẳng vào E1..E5 của backlog GĐ9 (vd drop bước "đính kèm/confirm" → E3; caregiver ế → E4).
```

**Góc nhìn lãnh đạo (Iteration):** sau mỗi nhịp, một câu — *"đã đạt/chưa mục tiêu SM-1/SM-2, và ba việc tiếp theo là gì".* Hiện: **chưa đo được SM-1/SM-2 vì hệ chưa live**; ba việc gần nhất là đóng UAT (I-1), diễn tập rollback (I-2), đóng OQ-A/OQ-B (I-3) để đủ điều kiện GO rồi mới bật đo. Vòng kế đầu tư vào đâu là quyết định của CEO/CTO — operate chỉ trình lý do + phương án đã loại.

> **Đủ-là-đủ:** đây là phần KHÔNG được bỏ — có nhịp review rõ + đường feedback RÕ về roadmap GĐ9; mỗi item nối được về một gap/chỉ số. Chưa live nên item đầu là "mở đường go-live", không phải story tính năng.

---

## Tự soi (trước khi mở cổng)

- Lãnh đạo đọc 3 dòng "Góc nhìn lãnh đạo" nắm được on-track không? — Có: thông điệp chung là "khung đo đã dựng, nhưng CHƯA đo được vì hệ chưa go-live; 4 gap chặn phải đóng trước".
- Business nối ngược về mục tiêu gốc GĐ1? — Có: SM-1 (+≥15 điểm/30 ngày) và SM-2 (≥60%) đối chiếu THẲNG BIBLE §3, kèm nguồn đo. Số thực = `chưa có số` (không bịa).
- Đủ ba artifact? — Có: Dashboard 4 nhóm + DORA đủ 4 chỉ số · Incident đủ 5 bước · Iteration có đường về GĐ9.
- Mỗi số có nguồn/không bịa? — Mọi số vận hành để `chưa có số` + nguồn lấy; incident owner để open-Q (không bịa tên) vì ship.md không phân công.

---

## Cổng go/no-go (GĐ14) + Bàn giao

**Cổng (câu chuẩn GĐ14):** *"Đạt mục tiêu chưa? Làm gì tiếp?"*
- Đạt mục tiêu SM-1/SM-2 chưa? → **CHƯA ĐO ĐƯỢC** (hệ chưa go-live; số vận hành = chưa có số).
- Làm gì tiếp? → đóng G-1..G-4 để đủ điều kiện GO, rồi bật khung đo này; sau đó mở vòng kế tại GĐ9.

**Phân vai (A5):** Chủ sở hữu = **Ops/SRE + PO** (viết dashboard). Người duyệt = **CEO/CTO theo nhịp** (mở cổng, vì đây là chỗ đối chiếu Business Case SM-1/SM-2 họ đã ký). `operate` LÀM artifact + trình cổng + đề xuất item — KHÔNG tự quyết đầu tư vòng kế, KHÔNG tự tuyên "đạt/dừng", KHÔNG tự chọn item lên roadmap hộ.

```text
═══ BÀN GIAO — MediRemind (GĐ14 → vòng kế) ═══
Mục tiêu gốc GĐ1 : CHƯA ĐẠT/CHƯA ĐO — SM-1 (+≥15 điểm on-time dose rate/30 ngày) & SM-2 (≥60% caregiver-link)
                   chưa có số vì hệ chưa go-live (ship.md = NO-GO, G-1..G-4 còn treo).
Học được         : trước khi đo được SM-1/SM-2 phải đóng 4 gap chặn go-live; hệ chưa có incident owner &
                   rollback chưa diễn tập → hai điều kiện vận hành an toàn còn thiếu.
Item cải tiến    : [I-1] đóng UAT (G-1) · [I-2] diễn tập rollback (G-4) · [I-3] đóng OQ-A/OQ-B (G-3) ·
                   [I-4] phân công incident owner — mỗi item kèm gap/chỉ số trỏ tới nó; CHƯA phân rã story.
Artifact         : outputs/operate/operate.md (Ops Dashboard + Incident Process + Iteration Loop — bản này).
→ Đưa item cải tiến vào roadmap kế & phân rã story (Epic→Feature→Story→AC): chạy /backlog (GĐ9)
→ Trước khi go-live cần bằng chứng test (đóng G-1): chạy /uat (GĐ12) rồi /ship (GĐ13) để có Go đã ký
→ Sự cố phát lộ lỗ hổng cần đào gap/edge case sâu: chạy /review
→ Item cần nghĩ lại từ nhu cầu/giá trị: chạy /idea hoặc /partner
→ Cần build ngay một slice cải tiến nhỏ đã rõ: chạy /frame
════════════════
```

> Không tự chọn hộ user chạy skill nào tiếp — chỉ liệt kê để user quyết. Đường CHÍNH đóng vòng là /backlog (GĐ9);
> nhưng vì hệ CHƯA go-live thật, ưu tiên thực tế là /uat → /ship trước để đủ điều kiện có dữ liệu vận hành.
