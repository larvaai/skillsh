# HexAgent (clean rebuild) — Master Index của gói rebuild

> Đây là **cửa vào** cả gói `rebuild-hex-agent/`. Đọc file này trước, rồi đi theo link tới từng artifact.
> Gói được dựng qua pipeline **Idea→Operate** ở chế độ **tự-quyết** (không hỏi approval; mỗi cổng có người-duyệt-đóng-vai tự quyết + ghi lý do). Ngôn ngữ: tiếng Việt; định danh code để nguyên tiếng Anh.

---

## ── GÓC NHÌN LÃNH ĐẠO (đọc 90 giây — không cần biết code) ──

**HexAgent là gì.** Bạn giao cho nó **một mục tiêu** (ví dụ "viết file X và một file ghi độ dài của X"). Nó **tự lập kế hoạch**, chia mục tiêu thành các bước có thứ tự, **giao cho các sub-agent** làm, và **chỉ báo "xong" khi mọi tiêu chí nghiệm thu được chứng minh bằng bằng chứng THẬT** — không phải "agent tự nói xong là xong".

**Nhu cầu nó giải.** Khi bạn để một AI tự chạy nhiều bước (gọi model, đọc/ghi file, nhờ agent con làm hộ), thứ đáng sợ không phải nó làm sai, mà là nó **làm sai ở chỗ bạn không nhìn thấy và không tua lại được** — hoặc **báo-xong-khống**, hoặc **chạy mãi đốt tiền**. HexAgent biến chuỗi "giao task → tự plan → delegate → chỉ dừng khi xong" đó thành thứ **xem lại được (audit), chặn được, tua lại được, và không rò bí mật** — nhờ hai chốt an toàn đối nhau: một chốt bắt "chỉ xong khi đủ bằng chứng", một chốt bắt "cắt cứng khi hết ngân sách / không tiến triển".

**Đã rebuild qua pipeline nào.** Gói này KHÔNG phải code chạy được — nó là **bộ thiết kế + kế hoạch có traceability** chạy trọn 15 giai đoạn Idea→Operate: từ đọc-hiểu bản gốc (atlas) → định hình kiến trúc (shape) → chọn stack → chứng minh live-slice → chia backlog/module → chuẩn delivery → nghiệm thu (uat) → go-live (ship) → vận hành (operate), có soi lỗ hổng (review) và đóng khung slice đầu (frame). **Trạng thái thật lúc chốt:** pipeline HOÀN CHỈNH-VỀ-HÌNH (mọi giai đoạn có artifact + cổng GO), nhưng **CHƯA HOÀN CHỈNH-VỀ-CHẠY-THẬT** — live-slice GĐ8 mới đóng-khung (0/9 tick), R3 multi-agent (lõi điểm bán) chưa build, nên **M1/M2/M3 chưa tuyên**. GĐ13 đã GO nhưng chỉ cho **alpha nội bộ, write-tool + delegation TẮT**.

**Một câu cho người dựng nền:** HexAgent = *hexagonal microkernel* (nhân đông cứng, session sống) + *event-log-first control plane* + một *vòng lặp task* dừng-bằng-bằng-chứng-thật và chặn-runaway bằng budget/guards. Ba trụ đó là bất biến; mọi thứ khác là để làm ba trụ đó an toàn.

---

## Cây artifact — mỗi file một link

### 00 · Nền hiểu biết (đọc trước mọi thứ)
- [`00-understanding/REBUILD-BRIEF.md`](00-understanding/REBUILD-BRIEF.md) — **anchor chung**: tên sản phẩm, domain entity, **7 invariant chịu lực**, roadmap epic. Mọi stage đọc file này đầu tiên.
- [`00-understanding/ATLAS.md`](00-understanding/ATLAS.md) — **bản đồ hiểu biết** bản GỐC (§1–§15): kiến trúc, bounded context, domain model, TRACE vòng đời một task, risk & unknown. Nền dùng chung để các stage khỏi quét lại.
- [`00-understanding/evidence-A-core-loop.md`](00-understanding/evidence-A-core-loop.md) — bằng chứng gốc **vòng lặp lõi** (plan→order→delegate→finish), anchor `file:line`.
- [`00-understanding/evidence-B-domain-architecture.md`](00-understanding/evidence-B-domain-architecture.md) — bằng chứng gốc **domain & kiến trúc** (kernel, chokepoint, 3 seam, control plane).
- [`00-understanding/evidence-C-roadmap.md`](00-understanding/evidence-C-roadmap.md) — bằng chứng gốc **roadmap** (E01–E21, 17 invariant, clone-from-scratch 7 phase).

