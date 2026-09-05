---
title: Crimson Hexagonal Archive — machine interface
emoji: 🔺
colorFrom: red
colorTo: gray
sdk: gradio
sdk_version: 6.26.0
app_file: app.py
pinned: true
license: cc-by-4.0
---
# Crimson Hexagonal Archive — machine interface

Records, citation graph, series chains, heteronym records and Greek-safe full-text search over the dataset [leesharks/crimson-hexagonal-archive](https://huggingface.co/datasets/leesharks/crimson-hexagonal-archive). A Gradio panel for people at `/`; a JSON API for agents under `/api`:

`/api/record/{n}` · `/api/axn/{hex}` · `/api/neighbours/{n}?hops=2` · `/api/series/{n}` · `/api/search?q=…` · `/api/heteronyms` · `/api/heteronym/{id}` · `/api/health`

Loads the parquet from the Hub at startup. Canonical seat of every record: `https://alexanarch.org/s/records/N/`. CC BY 4.0.
