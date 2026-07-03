# GRADE — explain-pastebin · architecture-first (baseline yeu)

- contract_fidelity: 4/10
- stakeholder_comm: 3/10
- collaboration: 6/10
- gate: FAIL — RỚT GATE ở 2/3 rubric. (1) SKILL-RUBRIC: tiêu chí 1 (MỨC/thứ tự) = 0 vì mở đầu bằng thuật ngữ kiến trúc, đảo ngược thứ tự bắt buộc (vấn đề+cho ai bị đẩy xuống dưới, mở màn bằng "web-tier tách write-path/read-path... reverse proxy Web Server... SQL Master-Slave... MapReduce"). Đây đúng là "Câu mở SAI" mà SKILL.md cấm và trượt self-check câu 1. (2) STAKEHOLDER-COMM: tiêu chí 1 (VẤN ĐỀ+CHO AI đặt trước) = 0 — Gate fail; tiêu chí 2 (không jargon mồ côi) = 0 — hàng loạt thuật ngữ (web-tier, reverse proxy, Base 62, MD5, MapReduce, RPC, SQL Master-Slave, CDN, Object Store) thả trần trước khi neo. COLLAB-LEADERSHIP: QUA gate (TC1 và TC4 đều ổn) — không vượt quyền, kết bằng một cổng rõ.
- fix_first: Đảo lại thứ tự: đưa khối "Bây giờ mới nói công dụng" (dịch vụ kiểu Pastebin, người dùng ẩn danh dán text lấy link ngắn) và luồng "bạn ở đây" lên ĐẦU, để chúng đứng TRƯỚC mọi thuật ngữ kiến trúc; mỗi tên kỹ thuật (MD5, Base 62, MapReduce, reverse proxy...) chỉ được gọi sau khi đã neo vào một bước trong luồng — chỉ riêng việc lật khối này lên là gỡ được cả hai gate.

---

## Bối cảnh chung
Output là một overview `explain` chế độ overview, mức L2. SKILL.md quy định thứ tự BẮT BUỘC: Zoom 0–1 (vấn đề thực tế + CHO AI, bằng lời, KHÔNG thuật ngữ code) → Zoom 2 (bản đồ luồng "bạn ở đây") → Zoom 3 (module). Luật cứng: "Vấn đề trước, thuật ngữ sau — luôn luôn." Self-check câu 1: "Câu đầu tiên có phải là VẤN ĐỀ + CHO AI không? (Không được là thuật ngữ kiến trúc.)"

**Sự thật cấu trúc quyết định điểm:** output ĐẢO NGƯỢC thứ tự này. Nó mở bằng kiến trúc thuần ("Hệ thống này là một kiến trúc web-tier tách write-path/read-path, đặt sau một reverse proxy Web Server, với một SQL Database... SQL Master-Slave... MapReduce"), rồi liệt kê component (MD5, Base 62, Object Store, MapReduce), rồi API surface (REST/RPC), và MÃI về sau mới lộ công dụng — có hẳn câu dẫn "Bây giờ mới nói công dụng: đây là bản thiết kế của một dịch vụ kiểu Pastebin.com". Bản đồ luồng "bạn ở đây" đặt còn muộn hơn nữa.

---

## RUBRIC 1 — SKILL-RUBRIC (contract_fidelity) → 4/14, RỚT GATE

**TC1 MỨC (xương sống) = 0 → GATE FAIL.**
Bằng chứng: câu đầu là thuật ngữ kiến trúc ("một kiến trúc web-tier tách write-path/read-path"), đúng khuôn "Câu mở SAI" mà SKILL.md liệt kê ("Đây là một hệ multi-agent hexagonal/microkernel..."). Ở L2, "tên module chỉ như gợi ý", nhưng đây thả cả rừng tên kỹ thuật trước khi neo. Trượt self-check câu 1. → 0.

