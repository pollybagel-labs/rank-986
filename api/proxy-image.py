"""
Vercel serverless function — proxies external images so they can be drawn
into a same-origin canvas. Without this, cross-origin pinned photos (e.g. Bing
CDN) load fine for display but taint the canvas, breaking toDataURL().

Endpoint: GET /api/proxy-image?url=<absolute_image_url>
Returns:  the image bytes with the upstream Content-Type and
          Access-Control-Allow-Origin: *
"""

import ipaddress
import socket
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler

# Wikimedia and other hosts reject generic Chrome UAs from server-side fetches.
# Use a descriptive UA per their policy — works for Wikimedia, Bing, etc.
UA = "Mozilla/5.0 (compatible; rank-986/1.0; +https://github.com/pollybagel-labs/rank-986)"

MAX_BYTES = 10 * 1024 * 1024  # 10 MB
TIMEOUT = 10
ALLOWED_SCHEMES = ("http", "https")


def is_safe_target(url: str):
    """Reject URLs pointing to internal/private addresses (SSRF guard)."""
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:
        return False, "unparseable url"
    if parsed.scheme not in ALLOWED_SCHEMES:
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


def fetch_image(url: str):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "image/*",
    })
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip()
        if not ctype.startswith("image/"):
            raise ValueError(f"not an image: {ctype or 'unknown'}")
        body = resp.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise ValueError("image too large")
    return ctype, body


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        target = (params.get("url") or [""])[0].strip()

        if not target:
            return self._error(400, "missing url")

        ok, reason = is_safe_target(target)
        if not ok:
            return self._error(400, reason)

        try:
            ctype, body = fetch_image(target)
        except urllib.error.HTTPError as e:
            return self._error(502, f"upstream {e.code}")
        except ValueError as e:
            return self._error(415, str(e))
        except Exception as e:
            return self._error(502, f"upstream failed: {e}")

        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "public, max-age=86400")
        self.end_headers()
        self.wfile.write(body)

    def _error(self, status: int, msg: str):
        body = msg.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass
