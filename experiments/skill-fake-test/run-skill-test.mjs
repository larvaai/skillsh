export const meta = {
  name: 'skill-fake-test',
  description: 'Inject coherent fake project data (MediRemind) into all 28 skills, run each, adversarially grade effectiveness',
  phases: [
    { title: 'Fixture', detail: 'expand BIBLE into the upstream reference chain (5 builders)' },
    { title: 'Test', detail: 'one agent per skill: read SKILL.md + fake input, execute, write output' },
    { title: 'Grade', detail: 'adversarial grader per skill: gate + effectiveness + recall vs answer key' },
    { title: 'Synthesize', detail: 'rank skills, recall table, broken-skill diagnosis, prioritized fixes' },
  ],
}

const ROOT = '/Users/uspro/Desktop/skillsh'
const SK = ROOT + '/.claude/skills'
const BASE = ROOT + '/experiments/skill-fake-test'
const FX = BASE + '/fixture/mediremind'            // reference chain (built this run)
const CODE = BASE + '/fixture/codebase/mediremind' // real fake code (already on disk)
const BIBLE = BASE + '/fixture/BIBLE.md'
const ANSWER = BASE + '/fixture/ANSWER-KEY.md'
const FLAWED = BASE + '/fixture/flawed-explain.md'
const OUT = BASE + '/outputs'

const TEST_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['skill', 'produced_files', 'worked', 'friction', 'notes'],
  properties: {
    skill: { type: 'string' },
    produced_files: { type: 'array', items: { type: 'string' } },
    worked: { type: 'boolean', description: 'did the skill procedure run to a usable artifact' },
    friction: { type: 'array', items: { type: 'string' }, description: 'anything that made the skill hard to execute: missing input, ambiguous step, contradictory instruction' },
    missing_inputs: { type: 'array', items: { type: 'string' } },
    notes: { type: 'string' },
  },
}

const GRADE_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['skill', 'gate', 'effectiveness', 'evidence', 'top_failure', 'verdict_one_line'],
  properties: {
    skill: { type: 'string' },
    gate: { type: 'string', enum: ['pass', 'fail', 'n/a'], description: 'did it pass the skill rubric backbone gate' },
    effectiveness: { type: 'integer', minimum: 0, maximum: 3, description: '0 broke/nothing usable · 1 produced but misses gate/contract · 2 works with friction · 3 works cleanly per contract' },
    recall: { type: 'string', description: 'for answer-key skills: X/N planted items caught, name misses; else n/a' },
    evidence: { type: 'string', description: 'concrete quote/path proving the verdict' },
    top_failure: { type: 'string', description: 'single biggest weakness, or NONE' },
    verdict_one_line: { type: 'string' },
  },
}

