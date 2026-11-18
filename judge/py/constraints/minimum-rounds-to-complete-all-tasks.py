"""Minimum Rounds to Complete All Tasks: an array of task difficulties."""


def check(tasks: list[int]) -> None:
    assert 1 <= len(tasks) <= 10**5, "1 <= tasks.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in tasks), "1 <= tasks[i] <= 10^9"
