"""Minimum Cost to Reach Destination in Time: connected roads, fees, time limit."""


def check(maxTime: int, edges: list[list[int]], passingFees: list[int]) -> None:
    n = len(passingFees)
    assert 1 <= maxTime <= 1000, "1 <= maxTime <= 1000"
    assert 2 <= n <= 1000, "2 <= n <= 1000"
    assert n - 1 <= len(edges) <= 1000, "n - 1 <= edges.length <= 1000"
    assert all(len(e) == 3 for e in edges), "edges[i].length == 3"
    assert all(0 <= e[0] <= n - 1 and 0 <= e[1] <= n - 1 for e in edges), "0 <= xi, yi <= n - 1"
    assert all(1 <= e[2] <= 1000 for e in edges), "1 <= timei <= 1000"
    assert all(1 <= f <= 1000 for f in passingFees), "1 <= passingFees[j] <= 1000"
    assert all(e[0] != e[1] for e in edges), "the graph does not contain self loops"
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for e in edges:
        parent[find(e[0])] = find(e[1])
    assert len({find(i) for i in range(n)}) == 1, "all the cities are connected"
