"""Maximize Sum of Weights after Edge Removals at n = 4 * 10^4: a hub holding 90% of the nodes, the
rest attached at random, and k in [0.4n, 0.5n], so picking the hub's k best gains one at a time, or
a knapsack over its children, is >= 5 * 10^8 steps against sorting them."""

SEEDS = 2
N = 4 * 10**4
TOP = 10**6


def generate(rng):
    labels = list(range(N))
    rng.shuffle(labels)
    edges = []
    for i in range(1, N):
        parent = 0 if rng.random() < 0.9 else rng.randrange(i)
        u, v = labels[i], labels[parent]
        if rng.random() < 0.5:
            u, v = v, u
        edges.append([u, v, rng.randint(1, TOP)])
    rng.shuffle(edges)
    return {"edges": edges, "k": rng.randint(N * 2 // 5, N // 2)}
