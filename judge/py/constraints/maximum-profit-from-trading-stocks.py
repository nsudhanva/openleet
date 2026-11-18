"""Maximum Profit From Trading Stocks: present and future prices and a budget."""


def check(present: list[int], future: list[int], budget: int) -> None:
    n = len(present)
    assert 1 <= n <= 1000, "1 <= n <= 1000"
    assert len(future) == n, "n == present.length == future.length"
    assert all(0 <= v <= 100 for v in present), "0 <= present[i] <= 100"
    assert all(0 <= v <= 100 for v in future), "0 <= future[i] <= 100"
    assert 0 <= budget <= 1000, "0 <= budget <= 1000"
