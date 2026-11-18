"""Minimum Cost to Reach City with Discounts: n cities, toll highways and a discount count."""


def check(n: int, highways: list[list[int]], discounts: int) -> None:
    assert 2 <= n <= 1000, "2 <= n <= 1000"
    assert 1 <= len(highways) <= 1000, "1 <= highways.length <= 1000"
    assert all(len(h) == 3 for h in highways), "highways[i].length == 3"
    assert all(0 <= h[0] <= n - 1 and 0 <= h[1] <= n - 1 for h in highways), (
        "0 <= city1i, city2i <= n - 1"
    )
    assert all(h[0] != h[1] for h in highways), "city1i != city2i"
    assert all(0 <= h[2] <= 10**5 for h in highways), "0 <= tolli <= 10^5"
    assert 0 <= discounts <= 500, "0 <= discounts <= 500"
    pairs = {frozenset((h[0], h[1])) for h in highways}
    assert len(pairs) == len(highways), "there are no duplicate highways"
