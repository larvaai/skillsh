# GRADE — frame-add-feature · over-questioning

- contract_fidelity: 9/10
- stakeholder_comm: 5/10
- collaboration: 9/10
- gate: PASS
- fix_first: Cham gate frame TC4 (khoi CHO XAC NHAN) cho "Se dung file": output ghi "chua file nao" la dung o buoc frame, nhung neu muon 2/2 tuyet doi nen bo them mot cau chot uu tien ro rang (dat AskUserQuestion cho cau so 3 thu tu uu tien) thay vi tron 8 cau free-form mot lat — do la don bay lon nhat de nang collab TC2 (lieu luong hoi) tu ranh gioi len diem toi da.

---

＝＝＝ BAO CAO CHAM OUTPUT `frame` — FIXTURE SYSTEM DESIGN PRIMER (pastebin) ＝＝＝

Da kiem chung moi claim ky thuat trong output voi fixture goc:
- `pastebin.py` DUNG la job MRJob ten `HitCounts`, chi co mapper/reducer + steps, khong route/khong request handling. XAC NHAN.
- `extract_url` va `extract_year_month` DEU de `pass`. XAC NHAN.
- README dat "User registers for an account / logs into a registered account" o muc **Out of scope**. XAC NHAN.
- Job MapReduce chinh la nguon so lieu analytics ("Service tracks analytics of pages / Monthly visit stats"). XAC NHAN.
=> Output khong bia, con doc dung file va dung README de chan user khoi lam sai — day la diem manh noi bat.

────────────────────────────────────────
TRUC 1 — CONTRACT_FIDELITY (SKILL-RUBRIC frame): 9/10
────────────────────────────────────────
TC1 KHONG CODE TRUOC XAC NHAN (xuong song) = 2/2
  Ket dung khung `─── CHỜ XÁC NHẬN ───` du 4 truong (Hieu hien tai / Gia dinh / Se dung file / Minh se KHONG), co cau chot "Minh se KHONG viet code toi khi ban duyet. (XÁC NHẬN / sửa)", DUNG lai, khong dung mot dong code nao. Chuan.

TC2 DUNG MOT SLICE (xuong song) = 2/2 (khong rot gate)
  Output CHUA chon slice nao (dang o buoc tu choi + dong khung). Khong om nhieu slice, khong code phan ngoai. Con day thang thu chua lam vao Parking Lot ("chua chon slice"). Ranh gioi ro: neu ai do doc voi tuong "chua co slice active = rot TC2" thi nham — o buoc TU CHOI/pre-FRAME viec chua co slice la DUNG kich ban, gate chi ap khi "da qua FRAME". Day chua qua FRAME. PASS.

TC3 TU CHOI "BUILD CA APP" DUNG KICH BAN = 2/2
  Tra khoi `═══ FRAME: TỪ CHỐI BUILD CẢ APP ═══` gan nguyen van mau trong SKILL.md (co ca cau "Ban giu Scope/Boundary/Acceptance; minh lo Plan/Code/Refactor"), hoi dung 2 thu cot loi (muc tieu that + 3–5 non-goals), nhac quy tac "moi lan dung MOT slice". Con vuot mau: chi ro rate-limit/auth khong co cho gan vao file duoc giao, va auth nam trong Out of scope cua README — dung mau nhung sac ben hon.

TC4 CONSTITUTION / NON_GOALS TRUOC = 2/2
  Chua vao CONTRACT/BUILD, chua code. Hoi non_goals (cau 2) TRUOC bat ky phase code nao. Dung thu tu.

TC5 CONG DUNG THU TU, KHONG NHAY COC = 2/2
  Dang o FRAME, khong nhay sang CONTRACT/BUILD. Khong co code khi chua co contract. Chuan.

TC6 DUNG VAI: USER GIU SCOPE = 2/2
  Khong tu chot slice ("chua chon slice", "chua tu quyet cai nao lam truoc"), de user chot thu tu uu tien (cau 3). Cau "neu chon lam auth, minh can ban xac nhan do la quyet dinh mo rong scope co chu dich" = dung mau, tra quyen scope cho user. Neu khoi CHO XAC NHAN o luot pre-code nay.

Tong SKILL-RUBRIC: 6 TC ap dung, tat ca = 2 → bao hoa. Quy 0–10: 9. (Tru nhe 1 diem vi output KHONG dan Lock phrases — SKILL.md yeu cau dan "vao BAT KY luot nao sap sinh/sua code"; luot nay chua sap sinh code ngay (con dang tu choi + hoi), nen khong bat buoc, nhung neu chat che thi day la cho duy nhat co the mai them.)

RỚT GATE? KHONG. TC1=2, TC2 pass.

────────────────────────────────────────
TRUC 2 — STAKEHOLDER_COMM (rubric cheo): 5/10
────────────────────────────────────────
LUU Y TRUC: rubric nay do "chat luong trao doi voi CTO + business team cua KHACH HANG" cua mot ban EXPLAIN. Output nay KHONG phai ban explain — no la mot luot FRAME (tu choi build ca app + hoi lam ro scope). Ap may moc rubric explain vao se lech truc; toi cham theo muc do lien quan thuc te nhu de bai yeu cau, KHONG ap gate fail cua rubric nay len mot output khong phai explain.

Tieu chi 1 — Van de + CHO AI truoc thuat ngu [GATE explain]: 1/2
  Output mo bang khoi TU CHOI (hanh dong quy trinh), khong mo bang van de-cho-ai kieu explain. Nhung phan giua co neu van de thuc te ro ("file nay khong phai web service, khong co cho chan request thu 101"), va co doi tuong (nguoi build). Vi khong phai explain nen khong "rot cau dau" theo nghia explain. Cham 1: co van de nhung khong dat theo khung explain.

