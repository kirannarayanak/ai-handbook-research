# AI handbook deep research

Working files for the Claude Doc "Enterprise AI Tools & Departments Deep Research"
(https://claude.ai/artifact/PzB4eRd3Trt1TU4GsT6hrH), which expands the
Corporate AI Tools & Training Handbook (60 departments, 57 tools, October 2026).

The doc is complete as of 25 October 2026. See `HANDOVER.md` for its structure,
how to edit it, and the known limits.

## Files

- `research/handbook.pdf`, `research/handbook.txt` – the source handbook and its extracted text.
- `research/data.json` – parsed records: 60 departments (num, name, tier, tools, app), vendor/category per tool, tool→departments map, frequency list.
- `research/wf_args.json`, `research/wf_args2.json` – the research brief (10 tool groups, 8 department clusters) and the args passed to the workflows.
- `research/fetch.py` – page fetcher the agents used to open sources (curl through the container proxy, HTML stripped).
- `research/run_tools.json`, `run_depts.json`, `run_expansion.json`, `run_critic.json`, `run_redo_depts.json` – raw workflow outputs.
- `research/run2.json` – merged and fact-checked result (57 tools, 60 departments, 41 additional tools, 18 additional departments).
- `research/gen.py` – turns a result JSON into markdown for the doc sections: `python3 gen.py <result.json>` writes `out/s6_*.md` (tool deep dives), `out/s7_*.md` (department clusters), `out/s7b.md` (additional tools), `out/s7c.md` (additional departments), `out/gaps.md`.
- `out/` – the generated section markdown as placed in the doc, plus `sources_list.md` (516 deduplicated source URLs).
- `workflows/*.js` – the Workflow scripts: tools, departments, expansion, critic and gap fill, and the second-pass department redo.

## Doc state

All sections filled: scope and method; handbook at a glance; department directory (60); tool catalog (57); coverage matrix; tool deep dives (10 groups); department deep dives (8 clusters); additional tools (41); additional departments (18); cross-cutting themes; gaps, caveats and recommendations; sources and verification notes (516 pages).
