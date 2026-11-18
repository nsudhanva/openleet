"""Shortest Distance After Road Addition Queries II: n cities and a list of [u, v] roads to add."""


def check(n: int, queries: list[list[int]]) -> None:
    assert 3 <= n <= 10**5, "3 <= n <= 10^5"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(0 <= u < v < n for u, v in queries), "0 <= queries[i][0] < queries[i][1] < n"
    assert all(v - u > 1 for u, v in queries), "1 < queries[i][1] - queries[i][0]"
    assert len({(u, v) for u, v in queries}) == len(queries), (
        "There are no repeated roads among the queries"
    )
    stack: list[tuple[int, int]] = []
    for u, v in sorted(((u, v) for u, v in queries), key=lambda q: (q[0], -q[1])):
        while stack and stack[-1][1] <= u:
            stack.pop()
        assert not (stack and stack[-1][0] < u < stack[-1][1] < v), (
            "no two queries with queries[i][0] < queries[j][0] < queries[i][1] < queries[j][1]"
        )
        stack.append((u, v))
