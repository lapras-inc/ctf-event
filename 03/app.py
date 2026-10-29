import hashlib
import hmac
import json
import secrets
import os

from flask import Flask, render_template, request

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4096
FLAG = os.environ["FLAG"]
KEY = secrets.token_bytes(32)  # Gunicorn --preload shares one key across workers.


def first_wins(pairs):
    result = {}
    for key, value in pairs:
        result.setdefault(key, value)
    return result


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/sign")
def sign():
    raw = request.get_data()
    try:
        text = raw.decode("utf-8")
        data = json.loads(text, object_pairs_hook=first_wins)
    except (UnicodeDecodeError, ValueError):
        return {"error": "Invalid UTF-8 JSON."}, 400
    if not isinstance(data, dict):
        return {"error": "Object required."}, 400
    if any(word in text.lower() for word in ("admin", "get_flag")):
        return {"error": "Restricted keyword."}, 403
    if data.get("action") != "preview" or data.get("role") != "viewer":
        return {"error": "Only viewer previews may be signed."}, 403
    return {"signature": hmac.new(KEY, raw, hashlib.sha256).hexdigest()}


@app.post("/api/execute")
def execute():
    raw = request.get_data()
    signature = request.headers.get("X-Signature", "")
    expected = hmac.new(KEY, raw, hashlib.sha256).hexdigest()
    if (len(signature) != 64
            or any(c not in "0123456789abcdef" for c in signature)
            or not hmac.compare_digest(expected, signature)):
        return {"error": "Invalid signature."}, 403
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return {"error": "Invalid UTF-8 JSON."}, 400
    if not isinstance(data, dict):
        return {"error": "Object required."}, 400
    if data.get("action") == "get_flag" and data.get("role") == "admin":
        return {"flag": FLAG}
    if data.get("action") == "preview" and data.get("role") == "viewer":
        return {"status": "preview ok", "message": data.get("message", "")}
    return {"error": "Job not permitted."}, 403


@app.get("/healthz")
def health():
    return {"status": "ok"}
