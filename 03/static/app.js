"use strict";
const out = document.querySelector("#output");
const status = document.querySelector("#status");
function show(value, ok = true) {
  out.textContent = typeof value === "string" ? value : JSON.stringify(value, null, 2);
  out.dataset.state = ok ? "ok" : "error";
  status.textContent = ok ? "RESPONSE RECEIVED" : "REQUEST FAILED";
}
async function call(path, options = {}) {
  status.textContent = "REQUESTING…";
  try {
    const res = await fetch(path, options);
    const text = await res.text();
    let body;
    try { body = JSON.parse(text); } catch { body = text; }
    show(body, res.ok);
    return res.ok ? body : null;
  } catch {
    show("通信に失敗しました。サービスの起動状態を確認してください。", false);
    return null;
  }
}
document.querySelectorAll("form[data-api]").forEach(form => {
  form.addEventListener("submit", async event => {
    event.preventDefault();
    const button = form.querySelector("button[type=submit]");
    button.disabled = true;
    const kind = form.dataset.kind;
    try {
      if (kind === "url") {
        await call(form.dataset.api, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({url: form.elements.url.value})});
      } else if (kind === "key") {
        await call(form.dataset.api, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({key: form.elements.key.value})});
      } else if (kind === "execute") {
        await call(form.dataset.api, {method: "POST", headers: {"Content-Type": "application/json", "X-Signature": form.elements.signature.value}, body: form.elements.body.value});
      } else if (kind === "sign") {
        const body = form.elements.body.value;
        const result = await call(form.dataset.api, {method: "POST", headers: {"Content-Type": "application/json"}, body});
        if (result) {
          document.querySelector("#signed-body").value = body;
          document.querySelector("#signature").value = result.signature;
        }
      } else { await call(form.dataset.api); }
    } finally { button.disabled = false; }
  });
});

