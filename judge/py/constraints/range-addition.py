"""Range Addition: an array length and [start, end, inc] updates."""


def check(length: int, updates: list[list[int]]) -> None:
    assert 1 <= length <= 10**5, "1 <= length <= 10^5"
    assert 0 <= len(updates) <= 10**4, "0 <= updates.length <= 10^4"
    assert all(len(u) == 3 for u in updates), "updates[i].length == 3"
    assert all(0 <= s <= e < length for s, e, _ in updates), "0 <= startIdxi <= endIdxi < length"
    assert all(-1000 <= c <= 1000 for _, _, c in updates), "-1000 <= inci <= 1000"
