# Handover: AI handbook deep-research doc

STATUS: COMPLETE (25 October 2026), plus a second expansion pass the same day. The Claude Doc "Enterprise AI Tools & Departments Deep Research" at
https://claude.ai/artifact/PzB4eRd3Trt1TU4GsT6hrH
(doc id ba24a598-aca5-433a-a827-900bf3026cb2, prose body node id abac2331-6fa6,
block-id prefix m431jm6wj84) has no pending blocks left. Doc rev 38.

## What the doc contains

Headings are unnumbered, in this order:

1. Scope and method
2. Handbook at a glance (roadmap drawing)
3. Complete department directory (60)
4. Complete tool catalog (57)
5. Department-by-tool coverage matrix (frequency chart)
6. Tool deep dives: 10 groups, 57 tools, each with a fact-check paragraph and per-tool sources
7. Department deep dives: 8 clusters, 60 departments, each with a fact-check paragraph and per-department sources
8. Additional tools the handbook omits (41 in two tables, then a second pass of 49 in two more tables: 90 in all)
9. Additional departments the handbook omits (18 in one table, then a second pass of 23 in two more: 41 in all)
10. Cross-cutting themes (regulation table, data residency, cost model, rationalisation, hallucination/prompt injection/shadow AI, adoption and ROI, accessibility, tiering and hours, naming drift)
11. Gaps, caveats and recommendations (confidence table, renames table, caveats, 8 curriculum and 8 matrix recommendations)
12. Sources and verification notes (method, counts, labels, failures, and all 626 pages opened, grouped by section)

Confidence: tools 10 high / 39 medium / 8 low; departments 15 high / 44 medium / 1 low (46).

## If you need to edit the doc

Use Claude Docs `update` on node abac2331-6fa6 (engine prose,
container {"kind":"project","id":"ba24a598-aca5-433a-a827-900bf3026cb2"}).
Whole-block replaces of existing blocks need `ifRev` (and `ifHash` for single blocks).
Read the outline first: `read` with payload {"kind":"view","outline":true} (continue with `from`).
Writes are capped at 32,768 bytes each; split larger sections and insert later parts
after the last block id the ack returns (or insert in reverse order after a fixed anchor).

## Repo files

- `research/wf_args.json`, `research/wf_args2.json` – research briefs and workflow args.
- `research/data.json` – parsed handbook (60 departments, 57 tools).
- `research/fetch.py` – page fetcher used by agents (`python3 -I research/fetch.py <url> [max_chars] [offset]`); WebFetch does not work in this container, curl through the proxy does.
- `research/run_tools.json`, `run_depts.json`, `run_expansion.json`, `run_critic.json`, `run_redo_depts.json` – raw workflow results.
- `research/run2.json` – merged, fact-checked result used to generate the doc sections.
- `research/gen.py` – converts a result JSON into `out/s6_*.md`, `out/s7_*.md`, `out/s7b.md`, `out/s7c.md`, `out/gaps.md`.
- `out/` – generated section markdown as written to the doc; `out/sources_list.md` is the deduplicated source list (516 URLs), split into `sources_0..2.md` for the three doc writes.
- `research/run_more_tools.json`, `research/run_more_depts.json` – second expansion pass (6 tool lenses, 4 department lenses), rendered by `research/gen2.py` into `out/more_tools_*.md` and `out/more_depts_*.md`; `out/sources_more.md` lists the 110 new pages.
- `workflows/*.js` – Workflow scripts (tools, departments, expansion, critic, redo-depts, more-expansion). Agents ran on Sonnet at medium effort, the critic on Opus at high.

## Website

`web/build.py` generates the GitHub Pages site into `docs/` (live at https://kirannarayanak.github.io/ai-handbook-research/). `research/run_certs.json` holds the fact-checked courses and certifications per tool (164 paths, 45 certifications); tool pages render them under "Learning path and certifications" and department pages derive an ordered "What to learn" path from them. Rebuild and commit `docs/` after any change.

## Known limits to carry forward

- Vendor pages that returned 403: openai.com, canva.com, adobe.com pricing/legal FAQ, gainsight.com, business.meta.com, gartner.com, EC AI literacy Q&A, EBU/BBC study, Redress, docs.servicenow.com, Tableau and Google AI Studio pricing. Claims that depended on them are labelled not verified in the doc.
- Eight low-confidence tools: ChatGPT Enterprise, Canva Magic Studio, Adobe Firefly, Adobe Acrobat AI Assistant, ServiceNow Now Assist, Meta Advantage+, Gainsight AI, Google AI Studio.
- Renames table in the gaps section lists 20 handbook names that are outdated or on a sunset path; re-check quarterly.
