"""Allocate Mailboxes at the maximum 100 distinct houses, unsorted, with k anywhere in 1..100
so the interval DP runs at full size."""

SEEDS = 3


def generate(rng):
    houses = rng.sample(range(1, 10**4 + 1), 100)
    k = rng.choice([1, rng.randint(2, 99), 100, rng.randint(2, 10)])
    return {"houses": houses, "k": k}
