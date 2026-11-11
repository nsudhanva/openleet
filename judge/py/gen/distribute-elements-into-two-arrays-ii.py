"""Distribute Elements Into Two Arrays II at n = 10^5, so counting the greater elements of
both arrays by a scan for every number is ~2.5 * 10^9 comparisons."""

SEEDS = 2
N = 10**5


def generate(rng):
    top = rng.choice([10**8, N // 4])
    return {"nums": [rng.randint(1, top) for _ in range(N)]}
