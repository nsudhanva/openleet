"""Arrays of length 10^4 with values in [1, 10^5]: random, or strictly increasing so the
maximum to the right changes at every step."""

SEEDS = 2
N = 10**4


def generate(rng):
    if rng.random() < 0.5:
        return {"arr": sorted(rng.sample(range(1, 10**5 + 1), N))}
    return {"arr": [rng.randint(1, 10**5) for _ in range(N)]}
