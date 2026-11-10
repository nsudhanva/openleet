"""Build data/problems.json: the problems top tech companies ask, plus LeetCode 1 to 1000.

Company lists come from liquidslr/leetcode-company-wise-problems: for each company, which
problems it asked in the last 30 days, 3 months, 6 months and all time, in frequency order,
with difficulty and topics. Every problem a listed company asked is included, plus every
problem numbered 1 to CLASSIC_MAX. Statements (premium ones included), and difficulty and tags
for problems no company lists, come from doocs/leetcode (CC BY-SA 4.0).

Each problem stores, per company and period, its rank (1 = asked most) and frequency (0-100).
"""

import csv
import io
import json
import re
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from openleet.data import CACHE_DIR, PROBLEMS_PATH, cached_download, doocs_readme_path
from openleet.sanitize import sanitize_html

LISTS_REPO = "liquidslr/leetcode-company-wise-problems"
LISTS_RAW = f"https://raw.githubusercontent.com/{LISTS_REPO}/main"
# Company slug used in the app -> display name, which is also its folder in the lists repo.
# Most asked first, the order of the UI's company picker.
COMPANIES = {
    "google": "Google",
    "meta": "Meta",
    "amazon": "Amazon",
    "microsoft": "Microsoft",
    "apple": "Apple",
    "netflix": "Netflix",
    "nvidia": "Nvidia",
    "openai": "OpenAI",
    "bloomberg": "Bloomberg",
    "uber": "Uber",
    "tiktok": "TikTok",
    "oracle": "Oracle",
    "salesforce": "Salesforce",
    "linkedin": "LinkedIn",
    "adobe": "Adobe",
    "snowflake": "Snowflake",
    "doordash": "DoorDash",
    "airbnb": "Airbnb",
    "atlassian": "Atlassian",
    "x": "X",
    "tesla": "Tesla",
    "databricks": "Databricks",
    "stripe": "Stripe",
    "coinbase": "Coinbase",
}
# Period key -> CSV file in each company folder.
PERIODS = {
    "30d": "1. Thirty Days.csv",
    "3m": "2. Three Months.csv",
    "6m": "3. Six Months.csv",
    "all": "5. All.csv",
}
CLASSIC_MAX = 1000

DOOCS_RAW = "https://raw.githubusercontent.com/doocs/leetcode/main"
DOOCS_INDEX = f"{DOOCS_RAW}/solution/README_EN.md"
FETCH_WORKERS = 16

DESCRIPTION = re.compile(r"<!-- description:start -->(.*?)<!-- description:end -->", re.S)
INDEX_LINK = re.compile(r"\[(.+)\]\((/solution/.+)\)")
LEETCODE_LINK = re.compile(r"^# \[\d+\. .+\]\((https://leetcode\.com/problems/[^)]+)\)", re.M)
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---", re.S)


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
class Listing:
    """What one company's lists say about one problem."""

    title: str
    difficulty: str
    topics: list[str]
    asked: dict[str, Asked]


@dataclass(frozen=True)
class Problem:
    id: int
    slug: str
    title: str
    difficulty: str
    # Company slug -> period -> rank and frequency, for every company that asked it.
    companies: dict[str, dict[str, Asked]]
    url: str
    topics: list[str]
    premium: bool
    description: str | None


def title_key(title: str) -> str:
    return re.sub(r"[^a-z0-9]", "", title.lower())


def fetch(url: str, path: Path) -> str:
    return cached_download(url, path).read_text()


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
    return fetch(f"{DOOCS_RAW}{entry.path}", doocs_readme_path(entry.id))


def statement(markdown: str) -> str | None:
    match = DESCRIPTION.search(markdown)
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


# doocs' older names for LeetCode's topic tags, mapped to the names the company lists use.
TOPIC_ALIASES = {
    "Dijkstra": "Dijkstra's Algorithm",
    "Graph": "Graph Theory",
    "Heap": "Heap (Priority Queue)",
    "Nearest Pair of Points": "Closest Pair of Points",
    "Sort": "Sorting",
    "Union Find": "Union-Find",
}


