"""Profitable Schemes: group sizes and profits of crimes, plus member and profit targets."""


def check(n: int, minProfit: int, group: list[int], profit: list[int]) -> None:
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert 0 <= minProfit <= 100, "0 <= minProfit <= 100"
    assert 1 <= len(group) <= 100, "1 <= group.length <= 100"
    assert all(1 <= g <= 100 for g in group), "1 <= group[i] <= 100"
    assert len(profit) == len(group), "profit.length == group.length"
    assert all(0 <= p <= 100 for p in profit), "0 <= profit[i] <= 100"
