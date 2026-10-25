export const meta = {
  name: 'ai-handbook-finish-tools',
  description: 'Fact-check 8 cached tool groups and research plus fact-check the 2 missing tool groups of the AI handbook',
  phases: [
    { title: 'Research', detail: '2 tool-group researchers, opened web sources only' },
    { title: 'Verify', detail: 'one adversarial fact-checker per tool group, re-opening cited sources' },
  ],
}

const SOURCE = { type: 'object', properties: { title: { type: 'string' }, url: { type: 'string' } }, required: ['title', 'url'] }
const CONF = { type: 'string', enum: ['high', 'medium', 'low'] }
const TOOL_ENTRY = { type: 'object', properties: {
  name: { type: 'string' }, vendor: { type: 'string' }, what_it_is: { type: 'string' },
  key_capabilities: { type: 'array', items: { type: 'string' } },
  enterprise_data_handling: { type: 'string' }, licensing_pricing: { type: 'string' }, integrations: { type: 'string' },
  recent_developments: { type: 'string' }, best_fit_departments: { type: 'string' }, training_notes: { type: 'string' },
  caveats: { type: 'string' }, confidence: CONF, sources: { type: 'array', items: SOURCE },
}, required: ['name', 'vendor', 'what_it_is', 'key_capabilities', 'enterprise_data_handling', 'licensing_pricing', 'integrations', 'recent_developments', 'best_fit_departments', 'training_notes', 'caveats', 'confidence', 'sources'] }
const TOOL_GROUP_SCHEMA = { type: 'object', properties: { group: { type: 'string' }, category_overview: { type: 'string' }, tools: { type: 'array', items: TOOL_ENTRY } }, required: ['group', 'category_overview', 'tools'] }
const VERIFIED_TOOL_SCHEMA = { type: 'object', properties: { ...TOOL_GROUP_SCHEMA.properties, verification_notes: { type: 'string' }, removed_or_corrected: { type: 'array', items: { type: 'string' } } }, required: [...TOOL_GROUP_SCHEMA.required, 'verification_notes', 'removed_or_corrected'] }

const WEB = `Web access: load WebSearch with ToolSearch using the query "select:WebSearch" and use it to find candidate pages. The WebFetch tool does NOT work in this environment (DNS is unavailable). To OPEN a page, run with the Bash tool: python3 -I ${args.fetchScript} <url> [max_chars] [offset]. It prints "OPENED <url>" followed by the page text (rerun with an offset to read further), or "FAILED" when the page could not be opened. Only a page that printed OPENED counts as a source; a search snippet is never a source, and every claim must be supported by an opened page cited in sources with its exact URL. A page that FAILED (for example a 403 bot block) must not be cited: find the fact on another page or label the claim 'not verified'.`
const STD = { model: 'sonnet', effort: 'medium' }

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

Also write category_overview: 3-5 sentences on how the tools in this group relate, overlap and compete, and what enterprises usually standardise on. Set group to exactly "${g}".

Keep each tool entry under 350 words. Return only the structured output.`

const verifyRules = `Rules:
- A claim no opened page supports is removed, or rewritten as 'not verified'.
- A wrong price, tier, date or product name is corrected, with the correcting source added to sources.
- A dead or irrelevant URL you encountered is removed from sources.
- Add no new claims beyond corrections. Keep the text concise.
- Set confidence per tool honestly after your checks.
- removed_or_corrected: one line per removal or correction (tool, what, why).
- verification_notes: 2-4 sentences on overall reliability.

Return the full corrected result in the same structure, with every tool still present and the group name unchanged.`

const verifyToolPrompt = (g, r) => `You are an adversarial fact-checker. Today is ${args.asOf}. Below is a research result on the AI tool group "${g}" produced by another agent. Try to REFUTE it, efficiently.

${WEB} For every tool entry: open the vendor's current pricing or plans page and trust/data-usage page and compare them with the licensing_pricing and enterprise_data_handling claims; open two further cited sources per tool, chosen where the claims look most surprising, and confirm they exist and support what is attributed to them; check vendor and product names are current (renames, discontinued products).

${verifyRules}

RESEARCH RESULT:
${JSON.stringify(r)}`

const verifyCachedToolPrompt = (g, path) => `You are an adversarial fact-checker. Today is ${args.asOf}. Another agent researched the AI tool group "${g}" for an enterprise training reference; its result is the JSON file at ${path}. Read it with the Read tool, then try to REFUTE it, efficiently. Note that it was written on 2026-10-24 by an agent that could open pages, so its sources are real URLs to re-open.

${WEB} For every tool entry: open the vendor's current pricing or plans page and trust/data-usage page and compare them with the licensing_pricing and enterprise_data_handling claims; open two further cited sources per tool, chosen where the claims look most surprising, and confirm they exist and support what is attributed to them; check vendor and product names are current (renames, discontinued products).

${verifyRules}`

const fallbackVerified = (r, why) => ({ ...r, verification_notes: `Fact-check stage did not complete (${why}); content is as researched and should be read as unverified.`, removed_or_corrected: [] })

phase('Research')
const cachedCount = Object.keys(args.cachedToolGroups).length
log(`${cachedCount} cached tool groups go straight to fact-check; ${args.toolGroupNames.length - cachedCount} are researched first`)

const toolResults = await pipeline(args.toolGroupNames,
  async g => args.cachedToolGroups[g] ? { cachedPath: args.cachedToolGroups[g] } : agent(researchToolPrompt(g), { ...STD, label: `research tools: ${g}`, phase: 'Research', schema: TOOL_GROUP_SCHEMA }),
  (r, g) => !r ? null : r.cachedPath
    ? agent(verifyCachedToolPrompt(g, r.cachedPath), { ...STD, label: `verify tools: ${g}`, phase: 'Verify', schema: VERIFIED_TOOL_SCHEMA })
    : agent(verifyToolPrompt(g, r), { ...STD, label: `verify tools: ${g}`, phase: 'Verify', schema: VERIFIED_TOOL_SCHEMA }).then(v => v || fallbackVerified(r, 'verifier returned nothing')))

const tools = (toolResults || []).filter(Boolean)
const toolCount = tools.reduce((s, g) => s + g.tools.length, 0)
const missing = args.toolGroupNames.filter(g => !tools.some(t => t.group === g))
log(`Verified ${toolCount} tools across ${tools.length} groups`)
if (missing.length) log(`DROPPED tool groups (agent failed): ${missing.join('; ')}`)

return { toolGroups: tools, dropped: { toolGroups: missing } }
