"""Second Minimum Time at n = 10^4 with 2 * 10^4 edges: a long path with sparse shortcuts (deep
BFS), or a random connected graph."""

SEEDS = 3


def generate(rng):
    n = 10**4
    m = 2 * 10**4
    edges, seen = [], set()

    def add(u, v):
        key = (min(u, v), max(u, v))
        if u != v and key not in seen:
            seen.add(key)
            edges.append([u, v])

    order = list(range(1, n + 1))
    if rng.random() < 0.5:
        # Long path 1 .. n in shuffled order with local shortcuts.
        rng.shuffle(order)
        order.remove(1)
        order.remove(n)
        order = [1, *order, n]
        for i in range(n - 1):
            add(order[i], order[i + 1])
        target = rng.randint(n, m)
        while len(edges) < target:
            i = rng.randrange(n)
            j = min(n - 1, i + rng.randint(2, 5))
            add(order[i], order[j])
    else:
        for i in range(2, n + 1):
            add(i, rng.randint(1, i - 1))
        while len(edges) < m:
            add(rng.randint(1, n), rng.randint(1, n))
    rng.shuffle(edges)
    return {"n": n, "edges": edges, "time": rng.randint(1, 1000), "change": rng.randint(1, 1000)}
