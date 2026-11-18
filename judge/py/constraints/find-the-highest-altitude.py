"""Find the Highest Altitude: net altitude gains between consecutive points."""


def check(gain: list[int]) -> None:
    assert isinstance(gain, list), "gain is an array"
    assert 1 <= len(gain) <= 100, "1 <= n == gain.length <= 100"
    assert all(-100 <= v <= 100 for v in gain), "-100 <= gain[i] <= 100"
