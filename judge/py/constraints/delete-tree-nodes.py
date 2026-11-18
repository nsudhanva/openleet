"""Delete Tree Nodes: a tree rooted at 0 given by parent indexes and node values."""


def check(nodes: int, parent: list[int], value: list[int]) -> None:
    assert 1 <= nodes <= 10**4, "1 <= nodes <= 10^4"
    assert len(parent) == nodes, "parent.length == nodes"
    assert len(value) == nodes, "value.length == nodes"
    assert parent[0] == -1, "parent[0] == -1"
    assert all(0 <= p <= nodes - 1 for p in parent[1:]), "0 <= parent[i] <= nodes - 1"
    assert all(-(10**5) <= v <= 10**5 for v in value), "-10^5 <= value[i] <= 10^5"
    state = [0] * nodes  # 0 unseen, 1 on current walk, 2 reaches the root
    state[0] = 2
    for start in range(1, nodes):
        walk = []
        cur = start
        while state[cur] == 0:
            state[cur] = 1
            walk.append(cur)
            cur = parent[cur]
        assert state[cur] == 2, "the given input represents a valid tree"
        for w in walk:
            state[w] = 2
