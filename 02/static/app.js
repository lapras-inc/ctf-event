"use strict";
const form = document.querySelector("#preview-form");
form.addEventListener("submit", async event => {
  event.preventDefault();
  const button = form.querySelector("button");
  const status = document.querySelector("#status");
  const out = document.querySelector("#output");
  button.disabled = true;
  status.textContent = "LOADING";
  const url = form.elements.url.value;
  let ok = false;
  try {
    const response = await fetch(form.dataset.api, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({url})});
    const data = await response.json();
    ok = response.ok && data.status >= 200 && data.status < 300;
    document.querySelector("#result-title").textContent = ok ? (data.title || "ページプレビュー") : "ページを取得できませんでした";
    document.querySelector("#result-host").textContent = new URL(url).host;
    out.textContent = ok ? data.content : (data.error === "Only the partner site is approved." ? "接続中のサイトのURLをご指定ください。" : "URLとページの公開状況をご確認ください。");
  } catch {
    document.querySelector("#result-title").textContent = "接続できませんでした";
    out.textContent = "時間をおいて、もう一度お試しください。";
  } finally {
    document.querySelector("#blank").hidden = true;
    document.querySelector("#preview-result").hidden = false;
    out.dataset.state = ok ? "ok" : "error";
    status.textContent = ok ? "PAGE LOADED" : "UNAVAILABLE";
    button.disabled = false;
  }
});
