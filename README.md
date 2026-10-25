# AI handbook deep research

Working files for the Claude Doc "Enterprise AI Tools & Departments Deep Research"
(https://claude.ai/artifact/PzB4eRd3Trt1TU4GsT6hrH), which expands the
Corporate AI Tools & Training Handbook (60 departments, 57 tools, October 2026).

## Files

- `research/handbook.pdf`, `research/handbook.txt` – the source handbook and its extracted text.
- `research/data.json` – parsed records: 60 departments (num, name, tier, tools, app), vendor/category per tool, tool→departments map, frequency list.
- `research/wf_args.json` – the research brief: 10 tool groups and 8 department clusters with handbook context. Workflow agents read this file.
- `research/run1.json` – first workflow run output. `result.toolGroups` holds 8 of the 10 tool groups fully researched (unverified). Missing: "Security, cloud operations and observability AI" and "Data, analytics and AI development platforms". No department clusters completed.
- `research/gen.py` – turns a workflow result JSON into markdown for the doc sections: `python3 gen.py <result.json>` writes `out/s6_*.md` (tool deep dives), `out/s7_*.md` (department clusters), `out/s7b.md` (additional tools), `out/s7c.md` (additional departments), `out/gaps.md`.
- `workflows/*.js` – the three Workflow scripts (deep research, departments only, expansion: additional tools and departments). Each expects `args.briefPath` pointing at `research/wf_args.json`.

## Doc state

Sections done: scope and method, handbook at a glance (with roadmap drawing), complete department directory (60), complete tool catalog (57), coverage matrix (with frequency chart).
Pending blocks still to fill, in order: tool deep dives, department cluster deep dives, additional tools, additional departments, cross-cutting themes, gaps and recommendations, sources.
