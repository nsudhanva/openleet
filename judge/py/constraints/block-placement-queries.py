"""Block Placement Queries: obstacle (type 1) and block-fit (type 2) queries on a number line."""


def check(queries: list[list[int]]) -> None:
    assert 1 <= len(queries) <= 15 * 10**4, "1 <= queries.length <= 15 * 10^4"
    assert all(2 <= len(q) <= 3 for q in queries), "2 <= queries[i].length <= 3"
    assert all(1 <= q[0] <= 2 for q in queries), "1 <= queries[i][0] <= 2"
    assert all(len(q) == q[0] + 1 for q in queries), "type 1 is [1, x], type 2 is [2, x, sz]"
    top = min(5 * 10**4, 3 * len(queries))
    assert all(1 <= v <= top for q in queries for v in q[1:]), (
        "1 <= x, sz <= min(5 * 10^4, 3 * queries.length)"
    )
    obstacles = [q[1] for q in queries if q[0] == 1]
    assert len(set(obstacles)) == len(obstacles), (
        "no obstacle exists at distance x when a type 1 query is asked"
    )
    assert any(q[0] == 2 for q in queries), "at least one query of type 2"
