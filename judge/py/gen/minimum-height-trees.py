"""Minimum Height Trees at n = 2 * 10^4: a long path (BFS from every node is n^2), a random
tree, or a caterpillar."""

SEEDS = 3
N = 2 * 10**4


def generate(rng):
    kind = rng.choice(("path", "random", "caterpillar"))
    labels = list(range(N))
    rng.shuffle(labels)
    edges = []
    for i in range(1, N):
        if kind == "path":
            parent = i - 1
        elif kind == "random":
            parent = rng.randrange(i)
        else:
            parent = i - 1 if i < N // 2 else rng.randrange(N // 2)
        a, b = labels[i], labels[parent]
        edges.append([a, b] if rng.random() < 0.5 else [b, a])
    rng.shuffle(edges)
    return {"n": N, "edges": edges}