// ---------- PHASE 1: fixture builders (disjoint file sets, all anchored to BIBLE) ----------
const anchor = 'Bám TUYỆT ĐỐI vào BIBLE tại ' + BIBLE + ' — KHÔNG bịa thực thể/số mâu thuẫn. Đọc BIBLE trước. '
const FIXTURE = [
  { label: 'fx-problem', p: anchor +
    'Dựng 4 artifact GĐ1-4 cho project mediremind, mỗi file ~1 trang, mở đầu bằng góc-nhìn-lãnh-đạo rồi chi tiết:\n' +
    '- ' + FX + '/problem/business-case.md (dùng SM-1, SM-2 ở BIBLE §3)\n' +
    '- ' + FX + '/problem/product-brief.md\n' +
    '- ' + FX + '/problem/requirements.md (liệt kê AC dạng Given/When/Then cho slice xác-nhận-liều + NFR-1..5 §6)\n' +
    '- ' + FX + '/problem/prd.md\nCũng ghi ' + FX + '/idea/mediremind.md (bản prose ý tưởng thô §1-3) và ' + FX + '/idea/_index.md. Chỉ trả 1 dòng xác nhận.' },
  { label: 'fx-domain-shape', p: anchor +
    'Dựng:\n- ' + FX + '/docs/domain-model.md: 7 entity §4 + 4 bounded context §5 + quan hệ + trạng thái DoseEvent.\n' +
    '- ' + FX + '/docs/architecture.md: Architecture Brief (bảng) + C4 Context&Container + Data Flow + Integration + Security Model (bám NFR-4) + ≥2 ADR (mỗi ADR có phương-án-đã-loại), theo kiến trúc §7. GIỮ open-Q §7 (managed queue vs cron) là "còn treo → GĐ7". KHÔNG chốt tên framework. Chỉ trả 1 dòng.' },
  { label: 'fx-stack-skel-backlog', p: anchor +
    'Dựng:\n- ' + FX + '/docs/tech-decision.md: Tech Decision Matrix có điểm (fit domain/team §8/scale §6/NFR) + ADR chọn framework + để OQ-B (retention §12) treo.\n' +
    '- ' + FX + '/docs/skeleton-live-slice.md: Live Slice Report cho slice §9, trỏ code thật ở ' + CODE + ', có "bằng chứng chạy" (giả lập staging + test E2E + log) + checklist validate 9 ô.\n' +
    '- ' + FX + '/docs/backlog.md: Roadmap (theme×release) + Backlog Epic→Feature→Story→AC (Given/When/Then), mỗi epic nối ngược SM-1/SM-2. Chỉ trả 1 dòng.' },
  { label: 'fx-modules-delivery-ship', p: anchor +
    'Dựng:\n- ' + FX + '/docs/module-map.md: 4 module theo bounded context §5, mỗi module 1 owner + "Does NOT own".\n' +
    '- ' + FX + '/docs/contracts/scheduling-v1.md và ' + FX + '/docs/contracts/adherence-v1.md: public API + domain event + data ownership + error code.\n' +
    '- ' + FX + '/codebase/delivery-standards.md: Delivery Standards + Definition of Ready/Done + PR Checklist.\n' +
    '- ' + FX + '/codebase/ship.md: Go/No-Go checklist + Rollback Plan + Rollout. CỐ Ý ĐỂ GAP: cổng GO/NO-GO CHƯA có 2 chữ ký (G-2), rollback ghi "CHƯA chạy thử" (G-4). KHÔNG tạo uat-report (G-1). Chỉ trả 1 dòng.' },
  { label: 'fx-governance', p: anchor +
    'Dựng bộ quản trị cho mediremind:\n- ' + FX + '/constitution/process.md, conventions.md, folders.md, definition-of-done.md (DoD rõ theo giai đoạn).\n' +
    '- ' + FX + '/codebase/pointer.md trỏ code thật ở ' + CODE + '.\n' +
    '- ' + FX + '/progress/progress.json: JSON hợp lệ, schema giống projects/multi-lens-chat, con trỏ giai_doan="gd11_delivery" (§11), gồm tasks GĐ0-10 done + một parallel_group build GĐ11 (vd pg-build: T sinh scheduling module, T sinh reminders module) đều READY (depends_on đã done), GĐ12 uat todo. GIỮ 2 open-Q chưa đóng (OQ-A queue/cron, OQ-B retention) như ghi chú.\n' +
    '- ' + FX + '/progress/board.md tóm tắt. Chỉ trả 1 dòng.' },
]

