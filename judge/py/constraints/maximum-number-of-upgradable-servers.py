"""Maximum Number of Upgradable Servers: per data center counts, upgrade costs, sell prices and
money."""


def check(count: list[int], upgrade: list[int], sell: list[int], money: list[int]) -> None:
    n = len(count)
    assert 1 <= n <= 10**5, "1 <= count.length <= 10^5"
    assert len(upgrade) == len(sell) == len(money) == n, "all four arrays have the same length"
    for name, arr in (("count", count), ("upgrade", upgrade), ("sell", sell), ("money", money)):
        assert all(1 <= v <= 10**5 for v in arr), f"1 <= {name}[i] <= 10^5"
