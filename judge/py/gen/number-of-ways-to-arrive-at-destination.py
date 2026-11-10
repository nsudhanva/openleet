"""Ways to Arrive at n = 200: a dense graph with tiny tied weights, or a layered graph whose
shortest-path count explodes past 10^9 + 7 with times near 10^9."""

import itertools

SEEDS = 2
N = 200


def generate(rng):
    nodes = list(range(1, N - 1))
    rng.shuffle(nodes)
    edges = {}
    if rng.random() < 0.5:
        order = [0, *nodes, N - 1]
        for i in range(1, N):
            a, b = order[rng.randrange(i)], order[i]
            edges[(min(a, b), max(a, b))] = rng.randint(1, 3)
        for a in range(N):
            for b in range(a + 1, N):
                if (a, b) not in edges and rng.random() < 0.4:
                    edges[(a, b)] = rng.randint(1, 3)
    else:
        width = 9
        layers = [[0]] + [nodes[i : i + width] for i in range(0, len(nodes), width)] + [[N - 1]]
        w = 10**9
        for la, lb in itertools.pairwise(layers):
            for a in la:
                for b in lb:
                    edges[(min(a, b), max(a, b))] = w
    roads = [[a, b, t] for (a, b), t in edges.items()]
    rng.shuffle(roads)
    return {"n": N, "roads": roads}