// ---------- PHASE 2/3: per-skill specs ----------
const S = (name, cat, task, opts = {}) => ({ name, cat, task, ak: opts.ak || null, forbid: opts.forbid || null })
const SKILLS = [
  // pipeline producers
  S('idea', 'pipeline', 'Cold-start từ ý tưởng thô ở ' + FX + '/idea/mediremind.md (+ BIBLE §1-3). Chạy router (độ rõ×khả thi) rồi dẫn GĐ0→5 sinh Idea Brief→Business Case→PRD→Domain Model vào ' + OUT + '/idea/. DỪNG ở Domain, KHÔNG code, KHÔNG tự kill.', { forbid: FX + '/problem/*, ' + FX + '/docs/domain-model.md' }),
  S('shape', 'pipeline', 'Input CHỈ: ' + FX + '/docs/domain-model.md + ' + FX + '/problem/requirements.md (NFR). Sinh Architecture Brief+C4+DataFlow+Integration+Security+ADR vào ' + OUT + '/shape/. KHÔNG chốt framework.', { forbid: FX + '/docs/architecture.md' }),
  S('stack', 'pipeline', 'Input: ' + FX + '/docs/architecture.md + BIBLE §8 (ràng buộc đội) + NFR §6. Sinh Tech Decision Matrix có điểm + ADR chọn framework vào ' + OUT + '/stack/.', { forbid: FX + '/docs/tech-decision.md' }),
  S('skeleton', 'pipeline', 'Input: ' + FX + '/docs/tech-decision.md + architecture.md + domain-model.md + code thật ' + CODE + '. Sinh Live Slice Report (slice §9) vào ' + OUT + '/skeleton/, tick checklist chỉ khi có bằng chứng.', { forbid: FX + '/docs/skeleton-live-slice.md' }),
  S('backlog', 'pipeline', 'Input: ' + FX + '/docs/skeleton-live-slice.md + ' + FX + '/problem/prd.md + docs/domain-model.md. Sinh Roadmap+Backlog(Epic→Story→AC) vào ' + OUT + '/backlog/, mỗi epic nối ngược SM-1/SM-2.', { forbid: FX + '/docs/backlog.md' }),
  S('modules', 'pipeline', 'Input: ' + FX + '/docs/domain-model.md + ' + FX + '/docs/backlog.md. Sinh Module Map + Module Contract vào ' + OUT + '/modules/, mỗi module 1 owner + "Does NOT own".', { forbid: FX + '/docs/module-map.md, ' + FX + '/docs/contracts' }),
  S('delivery', 'pipeline', 'Input: ' + FX + '/docs/module-map.md + ' + FX + '/docs/contracts/. Sinh Delivery Standards + DoD + PR Checklist vào ' + OUT + '/delivery/.', { forbid: FX + '/codebase/delivery-standards.md' }),
  S('uat', 'pipeline', 'Input: ' + FX + '/codebase/delivery-standards.md + ' + FX + '/constitution/definition-of-done.md + ' + FX + '/problem/requirements.md (AC) + code ' + CODE + '. Sinh Test&Verification Report (bảng Req→AC→TC→Result→Release) + 2 sign-off vào ' + OUT + '/uat/. Đánh dấu hở test, KHÔNG tự quyết go/no-go.'),
  S('ship', 'pipeline', 'Fixture CỐ Ý thiếu uat.md, nên đây là UAT tóm tắt cấp trực tiếp: "UAT pass 18/20 AC, 2 BLOCKED (permission trên confirm-dose, double-send reminder); Security sign-off: TREO vì lỗ IDOR; QA ký, Security CHƯA ký". Cùng ' + FX + '/codebase/skeleton-live-slice.md. Sinh Go/No-Go + Runbook + Rollback + Rollout vào ' + OUT + '/ship/. KHÔNG tự bấm GO.', { forbid: FX + '/codebase/ship.md' }),
  S('operate', 'pipeline', 'Input: ' + FX + '/codebase/ship.md + ' + FX + '/docs/backlog.md + BIBLE §3 (SM-1/SM-2). Sinh Ops Dashboard 4 nhóm + Incident Process + Iteration Loop→backlog vào ' + OUT + '/operate/, Business metric đối chiếu thẳng SM-1/SM-2.'),
  // project-management
  S('charter', 'pm', 'Từ ý tưởng ' + FX + '/idea/mediremind.md, DỰNG một workspace project MỚI (đừng đụng fixture) tại ' + OUT + '/charter/mediremind2/: 6 folder + constitution seed 4 file + progress.json seed (T-01 GĐ0) + README. Chỉ chạy scaffold một lần.'),
  S('resume', 'pm', 'READ-ONLY toàn workspace fixture ' + FX + ' (constitution + progress.json + artifact). In khối "ĐANG Ở ĐÂU" (bức tranh + đã chốt + task ready + parallel_group + tiến cử skill kế) ghi ' + OUT + '/resume/panorama.md. Không hỏi lại quyết định đã chốt.'),
  S('progress', 'pm', 'COPY ' + FX + '/progress/progress.json sang ' + OUT + '/progress/ rồi thao tác ở bản copy: (1) PLAN — chia chunk GĐ11 kế thành task có depends_on+parallel_group+owner+artifact, tính task ready; (2) ADVANCE — giả định T sinh scheduling báo xong, kiểm cần phiếu checkpoint PASS trước khi lật done. Ghi progress.json + board.md.'),
  S('checkpoint', 'pm', 'Artifact xét: ' + FX + '/codebase/delivery-standards.md. Chuẩn: ' + FX + '/constitution/definition-of-done.md. Cấp phiếu PASS/FAIL (checklist khớp + lý do cụ thể) vào ' + OUT + '/checkpoint/delivery.md. Chỉ kiểm, không sửa artifact.'),
  S('fanout', 'pm', 'DRY-RUN (đừng thực sự spawn). Đọc ' + FX + '/progress/progress.json, tìm parallel_group mọi task READY, gói cho mỗi task một context bundle gọn (constitution liên quan + contract ' + FX + '/docs/contracts/ + spec task + đích artifact + ranh giới KHÔNG-build). Ghi kế hoạch + các bundle vào ' + OUT + '/fanout/. Nêu rõ vì sao KHÔNG đổ cả repo cho agent.'),
  S('traceability', 'meta', 'Soi toàn pipeline fixture ' + FX + ' (+ progress.json). Sinh Traceability Report (Dashboard 15 GĐ + kiểm sợi + danh sách thiếu + cổng chưa qua) vào ' + OUT + '/traceability/report.md. Nhắc skill cần chạy, KHÔNG tự chạy.', { ak: 'D' }),
  S('frame', 'pm', 'Chọn MỘT user story từ ' + FX + '/docs/backlog.md. Input kèm: architecture.md, tech-decision.md, domain-model.md. Đóng khung slice: hỏi Scope/Boundary/Acceptance, chờ xác nhận TRƯỚC khi viết code (mô phỏng: nêu rõ điểm dừng chờ user). KHÔNG code cả app. Ghi khung + agent-state vào ' + OUT + '/frame/.'),
  S('partner', 'pm', 'Vào vai fractional-CTO với nhu cầu business ở BIBLE §1-3 (cold-start). Đánh giá khả thi → dẫn hỏi-đáp theo cụm → decision-log + handoff sang skill GĐ kế. TUYỆT ĐỐI không nhảy ý→code. Ghi ' + OUT + '/partner/pipeline-state.md.'),
  // code-understanding
  S('atlas', 'code', 'Đọc code thật ' + CODE + '. Dựng bản đồ hiểu biết vào ' + OUT + '/atlas/.ai-understanding/. Quy mô nhỏ nên làm ĐẠI DIỆN: 00_index + scorecard + ≥3 artifact, MỖI claim có bằng chứng (file·symbol·code·lý do·độ tin). Ghi rõ đây là bản scaled.'),
  S('explain', 'code', 'Giải thích codebase ' + CODE + ' — mode OVERVIEW, level L3. Theo thang zoom: vấn đề→ý tưởng lõi→luồng như câu chuyện→module; thuật ngữ chỉ xuất hiện sau khi neo. TRUNG THỰC theo code (modular monolith, KHÔNG Kafka/microservice). Ghi ' + OUT + '/explain/answer.md.'),
  S('trace', 'code', 'Trace đối tượng: trường "status" của một DoseEvent qua ' + CODE + '. Nêu đường đi chính + điểm thay đổi state + side effect, mỗi bước file·symbol·điều xảy ra·độ chắc. Ghi ' + OUT + '/trace/trace.md.', { ak: 'B' }),
  S('triage', 'code', 'Xét ĐÚNG file ' + CODE + '/src/legacy/old_reminder_cron.ts. Grep caller trong ' + CODE + '. Ra verdict (giữ/sửa-nhỏ/chuyển/xoá/rewrite/archive) + lý do + rủi ro. Ghi ' + OUT + '/triage/verdict.md.', { ak: 'C' }),
  S('review', 'code', 'Rà lỗ hổng của slice: ' + CODE + '/src/scheduling, /reminders, /adherence, /identity. Báo gap (edge case/error path/permission) theo Critical/Medium/Low, mỗi gap file·dòng·lý do. Đóng khung fix là việc /frame, không tự code. Ghi ' + OUT + '/review/gaps.md.', { ak: 'A' }),
  S('teen', 'code', 'Giải thích đoạn KHÓ ' + CODE + '/src/adherence/streak.ts bằng ngôn ngữ đời thường: 0 từ kỹ thuật (function/loop/variable/array...), vấn đề trước, chạy bằng lời, 1 câu vì sao quan trọng. Ghi ' + OUT + '/teen/plain.md.'),
  // meta
  S('grade', 'meta', 'Chấm bản explain ở ' + FLAWED + ' (mode overview, level L3) theo rubric ' + SK + '/grade/rubric.md. Để kiểm bịa, đối chiếu code thật ' + CODE + '. Ra 7 tiêu chí×0/1/2 + phán gate + đòn bẩy sửa. Ghi ' + OUT + '/grade/grade.md.', { ak: 'E' }),
  S('spar', 'meta', 'Mô phỏng vòng spar: (1) tạo prompt.md (status waiting-user) — câu hỏi "MediRemind nên xử lý reminder gửi lặp thế nào?"; (2) GIẢ user đã trả lời: tự ghi user-output.md + đặt status user-answered; (3) CHỈ SAU đó viết claude-output.md; (4) grade-output.md chấm cả hai + coach. Chứng minh gate status. Ghi ' + OUT + '/spar/round-1/.'),
  S('skill-define', 'meta', 'Nhu cầu: "muốn tự phát hiện reminder bị gửi lặp/flaky rồi cảnh báo". Liệt kê 3-5 trường hợp hay gặp + "không có skill thì làm sao" + kết luận có đáng làm skill không. Ghi ' + OUT + '/skill-define/define.md.'),
  S('tune', 'meta', 'THIẾT KẾ (dry-run, đừng chạy 5 variant) một thí nghiệm tune skill "teen" trên fixture ' + CODE + '/src/adherence/streak.ts: cố định fixture, baseline, 3-5 hướng sửa 1-biến, cách chấm mù, cách confirm bản thắng. Ghi ' + OUT + '/tune/design.md.'),
]

