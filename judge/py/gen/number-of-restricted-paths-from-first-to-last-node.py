"""Number of Restricted Paths From First to Last Node on a 141 by 141 grid graph (~2 * 10^4 nodes,
~4 * 10^4 edges with a few random extra ones) between opposite corners, so a Dijkstra that scans
every node for the nearest one costs ~4 * 10^8 steps."""

SEEDS = 2
SIDE = 141
EXTRA = 500


def generate(rng):
    n = SIDE * SIDE
    ids = [1, *rng.sample(range(2, n), n - 2), n]
    seen, edges = set(), []

    def add(u, v):
        a, b = ids[u], ids[v]
        if a != b and (min(a, b), max(a, b)) not in seen:
            seen.add((min(a, b), max(a, b)))
            edges.append(
                [a, b, rng.randint(1, 10**5)]
                if rng.random() < 0.5
                else [b, a, rng.randint(1, 10**5)]
            )

    for r in range(SIDE):
        for c in range(SIDE):
            u = r * SIDE + c
            if c + 1 < SIDE:
                add(u, u + 1)
            if r + 1 < SIDE:
                add(u, u + SIDE)
    while len(edges) < 2 * SIDE * (SIDE - 1) + EXTRA:
        add(rng.randrange(n), rng.randrange(n))
    rng.shuffle(edges)
    return {"n": n, "edges": edges}
