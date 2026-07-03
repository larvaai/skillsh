export const meta = {
  name: 'skill-fake-test-regrade',
  description: 'Re-grade all 28 skill outputs from disk (previous grades were rate-limited), persist each grade, re-synthesize with full recall table',
  phases: [
    { title: 'Grade', detail: 'adversarial grader per skill, writes grades/<skill>.json' },
    { title: 'Synthesize', detail: 'merge all disk grades into REPORT.md with recall table' },
  ],
}

const ROOT = '/Users/uspro/Desktop/skillsh'
const SK = ROOT + '/.claude/skills'
const BASE = ROOT + '/experiments/skill-fake-test'
const CODE = BASE + '/fixture/codebase/mediremind'
const ANSWER = BASE + '/fixture/ANSWER-KEY.md'
const FLAWED = BASE + '/fixture/flawed-explain.md'
const OUT = BASE + '/outputs'
const GRADES = BASE + '/grades'

const GRADE_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['skill', 'gate', 'effectiveness', 'recall', 'evidence', 'top_failure', 'verdict_one_line'],
  properties: {
    skill: { type: 'string' },
    gate: { type: 'string', enum: ['pass', 'fail', 'n/a'] },
    effectiveness: { type: 'integer', minimum: 0, maximum: 3 },
    recall: { type: 'string' },
    evidence: { type: 'string' },
    top_failure: { type: 'string' },
    verdict_one_line: { type: 'string' },
  },
}

// name, cat, answer-key section (or null)
const SKILLS = [
  ['idea', 'pipeline', null], ['shape', 'pipeline', null], ['stack', 'pipeline', null],
  ['skeleton', 'pipeline', null], ['backlog', 'pipeline', null], ['modules', 'pipeline', null],
  ['delivery', 'pipeline', null], ['uat', 'pipeline', null], ['ship', 'pipeline', null],
  ['operate', 'pipeline', null],
  ['charter', 'pm', null], ['resume', 'pm', null], ['progress', 'pm', null],
  ['checkpoint', 'pm', null], ['fanout', 'pm', null], ['frame', 'pm', null], ['partner', 'pm', null],
  ['traceability', 'meta', 'D'],
  ['atlas', 'code', null], ['explain', 'code', null], ['trace', 'code', 'B'],
  ['triage', 'code', 'C'], ['review', 'code', 'A'], ['teen', 'code', null],
  ['grade', 'meta', 'E'], ['spar', 'meta', null], ['skill-define', 'meta', null], ['tune', 'meta', null],
]

function gradePrompt([name, cat, ak]) {
  let p = 'Bạn là GIÁM KHẢO ĐỐI KHÁNG. Chấm xem skill "' + name + '" chạy trên dữ liệu giả MediRemind CÓ HIỆU QUẢ không.\n\n'
  p += 'BƯỚC 1 đọc hợp đồng gốc: ' + SK + '/' + name + '/SKILL.md (VÀ ' + SK + '/' + name + '/rubric.md nếu tồn tại — dùng gate xương sống của nó).\n'
  p += 'BƯỚC 2 đọc TẤT CẢ file skill vừa sinh trong ' + OUT + '/' + name + '/ (nếu trống → effectiveness 0, gate fail).\n'
  if (name === 'grade') p += 'Lưu ý: skill grade được yêu cầu chấm bản explain lỗi ở ' + FLAWED + ' (bịa Kafka/microservice). '
  if (name === 'review' || name === 'trace' || name === 'triage') p += 'Đối chiếu code thật ở ' + CODE + '. '
  if (ak) p += 'BƯỚC 3 đọc ĐÁP ÁN ' + ANSWER + ' mục ' + ak + ' — đo RECALL: bắt đúng bao nhiêu / tổng khuyết tật cài sẵn, THIẾU cái nào (ghi tên cụ thể, vd "thiếu BUG-5 IDOR").\n'
  else p += 'Skill này không có đáp án cứng → recall = "n/a"; chấm theo hợp đồng/rubric.\n'
  p += '\nChấm khắt khe, không cả nể:\n'
  p += '- gate: pass/fail theo xương sống rubric (skill không rubric → gate theo tiêu chí "works effectively" của hợp đồng); n/a nếu thật sự không có khái niệm gate.\n'
  p += '- effectiveness 0-3: 0=không ra gì dùng được · 1=ra nhưng rớt gate/lệch hợp đồng · 2=chạy được nhưng có friction đáng kể · 3=chạy sạch đúng hợp đồng.\n'
  p += '- recall (chỉ skill có đáp án): "X/N, thiếu: ...".\n- evidence: trích dẫn/đường dẫn cụ thể chứng minh.\n- top_failure: điểm yếu lớn nhất, hoặc NONE.\n- verdict_one_line.\n\n'
  p += 'BƯỚC 4 (BẮT BUỘC): ghi phán quyết ra ' + GRADES + '/' + name + '.json (đúng JSON, các field của schema). RỒI trả về cùng JSON đó. Viết tiếng Việt.'
  return p
}

