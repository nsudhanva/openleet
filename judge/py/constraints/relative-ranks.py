"""Relative Ranks: distinct athlete scores."""


def check(score: list[int]) -> None:
    assert 1 <= len(score) <= 10**4, "1 <= n <= 10^4"
    assert all(0 <= v <= 10**6 for v in score), "0 <= score[i] <= 10^6"
    assert len(set(score)) == len(score), "all the values in score are unique"
