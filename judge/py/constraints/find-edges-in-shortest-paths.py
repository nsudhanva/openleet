"""Find Edges in Shortest Paths: an undirected weighted graph, edges [a, b, w]."""


def check(n: int, edges: list[list[int]]) -> None:
    assert 2 <= n <= 5 * 10**4, "2 <= n <= 5 * 10^4"
    assert 1 <= len(edges) <= min(5 * 10**4, n * (n - 1) // 2), (
        "1 <= m <= min(5 * 10^4, n * (n - 1) / 2)"
    )
    assert all(len(e) == 3 for e in edges), "edges[i] = [ai, bi, wi]"
    assert all(0 <= a < n and 0 <= b < n for a, b, _ in edges), "0 <= ai, bi < n"
    assert all(a != b for a, b, _ in edges), "ai != bi"
    assert all(1 <= w <= 10**5 for _, _, w in edges), "1 <= wi <= 10^5"
    assert len({(min(a, b), max(a, b)) for a, b, _ in edges}) == len(edges), (
        "there are no repeated edges"
    )
