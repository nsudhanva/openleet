"""Shuffle String: a lowercase string and a permutation of its indices."""


def check(s: str, indices: list[int]) -> None:
    n = len(s)
    assert n == len(indices), "s.length == indices.length == n"
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert s.isascii() and s.isalpha() and s.islower(), (
        "s consists of only lowercase English letters"
    )
    assert all(0 <= i < n for i in indices), "0 <= indices[i] < n"
    assert len(set(indices)) == n, "all values of indices are unique"
