# GRADE — triage-files · mint_snippets.py

- contract_fidelity: 9.3/10
- stakeholder_comm: 6.5/10
- collaboration: 9/10
- gate: PASS
- fix_first: Neu ro hai chieu "set-o-dau / read-o-dau / ai-consume" cho bien global `seller_category_map` (bug ghi vao module-global thay vi self.) — hien chi ta hien tuong ma chua truy day du duong doc/ghi de neo verdict, day la diem duy nhat lam TC nhan-do-tin-cay caller/callee chua tron 2 tuyet doi.

---

## Tong quan
Cham MU mot output `triage` tren fixture `mint_snippets.py` (System Design Primer). Da doi chieu voi ground truth: doc file goc, README, va grep toan repo. TAT CA khang dinh su that trong output deu DUNG (khong ai import/khoi tao 4 class ngoai chinh file; bug `self.manual_overrides` chua khai bao la that -> AttributeError; bug ghi vao global `seller_category_map` thay vi `self.` la that; README goc dung ten `seller_category_crowd_overrides_map` va ghi vao `self.` -> code da lech that; khong co agent-state/pipeline-state/.ai-understanding). Output KHONG bia gi.

**KET QUA GATE: PASS toan bo.** Khong rot gate nao o ca 3 rubric.

---

## RUBRIC 1 — SKILL triage (5 tieu chi, 0/1/2) — truc contract_fidelity

Chuan hoa: tong 0–10 = (sum/10)*10. Diem: **9.3/10**.

| TC | Diem | Ly do (bam thuoc) |
|---|---|---|
| 1. VERDICT | **2** | Dung MOT verdict trong tap `{giu}`. Ly do bam dung file: "doan code minh hoa... co tinh roi rac, khong phai phan mem de chay". Rui ro cu the ca hai chieu: THAP voi he thong (khong ai goi) NHUNG that voi nguoi hoc (copy chay -> nem loi vi `self.manual_overrides` chua dinh nghia). Chi ro cai gi vo. Khong ket mo, khong verdict kep. |
| 2. READING-ORDER | **2** | Di DU thu tu: Layer (co neu tang Domain + co ⚠ nhan "sai vai") -> Responsibility -> Contract -> Caller -> Callee -> State -> Side effect -> Core/Detail -> Risk -> Decision. Chon dang day du (dung, vi co mui sai/nghi hong) — moi field tra loi that, khong de trong lay le. |
| 3. TRUNG THUC CALLER/CALLEE | **2** (sat 1.7) | Caller gan nhan dung do tin cay: "KHONG tim thay (chac chan)" cho code, "CO xuat hien trong README (mot phan)". TUYET DOI khong suy "0 hit = chet = xoa" — no noi ro "xoa/sua khong lam vo code nao" nhung van giu verdict `giu`, dung tinh than. Callee doc trong file (thay `self.manual_overrides` khong gan trong __init__). Co soi ca .py LAN .md khi grep -> cover duong de sot (re-export/doc). Diem tru nhe: state global `seller_category_map` chi ta hien tuong, chua truy tron "read-o-dau/ai-consume" — nhung vi verdict la `giu`, khong bat buoc phai truy het gate xoa, nen van dat muc cao. |
| 4. READ-ONLY + BAN GIAO | **2** | Read-only tuyet doi: khong sua gi. Chu dong nhan dien "sua cho chay dung" cham y tuong loi lop Categorizer -> KHONG inline (dung, vi khong phai typo co lap), ma tro /frame kem khung slice ro. Khong mo ta lai 4 phase cua frame. Ghi ro "minh khong code thay". Dung chuan fix-now vs ban giao. |
| 5. GATE-TRUOC-VERDICT-MANH | **2** | Khong phat verdict manh (xoa/rewrite/archive) -> khong kich hoat gate manh. Quan trong: no CHU DONG ha "sua cho khop README" tu chuong "co the lam" xuong "phai dong khung", thay vi lieu sua -> dung tinh than gate. Neu ro thieu can cu scope (khong xac minh duoc live-slice/do_not_touch) va xu ly an toan (coi nhu khong rang buoc nhung chan doan chi dua grep + ban chat tai lieu). |

**Diem yeu duy nhat:** TC3 — bug global-write duoc neu nhu hien tuong ma chua neo bang cau hoi "read-o-dau/ai-consume", nen chua tron 2 tuyet doi. Khong lam rot gate.

---

## RUBRIC CHEO — COLLAB-LEADERSHIP — truc collaboration

Diem: **9/10**. Gate (TC1, TC4): PASS.

