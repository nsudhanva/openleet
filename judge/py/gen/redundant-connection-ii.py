"""Redundant Connection II at n = 1000: a rooted tree plus one new directed edge, which either
gives a node two parents, points back into the root (a cycle), or both."""

SEEDS = 3
N = 1000


def generate(rng):
    label = list(range(1, N + 1))
    rng.shuffle(label)
    deep = rng.random() < 0.5
    parent = [-1] * N
    for v in range(1, N):
        parent[v] = rng.randint(max(0, v - 2), v - 1) if deep else rng.randrange(v)
    edges = {(label[parent[v]], label[v]) for v in range(1, N)}
    kind = rng.choice(["root", "two_parents"])
    while True:
        if kind == "root":
            u, v = label[rng.randrange(1, N)], label[0]
        else:
            u, v = label[rng.randrange(N)], label[rng.randrange(1, N)]
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
            break
    out = [list(e) for e in sorted(edges)]
    rng.shuffle(out)
    return {"edges": out}
