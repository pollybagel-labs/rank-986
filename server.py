#!/usr/bin/env python3
"""
Local dev server — no Vercel CLI needed.
Serves static files AND proxies:
  · live Bing image search via /api/images
  · external image bytes (CORS-friendly) via /api/proxy-image
Stdlib only — no pip install required.

Run:  python3 server.py
Open: http://localhost:3849
"""

import html
import ipaddress
import json
import os
import re
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn

PORT = 3849
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/121.0.0.0 Safari/537.36")
# Wikimedia and other hosts reject generic Chrome UAs from server-side fetches —
# they want a descriptive bot UA. The Bing-search proxy still uses the Chrome UA
# (Bing serves richer HTML to it). The image proxy uses a project-identifying UA.
PROXY_UA = "Mozilla/5.0 (compatible; rank-986/1.0; +https://github.com/pollybagel-labs/rank-986)"
PROXY_MAX_BYTES = 10 * 1024 * 1024
PROXY_TIMEOUT = 10
PROXY_ALLOWED_SCHEMES = ("http", "https")


def proxy_target_ok(url: str):
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:
        return False, "unparseable url"
    if parsed.scheme not in PROXY_ALLOWED_SCHEMES:
        return False, "scheme not allowed"
    if not parsed.hostname:
        return False, "no hostname"
    try:
        infos = socket.getaddrinfo(parsed.hostname, None)
    except socket.gaierror:
        return False, "dns failure"
    for info in infos:
        addr = info[4][0]
        try:
            ip = ipaddress.ip_address(addr)
        except ValueError:
            continue
        if (ip.is_private or ip.is_loopback or ip.is_link_local
                or ip.is_reserved or ip.is_multicast):
            return False, "private address"
    return True, ""


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
        if parsed.path == "/api/proxy-image":
            return self._serve_proxy_image(parsed.query)
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

    def _serve_proxy_image(self, qs: str):
        params = urllib.parse.parse_qs(qs)
        target = (params.get("url") or [""])[0].strip()
        if not target:
            return self._text(400, "missing url")
        ok, reason = proxy_target_ok(target)
        if not ok:
            return self._text(400, reason)
        try:
            req = urllib.request.Request(target, headers={
                "User-Agent": PROXY_UA,
                "Accept": "image/*",
            })
            with urllib.request.urlopen(req, timeout=PROXY_TIMEOUT) as resp:
                ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip()
                if not ctype.startswith("image/"):
                    return self._text(415, f"not an image: {ctype or 'unknown'}")
                body = resp.read(PROXY_MAX_BYTES + 1)
                if len(body) > PROXY_MAX_BYTES:
                    return self._text(413, "image too large")
        except urllib.error.HTTPError as e:
            return self._text(502, f"upstream {e.code}")
        except Exception as e:
            return self._text(502, f"upstream failed: {e}")
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "public, max-age=86400")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, payload: dict):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "public, max-age=300")
        self.end_headers()
        self.wfile.write(body)

    def _text(self, status: int, msg: str):
        body = msg.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
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
