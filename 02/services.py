import os
from urllib.parse import urlsplit

from flask import Flask, redirect, render_template, request

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4096
ROLE = os.environ["SERVICE_ROLE"]


@app.get("/")
def index():
    if ROLE != "partner":
        return {"error": "Not found"}, 404
    return render_template("partner.html")


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.get("/article")
def article():
    if ROLE != "partner":
        return {"error": "Not found"}, 404
    return render_template("article.html")


@app.get("/go")
def go():
    if ROLE != "partner":
        return {"error": "Not found"}, 404
    target = request.args.get("to", "")
    parsed = urlsplit(target)
    allowed = {"partner:8000": {"/article"}, "vault:8000": {"/document"}}
    if (parsed.scheme != "http" or parsed.netloc not in allowed
            or parsed.path not in allowed[parsed.netloc]
            or parsed.username or parsed.password or parsed.fragment):
        return {"error": "Unknown fixture destination"}, 400
    return redirect(target, code=302)


@app.get("/document")
def document():
    if ROLE != "vault":
        return {"error": "Not found"}, 404
    return "Internal archive / " + os.environ["FLAG"]
