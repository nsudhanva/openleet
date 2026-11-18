"""Find And Replace in String: a string and parallel lists of indices, sources and targets."""

from itertools import pairwise


def _lower(t: str) -> bool:
    return isinstance(t, str) and t.isascii() and t.islower() and t.isalpha()


def check(s: str, indices: list[int], sources: list[str], targets: list[str]) -> None:
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    k = len(indices)
    assert len(sources) == k and len(targets) == k, (
        "k == indices.length == sources.length == targets.length"
    )
    assert 1 <= k <= 100, "1 <= k <= 100"
    assert all(0 <= i < len(s) for i in indices), "0 <= indices[i] < s.length"
    assert all(1 <= len(t) <= 50 for t in sources + targets), (
        "1 <= sources[i].length, targets[i].length <= 50"
    )
    assert _lower(s), "s consists of only lowercase English letters"
    assert all(_lower(t) for t in sources + targets), (
        "sources[i] and targets[i] consist of only lowercase letters"
    )
    spans = sorted(
        (i, i + len(src)) for i, src in zip(indices, sources, strict=True) if s.startswith(src, i)
    )
    assert all(a[1] <= b[0] for a, b in pairwise(spans)), "the replacements do not overlap"
