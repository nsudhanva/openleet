"""Shopping Offers: item prices, special bundles (counts then price) and needed counts."""


def check(price: list[int], special: list[list[int]], needs: list[int]) -> None:
    n = len(price)
    assert 1 <= n <= 6, "1 <= n <= 6"
    assert len(needs) == n, "n == price.length == needs.length"
    assert all(0 <= p <= 10 for p in price), "0 <= price[i] <= 10"
    assert all(0 <= x <= 10 for x in needs), "0 <= needs[i] <= 10"
    assert 1 <= len(special) <= 100, "1 <= special.length <= 100"
    assert all(len(sp) == n + 1 for sp in special), "special[i].length == n + 1"
    assert all(0 <= x <= 50 for sp in special for x in sp), "0 <= special[i][j] <= 50"
    assert all(any(sp[:n]) for sp in special), (
        "at least one of special[i][j] is non-zero for 0 <= j <= n - 1"
    )