**TC2 CHẾ ĐỘ = 1.**
Là overview (đúng chế độ, không lạc sang flow/why). CÓ đủ ba mảnh (làm gì / cho ai / vì sao tồn tại) và có luồng — nhưng SAI THỨ TỰ: "cho ai / vì sao tồn tại" bị đẩy xuống dưới cùng thay vì mở màn. Đúng chế độ nhưng lẫn/lệch cấu trúc → 1.

**TC3 ĐỦ Ý = 2.**
Nội dung rất đủ: tách metadata/nội dung, tách read/write-path, sinh link hash+Base62, con số quy mô (10M user, 10:1 đọc:ghi, 450GB/3 năm), luồng ghi 6 bước + luồng đọc 4 bước + 2 job nền. Đọc xong nắm được cốt lõi. → 2.

**TC4 LỜI VĂN (xương sống) = 2.**
Câu phần lớn ngắn, phẳng, dễ đọc. Bullet chỉ dùng ở phần liệt kê component/module (đúng chỗ E3 cho phép). Không trích số dòng. Code block API hợp lý. → 2. (Gate này QUA.)

**TC5 BÁM CODE (xương sống) = 2.**
Mọi claim khớp fixture System Design Primer Pastebin: cột bảng `pastes`, MD5(ip+timestamp)→Base62→7 ký tự, 62^7, endpoint POST/GET, MapReduce HitCounts mapper/reducer, con số quy mô. Không thấy claim bịa. Ở L2 không trích code (đúng). → 2. (Gate này QUA.)

**TC6 RANH GIỚI = 2.**
Đúng vai explain: dạy hiểu tổng quan, không dựng .ai-understanding/, không đào side-effect sâu, không liệt edge case, không phán số phận file. → 2.

**TC7 KẾT = 1.**
Có gợi ý bước tiếp ("đi qua luồng từng bước / soi đường ghi / xử lý hết hạn / analytics") và có câu hỏi mức cuối — đúng khuôn L2. Nhưng gợi ý hơi chung, không neo rõ vai CTO/business nên đọc gì. → 1.

**Tổng: 0+1+2+2+2+2+1 = 10/14 nhưng RỚT GATE (TC1=0).** Theo luật gate: bản này KHÔNG ĐẠT dù tổng khá. Chuẩn hoá 0–10 có phạt gate: **4/10.**

---

## RUBRIC 2 — STAKEHOLDER-COMM → 3/10, RỚT GATE (cả 2 gate)

**TC1 VẤN ĐỀ + CHO AI đặt trước mọi thuật ngữ (GATE) = 0 → FAIL.**
Bằng chứng: đoạn mở đầu toàn thuật ngữ kiến trúc; công dụng + đối tượng ("dịch vụ kiểu Pastebin, người dùng ẩn danh dán text lấy link ngắn") bị đặt SAU cả phần component lẫn API, mở bằng chính câu tự thú "Bây giờ mới nói công dụng". Người ngoài (CTO/business khách hàng) rớt ngay câu đầu. → Gate fail.

**TC2 Không jargon mồ côi (GATE) = 0 → FAIL.**
Bằng chứng: "web-tier", "reverse proxy", "SQL Master-Slave có read-replica", "MapReduce", "Base 62 encode", "MD5 hash", "RPC", "CDN", "Memory Cache" đều thả trần ở phần đầu trước khi neo vào bước nào. Tên công nghệ ngoài (S3 có kèm "kiểu Amazon S3" — ổn; nhưng Base62/MD5/MapReduce/RPC không kèm cụm đời thường đúng lúc xuất hiện). Người ngoài gặp một chuỗi từ mồ côi. → Gate fail.

**TC3 Đúng độ cao cho CẢ HAI vai = 1.**
CTO thấy hình hài + rủi ro/độ chín (tách path, có job nền, phần analytics offline). Business CÓ thấy giá trị nhưng bị nhét xuống cuối và chỉ nhắc gọn; giá trị không lặp ở mỗi tầng zoom như hợp đồng đòi. Chạm cả hai nhưng lệch → 1.

