"""Moving Stones Until Consecutive II: an array of unique stone positions."""


def check(stones: list[int]) -> None:
    assert 3 <= len(stones) <= 10**4, "3 <= stones.length <= 10^4"
    assert all(1 <= v <= 10**9 for v in stones), "1 <= stones[i] <= 10^9"
    assert len(set(stones)) == len(stones), "all the values of stones are unique"
