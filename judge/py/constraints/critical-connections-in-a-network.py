"""Critical Connections in a Network: n servers and distinct connections, all reachable."""


def check(n: int, connections: list[list[int]]) -> None:
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert n - 1 <= len(connections) <= 10**5, "n - 1 <= connections.length <= 10^5"
    assert all(len(c) == 2 for c in connections), "connections[i].length == 2"
    assert all(0 <= v <= n - 1 for c in connections for v in c), "0 <= ai, bi <= n - 1"
    assert all(a != b for a, b in connections), "ai != bi"
    assert len({frozenset(c) for c in connections}) == len(connections), (
        "there are no repeated connections"
    )
    parent = list(range(n))

    def find(v: int) -> int:
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for a, b in connections:
        parent[find(a)] = find(b)
    assert len({find(v) for v in range(n)}) == 1, "any server can reach every other server"
