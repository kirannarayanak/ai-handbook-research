# SkillGrid

**Live site:** https://kirannarayanak.github.io/ai-handbook-research/

SkillGrid is an enterprise AI learning map built from the *Corporate AI Tools & Training Handbook* (60 departments, 57 tools, October 2026 revised edition) for iMinds Academy curriculum planning. It tells each department which AI tools fit its work, what the data rules are, which official courses and certifications to take, and in what order. Every claim links to a source page that was opened and checked; unverified claims are labelled.

## What is on the site

- A six-chapter learning path with progress tracking
- 57 tool profiles (data handling, pricing, developments, department fit, caveats, sources) with official courses and certifications
- 60 department profiles (use cases, capstone, data rules, KPIs, learning order)
- 90 additional tools and 41 additional functions the handbook omits
- An interactive coverage matrix (clusters × tool families, drill-down to the full grid)
- Side-by-side comparison of tools or departments
- Cross-cutting themes, gaps and renames, glossary, FAQ, and all 626 sources

## Editing the site

1. Text and copy live in `web/content.py`; page templates in `web/build.py`; styles and scripts in `web/assets/`.
2. Research data lives in `research/` (`run2.json` for tools and departments, `run_more_*.json` for the additional lists, `run_certs.json` for courses and certifications).
3. Rebuild with `python3 web/build.py` (needs Python 3 and the `markdown` package), which writes the static site to `docs/`.
4. Commit and push `docs/`. GitHub Pages publishes from `docs/` on the `main-7y595x` branch.

## Repository layout

- `docs/` – the built site served by GitHub Pages
- `web/` – generator, content and assets
- `research/` – handbook source text, parsed data, research results and helper scripts
- `out/` – generated markdown sections and the deduplicated source list
- `workflows/` – the research workflow scripts used to gather and fact-check the data
- `.github/workflows/pages.yml` – Pages deployment

## Notes

Research is dated 24-25 October 2026. Tool names, prices and availability change often; the Gaps and renames page lists what had already moved. Nothing on the site is purchase or legal advice.
