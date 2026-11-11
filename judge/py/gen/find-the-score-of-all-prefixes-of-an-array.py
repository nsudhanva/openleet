"""nums of 5 * 10^4 values rising on average, so recomputing each prefix's maximum and
conversion sum from scratch costs ~1.25 * 10^9 steps."""

SEEDS = 2
N = 5 * 10**4
LIMIT = 10**9


def generate(rng):
    # A noisy rise keeps the running maximum changing.
    step = LIMIT // N
    return {
        "nums": [
            min(LIMIT, max(1, i * step + rng.randint(-50 * step, 50 * step))) for i in range(N)
        ]
    }
