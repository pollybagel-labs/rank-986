#!/usr/bin/env python3
"""
Local dev server — no Vercel CLI needed.
Serves static files AND proxies live Bing image search via /api/images.
Stdlib only — no pip install required.

Run:  python3 server.py
Open: http://localhost:3849
"""

import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn

PORT = 3849
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/121.0.0.0 Safari/537.36")


def fetch_bing_images(query: str, page: int = 1, count: int = 35):
    first = (page - 1) * count + 1
    url = (
        "https://www.bing.com/images/async"
        f"?q={urllib.parse.quote(query)}"
        f"&first={first}&count={count}&relp={count}"
        "&scenario=ImageBasicHover&datsrc=I&layout=ColumnBased&mmasync=1"
    )
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=12) as resp:
        body = resp.read().decode("utf-8", errors="ignore")

    results = []
    seen = set()
    for match in re.finditer(r'class="iusc"[^>]*?\sm="([^"]+)"', body):
        raw = html.unescape(match.group(1))
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        full = data.get("murl")
        if not full or full in seen:
            continue
        seen.add(full)
        results.append({
            "thumb": data.get("turl") or full,
            "full": full,
            "title": (data.get("t") or "").strip(),
            "source": data.get("purl") or "",
        })
    return results


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write(f"  · {self.address_string()} — {fmt % args}\n")

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/images":
            return self._serve_images(parsed.query)
        # Pretty root: serve index.html for "/"
        if parsed.path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def _serve_images(self, qs: str):
        params = urllib.parse.parse_qs(qs)
        q = (params.get("q") or [""])[0].strip()
        try:
            page = max(1, int((params.get("page") or ["1"])[0]))
        except ValueError:
            page = 1
        if not q:
            return self._json(400, {"error": "missing q"})
        try:
            results = fetch_bing_images(q, page=page)
            return self._json(200, {"query": q, "page": page, "results": results})
        except Exception as e:
            return self._json(502, {"error": f"upstream failed: {e}"})

    def _json(self, status: int, payload: dict):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "public, max-age=300")
        self.end_headers()
        self.wfile.write(body)


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = ThreadingHTTPServer(("localhost", PORT), Handler)
    print(f"  · serving http://localhost:{PORT}/")
    print("  · ctrl-c to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  · stopped")
