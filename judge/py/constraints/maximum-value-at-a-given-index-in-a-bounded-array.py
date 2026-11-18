"""Maximum Value at a Given Index in a Bounded Array: length n, an index and a sum bound."""


def check(n: int, index: int, maxSum: int) -> None:
    assert 1 <= n <= maxSum <= 10**9, "1 <= n <= maxSum <= 10^9"
    assert 0 <= index < n, "0 <= index < n"
