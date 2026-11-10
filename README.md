# OpenLeet

Flashcards and a Python judge for the LeetCode problems top tech companies ask, plus every free
problem from 1 to 1000. Live: <https://openleet.sudhanva.me>

## How it fits together

```mermaid
flowchart LR
    B[Browser] -- HTTPS / HTTP/2 --> S
    subgraph VM [GCP e2-micro, 1 GB RAM, systemd]
        S["openleet<br/>Rust: API + embedded web app<br/>~20 MB RAM"]
        S -- read/write --> D[(DuckDB<br/>progress, drafts,<br/>submissions)]
        S -- read only --> T[(tests.duckdb)]
        S -- Unix socket --> J["openleet-judge<br/>Rust daemon"]
        J --> Z["Python 3.15 zygote<br/>LeetCode env loaded once"]
        Z -- fork per submission --> C["sandboxed child<br/>own uid, rlimits,<br/>no network"]
    end
```

## A submission

```mermaid
sequenceDiagram
    participant W as Web app
    participant S as openleet
    participant J as openleet-judge
    participant Z as zygote
    participant C as child
    W->>S: POST /api/submit {slug, code}
    S->>S: load tests (one row group)
    S->>J: code + inputs + expected outputs
    J->>Z: code + inputs (never the answers)
    Z->>Z: build inputs, generate stress tests
    Z->>C: fork
    loop each test
        C-->>J: output
        J->>J: compare, stop at first failure
    end
    J->>J: watchdog kills at the CPU limit
    J-->>S: verdict, passed/total, CPU ms
    S->>S: store in DuckDB
    S-->>W: Accepted / Wrong Answer / TLE / ...
```

## Where the tests come from

```mermaid
flowchart LR
    E[Statement examples] --> I[Inputs]
    L["LeetCodeDataset<br/>(Apache-2.0)"] --> I
    G["Stress generators<br/>judge/py/gen"] --> I
    I --> R{"Every reference<br/>runs every input"}
    R1["LeetCodeDataset solution<br/>doocs solutions<br/>Mercury accepted submissions<br/>(CC BY-NC, build only)"] --> R
    R -- all agree --> K["Kept test<br/>tests.duckdb"]
    R -- any disagree --> X[Dropped]
```

A reference counts only if it reproduces the statement's own example outputs. The time limit is
at least 4× the fastest reference and 1.25× the slowest, so what LeetCode accepted passes here.
Rebuild with `uv run openleet judge all`; `uv run openleet judge publish` uploads the new
`tests.duckdb` to the `corpus` release and records it in `data/judge/corpus.json`.

