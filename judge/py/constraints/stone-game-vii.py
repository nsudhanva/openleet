"""Stone Game VII: a row of stone values."""


def check(stones: list[int]) -> None:
    assert isinstance(stones, list), "stones is a list"
    assert 2 <= len(stones) <= 1000, "2 <= n <= 1000"
    assert all(isinstance(v, int) and 1 <= v <= 1000 for v in stones), "1 <= stones[i] <= 1000"
