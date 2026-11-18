"""Minimum Processing Time: processor availability times and tasks, four tasks per processor."""


def check(processorTime: list[int], tasks: list[int]) -> None:
    n = len(processorTime)
    assert 1 <= n <= 25000, "1 <= n == processorTime.length <= 25000"
    assert 1 <= len(tasks) <= 10**5, "1 <= tasks.length <= 10^5"
    assert all(0 <= v <= 10**9 for v in processorTime), "0 <= processorTime[i] <= 10^9"
    assert all(1 <= v <= 10**9 for v in tasks), "1 <= tasks[i] <= 10^9"
    assert len(tasks) == 4 * n, "tasks.length == 4 * n"
