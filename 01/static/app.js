"use strict";
const form = document.querySelector("form[data-api]");
form.addEventListener("submit", async event => {
  event.preventDefault();
  const button = form.querySelector("button");
  const out = document.querySelector("#output"), status = document.querySelector("#status");
  button.disabled = true;
  status.textContent = "読み込み中";
  try {
    const response = await fetch(form.dataset.api);
    const data = await response.json();
    out.textContent = data.report || data.error || "レポートを取得できませんでした。";
    out.dataset.state = response.ok ? "ok" : "error";
    status.textContent = response.ok ? "2026 Q3 · 運用サマリー" : "取得失敗";
  } catch {
    out.textContent = "通信に失敗しました。時間をおいて再度お試しください。";
    out.dataset.state = "error";
    status.textContent = "取得失敗";
  } finally { button.disabled = false; }
});
