export const meta = {
  name: 'ai-handbook-expansion',
  description: 'Find enterprise AI tools and departments the corporate AI training handbook omits, with adversarial fact-checking',
  phases: [
    { title: 'Expand', detail: '5 researchers for omitted tools (two categories each) and 3 for omitted departments (one lens each)' },
    { title: 'Verify', detail: 'one adversarial fact-checker per result' },
  ],
}

const SOURCE = { type: 'object', properties: { title: { type: 'string' }, url: { type: 'string' } }, required: ['title', 'url'] }
const CONF = { type: 'string', enum: ['high', 'medium', 'low'] }
const TIER = { type: 'string', enum: ['Core', 'Advanced', 'Specialist'] }

const ADD_TOOL = { type: 'object', properties: {
  name: { type: 'string' }, vendor: { type: 'string' }, category: { type: 'string' }, what_it_is: { type: 'string' }, why_include: { type: 'string' },
  suggested_departments: { type: 'array', items: { type: 'string' } }, suggested_tier: TIER, overlaps_with: { type: 'string' }, enterprise_data_note: { type: 'string' },
  confidence: CONF, sources: { type: 'array', items: SOURCE },
}, required: ['name', 'vendor', 'category', 'what_it_is', 'why_include', 'suggested_departments', 'suggested_tier', 'overlaps_with', 'enterprise_data_note', 'confidence', 'sources'] }
const ADD_TOOLS_SCHEMA = { type: 'object', properties: { categories: { type: 'array', items: { type: 'string' } }, overview: { type: 'string' }, candidates: { type: 'array', items: ADD_TOOL } }, required: ['categories', 'overview', 'candidates'] }
const VERIFIED_ADD_TOOLS_SCHEMA = { type: 'object', properties: { ...ADD_TOOLS_SCHEMA.properties, verification_notes: { type: 'string' }, removed_or_corrected: { type: 'array', items: { type: 'string' } } }, required: [...ADD_TOOLS_SCHEMA.required, 'verification_notes', 'removed_or_corrected'] }

const ADD_DEPT = { type: 'object', properties: {
  name: { type: 'string' }, why_missing: { type: 'string' }, typical_org_types: { type: 'string' }, suggested_tier: TIER,
  recommended_tools: { type: 'array', items: { type: 'string' } }, workplace_application: { type: 'string' }, ai_use_evidence: { type: 'string' }, data_risks: { type: 'string' },
  confidence: CONF, sources: { type: 'array', items: SOURCE },
}, required: ['name', 'why_missing', 'typical_org_types', 'suggested_tier', 'recommended_tools', 'workplace_application', 'ai_use_evidence', 'data_risks', 'confidence', 'sources'] }
const ADD_DEPTS_SCHEMA = { type: 'object', properties: { lens: { type: 'string' }, overview: { type: 'string' }, candidates: { type: 'array', items: ADD_DEPT } }, required: ['lens', 'overview', 'candidates'] }
const VERIFIED_ADD_DEPTS_SCHEMA = { type: 'object', properties: { ...ADD_DEPTS_SCHEMA.properties, verification_notes: { type: 'string' }, removed_or_corrected: { type: 'array', items: { type: 'string' } } }, required: [...ADD_DEPTS_SCHEMA.required, 'verification_notes', 'removed_or_corrected'] }

const WEB = 'Load web tools first with ToolSearch using the query "select:WebSearch,WebFetch". Search, then OPEN pages with WebFetch. A search snippet is never a source: only a page you opened counts, and every claim must be supported by an opened page cited in sources with its exact URL.'

const deptList = args.handbookDepartments.join('; ')
const addToolsPrompt = (cats) => `You are extending an enterprise AI training handbook that currently names 57 tools. Today is ${args.asOf}.

Your categories: ${cats.join(' and ')}. The handbook's existing 57 tools across all categories are: ${args.handbookTools.join('; ')}.

Task: identify the enterprise AI tools in your two categories that large organisations widely adopted in 2025-2026 but that are absent from that list. Prioritise tools that (a) appear in a 2025 or 2026 analyst evaluation (Gartner Magic Quadrant or Market Guide, Forrester Wave, IDC MarketScape, G2 Enterprise Grid), (b) publish enterprise customer counts or named large-enterprise customers, or (c) are AI capabilities now built into platforms the handbook's departments already run (ERP, CRM, HRIS, ITSM, contact centre, design or productivity suites). Give at most 8 candidates per category, strongest first. Exclude consumer-only tools and anything already on the list under another name; note such renames in the overview instead.

${WEB} For each candidate open the vendor's official product page and at least one independent 2025-2026 source.

For each candidate fill: name; vendor; category (one of your two); what_it_is (1-2 sentences, including where it lives); why_include (the adoption evidence, with specifics such as the analyst report and year, customer counts or named customers); suggested_departments (handbook department numbers and names, chosen from: ${deptList}); suggested_tier (per the handbook: Core 6-10 h, Advanced 12-20 h, Specialist 20-40+ h); overlaps_with (the handbook tool it most overlaps, or 'none'); enterprise_data_note (one sentence on the enterprise tier's training and data posture if the vendor states it); confidence (high only if every statement is backed by an opened page); sources (every page opened and relied on).

Also write overview: 3-4 sentences on what the handbook's coverage of these two categories misses, and any handbook tool names in them that are now outdated.

Keep each candidate under 120 words. Return only the structured output.`

