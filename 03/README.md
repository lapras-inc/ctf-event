# 03 — SEAL ジョブコンソール

## 舞台
SEAL は、ジョブ（JSON）に署名してから実行するコンソール。
現在のワークスペースのロールは `viewer` で、利用可能な操作は `preview` のみ。
署名の発行（`/api/sign`）と実行（`/api/execute`）の 2 ステップで構成されている。

## ゴール
viewer には許可されていない操作を実行し、フラグ `LAPRAS{...}` を取得する。

## 起動
```bash
docker compose up --build
```
→ http://localhost:8003
