"""Maximum Ice Cream Bars: bar costs and a coin budget."""


def check(costs: list[int], coins: int) -> None:
    assert 1 <= len(costs) <= 10**5, "1 <= n <= 10^5"
    assert all(1 <= c <= 10**5 for c in costs), "1 <= costs[i] <= 10^5"
    assert 1 <= coins <= 10**8, "1 <= coins <= 10^8"
