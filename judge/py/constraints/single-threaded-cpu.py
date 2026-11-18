"""Single-Threaded CPU: tasks as [enqueueTime, processingTime] pairs."""


def check(tasks: list[list[int]]) -> None:
    assert 1 <= len(tasks) <= 10**5, "1 <= tasks.length <= 10^5"
    assert all(len(t) == 2 for t in tasks), "tasks[i] = [enqueueTime, processingTime]"
    assert all(1 <= a <= 10**9 and 1 <= b <= 10**9 for a, b in tasks), (
        "1 <= enqueueTime, processingTime <= 10^9"
    )
