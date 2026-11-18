"""Minimized Maximum of Products Distributed to Any Store: n stores and product quantities."""


def check(n: int, quantities: list[int]) -> None:
    m = len(quantities)
    assert 1 <= m <= n <= 10**5, "1 <= m <= n <= 10^5"
    assert all(1 <= v <= 10**5 for v in quantities), "1 <= quantities[i] <= 10^5"