// ---------- build prompts ----------
function testPrompt(s) {
  let p = 'Bạn đang THỰC THI skill "' + s.name + '" trên DỮ LIỆU GIẢ để kiểm skill có chạy hiệu quả không.\n\n'
  p += 'BƯỚC 1 — đọc hợp đồng skill: ' + SK + '/' + s.name + '/SKILL.md (và rubric.md nếu có). Làm ĐÚNG như skill quy định.\n'
  p += 'BƯỚC 2 — làm việc sau trên input giả:\n' + s.task + '\n'
  if (s.forbid) p += '\nCẤM đọc (tránh lộ đáp án — đây là bản skill phải tự sinh): ' + s.forbid + '\n'
  p += '\nBƯỚC 3 — GHI artifact ra đĩa đúng đường dẫn nêu trên (tạo thư mục nếu cần).\n'
  p += 'BƯỚC 4 — trả self-report: produced_files (đường dẫn thật đã ghi), worked, friction (mọi chỗ khó/mâu thuẫn/thiếu input khi CHẠY THEO SKILL.md), missing_inputs, notes.\n'
  p += 'Trung thực: nếu SKILL.md có bước không làm được với input này, ghi vào friction thay vì giả vờ xong. Viết tiếng Việt.'
  return p
}
function gradePrompt(s, tr) {
  let p = 'Bạn là GIÁM KHẢO ĐỐI KHÁNG, chấm xem skill "' + s.name + '" chạy trên dữ liệu giả CÓ HIỆU QUẢ không.\n\n'
  p += 'Hợp đồng gốc: ' + SK + '/' + s.name + '/SKILL.md (+ rubric.md nếu có — đọc và dùng gate của nó).\n'
  p += 'Sản phẩm skill vừa sinh: đọc các file trong ' + OUT + '/' + s.name + '/ (self-report: ' + JSON.stringify(tr && tr.produced_files || []) + ').\n'
  if (s.ak) p += 'ĐÁP ÁN (chỉ giám khảo được xem) ở ' + ANSWER + ' — dùng ĐÚNG mục ' + s.ak + ' để đo RECALL (bắt được bao nhiêu/bao nhiêu khuyết tật cài sẵn, thiếu cái nào).\n'
  p += '\nChấm khắt khe:\n- gate: pass/fail theo xương sống rubric skill (nếu skill không có rubric, gate theo tiêu chí "works effectively" trong hợp đồng); n/a nếu không áp dụng.\n'
  p += '- effectiveness 0-3 (0 không ra gì dùng được · 1 ra nhưng rớt gate/lệch hợp đồng · 2 chạy được nhưng có friction · 3 chạy sạch đúng hợp đồng).\n'
  p += '- recall: với skill có đáp án ghi "X/N, thiếu: ...", còn lại "n/a".\n- evidence: trích dẫn/đường dẫn cụ thể.\n- top_failure: điểm yếu lớn nhất hoặc NONE.\n'
  p += 'Nếu skill KHÔNG sinh được file (thư mục trống) → effectiveness 0, gate fail. Đừng cả nể. Viết tiếng Việt.'
  return p
}

