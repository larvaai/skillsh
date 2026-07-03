# GRADE — review-pastebin · correctness-edgecase-lens

- contract_fidelity: 10/10
- stakeholder_comm: 2/10
- collaboration: 10/10
- gate: FAIL — Rot gate o truc stakeholder-comm (TC1 mo dau bang vai/che do thay vi van de+cho-ai; TC2 jargon tha tran: MapReduce/MD5/base62/PRIMARY KEY/Object Store...). NHUNG day la truc do mot ban explain cho CTO/business — output can cham la mot ban REVIEW ky thuat cho dev, nen rot gate o day la do ap sai thuoc, khong phai loi noi tai. Truc contract_fidelity (skill-rubric review) qua sach ca 3 xuong song t1/t2/t3. Truc collaboration (collab-leadership) qua ca 2 gate TC1/TC4.
- fix_first: Chinh vai dong neo bi lech 1 don vi cho khop tuyet doi (than rong pastebin.py o dong 8-14 chu khong 8-13; base_encode README o dong 134-141 chu khong 133-141) — la don bay duy nhat con lai vi noi dung gap, bang chung, phan muc va ket deu da o chuan cao nhat cua hop dong review.

---

## CHAM MU OUTPUT `review` — Fixture Pastebin (System Design Primer)

Fixture da kiem chung:
- `/Users/uspro/Desktop/skillsh/experiments/skill-eval/fixtures/system-design-primer/solutions/system_design/pastebin/pastebin.py` (47 dong; 4 ham loi than rong `pass`)
- `/Users/uspro/Desktop/skillsh/experiments/skill-eval/fixtures/system-design-primer/solutions/system_design/pastebin/README.md` (333 dong)

Da doc TOAN BO ca hai file de kiem tung finding. Ket luan: **khong co gap bia** — moi gap khop code/thiet ke that.

---

### TRUC 1 — contract_fidelity (SKILL-RUBRIC review, 6 TC × 0/1/2)  →  **10/10 — QUA GATE**

| TC | Diem | Cham |
|----|------|------|
| **1. Dung loai gap (xuong song)** | **2** | Moi muc la gap that thuoc edge/error/race. Khong lan sang explain/fix/triage/plan. Con tu tuyen bo "chi bao cao, khong de xuat fix". |
| **2. Bang chung (xuong song)** | **2** | Moi finding du `file · dong/symbol · dieu thieu · hau qua`. Vd race: "README 99-105 + PRIMARY KEY 116 → loi tho / rac mo coi Object Store". Vai dong neo lech NHE (than rong that 8-14 ghi 8-13; base_encode that 134-141 ghi 133-141) — khong doi ban chat. |
| **3. Khong bia (xuong song)** | **2** | Kiem tung gap deu khop: extract_url/extract_year_month `pass` → key (None,None); MD5(ip+timestamp) deterministic → retry vo han; schema thieu cot expiration tuyet doi vs dong 232 scan theo "expiration timestamp"; base_encode thieu `:` dong 136 + num=0 → rong. Cho chua chac tach xuong "CO THE LA GAP" kem cau hoi — chuan cao nhat. |
| **4. Xep uu tien** | **2** | Critical/Medium/Low khop ban chat hau qua, sap nang truoc nhe sau. |
| **5. Ket dung vai** | **2** | Hand off `plan` cho Critical, dao sau muc chua chac, doi lang kinh. Khong tu fix. |

**Tong 12/12. Khong rot gate.** Ban review bam hop dong gan nhu tuyet doi.

---

### TRUC 2 — stakeholder_comm (thuoc do EXPLAIN cho CTO+business)  →  **2/10 — ROT GATE (TC1+TC2)**

> Ban chat: thuoc nay do explain cho stakeholder ngoai. Output la mot ban REVIEW ky thuat cho dev. Diem thap phan anh MUC LIEN QUAN, khong phai khuyet diem cua output khi dung vai review.

| TC | Diem | Cham |
|----|------|------|
| **1. Van de+cho-ai truoc thuat ngu (GATE)** | **0** | Mo bang "Toi vao vai skill review... che do ro" — vai/quy trinh, khong van de-cho-ai doi thuong. → Gate fail. |
| **2. Khong jargon mo coi (GATE)** | **0** | MapReduce, MD5, base62, PRIMARY KEY, Object Store, TTL, race, reducer/mapper tha tran khong cum doi thuong. → Gate fail. |
| **3. Do cao 2 vai** | **1** | Co doi thuong cho nguoi build, khong cham vai business (gia tri) va khong cho CTO thay hinh hai/rui ro muc quan ly. |
| **4. Ban do dinh vi** | **0** | Khong co luong "ban o day" doi thuong cho nguoi ngoai. |
| **5. Actionable** | **2** | Ket co buoc tiep ro (plan / dao sau / doi lang kinh). |

**Rot ca 2 gate** — do ap thuoc explain vao review, lech vai.

---

### TRUC 3 — collaboration (collab-leadership)  →  **10/10 — QUA GATE**

| TC | Diem | Cham |
|----|------|------|
| **1. Khong vuot quyen (GATE)** | **2** | Khong sua code, khong tu fix; tuyen bo "chi bao cao, fix la buoc sau". |
| **2. Lieu luong hoi** | **2** | Cum 3 goi y cung tang, khong don qua. |
| **3. Restate+gia dinh** | **2** | Restate pham vi+che do; neu gia dinh (tach code that vs thiet ke, gan nhan "trong thiet ke"). |
| **4. Ket bang cong (GATE)** | **2** | 3 lua chon minh bach cho user quyet. |
| **5. Ban giao sibling** | **2** | Tro `plan` cho fix, giu ranh vai review. |

**Qua ca 2 gate.**

---

### TONG HOP
- contract_fidelity **10/10** (qua gate, 12/12)
- stakeholder_comm **2/10** (ROT GATE TC1+TC2 — ap sai thuoc explain vao review)
- collaboration **10/10** (qua gate)
- **gate_pass=false**: rot gate duy nhat o stakeholder-comm; hai truc con lai qua sach.

**Doc theo dung vai review:** output chat luong rat cao — bam hop dong, khong bia, bang chung neo chinh xac, ket dung vai. Diem thap stakeholder-comm phan anh su khong tuong thich thuoc↔vai, khong phai chat luong. Don bay con lai: sua vai dong neo lech 1 don vi.
