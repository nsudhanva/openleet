"""Minimum Operations to Make the Array Increasing at n = 5000 (the limit) with values sorted
descending, so the answer is ~3.5 * 10^7 and raising each element one step at a time does that
many increments."""

SEEDS = 2
N = 5000
LIMIT = 10**4


def generate(rng):
    return {"nums": sorted((rng.randint(1, LIMIT) for _ in range(N)), reverse=True)}