### Pipeline Idea→Operate (GĐ05 → GĐ14)
- [`pipeline/05-idea-domain.md`](pipeline/05-idea-domain.md) — **GĐ0–5 Idea→Domain**: Business/PRD/Domain Model (5 domain-rule lõi).
- [`pipeline/06-shape.md`](pipeline/06-shape.md) — **GĐ6 Shape**: Architecture Brief + C4 + Security Model (STRIDE) + 6 ADR.
- [`pipeline/07-stack.md`](pipeline/07-stack.md) — **GĐ7 Stack**: Tech Decision Matrix + 7 ADR (Python 3.11 · LangGraph · SQLite); SPIKE-1 treo.
- [`pipeline/08-skeleton.md`](pipeline/08-skeleton.md) — **GĐ8 Skeleton (cổng đắt #1)**: Live Slice Report `finish-by-evidence-tối-thiểu` — E2E 9+1 chặng, **0/9 tick** (chưa dựng thật).
- [`pipeline/09-backlog.md`](pipeline/09-backlog.md) — **GĐ9 Backlog**: Roadmap + Story/AC (R1 + R3 lõi M1/M2/M3).
- [`pipeline/10-modules.md`](pipeline/10-modules.md) — **GĐ10 Modules**: Module Map + Contract (6 module · 6 owner · 2 seam công khai).
- [`pipeline/11-delivery.md`](pipeline/11-delivery.md) — **GĐ11 Delivery**: Delivery Standards + DoD (9 dòng + 5 invariant-test D1–D5).
- [`pipeline/12-uat.md`](pipeline/12-uat.md) — **GĐ12 UAT**: Test & Verification (26/28 PASS, 2 PENDING R3); sign-off có điều kiện.
- [`pipeline/13-ship.md`](pipeline/13-ship.md) — **GĐ13 Ship (cổng đắt #2)**: Go/No-Go + Runbook + Rollback — **GO alpha nội bộ**, write/delegation OFF (CTO+PO ✔).
- [`pipeline/14-operate.md`](pipeline/14-operate.md) — **GĐ14 Operate**: Ops Dashboard + Metric; business "đạt MỘT PHẦN"; vòng đóng về GĐ9.

### Kiểm soát & giải thích (đọc-được-3-tầng)
- [`pipeline/_traceability.md`](pipeline/_traceability.md) — **Tháp kiểm soát**: soi cả 15 GĐ, chỉ chỗ thiếu/treo, trạng thái cổng. Panel cho CEO/CTO.
- [`review/REVIEW.md`](review/REVIEW.md) — **Rà soát lỗ hổng thiết kế**: 12 gap (3 Critical: cross-AC-evidence · loop-stuck · redact-before-write). Xương sống 7-invariant KHÔNG gãy.
- [`frame/slice-01-taskloop-happy-path.md`](frame/slice-01-taskloop-happy-path.md) — **Đóng khung slice đầu**: happy-path lõi (task→plan→order→delegate→judge→FINISHED + 1 guard budget), 8 AC đo được, resume tách ra slice-02.
- [`explain/EXPLAIN.md`](explain/EXPLAIN.md) — **Bản giải thích overview** (file này sinh ra): kể theo thang phóng-to, vấn đề → ý tưởng cốt lõi → luồng như câu chuyện → module. Đọc nếu muốn HIỂU hệ trước khi đọc thiết kế.

*State JSON kèm mỗi stage nằm cùng `pipeline/` (`shape.json`, `stack.json`, …, `_index.json`, `_traceability.json`, `_review.json`, `_frame.json`) — dành cho máy đọc, không cần đọc tay.*

---

## Bảng trạng thái pipeline (GĐ / artifact / cổng)

```
Đang ở: GĐ14 Operate (vòng đóng về GĐ9 /backlog)
Cổng đắt: [GĐ8 live slice: ✗ CHƯA PASS 0/9]  [GĐ13 go/no-go: ✓ GO-alpha có điều kiện]
```

| GĐ | Artifact | Cổng | Ghi chú |
|---|---|---|---|
| 00 | ATLAS (nền, 7 invariant) | ✓ GO | understanding L4, scope partial |
| 0–5 | Idea→Domain | ✓ GO×4 | 5 domain-rule lõi; done-handoff |
| 6 | Architecture Brief + C4 + 6 ADR | ✓ GO | có Security Model + STRIDE |
| 7 | Tech Decision Matrix + 7 ADR | ✓ GO | Python 3.11 · LangGraph · SQLite; **SPIKE-1 treo** |
| **8** | **Live Slice Report** (đắt) | **✗ NO-GO-pass** | **0/9 tick · staging=null** (chỉ GO cho "dựng-slice") |
| 9 | Roadmap + Backlog (Story/AC) | ✓ GO | R1 + R3 lõi có AC (M1/M2/M3) |
| 10 | Module Map + Contract | ✓ GO | 6 module · 6 owner · 2 seam |
| 11 | Delivery Std + DoD | ✓ GO | DoD 9 dòng + D1–D5 invariant-test |
| 12 | Test & Verification | ~ GO-có-ĐK | 26/28 PASS · **2 PENDING R3** · sign-off có-ĐK |
| **13** | **Go/No-Go + Runbook + Rollback** (đắt) | **✓ GO** | **alpha nội bộ, write/delegation OFF** · CTO+PO ✔ |
| 14 | Ops Dashboard + Metric | ~ GO | business "đạt **MỘT PHẦN**"; nhiều ô "chưa có số" |

`✓`=đủ/qua cổng · `~`=đủ-artifact-nhưng-điều-kiện-treo (hợp lệ) · `✗`=cổng chưa pass.

**Thiếu lớn nhất (một câu):** không thiếu artifact — mà thiếu **bằng-chứng-chạy-thật cho lõi**: (a) live slice GĐ8 chưa dựng, (b) R3 multi-agent chưa build → M1/M2/M3 chưa tuyên, (c) SPIKE-1 resume chưa xanh. Cả ba đã đổ về `/backlog` (I-1/I-2/I-3). **Không mắt xích traceability nào đứt** — vấn đề là độ chín thực thi, không phải lỗ hổng thiết kế.

---

## Cách đọc gói này

**Bạn là lãnh đạo / muốn nắm 3 phút:** đọc "Góc nhìn lãnh đạo" ở đầu mỗi file. Bắt đầu ở [`explain/EXPLAIN.md`](explain/EXPLAIN.md) (hiểu hệ) → [`pipeline/_traceability.md`](pipeline/_traceability.md) (đang ở đâu, cổng nào chưa qua).

**Bạn muốn HIỂU hệ làm gì / chạy thế nào:** [`explain/EXPLAIN.md`](explain/EXPLAIN.md) — kể theo thang phóng-to (vấn đề → ý tưởng cốt lõi → luồng → module), không cần đọc code.

**Bạn là CTO/kiến trúc sư dựng lại:** đọc theo thứ tự [`00-understanding/REBUILD-BRIEF.md`](00-understanding/REBUILD-BRIEF.md) → [`00-understanding/ATLAS.md`](00-understanding/ATLAS.md) → [`pipeline/06-shape.md`](pipeline/06-shape.md) → [`pipeline/10-modules.md`](pipeline/10-modules.md) → [`pipeline/11-delivery.md`](pipeline/11-delivery.md).

**Bạn là dev sắp gõ code:** [`frame/slice-01-taskloop-happy-path.md`](frame/slice-01-taskloop-happy-path.md) (slice đầu, 8 AC đo được) — cùng đọc [`pipeline/10-modules.md`](pipeline/10-modules.md) (contract) + [`pipeline/11-delivery.md`](pipeline/11-delivery.md) (DoD).

**Bạn muốn biết còn lỗ hổng / rủi ro gì:** [`review/REVIEW.md`](review/REVIEW.md) (12 gap, 3 Critical) + phần "risk & unknown" §12 của ATLAS.

**Quy ước 3 tầng:** mỗi artifact mở bằng **"Góc nhìn lãnh đạo"** (1–3 điều nghiệp vụ, không jargon) rồi mới tới chi tiết cho dev — đọc phần đầu là đủ nắm; xuống sâu khi cần build.
