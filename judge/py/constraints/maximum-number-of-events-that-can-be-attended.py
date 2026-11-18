"""Maximum Number of Events That Can Be Attended: [startDay, endDay] events."""


def check(events: list[list[int]]) -> None:
    assert 1 <= len(events) <= 10**5, "1 <= events.length <= 10^5"
    assert all(len(e) == 2 for e in events), "events[i].length == 2"
    assert all(1 <= a <= b <= 10**5 for a, b in events), "1 <= startDay_i <= endDay_i <= 10^5"
