# AGENTS.md

Instructions for coding agents that work in this repository. People start with the
[README](README.md) and [docs/](docs/). This file adds what an agent needs to work safely.

## Map

| Path | What it is | Docs |
| --- | --- | --- |
| `server/` | Rust API and web server; it embeds `web/dist` | [architecture](docs/architecture.md) |
| `judge/` | Rust judge daemon; `judge/py` is the Python zygote and sandbox, `judge/py/gen` holds the stress generators, `judge/py/constraints` holds the input constraints of each problem | [architecture](docs/architecture.md#judging-a-submission) |
| `proto/` | Types that the server and the judge share | |
| `web/` | React app (Vite, TanStack Router, Tailwind) | [development](docs/development.md) |
| `src/openleet/` | Python data tools: `openleet ingest`, `check`, `judge`, `videos`, `smoke` | [architecture](docs/architecture.md#where-the-tests-come-from) |
| `data/` | Problems, approaches, videos and judge specs (in git); `data/judge/tests.duckdb` comes from a release | |
| `deploy/` | systemd units, `install.sh`, `update.sh` | [deployment](docs/deployment.md) |
| `tests/`, `deploy/test_*.py` | Python tests | |

## Set up

```bash
uv sync && uv run openleet judge fetch && bun install && bun run build
uv run prek install                              # git hooks: the same checks as CI
docker compose --profile dev up -d judge-dev     # the judge needs Linux; on macOS it runs here
JUDGE_SOCKET=tcp://127.0.0.1:7777 cargo run --release -p openleet   # http://localhost:8080
```

To run the whole stack from the checkout, run `docker compose up -d --build`
(<http://openleet.localhost>).

## Before you commit

```bash
uv run prek run --all-files --hook-stage pre-push   # linters, type checks, clippy, all tests
uv run openleet smoke --base-url http://localhost:8080 --allow-network   # judge end to end
```

Do not skip hooks (`--no-verify`). CI runs exactly these checks. A push that fails the checks
does not deploy. After you change the web app, make sure that every page still scores 100 in
Lighthouse on mobile and on desktop (use `bunx lighthouse@12 URL --chrome-flags=--headless=new`
and add `--preset=desktop` for desktop).

## Conventions

- Write commits in Conventional Commits format with a scope: `feat(judge): ...`,
  `fix(web): ...`, `fix(deploy): ...`, `docs: ...`. Each commit is one complete change that
  passes the checks.
- Write clean, DRY and modular code, with the latest stable packages. `uv` manages Python
  (`pyproject.toml`, `uv.lock`), `bun` manages the web app, and `rust-toolchain.toml` sets Rust.
- A hook generates `judge/py/requirements.txt` from `pyproject.toml`. Do not edit it.
- The docs and the README describe the system as it is, in the present tense. Put history in
  commit messages, not in docs.
- A database change is a new file in `server/src/db/migrations/`. Never edit an applied
  migration.

## Product rules

- Python is the only language that the judge runs.
- No accounts or login. Progress belongs to the server that runs the app.
- Premium problems stay visible.
- No invented study content: problems, statements and solutions come from the sources that the
  README lists. Codex CLI reviews the approaches and hints that agents write. The review is
  recorded in `data/approach-reviews.json`. New approaches and hints get the same review.
- Do not call the LeetCode API and do not scrape leetcode.com.
- Every test input meets the constraints of its statement. Each judged problem has
  `judge/py/constraints/<slug>.py`, and `uv run openleet judge screen` drops the tests that the
  file rejects. Add the constraints file of a new problem before its tests ship.
- A time limit tests complexity, not machine speed. Limits come from trusted reference
  solutions (`src/openleet/judging/limits.py`). After Accepted, the app offers the next problem.
  The app does not move to it automatically.

## Data and production

- The test corpus (`data/judge/tests.duckdb`) is a release asset. `data/judge/corpus.json` names
  its repository, asset and sha256. `uv run openleet judge fetch` downloads it. To rebuild it,
  run `uv run openleet judge all`, then `judge publish`. The rebuild takes hours and needs Linux
  judges.
- A push to `main` deploys to the live site (<https://openleet.sudhanva.me>) within minutes.
- The live site holds the progress of a real user. Send only GET requests to it. Test anything
  that writes (submissions, reviews, plans, smoke tests) against a local or test server.
- Do not print or commit `/etc/openleet.env` or any secret.

## Verify a change on a server

`docs/deployment.md` has the setup, backups, restores and rollbacks. On a server, use
`curl https://HOST/api/health`, `curl https://HOST/api/version`, `journalctl -u openleet` and
`journalctl -u openleet-judge`.
