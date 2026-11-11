"""Minimum Weighted Subgraph: two seeds are random graphs of 3000 nodes and 9000 edges (a cycle
through every node keeps all of them connected), so a shortest-path search from every candidate
meeting node is ~3000 Dijkstras; one seed is a 7 * 10^4-node, ~10^5-edge graph in which 2.4 * 10^4
feeders improve a hub one after another, each improvement running down a 2.4 * 10^4-node tail,
~6 * 10^8 relaxations for a queue-based Bellman-Ford (SPFA) against ~10^5 for Dijkstra."""

from _shapes import pick_shape

SEEDS = 3
N = 3000
M = 9000
L = 24000  # feeders of the hub
TAIL = 24000  # nodes hanging off the hub


def _random_graph(rng):
    order = rng.sample(range(N), N)
    edges = [[order[i], order[(i + 1) % N], rng.randint(1, 10**5)] for i in range(N)]
    while len(edges) < M:
        u, v = rng.sample(range(N), 2)
        edges.append([u, v, rng.randint(1, 10**5)])
    rng.shuffle(edges)
    src1, src2, dest = rng.sample(range(N), 3)
    return {"n": N, "edges": edges, "src1": src1, "src2": src2, "dest": dest}


def _hub_graph(rng):
    # src -> g[0] -> ... -> g[L-1], each g[i] -> q[i] -> hub with weights that make the route
    # through q[i] one shorter than through q[i-1], but only learnt one queue round later; the hub
    # then leads down a tail, so a FIFO relaxation sends every improvement down the whole tail.
    # Labels: 0 src, 1 src2, 2 hub, then g, q, tail.
    g, q, tail = 3, 3 + L, 3 + 2 * L
    n = tail + TAIL
    edges = [[1, 0, 1], [0, g, 1], [2, tail, 1]]
    for i in range(L):
        if i + 1 < L:
            edges.append([g + i, g + i + 1, 1])
        edges.append([g + i, q + i, 1])
        edges.append([q + i, 2, 2 * (L - i) - 1])
    edges += [[tail + i, tail + i + 1, 1] for i in range(TAIL - 1)]
    label = rng.sample(range(n), n)
    edges = [[label[u], label[v], w] for u, v, w in edges]
    return {"n": n, "edges": edges, "src1": label[0], "src2": label[1], "dest": label[n - 1]}


def generate(rng):
    return _hub_graph(rng) if pick_shape(rng) == 1 else _random_graph(rng)
