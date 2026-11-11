"""Maximize Spanning Tree Stability with Upgrades at n = 3000 and 6000 edges: a random spanning tree
of strong edges (a few of them must edges) plus random extras, and one leaf hangs by a
mid-strength edge, so the answer sits mid-range and trying candidate stabilities one by one,
from either end, is >= 10^3 checks of O(m) each against the binary search's ~20."""

SEEDS = 2
N = 3000
EXTRA = 3000
TOP = 10**5


def generate(rng):
    edges, seen = [], set()

    def add(u, v, s, must):
        seen.add((min(u, v), max(u, v)))
        edges.append([u, v, s, must])

    order = list(range(N - 1))
    rng.shuffle(order)
    for i in range(1, N - 1):
        u, v = order[i], order[rng.randrange(i)]
        if rng.random() < 0.05:
            add(u, v, rng.randint(TOP * 9 // 10, TOP), 1)
        else:
            add(u, v, rng.randint(TOP // 2, TOP), 0)
    leaf = N - 1
    add(leaf, order[rng.randrange(N - 1)], rng.randint(TOP // 4, TOP // 2), 0)
    while len(edges) < N - 1 + EXTRA:
        u, v = rng.sample(range(N - 1), 2)
        if (min(u, v), max(u, v)) not in seen:
            add(u, v, rng.randint(1, TOP), 0)
    rng.shuffle(edges)
    return {"n": N, "edges": edges, "k": rng.randint(0, N // 50)}
