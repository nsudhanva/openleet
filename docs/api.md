# API

All endpoints are under `/api` and return JSON.

| Endpoint | Returns or does |
| --- | --- |
| `GET /companies` | Companies and their problem counts |
| `GET /problems?company=&period=&topic=&difficulty=&status=&order=&q=` | A problem list with your progress |
| `GET /topics?company=&period=&difficulty=` | The list's topics and counts, most first |
| `GET /problems/:slug` | One card: statement, topics, companies, approach |
| `GET /deck?company=&period=&set=&topic=&difficulty=` | The next card to study |
| `GET /search?q=` | Problems by number, title, topic or statement text |
| `POST /attempts` `{slug, grade, guessed, hints}` | Grade or skip a card |
| `PUT /notes` `{slug, text}` | Save your own answer |
| `DELETE /progress?slug=` or `?all=true` | Clear progress |
| `GET /report?company=` | Readiness, streak, weak topics and trend |
| `GET /code/:slug` | Starter code, your draft, examples and the time limit |
| `PUT /drafts`, `POST /drafts/reset`, `POST /drafts/restore` | Save, reset or restore code |
| `POST /run` `{slug, code, input?}` | Run the examples or your own input |
| `POST /submit` `{slug, code}` | Run every test |
| `GET /submissions?slug=` | Your submissions for a problem |
| `GET /next?slug=&company=&period=&topic=&difficulty=&status=&order=` | A plan's next problem after `slug`, its progress and, from `slug`, up to four related plans |
| `GET /plans` | Your pinned plans, then your recent ones, each with its progress and next problem |
| `PUT /plans` `{company, period, topic, difficulty, status, order}` | Remember a plan you used; returns it |
| `PATCH /plans/:id` `{name?, pinned?}` | Rename (`null` drops the name) or pin a plan |
| `DELETE /plans/:id` | Forget a plan |
| `GET /health` | Database, judge and certificate status; 503 when the database is down |
| `GET /version` | The running revision |

`period` is `30d`, `3m`, `6m`, `all` or `lc1000`. `difficulty` is `Easy`, `Medium` or `Hard`.
`status` is `unsolved` (no accepted submission), `untried` (no submission) or `all`; a plan
without one is `unsolved`, a problem list shows every problem. `order` is `rank` (list order, the
default), `number`, `easy-first` or `random` (a shuffle that is the same on every request).
Unknown filter values are ignored.

A practice plan is a list, its filters, a status and an order, built from data the app already
has. Its next problem carries no topics. Up to 8 unpinned plans are kept (the least recently used
go first) and 50 pinned ones; a plan name is 1 to 60 characters.

Errors are `{"error": "..."}` with status 400 for invalid input, 404 for an unknown problem, plan
or endpoint, and 415 when the body is not `application/json`.
