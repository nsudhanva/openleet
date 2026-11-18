"""Minimum Difficulty of a Job Schedule: job difficulties and a number of days."""


def check(jobDifficulty: list[int], d: int) -> None:
    assert 1 <= len(jobDifficulty) <= 300, "1 <= jobDifficulty.length <= 300"
    assert all(0 <= x <= 1000 for x in jobDifficulty), "0 <= jobDifficulty[i] <= 1000"
    assert 1 <= d <= 10, "1 <= d <= 10"
