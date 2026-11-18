"""Stone Game VIII: a row of stone values."""


def check(stones: list[int]) -> None:
    assert isinstance(stones, list), "stones is a list"
    assert 2 <= len(stones) <= 10**5, "2 <= n <= 10^5"
    assert all(isinstance(v, int) and -(10**4) <= v <= 10**4 for v in stones), (
        "-10^4 <= stones[i] <= 10^4"
    )
