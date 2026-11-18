"""Add to Array-Form of Integer: a digit list and an integer k."""


def check(num: list[int], k: int) -> None:
    assert 1 <= len(num) <= 10**4, "1 <= num.length <= 10^4"
    assert all(0 <= d <= 9 for d in num), "0 <= num[i] <= 9"
    assert num[0] != 0 or len(num) == 1, "num has no leading zeros except for the zero itself"
    assert 1 <= k <= 10**4, "1 <= k <= 10^4"
