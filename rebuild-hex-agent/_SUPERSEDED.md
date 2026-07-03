# ⚠️ SUPERSEDED — bản cũ, không phải nguồn chuẩn

Thư mục này (`rebuild-hex-agent/`) là **pipeline bản cũ** của project **hxag**. Nó
được giữ lại vì nhiều tài liệu còn link tới (harness-design.md, reports,
experiments/) — **không xoá**, nhưng **không phải nơi làm việc hiện tại**.

**Nguồn chuẩn bây giờ:**
- Workspace: [`projects/hxag/`](../projects/hxag/) (layout 6-folder, schema 1)
- State máy: `state/project/hxag/`
- Con trỏ + sổ cái: `state/current.json` · `state/portfolio.json`

Mọi khoá cũ của project này (`hex-agent-rebuild`, `hex_agent`, đường-dẫn tuyệt
đối) đã được `state/portfolio.json` gộp về **một key: `hxag`**. Kiểm:
`python3 scripts/portfolio.py resolve rebuild-hex-agent`.
