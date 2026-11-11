"""A 2 * 10^4-node caterpillar (a spine of 80% of the nodes) with 2 * 10^4 queries between its two
ends, so walking each path costs ~3 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
Q = 2 * 10**4


def generate(rng):
    spine = N * 4 // 5
    label = list(range(N))
    rng.shuffle(label)
    edges = []
    for i in range(1, N):
        parent = i - 1 if i < spine else rng.randrange(spine)
        edges.append([label[parent], label[i], rng.randint(1, 10**9)])
    rng.shuffle(edges)
    # Spine nodes in the first and last tenth, or the leaves hung on them.
    end = spine // 10
    queries = []
    for _ in range(Q):
        u, v = label[rng.randrange(end)], label[spine - 1 - rng.randrange(end)]
        queries.append([u, v] if rng.getrandbits(1) else [v, u])
    return {"n": N, "edges": edges, "queries": queries}
