"""Maximum Earnings From Taxi: n points and rides [start, end, tip]."""


def check(n: int, rides: list[list[int]]) -> None:
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 1 <= len(rides) <= 3 * 10**4, "1 <= rides.length <= 3 * 10^4"
    assert all(len(r) == 3 for r in rides), "rides[i].length == 3"
    assert all(1 <= s < e <= n for s, e, _ in rides), "1 <= starti < endi <= n"
    assert all(1 <= t <= 10**5 for _, _, t in rides), "1 <= tipi <= 10^5"
