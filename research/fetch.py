#!/usr/bin/env python3
"""Open a web page through the session's egress proxy and print it as plain text.

Usage: python3 -I research/fetch.py <url> [max_chars] [offset]

Downloads with curl (which honours HTTPS_PROXY and the proxy CA bundle), strips
scripts, styles and tags, collapses whitespace and prints up to max_chars
(default 12000) starting at offset (default 0). The final HTTP status and the
final URL are printed on the first line so a redirect or a block is visible.
Exit code is non-zero when the page could not be opened, so a failed open is
never mistaken for an opened page.
"""
import html
import re
import subprocess
import sys
import tempfile
import os


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    url = sys.argv[1]
    max_chars = int(sys.argv[2]) if len(sys.argv) > 2 else 12000
    offset = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    fd, body_path = tempfile.mkstemp(prefix="fetch_", suffix=".html")
    os.close(fd)
    try:
        cmd = [
            "curl", "-sS", "-L", "--max-time", "45", "--max-redirs", "8",
            "-A", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36",
            "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "-H", "Accept-Language: en-US,en;q=0.9",
            "-o", body_path, "-w", "%{http_code} %{url_effective} %{content_type}", url,
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        meta = (res.stdout or "").strip()
        if res.returncode != 0:
            print(f"FAILED to open {url}: curl exit {res.returncode}: {res.stderr.strip()[:300]}")
            sys.exit(1)
        parts = meta.split(" ", 2)
        status = parts[0] if parts else "000"
        final_url = parts[1] if len(parts) > 1 else url
        ctype = parts[2] if len(parts) > 2 else ""
        raw = open(body_path, "rb").read()
        if not status.startswith("2"):
            print(f"FAILED to open {url}: HTTP {status} (final URL {final_url}); body {len(raw)} bytes")
            sys.exit(1)
        text = raw.decode("utf-8", errors="replace")
        if "html" in ctype or text.lstrip()[:1] == "<":
            text = re.sub(r"(?is)<(script|style|noscript|svg|head)[^>]*>.*?</\1>", " ", text)
            text = re.sub(r"(?i)<br\s*/?>|</(p|div|li|tr|h[1-6]|section|article|table|ul|ol|blockquote)>", "\n", text)
            text = re.sub(r"(?s)<[^>]+>", " ", text)
            text = html.unescape(text)
        text = re.sub(r"[ \t\r\f\v]+", " ", text)
        text = re.sub(r"\n\s*\n+", "\n", text).strip()
        total = len(text)
        print(f"OPENED {final_url} (HTTP {status}, {total} chars of text; showing {offset}-{min(offset + max_chars, total)})")
        print(text[offset:offset + max_chars])
        if offset + max_chars < total:
            print(f"\n[... {total - offset - max_chars} more chars; rerun with offset {offset + max_chars} to continue]")
    finally:
        try:
            os.unlink(body_path)
        except OSError:
            pass


if __name__ == "__main__":
    main()
