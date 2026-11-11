"""Pseudo-Palindromic Paths at 10^5 nodes shaped as a caterpillar: a 5 * 10^4-node spine
with a leaf hanging off each node, so recounting each root-to-leaf path does ~10^9 steps."""

from _shapes import level_order

SEEDS = 2
N = 10**5


def generate(rng):
    # Spine nodes are 0, 2, 4, ...; node 2i + 1 is the leaf beside spine node 2i.
    left, right = [None] * N, [None] * N
    for v in range(0, N - 2, 2):
        kids = [v + 1, v + 2]
        rng.shuffle(kids)
        left[v], right[v] = kids
    vals = [rng.randint(1, 9) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
