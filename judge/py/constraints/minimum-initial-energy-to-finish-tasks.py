"""Minimum Initial Energy to Finish Tasks: a list of [actual, minimum] pairs."""


def check(tasks: list[list[int]]) -> None:
    assert 1 <= len(tasks) <= 10**5, "1 <= tasks.length <= 10^5"
    assert all(len(t) == 2 for t in tasks), "tasks[i].length == 2"
    assert all(1 <= a <= m <= 10**4 for a, m in tasks), "1 <= actual_i <= minimum_i <= 10^4"
