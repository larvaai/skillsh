# Rubric — chấm một bản chạy skill `backlog` (GĐ9 · Roadmap & Backlog Decomposition)

Mỗi tiêu chí 0/1/2. Chuẩn gốc để chấm = `backlog/SKILL.md` + `quy-trinh-idea-to-operate.md` mục "Giai đoạn 9". Rubric chỉ biến hợp đồng đó thành thước đo — KHÔNG thêm tiêu chuẩn mới. 7 tiêu chí; 1–3 là XƯƠNG SỐNG (gate): rớt (=0) một cái là RỚT cả bản, dù tổng cao.

**Đầu vào để chấm (fixture):** bản backlog (Roadmap + Epic→Feature→Story→AC) cần chấm · Live Slice Report GĐ8 (nguồn chính) + PRD GĐ4 + Domain GĐ5

## 1. ĐÚNG + ĐỦ ARTIFACT (xương sống)

Sinh đủ ba artifact GĐ9: **Roadmap** (theme × release) + **Backlog** phân rã (Epic→Feature→Story→AC) + **Release Plan**. AC nằm DƯỚI story/feature dạng Given/When/Then; Definition of Done tách khỏi AC (chỉ tham chiếu GĐ11, không định nghĩa lại).
- 0 — thiếu một artifact bắt buộc; HOẶC story release gần nhất không có AC; HOẶC AC bị viết thành PRD/danh mục yêu cầu tầng trên; HOẶC DoD trộn vào AC; HOẶC cây phân rã sai tầng (Epic → Task, thiếu Feature/Story ở giữa).
- 1 — đủ ba artifact nhưng một chỗ mỏng: vài story thiếu AC, hoặc Release Plan chỉ một dòng/thiếu lý do thứ tự, hoặc AC thiếu Given/When/Then chuẩn.
- 2 — đủ ba, cây Epic→Feature→Story→AC đúng tầng, AC là hành vi kiểm được dưới story, DoD tách riêng (trỏ GĐ11).

## 2. ĐỌC-ĐƯỢC 3 TẦNG — lãnh đạo + dev (xương sống)

Mở bằng Góc nhìn lãnh đạo (Roadmap 1 trang + business value/trạng thái mỗi epic, ngôn ngữ nghiệp vụ, không jargon), RỒI mới chi tiết đủ cho dev (story có AC cụ thể + task thô + Test ref). Cả gói scan 2–3 phút.
- 0 — nhảy thẳng vào story/AC/task kỹ thuật, không có tầng lãnh đạo; Roadmap/Epic mở bằng jargon; CTO không scan ra "xây gì / vì gì / tới đâu"; HOẶC chỉ có roadmap mà dev đọc story+AC vẫn không đủ để `frame` một slice.
- 1 — có cả hai tầng nhưng lệch: Roadmap đọc được nhưng vài Epic mở bằng chi tiết kỹ thuật; hoặc AC quá mơ hồ để code; đọc được nhưng phải hỏi thêm.
- 2 — Roadmap + mỗi Epic mở bằng business value nghiệp vụ; rồi story+AC đủ cho dev hành động ngay; một trang, scan được.

## 3. BÁM NGUỒN — dùng artifact GĐ trước, không bịa (xương sống)

Epic/feature/story/AC dẫn từ Live Slice Report (GĐ8) + PRD (GĐ4) + Domain (GĐ5), không tự chế nhu cầu mới. AC phản ánh business rule bất biến từ Domain. "Giả định đã đổi" ở GĐ8 được phản ánh vào backlog. Nguồn hợp lệ = artifact GĐ trước ĐÃ qua cổng HOẶC input ngoài user cung cấp KÈM cảnh báo ⚠️; dùng input ngoài mà THIẾU cảnh báo → trừ điểm (không minh bạch nguồn); vẫn CẤM bịa cái user không đưa.
- 0 — đặt ra feature/rule ngoài scope PRD đã chốt, mâu thuẫn Domain/Live Slice; bịa vision để lấp chỗ Domain còn treo; bỏ qua/không dùng Live Slice Report; hoặc chọn lại kiến trúc/stack/domain (lấn GĐ trước).
- 1 — bám nguồn phần lớn nhưng 1 chỗ suy đoán không gắn nhãn, hoặc bỏ qua giả định "đã phải đổi" mà Live Slice nêu.
- 2 — mọi story/AC truy ngược được về Live Slice + PRD + Domain; slice đã chạy (GĐ8) thành feature đầu R1; scope in/out tôn trọng PRD; chỗ Domain treo ghi thành open question thay vì bịa story.

## 4. ĐỦ-LÀ-ĐỦ — độ sâu theo rủi ro, không thủ tục thừa

