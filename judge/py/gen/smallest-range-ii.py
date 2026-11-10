"""Smallest Range II on 10^4 values in [0, 10^4] with k from 0 to 10^4 (punishes trying every
subset or every split with an inner scan)."""

SEEDS = 3


def generate(rng):
    nums = [rng.randint(0, 10**4) for _ in range(10**4)]
    k = rng.choice([0, rng.randint(1, 3000), 10**4])
    return {"nums": nums, "k": k}
