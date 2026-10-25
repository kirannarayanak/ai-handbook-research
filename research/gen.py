import json, re, sys, html

def clean(s):
    if s is None: return ''
    s = html.unescape(str(s)).replace('\r','').strip()
    s = re.sub(r'\s*\n\s*', ' ', s)          # single line inside bullets
    s = s.replace('|', '\\|')
    return s

def links(sources, limit=None):
    out = []
    seen = set()
    for s in sources or []:
        u = (s.get('url') or '').strip()
        t = clean(s.get('title') or u)
        if not u or u in seen: continue
        seen.add(u)
        t = re.sub(r'[\[\]]', '', t)
        if len(t) > 70: t = t[:67] + '...'
        out.append(f'[{t}]({u})')
        if limit and len(out) >= limit: break
    return out

CONF = {'high':'high confidence','medium':'medium confidence','low':'low confidence'}

def tool_group_md(g, with_heading=False):
    md = ''
    if with_heading:
        md += '## Tool deep dives\n\nEvery one of the 57 tools, grouped into the ten categories used in the catalog. Each entry was researched from pages the researcher opened and then re-checked by an independent fact-checker; the confidence label is the fact-checker\'s. Prices are list prices as published on the date opened and change often.\n\n'
    md += f"### {clean(g['group'])}\n\n{clean(g['category_overview'])}\n\n"
    vn = clean(g.get('verification_notes',''))
    rc = g.get('removed_or_corrected') or []
    if vn:
        md += f"*Fact-check:* {vn}"
        if rc: md += f" {len(rc)} correction(s) or removal(s) were applied."
        md += '\n\n'
    for t in g['tools']:
        v = clean(t['vendor'])
        v = re.sub(r"\s*Brief'?s guess (is )?correct\.?", '', v, flags=re.I)
        vshort = re.split(r'\.\s|;\s', v)[0].strip().rstrip('.')
        if len(vshort) > 70: vshort = vshort[:67] + '...'
        md += f"**{clean(t['name'])}** ({vshort}; {CONF.get(t.get('confidence'),'unrated')})\n\n"
        if len(v) > len(vshort) + 5:
            md += f"- **Vendor and product family:** {v}\n"
        md += f"- **What it is:** {clean(t['what_it_is'])}\n"
        caps = '; '.join(clean(c) for c in t.get('key_capabilities',[]))
        md += f"- **Key capabilities:** {caps}\n"
        md += f"- **Enterprise data handling:** {clean(t['enterprise_data_handling'])}\n"
        md += f"- **Licensing and pricing:** {clean(t['licensing_pricing'])}\n"
        md += f"- **Integrations:** {clean(t['integrations'])}\n"
        md += f"- **2025-2026 developments:** {clean(t['recent_developments'])}\n"
        md += f"- **Best-fit handbook departments:** {clean(t['best_fit_departments'])}\n"
        md += f"- **Training notes:** {clean(t['training_notes'])}\n"
        md += f"- **Caveats:** {clean(t['caveats'])}\n"
        L = links(t.get('sources'))
        md += f"- **Sources ({len(L)}):** {' · '.join(L)}\n\n"
    return md

def dept_cluster_md(c, with_heading=False):
    md = ''
    if with_heading:
        md += '## Department cluster deep dives\n\nAll 60 departments, grouped into eight functional clusters. For each department: real-world AI use cases with sources, a capstone that fits the handbook\'s assignment template, the data rules the function must follow, adoption indicators, where the training hours should go, and whether the handbook\'s tool list fits.\n\n'
    md += f"### {clean(c['cluster'])}\n\n{clean(c['cluster_overview'])}\n\n"
    vn = clean(c.get('verification_notes',''))
    rc = c.get('removed_or_corrected') or []
    if vn:
        md += f"*Fact-check:* {vn}"
        if rc: md += f" {len(rc)} correction(s) or removal(s) were applied."
        md += '\n\n'
    for d in c['departments']:
        md += f"**{clean(d['num'])} {clean(d['name'])}** ({clean(d['tier'])}; {CONF.get(d.get('confidence'),'unrated')})\n\n"
        md += "- **AI use cases in practice:**\n"
        for u in d.get('ai_use_cases',[]):
            md += f"    - {clean(u)}\n"
        md += f"- **Capstone deliverable:** {clean(d['capstone_deliverable'])}\n"
        md += f"- **Data risks and rules:** {clean(d['data_risks'])}\n"
        md += f"- **Adoption KPIs:** {clean(d['adoption_kpis'])}\n"
        md += f"- **Curriculum emphasis:** {clean(d['curriculum_emphasis'])}\n"
        md += f"- **Tool-list fit:** {clean(d['tool_fit_commentary'])}\n"
        L = links(d.get('sources'))
        md += f"- **Sources ({len(L)}):** {' · '.join(' '.join([f'[{i+1}]', l]) for i,l in enumerate(L))}\n\n"
    return md

