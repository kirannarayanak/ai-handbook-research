export const meta = {
  name: 'ai-handbook-certifications',
  description: 'Find official learning paths, courses and certifications for each handbook tool, with adversarial fact-checking',
  phases: [{ title: 'Research', detail: 'one researcher per tool group' }, { title: 'Verify', detail: 'one fact-checker per group' }],
}
const SOURCE = { type: 'object', properties: { title: { type: 'string' }, url: { type: 'string' } }, required: ['title', 'url'] }
const PATH = { type: 'object', properties: {
  title: { type: 'string' }, provider: { type: 'string' }, kind: { type: 'string', enum: ['certification', 'course', 'learning path', 'documentation', 'community'] },
  level: { type: 'string', enum: ['Foundation', 'Intermediate', 'Advanced', 'Admin'] }, duration: { type: 'string' }, cost: { type: 'string' },
  audience: { type: 'string' }, url: { type: 'string' }, verified: { type: 'boolean' }, note: { type: 'string' },
}, required: ['title', 'provider', 'kind', 'level', 'duration', 'cost', 'audience', 'url', 'verified', 'note'] }
const TOOL = { type: 'object', properties: { tool: { type: 'string' }, summary: { type: 'string' }, recommended_order: { type: 'array', items: { type: 'string' } }, paths: { type: 'array', items: PATH }, confidence: { type: 'string', enum: ['high', 'medium', 'low'] }, sources: { type: 'array', items: SOURCE } }, required: ['tool', 'summary', 'recommended_order', 'paths', 'confidence', 'sources'] }
const GROUP = { type: 'object', properties: { group: { type: 'string' }, overview: { type: 'string' }, tools: { type: 'array', items: TOOL } }, required: ['group', 'overview', 'tools'] }
const VGROUP = { type: 'object', properties: { ...GROUP.properties, verification_notes: { type: 'string' }, removed_or_corrected: { type: 'array', items: { type: 'string' } } }, required: [...GROUP.required, 'verification_notes', 'removed_or_corrected'] }
const WEB = `Web access: load WebSearch with ToolSearch using the query "select:WebSearch" and use it to find candidate pages. The WebFetch tool does NOT work in this environment. To OPEN a page, run with the Bash tool: python3 -I ${args.fetchScript} <url> [max_chars] [offset]. It prints "OPENED <url>" followed by the page text, or "FAILED" when the page could not be opened. Only a page that printed OPENED counts as verified; a search snippet is never a source. A page that FAILED must not be cited as verified: set verified=false and say so in note.`
const STD = { model: 'sonnet', effort: 'medium' }
const research = (g) => `You are building the "learning path and certifications" section of an enterprise AI training handbook. Today is ${args.asOf}.

Tool group: ${g.group}. Tools: ${g.tools.join('; ')}.

For EACH tool, find the official and widely used ways to learn it and get credentialed, as of ${args.asOf}:
- vendor academies and learning portals (for example Anthropic Academy and its "Claude 101" style courses, Microsoft Learn and Microsoft credentials, Google Cloud Skills Boost and Google certifications, GitHub Certifications, Salesforce Trailhead and Agentforce certifications, SAP Learning, Workday Learning, ServiceNow University / Now Learning, UiPath Academy, Databricks Academy, Snowflake University, AWS Training and Certification, Datadog Learning Center, CrowdStrike University, Dynatrace University, Adobe, Figma, Canva, Atlassian University, HubSpot Academy, Gong, Zendesk, Qualtrics, Thomson Reuters, Datasite, Optro);
- the official documentation or getting-started hub;
- a formal certification or exam if one exists (name, level, cost, duration, prerequisites);
- at most one strong third-party course (LinkedIn Learning, Coursera, Pluralsight) only if no vendor course exists.

Give 2-5 paths per tool, strongest first, and a recommended_order: the names of the paths in the sequence a learner should take them (foundation course, then role course, then certification). Fill level (Foundation, Intermediate, Advanced, Admin), duration and cost as the page states them (write "not stated" when they are not), audience (who it is for), verified (true only if you OPENED the page and it shows the course or certification), and a one-sentence note (for example that the course is free, that the exam was retired, or that the page could not be opened). summary: 2-3 sentences on how to learn this tool and whether a credential exists. confidence: high only if every path is verified.

${WEB} Open the vendor learning page for every tool. Set group to exactly "${g.group}". Keep text concise. Return only the structured output.`
const verify = (g, r) => `You are an adversarial fact-checker. Today is ${args.asOf}. Below are proposed learning paths and certifications for the tools in the group "${g.group}". Try to REFUTE each path, efficiently.

${WEB} For every path marked verified=true, open its URL and confirm the course or certification exists under that name today and that level, duration and cost match the page. For paths marked verified=false, try once to open the URL or find the official page; if you succeed, correct the entry and set verified=true.

Rules:
- Remove any path whose page does not show the course or certification, and record why.
- Retired or renamed credentials: keep only if the page says so, with the current name, and say so in note.
- Correct names, providers, levels, durations and costs from the opened page; set verified honestly.
- Add no new tools. Keep text concise. Keep group exactly as given.
- removed_or_corrected: one line per removal or correction. verification_notes: 2-4 sentences on reliability.

RESEARCH RESULT:
${JSON.stringify(r)}`
const fallback = (r, why) => ({ ...r, verification_notes: `Fact-check stage did not complete (${why}); unverified.`, removed_or_corrected: [] })
phase('Research')
const results = await pipeline(args.groups,
  g => agent(research(g), { ...STD, label: `certs: ${g.group}`, phase: 'Research', schema: GROUP }),
  (r, g) => r ? agent(verify(g, r), { ...STD, label: `verify certs: ${g.group}`, phase: 'Verify', schema: VGROUP }).then(v => v ? { ...v, group: g.group } : { ...fallback(r, 'verifier returned nothing'), group: g.group }) : null)
const groups = (results || []).filter(Boolean)
log(`groups done: ${groups.length}/${args.groups.length}; tools: ${groups.reduce((s, g) => s + g.tools.length, 0)}`)
return { groups }
