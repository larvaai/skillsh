# GRADE — explain-pastebin · analogy-business-heavy

- contract_fidelity: 9.5/10
- stakeholder_comm: 10/10
- collaboration: 9.5/10
- gate: PASS
- fix_first: Neo `pastebin.py` mot nhip nua (noi ro no la file that duy nhat NGAY khi lan dau nhac o phan "nguoi dem luot xem", thay vi de doc gia doi toi ghi chu cuoi moi ro) — do la cho duy nhat mot ten file that xuat hien duoi nguong L4, va lam vay se khoa not khe ho nho nhat cua ban von da rat manh.

---

## Bao cao cham — output `explain` tren fixture Pastebin (System Design Primer)

**Da doi chieu moi claim voi fixture that** (`.../system_design/pastebin/README.md` + `pastebin.py`). Tat ca chinh xac. Output tu khai bao muc **L2 (map)**, che do **overview**. Cham theo dung muc/che do do.

---

### TRUC 1 — CONTRACT_FIDELITY (SKILL-RUBRIC 7 tieu chi) = 9.5/10 · GATE PASS

| TC | Diem | Ghi chu |
|----|------|---------|
| 1. MUC (xuong song) | 2 (lech nhe) | L2 = dung o Zoom 2 (ban do luong), neo entrypoint + luong chinh, ten module chi nhu goi y. Output lam dung: hai chuyen gui/lay ke thanh luong danh so 1-7, ten module deu la cum doi thuong ("cua truoc", "quay ghi", "kho chua", "so cai") chu khong phai ten code tran. Do sau khop L2 — co y GIU LAI base62/MD5/7-ky-tu-vi-sao cho phan "dao sau" chu khong do ra. Lech nhe duy nhat: co nhac ten file that `pastebin.py` (va `foobar`) — duoi nguong L4 theo E4 la hoi som, nhung duoc bao boc trong ghi chu "code that duy nhat" nen chua thanh "sai muc ro". Khong rot gate. |
| 2. CHE DO (overview) | 2 | Bam dung thang zoom: Zoom 0-1 (van de + cho ai + y tuong cot loi mot cau) → Zoom 2 (ban do "ban dang o day" danh so) → cham Zoom 3 (hai worker nen + "vi sao hinh hai nay dang tin"). Overview co du LAM GI / CHO AI / VI SAO TON TAI. |
| 3. DU Y | 2 | Nam tron loi cot loi: tach chu nang khoi the nhe; doc gap 10 lan ghi nen duong doc phai nhanh/re; hai chuyen; hai worker nen (dem luot, don rac); nhip mo rong quy mo. Khong thieu y cot loi nao trong pham vi L2. |
| 4. LOI VAN (xuong song) | 2 | Cau ngan, phang, ke thanh cau chuyen; vi von doi thuong ("tu gui do o sieu thi", "cai the so nho"). List danh so chi dung cho luong (dung cho — day la ban do luong, khong phai tuong-bullet ne viet cau). Khong trich so dong. Rat de doc. PASS. |
| 5. BAM CODE (xuong song) | 2 | Moi claim khop README: "cua truoc"=Web Server reverse proxy; hai quay=Write/Read API tach rieng; the 7 ky tu kieu `foobar`; "ngo so cai xem trung khong, trung thi lam lai"=check SQL duplicate; "kho chua"=Object Store; "so cai"=bang pastes (shortlink/created_at/expiration); luong doc check-SQL→fetch-ObjectStore→loi; 10:1; MapReduce dem log khong realtime; don paste het han; hang tram trieu luot/thang=100M reads. TRUNG THUC noi bat: co han ghi chu rieng rang "code that chi co dung mot mau (nguoi-dem-luot-xem), phan con lai la mo ta kien truc khong phai code chay duoc" — dung E5 "gan nhan cho chua chac". Khong bia gi. PASS. |
| 6. RANH GIOI | 2 | Dung vai explain: day nguoi hieu theo muc. Khong dung `.ai-understanding/` (atlas), khong dao side-effect (trace), khong liet gap/edge-case (review), khong phan giu-xoa (triage). |
| 7. KET | 2 | Ket bang 3 goi y buoc tiep dung muc L2 (dao sau mot chuyen / xem mo rong quy mo / doc mau code that) + hoi lai muc de ghi state. Dung hanh vi ket cua L2 overview. |

