# Rubric — 6 tiêu chí chấm một bản `atlas` (nền hiểu biết `.ai-understanding/`)

Mỗi tiêu chí 0/1/2. Khung chung: `grade/meta-rubric.md`. Chuẩn gốc để chấm: `atlas/SKILL.md` (Mục tiêu + mục "## Luật cứng" + Bước 0–3) và `atlas/atlas-artifacts.md` (luật evidence + bộ 20 artifact + template). Rubric chỉ biến hợp đồng đó thành thước đo — KHÔNG thêm tiêu chuẩn mới.

Tiêu chí **1 (Đủ bộ artifact), 2 (Bám nguồn — không bịa), 3 (Đọc-được)** là **xương sống (gate)**: rớt bất kỳ cái nào → rớt cả bản dù tổng cao. Trong đó tiêu chí 2 là gate NẶNG NHẤT — atlas hay báo số/PASS/artifact từ thứ không tồn tại.

**Đầu vào để chấm (fixture):** project (đường dẫn codebase atlas đang map, để kiểm bịa) · thư mục `.ai-understanding/` bản atlas sinh ra (nguyên văn 20 artifact + `00_index` + `20_understanding_scorecard` + `99_changes`) · trạng thái git repo (built_commit, để kiểm freshness/ledger).

## 1. ĐỦ BỘ ARTIFACT — đúng path, một lượt (xương sống)

Một lượt chạy sinh **đủ bộ 20 artifact (01–20)** + `00_index.md` + `20_understanding_scorecard.md` + `99_changes.md`, tất cả nằm đúng `<project-path>/.ai-understanding/`, có `09_flow_traces/` trace tối thiểu 4 flow (≥1 happy path, 1 failure path, 1 side-effect path, 1 permission/security path). Bỏ artifact ≠ rút gọn độ sâu.

- 0 — thiếu hẳn artifact xương: không đủ 20 artifact 01–20, HOẶC thiếu `00_index` / `20_understanding_scorecard` / `99_changes`, HOẶC `09_flow_traces/` không đủ 4 flow bắt buộc, HOẶC ghi ra ngoài `.ai-understanding/`, HOẶC chia bộ artifact qua nhiều lượt (vi phạm luật "Một lần, đầy đủ").
- 1 — đủ mặt file nhưng một artifact xương quá sơ sài so với rủi ro (vd `14_security_permission_map` một dòng ở hệ có auth, `11_dependency_graph` bỏ trống), hoặc flow_traces đủ 4 nhưng một trace không đi end-to-end.
- 2 — đủ 20 artifact + index + scorecard + ledger đúng path; `09_flow_traces/` có đủ ≥1 happy/failure/side-effect/permission và mỗi trace đi từ entrypoint đến điểm cuối; độ sâu mỗi artifact khớp rủi ro; scorecard tự chấm 0–5 kèm lý do.

## 2. BÁM NGUỒN — mọi claim có evidence file:line, KHÔNG bịa (xương sống, gate nặng nhất)

Mọi nhận định kèm khối evidence (file path · symbol · dòng/đoạn code · suy luận · mức chắc chắn) theo `atlas-artifacts.md`. Không claim nào thiếu evidence; chưa đủ căn cứ → đẩy vào `18_risks_and_unknowns.md`, KHÔNG ghi như fact. Facts (đọc được trong code) tách khỏi assumptions (giả định), gắn nhãn rõ.

- 0 — có claim bịa: nhắc file/symbol/hành vi không có trong code đích; HOẶC claim không kèm evidence mà vẫn ghi như fact; HOẶC báo số/kết quả (số module, số flow, điểm scorecard "đã verify") từ thứ không tồn tại; HOẶC trộn assumption vào fact không gắn nhãn. Bất kỳ claim bịa nào → tiêu chí này 0.
- 1 — chủ yếu bám nguồn, nhưng 1–2 chỗ evidence thiếu mảnh (có file path nhưng không có symbol/dòng), hoặc một suy đoán chưa gắn mức chắc chắn `một phần`/`có thể sót`.
- 2 — mọi claim kèm evidence đủ 5 phần và mức chắc chắn; phần chưa hiểu nằm ở `18_risks_and_unknowns.md` chứ không giả làm fact; observed fact vs assumption gắn nhãn rõ; các con số/tên file đều truy được về code thật.

