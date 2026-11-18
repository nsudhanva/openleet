"""Alternating Groups II: a circular 0/1 colour array and a group size."""


def check(colors: list[int], k: int) -> None:
    assert 3 <= len(colors) <= 10**5, "3 <= colors.length <= 10^5"
    assert all(c in (0, 1) for c in colors), "0 <= colors[i] <= 1"
    assert 3 <= k <= len(colors), "3 <= k <= colors.length"