def canonical_topics(tags: list[str]) -> list[str]:
    """Tags under LeetCode's current names, each once, in their original order."""
    return list(dict.fromkeys(TOPIC_ALIASES.get(tag, tag) for tag in tags))


def slug_from_url(url: str) -> str:
    return urllib.parse.urlparse(url).path.rstrip("/").rsplit("/", 1)[-1]


def company_rows(folder: str, period: str) -> list[dict[str, str]]:
    path = urllib.parse.quote(f"{folder}/{PERIODS[period]}")
    text = fetch(f"{LISTS_RAW}/{path}", CACHE_DIR / "companies" / folder / f"{period}.csv")
    return list(csv.DictReader(io.StringIO(text)))


def listings() -> dict[str, dict[str, Listing]]:
    """Problem slug -> company slug -> what that company's lists say."""
    found: dict[str, dict[str, Listing]] = {}
    for company, folder in COMPANIES.items():
        for period in PERIODS:
            for rank, row in enumerate(company_rows(folder, period), 1):
                slug = slug_from_url(row["Link"])
                topics = [t.strip() for t in row["Topics"].split(",") if t.strip()]
                listing = found.setdefault(slug, {}).setdefault(
                    company,
                    Listing(row["Title"].strip(), row["Difficulty"].capitalize(), topics, {}),
                )
                listing.asked[period] = Asked(rank=rank, frequency=float(row["Frequency"]))
    return found


def build_problem(entry: DoocsEntry, listed: dict[str, Listing] | None) -> Problem:
    markdown = readme(entry)
    link = LEETCODE_LINK.search(markdown)
    if not link:
        raise SystemExit(f"No LeetCode link in doocs README {entry.id}")
    url = link.group(1).rstrip("/")
    difficulty, tags = front_matter(markdown)
    if listed:
        # The company lists carry LeetCode's current difficulty and topics.
        first = next(iter(listed.values()))
        difficulty, tags = first.difficulty, first.topics or tags
    return Problem(
        id=entry.id,
        slug=slug_from_url(url),
        title=entry.title,
        difficulty=difficulty,
        companies={c: dict(listing.asked) for c, listing in (listed or {}).items()},
        url=url,
        topics=canonical_topics(tags),
        premium=entry.premium,
        description=statement(markdown),
    )


def build_problems() -> list[Problem]:
    index = parse_doocs_index(fetch(DOOCS_INDEX, CACHE_DIR / "doocs-index.md"))
    by_title: dict[str, dict[str, Listing]] = {}
    for listed in listings().values():
        by_title[title_key(next(iter(listed.values())).title)] = listed
    missing = sorted(t for t in by_title if t not in index)
    if missing:
        print(f"No doocs entry for {len(missing)} listed problems, skipped: {missing[:10]}")
    wanted = [
        (entry, by_title.get(key))
        for key, entry in index.items()
        if key in by_title or entry.id <= CLASSIC_MAX
    ]
    with ThreadPoolExecutor(max_workers=FETCH_WORKERS) as pool:
        problems = list(pool.map(lambda pair: build_problem(*pair), wanted))
    return sorted(problems, key=lambda p: p.id)


def ingest(problems_path: Path = PROBLEMS_PATH) -> None:
    problems = build_problems()
    counts = {c: sum(c in p.companies for p in problems) for c in COMPANIES}
    document = {
        "sources": {
            "lists": f"https://github.com/{LISTS_REPO}",
            "statements": "https://github.com/doocs/leetcode (CC BY-SA 4.0)",
            "classic": f"free problems 1 to {CLASSIC_MAX} from the doocs index",
            "fetchedAt": datetime.now(UTC).date().isoformat(),
        },
        "companies": [
            {"slug": slug, "name": name, "problems": counts[slug]}
            for slug, name in COMPANIES.items()
            if counts[slug]
        ],
        "problems": [asdict(problem) for problem in problems],
    }
    problems_path.write_text(json.dumps(document, ensure_ascii=False, separators=(",", ":")) + "\n")
    premium = sum(problem.premium for problem in problems)
    print(f"Wrote {len(problems)} problems ({premium} premium) to {problems_path}")
