"""Minimum Edge Reversals So Every Node Is Reachable at n = 5000: a random tree with shuffled
labels and random edge directions, so a fresh traversal from every node is ~2.5 * 10^7 steps."""

SEEDS = 2
N = 5000


def generate(rng):
    labels = list(range(N))
    rng.shuffle(labels)
    edges = []
    for i in range(1, N):
        u, v = labels[i], labels[rng.randrange(i)]
        edges.append([u, v] if rng.random() < 0.5 else [v, u])
    rng.shuffle(edges)
    return {"n": N, "edges": edges}
