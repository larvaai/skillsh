# Scorecard — 5 scenario x 3 approach x 3 truc + gate

Thang: contract_fidelity (bam hop dong skill), stakeholder_comm (trao doi CTO/business), collaboration (dan dat de phoi hop). Moi truc 0-10. gate = qua het cac tieu chi xuong song CUA CHINH skill do (+ collab-leadership TC1/TC4). Luu y: stakeholder-comm la rubric cheo viet cho `explain`; voi output khong-phai-explain (idea/frame/triage/review) no chi tham chieu, KHONG keo gate tong.

## 1. explain-pastebin (skill=explain)  — do truc tiep ca 3 rubric

| Approach | contract | stake_comm | collab | gate | 1 dong |
|---|---|---|---|---|---|
| problem-first-zoom | 7.7 | 9.4 | 8.5 | PASS | Than bai + do sau L2 dung; chi tha 3 ten code that (`pastes`,`pastebin.py`,`HitCounts`) duoi nguong L4 keo MUC xuong 1 |
| architecture-first (baseline yeu) | 4.0 | 3.0 | 6.0 | **FAIL** | Mo bang thuat ngu kien truc, dao thu tu bat buoc; rot gate MUC + rot gate stakeholder TC1/TC2 |
| analogy-business-heavy | 9.5 | 10 | 9.5 | PASS | Ban manh nhat toan bo: neo dung, cau phang, ket bang menu 3 huong + hoi lai muc; ho nho: 1 ten file that duoi L4 |

## 2. idea-new-feature (skill=idea) — stakeholder-comm la truc THAM CHIEU

| Approach | contract | stake_comm | collab | gate | 1 dong |
|---|---|---|---|---|---|
| cost-capacity-calculator | 8.3 | 8.0 | 8.8 | PASS | Sat gate o idea-TC1: chot "KHA THI RO" khi an so `cost` (keo gia cloud ngoai repo) chua hoi lam ro → ha 1 khong 0 |
| spaced-repetition-study | 8.5 | 6.5 | 9.5 | PASS | Collab manh (TC1/TC4=2) nhung con la ly do ton tai cua Nhanh B: chua dat an so spike + time-box; nen restate "toi hieu ban muon X" truoc cum hoi |
| per-exercise-self-review | 7.4 | 6.0 | 8.5 | PASS | idea-TC3 (hoi dung tang)=1 vi tron cau WHAT (Q1/Q3) vao luot dan nhan GD0→GD1; khong cau nao bi tra non nen gate giu |

## 3. frame-add-feature (skill=frame) — stakeholder-comm la truc THAM CHIEU

| Approach | contract | stake_comm | collab | gate | 1 dong |
|---|---|---|---|---|---|
| strict-slice-discipline | 9.3 | 7.5 | 10 | PASS | Chuan muc frame: khoi ─CHO XAC NHAN─ du 4 truong + "KHONG code toi khi ban duyet", dung 1 slice, day 3 tinh nang vao Parking Lot |
| eager-drift (baseline yeu) | 1.0 | 3.0 | 1.0 | **FAIL** | Code chui: tuyen bo "code ngay o luot nay" + om 3 slice; rot ca gate frame TC1/TC2 lan collab TC1/TC4 |
| over-questioning | 9.0 | 5.0 | 9.0 | PASS | Khong code, khong om nhieu slice → gate PASS; yeu o lieu luong hoi: 8 cau free-form mot lat, nen dat AskUserQuestion cho cau uu tien |

## 4. triage-files (skill=triage) — stakeholder-comm la truc THAM CHIEU

| Approach (file) | contract | stake_comm | collab | gate | 1 dong |
|---|---|---|---|---|---|
| pastebin.py | 10 | 7.5 | 8.5 | PASS | Triage sach tuyet doi: verdict `giu`+ly do+rui ro; grep "KHONG tim thay" va TU CHOI suy "0 hit=chet"; da xac minh fixture that |
| web_crawler_snippets.py | 9.3 | 6.5 | 8.5 | PASS | 3 xuong song triage =2; rui ro that (goi extract_max_priority_page thua dong 73 → bo sot trang) bi tach khoi field Risk chinh |
| mint_snippets.py | 9.3 | 6.5 | 9.0 | PASS | Chu dong ha "sua cho chay" xuong ban giao thay vi tu sua; chua truy day du duong doc/ghi cua global `seller_category_map` |

## 5. review-pastebin (skill=review) — stakeholder-comm la truc THAM CHIEU

| Approach (lens) | contract | stake_comm | collab | gate | 1 dong |
|---|---|---|---|---|---|
| security-permission-lens | 9.2 | 5.7 | 7.5 | PASS | 3 xuong song review sach (loai gap dung/bang chung co vi tri/khong bia); mo bang "Write API/shortlink" — khong loi review nhung xa nguoi ngoai |
| scale-failure-lens | 9.2 | 4.5 | 7.5 | PASS | Gap that thuoc scale, neo dung file that; yeu: sap xep bam luong file chu chua bam muc nghiem trong (Critical xen ke) |
| correctness-edgecase-lens | 10 | 2.0 | 10 | **FAIL*** | contract + collab o tran (10/10); *rot gate CHI o stakeholder-comm — la ap SAI thuoc (rubric explain len output review cho dev). Loi noi tai = sach |

## Tom tat moi skill (trung binh 3 approach, bo baseline-yeu co chu dich)

| Skill | contract (tot nhat) | stake_comm | collab | Manh o | Yeu o |
|---|---|---|---|---|---|
| **explain** | 9.5 | **9.4-10** | 9.5 | Trao doi CTO/business (truc chu dich) — cao nhat suite | Rung ten code that duoi nguong L4 (MUC/contract) |
| **idea** | 8.5 | 6.0-8.0 | 8.5-9.5 | Dan dat/phoi hop (khong vuot quyen, ket 1 cong) | Phan tang hoi (tron WHAT/WHY), chot "kha thi" khi con an so |
| **frame** | 9.3 | (tham chieu) | **10** | Ky luat cong phoi hop tuyet doi (khoi CHO XAC NHAN) | Lieu luong hoi (free-form thay vi AskUserQuestion) |
| **triage** | **10** | (tham chieu) | 8.5-9 | Chinh xac chan doan + trung thuc caller | Ban do dinh vi cho nguoi ngoai; truy duong doc/ghi |
| **review** | **10** | (tham chieu) | 7.5-10 | Bang chung neo dung dong, khong bia | Ngon ngu doi thuong cho CTO/business; sap xep theo muc |

\* Cot gate cho review/correctness ghi FAIL chi vi ap rubric stakeholder-comm (cheo, sai thuoc) — loi noi tai cua review PASS het.