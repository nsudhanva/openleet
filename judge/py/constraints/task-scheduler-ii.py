"""Task Scheduler II: task types in order and a required spacing."""


def check(tasks: list[int], space: int) -> None:
    assert 1 <= len(tasks) <= 10**5, "1 <= tasks.length <= 10^5"
    assert all(1 <= t <= 10**9 for t in tasks), "1 <= tasks[i] <= 10^9"
    assert 1 <= space <= len(tasks), "1 <= space <= tasks.length"
