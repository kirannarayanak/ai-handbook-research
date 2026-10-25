#!/usr/bin/env python3
"""Static site generator for the Enterprise AI Handbook site.

Usage: python3 web/build.py            -> writes ./docs (GitHub Pages)
Reads research/*.json and web/content.py; copies web/assets.
"""
import html, json, os, re, shutil, sys
from pathlib import Path

import markdown as mdlib

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "docs"
sys.path.insert(0, str(HERE))
import content as C  # noqa: E402

BASE_URL = "https://kirannarayanak.github.io/ai-handbook-research/"

# ---------------------------------------------------------------- data

def load(p):
    with open(ROOT / p) as f:
        return json.load(f)

DATA = load("research/data.json")
RUN = load("research/run2.json")["result"]
MORE_T = load("research/run_more_tools.json")["result"]["additionalTools"]
MORE_D = load("research/run_more_depts.json")["result"]["additionalDepartments"]

def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "x"

def esc(s):
    return html.escape(str(s if s is not None else ""), quote=True)

def md(text):
    return mdlib.markdown(text, extensions=["tables", "sane_lists"])

def clean(s):
    s = html.unescape(str(s or "")).replace("\r", "").strip()
    return re.sub(r"\s*\n\s*", " ", s)

def short(s, n):
    s = clean(s)
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "…"

CONF_LABEL = {"high": "High confidence", "medium": "Medium confidence", "low": "Low confidence"}
TIER_HOURS = {"Core": "6-10 h", "Advanced": "12-20 h", "Specialist": "20-40+ h"}

# tools -----------------------------------------------------------
TOOLS = []          # ordered list of dicts
TOOL_BY_NAME = {}
GROUPS = []
for g in RUN["toolGroups"]:
    grp = {"name": g["group"], "slug": slugify(g["group"]), "overview": clean(g["category_overview"]),
           "verification": clean(g.get("verification_notes", "")), "corrections": len(g.get("removed_or_corrected") or []), "tools": []}
    for t in g["tools"]:
        rec = dict(t)
        rec["slug"] = slugify(t["name"])
        rec["group"] = grp["name"]
        rec["group_slug"] = grp["slug"]
        v = clean(t["vendor"])
        v = re.sub(r"\s*Brief'?s guess (is )?correct\.?", "", v, flags=re.I)
        rec["vendor_short"] = re.split(r"\.\s|;\s", v)[0].strip().rstrip(".")
        rec["vendor_full"] = v
        rec["handbook_vendor"], rec["handbook_category"] = DATA["vendor"].get(t["name"], ["", ""])
        rec["dept_nums"] = DATA["tool_depts"].get(t["name"], [])
        TOOLS.append(rec)
        TOOL_BY_NAME[t["name"]] = rec
        grp["tools"].append(rec)
    GROUPS.append(grp)
TOOL_INDEX = {t["name"]: i for i, t in enumerate(TOOLS)}

# departments -----------------------------------------------------
DEPTS = []
DEPT_BY_NUM = {}
CLUSTERS = []
hb = {d["num"]: d for d in DATA["depts"]}
for c in RUN["deptClusters"]:
    cl = {"name": c["cluster"], "slug": slugify(c["cluster"]), "overview": clean(c["cluster_overview"]),
          "verification": clean(c.get("verification_notes", "")), "corrections": len(c.get("removed_or_corrected") or []), "depts": []}
    for d in c["departments"]:
        num = int(d["num"])
        h = hb[num]
        rec = dict(d)
        rec["n"] = num
        rec["num2"] = f"{num:02d}"
        rec["slug"] = f"{num:02d}-{slugify(d['name'])}"
        rec["cluster"] = cl["name"]
        rec["cluster_slug"] = cl["slug"]
        rec["tools"] = h["tools"]
        rec["app"] = h["app"]
        DEPTS.append(rec)
        DEPT_BY_NUM[num] = rec
        cl["depts"].append(rec)
    CLUSTERS.append(cl)
DEPTS.sort(key=lambda d: d["n"])

TIER_COUNT = {}
for d in DEPTS:
    TIER_COUNT[d["tier"]] = TIER_COUNT.get(d["tier"], 0) + 1

# additional tools / departments ----------------------------------
ADD_TOOLS = [dict(t, pass_no=1) for t in RUN["additionalTools"]["merged"]] + [dict(t, pass_no=2) for t in MORE_T["merged"]]
ADD_DEPTS = [dict(d, pass_no=1) for d in RUN["additionalDepartments"]["merged"]] + [dict(d, pass_no=2) for d in MORE_D["merged"]]
for x in ADD_TOOLS + ADD_DEPTS:
    x["slug"] = slugify(x["name"])

