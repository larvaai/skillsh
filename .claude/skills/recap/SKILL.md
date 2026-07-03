---
name: recap
description: "Tổng kết MỘT phiên làm việc từ bằng chứng git + trace, cho người làm cả buổi với Claude (nhiều worktree, nhiều approve) mà không nhớ hết: dựng lại TRƯỚC phiên vấn đề là gì → SAU phiên giải quyết được gì, mở đầu bằng TL;DR 'bạn có thêm khả năng gì', liệt kê đống dở dang chưa commit (MỌI worktree), đọc sổ phê duyệt (state/trace/ — cổng nào chặn, ai ký), và báo cách chạy project ĐÃ đổi chưa (hook/settings mới). CHỈ ĐỌC git log/reflog/diff/worktree + trace, không sửa/không commit hộ. Dùng khi: 'chiều nay tôi đã làm những gì', 'tổng kết phiên/buổi', 'recap', 'tôi đã approve những gì', 'so trước–sau buổi làm việc', 'có gì đổi cách chạy project không'. KHÔNG phải resume (trạng thái tĩnh MỘT project workspace) — recap là DIFF theo cửa-sổ-thời-gian của CẢ repo."
---

# Recap — Dựng lại buổi làm việc từ git, không từ trí nhớ

Sau một buổi làm việc dài (nhiều nhánh/worktree, sửa rải rác, Claude bắt approve nhiều thứ), user không nhớ hết là chuyện BÌNH THƯỜNG — vì git là sàn (CLAUDE.md), mọi thứ đáng nhớ đã nằm sẵn: commit, reflog, diff, worktree, `state/trace/`. `recap` đọc hết rồi in MỘT khối TRƯỚC → SAU. Nó KHÔNG ghi, KHÔNG sửa, KHÔNG commit hộ.

Ranh giới:
- `recap` ≠ `resume`: `resume` in trạng thái TĨNH của một project workspace ("đang ở đâu"); `recap` in DIFF theo cửa-sổ-thời-gian của cả repo ("buổi này đã đổi gì").
- `recap` ≠ `traceability`: `traceability` soi sợi pipeline một project; `recap` soi lịch sử phiên.
- `recap` chỉ NHẮC việc nên làm (commit lẻ, ghi CLAUDE.md, merge nhánh) + in sẵn lệnh; user tự chạy.

## Quy tắc bắt buộc

- **Read-only tuyệt đối.** Không ghi file nào, không `git add/commit/merge` hộ — kể cả khi đống dở dang "rõ ràng nên commit". Chỉ IN lệnh.
- **Mọi dòng phải có bằng chứng:** commit hash, file, hoặc dòng trace. Cái gì git không ghi thì nói "git không ghi" — KHÔNG nhớ hộ user bằng suy diễn.
- **Số đếm sinh từ LỆNH ĐẾM, không chép tay:** "N commit" = `git rev-list --count`, "N lần chặn/FAIL" = `grep -c` trên trace. Đây chính là meta-lỗi nặng nhất của cả suite (cite số tổng hợp không đếm lại từ nguồn) — recap mà chép tay số là tự phản bội lý do tồn tại.
- **Phủ MỌI nhánh + MỌI worktree:** buổi làm việc sống ở nhiều worktree thì `git log <BASE>..HEAD` và `git status` tại chỗ đều mù một phần — phải dùng `--branches` và lặp status qua từng worktree (Bước 1). Under-report âm thầm = báo thiếu vì không đếm đủ nguồn.
- **Giới hạn sổ phê duyệt nói thẳng:** nội dung từng lần approve trong chat KHÔNG nằm trong git; chỉ HỆ QUẢ của approve (file mới, hook được wire, cổng chặn trong `state/trace/`) là bằng chứng. Đừng bịa "bạn đã approve X lúc Y" nếu không có dòng trace.
- **TL;DR khả năng mới đứng-một-mình-được:** user chỉ đọc mục đó vẫn biết mình có thêm gì. Mỗi dòng dạng "chạy X giờ được thêm Y (bằng chứng)".
- **Hành-vi-mới là ưu tiên cao nhất:** hook/`settings.json`/CLAUDE.md đổi trong cửa sổ = cách chạy ĐÃ đổi (thường âm thầm) — phải nổi thành mục riêng, không chôn cuối, kèm hệ quả hành vi. Hook/settings đổi mà CLAUDE.md CHƯA ghi (kiểm bằng grep, đừng đoán) → việc "ghi CLAUDE.md" vào Nên-làm-ngay.

## Bước 0 — Chốt cửa sổ (BASE)

1. User nói mốc ("chiều nay", "3 giờ qua", "từ commit X") → dùng.
2. Không nói → tự tìm bằng `git reflog --date=iso`: khoảng nghỉ dài nhất gần nhất (gap > ~2h giữa hai entry) là ranh phiên; **BASE = commit cuối TRƯỚC ranh**. Chú ý: reflog là **per-worktree** — buổi làm chủ yếu ở worktree khác thì HEAD-log của nó nằm ở `.git/worktrees/<tên>/logs/HEAD`; nghi ngờ thì soi cả đó hoặc hỏi user. Fallback: `git log --since="6 hours ago"`.
3. **In BASE ra khối** (hash + giờ) để user chỉnh nếu sai — cửa sổ sai thì cả khối lệch.

## Bước 1 — Gom bằng chứng (lệnh cụ thể, chạy hết)

