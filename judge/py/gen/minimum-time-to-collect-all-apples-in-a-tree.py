"""Collect All Apples in a Tree at n = 2 * 10^4: a path of n / 2 nodes from the root with the
other half hung at random below its end, every node there holding an apple, so walking each
apple's path to the root is ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    half = N // 2
    label = [0, *rng.sample(range(1, N), N - 1)]
    edges = [(v - 1, v) for v in range(1, half)]
    edges += [(rng.randrange(half - 1, v), v) for v in range(half, N)]
    edges = [sorted((label[u], label[v])) for u, v in edges]
    rng.shuffle(edges)
    apple = [False] * N
    for v in range(half, N):
        apple[label[v]] = rng.random() < 0.9
    return {"n": N, "edges": edges, "hasApple": apple}
