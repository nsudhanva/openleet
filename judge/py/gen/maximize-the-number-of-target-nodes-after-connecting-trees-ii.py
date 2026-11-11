"""Maximize the Number of Target Nodes After Connecting Trees II with two 3 * 10^4-node trees, each
a long path with random branches, so a BFS from every node is ~10^9 steps per tree and walking
each node up to the root ~2 * 10^8."""

SEEDS = 2
N = 3 * 10**4


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
