"""Odd String Difference: equal-length lowercase words, all but one sharing a difference array."""

from itertools import pairwise


def diffs(w: str) -> tuple[int, ...]:
    return tuple(ord(b) - ord(a) for a, b in pairwise(w))


def check(words: list[str]) -> None:
    assert 3 <= len(words) <= 100, "3 <= words.length <= 100"
    n = len(words[0])
    assert all(len(w) == n for w in words), "n == words[i].length"
    assert 2 <= n <= 20, "2 <= n <= 20"
    assert all(w.isascii() and w.islower() and w.isalpha() for w in words), (
        "words[i] consists of lowercase English letters"
    )
    counts: dict[tuple[int, ...], int] = {}
    for w in words:
        d = diffs(w)
        counts[d] = counts.get(d, 0) + 1
    assert sorted(counts.values()) == [1, len(words) - 1], (
        "all words have the same difference array except one"
    )