Sources: company lists from
[liquidslr/leetcode-company-wise-problems](https://github.com/liquidslr/leetcode-company-wise-problems),
statements from [doocs/leetcode](https://github.com/doocs/leetcode) (CC BY-SA 4.0, premium ones
included), approaches and hints written by Claude agents and reviewed with Codex CLI
(`data/approach-reviews.json`).

## Releases

```mermaid
flowchart LR
    P[push to main] --> CI["GitHub Actions<br/>lint, test, build x86-64-v3"]
    CI --> R["edge release<br/>openleet-REV.tar.zst"]
    CI -- "signed POST /api/deploy" --> S[openleet]
    S -- writes deploy-request --> PU[openleet-update.path]
    T[openleet-update.timer<br/>every 5 min, fallback] --> U
    PU --> U["update.sh (root)<br/>verify sha256, unpack,<br/>switch current, restart"]
    R --> U
    U --> V["CI polls /api/version<br/>until REV is live"]
```

Restarts drop no connection: `openleet.socket` holds ports 80 and 443 while the server restarts.
The server heals itself: systemd restarts it if it exits or stops pinging the watchdog (it pings
only while its database answers), rustls-acme renews the certificate 30 days before expiry, and
the server copies its database to `/var/lib/openleet/backups/<date>.duckdb` daily (14 kept). On
start it migrates the database (`server/src/db/migrations`, copying it to
`backups/pre-migration-*` first) or, if the file is unusable, moves it to
`/var/lib/openleet/quarantine/` and restores the newest backup.
Roll back by pointing `/opt/openleet/current` at an older release. New server: copy `deploy/`,
run `sudo deploy/install.sh`, fill in `/etc/openleet.env` (with `DEPLOY_SECRET`, the same value
as the GitHub secret), run `sudo /opt/openleet/update.sh`.

## Run locally

```mermaid
flowchart LR
    B[Browser] -- "http://openleet.localhost" --> C["caddy<br/>127.0.0.1:80"]
    C --> A["app<br/>static binary, read-only"]
    A -- "Unix socket<br/>(shared volume)" --> J["judge<br/>no network"]
    A --> V[("state volume<br/>DuckDB")]
```

```bash
docker compose up -d           # http://openleet.localhost (images from ghcr.io)
docker compose up -d --build   # or build both images from this checkout
HTTP_PORT=8088 docker compose up -d   # port 80 taken: http://openleet.localhost:8088
```

Working on the server: the judge needs Linux, so on macOS only the judge runs in Docker:

```bash
uv sync && uv run openleet judge fetch && bun install && bun run build
docker compose --profile dev up -d judge-dev   # the judge on 127.0.0.1:7777
JUDGE_SOCKET=tcp://127.0.0.1:7777 JUDGE_CPU_SCALE=1 cargo run --release -p openleet
# http://localhost:8080   (bun run dev: web on :3000 with hot reload)
```

```bash
bun run check && bun run typecheck && bun run test
cargo fmt --check && cargo clippy --all-targets && cargo test
uv run ruff check && uv run ty check
```

End to end, over HTTP only, against a running server (local or production): references,
wrong and crashing variants, time and memory limits, sandbox abuse, bad requests. It puts back
every draft it changes; its submissions stay in the history.

```bash
uv run openleet smoke --base-url http://localhost:8080 --allow-network   # local Docker judge
uv run openleet smoke --base-url https://openleet.sudhanva.me --seed 7 --json
```

```text
server/  Rust API + web app     judge/   judge daemon + judge/py sandbox
proto/   shared wire types      web/     React SPA
src/     Python data tools      data/    problems, approaches, judge specs and tests
deploy/  systemd units, install and update scripts
```

## API

| Method and path | Does |
| --- | --- |
| `GET /api/companies` | Companies and their problem counts |
| `GET /api/problems?company=meta&period=3m&topic=&difficulty=&q=` | One list with your progress, filtered; `q` searches within it |
| `GET /api/topics?company=&period=&difficulty=` | The list's topics and their problem counts, most first |
| `GET /api/problems/:slug` | One card: statement, topics, companies, approach |
| `GET /api/deck?company=&period=&set=&topic=&difficulty=` | Next card (`period`: `30d`, `3m`, `6m`, `all`, `lc1000`; `topic` by name, `difficulty` `Easy`, `Medium` or `Hard`; unknown values filter nothing) |
| `GET /api/search?q=two+sum` | Search by number, title, topic or statement |
| `POST /api/attempts` `{slug, grade, guessed, hints}` | Grade or skip a card |
| `PUT /api/notes` `{slug, text}` | Save your answer |
| `DELETE /api/progress?slug=` or `?all=true` | Clear progress |
| `GET /api/report?company=` | Readiness, streak, weak topics, trend |
| `GET /api/code/:slug` | Starter, draft, previous version, examples, time limit |
| `PUT /api/drafts`, `POST /api/drafts/reset`, `POST /api/drafts/restore` | Save, reset or restore code |
| `POST /api/run` `{slug, code, input?}` | Run examples or your own input |
| `POST /api/submit` `{slug, code}` | Run every test |
| `GET /api/submissions?slug=` | Your submissions |
| `GET /api/health` | `ok`, `db`, `judge`, certificate expiry; 503 when the database is down |

## Keys

`Enter` answer · `H` hint · `S` skip · `1` again · `2` got it · `3` less often · `B` back ·
`M` my answer · `/` search · ⌘Enter run · ⌘⇧Enter submit
