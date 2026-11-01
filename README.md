# Olist Advanced E-Commerce Pipeline

A learning-first data engineering project: replay the Olist Brazilian e-commerce
dataset as daily batches and build a real-style pipeline around it —
discovery, bronze, cleaning, quality checks, star schema, incremental loads,
SCD, orchestration and CDC.

Learning rules live in `AGENTS.md`. The 10-stage roadmap lives in `PROJECT_PLAN.md`.

## Structure

```
data/source/      original Olist CSVs (never modified)
data/landing/     daily files dropped by the simulator
data/bronze/      raw copies after discovery (never edited)
src/simulator/    makes the daily files
src/discovery/    finds new/changed files (hashing)
src/extract/      reads bronze into Python
src/transform/    cleaning + validation
src/quality/      data quality checks
src/load/         writes into Postgres
sql/              numbered SQL files (001_..., 002_...)
notes/            stage notes in my own words
tests/            connection checks now, pytest later
```

## How to run

```bash
docker compose up -d                              # start Postgres
./venv/Scripts/python.exe tests/test_db.py        # check the connection
```

Credentials live in `.env` (never committed).

## Status

- [x] Stage 1: containers, DB connection, CSVs downloaded, repo structure
- [ ] Stage 1: simulator v1
- [ ] Stages 2-10: see PROJECT_PLAN.md

## Design notes

(Write this yourself as the stages progress — what the pipeline does,
quality rules, incremental strategy, SCD design, failure handling.)
