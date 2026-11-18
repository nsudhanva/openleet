"""Find Kth Bit in Nth Binary String: the string index n and a position k."""


def check(n: int, k: int) -> None:
    assert 1 <= n <= 20, "1 <= n <= 20"
    assert 1 <= k <= 2**n - 1, "1 <= k <= 2^n - 1"
