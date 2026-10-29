import os

from flask import Flask, render_template, request

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4096
FLAG = os.environ["FLAG"]


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/report")
def report():
    return {"workspace": "northline", "role": "guest", "report":
            "Quarterly review complete. Internal audit export is restricted."}


@app.get("/api/admin/export")
def export():
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if client_ip != "127.0.0.1":
        return {"error": "Internal network only."}, 403
    return {"document": "internal-audit", "flag": FLAG}


@app.get("/healthz")
def health():
    return {"status": "ok"}
