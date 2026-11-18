"""Faulty Sensor: two equal-length lists of sensor readings."""


def check(sensor1: list[int], sensor2: list[int]) -> None:
    assert len(sensor1) == len(sensor2), "sensor1.length == sensor2.length"
    assert 1 <= len(sensor1) <= 100, "1 <= sensor1.length <= 100"
    assert all(1 <= x <= 100 for x in sensor1), "1 <= sensor1[i] <= 100"
    assert all(1 <= x <= 100 for x in sensor2), "1 <= sensor2[i] <= 100"
    assert sensor1 == sensor2 or _dropped(sensor1, sensor2) or _dropped(sensor2, sensor1), (
        "at most one sensor has a defect"
    )


def _dropped(bad: list[int], good: list[int]) -> bool:
    """True if `bad` is `good` with one point dropped, shifted left, and a different last value."""
    n = len(good)
    return any(
        bad[:k] == good[:k] and bad[k : n - 1] == good[k + 1 :] and bad[n - 1] != good[k]
        for k in range(n)
    )
