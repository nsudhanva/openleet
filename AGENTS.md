# AGENTS.md

Instructions for coding agents working in this repository. Start with [README](README.md) and
[docs/](docs/) for product context; this file covers safety rules and workflows.

## Map

| Path | What it is | Docs |
| --- | --- | --- |
| `server/` | Rust API and web server; embeds `web/dist` | [architecture](docs/architecture.md) |
| `judge/` | Rust judge daemon; `judge/py` has the Python zygote, sandbox, stress generators (`gen/`), and input constraints (`constraints/`) | [architecture](docs/architecture.md#judging-a-submission) |
| `proto/` | Types shared between `server/` and `judge/` | |
| `web/` | React app (Vite, TanStack Router, Tailwind) | [development](docs/development.md) |
| `src/openleet/` | Python CLI tools: `openleet ingest`, `check`, `judge`, `videos`, `smoke` | [architecture](docs/architecture.md#where-the-tests-come-from) |
| `data/` | Problems, approaches, videos, and judge specs (in git); `data/judge/tests.duckdb` comes from a release | |
| `deploy/` | Systemd units, `install.sh`, `update.sh` | [deployment](docs/deployment.md) |
| `tests/`, `deploy/test_*.py` | Python tests | |

## Setup

```bash
uv sync && uv run openleet judge fetch && bun install && bun run build
uv run prek install                              # git hooks matching CI
docker compose --profile dev up -d judge-dev     # judge needs Linux; runs in Docker on macOS
JUDGE_SOCKET=tcp://127.0.0.1:7777 cargo run --release -p openleet   # http://localhost:8080
```

To run the full stack from this checkout: `docker compose up -d --build`
(<http://openleet.localhost>).

## Before committing

```bash
uv run prek run --all-files --hook-stage pre-push   # linters, type checks, clippy, all tests
uv run openleet smoke --base-url http://localhost:8080 --allow-network   # end-to-end judge test
```

Never skip hooks (`--no-verify`). CI runs these exact checks and blocks deploys on failure. After
changing `web/`, verify every page still scores 100 in Lighthouse on mobile and desktop
(`bunx lighthouse@12 URL --chrome-flags=--headless=new`, plus `--preset=desktop`).

## Conventions

- **Commits**: Conventional Commits with a scope (`feat(judge): ...`, `fix(web): ...`,
  `fix(deploy): ...`, `docs: ...`). Each commit is one complete change that passes all checks.
- **Tooling**: Keep code clean, DRY, and modular with current stable packages. `uv` manages
  Python (`pyproject.toml`, `uv.lock`), `bun` manages `web/`, and `rust-toolchain.toml` pins Rust.
- **Generated files**: A git hook regenerates `judge/py/requirements.txt` from `pyproject.toml`.
  Do not edit it by hand.
- **Docs**: Describe the system in the present tense. Put history in commit messages, not docs.
- **Database migrations**: Add a new file in `server/src/db/migrations/`. Never edit an applied
  migration.

## Product rules

- Python is the only supported judge language.
- Accounts: email and password, no email verification. Each account's progress is its own: every
  progress query and endpoint is scoped to the signed-in account (see
  [architecture](docs/architecture.md#accounts-and-sessions)). Never add an endpoint that reads or
  writes progress without `auth::Me`, and never take a user id from the request.
- Keep premium problems visible.
- No invented study content: problems, statements, and solutions come from the sources listed in
  [README](README.md). Agent-written approaches and hints must be reviewed with Codex CLI and
  recorded in `data/approach-reviews.json`.
- Never call the LeetCode API or scrape `leetcode.com`.
- Every test input must satisfy its problem constraints. Each judged problem needs
  `judge/py/constraints/<slug>.py`, and `uv run openleet judge screen` drops tests it rejects. Add
  the constraints file for any new problem before shipping its tests.
- Time limits are derived from trusted reference solutions (`src/openleet/judging/limits.py`) to
  test algorithmic complexity. After Accepted, offer the next problem without auto-navigating.

## Data and production

- `data/judge/tests.duckdb` is distributed as a GitHub release asset pinned in
  `data/judge/corpus.json`. Fetch it with `uv run openleet judge fetch`. Rebuilding
  (`uv run openleet judge all` then `judge publish`) takes hours and requires Linux judges.
- Pushing to `main` deploys to production (<https://openleet.sudhanva.me>) within minutes.
- Production holds real user progress. Send only `GET` requests to it. Run write operations
  (submissions, reviews, plans, smoke tests) against a local or test server.
- Never print or commit `/etc/openleet.env` or any secrets.

## Verifying a server

See [docs/deployment.md](docs/deployment.md) for setup, backups, restores, and rollbacks. Quick
server checks: `curl https://HOST/api/health`, `curl https://HOST/api/version`,
`journalctl -u openleet`, and `journalctl -u openleet-judge`.
