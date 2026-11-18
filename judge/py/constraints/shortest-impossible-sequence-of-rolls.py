"""Shortest Impossible Sequence of Rolls: k-sided die rolls and the side count k."""


def check(rolls: list[int], k: int) -> None:
    assert 1 <= len(rolls) <= 10**5, "1 <= n <= 10^5"
    assert k <= 10**5, "k <= 10^5"
    assert all(1 <= r <= k for r in rolls), "1 <= rolls[i] <= k"
