"""Time Taken to Cross the Door: sorted arrival times and enter(0)/exit(1) states."""


def check(arrival: list[int], state: list[int]) -> None:
    n = len(arrival)
    assert len(state) == n, "n == arrival.length == state.length"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(0 <= a <= n for a in arrival), "0 <= arrival[i] <= n"
    assert all(arrival[i] <= arrival[i + 1] for i in range(n - 1)), (
        "arrival is sorted in non-decreasing order"
    )
    assert all(s in (0, 1) for s in state), "state[i] is either 0 or 1"
