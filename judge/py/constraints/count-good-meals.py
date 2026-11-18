"""Count Good Meals: a list of deliciousness values."""


def check(deliciousness: list[int]) -> None:
    assert 1 <= len(deliciousness) <= 10**5, "1 <= deliciousness.length <= 10^5"
    assert all(0 <= v <= 2**20 for v in deliciousness), "0 <= deliciousness[i] <= 2^20"
