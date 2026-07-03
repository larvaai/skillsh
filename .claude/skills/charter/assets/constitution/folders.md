# Bản đồ 6 folder — artifact nằm ở đâu, ai điền

Folder gom theo KHÁI NIỆM, không theo số giai đoạn. Một khái niệm một chỗ, xoá/lưu trữ dễ.

```
projects/<key>/
├── constitution/   luật chơi (file này + process + conventions + definition-of-done)
├── problem/        WHY + WHAT: cái đau, việc tay hằng ngày, giá trị
├── idea/           hộp brainstorm: mỗi ý một file, prose mơ hồ → plan có input/output
├── docs/           hình hài: domain, kiến trúc, tech, contract, roadmap
├── codebase/       code thật (hoặc trỏ repo) + build/verify/ship/operate
└── progress/       đồ thị task + con trỏ resume
```

## Chi tiết từng folder

| Folder | Chứa | Giai đoạn | Skill điền (chủ artifact) |
|---|---|---|---|
| `constitution/` | process, conventions, folders, definition-of-done | — | `charter` gieo một lần |
| `problem/` | business-case.md, product-brief.md, requirements.md, prd.md | 1–4 | `idea` / `partner` |
| `idea/` | `<slug>.md` mỗi ý + `_index.md` | 0 | `idea` |
| `docs/` | domain-model.md, architecture.md, tech-decision.md, `contracts/`, roadmap.md, module-map.md | 5–10 | `shape` `stack` `backlog` `modules` |
| `codebase/` | pointer.md (trỏ repo thật + atlas) hoặc code; delivery-standards.md, uat-report.md, runbook.md, ops.md | 11–14 | `delivery` `uat` `ship` `operate` + `frame` |
| `progress/` | progress.json, board.md, `checkpoints/<id>.md` | xuyên suốt | `progress` (json+board), `checkpoint` (phiếu) |

## Quy tắc đặt artifact

Một task trong `progress.json` có trường `artifact` trỏ đúng path trong bảng trên. Khi bước xong, artifact phải nằm đúng chỗ đó thì `checkpoint` mới cấp PASS. Đặt sai folder = chưa đạt Định-nghĩa-Xong.

`state/project/<key>/` (ngoài workspace này) vẫn là nơi các skill giai đoạn giữ state máy riêng của chúng (idea-state, pipeline-state…). Workspace 6-folder không sở hữu các file đó, chỉ tham chiếu.
