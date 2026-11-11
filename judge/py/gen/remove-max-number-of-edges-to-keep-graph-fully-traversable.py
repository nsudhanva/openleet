"""Remove Max Number of Edges to Keep Graph Fully Traversable at n = 10^4 and ~3 * 10^4 edges, so
a connectivity search per edge costs ~10^9 steps."""

SEEDS = 2
N = 10**4


def generate(rng):
    edges = set()
    shared = rng.randint(N // 4, N // 2)
    # Shared edges join nodes 1..shared (half as a star on node 1); Alice and Bob each join the
    # remaining nodes with their own random tree. Random extra edges of every type follow.
    for v in range(2, shared + 1):
        edges.add((3, 1, v) if v <= shared // 2 else (3, rng.randint(1, v - 1), v))
    for t in (1, 2):
        for v in range(shared + 1, N + 1):
            edges.add((t, rng.randint(1, v - 1), v))
    while len(edges) < 3 * N:
        u, v = sorted(rng.sample(range(1, N + 1), 2))
        edges.add((rng.randint(1, 3), u, v))
    out = [list(e) for e in sorted(edges)]
    rng.shuffle(out)
    return {"n": N, "edges": out}
