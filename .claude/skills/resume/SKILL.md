---
name: resume
description: "Cửa vào một project đã dựng: đọc constitution + progress.json + các artifact trong problem/idea/docs/codebase rồi in một khối toàn cảnh — bức tranh lớn, đã chốt gần nhất, đang đứng ở đâu, task nào hết bị chặn (ready), nhóm nào chạy được song song, và skill kế nên gọi. CHỈ ĐỌC, chỉ tiến cử, không tự làm tiếp. Dùng khi: 'đang ở đâu rồi', 'tiếp tục project X', 'resume', 'project này thế nào', 'quay lại làm tiếp', mỗi lần mở lại một project sau khi nghỉ. KHÔNG tạo/sửa file — muốn dựng mới thì charter, muốn cập nhật task thì progress."
---

# Resume — Nạp ngữ cảnh, nói đang ở đâu, tiến cử bước kế

`resume` là hiện thân người-đọc-được của hợp đồng nạp-ngữ-cảnh (conventions §4). Mỗi lần quay lại một project, chạy `resume` để không phải nhớ "hôm trước đang dở gì" — state nhớ hộ. Nó đọc hết rồi tóm lại; nó KHÔNG quyết, KHÔNG ghi, KHÔNG chạy skill kế thay bạn.

Ranh giới:
- `resume` đọc và kể. `progress` mới được sửa `progress.json`. `charter` mới được dựng project.
- `resume` tiến cử một skill kế; user tự chạy skill đó.
- Muốn tổng kết BUỔI làm việc (diff theo thời-gian của CẢ repo: commit/worktree/sổ phê duyệt) → đó là `recap`; `resume` chỉ nói trạng thái hiện tại của MỘT project.

## Quy tắc bắt buộc

- **Read-only tuyệt đối.** Không ghi bất kỳ file nào, kể cả `state/current.json`.
- **Không hỏi lại điều đã có trong file.** Con trỏ, quyết định đã chốt, task đang mở — đọc ra, không hỏi.
- **Chỉ tiến cử, không tự chạy.** Nói "nên chạy `/idea`", không tự mở `idea`.
- **Trung thực với tiến độ thật.** Chỉ báo done những task `progress.json` ghi done. Không suy diễn tiến độ từ việc "đã bàn tới".

## Bước 0 — Xác định project (qua sổ cái, không đoán)

1. Argument (`/resume hex-agent` — nhận cả tên cũ): chuẩn hoá bằng sổ cái —
   `python3 scripts/portfolio.py resolve <arg>` trả về `key` + `path` chuẩn (gộp mọi alias/tên-cũ về một key).
2. Không có arg → `python3 scripts/portfolio.py list` in mọi project + con trỏ đang mở (`→`); mặc định lấy `current`.
3. Vẫn không rõ → hỏi mở cái nào.

(Portfolio là engine tra cứu tất định — đừng tự suy `tên ↔ path`, để script trả lời.)

## Bước 1 — Đọc (đúng thứ tự nạp-ngữ-cảnh)

1. `projects/<key>/constitution/` — nạp luật (đọc lướt, biết cách chơi).
2. `projects/<key>/progress/progress.json` — con trỏ + toàn bộ tasks. *(Project PIPELINE-mode có thể chưa có file này — không sao, đọc tiếp mục 5.)*
3. Đầu mục artifact có thật: `ls` bốn folder `problem idea docs codebase`, đọc tiêu đề/dòng đầu file mới nhất để lấy một-dòng-tổng-thể.
4. Kiểm sợi bằng MÁY (không soi tay): `python3 scripts/spine_check.py <key>` — trả link đứt / vòng lặp / task mồ côi / thiếu `traces_to`. Đưa kết quả vào dòng "Sợi" của khối toàn cảnh; exit 0 = liền.
5. **Cổng đang chờ ký — đọc DỮ LIỆU, không đoán.** Nếu tồn tại `state/project/<key>/pipeline/` hoặc `projects/<key>/pipeline/`: đọc `_index.json` + các `<skill>.json`. Bất kỳ artifact nào có `cho_duyet: true` hoặc `trang_thai` ∈ {`cho_ky`, `cho_duyet`} = **MỘT CỔNG ĐANG CHỜ BẠN KÝ** (ghi nhớ stage đó cho Bước 2). Đây là cơ chế theo-dữ-liệu: một cổng đang treo thì thấy dù con trỏ nằm đâu — không phụ thuộc phán đoán "con trỏ có ở cổng không".

