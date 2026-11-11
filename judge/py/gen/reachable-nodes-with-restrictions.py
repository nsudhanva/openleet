"""Reachable Nodes With Restrictions at n = 4 * 10^4 with a half or two thirds of the nodes
restricted leaves, so a restricted list scanned per neighbour costs ~10^9 comparisons."""

SEEDS = 2
N = 4 * 10**4


def generate(rng):
    free = N // rng.choice((2, 3))
    # Nodes below `free` form a random tree around 0; the rest hang off it and are restricted.
    parent = [rng.randrange(v) for v in range(1, free)]
    parent += [rng.randrange(free) for _ in range(free, N)]
    label = [0, *rng.sample(range(1, N), N - 1)]
    edges = [[label[v], label[p]] for v, p in enumerate(parent, 1)]
    for e in edges:
        if rng.random() < 0.5:
            e.reverse()
    rng.shuffle(edges)
    restricted = [label[v] for v in range(free, N)]
    rng.shuffle(restricted)
    return {"n": N, "edges": edges, "restricted": restricted}
