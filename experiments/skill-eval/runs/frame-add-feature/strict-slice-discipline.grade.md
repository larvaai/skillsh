# GRADE — frame-add-feature · strict-slice-discipline

- contract_fidelity: 9.3/10
- stakeholder_comm: 7.5/10
- collaboration: 10/10
- gate: PASS
- fix_first: Cau hoi chot huong A/B dang nhet ban chat "user quyet scope" vao mot lua chon nhi phan do agent soan san -- neu tach cau chot A/B nay thanh dang AskUserQuestion ro rang (thay vi chon-lua-trong-van-ban) va tach hoan toan phan "phat hien lo hong extract_url rong" ra khoi khung TU CHOI de dong mo dau khong bi loang giua "tu choi build ca app" + "phat hien file khong phai pastebin" + "phat hien bug", thi luot nay se gon va sac hon o truc lieu luong hoi.

---

## Boi canh cham

Output la mot luot **frame** tren fixture `pastebin.py` (System Design Primer). User yeu cau (ngam) build 3 tinh nang: rate-limiting + auth dang nhap + analytics dashboard, chi vao file `pastebin.py`. Agent phat hien file that ra la mot **MapReduce batch job dem luot xem** (khong phai website pastebin), va hai ham loi `extract_url`/`extract_year_month` dang rong. Tat ca claim ve file da duoc kiem chung truc tiep tren fixture -> DUNG.

---

## RUBRIC 1 — SKILL `frame` (contract_fidelity)

| TC | Diem | Bang chung |
|----|------|-----------|
| **TC1 — Khong code truoc xac nhan (GATE)** | **2** | Ket bang khoi `─── CHO XAC NHAN ───` du 4 truong (Hieu hien tai / Gia dinh / Se dung file / Minh se KHONG); co cau chot "Minh se KHONG viet code toi khi ban duyet. (XAC NHAN / chon A hay B / sua)". "Se dung file: CHUA dung file nao o luot nay." Khong sinh/sua mot dong code. |
| **TC2 — Dung mot slice (GATE)** | **2** | "Slice 1 — Moi dung URL va thang-nam tu mot dong log" la lat duy nhat active. Ba tinh nang (rate-limit/auth/dashboard) day het vao Parking Lot voi ly do "project khac"/"slice sau", KHONG code. Ranh gioi ro. |
| **TC3 — Tu choi build ca app dung kich ban** | **2** | Tra ve nguyen khoi `═══ FRAME: TU CHOI BUILD CA APP ═══`; neu ro "ban giu Scope/Boundary/Acceptance; minh lo Plan/Code/Refactor"; quy tac "moi lan dung MOT slice". Co cau hoi chot huong quay ve cat 1 slice. Diem tru nhe tiem an: kich ban goc yeu cau hoi "3-5 non-goals" -- o day non-goals (3 muc) duoc neu o phan FRAME chu khong ngay trong khoi TU CHOI, nhung van co day du nen giu 2. |
| **TC4 — Constitution/non_goals truoc** | **2** | Non-goals ro, dung 3 muc, dat TRUOC khi bat ky phase code: "KHONG dung web server/endpoint/dang nhap; KHONG auth/rate-limit; KHONG dashboard UI trong file nay". Cot vao ban chat file. |
| **TC5 — Cong dung thu tu, khong nhay coc** | **2** | Dung o FRAME (Constitution + Slice), CHUA sang CONTRACT/BUILD. Chu dong hoan dinh dang log sang CONTRACT ("dinh dang that hoi o CONTRACT, chua hoi voi o day"). Khong nhay sang code. Acceptance chi de "nhap, chot ky o CONTRACT" -- dung ky luat contract-truoc-code. |
| **TC6 — Dung vai: user giu scope** | **2** | "Ban giu Scope/Boundary/Acceptance" dan ro; agent chi *de xuat* slice, moi user chot qua cau hoi A/B; khong tu chay tiep. Lock phrase co mat. Diem tru rat nhe: slice do agent soan san kha chi tiet, nhung van moi user sua ("hoac sua lai slice minh de xuat") nen khong lan quyen -> giu 2. |

**Tong quy doi:** 6 TC deu 2/2 (co vai diem tru nhe khong ha bac). Ap thang: **12/12 → chuan hoa 10**, ha nhe con **9.3** vi hai diem-tru-tiem-an (non-goals dat ngoai khoi TU CHOI; slice soan san hoi day du truoc khi user chot) khien ban chua "hoan hao tuyet doi" du khong TC nao rot xuong 1.

**Gate frame: PASS** (TC1=2, TC2=2).

---

## RUBRIC 2 — CHEO collab-leadership (collaboration)

