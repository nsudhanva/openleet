"""Minimize the Maximum Waiting Time at Synchronized Traffic Lights: period, lights, arrivals."""


def check(period: int, lights: list[int], arrivalTime: list[int]) -> None:
    assert 2 <= period <= 10**9, "2 <= period <= 10^9"
    assert 1 <= len(lights) <= 10**4, "1 <= lights.length <= 10^4"
    assert all(1 <= v <= period - 1 for v in lights), "1 <= lights[i] <= period - 1"
    assert 1 <= len(arrivalTime) <= 10**5, "1 <= arrivalTime.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in arrivalTime), "1 <= arrivalTime[i] <= 10^9"
