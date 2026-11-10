"""Build data/problems.json from the Google company lists and doocs/leetcode statements.

The CSVs (liquidslr/leetcode-company-wise-problems) give, for the last 30 days, 3 months and
6 months, which problems Google asked, in frequency order, with their topics. The 6-month list
is the full set; the shorter periods are subsets of it.
doocs/leetcode (CC BY-SA 4.0) gives the problem statement. Premium problems keep no statement:
the app links to LeetCode for those.
The classic list adds every free problem numbered 1 to 1000 that Google did not ask; those have an
empty `asked`, and their difficulty and topics come from the doocs front matter.
"""

import csv
import io
import json
import re
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from google.sanitize import sanitize_html

LIST_URL = "https://raw.githubusercontent.com/liquidslr/leetcode-company-wise-problems/main/Google"
# Period key -> CSV file name in the company folder. The last one is the full problem set.
PERIODS = {
    "30d": "1.%20Thirty%20Days.csv",
    "3m": "2.%20Three%20Months.csv",
    "6m": "3.%20Six%20Months.csv",
}
DOOCS_RAW = "https://raw.githubusercontent.com/doocs/leetcode/main"
DOOCS_INDEX = f"{DOOCS_RAW}/solution/README_EN.md"

DATA_DIR = Path("data")
CACHE_DIR = DATA_DIR / ".cache"
PROBLEMS_PATH = DATA_DIR / "problems.json"

DESCRIPTION = re.compile(r"<!-- description:start -->(.*?)<!-- description:end -->", re.S)
INDEX_LINK = re.compile(r"\[(.+)\]\((/solution/.+)\)")
LEETCODE_LINK = re.compile(r"^# \[\d+\. .+\]\((https://leetcode\.com/problems/[^)]+)\)", re.M)
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---", re.S)
# The classic list: every free problem numbered 1 to CLASSIC_MAX.
CLASSIC_MAX = 1000


@dataclass(frozen=True)
class DoocsEntry:
    id: int
    title: str
    path: str
    premium: bool


@dataclass(frozen=True)
class Asked:
    rank: int
    frequency: float


@dataclass(frozen=True)
class Problem:
    id: int
    slug: str
    title: str
    difficulty: str
    # Rank and frequency for each period in which Google asked the problem.
    asked: dict[str, Asked]
    url: str
    topics: list[str]
    premium: bool
    description: str | None


def title_key(title: str) -> str:
    return re.sub(r"[^a-z0-9]", "", title.lower())


def fetch(url: str, cache_name: str) -> str:
    """GET a URL once; later runs read the cached copy."""
    path = CACHE_DIR / cache_name
    if path.exists():
        return path.read_text()
    with urllib.request.urlopen(url, timeout=60) as response:
        text = response.read().decode()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return text


def parse_doocs_index(markdown: str) -> dict[str, DoocsEntry]:
    entries: dict[str, DoocsEntry] = {}
    for line in markdown.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 5 or not cells[0].isdigit():
            continue
        if link := INDEX_LINK.match(cells[1]):
            title, path = link.groups()
            entries[title_key(title)] = DoocsEntry(int(cells[0]), title, path, "🔒" in cells[-1])
    return entries


def readme(entry: DoocsEntry) -> str:
    return fetch(f"{DOOCS_RAW}{entry.path}", f"doocs/{entry.id:04d}.md")


def description(entry: DoocsEntry) -> str | None:
    if entry.premium:
        return None
    match = DESCRIPTION.search(readme(entry))
    return sanitize_html(match.group(1)) if match else None


def front_matter(markdown: str) -> tuple[str, list[str]]:
    """Difficulty and topic tags from a doocs README's YAML front matter."""
    match = FRONT_MATTER.match(markdown)
    if not match:
        raise SystemExit("doocs README without front matter")
    difficulty, tags, in_tags = "", [], False
    for line in match.group(1).splitlines():
        if line.startswith("difficulty:"):
            difficulty = line.split(":", 1)[1].strip()
        in_tags = line.startswith("tags:") or (in_tags and line.startswith(" "))
        if in_tags and line.strip().startswith("- "):
            tags.append(line.strip()[2:].strip())
    return difficulty, tags


