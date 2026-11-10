"""Cat and Mouse on the maximum 50-node undirected graph, dense or sparse, where every node has
a non-hole neighbour so both players can always move."""

SEEDS = 3
N = 50


def generate(rng):
    p = rng.choice([0.05, 0.15, 0.5])
    adj = [set() for _ in range(N)]

    def link(a, b):
        adj[a].add(b)
        adj[b].add(a)

    ring = list(range(1, N))
    rng.shuffle(ring)
    for i in range(len(ring)):  # a cycle over 1..49: every non-hole node has two non-hole moves
        link(ring[i], ring[(i + 1) % len(ring)])
    for a in range(N):
        for b in range(a + 1, N):
            if rng.random() < p:
                link(a, b)
    if not adj[0]:
        link(0, rng.randrange(3, N))
    graph = []
    for a in range(N):
        out = sorted(adj[a])
        rng.shuffle(out)
        graph.append(out)
    return {"graph": graph}
