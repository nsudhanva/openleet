"""Find Original Array From Doubled Array: a list of non-negative integers."""


def check(changed: list[int]) -> None:
    assert 1 <= len(changed) <= 10**5, "1 <= changed.length <= 10^5"
    assert all(0 <= v <= 10**5 for v in changed), "0 <= changed[i] <= 10^5"
