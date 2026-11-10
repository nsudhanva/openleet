# google

Flashcards and a small LeetCode-style judge for the 793 LeetCode problems Google asked in the
last six months (filters for the last 3 months and 30 days), plus every free problem numbered
1 to 1000. Read the problem, guess its topics, open a hint if you are stuck, check a short
approach written in ASD-STE100 Simplified Technical English, then solve it in Python and submit:
your code runs against the statement's examples, about a hundred hidden tests, and generated
stress tests that a too-slow solution fails with Time Limit Exceeded.

```
.
├── server/          # Rust (axum + DuckDB 2.0): JSON API, the web app embedded, automatic HTTPS
├── judge/           # Rust judge daemon + judge/py: the Python 3.15 sandbox (zygote, harness)
├── proto/           # Wire types shared by server and judge
├── web/             # React SPA (Vite, TanStack Router, Tailwind, shadcn/ui, CodeMirror 6)
├── src/google/      # Python tools: `uv run google ingest | check | judge ...`
├── data/
│   ├── problems.json, approaches.json, approach-reviews.json
│   └── judge/       # specs.json (signatures, checkers, references) + tests.duckdb (the corpus)
├── deploy/          # systemd units, install and update scripts for the server
└── Dockerfile, docker-compose.yml   # local development only: the judge in a Linux container
```

## Run it locally

```bash
uv sync && bun install
bun run build                      # web/dist, embedded into the server at compile time
docker compose up -d judge         # the judge needs Linux; on Linux run bin/judge instead
JUDGE_SOCKET=tcp://127.0.0.1:7777 JUDGE_CPU_SCALE=1 cargo run --release -p cards
# open http://localhost:8080 (progress in data/cards.duckdb)
```

For frontend work, `bun run dev` serves the SPA on :3000 with hot reload and proxies `/api` to
the server on :8080.

## Deploy (live at https://google.sudhanva.me)

Native, no containers: a free GCP e2-micro (2 shared vCPUs, 1 GB RAM) runs two systemd services.

- **`google-cards`** (`bin/cards`, about 20 MB of RAM): the web app is embedded in the binary,
  precompressed with Brotli 11 and zstd 19, served with year-long immutable caching. It gets its
  own Let's Encrypt certificate (TLS-ALPN-01) and serves HTTP/2; port 80 only redirects.
  Progress lives in DuckDB at `/var/lib/google-cards/cards.duckdb`.
- **`google-judge`** (`bin/judge` + Python 3.15 from uv): one submission at a time. The Python
  zygote imports LeetCode's environment once and forks a child per submission; inputs are
  converted (and stress inputs generated) before the fork, so CPU time is the solution's own.
  The child drops to its own user (uid 61000) with CPU, memory, file and process limits.
  systemd adds no network, a read-only system, no view of the app's data, 450 MB, 64 tasks.
- **Releases**: every push to `main` runs `.github/workflows/release.yml` (lint, tests, a native
  x86-64-v3 build) and publishes the archive to the `edge` GitHub release. The server's
  `google-cards-update.timer` checks every 5 minutes, unpacks a new release next to the old
  ones, switches `/opt/google-cards/current`, and restarts both services. Units and scripts ship
  in each release and update themselves. Roll back by pointing `current` at an older release.
- **First install**: copy `deploy/` to the server, run `sudo deploy/install.sh`, set
  `SITE_ADDRESS`, `TZ` and `JUDGE_CPU_SCALE` in `/etc/google-cards.env`, then run
  `sudo /opt/google-cards/update.sh`. A `progress.db` from the old SQLite version in
  `/var/lib/google-cards` is imported on first start.
- **GCP**: e2-micro and a 30 GB standard disk in `us-central1` (Always Free), a static IP in use
  by that VM, and a firewall rule for 80/443. Keep the VM running: a reserved IP is only free
  while attached. DNS is a plain (not proxied) Cloudflare A record.

## Develop

```bash
bun run check && bun run typecheck && bun run test     # web: Biome, tsc, Vitest
cargo clippy --all-targets && cargo test               # server, judge, proto
uv run ruff check && uv run ruff format --check && uv run ty check
```

## How it works

