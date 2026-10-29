"use strict";
const form = document.querySelector("#unlock-form");
form.addEventListener("submit", async event => {
  event.preventDefault();
  const button = form.querySelector("button"), status = document.querySelector("#status");
  const out = document.querySelector("#output");
  button.disabled = true;
  status.textContent = "アクセスキーを確認中";
  try {
    const response = await fetch(form.dataset.api, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({key: form.elements.key.value})});
    const data = await response.json();
    out.dataset.state = response.ok ? "ok" : "error";
    out.textContent = response.ok ? data.flag : "アクセスキーを確認できませんでした。入力内容をご確認ください。";
    status.textContent = response.ok ? "コレクションの内容" : "アクセス未確認";
    document.querySelector("#lock-status").textContent = response.ok ? "コレクションへのアクセスを確認しました" : "このコレクションはロックされています";
    document.querySelector(".access-state").classList.toggle("open", response.ok);
  } catch {
    out.dataset.state = "error";
    out.textContent = "接続できませんでした。時間をおいて再度お試しください。";
    status.textContent = "接続失敗";
  } finally { button.disabled = false; }
});
