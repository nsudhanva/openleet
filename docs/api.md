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
| `GET /report?company=` | Readiness and its trend, study counts, streak and the topics you name least; coding progress, shaky solves, the topic map and the activity calendar |
| `GET /readiness?company=` | Readiness alone, for the page header |
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
`status` is `unsolved` (no accepted submission), `untried` (no submission), `shaky` (a shaky
solve, as [the report](#the-report) defines it) or `all`. A plan
without a status uses `unsolved`, and a problem list without one shows every problem. `order` is
`rank` (list order, the default), `number`, `easy-first` or `random` (a shuffle that is the same
on every request). Unknown filter values are ignored.

A practice plan is a list, its filters, a status and an order. `/next` never returns the next
problem's topics, so it cannot give away a flashcard's answer. The server keeps the 8 most
recently used unpinned plans and up to 50 pinned ones. A plan name is 1 to 60 characters.

## The report

`GET /report?company=` (with `any`, every company) returns `report` and the progress page's
insights. Each figure covers one of three scopes: the company's most-asked problems
(readiness), its 6-month list, or everything you did on any list.

`report` holds:

| Field | Scope | Holds |
| --- | --- | --- |
| `readiness` | Most asked | As `GET /readiness` returns it, below |
| `trend` | Most asked | `{practiceDays, points}`: readiness at the end of each day, `{day, readiness}`, from your first day of practice (at most 90 days back) to today, leaving out days before readiness had any data. `points` is empty until `practiceDays`, your distinct days with practice, reaches 7 |
| `counts` | 6-month list | Cards `due`, `new`, on the `again` list and on the `less` list |
| `byDifficulty` | 6-month list | `{difficulty, seen, total}`: cards graded at least once, per difficulty |
| `accuracy` | Any list | Mean topic score (F1) of the last 50 graded cards; `null` before any |
| `graded` | Any list | Grades given (skips left out) |
| `streakDays` | Any list | Consecutive days with a graded card or a submission, ending today or yesterday: the days the activity calendar shades |
| `topics` | Any list | The topics you name least, weakest first: `{topic, score, named, seen}`. A topic is rated once `seen`, the graded cards carrying it, reaches 5; `score` is `named / (named + (misses + false alarms) / 2)`, where a false alarm is naming it on a card without it. Only topics under 0.6 are listed |

`GET /readiness?company=` returns the readiness alone, for the page header:
`{score, period, problems, recent, solved, shaky, cards, fading}`. It covers the company's
`problems` most-asked problems (at most 100), from its 6-month list, or from its all-time list
(`period` is then `all`) when the 6-month list has fewer than 25 problems; `recent` is the
6-month list's size. For each problem, with `f` its frequency in that list:

```text
score = Σ f · (0.6 · code + 0.4 · card) / Σ f
code  = 1 for a clean solve in the judge, 0.5 for a shaky one, else 0
card  = 1 when the card's last grade was "Got it" or "Visit less often" and it is not overdue,
        0.5 when it is overdue by less than its interval, else 0
```

`score` is `null` until you grade a card or submit a solution for one of the problems. `solved`
and `shaky` count the problems with each coding credit, `cards` and `fading` those with a full
and a half card credit.

The insights cover the company's 6-month list:

| Field | Holds |
| --- | --- |
| `coding` | `byDifficulty` (`{difficulty, solved, total}`), `tried`, `firstTry` (solves with no real failure before the first Accepted), `submissions` and `failures`: the failed submissions before each problem's first Accepted (all of them while unsolved), as counts of `wrongAnswer`, `timeLimitExceeded`, `memoryLimitExceeded`, `runtimeError`, `compileError` and `outputLimitExceeded` |
| `shaky` | The list's shaky solves, newest first: `{id, slug, title, difficulty, failures, solvedAt}`, with the failures before the first Accepted |
| `shakyElsewhere` | How many shaky solves are outside the list |
| `topicMap` | The list's topics, most problems first: `{topic, problems, covered, solved, graded, named}`. `covered` counts the problems you graded or solved, `graded` the graded cards of the list's problems with the topic, and `named` how many of those named it (`null` below 5) |
| `activity` | `{start, today, days}`: 26 weeks from a Monday, in the server's time zone, with `{day, reviews, submissions}` for each day you practiced |

A real failure is a wrong answer, a time limit, a memory limit or a runtime error; compile
errors and output limits do not count. A solve is shaky when two or more real failures came
before the first Accepted, or any time limit did, until a later Accepted clears it: one at
least a calendar day after the first Accepted, with no real failure since the Accepted before
it. The server keeps the newest 100 submissions of each problem and its latest Accepted one;
the report counts only those. Days are calendar days in the server's time zone.

## Errors

Errors are `{"error": "..."}` with status 400 for invalid input, 404 for an unknown problem, plan
or endpoint, and 415 when the body is not `application/json`.
