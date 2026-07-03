# GRADE — idea-new-feature · cost-capacity-calculator

- contract_fidelity: 8.3/10
- stakeholder_comm: 8/10
- collaboration: 8.8/10
- gate: PASS
- fix_first: O Router: dung tu dong dan "KHA THI RO" khi con an so "cost" chua kiem chung — hoi 1 cau lam ro bien do "cost" (chi QPS/storage hay keo gia cloud ngoai) TRUOC roi moi chot truc kha thi, va ghi ro "phuong an da loai" cho quyet dinh chon Nhanh C de audit duoc.

---

ð BAO CAO CHAM — output `idea` tren fixture System Design Primer

Da doc fixture that de kiem bia: MOI so lieu output neu deu KHOP verbatim voi repo (pastebin 12.7 GB/thang, ~450 GB/3nam, 4 write/s, 40 read/s; twitter 150 TB/thang = 10 KB x 500 trieu/ngay x 30; mint 250 GB = 50 byte x 5 ty; web_crawler 2 PB = 500 KB x 4 ty, 1.600 write/s; hang so "2.5 trieu giay/thang" + "1 req/s = 2.5 trieu req/thang" co that o nhieu bai; Powers-of-two / Latency / Back-of-the-envelope co that trong README). => KHONG BIA mot chi tiet nao. Day la diem manh nen tang xuyen suot ba truc.

==================================================================
RUBRIC 1 — SKILL-RUBRIC `idea` (7 tieu chi, 0/1/2)   RAW 10/12 -> 8.3/10
==================================================================

[TC1] ROUTER — phan loai do ro + do kha thi ............ 1/2
  Phan loai CA HAI truc, co can cu: do ro = "RO RANG (kha)" (biet cho ai, input/output, ranh gioi), do kha thi = "KHA THI RO" (cong thuc da ton tai + nhat quan 4 bai, du lieu tham chieu co san). Can cu tot va co that.
  Tru vi: TU CHOT "KHA THI RO" trong khi CHINH output nhan co an so "cost tinh toi dau" (option C keo bang gia cloud that = nguon NGOAI repo) — day dung la loai "con an so chua kiem chung" ma anchor 0 canh bao, va anchor cung phat "doan do kha thi ma chua hoi khi thieu thong tin (dang le hoi <=3 cau truoc)". Khong ha han xuong 0 vi phan feasibility LOI (QPS/storage) da duoc so that chung minh; an so cost chi cham bien do MVP chu khong chan duong. -> lech do-chot-kha-thi khi con an so = dung muc 1.

[TC2] DUNG NHANH — kha thi ro -> Nhanh C GD1->GD5 ...... 2/2
  "-> Di Nhanh C (di qua GD1 -> GD5)"; do ro cao nen "luot nhanh... chi dao sau cho con an so (dinh nghia cost)". Dung luat: do ro chi doi TOC DO trong C, khong doi duong. Chuan.

[TC3] HOI DUNG TANG — GD1 chi hoi pain/gia tri/metric ... 2/2
  Cum 3 cau GD1: (1) di tiep/dung, (2) nguoi dung chinh la ai, (3) "cost" hieu toi dau de dinh bien MVP. Tat ca tang Business. KHONG cham DB/framework/kien truc/stack/deadline. Cau cham tang sau (cost -> nguon du lieu ngoai) duoc PARK lai ("danh dau an so, can nhac o GD2, khong hua voi") thay vi tra non. Dung anchor 2.

[TC4] KHONG VUOT VAI ....................................... 2/2
  Tuyen bo ro "KHONG tu viet code, KHONG tu chon framework, KHONG tu kill"; Cau 1C "chi ban moi quyet kill, toi se ghi ly do cua ban, khong tu dap". Dung dung GD5 Domain lam ranh, chua cham code/stack/kien truc. Khong co cau phu dinh cung. Anchor 2.

[TC5] NHIP HOI + TRUY VET ................................. 1/2
  Nhip tot: DUNG mot cum <=3 cau cung chu de (Business), dang AskUserQuestion, khong don nhieu tang. Tru vi: quyet dinh lon "chon Nhanh C" co LY DO nhung THIEU "phuong an da loai" (khong noi vi sao khong di Nhanh B spike du co an so cost) — dung muc 1 cua anchor ("quyet dinh lon co ly do nhung thieu phuong an da loai").

[TC6] DU-LA-DU ............................................. 2/2
  Khong nhay coc giai doan; GD1 giu gon CO LY DO ("gia tri da kha ro va khong lon... khong dung Business Case 10 muc"). Do sau khop rui ro thap. Dung anchor 2.

[TC7] BAN GIAO ............................................. N/A
  Luot moi den cong GD1, chua toi GD5 nen chua den luc ban giao. Khong keo diem, khong tinh gate.

GATE idea: TC1..TC4 la xuong song. TC1=1 (khong =0), TC2=TC3=TC4=2 -> KHONG rot gate. Tong chuan hoa: 10/12 = 8.3/10.

==================================================================
RUBRIC 2 — CHEO STAKEHOLDER-COMM (5 tieu chi)   RAW 8/10 -> 8.0/10
==================================================================
(Do voi doi CTO+business khach hang. Luu y: day la output `idea` chu khong phai `explain`, nen mot so tieu chi "ban do/zoom" ap dung o muc lien quan thuc te.)

