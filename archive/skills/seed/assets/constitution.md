# Luật project — <TÊN PROJECT> (v2 — mô hình solo)

File này là `constitution/00-luat.md`. **Mọi agent — kể cả agent con fan-out — đọc file này TRƯỚC khi làm gì.**

Bối cảnh: project chỉ có Son và agent. Quy trình KHÔNG tồn tại để quy trách nhiệm hay xin phép — nó tồn tại để: **vấn đề** đi qua thì ra **ý tưởng**; ý tưởng đi qua thì ra **cách triển khai + độ khả thi đã kiểm**; sản phẩm cuối **khớp kỳ vọng ban đầu**. Fail ở đâu → vòng lại ở đó. Không có ai để đổ lỗi, và không cần.

## Folder contract

| Folder | Chứa gì | Agent nào ghi |
|---|---|---|
| `problem/` | `00-de-bai.md` (đề bài + **Kỳ vọng ban đầu**), `01-nghiep-vu.md`, `goc/` (nguyên liệu Son ném vào: file, data mẫu, link — chỉ-thêm, không sửa) | seed, meet |
| `idea/` | Mỗi ý 1 file theo `_mau.md`: ý là gì, input, output, giả định, ẩn số, trạng thái | mọi skill khi bắt được ý |
| `progress/` | `board.md`, `journal.md`, `decisions.md` (sổ quyết định), `risks.md` (sổ ẩn số & khả thi) | CHỈ agent điều phối — agent con KHÔNG chạm |
| `constitution/` | Luật (file này) | sửa khi Son gật — thường sau retro của `pulse` |
| `docs/` | Artifact theo giai đoạn + `contracts/` | skill của giai đoạn đó |
| `codebase/` | Code; spike/thí nghiệm ở `codebase/spikes/`; `README.md` phải sống | run (sketch cho slice) |

## Kỳ vọng — mỏ neo chống lệch

- `problem/00-de-bai.md` có mục **Kỳ vọng ban đầu**: K1..Kn, mỗi K một câu mà khi thành sự thật Son TỰ THẤY được bằng mắt. `seed` ghi bản thô ngay ngày 0 (trước khi agent kịp ảnh hưởng); `meet` mài thành bản đo được. Từ đó không ai sửa ngầm — đổi kỳ vọng là một quyết định, ghi `decisions.md`.
- `docs/00-buc-tranh.md` (1 trang văn xuôi, mơ hồ dần rõ, mỗi GĐ kết thúc viết lại) có dòng cố định: **"So kỳ vọng: ..."** — khớp, hay lệch ở K nào, lệch thì chấp nhận hay vòng lại.
- PRD map từng phần phạm vi về K nào. `gate` cuối đối chiếu từng K một.

## 4 điểm chốt — chỗ duy nhất dừng chờ Son

Chỉ dừng ở nơi đoán sai thì đắt; còn lại agent tự quyết, ghi sổ, chạy tiếp — Son đổi được bất cứ lúc nào vì làm lại là rẻ.

1. **Sau `meet`:** kỳ vọng K1..Kn + PRD (mọi thứ sau neo vào đây).
2. **Sau `sketch`:** hình hài + stack + bằng chứng live slice (đoán sai kiến trúc là đắt nhất).
3. **Tại `plan`:** contract `locked` trước khi fan-out (agent song song chạy trên contract sai là công cốc).
4. **Tại `gate`:** đối chiếu ƯNG Ý — điểm chốt cuối, chính là mục đích của cả quy trình.

Ngoài 4 điểm: không hỏi xin, không chờ. Lựa chọn mà sau này có thể hỏi "vì sao" → ghi `decisions.md` 1 dòng rồi đi tiếp.

## Vòng đời một ý (vấn đề → ý tưởng → khả thi → sản phẩm)

pain trong `problem/01` → ý thô `idea/<slug>.md` (đủ input/output/ẩn số) → được chọn vào PRD (không chọn → `gac`, không xoá) → có hình trong thiết kế (`sketch`) → ẩn số đóng bằng spike/slice, ghi kết quả vào `risks.md` → thành task trên board (`plan`) → thành code (`run`) → đối chiếu kỳ vọng (`gate`). Đứt ở khâu nào cũng truy được vì mỗi khâu để lại một dòng.

## Resume protocol — Bước 0 của mọi skill

1. Đọc file này.
2. Đọc `progress/board.md` + 5 dòng cuối `journal.md` + rủi ro `mo` trong `risks.md`.
3. Đọc đúng artifact upstream của việc sắp làm (bảng dưới) — không quét cả folder.
4. Làm việc. **Kết phiên bắt buộc:** artifact đúng chỗ + board + 1 dòng journal + ẩn số mới → `risks.md` + lựa chọn đáng nhớ → `decisions.md` + bức tranh nếu kết một GĐ.

Dòng journal: `YYYY-MM-DD · <skill> · <làm gì, 1 câu> · <artifact chính>`

## Bảng artifact — giai đoạn → file → skill

