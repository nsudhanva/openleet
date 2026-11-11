"""Reorder Routes to Make All Paths Lead to the City Zero at n = 10^4: a long path from city 0
with random directions, roads listed farthest first, so sweeping the road list until every city
is reached takes ~n sweeps."""

SEEDS = 2
N = 10**4


def generate(rng):
    path = int(N * rng.choice((0.9, 1.0)))
    parent = [-1] + [v - 1 for v in range(1, path)] + [rng.randrange(v) for v in range(path, N)]
    depth = [0] * N
    for v in range(1, N):
        depth[v] = depth[parent[v]] + 1
    label = [0, *rng.sample(range(1, N), N - 1)]
    roads = []
    for v in sorted(range(1, N), key=lambda v: -depth[v]):
        a, b = label[v], label[parent[v]]
        roads.append([a, b] if rng.random() < 0.5 else [b, a])
    return {"n": N, "connections": roads}
