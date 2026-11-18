"""Minimum Cost to Merge Stones: piles of stones and a merge size k."""


def check(stones: list[int], k: int) -> None:
    assert 1 <= len(stones) <= 30, "1 <= n <= 30"
    assert all(1 <= x <= 100 for x in stones), "1 <= stones[i] <= 100"
    assert 2 <= k <= 30, "2 <= k <= 30"
