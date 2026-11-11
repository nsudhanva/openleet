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
| `GET /report?company=` | Readiness, streak, weak topics and trend; coding progress, shaky solves, the topic map and the activity calendar |
| `GET /code/:slug` | Starter code, your draft, the time limit and the examples, each as the Testcase box takes it (one JSON value per line) |
| `PUT /drafts`, `POST /drafts/reset`, `POST /drafts/restore` | Save, reset or restore code |
| `POST /run` `{slug, code, input?}` | Run the examples or your own input |
| `POST /submit` `{slug, code}` | Run every test: verdict, CPU time against the limit, the intended complexity |
| `GET /submissions?slug=` | Your submissions for a problem |
| `GET /next?slug=&company=&period=&topic=&difficulty=&status=&order=` | The plan's next problem after `slug`, the plan's progress, and up to four related plans |
| `GET /plans` | Your pinned plans, then your recent ones, each with its progress and next problem |
| `PUT /plans` `{company, period, topic, difficulty, status, order}` | Remember a plan you used; returns it |
| `PATCH /plans/:id` `{name?, pinned?}` | Rename (`null` drops the name) or pin a plan |
| `DELETE /plans/:id` | Forget a plan |
| `GET /health` | Database, judge and certificate status; 503 when the database is down |
| `GET /version` | The running revision |

`period` is `30d`, `3m`, `6m`, `all` or `lc1000`. `difficulty` is `Easy`, `Medium` or `Hard`.
`status` is `unsolved` (no accepted submission), `untried` (no submission), `shaky` (accepted
only after two or more failed submissions or a time limit) or `all`. A plan
without a status uses `unsolved`, and a problem list without one shows every problem. `order` is
`rank` (list order, the default), `number`, `easy-first` or `random` (a shuffle that is the same
on every request). Unknown filter values are ignored.

A practice plan is a list, its filters, a status and an order. `/next` never returns the next
problem's topics, so it cannot give away a flashcard's answer. The server keeps the 8 most
recently used unpinned plans and up to 50 pinned ones. A plan name is 1 to 60 characters.

## The report

`GET /report?company=` covers the company's 6-month list (with `any`, every company's). Besides
`report` (the flashcard scores) and `history` (the daily scores), it returns:

| Field | Holds |
| --- | --- |
| `coding` | `byDifficulty` (`{difficulty, solved, total}`), `tried`, `firstTry` (solved problems whose first submission was Accepted), `submissions` and `failures` (counts of `wrongAnswer`, `timeLimitExceeded`, `memoryLimitExceeded`, `runtimeError`, `compileError` and `outputLimitExceeded`) |
| `shaky` | The list's shaky solves, newest first: `{id, slug, title, difficulty, failures, solvedAt}`, with the failures before the first Accepted |
| `shakyElsewhere` | How many shaky solves are outside the list |
| `topicMap` | The list's topics, most asked first: `{topic, weight, problems, covered, solved, recall}`. `weight` is the company's frequency summed over the topic's problems, `covered` counts the problems you graded or solved, and `recall` is your flashcard accuracy on the topic (`null` before any card) |
| `activity` | `{start, today, days}`: 26 weeks from a Monday, in the server's time zone, with `{day, reviews, submissions}` for each day you practiced |

A solve is shaky when two or more wrong answers, time limits, memory limits or runtime errors
came before the first Accepted (compile errors do not count), or any time limit did. The server
keeps the newest 100 submissions of each problem and its latest Accepted one; the report counts
only those.

## Errors

Errors are `{"error": "..."}` with status 400 for invalid input, 404 for an unknown problem, plan
or endpoint, and 415 when the body is not `application/json`.
