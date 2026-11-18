"""Optimize Water Distribution in a Village: n houses, well costs and pipes [a, b, cost]."""


def check(n: int, wells: list[int], pipes: list[list[int]]) -> None:
    assert isinstance(wells, list) and isinstance(pipes, list), "wells and pipes are lists"
    assert 2 <= n <= 10**4, "2 <= n <= 10^4"
    assert len(wells) == n, "wells.length == n"
    assert all(0 <= w <= 10**5 for w in wells), "0 <= wells[i] <= 10^5"
    assert 1 <= len(pipes) <= 10**4, "1 <= pipes.length <= 10^4"
    assert all(len(p) == 3 for p in pipes), "pipes[j].length == 3"
    assert all(1 <= p[0] <= n and 1 <= p[1] <= n for p in pipes), "1 <= house1j, house2j <= n"
    assert all(0 <= p[2] <= 10**5 for p in pipes), "0 <= costj <= 10^5"
    assert all(p[0] != p[1] for p in pipes), "house1j != house2j"