[TC1 GATE] Van de + CHO AI truoc thuat ngu ............... 2/2
  Mo dau bang VAN DE that ("moi bai giai nguoi hoc phai nhan chia tay cung mot bo so... de sai so mu") + CHO AI ("nguoi tu hoc luyen estimation; nguoi doc CTO/business muon ra so nhanh") bang loi doi thuong, TRUOC moi thuat ngu. Khong mo bang ten kien truc. -> qua GATE.

[TC2 GATE] Khong jargon mo coi ............................ 2/2
  Rat it thuat ngu code; "QPS", "back-of-the-envelope", "storage" deu di kem cum doi thuong ("QPS + storage + uoc luong cost", "tinh tay bo so"). Khong tha ten cong nghe ngoai tran (khong LangGraph/Redis... vi khong can). Nguoi ngoai khong gap tu mo coi. -> qua GATE.

[TC3] Dung do cao cho CA HAI vai (CTO + business) ........ 1/2
  Business duoc phuc vu ro (gia tri: tu dong hoa, giam sai so mu, thu "neu x10"; metric tai tao dung so co san). Nhung vai CTO chi THOANG: co "ranh gioi mot may tinh uoc luong gan vao moi bai, khong phai he production" va nhan an so cost la nguon ngoai — nhung THIEU do chin (phan nao xong/dang do) va rui ro ky thuat cu the. Cham ca hai nhung LECH ve business -> muc 1.

[TC4] Ban do / khung dinh vi ............................. 2/2
  Co khung dinh vi ro: khoi Router phan loai + lo trinh GD1->GD5 duoc neu som, va CONG GO/NO-GO GD1 dat moc "ban o day". Moi phan sau moc duoc ve mot giai doan. Voi dinh dang `idea` (khong phai explain overview) day la khung dinh vi day du. -> 2.

[TC5] Actionable: biet lam gi tiep ....................... 1/2
  Co buoc tiep ro tai cong ("chon Cau 1=A thi mo GD2 Product/PRD... dua tren dap an Cau 2-3"). Nhung huong tiep bam vao LUONG NOI BO cua skill, chua chi ro cho tung vai CTO/business nen doc gi/hoi gi ben ngoai; cung chua tro sibling (vi chua het vai). -> co huong nhung chua that cu the theo vai = muc 1.

GATE stakeholder: TC1=2 va TC2=2 -> QUA CA HAI GATE. Tong chuan hoa: 8/10 = 8.0/10.

==================================================================
RUBRIC 3 — CHEO COLLAB-LEADERSHIP (5 tieu chi)   RAW 7/8 -> 8.8/10
==================================================================

[TC1 GATE] Khong tu tien vuot quyen ...................... 2/2
  Tach vai ro: "KHONG tu viet code, KHONG tu chon framework, KHONG tu kill"; "chi ban moi quyet kill, toi se ghi ly do cua ban, khong tu dap"; scope cost de ngo cho user chon (Cau 3). Khong dong code, khong tu chot scope, khong tu kill. -> qua GATE, muc 2.

[TC2] Hoi dung lieu luong ................................. 2/2
  Mot cum <=3 cau cung tang Business, cau chot dang AskUserQuestion (Cau 1 A/B/C), cau kham pha (nguoi dung la ai) hop the. Khong don nhieu tang mot lat. -> 2.

[TC3] Restate + neu gia dinh truoc khi hoi ............... 1/2
  Co NEU GIA DINH ro va moi sua ("Muc nguoi doc lay theo boi canh: L2", "coi day la greenfield feature", "cold start", danh dau cost la an so). Nhung THIEU restate "toi hieu ban dang muon gi" tu loi user (fixture khong cho cau gia lap user nen restate nhu cau bi mong). Co mot trong hai (gia dinh manh, restate yeu) -> muc 1.

[TC4 GATE] Ket bang mot cong / buoc ke ro ................ 2/2
  Ket bang CONG GO/NO-GO GD1 minh bach: "Cau hoi cong: Dang dau tu di tiep GD2 khong?" + neu ro user chon gi de di tiep + "chua cham code". Dung tang, dut khoat. -> qua GATE, muc 2.

[TC5] Ban giao dung sibling ............................... N/A
  Chua het vai (moi GD1), chua den luc ban giao sibling. Khong tinh gate, khong keo diem.

GATE collab: TC1=2 va TC4=2 -> QUA CA HAI GATE. Tong chuan hoa (bo N/A): 7/8 = 8.8/10.

==================================================================
TONG HOP
==================================================================
- contract_fidelity (idea)   = 8.3/10  (gate pass; diem chim duy nhat: TC1 Router tu chot kha-thi-ro khi con an so cost + TC5 thieu phuong an loai)
- stakeholder_comm           = 8.0/10  (gate pass; lech ve business, vai CTO/do-chin/rui-ro con mong)
- collaboration              = 8.8/10  (gate pass; chi thieu restate hieu-biet truoc khi hoi)
- gate_pass = TRUE (khong rot bat ky gate xuong song nao cua ca ba rubric)

Diem noi bat: ky luat vai + neo bang chung repo tuyet doi (khong bia mot so nao), dung nhanh, hoi dung tang, ket bang cong ro.
Don bay lon nhat: sua Router — dung "khang dinh KHA THI RO" khi con an so cost chua kiem chung; hoi lam ro bien do cost truoc, va ghi phuong an da loai cho quyet dinh chon nhanh.
