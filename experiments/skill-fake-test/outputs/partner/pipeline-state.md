# Partner — pipeline-state (MediRemind, COLD-START)

> Bản này là **state máy của partner** + lượt hội thoại đầu (feasibility-first → một cụm
> hỏi đòn-bẩy-cao → decision-log → handoff). Nguồn sự thật: BIBLE §1–3. Vào skill ở
> **Bước 1 = COLD-START** (chưa có `pipeline-state.json` cho `mediremind`) → chào, chạy
> đánh giá khả thi ban đầu, mở `open_questions`, đặt con trỏ ở **Trụ 1 · Business Need**.

---

## 0. Xác định project (Bước 0)

Không có arg path chỉ vào code; tin nhắn khung nhu cầu này là **nhu cầu business mới, chưa
mở codebase** (cold-start). → nhánh **GREENFIELD**, slug `mediremind`, `mode = "greenfield"`.
Chưa verify folder, chưa chạy `/frame` hay `/explain` cho tới khi có path thật.

`state/current.json` (cần cập nhật khi ghi thật):
```json
{ "project": "mediremind", "greenfield": true, "updated_at": "2026-07-03T00:00:00Z" }
```

---

## 1. Lượt vào skill — chào COLD-START (đọc theo level; giả định L6, CTO → xác nhận gọn)

```
═══ CHÀO — mình đi cùng bạn từ nhu cầu → release ═══
Mình là partner (fractional-CTO) của bạn. Trước khi tính build gì, mình soi khả thi thật
đã — để không tốn tiền tốn ngày vào chỗ đang đoán mò. Mình thấy ngay hạt giá trị: người
uống 3–8 loại thuốc/ngày hay quên liều là nỗi đau có thật và đo được, còn caregiver ở xa
thì đang "mù" — đúng chỗ một cái nhắc-đúng-giờ + báo-cáo-tin-cậy tạo giá trị.
Con trỏ hiện tại: Trụ 1 · Business Need. Mình hỏi bạn đúng một cụm (3 câu) để chốt "đáng
làm không, bằng con số", rồi mới đi tiếp — không nhảy thẳng sang code.
════════════════
```

---

## 2. Đánh giá khả thi ban đầu (FEASIBILITY-FIRST — nguyên tắc #2)

- **Business:** Đáng-giải rõ. Nỗi đau (quên liều ở người già + bệnh mạn tính) phổ biến và
  tốn kém; caregiver hiện chỉ "gọi điện hỏi". Ẩn số business: **ai trả tiền / vì sao là BÂY
  GIỜ / độ lớn giá trị** chưa có con số — đây đúng là chỗ Trụ 1 phải chốt.
- **Product:** Job-to-be-done rõ ba mảnh (khai báo thuốc+lịch · nhắc + xác nhận "đã uống"
  ngay từ thông báo · tổng hợp adherence + chia sẻ chỉ-xem). Success metric **đã có ngưỡng
  đo được sẵn** (SM-1: +≥15 điểm on-time dose rate sau 30 ngày; SM-2: ≥60% caregiver-link
  kích hoạt tuần đầu) — thuận lợi, không phải đoán.
- **Technical:** Khả thi cao, KHÔNG life-critical (app ghi rõ "không dùng cho cấp cứu"),
  đội mạnh TS. Ẩn số kỹ thuật nằm ở các trụ sau (đúng giờ 60s, dữ liệu sức khoẻ nhạy cảm) —
  chưa cần chạm ở Trụ 1.
- **Unknowns (mở, mang theo):**
  - U-1: Vì sao là BÂY GIỜ? (thời điểm — thị trường/ràng buộc/cửa sổ cơ hội)
  - U-2: Giá trị ước lượng thô = con số nào? (vd số patient mục tiêu, hoặc %adherence×tác động)
  - U-3: Chi phí/khung thời gian MVP ước lượng thô = bao nhiêu tuần/người?
  - U-4 (Trụ 4, treo): retention dữ liệu sức khoẻ giữ bao lâu — chạm NFR-4, đóng ở delivery.