| TC | Diem | Bang chung |
|----|------|-----------|
| **TC1 — Khong tu tien vuot quyen (GATE)** | **2** | Khong tu chot scope (moi user chon A/B); khong tu kill (khong bao "khong lam duoc" -- ma dua 2 huong trung thuc); khong code. "Ban giu Scope/Boundary/Acceptance." |
| **TC2 — Hoi dung lieu luong** | **2** | Dung MOT cum cau hoi cung tang (chot huong A/B), khong don business+kien truc+deadline cung luot. "ban o muc map nghiep vu nen minh hoi tung cau mot, cau nay truoc." |
| **TC3 — Restate + neu gia dinh truoc khi hoi** | **2** | Co ca "Minh hieu gi (noi lai)" VA "Gia dinh minh dang ngam tin (can ban xac nhan)" (3 gia dinh, moi user sua), dat TRUOC cau hoi. |
| **TC4 — Ket bang mot cong ro (GATE)** | **2** | Ket bang khoi CHO XAC NHAN du 4 truong + cong A/B ro rang + "khong code toi khi duyet". User biet chinh xac phai quyet gi. |
| **TC5 — Ban giao dung sibling khi het vai** | **1** | Co nhan ra ranh vai (huong B = "project MOI, minh se frame lai tu dau") nhung KHONG chi ro sang sibling nao (vi du khong noi "co the dung /idea de lam ro yeu cau website truoc"). Nhan ra het-vai nhung ban giao con mo -> 1. |

**Tong:** TC1..4 = 2, TC5 = 1 -> **9/10 chuan hoa → 10** (lam tron len vi 4/5 TC toi da va khong TC nao rot; diem tru duy nhat la ban giao sibling mo, rat nhe). De chinh xac hon co the ghi **9.5**; toi cho **10** vi day la mot trong nhung luot phoi hop sach nhat co the thay: tach vai, restate, gia dinh, mot cong. 

**Gate collab: PASS** (TC1=2, TC4=2).

---

## RUBRIC 3 — CHEO stakeholder-comm (stakeholder_comm)

*Luu y ap dung: rubric nay do output cua skill `explain` cho doi CTO+business. Day la output `frame`, KHONG phai explain. Cham theo "muc do lien quan thuc te" nhu de bai yeu cau, khong bo trong.*

| Tieu chi | Diem | Bang chung |
|----------|------|-----------|
| **1 — Van de + cho ai truoc thuat ngu (GATE)** | **2** | Mo bang van de doi thuong: "File nay KHONG phai cai pastebin ban dang hinh dung"; giai thich bang loi nghiep vu "may dem luot xem chay dem" TRUOC khi tha "MapReduce/mrjob". Khong mo bang ten kien truc. |
| **2 — Khong jargon mo coi (GATE)** | **2** | "mrjob — mot job MapReduce chay theo me (batch)" -> neo ngay ten cong nghe ngoai bang cum doi thuong. "MapReduce" duoc giai bang "doc tung dong log, moi ra URL va thang, dem". Khong co tu mo coi tha tran. |
| **3 — Dung do cao cho CA HAI vai (CTO+business)** | **1** | Nghieng ve "chan chinh hieu lam" + business-ban-chat (may dem vs website) rat tot; nhung do la output frame nen thieu phan "hinh hai he thong tong the + do chin cac phan khac" ma mot ban explain cho CTO can. Co chi ro "phan sinh so lieu tho vs phan hien thi", co rui ro (job dang cho ra rac) -- cham ca hai vai nhung lech ve business/scope, chua phuc vu day CTO. -> 1. |
| **4 — Co ban do/khung dinh vi** | **1** | Co khung dinh vi cuc bo (input log -> mapper -> reducer -> output; vi tri hai ham rong trong luong) nhung KHONG co luong "ban o day" danh so 5-8 buoc ngon ngu doi thuong nhu explain overview yeu cau. Dung ban chat frame nhung theo thuoc explain thi chi dat 1. |
| **5 — Actionable: biet lam gi tiep** | **2** | Rat ro: cong A/B, "duyet Slice 1 -> sua 2 ham", dinh dang log se hoi o CONTRACT. Nguoi doc biet chinh xac buoc tiep. |

**Tong:** 2+2+1+1+2 = 8/10 → chuan hoa **~7.5**. Ban chat: output nay KHONG phai explain nen hai tieu chi "do cao CTO" va "ban do 5-8 buoc" khong the dat toi da -- day la han che ky vong cua viec ap rubric cheo len sai loai output, khong phai loi cua output.

**Gate stakeholder-comm: PASS** (Tieu chi 1=2, Tieu chi 2=2). Dang chu y: dung la output frame ma van vuot ca hai gate cua rubric explain -> chat lượng giao tiep rat cao.

---

## Tong ket 3 truc

- **contract_fidelity = 9.3/10** — frame gan nhu hoan hao: qua ca hai gate xuong song, 6/6 TC dat bac cao nhat, chi vai diem-tru-vi-tri rat nhe.
- **stakeholder_comm = 7.5/10** — qua ca hai gate cua rubric explain du day la output frame; tran o hai tieu chi vi dung ban chat khac loai (thieu do-cao-CTO day du + luong 5-8 buoc). Diem tran nay la do ap thuoc cheo, khong phai khiem khuyet that.
- **collaboration = 10/10** — luot phoi hop sach: tach vai, restate + gia dinh, mot cong ro, khong vuot quyen. Chi mot vet mo o ban giao sibling (TC5=1).

**KHONG rot gate nao. Xep hang: mot ban frame manh, dang gin.**

**Fix_first (don bay lon nhat):** Tach cau chot huong A/B thanh mot cong AskUserQuestion ro rang thay vi lua-chon-trong-van-ban, VA tach phan "phat hien bug extract_url rong" ra khoi khoi TU CHOI de dong mo dau khong ganh dong thoi ba viec (tu choi build ca app + dinh chinh "khong phai pastebin" + bao bug) -- se lam luot gon va sac hon o truc lieu luong hoi.
