"""Count K-th Roots in a Range: bounds l, r and a power k."""


def check(l: int, r: int, k: int) -> None:  # noqa: E741
    assert 0 <= l <= r <= 10**9, "0 <= l <= r <= 10^9"
    assert 1 <= k <= 30, "1 <= k <= 30"
