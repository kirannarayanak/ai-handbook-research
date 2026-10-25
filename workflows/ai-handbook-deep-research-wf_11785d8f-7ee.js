export const meta = {
  name: 'ai-handbook-deep-research',
  description: 'Deep research on 57 AI tools and 60 departments from the corporate AI training handbook, plus additional tools and departments the handbook omits, with adversarial fact-checking, completeness critique and gap-fill',
  phases: [
    { title: 'Research', detail: '10 tool-category researchers and 8 department-cluster researchers, opened web sources only' },
    { title: 'Expand', detail: '5 researchers for tools the handbook omits (two categories each) and 3 for departments it omits (one lens each)' },
    { title: 'Verify', detail: 'one adversarial fact-checker per result, re-opening cited sources' },
    { title: 'Critique', detail: 'completeness critic across all verified results' },
    { title: 'Gap fill', detail: 'targeted research on the gaps the critic found' },
  ],
}

const SOURCE = { type: 'object', properties: { title: { type: 'string' }, url: { type: 'string' } }, required: ['title', 'url'] }
const CONF = { type: 'string', enum: ['high', 'medium', 'low'] }
const TIER = { type: 'string', enum: ['Core', 'Advanced', 'Specialist'] }

const TOOL_ENTRY = { type: 'object', properties: {
  name: { type: 'string' }, vendor: { type: 'string' }, what_it_is: { type: 'string' },
  key_capabilities: { type: 'array', items: { type: 'string' } },
  enterprise_data_handling: { type: 'string' }, licensing_pricing: { type: 'string' }, integrations: { type: 'string' },
  recent_developments: { type: 'string' }, best_fit_departments: { type: 'string' }, training_notes: { type: 'string' },
  caveats: { type: 'string' }, confidence: CONF, sources: { type: 'array', items: SOURCE },
}, required: ['name', 'vendor', 'what_it_is', 'key_capabilities', 'enterprise_data_handling', 'licensing_pricing', 'integrations', 'recent_developments', 'best_fit_departments', 'training_notes', 'caveats', 'confidence', 'sources'] }

const TOOL_GROUP_SCHEMA = { type: 'object', properties: { group: { type: 'string' }, category_overview: { type: 'string' }, tools: { type: 'array', items: TOOL_ENTRY } }, required: ['group', 'category_overview', 'tools'] }
const VERIFIED_TOOL_SCHEMA = { type: 'object', properties: { ...TOOL_GROUP_SCHEMA.properties, verification_notes: { type: 'string' }, removed_or_corrected: { type: 'array', items: { type: 'string' } } }, required: [...TOOL_GROUP_SCHEMA.required, 'verification_notes', 'removed_or_corrected'] }

const DEPT_ENTRY = { type: 'object', properties: {
  num: { type: 'string' }, name: { type: 'string' }, tier: { type: 'string' },
  ai_use_cases: { type: 'array', items: { type: 'string' } },
  capstone_deliverable: { type: 'string' }, data_risks: { type: 'string' }, adoption_kpis: { type: 'string' },
  curriculum_emphasis: { type: 'string' }, tool_fit_commentary: { type: 'string' },
  confidence: CONF, sources: { type: 'array', items: SOURCE },
}, required: ['num', 'name', 'tier', 'ai_use_cases', 'capstone_deliverable', 'data_risks', 'adoption_kpis', 'curriculum_emphasis', 'tool_fit_commentary', 'confidence', 'sources'] }

const DEPT_CLUSTER_SCHEMA = { type: 'object', properties: { cluster: { type: 'string' }, cluster_overview: { type: 'string' }, departments: { type: 'array', items: DEPT_ENTRY } }, required: ['cluster', 'cluster_overview', 'departments'] }
const VERIFIED_DEPT_SCHEMA = { type: 'object', properties: { ...DEPT_CLUSTER_SCHEMA.properties, verification_notes: { type: 'string' }, removed_or_corrected: { type: 'array', items: { type: 'string' } } }, required: [...DEPT_CLUSTER_SCHEMA.required, 'verification_notes', 'removed_or_corrected'] }

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

const CRITIC_SCHEMA = { type: 'object', properties: {
  overall_assessment: { type: 'string' },
  gaps: { type: 'array', items: { type: 'object', properties: { area: { type: 'string' }, description: { type: 'string' }, research_task: { type: 'string' }, priority: { type: 'string', enum: ['high', 'medium', 'low'] } }, required: ['area', 'description', 'research_task', 'priority'] } },
}, required: ['overall_assessment', 'gaps'] }

const GAP_SCHEMA = { type: 'object', properties: { area: { type: 'string' }, findings_markdown: { type: 'string' }, sources: { type: 'array', items: SOURCE }, confidence: CONF }, required: ['area', 'findings_markdown', 'sources', 'confidence'] }

