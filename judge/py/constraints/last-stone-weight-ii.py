"""Last Stone Weight II: a list of stone weights."""


def check(stones: list[int]) -> None:
    assert 1 <= len(stones) <= 30, "1 <= stones.length <= 30"
    assert all(1 <= v <= 100 for v in stones), "1 <= stones[i] <= 100"
