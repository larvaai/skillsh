# Bao cao tong hop — Eval Skills tren System Design Primer

## Tra loi thang 2 cau hoi

### CAU 1 — Agent (khi goi skills) TRAO DOI voi CTO/business co dat chuan khong?

**Co, va rat manh — NHUNG chi khi dung skill `explain` va khi output CO MUC DICH gui nguoi ngoai.**

- Truc `stakeholder_comm` chi la thuoc do THAT SU cho `explain`. Tren scenario explain-pastebin, ban tot (analogy-business-heavy) dat **10/10**, ban khac (problem-first-zoom) dat **9.4** — deu mo bang VAN DE + CHO AI truoc moi thuat ngu, moi ten ky thuat deu duoc neo boi 1 cum doi thuong. Day la chuan "explain tot" (tong quan truoc, cho nguoi doc tron CTO/business/dev) da ghi trong memory.
- Diem then chot: **thu tu quyet dinh dat/rot gate.** Ban architecture-first mo bang "web-tier/reverse proxy/MD5/MapReduce" tha tran → rot gate ca MUC lan stakeholder (3.0). Cung mot noi dung ky thuat, chi lat khoi "cong dung + luong ban-o-day" len TRUOC la go duoc 2 gate. Skill co day du co che de dat chuan; sai la sai o thu tu, khong phai thieu nang luc.
- **Canh bao ve rubric:** voi output KHONG phai explain (idea/frame/triage/review), stakeholder-comm chi cham THAM CHIEU va KHONG keo gate tong. review/correctness-edgecase-lens dat contract 10 + collab 10 nhung "rot gate" stakeholder-comm 2.0 — day la ap SAI thuoc (rubric explain len bao cao ky thuat cho dev), khong phai loi noi tai. Neu doc nham diem nay se ket luan sai rang review "khong trao doi duoc voi business".

**Ket luan cau 1:** Khi CAN trao doi voi CTO/business (explain), agent dat chuan cao. Cac skill ky thuat (review/triage) HIEN mac dinh viet cho dev — muon chung phuc vu ca doi CTO/business can them 2-3 cau mo dau doi thuong TRUOC khi tha thuat ngu (don bay da chi ro trong tung fix_first).

### CAU 2 — Agent DAN DAT khi goi skills co DE PHOI HOP voi user khong?

**Co — day la mat manh dong deu nhat toan suite.** Truc `collaboration` (do collab-leadership: TC1 khong vuot quyen + TC4 ket bang mot cong ro) dat cao o gan nhu moi ban:

- **frame/strict-slice-discipline = 10, correctness-review = 10, spaced-repetition = 9.5.** Cong "─CHO XAC NHAN─" cua frame + cau "minh se KHONG code toi khi ban duyet" la khuon mau phoi hop tot nhat: user giu quyen scope, agent chi de xuat.
- Moi skill deu ket bang MOT cong go/no-go ro (menu huong, cau hoi hand-off, buoc-ke), khong tu quyet, khong code chui.
- **Ngoai le duy nhat:** frame/eager-drift (baseline yeu co chu dich) tuyen bo "code ngay o luot nay" + om 3 slice → rot gate collab (1.0). Day la bang chung NGUOC chung minh rubric bat dung hanh vi vuot quyen.

**Cho de phoi hop CON YEU (lieu luong hoi + phan tang):**
- idea/per-exercise-self-review: tron cau WHAT (rubric cham cai gi) vao luot dan nhan GD0→GD1 → idea-TC3=1. Nen tach 1-luot-1-tang.
- frame/over-questioning: dat 8 cau free-form mot lat thay vi AskUserQuestion cho cau uu tien → user kho nan lai.
- idea/spaced-repetition: nen restate "toi dang hieu ban muon X" TRUOC cum cau hoi de user de sua.

**Ket luan cau 2:** Ky luat "user-quyet-scope, agent-chi-de-xuat" dat chuan vung (collab la truc cao nhat, deu nhat). Diem mai tiep theo KHONG phai "co phoi hop khong" (da co) ma la "lieu luong hoi" — tach tang, dung AskUserQuestion, restate hieu-biet truoc khi hoi.

## Skill nao manh/yeu o truc nao

- **explain** — VO DICH truc stakeholder_comm (9.4-10). Nhiem vu cot loi "trao doi voi nguoi ngoai" da dat tran. Yeu duy nhat: rung ten code that duoi nguong L4 (keo MUC/contract). Do la mot cho chinh trong SKILL, khong phai lo hong nang luc.
- **frame** — VO DICH truc collaboration (10). Ky luat cong phoi hop la manh nhat. Yeu o lieu luong hoi (free-form).
- **triage / review** — VO DICH truc contract_fidelity (nhieu ban 9.2-10). Chinh xac chan doan, khong bia, neo dung dong. Yeu chung: viet cho dev nen truc stakeholder_comm thap — nhung do la lech-vai-rubric, khong phai loi.
- **idea** — Can bang, khong dinh tran truc nao. Manh o collab (khong vuot quyen, ket 1 cong). Yeu ro nhat o phan-tang-hoi va o cho "chot kha thi khi con an so".

