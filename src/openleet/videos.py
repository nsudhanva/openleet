"""Build data/videos.json: YouTube explanations of each problem, at most one per creator.

In order: NeetCode (the video neetcode.io links for the problem, else the most viewed match on
the NeetCode and NeetCodeIO channels), Greg Hogg (the most viewed match on his channel), then
the most viewed match by anyone else in a YouTube search for the problem. A video matches a
problem when its title names the problem's LeetCode number and title words, or its exact
title. NeetCode's and Greg Hogg's Shorts count when they have no longer video of the problem;
nobody else's do.
"""

import json
import re
import time
from collections.abc import Iterable, Iterator
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from openleet.data import CACHE_DIR, VIDEOS_PATH, cached_download

NEETCODE_SITE = "https://raw.githubusercontent.com/neetcode-gh/leetcode/main/.problemSiteData.json"
NEETCODE = ("NeetCode", ("UC_mYaQAE6-71rjSN6CeCA-g", "UCevUmOfLTUX9MNGJQKsPdIA"))
GREG_HOGG = ("Greg Hogg", ("UCJublDh2UsiIKsAE1553miw",))
CREATORS = (NEETCODE, GREG_HOGG)
SEARCH_RESULTS = 20
SEARCH_WORKERS = 3
SEARCH_TRIES = 4
# Shorts are at most a minute long.
MIN_SECONDS = 61
YOUTUBE_CACHE = CACHE_DIR / "youtube"

# "Leetcode 1", "LeetCode #1", "LC 1", "1. Two Sum"
NUMBER = re.compile(r"\b(?:leet\s*code|lc)\s*(?:#|no\.?|problem)?\s*(\d{1,4})\b", re.I)
LEADING_NUMBER = re.compile(r"^\W*(\d{1,4})\s*[.:)]")
# What separates a title's parts: " - " (or an en or em dash), " | ", ": ", brackets.
SEPARATOR = re.compile(r"\s[-\u2013\u2014]\s|[|:()[\]\u3010\u3011]")
WORD = re.compile(r"[a-z0-9]+")
# Words a part may start with before the problem's title: "Leetcode 1. Two Sum".
PREFIX_WORDS = frozenset({"leetcode", "leet", "code", "lc", "problem", "no"})
FILLER_WORDS = frozenset({"a", "an", "the", "of", "in", "to", "and", "or", "with", "is", "i"})


@dataclass(frozen=True)
class Video:
    id: str
    title: str
    channel: str
    channel_id: str
    views: int
    seconds: int

    @classmethod
    def of(cls, entry: dict[str, Any], channel: str = "", channel_id: str = "") -> Video:
        return cls(
            id=entry["id"],
            title=entry.get("title") or "",
            channel=entry.get("channel") or channel,
            channel_id=entry.get("channel_id") or channel_id,
            views=entry.get("view_count") or 0,
            seconds=int(entry.get("duration") or 0),
        )


def words(text: str) -> list[str]:
    return WORD.findall(text.lower())


def numbers(title: str) -> set[int]:
    """The LeetCode numbers a video title names."""
    found = {int(n) for n in NUMBER.findall(title)}
    for part in SEPARATOR.split(title):
        if leading := LEADING_NUMBER.match(part):
            found.add(int(leading.group(1)))
    return found


def names(video_title: str, problem_title: str) -> bool:
    """Whether a part of the video title (or a run of parts) is exactly the problem's title,
    after a "Leetcode 1." style prefix: "Two Sum - Leetcode 1" names Two Sum, but "Two Sum II"
    and "Best Time to Buy and Sell Stock with Cooldown" do not name their shorter namesakes."""
    want = words(problem_title)
    tokens = [
        (w, part) for part, text in enumerate(SEPARATOR.split(video_title)) for w in words(text)
    ]
    for start in range(len(tokens) - len(want) + 1):
        end = start + len(want)
        if [w for w, _ in tokens[start:end]] != want:
            continue
        part = tokens[start][1]
        before = [w for w, p in tokens[:start] if p == part]
        starts_part = all(w in PREFIX_WORDS or w.isdigit() for w in before)
        ends_part = end == len(tokens) or tokens[end][1] != tokens[end - 1][1]
        if starts_part and ends_part:
            return True
    return False


def has_words(video_title: str, problem_title: str) -> bool:
    """Whether every significant word of the problem's title is in the video title."""
    have = set(words(video_title))
    return all(w in have for w in words(problem_title) if w not in FILLER_WORDS)


def explains(video: Video, problem_id: int, problem_title: str, *, trusted: bool) -> bool:
    """Whether a video explains this problem. A trusted channel titles every video after the
    problem; anyone else's title must also name the problem and LeetCode, and be no Short."""
    if not trusted and video.seconds < MIN_SECONDS:
        return False
    named = numbers(video.title)
    if named and problem_id not in named:
        return False
    if trusted:
        return problem_id in named or names(video.title, problem_title)
    if problem_id in named:
        return has_words(video.title, problem_title)
    return names(video.title, problem_title) and bool(re.search(r"leet\s*code", video.title, re.I))


