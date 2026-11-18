"""Maximum Number of Groups With Increasing Length: a list of usage limits."""


def check(usageLimits: list[int]) -> None:
    assert 1 <= len(usageLimits) <= 10**5, "1 <= usageLimits.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in usageLimits), "1 <= usageLimits[i] <= 10^9"
