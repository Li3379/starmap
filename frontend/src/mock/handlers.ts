/**
 * MSW Mock — 前端独立开发数据源。
 * 三个页面（匹配诊断/质量看板/管理后台）的 mock 数据全部在此。
 */
import { http, HttpResponse } from 'msw'

// ── Mock 岗位列表 ──
const MOCK_POSITIONS = [
  '数据分析师', '算法工程师', 'NLP工程师', 'CV工程师',
  '大数据开发工程师', '云架构师', 'DevOps工程师', '安全工程师',
  '前端开发工程师', '后端开发工程师',
]

// ── Mock JD 列表 ──
const MOCK_JD_LIST = Array.from({ length: 20 }, (_, i) => ({
  id: i + 1,
  source: ['boss', 'lagou', 'liepin'][i % 3],
  title: MOCK_POSITIONS[i % MOCK_POSITIONS.length],
  company: `${['字节跳动', '腾讯', '阿里', '百度', '华为'][i % 5]}科技`,
  content: `负责${MOCK_POSITIONS[i % MOCK_POSITIONS.length]}相关工作…`,
  city: ['北京', '上海', '深圳', '杭州', '成都'][i % 5],
  salary_min: (i % 5 + 1) * 10,
  salary_max: (i % 5 + 2) * 12,
  publish_date: `2026-06-${String(15 - i % 14).padStart(2, '0')}`,
}))

// ── Mock 匹配结果 ──
const MOCK_MATCH = {
  target_position: '数据分析师',
  match_score: 0.68,
  matched_skills: ['Python', 'Excel', 'SQL基础'],
  missing_required: ['Pandas', '统计学', '数据可视化'],
  missing_bonus: ['Tableau', '机器学习'],
  skill_gap_detail: [
    { skill: 'Pandas', importance: 'required', gap_level: '完全缺失', learning_path: ['Python基础 → NumPy → Pandas入门 → 数据处理实战'] },
    { skill: '统计学', importance: 'required', gap_level: '完全缺失', learning_path: ['概率论基础 → 描述统计 → 推断统计 → 假设检验'] },
    { skill: '数据可视化', importance: 'required', gap_level: '部分掌握', learning_path: ['Matplotlib基础 → Seaborn → 交互式图表'] },
    { skill: 'Tableau', importance: 'bonus', gap_level: '完全缺失', learning_path: ['Tableau入门 → 仪表盘设计'] },
    { skill: '机器学习', importance: 'bonus', gap_level: '完全缺失', learning_path: ['统计学 → Scikit-learn → 模型调参'] },
  ],
  overall_assessment: '基础编程能力扎实，需补充数据分析核心工具和统计学方法',
  estimated_learning_time: '3-4个月（兼职学习）',
}

// ── Mock 质量指标 ──
const MOCK_QUALITY = {
  total_nodes: 347,
  total_edges: 1256,
  avg_trust_score: 78.5,
  high_trust_ratio: 0.73,
  hallucination_rate: 0.06,
  pending_count: 12,
  weekly_new_nodes: 15,
  audit_pass_rate: 0.82,
  source_distribution: [
    { name: 'BOSS直聘', count: 180, trust: 0.75 },
    { name: '拉勾', count: 90, trust: 0.72 },
    { name: '猎聘', count: 55, trust: 0.70 },
    { name: 'ESCO', count: 22, trust: 0.92 },
  ],
  hallucination_trend: [
    { date: 'W1', rate: 0.12 },
    { date: 'W2', rate: 0.10 },
    { date: 'W3', rate: 0.08 },
    { date: 'W4', rate: 0.07 },
    { date: 'W5', rate: 0.06 },
    { date: 'W6', rate: 0.06 },
  ],
  audit_queue: [
    { id: 1, position: '算法工程师', skill: 'Transformers', trust: 62 },
    { id: 2, position: '数据分析师', skill: 'PySpark', trust: 55 },
    { id: 3, position: 'DevOps工程师', skill: 'Helm', trust: 71 },
  ],
  trust_distribution: [
    { range: '0-50', count: 5 },
    { range: '50-60', count: 12 },
    { range: '60-70', count: 35 },
    { range: '70-80', count: 68 },
    { range: '80-90', count: 42 },
    { range: '90-100', count: 18 },
  ],
}

// ── Mock 岗位技能要求（双层雷达用）──
const MOCK_POSITION_REQUIREMENTS: Record<string, { skill: string; required: number; user: number }[]> = {
  '数据分析师': [
    { skill: 'Python', required: 0.9, user: 0.7 },
    { skill: 'SQL', required: 0.85, user: 0.4 },
    { skill: 'Excel', required: 0.7, user: 0.9 },
    { skill: '统计学', required: 0.8, user: 0.2 },
    { skill: 'Pandas', required: 0.75, user: 0.1 },
    { skill: '数据可视化', required: 0.75, user: 0.3 },
  ],
  '前端开发工程师': [
    { skill: 'JavaScript', required: 0.9, user: 0.6 },
    { skill: 'Vue.js', required: 0.85, user: 0.5 },
    { skill: 'CSS', required: 0.8, user: 0.7 },
    { skill: 'TypeScript', required: 0.7, user: 0.3 },
    { skill: 'Node.js', required: 0.5, user: 0.2 },
    { skill: 'Webpack', required: 0.6, user: 0.4 },
  ],
  '后端开发工程师': [
    { skill: 'Java', required: 0.9, user: 0.8 },
    { skill: 'Spring Boot', required: 0.85, user: 0.3 },
    { skill: 'MySQL', required: 0.8, user: 0.6 },
    { skill: 'Redis', required: 0.7, user: 0.2 },
    { skill: 'Docker', required: 0.6, user: 0.4 },
    { skill: '微服务', required: 0.5, user: 0.1 },
  ],
  '算法工程师': [
    { skill: 'Python', required: 0.95, user: 0.7 },
    { skill: '机器学习', required: 0.9, user: 0.5 },
    { skill: '深度学习', required: 0.8, user: 0.3 },
    { skill: 'PyTorch', required: 0.75, user: 0.4 },
    { skill: '数学基础', required: 0.85, user: 0.6 },
    { skill: '数据处理', required: 0.7, user: 0.5 },
  ],
}

