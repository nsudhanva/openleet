"""Minimum Edge Reversals So Every Node Is Reachable at n = 10^5 with randomly directed edges
over shuffled labels: a random tree, a bare path and a path with short side branches, so a
traversal from every node is ~10^10 steps and walking each node's path to the root is ~10^9 to
5 * 10^9."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5


def generate(rng):
    shape = pick_shape(rng)
    labels = list(range(N))
    rng.shuffle(labels)
    edges = []
    for i in range(1, N):
        if shape == 0:
            parent = rng.randrange(i)
        elif shape == 1:
            parent = i - 1
        else:
            parent = i - 1 if i % 4 else rng.randrange(max(0, i - 8), i)
        u, v = labels[i], labels[parent]
        edges.append([u, v] if rng.random() < 0.5 else [v, u])
    rng.shuffle(edges)
    return {"n": N, "edges": edges}
