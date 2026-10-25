"""Second-pass expansion: render additional tools / departments as chunked markdown.

Usage: python3 research/gen2.py tools research/run_more_tools.json
       python3 research/gen2.py depts research/run_more_depts.json
Writes out/more_tools_<i>.md or out/more_depts_<i>.md, each under ~28 KB.
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen import clean, links

CAP = 28000

def tool_rows(merged):
    rows = []
    for t in merged:
        L = links(t.get('sources'), 3)
        deps = ', '.join(clean(x) for x in t.get('suggested_departments', []))
        rows.append(f"| {clean(t['name'])} | {clean(t['vendor'])} | {clean(t['category'])} | {clean(t['what_it_is'])} | {clean(t['why_include'])} | {deps} | {clean(t['suggested_tier'])} | {clean(t['overlaps_with'])} | {clean(t.get('confidence',''))} | {' · '.join(L)} |")
    return rows

def dept_rows(merged):
    rows = []
    for d in merged:
        L = links(d.get('sources'), 3)
        tools = ', '.join(clean(x) for x in d.get('recommended_tools', []))
        rows.append(f"| {clean(d['name'])} | {clean(d['why_missing'])} | {clean(d['typical_org_types'])} | {clean(d['suggested_tier'])} | {tools} | {clean(d['workplace_application'])} | {clean(d['data_risks'])} | {clean(d['ai_use_evidence'])} | {clean(d.get('confidence',''))} | {' · '.join(L)} |")
    return rows

TOOL_HDR = '| Tool | Vendor | Lens | What it is | Why include | Suggested departments | Tier | Overlaps with | Confidence | Sources |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n'
DEPT_HDR = '| Proposed department | Why missing | Where found | Tier | Recommended tools | Workplace application | Data risks | Evidence | Confidence | Sources |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n'

def chunk(intro, hdr, rows, label):
    # group rows into tables each under CAP bytes (intro rides with the first)
    groups, cur, size = [], [], len(intro.encode()) + len(hdr.encode())
    for r in rows:
        if cur and size + len(r.encode()) + 1 > CAP:
            groups.append(cur); cur, size = [], len(hdr.encode())
        cur.append(r); size += len(r.encode()) + 1
    groups.append(cur)
    n = len(groups); out = []
    for i, g in enumerate(groups):
        head = intro + '\n\n' if i == 0 else ''
        if n > 1: head += f"*{label}, part {i+1} of {n}.*\n\n"
        out.append(head + hdr + '\n'.join(g) + '\n')
    return out

def main(mode, src):
    R = json.load(open(src))
    if 'result' in R: R = R['result']
    os.makedirs('out', exist_ok=True)
    if mode == 'tools':
        at = R['additionalTools']; merged, runs = at['merged'], at['runs']
        intro = f"**Second pass: {len(merged)} more tools.** A further research pass used six new lenses (HR, talent and learning; finance, procurement and supply chain; knowledge, documents, meetings and translation; agent builders, automation and voice; marketing, creative and commerce; engineering, IT operations, identity and risk), excluding the handbook's 57 tools and the 41 tools above. Each lens was fact-checked by a separate agent; the confidence column is the fact-checker's.\n\n"
        for r in runs:
            ov = clean(r.get('overview', ''))
            vn = clean(r.get('verification_notes', ''))
            rc = r.get('removed_or_corrected') or []
            if ov: intro += f"*{clean(r['categories'][0])}:* {ov}"
            if vn: intro += f" *Fact-check:* {vn}" + (f" {len(rc)} correction(s) or removal(s) were applied." if rc else '')
            intro += '\n\n'
        parts = chunk(intro.rstrip(), TOOL_HDR, tool_rows(merged), 'Second-pass tools table')
        for i, p in enumerate(parts):
            open(f'out/more_tools_{i}.md', 'w').write(p)
    else:
        ad = R['additionalDepartments']; merged, runs = ad['merged'], ad['runs']
        intro = f"**Second pass: {len(merged)} more departments.** A further research pass used four new lenses (commercial, brand and customer-adjacent; technology, data and engineering-adjacent; industry line-of-business; people, governance and enterprise support), excluding the handbook's 60 departments and the 18 above. Each lens was fact-checked by a separate agent; the confidence column is the fact-checker's.\n\n"
        for r in runs:
            ov = clean(r.get('overview', ''))
            vn = clean(r.get('verification_notes', ''))
            rc = r.get('removed_or_corrected') or []
            if ov: intro += f"*{clean(r['lens'])}:* {ov}"
            if vn: intro += f" *Fact-check:* {vn}" + (f" {len(rc)} correction(s) or removal(s) were applied." if rc else '')
            intro += '\n\n'
        parts = chunk(intro.rstrip(), DEPT_HDR, dept_rows(merged), 'Second-pass departments table')
        for i, p in enumerate(parts):
            open(f'out/more_depts_{i}.md', 'w').write(p)
    print({f: os.path.getsize('out/' + f) for f in sorted(os.listdir('out')) if f.startswith('more_')})

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
