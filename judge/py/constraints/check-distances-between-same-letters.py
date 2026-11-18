"""Check Distances Between Same Letters: a string with each letter twice and 26 distances."""

from collections import Counter


def check(s: str, distance: list[int]) -> None:
    assert isinstance(s, str) and isinstance(distance, list), "s is a string, distance a list"
    assert 2 <= len(s) <= 52, "2 <= s.length <= 52"
    assert all("a" <= c <= "z" for c in s), "s consists only of lowercase English letters"
    assert all(c == 2 for c in Counter(s).values()), "each letter appears in s exactly twice"
    assert len(distance) == 26, "distance.length == 26"
    assert all(0 <= d <= 50 for d in distance), "0 <= distance[i] <= 50"
