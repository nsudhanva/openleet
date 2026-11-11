"""Minimum Cost Path With Edge Reversals with 10^4 nodes: a random 3 * 10^4-edge graph whose node
n - 1 is entered only by weight-1000 edges, or a weight-1 chain to n - 1 fed by a hub fan that
makes a FIFO label-correcting search improve the chain one node per round; a Dijkstra that scans
for its next node is quadratic on both."""

from _shapes import pick_shape

SEEDS = 3
N = 10**4
M = 3 * 10**4
LIMIT = 1000


def random_graph(rng):
    order = list(range(N - 1))
    rng.shuffle(order)
    edges = []
    for i in range(1, N - 1):
        u, v = order[i], order[rng.randrange(i)]
        if rng.random() < 0.5:
            u, v = v, u
        edges.append([u, v, rng.randint(1, LIMIT)])
    for _ in range(5):
        edges.append([rng.randrange(N - 1), N - 1, LIMIT])
    while len(edges) < M:
        u, v = rng.sample(range(N - 1), 2)
        edges.append([u, v, rng.randint(1, LIMIT)])
    rng.shuffle(edges)
    return edges


def anti_spfa(rng):
    # A chain v_0 -> ... -> v_{L-1} = n - 1 of weight-1 edges, and a path of hubs from node 0 whose
    # hub t reaches v_j directly at total cost base + 2j: one hop costs more than walking the
    # chain, and each hub lists its chain edges from the far end.
    chain_len = N - 1 - (2 * N // LIMIT + 3)
    ids = list(range(1, N - 1))
    rng.shuffle(ids)
    hubs = [0, *ids[: N - 1 - chain_len]]
    chain = [*ids[N - 1 - chain_len :], N - 1]
    edges = [[hubs[t], hubs[t + 1], LIMIT] for t in range(len(hubs) - 1)]
    fan = [[] for _ in hubs]
    base = rng.randint(1, max(1, LIMIT // 20))
    for j in range(chain_len):
        c = base + 2 * j
        t = (c - 1) // LIMIT
        fan[t].append([hubs[t], chain[j], c - LIMIT * t])
    for spokes in fan:
        edges += spokes[::-1]
    edges += [[chain[j], chain[j + 1], 1] for j in range(chain_len - 1)]
    return edges


def generate(rng):
    edges = random_graph(rng) if pick_shape(rng) == 0 else anti_spfa(rng)
    return {"n": N, "edges": edges}