def youtube(url: str) -> dict[str, Any]:
    """yt-dlp's flat listing of a channel, playlist or search."""
    from yt_dlp import YoutubeDL

    options = {"extract_flat": True, "quiet": True, "no_warnings": True, "skip_download": True}
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)
    return ydl.sanitize_info(info)


def cached(path: Path, fetch: Any) -> Any:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        partial = path.with_name(path.name + ".part")
        partial.write_text(json.dumps(fetch()))
        partial.replace(path)
    return json.loads(path.read_text())


def uploads(channel_id: str) -> list[Video]:
    """Every upload of a channel (its UU playlist), Shorts included."""
    playlist = "UU" + channel_id.removeprefix("UC")
    info = cached(
        YOUTUBE_CACHE / "channels" / f"{channel_id}.json",
        lambda: youtube(f"https://www.youtube.com/playlist?list={playlist}"),
    )
    channel = info.get("channel") or info.get("uploader") or ""
    return [Video.of(e, channel, channel_id) for e in info.get("entries") or []]


def search_listing(query: str) -> dict[str, Any]:
    """A YouTube search's listing. A throttled YouTube answers 403, or lists results without
    their channels and views; both are retried with a pause, then raised."""
    for attempt in range(SEARCH_TRIES):
        try:
            info = youtube(f"ytsearch{SEARCH_RESULTS}:{query}")
            entries = info.get("entries") or []
            if not entries or any(e.get("channel_id") for e in entries):
                return info
            error: Exception = RuntimeError("results without channels")
        except Exception as raised:  # yt-dlp raises its own DownloadError and network errors
            error = raised
        if attempt + 1 < SEARCH_TRIES:
            time.sleep(30 * 2**attempt)
    raise error


def search(problem: dict[str, Any]) -> list[Video]:
    """The top results of a YouTube search for the problem; none when the search fails (it is
    not cached, so the next run tries again)."""
    query = f"leetcode {problem['id']} {problem['title']}"
    try:
        info = cached(
            YOUTUBE_CACHE / "search" / f"{problem['slug']}.json", lambda: search_listing(query)
        )
    except Exception as error:
        print(f"search failed for {problem['slug']}: {error}")
        return []
    return [Video.of(e) for e in info.get("entries") or [] if e.get("id")]


def neetcode_links() -> dict[str, str]:
    """The video neetcode.io links for each problem slug."""
    site = cached_download(NEETCODE_SITE, CACHE_DIR / "neetcode-site.json")
    return {
        row["link"].strip("/"): row["video"]
        for row in json.loads(site.read_text())
        if row.get("video")
    }


def most_viewed(videos: Iterable[Video]) -> Video | None:
    """The most viewed video, a longer one before any Short."""
    return max(videos, key=lambda v: (v.seconds >= MIN_SECONDS, v.views), default=None)


def pick(
    problem: dict[str, Any],
    found: list[Video],
    channel_videos: dict[str, list[Video]],
    neetcode: dict[str, str],
    known: dict[str, Video],
) -> Iterator[dict[str, str]]:
    """The problem's videos, one per creator, in priority order."""
    pid, title = problem["id"], problem["title"]
    taken: set[str] = set()
    for creator, channel_ids in CREATORS:
        own = [
            v
            for v in [*found, *(v for c in channel_ids for v in channel_videos[c])]
            if v.channel_id in channel_ids and explains(v, pid, title, trusted=True)
        ]
        video = most_viewed(own)
        if creator == NEETCODE[0] and (linked := neetcode.get(problem["slug"])):
            video = known.get(linked) or Video(linked, title, creator, channel_ids[0], 0, 0)
        if video:
            taken.update(channel_ids)
            yield {"creator": creator, "id": video.id, "title": video.title}
    others = (
        v
        for v in found
        if v.channel_id not in taken
        and v.channel_id not in {c for _, ids in CREATORS for c in ids}
        and explains(v, pid, title, trusted=False)
    )
    if video := most_viewed(others):
        yield {"creator": video.channel, "id": video.id, "title": video.title}


def build(problems_path: Path, out: Path = VIDEOS_PATH) -> None:
    problems = json.loads(problems_path.read_text())["problems"]
    channel_videos = {c: uploads(c) for _, ids in CREATORS for c in ids}
    known = {v.id: v for vs in channel_videos.values() for v in vs}
    neetcode = neetcode_links()
    with ThreadPoolExecutor(SEARCH_WORKERS) as pool:
        results = list(pool.map(search, problems))
    videos = {
        p["slug"]: chosen
        for p, found in zip(problems, results, strict=True)
        if (chosen := list(pick(p, found, channel_videos, neetcode, known)))
    }
    out.write_text(
        json.dumps(
            {
                "sources": {
                    "neetcode": NEETCODE_SITE,
                    "youtube": "channel uploads and searches, listed with yt-dlp",
                    "fetchedAt": datetime.now(UTC).date().isoformat(),
                },
                "videos": videos,
            },
            indent=1,
            ensure_ascii=False,
        )
        + "\n"
    )
    counts = {
        creator: sum(any(v["creator"] == creator for v in vs) for vs in videos.values())
        for creator, _ in CREATORS
    }
    print(f"{len(videos)} of {len(problems)} problems have a video; {counts}")
