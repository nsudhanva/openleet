"""Network Delay Time: directed weighted edges [u, v, w], node count n and source k."""


def check(times: list[list[int]], n: int, k: int) -> None:
    assert 1 <= k <= n <= 100, "1 <= k <= n <= 100"
    assert 1 <= len(times) <= 6000, "1 <= times.length <= 6000"
    assert all(len(t) == 3 for t in times), "times[i].length == 3"
    assert all(1 <= u <= n and 1 <= v <= n for u, v, _ in times), "1 <= ui, vi <= n"
    assert all(u != v for u, v, _ in times), "ui != vi"
    assert all(0 <= w <= 100 for _, _, w in times), "0 <= wi <= 100"
    assert len({(u, v) for u, v, _ in times}) == len(times), "all the pairs (ui, vi) are unique"
