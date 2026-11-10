"""Validate data/approaches.json: one entry per problem, written to ASD-STE100 limits.

Mechanical checks only (shape, sentence length, unapproved words, hints that name the
technique). Accuracy is reviewed separately by model agents and Codex.
"""

import json
import re
from pathlib import Path
from typing import Any

from openleet.ingest import PROBLEMS_PATH

APPROACHES_PATH = Path("data/approaches.json")

# ASD-STE100: procedural sentences max 20 words, descriptive sentences max 25 words.
MAX_STEP_WORDS = 20
MAX_DESCRIPTIVE_WORDS = 25
STEP_COUNT = range(2, 7)
HINT_COUNT = range(1, 4)
MAX_HINT_SENTENCES = 2
COMPLEXITY = re.compile(r"^O\(.+\)")
UNAPPROVED = frozenset(
    {
        "should",
        "could",
        "would",
        "might",
        "may",
        "shall",
        "basically",
        "simply",
        "just",
        "easily",
        "obviously",
        "clearly",
        "utilize",
        "utilise",
        "leverage",
        "via",
        "etc",
        "etc.",
        "e.g.",
        "i.e.",
        "please",
        "very",
        "really",
    }
)
CODE_SPAN = re.compile(r"`[^`]*`")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z`])")

# Topic tags that describe the input rather than the technique; a hint may name them.
SHAPE_TOPICS = frozenset(
    {
        "Array",
        "String",
        "Math",
        "Matrix",
        "Database",
        "Simulation",
        "Design",
        "Tree",
        "Binary Tree",
        "Binary Search Tree",
        "Linked List",
        "Doubly-Linked List",
        "Graph Theory",
        "Directed Acyclic Graph",
        "Interactive",
        "Data Stream",
        "Iterator",
        "Geometry",
        "Brainteaser",
        "Counting",
        "Number Theory",
        "Combinatorics",
        "Randomized",
        "Enumeration",
    }
)
# How a technique tag reads in prose, when that differs from the tag itself.
TOPIC_ALIASES = {
    "Heap (Priority Queue)": ["heap", "priority queue"],
    "Depth-First Search": ["depth-first", "depth first", "dfs"],
    "Breadth-First Search": ["breadth-first", "breadth first", "bfs"],
    "Dynamic Programming": ["dynamic programming", "dp"],
    "Union-Find": ["union-find", "union find", "disjoint set", "dsu"],
    "Two Pointers": ["two pointer", "two-pointer"],
    "Hash Table": ["hash"],
    "Sorting": ["sort"],
    "Monotonic Stack": ["monotonic"],
    "Monotonic Queue": ["monotonic"],
    "Trie": ["trie", "prefix tree"],
    "Backtracking": ["backtrack"],
    "Recursion": ["recursion", "recursive"],
    "Binary Indexed Tree": ["binary indexed", "fenwick"],
    "Topological Sort": ["topological"],
    "Memoization": ["memo"],
}


def words(sentence: str) -> list[str]:
    # A code span such as `dp[i][j]` counts as one word.
    return CODE_SPAN.sub("CODE", sentence).split()


def sentences(text: str) -> list[str]:
    return [part for part in SENTENCE_END.split(text.strip()) if part]


def lint_text(text: str, max_words: int, label: str) -> list[str]:
    errors = []
    if not text.strip().endswith((".", "?")):
        errors.append(f"{label}: end each sentence with a period")
    for sentence in sentences(text):
        tokens = words(sentence)
        if len(tokens) > max_words:
            errors.append(f"{label}: {len(tokens)} words (max {max_words}): {sentence}")
        # Strip trailing punctuation too, so a sentence-final "may." is caught.
        bare = {t.lower().strip(",;:()") for t in tokens}
        bad = sorted((bare | {t.rstrip(".?!") for t in bare}) & UNAPPROVED)
        if bad:
            errors.append(f"{label}: unapproved words {bad}")
    return errors


def technique_terms(topics: list[str], title: str) -> list[str]:
    """Names of the problem's techniques, minus any the title already gives away."""
    named_by_title = title.lower()
    terms: list[str] = []
    for topic in topics:
        if topic not in SHAPE_TOPICS:
            terms += TOPIC_ALIASES.get(topic, [topic.lower()])
    return [t for t in terms if t not in named_by_title]


def lint_hints(hints: Any, topics: list[str], title: str = "") -> list[str]:
    """Hints nudge toward the idea without naming the technique the learner must guess."""
    if not isinstance(hints, list) or len(hints) not in HINT_COUNT:
        return [f"hints: need {HINT_COUNT.start}-{HINT_COUNT.stop - 1} hints"]
    errors = []
    terms = technique_terms(topics, title)
    for number, hint in enumerate(hints, 1):
        label = f"hint {number}"
        text = str(hint)
        errors += lint_text(text, MAX_DESCRIPTIVE_WORDS, label)
        if len(sentences(text)) > MAX_HINT_SENTENCES:
            errors.append(f"{label}: max {MAX_HINT_SENTENCES} sentences")
        prose = CODE_SPAN.sub("", text).lower()
        # Plurals count too: "two stacks" names the Stack technique.
        named = [t for t in terms if re.search(rf"\b{re.escape(t)}(?:s|es)?\b", prose)]
        if named:
            errors.append(f"{label}: names the technique {named}")
    return errors


def lint_entry(entry: Any, topics: list[str], title: str) -> list[str]:
    if not isinstance(entry, dict):
        return ["entry must be an object"]
    errors = []
    insight, steps = entry.get("insight"), entry.get("steps")
    if not isinstance(insight, str) or not insight.strip():
        errors.append("insight: required")
    else:
        errors += lint_text(insight, MAX_DESCRIPTIVE_WORDS, "insight")
    if not isinstance(steps, list) or len(steps) not in STEP_COUNT:
        errors.append(f"steps: need {STEP_COUNT.start}-{STEP_COUNT.stop - 1} steps")
    else:
        for number, step in enumerate(steps, 1):
            errors += lint_text(str(step), MAX_STEP_WORDS, f"step {number}")
    for field in ("time", "space"):
        if not COMPLEXITY.match(str(entry.get(field, ""))):
            errors.append(f"{field}: expected big-O, such as O(n log n)")
    return errors + lint_hints(entry.get("hints"), topics, title)


def lint(approaches: dict[str, Any], problems: list[dict[str, Any]]) -> dict[str, list[str]]:
    """`problems` need slug, title and topics; returns errors for failing slugs only."""
    known = {p["slug"] for p in problems}
    report = {
        p["slug"]: lint_entry(approaches[p["slug"]], p["topics"], p["title"])
        if p["slug"] in approaches
        else ["missing approach"]
        for p in problems
    }
    report |= {slug: ["not in problem list"] for slug in approaches if slug not in known}
    return {slug: errors for slug, errors in report.items() if errors}


def check() -> int:
    problems = json.loads(PROBLEMS_PATH.read_text())["problems"]
    approaches = json.loads(APPROACHES_PATH.read_text()) if APPROACHES_PATH.exists() else {}
    report = lint(approaches, problems)
    for slug, errors in report.items():
        for error in errors:
            print(f"{slug}: {error}")
    print(f"{len(problems) - len(report)}/{len(problems)} approaches pass")
    return 1 if report else 0