phase('Grade')
log('Chấm lại 28 skill từ artifact trên đĩa (grade trước bị rate-limit). Mỗi grade tự ghi ra grades/.')
const grades = await parallel(SKILLS.map((s) => () =>
  agent(gradePrompt(s), { label: 'grade:' + s[0], phase: 'Grade', schema: GRADE_SCHEMA, effort: 'high' })
    .then((g) => (g ? { name: s[0], cat: s[1], ak: s[2], grade: g } : null))))

const clean = grades.filter(Boolean)
phase('Synthesize')
log('Có ' + clean.length + '/28 grade. Tổng hợp REPORT.md (đọc thêm grades/ trên đĩa cho chắc).')

const synth = await agent(
  'Tổng hợp cuộc thử: nhét dữ liệu giả (project MediRemind, đang giữa GĐ11) vào 28 skill của pipeline Idea→Operate rồi chấm từng skill có chạy HIỆU QUẢ không.\n\n' +
  'Nguồn chấm: đọc TẤT CẢ file ' + GRADES + '/*.json trên đĩa (đây là bản đầy đủ, đã ghi lại sau khi sửa rate-limit). Đáp án đo recall ở ' + ANSWER + '.\n\n' +
  'GHI ĐÈ ' + BASE + '/REPORT.md, tiếng Việt, gồm:\n' +
  '1. TL;DR 5-7 dòng: đếm skill theo effectiveness (mấy cái =3, =2, =0-1), mấy skill RỚT gate, và PHÁT HIỆN LỚN NHẤT.\n' +
  '2. Bảng xếp hạng MỌI skill, nhóm theo cat (pipeline/pm/code/meta): skill · gate · eff(0-3) · recall · top_failure · verdict 1 dòng.\n' +
  '3. Bảng RECALL đáp án cho 5 skill có đáp án — review(A,7 bug) · trace(B) · triage(C) · traceability(D,4 gap) · grade(E): BẮT gì / THIẾU gì / kết luận đạt-không. Đây là mục quan trọng nhất.\n' +
  '4. Skill RỚT hoặc friction cao: chẩn đoán nguyên nhân (thiếu input? mâu thuẫn SKILL.md? lệch convention đích ghi docs/ vs state/ vs outputs/? thiếu user thật?).\n' +
  '5. Meta-findings xuyên skill: pattern lỗi lặp lại (phân biệt rõ: lỗi do FIXTURE/môi trường test vs lỗi THẬT trong SKILL.md).\n' +
  '6. TOP việc nên sửa theo đòn bẩy, tách "sửa harness test" khỏi "sửa skill".\n\n' +
  'Trung thực về giới hạn: đây là chạy MÔ PHỎNG (agent đọc SKILL.md rồi làm theo), không phải invoke skill thật; nêu điều đó ở cuối. Trả về đường dẫn REPORT.md + TL;DR đầy đủ.',
  { label: 'synthesize', phase: 'Synthesize', effort: 'high' })

return { report: BASE + '/REPORT.md', graded: clean.length, synth }
