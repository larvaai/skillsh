⚠️ CẢNH BÁO — soi bằng đầu vào ngoài state
- Bức tranh dựng từ mô tả bạn gõ, KHÔNG phải state pipeline đã qua cổng. Tôi kiểm `state/project/hex_agent/` — chỉ có `ideas/` (GĐ0–5), KHÔNG có `pipeline/` (shape/stack/skeleton…). Nên "đã xong shape/stack/live slice" tôi tin theo LỜI bạn, chưa đọc được artifact đã gated.
- Rủi ro: (1) có thể có artifact thật bạn quên nêu; (2) "đã có/đã thiếu" chưa chắc khớp thực tế; (3) snapshot này chưa nối vào state.
- Vẫn báo theo mô tả của bạn. Muốn chính xác: để /shape /stack /skeleton ghi state pipeline rồi soi lại.

---

**Góc nhìn lãnh đạo:** Rebuild hex_agent (multi-agent microkernel — mọi call qua `execute_tool`, delegation cửa riêng, SQLite checkpoint, chạy trên LangGraph) đang ở **ranh GĐ8→GĐ9**. Cổng đắt số 1 — **GĐ8 Live Slice — theo bạn ĐÃ pass** (một lát cắt chạy thật), nên kiến trúc + stack coi như đã được thực tế bảo chứng. Cổng đắt số 2 — **GĐ13 go/no-go — CHƯA tới**. Thiếu lớn nhất ngay lúc này: **chưa có Backlog (Story/AC)** → mọi thứ sau nó đang mù, không biết xây-gì-trước. Chỗ ĐỨT nghiêm trọng nhất: **live slice đứng chơ vơ, không nối ngược được về Business Objective/Requirement nào** (vì GĐ9 chưa mở).

```
DASHBOARD — hex_agent            Đang ở: GĐ8→9 · Cổng đắt: [GĐ8 live slice: ✓ theo mô tả][GĐ13 go/no-go: chưa tới]
GĐ  Artifact                        Trạng thái   Skill      Cổng kế
0-5 Idea→Domain                     ✓ (mô tả)    /idea      —
6   Architecture Brief+ADR (shape)  ✓ (mô tả)    /shape     đủ vững chọn stack? ✓
7   Tech Decision Matrix (stack)    ✓ (mô tả)    /stack     stack chốt? ✓
8   Live Slice Report (đắt)         ✓ (mô tả)    /skeleton  live slice pass? ✓
9   Roadmap+Backlog (Story/AC*)     ✗            /backlog   đủ để plan?  ← ĐANG KẸT
10  Module Map+Contract             ✗            /modules   ownership rõ?
11  Delivery Std+DoD*               ✗            /delivery  đạt DoD?
12  Test&Verification (mapping*)    ✗            /uat       đủ go-live?
13  Go/No-Go+Runbook+Rollback* (đắt)✗            /ship      GO/NO-GO?
14  Ops Dashboard+Metric            ✗            /operate   đạt mục tiêu?
```
`✓`=đủ · `✗`=thiếu · `*`=never-skip (thiếu là báo dù việc nhỏ).

**Kiểm Sợi traceability — chỗ đứt:**
- **Live Slice (GĐ8) → Business Objective: ĐỨT.** Lát cắt đã chạy nhưng chưa có Story/AC/Feature nào phía trên để nó "chứng minh cho yêu cầu X" — GĐ9 chưa mở nên không truy ngược được. Đây là đứt do thiếu đầu vào GĐ sau, không phải rút gọn hợp lệ.
- **shape→stack→skeleton: liền** (nếu đúng như bạn mô tả, 3 mắt xích kiến trúc→công cụ→proof nối nhau).
- Chuỗi `Story → AC → Test Case → PR → Release → Metric` **chưa có mắt nào** — bắt đầu từ GĐ9 trở đi.

**Thiếu (ưu tiên) + nhắc skill:**
1. **Backlog: Roadmap + Story + AC — bắt buộc (never-skip).** Thiếu thì GĐ10–12 mù (không biết chia module theo feature nào, test map vào AC nào). → chạy **/backlog**. [đây là nút thắt — mở trước]
2. **Module Map + Contract.** hex_agent đã có ranh giới module rõ trong code (core/ delegation/ supervisor/ control/…), nhưng chưa có Contract (public API/event/ownership per team) để nhiều người xây song song không đạp nhau. → chạy **/modules** (sau backlog).
3. **Delivery Standards + Definition of Done — bắt buộc (never-skip).** → chạy **/delivery**.
4. **UAT test mapping — bắt buộc**; **Ship rollback + monitoring — bắt buộc**; **Operate metric.** → /uat → /ship → /operate, theo thứ tự, chưa vội.

**Cổng & security chưa đủ:**
- Cổng đang mở phải chốt: **GĐ9 "Backlog đủ để plan?"** (PO + Tech ký). Các cổng GĐ10–13 chưa tới.
- Security đan chuỗi (C2): threat model GĐ6 / secret GĐ8 — bạn chưa nêu, tôi để **"không rõ"** (đừng coi là đã-có). SAST/DAST GĐ12 + checklist GĐ13 còn trống vì các GĐ đó chưa mở.

```
═══ TRACEABILITY — hex_agent ═══
Đang ở: GĐ8→9   Cổng đắt: live slice ✓(mô tả) · go/no-go chưa tới
Thiếu ưu tiên: Backlog Story/AC (bắt buộc, đang kẹt) · Module Contract · DoD (bắt buộc)
→ Bổ sung Backlog: /backlog   (mở nút thắt trước tiên)
→ Bổ sung Module Map+Contract: /modules
→ Bổ sung Delivery Std+DoD: /delivery
→ Muốn được dẫn đi tiếp cả pipeline: /partner
→ Muốn chấm chất lượng một artifact đã có: /grade
════════════════
```
Tôi chỉ soi + nhắc, KHÔNG tự chạy skill nào hay tự làm giai đoạn. Bước hợp lý tiếp theo: chạy **/backlog** để gỡ nút thắt GĐ9.