| GĐ | Artifact | File | Skill |
|---|---|---|---|
| 0 | Đề bài + Kỳ vọng thô | `problem/00-de-bai.md` | seed |
| 1 | Nghiệp vụ + Business Case | `problem/01-nghiep-vu.md` + `docs/10-business-case.md` | meet |
| 2 | Product Brief | `docs/11-product-brief.md` | meet |
| 3 | Requirement Catalogue | `docs/12-requirements.md` | meet |
| 4 | PRD + K-list đo được | `docs/13-prd.md` | meet |
| 5 | Domain Model | `docs/20-domain-model.md` | sketch |
| 6 | Architecture Brief + ADR | `docs/21-architecture-brief.md` | sketch |
| 7 | Tech Decision Matrix | `docs/22-tech-matrix.md` | sketch |
| 8 | Live Slice Report + code | `docs/23-live-slice-report.md` + `codebase/` | sketch |
| 9 | Roadmap + Backlog | `docs/30-roadmap.md` + `progress/board.md` | plan |
| 10 | Module Map + Contracts | `docs/31-module-map.md` + `docs/contracts/` | plan |
| 11 | Code + DoD checks | `codebase/` | run |
| 12 | Verification Report | `docs/40-verification.md` | gate |
| 13 | Đối chiếu ưng ý + Runbook | `docs/41-ung-y.md` + `docs/42-runbook.md` | gate |
| 14 | Ops & Learn | `docs/50-ops.md` → task mới về board | pulse |

Nội dung chi tiết từng giai đoạn: `quy-trinh-idea-to-operate.md` ở gốc repo skillsh, mục GĐ tương ứng. Không chế khung mới.

## Board schema

```
| ID | Task | GĐ | Trạng thái | Phụ thuộc | Song song | Vùng chạm | Artifact |
```

- Trạng thái: `todo | ready | doing | review | done | blocked | gac`. `ready` = mọi Phụ thuộc đã `done`.
- Song song = tên nhóm (vd `xay-1`) hoặc `—`. Vùng chạm = file/folder task được sửa.
- Chỉ agent điều phối đổi trạng thái. `blocked` kèm lý do dưới bảng.

## Luật fan-out (nhiều agent song song)

Chỉ fan-out các task **cùng nhóm Song song** khi đủ 3 điều kiện: (1) mọi Phụ thuộc của cả nhóm `done`; (2) contract giữa chúng có dòng `Trạng thái: locked` trong `docs/contracts/`; (3) Vùng chạm không giao nhau.

Agent con: đọc luật này, chỉ sửa trong Vùng chạm của mình, KHÔNG chạm `progress/`, xong trả về tóm tắt + danh sách file + kết quả check. Agent điều phối là người duy nhất ghi board/journal/sổ, review theo AC rồi mới chuyển `done`.

## Hai sổ sống trong progress/

- **`decisions.md`** — mỗi dòng: `ngày · chọn gì · thay vì gì · vì sao · link artifact`. Ghi khi: qua điểm chốt, chốt ADR, đổi kỳ vọng/phạm vi, vòng lại, hoặc lựa chọn agent tự quyết mà mai sau có thể hỏi "vì sao hồi đó". Trả lời "vì sao" trong 30 giây thay vì đào 3 file.
- **`risks.md`** — thước ĐỘ KHẢ THI của project. Mỗi dòng: `R-x · điều chưa chắc · từ đâu (GĐ/file) · nếu sai thì sao · cách kiểm rẻ nhất · trạng thái · kết quả`. Trạng thái: `mo | dang-kiem | dong-dung | dong-sai`. Chỉ được đóng bằng BẰNG CHỨNG (spike, slice, số đo, thử thật) — không đóng bằng cảm giác. Skill nào lộ ra ẩn số vẫn ghi trong artifact của mình, nhưng PHẢI thêm 1 dòng vào đây — đây là index.

## Làm lại — một nước đi hợp lệ

Lệch phát hiện muộn → quay về điểm chốt gần nhất còn đúng, làm lại từ đó. `decisions.md` ghi: `vòng lại vì X · học được Y`. Task cũ đổi trạng thái, không xoá lịch sử. Vòng lại không phải thất bại — đó là quy trình đang làm đúng việc: giữ sản phẩm khớp kỳ vọng.

## Definition of Done

Task `done` khi: artifact đúng chỗ theo bảng; check của giai đoạn đạt (code: build/test pass, `codebase/README.md` còn đúng; docs: đủ mục theo playbook); board + journal + sổ đã cập nhật; AC của story tương ứng nghiệm lại được; **không còn rủi ro `mo` gắn vào task đó**.

## Luật gốc v2

- **Đủ-là-đủ.** Độ sâu tỉ lệ rủi ro/ẩn số. Không bỏ artifact — chỉ rút gọn độ sâu.
- **Artifact 1 trang,** mở bằng 2–3 câu mà Son-sau-2-tuần-quay-lại (hoặc agent mới) đọc là nắm ngay, rồi mới tới chi tiết.
- **Một cụm câu hỏi mỗi lượt** (≤3 câu cùng chủ đề). Cấm câu phủ định cứng khi phản biện — nêu ràng buộc kèm lối đi tiếp.
- **Không đoán project.** ≥2 project ứng viên trong `projects/` → hỏi.
- **Secrets không bao giờ nằm trong folder** — chỉ ghi pointer (ở đâu, cách lấy). `codebase/` chỉ chứa `.env.example`.
- **Artifact đóng version tại điểm chốt** (v1, v2… + lịch sử 1 dòng cuối file, như bức tranh đang làm) — vòng 2 sửa gì cũng còn dấu bản đã chốt.
- **Retro không đổ lỗi:** bài học về CÁCH LÀM → `pulse` đề xuất sửa luật này hoặc nâng template gốc trong `seed/assets/`.
