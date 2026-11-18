"""Time to Cross a Bridge: n boxes, k workers with four timings each."""


def check(n: int, k: int, time: list[list[int]]) -> None:
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert 1 <= k <= 10**4, "1 <= k <= 10^4"
    assert len(time) == k, "time.length == k"
    assert all(len(t) == 4 for t in time), "time[i].length == 4"
    assert all(1 <= x <= 1000 for t in time for x in t), "1 <= lefti, picki, righti, puti <= 1000"
