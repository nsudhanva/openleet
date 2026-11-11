"""Count Special Triplets at n = 3 * 10^4 values in 0..40 (many doubles), so scanning both sides
of every middle index costs ~10^9 steps."""

SEEDS = 2
N = 3 * 10**4
VALUES = 40


def generate(rng):
    return {"nums": [rng.randint(0, VALUES) for _ in range(N)]}
