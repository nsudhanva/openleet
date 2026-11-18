"""Queries on Number of Points Inside a Circle: integer points and circle queries."""


def check(points: list[list[int]], queries: list[list[int]]) -> None:
    assert isinstance(points, list) and isinstance(queries, list), "points and queries are arrays"
    assert 1 <= len(points) <= 500, "1 <= points.length <= 500"
    assert all(isinstance(p, list) and len(p) == 2 for p in points), "points[i].length == 2"
    assert all(isinstance(v, int) and 0 <= v <= 500 for p in points for v in p), (
        "0 <= xi, yi <= 500"
    )
    assert 1 <= len(queries) <= 500, "1 <= queries.length <= 500"
    assert all(isinstance(q, list) and len(q) == 3 for q in queries), "queries[j].length == 3"
    assert all(isinstance(v, int) for q in queries for v in q), "all coordinates are integers"
    assert all(0 <= x <= 500 and 0 <= y <= 500 for x, y, _ in queries), "0 <= xj, yj <= 500"
    assert all(1 <= r <= 500 for _, _, r in queries), "1 <= rj <= 500"
