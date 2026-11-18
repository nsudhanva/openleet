"""K-th Smallest in Lexicographical Order: integers n and k."""


def check(n: int, k: int) -> None:
    assert 1 <= k <= n <= 10**9, "1 <= k <= n <= 10^9"
