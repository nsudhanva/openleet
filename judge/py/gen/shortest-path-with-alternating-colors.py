"""Alternating Colors at n = 100 with 400 red and 400 blue edges (some self-edges and parallel
edges, which the statement allows), or a long alternating chain."""

SEEDS = 3


def generate(rng):
    n = 100
    if rng.random() < 0.4:
        order = list(range(1, n))
        rng.shuffle(order)
        order = [0, *order]
        red, blue = [], []
        for i in range(n - 1):
            (red if i % 2 == 0 else blue).append([order[i], order[i + 1]])
        while len(red) < 400:
            red.append([rng.randrange(n), rng.randrange(n)])
        while len(blue) < 400:
            blue.append([rng.randrange(n), rng.randrange(n)])
        rng.shuffle(red)
        rng.shuffle(blue)
        return {"n": n, "redEdges": red, "blueEdges": blue}
    red = [[rng.randrange(n), rng.randrange(n)] for _ in range(400)]
    blue = [[rng.randrange(n), rng.randrange(n)] for _ in range(400)]
    return {"n": n, "redEdges": red, "blueEdges": blue}
