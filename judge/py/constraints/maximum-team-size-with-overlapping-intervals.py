"""Maximum Team Size with Overlapping Intervals: parallel start and end time arrays."""


def check(startTime: list[int], endTime: list[int]) -> None:
    n = len(startTime)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert len(endTime) == n, "n == startTime.length == endTime.length"
    assert all(0 <= s <= e <= 10**9 for s, e in zip(startTime, endTime, strict=True)), (
        "0 <= startTime[i] <= endTime[i] <= 10^9"
    )