const WEB = 'Load web tools first with ToolSearch using the query "select:WebSearch,WebFetch". Search, then OPEN pages with WebFetch. A search snippet is never a source: only a page you opened counts, and every claim must be supported by an opened page cited in sources with its exact URL.'

const researchToolPrompt = (g) => `You are researching AI tools for an enterprise training reference document. Today is ${args.asOf}.

Your group: "${g}". Read the JSON brief at ${args.briefPath} with the Read tool, find the entry in toolGroups whose group equals "${g}", and research EVERY tool listed in it. The brief lists each tool's handbook departments and a vendor guess that you must verify.

${WEB} For each tool open: the vendor's official product page, its pricing or plans page, its trust/security or data-usage page, and at least one independent 2025-2026 source (news, analyst, documentation, changelog).

For each tool fill every field:
- vendor: the actual company and product family; correct the brief's guess if wrong.
- what_it_is: 2-3 plain sentences: what it does and the surface it lives in (chat app, IDE, inside an existing suite, API).
- key_capabilities: 3-6 concrete capabilities relevant to enterprise knowledge workers.
- enterprise_data_handling: does the business/enterprise tier train on customer data by default; admin controls, SSO, data residency, retention; compliance attestations stated (SOC 2, ISO 27001, HIPAA, FedRAMP). Say WHICH tier each statement applies to.
- licensing_pricing: published list prices per user per month with currency and billing term, or 'contact sales'; whether it is bundled with a suite (e.g. included in a Microsoft 365 or Google Workspace plan) and which plan.
- integrations: the integrations that matter to the handbook departments listed.
- recent_developments: 2-4 notable 2025-2026 changes (new models, renames, launches, acquisitions, discontinuations). Flag renames explicitly, e.g. if a handbook name is now marketed under another brand.
- best_fit_departments: which handbook departments listed for this tool fit best and why; name any listed department where the fit is weak.
- training_notes: what a learner must master to use it safely and well, and suggested hours within the handbook bands (Core 6-10, Advanced 12-20, Specialist 20-40+).
- caveats: limitations, accuracy risks, licensing gotchas, regional availability.
- confidence: high only if every statement is backed by an opened page.
- sources: every page you opened and relied on.

Also write category_overview: 3-5 sentences on how the tools in this group relate, overlap and compete, and what enterprises usually standardise on.

Keep each tool entry under 350 words. Return only the structured output.`

const verifyToolPrompt = (g, r) => `You are an adversarial fact-checker. Today is ${args.asOf}. Below is a research result on the AI tool group "${g}" produced by another agent. Try to REFUTE it, efficiently.

${WEB} For every tool entry: open the vendor's current pricing or plans page and trust/data-usage page and compare them with the licensing_pricing and enterprise_data_handling claims; open two further cited sources per tool, chosen where the claims look most surprising, and confirm they exist and support what is attributed to them; check vendor and product names are current (renames, discontinued products).

Rules:
- A claim no opened page supports is removed, or rewritten as 'not verified'.
- A wrong price, tier, date or product name is corrected, with the correcting source added to sources.
- A dead or irrelevant URL you encountered is removed from sources.
- Add no new claims beyond corrections. Keep the text concise.
- Set confidence per tool honestly after your checks.
- removed_or_corrected: one line per removal or correction (tool, what, why).
- verification_notes: 2-4 sentences on overall reliability.

Return the full corrected result in the same structure, with every tool still present.

RESEARCH RESULT:
${JSON.stringify(r)}`

const researchDeptPrompt = (c) => `You are researching how specific corporate departments use AI tools in practice, for an enterprise training reference document. Today is ${args.asOf}.

Your cluster: "${c}". Read the JSON brief at ${args.briefPath} with the Read tool, find the entry in deptClusters whose cluster equals "${c}", and research EVERY department in it. The brief gives each department's tier (Core, Advanced or Specialist), its handbook tool list and a one-line workplace application.

${WEB} For each department open at least 2 credible sources published 2024-2026: vendor case studies, consulting or analyst reports, professional-body or regulator guidance, practitioner articles.

For each department fill:
- ai_use_cases: 4-6 concrete real-world AI use cases for this function (task, tool type, outcome), each ending with a source marker like [1] that maps to the sources list order.
- capstone_deliverable: one specific, assessable capstone that fits the handbook's template (one role-specific deliverable, validated sources, documented prompts and time saved) and the department's tier hours.
- data_risks: the sensitive data categories this function handles and the resulting rules for AI use; name regulatory hooks where relevant (GDPR, SOX, HIPAA, PCI DSS, legal privilege, material non-public information, employment law).
- adoption_kpis: 3-5 measurable indicators a manager could track.
- curriculum_emphasis: where the training hours should go given the tier; name the 2-4 handbook tools to prioritise and why.
- tool_fit_commentary: does the handbook's tool list fit this department? Name any listed tool that is a weak fit and any widely used tool the handbook omits, with a source.
- confidence: high only if every statement is backed by an opened page.
- sources: every page you opened and relied on.

Also write cluster_overview: 3-5 sentences on shared patterns, shared risks, and where the cluster's departments should train together.

Keep each department entry under 300 words. Return only the structured output.`

