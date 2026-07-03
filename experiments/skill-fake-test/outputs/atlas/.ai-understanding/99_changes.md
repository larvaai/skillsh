# 99_changes — Pending changes & artifact drift

> last_synced_commit: n/a (không phải git repo — fixture không có .git)
> current_commit: n/a
> status: clean

## Pending (chưa cập nhật vào artifact)
| # | Date | Change (commit/PR/mô tả) | Files đổi | Artifact cần update | Status |
|---|------|--------------------------|-----------|---------------------|--------|
| – | – | (chưa có — atlas vừa build lần đầu) | – | – | – |

## Artifact đang stale (tổng hợp nhanh)
- (không) — bản vừa build.

## Quy ước
- Mỗi lần đổi code → thêm một dòng pending. Cột "Artifact cần update" suy từ 17_change_impact_map.
- Cập nhật xong artifact → đổi status dòng đó thành `applied`, bump last_synced_commit = current_commit.
- Pending quá nhiều / thay đổi lớn → chạy `/atlas` refresh (full).

## Raw inbox (git hook tự ghi — agent phân loại lên Pending rồi xóa dòng ở đây)
| Date | Commit | Subject | Files |
|------|--------|---------|-------|
| – | – | (không có git → hook post-commit không chạy được) | – |

## Ghi chú bản scaled
- Fixture KHÔNG phải git repo → không bump được commit; freshness check theo commit không áp dụng.
- Bản này là scaled (8 artifact + 4 flow). Nếu refresh full sẽ sinh nốt 03/10/13/16/19.
