"""Minimum Weighted Subgraph at n = 3000 nodes and 9000 random directed edges (a cycle through
every node keeps all of them connected), so running a shortest-path search from every candidate
meeting node is ~3000 Dijkstras."""

SEEDS = 2
N = 3000
M = 9000


def generate(rng):
    order = rng.sample(range(N), N)
    edges = [[order[i], order[(i + 1) % N], rng.randint(1, 10**5)] for i in range(N)]
    while len(edges) < M:
        u, v = rng.sample(range(N), 2)
        edges.append([u, v, rng.randint(1, 10**5)])
    rng.shuffle(edges)
    src1, src2, dest = rng.sample(range(N), 3)
    return {"n": N, "edges": edges, "src1": src1, "src2": src2, "dest": dest}