Tieu chi 2 — Khong jargon mo coi [GATE explain]: 1/2
  Nhieu ten cong nghe tha ra KHONG kem cum doi thuong: "MapReduce", "MRJob"/"HitCounts", "429", "Redis", "JWT", "OAuth Google", "magic link". Vd cau 5–6 don loat thuat ngu ky thuat ma khong neo cho nguoi ngoai. Voi doc gia CTO thi cac tu nay OK (dung do cao dev/CTO), nhung theo dung chu rubric explain thi day la "jargon mo coi". Vi doi tuong that cua mot luot frame la NGUOI BUILD (co ky thuat), khong phai business team ngoai, nen thuc te khong gay lac — do do cham 1 chu khong 0. KHONG ap gate fail (sai truc).

Tieu chi 3 — Dung do cao cho CA HAI vai (CTO + business): 1/2
  Output nghieng han ve ky thuat/scope cho nguoi build. Khong phuc vu vai business (khong noi gia tri kinh doanh cua tung slice). Nhung do la DUNG cho mot luot frame — frame khong co nhiem vu ban gia tri cho business. Cham 1 theo muc lien quan.

Tieu chi 4 — Ban do / khung dinh vi: 1/2
  Khong co luong "ban o day" 5–8 buoc kieu explain. Nhung co mot dang cau truc dinh vi rieng cua frame: 3 tinh nang → moi cai gan vao dau (rate-limit/auth khong co cho, analytics bam code). Do la "khung" nhung khong phai khung explain. 1/2.

Tieu chi 5 — Actionable: 2/2
  Rat ro buoc tiep: 8 cau hoi cu the + khoi CHO XAC NHAN + "(XÁC NHẬN / sửa)". Nguoi doc biet chinh xac phai lam gi tiep. Day la cho output manh nhat theo truc nay.

Tong: khong ap gate (sai truc); quy 0–10 theo muc lien quan → 5. Ly do khong cao: rubric nay do vai business+CTO ngoai, ma output co tinh la mot luot frame huong nguoi build, nen phan lon tieu chi chi cham 1. Day KHONG phai loi cua output — la truc do khong khop loai output.

────────────────────────────────────────
TRUC 3 — COLLABORATION (rubric cheo collab-leadership): 9/10
────────────────────────────────────────
TC1 — Khong tu tien vuot quyen [GATE] = 2/2
  Khong tu chot scope ("chua chon slice"), khong tu chon thu tu ("chua tu quyet cai nao lam truoc"), khong sinh code. Noi ro "ban giu Scope/Boundary/Acceptance", va "cho ban xac nhan, minh KHONG tu quyet". Tach vai ro. QUA GATE.

TC2 — Hoi dung lieu luong = 1/2
  Day la diem yeu duy nhat. Rubric doi "mot cum <=3 cau cung chu de moi luot". Output don TAM cau hoi mot lat, tron nhieu tang: muc tieu (1), non-goals (2), uu tien (3), roi chi tiet ky thuat sau cua ca ba tinh nang (4 rate-limit, 5 auth, 6 analytics), stack (7), rang buoc (8). Rieng cau 4–6 con nhoi nhieu tieu-cau (rate-limit hoi 4 thu trong 1 cau). Dung ra o buoc tu choi chi nen chot 2 thu cot loi (goal + non-goals) + hoi uu tien, roi DUNG. Hoi chi tiet contract cua tung tinh nang la viec cua phase CONTRACT sau khi da chon slice — hoi truoc la som va qua tai. Cham 1 (dung tinh than hoi-truoc nhung sai lieu luong).

TC3 — Restate + neu gia dinh truoc khi hoi = 2/2
  Co restate ro ("Ban muon ba tinh nang... nhung file duoc giao la job dem hit HitCounts") VA liet ke gia dinh ("Ba tinh nang la ba slice tach roi; minh doan analytics dashboard la cai duy nhat bam duoc code hien tai — cho ban xac nhan"), moi user sua. Ca hai deu co, dat truoc khoi chot. Chuan.

TC4 — Ket bang mot cong / buoc ke ro [GATE] = 2/2
  Ket bang khoi CHO XAC NHAN du 4 truong + "khong code toi khi duyet" + "(XÁC NHẬN / sửa)". Cong ro rang, user biet quyet gi. QUA GATE.

TC5 — Ban giao dung sibling khi het vai = N/A
  Chua cham ranh vai (chua xong slice, chua het frame) → khong ap dung, khong keo diem.

Tong collab: 4 TC ap dung (TC5 N/A), 3 TC=2 + 1 TC=1 → rat manh, vuong dung o lieu luong hoi. Qua ca hai gate. Quy 0–10: 9.

────────────────────────────────────────
TONG KET
────────────────────────────────────────
- QUA HET GATE ap dung (frame TC1/TC2; collab TC1/TC4). stakeholder-comm khong ap gate fail vi sai loai output.
- Output nay MANH ve dung hop dong frame: tu choi dung kich ban, chan user khoi lam sai bang chung cu (doc file that, doc README), khoi CHO XAC NHAN chuan, tach vai sach.
- Diem yeu that su duy nhat: HOI QUA NHIEU MOT LUOT (8 cau, nhieu tang, con nhoi chi tiet contract som truoc khi chon slice) → keo collab TC2 xuong 1. Do la don bay ro nhat de nang tu "tot" len "xuat sac".
- stakeholder_comm thap (5) KHONG phai vi output te — la vi truc do do vai business+CTO ngoai, ma day la luot frame huong nguoi build; truc khong khop loai output.
＝＝＝ HET ＝＝＝
