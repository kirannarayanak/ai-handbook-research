export const meta = {
  name: 'ai-handbook-more-expansion',
  description: 'Second pass: find more enterprise AI tools or departments the handbook and the first expansion missed, with adversarial fact-checking',
  phases: [
    { title: 'Expand', detail: 'one researcher per lens' },
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

const WEB = `Web access: load WebSearch with ToolSearch using the query "select:WebSearch" and use it to find candidate pages. The WebFetch tool does NOT work in this environment (DNS is unavailable). To OPEN a page, run with the Bash tool: python3 -I ${args.fetchScript} <url> [max_chars] [offset]. It prints "OPENED <url>" followed by the page text (rerun with an offset to read further), or "FAILED" when the page could not be opened. Only a page that printed OPENED counts as a source; a search snippet is never a source, and every claim must be supported by an opened page cited in sources with its exact URL. A page that FAILED (for example a 403 bot block) must not be cited: find the fact on another page or label the claim 'not verified'.`
const STD = { model: 'sonnet', effort: 'medium' }

const deptList = args.handbookDepartments.join('; ')
const excludedTools = [...args.handbookTools, ...args.excludeTools].join('; ')
const excludedDepts = [...args.handbookDepartments, ...args.excludeDepts].join('; ')

const TOOL_LENSES = [
  { name: 'HR, talent, learning and workplace AI', brief: 'HRIS and talent-suite AI not yet listed (for example SAP SuccessFactors Joule agents are covered under SAP Joule, but think of Oracle HCM, UKG, ADP, Dayforce, Eightfold, Phenom, HireVue, Paradox, Lattice, Culture Amp, Leapsome), learning platforms with AI (Docebo, Cornerstone, Degreed, Sana Learn, LinkedIn Learning AI coaching, Articulate AI Assistant), AI video and avatar tools for training (Synthesia, HeyGen, Colossyan), and employee-experience or digital-workplace AI (Moveworks, Leena AI, Simpplr, Firstup).' },
  { name: 'Finance, accounting, procurement and supply chain AI', brief: 'Close and consolidation platforms with AI (BlackLine, FloQast, Workiva, OneStream, Anaplan, Pigment, Planful, Vena), AP and spend tools (Coupa, Ivalua, GEP, Zip, Ramp, Brex, Tipalti, Bill), treasury and tax (Kyriba, Avalara, Vertex, Bloomberg Tax AI), audit analytics (MindBridge, DataSnipper, Caseware), and supply-chain planning platforms (Kinaxis Maestro, o9, Blue Yonder, SAP IBP is covered, project44, FourKites, Coupa Supply Chain).' },
  { name: 'Knowledge, documents, meetings, translation and content operations AI', brief: 'Enterprise search and knowledge (Glean is already listed; think of Coveo, Guru, Sinequa, Elastic AI, Microsoft Copilot connectors are covered), intelligent document processing (UiPath Document Understanding is partly covered; think of ABBYY, Hyperscience, Rossum, Instabase, Google Document AI, Azure Document Intelligence), meeting and note-taking AI (Otter, Fireflies, Read AI, Gong is covered, Microsoft Teams Copilot is covered), translation and localisation (DeepL, Smartling, Phrase, Lokalise, RWS Language Weaver), and content operations (Jasper, Copy.ai, Contentful AI, Acrolinx, Sitecore, Optimizely Opal).' },
  { name: 'Agent builders, automation, low-code and voice AI', brief: 'Agent-building and orchestration platforms not yet listed (Microsoft Copilot Studio and Agent 365, ServiceNow AI Agent Studio and AI Control Tower may be covered under their platform entries; think of Salesforce Agentforce Builder is covered, Google Agentspace or Gemini Enterprise is covered, Workato, Zapier Agents, n8n, Make, Automation Anywhere, Appian, Pega GenAI Blueprint, OutSystems Mentor, Mendix, Retool), conversational and voice AI (Kore.ai, Cognigy, Sierra, Decagon, PolyAI, ElevenLabs, Deepgram), and AI gateways or LLM ops (LangChain and LangSmith, Portkey, Kong AI Gateway, Arize, Weights & Biases, Galileo).' },
  { name: 'Marketing, creative, commerce and customer-data AI', brief: 'Marketing clouds and CDPs with AI beyond those listed (Adobe GenStudio and AEP are listed; think of Braze, Klaviyo, Iterable, Marketo Engage, Salesforce Marketing Cloud Next is partly covered, Sprinklr, Sprout Social, Hootsuite OwlyGPT, Brandwatch, Semrush and Ahrefs AI, Seventh Sense), creative and video (Runway, Midjourney for business, Pika, Descript, Captions, Veo via Gemini is covered, Sora in ChatGPT), commerce and personalisation (Shopify Sidekick and Magic, Salesforce Commerce, Bloomreach, Algolia, Dynamic Yield, Amazon Rufus for sellers), and customer-data platforms (Segment, Tealium, Treasure Data, Amperity).' },
  { name: 'Engineering, IT operations, identity and risk AI (second pass)', brief: 'Developer and platform tools not yet listed (OpenAI Codex, Devin, GitLab Duo, Tabnine, JetBrains are listed; think of Sourcegraph Amp, Replit, Lovable, Vercel v0, Warp, Snyk and Semgrep AI, Harness AI, Atlassian Rovo Dev, PagerDuty AI, incident.io, Rootly, BigPanda, Moogsoft), IT and asset management (Freshservice Freddy, Jira Service Management Virtual Service Agent, BMC Helix, Ivanti Neurons, Nexthink, Flexera, Zylo for SaaS management), identity and security beyond the SIEMs listed (Okta AI, SailPoint, CyberArk CORA, Zscaler, Netskope, Abnormal, Wiz, Vanta, Drata), and FinOps (CloudZero, Apptio Cloudability, Vantage).' },
]

const DEPT_LENSES = [
  { name: 'Commercial, brand and customer-adjacent functions (second pass)', brief: 'Think of commercial functions the 60 and the first-pass additions still lack: brand management, product marketing, content and editorial, SEO and answer-engine optimisation, social media and community management, events and field marketing, customer education and training services, localisation and translation, channel and partner marketing, customer insights and voice-of-customer analytics (check against 33 Market Research and 38 Customer Experience), loyalty and CRM marketing, e-commerce operations (Merchandising & Store Operations is already added), sales compensation and deal desk (check 30 Sales Operations). Include only what you can evidence and what the existing list truly lacks.' },
  { name: 'Technology, data and engineering-adjacent functions (second pass)', brief: 'Think of technical functions still missing: hardware and product engineering R&D, embedded and firmware engineering, technical writing and documentation, UX writing and content design, release and configuration management, developer experience and platform engineering (check 43 and 44), FinOps and cloud financial management, IT asset and SaaS management, identity and access management (check 45 and 47), privacy engineering and the data protection office (check 48), records and information management, GIS and geospatial, scientific computing and research IT, telecom network engineering. Include only what you can evidence and what the existing list truly lacks.' },
  { name: 'Industry line-of-business functions (second pass)', brief: 'The first pass added manufacturing and plant maintenance, insurance underwriting and claims, payments fraud and credit risk, clinical and regulatory affairs, field service, trade compliance, merchandising and store operations, QC laboratories, and grid operations. Now think of what remains: hospital and clinical operations (nursing, revenue cycle, medical coding), pharmacovigilance and medical affairs, medical writing, wealth management and advisory, retail and commercial banking operations, anti-money-laundering and KYC, actuarial, loan origination and mortgage operations, airline and rail operations, warehouse and fulfilment operations (check 60), construction project controls and estimating, hospitality and guest services, media newsroom and content production, higher-education admissions and student services, public-sector casework and benefits administration, utilities customer billing, oil and gas subsurface and asset integrity, automotive dealer and aftersales, telecom network operations centre. Include only what you can evidence and what the existing list truly lacks.' },
  { name: 'People, governance and enterprise-support functions (second pass)', brief: 'The first pass added corporate communications, government affairs, corporate real estate, pricing, executive administration, AI governance, model risk, data governance and revenue enablement. Now think of: internal communications and employee engagement (check 11 and 17), employer brand and recruitment marketing (check 12), HR shared services and the people helpdesk (check 11 and 55), payroll shared services (check 14), global mobility and immigration, workforce planning (check 16), employee relations and investigations (check 09), legal operations (check 06), corporate secretariat is covered (04), philanthropy and corporate foundation (check 10), travel and expense management, physical and corporate security, crisis management and communications (check 59), enterprise risk management (check 05 and 48), insurance and claims for the company itself, environmental permitting, translation and interpreting services, library and research services, facilities helpdesk (check 18). Include only what you can evidence and what the existing list truly lacks.' },
]

const addToolsPrompt = (lens) => `You are extending an enterprise AI training handbook. Today is ${args.asOf}.

Your lens: ${lens.name}. ${lens.brief}

ALREADY COVERED (do not propose any of these, under any name): ${excludedTools}.

Task: identify up to 10 enterprise AI tools or AI capabilities under your lens that large organisations widely adopted in 2025-2026 and that are absent from the covered list. Prioritise tools that (a) appear in a 2025 or 2026 analyst evaluation (Gartner Magic Quadrant or Market Guide, Forrester Wave, IDC MarketScape, G2 Enterprise Grid), (b) publish enterprise customer counts or named large-enterprise customers, or (c) are AI capabilities now built into platforms the handbook's departments already run. Strongest first. Exclude consumer-only tools. If a tool in your brief turns out to be covered under another name, say so in the overview and skip it.

${WEB} For each candidate open the vendor's official product page and at least one independent 2025-2026 source.

For each candidate fill: name; vendor; category (set to "${lens.name}"); what_it_is (1-2 sentences, including where it lives); why_include (the adoption evidence, with specifics such as the analyst report and year, customer counts or named customers); suggested_departments (handbook department numbers and names, chosen from: ${deptList}; you may also name one of these added departments: ${args.excludeDepts.join('; ')}); suggested_tier (Core 6-10 h, Advanced 12-20 h, Specialist 20-40+ h); overlaps_with (the covered tool it most overlaps, or 'none'); enterprise_data_note (one sentence on the enterprise tier's training and data posture if the vendor states it); confidence (high only if every statement is backed by an opened page); sources (every page opened and relied on).

Also write overview: 3-4 sentences on what the handbook misses under this lens and any near-misses you skipped. Set categories to exactly ${JSON.stringify([lens.name])}.

Keep each candidate under 120 words. Return only the structured output.`

const verifyAddToolsPrompt = (lens, r) => `You are an adversarial fact-checker. Today is ${args.asOf}. Below is a list of AI tools another agent proposes adding to an enterprise training handbook (lens: ${lens.name}). Try to REFUTE each candidate, efficiently.

ALREADY COVERED tools (a candidate that is one of these under another name must be removed): ${excludedTools}.

${WEB} For every candidate: open the vendor page cited and one independent source, confirm the product exists under that name today and that the adoption evidence in why_include is real (the named analyst report, customer count or customer names); check it is not a covered tool under another name.

Rules:
- A candidate whose adoption evidence no opened page supports is kept only if you can replace the evidence with a verified one; otherwise remove it and record why.
- A duplicate of a covered tool is removed and recorded.
- Correct names, vendors and tiers where wrong, adding the correcting source.
- Add no new candidates. Keep text concise.
- Set confidence per candidate honestly after your checks.
- removed_or_corrected: one line per removal or correction.
- verification_notes: 2-4 sentences on overall reliability.

Return the full corrected result in the same structure, keeping categories exactly as given.

RESEARCH RESULT:
${JSON.stringify(r)}`

const addDeptsPrompt = (lens) => `You are extending an enterprise AI training handbook. Today is ${args.asOf}.

ALREADY COVERED departments (do not propose any of these, under any name): ${excludedDepts}.

Your lens: ${lens.name}. ${lens.brief}

Task: identify up to 12 departments or functions that large organisations commonly have, that this lens surfaces, and that the covered list does not include. A function already folded into a covered department under a different name does not count; mention such near-misses in the overview instead. Each candidate must have documented AI use in that function in 2024-2026.

${WEB} For each candidate open at least 2 credible sources (vendor case studies, analyst or consulting reports, professional bodies, regulators, reputable press) that show AI use in that function.

For each candidate fill: name (in the handbook's naming style, e.g. 'Corporate Communications & Public Relations'); why_missing (what the covered list does not cover, one or two sentences); typical_org_types (all large companies, or which industries); suggested_tier (Core 6-10 h, Advanced 12-20 h, Specialist 20-40+ h); recommended_tools (4-6 tools: prefer the handbook's 57, which are ${args.handbookTools.join('; ')}; add a specialist tool only where the function needs one, naming the vendor); workplace_application (one line in the handbook's style: three comma-separated use cases); ai_use_evidence (2-3 sentences with [n] markers to the sources list order); data_risks (one sentence on the sensitive data this function handles); confidence (high only if every statement is backed by an opened page); sources (every page opened and relied on).

Also write overview: 3-4 sentences on the pattern of what is still missing under this lens, including near-misses. Set lens to exactly "${lens.name}".

Keep each candidate under 150 words. Return only the structured output.`

const verifyAddDeptsPrompt = (lens, r) => `You are an adversarial fact-checker. Today is ${args.asOf}. Below is a list of departments another agent proposes adding to an enterprise AI training handbook (lens: ${lens.name}). Try to REFUTE each candidate, efficiently.

ALREADY COVERED departments (a candidate that duplicates one of these must be removed): ${excludedDepts}.

${WEB} For every candidate: open at least one cited source and confirm it shows AI use in that function; check the candidate is genuinely absent from the covered list rather than a renamed duplicate; check the recommended tools exist and fit.

Rules:
- A candidate whose AI-use evidence no opened page supports is removed and recorded.
- A duplicate of a covered department is removed and recorded.
- Correct names, tiers and tools where wrong, adding the correcting source.
- Add no new candidates. Keep text concise.
- Set confidence per candidate honestly after your checks.
- removed_or_corrected: one line per removal or correction.
- verification_notes: 2-4 sentences on overall reliability.

Return the full corrected result in the same structure, keeping lens exactly as given.

RESEARCH RESULT:
${JSON.stringify(r)}`

const fallbackVerified = (r, why) => ({ ...r, verification_notes: `Fact-check stage did not complete (${why}); content is as researched and should be read as unverified.`, removed_or_corrected: [] })
const norm = s => String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, '')

phase('Expand')
if (args.mode === 'tools') {
  log(`Starting ${TOOL_LENSES.length} additional-tools researchers`)
  const results = await pipeline(TOOL_LENSES,
    lens => agent(addToolsPrompt(lens), { ...STD, label: `more tools: ${lens.name}`, phase: 'Expand', schema: ADD_TOOLS_SCHEMA }),
    (r, lens) => r ? agent(verifyAddToolsPrompt(lens, r), { ...STD, label: `verify: ${lens.name}`, phase: 'Verify', schema: VERIFIED_ADD_TOOLS_SCHEMA }).then(v => v ? { ...v, categories: [lens.name] } : { ...fallbackVerified(r, 'verifier returned nothing'), categories: [lens.name] }) : null)
  const runs = (results || []).filter(Boolean)
  const missing = TOOL_LENSES.filter(l => !runs.some(a => a.categories && a.categories[0] === l.name)).map(l => l.name)
  if (missing.length) log(`DROPPED lenses: ${missing.join('; ')}`)
  const excluded = new Set([...args.handbookTools, ...args.excludeTools].map(norm))
  const merged = []; const seen = new Map()
  for (const r of runs) for (const c of r.candidates || []) {
    const k = norm(c.name)
    if (!k || excluded.has(k)) continue
    if (seen.has(k)) { const prev = seen.get(k); prev.suggested_departments = Array.from(new Set([...prev.suggested_departments, ...c.suggested_departments])); continue }
    seen.set(k, c); merged.push(c)
  }
  log(`Additional tools after dedup: ${merged.length}`)
  return { additionalTools: { runs, merged }, dropped: missing }
} else {
  log(`Starting ${DEPT_LENSES.length} additional-departments researchers`)
  const results = await pipeline(DEPT_LENSES,
    lens => agent(addDeptsPrompt(lens), { ...STD, label: `more depts: ${lens.name}`, phase: 'Expand', schema: ADD_DEPTS_SCHEMA }),
    (r, lens) => r ? agent(verifyAddDeptsPrompt(lens, r), { ...STD, label: `verify: ${lens.name}`, phase: 'Verify', schema: VERIFIED_ADD_DEPTS_SCHEMA }).then(v => v ? { ...v, lens: lens.name } : { ...fallbackVerified(r, 'verifier returned nothing'), lens: lens.name }) : null)
  const runs = (results || []).filter(Boolean)
  const missing = DEPT_LENSES.filter(l => !runs.some(a => a.lens === l.name)).map(l => l.name)
  if (missing.length) log(`DROPPED lenses: ${missing.join('; ')}`)
  const excluded = new Set([...args.handbookDepartments.map(d => d.replace(/^\d+\s*/, '')), ...args.excludeDepts].map(norm))
  const merged = []; const seen = new Map()
  for (const r of runs) for (const c of r.candidates || []) {
    const k = norm(c.name)
    if (!k || excluded.has(k) || seen.has(k)) continue
    seen.set(k, c); merged.push(c)
  }
  log(`Additional departments after dedup: ${merged.length}`)
  return { additionalDepartments: { runs, merged }, dropped: missing }
}
