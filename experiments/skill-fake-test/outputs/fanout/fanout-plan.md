# FAN-OUT PLAN — nhóm `pg-build` (DRY-RUN, không spawn thật)

> Skill: `fanout` · Project: MediRemind · Con trỏ: gd11_delivery
> Nguồn sự thật: `fixture/mediremind/progress/progress.json` (đọc, không ghi)
> Ngày: 2026-07-03 · Chế độ: DRY-RUN (Bước 0–2 của SKILL.md; KHÔNG chạy Bước 3 spawn, Bước 5 đóng cổng)

---

## Bước 0 — Nạp ngữ cảnh, chọn nhóm

Đọc theo hợp đồng nạp-ngữ-cảnh (conventions §4): `constitution/` → `progress.json` → artifact liên quan (`docs/contracts/`, `docs/module-map.md`, `codebase/delivery-standards.md`, `codebase/pointer.md`).

`parallel_group` duy nhất có mọi task READY: **`pg-build`**
- **T-11a** — Sinh Scheduling module theo contract — `ready` — depends_on [T-08, T-11] — owner delivery — artifact `codebase/mediremind/src/scheduling/`
- **T-11b** — Sinh Reminders module theo contract — `ready` — depends_on [T-08, T-11] — owner delivery — artifact `codebase/mediremind/src/reminders/` — traces NFR-1

Không có nhóm song song nào khác. T-12 (UAT) còn `todo` và phụ thuộc CẢ T-11a + T-11b → là điểm HỢP NHẤT sau fan-out, chưa bung được.

## Bước 1 — Kiểm điều kiện fan-out

| Điều kiện (SKILL.md Bước 1) | Kết quả | Bằng chứng |
|---|---|---|
| Mọi task trong nhóm `ready`? | ĐẠT | T-11a=ready, T-11b=ready trong progress.json |
| Depends_on đã `done`? | ĐẠT | T-08 done, T-11 done |
| Task đầu vào chung (contract) đã `done`? | ĐẠT (theo trạng thái) | T-08 trạng thái `done` |
| Contract có phiếu checkpoint `PASS`? | **KHÔNG XÁC MINH ĐƯỢC** | `progress/checkpoints/` không tồn tại — xem CẢNH BÁO |
| Đầu vào chung đã FREEZE? | ĐẠT (theo nội dung) | scheduling-v1 + adherence-v1 có đủ API/event/error/ownership; module-map ghi "Does NOT own" rõ |

### CẢNH BÁO điều kiện (ghi vào friction)

1. **Thiếu phiếu PASS cho contract.** SKILL.md Bước 1 và Quy tắc bắt buộc yêu cầu contract "có phiếu checkpoint `PASS` trước khi fan-out". Thư mục `progress/checkpoints/` KHÔNG tồn tại trong fixture. T-08 chỉ `done` bằng cờ trong progress.json, không có bằng-chứng-phiếu. Chiếu `definition-of-done.md` (một bước XONG cần đủ 3: artifact + phiếu PASS + progress), điều kiện fan-out chỉ đáp ứng MỘT PHẦN. Bản live sẽ phải chặn hoặc yêu cầu `/checkpoint T-08` trước. DRY-RUN nên tôi tiếp tục nhưng đánh dấu rõ.

2. **Contract path trong graph SAI so với đĩa.** progress.json (T-08) + board.md trỏ artifact contract tới `docs/contracts/module-contract-v1.md` — file này KHÔNG tồn tại. Contract THẬT là 2 file: `docs/contracts/scheduling-v1.md` (cho T-11a) + `docs/contracts/adherence-v1.md`. Bundle dưới bám 2 file thật này. delivery-standards.md §2 cũng gọi tên "scheduling-v1, adherence-v1" → xác nhận 2 file thật là nguồn sự thật, còn `module-contract-v1.md` là tên treo lơ lửng trong graph.

## Bước 2 — Gói ngữ cảnh mỗi task

Hai bundle GỌN nằm cạnh file này:
- `bundle-T-11a-scheduling.md`
- `bundle-T-11b-reminders.md`