const verifyAddToolsPrompt = (cats, r) => `You are an adversarial fact-checker. Today is ${args.asOf}. Below is a list of AI tools another agent proposes adding to an enterprise training handbook (categories: ${cats.join(' and ')}). Try to REFUTE each candidate, efficiently.

The handbook's existing 57 tools are: ${args.handbookTools.join('; ')}.

${WEB} For every candidate: open the vendor page cited and one independent source, confirm the product exists under that name today and that the adoption evidence in why_include is real (the named analyst report, customer count or customer names); check it is not one of the 57 under another name.

Rules:
- A candidate whose adoption evidence no opened page supports is kept only if you can replace the evidence with a verified one; otherwise remove it and record why.
- A duplicate of a handbook tool is removed and recorded.
- Correct names, vendors and tiers where wrong, adding the correcting source.
- Add no new candidates. Keep text concise.
- Set confidence per candidate honestly after your checks.
- removed_or_corrected: one line per removal or correction.
- verification_notes: 2-4 sentences on overall reliability.

Return the full corrected result in the same structure.

RESEARCH RESULT:
${JSON.stringify(r)}`

const addDeptsPrompt = (lens) => `You are extending an enterprise AI training handbook that currently covers 60 departments: ${deptList}. Today is ${args.asOf}.

Your lens: ${lens.name}. ${lens.brief}

Task: identify up to 12 departments or functions that large organisations commonly have, that this lens surfaces, and that the 60 do not cover. A function already folded into one of the 60 under a different name does not count; mention such near-misses in the overview instead. Each candidate must have documented AI use in that function in 2024-2026.

${WEB} For each candidate open at least 2 credible sources (vendor case studies, analyst or consulting reports, professional bodies, regulators, reputable press) that show AI use in that function.

For each candidate fill: name (in the handbook's naming style, e.g. 'Corporate Communications & Public Relations'); why_missing (what the 60 do not cover, one or two sentences); typical_org_types (all large companies, or which industries); suggested_tier (Core 6-10 h, Advanced 12-20 h, Specialist 20-40+ h); recommended_tools (4-6 tools: prefer the handbook's 57, which are ${args.handbookTools.join('; ')}; add a specialist tool only where the function needs one, naming the vendor); workplace_application (one line in the handbook's style: three comma-separated use cases); ai_use_evidence (2-3 sentences with [n] markers to the sources list order); data_risks (one sentence on the sensitive data this function handles); confidence (high only if every statement is backed by an opened page); sources (every page opened and relied on).

Also write overview: 3-4 sentences on the pattern of what the handbook's 60 miss under this lens, including near-misses.

Keep each candidate under 150 words. Return only the structured output.`

const verifyAddDeptsPrompt = (lens, r) => `You are an adversarial fact-checker. Today is ${args.asOf}. Below is a list of departments another agent proposes adding to an enterprise AI training handbook (lens: ${lens.name}). Try to REFUTE each candidate, efficiently.

The handbook's existing 60 departments are: ${deptList}.

${WEB} For every candidate: open at least one cited source and confirm it shows AI use in that function; check the candidate is genuinely absent from the 60 rather than a renamed duplicate; check the recommended tools exist and fit.

Rules:
- A candidate whose AI-use evidence no opened page supports is removed and recorded.
- A duplicate of one of the 60 departments is removed and recorded.
- Correct names, tiers and tools where wrong, adding the correcting source.
- Add no new candidates. Keep text concise.
- Set confidence per candidate honestly after your checks.
- removed_or_corrected: one line per removal or correction.
- verification_notes: 2-4 sentences on overall reliability.

Return the full corrected result in the same structure.

RESEARCH RESULT:
${JSON.stringify(r)}`

const fallbackVerified = (r, why) => ({ ...r, verification_notes: `Fact-check stage did not complete (${why}); content is as researched and should be read as unverified.`, removed_or_corrected: [] })

const TOOL_PAIRS = []
for (let i = 0; i < args.toolGroupNames.length; i += 2) TOOL_PAIRS.push(args.toolGroupNames.slice(i, i + 2))

