"""Count of Unfinished Tasks After Each Shift: task sizes and shift sizes."""


def check(tasks: list[int], shifts: list[int]) -> None:
    assert isinstance(tasks, list) and isinstance(shifts, list), "arrays"
    assert 1 <= len(tasks) <= 10**5, "1 <= tasks.length <= 10^5"
    assert 1 <= len(shifts) <= 10**5, "1 <= shifts.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in tasks), "1 <= tasks[i] <= 10^9"
    assert all(1 <= v <= 10**9 for v in shifts), "1 <= shifts[i] <= 10^9"
