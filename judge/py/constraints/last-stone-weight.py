"""Last Stone Weight: a list of stone weights."""


def check(stones: list[int]) -> None:
    assert 1 <= len(stones) <= 30, "1 <= stones.length <= 30"
    assert all(1 <= v <= 1000 for v in stones), "1 <= stones[i] <= 1000"