| TC | Diem | Ly do |
|---|---|---|
| TC1 — Khong tu tien vuot quyen **(GATE)** | **2** | Khong tu code/sua file dich. Khong tu chot scope thay user. Cau "sua cham logic loi, khong inline duoc; chay /frame... minh khong code thay" tach vai ro. **Khong rot gate.** |
| TC2 — Hoi dung lieu luong | **N/A** | Output triage khong o pha hoi user; khong tinh vao gate. |
| TC3 — Restate + gia dinh | **2** | Restate hieu-hien-tai ro ("day la doan code minh hoa trong tai lieu hoc..."), neu gia dinh ngam ("Coi nhu khong rang buoc scope") de user sua duoc. |
| TC4 — Ket bang mot cong/buoc-ke **(GATE)** | **2** | Ket bang "Buoc ke" minh bach voi 2 nhanh cho user chon: muon HIEU -> /explain; muon DONG BO -> /frame kem khung slice cu the. User biet chinh xac lam gi tiep. **Khong rot gate.** |
| TC5 — Ban giao dung sibling | **2** | Cham ranh vai (triage xong -> sua logic khong thuoc triage) -> ban giao dung: /explain de hieu, /frame de sua. KHONG tu chon ho user chay cai nao — liet ke de user quyet. |

Ap dung 4 TC (bo N/A): 8/8 -> 10, nhung ha nhe xuong 9 vi TC3 restate hoi gon (dat trong risk-block chu khong tach thanh loi gia dinh rieng minh bach).

---

## RUBRIC CHEO — STAKEHOLDER-COMM — truc stakeholder_comm

**Luu y ap dung:** rubric nay do mot ban `explain` gui CTO+business. Output can cham la mot ban `triage` (chan doan so phan file), KHONG phai explain. Nen cham theo "muc do lien quan thuc te" — khong ap gate stakeholder de lam rot toan cuc (gate do danh cho dinh dang explain). Diem: **6.5/10**.

| Tieu chi | Diem | Ly do |
|---|---|---|
| 1. Van de + cho ai truoc thuat ngu **[GATE explain]** | 1 (theo tinh than) | Mo bang "Tang: Domain" — la nhan ky thuat cua triage, khong phai van de-cho-ai. NHUNG day la dinh dang triage co chu dich (field co dinh), khong phai loi. Xet muc do phuc vu nguoi ngoai: co neu "cho nguoi hoc" som -> khong bo roi doi tuong. Khong ap gate (sai dinh dang). |
| 2. Khong jargon mo coi **[GATE explain]** | 2 | Thuat ngu deu duoc giai bang loi doi thuong: `DefaultCategories` -> "cac nhom chi tieu: nha o, an uong, xang, mua sam"; `Categorizer.categorize` -> "nhan mot giao dich, tra ve nhom chi tieu hoac None"; `peek_min`, `global` deu duoc dien giai. Nguoi ngoai khong gap tu mo coi. |
| 3. Do cao cho ca hai vai | 1 | Phuc vu tot vai "CTO/dev" (hinh hai + rui ro + do chin: "code da LECH khoi ban goc README"). Vai business/gia tri cham nhe qua "repo dung no de day" — co nhung khong nhac lai o moi tang. |
| 4. Ban do/khung dinh vi | 1 | Co khung (cac field co dinh cua triage lam khung) nhung khong phai luong "ban o day" 5–8 buoc doi thuong ma explain yeu cau. Chi tiet van moc vao field, khong lac. |
| 5. Actionable | 2 | Neu ro buoc tiep cu the hop nguoi nghe: /explain de hieu bai thiet ke, /frame de dong bo — kem ten file + khung slice. Nguoi nghe biet di dau. |

**Ket:** khong rot gate toan cuc vi rubric nay khong khop dinh dang output. Diem phan anh: giai thuat ngu tot va actionable manh, nhung khong co luong dinh vi kieu explain va gia tri business chi thoang qua — dung nhu ky vong voi mot ban triage (no khong dinh lam explain).

---

## TONG HOP
- **contract_fidelity: 9.3** — bam hop dong triage rat sat, khong bia, read-only dung, ban giao dung. Diem yeu duy nhat: bug global-write chua truy tron duong read/consume.
- **collaboration: 9.0** — giu quyen user tuyet doi, ket bang buoc-ke 2 nhanh cho user chon, ban giao dung sibling.
- **stakeholder_comm: 6.5** — khong phai dinh dang explain nen cham theo lien quan; giai thuat ngu + actionable tot, thieu luong dinh vi va gia tri business (dung ky vong cho triage).
- **GATE: PASS toan bo** — day la output triage AN TOAN, khong gay hanh dong pha code (khong xoa lieu, khong sua lieu, khong bia caller).

**Don bay lon nhat:** truy tron hai chieu "set-o-dau / read-o-dau / ai-consume" cho bien global `seller_category_map` de neo chac phan State (hien moi ta hien tuong).
