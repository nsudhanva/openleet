"""High Five: [ID, score] pairs where every ID has at least five scores."""

from collections import Counter


def check(items: list[list[int]]) -> None:
    assert 1 <= len(items) <= 1000, "1 <= items.length <= 1000"
    assert all(len(r) == 2 for r in items), "items[i].length == 2"
    assert all(1 <= i <= 1000 for i, _ in items), "1 <= IDi <= 1000"
    assert all(0 <= s <= 100 for _, s in items), "0 <= scorei <= 100"
    counts = Counter(i for i, _ in items)
    assert all(c >= 5 for c in counts.values()), "each ID has at least five scores"