const verifyDeptPrompt = (c, r) => `You are an adversarial fact-checker. Today is ${args.asOf}. Below is a research result on the department cluster "${c}" produced by another agent. Try to REFUTE it, efficiently.

${WEB} For every department: open at least two of its cited sources, chosen where the claims look most surprising, and confirm they exist and support the use cases and claims attributed to them; check regulatory references are correct (right regulation, right scope); check any named tool actually offers what is claimed.

Rules:
- A claim no opened page supports is removed, or rewritten as 'not verified'.
- A wrong regulation, product capability or statistic is corrected, with the correcting source added.
- A dead or irrelevant URL you encountered is removed from sources and the use-case markers renumbered.
- Add no new claims beyond corrections. Keep the text concise.
- Set confidence per department honestly after your checks.
- removed_or_corrected: one line per removal or correction (department, what, why).
- verification_notes: 2-4 sentences on overall reliability.

Return the full corrected result in the same structure, with every department still present.

RESEARCH RESULT:
${JSON.stringify(r)}`

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

phase('Research')
log('Starting 10 tool-group and 8 department-cluster researchers (finished ones replay from cache), plus 5 additional-tools and 3 additional-departments researchers')

const [toolResults, deptResults, addToolResults, addDeptResults] = await parallel([
  () => pipeline(args.toolGroupNames,
    g => agent(researchToolPrompt(g), { label: `research tools: ${g}`, phase: 'Research', schema: TOOL_GROUP_SCHEMA }),
    (r, g) => r ? agent(verifyToolPrompt(g, r), { label: `verify tools: ${g}`, phase: 'Verify', schema: VERIFIED_TOOL_SCHEMA }).then(v => v || fallbackVerified(r, 'verifier returned nothing')) : null),
  () => pipeline(args.deptClusterNames,
    c => agent(researchDeptPrompt(c), { label: `research depts: ${c}`, phase: 'Research', schema: DEPT_CLUSTER_SCHEMA }),
    (r, c) => r ? agent(verifyDeptPrompt(c, r), { label: `verify depts: ${c}`, phase: 'Verify', schema: VERIFIED_DEPT_SCHEMA }).then(v => v || fallbackVerified(r, 'verifier returned nothing')) : null),
  () => pipeline(TOOL_PAIRS,
    cats => agent(addToolsPrompt(cats), { label: `more tools: ${cats.join(' + ')}`, phase: 'Expand', schema: ADD_TOOLS_SCHEMA }),
    (r, cats) => r ? agent(verifyAddToolsPrompt(cats, r), { label: `verify more tools: ${cats.join(' + ')}`, phase: 'Verify', schema: VERIFIED_ADD_TOOLS_SCHEMA }).then(v => v || fallbackVerified(r, 'verifier returned nothing')) : null),
  () => pipeline(LENSES,
    lens => agent(addDeptsPrompt(lens), { label: `more depts: ${lens.name}`, phase: 'Expand', schema: ADD_DEPTS_SCHEMA }),
    (r, lens) => r ? agent(verifyAddDeptsPrompt(lens, r), { label: `verify more depts: ${lens.name}`, phase: 'Verify', schema: VERIFIED_ADD_DEPTS_SCHEMA }).then(v => v || fallbackVerified(r, 'verifier returned nothing')) : null),
])

const tools = (toolResults || []).filter(Boolean)
const depts = (deptResults || []).filter(Boolean)
const addTools = (addToolResults || []).filter(Boolean)
const addDepts = (addDeptResults || []).filter(Boolean)
const toolCount = tools.reduce((s, g) => s + g.tools.length, 0)
const deptCount = depts.reduce((s, c) => s + c.departments.length, 0)
log(`Verified ${toolCount} tools across ${tools.length} groups and ${deptCount} departments across ${depts.length} clusters`)
const missingToolGroups = args.toolGroupNames.filter(g => !tools.some(t => t.group === g))
const missingDeptClusters = args.deptClusterNames.filter(c => !depts.some(d => d.cluster === c))
const missingToolPairs = TOOL_PAIRS.filter(p => !addTools.some(a => a.categories && a.categories.join('|') === p.join('|'))).map(p => p.join(' + '))
const missingLenses = LENSES.filter(l => !addDepts.some(a => a.lens === l.name)).map(l => l.name)
if (missingToolGroups.length) log(`DROPPED tool groups (agent failed): ${missingToolGroups.join('; ')}`)
if (missingDeptClusters.length) log(`DROPPED department clusters (agent failed): ${missingDeptClusters.join('; ')}`)
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

