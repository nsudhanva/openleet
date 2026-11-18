"""Reschedule Meetings for Maximum Free Time II: an event length and sorted meetings."""


def check(eventTime: int, startTime: list[int], endTime: list[int]) -> None:
    n = len(startTime)
    assert 1 <= eventTime <= 10**9, "1 <= eventTime <= 10^9"
    assert n == len(endTime), "n == startTime.length == endTime.length"
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert all(0 <= s < e <= eventTime for s, e in zip(startTime, endTime, strict=True)), (
        "0 <= startTime[i] < endTime[i] <= eventTime"
    )
    assert all(endTime[i] <= startTime[i + 1] for i in range(n - 1)), (
        "endTime[i] <= startTime[i + 1]"
    )