## 3. ĐỌC-ĐƯỢC THEO TẦNG (xương sống)

`00_index` mở được cho người mới nắm bức tranh lớn; từng artifact scan được trong 2–3 phút; thuật ngữ lạ nối được về `19_glossary`. Đúng đối tượng đọc (skill khác + người vận hành atlas) là nắm được.

- 0 — `00_index` không cho biết hệ thống làm gì / có những artifact nào; HOẶC artifact dày đặc jargon không giải thích, không có mục lục/điểm vào, đọc xong không biết module nào sở hữu gì; HOẶC sai đối tượng (viết như bài giảng cho người mới thay vì bản đồ tra cứu).
- 1 — đọc được nhưng lệch: index có nhưng thiếu trạng thái/điểm vào, hoặc một vài artifact rườm/thiếu điểm neo khiến phải đọc cả file mới hiểu.
- 2 — `00_index` mở bằng hệ-thống-làm-gì + mục lục 20 artifact + trạng thái + built_at/built_commit; mỗi artifact có điểm vào rõ, scan 2–3 phút; thuật ngữ nối `19_glossary`.

## 4. ĐÚNG VAI — dựng bản đồ, KHÔNG sửa code, KHÔNG giải thích một phần

Atlas read-only trên code đích (chỉ ghi vào `.ai-understanding/`), KHÔNG đụng `user-state.json` / `agent-state.json` / `pipeline-state.json` / `triage.json`. Nó dựng bản đồ CHO HỆ THỐNG (bằng chứng, dùng chung) — KHÔNG dạy người theo mức L0–L8 (đó là `explain`), KHÔNG phán giữ-sửa-xoá file (đó là `triage`), KHÔNG chỉ giải thích một phần.

- 0 — sửa/tạo file code trong project đích; HOẶC ghi đè state của skill khác; HOẶC làm việc explain (giải thích một phần theo mức user thay vì map cả repo) / triage (ra quyết định số phận file) / chỉ tóm tắt vài file thay vì chứng minh đã hiểu cả hệ.
- 1 — chủ yếu đúng vai, lấn nhẹ (vd chèn một đoạn giải thích kiểu explain, hoặc gợi ý số phận một file kiểu triage) nhưng không sửa code / không đụng state.
- 2 — thuần bản đồ có bằng chứng cho toàn hệ; read-only trên code; chỉ ghi `.ai-understanding/`; không đụng state skill khác; chứng minh đã hiểu (bài toán gì · hành vi thật đi đâu · sửa đâu thì vỡ đâu), không tóm tắt file.

## 5. FRESHNESS + DRIFT LEDGER — chạy một lần rồi tái dùng

Nếu `.ai-understanding/` đã tồn tại → KHÔNG quét lại; đọc `99_changes.md` + `00_index.md`, so với commit hiện tại, báo đã build lúc nào / ở commit nào rồi hỏi *tái dùng* hay *refresh* (mặc định tái dùng). `99_changes.md` mang status + `last_synced_commit`; chỉ atlas được bump last_synced_commit.

- 0 — khi atlas đã tồn tại vẫn quét lại toàn bộ mà không freshness-check (vi phạm "Chạy một lần rồi tái dùng"); HOẶC `99_changes.md` thiếu status / `last_synced_commit`; HOẶC full re-build khi lẽ ra chỉ cần targeted update từ pending; HOẶC tự bump last_synced_commit sai/không đồng bộ built_commit ở build đầu.
- 1 — có freshness-check và ledger nhưng thiếu một mảnh: không báo built_commit, hoặc không hỏi tái-dùng/refresh, hoặc targeted-update áp dụng pending nhưng quên đổi status `applied`.
- 2 — build đầu: `99_changes.md` status `clean`, `last_synced_commit` = built_commit, chưa pending; khi đã tồn tại: đọc ledger + index, báo build-lúc-nào/commit-nào, hỏi tái-dùng/refresh (default tái dùng), targeted-update khi pending ít, full re-build chỉ khi pending nhiều / thay đổi lớn / user yêu cầu.

