"""Minimum Number of Seconds to Make Mountain Height Zero: a mountain height and worker
times."""


def check(mountainHeight: int, workerTimes: list[int]) -> None:
    assert isinstance(mountainHeight, int) and 1 <= mountainHeight <= 10**5, (
        "1 <= mountainHeight <= 10^5"
    )
    assert isinstance(workerTimes, list), "workerTimes is an array"
    assert 1 <= len(workerTimes) <= 10**4, "1 <= workerTimes.length <= 10^4"
    assert all(isinstance(v, int) and 1 <= v <= 10**6 for v in workerTimes), (
        "1 <= workerTimes[i] <= 10^6"
    )