- 0 — phân rã đều tay bất kể rủi ro: viết hàng loạt story cho cả R2/R3 khi Domain chưa rõ (cầu toàn), HOẶC ngược lại bỏ mỏng/bỏ hẳn một phần bắt buộc của release gần nhất cho "gọn".
- 1 — phần lớn cân đúng, 1–2 chỗ lệch (release xa phân rã quá chi tiết, hoặc story rủi ro cao chỉ 1 AC sơ sài).
- 2 — release gần nhất phân rã tới story+AC, release xa chỉ theme+epic; số AC tỉ lệ rủi ro; mỗi quyết định lớn có lý do 1 dòng; không thủ tục thừa, không bỏ tầng.

## 5. TRACEABILITY — nối GĐ trước ↔ sau

- 0 — cây phân rã đứt rõ: story không quy về được epic/business objective; AC rời khỏi story; không nối lên Live Slice/Domain cũng không nối xuống task/test ref.
- 1 — nối được nhưng đứt một mắt mà không ghi rõ chỗ đứt (thiếu Test ref, hoặc Epic không ghi business value để lần ngược objective).
- 2 — chuỗi liền: Business Objective → Theme → Epic → Feature → Story → AC → Task → Test ref; AC nối business rule Domain; story đầu tiên nhận diện được là Live Slice GĐ8; chỗ đứt (nếu có) ghi rõ thay vì bịa nối.

## 6. CỔNG + PHÂN VAI đúng (A5)

- 0 — không có cổng go/no-go; HOẶC AI tự tuyên bố pass thay user; HOẶC gán sai người duyệt; HOẶC lấn vai (chọn stack, chia module, viết code/DoD chi tiết, viết Test Case chi tiết).
- 1 — có cổng nhưng câu hỏi chung chung, hoặc thiếu bước AI duyệt / phân vai duyệt (PO + Tech lead) không rõ, hoặc lấn vai nhẹ.
- 2 — cổng đúng câu GĐ9 ("đủ để lập kế hoạch delivery & phân module chưa?"), Chủ sở hữu = PO / Người duyệt = PO + Tech lead; AI trình đánh giá + rủi ro, chỉ rõ phần thiếu khi NO-GO, để user quyết — không tự pass; vai sạch.

## 7. BÀN GIAO đúng skill kế (modules · GĐ10)

- 0 — không có khối bàn giao; hoặc chỉ trỏ sai bước kế (không phải `modules`); hoặc tự chọn hộ user; hoặc tự ghi artifact vào repo code không xin phép.
- 1 — có bàn giao nhưng thiếu lối rẽ (chỉ `modules`, quên `frame` khi build story, hoặc quên đường quay lại `idea`/`partner` khi Domain treo), hoặc thiếu đường dẫn artifact / ghi state sai chỗ.
- 2 — khối bàn giao liệt kê `/modules` (GĐ10, mặc định) + `/frame` (build một story R1) + đường quay lại GĐ5 khi Domain còn treo; chỉ liệt kê để user quyết; state ghi vào `pipeline/`, không vào repo code trừ khi user đồng ý.

## Gate

Tiêu chí 1, 2, 3 là xương sống. Bất kỳ cái nào = 0 → bản **RỚT gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Một bản 12/14 nhưng bịa story ngoài scope (tiêu chí 3 = 0), hoặc AC thành PRD (tiêu chí 1 = 0), hoặc không ai phía lãnh đạo đọc nổi (tiêu chí 2 = 0), là backlog không dùng được — đội khách hàng sẽ lập kế hoạch sai. Khi so nhiều bản: loại hết bản rớt gate trước, rồi mới xếp theo tổng (tối đa 14).

## Khung report (xếp nhiều bản cạnh nhau)

```text
BẢN <id> — backlog
1 Đúng+đủ artifact (gate) : _/2   <1 dòng>
2 Đọc-được 3 tầng (gate)  : _/2   <1 dòng>
3 Bám nguồn (gate)        : _/2   <1 dòng>
4 Đủ-là-đủ                : _/2   <1 dòng>
5 Traceability            : _/2   <1 dòng>
6 Cổng + phân vai         : _/2   <1 dòng>
7 Bàn giao                : _/2   <1 dòng>
TỔNG: _/14   GATE: PASS | RỚT (tiêu chí #)
Điểm mạnh nhất : <1 dòng>
Sửa trước tiên : <1 dòng>
```

## Vì sao các tiêu chí này

Ba tiêu chí gate đo *có ra đúng thứ + đọc được + trung thực không*; các tiêu chí sau đo *có đúng kỷ luật pipeline không* (đủ-là-đủ, không lấn vai, cổng/traceability, bàn giao). Gộp lại = trọn hợp đồng của `backlog`, không hơn. Thêm một tiêu chí mới chỉ khi có một kiểu lỗi thật lặp lại mà bộ hiện tại không bắt được.
