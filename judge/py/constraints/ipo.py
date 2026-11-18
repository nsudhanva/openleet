"""IPO: k projects, initial capital w, and per-project profits and capital."""


def check(k: int, w: int, profits: list[int], capital: list[int]) -> None:
    assert isinstance(profits, list) and isinstance(capital, list), "profits and capital are lists"
    assert 1 <= k <= 10**5, "1 <= k <= 10^5"
    assert 0 <= w <= 10**9, "0 <= w <= 10^9"
    assert len(profits) == len(capital), "n == profits.length == capital.length"
    assert 1 <= len(profits) <= 10**5, "1 <= n <= 10^5"
    assert all(0 <= p <= 10**4 for p in profits), "0 <= profits[i] <= 10^4"
    assert all(0 <= c <= 10**9 for c in capital), "0 <= capital[i] <= 10^9"