- **Data** (`src/google/ingest.py`): the problem lists, ranks, frequency and topics come from
  [liquidslr/leetcode-company-wise-problems](https://github.com/liquidslr/leetcode-company-wise-problems)
  (Google: 30 days, 3 months, 6 months). The LC 1–1000 list adds every free problem numbered 1 to
  1000 from the doocs index. Statements come from [doocs/leetcode](https://github.com/doocs/leetcode)
  (CC BY-SA 4.0) and are allowlist-sanitized. Premium statements are left out.
- **Approaches and hints** (`data/approaches.json`, Google problems): Claude agents wrote one
  approach and one hint per problem; Claude reviewers and Codex CLI checked each one, and every
  disagreement was adjudicated (`data/approach-reviews.json` keeps the trail). `uv run google
  check` enforces the ASD-STE100 rules.
- **Tests** (`uv run google judge all`, see `src/google/judging/`): inputs come from the
  statements' examples and [LeetCodeDataset](https://huggingface.co/datasets/newfacade/LeetCodeDataset)
  (Apache-2.0); stress inputs from `judge/py/gen/<slug>.py`, generators of maximum-size inputs.
  No expected output is copied from anywhere: every reference solution (LeetCodeDataset's
  canonical one, every doocs solution, and accepted LeetCode submissions from
  [Mercury](https://huggingface.co/datasets/Elfsong/Mercury), CC BY-NC 4.0, used offline only)
  runs every input in the judge's own sandbox. A reference counts only if it reproduces every
  statement example's official output; a test is kept only if all counting references agree.
  Each problem's checker (exact, any order, any order at two levels, 1e-5 for floats) is the
  strictest one under which the references reproduce the examples.
- **Time limits**: CPU time for the whole suite, at least 4 × the fastest reference and
  1.25 × the slowest (references include submissions LeetCode accepted, so whatever LeetCode
  accepts passes), scaled by `JUDGE_CPU_SCALE` for the machine, between 2 and 20 seconds.
- **Storage** (`server/src/db.rs`): DuckDB 2.0. Reads never touch it: the attempt log, card
  states, notes and the readiness report live in memory and every write goes through. It holds
  the attempt log (ENUM grades, `VARCHAR[]` guesses), notes and drafts (upserted with `MERGE`),
  daily scores, and submissions with a `VARIANT` detail column; the test corpus is a separate
  DuckDB file attached read-only, sorted by problem so a lookup touches one row group.
- **Search, scheduling, scoring** (`server/src/{search,scheduler,scorer}.rs`): LeetCode number,
  title words and prefixes, acronyms (`lis`), small typos, difficulty, topics and statement text.
  Leitner boxes replayed from the attempt log (*Visit again* 10 minutes; *Got it* up one box: 1,
  3, 7, 16, 35, 90 days; *Visit less often* two boxes and double the wait; *Skip* one hour).
  Readiness is mastery (half topic F1 less a quarter per hint, half your grade, fading with time)
  weighted by Google frequency.

## API

| Method and path | Does |
| --- | --- |
| `GET /api/search?q=two+sum&limit=10` | Ranked problems for a free-text query |
| `GET /api/problems` | Every problem with its progress (no topics) |
| `GET /api/problems/:slug` | One full card: statement, topics, approach, hints, state |
| `GET /api/deck?period=30d&set=again&topic=Graph+Theory&difficulty=Hard` | The next card (`period` is `30d`, `3m`, `6m` or `lc1000`) |
| `POST /api/attempts` `{slug, grade, guessed, hints}` | Grade (`again`, `good`, `less`) or `skip` a card |
| `PUT /api/notes` `{slug, text}` | Save your own answer to a problem (empty text deletes it) |
| `DELETE /api/progress?slug=two-sum` or `?all=true` | Clear one problem, or everything |
| `GET /api/report`, `GET /api/readiness` | Readiness, coverage, accuracy, streak, weak topics, trend |
| `GET /api/code/:slug` | Starter code, your draft, examples, test counts, time limit |
| `PUT /api/drafts` `{slug, code}` | Save your code (empty deletes it) |
| `POST /api/run` `{slug, code, input?}` | Run the examples, or custom input (one JSON value per line) |
| `POST /api/submit` `{slug, code}` | Judge against every test |
| `GET /api/submissions?slug=`, `GET /api/submissions/:id` | Submission history, one submission with its code |

Errors are `{"error": "..."}`: 400 bad input, 404 unknown problem, 503 judge busy.

## Keys

`Enter` show answer, `H` hint, `S` skip, `1` visit again, `2` got it, `3` visit less often,
`B` back, `M` my answer, `←`/`→` statement pages, `/` or ⌘K search. On the code page,
⌘/Ctrl+Enter runs and ⌘/Ctrl+Shift+Enter submits.
