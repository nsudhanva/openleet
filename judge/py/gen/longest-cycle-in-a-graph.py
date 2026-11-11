"""Longest Cycle in a Graph at n = 2 * 10^4 with one cycle through half the nodes and the rest in
trees leading into it, so walking from every node until a repeat costs ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    order = list(range(N))
    rng.shuffle(order)
    edges = [-1] * N
    big = N // 2
    for i in range(big):
        edges[order[i]] = order[(i + 1) % big]
    # A few short cycles, then trees hanging off earlier nodes (or a dead end now and then).
    i = big
    for _ in range(5):
        k = rng.randint(2, 10)
        for t in range(k):
            edges[order[i + t]] = order[i + (t + 1) % k]
        i += k
    for j in range(i, N):
        edges[order[j]] = -1 if rng.random() < 0.01 else order[rng.randrange(j)]
    return {"edges": edges}