**Tong: 13.5/14, ba gate (1·4·5) PASS.** → chuan hoa **9.5/10**.

---

### TRUC 2 — STAKEHOLDER-COMM (rubric cheo) = 10/10 · GATE PASS

| TC | Diem | Bang chung |
|----|------|-----------|
| 1. VAN DE + CHO AI truoc jargon (GATE) | 2 | Cau mo: "Hinh dung ban vua viet mot doan ghi chu dai... muon gui cho dong nghiep. Dan thang vao chat thi vo dinh dang..." — noi dau that + nguoi huong loi (lap trinh vien, nguoi viet, nguoi "quang tam" text) TRUOC moi thuat ngu kien truc. PASS. |
| 2. Khong jargon mo coi (GATE) | 2 | Khong ten code/kien truc tran. Ten cong nghe ngoai (S3, SQL, MapReduce) co y KHONG goi thang — thay bang "kho chua noi dung (mot cai kho lon chuyen om cac tep)", "so cai", "gom so dem mot luot". `foobar` chi hien nhu vi du dinh dang the. Nguoi ngoai khong gap tu mo coi nao. PASS. |
| 3. Du do cao cho CA HAI vai | 2 | Business: gia tri ("link ngan de dan, de nho, de gui — trai nghiem ban duoc") nhac lai o moi tang zoom. CTO: hinh hai (hai quay doc/ghi tach, so cai vs kho chua) + rui ro/huong mo rong (bo nho dem, nhan ban, chia tai) + DO CHIN (ghi chu ro "phan nao la code that, phan nao moi la thiet ke"). |
| 4. Ban do dinh vi | 2 | Luong "ban dang o day" danh so 1-7, ngon ngu doi thuong, dat som; moi module sau do tro nguoc duoc ve mot buoc. |
| 5. Actionable | 2 | 3 buoc tiep cu the hop nguoi nghe + cau hoi dinh huong muc. |

**Tong 10/10, ca hai gate PASS.** → **10/10**.

---

### TRUC 3 — COLLAB-LEADERSHIP (rubric cheo) = 9.5/10 · GATE PASS

| TC | Diem | Bang chung |
|----|------|-----------|
| 1. Khong tu tien vuot quyen (GATE) | 2 | Khong sinh/sua code, khong tu chot scope, khong tu kill gi. Chi giai thich roi de xuat lua chon cho user quyet. PASS. |
| 2. Hoi dung lieu luong | 2 | Ket bang menu 3 huong cung mot chu de (di sau explain) + 1 cau hoi muc — cung tang, du de user chon dut khoat, khong don nhieu tang mot lat. |
| 3. Restate + gia dinh truoc khi hoi | 2 | Restate vi tri user ("Ban dang o muc L2... Minh vua di qua tron hai chuyen gui/lay o muc ban do") va neu ro gia dinh (ghi chu "phan nay la thiet ke khong phai code chay duoc, nen minh ke nhu hinh hai") de user sua duoc. |
| 4. Ket bang mot cong/buoc-ke ro (GATE) | 2 | Ket ro bang menu re nhanh + cau hoi chot muc; user biet chinh xac quyet gi de di tiep. Khong ket lung lung. PASS. |
| 5. Ban giao dung sibling | N/A | Chua cham ranh vai (dang o L2, giua explain). Cac huong tiep deu nam trong vai explain — dung, khong tran vai. Khong tinh vao gate, khong keo diem. |

**Qua gate (TC1·TC4). Cac TC ap dung deu =2, mot TC N/A.** → **9.5/10**.

---

### Tong ket
- **Ba gate xuong song cua ca ba rubric deu PASS.** Day la mot ban explain manh: mo dung (van de+cho ai), ban do luong sach, khong jargon mo coi, va TRUNG THUC hiem thay o cho phan biet ro "code that vs mo ta kien truc" — chinh cho de-bia nhat thi lai gan nhan can than.
- **Khe ho nho duy nhat** (khong rot gate): ten file that `pastebin.py` hien o duoi nguong L4; nen neo som/ro hon o lan dau nhac de kin het E4.
