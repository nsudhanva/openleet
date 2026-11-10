# OpenLeet

Practice the LeetCode problems that top tech companies ask, with flashcards that schedule your
reviews and a judge that runs your solutions in the browser.

[Live site](https://openleet.sudhanva.me) · [Quick start](#quick-start) · [Docs](docs/)

## Features

- Problem lists for 24 companies, by how recently each problem was asked (30 days, 3 months,
  6 months or all time), plus every free problem from 1 to 1000.
- Flashcards: name a problem's topics, then check the approach and its complexity. Spaced
  repetition decides when each card comes back.
- Write Python solutions and run them against the examples, hidden tests and large stress tests,
  with the same verdicts LeetCode gives.
- A readiness score for each company, plus your streak and weakest topics.
- Keyboard shortcuts for every action, listed on the site's About page.
- No account. Progress is stored on the server you run it on.

## Quick start

With Docker installed:

```bash
git clone https://github.com/nsudhanva/openleet && cd openleet
docker compose up -d
```

Open <http://openleet.localhost>. If port 80 is taken, run `HTTP_PORT=8088 docker compose up -d`
and open <http://openleet.localhost:8088>.

## Documentation

- [Architecture](docs/architecture.md): how pages load, how a submission is judged, and where
  the tests come from.
- [Development](docs/development.md): running from source, checks and end-to-end tests.
- [Deployment](docs/deployment.md): releases, the production server and recovery.
- [API](docs/api.md): the JSON endpoints.

## Data sources

- Company lists: [liquidslr/leetcode-company-wise-problems](https://github.com/liquidslr/leetcode-company-wise-problems)
- Problem statements and solutions: [doocs/leetcode](https://github.com/doocs/leetcode)
  (CC BY-SA 4.0)
- Starter code, tests and solutions: [LeetCodeDataset](https://huggingface.co/datasets/newfacade/LeetCodeDataset)
  (Apache-2.0)
- Accepted submissions used only to check tests at build time, never shipped:
  [Mercury](https://huggingface.co/datasets/Elfsong/Mercury) (CC BY-NC)
- Approaches and hints were written by Claude agents and reviewed with Codex CLI
  (`data/approach-reviews.json`).

## License

[MIT](LICENSE). Problem statements from doocs/leetcode remain under CC BY-SA 4.0.