// ── Mock 管理后台 ──
const MOCK_SOURCES = [
  { id: 1, name: 'BOSS直聘', authority_score: 0.7, source_type: 'aggregator' },
  { id: 2, name: '拉勾', authority_score: 0.7, source_type: 'aggregator' },
  { id: 3, name: '猎聘', authority_score: 0.7, source_type: 'aggregator' },
  { id: 4, name: 'ESCO', authority_score: 0.9, source_type: 'official' },
]

const MOCK_AUDIT = [
  { id: 1, type: 'skill', name: 'AI Agent开发', trust: 58, status: 'pending' },
  { id: 2, type: 'position', name: '大模型应用工程师', trust: 64, status: 'pending' },
  { id: 3, type: 'skill', name: 'Spring AI', trust: 72, status: 'pending' },
  { id: 4, type: 'skill', name: 'RAG', trust: 45, status: 'pending' },
]

export const handlers = [
  // ── 全景图谱（给队友用）──
  http.get('/api/v1/graph/panorama', () =>
    HttpResponse.json({
      nodes: [
        { id: 'pos-1', label: '算法工程师', type: 'position' },
        { id: 'pos-2', label: '数据分析师', type: 'position' },
        { id: 'skill-1', label: 'Python', type: 'skill' },
        { id: 'skill-2', label: '机器学习', type: 'skill' },
        { id: 'skill-3', label: 'SQL', type: 'skill' },
      ],
      edges: [
        { source: 'pos-1', target: 'skill-1' },
        { source: 'pos-1', target: 'skill-2' },
        { source: 'pos-2', target: 'skill-1' },
        { source: 'pos-2', target: 'skill-3' },
      ],
    }),
  ),

  // ── JD 列表 ──
  http.get('/api/v1/jd/list', () =>
    HttpResponse.json({ items: MOCK_JD_LIST, total: MOCK_JD_LIST.length }),
  ),

  // ── 简历解析 ──
  http.post('/api/v1/resume/parse', () =>
    HttpResponse.json({
      name: '张三',
      skills: [
        { skill: 'Python', category: 'hard_skill', proficiency: '熟悉' },
        { skill: 'Excel', category: 'hard_skill', proficiency: '精通' },
        { skill: 'SQL', category: 'hard_skill', proficiency: '了解' },
        { skill: '沟通能力', category: 'soft_skill', proficiency: '熟悉' },
      ],
      experience_years: 2,
      education: '本科',
    }),
  ),

  // ── 匹配诊断 ──
  http.post('/api/v1/match/diagnose', () =>
    HttpResponse.json(MOCK_MATCH),
  ),

  // ── 质量指标 ──
  http.get('/api/v1/quality/metrics', () =>
    HttpResponse.json(MOCK_QUALITY),
  ),

  // ── 管理后台：数据源列表 ──
  http.get('/api/v1/admin/sources', () =>
    HttpResponse.json({ items: MOCK_SOURCES }),
  ),

  // ── 管理后台：审核队列 ──
  http.get('/api/v1/admin/audit-queue', () =>
    HttpResponse.json({ items: MOCK_AUDIT }),
  ),

  // ── 管理后台：审核批准 ──
  http.post('/api/v1/admin/audit/:id/approve', () =>
    HttpResponse.json({ ok: true }),
  ),

  // ── 管理后台：审核拒绝 ──
  http.post('/api/v1/admin/audit/:id/reject', () =>
    HttpResponse.json({ ok: true }),
  ),

  // ── 管理后台：重置演示数据 ──
  http.post('/api/v1/admin/reset-demo', () =>
    HttpResponse.json({ ok: true }),
  ),

  // ── 岗位搜索 ──
  http.get('/api/v1/positions/search', ({ request }) => {
    const url = new URL(request.url)
    const q = (url.searchParams.get('q') ?? '').toLowerCase()
    const filtered = MOCK_POSITIONS.filter(p => p.toLowerCase().includes(q))
    return HttpResponse.json({ items: filtered.map(p => ({ name: p, category: '技术岗' })), total: filtered.length })
  }),

  // ── 岗位技能要求（双层雷达图）──
  http.get('/api/v1/position/:name/requirements', ({ params }) => {
    const { name } = params
    const requirements = MOCK_POSITION_REQUIREMENTS[name as string] ?? [
      { skill: 'Python', required: 0.8, user: 0.6 },
      { skill: 'SQL', required: 0.7, user: 0.5 },
      { skill: '沟通能力', required: 0.6, user: 0.8 },
      { skill: '问题分析', required: 0.75, user: 0.4 },
    ]
    return HttpResponse.json({ position: name, requirements })
  }),
]
