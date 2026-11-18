"""Two Best Non-Overlapping Events: events as [startTime, endTime, value]."""


def check(events: list[list[int]]) -> None:
    assert 2 <= len(events) <= 10**5, "2 <= events.length <= 10^5"
    assert all(len(e) == 3 for e in events), "events[i].length == 3"
    assert all(1 <= s <= e <= 10**9 for s, e, _ in events), "1 <= startTime <= endTime <= 10^9"
    assert all(1 <= v <= 10**6 for _, _, v in events), "1 <= value <= 10^6"
