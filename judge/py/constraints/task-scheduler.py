"""Task Scheduler: uppercase letter tasks and a cooldown n."""


def check(tasks: list[str], n: int) -> None:
    assert 1 <= len(tasks) <= 10**4, "1 <= tasks.length <= 10^4"
    assert all(isinstance(t, str) and len(t) == 1 and "A" <= t <= "Z" for t in tasks), (
        "tasks[i] is an uppercase English letter"
    )
    assert 0 <= n <= 100, "0 <= n <= 100"