## 6. BÀN GIAO — trỏ tái dùng + `/explain` cho người mới

Báo cáo ngắn: đã dựng ở đâu, scorecard mấy, 2–3 rủi ro lớn nhất, nhắc các skill khác (explain/frame/triage/partner) sẽ tái dùng folder này khỏi quét lại; nếu user mới, gợi ý `/explain` để học codebase theo mức của họ. Ghi `state/current.json` (project + updated_at).

- 0 — không có báo cáo bàn giao, HOẶC không nhắc folder được tái dùng, HOẶC không trỏ `/explain` cho người mới muốn học theo mức, HOẶC tự nhảy sang làm việc skill kế thay vì chỉ bàn giao.
- 1 — có bàn giao nhưng thiếu một mảnh: quên nêu scorecard/rủi ro, hoặc không nhắc skill nào tái dùng, hoặc không gợi `/explain`.
- 2 — báo đủ nơi dựng + scorecard + 2–3 rủi ro lớn + nhắc explain/frame/triage/partner tái dùng `.ai-understanding/`; gợi `/explain` cho user mới; ghi `state/current.json`; chỉ liệt kê, không tự chạy skill kế thay user.

## Gate

Tiêu chí **1 (Đủ bộ artifact — A1), 2 (Bám nguồn — A2), 3 (Đọc-được — A3)** là xương sống. Bất kỳ cái nào = 0 → bản **rớt gate**, ghi rõ rớt ở đâu, dù TỔNG cao. Bản đủ 20 file nhưng có một claim báo số/artifact từ thứ không tồn tại (tiêu chí 2 = 0) vẫn rớt — vì mọi skill hạ nguồn sẽ tin nhầm bản đồ. Khi so nhiều bản: loại hết bản rớt gate TRƯỚC, rồi mới xếp phần còn lại theo tổng.

## Khung report (xếp nhiều bản cạnh nhau)

```
CHẤM: atlas · <project> · <built_commit>
1 Đủ bộ artifact   [n/2] — <lý do 1 câu>
2 Bám nguồn        [n/2] — <...>
3 Đọc-được         [n/2] — <...>
4 Đúng vai         [n/2] — <...>
5 Freshness+Drift  [n/2] — <...>
6 Bàn giao         [n/2] — <...>
TỔNG: <n>/12   ·   GATE: đạt / RỚT ở <tiêu chí ...>
SỬA TRƯỚC TIÊN: <một câu — đòn bẩy lớn nhất để bản này tốt hơn>
```

## Vì sao 6 tiêu chí này

Ba xương sống đo *có ra đúng thứ + trung thực + đọc được không* (đủ bộ artifact đúng path, mọi claim có evidence file:line, đọc-được theo tầng) — trục A1/A2/A3, với A2 là gate nặng nhất vì lỗi lặp nhiều nhất của atlas là báo số/PASS/artifact từ thứ không tồn tại. Ba cái sau đo *có đúng kỷ luật riêng của atlas không*: đúng vai (dựng bản đồ, không sửa code, không lấn explain/triage — A4), freshness + drift ledger (chạy một lần rồi tái dùng, gấp đúng hai luật cứng còn lại — A4/A5), bàn giao (trỏ tái dùng + `/explain` — A5). Gộp lại = trọn hợp đồng của `atlas` trong SKILL.md, không hơn. Sáu tiêu chí thay vì bảy: atlas không phải skill pipeline GĐ (không có cổng GO/NO-GO đôi bên ký), nên trục cổng/traceability thu về "freshness + bàn giao"; thêm tiêu chí thứ 7 chỉ khi có kiểu lỗi thật lặp lại mà 6 cái này không bắt được.
