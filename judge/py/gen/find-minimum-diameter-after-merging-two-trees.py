"""Minimum Diameter After Merging Two Trees with two 5000-node trees, each a long path with
random branches, so a BFS from every node is ~2.5 * 10^7 steps per tree."""

SEEDS = 2
N = 5000


def tree(rng, n):
    labels = list(range(n))
    rng.shuffle(labels)
    spine = rng.randint(n // 3, n * 2 // 3)
    edges = []
    for i in range(1, n):
        parent = i - 1 if i < spine else rng.randrange(i)
        a, b = labels[i], labels[parent]
        edges.append([a, b] if rng.random() < 0.5 else [b, a])
    rng.shuffle(edges)
    return edges


def generate(rng):
    return {"edges1": tree(rng, N), "edges2": tree(rng, N - rng.randrange(N // 50 + 1))}
