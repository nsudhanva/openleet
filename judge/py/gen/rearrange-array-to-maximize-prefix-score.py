"""Rearrange Array to Maximize Prefix Score at n = 5 * 10^4 with nearly every prefix positive, so
summing each prefix afresh costs ~10^9 additions."""

SEEDS = 2
N = 5 * 10**4
LIMIT = 10**6


def generate(rng):
    negative = rng.choice((0.2, 0.55))
    nums = [
        -rng.randint(1, LIMIT) if rng.random() < negative else rng.randint(0, LIMIT)
        for _ in range(N)
    ]
    return {"nums": nums}
