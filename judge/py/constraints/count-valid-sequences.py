"""Count Valid Sequences: positive integers n and k."""


def check(n: int, k: int) -> None:
    assert 1 <= n <= 5 * 10**5, "1 <= n <= 5 * 10^5"
    assert 1 <= k <= n, "1 <= k <= n"
