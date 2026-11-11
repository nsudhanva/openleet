"""nums of 5 * 10^4 drawn from 3 * 10^4 values with skewed frequencies, windows of about half the
array holding ~1.5 * 10^4 distinct values and x near 10^4, so summing the top x of each of the
~2.5 * 10^4 windows costs ~2.5 * 10^8 steps and recounting them far more."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    pool = rng.sample(range(1, 10**9 + 1), 30000)
    # Weight 1 / sqrt(rank) keeps some values common and many rare, so the top x keeps changing.
    weights = [1 / (r + 1) ** 0.5 for r in range(len(pool))]
    nums = rng.choices(pool, weights, k=N)
    k = rng.randint(N // 2 - 1000, N // 2 + 1000)
    x = rng.randint(8000, 11000)
    return {"nums": nums, "k": k, "x": x}
