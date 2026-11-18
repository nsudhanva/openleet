"""Maximum Path Quality of a Graph: node values, weighted undirected edges, a time limit."""


def check(values: list[int], edges: list[list[int]], maxTime: int) -> None:
    n = len(values)
    assert 1 <= n <= 1000, "1 <= n <= 1000"
    assert all(0 <= v <= 10**8 for v in values), "0 <= values[i] <= 10^8"
    assert 0 <= len(edges) <= 2000, "0 <= edges.length <= 2000"
    assert all(len(e) == 3 for e in edges), "edges[j].length == 3"
    assert all(0 <= u < v <= n - 1 for u, v, _ in edges), "0 <= uj < vj <= n - 1"
    assert all(10 <= t <= 100 for _, _, t in edges), "10 <= timej <= 100"
    assert 10 <= maxTime <= 100, "10 <= maxTime <= 100"
    assert len({(u, v) for u, v, _ in edges}) == len(edges), "All the pairs [uj, vj] are unique"
    degree = [0] * n
    for u, v, _ in edges:
        degree[u] += 1
        degree[v] += 1
    assert max(degree) <= 4, "There are at most four edges connected to each node"
