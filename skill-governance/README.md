# skill-governance — theo dõi & quyết định về skill

Thư mục này giữ hai việc tách bạch: **theo dõi skill của chính skillsh** (mới cài), và **phân tích harness hex_agent** (bản tham chiếu học theo).

## 1. Theo dõi skill của skillsh (đã cài, chạy tự động)

Từ giờ mỗi lần một skill trong `.claude/skills/` được gọi, nó được ghi lại. Không phải làm gì thêm — hook chạy khi bạn dùng skillsh như một project Claude Code.

Cơ chế, gồm ba mảnh:

`.claude/hooks/track_skill_invocation.py` — hook telemetry, self-contained (không phụ thuộc runtime harness). Nó đọc payload, lấy tên skill, ghi một dòng `{ts, skill, session, via}` vào log. Dedup theo phút. **Fail-open tuyệt đối**: stdin rác, đĩa đầy, lỗi gì cũng nuốt và trả `{"continue": true}` — không bao giờ chặn phiên của bạn.

`.claude/settings.json` — đăng ký hook trên hai sự kiện: `PreToolUse` (matcher `Skill`, khi model gọi qua Skill-tool) và `UserPromptExpansion` (khi bạn gõ `/tên-skill`). Đây là điểm cài đặt; xoá hai dòng này là tắt logging.

`state/telemetry/invocations.jsonl` — log, mỗi lần gọi một dòng. Tự sinh khi có lần gọi đầu tiên. Là runtime, không nên commit (đã cho vào `.gitignore`).

Xem việc dùng bất cứ lúc nào:

```bash
python3 skill-governance/skill_usage_report.py --days 30
```

Nó in: skill nào được gọi (xếp theo tần suất, kèm lần cuối), và skill nào **chưa** xuất hiện. Chạy `--format json` nếu muốn số thô.

Hai giới hạn phải nhớ, để không đọc sai:

Hook chỉ thấy skill gọi qua `/slash` hoặc Skill-tool. Skill bạn **mở SKILL.md đọc tay** thì không có bản ghi — "chưa dùng" trên giấy không chắc là chưa dùng thật.

Report áp **cổng-trung-thực**: chỉ gọi một skill là "ứng viên cắt" khi số-lần-gọi đã ≥ số-skill (mỗi skill trung bình có ≥1 cơ hội chạy). Dưới ngưỡng, "chưa dùng" chỉ là **danh sách theo dõi**, không phải danh sách cắt. Đừng cắt skill trên vài ngày dữ liệu.

Muốn báo cáo tự động: đặt scheduled task chạy lệnh trên mỗi tuần và gửi bạn bản md.

## 2. Phân tích harness hex_agent (tham chiếu)

`SKILL-GOVERNANCE.md` — quyết định giữ/bỏ/sửa cho 97 skill của `namnson/hex_agent/harness`, dựa trên log thật của nó (`invocations.jsonl` + 6 lens `analyze_telemetry.py`). Kết luận: chưa cắt được gì, vá ba lỗ đo trước.

`skill_decision_report.py` — bộ sinh báo cáo đó (chạy trên layout plugin `hs:*` của harness). `SKILL-DECISION.generated.md` là bản máy sinh.

Khác nhau chỗ nào: harness hex_agent dùng skill dạng plugin `hs:plan`, có khái niệm "skill-nhà vs vendored". skillsh dùng skill phẳng (`atlas`, `explain`…), tất cả là của bạn — nên bản cho skillsh (`skill_usage_report.py`) gọn hơn. Cùng một cổng-trung-thực.