```
git log --branches <BASE>.. --date=iso --pretty='%h|%ad|%s|%D'   # việc đã đóng — MỌI nhánh, không chỉ ancestry của HEAD
git rev-list --count <BASE>..HEAD                                 # đếm commit bằng lệnh (thêm nhánh khác nếu diverge)
git reflog --date=iso                                              # hướng thử KHÔNG thành commit (per-worktree!)
git worktree list && git branch -vv                                # hướng còn mở, nhánh chưa merge/chưa push
# đống dở dang phải quét TỪNG worktree, không chỉ chỗ đang đứng:
git worktree list --porcelain | awk '/^worktree /{print $2}' \
  | while read w; do echo "── $w"; git -C "$w" status --short; done
git diff <BASE> --stat -- .claude/ CLAUDE.md bin/ scripts/         # cách chạy + engine đổi? (so BASE với working tree — bắt cả cái wire chưa commit)
grep -c <event> state/trace/<các-ngày-trong-cửa-sổ>.jsonl          # sổ phê duyệt: ĐẾM gate chặn / check FAIL / chữ ký, rồi mới đọc từng dòng
```

Suy **khả năng mới** CHỈ từ diff `<BASE>` tới tip MỌI nhánh trong cửa sổ (`--branches`, cộng working tree): SKILL.md nào thêm bước/engine → "skill X giờ làm được Y"; `bin/`/`scripts/` mới → lệnh mới chạy được; hook mới **và có trong `settings.json`** → guard mới đang sống (mới-mà-chưa-wire thì ghi rõ "chưa wire"). Mỗi dòng TL;DR neo một hash/file.

## Bước 2 — In khối recap

```
═══ RECAP — <BASE hash (giờ)> → <mốc cuối hash (giờ)> ═══
TL;DR — bạn có thêm khả năng:
  • <lệnh/skill>: <giờ làm được gì> (<hash/file>)
  • ...                                (≤6 dòng; không có gì mới → "không có khả năng mới — buổi này là <loại việc>")
TRƯỚC: <1–2 câu — tại BASE, vấn đề gì đang mở>
SAU:   <1–2 câu — đã giải quyết gì; N commit / nhánh / worktree — số từ rev-list>
Đống rải rác: <uncommitted/untracked TỪNG worktree + rủi ro mất, hoặc "sạch (đã quét N worktree)">
Sổ phê duyệt: <từ trace: N lần chặn/FAIL/ký (grep -c) + giờ, hoặc "trace trống trong cửa sổ">
Cách chạy ĐÃ đổi: <CÓ/KHÔNG — hook/settings/CLAUDE.md nào + hệ quả hành vi>
→ Nên làm ngay: <tối đa 3 gạch, MỖI gạch kèm lệnh in sẵn; nhiều lựa chọn ngang nhau thì liệt kê, không chọn hộ>
════════════════
```

Khối một màn hình. **Mốc hai đầu ghi rõ hash để mọi số trong khối tái lập được** — repo còn chạy tiếp thì số còn trôi. **Mọi timestamp quy về MỘT múi giờ** (local, ghi hậu tố +07/Z) — trace ghi UTC, git ghi local, trộn lẫn là người đọc hiểu sai buổi. Chi tiết dài (bảng việc↔bằng chứng, diff từng file) chỉ đưa SAU khối, khi user hỏi tiếp.

## Ví dụ (thật — buổi 2026-07-03/04, cửa sổ chốt cứng `cf330c6` → `0ef0db5`; giờ +07)

```
═══ RECAP — cf330c6 (07-03 23:38) → 0ef0db5 (07-04 00:39) ═══
TL;DR — bạn có thêm khả năng:
  • /resume: nhận alias/tên cũ (portfolio.py e5afa6d) + dòng "Sợi" kiểm máy (8aaccb4)
  • /traceability: soi sợi workspace bằng spine_check.py, hết soi mắt (bcad435·8aaccb4)
  • Lật done = script fail-closed bin/advance.py — hết tay lật phiếu chờ ký (8c4f2b0)
  • Đẩy một GO lên remote ĐÒI chữ ký người .sign.json (ff2931c)
  • Bash/ghi-config đi qua guard mới bash_safety + config_write_guard (8c4f2b0)
TRƯỚC: cổng toàn văn xuôi — AI tự ký GO được, progress lật done bằng tay.
SAU:   9 commit / 3 nhánh (rev-list: dot1 git-floor · dot2 chữ-ký · dot3 enforcement) + 3 engine + lưới test.
Đống rải rác: quét 2 worktree — chính .claude/skills/recap/ đang untracked (skill này chưa commit).
Sổ phê duyệt: gate_ship CHẶN 3 lần (00:05·00:11·00:35) · check_pipeline FAIL 5 lần (grep -c trên trace 07-03).
Cách chạy ĐÃ đổi: CÓ — 6 hook sống trong settings.json (5 mới wire trong buổi; track_skill_invocation có từ BASE); đã ghi CLAUDE.md ở 8c4f2b0.
→ Nên làm ngay: commit skill recap — `git add .claude/skills/recap && git commit -m "feat(skills): recap"`
               · quyết số phận nhánh dot1 — merge (`git merge feat/dot1-git-floor-push-guard`) hay xoá worktree
               · push dot2 bản mới — `git push origin feat/dot2-sign-evidence-gate`
════════════════
```

(Ví dụ này từng khai 6 commit/2 nhánh · 2 chặn/4 FAIL · "5 hook" — panel review đếm lại từ nguồn ra 9/3 · 3/5 · 6, đúng meta-lỗi chép-tay-số. Giữ lại dòng này làm sẹo nhắc: recap KHÔNG được chép số, phải đếm.)

## Khi cửa sổ trống

BASE..HEAD không có commit trên nhánh nào, mọi worktree sạch, trace trống → nói thẳng "cửa sổ này không có thay đổi ghi nhận được trong git" — đừng độn reflog cũ vào cho có. Gợi ý nới cửa sổ nếu user nghĩ là phải có.
