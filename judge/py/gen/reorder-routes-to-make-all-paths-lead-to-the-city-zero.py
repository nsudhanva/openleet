"""Reorder Routes to Make All Paths Lead to the City Zero at n = 5 * 10^4: a long path from city 0
with random directions, its roads listed farthest first, nearest first or shuffled (one seed
each), so sweeping the road list until every city is reached, in either direction, takes
~n / 2 to n sweeps of ~n roads."""

from _shapes import pick_shape

SEEDS = 3
N = 5 * 10**4


def generate(rng):
    shape = pick_shape(rng)
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
    if shape == 1:
        roads.reverse()
    elif shape == 2:
        rng.shuffle(roads)
    return {"n": N, "connections": roads}
