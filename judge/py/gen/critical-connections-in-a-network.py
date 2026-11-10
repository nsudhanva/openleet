"""Critical Connections on a connected graph with up to 10^5 nodes and 10^5 edges: a single
10^5-long path plus one chord (deep DFS), or a random tree with extra local edges mixing
bridges and cycles."""

SEEDS = 2
E = 10**5


def generate(rng):
    if rng.random() < 0.5:
        n = 10**5
        order = list(range(n))
        rng.shuffle(order)
        edges = [(order[i], order[i + 1]) for i in range(n - 1)]
        i = rng.randrange(n - 10)
        edges.append((order[i], order[rng.randrange(i + 2, n)]))
    else:
        n = 5 * 10**4
        seen = set()
        edges = []
        for v in range(1, n):
            p = rng.randrange(max(0, v - 5), v)
            edges.append((p, v))
            seen.add((p, v))
        while len(edges) < E:
            a = rng.randrange(n)
            b = a + rng.randint(1, 30)
            if b < n and (a, b) not in seen:
                seen.add((a, b))
                edges.append((a, b))
        perm = list(range(n))
        rng.shuffle(perm)
        edges = [(perm[a], perm[b]) for a, b in edges]
    connections = [[a, b] if rng.random() < 0.5 else [b, a] for a, b in edges]
    rng.shuffle(connections)
    return {"n": n, "connections": connections}