// ---------- run ----------
phase('Fixture')
log('Dựng chuỗi artifact tham chiếu MediRemind từ BIBLE (5 builder)...')
await parallel(FIXTURE.map((f) => () => agent(f.p, { label: f.label, phase: 'Fixture' })))
log('Fixture xong. Bắt đầu test ' + SKILLS.length + ' skill (test → grade theo pipeline).')

const results = await pipeline(
  SKILLS,
  (s) => agent(testPrompt(s), { label: 'test:' + s.name, phase: 'Test', schema: TEST_SCHEMA })
           .then((tr) => ({ s, tr })),
  (prev, s) => {
    const tr = prev && prev.tr
    return agent(gradePrompt(s, tr), { label: 'grade:' + s.name, phase: 'Grade', schema: GRADE_SCHEMA, effort: 'high' })
             .then((g) => ({ name: s.name, cat: s.cat, ak: s.ak, worked: tr && tr.worked, friction: (tr && tr.friction) || [], grade: g }))
  },
)

const clean = results.filter(Boolean)
phase('Synthesize')
log('Chấm xong ' + clean.length + '/' + SKILLS.length + ' skill. Tổng hợp báo cáo...')

const synthInput = JSON.stringify(clean.map((r) => ({
  skill: r.name, cat: r.cat,
  gate: r.grade && r.grade.gate, eff: r.grade && r.grade.effectiveness,
  recall: r.grade && r.grade.recall, top_failure: r.grade && r.grade.top_failure,
  verdict: r.grade && r.grade.verdict_one_line, friction: r.friction,
})))

