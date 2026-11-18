"""Number of Ways to Rearrange Sticks With K Sticks Visible: stick count n and visible count k."""


def check(n: int, k: int) -> None:
    assert 1 <= n <= 1000, "1 <= n <= 1000"
    assert 1 <= k <= n, "1 <= k <= n"
