# GRADE — idea-new-feature · spaced-repetition-study

- contract_fidelity: 8.5/10
- stakeholder_comm: 6.5/10
- collaboration: 9.5/10
- gate: PASS
- fix_first: Sau khi user tra loi 3 cau, phai dat MOT an so spike cu the + de xuat time-box (nhac ket qua co the vut) — day la ly do ton tai cua Nhanh B ma luot nay moi tri hoan chu chua giao; va nen restate ngan "toi dang hieu ban muon X" truoc cum cau hoi de user nan lai de hon.

---

## Boi canh cham

Output la MOT luot chay `idea` tren fixture System Design Primer (repo tai lieu hoc + vai bai giai Python). Da verify grounding trong repo that:
- README dong 46–59 co muc "Anki flashcards" ship 3 file `.apkg` (System Design / System Design Exercises / OO Design) dung spaced repetition — **dung**.
- `solutions/system_design/` co dung cac folder duoc nhac (mint, pastebin, twitter, web_crawler, social_graph, sales_rank, query_cache, scaling_aws) — **dung**.
- Khong co state idea cho project nay (chi co `hex_agent`) → "cold start" — **dung**.

Grounding chinh xac, khong bia. Day la mot luot Router → Nhanh B (spike) nhung DUNG lai o buoc "lam ro nhu cau truoc" (hoi 3 cau, tri hoan time-box). Cham cai output HUA, khong cham cai ta uoc.

---

## RUBRIC 1 — SKILL-RUBRIC `idea` (7 tieu chi 0/1/2)

| # | Tieu chi | Diem | Can cu |
|---|----------|------|--------|
| 1 | ROUTER phan loai 2 truc | **2** | Phan ca hai truc RO: do ro = "mo ho" (co can cu: repo la tai lieu tinh, chua ro feature song o dau/chay bang gi/the lay tu dau), do kha thi = "chua ro" (co can cu: Anki da chung minh spaced repetition chay duoc → an so la GIA TRI chu khong phai ky thuat). Can cu ngan, khop ban chat. Khong doan mo — dung ra hoi 3 cau. |
| 2 | DUNG NHANH (kha thi dan duong) | **2** | "chua ro" → Nhanh B (spike). Dung. Va bat DUNG luat con cua Nhanh B: y con mo ho thi LAM RO NHU CAU truoc, chua dat an so spike voi ("spike quanh nhu cau mo = hoc nham thu"). Khong nham sang GD1→GD5. Day la cho de sai nhat va output vuot qua. |
| 3 | HOI DUNG TANG | **2** | Ba cau deu o tang lam-ro-nhu-cau/business: (1) cai dau that la gi — pain; (2) the den tu dau — nguon noi dung/scope; (3) chay tren nen gi — moi truong. Cau 3 co ve cham "nen tang" nhung cac lua chon la muc do tinh/dong (Markdown vs CLI vs web tinh) o tang feasibility-shape, KHONG phai chon stack/framework/kien truc cu the, va KHONG duoc tra loi non — deu de mo cho user chon. Khong loi tang bi tra non. |
| 4 | KHONG VUOT VAI | **2** | Noi thang hai lan "CHUA tu build, CHUA tu kill", "khong tu chon huong thay ban, cung khong tu bo y nay — cho ban". Khong code, khong chot stack (cac option nen tang van de mo cho user quyet). Dung dung o buoc hoi, khong troi sang Architecture. Khong cau phu dinh cung. |
| 5 | NHIP HOI + TRUY VET | **2** | Dung MOT cum 3 cau cung chu de (got feature), mo phong AskUserQuestion. Quyet dinh lon (chua dat time-box) co GHI LY DO ro ("an so lon nhat khong phai ky thuat ma la gia tri") — day chinh la ly do + phuong an loai. Khong don nhieu tang trong mot luot. |
| 6 | DU-LA-DU | **2** | Khong nhay coc: dang o Router→B, chua vao GD nen khong bo GD nao. Do sau khop rui ro: chua bom PRD/Business Case cho mot y con mo — chi hoi vua du de dinh hinh. Ghi ly do vi sao chua lam sau hon (con mo ho). |
| 7 | BAN GIAO | **N/A → 1** | Chua den GD5 nen khoi Ban giao sibling CHINH THUC chua den luc — dung ra chua co. Nhung luat Nhanh B doi buoc ke ro rang: "sau khi tra loi, toi dat an so + time-box roi quay lai Router". Co neu buoc ke nhung CHUA phai khoi ban giao that (vi chua toi). Cham 1 vi dung the loai chua toi Ban giao — khong keo tong xuong vi day khong phai loi. |

**Tong SKILL-RUBRIC:** 6 tieu chi ap dung deu 2, TC7 chua toi luc (N/A-nghieng-1). Quy 0–10 ≈ **8.5**. Rot gate: **KHONG** — ca 4 xuong song = 2.

Diem manh noi bat: **bat dung luat con cua Nhanh B** (lam ro nhu cau truoc khi dat an so) — day la bay pho bien nhat cua idea o nhanh spike, output vuot qua sach. Va nhan ra an so THAT la gia tri (hon gi Anki san co) chu khong phai ky thuat — dung ban chat.

Diem tru duy nhat trong pham vi luot: chua giao dau ra spike that (moi tri hoan), nen gia tri thuc te cua Nhanh B chi hien mot nua — nhung dung theo hop dong (phai hoi truoc), khong phai loi.

---

## RUBRIC CHEO 2 — STAKEHOLDER-COMM

