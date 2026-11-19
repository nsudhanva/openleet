# API

All endpoints are under `/api` and return JSON.

| Endpoint | Returns or does |
| --- | --- |
| `GET /companies` | Companies and their problem counts |
| `GET /problems?company=&period=&list=&topic=&difficulty=&status=&order=&q=` | A problem list with your progress |
| `GET /topics?company=&period=&difficulty=` | The list's topics and counts, most first |
| `GET /problems/:slug` | One card: statement, topics, companies, approach, videos |
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
| `GET /submissions/:id` | One submission with its code and result |
| `GET /next?slug=&company=&period=&list=&topic=&difficulty=&status=&order=` | The plan's next problem after `slug`, the plan's progress, and up to four related plans |
| `GET /plans` | Your pinned plans, then your recent ones, each with its progress and next problem |
| `PUT /plans` `{company, period, topic, difficulty, status, order}` | Remember a plan that you used; returns it |
| `PATCH /plans/:id` `{name?, pinned?}` | Rename (`null` drops the name) or pin a plan |
| `DELETE /plans/:id` | Forget a plan |
| `GET /lists` | Your lists, newest first, each with its problems, progress and next problem |
| `POST /lists` `{name, slugs?}` | Make a list |
| `PATCH /lists/:id` `{name?, slugs?}` | Rename a list, or replace its problems (`slugs` in the new order) |
| `DELETE /lists/:id` | Delete a list. Its problems and your progress stay. |
| `GET /health` | Database, judge and certificate status; 503 when the database is down |
| `GET /version` | The running revision |

`period` is `30d`, `3m`, `6m`, `all` or `lc1000`. `difficulty` is `Easy`, `Medium` or `Hard`.
`status` is `unsolved` (no accepted submission), `untried` (no submission), `shaky` (a shaky
solve, as [the report](#the-report) defines it) or `all`. A plan without a status uses
`unsolved`. A problem list without a status shows every problem. `order` is `rank` (list order,
the default), `number`, `easy-first` or `random` (a shuffle that is the same on every request).
The server ignores unknown filter values.

A practice plan is a list, its filters, a status and an order. `/next` never returns the topics
of the next problem, so it cannot give away the answer of a flashcard. The server keeps the 8
most recently used unpinned plans and up to 50 pinned plans. A plan name is 1 to 60 characters.

`list` is the id of one of your lists. With `list`, `/problems` and `/next` use that list
instead of the company list. In your list, `rank` is the order in which you added the problems.
The server does not keep a plan over one of your lists in `/plans`, because the server keeps the
list itself. You can have 50 lists. A list holds 1,000 problems at most, each problem one time.
A list name is 1 to 60 characters.

## The report

`GET /report?company=` (with `any`, every company) returns `report` and the insights of the
progress page. Each figure covers one of three scopes: the most-asked problems of the company
(readiness), its 6-month list, or everything that you did on any list.

`report` holds:

| Field | Scope | Holds |
| --- | --- | --- |
| `readiness` | Most asked | As `GET /readiness` returns it, below |
| `trend` | Most asked | `{practiceDays, points}`: readiness at the end of each day, `{day, readiness}`, from your first day of practice (at most 90 days back) to today. The list omits days before readiness had any data. `points` is empty until `practiceDays`, your distinct days with practice, reaches 7 |
| `counts` | 6-month list | Cards `due`, `new`, on the `again` list and on the `less` list |
| `byDifficulty` | 6-month list | `{difficulty, seen, total}`: cards graded at least once, per difficulty |
| `accuracy` | Any list | Mean topic score (F1) of the last 50 graded cards; `null` before any grade |
| `graded` | Any list | Number of grades given, without skips |
| `streakDays` | Any list | Consecutive days with a graded card or a submission, that end today or yesterday: the days that the activity calendar shades |
| `topics` | Any list | The topics that you name least, weakest first: `{topic, score, named, seen}`. A topic gets a rating when `seen`, the graded cards that carry it, reaches 5. `score` is `named / (named + (misses + false alarms) / 2)`, where a false alarm is when you name the topic on a card that does not have it. The list shows only topics under 0.6 |

`GET /readiness?company=` returns the readiness alone, for the page header:
`{score, period, problems, recent, solved, shaky, cards, fading}`. It covers the `problems`
most-asked problems of the company (at most 100), from its 6-month list, or from its all-time
list (`period` is then `all`) when the 6-month list has fewer than 25 problems. `recent` is the
size of the 6-month list. For each problem, with `f` its frequency in that list:

```text
score = Σ f · (0.6 · code + 0.4 · card) / Σ f
code  = 1 for a clean solve in the judge, 0.5 for a shaky one, else 0
card  = 1 when the card's last grade was "Got it" or "Visit less often" and it is not overdue,
        0.5 when it is overdue by less than its interval, else 0
```

`score` is `null` until you grade a card or submit a solution for one of the problems. `solved`
and `shaky` count the problems with each coding credit. `cards` and `fading` count the problems
with a full card credit and with a half card credit.

The insights cover the 6-month list of the company:

| Field | Holds |
| --- | --- |
| `coding` | `byDifficulty` (`{difficulty, solved, total}`), `tried`, `firstTry` (solves with no real failure before the first Accepted), `submissions` and `failures`: the failed submissions before the first Accepted of each problem (all of them while the problem is unsolved), as counts of `wrongAnswer`, `timeLimitExceeded`, `memoryLimitExceeded`, `runtimeError`, `compileError` and `outputLimitExceeded` |
| `shaky` | The shaky solves of the list, newest first: `{id, slug, title, difficulty, failures, solvedAt}`, with the failures before the first Accepted |
| `shakyElsewhere` | How many shaky solves are outside the list |
| `topicMap` | The topics of the list, most problems first: `{topic, problems, covered, solved, graded, named}`. `covered` counts the problems that you graded or solved, `graded` the graded cards of the problems of the list with the topic, and `named` how many of those cards name it (`null` below 5) |
| `activity` | `{start, today, days}`: 26 weeks from a Monday, in the time zone of the server, with `{day, reviews, submissions}` for each day that you practiced |

A real failure is a wrong answer, a time limit, a memory limit or a runtime error. Compile
errors and output limits do not count. A solve is shaky when two or more real failures came
before the first Accepted, or when any time limit did. A later Accepted clears the shaky state.
That Accepted is one at least a calendar day after the first Accepted, with no real failure
since the Accepted before it.

The report counts every submission. `GET /submissions/:id` returns the code and result only
for the newest 100 submissions of a problem and its latest Accepted submission. Days are
calendar days in the time zone of the server.

## Errors

An error is `{"error": "..."}` with status 400 for invalid input, 404 for an unknown problem, plan
or endpoint, and 415 when the body is not `application/json`.
