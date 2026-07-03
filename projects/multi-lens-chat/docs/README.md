# docs/ — hình hài (GĐ5–10)

Chưa tới. Folder này sẽ điền từ GĐ5 trở đi, theo lộ trình trong `../progress/board.md`:

- `domain-model.md` (GĐ5, `/idea`) — entity: Conversation, MainAgent, LensWorker, Insight; rule bất biến; domain event.
- `architecture.md` (GĐ6, `/shape`) — orchestrator + N worker, fan-out/gather.
- `tech-decision.md` (GĐ7, `/stack`) — Claude Agent SDK vs tự viết orchestrator.
- `contracts/worker-v1.md` (GĐ10, `/modules`) — hợp đồng orchestrator↔worker (task vào → insight ra). **Đây là cổng mở nhánh song song:** freeze xong thì các lens worker + orchestrator build song song qua `/fanout`.

Đang chờ chốt 3 open question ở `../problem/prd.md` trước khi bắt đầu domain.
