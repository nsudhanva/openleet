"""Count Unreachable Pairs of Nodes in an Undirected Graph: n nodes and an edge list."""


def check(n: int, edges: list[list[int]]) -> None:
    assert isinstance(edges, list), "edges is a list"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 0 <= len(edges) <= 2 * 10**5, "0 <= edges.length <= 2 * 10^5"
    assert all(isinstance(e, list) and len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= a < n and 0 <= b < n for a, b in edges), "0 <= ai, bi < n"
    assert all(a != b for a, b in edges), "ai != bi"
    assert len({(min(a, b), max(a, b)) for a, b in edges}) == len(edges), (
        "there are no repeated edges"
    )
