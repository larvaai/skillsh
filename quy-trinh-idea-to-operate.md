# Quy trình phát triển phần mềm doanh nghiệp — Idea → Operate

> Từ **một ý tưởng** đến **vận hành**, một luồng duy nhất, có thứ tự chuẩn.
> Mỗi giai đoạn để lại **đúng một artifact một trang** mà CEO/CTO đọc trong vài phút là **hiểu và quản lý được**.
> Nguyên tắc sống còn: **viết đủ để ra quyết định, không viết để làm dày hồ sơ.**

Tài liệu này là **playbook chi tiết** đứng sau skill `partner`. `partner` điều phối luồng theo rủi ro; tài liệu này định nghĩa **từng giai đoạn, từng artifact, từng cổng** một cách cụ thể để cả công ty dùng chung. Đây là **bản nguồn** trước khi đúc thành skill.

---

## Mục lục

- [Phần A — Bản đồ & nguyên tắc](#phần-a--bản-đồ--nguyên-tắc)
- [Phần B — 15 giai đoạn (template + ví dụ)](#phần-b--15-giai-đoạn)
  - GĐ 0 Idea Intake · GĐ 1 Business · GĐ 2 Product · GĐ 3 Requirements · GĐ 4 PRD
  - GĐ 5 Domain · GĐ 6 Architecture · GĐ 7 Tech Stack · GĐ 8 Live Slice
  - GĐ 9 Backlog · GĐ 10 Module · GĐ 11 Delivery · GĐ 12 Verify · GĐ 13 Release · GĐ 14 Operate
- [Phần C — Sợi xuyên suốt](#phần-c--sợi-xuyên-suốt)
- [Phần D — Phụ lục: Bảng điều khiển cho CEO/CTO](#phần-d--phụ-lục)

---

# Phần A — Bản đồ & nguyên tắc

## A1. Bản đồ tổng thể (đúng thứ tự)

```text
0  Idea Intake          → Idea Brief
1  Business Discovery    → Business Case            ── WHY
2  Product Discovery     → Product Brief            ── WHAT VALUE
3  Requirements          → Requirement Catalogue    ── WHAT EXACTLY
4  PRD                   → PRD (bản đồng thuận)
5  Domain Model          → Domain Model             ── WORLD MODEL
6  Solution Architecture → Architecture Brief        ── SHAPE
7  Tech Stack / Framework→ Tech Decision Matrix      ── TOOLS
8  Live Slice            → Live Slice Report         ── PROOF
9  Roadmap & Backlog     → Roadmap + Epic→Feature→Story→AC ── PLAN
10 Module & Team Ownership→ Module Map + Contracts
11 Delivery / Implementation → Delivery Standards + DoD ── BUILD
12 Verification / UAT    → Test & Verification Report
13 Release Readiness     → Go/No-Go + Runbook        ── SHIP
14 Operations & Measure  → Ops Dashboard             ── LEARN → quay lại 9
```

Một câu cho mỗi tầng quyết định:

```text
Business   quyết  WHY            — vì sao đáng làm
Product    quyết  WHAT VALUE     — user cần trải nghiệm gì để tạo giá trị đó
Domain     quyết  WORLD MODEL    — hệ thống mô phỏng thế giới nghiệp vụ nào
Architecture quyết HOW SHAPED    — hệ thống có hình hài gì
Tech stack quyết  WITH WHAT      — dựng bằng công cụ nào
Backlog    quyết  WHAT FIRST     — xây gì trước
Engineering quyết HOW SAFELY     — giao hàng an toàn thế nào
Operations quyết  RUN & IMPROVE  — vận hành và cải tiến ra sao
```

## A2. Mô hình ghi nhớ (bản ngắn nhất để cả công ty thuộc)

```text
1 WHY    Business need · pain · value · metric
2 WHO    User · stakeholder · operator · owner
3 WHAT   PRD · requirement · scope · behavior
4 WORLD  Domain · entity · rule · event · data
5 SHAPE  Architecture · boundary · module · integration
6 TOOLS  Framework · language · infra · vendor
7 PROOF  Live slice · spike · prototype
8 PLAN   Roadmap · epic · feature · story · AC
9 BUILD  Implementation · PR · CI/CD · test
10 SHIP  UAT · go-live · rollback · support
11 LEARN Metrics · incident · feedback · next iteration
```

## A3. Bảy nguyên tắc bất biến về thứ tự (vi phạm là sai)

```text
1. PRD đứng TRƯỚC backlog chi tiết.    (Không viết story hàng loạt khi PRD chưa rõ.)
2. Architecture đứng TRƯỚC framework.  (Không chọn Next/Nest/Spring/Django trước khi biết NFR.)
3. Domain đứng TRƯỚC module.            (Không chia module khi chưa hiểu domain boundary.)
4. Live slice đứng TRƯỚC build full.    (Không dựng cả hệ trước khi một lát cắt chạy thật.)
5. Monitoring + rollback đứng TRƯỚC release. (Không release khi chưa quan sát/lùi được.)
6. AC nằm DƯỚI story/feature, KHÔNG thay thế requirement/PRD.
7. Database schema KHÔNG phải domain model. (Entity là khái niệm có identity + lifecycle.)
```

Lỗi kinh điển mà 7 nguyên tắc này chặn: **build quá sớm, chọn framework quá sớm, chia module sai domain, viết story không có business traceability, và release khi chưa sẵn sàng vận hành.**

## A4. Giữ cho THỰC TẾ — chống bureaucracy (đọc kỹ)

Đây là **một luồng duy nhất** cho mọi việc — không chia tier. Nó nhanh được là nhờ **kỷ luật về độ sâu**, không nhờ bỏ bớt giai đoạn. Năm đòn bẩy:

```text
1. ĐỦ-LÀ-ĐỦ (Definition of Enough)
   Mỗi giai đoạn có một mức "đủ để ra quyết định kế tiếp". Đạt mức đó là ĐI.
   Sửa một dòng config: Idea Brief + một dòng note kiến trúc có thể là đủ;
   nhiều giai đoạn rút lại còn một đoạn văn. Sản phẩm mới: làm đầy đủ.
   => Cùng một luồng, độ sâu co giãn theo rủi ro, KHÔNG bỏ bước.

2. CÂN THEO RỦI RO, không theo số giai đoạn.
   Số trang một artifact tỉ lệ với ẩn số & rủi ro, không phải với vị trí trong luồng.

3. CỔNG NHẸ — 1 người duyệt, 1 câu hỏi go/no-go.
   Cổng là một quyết định của một người chịu trách nhiệm, KHÔNG phải hội đồng.

4. CHẠY SONG SONG có chủ đích (xem Phần C). Tuần tự chỉ ở những chỗ nguyên tắc A3 cấm đảo.

5. ARTIFACT LÀ CÔNG CỤ TƯ DUY, không phải thủ tục.
   Một trang, scan trong 2–3 phút. Nếu một artifact không đổi được quyết định nào,
   nó đang thừa — cắt.
```

Câu thử mỗi artifact: *"Bỏ artifact này đi thì có quyết định nào ở giai đoạn sau bị mù không?"* Không → cắt. Có → giữ, nhưng chỉ viết phần làm hết mù.

## A5. Phân vai (ai giữ quyền gì)

```text
CEO / Sponsor        : giữ WHY & ngân sách. Ký Business Case, ký Go/No-Go.
Product Owner        : giữ WHAT VALUE & scope. Sở hữu Product Brief, PRD, Backlog.
CTO / Kiến trúc sư   : giữ SHAPE & rủi ro kỹ thuật. Sở hữu Architecture, Tech, chuẩn delivery.
Team owner (mỗi module): giữ contract & chất lượng module mình. Sở hữu code + test + vận hành.
```

Quy ước nền (khớp skill `frame`/`partner`): **người giữ vai chủ chốt giữ Scope / Boundary / Acceptance / quyết định GO**; người thực thi làm Plan / Build / Verify. Mỗi giai đoạn có **đúng 1 Chủ sở hữu** (viết artifact) và **đúng 1 Người duyệt** (mở cổng). Mọi quyết định lớn ghi kèm **lý do + phương án đã loại (rejected alternatives)** để sau này audit được.

## A6. Cách đọc mỗi giai đoạn (cấu trúc cố định)

Mỗi giai đoạn ở Phần B đều có 7 ô giống nhau, để đọc nhanh:

```text
Mục tiêu (1 câu)        — giai đoạn này trả lời câu hỏi gì.
Chủ sở hữu / Người duyệt — ai viết / ai mở cổng.
Chạy song song với      — giai đoạn nào có thể làm cùng lúc.
Artifact (template)     — khung điền sẵn, copy là dùng.
Ví dụ — Case Management — bản đã điền, dùng một case xuyên suốt cả tài liệu.
Đủ-là-đủ                — khi nào coi như xong để đi tiếp (chống cầu toàn).
Góc nhìn lãnh đạo       — ĐÚNG MỘT thứ CEO/CTO nhìn để biết on-track & quản lý.
Cổng                    — câu hỏi go/no-go + người duyệt.
```

> **Case xuyên suốt:** Hệ thống **Quản lý Hồ sơ Khách hàng (Customer Case Management)**.
> Mục tiêu kinh doanh gốc: **giảm 40% thời gian xử lý hồ sơ** (từ 12 phút xuống ~7 phút).
> Cùng một case đi qua cả 15 giai đoạn, để bạn thấy artifact nối nhau thế nào.

---

# Phần B — 15 giai đoạn

---

## Giai đoạn 0 — Idea Intake (TIẾP NHẬN)

**Mục tiêu:** Ghi nhận ý tưởng đủ rõ để quyết định *có đáng phân tích sâu không*. Chưa phân tích, chưa công nghệ.
**Chủ sở hữu / Người duyệt:** Người đề xuất / Sponsor (hoặc CTO).
**Chạy song song với:** —

### Artifact: Idea Brief

```text
IDEA BRIEF — <tên ý tưởng>                          Ngày: __  Người đề xuất: __  Sponsor: __
- Ý tưởng là gì? (1–2 câu)
- Vấn đề đang gặp là gì?
- Ai bị ảnh hưởng? (nhóm người dùng / phòng ban)
- Kết quả mong muốn? (1 câu)
- Vì sao làm bây giờ?
- Ràng buộc đã biết: deadline / budget / pháp lý / dependency / vendor
- Loại: [ ] sản phẩm mới  [ ] module mới  [ ] cải tiến hệ cũ
```

### Ví dụ — Case Management

```text
IDEA BRIEF — Case Management Platform               Ngày: 01/03  Người đề xuất: Trưởng phòng Vận hành  Sponsor: COO
- Ý tưởng: Một màn hình thống nhất để nhân viên tạo, xét duyệt, theo dõi hồ sơ khách hàng.
- Vấn đề: Hồ sơ rải rác qua email + 3 file Excel; trung bình 12 phút/hồ sơ, hay sót bước.
- Ai bị ảnh hưởng: ~40 nhân viên vận hành, 8 reviewer, bộ phận audit.
- Kết quả mong muốn: Giảm mạnh thời gian xử lý và sai sót, có vết audit đầy đủ.
- Vì sao bây giờ: Lượng hồ sơ tăng 30%/quý, quy trình thủ công sắp vỡ.
- Ràng buộc: Go-live trước mùa cao điểm Q4; phải tuân thủ PDPA; tích hợp hệ CRM hiện có.
- Loại: [x] sản phẩm mới
```

**Đủ-là-đủ:** Nửa trang, ~10 phút. Trả lời được "ai đau, đau gì, muốn gì". KHÔNG bàn giải pháp/công nghệ.
**Góc nhìn lãnh đạo:** Một đoạn đọc trong 2 phút — *vấn đề + ai bị ảnh hưởng + vì sao bây giờ*. Đủ để nói "đào sâu" hay "để sau".
**Cổng:** *Có đáng đưa vào Business Discovery không?* — duyệt bởi Sponsor/CTO.

---

## Giai đoạn 1 — Business Discovery (WHY)

**Mục tiêu:** Xác định ý tưởng này **có đáng làm không** — bằng con số, không phải cảm tính. Chưa bàn "build thế nào".
**Chủ sở hữu / Người duyệt:** BA / Product Owner — duyệt bởi **CEO/Sponsor**.
**Chạy song song với:** User research (GĐ 2 sớm).

### Artifact: Business Case (1 trang)

```text
BUSINESS CASE — <tên>
1. Problem Statement     : Đau ở đâu? ai đau? đau bao lâu rồi?
2. Hiện trạng            : Quy trình đang chạy thế nào (as-is, ngắn).
3. Chi phí của vấn đề    : Không làm thì mất gì? (tiền / giờ / rủi ro — có số).
4. Cơ hội                : Làm xong tăng doanh thu / giảm chi phí / giảm rủi ro / tăng năng suất?
5. Stakeholder map       : Ai quyết · ai dùng · ai vận hành · ai bị ảnh hưởng.
6. Business rules bắt buộc: Quy tắc nghiệp vụ không được phá.
7. Ràng buộc             : Budget · pháp lý · dữ liệu · security · timeline · vendor · integration.
8. Success metrics       : Thành công đo bằng chỉ số nào + target.
9. Risk register v0      : Rủi ro business / pháp lý / vận hành / adoption / kỹ thuật.
10. Scope in / out v0    : Làm gì · KHÔNG làm gì (sơ bộ).
```

### Ví dụ — Case Management

```text
BUSINESS CASE — Case Management Platform
1. Problem      : Xử lý hồ sơ thủ công, 12 phút/hồ sơ, ~6% sai sót, không có vết audit.
3. Chi phí      : 40 NV × 60 hồ sơ/ngày × 5 phút lãng phí ≈ 200 giờ/ngày; rủi ro phạt PDPA khi lộ dữ liệu.
4. Cơ hội       : Giảm 40% thời gian xử lý; giảm sai sót về <1%; audit-ready.
5. Stakeholders : Quyết = COO · Dùng = NV vận hành + Reviewer · Vận hành = IT Ops · Ảnh hưởng = Audit, Legal.
6. Business rules: Reviewer không tự duyệt hồ sơ mình tạo; hồ sơ thiếu chứng từ bắt buộc không được duyệt.
8. Success      : (a) Avg handling time 12'→≤7'  (b) Error rate <1%  (c) 100% hồ sơ có audit log.
9. Risks        : Adoption (NV ngại đổi), PDPA, di trú dữ liệu từ Excel, tích hợp CRM.
10. Scope       : IN = intake/review/approve/audit. OUT = thanh toán, chấm điểm tín dụng.
```

**Đủ-là-đủ:** 1 trang. Có **ít nhất một success metric đo được** và **chi phí-không-làm bằng số**. Đó là cái CEO ký.
**Góc nhìn lãnh đạo:** Ba thứ — *success metric + chi phí nếu không làm + 3 rủi ro lớn nhất*. Đủ để duyệt ngân sách.
**Cổng:** *Đáng đầu tư đi tiếp không?* — duyệt bởi CEO/Sponsor.

---

## Giai đoạn 2 — Product Discovery (WHAT VALUE)

**Mục tiêu:** Biến nhu cầu kinh doanh thành **hướng sản phẩm**: user cần trải nghiệm gì để tạo ra giá trị đó.
**Chủ sở hữu / Người duyệt:** Product Owner — duyệt bởi **PO + CTO**.
**Chạy song song với:** UX exploration; bắt đầu phác requirement (GĐ 3).

### Artifact: Product Brief

```text
PRODUCT BRIEF — <tên>
- Personas / user segment : ai dùng, vai trò, quyền.
- Journey AS-IS           : luồng hiện tại (đau ở đâu).
- Journey TO-BE           : luồng mong muốn.
- Use case chính          : danh sách (3–7).
- Job-to-be-done (JTBD)   : khi __ tôi muốn __ để __.
- MVP hypothesis          : lát giá trị nhỏ nhất đáng ship.
- Feature candidates      : ứng viên (chưa cam kết).
- Out-of-scope            : rõ ràng KHÔNG làm.
- Product metrics         : activation / retention / conversion / time-saved / error-reduction.
- Adoption plan           : training · change management · kháng cự dự kiến.
```

### Ví dụ — Case Management

```text
PRODUCT BRIEF — Case Management
- Personas    : Case Creator (NV vận hành) · Case Reviewer · Auditor (chỉ đọc).
- AS-IS       : nhận yêu cầu qua email → điền Excel → gửi reviewer qua chat → cập nhật tay.
- TO-BE       : tạo case trên 1 màn hình → tự định tuyến reviewer → trạng thái + audit tự ghi.
- Use case    : tạo case · tìm/lọc case · giao reviewer · duyệt/từ chối · xem lịch sử trạng thái.
- JTBD        : "Khi có yêu cầu khách, tôi muốn mở & theo dõi hồ sơ ở một chỗ để xử lý nhanh, không sót."
- MVP         : Tạo case + tìm/lọc theo trạng thái + duyệt/từ chối + audit log. (Chưa cần SLA tự động.)
- Out-of-scope: báo cáo BI nâng cao, app mobile, tích hợp thanh toán.
- Metrics     : time-to-create <60s · % hồ sơ xử lý đúng hạn · error-rate · weekly active reviewers.
- Adoption    : 2 buổi training; champion mỗi tổ; chạy song song Excel 2 tuần rồi cắt.
```

**Đủ-là-đủ:** 1–2 trang. **MVP nêu rõ** và **đo bằng product metric nào**. Out-of-scope viết ra giấy.
**Góc nhìn lãnh đạo:** *MVP là gì + đo bằng metric nào + cái gì cố tình KHÔNG làm.* Đây là nơi exec chặn scope creep.
**Cổng:** *Hướng sản phẩm & MVP đủ rõ chưa?* — duyệt bởi PO + CTO.

---

## Giai đoạn 3 — Requirements Engineering (WHAT EXACTLY)

**Mục tiêu:** Chuẩn hoá requirement và **tách tầng** rạch ròi (đây là chỗ nhiều công ty làm sai vì trộn lẫn).
**Chủ sở hữu / Người duyệt:** BA / PO — duyệt bởi **PO + Tech lead**.
**Chạy song song với:** Domain Discovery (GĐ 5) có thể bắt đầu phác.

Tách 8 tầng — không trộn:

```text
Business Requirement → Stakeholder Requirement → User Requirement → Product Requirement
→ System Requirement → Software Requirement → Non-functional Requirement → Acceptance Criteria
```

### Artifact: Requirement Catalogue + NFR + Traceability seed

```text
REQUIREMENT CATALOGUE — <tên>
ID     | Tầng        | Phát biểu                                  | Nguồn (Business obj) | AC ref
R-001  | User        | ...                                         | BO-1                 | AC-001
...
NFR LIST
ID     | Loại        | Yêu cầu đo được
NFR-01 | Performance | P95 < 500ms với 10.000 hồ sơ
NFR-02 | Security    | RBAC; mọi hành động ghi audit log bất biến
...
BUSINESS RULES   : liệt kê rule bất biến.
DATA REQUIREMENTS: dữ liệu cần lưu · chủ sở hữu · retention · migration.
INTEGRATION      : hệ nào · API/Event nào · dependency nào.
COMPLIANCE       : PDPA/GDPR · audit · retention.
```

### Ví dụ — Case Management (một chuỗi tầng)

```text
Business Req     : Giảm 40% thời gian xử lý hồ sơ khách hàng.
Stakeholder Req  : NV vận hành xem được trạng thái mọi hồ sơ trên MỘT màn hình.
User Req         : Người dùng tìm hồ sơ theo mã KH, trạng thái, ngày tạo.
Product Req      : Trang Case Management có filter + search + status timeline.
System Req       : Backend expose GET /cases (pagination, filter, permission check).
NFR              : P95 < 500ms với 10.000 hồ sơ; uptime 99.9%; mọi truy cập ghi audit.
Acceptance Crit  : Given user có quyền Case Viewer, When lọc trạng thái "Pending",
                   Then chỉ hiển thị hồ sơ Pending mà user được phép xem.
```

**Đủ-là-đủ:** Đủ requirement quan trọng + **NFR có con số** + cột nguồn (traceability). KHÔNG cần 100% — đủ để không build mù.
**Góc nhìn lãnh đạo:** *Bảng NFR có số* (P95, uptime, security, compliance) + danh mục requirement nhóm theo business objective. NFR là nơi rủi ro kỹ thuật & chi phí nằm.
**Cổng:** *Requirement & NFR đủ rõ để viết PRD chưa?*

---

## Giai đoạn 4 — PRD (cầu nối đồng thuận)

**Mục tiêu:** Một tài liệu **nối Business · Product · Tech · Design · QA · Security · Ops** về cùng một hiểu biết. PRD đứng **trước** backlog chi tiết.
**Chủ sở hữu / Người duyệt:** Product Owner — duyệt bởi **Product + Business + Tech (3 chữ ký)**.
**Chạy song song với:** —  (đây là điểm hội tụ; nên có trước khi rẽ sang Domain/Architecture)

PRD theo tinh thần **agile**: tạo *shared understanding* + bám *customer need* + còn *linh hoạt*, KHÔNG phải spec cứng 100%.

### Artifact: PRD (1–3 trang, 14 mục — co giãn theo rủi ro)

```text
PRD — <tên>                                    Trạng thái: Draft/Approved   Phê duyệt: PO · Biz · Tech
1. Context              : vì sao làm · vấn đề · ai bị ảnh hưởng.
2. Goals                : business goal · product goal · user goal.
3. Success metrics      : metric trước / sau · target cụ thể.
4. Users / Personas     : ai dùng · role · permission.
5. Scope                : in · out · future.
6. User journey / flow  : luồng hiện tại → mong muốn.
7. Functional req       : feature · use case · rule · edge case.
8. Non-functional req   : performance · security · privacy · availability · scalability · observability · a11y · maintainability.
9. Data requirements    : lưu gì · ai sở hữu · retention · migration.
10. Integration         : hệ nào · API · event · dependency.
11. Analytics/tracking  : event cần track · dashboard.
12. Rollout plan        : pilot · beta · full · rollback.
13. Risks / assumptions : giả định · rủi ro · cách validate.
14. Open questions      : những thứ chưa quyết.
```

### Ví dụ — Case Management (rút gọn)

```text
PRD — Case Management Platform v1                Trạng thái: Approved (PO ✔ · COO ✔ · CTO ✔)
2. Goals       : Biz = giảm 40% handling time · Product = xử lý hồ sơ trên 1 màn hình · User = không sót bước.
3. Metrics     : handling time 12'→≤7' · error <1% · 100% có audit log. Đo qua dashboard tuần.
5. Scope       : IN = intake/search/review/approve/audit · OUT = payment, BI, mobile · FUTURE = SLA tự động.
7. Functional  : tạo case · tìm/lọc · giao reviewer · duyệt/từ chối (chặn nếu thiếu chứng từ) · timeline.
8. NFR         : P95<500ms@10k · 99.9% uptime · RBAC + audit bất biến · log/metric/trace đầy đủ.
9. Data        : cases, attachments, status_history; chủ sở hữu = Team Case; retention 7 năm (PDPA).
12. Rollout    : pilot 1 tổ (2 tuần) → beta 50% → full; rollback = tắt feature flag, quay lại Excel.
14. Open Qs    : Quy tắc escalation quá hạn? (chốt ở GĐ 5) · Tích hợp CRM real-time hay batch? (GĐ 6)
```

**Đủ-là-đủ:** Đủ để Tech bắt đầu Solution Design — **không cần hoàn hảo 100%**, nhưng đủ để không build mù. Open questions được phép tồn tại nếu có chỗ chốt sau.
**Góc nhìn lãnh đạo:** *Goals (3 tầng) + Success metrics + Scope in/out + Rollout/rollback + Open questions.* Một tài liệu có 3 chữ ký = mọi bên đã đồng thuận.
**Cổng:** *PRD được Product + Business + Tech duyệt chưa?* → mở đường sang Domain & Architecture.

---

## Giai đoạn 5 — Domain Model (WORLD MODEL)

**Mục tiêu:** Mô hình hoá **thế giới nghiệp vụ** trước khi nghĩ tới schema hay code. Đi từ ngôn ngữ nghiệp vụ → entity/rule/event.
**Chủ sở hữu / Người duyệt:** Tech lead + PO (cùng làm) — duyệt bởi **CTO/Kiến trúc sư**.
**Chạy song song với:** Có thể bắt đầu cùng cuối GĐ 3.

Thứ tự đi: `Domain → Subdomain → Bounded Context → Use case → Workflow → Entity → Relationship → Aggregate → Domain Rule → Domain Event → Data Ownership`.

> **Quan trọng:** Entity **không phải** bảng database. Entity là **khái niệm nghiệp vụ có identity + lifecycle**. Nhảy thẳng PRD → DB schema là cách chắc chắn thiết kế sai domain (nguyên tắc A3-#7).

### Artifact: Domain Model

```text
DOMAIN MODEL — <tên>
Domain            : ...
Subdomains        : ...
Bounded Contexts  : ...                 (mỗi context = một ranh giới ngôn ngữ + sở hữu dữ liệu)
Entities          : ... (mỗi cái: identity + lifecycle)
Value Objects     : ...
Aggregates        : ... (gốc nhất quán giao dịch)
Domain Events     : ... (việc đã xảy ra, thì quá khứ)
Business Rules    : ... (bất biến của domain)
Data Ownership    : context nào sở hữu dữ liệu nào.
```

### Ví dụ — Case Management

```text
DOMAIN MODEL — Customer Case Management
Domain          : Customer Case Management
Subdomains      : Case Intake · Case Review · Case Approval · Notification · Audit
Bounded Context : Case Management (lõi)  |  Identity (ngoài)  |  Notification (ngoài)
Entities        : Case · Customer · Reviewer · Attachment · Comment · StatusHistory
Value Objects   : CaseStatus · CustomerCode · ReviewDecision · TimeRange
Aggregates      : Case (gốc) gom Attachment + Comment + StatusHistory
Domain Events   : CaseCreated · CaseSubmitted · CaseAssigned · CaseApproved · CaseRejected · CaseEscalated
Business Rules  : - Case không thể Approved nếu thiếu Attachment bắt buộc.
                  - Reviewer không được approve case do chính mình tạo.
                  - Case quá 7 ngày chưa xử lý → tự động Escalated.
Data Ownership  : Case Management sở hữu cases/attachments/status_history.
                  KHÔNG sở hữu: identity người dùng (Identity context), gửi thông báo (Notification).
```

**Đủ-là-đủ:** Các entity có **identity + lifecycle** rõ; các **business rule bất biến** liệt kê; các **domain event chính** đặt tên; ranh giới context + data ownership rõ. Chưa cần schema.
**Góc nhìn lãnh đạo:** *Danh sách bounded context + 5–7 business rule bất biến + ai sở hữu dữ liệu nào.* Đây là "thế giới" hệ thống cam kết mô phỏng — sai ở đây là sai gốc.
**Cổng:** *Domain đủ rõ để định hình kiến trúc & ranh giới module chưa?*

---

## Giai đoạn 6 — Solution Architecture (SHAPE)

**Mục tiêu:** Quyết **hình hài hệ thống** từ Requirement + NFR + Domain. **Architecture trước, framework sau** (A3-#2).
**Chủ sở hữu / Người duyệt:** Kiến trúc sư / CTO — duyệt bởi **CTO** (+ Security review song song).
**Chạy song song với:** NFR clarification; Security/threat modeling; phác Tech spike (GĐ 7).

Thứ tự đúng: `Requirement + NFR + Domain → Architecture style → Principles → Integration pattern → Deployment model → (rồi mới) Framework`.

### Artifact: Architecture Brief + C4 + ADRs

```text
ARCHITECTURE BRIEF — <tên>
Bảng quyết định:
  Architecture style : modular monolith | microservices | event-driven | serverless ...
  Module boundary    : module nào sở hữu nghiệp vụ nào (bám bounded context GĐ 5).
  Data ownership     : DB chung | DB per service.
  Integration        : REST | GraphQL | event | queue | batch.
  Auth               : RBAC | ABAC | SSO | OAuth.
  Security           : threat model · data classification · audit.
  Reliability        : retry · timeout · circuit breaker · fallback.
  Performance        : caching · indexing · async.
  Observability      : log · metric · trace · alert.
  Deployment         : cloud | on-prem | hybrid.
  Compliance         : PDPA/GDPR · retention.
Sơ đồ: C4 Context + C4 Container + Data Flow + Integration.
ADRs : mỗi quyết định lớn 1 ADR (Quyết định · Bối cảnh · Lựa chọn · Phương án đã loại · Hệ quả).
```

### Ví dụ — Case Management

```text
ARCHITECTURE BRIEF — Case Management
Style       : Modular monolith (3 module: Case · Identity-adapter · Notification-adapter).
Boundary    : module Case sở hữu toàn bộ vòng đời case; tích hợp ra ngoài qua adapter.
Data        : một DB, schema-per-module, KHÔNG cross-module query trực tiếp.
Integration : REST cho UI; domain events nội bộ; CRM đồng bộ qua batch hằng đêm (chốt open-Q PRD).
Auth        : RBAC (Creator/Reviewer/Auditor/Admin) qua SSO công ty.
Security    : dữ liệu KH = "Confidential"; audit log bất biến (append-only); threat model STRIDE.
Reliability : retry + timeout cho CRM batch; ngoài giờ vẫn tạo case được (offline-tolerant intake).
Observability: structured log + RED metrics + trace; alert P95>500ms & error>1%.
Deployment  : cloud, 1 region, blue-green.
ADR-001 Modular monolith thay vì microservices (đội 6 người, 1 domain) — loại: microservices (quá tải vận hành).
ADR-002 Batch CRM thay vì real-time — loại: real-time (CRM rate-limit, không cần tức thời).
```

**Đủ-là-đủ:** Chọn được style + boundary + integration + auth/security + có **1 sơ đồ C4 Context** và **ADR cho mỗi quyết định lớn (kèm phương án đã loại)**. Sơ đồ vẽ tay cũng được.
**Góc nhìn lãnh đạo:** *Một sơ đồ C4 Context + bảng quyết định kiến trúc + danh sách ADR có lý do & cái đã loại.* Đọc ADR là biết "vì sao hệ thống có hình này" — quản lý được rủi ro mà không cần đọc code.
**Cổng:** *Architecture đủ vững để chọn stack & dựng live slice chưa?*

---

## Giai đoạn 7 — Tech Stack / Framework Selection (TOOLS)

**Mục tiêu:** Chọn framework/stack **sau khi** đã biết domain complexity, NFR, integration, team skill, deployment, security, time-to-market. Framework chỉ là **tool hiện thực cái shape** đã chốt.
**Chủ sở hữu / Người duyệt:** Kiến trúc sư / Tech lead — duyệt bởi **CTO**.
**Chạy song song với:** Lập kế hoạch live slice (GĐ 8).

### Artifact: Tech Decision Matrix + ADR (+ spike nếu cần)

```text
TECH DECISION MATRIX — <hạng mục, vd: Backend framework>
Tiêu chí               | Trọng số | Candidate A | Candidate B | Candidate C
Fit với domain         |   ...    |    điểm     |     ...     |    ...
Fit với team (đã biết?)|   ...    |
Fit với scale (NFR)    |   ...    |
Fit enterprise (auth/audit/log/monitor) |
Fit testing (unit/integration/e2e/contract) |
Fit hiring             |
Fit ecosystem/vendor/cloud |
Fit maintainability (2 năm nữa) |
TỔNG                   |          |
=> Chọn: ___  ·  Lý do: ___  ·  Đã loại & vì sao: ___
ADR-00x: ghi quyết định.  Spike result (nếu rủi ro cao): ___
```

### Ví dụ — Case Management

```text
TECH DECISION MATRIX — Backend framework
Tiêu chí (trọng số)     | NestJS | Spring Boot | Django
Fit domain (module rõ)  |   5    |     5       |   3
Fit team (đã biết)      |   5    |     2       |   3
Fit NFR (P95<500ms)     |   4    |     5       |   4
Fit enterprise (auth/audit) | 4  |     5       |   4
Fit testing             |   5    |     4       |   4
Fit hiring (thị trường) |   4    |     4       |   4
TỔNG (có trọng số)      |  27    |    25       |  22
=> Chọn: NestJS · Lý do: team thạo TS, module/DI rõ, test tốt, đủ NFR.
   Đã loại: Spring (đội chưa thạo, lên chậm); Django (mô hình module kém rõ cho case này).
ADR-003: Chọn NestJS + PostgreSQL + Prisma. Spike: dựng GET /cases với 10k bản ghi → P95 ~210ms (đạt).
```

**Đủ-là-đủ:** Ma trận tiêu chí **có điểm** + 1 ADR + (nếu rủi ro cao) **kết quả spike thực đo**. Không chọn theo "đang hot".
**Góc nhìn lãnh đạo:** *Bảng so sánh 1 trang + lý do chọn + cái gì đã loại và vì sao.* Quyết định công cụ truy vết được, không cảm tính.
**Cổng:** *Stack đã chốt, sẵn sàng dựng live slice?*

---

## Giai đoạn 8 — Live Slice / Walking Skeleton (PROOF)

**Mục tiêu:** Trước khi build full, dựng **một lát cắt sống end-to-end chạy thật** để validate architecture + stack + boundary + delivery. **Live slice trước build full** (A3-#4).
**Chủ sở hữu / Người duyệt:** Tech lead + 1–2 dev — duyệt bởi **CTO**.
**Chạy song song với:** Hoàn thiện Design system & API contract draft.

Lát cắt phải xuyên hết các tầng: `UI → API → Domain logic → DB → Auth → Logging → Test → CI/CD → Deploy staging → Monitoring`. **Không phải mockup — phải chạy thật.**

### Artifact: Live Slice Report

```text
LIVE SLICE REPORT — <tên slice>
Slice            : tính năng nhỏ end-to-end là gì.
Đường đi (E2E)   : UI → API → domain → DB → auth → log → test → CI/CD → staging → monitor.
Link staging     : URL chạy thật.
Đã validate      : [ ] architecture hợp lý [ ] framework phù hợp [ ] module boundary ổn
                   [ ] auth chạy [ ] DB schema hợp lý [ ] CI/CD chạy [ ] test strategy thực tế
                   [ ] observability đủ (log/metric/trace) [ ] team hiểu flow delivery.
Giả định đã đổi  : điều gì trong PRD/Architecture cần chỉnh sau khi chạy thật.
Rủi ro kiến trúc còn lại : ...
```

### Ví dụ — Case Management

```text
LIVE SLICE REPORT — "Tạo một Case mới"
Slice  : User login → mở form Create Case → submit → backend validate → tạo Case (Draft)
         → lưu DB → emit CaseCreated → ghi audit log → trả mã case → UI hiện trạng thái.
Link   : https://staging.internal/case-app  (tài khoản demo: creator01)
Validate: [x] modular monolith ổn  [x] NestJS hợp  [x] boundary Case/Identity rõ
          [x] SSO chạy  [x] schema cases/status_history hợp lý  [x] CI/CD xanh
          [x] unit + 1 integration pass  [x] có log + RED metric + trace  [x] team chạy được full flow.
Giả định đổi : cần thêm field `source_channel` cho audit (PRD chưa có) → bổ sung requirement.
Rủi ro còn lại: tải đồng thời khi nhiều reviewer — sẽ kiểm ở perf test (GĐ 12).
```

**Đủ-là-đủ:** Slice **chạy thật trên staging**, có **test + log/metric/trace**, và checklist "đã validate" tick đủ các ô rủi ro cao. Đây là **cổng quan trọng nhất** trước khi đổ người vào.
**Góc nhìn lãnh đạo:** *Một link staging chạy được + checklist validate + danh sách giả định đã phải đổi.* Bằng chứng "kiến trúc & stack này thật sự chạy" trước khi tiêu phần lớn ngân sách.
**Cổng:** *Live slice pass chưa?* — **Pass mới được scale ra nhiều module/feature.**

---

## Giai đoạn 9 — Roadmap & Backlog Decomposition (PLAN)

**Mục tiêu:** Phân rã từ chiến lược xuống việc làm được, **đúng thứ tự** và có business traceability. AC nằm **dưới** story/feature (A3-#6).
**Chủ sở hữu / Người duyệt:** Product Owner — duyệt bởi **PO + Tech lead**.
**Chạy song song với:** Module ownership (GĐ 10).

Cây phân rã: `Company Strategy → Business Objective → Product Goal → Roadmap Theme → Initiative → Epic → (Capability nếu rất lớn) → Feature → User Story → AC → Engineering Task → Test Case`.

> Theo SAFe: **Feature** mô tả functionality tạo business value, size vừa một Program Increment; team **split feature thành stories** để code/integrate/test/demo. Scrum: **backlog refinement** là việc liên tục để chia nhỏ & làm rõ item.

### Artifact: Roadmap + Backlog (Epic → Feature → Story → AC)

```text
ROADMAP            : Theme × Release (3–4 cột thời gian), mỗi ô vài epic.
BACKLOG ITEM
  Epic     : <tên> — business value — trạng thái.
  Feature  : <tên> — thuộc epic — value — size.
  Story    : "Là <role>, tôi muốn <hành động>, để <giá trị>."
  AC       : Given/When/Then (mỗi story 1–N AC).
  Tasks    : các engineering task.
  Test ref : TC-...
```

### Ví dụ — Case Management

```text
ROADMAP
  Theme "Xử lý hồ sơ nhanh"  | R1 (MVP)            | R2                  | R3
                            | Intake & Review     | Search & SLA        | Reporting
Business Objective : Giảm 40% thời gian xử lý hồ sơ.
Product Goal       : Xử lý hồ sơ trên một màn hình thống nhất.
Initiative         : Case Management Platform.
Epic               : Case Intake & Review.
Feature            : Create Case.
User Story         : "Là NV vận hành, tôi muốn tạo hồ sơ khách hàng mới, để bắt đầu quy trình xét duyệt."
AC                 : Given tôi login quyền Case Creator,
                     When nhập đủ thông tin bắt buộc và Submit,
                     Then hệ thống tạo Case trạng thái Draft, ghi audit CaseCreated, hiển thị mã Case.
Engineering Tasks  : API POST /cases · Case aggregate · bảng cases · form Create Case · unit + integration test · audit log.
Test ref           : TC-CASE-CREATE-001
```

**Các tầng AC (doanh nghiệp lớn có thể nhiều tầng):**

```text
Feature AC : feature xong khi user tạo/sửa/xem/submit case được.
Story AC   : từng behavior Given/When/Then.
Release AC : được go-live khi pass UAT + security scan + perf test + có rollback plan.
Definition of Done: chuẩn chất lượng bắt buộc cho MỌI item (xem GĐ 11).
```

**Đủ-là-đủ:** Roadmap theme + epic/feature cho **release gần nhất** + story **có AC** cho sprint sắp tới. KHÔNG viết hàng loạt story khi PRD/Domain chưa rõ.
**Góc nhìn lãnh đạo:** *Roadmap 1 trang (theme × release) + bảng epic→feature gắn business value & trạng thái.* Thấy ngay "đang xây gì, vì giá trị gì, tới đâu".
**Cổng:** *Backlog đủ để lập kế hoạch delivery & phân module chưa?*

---

## Giai đoạn 10 — Module & Team Ownership (SỞ HỮU)

**Mục tiêu:** Chia module theo **domain boundary**, gán **owner** và **contract** — KHÔNG chia theo màn hình. **Domain trước module** (A3-#3).
**Chủ sở hữu / Người duyệt:** Kiến trúc sư + Eng managers — duyệt bởi **CTO**.
**Chạy song song với:** Backlog (GĐ 9), chuẩn delivery (GĐ 11).

Chia theo: `bounded context · data ownership · change frequency · team ownership · integration boundary · security boundary · operational responsibility`.

### Artifact: Module Map + Module Contract

```text
MODULE MAP : module × team owner × phụ thuộc (sơ đồ).
MODULE CONTRACT — <module>
  Owner            : team.
  Responsibilities : làm gì.
  Owns (data/event): bảng nào · event nào.
  Does NOT own     : ranh giới ra ngoài.
  Public API       : (mô tả bằng OpenAPI cho REST — chuẩn mô tả interface độc lập ngôn ngữ).
  Domain events    : phát ra / lắng nghe.
  Permission model : ai được gọi gì.
  Error codes      : mã lỗi công khai.
  SLA/SLO          : nếu cần.
  Test contract    : hợp đồng test với module gọi.
```

### Ví dụ — Case Management

```text
MODULE: Case Management            Owner: Team A
Responsibilities : tạo case · cập nhật case · theo dõi trạng thái · giao reviewer.
Owns             : bảng cases · vòng đời CaseStatus · event CaseCreated/CaseUpdated/CaseApproved...
Does NOT own     : gửi thông báo (Team Notification) · identity người dùng (Team Identity) · thanh toán.
Public API       : POST /cases · GET /cases · PATCH /cases/{id}/status  (đặc tả OpenAPI).
Domain events    : phát CaseCreated, CaseApproved; nghe (không có — lõi).
Permission       : Creator tạo · Reviewer duyệt · Auditor đọc · Admin cấu hình.
Error codes      : CASE_REQUIRED_ATTACHMENT_MISSING · CASE_SELF_REVIEW_FORBIDDEN.
Test contract    : Notification dựa trên event CaseApproved (contract test giữa 2 team).
```

**Đủ-là-đủ:** Mỗi module có **owner + contract + data ownership + dependency** rõ. Contract REST mô tả bằng OpenAPI.
**Góc nhìn lãnh đạo:** *Bản đồ module × team owner + cái mỗi module sở hữu / KHÔNG sở hữu.* Trả lời tức thì "ai chịu trách nhiệm cái gì khi có sự cố".
**Cổng:** *Ownership & contract rõ để các team chạy delivery song song?*

---

## Giai đoạn 11 — Delivery / Implementation (BUILD)

**Mục tiêu:** Build có kỷ luật, mọi thay đổi truy vết được. Bàn giao xuống skill `frame` cho từng slice.
**Chủ sở hữu / Người duyệt:** Team owner mỗi module — duyệt PR bởi **reviewer được chỉ định**.
**Chạy song song với:** Test strategy + CI/CD setup (bắt đầu từ GĐ 8).

### Artifact: Delivery Standards + Definition of Done + PR Checklist

```text
DELIVERY STANDARDS — chuẩn hoá 1 lần, áp cho mọi team:
  Repository · Branching · Coding standard · Review policy · Testing pyramid
  · CI/CD pipeline · Environment strategy · Secret management · Feature flag
  · Migration strategy · Observability standard · Incident process.

DEFINITION OF READY (item được phép vào sprint):
  có AC · ước lượng · phụ thuộc rõ · đủ context để bắt đầu.

DEFINITION OF DONE (item được coi là xong — bắt buộc mọi item):
  code review pass · test pass (unit+integration) · contract giữ · observability có
  · doc cập nhật · không giảm chất lượng · merge xanh CI. (Không đạt DoD → không release.)

PR CHECKLIST:
  [ ] link tới story/requirement   [ ] có test   [ ] breaking change? (đã thông báo)
  [ ] update API contract?         [ ] có migration?   [ ] security impact?
  [ ] observability (log/metric)?  [ ] ảnh hưởng module khác?   [ ] rollback plan nếu rủi ro cao?
```

### Ví dụ — Case Management (PR đã điền)

```text
PR #1832 — feat(case): POST /cases tạo case Draft
[x] link: Story "Create Case" / R-Product-Req Case page   [x] test: unit + integration
[ ] breaking change   [x] update OpenAPI (POST /cases)   [x] migration: thêm bảng cases
[x] security: input validation + audit log CaseCreated   [x] observability: log + metric created_total
[ ] ảnh hưởng module khác   [x] rollback: sau feature flag `case_create`
Reviewer: Tech lead Team A — DoD: ✔ tests xanh · ✔ contract giữ · ✔ doc cập nhật.
```

**Đủ-là-đủ:** DoR/DoD chốt + CI/CD chạy + PR checklist được áp dụng thật. Mỗi PR **link tới requirement/story** (sợi traceability).
**Góc nhìn lãnh đạo:** *Definition of Done (1 khối) + sức khoẻ giao hàng kiểu DORA bắt đầu được đo* (lead time · deployment frequency · change failure rate · recovery time). Exec không đọc code — đọc DoD + 4 chỉ số này.
**Cổng:** *Item đạt Definition of Done chưa?*

---

## Giai đoạn 12 — Verification / UAT (PROOF IT WORKS)

**Mục tiêu:** Chứng minh hệ làm đúng — không chỉ QA bấm UI. Mọi AC có test, có kết quả, truy vết được.
**Chủ sở hữu / Người duyệt:** QA lead — duyệt bởi **PO (UAT) + Security (security sign-off)**.
**Chạy song song với:** Implementation (test viết cùng code).

Các lớp test: `unit · integration · contract · e2e · regression · performance · security (SAST/DAST/pentest) · accessibility · UAT · operational readiness · DR/rollback (nếu hệ quan trọng)`.

### Artifact: Test & Verification Report (mapping)

```text
MAPPING (bắt buộc — không có là sau khó audit):
  Requirement → Acceptance Criteria → Test Case → Test Result → Release Decision
TEST & VERIFICATION REPORT
  Lớp test     | Phạm vi            | Pass/Fail | Ghi chú
  unit/integration/contract/e2e/perf/security/a11y/UAT ...
  UAT sign-off     : <PO> ngày __
  Security sign-off: <Sec> ngày __
```

### Ví dụ — Case Management

```text
MAPPING
  R: "User tìm hồ sơ theo trạng thái"
  → AC: chỉ thấy hồ sơ Pending user có quyền xem
  → TC-CASE-SEARCH-001
  → Result: PASS
  → Release: đủ điều kiện đưa vào v1.4.0
REPORT
  unit 312/312 · integration 48/48 · contract (Case↔Notification) PASS
  perf: P95 210ms @10k (đạt NFR<500ms) · security: SAST 0 high, DAST 0 high · a11y: WCAG AA pass
  UAT sign-off: PO ✔ (15/09) · Security sign-off: CISO ✔ (16/09)
```

**Đủ-là-đủ:** Mỗi AC có **test + kết quả**; có **UAT sign-off + security sign-off** cho release.
**Góc nhìn lãnh đạo:** *Bảng mapping requirement→test→result (tỷ lệ pass) + 2 chữ ký: UAT và Security.* Một trang biết "đã kiểm cái gì, còn hở gì".
**Cổng:** *Pass đủ điều kiện để go-live chưa?*

---

## Giai đoạn 13 — Release Readiness & Rollout (SHIP)

**Mục tiêu:** Go-live có **release readiness**, không phải "merge xong là deploy". **Monitoring + rollback trước release** (A3-#5).
**Chủ sở hữu / Người duyệt:** Release manager / Tech lead — duyệt bởi **CTO + PO (Go/No-Go)**.
**Chạy song song với:** Chuẩn bị comms & training.

### Artifact: Go/No-Go Checklist + Runbook + Rollback Plan

```text
GO / NO-GO CHECKLIST (mỗi dòng: owner + trạng thái)
  [ ] Release note         [ ] Deployment plan       [ ] Rollback plan (đã test nếu hệ quan trọng)
  [ ] Data migration plan  [ ] Feature flag plan      [ ] User communication
  [ ] Training material     [ ] Support playbook       [ ] Monitoring dashboard + alert rule
  [ ] Incident owner đã phân công   [ ] UAT + Security sign-off (từ GĐ 12)
ROLLOUT STRATEGY : internal alpha → pilot group → beta → gradual rollout → full.
RUNBOOK          : các bước deploy, kiểm tra sau deploy, cách rollback từng bước.
```

### Ví dụ — Case Management

```text
GO/NO-GO — Case Management v1.4.0
  [x] Release note (COO duyệt)   [x] Deploy plan (blue-green)   [x] Rollback đã test trên staging
  [x] Migration cases/status_history (forward + backward script)   [x] Feature flag `case_create`, `case_search`
  [x] Comms gửi 40 NV   [x] Training 2 buổi xong   [x] Support playbook   [x] Dashboard + alert P95/error
  [x] Incident owner: Tech lead Team A   [x] UAT ✔ · Security ✔
ROLLOUT : pilot Tổ 1 (2 tuần) → beta 50% → full. Rollback = tắt flag, quay lại Excel song song.
QUYẾT ĐỊNH: GO ✔ (CTO + COO, 20/09)
```

**Đủ-là-đủ:** Go/No-Go **được ký** + rollback **đã test** (với hệ quan trọng) + monitoring/alert đã bật + có người trực sự cố.
**Góc nhìn lãnh đạo:** *Một trang Go/No-Go — mỗi dòng có owner + trạng thái — kèm rollback plan & ai trực sự cố.* Đây là tài liệu CEO/CTO **ký để cho lên**.
**Cổng:** **GO / NO-GO.**

---

## Giai đoạn 14 — Operations & Measurement (LEARN → lặp)

**Mục tiêu:** Sau release dự án **chưa kết thúc**. Vận hành được, đo được, cải tiến được — và **đóng vòng** với Business Case ở GĐ 1.
**Chủ sở hữu / Người duyệt:** Ops/SRE + PO — review bởi **CEO/CTO theo nhịp**.
**Chạy song song với:** Quay lại GĐ 9 cho vòng kế.

### Artifact: Ops Dashboard + Incident & Iteration Loop

```text
OPS DASHBOARD — 4 nhóm chỉ số trên một màn hình:
  BUSINESS    : có giảm chi phí / tăng doanh thu / giảm thời gian xử lý? (so target GĐ 1)
  PRODUCT     : adoption · flow nào bị drop · feature nào không ai dùng.
  ENGINEERING : DORA — lead time · deployment frequency · change failure rate · recovery time.
  OPERATIONS  : error rate · latency · uptime · incident count · support tickets.
INCIDENT PROCESS : phát hiện → phân loại → owner → khắc phục → hậu kiểm.
ITERATION        : metric review theo nhịp → input cho roadmap kế (về GĐ 9).
```

### Ví dụ — Case Management

```text
OPS DASHBOARD — Case Management (sau 8 tuần)
  BUSINESS    : avg handling time 12'→7' (đạt mục tiêu -40%) · error 6%→0.8%.
  PRODUCT     : 38/40 NV active tuần · drop ở bước "đính kèm" 12% → cần cải thiện UX.
  ENGINEERING : lead time 2.1 ngày · deploy 4/tuần · change failure 6% · recovery 35 phút.
  OPERATIONS  : uptime 99.95% · P95 230ms · 1 incident (đã hậu kiểm) · 9 support tickets.
ITERATION   : đưa "cải thiện bước đính kèm" + "SLA tự động" vào roadmap R2 (về GĐ 9).
```

**Đủ-là-đủ:** Dashboard sống + nhịp review + **đường feedback rõ về roadmap** (GĐ 9). Business metric đối chiếu thẳng với mục tiêu gốc GĐ 1.
**Góc nhìn lãnh đạo:** *4 nhóm chỉ số trên một dashboard: Business (đạt mục tiêu gốc?) · Product (adoption) · Engineering (DORA) · Operations (uptime/incident).* Đây là chỗ vòng đời **đóng lại** với cái CEO đã ký ở GĐ 1.
**Cổng:** *Đạt mục tiêu chưa? Làm gì tiếp?* → mở vòng lặp mới tại GĐ 9.

---

# Phần C — Sợi xuyên suốt

## C1. Sợi traceability bắt buộc (xương sống của cả luồng)

Một item phải truy được từ **mục tiêu kinh doanh** xuống tới **chỉ số sau release** — và ngược lại. Đây là thứ khiến CEO/CTO **quản lý được** thay vì chỉ "tin tưởng".

```text
Business Objective → Product Goal → Requirement → PRD Section → Epic → Feature
→ Story → Acceptance Criteria → Test Case → Pull Request → Release → Metric
```

Ví dụ — một sợi đi hết, dùng case xuyên suốt:

```text
Business Objective : Giảm 40% thời gian xử lý hồ sơ.
Product Goal       : Xử lý hồ sơ trên một màn hình thống nhất.
Requirement        : User tìm kiếm hồ sơ theo trạng thái.
PRD Section        : Case Search & Filtering.
Epic               : Case Management.
Feature            : Case Search.
Story              : Search cases by status.
AC                 : Given chọn status Pending, Then chỉ thấy case Pending user có quyền xem.
Test Case          : TC-CASE-SEARCH-001.
Pull Request       : PR #1832 (và các PR liên quan).
Release            : v1.4.0.
Metric             : Average handling time giảm 12' → 7'.
```

Quy tắc tối thiểu: **mỗi PR link tới story; mỗi story thuộc feature; mỗi feature phục vụ một business objective.** Thiếu liên kết nào → không merge.

## C2. Security & Compliance đan qua mọi giai đoạn (không để cuối)

Trong doanh nghiệp lớn, security **không phải bước test cuối**. Theo OWASP SAMM, nó trải khắp vòng đời: Governance · Design · Implementation · Verification · Operations. Bảng "security cần làm ở từng phase":

```text
GĐ 1 Business     : data classification · rủi ro pháp lý/quy định.
GĐ 4 PRD          : privacy · permission · yêu cầu audit.
GĐ 6 Architecture : threat modeling · auth model · trust boundary.
GĐ 7 Framework    : sức khoẻ bảo mật của ecosystem · vá lỗi · dependency.
GĐ 8 Live slice   : auth · audit · logging · secret management chạy thật.
GĐ 11 Implement   : secure coding · dependency scan.
GĐ 12 Testing     : SAST · DAST · pentest (nếu cần).
GĐ 13 Release     : security checklist go-live.
GĐ 14 Operations  : monitoring · incident response.
```

## C3. Việc có thể chạy SONG SONG (tăng tốc mà không phá thứ tự)

```text
Business Discovery        ∥ User research
Product Discovery         ∥ UX exploration
Requirement drafting      ∥ Domain discovery
Architecture optioning    ∥ NFR clarification
Framework spike           ∥ Live slice planning
Design system             ∥ API contract draft
Test strategy             ∥ CI/CD setup
Security review           ∥ Architecture review
```

## C4. KHÔNG bao giờ đảo thứ tự (anti-patterns)

```text
✗ Chọn framework trước khi biết NFR.
✗ Chia module trước khi hiểu domain boundary.
✗ Viết story hàng loạt trước khi PRD đủ rõ.
✗ Build full system trước live slice.
✗ Release trước khi có monitoring & rollback.
✗ Coi AC là thay thế cho requirement/PRD.
✗ Coi database schema là domain model.
```

## C5. Sửa lại chuỗi "thường gặp" cho đúng

Chuỗi hay bị viết sai (chọn framework/architecture quá sớm, PRD/Story đặt cuối):

```text
SAI: Business → domain → entity → live slice → chọn framework → chọn architecture
     → chia module → PRD → Epic → Feature → Story → AC
```

Sửa thành (đây là thứ tự an toàn của tài liệu này):

```text
ĐÚNG: Business Need → Business Case → Product Discovery → Requirements → PRD
      → Domain → (Entity/Rule/Event/Bounded Context) → Architecture options → Choose Architecture
      → Choose Framework/Tech → Define Module Boundaries → Build Live Slice → Validate
      → Roadmap → Epic → (Capability nếu cần) → Feature → Story → AC → Task → Test
      → Implementation → Release → Operate → Measure → Iterate
```

Năm chỉnh lớn nhất:

```text
1. PRD phải nằm TRƯỚC backlog chi tiết.
2. Architecture phải nằm TRƯỚC framework.
3. Domain phải nằm TRƯỚC module.
4. Live slice phải nằm TRƯỚC build full-scale.
5. AC nằm DƯỚI story/feature — không thay thế PRD.
```

## C6. Công thức cuối — 5 thứ một quy trình enterprise tốt phải bảo đảm

```text
1. Business alignment    : làm đúng vấn đề có giá trị.
2. Product clarity       : biết user cần gì, success đo bằng gì.
3. Technical correctness : domain · architecture · module · framework đều có lý do.
4. Delivery control      : epic·feature·story·AC·test·PR·release có traceability.
5. Operational readiness : release xong chạy được · monitor được · support được · rollback được · cải tiến được.
```

Bản một câu để dán vào guideline:

```text
Từ một ý tưởng phần mềm, doanh nghiệp đi qua:
Idea → Business Discovery → Product Discovery → Requirements → PRD → Domain Model
→ Architecture → Tech Stack → Live Slice → Roadmap → Epic → Feature → Story → AC
→ Build → Test → Release → Operate → Measure.
```

---

# Phần D — Phụ lục

## D1. Bảng điều khiển Artifact (dùng cho CEO/CTO theo dõi cả pipeline)

Một bảng — đọc dọc là biết dự án đang ở đâu, ai chịu trách nhiệm, cổng kế tiếp là gì. Đây là **panel quản lý** của lãnh đạo.

| GĐ | Artifact | Chủ sở hữu | Người duyệt (cổng) | Góc nhìn lãnh đạo (nhìn 1 thứ) | Cổng go/no-go |
|----|----------|-----------|--------------------|--------------------------------|---------------|
| 0 | Idea Brief | Người đề xuất | Sponsor/CTO | Vấn đề + ai + vì sao bây giờ | Đáng phân tích sâu? |
| 1 | Business Case | BA/PO | CEO/Sponsor | Success metric + chi phí-không-làm + 3 rủi ro | Đáng đầu tư tiếp? |
| 2 | Product Brief | PO | PO+CTO | MVP + product metric + scope-out | Hướng SP đủ rõ? |
| 3 | Requirement Catalogue + NFR | BA/PO | PO+Tech lead | Bảng NFR có số (P95/uptime/security) | Đủ rõ để viết PRD? |
| 4 | PRD | PO | Product+Biz+Tech | Goals + metrics + scope + rollout + open Qs | 3 bên đã duyệt? |
| 5 | Domain Model | Tech lead+PO | CTO | Bounded context + rule bất biến + data ownership | Đủ rõ để định hình kiến trúc? |
| 6 | Architecture Brief + ADR | Kiến trúc sư | CTO | C4 Context + bảng quyết định + ADR (lý do/đã loại) | Đủ vững để chọn stack? |
| 7 | Tech Decision Matrix | Tech lead | CTO | Bảng so sánh + lý do chọn + cái đã loại | Stack chốt? |
| 8 | Live Slice Report | Tech lead | CTO | Link staging chạy + checklist validate | **Live slice pass?** |
| 9 | Roadmap + Backlog | PO | PO+Tech lead | Roadmap 1 trang + epic→feature có value | Đủ để lập kế hoạch? |
| 10 | Module Map + Contracts | Kiến trúc sư | CTO | Module × owner + sở hữu/không sở hữu | Ownership rõ? |
| 11 | Delivery Standards + DoD | Team owner | Reviewer | DoD + 4 chỉ số DORA | Item đạt DoD? |
| 12 | Test & Verification Report | QA lead | PO(UAT)+Security | Mapping req→test→result + 2 chữ ký | Đủ để go-live? |
| 13 | Go/No-Go + Runbook | Release mgr | CTO+PO | Go/No-Go 1 trang + rollback + trực sự cố | **GO / NO-GO** |
| 14 | Ops Dashboard | Ops/SRE+PO | CEO/CTO (nhịp) | 4 nhóm: Business/Product/Engineering/Ops | Đạt mục tiêu? Tiếp gì? |

**Hai cổng đậm (GĐ 8 và GĐ 13)** là hai cổng đắt nhất nếu bỏ qua: live slice (chứng minh trước khi đổ người) và go/no-go (chứng minh sẵn sàng vận hành trước khi cho lên).

## D2. Đủ-là-đủ — tham chiếu nhanh (để việc nhỏ đi nhanh)

Cùng một luồng, nhưng với việc nhỏ (sửa/cải tiến) nhiều giai đoạn rút còn vài dòng. Mức tối thiểu:

```text
GĐ 0  : 1 đoạn — vấn đề + kết quả mong muốn.
GĐ 1  : bỏ qua nếu đã rõ giá trị; ngược lại 3 dòng (metric + chi phí + rủi ro).
GĐ 3+4: gộp PRD-lite 1 trang nếu phạm vi nhỏ.
GĐ 5  : chỉ ghi rule/entity MỚI bị đụng tới.
GĐ 6+7: 1 ADR nếu có quyết định mới; không thì trỏ về ADR cũ.
GĐ 8  : bỏ nếu nằm trong slice đã chứng minh; có rủi ro mới thì spike nhỏ.
GĐ 9  : story + AC là bắt buộc, luôn có.
GĐ 11–13: DoD + PR checklist + rollback luôn bắt buộc, dù việc nhỏ.
GĐ 14 : luôn kiểm metric sau khi đổi.
```

Nguyên tắc: **cắt độ sâu, không cắt cổng an toàn.** Story/AC (GĐ 9), DoD (GĐ 11), test mapping (GĐ 12), rollback + monitoring (GĐ 13) **không bao giờ** bỏ — kể cả việc nhỏ.

## D3. Tổng hợp cổng (một chuỗi quyết định)

```text
0  Đáng phân tích sâu?          → Sponsor/CTO
1  Đáng đầu tư tiếp?            → CEO
2  Hướng sản phẩm đủ rõ?        → PO+CTO
3  Requirement đủ cho PRD?      → PO+Tech
4  PRD được 3 bên duyệt?        → Product+Biz+Tech
5  Domain đủ rõ cho kiến trúc?  → CTO
6  Kiến trúc đủ vững cho stack? → CTO
7  Stack chốt?                  → CTO
8  Live slice pass?  (đắt)      → CTO
9  Backlog đủ để plan?          → PO+Tech
10 Ownership rõ?                → CTO
11 Đạt Definition of Done?      → Reviewer
12 Đủ điều kiện go-live?        → PO(UAT)+Security
13 GO / NO-GO  (đắt)            → CTO+PO
14 Đạt mục tiêu? làm gì tiếp?   → CEO/CTO
```

## D4. Căn cứ chuẩn (để dẫn chiếu khi cần)

```text
ISO/IEC/IEEE 29148  : requirements engineering xuyên vòng đời; định nghĩa process,
                      information items & nội dung của chúng → nền cho Phần 3, 4 và traceability.
PRD (Atlassian)     : PRD định nghĩa mục đích/feature/behavior để align stakeholder; agile PRD
                      ưu tiên shared understanding + customer need + linh hoạt → nền GĐ 4.
SAFe                : Feature tạo business value, size vừa một PI; split thành stories → nền GĐ 9.
Scrum Guide         : backlog refinement liên tục; Definition of Done là chuẩn chất lượng của
                      Increment, không đạt thì không release → nền GĐ 9, 11.
OpenAPI             : chuẩn mô tả interface REST độc lập ngôn ngữ → nền module contract GĐ 10.
OWASP SAMM          : secure SDLC qua Governance/Design/Implementation/Verification/Operations → nền C2.
DORA                : lead time · deployment frequency · change failure rate · recovery time
                      (+ rework) đo software delivery performance → nền GĐ 11, 14.
```

## D5. Bước kế tiếp — đúc thành skill

Tài liệu này là **bản nguồn**. Khi đúc thành skill trong folder (cạnh `explain`/`frame`/`triage`/`partner`), nên giữ:

```text
- Một luồng, 15 giai đoạn, mỗi giai đoạn 1 artifact + 1 cổng.
- Cơ chế "đủ-là-đủ" (D2) để skill không làm chậm việc nhỏ.
- Vai & quyền (A5): user giữ Scope/Boundary/Acceptance/GO; skill làm plan/draft/điều phối.
- Bàn giao: tới GĐ 8 & 11 (build) → hand off sang `frame`; cần hiểu code cũ → trỏ `explain`.
- Trạng thái pipeline ghi ở state/project/<project>/ (khớp `partner`), chỉ đọc user-state.json.
- Bảng điều khiển D1 là output chính skill trình cho lãnh đạo mỗi lần báo cáo tiến độ.
```

---

*Hết. Một luồng — Idea → Operate. Mỗi giai đoạn một artifact đọc trong vài phút. Cắt độ sâu khi việc nhỏ, không bao giờ cắt cổng an toàn.*





