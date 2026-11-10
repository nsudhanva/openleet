"""Max Consecutive Ones at n = 10^5: random bits, or long runs of ones."""

SEEDS = 2
N = 10**5


def generate(rng):
    p = rng.choice([0.5, 0.999])
    return {"nums": [1 if rng.random() < p else 0 for _ in range(N)]}
