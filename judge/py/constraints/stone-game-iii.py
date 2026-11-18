"""Stone Game III: a row of stone values."""


def check(stoneValue: list[int]) -> None:
    assert 1 <= len(stoneValue) <= 5 * 10**4, "1 <= stoneValue.length <= 5 * 10^4"
    assert all(-1000 <= v <= 1000 for v in stoneValue), "-1000 <= stoneValue[i] <= 1000"
