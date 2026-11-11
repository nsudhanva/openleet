"""Most Profitable Path in a Tree at n = 2 * 10^4: a path of n / 2 nodes from the root with the
other half hung at random below its end (Bob starts deep in that half), so walking every leaf's
path to the root is ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    half = N // 2
    label = [0, *rng.sample(range(1, N), N - 1)]
    edges = [(v - 1, v) for v in range(1, half)]
    edges += [(rng.randrange(half - 1, v), v) for v in range(half, N)]
    edges = [[label[u], label[v]] for u, v in edges]
    for e in edges:
        if rng.random() < 0.5:
            e.reverse()
    rng.shuffle(edges)
    amount = [2 * rng.randint(-5000, 5000) for _ in range(N)]
    return {"edges": edges, "bob": label[rng.randrange(half, N)], "amount": amount}
