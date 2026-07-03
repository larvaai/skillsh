# README — Bo Eval Skills (System Design Primer)

## Muc dich
Do 3 nang luc cua agent khi goi skills tren mot codebase that:
1. **contract_fidelity** — bam dung hop dong CUA CHINH skill (explain/idea/frame/triage/review co rubric xuong song rieng).
2. **stakeholder_comm** — trao doi voi CTO/business co dat chuan (van de+cho-ai truoc thuat ngu; khong jargon mo coi). *Rubric goc cua `explain`.*
3. **collaboration** — dan dat de phoi hop (khong vuot quyen scope; ket bang mot cong go/no-go ro). *Rubric collab-leadership.*

## Cau truc thu muc
```
experiments/
  skill-eval/
    fixtures/system-design-primer/     # codebase that (read-only) — nguon fixture
      solutions/system_design/
        pastebin/pastebin.py           # fixture explain + review
        web_crawler/web_crawler_snippets.py   # fixture triage
        mint/mint_snippets.py          # fixture triage
        ...
  runs/<timestamp>/                    # mot vong chay (mau tune explain)
    fixture.txt                        # project·level·mode co dinh cho ca vong
    baseline/{variant.md, grade.txt}   # ban goc
    A/ B/ C/ D/ E/{variant.md,grade.txt} # cac huong sua
    RESULT.md                          # bang xep hang + gate + fix_first
.claude/skills/
  grade/{SKILL.md, rubric.md, example.md}  # thuoc do explain (7 tieu chi x0/1/2)
  tune/SKILL.md                        # harness thi nghiem song song
```

## Y nghia moi rubric/metric
- **6 rubric da xay:** 4 rubric skill (idea/frame/triage/review) + 2 rubric cheo (stakeholder-comm, collab-leadership).
- **Moi tieu chi = 0/1/2.** Mot so tieu chi la **xuong song (gate):** =0 la ROT gate du tong cao. Vi du (rubric explain, `grade/rubric.md`): tieu chi 1 (MUC), 4 (LOI VAN), 5 (BAM CODE).
- **Gate cua tung ho skill:**
  - explain: MUC / LOI VAN / BAM CODE.
  - idea: Router / Dung nhanh / Hoi dung tang / Khong vuot vai (deu phai >0).
  - frame: KHONG code truoc xac nhan / DUNG mot slice.
  - triage: verdict hop le (1 trong 7) / trung thuc caller / gate truoc verdict manh.
  - review: dung loai gap / bang chung co vi tri / khong bia.
  - collab-leadership (moi output): TC1 khong vuot quyen / TC4 ket bang mot cong.
- **QUY TAC QUAN TRONG — stakeholder-comm la rubric cua explain.** Chi cham GATE-CO-HIEU-LUC cho output `explain`. Voi idea/frame/triage/review no cham THAM CHIEU va KHONG keo gate_pass tong. Ghi ro "N/A tren truc gate" de tranh gate-fail gia (vd review/correctness sach nhung "FAIL" chi vi ap sai thuoc).

## Cach chay lai bo test
Mo hinh giong `tune` (thi nghiem song song, cham mu):
1. **Co dinh fixture:** chon project·level·mode (vd `pastebin · L2 · overview`), ghi vao `runs/<ts>/fixture.txt`. Moi variant + baseline PHAI chay CUNG fixture (doi fixture giua chung → loai thi nghiem — gate cua tune).
2. **Sinh output:** goi skill (`/explain`, `/idea`, `/frame`, `/triage`, `/review`) tren fixture → luu `<variant>/variant.md`.
3. **Cham mu bang `grade`:** giam khao chi nhan `{project, level, mode, output.txt}`, khong biet variant nao. `grade` nhan tham so `skill` de doc `rubric-<skill>.md` (mo tran cham ngoai explain).
   - Cham >=2 giam khao doc lap, lay trung vi, BAO PHUONG SAI. Dung doc chenh-lech-1-diem la tin hieu (bai hoc tu RESULT.md: 2 agent khac nhau tren codebase la tron "hieu ung sua" voi "nhieu grounding").
4. **Loai het ban ROT GATE truoc, roi moi xep theo tong** (rubric.md muc Gate).
5. **Chong over-fit (Buoc 5 cua tune):** chay lai ban thang tren project THU HAI khac domain; chi hon o fixture goc → nhan over-fit.

## Cach them scenario / skill moi
- **Them scenario:** them mot file/luong trong `fixtures/system-design-primer/` (hoac fixture 2-project cho test cach-ly, xem roadmap-suite.md P1) → tao `runs/<ts>/` moi voi fixture.txt tro toi no.
- **Them skill vao eval:** viet `rubric-<skill>.md` (bien hop dong skill thanh 0/1/2, danh dau tieu chi xuong song). `grade` nhan `skill=<ten>` → doc rubric do. **Gate cua tune:** tune skill CHUA co rubric → DUNG, yeu cau lam rubric truoc.
- **Bo/sua metric:** giu 3 truc; neu them tieu chi thu 8 chi khi co MOT kieu loi that lap lai ma 7 tieu chi khong bat duoc (vd consistency — mau thuan noi tai). Xem RESULT.md muc "Mau thuan rubric-skill".

## Chay lai bang cong cu co san
- `/tune <skill>` — chay baseline + cac huong song song, cham bang thuoc, xep hang (mau o `runs/20260701-143138/`).
- `/grade` (tham so `skill`) — cham 1 output theo rubric tuong ung, tra khung 7 dong + TONG/14 + GATE + "SUA TRUOC TIEN".