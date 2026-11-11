"""Maximum Length of Semi-Decreasing Subarrays at n = 2 * 10^4: a rising line with small noise,
so only nearby pairs qualify and checking every pair of ends is 2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
STEP = 5 * 10**4
LIMIT = 10**9


def generate(rng):
    noise = rng.randint(STEP, 3 * STEP)
    start = -LIMIT + noise
    return {"nums": [start + STEP * i + rng.randint(-noise, noise) for i in range(N)]}