## Moi scenario: huong nao THANG va vi sao

1. **explain-pastebin → analogy-business-heavy** (9.5/10/9.5). Neo tung thuat ngu sau khi da co khung doi thuong, cau phang, ket bang menu 3 huong. Vuot problem-first-zoom vi khong rung ten code that.
2. **idea-new-feature → spaced-repetition-study** (8.5/6.5/9.5) ve tong the manh nhat (collab 9.5). Nhung cost-capacity-calculator (8.3/8.0/8.8) can bang hon ca 3 truc va stakeholder cao hon. Chon spaced-repetition vi contract+collab cao hon va la cho idea the hien dung Nhanh B; cost-capacity la a-quan sit sao.
3. **frame-add-feature → strict-slice-discipline** (9.3/7.5/10). Duy nhat dat khoi CHO XAC NHAN du 4 truong + dung 1 slice + Parking Lot. Chuan vang cua frame.
4. **triage-files → pastebin.py** (10/7.5/8.5). contract tuyet doi 10: verdict an toan + TU CHOI suy "0 hit=chet" + da xac minh fixture that. Cao hon 2 file kia o ca contract lan stakeholder.
5. **review-pastebin → correctness-edgecase-lens** (10/2/10) xet theo LOI NOI TAI cua review (contract+collab deu 10, gate review sach). Diem stakeholder 2.0 la ap sai thuoc, bo qua. security-permission-lens la lua chon "an toan" neu tinh ca stakeholder, nhung xet dung hop dong review thi correctness thang.

## Gap tong the cua bo eval (meta)

1. **stakeholder-comm dung sai truc.** No la rubric CUA explain, bi ap len idea/frame/triage/review → tao gate-fail gia (review/correctness "FAIL" du sach). Can tach: hoac lam rubric-stakeholder rieng cho tung ho skill, hoac danh dau ro "N/A, khong keo gate" trong scorecard (hien da lam bang tay trong gate_notes, nhung de bi doc nham).
2. **Tran diem che khac biet** (giong het phat hien vong tune explain: baseline/B/D/E cung 14/14). Nhieu ban cham sat tran (contract 9.2-10) → 3 muc 0/1/2 khong con phan giai duoc nhom dan dau. Can thang min hon.
3. **stakeholder-comm chua co gate ro cho ranh gioi "review cho dev vs explain cho business"** — nen output ky thuat bi phat oan.

---

## Per-scenario winners

- **explain-pastebin** → `analogy-business-heavy` — 9.5/10/9.5 — neo tung thuat ngu sau khung doi thuong, cau phang, ket bang menu 3 huong + hoi lai muc; khong rung ten code that (chi 1 file that duoi L4). Vuot problem-first-zoom o ca 3 truc; architecture-first rot gate.
- **idea-new-feature** → `spaced-repetition-study` — 8.5/6.5/9.5 — collab cao nhat (TC1/TC4=2, khong vuot quyen), the hien dung Nhanh B cua idea. cost-capacity-calculator (8.3/8.0/8.8) can bang stakeholder tot hon, la a-quan sit sao; per-exercise-self-review yeu nhat vi tron WHAT vao luot GD0->GD1.
- **frame-add-feature** → `strict-slice-discipline` — 9.3/7.5/10 — duy nhat dat khoi CHO XAC NHAN du 4 truong + dung 1 slice + Parking Lot + cau 'KHONG code toi khi ban duyet'. Chuan vang cua frame. eager-drift rot gate (code chui, om 3 slice); over-questioning PASS nhung yeu lieu luong hoi.
- **triage-files** → `pastebin.py` — 10/7.5/8.5 — contract tuyet doi: verdict `giu`+ly do+rui ro, grep 'KHONG tim thay' va TU CHOI suy '0 hit=chet', da xac minh fixture that. Cao hon web_crawler va mint o ca contract lan stakeholder.
- **review-pastebin** → `correctness-edgecase-lens` — 10/2/10 xet theo hop dong NOI TAI cua review: contract+collab deu 10, 3 xuong song review sach, chi 1-2 dong neo lech 1 don vi. Diem stakeholder 2.0 la ap SAI thuoc (rubric explain len bao cao ky thuat cho dev), bo qua. security-permission-lens la lua chon an toan neu tinh ca stakeholder.

