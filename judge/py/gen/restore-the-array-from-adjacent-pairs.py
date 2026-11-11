"""Restore the Array From Adjacent Pairs at n = 10^4 distinct values with the pairs shuffled, so
searching the pair list for each next neighbour costs ~5 * 10^7 steps."""

from itertools import pairwise

SEEDS = 2
N = 10**4


def generate(rng):
    nums = rng.sample(range(-(10**5), 10**5 + 1), N)
    pairs = [[a, b] if rng.random() < 0.5 else [b, a] for a, b in pairwise(nums)]
    rng.shuffle(pairs)
    return {"adjacentPairs": pairs}