def classic_problem(entry: DoocsEntry) -> Problem:
    """A free problem numbered 1 to 1000 that Google did not ask."""
    markdown = readme(entry)
    link = LEETCODE_LINK.search(markdown)
    if not link:
        raise SystemExit(f"No LeetCode link in doocs README {entry.id}")
    url = link.group(1).rstrip("/")
    difficulty, tags = front_matter(markdown)
    return Problem(
        id=entry.id,
        slug=slug_from_url(url),
        title=entry.title,
        difficulty=difficulty,
        asked={},
        url=url,
        topics=tags,
        premium=False,
        description=description(entry),
    )


def slug_from_url(url: str) -> str:
    return urllib.parse.urlparse(url).path.rstrip("/").rsplit("/", 1)[-1]


def period_rows(period: str) -> list[dict[str, str]]:
    text = fetch(f"{LIST_URL}/{PERIODS[period]}", f"google-{period}.csv")
    return list(csv.DictReader(io.StringIO(text)))


def asked_by_slug() -> dict[str, dict[str, Asked]]:
    asked: dict[str, dict[str, Asked]] = {}
    for period in PERIODS:
        for rank, row in enumerate(period_rows(period), 1):
            stat = Asked(rank=rank, frequency=float(row["Frequency"]))
            asked.setdefault(slug_from_url(row["Link"]), {})[period] = stat
    return asked


def build_problems() -> list[Problem]:
    rows = period_rows(list(PERIODS)[-1])
    asked = asked_by_slug()
    index = parse_doocs_index(fetch(DOOCS_INDEX, "doocs-index.md"))

    missing = [row["Title"] for row in rows if title_key(row["Title"]) not in index]
    if missing:
        raise SystemExit(f"No doocs entry for: {missing}")

    entries = [index[title_key(row["Title"])] for row in rows]
    with ThreadPoolExecutor(max_workers=8) as pool:
        descriptions = list(pool.map(description, entries))

    google = [
        Problem(
            id=entry.id,
            slug=slug_from_url(row["Link"]),
            title=row["Title"].strip(),
            difficulty=row["Difficulty"].capitalize(),
            asked=asked[slug_from_url(row["Link"])],
            url=row["Link"],
            topics=[topic.strip() for topic in row["Topics"].split(",") if topic.strip()],
            premium=entry.premium,
            description=text,
        )
        for row, entry, text in zip(rows, entries, descriptions, strict=True)
    ]
    asked_ids = {problem.id for problem in google}
    classic = sorted(
        (
            e
            for e in index.values()
            if e.id <= CLASSIC_MAX and not e.premium and e.id not in asked_ids
        ),
        key=lambda e: e.id,
    )
    with ThreadPoolExecutor(max_workers=8) as pool:
        return google + list(pool.map(classic_problem, classic))


def ingest() -> None:
    problems = build_problems()
    document = {
        "sources": {
            "lists": {period: f"{LIST_URL}/{name}" for period, name in PERIODS.items()},
            "statements": "https://github.com/doocs/leetcode (CC BY-SA 4.0)",
            "classic": f"free problems 1 to {CLASSIC_MAX} from the doocs index",
            "fetchedAt": datetime.now(UTC).date().isoformat(),
        },
        "problems": [asdict(problem) for problem in problems],
    }
    PROBLEMS_PATH.write_text(json.dumps(document, indent=1, ensure_ascii=False) + "\n")
    premium = sum(problem.premium for problem in problems)
    classic = sum(not problem.asked for problem in problems)
    print(
        f"Wrote {len(problems)} problems ({premium} premium, {classic} classic-only) "
        f"to {PROBLEMS_PATH}"
    )
