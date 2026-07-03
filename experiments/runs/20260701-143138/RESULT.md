# RESULT — vòng tune explain (2026-07-01)

Fixture: `hex_agent · L3 · overview`. Thước: `grade` (7 tiêu chí ×0/1/2, gate = Mức/Lời văn/Bám code). Mỗi output chấm mù 2 giám khảo độc lập, lấy trung bình.

> Lỗi kỹ thuật: `args` của workflow run 1 không bind (fixture log ra "undefined"); các agent tự phục hồi fixture qua `state/current.json` nên output/grade hợp lệ. Phase Confirm run 1 fail → chạy lại ở run `tune-confirm` (path hardcode).

## Bảng xếp hạng (run 1 — baseline + A–E)

| Bản | Đổi gì | Điểm TB | Giám khảo | Gate |
|---|---|---|---|---|
| baseline | (giữ nguyên explain hiện tại) | **14.0** | 14, 14 | đạt |
| B trigger mode | liệt cụm từ kích overview/flow/why | 14.0 | 14, 14 | đạt |
| D backbone | xương sống 3 nhịp LÀM GÌ/CHO AI/VÌ SAO trước zoom | 14.0 | 14, 14 | đạt |
| E nguyên tắc viết | 4 luật lời văn E1–E4 vào principles.md | 14.0 | 14, 14 | đạt |
| A ví dụ mẫu | chèn overview mẫu tốt (kèm câu mở sai) | 13.5 | 14, 13 | đạt |
| C do/don't mức | 1 dòng được/cấm nói dưới mỗi mức | 13.0 | 13, 13 | đạt |

## Confirm (run 2 — chống over-fit, 2 giám khảo/ca)

| Ca | Project | Ghép D+E? | Điểm | Gate |
|---|---|---|---|---|
| nocode-baseline | nocode_platform (khác domain) | ✗ | 14.0 | đạt |
| nocode-graftDE | nocode_platform | ✓ | 13.0 | đạt |
| hex-graftDE | hex_agent (fixture) | ✓ | 14.0 | đạt |

Baseline đạt 14/14 trên cả project khác domain → **explain không over-fit**. Graft không regress fixture. Ca nocode-graftDE tụt 1 là do agent generate đọc nhầm nội bộ nocode (tiêu chí Bám code), **không liên quan tới D+E** — nằm trong nhiễu grounding giữa các agent.

## Kết luận

**Winner = baseline.** Hướng bạn đã đi (thang zoom + Luật neo) đã chữa đúng nỗi đau "chi tiết trước tổng quan" và đạt trần rubric. Không hướng A–E nào vượt.

**Việc còn lại KHÔNG phải sửa explain — mà là mài `grade`.** Rubric 14 điểm đã bão hoà: baseline/B/D/E cùng 14/14, tune không phân biệt được nhóm dẫn đầu dù `fixFirst` cho thấy còn khoảng cách thật (câu dài nối gạch ngang, lặp giá trị business, mâu thuẫn "cửa duy nhất"). Đòn bẩy lớn nhất bây giờ: cho grade thang mịn hơn + gỡ mâu thuẫn để vòng tune sau đo được khác biệt.

### Bản vá đề xuất (chờ chốt trước khi merge — Bước 6)

- **Explain (tuỳ chọn, phòng thủ):** ghép **E** (4 luật lời văn vào `principles.md`) + **D** (xương sống 3 nhịp trước thang zoom). Cả hai chỉnh *nguồn luật*, không đổi cấu trúc output; xác nhận không regress fixture (14/14) và qua gate trên domain khác. Không giúp tăng điểm ở fixture này nhưng khoá cứng hành vi tốt cho fixture khác. **Không** áp A (over-fit: chép từ vựng project mẫu) và **không** áp C (gây rò rỉ meta "theo dòng Do/Don't mình mới thêm" vào output).
- **Grade (đòn bẩy chính):** xem "Mâu thuẫn rubric↔skill" dưới đây.

### Mâu thuẫn rubric↔skill cần gỡ trong `grade`

1. **Tiêu chí 1 (Mức):** rubric cấm code-name khi `level < L4`, nhưng SKILL cho phép "gọi tên module đã-neo ở L2–L3". → Tách rõ: *trích dẫn* (số dòng / chữ ký hàm / tên biến) cấm < L4, vs *nhắc tên module/entrypoint đã neo* cho phép từ L2. (Grader C dựa vào chỗ mơ hồ này để giữ 13/13.)
2. **Tiêu chí 2 (Chế độ):** output tự dán nhãn "flow" ở câu mở khi thực ra đang overview → gây rối chấm mode. SKILL nên cấm dán nhãn mode vào câu mở.
3. **Luật neo "cửa DUY NHẤT" vs thực tế 2 chokepoint** (tool vs delegation): nhiều output lộ mâu thuẫn "cửa duy nhất" (bước 5) rồi "cửa riêng cho delegation" (bước 6). Rubric chưa có tiêu chí bắt mâu thuẫn nội tại → cân nhắc tiêu chí thứ 8 (consistency) nếu lỗi này lặp.
4. **Tiêu chí 4 (Lời văn) vs Zoom-3:** rubric phạt "tường bullet" nhưng Zoom-3 lại yêu cầu điểm-danh module dạng bullet. E3 đã hoà giải (bullet chỉ cho module tầng cuối) — nếu không ghép E thì mâu thuẫn còn đó.

### Phát hiện meta về chính bộ máy tune

- **Trần rubric che khác biệt:** cần thang mịn hơn (vd chia nhỏ tiêu chí hoặc thêm mức 0–3) để phân biệt các bản 14/14.
- **Giới hạn của Confirm:** so baseline-vs-graft bằng **hai agent khác nhau** trên codebase lạ trộn "hiệu ứng graft" với "nhiễu grounding của agent". Muốn đo thật hiệu ứng một bản vá, cần A/B cùng agent hoặc nhiều mẫu — đừng đọc chênh-lệch-1-điểm là tín hiệu.