Mỗi bundle chỉ chứa: luật liên quan (trích, không đổ cả constitution) + contract của đúng nhánh đó + spec task + đích artifact + danh sách KHÔNG-build. Cô lập đầu ra: T-11a ghi `src/scheduling/`, T-11b ghi `src/reminders/` — hai path không giao nhau.

---

## Bước 3 — Bung agent đồng thời (DRY-RUN — MÔ TẢ, KHÔNG spawn)

```
═══ FAN-OUT — pg-build (DRY-RUN) ═══
Đầu vào chung: docs/contracts/scheduling-v1.md + adherence-v1.md (frozen theo nội dung; phiếu PASS chưa xác minh — xem cảnh báo)
Agent 1 → T-11a: Sinh Scheduling module  → codebase/mediremind/src/scheduling/
Agent 2 → T-11b: Sinh Reminders module   → codebase/mediremind/src/reminders/
(sẽ chạy đồng thời — TẤT CẢ trong một lượt Agent tool call; DRY-RUN nên KHÔNG thực thi)
════════════════
```

Khớp task-id ↔ agent: Agent 1 ⇄ T-11a, Agent 2 ⇄ T-11b.

## Bước 4 — Thu kết quả (chưa chạy)

Live: mỗi agent về → `ls` xác nhận artifact nằm đúng path → giữ tóm tắt (đã làm gì, gắn contract/AC nào, còn treo gì). DRY-RUN: bỏ qua.

## Bước 5 — Đóng từng nhánh (chưa chạy)

Live: mỗi task → `/checkpoint <id>` → PASS thì `/progress` advance → khi cả T-11a + T-11b done thì mở khóa T-12 (UAT). `fanout` KHÔNG tự ghi progress.json, KHÔNG tự cấp phiếu — gọi `checkpoint` + `progress`. DRY-RUN: bỏ qua.

```
═══ FAN-OUT XONG — pg-build (mẫu, chưa chạy) ═══
T-11a scheduling : (chờ checkpoint)
T-11b reminders  : (chờ checkpoint)
Mở khóa khi CẢ HAI PASS: T-12 UAT (depends_on T-11a, T-11b) → ready
→ Kế: /progress hoặc /resume
════════════════
```

---

## VÌ SAO KHÔNG đổ cả repo cho agent

Nguyên tắc SKILL.md: "Gói ngữ cảnh GỌN, không đổ cả repo." Lý do cụ thể cho fixture này:

1. **Chống lệch nhánh (drift).** Contract là nguồn sự thật DUY NHẤT để 2 bên bám mà build độc lập (definition-of-done GĐ10). Đưa cả repo, agent dễ suy diễn API từ code sẵn có thay vì bám contract → hai nhánh trôi lệch nhau, phá đúng cái fan-out muốn bảo toàn.

2. **Cưỡng chế ranh giới "Does NOT own".** conventions §1 (một file một chủ) + module-map "Does NOT own" cấm ghi chéo module. Nếu T-11a nhìn thấy `src/reminders/` + `src/adherence/`, nó có thể vô tình sửa entity của module khác. Bundle chỉ đưa ĐÚNG contract nhánh mình + liệt kê KHÔNG-build → biên cứng, không cần agent tự đoán biên.

3. **Cô lập đầu ra khi chạy đồng thời.** Hai agent chạy song song; mỗi agent chỉ biết path artifact của MÌNH (`src/scheduling/` vs `src/reminders/`) → không giẫm chân, không cần khoá.

4. **Không rò open-question chưa đóng.** OQ-A (queue vs cron) và OQ-B (retention) còn treo. Đổ cả repo kèm `src/legacy/old_reminder_cron.ts` (ứng viên triage, dính OQ-A) dễ khiến agent "quyết luôn" một open-question chưa được ADR đóng — vi phạm conventions §7. Bundle nêu rõ open-Q là ranh giới KHÔNG-quyết.

5. **Giữ context nhỏ = rẻ + tập trung.** Đổ cả constitution (4 file) + docs (7 file) + toàn repo vào mỗi agent làm loãng tín hiệu và tốn token vô ích. Agent build chỉ cần: 1 contract + trích luật liên quan + spec + đích + biên. Mọi thứ khác là nhiễu.
