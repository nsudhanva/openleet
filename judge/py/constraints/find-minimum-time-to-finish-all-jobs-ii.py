"""Find Minimum Time to Finish All Jobs II: job durations and worker daily capacities of the
same length."""


def check(jobs: list[int], workers: list[int]) -> None:
    n = len(jobs)
    assert n == len(workers), "n == jobs.length == workers.length"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(1 <= v <= 10**5 for v in jobs), "1 <= jobs[i] <= 10^5"
    assert all(1 <= v <= 10**5 for v in workers), "1 <= workers[i] <= 10^5"
