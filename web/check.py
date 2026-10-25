#!/usr/bin/env python3
"""Checks the built site in docs/: internal links resolve and no page has duplicate ids."""
import re, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent / "docs"
bad = dups = total = 0
for html in root.rglob("*.html"):
    text = html.read_text(encoding="utf-8")
    for m in re.finditer(r'(?:href|src)="([^"#?]+)(?:[?#][^"]*)?"', text):
        u = m.group(1)
        if not u or u.startswith(("http", "mailto:", "//")): continue
        total += 1
        p = (root / u.lstrip("/")) if u.startswith("/") else (html.parent / u)
        p = p.resolve()
        if p.is_dir(): p = p / "index.html"
        if not p.exists():
            bad += 1; print(f"BROKEN {html.relative_to(root)} -> {u}")
    ids = re.findall(r' id="([^"]+)"', text)
    seen, d = set(), []
    for i in ids:
        (d.append(i) if i in seen else seen.add(i))
    if d:
        dups += 1; print(f"DUPLICATE IDS {html.relative_to(root)}: {sorted(set(d))[:5]}")
print(f"{total} internal links checked, {bad} broken; {dups} pages with duplicate ids")
sys.exit(1 if bad or dups else 0)