const LENSES = [
  { name: 'Core corporate and shared-service functions', brief: 'Think of the functions every large company staffs that are not among the 60: for example corporate communications and public relations, internal communications, government and public affairs, legal operations, corporate real estate, executive assistants and administration, knowledge management, the data privacy office, pricing, sales enablement, product marketing, content, editorial and localisation, events, corporate and physical security. Treat these as prompts, not a list to copy: include only what you can evidence and what the 60 truly lack.' },
  { name: 'Industry and operational functions', brief: 'Think of line-of-business functions in manufacturing, retail, healthcare and pharma, financial services, insurance, energy and utilities, transport and logistics, construction, hospitality, telecom and the public sector: for example production and plant maintenance, hardware R&D and product engineering, quality laboratories, field service, store operations, e-commerce and merchandising, clinical and regulatory affairs, underwriting and claims, credit risk and fraud, trade compliance and customs, grid operations, fleet. Treat these as prompts, not a list to copy: include only what you can evidence and what the 60 truly lack.' },
  { name: 'AI-era governance and enablement functions', brief: 'Think of functions that have emerged or grown because of AI adoption itself: for example an AI governance or responsible-AI office, an AI centre of excellence or enablement team, an automation centre of excellence, prompt and agent operations, data governance and stewardship, model risk management, digital workplace and employee experience, revenue enablement, developer experience and platform teams, customer insights and analytics. Check carefully against department 51 (AI, Machine Learning & Automation) and 49 (Data Engineering) so you do not duplicate them. Treat these as prompts, not a list to copy: include only what you can evidence and what the 60 truly lack.' },
]

phase('Expand')
log('Starting 5 additional-tools and 3 additional-departments researchers')
const [addToolResults, addDeptResults] = await parallel([
  () => pipeline(TOOL_PAIRS,
    cats => agent(addToolsPrompt(cats), { label: `more tools: ${cats.join(' + ')}`, phase: 'Expand', schema: ADD_TOOLS_SCHEMA }),
    (r, cats) => r ? agent(verifyAddToolsPrompt(cats, r), { label: `verify more tools: ${cats.join(' + ')}`, phase: 'Verify', schema: VERIFIED_ADD_TOOLS_SCHEMA }).then(v => v || fallbackVerified(r, 'verifier returned nothing')) : null),
  () => pipeline(LENSES,
    lens => agent(addDeptsPrompt(lens), { label: `more depts: ${lens.name}`, phase: 'Expand', schema: ADD_DEPTS_SCHEMA }),
    (r, lens) => r ? agent(verifyAddDeptsPrompt(lens, r), { label: `verify more depts: ${lens.name}`, phase: 'Verify', schema: VERIFIED_ADD_DEPTS_SCHEMA }).then(v => v || fallbackVerified(r, 'verifier returned nothing')) : null),
])

const addTools = (addToolResults || []).filter(Boolean)
const addDepts = (addDeptResults || []).filter(Boolean)
const missingToolPairs = TOOL_PAIRS.filter(p => !addTools.some(a => a.categories && a.categories.join('|') === p.join('|'))).map(p => p.join(' + '))
const missingLenses = LENSES.filter(l => !addDepts.some(a => a.lens === l.name)).map(l => l.name)
if (addTools.length < TOOL_PAIRS.length) log(`DROPPED additional-tools researchers: ${TOOL_PAIRS.length - addTools.length} of ${TOOL_PAIRS.length} failed`)
if (missingLenses.length) log(`DROPPED additional-departments lenses (agent failed): ${missingLenses.join('; ')}`)

const norm = s => String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, '')
const handbookToolKeys = new Set(args.handbookTools.map(norm))
const handbookDeptKeys = new Set(args.handbookDepartments.map(d => norm(d.replace(/^\d+\s*/, ''))))
const mergedTools = []
const seenTools = new Map()
for (const r of addTools) for (const c of r.candidates || []) {
  const k = norm(c.name)
  if (!k || handbookToolKeys.has(k)) continue
  if (seenTools.has(k)) { const prev = seenTools.get(k); prev.suggested_departments = Array.from(new Set([...prev.suggested_departments, ...c.suggested_departments])); continue }
  seenTools.set(k, c); mergedTools.push(c)
}
const mergedDepts = []
const seenDepts = new Map()
for (const r of addDepts) for (const c of r.candidates || []) {
  const k = norm(c.name)
  if (!k || handbookDeptKeys.has(k) || seenDepts.has(k)) continue
  seenDepts.set(k, c); mergedDepts.push(c)
}
log(`Additional tools after dedup: ${mergedTools.length}; additional departments after dedup: ${mergedDepts.length}`)

return { additionalTools: { runs: addTools, merged: mergedTools }, additionalDepartments: { runs: addDepts, merged: mergedDepts }, dropped: { additionalToolPairs: missingToolPairs, additionalDeptLenses: missingLenses } }