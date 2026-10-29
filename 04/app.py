import os

from flask import Flask, render_template, request

from vm import verify

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4096
FLAG = os.environ["FLAG"]


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/unlock")
def unlock():
    data = request.get_json(silent=True)
    key = data.get("key") if isinstance(data, dict) else None
    if not isinstance(key, str) or not verify(key):
        return {"error": "Key rejected."}, 403
    return {"status": "archive unlocked", "flag": FLAG}


@app.get("/healthz")
def health():
    return {"status": "ok"}
