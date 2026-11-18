"""Minimum Time to Complete All Tasks: tasks given as [start, end, duration]."""


def check(tasks: list[list[int]]) -> None:
    assert 1 <= len(tasks) <= 2000, "1 <= tasks.length <= 2000"
    assert all(len(t) == 3 for t in tasks), "tasks[i].length == 3"
    assert all(1 <= s <= 2000 and 1 <= e <= 2000 for s, e, _ in tasks), "1 <= starti, endi <= 2000"
    assert all(1 <= d <= e - s + 1 for s, e, d in tasks), "1 <= durationi <= endi - starti + 1"
