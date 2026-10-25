export const meta = {
  name: 'ai-handbook-finish-depts',
  description: 'Research and fact-check real-world AI use in the 60 handbook departments, by cluster',
  phases: [
    { title: 'Research', detail: '8 department-cluster researchers, opened web sources only' },
    { title: 'Verify', detail: 'one adversarial fact-checker per cluster' },
  ],
}

const SOURCE = { type: 'object', properties: { title: { type: 'string' }, url: { type: 'string' } }, required: ['title', 'url'] }
const CONF = { type: 'string', enum: ['high', 'medium', 'low'] }
const DEPT_ENTRY = { type: 'object', properties: {
  num: { type: 'string' }, name: { type: 'string' }, tier: { type: 'string' },
  ai_use_cases: { type: 'array', items: { type: 'string' } },
  capstone_deliverable: { type: 'string' }, data_risks: { type: 'string' }, adoption_kpis: { type: 'string' },
  curriculum_emphasis: { type: 'string' }, tool_fit_commentary: { type: 'string' },
  confidence: CONF, sources: { type: 'array', items: SOURCE },
}, required: ['num', 'name', 'tier', 'ai_use_cases', 'capstone_deliverable', 'data_risks', 'adoption_kpis', 'curriculum_emphasis', 'tool_fit_commentary', 'confidence', 'sources'] }
const DEPT_CLUSTER_SCHEMA = { type: 'object', properties: { cluster: { type: 'string' }, cluster_overview: { type: 'string' }, departments: { type: 'array', items: DEPT_ENTRY } }, required: ['cluster', 'cluster_overview', 'departments'] }
const VERIFIED_DEPT_SCHEMA = { type: 'object', properties: { ...DEPT_CLUSTER_SCHEMA.properties, verification_notes: { type: 'string' }, removed_or_corrected: { type: 'array', items: { type: 'string' } } }, required: [...DEPT_CLUSTER_SCHEMA.required, 'verification_notes', 'removed_or_corrected'] }

const WEB = `Web access: load WebSearch with ToolSearch using the query "select:WebSearch" and use it to find candidate pages. The WebFetch tool does NOT work in this environment (DNS is unavailable). To OPEN a page, run with the Bash tool: python3 -I ${args.fetchScript} <url> [max_chars] [offset]. It prints "OPENED <url>" followed by the page text (rerun with an offset to read further), or "FAILED" when the page could not be opened. Only a page that printed OPENED counts as a source; a search snippet is never a source, and every claim must be supported by an opened page cited in sources with its exact URL. A page that FAILED (for example a 403 bot block) must not be cited: find the fact on another page or label the claim 'not verified'.`
const STD = { model: 'sonnet', effort: 'medium' }

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

Also write cluster_overview: 3-5 sentences on shared patterns, shared risks, and where the cluster's departments should train together. Set cluster to exactly "${c}".

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

Return the full corrected result in the same structure, with every department still present and the cluster name unchanged.

RESEARCH RESULT:
${JSON.stringify(r)}`

const fallbackVerified = (r, why) => ({ ...r, verification_notes: `Fact-check stage did not complete (${why}); content is as researched and should be read as unverified.`, removed_or_corrected: [] })

phase('Research')
log(`Starting ${args.deptClusterNames.length} department-cluster researchers`)
const deptResults = await pipeline(args.deptClusterNames,
  c => agent(researchDeptPrompt(c), { ...STD, label: `research depts: ${c}`, phase: 'Research', schema: DEPT_CLUSTER_SCHEMA }),
  (r, c) => r ? agent(verifyDeptPrompt(c, r), { ...STD, label: `verify depts: ${c}`, phase: 'Verify', schema: VERIFIED_DEPT_SCHEMA }).then(v => v || fallbackVerified(r, 'verifier returned nothing')) : null)

const depts = (deptResults || []).filter(Boolean)
const deptCount = depts.reduce((s, c) => s + c.departments.length, 0)
const missing = args.deptClusterNames.filter(c => !depts.some(d => d.cluster === c))
log(`Verified ${deptCount} departments across ${depts.length} clusters`)
if (missing.length) log(`DROPPED department clusters (agent failed): ${missing.join('; ')}`)

return { deptClusters: depts, dropped: { deptClusters: missing } }
