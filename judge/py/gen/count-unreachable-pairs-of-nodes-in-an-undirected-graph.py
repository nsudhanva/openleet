"""Count Unreachable Pairs at n = 5 * 10^4: two stars of 1.2 * 10^4 nodes, one listing its edges
hub first and one hub last, and ~1.6 * 10^4 tiny components, so checking every pair of components
or linking roots without path compression or union by size costs ~10^8 steps."""

SEEDS = 2
N = 5 * 10**4
STAR = 12000


def generate(rng):
    order = list(range(N))
    rng.shuffle(order)
    # Whichever way a naive union-find links the two roots, one of the stars becomes a chain.
    a, b = order[:STAR], order[STAR : 2 * STAR]
    edges = [[a[0], x] for x in a[1:]] + [[x, b[0]] for x in b[1:]]
    start = 2 * STAR
    while start < N:
        size = min(N - start, rng.choice((1, 1, 1, 2, 3)))
        comp = order[start : start + size]
        edges += [[comp[rng.randrange(i)], comp[i]] for i in range(1, size)]
        start += size
    rng.shuffle(edges)
    return {"n": N, "edges": edges}
