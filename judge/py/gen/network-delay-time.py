"""Network Delay Time at n = 100 with 6000 distinct directed edges, weights in [0, 100];
sometimes a node is unreachable (answer -1)."""

SEEDS = 3
N = 100
EDGES = 6000


def generate(rng):
    pairs = [(u, v) for u in range(1, N + 1) for v in range(1, N + 1) if u != v]
    k = rng.randint(1, N)
    if rng.random() < 0.3:
        cut = rng.choice([v for v in range(1, N + 1) if v != k])
        pairs = [(u, v) for u, v in pairs if v != cut]
    chosen = rng.sample(pairs, EDGES)
    top = rng.choice((100, 3))
    return {"times": [[u, v, rng.randint(0, top)] for u, v in chosen], "n": N, "k": k}
