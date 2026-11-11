"""Minimum Cost Walk in Weighted Graph with 2 * 10^4 nodes, edges and queries: one giant component
whose spanning path comes first in path order, so union-find without balancing builds a deep
tree, and a search or edge scan per query walks the whole graph each time."""

SEEDS = 2
N = 2 * 10**4
EDGES = 2 * 10**4
QUERIES = 2 * 10**4


def generate(rng):
    nodes = list(range(N))
    rng.shuffle(nodes)
    main, rest = nodes[:-40], nodes[-40:]
    # Every weight (below 2^16 <= 10^5) keeps the bits of `keep`, so the AND is not simply 0.
    keep = rng.getrandbits(16) & rng.getrandbits(16)

    def weight():
        return keep | rng.getrandbits(16)

    # The path is listed in path order with each edge's ends in random order, so linking one root
    # under the other without rank or path compression makes a deep tree whichever way it links.
    edges = []
    for i in range(len(main) - 1):
        u, v = main[i], main[i + 1]
        edges.append([u, v, weight()] if rng.random() < 0.5 else [v, u, weight()])
    for i in range(0, len(rest), 2):
        edges.append([rest[i], rest[i + 1], weight()])
    while len(edges) < EDGES:
        u, v = rng.sample(main, 2)
        edges.append([u, v, weight()])
    query = []
    for _ in range(QUERIES):
        pool = rest if rng.random() < 0.02 else main
        s, t = rng.choice(main), rng.choice(pool)
        while s == t:
            t = rng.choice(pool)
        query.append([s, t])
    return {"n": N, "edges": edges, "query": query}
