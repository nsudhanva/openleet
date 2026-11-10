"""Reachable Nodes in Subdivided Graph with n = 3000 and 10^4 unique edges, each subdivided up
to 10^4 times, so expanding the subdivided graph explicitly is far too large."""

import itertools

SEEDS = 2
N = 3000
M = 10**4


def generate(rng):
    pairs = set()
    # A spanning chain first so most of the graph is reachable, then random extras.
    order = list(range(N))
    rng.shuffle(order)
    for a, b in itertools.pairwise(order):
        pairs.add((min(a, b), max(a, b)))
    while len(pairs) < M:
        a, b = rng.randrange(N), rng.randrange(N)
        if a != b:
            pairs.add((min(a, b), max(a, b)))
    edges = [[a, b, rng.randint(0, 10**4)] for a, b in sorted(pairs)]
    rng.shuffle(edges)
    max_moves = rng.choice([rng.randint(10**4, 10**6), rng.randint(10**8, 10**9)])
    return {"edges": edges, "maxMoves": max_moves, "n": N}
