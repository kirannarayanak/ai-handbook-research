# Handover: finish the AI handbook deep-research doc

GOAL: finish the Claude Doc "Enterprise AI Tools & Departments Deep Research" at
https://claude.ai/artifact/PzB4eRd3Trt1TU4GsT6hrH
(doc id ba24a598-aca5-433a-a827-900bf3026cb2, tab file id 59362327-c86d,
prose body node id abac2331-6fa6, block-id prefix m431jm6wj84).

Sections 1-5 are complete. Seven pending blocks remain, in doc order, full ids:

| Section | Pending block id |
| --- | --- |
| Tool deep dives | m431jm6wj84.278 |
| Department cluster deep dives | m431jm6wj84.279 |
| Additional tools the handbook omits | m431jm6wj84.27945 |
| Additional departments the handbook omits | m431jm6wj84.27946 |
| Cross-cutting themes | m431jm6wj84.280 |
| Gaps, caveats and recommendations | m431jm6wj84.281 |
| Sources and verification notes | m431jm6wj84.282 |

Fill each with a Claude Docs `update` on node abac2331-6fa6 (engine prose,
container {"kind":"project","id":"ba24a598-aca5-433a-a827-900bf3026cb2"}),
op replace, target {"kind":"blocks","ids":["<full id>"]},
with {"from":{"kind":"inline","content":"## Heading\n\n..."},"as":"markdown"}.
One section per call. Load the docs skill and `guide(["topic.index"])` first.
Fill big sections in parts: replace the pending block with part one, then insert
later parts after the last block id the ack returns.

## Repo files

- `research/wf_args.json` – research brief (10 tool groups, 8 department clusters). Point every workflow's `args.briefPath` at its absolute path in this checkout.
- `research/run1.json` – research for 8 of 10 tool groups under `result.toolGroups` (missing: "Security, cloud operations and observability AI" and "Data, analytics and AI development platforms"). Reuse it, but still fact-check those 8.
- `research/gen.py` – converts a result JSON into section markdown: `python3 research/gen.py <result.json>` writes `out/s6_*.md`, `out/s7_*.md`, `out/s7b.md`, `out/s7c.md`, `out/gaps.md`.
- `workflows/*.js` – three Workflow scripts: deep research (with critic and gap fill), departments only, expansion (additional tools, 5 category pairs; additional departments, 3 lenses).

## Work remaining

1. Research the 2 missing tool groups and all 8 department clusters.
2. Fact-check all 10 tool groups and 8 clusters (adversarial: open cited sources, remove or correct unsupported claims).
3. Run the expansion workflow: additional tools and additional departments the handbook omits, fact-checked and de-duplicated against the handbook's 57 tools and 60 departments.
4. Completeness critic, then gap fill.
5. Write the four remaining prose sections from the verified results: cross-cutting themes (governance, data privacy, EU AI Act obligations for employers, licensing cost models for the six horizontal tools, overlap and rationalisation, hours by tier); gaps and recommendations for curriculum and matrix design; sources listing every page cited.

Every claim carries a source the agent actually opened; label unverified content as such.

## Model and effort (user's instruction, to save credits)

- This session: Opus 5, medium effort.
- All research and fact-check agents: Sonnet 5, medium (`agent()` opts `model: 'sonnet'`, `effort: 'medium'`).
- Completeness critic: Opus 5, high.
- Agents load web tools via ToolSearch `select:WebSearch,WebFetch`.
- If the Workflow tool is unavailable, use the Agent tool with the scripts' prompts.
- If the Claude Docs connector is unavailable, write finished section markdown into `out/` in this repo, commit, and say so, so a local session can place it.

## User context

Kiran is building a department-by-tool training matrix from this handbook (iMinds Academy curriculum) and wants it exhaustive: every department, every tool, plus the additional tools and departments. Short progress lines; the doc is the deliverable.
