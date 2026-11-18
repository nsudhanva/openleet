"""Find Minimum Time to Finish All Jobs: job durations and a worker count k."""


def check(jobs: list[int], k: int) -> None:
    assert 1 <= len(jobs) <= 12, "k <= jobs.length <= 12"
    assert 1 <= k <= len(jobs), "1 <= k <= jobs.length"
    assert all(1 <= v <= 10**7 for v in jobs), "1 <= jobs[i] <= 10^7"
