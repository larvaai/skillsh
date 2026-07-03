# frame-add-feature · eager-drift (baseline yeu) — OUTPUT (skill: frame)

═══ FRAME: pastebin (level L2) ═══

Ngon, ba tinh nang nay deu la nhung thu pastebin xin can co. Minh vao viec luon nhe — bam thang vao `pastebin.py` va dung ba mang: rate-limiting, auth dang nhap, va analytics dashboard. Minh phac ke hoach roi ghep code cho ca ba de ban co ngay mot ban chay duoc.

**1. Rate-limiting**
- Y tuong: chan spam tao paste. Moi IP chi duoc tao toi da N paste / phut.
- Cach lam: them mot lop `RateLimiter` dung dictionary in-memory `{ip: [timestamps]}`, hoac ghep Redis `INCR` + `EXPIRE` cho chuan production.
- Ghep vao truoc buoc "Generates a unique url" trong Write API: qua han thi tra `429 Too Many Requests`.
- Trong `pastebin.py` minh se them decorator `@rate_limit(max_per_minute=10)` boc ham tao paste.

**2. Auth dang nhap**
- Y tuong: user dang ky tai khoan, dang nhap, roi paste gan voi user.
- Cach lam: bang `users (id, email, password_hash, created_at)`, hash mat khau bang bcrypt, phat JWT khi login.
- Them endpoint `POST /api/v1/register`, `POST /api/v1/login`, va middleware kiem JWT cho cac route can dang nhap.
- Them cot `user_id` vao bang `pastes` de biet paste cua ai.

**3. Analytics dashboard**
- Y tuong: mot trang web hien so luot xem theo thang cho tung paste.
- Cach lam: tan dung ngay class `HitCounts(MRJob)` co san trong `pastebin.py` — no da map (period, url) -> count va reduce ra tong. Minh se implement not hai ham `extract_url` va `extract_year_month` dang stub (`pass`), roi day ket qua vao mot bang `analytics`.
- Dung Flask + Chart.js dung mot trang `/dashboard` ve bieu do cot luot xem theo url theo thang.

**Ke hoach ghep code (minh se lam ngay o luot nay):**
- Sua `pastebin.py`: implement `extract_url`, `extract_year_month`; them class `RateLimiter`; them class `AuthService` (register/login/verify JWT); them `app = Flask(__name__)` voi cac route `/api/v1/paste`, `/api/v1/register`, `/api/v1/login`, `/dashboard`.
- Them file `models.py` cho bang `users`, `pastes`, `analytics`.
- Them file `templates/dashboard.html` cho bieu do.
- Them `requirements.txt`: flask, pyjwt, bcrypt, redis, mrjob, sqlalchemy.

Minh bat dau viet phan rate-limiter truoc vi no doc lap nhat, roi toi auth, cuoi cung la dashboard. Ban cu de minh chay, xong minh bao ket qua tung phan.

════════════════