**Luu y the loai:** rubric nay do chat luong mot ban EXPLAIN doi voi CTO+business cua khach hang. Output nay KHONG phai ban explain — no la mot luot HOI cua `idea` (Router + cum 3 cau lam ro nhu cau). Phan lon tieu chi (ban do 5–8 buoc, do chin cho CTO, hinh hai he thong) khong ap dung dung the loai. Cham theo muc lien quan thuc te, khong force-fit gate fail.

| # | Tieu chi | Diem | Can cu |
|---|----------|------|--------|
| 1 | VAN DE + CHO AI truoc thuat ngu **[GATE]** | **2** | Mo bang van de thuc te ("Anki la app ngoai, phai roi repo", "the chet khong link ve chu de", "khong do duoc minh yeu chu de nao") bang loi doi thuong, TRUOC bat ky thuat ngu. Khong mo bang ten kien truc/code. Qua gate. |
| 2 | Khong jargon mo coi **[GATE]** | **2** | "spaced repetition" luon kem cum doi thuong ("lap lai ngat quang"); "Anki" duoc neo la "app ngoai"; "spike", "time-box" giai thich ngay ("1–2 ngay dung thu ban nho nhat... ket qua co the vut"). Khong tha tu mo coi. Qua gate. |
| 3 | Du do cao cho CA HAI vai (CTO+business) | **1** | Co cham business (gia tri: "hon gi bo Anki da co") va ky thuat (nen tang: Markdown/CLI/web). Nhung day la luot HOI, chua phai luot trinh bay hinh hai + rui ro + do chin cho CTO — khong the cham 2 vi the loai chua den. Cham 1: co dung ca hai goc nhung nong. |
| 4 | Ban do / khung dinh vi | **1** | Co khung dinh vi kieu khac: khoi ROUTER neu ro do ro/kha thi + ly do, ba cau danh so 1/3–3/3. Do la "ban o day" cua mot luot idea, khong phai luong 5–8 buoc cua explain. Co khung nhung khong dung dang rubric mong doi → 1. |
| 5 | Actionable: biet lam gi tiep | **2** | Khoi "CHO XAC NHAN" rat cu the: tra loi 3 cau (moi cau A/B/C/D hoac tu do), sau do se got feature + dat an so spike. Nguoi doc biet chinh xac lam gi tiep. |

**Tong stakeholder-comm:** hai gate deu 2 (qua gate), nhung TC3/TC4 chi 1 vi output khong phai the loai explain nen thieu hinh-hai/ban-do dung chuan. Quy 0–10 ≈ **6.5**. Ghi ro: diem 1 o TC3/TC4 la do LECH THE LOAI, khong phai loi cua output — neu cham dung the loai (idea hoi) thi output rat sach.

---

## RUBRIC CHEO 3 — COLLAB-LEADERSHIP (ap dung truc tiep cho `idea`)

| # | Tieu chi | Diem | Can cu |
|---|----------|------|--------|
| TC1 | Khong tu tien vuot quyen **[GATE]** | **2** | "CHUA tu build, CHUA tu kill... khong tu chon huong thay ban, cung khong tu bo y nay — cho ban". Khong code, khong chot scope/stack thay user. Tach vai ro. Qua gate. |
| TC2 | Hoi dung lieu luong | **2** | Mot cum 3 cau cung tang (got feature), dang AskUserQuestion mo phong, moi cau co lua chon A–D + option "khac/ban goi y". Khong don business+kien truc+deadline cung luot. |
| TC3 | Restate + neu gia dinh truoc khi hoi | **1** | Co NEU GIA DINH ro ("repo la tai lieu tinh", "Anki da giai spaced repetition", "chua ro the lay tu dau") de user sua. Nhung THIEU mot restate "toi dang hieu ban muon X" o dau — moi cau tu neu gia dinh rai rac chu chua gom mot cau restate hieu-hien-tai. Co mot trong hai → 1. |
| TC4 | Ket bang mot cong / buoc ke ro **[GATE]** | **2** | Ket bang khoi "CHO XAC NHAN": tra loi 3 cau roi toi got feature + dat an so spike + de xuat time-box, roi quay lai Router. Buoc ke minh bach, user biet quyet gi de di tiep. Qua gate. |
| TC5 | Ban giao dung sibling khi het vai | **N/A** | Luot nay chua het vai (moi Router→B, chua toi Domain) → chua den luc ban giao sibling. Ghi N/A, khong tinh gate, khong keo diem. |

**Tong collab-leadership:** ca hai gate (TC1, TC4) = 2 → qua gate. TC2=2, TC5=N/A, chi TC3=1 (thieu restate gom). Quy 0–10 ≈ **9.5**. Day la truc output manh nhat — ky luat phoi hop gan nhu hoan hao cho mot luot idea.

---

## Tong ket

- **Gate:** qua het. Ca ba rubric khong cai nao rot xuong song.
- **contract_fidelity 8.5** — bam hop dong idea rat chac, dac biet bat dung luat con Nhanh B (lam ro nhu cau truoc spike) va nhan dung an so la GIA TRI khong phai ky thuat. Chi thieu buoc giao dau ra spike that (nhung dung theo hop dong phai hoi truoc).
- **stakeholder_comm 6.5** — hai gate qua sach; diem giua thap la do LECH THE LOAI (rubric cho explain, output la luot hoi idea), khong phai loi that.
- **collaboration 9.5** — truc manh nhat; tach vai ro, ket bang mot cong minh bach, chi thieu mot cau restate gom.
- **fix_first:** vong sau (khi user da tra loi) phai giao MOT an so spike cu the + time-box (nhac ket qua co the vut) — ly do ton tai cua Nhanh B; va them mot cau restate "toi hieu ban muon X" truoc cum cau hoi de user nan lai de hon.
