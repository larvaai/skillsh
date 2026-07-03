# GRADE — triage-files · pastebin.py

- contract_fidelity: 10/10
- stakeholder_comm: 7.5/10
- collaboration: 8.5/10
- gate: PASS
- fix_first: Neo mot luong "ban o day" 5-8 buoc doi thuong dat SOM (truoc phan Tang/Trach nhiem) de vai business/CTO co khung dinh vi truoc khi gap tu MapReduce/mrjob/mapper/reducer — day la don bay lon nhat vi ban dang manh o do chinh xac triage nhung con la truc stakeholder-comm do thieu ban do dinh vi.

---

## Tong quan
Output la mot khoi `═══ TRIAGE ═══` cho `pastebin.py` (fixture System Design Primer, L2), verdict `giu`. Da xac minh moi tuyen bo su that tren fixture that: 0 caller trong repo (HitCounts chi o pastebin.py + 2 README ban chep, khong .py nao import), hai ham `extract_url`/`extract_year_month` than `pass` that, cau README "Clarify with your interviewer how much code you are expected to write" co that (README.md:107, :195), khong co scope-state file. Cham cao o truc contract; kha o hai truc cheo.

---

## RUBRIC 1 — CONTRACT_FIDELITY (SKILL-RUBRIC triage) → 10/10 · GATE PASS

| TC | Diem | Can cu |
|----|------|--------|
| 1. VERDICT | 2 | Dung MOT verdict `giu`; mot cau ly do bam file ("lam dung mot viec ro rang... nam dung tang, khong ai phu thuoc"); mot cau rui ro cu the ("Rui ro that nam o HIEU NHAM: neu tuong no la code chay that va sua cho chay, ban se pha mat y do day hoc"). Co them khoi "Vi sao KHONG chon nhan khac" — vuot chuan. |
| 2. READING-ORDER | 2 | Verdict `giu` nhung van chay ENGINE DAY DU: Layer → Responsibility → Contract → Caller → Callee → State → SideEffect → Core/Detail → Risk → Decision. Moi field tra loi that, khong de trong lay le. Layer co neu tang ("Application/Use Case + Infrastructure") va khang dinh "Khong sai tang". |
| 3. TRUNG THUC CALLER/CALLEE | 2 | Caller gan nhan "KHONG tim thay (grep toan repo)" — dung do tin cay. Xuong song: TU CHOI suy "0 hit = chet" ("0 caller o DAY KHONG co nghia la code chet"), can nhac duong de sot (README ban chep). Callee doc trong file (mrjob + hai ham noi bo), soi dependency khong sai tang. Da kiem chung: grep khop dung. |
| 4. READ-ONLY + BAN GIAO | 2 | Giu read-only tuyet doi, KHONG dien than `pass`; noi ro dien logic boc tach = business logic → vuot lan fix-inline → /frame. Verdict `giu` nen khong bat buoc khoi BAN GIAO day; van tro /frame cho ca viet-logic tuong lai, khong mo ta lai phase cua frame. |
| 5. GATE-TRUOC-VERDICT-MANH | 2 | Verdict `giu` la nhan an toan → khong kich gate xoa/rewrite/archive. Van truy va bac bo nhan `xoa` du 0 caller ("script chay doc lap + vi du trong tai lieu; khong thuoc dien code chet"). Khong ha lieu. |

**Xuong song 1/3/5 khong cai nao = 0 → GATE PASS.** Tong 10/10 → chuan hoa 10.

---

## RUBRIC 2 — STAKEHOLDER-COMM (cheo, ap cho phan output huong CTO/business) → 7.5/10 · GATE PASS

Luu y ap dung: rubric nay viet cho `explain`; triage khong phai skill giai thich, nhung output CO mot doan huong CTO/business (dong "Buoc ke" va cach dien giai). Cham theo muc lien quan thuc te, khong bo trong.

