# GRADE — explain-pastebin · problem-first-zoom

- contract_fidelity: 7.7/10
- stakeholder_comm: 9.4/10
- collaboration: 8.5/10
- gate: PASS
- fix_first: Bo hoac doi thuong-hoa ba ten code that (`pastes` -> "bang the tra cuu", `pastebin.py`/`HitCounts` -> "phan Python duy nhat lo dem luot") de khop nguong L2 (chi trich ten code tu L4) — day la cho duy nhat keo tut MUC/contract_fidelity.

---

# BAO CAO CHAM — explain / Pastebin (System Design Primer) — user L2 (map)

Da doi chieu MOI claim voi nguon that:
- `.../pastebin/README.md` (thiet ke)
- `.../pastebin/pastebin.py` (code that duy nhat: class HitCounts)
Ket qua fact-check: **khong co claim bia nao**. Bit.ly-vs-Pastebin, anonymous, 7 ky tu, MD5(ip+timestamp), Base62 [a-zA-Z0-9], 62^7 / 360 trieu shortlinks, tach bang `pastes` (shortlink/expiration/created_at/paste_path, PRIMARY KEY shortlink) khoi Object Store (S3), Web Server = reverse proxy, tach Write/Read API, 10:1 read:write, MapReduce web-server logs cho monthly hit-count, quet xoa paste het han, lop scale cache/read-replica/CDN — TAT CA khop README/py.

---

## TRUC 1 — SKILL-RUBRIC (contract_fidelity)  = 7.7/10  → **11/14, QUA GATE**

| # | Tieu chi | Diem | Ghi chu |
|---|----------|------|---------|
| 1 | MUC (xuong song) | **1** | Than bai dung do sau L2: mo bang van de, luong danh so 1-8, module chi diem nhu goi y. NHUNG tha 3 ten code that duoi nguong L4: `pastes` (ten bang), `pastebin.py` (ten file), `HitCounts` (ten lop). Rule line 15 + E4: duoi L4 khong trich ten file/code. Vi than bai va do sau van chuan L2, cham 1 (lech nhe 1-2 cho), khong 0. |
| 2 | CHE DO (overview) | **2** | Dung overview: LAM GI + CHO AI + VI SAO TON TAI deu co; ke theo thang zoom 0->2->cham 3, khong lan sang why/flow-tung-buoc-dung-cho. |
| 3 | DU Y | **2** | Du y cho pham vi overview L2: y tuong cot loi (2 kho tach nhau), ca 2 hanh trinh ghi/doc, 2 viec nen (dem luot, don han), 3 lua chon thiet ke duoc giai thich. Khong thua khong thieu. |
| 4 | LOI VAN (xuong song) | **2** | Cau ngan, phang, ke lien mach; bullet chi dung cho luong danh so va diem module cuoi — dung E3. Khong trich so dong. De doc. |
| 5 | BAM CODE (xuong song) | **2** | Moi claim khop code that (da fact-check tung dong). Khong bia file/API/hanh vi. `HitCounts`/`pastebin.py` co that. |
| 6 | RANH GIOI | **2** | Dung vai explain: day nguoi hieu theo muc, khong dung .ai-understanding/, khong dao trace/side-effect, khong liet edge-case, khong phan giu-xoa. |
| 7 | KET | **2** | Ket bang goi y dung muc L2->L3/L4: "di ky tung buoc (flow)" hoac "diem danh tung phan + trach nhiem (len L3-L4)", cong cau hoi dinh huong + hoi lai muc cuoi phien. |

**Gate:** TC1/TC4/TC5 khong cai nao = 0 -> **QUA GATE.** Chi TC1 = 1 keo diem. Neu giam khao khac coi "tha ten file/lop duoi L4" la lech RO (khong chi nhe) thi TC1 -> 0 va ban ROT GATE — day la ranh gioi mong nhat cua ban nay.

---

## TRUC 2 — STAKEHOLDER-COMM (stakeholder_comm)  = 9.4/10  → **9/10, QUA GATE**

