# GRADE — idea-new-feature · per-exercise-self-review

- contract_fidelity: 7.4/10
- stakeholder_comm: 6/10
- collaboration: 8.5/10
- gate: PASS
- fix_first: Tach luot hoi: giu lai DUNG cau WHY/pain (Q2) o GD1, day Q1 (rubric cham cai gi) thanh mot cum GD0-disambiguation RIENG truoc do, va hoan Q3 (rubric chung hay rieng tung bai — la cau WHAT/scope thuoc GD2-4) sang sau cong go/no-go; nhu vay moi luot chi mot tang, nang TC3 tu 1 len 2.

---

bao cao duoi day cham theo 3 rubric ap dung. Output la mot luot chay `idea` tren fixture System Design Primer (da doi chieu: repo co README voi khung 4 buoc "How to approach", va solutions/system_design co dung 9 bai + template — output KHONG bia).

════════════════════════════════════════
RUBRIC 1 — SKILL-RUBRIC `idea` (7 tieu chi, 3 truc chinh)
════════════════════════════════════════

TC1 — ROUTER (xuong song): 2/2
  Phan loai ca hai truc, co can cu ngan, khop ban chat.
  - Do ro = "hoi mo ho" + neu 3 an so cu the: cham cai gi / cham bang cach nao / song o dau. Can cu that, khong dan nhan bua.
  - Do kha thi = "kha thi ro" + ly do: "them noi dung Markdown vao repo von toan Markdown, khong co an so ky thuat" va "4 buoc How-to-approach da la bo tieu chi de dung checklist". Chuan.
  - Khong doan mo: no phan loai kha thi dua tren bang chung repo, khong che deadline/stack. Dat anchor 2.

TC2 — DUNG NHANH (xuong song): 2/2
  kha thi ro -> Nhanh C, dung. Va no phat bieu dung luat: "Vi do ro con hoi mo ho, toi se hoi ky hon mot chut o moi tang chu khong luot" — do ro doi TOC DO, khong doi duong. Bam sat hop dong.

TC3 — HOI DUNG TANG (xuong song): 1/2  ← diem yeu chinh
  Luot duoc dan nhan "GD0 -> GD1" nhung cum 3 cau tron tang:
  - Q2 (cung-dau nhat la gi) = dung tang GD1 (WHY/pain). Tot.
  - Q1 (rubric soi vao cai gi: cham bai tu viet / cham muc hieu bai mau / ca hai) = cau ve DOI TUONG-CUA-TINH-NANG, tang WHAT. No tu bao la "GD0 disambiguation" truoc WHY — co ly (phai biet cham cai gi moi noi duoc pain), chap nhan duoc.
  - Q3 (mot rubric chung hay moi bai mot rubric rieng) = cau ve HINH DANG GIAI PHAP / scope, ro rang thuoc GD2-4, noi len qua som.
  KHONG rot ve 0: khong cau lech tang nao bi tra non tai cho — Q1/Q3 duoc dat thanh lua chon mo cho user, va ket luot bang cong "chot WHY roi moi sang GD2-4". Vi co park chu khong tra non, dat anchor 1 (lo cham 1+ cau sai tang nhung ghi nhan mang sang sau).

TC4 — KHONG VUOT VAI (xuong song): 2/2
  - Khong tu kill: khong mot cau phu dinh cung nao; khong ghi killed.
  - Khong tu build: noi thang "toi khong dung toi chuyen dung bang cong cu gi hay viet file that vao repo".
  - Dung dung Domain: neu truoc se dung o tang Domain (chot thuc the Bai tap/Rubric/Tieu chi/Lan tu cham + luat bat bien) roi ban giao, khong troi sang Architecture.
  - Con ton trong luat "khong tu tao file trong repo brownfield": "toi se hoi ban truoc khi ghi bat cu artifact nao vao chinh repo". Dung Quy-tac-bat-buoc. Manh 2.

TC5 — NHIP HOI + TRUY VET: 1/2
  - Mot cum nhung HOI QUA TAI: 3 cau x 3 chu de (doi tuong cham / pain / hinh dang rubric) trong mot luot — dung so luong <=3 nhung khong "cung chu de". Sat anchor "1 luot hoi qua tai".
  - Truy vet: chua co quyet dinh lon nao duoc CHOT (dang o buoc hoi, chua qua cong) nen dieu khoan "ly do + phuong an loai" chua kich manh; phan Router co ghi ly do chon nhanh. Chap nhan, nhung vi qua tai nen dung 1.

TC6 — DU-LA-DU: 2/2
  - Khong nhay coc giai doan: dang o GD0->GD1, chua bom PRD/Business Case day du cho viec chua chot — dung tinh than "ru gon do sau, khong nhay coc".
  - Do sau bam rui ro: vi con mo ho nen dung muc "hoi lam ro" thay vi phun artifact non. Neu truoc Domain se chot entity+rule o muc vua du. Khong thua khong mong. 2.

TC7 — BAN GIAO: 2/2 (moi la khoi "CHO XAC NHAN", chua den luot ban giao thuc — nhung phan preview ban giao dung)
  Chua toi GD5 nen chua ra khoi Ban giao that. Tuy vay no da preview dung sibling: "/frame hoac /partner sau nay", dung vai. Khoi ket la "CHO XAC NHAN" + cong go/no-go — dung nhip. Khong tu chon ho skill nao. Cho diem theo phan da the hien: 2.

