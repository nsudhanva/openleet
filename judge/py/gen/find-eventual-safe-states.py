"""Find Eventual Safe States with n = 10^4 and 4 * 10^4 edges: long forward chains feeding into a
few cycles, so the reachability of the cycles decides most nodes."""

import itertools

SEEDS = 3
N = 10**4
EDGES = 4 * 10**4


def generate(rng):
    edges = set()
    # A path through every node in random order gives deep DFS paths.
    order = list(range(N))
    rng.shuffle(order)
    for a, b in itertools.pairwise(order):
        edges.add((a, b))
    back = rng.choice([1, 20, 2000])
    for _ in range(back):
        i = rng.randrange(N)
        j = rng.randrange(i + 1)
        edges.add((order[i], order[j]))
    while len(edges) < EDGES:
        i = rng.randrange(N)
        j = rng.randrange(i, N)
        edges.add((order[i], order[j]))
    graph = [[] for _ in range(N)]
    for a, b in edges:
        graph[a].append(b)
    for row in graph:
        row.sort()
    return {"graph": graph}