| # | Tieu chi | Diem | Bang chung |
|---|----------|------|-----------|
| 1 | VAN DE + CHO AI truoc thuat ngu (GATE) | **2** | Cau mo: "Ban co mot doan text... muon dua cho nguoi khac xem. Dan thang vao chat thi dai, vo khung..." — van de doi thuong + nguoi huong loi ("bat ky ai can chia se mot khoi text qua mot duong link") TRUOC moi ten kien truc. |
| 2 | Khong jargon mo coi (GATE) | **2** | Moi ten cong nghe ngoai deu kem cum doi thuong: Web Server = "tram trung chuyen dung chan phia truoc", Object Store = "kho chua file rieng, kieu Amazon S3", MD5/Base62 = "bam...ma lai thanh chu-va-so an toan cho URL", MapReduce = "chia-de-dem". Khong tu mo coi. |
| 3 | Du do cao cho CA HAI vai | **2** | CTO: hinh hai (Web Server -> Write/Read API -> 2 kho), rui ro (trung ten -> bia lai), do chin (neu ro "day dung la phan Python duy nhat co trong bai, phan con lai chi la thiet ke tren giay"). Business: gia tri ("doc phai nhanh", "chi phi luu tru gon") nhac lai o moi tang zoom + doan "vi sao hinh hai nay dang". |
| 4 | Ban do dinh vi | **2** | Luong "ban o day" 8 buoc danh so, ngon ngu doi thuong, dat som; moi thuat ngu (Write API, bang the, Object Store, Read API) tro nguoc ve mot buoc. |
| 5 | Actionable | **2** | Neu ro 2 huong tiep hop nguoi nghe (di ky flow / diem danh phan len L3-L4) + moi hoi khuc cu the ("sao can ca cache lan read-replica", "ten ngan trung thi sao"). |

**Gate:** TC1 + TC2 = 2/2 -> **QUA GATE.** Day la truc manh nhat cua ban.

---

## TRUC 3 — COLLAB-LEADERSHIP (collaboration)  = 8.5/10  → **8/10 tren cac TC ap dung, QUA GATE**

| # | Tieu chi | Diem | Bang chung |
|---|----------|------|-----------|
| 1 | Khong tu tien vuot quyen (GATE) | **2** | Chi giai thich + de xuat huong; khong code/build/sua file, khong tu chot scope, khong tu quyet ho user. |
| 2 | Hoi dung lieu luong | **2** | Cuoi luot mot cum goi y + cau hoi cung chu de ("di sau phan nao?"), cong cau hoi muc cuoi phien — khong don qua nhieu tang mot lat. |
| 3 | Restate + gia dinh truoc khi hoi | **1** | Co restate muc hien tai ("Ban dang o L2 — da hieu nghiep vu, chua nam luong chay") va neo huong di theo do. Nhung KHONG neu gia dinh ngam ro rang de user sua (chi co MOT trong hai) -> 1. |
| 4 | Ket bang mot cong / buoc ke ro (GATE) | **2** | Ket bang cong ro: 2 lua chon buoc ke (flow / len L3-L4) + duong mo ("hoac chi toi khuc ban dang gon") + cau hoi chot muc. User biet quyet gi de di tiep. |
| 5 | Ban giao dung sibling khi het vai | **N/A** | Luot nay chua cham ranh vai (van trong overview L2, chua den L5+ de hand off sang trace/review/frame). Khong tinh gate, khong keo diem. |

**Gate:** TC1 + TC4 = 2/2 -> **QUA GATE.** Chi TC3 = 1 keo nhe (thieu ve "neu gia dinh").

---

## TONG HOP

- **Gate:** qua het gate cua CA BA rubric (SKILL-RUBRIC 1/4/5, stakeholder 1/2, collab 1/4). **gate_pass = true.**
- Ban rat manh o giao tiep stakeholder (9.4) va bam-code (khong bia mot claim nao). Diem yeu duy nhat co the nhin thay: 3 ten code that (`pastes`, `pastebin.py`, `HitCounts`) tha ra o muc L2, duoi nguong L4 ma rule/E4 cho phep trich ten file. Day la cho duy nhat lam contract_fidelity tut khoi diem toi da va la ranh gioi gate mong nhat cua ban.
- **Diem so:** contract_fidelity 7.7 · stakeholder_comm 9.4 · collaboration 8.5.
