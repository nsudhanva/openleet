"""Number of Good Paths on a 3 * 10^4-node tree: a long path or random tree with values from a
tiny set (huge answers, many equal-value pairs) or all equal, so per-pair path checks are
quadratic."""

SEEDS = 3
N = 3 * 10**4


def generate(rng):
    labels = list(range(N))
    rng.shuffle(labels)
    path = rng.random() < 0.5
    edges = []
    for i in range(1, N):
        parent = i - 1 if path else rng.randrange(max(0, i - 50), i)
        a, b = labels[i], labels[parent]
        edges.append([a, b] if rng.random() < 0.5 else [b, a])
    rng.shuffle(edges)
    top = rng.choice((0, 3, 10**5))
    return {"vals": [rng.randint(0, top) for _ in range(N)], "edges": edges}
