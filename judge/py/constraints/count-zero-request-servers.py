"""Count Zero Request Servers: n servers, request logs [server, time], x and query times."""


def check(n: int, logs: list[list[int]], x: int, queries: list[int]) -> None:
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 1 <= len(logs) <= 10**5, "1 <= logs.length <= 10^5"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(len(log) == 2 for log in logs), "logs[i].length == 2"
    assert all(1 <= s <= n for s, _ in logs), "1 <= logs[i][0] <= n"
    assert all(1 <= t <= 10**6 for _, t in logs), "1 <= logs[i][1] <= 10^6"
    assert 1 <= x <= 10**5, "1 <= x <= 10^5"
    assert all(x < q <= 10**6 for q in queries), "x < queries[i] <= 10^6"
