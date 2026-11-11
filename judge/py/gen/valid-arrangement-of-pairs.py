"""Valid Arrangement of Pairs at 2 * 10^4 pairs: one random walk over 300 nodes with no pair
used twice, shuffled, so checking that each next pair keeps the rest reachable (Fleury) is
~4 * 10^8 steps."""

from itertools import pairwise

SEEDS = 2
N = 2 * 10**4
NODES = 300


def generate(rng):
    nodes = rng.sample(range(10**9 + 1), NODES)
    walk, used = [rng.choice(nodes)], set()
    while len(used) < N:
        v = rng.choice(nodes)
        if v != walk[-1] and (walk[-1], v) not in used:
            used.add((walk[-1], v))
            walk.append(v)
    pairs = [[a, b] for a, b in pairwise(walk)]
    rng.shuffle(pairs)
    return {"pairs": pairs}
