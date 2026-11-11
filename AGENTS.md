# AGENTS.md

Instructions for coding agents working in this repository. People start with the
[README](README.md) and [docs/](docs/); this file adds what an agent needs to work safely.

## Map

| Path | What it is | Docs |
| --- | --- | --- |
| `server/` | Rust API and web server; embeds `web/dist` | [architecture](docs/architecture.md) |
| `judge/` | Rust judge daemon; `judge/py` is the Python zygote and sandbox | [architecture](docs/architecture.md#judging-a-submission) |
| `proto/` | Types shared by server and judge | |
| `web/` | React app (Vite, TanStack Router, Tailwind) | [development](docs/development.md) |
| `src/openleet/` | Python data tools: `openleet ingest`, `check`, `judge`, `smoke` | [architecture](docs/architecture.md#where-the-tests-come-from) |
| `data/` | Problems, approaches and judge specs (in git); `data/judge/tests.duckdb` comes from a release | |
| `deploy/` | systemd units, `install.sh`, `update.sh` | [deployment](docs/deployment.md) |
| `tests/`, `deploy/test_*.py` | Python tests | |

## Set up

```bash
uv sync && uv run openleet judge fetch && bun install && bun run build
uv run prek install                              # git hooks: the same checks as CI
docker compose --profile dev up -d judge-dev     # the judge needs Linux; on macOS it runs here
JUDGE_SOCKET=tcp://127.0.0.1:7777 cargo run --release -p openleet   # http://localhost:8080
```

`docker compose up -d --build` runs the whole stack from the checkout instead
(<http://openleet.localhost>).

## Before you commit

```bash
uv run prek run --all-files --hook-stage pre-push   # linters, type checks, clippy, all tests
uv run openleet smoke --base-url http://localhost:8080 --allow-network   # judge end to end
```

Never skip hooks (`--no-verify`). CI runs exactly these checks; a push that fails them does not
deploy. After changing the web app, check that every page still scores 100 in Lighthouse on
mobile and desktop (`bunx lighthouse@12 URL --chrome-flags=--headless=new`, plus
`--preset=desktop`).

## Conventions

- Commits follow Conventional Commits with a scope: `feat(judge): ...`, `fix(web): ...`,
  `fix(deploy): ...`, `docs: ...`. Each commit is one complete change that passes the checks.
- Write the code clean, DRY and modular, with the latest stable packages. Python is managed by
  `uv` (`pyproject.toml`, `uv.lock`), the web app by `bun`, Rust by `rust-toolchain.toml`.
- `judge/py/requirements.txt` is generated from `pyproject.toml` by a hook; do not edit it.
- Docs and the README describe the system as it is, in the present tense. History belongs in
  commit messages, not in docs.
- Database changes are new files in `server/src/db/migrations/`; never edit an applied one.

## Product rules

- Python is the only language the judge runs.
- No accounts or login; progress belongs to the server it runs on.
- Premium problems stay visible.
- No invented study content: problems, statements and solutions come from the sources the README
  lists. Approaches and hints written by agents are reviewed with Codex CLI, and the review is
  recorded in `data/approach-reviews.json`; new ones get the same review.
- Do not call LeetCode's API or scrape leetcode.com.
- A time limit tests complexity, not machine speed: limits come from trusted reference
  solutions (`src/openleet/judging/limits.py`). After Accepted, the app offers the next problem
  but never moves on by itself.

## Data and production

- The test corpus (`data/judge/tests.duckdb`) is a release asset; `data/judge/corpus.json` names
  its repository, asset and sha256. `uv run openleet judge fetch` downloads it. Rebuilding it
  (`uv run openleet judge all`, then `judge publish`) takes hours and needs Linux judges.
- A push to `main` deploys to the live site (<https://openleet.sudhanva.me>) within minutes.
- The live site holds a real user's progress. Send it GET requests only; test anything that
  writes (submissions, reviews, plans, smoke tests) against a local or test server.
- Never print or commit `/etc/openleet.env` or any secret.

## Verify a change on a server

`docs/deployment.md` has the setup, backups, restores and rollbacks. On a server:
`curl https://HOST/api/health`, `curl https://HOST/api/version`, `journalctl -u openleet` and
`journalctl -u openleet-judge`.
