# Board — <TÊN PROJECT>

Luật đọc/ghi board: `constitution/00-luat.md`. Chỉ agent điều phối đổi trạng thái.

| ID | Task | GĐ | Trạng thái | Phụ thuộc | Song song | Vùng chạm | Artifact |
|---|---|---|---|---|---|---|---|
| T01 | Nhận đề bài, dựng khung project | 0 | done | — | — | problem/, constitution/ | problem/00-de-bai.md |
| T02 | Họp làm rõ nghiệp vụ → Business Case → PRD | 1–4 | ready | T01 | — | problem/, docs/1x | docs/13-prd.md |
| T03 | Domain → kiến trúc → stack → live slice | 5–8 | todo | T02 | — | docs/2x, codebase/ | docs/23-live-slice-report.md |
| T04 | Roadmap + contracts + đổ task chi tiết vào board | 9–10 | todo | T03 | — | docs/3x, progress/ | docs/30-roadmap.md |
| T05 | Build theo board (fan-out khi đủ điều kiện) | 11 | todo | T04 | — | codebase/ | codebase/ |
| T06 | Verification + đối chiếu ưng ý + Runbook | 12–13 | todo | T05 | — | docs/4x | docs/41-ung-y.md |
| T07 | Ops & learn → đề xuất vòng mới | 14 | todo | T06 | — | docs/50-ops.md | docs/50-ops.md |

Ghi chú task (blocked ghi lý do ở đây):
- (trống)
