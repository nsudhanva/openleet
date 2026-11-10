"""Find Root of a Colored Tree with n = 10^5: a binary tree of max degree three whose levels
follow the color cycle from one hidden root (deep or bushy), relabelled at random, or the same
with one node recolored."""

SEEDS = 3
N = 10**5
CYCLE = "RBW"


def generate(rng):
    deep = rng.random() < 0.4
    children = [0] * N
    parent = [-1] * N
    depth = [0] * N
    free = [0, 0]
    for i in range(1, N):
        if deep:
            j = len(free) - 1 - rng.randrange(min(2, len(free)))
        else:
            j = rng.randrange(len(free))
            free[j], free[-1] = free[-1], free[j]
            j = len(free) - 1
        p = free.pop(j)
        parent[i] = p
        depth[i] = depth[p] + 1
        children[p] += 1
        free.append(i)
        free.append(i)
    label = list(range(N))
    rng.shuffle(label)
    offset = rng.randrange(3)
    colors = [""] * N
    for i in range(N):
        colors[label[i]] = CYCLE[(depth[i] + offset) % 3]
    if rng.random() < 0.34:
        v = rng.randrange(N)
        colors[v] = CYCLE[(CYCLE.index(colors[v]) + 1) % 3]
    edges = [[label[parent[i]], label[i]] for i in range(1, N)]
    rng.shuffle(edges)
    for e in edges:
        if rng.random() < 0.5:
            e.reverse()
    return {"edges": edges, "colors": "".join(colors)}
