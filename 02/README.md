# 02 — Waypoint リンクプレビュー

## 舞台
Waypoint は、リンク先ページの内容を取り込んで表示するプレビューサービス。
接続先として提携サイト「FIELDNOTE」がつながっている。

## ゴール
プレビュー機能を通じて本来見えないはずの内部コンテンツに到達し、
フラグ `LAPRAS{...}` を取得する。

## 起動
```bash
docker compose up --build
```
→ http://localhost:8002 （提携サイトは http://localhost:8012）
