import os

from flask import Flask, render_template, request

from urllib.parse import urlsplit
from html.parser import HTMLParser

import requests
from transport import FixtureOnlyAdapter

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4096
PARTNER_PORT = os.environ.get("PARTNER_PORT", "8012")
PUBLIC_ORIGINS = {f"localhost:{PARTNER_PORT}", f"127.0.0.1:{PARTNER_PORT}"}
session = requests.Session()
session.trust_env = False
session.max_redirects = 4
session.mount("http://", FixtureOnlyAdapter())
session.mount("https://", FixtureOnlyAdapter())


@app.get("/")
def index():
    host = "127.0.0.1" if request.host.split(":")[0] == "127.0.0.1" else "localhost"
    return render_template("index.html", partner_url=f"http://{host}:{PARTNER_PORT}")


class PreviewText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.in_title = False
        self.parts, self.title = [], []

    def handle_starttag(self, tag, attrs):
        self.hidden += tag in ("style", "script")
        self.in_title = tag == "title" or self.in_title

    def handle_endtag(self, tag):
        self.hidden -= tag in ("style", "script")
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if not self.hidden and data.strip():
            self.parts.append(data.strip())
            if self.in_title:
                self.title.append(data.strip())


@app.post("/api/preview")
def preview():
    data = request.get_json(silent=True)
    url = data.get("url") if isinstance(data, dict) else None
    if not isinstance(url, str) or len(url) > 1024:
        return {"error": "A URL is required."}, 400
    try:
        parsed = urlsplit(url)
        if (parsed.scheme != "http" or parsed.netloc not in PUBLIC_ORIGINS
                or parsed.username or parsed.password):
            return {"error": "Only the partner site is approved."}, 403
        with session.get(url, timeout=(2, 3)) as response:
            page = PreviewText()
            page.feed(response.text[:16000])
            return {"status": response.status_code, "title": " ".join(page.title),
                    "content": "\n".join(page.parts)[:4096]}
    except (requests.RequestException, ValueError):
        return {"error": "Preview unavailable."}, 502


@app.get("/healthz")
def health():
    return {"status": "ok"}
