"""Find Edges in Shortest Paths with n = 2 * 10^4 and 3.5 * 10^4 edges: one long weighted path
from 0 to n - 1 with short chords that tie, lose or win against it, so a Dijkstra that scans
every node for the next closest is ~4 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
M = 35 * 10**3
TIES = 8


def generate(rng):
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