phase('Critique')
const condensed = {
  tool_groups: tools.map(g => ({ group: g.group, overview: g.category_overview, verification_notes: g.verification_notes, tools: g.tools.map(t => ({ name: t.name, vendor: t.vendor, confidence: t.confidence, licensing_pricing: t.licensing_pricing, enterprise_data_handling: t.enterprise_data_handling.slice(0, 300), recent_developments: t.recent_developments.slice(0, 300), caveats: t.caveats.slice(0, 200), source_count: t.sources.length })) })),
  dept_clusters: depts.map(c => ({ cluster: c.cluster, overview: c.cluster_overview, verification_notes: c.verification_notes, departments: c.departments.map(d => ({ num: d.num, name: d.name, tier: d.tier, confidence: d.confidence, tool_fit_commentary: d.tool_fit_commentary, data_risks: d.data_risks.slice(0, 200), source_count: d.sources.length })) })),
  additional_tools: mergedTools.map(t => ({ name: t.name, vendor: t.vendor, category: t.category, confidence: t.confidence, overlaps_with: t.overlaps_with })),
  additional_departments: mergedDepts.map(d => ({ name: d.name, tier: d.suggested_tier, confidence: d.confidence, why_missing: d.why_missing })),
  dropped: { tool_groups: missingToolGroups, dept_clusters: missingDeptClusters, additional_tool_pairs: missingToolPairs, additional_dept_lenses: missingLenses },
}
const critic = await agent(`You are the completeness critic for a deep-research document that expands a corporate AI training handbook covering 57 AI tools and 60 departments, and proposes additional tools and departments. Today is ${args.asOf}. Below is a condensed view of the verified research so far.

Ask: what is missing that a CHRO, CIO or L&D director reading this document would expect? Consider: tools or departments with low confidence or few sources; cross-cutting topics not yet covered (EU AI Act and other AI regulation obligations for employers in 2026, data residency and enterprise licensing cost models for the six horizontal tools, overlap and redundancy between tools that an organisation should rationalise, vendor lock-in, accessibility, change management and adoption research, measuring training ROI, hallucination and verification practice, prompt-injection and shadow-AI risk); any handbook tool name that is now outdated; any department cluster where use cases look generic rather than specific; obvious additional tools or departments the expansion missed.

Return overall_assessment (4-6 sentences) and at most 6 gaps, each with a self-contained research_task that a researcher with web access can complete in one sitting and a priority. Order by priority.

CONDENSED RESEARCH:
${JSON.stringify(condensed)}`, { label: 'completeness critic', phase: 'Critique', schema: CRITIC_SCHEMA })

const gaps = critic ? critic.gaps.slice(0, 6) : []
log(`Critic found ${gaps.length} gaps` + (critic && critic.gaps.length > 6 ? ` (${critic.gaps.length - 6} lower-priority gaps dropped)` : ''))

phase('Gap fill')
const gapFills = (await parallel(gaps.map(gap => () => agent(`You are filling a gap in a deep-research document that expands a corporate AI training handbook (57 AI tools, 60 departments). Today is ${args.asOf}.

Gap area: ${gap.area}
Why it matters: ${gap.description}
Your task: ${gap.research_task}

${WEB} Open at least 3 credible sources published 2024-2026 (regulators, vendors' official pages, analyst or consulting reports, professional bodies, reputable press).

Return findings_markdown: 150-350 words of markdown (short paragraphs, bullets or one small pipe table; no headings), every factual claim followed by a [n] marker that maps to the sources list order; concrete numbers, dates and names rather than generalities. Set confidence honestly.`, { label: `gap: ${gap.area}`, phase: 'Gap fill', schema: GAP_SCHEMA })))).filter(Boolean)

log(`Gap fill complete: ${gapFills.length} of ${gaps.length} gaps researched`)

return { toolGroups: tools, deptClusters: depts, additionalTools: { runs: addTools, merged: mergedTools }, additionalDepartments: { runs: addDepts, merged: mergedDepts }, critic, gapFills, dropped: { toolGroups: missingToolGroups, deptClusters: missingDeptClusters, additionalToolPairs: missingToolPairs, additionalDeptLenses: missingLenses } }