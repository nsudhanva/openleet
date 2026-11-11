"""All Divisions With the Highest Score at n = 10^5 random bits, so counting both sides afresh
at every division is ~10^10 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    p = rng.choice([0.5, 0.3])
    return {"nums": [int(rng.random() < p) for _ in range(N)]}
