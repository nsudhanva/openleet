"""Minimize the Maximum Edge Weight of Graph with 10^4 nodes and 2 * 10^4 distinct-weight edges,
one node leaving only by the median-weight edge, so a search per candidate weight is quadratic
from either end."""

SEEDS = 2
N = 10**4
M = 2 * 10**4
LIMIT = 10**6


def generate(rng):
    order = list(range(1, N))
    rng.shuffle(order)
    order = [0, *order]
    weights = sorted(rng.sample(range(1, LIMIT + 1), M))
    low, answer, high = weights[: M // 2], weights[M // 2], weights[M // 2 + 1 :]
    rng.shuffle(low)
    # Each node points to an earlier one by a lower-half weight, so all but the last reach node 0
    # cheaply; the last node's only way out carries the median weight, which is the answer.
    edges = [[order[i], order[rng.randrange(i)], low[i - 1]] for i in range(1, N - 1)]
    last = order[-1]
    edges.append([last, order[rng.randrange(N - 1)], answer])
    pool = low[N - 2 :] + high
    rng.shuffle(pool)
    for w in pool:
        u, v = rng.sample(range(N), 2)
        while u == last:
            u, v = rng.sample(range(N), 2)
        edges.append([u, v, w])
    rng.shuffle(edges)
    return {"n": N, "edges": edges, "threshold": 1}
