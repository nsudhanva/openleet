"""Maximize the Profit as the Salesman: n houses and offers [start, end, gold]."""


def check(n: int, offers: list[list[int]]) -> None:
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 1 <= len(offers) <= 10**5, "1 <= offers.length <= 10^5"
    assert all(len(o) == 3 for o in offers), "offers[i].length == 3"
    assert all(0 <= s <= e <= n - 1 for s, e, _ in offers), "0 <= starti <= endi <= n - 1"
    assert all(1 <= g <= 10**3 for _, _, g in offers), "1 <= goldi <= 10^3"
