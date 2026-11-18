"""Most Beautiful Item for Each Query: [price, beauty] items and price queries."""


def check(items: list[list[int]], queries: list[int]) -> None:
    assert 1 <= len(items) <= 10**5, "1 <= items.length <= 10^5"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(len(it) == 2 for it in items), "items[i].length == 2"
    assert all(1 <= v <= 10**9 for it in items for v in it), "1 <= pricei, beautyi <= 10^9"
    assert all(1 <= q <= 10**9 for q in queries), "1 <= queries[j] <= 10^9"
