# Requirements — HexAgent (GĐ3 WHAT EXACTLY)

## Functional (bắt buộc)
- R1: Nhận `Task` (mục tiêu NL + AC[] + budget) và trả trạng thái terminal + evidence.
- R2: Tự lập **plan** = cây bước (forest cha + DAG `depends_on`), có cổng cấu-trúc chứng-minh-dừng.
- R3: Chọn bước theo thứ tự deps; **delegate** cho sub-agent với scope con ⊆ cha.
- R4: Mọi hành động (LLM/tool) qua **một chokepoint** → trace + scope-check + envelope chuẩn.
- R5: **Nghiệm thu**: AC "đạt" phải trỏ ≥1 evidence THẬT (không scaffolding); worker không tự ghi verdict.
- R6: Chỉ FINISHED khi `all_accepted()`; guard chặn runaway (max bước/no-progress/repeat/depth).
- R7: Ghi `events.jsonl` + checkpoint SQLite; **resume** lại được từ checkpoint.

## Non-functional (có số nơi biết)
- NFR-1 (bảo mật): 0 secret thô trong `ui_payload` (redact tại biên); scope enforce fail-closed.
- NFR-2 (độ tin): resume một-lần-đúng, không re-emit side-effect (⚠ ẩn số U1 → đo GĐ8).
- NFR-3 (quan sát): mỗi capability call phát `tool.requested/completed`; replay(events)=snapshot.
- NFR-4 (chi phí): mọi run có trần bước/độ sâu; ngưỡng-số P95/alert = open-Q (đo ở Operate, không bịa).

## Ưu tiên
R2·R5·R6 (lõi finish-by-evidence có biên) = must; R7 (resume) = must nhưng có ẩn số; RAG/UI = won't (MVP).