Tính (không ghi, chỉ tính trong đầu):
- **ready** = task `trang_thai` là `ready`, hoặc `todo` mà mọi `depends_on` đều `done`.
- **nhóm song song sẵn sàng** = các `parallel_group` mà mọi task trong nhóm đều ready → gợi ý `/fanout`.
- **skill kế** = suy từ `owner` của task ready đầu tiên (idea→`/idea`, shape→`/shape`, modules→`/modules`, delivery→`/delivery`…).

## Bước 2 — In khối toàn cảnh

```
═══ ĐANG Ở ĐÂU — <key> ═══
Bức tranh: <1–2 câu vấn đề đang giải, từ problem/ + idea/>
Con trỏ: <giai_doan> — <ghi_chu>
Đã chốt gần nhất: <1 dòng, task done mới nhất + artifact>
Sẵn sàng chạy: <task id · việc> (owner: <skill>)
Chạy song song được: <parallel_group + các task, hoặc "chưa">
Sợi: <✓ liền | N chỗ cần vá: link đứt/mồ côi/thiếu neo — chạy /traceability xem chi tiết>
Còn treo: <open question/blocked nếu có, 1 dòng>
→ Tiến cử: /<skill>   (hoặc /fanout nếu có nhóm song song sẵn sàng)
════════════════
```

Nếu có nhiều task ready không cùng nhóm → liệt kê tối đa 3, để user chọn chạy cái nào trước.

**Cổng đang chờ ký (từ Bước 1 mục 5, HOẶC con trỏ đang ở live-slice/release):** in một dòng ⏳ làm **DÒNG ĐẦU** khối toàn cảnh (ngay dưới `═══ ĐANG Ở ĐÂU`, trước "Bức tranh"):
```
⏳ ĐANG CHỜ BẠN KÝ CỔNG <stage> — resume KHÔNG tiến cử skill sau cổng.
```
Và ở dòng "→ Tiến cử" ghi `chờ bạn ký GO/NO-GO rồi mới đi tiếp` — **KHÔNG** gợi ý skill giai đoạn kế. Cổng chờ-người bị bước qua trong im lặng ("/resume rồi làm tiếp" → chạy thẳng skill sau cổng) chính là vết mà mục này vá; cổng do DỮ LIỆU `cho_duyet` quyết, không do resume tự đánh giá.

## Khi project trống (vừa charter xong)

Chỉ có T-01 ở `gd0_intake` → khối toàn cảnh rút gọn: "Project vừa dựng, chưa có ý nào. → Tiến cử: /idea để brainstorm ý đầu tiên."

## Ví dụ (multi-lens-chat, đang ở PRD)

```
═══ ĐANG Ở ĐÂU — multi-lens-chat ═══
Bức tranh: 1 agent chính hội thoại + N trợ lý nền chạy song song theo lens khác nhau; dùng cá nhân, ca đầu là review code đa góc nhìn.
Con trỏ: gd2_4_product_prd — chờ chốt 3 open question (lens cố định?, streaming?, tổng hợp?)
Đã chốt gần nhất: T-01 Business Need + Case (problem/business-case.md)
Sẵn sàng chạy: T-02 · Chốt PRD + MVP (owner: idea)
Chạy song song được: chưa (nhánh BE/FE chỉ mở sau khi freeze contract ở gd10)
Còn treo: OQ-4/5/6 — lens, streaming, cách tổng hợp insight
→ Tiến cử: /idea (chốt 3 open question rồi qua Domain)
════════════════
```
