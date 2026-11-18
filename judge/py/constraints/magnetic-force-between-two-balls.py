"""Magnetic Force Between Two Balls: distinct basket positions and a ball count m."""


def check(position: list[int], m: int) -> None:
    n = len(position)
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert all(1 <= p <= 10**9 for p in position), "1 <= position[i] <= 10^9"
    assert len(set(position)) == n, "all integers in position are distinct"
    assert 2 <= m <= n, "2 <= m <= position.length"
