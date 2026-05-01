"""
Vercel serverless function — proxies Bing image search.

Endpoint: GET /api/images?q=<query>&page=<n>
Returns:  { query, page, results: [{thumb, full, title, source}, ...] }
"""

import html
import json
import re
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler

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
    with urllib.request.urlopen(req, timeout=10) as resp:
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


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
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
        self.send_header("Cache-Control", "public, max-age=600")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass
