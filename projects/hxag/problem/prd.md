# PRD — HexAgent (GĐ4, bản đồng thuận 1 trang)

## Góc nhìn lãnh đạo
HexAgent biến chuỗi "giao task → tự plan → delegate → chỉ dừng khi xong" thành thứ **audit-được, chặn-được, tua-lại-được, không rò secret** — nhờ hai chốt đối nhau: một chốt bắt "chỉ xong khi đủ bằng chứng", một chốt "cắt cứng khi hết ngân sách / không tiến triển".

## Goals + success metric
- Goal: agent tự-điều-phối đạt **M1 zero-false-finish · M2 bounded · M3 no-escalation** (xem business-case).

## Scope
- **In (MVP):** task loop (plan→order→delegate→judge→finish) + budget/guards + event log + resume + redaction + scope enforcement.
- **Out:** UI realtime, RAG, department catalog, nới-ngân-sách-động (giữ META-cap).

## Rollout thô
Alpha nội bộ (write-tool + delegation TẮT) → pilot (bật write-tool sau khi redact-before-write xanh) → beta (bật delegation sau khi scope-property xanh) → gradual.

## Open questions (mang sang GĐ sau, KHÔNG bịa số)
- OQ-1: baseline chi phí + tỉ lệ false-finish thực + NFR-số (P95/alert) → đo ở Operate.
- OQ-2 (U1): resume atomic + không re-emit side-effect → SPIKE ở GĐ8.
- OQ-3 (U3): honor-system nghiệm thu (Agent-O tự chấm) → soi ở review; verifier độc lập pha sau.

## Cổng GĐ4: PRD đủ tin cậy để đi Domain? → GO.
