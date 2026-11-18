"""Earliest Finish Time for Land and Water Rides I: start times and durations of rides."""


def check(
    landStartTime: list[int],
    landDuration: list[int],
    waterStartTime: list[int],
    waterDuration: list[int],
) -> None:
    n, m = len(landStartTime), len(waterStartTime)
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert 1 <= m <= 100, "1 <= m <= 100"
    assert len(landDuration) == n, "landStartTime.length == landDuration.length == n"
    assert len(waterDuration) == m, "waterStartTime.length == waterDuration.length == m"
    for name, arr in (
        ("landStartTime", landStartTime),
        ("landDuration", landDuration),
        ("waterStartTime", waterStartTime),
        ("waterDuration", waterDuration),
    ):
        assert all(isinstance(v, int) and 1 <= v <= 1000 for v in arr), f"1 <= {name}[i] <= 1000"
