"""Minimize the Maximum of Two Arrays: two divisors and two counts of unique values."""


def check(divisor1: int, divisor2: int, uniqueCnt1: int, uniqueCnt2: int) -> None:
    assert 2 <= divisor1 <= 10**5, "2 <= divisor1 <= 10^5"
    assert 2 <= divisor2 <= 10**5, "2 <= divisor2 <= 10^5"
    assert 1 <= uniqueCnt1 < 10**9, "1 <= uniqueCnt1 < 10^9"
    assert 1 <= uniqueCnt2 < 10**9, "1 <= uniqueCnt2 < 10^9"
    assert 2 <= uniqueCnt1 + uniqueCnt2 <= 10**9, "2 <= uniqueCnt1 + uniqueCnt2 <= 10^9"
