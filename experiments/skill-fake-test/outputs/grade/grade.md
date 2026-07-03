# CHẤM: explain · mediremind · L3 · overview

Bản chấm: `experiments/skill-fake-test/fixture/flawed-explain.md`
Chuẩn gốc: `explain/SKILL.md` + `explain/rule/principles.md`; thước: `explain/rubric.md`; khung: `grade/meta-rubric.md`.
Nguồn đối chiếu (kiểm bịa): `fixture/codebase/mediremind/**`.

```
CHẤM: explain · mediremind · L3 · overview

1 Mức        [0] — L3 mà nhồi jargon kiến trúc (orchestrator/DAG/microservices/event bus) và thả thẳng tên hàm dispatchDue()/confirmDose(); tên hàm chỉ được xuất hiện từ L4 (E4).
2 Chế độ     [0] — overview nhưng KHÔNG nói app làm gì / cho ai / vì sao tồn tại; mở bằng "orchestrator" rồi kể cơ chế kỹ thuật, đúng việc của flow chứ không phải overview.
3 Đủ ý       [0] — đọc xong không nắm được ý cốt lõi thật: đây là app nhắc uống thuốc chạy bằng 2 cron (sinh liều ban đêm + bắn nhắc mỗi phút); ý cốt lõi bị thay bằng một hệ tưởng tượng.
4 Lời văn    [0] — mở câu bằng tên kiến trúc (vi phạm E1 vấn-đề-trước-thuật-ngữ-sau), câu dài lồng nhiều mệnh đề nối "mà/rồi" (E2), dày đặc thuật ngữ không neo.
5 Bám code   [0] — bịa gần như toàn bộ: KHÔNG có Kafka/event bus, KHÔNG orchestrator/DAG, KHÔNG microservices, AdherenceService KHÔNG phải sidecar, confirmDose KHÔNG phát DoseConfirmed. Nhiều claim bịa.
6 Ranh giới  [1] — chủ yếu ở vai explain (không dựng .ai-understanding, không liệt edge case), nhưng lạm sang mô tả cơ chế như trace mà lại toàn cơ chế không có thật.
7 Kết        [0] — không có gợi ý bước tiếp; kết bằng một câu khẳng định sai ("event-driven microservices điển hình, throughput cao nhờ Kafka partitioning").

TỔNG: 1/14   GATE: RỚT ở tiêu chí 1 (Mức), 4 (Lời văn), 5 (Bám code) — cả 3 xương sống đều = 0
SỬA TRƯỚC TIÊN: Vứt toàn bộ kiến trúc tưởng tượng, viết lại từ code thật — một monolith in-memory nhắc uống thuốc, 2 cron (nightlyGenerate sinh DoseEvent, everyMinute gọi dispatchDue bắn push), confirmDose gọi thẳng AdherenceService — bằng lời L3 (vấn đề trước, không tên hàm).
```

---

## Bằng chứng đối chiếu code (trục A2 — gate nặng nhất)

Mọi claim kiến trúc trong bản explain được truy về code thật; hầu hết là **bịa**.

| Claim trong bản explain | Code thật | Phán |
|---|---|---|
| "orchestrator trung tâm điều phối job idempotent qua một DAG phụ thuộc" | `reminders/reminder.worker.ts`: chỉ 2 hàm cron phẳng `nightlyGenerate()` (00:05) và `everyMinute()`. Không orchestrator, không DAG, không phụ thuộc. Job KHÔNG idempotent (BUG-3: mỗi liều gửi tới 5 lần). | BỊA |
| "DoseEvent tới hạn → đẩy lên Kafka event bus" | `reminders/reminder.service.ts` `dispatchDue()`: lọc mảng in-memory `db.doseEvents` rồi gọi thẳng `pushProvider.send`. Không có Kafka ở bất kỳ file nào. | BỊA |
| "microservice Notification riêng consume để bắn push" | `dispatchDue()` gọi trực tiếp `pushProvider.send` trong vòng lặp. Không service riêng, không consumer. | BỊA |
| "AdherenceService là một sidecar tính rate theo eventual-consistency" | `adherence/adherence.service.ts` `rateFor()`: method đồng bộ, gọi thẳng trong tiến trình bởi `confirmDose()`. Không sidecar, không eventual-consistency. | BỊA |
| "`dispatchDue()` quét window rồi fan-out qua message queue" | `dispatchDue(now, windowMinutes=5)` CÓ quét cửa sổ [now, now+window] (đúng), nhưng "fan-out qua message queue" là bịa — thực chất là vòng `await pushProvider.send` tuần tự. | NỬA ĐÚNG (tên hàm + window đúng; message queue bịa) |
| "`confirmDose()` phát một `DoseConfirmed` event mà Notification + Adherence cùng subscribe" | `adherence/dose.controller.ts` `confirmDose()`: set `dose.status='taken'` rồi gọi thẳng `adherence.rateFor(...)`. Không phát event, không có `DoseConfirmed`, không subscriber. | BỊA |
| "kiến trúc microservices, mỗi bounded context một service, async qua Kafka" | Một monolith duy nhất; các folder `scheduling/reminders/adherence/identity` là module trong CÙNG một tiến trình; `common/db.ts` là repo in-memory chung; mọi lời gọi đồng bộ. | BỊA |
| "event-driven microservices điển hình, throughput cao nhờ Kafka partitioning" | Không event, không Kafka, không partitioning. | BỊA |

Điểm đúng duy nhất bám code: tên hàm `dispatchDue()` và `confirmDose()` có thật, và `dispatchDue` thật sự quét một cửa sổ thời gian. Nhưng ở L3, việc dẫn tên hàm đã sai mức (E4: tên hàm chỉ từ L4).

## Vì sao rớt gate (không chỉ tổng thấp)

3 tiêu chí xương sống (1 Mức, 4 Lời văn, 5 Bám code) đều = 0 — theo luật gate của `explain/rubric.md`, chỉ cần một cái = 0 là rớt, đây rớt cả ba. Nguy hiểm nhất là tiêu chí 5: người đọc L3 tin bản này sẽ đi dựng Kafka/microservices cho một app vốn chỉ là 2 cron in-memory — sai lệch dẫn tới quyết định tốn kém. Tổng 1/14 chỉ để xếp hạng; phán quyết thực là **RỚT GATE**.
