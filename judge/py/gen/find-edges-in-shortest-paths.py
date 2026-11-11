"""Find Edges in Shortest Paths with n = 2 * 10^4 and 3.5 * 10^4 edges: one long weighted path
from 0 to n - 1 with short chords that tie, lose or win against it, so a Dijkstra that scans
every node for the next closest is ~4 * 10^8 steps; or a chain of 2.5 * 10^4 nodes whose hub edges
from node 0 get ever longer routes cheaper, so a queue-based Bellman-Ford improves each node once
per hop count, ~3 * 10^8 relaxations."""

from _shapes import pick_shape

SEEDS = 2
N = 2 * 10**4
M = 35 * 10**3
TIES = 8
LONG = 25 * 10**3  # nodes on the chain of the queue-based shape


def chain_with_hub(rng):
    """A chain 0 .. LONG with a hub edge from 0 to each node i >= 2 of weight (chain distance to i)
    + i + 1: the route to node j through the hub edge to i costs j's chain distance + i + 1, so
    the queue sees ever better routes to j, one more hop each round."""
    n = LONG + 1
    order = list(range(1, n - 1))
    rng.shuffle(order)
    order = [0, *order, n - 1]
    w = [rng.randint(1, 3) for _ in range(LONG)]
    edges = [[order[i], order[i + 1], w[i]] for i in range(LONG)]
    dist = 0
    for i in range(1, LONG):
        dist += w[i - 1]
        if i >= 2:
            edges.append([order[0], order[i], dist + i + 1])
    for e in edges:
        if rng.random() < 0.5:
            e[0], e[1] = e[1], e[0]
    rng.shuffle(edges)
    return {"n": n, "edges": edges}


def generate(rng):
    if pick_shape(rng) != 0:
        return chain_with_hub(rng)
    order = list(range(1, N - 1))
    rng.shuffle(order)
    order = [0, *order, N - 1]
    w = [rng.randint(1, 2 * 10**4) for _ in range(N - 1)]
    edges = [[order[i], order[i + 1], w[i]] for i in range(N - 1)]
    seen = {(i, i + 1) for i in range(N - 1)}
    # Disjoint chords, one per short stretch, each shorter than the path or tying it; ties stay
    # few and near node 0, since every tie doubles the shortest paths behind it.
    i, ties = 0, 0
    while i + 2 < N:
        j = min(N - 1, i + rng.randint(2, 4))
        span = sum(w[i:j])
        if ties < TIES and i < N // 50 and rng.random() < 0.5:
            weight, ties = span, ties + 1
        else:
            weight = rng.randint(1, span - 1)
        edges.append([order[i], order[j], weight])
        seen.add((i, j))
        i = j
    # Overlapping chords longer than the path between their ends never lie on a shortest path.
    while len(edges) < M:
        i = rng.randrange(N - 2)
        j = min(N - 1, i + rng.randint(2, 5))
        span = sum(w[i:j])
        if (i, j) not in seen and span + 10 <= 10**5:
            seen.add((i, j))
            edges.append([order[i], order[j], span + rng.randint(1, 10)])
    for e in edges:
        if rng.random() < 0.5:
            e[0], e[1] = e[1], e[0]
    rng.shuffle(edges)
    return {"n": N, "edges": edges}
