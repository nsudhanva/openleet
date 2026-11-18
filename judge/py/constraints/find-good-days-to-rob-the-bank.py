"""Find Good Days to Rob the Bank: security levels per day and a window size."""


def check(security: list[int], time: int) -> None:
    assert 1 <= len(security) <= 10**5, "1 <= security.length <= 10^5"
    assert all(0 <= v <= 10**5 for v in security), "0 <= security[i] <= 10^5"
    assert 0 <= time <= 10**5, "0 <= time <= 10^5"
