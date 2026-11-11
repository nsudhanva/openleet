"""Largest Color Value in a Directed Graph at n = 8000 and m = 10^4: a DAG on a shuffled
Hamiltonian path, coloured from 3 or 26 letters, so a cycle search or colour DP redone from every
start node costs ~7 * 10^7 edge visits."""

from string import ascii_lowercase

from _shapes import pick_shape

SEEDS = 2
N = 8000
M = 10**4


def generate(rng):
    alpha = ascii_lowercase[: 3 if pick_shape(rng) == 0 else 26]
    order = list(range(N))
    rng.shuffle(order)
    edges = {(order[i], order[i + 1]) for i in range(N - 1)}
    while len(edges) < M:
        i, j = sorted(rng.sample(range(N), 2))
        edges.add((order[i], order[j]))
    edges = [list(e) for e in edges]
    rng.shuffle(edges)
    colors = "".join(rng.choice(alpha) for _ in range(N))
    return {"colors": colors, "edges": edges}
