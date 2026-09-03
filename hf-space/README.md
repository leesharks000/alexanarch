---
title: Crimson Hexagonal Archive — machine interface
emoji: ⬡
colorFrom: red
colorTo: gray
sdk: docker
app_port: 7860
pinned: true
license: cc-by-4.0
---
# Crimson Hexagonal Archive — machine interface

Records, citation graph, series chains, heteronym records and full-text search over the dataset [leesharsks/crimson-hexagonal-archive](https://huggingface.co/datasets/leesharsks/crimson-hexagonal-archive), as a plain HTTP API for agents and tools. Loads the parquet from the Hub at startup; rebuilt whenever the dataset is.

`/record/{n}` · `/axn/{hex}` · `/neighbours/{n}?hops=2` · `/series/{n}` · `/search?q=…` · `/heteronyms` · `/heteronym/{id}` · `/health`

Canonical seat of every record: `https://alexanarch.org/s/records/N/`. CC BY 4.0.
