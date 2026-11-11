"""Checking Existence of Edge Length Limited Paths at n = edges = queries = 10^4: two long
chains over shuffled nodes on light edges, and queries whose limits mostly let every chain edge
through, so a search per query walks half the graph and is quadratic."""

SEEDS = 2
N = 10**4
LIMIT = 10**9


def generate(rng):
    order = list(range(N))
    rng.shuffle(order)
    split = rng.randint(N // 3, 2 * N // 3)
    edges = []
    for k in range(N - 1):
        if k + 1 != split:
            edges.append([order[k], order[k + 1], rng.randint(1, LIMIT // 2)])
    while len(edges) < N:
        a, b = rng.sample(range(split), 2)
        edges.append([order[a], order[b], rng.randint(LIMIT // 2, LIMIT)])
    rng.shuffle(edges)
    queries = []
    for _ in range(N):
        p, q = rng.sample(range(N), 2)
        low = 1 if rng.random() < 0.3 else LIMIT // 2
        queries.append([p, q, rng.randint(low, LIMIT)])
    return {"n": N, "edgeList": edges, "queries": queries}
