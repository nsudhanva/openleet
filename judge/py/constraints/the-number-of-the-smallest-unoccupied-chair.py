"""The Number of the Smallest Unoccupied Chair: arrival and leaving times per friend."""


def check(times: list[list[int]], targetFriend: int) -> None:
    n = len(times)
    assert 2 <= n <= 10**4, "2 <= n <= 10^4"
    assert all(len(t) == 2 for t in times), "times[i].length == 2"
    assert all(1 <= a < b <= 10**5 for a, b in times), "1 <= arrivali < leavingi <= 10^5"
    assert 0 <= targetFriend <= n - 1, "0 <= targetFriend <= n - 1"
    assert len({t[0] for t in times}) == n, "each arrivali time is distinct"
