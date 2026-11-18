"""The Earliest Moment When Everyone Become Friends: friendship logs and n people."""


def check(logs: list[list[int]], n: int) -> None:
    assert 2 <= n <= 100, "2 <= n <= 100"
    assert 1 <= len(logs) <= 10**4, "1 <= logs.length <= 10^4"
    assert all(len(log) == 3 for log in logs), "logs[i].length == 3"
    assert all(0 <= t <= 10**9 for t, _, _ in logs), "0 <= timestampi <= 10^9"
    assert all(0 <= x <= n - 1 and 0 <= y <= n - 1 for _, x, y in logs), "0 <= xi, yi <= n - 1"
    assert all(x != y for _, x, y in logs), "xi != yi"
    assert len({log[0] for log in logs}) == len(logs), "all the values timestampi are unique"
    pairs = [(x, y) for _, x, y in logs]
    assert len(set(pairs)) == len(pairs), "all the pairs (xi, yi) occur at most one time"
