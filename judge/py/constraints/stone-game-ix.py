"""Stone Game IX: an array of stone values."""


def check(stones: list[int]) -> None:
    assert 1 <= len(stones) <= 10**5, "1 <= stones.length <= 10^5"
    assert all(1 <= v <= 10**4 for v in stones), "1 <= stones[i] <= 10^4"
