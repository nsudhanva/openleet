"""Maximum Profit in Job Scheduling: parallel arrays of job start times, end times and profits."""


def check(startTime: list[int], endTime: list[int], profit: list[int]) -> None:
    n = len(startTime)
    assert 1 <= n <= 5 * 10**4, "1 <= startTime.length <= 5 * 10^4"
    assert len(endTime) == n and len(profit) == n, (
        "startTime.length == endTime.length == profit.length"
    )
    assert all(1 <= s < e <= 10**9 for s, e in zip(startTime, endTime, strict=True)), (
        "1 <= startTime[i] < endTime[i] <= 10^9"
    )
    assert all(1 <= p <= 10**4 for p in profit), "1 <= profit[i] <= 10^4"
