"""Minimum Number of Work Sessions to Finish the Tasks: task durations and a session length."""


def check(tasks: list[int], sessionTime: int) -> None:
    assert isinstance(tasks, list) and tasks, "tasks is a non-empty list"
    assert 1 <= len(tasks) <= 14, "1 <= n <= 14"
    assert all(1 <= t <= 10 for t in tasks), "1 <= tasks[i] <= 10"
    assert max(tasks) <= sessionTime <= 15, "max(tasks[i]) <= sessionTime <= 15"
