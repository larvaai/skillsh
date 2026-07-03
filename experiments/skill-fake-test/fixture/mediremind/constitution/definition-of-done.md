# Định-nghĩa-Xong của một bước (MediRemind)

Một bước (một task trong `progress.json`) chỉ được coi là XONG khi đủ cả ba, không thiếu cái nào:

```
1. ARTIFACT   — file kết quả tồn tại đúng folder theo folders.md
                (không có artifact thì bước chưa xong, dù đã "bàn xong")
2. PHIẾU ĐẠT  — checkpoint kiểm và cấp verdict PASS ở progress/checkpoints/<task-id>.md
                (đúng path + đủ mục bắt buộc của giai đoạn + qua rubric nếu có)
3. PROGRESS   — progress cập nhật: task → done, mở khóa task phụ thuộc, dời con trỏ resume
```

Thiếu 1 → không có gì để kiểm. Thiếu 2 → chưa ai xác nhận nó đủ. Thiếu 3 → đồ thị không biết bước sau được phép chạy. Cả ba mới khép được một bước.

## Mục bắt buộc tối thiểu theo GIAI ĐOẠN (checkpoint kiểm)

| GĐ | Bước | Xong khi artifact có tối thiểu |
|---|---|---|
| 0 | Idea Intake | input/output rõ, một plan thô đi được, ẩn số lớn nhất nêu tên |
| 1 | Business | có ai đau + đau ở đâu (một câu cụ thể); success metric đo được (SM-1, SM-2); scope in/out |
| 2–4 | Product / Req / PRD | persona chính, user value, requirement có id, NFR số cứng (NFR-1..5), acceptance nằm dưới story |
| 5 | Domain | entity có identity + lifecycle (DoseEvent: pending→taken/missed/skipped), business rule bất biến, domain event, ranh giới 4 bounded context |
| 6 | Architecture | quyết định hình hài (modular monolith) + `rationale` + ≥1 `rejected_alternative`; C4 Context+Container; open-Q kiến trúc nêu tên (OQ-A) |
| 7 | Stack | Tech Decision Matrix có tiêu chí chấm điểm + `rationale` + phương án đã loại; spike nếu có ẩn số |
| 8 | Live Slice | slice chạy THẬT (staging + test E2E + log), Live Slice Report; chứng minh kiến trúc+stack+boundary |
| 9 | Backlog | Roadmap + Epic→Feature→Story→AC có traceability về business value; DoD tách khỏi AC |
| 10 | Contract | interface đủ để hai bên bám mà build độc lập (endpoint/field/kiểu, chữ ký hàm, domain event, error code, data ownership) — **đây là cổng mở nhánh song song** |
| 11 | Build / Delivery | Delivery Standards + DoD + PR Checklist; artifact code trỏ đúng path, gắn được về contract và AC; mỗi module build xong có test theo test-pyramid |
| 12 | UAT | Test & Verification Report: Requirement→AC→Test Case→Test Result→Release Decision; UAT sign-off + Security sign-off |
| 13 | Ship | Go/No-Go Checklist + Runbook + Rollback Plan (đã test) + Rollout Strategy; **cổng GO/NO-GO ký đủ CTO + PO** |
| 14 | Operate | Ops Dashboard (Business·Product·Engineering[DORA]·Operations) + Incident Process + Iteration Loop về GĐ9 |

## Luật cổng riêng của MediRemind

- **Cổng GĐ11 → GĐ12:** một module GĐ11 chỉ done khi code trỏ đúng path repo (pointer.md) + có test theo test-pyramid + không nới NFR-4 (kiểm quyền caregiver + audit-log). Nhóm `pg-build` chỉ được mở vì contract GĐ10 đã freeze (depends_on đã done).
- **Cổng GĐ12:** không có Test & Verification Report thì chain Req→Test đứt — chưa đủ điều kiện xét go-live.
- **Cổng GĐ13:** Go/No-Go chưa đủ 2 chữ ký (CTO + PO) và Rollback Plan chưa test thật thì cổng CHƯA qua, không release.
- **Open-question:** OQ-A (managed queue vs cron) và OQ-B (retention cho NFR-4) phải được đóng bằng ADR trước khi qua cổng GĐ13; còn treo thì ghi rõ ở progress, không coi là đã đóng.

## Vì sao siết ở đây

Yêu cầu của project: "mỗi bước xong phải có artifact và update vào folder tương ứng". Ba điều kiện trên biến câu đó thành thứ máy kiểm được, để `progress` không bao giờ đẩy nhánh sau khi bước trước mới nói miệng là xong.
