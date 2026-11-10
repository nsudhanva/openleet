"""Sum of Distances in Tree at n = 3 * 10^4: a path (deep recursion, worst for per-node BFS)
or a random tree, with shuffled labels and edge orientation."""

from _shapes import pick_shape

SEEDS = 3
N = 3 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    labels = list(range(N))
    rng.shuffle(labels)
    edges = []
    for v in range(1, N):
        if shape == 0:
            parent = v - 1
        elif shape == 1:
            parent = rng.randrange(v)
        else:
            parent = rng.randrange(max(0, v - 3), v)  # long and thin
        a, b = labels[parent], labels[v]
        edges.append([a, b] if rng.random() < 0.5 else [b, a])
    rng.shuffle(edges)
    return {"n": N, "edges": edges}