def add_tools_md(merged, runs):
    md = '## Additional tools the handbook omits\n\n'
    n = len(merged)
    md += f"{n} widely adopted enterprise AI tools are absent from the handbook's 57. Candidates were researched by category, fact-checked, and de-duplicated against the handbook list; anything found to be a handbook tool under another name was dropped. Suggested departments use the handbook's numbering.\n\n"
    for r in runs:
        ov = clean(r.get('overview',''))
        if ov: md += f"*{' and '.join(clean(x) for x in r.get('categories',[]))}:* {ov}\n\n"
    md += '| Tool | Vendor | Category | What it is | Why include | Suggested departments | Tier | Overlaps with | Sources |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n'
    for t in merged:
        L = links(t.get('sources'), 3)
        deps = ', '.join(clean(x) for x in t.get('suggested_departments',[]))
        md += f"| {clean(t['name'])} | {clean(t['vendor'])} | {clean(t['category'])} | {clean(t['what_it_is'])} | {clean(t['why_include'])} | {deps} | {clean(t['suggested_tier'])} | {clean(t['overlaps_with'])} | {' · '.join(L)} |\n"
    return md

def add_depts_md(merged, runs):
    md = '## Additional departments the handbook omits\n\n'
    md += f"{len(merged)} functions common in large organisations, each with documented AI use in 2024-2026, are absent from the handbook's 60. Three research lenses were used (core corporate functions, industry and operational functions, AI-era governance functions); candidates were fact-checked and de-duplicated against the 60.\n\n"
    for r in runs:
        ov = clean(r.get('overview',''))
        if ov: md += f"*{clean(r.get('lens',''))}:* {ov}\n\n"
    md += '| Proposed department | Why missing | Where found | Tier | Recommended tools | Workplace application | Data risks | Evidence | Sources |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n'
    for d in merged:
        L = links(d.get('sources'), 3)
        tools = ', '.join(clean(x) for x in d.get('recommended_tools',[]))
        md += f"| {clean(d['name'])} | {clean(d['why_missing'])} | {clean(d['typical_org_types'])} | {clean(d['suggested_tier'])} | {tools} | {clean(d['workplace_application'])} | {clean(d['data_risks'])} | {clean(d['ai_use_evidence'])} | {' · '.join(L)} |\n"
    return md

def gapfills_md(gapFills):
    md = ''
    for g in gapFills:
        md += f"### {clean(g['area'])}\n\n"
        body = html.unescape(g['findings_markdown']).strip()
        body = re.sub(r'^#+\s*', '', body, flags=re.M)
        md += body + '\n\n'
        L = links(g.get('sources'))
        md += f"Sources ({CONF.get(g.get('confidence'),'unrated')}): {' · '.join(' '.join([f'[{i+1}]', l]) for i,l in enumerate(L))}\n\n"
    return md

if __name__ == '__main__':
    src = sys.argv[1]
    R = json.load(open(src))
    if 'result' in R: R = R['result']
    import os
    os.makedirs('out', exist_ok=True)
    for i,g in enumerate(R.get('toolGroups',[])):
        open(f'out/s6_{i}.md','w').write(tool_group_md(g, with_heading=(i==0)))
    for i,c in enumerate(R.get('deptClusters',[])):
        open(f'out/s7_{i}.md','w').write(dept_cluster_md(c, with_heading=(i==0)))
    at = R.get('additionalTools') or {}
    if at.get('merged') is not None:
        open('out/s7b.md','w').write(add_tools_md(at['merged'], at.get('runs',[])))
    ad = R.get('additionalDepartments') or {}
    if ad.get('merged') is not None:
        open('out/s7c.md','w').write(add_depts_md(ad['merged'], ad.get('runs',[])))
    if R.get('gapFills'):
        open('out/gaps.md','w').write(gapfills_md(R['gapFills']))
    print({f: os.path.getsize('out/'+f) for f in sorted(os.listdir('out'))})
