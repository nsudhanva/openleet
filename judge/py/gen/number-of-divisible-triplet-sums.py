"""Number of Divisible Triplet Sums at the maximum 1,000 values with a divisor in the hundreds, so
checking every triplet costs ~1.7 * 10^8 steps."""

SEEDS = 2
N = 1000


def generate(rng):
    d = rng.randint(50, 500)
    return {"nums": [rng.randint(1, 10**9) for _ in range(N)], "d": d}