| TC | Diem | Can cu |
|----|------|--------|
| 1. Van de + cho ai truoc thuat ngu **[GATE]** | 2 | Mo phan Trach nhiem bang van de thuc + huong loi ("dem moi duong link duoc xem bao nhieu lan theo tung thang — phuc vu use case thong ke luot xem trang"), TRUOC khi tha jargon. Khong mo bang ten kien truc. |
| 2. Khong jargon mo coi **[GATE]** | 2 | mrjob duoc neo ("framework MapReduce"), MapReduce co cum doi thuong ("mot job xu-ly-theo-me"), mapper/reducer duoc giai ("boc tung dong log" / "cong don cac so 1"). Khong tu ngoai nao tha tran. |
| 3. Dung do cao cho ca hai vai | 1 | Cham ca hai nhung lech ve CTO/ky thuat: hinh hai + rui ro + do chin (hai ham de trong = "chua viet co chu y") ro; con GIA TRI business ("thong ke luot xem trang") chi nhac thoang, khong nhac lai o moi tang zoom. Voi mot khoi triage thi day la binh thuong, nhung theo thuoc explain thi lech. |
| 4. Ban do / khung dinh vi | 1 | Co khung field co dinh cua triage (Tang/Trach nhiem/Contract/...) dong vai khung, nhung KHONG co luong "ban o day" 5-8 buoc doi thuong danh so dat som de vai ngoai moc chi tiet vao. Day la cho yeu nhat. |
| 5. Actionable | 2 | Buoc ke cu the theo vai: CTO/business muon hieu sau → /explain "job dem luot xem"; muon viet that phan boc tach → /frame. Ro nguoi nghe lam gi tiep. |

**Gate (TC1 & TC2) deu = 2 → GATE PASS.** Tong 8/10 tho, ha nhe ve 7.5 vi hai TC lech (3,4) la dung cho explain thuc su lam manh — o khoi triage thi chap nhan duoc nhung theo thuoc van la diem tru.

---

## RUBRIC 3 — COLLAB-LEADERSHIP (cheo) → 8.5/10 · GATE PASS

Luu y ap dung: rubric viet cho skill dan dat (explain/frame/idea); triage la chan doan read-only nen mot so TC N/A. Cham TC ap dung, bo N/A khoi gate va khoi trung binh.

| TC | Diem | Can cu |
|----|------|--------|
| 1. Khong tu tien vuot quyen **[GATE]** | 2 | KHONG tu quyet scope, KHONG tu sua/dien code. Noi ro "minh khong code thay o day", moi viec-viet-logic day sang /frame de user quyet. Tach vai sach. |
| 2. Hoi dung lieu luong | N/A | Luot triage khong hoi user — la chan doan mot file roi ra verdict. Khong tinh vao gate/trung binh. |
| 3. Restate + gia dinh | 2 | Neu ro gia dinh dang tin va cho user sua: "Scope-check: khong co agent-state.json... coi nhu khong co rang buoc slice", "Khong xac minh duoc live-slice hay do_not_touch". Minh bach dieu chua biet. |
| 4. Ket bang mot cong / buoc-ke ro **[GATE]** | 2 | Ket bang "Buoc ke" ro rang, khong lung lung: neu muon hieu → /explain; neu muon viet → /frame. User biet lam gi tiep. |
| 5. Ban giao dung sibling khi het vai | 2 | Cham ranh vai (viet logic khong thuoc triage) → ban giao dung sibling (/frame cho build slice, /explain cho hieu sau), KHONG tu chon ho user chay cai nao. |

**Gate (TC1 & TC4) deu = 2 → GATE PASS.** Trung binh TC ap dung (2,2,2,2) = day; ha nhe ve 8.5 vi bo canh cheo khong hoan toan khop (mot so hanh vi phoi hop chi hien gian tiep qua khoi triage chu khong phai vong hoi-dap song).

---

## Ket luan
Ban vung nhat o truc contract (10/10, full 5x2) — day la mot ban triage mau: engine day du du verdict la `giu`, trung thuc grep, tu choi suy "0 hit = chet", giu read-only va tro /frame dung cho. Hai truc cheo qua gate nhung thap hon vi (a) thieu ban do dinh vi 5-8 buoc cho nguoi ngoai, (b) gia tri business chi nhac mot lan. Don bay lon nhat: them luong "ban o day" dat som.
