"""Delete Tree Nodes at 10^4 nodes: a spine of 9500 with short branches near its bottom and
zero-sum subtrees only in its lowest tenth, so summing each node's subtree from scratch, or walking
up from each node to a zero-sum ancestor, costs ~4 * 10^7 steps."""

SEEDS = 2
N = 10**4
SPINE = 9500


def generate(rng):
    parent = [-1] + [i - 1 for i in range(1, SPINE)]
    parent += [rng.randrange(SPINE // 2, i) for i in range(SPINE, N)]
    value = [rng.randint(-(10**5), 10**5) for _ in range(N)]
    children = [[] for _ in range(N)]
    for i in range(1, N):
        children[parent[i]].append(i)
    # Children have larger ids, so going down the ids visits each subtree before its root. Only
    # the bottom of the spine and the branches get zero-sum subtrees, so the long walks survive.
    total = value[:]
    for i in range(N - 1, -1, -1):
        rest = sum(total[j] for j in children[i])
        if i >= SPINE * 9 // 10 and rng.random() < 0.05 and abs(rest) <= 10**5:
            value[i] = -rest
        total[i] = value[i] + rest
    label = [0, *rng.sample(range(1, N), N - 1)]
    out_parent, out_value = [0] * N, [0] * N
    for i in range(N):
        out_parent[label[i]] = -1 if i == 0 else label[parent[i]]
        out_value[label[i]] = value[i]
    return {"nodes": N, "parent": out_parent, "value": out_value}
