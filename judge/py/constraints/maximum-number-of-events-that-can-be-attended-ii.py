"""Maximum Number of Events That Can Be Attended II: [start, end, value] events and k."""


def check(events: list[list[int]], k: int) -> None:
    assert 1 <= k <= len(events), "1 <= k <= events.length"
    assert 1 <= k * len(events) <= 10**6, "1 <= k * events.length <= 10^6"
    assert all(len(e) == 3 for e in events), "events[i].length == 3"
    assert all(1 <= a <= b <= 10**9 for a, b, _ in events), "1 <= startDay_i <= endDay_i <= 10^9"
    assert all(1 <= v <= 10**6 for _, _, v in events), "1 <= value_i <= 10^6"