# sources ---------------------------------------------------------
def parse_sources(path):
    sections, cur = [], None
    for line in open(ROOT / path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("### "):
            cur = {"title": line[4:], "groups": [], "items": []}; sections.append(cur)
        elif line.startswith("**") and cur is not None:
            cur["groups"].append({"title": line.strip("*"), "items": []})
        elif line.startswith("- [") and cur is not None:
            m = re.match(r"- \[(.*)\]\((.*)\)", line)
            if m:
                item = (m.group(1), m.group(2))
                (cur["groups"][-1]["items"] if cur["groups"] else cur["items"]).append(item)
    return sections

SOURCES = parse_sources("out/sources_list.md") + parse_sources("out/sources_more.md")
N_SOURCES = sum(len(s["items"]) + sum(len(g["items"]) for g in s["groups"]) for s in SOURCES)

# ---------------------------------------------------------------- html bits

ICONS = {
    "spark": '<path d="M12 2l1.8 5.2L19 9l-5.2 1.8L12 16l-1.8-5.2L5 9l5.2-1.8z"/><path d="M19 15l.9 2.1L22 18l-2.1.9L19 21l-.9-2.1L16 18l2.1-.9z"/>',
    "org": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="8.5" y="14" width="7" height="7" rx="1.5"/><path d="M6.5 10v2.5h11V10M12 12.5V14"/>',
    "scale": '<path d="M12 3v18M4 7h16M6 7l-3 7a3 3 0 006 0zM18 7l-3 7a3 3 0 006 0z"/>',
    "book": '<path d="M4 5a2 2 0 012-2h13v16H6a2 2 0 00-2 2z"/><path d="M4 19a2 2 0 012-2h13"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "moon": '<path d="M21 12.8A9 9 0 1111.2 3a7 7 0 009.8 9.8z"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M5 12l5 5L20 7"/>',
    "grid": '<rect x="3" y="3" width="8" height="8" rx="1.5"/><rect x="13" y="3" width="8" height="8" rx="1.5"/><rect x="3" y="13" width="8" height="8" rx="1.5"/><rect x="13" y="13" width="8" height="8" rx="1.5"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8.5-8 9-4.5-.5-8-4-8-9V6z"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
}

def icon(name, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

def badge(kind, text):
    return f'<span class="badge badge-{esc(kind)}">{esc(text)}</span>'

def conf_badge(c):
    return badge(f"conf-{c}", CONF_LABEL.get(c, c))

def tier_badge(t):
    return badge(f"tier-{t.lower()}", f"{t} · {TIER_HOURS.get(t, '')}")

def nav_html(root):
    def link(h, t, desc=None):
        d = f'<span class="dd-desc">{esc(desc)}</span>' if desc else ""
        return f'<li><a href="{root}{h}"><span class="dd-title">{esc(t)}</span>{d}</a></li>'
    learn = "".join(link(f"learn/{c['slug']}/", f"{i+1}. {c['title']}", c["summary"]) for i, c in enumerate(C.CHAPTERS))
    tools = "".join(link(f"tools/#{g['slug']}", g["name"], f"{len(g['tools'])} tools") for g in GROUPS)
    depts = "".join(link(f"departments/#{c['slug']}", c["name"], f"{len(c['depts'])} departments") for c in CLUSTERS)
    return f"""
<header class="site-header" id="top">
  <a class="skip" href="#main">Skip to content</a>
  <nav class="nav" aria-label="Primary">
    <a class="brand" href="{root}"><span class="brand-mark">{icon('spark','ico')}</span><span class="brand-text">{esc(C.SITE_NAME)}</span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav-menu" aria-label="Open menu">{icon('menu')}</button>
    <ul class="nav-menu" id="nav-menu">
      <li class="has-dd"><button class="nav-link" aria-expanded="false">Learn <span class="caret"></span></button>
        <div class="dd dd-wide"><div class="dd-col"><p class="dd-head">Learning path</p><ul>{link('learn/','Start here','The six-chapter path, with progress tracking')}{learn}{link('learn/certifications/','Courses and certifications','Official learning paths and credentials for every tool')}</ul></div></div></li>
      <li class="has-dd"><button class="nav-link" aria-expanded="false">Tools <span class="caret"></span></button>
        <div class="dd dd-wide"><div class="dd-col"><p class="dd-head">Catalogue</p><ul>{link('tools/','All 57 tools','Profiles with pricing, data handling and sources')}{link('tools/more/','90 more tools','Widely adopted tools the handbook omits')}{link('learn/certifications/','Courses and certifications','How to learn and get credentialed on each tool')}{link('compare/','Compare tools','Side by side, up to four at once')}</ul></div><div class="dd-col"><p class="dd-head">By family</p><ul class="dd-grid">{tools}</ul></div></div></li>
      <li class="has-dd"><button class="nav-link" aria-expanded="false">Departments <span class="caret"></span></button>
        <div class="dd dd-wide"><div class="dd-col"><p class="dd-head">Directory</p><ul>{link('departments/','All 60 departments','Use cases, capstones, data rules and KPIs')}{link('departments/more/','41 more functions','Departments the handbook omits')}{link('matrix/','Coverage matrix','Who uses what, at a glance')}</ul></div><div class="dd-col"><p class="dd-head">By cluster</p><ul class="dd-grid">{depts}</ul></div></div></li>
      <li><a class="nav-link" href="{root}matrix/">Matrix</a></li>
      <li><a class="nav-link" href="{root}compare/">Compare</a></li>
      <li class="has-dd"><button class="nav-link" aria-expanded="false">Reference <span class="caret"></span></button>
        <div class="dd"><div class="dd-col"><ul>{link('themes/','Cross-cutting themes','Regulation, residency, cost, verification, adoption')}{link('gaps/','Gaps and renames','Confidence, outdated names, recommendations')}{link('sources/','Sources and method','All 626 pages opened, and how')}{link('about/','About','What this site is and how to use it')}</ul></div></div></li>
    </ul>
    <div class="nav-actions">
      <button class="icon-btn" id="search-btn" aria-label="Search (Ctrl+K)" title="Search (Ctrl+K)">{icon('search')}<kbd class="kbd">⌘K</kbd></button>
      <button class="icon-btn" id="theme-btn" aria-label="Toggle colour theme" title="Toggle theme"><span class="only-light">{icon('moon')}</span><span class="only-dark">{icon('sun')}</span></button>
    </div>
  </nav>
  <div class="progress" aria-hidden="true"><span id="read-progress"></span></div>
</header>"""

def footer_html(root):
    return f"""
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div><a class="brand" href="{root}"><span class="brand-mark">{icon('spark')}</span><span class="brand-text">{esc(C.SITE_NAME)}</span></a>
      <p class="muted">Companion to the Corporate AI Tools &amp; Training Handbook (60 departments, 57 tools, {esc(C.AS_OF)}). Every profile cites the pages a researcher opened; unverified claims are labelled.</p></div>
    <div><p class="foot-head">Learn</p><ul>{''.join(f'<li><a href="{root}learn/{c["slug"]}/">{esc(c["title"])}</a></li>' for c in C.CHAPTERS)}</ul></div>
    <div><p class="foot-head">Explore</p><ul><li><a href="{root}tools/">Tools</a></li><li><a href="{root}departments/">Departments</a></li><li><a href="{root}matrix/">Matrix</a></li><li><a href="{root}compare/">Compare</a></li><li><a href="{root}tools/more/">More tools</a></li><li><a href="{root}departments/more/">More functions</a></li></ul></div>
    <div><p class="foot-head">Reference</p><ul><li><a href="{root}themes/">Themes</a></li><li><a href="{root}gaps/">Gaps and renames</a></li><li><a href="{root}sources/">Sources and method</a></li><li><a href="{root}about/">About</a></li><li><a href="{esc(C.DOC_URL)}" rel="noopener">Long-form document</a></li><li><a href="{esc(C.REPO_URL)}" rel="noopener">Source on GitHub</a></li></ul></div>
  </div>
  <div class="wrap foot-bottom"><span>Research dated 24-25 October 2026. Not purchase or legal advice.</span><a href="#top">Back to top ↑</a></div>
</footer>
<div class="palette" id="palette" hidden>
  <div class="palette-box" role="dialog" aria-modal="true" aria-label="Search">
    <div class="palette-input">{icon('search')}<input id="palette-q" type="search" placeholder="Search tools, departments, chapters…" autocomplete="off" spellcheck="false"><kbd class="kbd">Esc</kbd></div>
    <ul class="palette-list" id="palette-list" role="listbox"></ul>
    <p class="palette-hint">↑↓ to move · Enter to open · type <b>t:</b> for tools, <b>d:</b> for departments</p>
  </div>
</div>"""

def page(path, title, body, *, desc="", extra_head="", extra_js=(), kind="page", crumbs=None):
    depth = path.count("/")
    root = "../" * depth
    url = BASE_URL + path
    crumb_html = ""
    if crumbs:
        items = [f'<li><a href="{root}">Home</a></li>'] + [
            (f'<li><a href="{root}{h}">{esc(t)}</a></li>' if h else f'<li aria-current="page">{esc(t)}</li>') for t, h in crumbs]
        crumb_html = f'<nav class="crumbs wrap" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'
    scripts = "".join(f'<script src="{root}assets/{s}" defer></script>' for s in ("site.js",) + tuple(extra_js))
    doc = f"""<!doctype html>
<html lang="en" data-theme="auto">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · {esc(C.SITE_NAME)}</title>
<meta name="description" content="{esc(short(desc or C.TAGLINE, 160))}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(short(desc or C.TAGLINE, 200))}"><meta property="og:type" content="website"><meta property="og:url" content="{esc(url)}"><meta property="og:site_name" content="{esc(C.SITE_NAME)}">
<meta name="theme-color" content="#0b1020" media="(prefers-color-scheme: dark)"><meta name="theme-color" content="#f6f7fb" media="(prefers-color-scheme: light)">
<link rel="canonical" href="{esc(url)}">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="{root}manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/site.css">
<script>(function(){{try{{var t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
<meta name="site-root" content="{root}">
{extra_head}
</head>
<body class="kind-{kind}">
{nav_html(root)}
{crumb_html}
<main id="main">
{body}
</main>
{footer_html(root)}
{scripts}
</body>
</html>"""
    out = OUT / path / "index.html" if not path.endswith(".html") else OUT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    SITEMAP.append(url)

SITEMAP = []
SEARCH = []

def add_search(title, url, kind, snippet, tags=""):
    SEARCH.append({"t": title, "u": url, "k": kind, "s": short(snippet, 140), "g": tags})

def hero(kicker, title, lead, actions="", meta="", cls=""):
    k = f'<p class="kicker">{kicker}</p>' if kicker else ""
    m = f'<div class="hero-meta">{meta}</div>' if meta else ""
    a = f'<div class="hero-actions">{actions}</div>' if actions else ""
    return f'<section class="hero {cls}"><div class="wrap">{k}<h1>{title}</h1><p class="lead">{lead}</p>{m}{a}</div></section>'

def btn(href, text, primary=False, ic="arrow"):
    return f'<a class="btn {"btn-primary" if primary else "btn-ghost"}" href="{href}">{esc(text)} {icon(ic, "ico-s")}</a>'

def card(href, title, desc, meta="", ic=None, cls=""):
    i = f'<span class="card-ico">{icon(ic)}</span>' if ic else ""
    m = f'<div class="card-meta">{meta}</div>' if meta else ""
    return f'<a class="card {cls}" href="{href}">{i}<h3>{esc(title)}</h3><p>{esc(desc)}</p>{m}</a>'

def sources_list(sources):
    items = []
    seen = set()
    for i, s in enumerate(sources or []):
        u = (s.get("url") or "").strip()
        if not u or u in seen: continue
        seen.add(u)
        t = clean(s.get("title") or u)
        items.append(f'<li><span class="src-n">[{len(items)+1}]</span> <a href="{esc(u)}" rel="noopener nofollow" target="_blank">{esc(t)}</a> <span class="src-host muted">{esc(re.sub(r"^https?://(www\.)?", "", u).split("/")[0])}</span></li>')
    return f'<ol class="sources">{"".join(items)}</ol>' if items else '<p class="muted">No sources recorded.</p>'

def deflist(pairs):
    return '<dl class="facts">' + "".join(f"<div><dt>{esc(k)}</dt><dd>{v}</dd></div>" for k, v in pairs if v) + "</dl>"

# ---------------------------------------------------------------- certifications / learning paths

CERTS = {}       # tool name -> {summary, recommended_order, paths, confidence, sources}
CERT_GROUPS = [] # [{group, overview, verification_notes, corrections}]
_cp = ROOT / "research" / "run_certs.json"
if _cp.exists():
    for g in load("research/run_certs.json")["result"]["groups"]:
        CERT_GROUPS.append({"group": g["group"], "overview": clean(g.get("overview", "")), "verification": clean(g.get("verification_notes", "")), "corrections": len(g.get("removed_or_corrected") or [])})
        for t in g["tools"]:
            CERTS[t["tool"]] = t

KIND_LABEL = {"certification": "Certification", "course": "Course", "learning path": "Learning path", "documentation": "Documentation", "community": "Community"}

def cert_cards(t, root):
    """Render a tool's learning paths as ordered step cards."""
    c = CERTS.get(t["name"])
    if not c or not c.get("paths"):
        return '<p class="muted">No official course or certification was found for this tool at the time of research. Start with the vendor documentation linked in the sources, then the shared foundation module.</p>'
    order = [clean(x) for x in c.get("recommended_order") or []]
    paths = list(c["paths"])
    def rank(p):
        try: return order.index(clean(p["title"]))
        except ValueError: return len(order) + {"course": 0, "learning path": 1, "documentation": 2, "certification": 3, "community": 4}.get(p["kind"], 5)
    paths.sort(key=rank)
    out = '<ol class="path-steps">'
    for i, p in enumerate(paths):
        v = '<span class="badge badge-conf-high">Verified</span>' if p.get("verified") else '<span class="badge badge-conf-low">Not verified</span>'
        meta = "".join(f'<span class="badge">{esc(x)}</span>' for x in (KIND_LABEL.get(p["kind"], p["kind"]), p["level"], p["duration"], p["cost"]) if x and x.lower() != "not stated")
        out += f'<li class="path-step"><span class="step-n">{i+1}</span><div><h4><a href="{esc(p["url"])}" rel="noopener" target="_blank">{esc(clean(p["title"]))}</a> <span class="muted small">· {esc(clean(p["provider"]))}</span></h4><div class="chips">{meta}{v}</div><p class="small"><b>For:</b> {esc(clean(p["audience"]))}{(" · " + esc(clean(p["note"]))) if p.get("note") else ""}</p></div></li>'
    out += "</ol>"
    return out

def best_credential(name):
    """(start, credential): the first step of the recommended order, and a verified certification if one exists."""
    c = CERTS.get(name)
    if not c or not c.get("paths"): return None
    ps = c["paths"]
    order = [clean(x) for x in c.get("recommended_order") or []]
    start = None
    for o in order:
        start = next((p for p in ps if clean(p["title"]) == o), None)
        if start: break
    if not start:
        start = next((p for p in ps if p.get("verified") and p["kind"] in ("course", "learning path")), ps[0])
    cert = next((p for p in ps if p["kind"] == "certification" and p.get("verified") and p is not start), None)
    return (start, cert)

def dept_path(d, root):
    """Ordered learning path for a department: foundation, general assistant, productivity, specialist tools."""
    steps = []
    hours = TIER_HOURS.get(d["tier"], "")
    steps.append(("Foundation module", f"{root}learn/foundations/", "Shared by every department: one approved assistant, verification, data classification, agent safety.", "4-6 h Core · 6-8 h Advanced and Specialist", None))
    ordered = sorted(d["tools"], key=lambda x: (GROUPS.index(next(g for g in GROUPS if g["name"] == TOOL_BY_NAME[x]["group"])) if x in TOOL_BY_NAME else 99, x))
    for x in ordered:
        t = TOOL_BY_NAME.get(x)
        if not t:
            steps.append((x, None, "Not profiled.", hours, None)); continue
        gi = GROUPS.index(next(g for g in GROUPS if g["name"] == t["group"]))
        role = "General assistant: learn this one well first." if gi == 0 else ("Productivity surface: learn inside the documents, sheets and meetings you already use." if gi in (1, 2) else "Specialist platform: train only if your organisation runs it.")
        steps.append((x, f"{root}tools/{t['slug']}/", role, hours, best_credential(x)))
    out = '<ol class="path-steps">'
    for i, (title, href, desc, hrs, cred) in enumerate(steps):
        link = f'<a href="{href}">{esc(title)}</a>' if href else esc(title)
        credh = ""
        if cred:
            start, cert = cred
            credh = f'<p class="small"><b>Start with:</b> <a href="{esc(start["url"])}" rel="noopener" target="_blank">{esc(clean(start["title"]))}</a> <span class="muted">({esc(clean(start["provider"]))}, {esc(KIND_LABEL.get(start["kind"], start["kind"]).lower())})</span>'
            if cert:
                credh += f' · <b>Credential:</b> <a href="{esc(cert["url"])}" rel="noopener" target="_blank">{esc(clean(cert["title"]))}</a>'
            credh += f' · <a href="{href}#learn">all paths</a></p>'
        elif href and i > 0:
            credh = f'<p class="small muted">No official credential found; use the vendor documentation on the <a href="{href}#learn">tool page</a>.</p>'
        out += f'<li class="path-step"><span class="step-n">{i}</span><div><h4>{link} <span class="badge">{esc(hrs)}</span></h4><p class="small">{esc(desc)}</p>{credh}</div></li>'
    out += "</ol>"
    n = len(d["tools"])
    lo, hi = {"Core": (6, 10), "Advanced": (12, 20), "Specialist": (20, 40)}[d["tier"]]
    fl, fh = (4, 6) if d["tier"] == "Core" else (6, 8)
    total = f'{fl + lo * min(n, 3)}-{fh + hi * n} hours'
    return out, total

# ---------------------------------------------------------------- pages

def build_home():
    H = C.HOME
    stats = "".join(f'<div class="stat"><span class="stat-n" data-count="{esc(n)}">{esc(n)}</span><span class="stat-l">{esc(l)}</span></div>' for n, l in H["stats"])
    paths = "".join(card(p["href"], p["title"], p["desc"], ic=p["icon"], cls="card-path reveal") for p in H["paths"])
    principles = "".join(f'<div class="prin reveal"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in H["principles"])
    clusters = "".join(card(f"departments/#{c['slug']}", c["name"], short(c["overview"], 120), meta=f'<span>{len(c["depts"])} departments</span>', cls="reveal") for c in CLUSTERS)
    groups = "".join(f'<a class="chip chip-lg" href="tools/#{g["slug"]}">{esc(g["name"])}<span class="chip-n">{len(g["tools"])}</span></a>' for g in GROUPS)
    chapters = "".join(f'<a class="step reveal" href="learn/{c["slug"]}/"><span class="step-n">{i+1}</span><div><h3>{esc(c["title"])}</h3><p>{esc(c["summary"])}</p><span class="muted">{c["minutes"]} min</span></div></a>' for i, c in enumerate(C.CHAPTERS))
    renames = "".join(f'<li><b>{esc(a)}</b> → {esc(short(b, 70))}</li>' for a, b, _, _ in C.RENAMES[:6])
    body = f"""
<section class="hero hero-home"><div class="hero-bg" aria-hidden="true"></div><div class="wrap">
  <p class="kicker">{esc(H['kicker'])}</p>
  <h1 class="display">{esc(H['title'])}</h1>
  <p class="lead">{esc(H['lead'])}</p>
  <div class="hero-actions">{btn('learn/', 'Start the learning path', True)}{btn('departments/', 'Find my department', False, 'org')}{btn('matrix/', 'Open the matrix', False, 'grid')}</div>
  <div class="stats">{stats}</div>
</div></section>
<section class="section"><div class="wrap">
  <h2 class="section-title">Where do you want to start?</h2>
  <div class="grid grid-4">{paths}</div>
</div></section>
<section class="section section-alt"><div class="wrap">
  <div class="split"><div><h2 class="section-title">The path, in six chapters</h2><p class="muted">Short, in order, and saved as you go. The whole path reads in under an hour; the detail pages are there when you need them.</p>{btn('learn/', 'View the path', True)}</div>
  <div class="steps">{chapters}</div></div>
</div></section>
<section class="section"><div class="wrap">
  <h2 class="section-title">Four principles the handbook is built on</h2>
  <div class="grid grid-4 prins">{principles}</div>
</div></section>
<section class="section section-alt"><div class="wrap">
  <h2 class="section-title">Sixty departments, eight clusters</h2>
  <div class="grid grid-4">{clusters}</div>
</div></section>
<section class="section"><div class="wrap">
  <h2 class="section-title">Fifty-seven tools, ten families</h2>
  <p class="muted">Two families are horizontal and appear almost everywhere. The other eight are platforms you train on only if your company runs them.</p>
  <div class="chips">{groups}</div>
  <div class="cta-row">{btn('tools/', 'Browse all tools', True)}{btn('compare/', 'Compare side by side', False, 'scale')}{btn('tools/more/', '90 more the handbook omits')}</div>
</div></section>
<section class="section section-alt"><div class="wrap split">
  <div><h2 class="section-title">Names move fast</h2><p class="muted">At least fourteen handbook tool names were already out of date when this research ran. Use the current name with the handbook name in brackets, and re-check quarterly.</p>{btn('gaps/', 'See the renames table')}</div>
  <ul class="rename-list">{renames}</ul>
</div></section>
"""
    page("", "Home", body, desc=H["lead"], kind="home", extra_js=("home.js",))

def build_learn():
    cards = "".join(f'<a class="chapter-card reveal" href="{c["slug"]}/" data-chapter="{c["slug"]}"><span class="step-n">{i+1}</span><div><h3>{esc(c["title"])}</h3><p>{esc(c["summary"])}</p><div class="card-meta"><span>{c["minutes"]} min read</span><span class="done-mark" hidden>{icon("check","ico-s")} Done</span></div></div></a>' for i, c in enumerate(C.CHAPTERS))
    body = hero("Learning path", esc(C.LEARN_INTRO["title"]), esc(C.LEARN_INTRO["lead"]), meta='<div class="path-progress"><div class="bar"><span id="path-bar"></span></div><span id="path-text" class="muted">0 of 6 chapters done</span></div>') + f'<section class="section"><div class="wrap"><div class="chapters">{cards}</div></div></section>'
    page("learn/", "Learning path", body, desc=C.LEARN_INTRO["lead"], crumbs=[("Learn", None)], extra_js=("learn.js",))
    add_search("Learning path", "learn/", "Learn", C.LEARN_INTRO["lead"])
    for i, c in enumerate(C.CHAPTERS):
        prev = C.CHAPTERS[i - 1] if i > 0 else None
        nxt = C.CHAPTERS[i + 1] if i + 1 < len(C.CHAPTERS) else None
        nav = '<div class="pager">'
        nav += f'<a class="pager-prev" href="../{prev["slug"]}/"><span class="muted">Previous</span><b>{esc(prev["title"])}</b></a>' if prev else "<span></span>"
        nav += f'<a class="pager-next" href="../{nxt["slug"]}/"><span class="muted">Next</span><b>{esc(nxt["title"])}</b></a>' if nxt else f'<a class="pager-next" href="../../departments/"><span class="muted">Next</span><b>Find your department</b></a>'
        nav += "</div>"
        links = "".join(f'<li><a href="../../{h}">{esc(t)} {icon("arrow","ico-s")}</a></li>' for t, h in c["next_links"])
        body = hero(f"Chapter {i+1} of {len(C.CHAPTERS)} · {c['minutes']} min", esc(c["title"]), esc(c["summary"]), cls="hero-sm")
        body += f'<section class="section"><div class="wrap prose-wrap"><article class="prose">{md(c["body"])}</article><aside class="side"><div class="side-box"><p class="foot-head">Go deeper</p><ul class="linklist">{links}</ul></div><div class="side-box"><button class="btn btn-primary btn-block" id="mark-done" data-chapter="{c["slug"]}">{icon("check","ico-s")} Mark chapter done</button><p class="muted small">Saved in this browser only.</p></div></aside></div><div class="wrap">{nav}</div></section>'
        page(f"learn/{c['slug']}/", c["title"], body, desc=c["summary"], crumbs=[("Learn", "learn/"), (c["title"], None)], kind="article", extra_js=("learn.js",))
        add_search(f"Chapter {i+1}: {c['title']}", f"learn/{c['slug']}/", "Learn", c["summary"])

def tool_card(t, root=""):
    meta = f'{conf_badge(t["confidence"])}<span class="muted">{len(t["dept_nums"])} departments</span>'
    return f'<a class="card card-tool reveal" href="{root}tools/{t["slug"]}/" data-conf="{t["confidence"]}" data-group="{t["group_slug"]}" data-name="{esc(t["name"].lower())}"><h3>{esc(t["name"])}</h3><p class="muted small">{esc(short(t["vendor_short"], 60))}</p><p>{esc(short(t["what_it_is"], 150))}</p><div class="card-meta">{meta}</div></a>'

def build_tools():
    filters = '<div class="filters" id="filters"><input type="search" id="filter-q" placeholder="Filter by name…" aria-label="Filter tools"><div class="seg" role="group" aria-label="Confidence"><button data-conf="" class="on">All</button><button data-conf="high">High</button><button data-conf="medium">Medium</button><button data-conf="low">Low</button></div></div>'
    sections = ""
    toc = ""
    for g in GROUPS:
        toc += f'<a class="chip" href="#{g["slug"]}">{esc(g["name"])}<span class="chip-n">{len(g["tools"])}</span></a>'
        fc = f'<details class="factcheck"><summary>Fact-check notes · {g["corrections"]} corrections applied</summary><p>{esc(g["verification"])}</p></details>' if g["verification"] else ""
        sections += f'<section class="group" id="{g["slug"]}"><div class="group-head"><h2>{esc(g["name"])}</h2><p>{esc(g["overview"])}</p>{fc}</div><div class="grid grid-3">{"".join(tool_card(t, "../") for t in g["tools"])}</div></section>'
    body = hero("Tool catalogue", "57 tools, profiled and fact-checked", "Each profile covers what the tool is, how it handles enterprise data, how it is priced, what changed in 2025-2026, and which departments it fits. Confidence is the fact-checker's rating.", meta=f'<div class="chips">{toc}</div>')
    body += f'<section class="section"><div class="wrap">{filters}{sections}<p class="empty" id="empty" hidden>No tools match.</p></div></section>'
    page("tools/", "Tools", body, desc="Profiles of all 57 handbook tools with pricing, data handling, developments and sources.", crumbs=[("Tools", None)], extra_js=("filters.js",))
    add_search("All tools", "tools/", "Tools", "Catalogue of the 57 handbook tools by family")
    for g in GROUPS:
        add_search(g["name"], f"tools/#{g['slug']}", "Tool family", g["overview"])
    for i, t in enumerate(TOOLS):
        build_tool(t, i)

def build_tool(t, i):
    grp = next(g for g in GROUPS if g["name"] == t["group"])
    depts = "".join(f'<a class="chip" href="../../departments/{DEPT_BY_NUM[n]["slug"]}/">{DEPT_BY_NUM[n]["num2"]} {esc(DEPT_BY_NUM[n]["name"])}</a>' for n in t["dept_nums"]) or '<span class="muted">Not listed for any department in the handbook.</span>'
    related = "".join(f'<li><a href="../{o["slug"]}/">{esc(o["name"])}</a></li>' for o in grp["tools"] if o["name"] != t["name"])
    caps = "".join(f"<li>{esc(clean(c))}</li>" for c in t.get("key_capabilities", []))
    prev = TOOLS[i - 1] if i > 0 else None
    nxt = TOOLS[i + 1] if i + 1 < len(TOOLS) else None
    pager = '<div class="pager">' + (f'<a class="pager-prev" href="../{prev["slug"]}/"><span class="muted">Previous tool</span><b>{esc(prev["name"])}</b></a>' if prev else "<span></span>") + (f'<a class="pager-next" href="../{nxt["slug"]}/"><span class="muted">Next tool</span><b>{esc(nxt["name"])}</b></a>' if nxt else "<span></span>") + "</div>"
    meta = f'{conf_badge(t["confidence"])}<span class="badge">{esc(grp["name"])}</span><span class="badge">{len(t["dept_nums"])} departments</span>'
    actions = btn(f"../../compare/?t={t['slug']}", "Compare this tool", True, "scale") + btn("../../matrix/?tool=" + t["slug"], "Show in matrix", False, "grid")
    body = hero(esc(t["vendor_short"]), esc(t["name"]), esc(short(t["what_it_is"], 260)), actions=actions, meta=meta, cls="hero-sm")
    toc = [("learn", "Learning path and certifications"), ("what", "What it is"), ("caps", "Key capabilities"), ("data", "Enterprise data handling"), ("price", "Licensing and pricing"), ("integ", "Integrations"), ("dev", "2025-2026 developments"), ("fit", "Best-fit departments"), ("train", "Training notes"), ("caveats", "Caveats"), ("sources", "Sources")]
    cert = CERTS.get(t["name"])
    cert_intro = f'<p>{esc(clean(cert["summary"]))}</p>' if cert else ""
    cert_src = ""
    if cert and cert.get("sources"):
        cert_src = f'<details class="factcheck"><summary>Pages opened for this learning path ({len(cert["sources"])})</summary>{sources_list(cert["sources"])}</details>'
    toc_html = "".join(f'<li><a href="#{a}">{esc(l)}</a></li>' for a, l in toc)
    body += f"""
<section class="section"><div class="wrap prose-wrap">
<article class="prose detail">
  <h2 id="learn">Learning path and certifications</h2>{cert_intro}{cert_cards(t, "../../")}{cert_src}
  <h2 id="what">What it is</h2><p>{esc(clean(t['what_it_is']))}</p>
  {deflist([("Vendor and product family", esc(t['vendor_full'])), ("Handbook category", esc(t['handbook_category']))])}
  <h2 id="caps">Key capabilities</h2><ul class="ticks">{caps}</ul>
  <h2 id="data">Enterprise data handling</h2><p>{esc(clean(t['enterprise_data_handling']))}</p>
  <h2 id="price">Licensing and pricing</h2><p>{esc(clean(t['licensing_pricing']))}</p>
  <h2 id="integ">Integrations</h2><p>{esc(clean(t['integrations']))}</p>
  <h2 id="dev">2025-2026 developments</h2><p>{esc(clean(t['recent_developments']))}</p>
  <h2 id="fit">Best-fit handbook departments</h2><p>{esc(clean(t['best_fit_departments']))}</p>
  <h3>Listed for these departments in the handbook</h3><div class="chips">{depts}</div>
  <h2 id="train">Training notes</h2><p>{esc(clean(t['training_notes']))}</p>
  <h2 id="caveats">Caveats</h2><div class="callout callout-warn">{esc(clean(t['caveats']))}</div>
  <h2 id="sources">Sources</h2>{sources_list(t.get('sources'))}
</article>
<aside class="side">
  <div class="side-box sticky"><p class="foot-head">On this page</p><ul class="toc">{toc_html}</ul></div>
  <div class="side-box"><p class="foot-head">Same family</p><ul class="linklist">{related}</ul><a class="small" href="../#{grp['slug']}">All {esc(grp['name'].lower())} →</a></div>
</aside></div>
<div class="wrap">{pager}</div></section>"""
    page(f"tools/{t['slug']}/", t["name"], body, desc=t["what_it_is"], crumbs=[("Tools", "tools/"), (grp["name"], f"tools/#{grp['slug']}"), (t["name"], None)], kind="article")
    add_search(t["name"], f"tools/{t['slug']}/", "Tool", t["what_it_is"], f"t: {t['vendor_short']} {grp['name']}")

def dept_card(d, root=""):
    tools = "".join(f'<span class="chip chip-xs">{esc(x)}</span>' for x in d["tools"][:4]) + (f'<span class="chip chip-xs">+{len(d["tools"])-4}</span>' if len(d["tools"]) > 4 else "")
    return f'<a class="card card-dept reveal" href="{root}departments/{d["slug"]}/" data-tier="{d["tier"]}" data-conf="{d["confidence"]}" data-cluster="{d["cluster_slug"]}" data-name="{esc(d["name"].lower())}"><span class="dept-num">{d["num2"]}</span><h3>{esc(d["name"])}</h3><p>{esc(d["app"])}</p><div class="chips">{tools}</div><div class="card-meta">{tier_badge(d["tier"])}{conf_badge(d["confidence"])}</div></a>'

def build_departments():
    filters = '<div class="filters" id="filters"><input type="search" id="filter-q" placeholder="Filter by name…" aria-label="Filter departments"><div class="seg" role="group" aria-label="Tier"><button data-tier="" class="on">All tiers</button><button data-tier="Core">Core</button><button data-tier="Advanced">Advanced</button><button data-tier="Specialist">Specialist</button></div></div>'
    toc = "".join(f'<a class="chip" href="#{c["slug"]}">{esc(c["name"])}<span class="chip-n">{len(c["depts"])}</span></a>' for c in CLUSTERS)
    sections = ""
    for c in CLUSTERS:
        fc = f'<details class="factcheck"><summary>Fact-check notes · {c["corrections"]} corrections applied</summary><p>{esc(c["verification"])}</p></details>' if c["verification"] else ""
        sections += f'<section class="group" id="{c["slug"]}"><div class="group-head"><h2>{esc(c["name"])}</h2><p>{esc(c["overview"])}</p>{fc}</div><div class="grid grid-3">{"".join(dept_card(d, "../") for d in c["depts"])}</div></section>'
    tiers = " · ".join(f"{TIER_COUNT.get(t,0)} {t}" for t in ("Core", "Advanced", "Specialist"))
    body = hero("Department directory", "60 departments, eight clusters", f"For each department: real AI use cases with sources, a capstone that fits the handbook's assignment template, the data rules the function must follow, adoption KPIs, where the hours should go, and whether the handbook's tool list fits. {tiers}.", meta=f'<div class="chips">{toc}</div>')
    body += f'<section class="section"><div class="wrap">{filters}{sections}<p class="empty" id="empty" hidden>No departments match.</p></div></section>'
    page("departments/", "Departments", body, desc="All 60 handbook departments with AI use cases, capstones, data rules, KPIs and sources.", crumbs=[("Departments", None)], extra_js=("filters.js",))
    add_search("All departments", "departments/", "Departments", "Directory of the 60 handbook departments by cluster")
    for c in CLUSTERS:
        add_search(c["name"], f"departments/#{c['slug']}", "Cluster", c["overview"])
    for i, d in enumerate(DEPTS):
        build_dept(d, i)

def build_dept(d, i):
    cl = next(c for c in CLUSTERS if c["name"] == d["cluster"])
    tools = "".join((f'<a class="chip" href="../../tools/{TOOL_BY_NAME[x]["slug"]}/">{esc(x)}</a>' if x in TOOL_BY_NAME else f'<span class="chip">{esc(x)}</span>') for x in d["tools"])
    uses = "".join(f"<li>{esc(clean(u))}</li>" for u in d.get("ai_use_cases", []))
    sib = "".join(f'<li><a href="../{o["slug"]}/">{o["num2"]} {esc(o["name"])}</a></li>' for o in cl["depts"] if o["n"] != d["n"])
    prev = DEPTS[i - 1] if i > 0 else None
    nxt = DEPTS[i + 1] if i + 1 < len(DEPTS) else None
    pager = '<div class="pager">' + (f'<a class="pager-prev" href="../{prev["slug"]}/"><span class="muted">Previous</span><b>{prev["num2"]} {esc(prev["name"])}</b></a>' if prev else "<span></span>") + (f'<a class="pager-next" href="../{nxt["slug"]}/"><span class="muted">Next</span><b>{nxt["num2"]} {esc(nxt["name"])}</b></a>' if nxt else "<span></span>") + "</div>"
    meta = f'{tier_badge(d["tier"])}{conf_badge(d["confidence"])}<span class="badge">{esc(cl["name"])}</span>'
    actions = btn(f"../../compare/?d={d['slug']}", "Compare this department", True, "scale") + btn(f"../../matrix/?dept={d['num2']}", "Show in matrix", False, "grid")
    toc = [("tools", "Recommended tools"), ("path", "What to learn, in order"), ("uses", "AI use cases in practice"), ("capstone", "Capstone deliverable"), ("data", "Data risks and rules"), ("kpis", "Adoption KPIs"), ("curriculum", "Curriculum emphasis"), ("fit", "Tool-list fit"), ("sources", "Sources")]
    path_html, path_total = dept_path(d, "../../")
    toc_html = "".join(f'<li><a href="#{a}">{esc(l)}</a></li>' for a, l in toc)
    body = hero(f"Department {d['num2']} · {esc(cl['name'])}", esc(d["name"]), esc(d["app"]), actions=actions, meta=meta, cls="hero-sm")
    body += f"""
<section class="section"><div class="wrap prose-wrap">
<article class="prose detail">
  <h2 id="tools">Recommended tools</h2><p class="muted">From the handbook. Tier {esc(d['tier'])}, {TIER_HOURS[d['tier']]} per tool as a planning band.</p><div class="chips chips-lg">{tools}</div>
  <h2 id="path">What to learn, in order</h2><p class="muted">Foundation first, then the general assistant, then the productivity surfaces, then the specialist platform. Each step links to the tool's official courses and certifications. Planning total: about {path_total} including the shared foundation module, less overlaps within one licence.</p>{path_html}
  <h2 id="uses">AI use cases in practice</h2><ul class="ticks">{uses}</ul>
  <h2 id="capstone">Capstone deliverable</h2><div class="callout callout-info">{esc(clean(d['capstone_deliverable']))}</div>
  <h2 id="data">Data risks and rules</h2><div class="callout callout-warn">{esc(clean(d['data_risks']))}</div>
  <h2 id="kpis">Adoption KPIs</h2><p>{esc(clean(d['adoption_kpis']))}</p>
  <h2 id="curriculum">Curriculum emphasis</h2><p>{esc(clean(d['curriculum_emphasis']))}</p>
  <h2 id="fit">Tool-list fit</h2><p>{esc(clean(d['tool_fit_commentary']))}</p>
  <h2 id="sources">Sources</h2>{sources_list(d.get('sources'))}
</article>
<aside class="side">
  <div class="side-box sticky"><p class="foot-head">On this page</p><ul class="toc">{toc_html}</ul></div>
  <div class="side-box"><p class="foot-head">Same cluster</p><ul class="linklist">{sib}</ul></div>
</aside></div>
<div class="wrap">{pager}</div></section>"""
    page(f"departments/{d['slug']}/", f"{d['num2']} {d['name']}", body, desc=f"{d['name']}: {d['app']}", crumbs=[("Departments", "departments/"), (cl["name"], f"departments/#{cl['slug']}"), (f"{d['num2']} {d['name']}", None)], kind="article")
    add_search(f"{d['num2']} {d['name']}", f"departments/{d['slug']}/", "Department", d["app"], f"d: {cl['name']} {d['tier']}")

def build_more_tools():
    lenses = sorted({t["category"] for t in ADD_TOOLS})
    lens_chips = "".join(f'<button class="chip chip-btn" data-lens="{esc(l)}">{esc(l)}</button>' for l in lenses)
    cards = ""
    for t in ADD_TOOLS:
        deps = "".join(f'<span class="chip chip-xs">{esc(x)}</span>' for x in t.get("suggested_departments", [])[:5])
        srcs = sources_list(t.get("sources"))
        cards += f"""<details class="more-card reveal" id="{t['slug']}" data-lens="{esc(t['category'])}" data-conf="{t['confidence']}" data-name="{esc(t['name'].lower())}">
<summary><div><h3>{esc(t['name'])}</h3><p class="muted small">{esc(short(t['vendor'], 70))} · {esc(t['category'])}</p></div><div class="card-meta">{badge('tier-'+t['suggested_tier'].lower(), t['suggested_tier'])}{conf_badge(t['confidence'])}<span class="badge">Pass {t['pass_no']}</span></div></summary>
<div class="more-body"><p>{esc(clean(t['what_it_is']))}</p>{deflist([("Why include", esc(clean(t['why_include']))), ("Overlaps with", esc(clean(t['overlaps_with']))), ("Enterprise data note", esc(clean(t['enterprise_data_note'])))])}<p class="foot-head">Suggested departments</p><div class="chips">{deps}</div>{srcs}</div></details>"""
    body = hero("Beyond the handbook", f"{len(ADD_TOOLS)} more tools large organisations run", "Found in two research passes, each candidate fact-checked against pages a researcher opened and de-duplicated against the handbook's 57. Most adoption evidence is vendor-reported analyst placements, so confidence clusters at medium.", meta=f'<div class="chips" id="lens-chips"><button class="chip chip-btn on" data-lens="">All lenses</button>{lens_chips}</div>')
    body += f'<section class="section"><div class="wrap"><div class="filters" id="filters"><input type="search" id="filter-q" placeholder="Filter by name…" aria-label="Filter"><div class="seg" role="group"><button data-conf="" class="on">All</button><button data-conf="high">High</button><button data-conf="medium">Medium</button><button data-conf="low">Low</button></div></div><div class="more-list">{cards}</div><p class="empty" id="empty" hidden>Nothing matches.</p></div></section>'
    page("tools/more/", "More tools", body, desc=f"{len(ADD_TOOLS)} widely adopted enterprise AI tools absent from the handbook, with evidence and suggested departments.", crumbs=[("Tools", "tools/"), ("More tools", None)], extra_js=("filters.js",))
    for t in ADD_TOOLS:
        add_search(t["name"], f"tools/more/#{t['slug']}", "Additional tool", t["what_it_is"], f"t: {t['vendor']} {t['category']}")

def build_more_depts():
    lenses = []
    for r in RUN["additionalDepartments"]["runs"] + MORE_D["runs"]:
        lenses.append(r["lens"])
    cards = ""
    for d in ADD_DEPTS:
        tools = "".join(f'<span class="chip chip-xs">{esc(x)}</span>' for x in d.get("recommended_tools", []))
        cards += f"""<details class="more-card reveal" id="{d['slug']}" data-conf="{d['confidence']}" data-tier="{d['suggested_tier']}" data-name="{esc(d['name'].lower())}">
<summary><div><h3>{esc(d['name'])}</h3><p class="muted small">{esc(short(d['typical_org_types'], 90))}</p></div><div class="card-meta">{badge('tier-'+d['suggested_tier'].lower(), d['suggested_tier'])}{conf_badge(d['confidence'])}<span class="badge">Pass {d['pass_no']}</span></div></summary>
<div class="more-body">{deflist([("Why it is missing", esc(clean(d['why_missing']))), ("Workplace application", esc(clean(d['workplace_application']))), ("Evidence of AI use", esc(clean(d['ai_use_evidence']))), ("Data risks", esc(clean(d['data_risks'])))])}<p class="foot-head">Recommended tools</p><div class="chips">{tools}</div>{sources_list(d.get('sources'))}</div></details>"""
    body = hero("Beyond the handbook", f"{len(ADD_DEPTS)} more functions with documented AI use", "Functions large organisations commonly staff that the handbook's 60 departments do not cover, found under seven research lenses, fact-checked and de-duplicated. Each carries a starting tool list, the evidence, and the data it handles.")
    body += f'<section class="section"><div class="wrap"><div class="filters" id="filters"><input type="search" id="filter-q" placeholder="Filter by name…" aria-label="Filter"><div class="seg" role="group"><button data-tier="" class="on">All tiers</button><button data-tier="Core">Core</button><button data-tier="Advanced">Advanced</button><button data-tier="Specialist">Specialist</button></div></div><div class="more-list">{cards}</div><p class="empty" id="empty" hidden>Nothing matches.</p></div></section>'
    page("departments/more/", "More functions", body, desc=f"{len(ADD_DEPTS)} functions absent from the handbook's 60 departments, with AI-use evidence and tool suggestions.", crumbs=[("Departments", "departments/"), ("More functions", None)], extra_js=("filters.js",))
    for d in ADD_DEPTS:
        add_search(d["name"], f"departments/more/#{d['slug']}", "Additional function", d["workplace_application"], f"d: {d['typical_org_types']}")

def build_certs():
    """Index of every course and certification, grouped by tool family."""
    if not CERTS:
        return
    n_paths = sum(len(c.get("paths", [])) for c in CERTS.values())
    n_cert = sum(1 for c in CERTS.values() for p in c.get("paths", []) if p["kind"] == "certification")
    toc = "".join(f'<a class="chip" href="#{g["slug"]}">{esc(g["name"])}</a>' for g in GROUPS)
    sections = ""
    for g in GROUPS:
        cg = next((x for x in CERT_GROUPS if x["group"] == g["name"]), None)
        head = f'<div class="group-head"><h2>{esc(g["name"])}</h2>' + (f'<p>{esc(cg["overview"])}</p>' if cg and cg["overview"] else "") + (f'<details class="factcheck"><summary>Fact-check notes · {cg["corrections"]} corrections applied</summary><p>{esc(cg["verification"])}</p></details>' if cg and cg["verification"] else "") + "</div>"
        cards = ""
        for t in g["tools"]:
            c = CERTS.get(t["name"])
            if not c: continue
            rows = "".join(f'<tr data-kind="{esc(p["kind"])}" data-level="{esc(p["level"])}"><td><a href="{esc(p["url"])}" rel="noopener" target="_blank">{esc(clean(p["title"]))}</a><br><span class="muted small">{esc(clean(p["provider"]))}</span></td><td>{esc(KIND_LABEL.get(p["kind"], p["kind"]))}</td><td>{esc(p["level"])}</td><td>{esc(p["duration"])}</td><td>{esc(p["cost"])}</td><td>{"<span class=\'badge badge-conf-high\'>Verified</span>" if p.get("verified") else "<span class=\'badge badge-conf-low\'>Not verified</span>"}</td></tr>' for p in c.get("paths", []))
            cards += f'<details class="more-card cert-card" id="{t["slug"]}" data-name="{esc(t["name"].lower())}" open><summary><div><h3>{esc(t["name"])}</h3><p class="muted small">{esc(short(c.get("summary", ""), 160))}</p></div><div class="card-meta">{conf_badge(c.get("confidence", "medium"))}<span class="badge">{len(c.get("paths", []))} paths</span><a class="chip chip-xs" href="../../tools/{t["slug"]}/#learn">Tool page</a></div></summary><div class="more-body"><div class="table-scroll"><table class="data"><thead><tr><th>Course or credential</th><th>Type</th><th>Level</th><th>Duration</th><th>Cost</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div></div></details>'
        sections += f'<section class="group" id="{g["slug"]}">{head}<div class="more-list">{cards}</div></section>'
    body = hero("Learning path", "Courses and certifications for every tool", f"{n_paths} official courses, learning paths, documentation hubs and {n_cert} formal certifications across the 57 tools, each opened and checked by a researcher. Start with the foundation course for the tool you have, then the role course, then the credential.", meta=f'<div class="chips">{toc}</div>')
    body += f'<section class="section"><div class="wrap"><div class="filters" id="filters"><input type="search" id="filter-q" placeholder="Filter by tool…" aria-label="Filter"><div class="seg" role="group"><button data-kind="" class="on">All types</button><button data-kind="certification">Certifications</button><button data-kind="course">Courses</button><button data-kind="learning path">Learning paths</button></div></div>{sections}<p class="empty" id="empty" hidden>Nothing matches.</p></div></section>'
    page("learn/certifications/", "Courses and certifications", body, desc=f"{n_paths} official courses and {n_cert} certifications for the 57 handbook tools, verified against vendor pages.", crumbs=[("Learn", "learn/"), ("Courses and certifications", None)], extra_js=("filters.js", "certs.js"))
    add_search("Courses and certifications", "learn/certifications/", "Learn", "Official courses, learning paths and certifications for every tool")
    for name, c in CERTS.items():
        t = TOOL_BY_NAME.get(name)
        if not t: continue
        for p in c.get("paths", []):
            if p["kind"] == "certification":
                add_search(clean(p["title"]), f"learn/certifications/#{t['slug']}", "Certification", f"{p['provider']} · {p['level']} · {name}", f"cert {name}")

def build_matrix():
    data = {
        "groups": [g["name"] for g in GROUPS],
        "clusters": [c["name"] for c in CLUSTERS],
        "tools": [{"n": t["name"], "s": t["slug"], "g": GROUPS.index(next(g for g in GROUPS if g["name"] == t["group"])), "c": t["confidence"]} for t in TOOLS],
        "depts": [{"n": d["n"], "name": d["name"], "s": d["slug"], "t": d["tier"], "c": CLUSTERS.index(next(c for c in CLUSTERS if c["name"] == d["cluster"])), "conf": d["confidence"], "tools": [TOOL_INDEX[x] for x in d["tools"] if x in TOOL_INDEX]} for d in DEPTS],
    }
    body = hero("Coverage matrix", "Who uses what, at a glance", "Start high: eight clusters against ten tool families, coloured by how many department-tool recommendations fall in each cell. Then drill into the full 60-by-57 grid, filter by tier or family, and click any cell to open the department or the tool.", cls="hero-sm")
    body += """
<section class="section"><div class="wrap">
<div class="matrix-controls">
  <div class="seg" role="group" aria-label="View"><button data-view="high" class="on">High level</button><button data-view="detail">Detailed grid</button></div>
  <div class="seg" role="group" aria-label="Tier"><button data-tier="" class="on">All tiers</button><button data-tier="Core">Core</button><button data-tier="Advanced">Advanced</button><button data-tier="Specialist">Specialist</button></div>
  <select id="m-group" aria-label="Tool family"><option value="">All tool families</option></select>
  <select id="m-cluster" aria-label="Cluster"><option value="">All clusters</option></select>
  <label class="check"><input type="checkbox" id="m-horiz"> Hide the six general assistants</label>
</div>
<p class="muted small" id="m-summary"></p>
<div class="matrix-scroll"><div id="matrix" role="grid" aria-label="Coverage matrix"></div></div>
<div class="legend" id="legend"></div>
<div class="m-panel" id="m-panel" hidden></div>
</div></section>
<section class="section section-alt"><div class="wrap split">
  <div><h2 class="section-title">How to read it</h2><p>A filled cell means the handbook recommends that tool for that department. Darker cells in the high-level view mean more recommendations between a cluster and a tool family. The six general assistants dominate every row; hide them to see the specialist pattern underneath.</p></div>
  <div><h2 class="section-title">What it is for</h2><p>Rationalising licences (which families cover which clusters), planning shared modules (clusters that share families can train together), and spotting gaps (clusters with no specialist platform at all). Confidence and hours live on the detail pages.</p></div>
</div></section>"""
    extra = f'<script id="matrix-data" type="application/json">{json.dumps(data, separators=(",", ":"))}</script>'
    page("matrix/", "Matrix", body, desc="Interactive department-by-tool coverage matrix for the 60 departments and 57 tools.", crumbs=[("Matrix", None)], extra_head=extra, extra_js=("matrix.js",), kind="app")
    add_search("Coverage matrix", "matrix/", "Matrix", "Interactive 60 by 57 department-by-tool coverage matrix")

def build_compare():
    tools = [{
        "s": t["slug"], "n": t["name"], "v": t["vendor_short"], "g": t["group"], "c": t["confidence"], "nd": len(t["dept_nums"]),
        "what": clean(t["what_it_is"]), "data": clean(t["enterprise_data_handling"]), "price": clean(t["licensing_pricing"]),
        "integ": clean(t["integrations"]), "dev": clean(t["recent_developments"]), "fit": clean(t["best_fit_departments"]),
        "train": clean(t["training_notes"]), "cav": clean(t["caveats"]), "caps": [clean(c) for c in t.get("key_capabilities", [])],
    } for t in TOOLS]
    depts = [{
        "s": d["slug"], "n": f"{d['num2']} {d['name']}", "tier": d["tier"], "cl": d["cluster"], "c": d["confidence"], "tools": d["tools"], "app": d["app"],
        "cap": clean(d["capstone_deliverable"]), "risk": clean(d["data_risks"]), "kpi": clean(d["adoption_kpis"]), "cur": clean(d["curriculum_emphasis"]),
    } for d in DEPTS]
    presets = [
        ("General assistants", ["gemini", "claude", "chatgpt-enterprise", "perplexity-enterprise"]),
        ("Coding assistants", ["claude-code", "github-copilot", "cursor", "gemini-code-assist"]),
        ("SOC agents", ["microsoft-security-copilot", "crowdstrike-charlotte-ai", "google-gemini-in-security"]),
        ("Observability", ["datadog-bits-ai", "dynatrace-davis-ai", "azure-copilot"]),
        ("Data platforms", ["databricks-assistant", "snowflake-cortex-ai", "tableau-pulse", "power-bi-copilot"]),
        ("AI platforms", ["azure-ai-foundry", "amazon-bedrock", "google-ai-studio", "mlflow"]),
        ("Business platforms", ["servicenow-now-assist", "salesforce-einstein", "sap-joule", "workday-ai"]),
        ("Customer service", ["zendesk-ai", "intercom-fin", "gainsight-ai", "qualtrics-ai"]),
    ]
    body = hero("Compare", "Side by side, up to four at once", "Pick tools to compare pricing models, data handling, confidence and department fit. Or switch to departments to compare tiers, tool lists, capstones and data rules. Share the URL to keep the selection.", cls="hero-sm")
    body += f"""
<section class="section"><div class="wrap">
<div class="seg seg-lg" role="group" aria-label="Compare what"><button data-mode="tools" class="on">Tools</button><button data-mode="depts">Departments</button></div>
<div class="cmp-pick">
  <div class="cmp-search"><input id="cmp-q" type="search" placeholder="Add a tool…" aria-label="Add item" autocomplete="off"><ul id="cmp-suggest" class="suggest" hidden></ul></div>
  <div class="chips" id="cmp-selected"></div>
</div>
<div class="presets" id="presets"><span class="muted small">Presets:</span>{''.join(f'<button class="chip chip-btn" data-preset="{",".join(p)}">{esc(n)}</button>' for n, p in presets)}</div>
<div class="cmp-scroll"><table class="cmp" id="cmp-table"></table></div>
<p class="empty" id="cmp-empty">Add two or more items to compare.</p>
</div></section>"""
    extra = f'<script id="compare-data" type="application/json">{json.dumps({"tools": tools, "depts": depts}, separators=(",", ":"))}</script>'
    page("compare/", "Compare", body, desc="Compare handbook AI tools or departments side by side: pricing, data handling, confidence, fit.", crumbs=[("Compare", None)], extra_head=extra, extra_js=("compare.js",), kind="app")
    add_search("Compare tools and departments", "compare/", "Compare", "Side-by-side comparison of up to four tools or departments")

def build_reference():
    # themes
    body = hero("Reference", "Cross-cutting themes", "The topics every department shares, consolidated so the curriculum teaches each once: regulation, data residency, cost models and overlap, verification and agent safety, adoption and ROI, accessibility, tiering.", cls="hero-sm")
    html_ = md(C.THEMES_MD)
    toc = "".join(f'<li><a href="#{slugify(h)}">{esc(h)}</a></li>' for h in re.findall(r"^## (.+)$", C.THEMES_MD, flags=re.M))
    html_ = re.sub(r"<h2>(.+?)</h2>", lambda m: f'<h2 id="{slugify(html.unescape(m.group(1)))}">{m.group(1)}</h2>', html_)
    body += f'<section class="section"><div class="wrap prose-wrap"><article class="prose">{html_}</article><aside class="side"><div class="side-box sticky"><p class="foot-head">On this page</p><ul class="toc">{toc}</ul></div></aside></div></section>'
    page("themes/", "Cross-cutting themes", body, desc="Regulation, data residency, licensing cost models, hallucination and prompt injection, shadow AI, adoption, accessibility and hours.", crumbs=[("Reference", None), ("Themes", None)], kind="article")
    add_search("Cross-cutting themes", "themes/", "Reference", "Regulation, residency, cost, verification, adoption, accessibility, hours")
    # gaps
    rows = "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td><td>{esc(c)}</td><td>{esc(d)}</td></tr>" for a, b, c, d in C.RENAMES)
    table = f'<h2 id="renames">Handbook names that are out of date</h2><p>Use the current name with the handbook name in brackets. Rows marked verified were confirmed on a page an agent opened.</p><div class="table-scroll"><table class="data"><thead><tr><th>Handbook name</th><th>Current name or status</th><th>Effective</th><th>Verification</th></tr></thead><tbody>{rows}</tbody></table></div>'
    html_ = md(C.GAPS_MD)
    html_ = re.sub(r"<h2>(.+?)</h2>", lambda m: f'<h2 id="{slugify(html.unescape(m.group(1)))}">{m.group(1)}</h2>', html_)
    html_ = html_.replace('<h2 id="caveats-that-apply-to-the-whole-site">', table + '<h2 id="caveats-that-apply-to-the-whole-site">')
    heads = re.findall(r"^## (.+)$", C.GAPS_MD, flags=re.M)
    heads.insert(2, "Handbook names that are out of date")
    toc = "".join(f'<li><a href="#{"renames" if h.startswith("Handbook names") else slugify(h)}">{esc(h)}</a></li>' for h in heads)
    body = hero("Reference", "Gaps, caveats and recommendations", "Where the research is thin, which names have changed, and the decisions that shape a curriculum and a matrix built from it.", cls="hero-sm")
    body += f'<section class="section"><div class="wrap prose-wrap"><article class="prose">{html_}</article><aside class="side"><div class="side-box sticky"><p class="foot-head">On this page</p><ul class="toc">{toc}</ul></div></aside></div></section>'
    page("gaps/", "Gaps and renames", body, desc="Confidence ratings, outdated tool names, caveats and recommendations for curriculum and matrix design.", crumbs=[("Reference", None), ("Gaps and renames", None)], kind="article")
    add_search("Gaps, caveats and renames", "gaps/", "Reference", "Confidence table, 20 outdated names, recommendations")
    # sources
    secs = ""
    for s in SOURCES:
        inner = ""
        if s["items"]:
            inner += "<ul class='srcs'>" + "".join(f'<li><a href="{esc(u)}" rel="noopener nofollow" target="_blank">{esc(t)}</a> <span class="muted small">{esc(re.sub(r"^https?://(www\.)?", "", u).split("/")[0])}</span></li>' for t, u in s["items"]) + "</ul>"
        for g in s["groups"]:
            inner += f'<details class="src-group"><summary>{esc(g["title"])} <span class="muted">({len(g["items"])})</span></summary><ul class="srcs">' + "".join(f'<li><a href="{esc(u)}" rel="noopener nofollow" target="_blank">{esc(t)}</a> <span class="muted small">{esc(re.sub(r"^https?://(www\.)?", "", u).split("/")[0])}</span></li>' for t, u in g["items"]) + "</ul></details>"
        secs += f'<h2 id="{slugify(s["title"])}">{esc(s["title"])}</h2>{inner}'
    body = hero("Reference", f"Sources and method", f"{N_SOURCES} pages opened and cited, how the research was run, and what each verification label means.", cls="hero-sm")
    body += f'<section class="section"><div class="wrap prose-wrap"><article class="prose">{md(C.METHOD_MD)}<h2 id="all">Every page cited</h2><input type="search" id="src-filter" class="src-filter" placeholder="Filter sources by title or domain…" aria-label="Filter sources">{secs}</article><aside class="side"><div class="side-box sticky"><p class="foot-head">Sections</p><ul class="toc"><li><a href="#how-the-research-was-done">Method</a></li><li><a href="#verification-labels">Labels</a></li><li><a href="#known-failures">Known failures</a></li>{"".join(f"<li><a href=\'#{slugify(s["title"])}\'>{esc(s["title"].replace("Pages opened for the ", "").capitalize())}</a></li>" for s in SOURCES)}</ul></div></aside></div></section>'
    page("sources/", "Sources and method", body, desc=f"All {N_SOURCES} pages opened in the research, the method, and the verification labels.", crumbs=[("Reference", None), ("Sources", None)], kind="article", extra_js=("sources.js",))
    add_search("Sources and method", "sources/", "Reference", f"All {N_SOURCES} pages opened, method and labels")
    # about
    body = hero("Reference", "About this site", C.TAGLINE, cls="hero-sm") + f'<section class="section"><div class="wrap prose-wrap"><article class="prose">{md(C.ABOUT_MD)}<p>{btn(C.DOC_URL, "Open the long-form document")} {btn(C.REPO_URL, "View the research repository")}</p></article></div></section>'
    page("about/", "About", body, desc="What this site is, who it is for, and how to keep it current.", crumbs=[("Reference", None), ("About", None)], kind="article")
    add_search("About", "about/", "Reference", "What this site is and how to use it")

def build_misc():
    body = hero("404", "That page is not here", "The address may have changed when a tool or department was renamed. Try search, or start from one of these.", actions=btn("", "Home", True) + btn("tools/", "Tools") + btn("departments/", "Departments"), cls="hero-sm")
    page("404.html", "Not found", body, kind="page")
    SITEMAP.pop()
    (OUT / "search.json").write_text(json.dumps(SEARCH, separators=(",", ":")), encoding="utf-8")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{esc(u)}</loc></url>" for u in SITEMAP) + "</urlset>", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}sitemap.xml\n", encoding="utf-8")
    (OUT / "manifest.webmanifest").write_text(json.dumps({"name": C.SITE_NAME, "short_name": "AI Handbook", "start_url": "./", "display": "standalone", "background_color": "#0b1020", "theme_color": "#0b1020", "icons": [{"src": "assets/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}), encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(HERE / "assets", OUT / "assets")
    build_home()
    build_learn()
    build_tools()
    build_more_tools()
    build_departments()
    build_more_depts()
    build_certs()
    build_matrix()
    build_compare()
    build_reference()
    build_misc()
    n = sum(1 for _ in OUT.rglob("index.html"))
    print(f"built {n} pages, {len(SEARCH)} search entries, {N_SOURCES} sources -> {OUT}")

if __name__ == "__main__":
    main()
