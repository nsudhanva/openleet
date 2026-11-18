"""Stone Game V: a row of stone values."""


def check(stoneValue: list[int]) -> None:
    assert 1 <= len(stoneValue) <= 500, "1 <= stoneValue.length <= 500"
    assert all(1 <= v <= 10**6 for v in stoneValue), "1 <= stoneValue[i] <= 10^6"
