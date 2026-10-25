export const meta = {
  name: 'ai-handbook-finish-critic',
  description: 'Completeness critique of the verified AI handbook research, then targeted gap-fill research',
  phases: [
    { title: 'Critique', detail: 'completeness critic across all verified results', model: 'opus' },
    { title: 'Gap fill', detail: 'targeted research on the gaps the critic found' },
  ],
}

const SOURCE = { type: 'object', properties: { title: { type: 'string' }, url: { type: 'string' } }, required: ['title', 'url'] }
const CONF = { type: 'string', enum: ['high', 'medium', 'low'] }
const CRITIC_SCHEMA = { type: 'object', properties: {
  overall_assessment: { type: 'string' },
  gaps: { type: 'array', items: { type: 'object', properties: { area: { type: 'string' }, description: { type: 'string' }, research_task: { type: 'string' }, priority: { type: 'string', enum: ['high', 'medium', 'low'] } }, required: ['area', 'description', 'research_task', 'priority'] } },
}, required: ['overall_assessment', 'gaps'] }
const GAP_SCHEMA = { type: 'object', properties: { area: { type: 'string' }, findings_markdown: { type: 'string' }, sources: { type: 'array', items: SOURCE }, confidence: CONF }, required: ['area', 'findings_markdown', 'sources', 'confidence'] }

const WEB = `Web access: load WebSearch with ToolSearch using the query "select:WebSearch" and use it to find candidate pages. The WebFetch tool does NOT work in this environment (DNS is unavailable). To OPEN a page, run with the Bash tool: python3 -I ${args.fetchScript} <url> [max_chars] [offset]. It prints "OPENED <url>" followed by the page text (rerun with an offset to read further), or "FAILED" when the page could not be opened. Only a page that printed OPENED counts as a source; a search snippet is never a source, and every claim must be supported by an opened page cited in sources with its exact URL. A page that FAILED (for example a 403 bot block) must not be cited: find the fact on another page or label the claim 'not verified'.`
const STD = { model: 'sonnet', effort: 'medium' }

phase('Critique')
const critic = await agent(`You are the completeness critic for a deep-research document that expands a corporate AI training handbook covering 57 AI tools and 60 departments, and proposes additional tools and departments. Today is ${args.asOf}. A condensed view of the verified research so far is in the JSON file at ${args.condensedPath}; read it with the Read tool first.

Ask: what is missing that a CHRO, CIO or L&D director reading this document would expect? Consider: tools or departments with low confidence or few sources; cross-cutting topics not yet covered (EU AI Act and other AI regulation obligations for employers in 2026, data residency and enterprise licensing cost models for the six horizontal tools, overlap and redundancy between tools that an organisation should rationalise, vendor lock-in, accessibility, change management and adoption research, measuring training ROI, hallucination and verification practice, prompt-injection and shadow-AI risk); any handbook tool name that is now outdated; any department cluster where use cases look generic rather than specific; obvious additional tools or departments the expansion missed.

Return overall_assessment (4-6 sentences) and at most ${args.maxGaps} gaps, each with a self-contained research_task that a researcher with web access can complete in one sitting and a priority. Order by priority.`, { model: 'opus', effort: 'high', label: 'completeness critic', phase: 'Critique', schema: CRITIC_SCHEMA })

const gaps = critic ? critic.gaps.slice(0, args.maxGaps) : []
log(`Critic found ${gaps.length} gaps` + (critic && critic.gaps.length > args.maxGaps ? ` (${critic.gaps.length - args.maxGaps} lower-priority gaps dropped)` : ''))

phase('Gap fill')
const gapFills = (await parallel(gaps.map(gap => () => agent(`You are filling a gap in a deep-research document that expands a corporate AI training handbook (57 AI tools, 60 departments). Today is ${args.asOf}.

Gap area: ${gap.area}
Why it matters: ${gap.description}
Your task: ${gap.research_task}

${WEB} Open at least 3 credible sources published 2024-2026 (regulators, vendors' official pages, analyst or consulting reports, professional bodies, reputable press).

Return findings_markdown: 150-350 words of markdown (short paragraphs, bullets or one small pipe table; no headings), every factual claim followed by a [n] marker that maps to the sources list order; concrete numbers, dates and names rather than generalities. Set area to exactly "${gap.area}". Set confidence honestly.`, { ...STD, label: `gap: ${gap.area}`, phase: 'Gap fill', schema: GAP_SCHEMA })))).filter(Boolean)

log(`Gap fill complete: ${gapFills.length} of ${gaps.length} gaps researched`)
return { critic, gapFills }