> Ghi chú security xuyên suốt (nguyên tắc #11, Trụ 1–2): **dữ liệu thuốc = dữ liệu sức khoẻ
> nhạy cảm** → data-classification "sensitive/health" là RÀNG BUỘC bắt buộc ngay từ business,
> không phải tính năng thêm. Rủi ro pháp lý (quyền riêng tư y tế) cần nêu khi định giá.

---

## 3. Cụm câu hỏi đòn-bẩy cao nhất (Trụ 1 · Business Need — một cụm/lượt, nguyên tắc #4)

```
═══ LÀM RÕ — Trụ 1 · Business Need ═══
(cụm 1/1 · trả lời xong 3 câu này là đủ đóng Trụ 1)
1. Vì sao là BÂY GIỜ? Có cửa sổ cụ thể nào (ra mắt cùng sản phẩm khác, ràng buộc mùa vụ,
   đối thủ, hay chỉ nội bộ muốn có công cụ) khiến việc này đáng làm lúc này?
2. Giá trị ước lượng thô: con số/khoảng nào bạn kỳ vọng? (vd "phục vụ ~N patient", hoặc
   "nâng adherence từ baseline X% lên Y%") — chỉ cần thô để mình cân với chi phí.
3. Chi phí/khung thời gian MVP bạn hình dung: bao nhiêu tuần với mấy người? (đội đang là
   3 dev mạnh TS — mình sẽ soi ROI thô ngay khi có hai con số này.)
════════════════
```

> Vì sao đúng ba câu này trước: Trụ 1 chỉ còn thiếu **why-now**, **giá trị thô**, **chi phí
> thô** để đóng gate (bài-toán-rõ và ai-đau đã có từ §1–2). SM-1/SM-2 đã đo được nên KHÔNG
> hỏi lại metric ở đây — dồn đòn bẩy vào 3 ô còn trống. Đúng kỷ luật "số cụm hỏi tỉ lệ ẩn
> số, không tỉ lệ số stage" (nguyên tắc #5): initiative này ẩn số business ít → chỉ một cụm.

---

## 4. Decision-log + traceability spine (append-only)

| id | stage | trụ | status | quyết định (rút gọn) | traces_to |
|----|-------|-----|--------|----------------------|-----------|
| NEED-1 | Business Need | 1 | **confirmed** | Xây MediRemind: nhắc uống thuốc + đo adherence cho patient uống nhiều thuốc/ngày; caregiver theo dõi chỉ-xem từ xa. | — |
| NEED-2 | Business Need | 1 | **confirmed** | Ranh buộc nền: KHÔNG life-critical (ghi rõ "không dùng cấp cứu"); dữ liệu thuốc = sức khoẻ nhạy cảm → security là ràng buộc bắt buộc, không phải feature. | NEED-1 |
| CASE-1 | Business Case | 1 | **assumed** | Đáng làm về ROI thô — **chờ** why-now + giá trị-thô + chi phí-thô (cụm 1/1) để nâng lên confirmed. | NEED-1 |

Gate **suy ra** từ `confirmed`: Trụ 1 còn **chưa đóng** vì CASE-1 đang `assumed` (thiếu
why-now + giá-trị-thô + chi-phí-thô). Đúng nguyên tắc #6 — không skip im lặng, không tự
chốt hộ giá trị/chi phí (đó là quyền GO của bạn).

---

## 5. Bàn giao sang skill giai đoạn kế (KHÔNG tự làm inline — nguyên tắc #8)

Sau khi cụm 1/1 trả lời xong và CASE-1 lên `confirmed`, Trụ 1 đóng. Stage kế là **Product
Clarity (Trụ 2)** — GĐ1–5 (Business Case đầy đủ → Product Discovery → Requirements → PRD →
Domain Model). Skill chuyên trách chuỗi đầu này là **`/idea`** (nó tự dẫn GĐ0→GĐ5 rồi DỪNG
ở Domain). Partner giữ tổng thể + traceability, không chép lại việc của `idea`.

```
═══ BÀN GIAO → idea — Trụ 1→2 · Business Case → Domain (GĐ1–5) ═══
Đầu vào đã có: NEED-1, NEED-2 (business need + ràng buộc nền, trace NEED-1);
  success metric đo được sẵn (SM-1 +≥15đpt on-time sau 30 ngày; SM-2 ≥60% caregiver-link
  tuần đầu) → dùng thẳng khi làm PRD, đừng hỏi lại.
Việc của skill này: dẫn GĐ1 Business Case (đầy đủ) → GĐ2–4 Product/Requirements/PRD →
  GĐ5 Domain Model, rồi DỪNG ở Domain và bàn giao lên.
Điều kiện trước khi chạy: trả lời cụm 1/1 ở §3 để mình chốt CASE-1 = confirmed và đóng Trụ 1.
→ Bạn chạy: /idea. Xong quay lại đây, mình lật gate Trụ 1, kiểm Domain rồi đẩy sang Trụ 3
  (Choose Architecture → /shape).
════════════════
```

> TUYỆT ĐỐI không nhảy ý→code: từ business need này tới bất kỳ dòng code nào còn cách tối
> thiểu Trụ 2 (product/PRD/domain) → Trụ 3 (shape → stack → live slice qua `/frame`).
> Partner sẽ chỉ ghi khung slice + `/frame` ở Trụ 3, không viết code.

---

## 6. State máy (`pipeline-state.json` — bản sẽ ghi khi chạy thật)

```json
{
  "schema_version": 1,
  "project": "mediremind",
  "mode": "greenfield",
  "current_pillar": 1,
  "current_stage": "Business Need",
  "feasibility": {
    "business": "Đáng giải rõ: quên liều ở người già + bệnh mạn tính là nỗi đau đo được; caregiver ở xa đang 'mù'. Ẩn số: ai trả tiền / vì sao BÂY GIỜ / độ lớn giá trị chưa có số.",
    "product": "JTBD rõ (khai báo thuốc+lịch · nhắc + xác nhận 'đã uống' từ thông báo · adherence + chia sẻ chỉ-xem). Success metric đã có ngưỡng đo được (SM-1, SM-2) — không phải đoán.",
    "technical": "Khả thi cao, KHÔNG life-critical, đội mạnh TS. Ẩn số kỹ thuật (60s timeliness, dữ liệu sức khoẻ nhạy cảm) thuộc các trụ sau, chưa chạm ở Trụ 1.",
    "unknowns": [
      "U-1: Vì sao là BÂY GIỜ (cửa sổ thời điểm cụ thể)?",
      "U-2: Giá trị ước lượng thô = con số/khoảng nào?",
      "U-3: Chi phí/khung thời gian MVP thô = bao nhiêu tuần/người?",
      "U-4: (treo, Trụ 4) retention dữ liệu sức khoẻ giữ bao lâu — chạm NFR-4."
    ]
  },
  "open_questions": [
    { "id": "OQ-1", "stage": "Business Need", "q": "Vì sao là BÂY GIỜ? Cửa sổ cụ thể nào khiến đáng làm lúc này?", "leverage": "high", "status": "open" },
    { "id": "OQ-2", "stage": "Business Need", "q": "Giá trị ước lượng thô = con số/khoảng nào (số patient mục tiêu, hoặc %adherence kỳ vọng)?", "leverage": "high", "status": "open" },
    { "id": "OQ-3", "stage": "Business Need", "q": "Chi phí/khung thời gian MVP thô = bao nhiêu tuần với mấy người?", "leverage": "high", "status": "open" }
  ],
  "decisions": [
    { "id": "NEED-1", "stage": "Business Need", "pillar": 1, "status": "confirmed",
      "decision": "Xây MediRemind: app nhắc uống thuốc + đo adherence cho patient uống 3–8 loại thuốc/ngày; caregiver theo dõi chỉ-xem từ xa.",
      "rationale": "Nỗi đau quên liều ở người già + bệnh mạn tính là có thật và đo được; caregiver ở xa hiện chỉ gọi điện hỏi, không có bức tranh tin cậy.",
      "rejected_alternatives": [], "traces_to": [] },
    { "id": "NEED-2", "stage": "Business Need", "pillar": 1, "status": "confirmed",
      "decision": "Ràng buộc nền: KHÔNG life-critical (ghi rõ 'không dùng cho cấp cứu'); dữ liệu thuốc = dữ liệu sức khoẻ nhạy cảm → security/kiểm-soát-truy-cập là ràng buộc bắt buộc từ business, không phải tính năng thêm.",
      "rationale": "Định vị đúng mức rủi ro (không phải hệ cứu người) tránh over-engineering; đồng thời khoá security-first vì dữ liệu sức khoẻ có rủi ro pháp lý (nguyên tắc #11).",
      "rejected_alternatives": [], "traces_to": ["NEED-1"] },
    { "id": "CASE-1", "stage": "Business Case", "pillar": 1, "status": "assumed",
      "decision": "MediRemind đáng làm về ROI thô — CHỜ validate bằng why-now + giá-trị-thô + chi-phí-thô (cụm 1/1).",
      "rationale": "", "rejected_alternatives": [], "traces_to": ["NEED-1"] }
  ],
  "handoffs": [
    { "to": "idea", "slice": "Business Case → Domain (GĐ1–5)",
      "framing_ref": "NEED-1,NEED-2 + SM-1/SM-2",
      "ac_refs": [], "non_scope": ["Clinic admin (ngoài MVP)", "dùng cho cấp cứu", "caregiver sửa lịch (chỉ-xem)"],
      "returned": false }
  ],
  "updated_at": "2026-07-03T00:00:00Z"
}
```

---

## 7. Trạng thái gate (suy ra, không lưu mảng riêng)

- **Trụ 1 · Business Alignment:** ĐANG MỞ. Đã có: bài-toán-rõ + ai-đau (NEED-1), ràng-buộc
  nền/security (NEED-2). Còn thiếu để đóng: why-now, giá-trị-thô, chi-phí-thô (CASE-1 lên
  `confirmed`). → chờ cụm 1/1.
- Trụ 2–5: chưa mở (cold-start, đúng con trỏ ở Trụ 1).
