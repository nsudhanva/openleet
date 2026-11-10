"""Delete and Earn at n = 2 * 10^4 with values across [1, 10^4], so adjacent-value conflicts
chain through the whole range."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        nums = [rng.randint(1, 10**4) for _ in range(N)]
    else:
        nums = [rng.randint(9000, 10**4) for _ in range(N)]
    return {"nums": nums}
