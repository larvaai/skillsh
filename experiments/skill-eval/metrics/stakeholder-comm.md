<!-- Do chat luong trao doi cua ban explain voi doi CTO + business cua doanh nghiep khach hang (nguoi ngoai, khong kien thuc noi bo): van de dat truoc thuat ngu, khong jargon mo coi, dung do cao cho ca hai vai, co ban do dinh vi, va nguoi nghe biet lam gi tiep. | gate: Tieu chi 1 — VAN DE + CHO AI dat truoc moi thuat ngu kien truc (mo bang van de thuc te + nguoi huong loi, khong mo bang ten kien truc/ten code), Tieu chi 2 — Khong jargon mo coi (moi thuat ngu code neo vi tri + loi ich truoc khi goi ten; ten cong nghe ngoai kem cum doi thuong) -->

# Rubric CHEO — STAKEHOLDER-COMM

**Do cai gi:** chat luong trao doi cua mot ban explain voi doi CTO + business team cua doanh nghiep KHACH HANG — nguoi ngoai, khong co kien thuc noi bo, khong truc tiep lam ra san pham. Thuoc do lay tu hop dong cua skill `explain`: "khong bo roi ai" (business thay gia tri, CTO thay hinh hai, dev thay duong vao), Luat neo (van de truoc / thuat ngu sau), va ba nhip LAM GI / CHO AI / VI SAO. KHONG them tieu chuan moi ngoai hop dong nay.

**Cham tren ban tra loi da co, khong doan y do.** Moi tieu chi 0/1/2 theo anchor. Tieu chi 1 va 2 la **Gate** (xuong song): mot trong hai = 0 thi ca ban khong dat, du cac tieu chi khac cao.

---

### Tieu chi 1 — VAN DE + CHO AI dat truoc moi thuat ngu kien truc  **[GATE]**
Do luat goc cua explain: mo bang van de thuc te + doi tuong huong loi, KHONG mo bang ten kien truc/ten code. La cai giu CTO va business khoi rot ngay cau dau.

- **0** — Cau/doan mo dau la thuat ngu kien truc hoac ten code (vd "day la he hexagonal / microkernel", "mot AgentKernel frozen…"). Nguoi ngoai khong biet project giai quyet van de gi cho ai. → **Gate fail.**
- **1** — Co neu van de va/hoac doi tuong, nhung mo ho, dat tre (sau khi da tha thuat ngu), hoac thieu mot trong hai (co van de nhung khong ro CHO AI, hoac nguoc lai).
- **2** — Mo dau ro rang bang van de thuc te + CHO AI (nguoi huong loi that), bang loi doi thuong, TRUOC khi bat ky thuat ngu kien truc/ten code nao xuat hien.

### Tieu chi 2 — Khong jargon mo coi  **[GATE]**
Do Luat neo #1 + #4: moi thuat ngu code noi bo phai duoc neo (o dau trong luong + ngan/loi gi) TRUOC khi goi ten; ten cong nghe ngoai (LangGraph, SQLite, Redis…) phai kem mot cum doi thuong noi no lam gi. Khong duoc de nguoi ngoai gap mot tu ho khong hieu.

- **0** — Co it nhat mot thuat ngu code/kien truc bi goi ten tran, chua neo vi tri + loi ich; HOAC ten cong nghe ngoai tha ra khong kem cum doi thuong. Nguoi ngoai gap tu la khong noi vao dau. → **Gate fail.**
- **1** — Da so thuat ngu duoc neo, nhung con 1–2 cho tha hoi som hoac cum doi thuong so sai, mo. Chua den muc lam nguoi ngoai lac han.
- **2** — Moc thuat ngu code deu neo truoc khi goi ten (vi tri trong luong + van de no ngan); moi ten cong nghe ngoai deu kem cum doi thuong dung nghia. Nguoi ngoai khong gap tu mo coi nao.

### Tieu chi 3 — Dung do cao cho CA HAI vai (CTO + business)
Do hop dong "khong bo roi ai". CTO can HINH HAI he thong + RUI RO + DO CHIN (phan nao xong, phan nao dang do). Business can GIA TRI + NO LAM GI. Mot ban chi noi ky thuat cho CTO ma quen gia tri, hoac chi ban gia tri ma khong cho CTO thay hinh hai/rui ro, la truot tieu chi nay.

- **0** — Chi phuc vu mot vai: hoac toan ky thuat (business khong thay gia tri / no lam gi), hoac toan gia tri (CTO khong thay hinh hai, rui ro, do chin).
- **1** — Cham ca hai vai nhung lech: mot ben duoc lo, ben kia chi thoang qua; hoac co gia tri nhung thieu do chin/rui ro cho CTO; hoac co hinh hai nhung gia tri chi nhac lay le mot lan.
- **2** — Ca hai vai duoc phuc vu du: CTO thay hinh hai + rui ro + do chin (phan dang do noi ro), business thay gia tri + no lam gi, va gia tri duoc nhac lai o moi tang zoom chu khong chi mot lan.

### Tieu chi 4 — Co ban do / khung dinh vi de moi chi tiet moc vao
Do Luat neo #2: overview phai co mot luong "ban o day" mot-cai-liec (5–8 buoc, ngon ngu doi thuong) dat SOM, va moi thuat ngu/module sau do tro nguoc ve duoc mot buoc trong luong. Khong co ban do thi nguoi ngoai khong biet minh dang o dau.

- **0** — Khong co luong/khung dinh vi nao. Chi tiet, module, thuat ngu tha ra roi rac, khong moc vao dau.
- **1** — Co mot dang khung (luong hoac danh sach phan) nhung so sai: khong danh so / khong ngon ngu doi thuong / dat qua tre / cac chi tiet sau khong tro nguoc ve duoc buoc nao.
- **2** — Co luong "ban o day" ro rang, dat som, 5–8 buoc doi thuong; moi module/thuat ngu ve sau deu moc duoc ve dung mot buoc trong luong.

### Tieu chi 5 — Actionable: nguoi nghe biet lam gi tiep
Do phan "goi y theo muc / hand off" cua explain. Sau khi giai thich, ban phai chi ra buoc tiep hop voi nguoi nghe — doc file nao truoc, hoi tiep gi, hay chuyen sang skill nao (L5+). Khong duoc ket lung lung de nguoi ngoai khong biet lam gi.

- **0** — Ket cut, khong mot goi y buoc tiep nao. Nguoi nghe doc xong khong biet di dau.
- **1** — Co huong tiep nhung chung chung ("neu can cu hoi"), khong bam vao vai CTO/business hoac khong cu the (khong ten file / khong cau hoi dinh huong / khong tro skill dung).
- **2** — Neu ro buoc tiep cu the, hop voi nguoi nghe: doc gi truoc / cau hoi dinh huong / tro dung skill neu qua tam explain — CTO va business deu biet lam gi tiep.

---

**Gate:** tieu chi 1 (van de truoc) VA tieu chi 2 (khong jargon mo coi). Bat ky tieu chi Gate nao = 0 thi ban KHONG DAT, du tong diem cac tieu chi con lai cao. Cham tieu chi con lai nhung ghi ro "gate fail" o dau ket qua.