const synth = await agent(
  'Bạn tổng hợp một cuộc thử: nhét dữ liệu giả (project MediRemind, đang giữa GĐ11) vào 28 skill của pipeline Idea→Operate và chấm từng skill có chạy HIỆU QUẢ không.\n\n' +
  'Dữ liệu chấm (JSON): ' + synthInput + '\n\n' +
  'Viết báo cáo tiếng Việt vào ' + BASE + '/REPORT.md gồm:\n' +
  '1. TL;DR 4-6 dòng: bao nhiêu skill chạy sạch (eff 3), bao nhiêu có friction (2), bao nhiêu rớt (0-1); phát hiện lớn nhất.\n' +
  '2. Bảng xếp hạng mọi skill: skill · nhóm · gate · effectiveness · recall · verdict 1 dòng (nhóm theo cat: pipeline/pm/code/meta).\n' +
  '3. Bảng RECALL đáp án cho skill có đáp án (review A / trace B / triage C / traceability D / grade E): bắt được gì, THIẾU gì.\n' +
  '4. Skill RỚT hoặc friction cao: chẩn đoán vì sao (thiếu input? mâu thuẫn trong SKILL.md? lệch convention thư mục docs/ vs state/?).\n' +
  '5. Meta-findings xuyên skill: pattern lỗi lặp lại (vd nhiều skill mơ hồ chỗ ghi artifact, hoặc gate không nhất quán).\n' +
  '6. TOP việc nên sửa, xếp theo đòn bẩy.\n' +
  'Trả về đúng đường dẫn REPORT.md + TL;DR.',
  { label: 'synthesize', phase: 'Synthesize', effort: 'high' },
)

return { report: BASE + '/REPORT.md', graded: clean.length, synth }
