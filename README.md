# OpenLeet

Practice the LeetCode problems that top tech companies ask. Flashcards schedule your reviews, and
a judge checks the Python solutions that you write in the browser.

[Live site](https://openleet.sudhanva.me) · [Quick start](#quick-start) · [Docs](docs/)

## Features

- Problem lists for 24 companies, sorted by how recently the company asked each problem (30 days,
  3 months, 6 months or all time). The site also has every free problem from 1 to 1000.
- Flashcards: name the topics of a problem, then check the approach and its complexity. Spaced
  repetition decides when each card comes back.
- Run your solutions against the examples, the hidden tests and the large stress tests. The judge
  gives the same verdicts as LeetCode.
- Next moves to the next problem in your practice plan, with or without a solve. After an
  accepted submission, it also offers related plans. A plan is a list, topic, difficulty and
  order that you can change at any time. The app remembers your recent plans. You can pin the
  plans that you want to keep.
- Your own lists: tick problems, or use Add to list on a problem, to put them in a named list.
  Next, progress and the plan filters work on your list as they work on a company list. You can
  rename a list, remove problems from it, or delete it.
- Readiness for the 100 most-asked problems of a company, weighted by how often the company asks
  each problem: 60% for a clean solve in the judge, 40% for a current flashcard. A daily trend,
  your streak and the topics that you name least show beside it.
- Video explanations on YouTube for each problem that has one: the NeetCode video first, then
  the Greg Hogg video, then the most viewed video by anyone else.
- Keyboard shortcuts. The About page of the site lists them.
- No account. The server that runs the app stores your progress.

## Quick start

If Docker is installed, run:

```bash
git clone https://github.com/nsudhanva/openleet && cd openleet
docker compose up -d
```

Open <http://openleet.localhost>. If port 80 is in use, run `HTTP_PORT=8088 docker compose up -d`
and open <http://openleet.localhost:8088>.

On an Ubuntu server, point a domain at the server and open ports 80 and 443. Then run:

```bash
git clone https://github.com/nsudhanva/openleet && cd openleet
sudo SITE_ADDRESS=openleet.example.com deploy/install.sh
```

The server serves <https://openleet.example.com> with a certificate from Let's Encrypt. It
installs new releases automatically. See [Deployment](docs/deployment.md#new-server).

## Documentation

- [Architecture](docs/architecture.md): how pages load, how the judge checks a submission, and
  where the tests come from.
- [Development](docs/development.md): how to run the app from source, the checks and the
  end-to-end tests.
- [Deployment](docs/deployment.md): releases, the production server and recovery.
- [API](docs/api.md): the JSON endpoints.

## Data sources

- Company lists: [liquidslr/leetcode-company-wise-problems](https://github.com/liquidslr/leetcode-company-wise-problems)
- Problem statements and solutions: [doocs/leetcode](https://github.com/doocs/leetcode)
  (CC BY-SA 4.0)
- Starter code, tests and solutions: [LeetCodeDataset](https://huggingface.co/datasets/newfacade/LeetCodeDataset)
  (Apache-2.0)
- Accepted submissions. OpenLeet uses them only to check tests at build time and never ships
  them: [Mercury](https://huggingface.co/datasets/Elfsong/Mercury) (CC BY-NC)
- Video explanations: the video that [neetcode.io](https://neetcode.io) links for each problem
  ([neetcode-gh/leetcode](https://github.com/neetcode-gh/leetcode)), and YouTube channel uploads
  and searches that [yt-dlp](https://github.com/yt-dlp/yt-dlp) lists (`uv run openleet videos`
  writes `data/videos.json`)
- Approaches and hints: Claude agents wrote them and Codex CLI reviewed them
  (`data/approach-reviews.json`).

## License

[MIT](LICENSE). Problem statements from doocs/leetcode keep the CC BY-SA 4.0 license.