## Top findings

- explain la skill trao doi CTO/business tot nhat suite (stakeholder_comm 9.4-10, dat tran); nhiem vu cot loi da xong, yeu duy nhat la rung ten code that duoi nguong L4.
- collaboration la mat manh dong deu nhat: moi ban PASS deu khong vuot quyen scope va ket bang mot cong go/no-go ro; frame/strict-slice + review/correctness dat 10/10. Ky luat user-quyet-scope vung.
- review/triage vo dich truc contract_fidelity (nhieu ban 9.2-10, khong bia, neo dung dong) nhung viet cho DEV nen stakeholder_comm thap — do la lech-vai-rubric, khong phai loi nang luc.
- LOI DO LUONG: stakeholder-comm la rubric cua explain bi ap len idea/frame/triage/review, tao gate-fail GIA (review/correctness 'FAIL' du contract+collab=10). Phai danh dau N/A, khong keo gate tong.
- Thu tu quyet dinh dat/rot gate: architecture-first va eager-drift (2 baseline yeu) rot gate KHONG vi thieu noi dung ma vi sai thu tu (tha thuat ngu truoc / code truoc xac nhan). Lat khoi la go duoc gate.
- Diem yeu phoi hop con lai KHONG phai 'co hoi khong' (da co) ma la 'lieu luong hoi': tron nhieu tang trong 1 luot (idea per-exercise), 8 cau free-form mot lat (frame over-questioning), thieu restate hieu-biet truoc khi hoi.
- Tran diem 0/1/2 che khac biet giua nhom dan dau (contract 9.2-10 sat nhau), lap lai dung phat hien cua vong tune explain (baseline/B/D/E cung 14/14). Can thang min hon.

## Recommendations

- explain: tach ro trong SKILL/rubric TC1 (MUC) giua 'trich dan code' (so dong/chu ky ham/ten bien — cam < L4) va 'nhac ten module/entrypoint da neo' (cho phep tu L2). Day la cho duy nhat keo contract cua ca 2 ban explain manh xuong; thuong-hoa `pastes`/`pastebin.py`/`HitCounts` khi < L4.
- idea: tach '1 luot 1 tang' — day cau WHAT (rubric cham cai gi / chung-hay-rieng) sang cum GD0-disambiguation hoac sau cong go/no-go, chi giu cau WHY/pain o GD1; nang idea-TC3 tu 1 len 2. Va: dung chot 'KHA THI RO' khi con an so (vd cost keo gia cloud ngoai) — hoi lam ro bien do TRUOC roi moi chot truc kha thi.
- frame: doi 8 cau free-form thanh AskUserQuestion co cau truc cho cau uu tien; tach phan 'phat hien bug/file khong phai pastebin' ra khoi khung TU CHOI de dong mo dau khong loang. Cong CHO XAC NHAN da chuan, chi mai lieu luong hoi.
- triage: neo mot luong 'ban o day' 5-8 buoc doi thuong dat SOM (truoc phan Tang/Trach nhiem) de vai CTO/business co khung dinh vi truoc khi gap MapReduce/mrjob; keo rui ro THAT (vd goi ham thua dong 73 → bo sot trang) vao thang dong 'Rui ro khi tac dong' thay vi tach khoi field.
- review: them 2-3 cau mo dau doi thuong ('pastebin cho ai dan link cong khai, rui ro lon nhat la ai cung doan duoc link') TRUOC khi tha Write API/shortlink; sap xep bao cao theo MUC nghiem trong (gom Critical lien tiep) thay vi bam luong file; chinh vai dong neo lech 1 don vi cho khop tuyet doi.
- Bo metric — sua stakeholder-comm: KHONG ap gate cua no len output khong-phai-explain. Hoac (a) lam rubric-stakeholder rieng cho tung ho skill (review/triage cho dev co the co bien the doi thuong tuy chon, khong bat buoc), hoac (b) trong scorecard danh dau ro 'N/A - tham chieu' de khong tao gate-fail gia.
- Bo metric — thang min hon: 3 muc 0/1/2 da bao hoa o nhom dan dau (contract 9.2-10). Chia nho tieu chi hoac them muc 0-3 de vong sau phan giai duoc cac ban sat tran; can nhac tieu chi thu 8 (consistency/mau-thuan-noi-tai) neu loi 'cua duy nhat vs 2 chokepoint' lap lai.
- Bo eval — chong nhieu grounding: cham cung-agent A/B hoac nhieu mau khi so baseline-vs-variant, dung doc chenh-1-diem giua 2 agent khac nhau la tin hieu (bai hoc RESULT.md). Va them fixture 2-project de test cach-ly state truoc khi mo rong (roadmap P1).
