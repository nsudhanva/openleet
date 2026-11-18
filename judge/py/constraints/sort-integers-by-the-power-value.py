"""Sort Integers by The Power Value: a range lo..hi and a rank k."""


def check(lo: int, hi: int, k: int) -> None:
    assert 1 <= lo <= hi <= 1000, "1 <= lo <= hi <= 1000"
    assert 1 <= k <= hi - lo + 1, "1 <= k <= hi - lo + 1"