Tong SKILL-RUBRIC: 2+2+1+2+1+2+2 = 12/14. Khong rot gate (ca 4 truc xuong song >0).
Chuan hoa 0-10: 12/14 x 10 ≈ 8.6, tru nhe ve TC3+TC5 (hai diem 1 deu la loi that ve ky luat hoi) -> contract_fidelity = 7.4.

════════════════════════════════════════
RUBRIC 2 — CHEO stakeholder-comm (do "ban explain" — ap theo muc lien quan vi output la `idea`)
════════════════════════════════════════
Luu y: rubric nay viet cho output cua `explain` (giao tiep voi CTO+business). Output nay la `idea` dang o pha hoi, chua phai ban giai thich hoan chinh — nen cham theo muc do lien quan, khong ep khung.

TC1 — VAN DE + CHO AI truoc thuat ngu (GATE): 2/2  PASS
  Mo dau bang vai tro + viec ("nhan y tuong tinh nang moi... phan loai... dan qua tung tang"), roi neu boi canh repo bang loi doi thuong ("cuon cam nang hoc thiet ke he thong"). Khong mo bang ten kien truc/ten code. Ai dau = "nguoi hoc tu luyen". Dat 2.

TC2 — KHONG JARGON MO COI (GATE): 2/2  PASS
  Cac tu ky thuat deu duoc neo bang loi thuong: "checklist/rubric de tu cham loi giai cua chinh minh", "4 buoc How-to-approach". Ten thu muc solutions/system_design co kem giai thich "9 bai giai mau". Khong tha tu mo coi cho nguoi ngoai. 2.

TC3 — DU DO CAO CHO CA HAI VAI (CTO+business): 1/2
  Output nghieng ve business/nguoi-hoc (pain, gia tri hoc tap) va ve ranh gioi vai skill. Chua co "hinh hai he thong / rui ro / do chin" cho CTO — nhung do la vi `idea` co tinh DUNG truoc kien truc, nen thieu nay mot phan la do vai. Cham ca hai nhung lech: 1.

TC4 — BAN DO / KHUNG DINH VI: 1/2
  Co neu khung ("4 buoc How-to-approach", "WHY -> WHAT -> WORLD MODEL") va lo trinh tang, nhung chua co luong "ban o day" 5-8 buoc doi thuong danh so de moi chi tiet moc nguoc ve. Co dang khung nhung so sai. 1.

TC5 — ACTIONABLE: 2/2
  Ket rat ro buoc tiep: tra loi 3 cau (nhat la Q1), roi se chot WHY va dua cong go/no-go; va tro sibling dung (/frame, /partner) cho pha sau. Nguoi nghe biet lam gi tiep. 2.

Gate stakeholder-comm: TC1=2, TC2=2 -> PASS.
Tong ap dung: (2+2+1+1+2)/10 = 8/10 tho, nhung vi rubric nay do dung "ban explain" ma output la `idea` (thieu do-chin/hinh-hai cho CTO la ban chat vai, khong phai loi) -> ha ve muc lien quan thuc te: stakeholder_comm = 6.

════════════════════════════════════════
RUBRIC 3 — CHEO collab-leadership
════════════════════════════════════════

TC1 — KHONG TU TIEN VUOT QUYEN (GATE): 2/2  PASS
  Tach vai ro: "toi khong tu viet code, khong tu khai tu y tuong". Neu ranh gioi "toi se hoi ban truoc khi ghi bat cu artifact nao vao repo". Khong tu chot scope, khong dong chu code. Manh 2.

TC2 — HOI DUNG LIEU LUONG: 1/2
  Mot cum <=3 cau nhung tron nhieu tang (doi tuong cham + pain + hinh dang rubric) — dung anchor "so luong dung nhung lech, tron nhieu tang". Cau chot dung dinh dang lua chon A/B/C (tot cho AskUserQuestion). Dat 1.

TC3 — RESTATE + NEU GIA DINH TRUOC KHI HOI: 2/2
  Co restate hieu-hien-tai ("Boi canh toi thay: README la cuon cam nang... solutions/ co 9 bai...") va co neu gia dinh ngam ("Do kha thi: kha thi ro" kem ly do de user sua). User co cho de nan lai. 2.

TC4 — KET BANG MOT CONG (GATE): 2/2  PASS
  Ket bang khoi "CHO XAC NHAN" + noi ro se xin cong go/no-go "Dang dau tu di tiep khong?" sau khi chot WHY. Dung tang, minh bach buoc ke. User biet phai quyet gi. 2.

TC5 — BAN GIAO DUNG SIBLING: 2/2 (som nhung dung)
  Chua het vai (moi GD0->GD1) nhung da liet ke sibling dung vai cho pha sau (/frame, /partner) va KHONG tu chon ho. Dung anchor 2.

Gate collab: TC1=2, TC4=2 -> PASS.
Tong: (2+1+2+2+2)/10 = 9/10 -> collaboration = 8.5.

════════════════════════════════════════
TONG KET
════════════════════════════════════════
- gate_pass = TRUE (qua het gate cua ca 3 rubric).
- Diem: contract_fidelity 7.4 | stakeholder_comm 6 | collaboration 8.5.
- Diem manh nhat: giu vai (khong tu kill / khong tu build / dung dung Domain), Router co can cu that tu repo, ban giao + restate + cong go/no-go ro.
- Diem yeu chung (lap lai o ca SKILL TC3/TC5 va collab TC2): mot luot hoi tron nhieu tang (WHY lan WHAT). Do la don bay lon nhat de len diem.