**TC4 Bản đồ/khung định vị = 1.**
CÓ luồng "map bạn ở đây" đánh số (6 bước ghi + 4 bước đọc), ngôn ngữ khá đời thường — nhưng đặt QUÁ TRỄ (sau kiến trúc + component + API), nên với người ngoài nó không còn làm nhiệm vụ "định vị trước khi vào chi tiết". Có khung nhưng đặt sai chỗ → 1.

**TC5 Actionable = 1.**
Có câu hỏi bước tiếp nhưng chung chung, không bám riêng vai CTO vs business, không chỉ đọc gì trước. → 1.

**Kết: RỚT CẢ HAI GATE (TC1=0, TC2=0). KHÔNG ĐẠT.** Điểm phần còn lại 1+1+1 chỉ để tham khảo. Chuẩn hoá 0–10: **3/10.**

---

## RUBRIC 3 — COLLAB-LEADERSHIP → 6/10, QUA GATE

**TC1 Không tự tiện vượt quyền (GATE) = 2.**
Không tự chốt scope, không tự kill, không sinh/sửa code. Chỉ giải thích + hỏi hướng đi tiếp. → 2. (Gate QUA.)

**TC2 Hỏi đúng liều lượng = 2.**
Cụm câu hỏi cuối gọn, cùng chủ đề ("đi qua luồng từng bước, hay có một luồng cụ thể... hết hạn hoặc analytics"), ≤3 câu, cùng một tầng. → 2.

**TC3 Restate + nêu giả định trước khi hỏi = N/A / 1.**
Đây là lượt explain một chiều (đã có level L2 trong đề), không phải lượt hỏi-làm-rõ, nên restate/giả định ít áp dụng. Có ngầm restate ("Bạn đang ở L2 — map") nhưng không nêu giả định. Cho 1 vì áp dụng một phần.

**TC4 Kết bằng một cổng/bước kế rõ (GATE) = 2.**
Kết bằng một cổng lựa chọn rõ: "Bạn muốn tôi đi qua luồng chạy từng bước... hay có một luồng cụ thể... bạn muốn xem trước?" + câu hỏi tự-định-mức. User biết phải quyết gì để đi tiếp. → 2. (Gate QUA.)

**TC5 Bàn giao đúng sibling khi hết vai = N/A.**
Ở L2 explain chưa chạm ranh hết vai (L5+ mới hand off). Câu hỏi mức cuối có liệt kê thang L0–L8 để user tự định vị, đúng cơ chế. Không tính vào gate. → N/A.

**Kết: QUA GATE. Tổng TC áp dụng (2+2+1+2) mạnh. Chuẩn hoá 0–10: **6/10.** (Không kéo cao hơn vì TC3 chỉ 1 và bản này thiên về một-chiều nên phối hợp chỉ hiện rõ ở khối kết.)

---

## TỔNG KẾT
- contract_fidelity: **4/10** — rớt gate TC1 (mở bằng kiến trúc, đảo thứ tự bắt buộc).
- stakeholder_comm: **3/10** — rớt CẢ HAI gate (vấn đề không đặt trước + jargon mồ côi).
- collaboration: **6/10** — qua gate, phối hợp lành ở khối kết.

**Nghịch lý đáng ghi:** nội dung (đủ ý, bám code, ranh giới) rất chắc — nếu tính tổng thô thì cao. Nhưng bản này cố tình đảo trật tự kể (kiến trúc trước, công dụng sau, tự thú "Bây giờ mới nói công dụng"), vi phạm đúng luật xương sống của explain. Vì thế cả hai rubric đo "người ngoài có theo được không" đều rớt gate. Đây là ca điển hình gate quan trọng hơn tổng: một overview đầy đủ dữ kiện nhưng bỏ rơi CTO/business ngay câu đầu.
