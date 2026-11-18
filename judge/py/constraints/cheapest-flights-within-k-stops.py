"""Cheapest Flights Within K Stops: n cities, [from, to, price] flights, src, dst, k."""


def check(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> None:
    assert 2 <= n <= 100, "2 <= n <= 100"
    assert isinstance(flights, list), "flights is a list"
    assert 0 <= len(flights) <= n * (n - 1) // 2, "0 <= flights.length <= n * (n - 1) / 2"
    assert all(isinstance(f, list) and len(f) == 3 for f in flights), "flights[i].length == 3"
    assert all(0 <= a < n and 0 <= b < n for a, b, _ in flights), "0 <= from, to < n"
    assert all(a != b for a, b, _ in flights), "from != to"
    assert all(1 <= p <= 10**4 for _, _, p in flights), "1 <= price <= 10^4"
    assert len({(a, b) for a, b, _ in flights}) == len(flights), (
        "no multiple flights between two cities"
    )
    assert 0 <= src < n and 0 <= dst < n and 0 <= k < n, "0 <= src, dst, k < n"
    assert src != dst, "src != dst"
