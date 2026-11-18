"""Process Tasks Using Servers: server weights and task durations."""


def check(servers: list[int], tasks: list[int]) -> None:
    assert isinstance(servers, list) and isinstance(tasks, list), "servers and tasks are arrays"
    assert 1 <= len(servers) <= 2 * 10**5, "1 <= n <= 2 * 10^5"
    assert 1 <= len(tasks) <= 2 * 10**5, "1 <= m <= 2 * 10^5"
    assert all(1 <= v <= 2 * 10**5 for v in servers), "1 <= servers[i] <= 2 * 10^5"
    assert all(1 <= v <= 2 * 10**5 for v in tasks), "1 <= tasks[j] <= 2 * 10^5"
