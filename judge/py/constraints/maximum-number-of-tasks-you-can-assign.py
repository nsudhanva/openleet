"""Maximum Number of Tasks You Can Assign: task and worker strengths, pills and pill strength."""


def check(tasks: list[int], workers: list[int], pills: int, strength: int) -> None:
    assert 1 <= len(tasks) <= 5 * 10**4, "1 <= n <= 5 * 10^4"
    assert 1 <= len(workers) <= 5 * 10**4, "1 <= m <= 5 * 10^4"
    assert 0 <= pills <= len(workers), "0 <= pills <= m"
    assert all(0 <= v <= 10**9 for v in tasks), "0 <= tasks[i] <= 10^9"
    assert all(0 <= v <= 10**9 for v in workers), "0 <= workers[j] <= 10^9"
    assert 0 <= strength <= 10**9, "0 <= strength <= 10^9"
